# Contributing Guide

**Project:** Customer Support Expert System
**Team:** ProImpactNova Engineers

---

## Current Baseline Status (Ready For Team Work)

The repository now has a working baseline:

- `/knowledge_base/customer_support.pl` contains initial facts, keyword mappings, and recommendation rules.
- `/interface/main.py` contains a working CLI interface connected to Prolog via `pyswip`.
- `/docs/knowledge_engineering.md` contains initial knowledge engineering notes.
- `requirements.txt` includes Python dependencies.

Team members can safely start from this baseline by branching from `dev` and working on scoped tasks below.

**Important environment note:** run commands with the project virtual environment Python when possible to avoid interpreter mismatch.

```bash
# From project root
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe interface\main.py
```

---

## Branching Strategy

This project uses two long-lived branches:

| Branch | Purpose | Who merges |
| ------ | ------- | ---------- |
| `main` | Stable, reviewed code only | Group Leader (Ishmael) |
| `dev`  | Active development (default branch) | Via Pull Request |

**Rules:**

- **No one pushes directly to `main`.** All code reaches `main` only through a reviewed PR from `dev`.
- **No one pushes directly to `dev`.** All contributions go through feature/bugfix branches merged into `dev` via PR.

---

## Work Packages And Member Assignment

Each member owns one primary package and can support another package as backup reviewer.

| Member | Primary Package | Scope | Suggested Branch |
| ------ | --------------- | ----- | ---------------- |
| Ishmael Affum Kwakye (Leader) | Integration + Review | Final integration checks, merge coordination, quality gate, release notes | `feature/integration-quality-gate` |
| Samuel Kofi Ntem Amankwah | Knowledge Base Expansion | Add new issues, keywords, and solution rules in Prolog | `feature/knowledge-base-expansion` |
| Prince Boateng | Inference Quality | Add confidence scoring and disambiguation rules | `feature/inference-confidence` |
| Christian Agyapong | Python Interface Improvements | Improve UX flow, follow-up prompts, validation in CLI | `feature/interface-improvements` |
| Michael Asante-Arhin | Testing | Add Python tests and rule-level validation tests | `feature/testing-suite` |
| Jeremiah Kwadwo Wiafe | Documentation | Update README and knowledge engineering report with setup + examples | `docs/documentation-polish` |
| Dzikum Isaac | Dev Experience + Reliability | Setup scripts, dependency guidance, troubleshooting section | `feature/devx-reliability` |

---

## How To Implement Your Assigned Part

When a member picks a part, use this exact flow:

1. Sync with latest `dev`.

```bash
git checkout dev
git pull origin dev
```

2. Create your task branch using the suggested name (or a close variant).

```bash
git checkout -b feature/your-task-name
```

3. Work only in your scope folders:
- Knowledge Base: `/knowledge_base`
- Interface: `/interface`
- Docs: `/docs`, `README.md`
- Tooling/reliability: project root scripts/config only

4. Run local checks before commit:

```bash
.venv\Scripts\python.exe interface\main.py
```

5. Commit with focused messages.

```bash
git add .
git commit -m "Add <specific improvement>"
```

6. Push and open PR to `dev`.

```bash
git push origin feature/your-task-name
```

7. In PR description, include:
- What changed
- Why it was needed
- How to test it
- Any limitations

8. Tag Ishmael (leader) for review.

---

## If Someone Wants To Pick Another Member's Part

If a member is unavailable or workload is uneven:

1. Comment in group channel: "Picking package: <package-name>"
2. Create a branch for that package from latest `dev`.
3. Continue using the same scope boundaries and PR rules.
4. Mention in PR title: `[Pickup] <package-name>`.
5. The originally assigned member becomes reviewer if available.

This keeps ownership clear while avoiding blocked progress.

---

## Definition Of Done Per Package

A package is complete only when:

1. Scope changes are implemented and pushed in a focused PR.
2. The app still starts successfully with:

```bash
.venv\Scripts\python.exe interface\main.py
```

3. Documentation is updated for any behavior change.
4. PR is reviewed and approved before merge.

---

## How to Contribute

### 1. Clone the Repository (first time only)

```bash
git clone https://github.com/<org>/DCIT313-Group-ProImpactNova-Engineers-CustomerSupportExpertSystem.git
cd DCIT313-Group-ProImpactNova-Engineers-CustomerSupportExpertSystem
```

### 2. Make Sure You Are on `dev`

```bash
git checkout dev
git pull origin dev
```

### 3. Create a Branch for Your Work

Use the following naming conventions:

- **New feature:** `feature/<short-description>`
- **Bug fix:** `bugfix/<short-description>`
- **Documentation:** `docs/<short-description>`

```bash
git checkout -b feature/login-diagnosis-rules
```

### 4. Make Your Changes

- Work only inside the correct project folder (`/knowledge_base`, `/interface`, or `/docs`).
- Write clear, descriptive commit messages.

```bash
git add .
git commit -m "Add login diagnosis rules to knowledge base"
```

### 5. Push Your Branch

```bash
git push origin feature/login-diagnosis-rules
```

### 6. Open a Pull Request to `dev`

- Go to the repository on GitHub.
- Click **"Compare & pull request"**.
- Set the **base branch** to `dev` (not `main`).
- Add a clear title and description of what you changed and why.
- **Tag Ishmael Affum Kwakye as a reviewer.**

### 7. Address Review Feedback

If changes are requested, push additional commits to the same branch. The PR updates automatically.

### 8. Merge

Once approved, the PR will be merged into `dev`. Do not merge your own PR without approval.

---

## Branch Flow

```
feature/your-feature  -->  PR  -->  dev  -->  PR (Leader review)  -->  main
bugfix/your-fix       -->  PR  -->  dev  -->  PR (Leader review)  -->  main
```

---

## Commit Message Guidelines

Write commit messages in the imperative mood. Keep them short and specific.

**Good examples:**

```
Add billing dispute rules to knowledge base
Fix incorrect symptom matching for network issues
Update knowledge engineering report with telecom sources
```

**Bad examples:**

```
fixed stuff
update
changes
```

---

## What NOT to Do

- Do not push directly to `main` or `dev`.
- Do not merge your own pull request without review.
- Do not commit large unrelated changes in a single PR — keep PRs focused.
- Do not commit IDE-specific files, virtual environments, or compiled output (use `.gitignore`).

---

## Project Folder Rules

| Folder | What goes here |
| ------ | -------------- |
| `/knowledge_base` | Prolog `.pl` files (facts and rules only) |
| `/interface` | Python scripts (UI and inference logic) |
| `/docs` | Knowledge engineering report and documentation |

Do not place files outside these folders without discussion.
