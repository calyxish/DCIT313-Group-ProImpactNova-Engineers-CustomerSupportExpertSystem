from __future__ import annotations

from pathlib import Path
from typing import Dict, List

try:
    from pyswip import Prolog
except ImportError as exc:
    raise SystemExit(
        "pyswip is not installed. Run: pip install pyswip"
    ) from exc


def project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def knowledge_base_path() -> Path:
    return project_root() / "knowledge_base" / "customer_support.pl"


def atom_to_label(atom_name: str) -> str:
    return atom_name.replace("_", " ").title()


def load_engine() -> Prolog:
    kb_path = knowledge_base_path()
    if not kb_path.exists():
        raise SystemExit(f"Knowledge base file not found: {kb_path}")

    engine = Prolog()
    engine.consult(str(kb_path))
    return engine


def get_issues(engine: Prolog) -> List[str]:
    issues = [row["Issue"] for row in engine.query("list_issue(Issue)")]
    unique_issues = sorted(set(issues))
    return unique_issues


def solve_by_issue(engine: Prolog, issue: str) -> str:
    query = f"resolve_issue({issue}, Message)"
    result = list(engine.query(query, maxresult=1))
    if not result:
        return "No recommendation found. Please escalate to human support."
    return result[0]["Message"]


def normalize_text(text: str) -> str:
    # Prolog keyword matching uses lowercase atoms with underscores.
    return (
        text.lower()
        .replace("'", "")
        .replace("-", " ")
        .replace("/", " ")
        .replace("  ", " ")
        .strip()
        .replace(" ", "_")
    )


def solve_by_text(engine: Prolog, raw_text: str) -> str:
    normalized = normalize_text(raw_text)
    query = f"recommendation({normalized}, Message)"
    result = list(engine.query(query, maxresult=1))
    if not result:
        return "No recommendation found. Please escalate to human support."
    return result[0]["Message"]


def render_menu(issues: List[str]) -> Dict[str, str]:
    option_map: Dict[str, str] = {}
    print("\nCustomer Support Expert System")
    print("=" * 32)
    print("Select an issue category or describe the problem in free text.")

    for index, issue in enumerate(issues, start=1):
        key = str(index)
        option_map[key] = issue
        print(f"{key}. {atom_to_label(issue)}")

    text_option = str(len(issues) + 1)
    exit_option = str(len(issues) + 2)
    option_map[text_option] = "__free_text__"
    option_map[exit_option] = "__exit__"

    print(f"{text_option}. Enter free-text complaint")
    print(f"{exit_option}. Exit")
    return option_map


def main() -> None:
    engine = load_engine()
    issues = get_issues(engine)

    if not issues:
        raise SystemExit("No issues found in the knowledge base.")

    while True:
        option_map = render_menu(issues)
        choice = input("\nChoose an option: ").strip()

        selected = option_map.get(choice)
        if selected is None:
            print("Invalid option. Please try again.")
            continue

        if selected == "__exit__":
            print("Goodbye.")
            break

        if selected == "__free_text__":
            complaint = input("Describe your issue: ").strip()
            if not complaint:
                print("Please enter a valid complaint.")
                continue
            recommendation = solve_by_text(engine, complaint)
            print(f"\nRecommendation: {recommendation}\n")
            continue

        recommendation = solve_by_issue(engine, selected)
        print(f"\nRecommendation: {recommendation}\n")


if __name__ == "__main__":
    main()
