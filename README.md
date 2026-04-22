# Customer Support Expert System

**DCIT 313 — Group Project**
**Team: ProImpactNova Engineers**

---

## Group Members

| #   | Name                                  | GitHub Username       | Student ID |
| --- | ------------------------------------- | --------------------- | ---------- |
| 1   | Ishmael Affum Kwakye *(Group Leader)* | calyxish              | 22032451   |
| 2   | Samuel Kofi Ntem Amankwah             | Sammy-157             | 22017217   |
| 3   | Prince Boateng                        | —                     | 22017084   |
| 4   | Christian Agyapong                    | ChristianAgyapong     | 22054189   |
| 5   | Michael Asante-Arhin                  | Icon-1k               | 22241078   |
| 6   | Jeremiah Kwadwo Wiafe                 | kojowiafe-dev         | 22151311   |
| 7   | Dzikum Isaac                          | —                     | 22045685   |

---

## Overview

The **Customer Support Expert System (CSES)** is a Knowledge-Based System (KBS) that mimics the decision-making of human customer service agents. It maps customer-reported problems to recommended solutions using a **Prolog knowledge base** of facts and inference rules, driven by a **Python CLI front-end** powered by [`pyswip`](https://pypi.org/project/pyswip/).

It is designed for small-to-medium businesses — online retail stores, telecom providers, and service companies — where handling high volumes of repetitive customer queries manually is time-consuming and error-prone.

---

## Key Capabilities

| Capability | Description |
|---|---|
| **Problem Diagnosis** | Matches free-text or menu-selected complaints to known issue categories via keyword inference |
| **Solution Delivery** | Returns concise, actionable guidance for each recognised issue |
| **Escalation Fallback** | Gracefully routes unknown or ambiguous queries to a human support agent |
| **Dual Input Modes** | Supports both numbered menu selection and open free-text entry |
| **Case-Insensitive Matching** | All keyword comparisons are performed in lowercase for robustness |
| **Best-Match Scoring** | The most frequently matched issue category wins when multiple candidates match |

---

## Supported Issue Categories (15)

| Issue Atom | Trigger Keywords | Example Customer Phrase |
|---|---|---|
| `login_issue` | login, password, signin, account | *"I cannot login to my account"* |
| `password_reset` | reset, forgot, recover | *"I forgot my password"* |
| `account_locked` | locked, blocked, suspended | *"My account is blocked"* |
| `order_delayed` | delayed, late, tracking, shipment | *"My shipment is late"* |
| `order_missing` | missing, not_delivered, not_received | *"My order is missing"* |
| `wrong_item_received` | wrong_item, incorrect, mismatch | *"I received the wrong item"* |
| `billing_error` | billing, charged, invoice, payment | *"I was incorrectly charged"* |
| `duplicate_charge` | duplicate, double_charge, twice | *"I was charged twice"* |
| `refund_request` | refund, return, money_back | *"I want a refund"* |
| `defective_product` | broken, damaged, defective, faulty | *"The product is broken"* |
| `no_internet_connection` | no_connection, disconnected, offline | *"I am offline"* |
| `slow_internet` | slow, buffering, lag | *"My internet is very slow"* |
| `network_error` | error, timeout, failed | *"Request timed out"* |
| `app_crash` | crash, freeze, stop, closing | *"The app keeps crashing"* |
| `subscription_cancellation` | cancel, unsubscribe, subscription | *"I want to cancel my subscription"* |

---

## Project Structure

```
DCIT313-Group-ProImpactNova-Engineers-CustomerSupportExpertSystem/
├── knowledge_base/
│   └── customer_support.pl      # Prolog facts, keywords, rules, and solutions
├── interface/
│   └── main.py                  # Python CLI — loads KB, runs inference, displays results
├── docs/
│   └── knowledge_engineering.md # Knowledge acquisition and representation report
├── tests/
│   ├── test_interface.py        # Unit tests for Python utility functions
│   └── test_knowledge_base.py   # Integration tests against the live Prolog engine
├── requirements.txt             # Python dependencies (pyswip>=0.2.11)
├── CONTRIBUTING.md              # Branching workflow and contribution guide
├── LICENSE
└── README.md
```

---

## Tech Stack

| Component | Technology |
|---|---|
| Logic / Inference Engine | SWI-Prolog |
| Python–Prolog Bridge | `pyswip >= 0.2.11` |
| User Interface | Python 3 CLI (`interface/main.py`) |
| Test Framework | Python `unittest` |
| Version Control | Git / GitHub |

---

## Getting Started

### Prerequisites

1. **SWI-Prolog** — Download and install from [swi-prolog.org](https://www.swi-prolog.org/download/stable).  
   After installation, verify it is on your system `PATH`:
   ```bash
   swipl --version
   ```

2. **Python 3.8 or higher**  
   ```bash
   python --version
   ```

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/<your-org>/DCIT313-Group-ProImpactNova-Engineers-CustomerSupportExpertSystem.git
cd DCIT313-Group-ProImpactNova-Engineers-CustomerSupportExpertSystem

# 2. (Recommended) Create and activate a virtual environment
python -m venv .venv

# On Windows (PowerShell):
.venv\Scripts\Activate.ps1

# On macOS / Linux:
source .venv/bin/activate

# 3. Install Python dependencies
pip install -r requirements.txt
```

> **Windows note:** If your execution policy blocks activation, run:
> ```powershell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```

### Running the System (CLI)

```bash
python interface/main.py
```

**Windows (using the virtual environment interpreter directly):**
```powershell
.venv\Scripts\python.exe interface\main.py
```

### Running the Web Interface

```bash
python interface/web_app.py
```

Then open your browser at:

```text
http://127.0.0.1:5000
```

**Windows (using the virtual environment interpreter directly):**
```powershell
.venv\Scripts\python.exe interface\web_app.py
```

---

## Example Session

```
Customer Support Expert System
================================
Select an issue category or describe the problem in free text.
1. Account Locked
2. App Crash
3. Billing Error
4. Defective Product
5. Duplicate Charge
6. Login Issue
7. Network Error
8. No Internet Connection
9. Order Delayed
10. Order Missing
11. Password Reset
12. Refund Request
13. Slow Internet
14. Subscription Cancellation
15. Wrong Item Received
16. Enter free-text complaint
17. Exit

Choose an option: 16

Describe your issue: My order hasn't arrived and I don't know where it is

Recommendation: We are sorry about this. Please confirm your shipping address and contact support with your order ID for an urgent trace.
```

### Free-Text Diagnosis Example

| User Input | Detected Issue | Recommendation Excerpt |
|---|---|---|
| *"I forgot my password"* | `password_reset` | *"Use the Forgot Password option…"* |
| *"My shipment is late"* | `order_delayed` | *"Your order is in transit…"* |
| *"I was charged twice"* | `duplicate_charge` | *"Please share your transaction details…"* |
| *"The app keeps freezing"* | `app_crash` | *"Restart the app or reinstall it…"* |
| *"I just want to say hello"* | *(unknown)* — escalation | *"Please escalate to a human support agent…"* |

---

## How the Inference Works

```
Customer Input
     │
     ▼
normalize_text()          ← lowercase, strip punctuation, replace spaces with _
     │
     ▼
diagnose(Text, Issue)     ← Prolog: find all issues whose keywords appear in Text
     │
     ▼
most_frequent(Issues)     ← Pick the issue with the highest keyword match count
     │
     ▼
resolve_issue(Issue, Msg) ← Return the mapped solution string
     │
     ▼
[Unknown → escalation_message()]
```

The Prolog `diagnose/2` predicate uses `sub_atom/5` for substring matching, allowing partial matches (e.g., *"billing"* inside *"incorrect billing reference"*).

---

## Running Tests

Make sure the virtual environment is activated, then:

```bash
# Run all tests
python -m unittest discover tests

# Run interface utility tests only
python -m unittest tests/test_interface.py

# Run knowledge base integration tests only (requires SWI-Prolog)
python -m unittest tests/test_knowledge_base.py
```

**Windows (PowerShell):**
```powershell
.venv\Scripts\python.exe -m unittest discover tests
```

Expected output:
```
......
----------------------------------------------------------------------
Ran 5 tests in 0.XXXs

OK
```

---

## Inference Flow Summary

1. **Customer** submits a complaint (menu choice or free text).
2. **`normalize_text()`** cleans and tokenises the input.
3. **Prolog `diagnose/2`** scans all `keyword/2` facts for substring matches.
4. **`most_frequent/2`** selects the best-matching issue category.
5. **`resolve_issue/2`** fetches the mapped solution string.
6. If no match → **`escalation_message/1`** instructs handover to a human agent.

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
