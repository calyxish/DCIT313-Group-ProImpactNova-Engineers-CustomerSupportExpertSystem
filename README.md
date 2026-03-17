# Customer Support Expert System

**DCIT 313 — Group Project**
**Team: ProImpactNova Engineers**

---

## Group Members

| #   | Name                                  |
| --- | ------------------------------------- |
| 1   | Ishmael Affum Kwakye *(Group Leader)* |
| 2   | Samuel Kofi Ntem Amankwah             |
| 3   | Prince Boateng                        |
| 4   | Christian Agyapong                    |
| 5   | Michael Asante-Arhin                  |
| 6   | Jeremiah Kwadwo Wiafe                 |
| 7   | Dzikum Isaac                          |

---

## Overview

The **Customer Support Expert System (CSES)** is a Knowledge-Based System that mimics the decision-making process of human customer service agents. It maps customer-reported problems (perceptions) to recommended solutions (actions) using a Prolog knowledge base of facts and rules, with a Python front-end powered by `pyswip`.

The system is designed for small-to-medium businesses — online retail stores, telecom providers, service companies — where handling high volumes of customer queries manually is time-consuming and error-prone.

## Current Implementation Status

The project currently includes a working baseline:

- A Prolog knowledge base with starter issue categories, keywords, and solution rules.
- A Python CLI interface that queries Prolog through `pyswip`.
- Escalation fallback when no confident issue match is found.
- Initial documentation for the knowledge engineering process.

### Key Capabilities

- **Problem Diagnosis** — Matches customer input to known issues using logical inference.
- **Step-by-Step Guidance** — Provides actionable solutions for common problems (login issues, order tracking, billing, defective products, etc.).
- **Escalation** — Routes unresolved queries to human support agents.
- **24/7 Availability** — Operates without human intervention around the clock.

---

## How It Works

The system is built on three core components:

### 1. Knowledge Base (`/knowledge_base`)

A Prolog `.pl` file containing **facts** (known problems and solutions) and **rules** (logical mappings from symptoms to conclusions).

```prolog
% Fact
solution(login_issue, 'Reset your password using the Forgot Password link.').

% Rule
diagnose(slow_internet) :- symptom(no_connection), symptom(router_light_off).
```

### 2. Inference Engine / Interface (`/interface`)

A Python script using `pyswip` that:

- Accepts user input (typed problem description or menu selection).
- Queries the Prolog knowledge base.
- Returns the best-matching solution or escalates to human support.

### 3. Documentation (`/docs`)

A report on the **Knowledge Engineering** process — how real-world customer support expertise was translated into logical facts and rules.

---

## Project Structure

```
├── knowledge_base/
│   └── customer_support.pl      # Prolog facts and rules
├── interface/
│   └── main.py                  # Python UI / inference interface
├── docs/
│   └── knowledge_engineering.md # Knowledge acquisition report
├── requirements.txt             # Python dependencies
├── README.md
└── LICENSE
```

---

## Tech Stack

| Component        | Technology                |
| ---------------- | ------------------------- |
| Logic Engine     | SWI-Prolog                |
| User Interface   | Python 3 + `pyswip`      |
| Version Control  | Git / GitHub              |

---

## Getting Started

### Prerequisites

- [SWI-Prolog](https://www.swi-prolog.org/download/stable) installed and on PATH
- Python 3.8+
- `pyswip` library

### Installation

```bash
# Clone the repository
git clone https://github.com/<your-org>/DCIT313-Group-ProImpactNova-Engineers-CustomerSupportExpertSystem.git
cd DCIT313-Group-ProImpactNova-Engineers-CustomerSupportExpertSystem

# Install Python dependencies
pip install -r requirements.txt
```

### Running the System

```bash
python interface/main.py
```

### Recommended Windows Run Commands

Use the project virtual environment interpreter to avoid Python version mismatch:

```powershell
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe interface\main.py
```

---

## Workflow Example

1. **Customer** types: *"My order hasn't arrived."*
2. **Inference engine** queries the Prolog knowledge base for matching rules.
3. **System** finds: `IF problem = order_delayed THEN provide tracking info`.
4. **Solution displayed**: *"Your order is on the way. Track it here: [tracking link]."*
5. If unresolved → **escalation** to a human support agent.

---

## Contributing

This project follows a strict branching workflow:

- `main` — stable, reviewed code only (merged by the Group Leader).
- `dev` — default development branch. All work targets `dev` via Pull Request.

To contribute: create a feature or bugfix branch off `dev`, push it, open a PR to `dev`, and tag the Group Leader as reviewer.

See [CONTRIBUTING.md](CONTRIBUTING.md) for full details.

---

## License

See [LICENSE](LICENSE) for details.
