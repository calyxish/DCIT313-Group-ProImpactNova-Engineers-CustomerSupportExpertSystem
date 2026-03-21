from __future__ import annotations

import os
import sys
from pathlib import Path

from flask import Flask, render_template, request

if __package__ is None or __package__ == "":
    sys.path.append(str(Path(__file__).resolve().parents[1]))
    from interface.main import atom_to_label, get_issues, load_engine, normalize_text, solve_by_issue, solve_by_text
else:
    from .main import atom_to_label, get_issues, load_engine, normalize_text, solve_by_issue, solve_by_text


app = Flask(__name__, template_folder="templates", static_folder="static")
engine = load_engine()
issues = get_issues(engine)


@app.route("/", methods=["GET", "POST"])
def home():
    recommendation = None
    selected_issue = ""
    selected_issue_preview = ""
    complaint = ""
    active_mode = "issue"
    diagnosis_mode = None
    diagnosis_issue_label = None

    if request.method == "POST":
        mode = request.form.get("mode", "issue")
        active_mode = mode

        if mode == "text":
            complaint = request.form.get("complaint", "").strip()
            if complaint:
                # We need to get the issue AND the message
                normalized = normalize_text(complaint)
                query = f"recommendation({normalized}, Message, Issue)"
                result = list(engine.query(query, maxresult=1))
                if result:
                    recommendation = result[0]["Message"]
                    diagnosis_issue_label = atom_to_label(result[0]["Issue"])
                else:
                    recommendation = "No recommendation found. Please escalate to human support."
                diagnosis_mode = "Free-Text Analysis"
            else:
                recommendation = "Please describe your issue before submitting."
        else:
            selected_issue = request.form.get("issue", "").strip()
            if selected_issue:
                recommendation = solve_by_issue(engine, selected_issue)
                diagnosis_issue_label = atom_to_label(selected_issue)
                diagnosis_mode = "Category Selection"
            else:
                recommendation = "Please choose an issue category before submitting."

    issue_cards = [
        {
            "atom": issue,
            "label": atom_to_label(issue),
            "preview": solve_by_issue(engine, issue),
        }
        for issue in issues
    ]

    if selected_issue:
        selected_issue_preview = solve_by_issue(engine, selected_issue)

    return render_template(
        "index.html",
        issue_cards=issue_cards,
        recommendation=recommendation,
        selected_issue=selected_issue,
        selected_issue_preview=selected_issue_preview,
        complaint=complaint,
        active_mode=active_mode,
        diagnosis_mode=diagnosis_mode,
        diagnosis_issue_label=diagnosis_issue_label,
    )


if __name__ == "__main__":
    host = os.getenv("CSES_HOST", "127.0.0.1")
    port = int(os.getenv("CSES_PORT", "5000"))
    app.run(host=host, port=port, debug=False)
