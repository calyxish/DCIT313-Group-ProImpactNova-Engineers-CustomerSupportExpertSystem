# Knowledge Engineering Report

**Project:** Customer Support Expert System (CSES)
**Team:** ProImpactNova Engineers — DCIT 313 Group Project

---

## 1. Purpose

This report documents how real-world customer support expertise was acquired, structured, and encoded as a rule-based Prolog knowledge base. It covers the knowledge sources used, the representation strategy chosen, the inference method implemented, full coverage of the encoded issues, and directions for future extension.

---

## 2. Knowledge Acquisition

### 2.1 Knowledge Sources

| Source | Description |
|---|---|
| E-commerce support patterns | Common issues in online retail: order tracking, refunds, wrong items |
| Telecom ISP support scripts | Connectivity troubleshooting: no internet, slow speeds, network errors |
| SaaS/app support workflows | Account access: login failures, locked accounts, app crashes, password resets |
| Billing department FAQs | Overcharges, duplicate transactions, invoice disputes |
| Escalation best practices | Criteria for when automated systems must hand off to human agents |

### 2.2 Knowledge Elicitation Method

Knowledge was elicited by:
- Reviewing standard first-line customer support scripts from publicly available sources.
- Mapping the vocabulary customers naturally use (e.g., *"it won't load"*, *"I'm locked out"*) to formal issue categories.
- Identifying the minimal set of solution actions that would resolve each category.
- Defining clear escalation criteria for cases that cannot be resolved automatically.

---

## 3. Representation Strategy

The knowledge base (`knowledge_base/customer_support.pl`) uses three layers of Prolog facts and one inference rule chain:

### Layer 1 — Issue Facts
Declare all known problem categories as ground atoms:
```prolog
issue(login_issue).
issue(order_delayed).
issue(refund_request).
% ... (15 issues total)
```

### Layer 2 — Keyword Facts
Map natural-language vocabulary to issue categories:
```prolog
keyword(login_issue, password).
keyword(login_issue, signin).
keyword(order_delayed, late).
keyword(refund_request, refund).
```
Each keyword is the lowercase, normalised form of a word a customer might use.

### Layer 3 — Solution Facts
Map each issue category to a concrete, actionable resolution message:
```prolog
solution(login_issue,
  'Reset your password from the Forgot Password page, then try logging in again.').
solution(refund_request,
  'Please provide your order ID and reason for refund. We will process it within 3-5 business days.').
```

### Layer 4 — Escalation Fallback
A catch-all message returned when no issue can be confidently identified:
```prolog
escalation_message(
  'I could not confidently diagnose this issue. Please escalate to a human support agent with customer details and screenshots.').
```

---

## 4. Inference Mechanism

### 4.1 Text Normalisation (Python layer)

Before the Prolog engine is queried, `interface/main.py` normalises user input:

```python
def normalize_text(text: str) -> str:
    return (
        text.lower()
            .replace("'", "")
            .replace("-", " ")
            .replace("/", " ")
            .replace("  ", " ")
            .strip()
            .replace(" ", "_")
    )
```

This converts a phrase like *"Can't login / signin"* → `cant_login_signin`, making it compatible with Prolog atom matching.

### 4.2 Keyword Matching (Prolog)

```prolog
matches(Text, Keyword) :-
    downcase_atom(Text, LowerText),
    downcase_atom(Keyword, LowerKeyword),
    sub_atom(LowerText, _, _, _, LowerKeyword).
```

`sub_atom/5` performs substring matching, so *"password"* is found inside *"forgot_my_password"* without requiring exact word boundaries.

### 4.3 Best-Match Diagnosis

```prolog
diagnose(Text, Issue) :-
    findall(I,
        (issue(I), keyword(I, Keyword), matches(Text, Keyword)),
        Issues),
    Issues \= [],
    most_frequent(Issues, Issue),
    !.

diagnose(_, unknown_issue).
```

All issue categories whose keywords appear in the text are collected. The one with the **highest keyword match count** wins. A deterministic cut (`!`) prevents backtracking into the unknown-issue fallback once a match is found.

### 4.4 End-to-End Resolution

```prolog
recommendation(Text, Message) :-
    diagnose(Text, Issue),
    resolve_issue(Issue, Message).
```

This is the single public predicate called by the Python interface.

### 4.5 Inference Flow Diagram

```
Customer Input (free text or menu selection)
        │
        ▼
[Python] normalize_text()
        │  lowercase, strip punctuation, underscoreify
        ▼
[Prolog] diagnose(Text, Issue)
        │  findall matching issues via keyword sub_atom search
        │  most_frequent/2 picks best match
        ▼
[Prolog] resolve_issue(Issue, Message)
        │  looks up solution/2 fact
        │
        ├──► Known Issue → Return solution string
        │
        └──► unknown_issue → Return escalation_message
```

---

## 5. Knowledge Coverage

### 5.1 Issue Categories and Keywords

| Issue | Keywords |
|---|---|
| `login_issue` | login, password, signin, account |
| `password_reset` | reset, forgot, recover |
| `account_locked` | locked, blocked, suspended |
| `order_delayed` | delayed, late, tracking, shipment |
| `order_missing` | missing, not_delivered, not_received |
| `wrong_item_received` | wrong_item, incorrect, mismatch |
| `billing_error` | billing, charged, invoice, payment |
| `duplicate_charge` | duplicate, double_charge, twice |
| `refund_request` | refund, return, money_back |
| `defective_product` | broken, damaged, defective, faulty |
| `no_internet_connection` | no_connection, disconnected, offline |
| `slow_internet` | slow, buffering, lag |
| `network_error` | error, timeout, failed |
| `app_crash` | crash, freeze, stop, closing |
| `subscription_cancellation` | cancel, unsubscribe, subscription |

**Total issues:** 15 | **Total keyword mappings:** 51 | **Solutions:** 15 + 1 escalation

### 5.2 Example Diagnoses

| Input Text | Normalised Form | Matched Keywords | Diagnosed Issue |
|---|---|---|---|
| *"I forgot my password"* | `i_forgot_my_password` | forgot → `password_reset`, password → `password_reset`, `login_issue` | `password_reset` (2 hits) |
| *"My shipment is late"* | `my_shipment_is_late` | shipment → `order_delayed`, late → `order_delayed` | `order_delayed` (2 hits) |
| *"I was charged twice"* | `i_was_charged_twice` | charged → `billing_error`, twice → `duplicate_charge` | tie-broken by `most_frequent` |
| *"I just want to say hello"* | `i_just_want_to_say_hello` | *(none)* | → escalation |

---

## 6. Testing and Validation

The system is validated by two test modules in `/tests/`:

### `test_interface.py` — Unit Tests
Tests Python utility functions in isolation (no Prolog required):
- `atom_to_label("login_issue")` → `"Login Issue"`
- `normalize_text("Can't login")` → `"cant_login"`
- `normalize_text("Billing/Invoice")` → `"billing_invoice"`

### `test_knowledge_base.py` — Integration Tests
Tests the full Python → Prolog inference pipeline:
- Known issue resolution: `solve_by_issue(engine, "login_issue")` must contain `"Reset your password"`.
- Free-text keyword diagnosis: `"I forgot my password"` must trigger `login_issue` solution.
- Escalation fallback: `"I just want to say hello"` must return the escalation message.

Run tests:
```bash
python -m unittest discover tests
```

---

## 7. Limitations

| Limitation | Impact |
|---|---|
| Keyword-only matching — no semantic understanding | Synonyms not in the keyword list are missed |
| No confidence threshold | A single keyword match is treated the same as many |
| English-only | Non-English input will not match any keyword and will escalate |
| No session memory | Each query is independent; the system has no conversation context |
| Static knowledge base | Adding new issues requires editing the `.pl` file and restarting |

---

## 8. Future Improvements

| Idea | Benefit |
|---|---|
| Confidence scoring (keyword match ratio) | Suppress low-confidence single-keyword matches |
| Synonym and stemming expansion | Increase recall (e.g., *"ship"* matching `shipment`) |
| Multilingual keyword sets | Support French, Spanish, Portuguese customers |
| Case history / query log | Enable analytics and trend detection |
| Domain module splitting | Separate billing, logistics, and tech issues into `.pl` modules |
| Web or chat interface | Replace CLI with a messenger-style front-end |
| NLP pre-processing layer | Use NLTK or spaCy to extract intent before Prolog query |

---

## 9. Conclusion

The Customer Support Expert System successfully encodes first-line support expertise as a Prolog knowledge base queryable from Python. The `diagnose → resolve → escalate` inference chain handles 15 issue categories with 51 keyword mappings and degrades gracefully to human escalation for unrecognised complaints. The architecture is modular and straightforward to extend by adding new `issue/1`, `keyword/2`, and `solution/2` facts.
