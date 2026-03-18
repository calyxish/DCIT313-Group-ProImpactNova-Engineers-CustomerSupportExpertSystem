import os
import re
import sys
from pathlib import Path
from typing import Dict, List

try:
    from pyswip import Prolog
except ImportError as exc:
    raise SystemExit(
        "pyswip is not installed. Run: pip install pyswip"
    ) from exc


# ---------------------------------------------------------------------------
# Paths and engine setup
# ---------------------------------------------------------------------------

def clear_screen() -> None:
    """Clears the terminal screen."""
    os.system("cls" if os.name == "nt" else "clear")


def project_root() -> Path:
    """Gets the project's root directory."""
    return Path(__file__).resolve().parents[1]


def knowledge_base_path() -> Path:
    """Gets the full path to the knowledge base file."""
    return project_root() / "knowledge_base" / "customer_support.pl"


def load_engine() -> Prolog:
    """Loads the Prolog engine and consults the knowledge base."""
    kb_path = knowledge_base_path()
    if not kb_path.exists():
        raise SystemExit(f"Knowledge base file not found: {kb_path}")

    engine = Prolog()
    try:
        engine.consult(str(kb_path))
    except Exception as e:
        raise SystemExit(f"Failed to consult knowledge base: {e}") from e
    return engine


# ---------------------------------------------------------------------------
# Knowledge base queries
# ---------------------------------------------------------------------------

def get_issues(engine: Prolog) -> List[str]:
    """Fetches all unique issue categories from the knowledge base."""
    try:
        issues = [row["Issue"] for row in engine.query("list_issue(Issue)")]
        unique_issues = sorted(set(issues))
        return unique_issues
    except Exception as e:
        print(f"Error querying issues: {e}", file=sys.stderr)
        return []


def solve_by_issue(engine: Prolog, issue: str) -> str:
    """Resolves an issue by its category name."""
    query = f"resolve_issue({issue}, Message)"
    try:
        result = list(engine.query(query, maxresult=1))
        if not result:
            return (
                "No recommendation found for this issue. "
                "Please try describing your problem or escalate to human support."
            )
        return result[0]["Message"]
    except Exception as e:
        return f"An error occurred during inference: {e}"


def solve_by_text(engine: Prolog, raw_text: str) -> str:
    """Finds a recommendation based on keywords in free text."""
    normalized = normalize_text(raw_text)
    if not normalized:
        return ""   # caller handles the empty-after-norm case

    query = f"recommendation({normalized}, Message)"
    try:
        result = list(engine.query(query, maxresult=1))
        if not result:
            return ""   # signal to caller: no match found
        return result[0]["Message"]
    except Exception as e:
        return f"An error occurred during inference: {e}"


# ---------------------------------------------------------------------------
# Text helpers
# ---------------------------------------------------------------------------

def atom_to_label(atom_name: str) -> str:
    """Converts a Prolog atom string to a human-readable label."""
    return atom_name.replace("_", " ").title()


def normalize_text(text: str) -> str:
    """
    Normalizes user free text to a Prolog-compatible atom.

    Steps:
      - Lower-case everything.
      - Strip apostrophes.
      - Replace hyphens and slashes with a single space.
      - Collapse any run of whitespace (including multiple spaces) to one space.
      - Strip leading/trailing whitespace.
      - Replace spaces with underscores.
    """
    normalized = (
        text.lower()
        .replace("'", "")
        .replace("-", " ")
        .replace("/", " ")
    )
    normalized = re.sub(r"\s+", " ", normalized).strip()
    return normalized.replace(" ", "_")


# ---------------------------------------------------------------------------
# UI helpers
# ---------------------------------------------------------------------------

def render_menu(issues: List[str]) -> Dict[str, str]:
    """
    Displays the main menu and returns a map of valid choices to issue atoms.
    Also prints the total number of categories available.
    """
    option_map: Dict[str, str] = {}
    print("=" * 46)
    print("    Customer Support Expert System")
    print("=" * 46)
    print(f"  {len(issues)} issue categories available.\n")
    print("  Select a category or describe your problem.")
    print("-" * 46)

    for index, issue in enumerate(issues, start=1):
        key = str(index)
        option_map[key] = issue
        print(f"  {key:>2}. {atom_to_label(issue)}")

    text_option = str(len(issues) + 1)
    exit_option = str(len(issues) + 2)
    option_map[text_option] = "__free_text__"
    option_map[exit_option] = "__exit__"

    print(f"  {text_option:>2}. Enter a free-text complaint")
    print(f"  {exit_option:>2}. Exit")
    print("-" * 46)
    return option_map


def get_user_choice(prompt: str, valid_options: List[str], hint: str = "") -> str:
    """
    Prompts the user and validates their input against a list of valid options.

    Args:
        prompt:        The text shown to the user.
        valid_options: Accepted answer strings (case-insensitive comparison).
        hint:          Optional human-readable hint shown on invalid input.
                       If empty, a sensible default is generated.
    """
    if not hint:
        # Build a clean display e.g. "yes / no" instead of a Python list
        display = " / ".join(dict.fromkeys(valid_options))   # preserves order, deduplicates
        hint = f"Please enter: {display}"

    while True:
        choice = input(prompt).strip().lower()
        if choice in valid_options:
            return choice
        print(f"  ⚠  Invalid input. {hint}\n")


def prompt_free_text() -> str:
    """
    Asks the user to describe their issue and enforces a minimum length of
    3 characters so that trivially short inputs don't reach the Prolog engine.

    Returns:
        A non-empty string of at least 3 characters, or "__back__" if the
        user explicitly types 'back' to return to the main menu.
    """
    print("\n  Type 'back' at any time to return to the main menu.")
    while True:
        complaint = input("  Describe your issue: ").strip()

        if complaint.lower() == "back":
            return "__back__"

        if len(complaint) < 3:
            print("  ⚠  Please enter at least 3 characters so we can understand your issue.\n")
            continue

        return complaint


# ---------------------------------------------------------------------------
# Main application loop
# ---------------------------------------------------------------------------

def main() -> None:
    """
    Main application loop for the Customer Support Expert System CLI.

    Flow per session:
      1. Load Prolog engine and issue list.
      2. Show the numbered issue menu.
      3. Validate the user's menu choice using get_user_choice().
      4. For a category selection:
           a. Confirm the selected category name.
           b. Fetch and display the recommendation.
      5. For free-text entry:
           a. Enforce minimum-length validation.
           b. Query Prolog for a match.
           c. If no match: offer the user one retry opportunity.
           d. Display the recommendation or escalation message.
      6. Ask the follow-up prompt (another question?).
      7. On exit: print a session summary with the query count.
    """
    try:
        engine = load_engine()
        issues = get_issues(engine)
    except SystemExit as e:
        print(f"Fatal Error: {e}", file=sys.stderr)
        return

    if not issues:
        print(
            "Could not load any issues from the knowledge base. Exiting.",
            file=sys.stderr,
        )
        return

    clear_screen()
    print("\n  Welcome to the ProImpactNova Customer Support Expert System!\n")

    query_count = 0   # session counter

    while True:
        # ── Build and show menu ────────────────────────────────────────────
        option_map = render_menu(issues)
        valid_keys = list(option_map.keys())

        # ── Validated menu selection ───────────────────────────────────────
        hint = f"Enter a number between 1 and {valid_keys[-1]}"
        choice = get_user_choice("\n  Choose an option: ", valid_keys, hint=hint)

        selected = option_map[choice]

        if selected == "__exit__":
            break

        clear_screen()

        # ── Free-text path ─────────────────────────────────────────────────
        if selected == "__free_text__":
            complaint = prompt_free_text()

            if complaint == "__back__":
                clear_screen()
                continue

            recommendation = solve_by_text(engine, complaint)

            # No match on first try — offer one retry
            if not recommendation:
                print(
                    "\n  ℹ  We couldn't find a match for your description. "
                    "Try rephrasing with different keywords.\n"
                )
                retry = get_user_choice(
                    "  Would you like to rephrase? (yes / no): ",
                    ["yes", "no", "y", "n"],
                    hint="Please enter yes or no",
                )
                if retry in ("yes", "y"):
                    complaint = prompt_free_text()
                    if complaint == "__back__":
                        clear_screen()
                        continue
                    recommendation = solve_by_text(engine, complaint)

            # Still no match after retry (or user declined) → escalation message
            if not recommendation:
                recommendation = (
                    "We could not identify your issue automatically. "
                    "Please escalate to a human support agent with your details and any screenshots."
                )

        # ── Category-selection path ────────────────────────────────────────
        else:
            label = atom_to_label(selected)
            print(f"  ✔  You selected: {label}\n")
            recommendation = solve_by_issue(engine, selected)

        # ── Display recommendation ─────────────────────────────────────────
        query_count += 1
        print(f"  📋 Recommendation:\n  {recommendation}\n")

        # ── Follow-up prompt ───────────────────────────────────────────────
        again = get_user_choice(
            "  Do you have another question? (yes / no): ",
            ["yes", "no", "y", "n"],
            hint="Please enter yes or no",
        )
        if again in ("no", "n"):
            break

        clear_screen()

    # ── Session goodbye ────────────────────────────────────────────────────
    question_word = "question" if query_count == 1 else "questions"
    print(
        f"\n  You asked {query_count} {question_word} this session.\n"
        "  Thank you for using the ProImpactNova Expert System. Goodbye!\n"
    )


if __name__ == "__main__":
    main()
