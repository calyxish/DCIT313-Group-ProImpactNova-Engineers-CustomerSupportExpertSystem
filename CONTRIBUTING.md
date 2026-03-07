# Contributing Guide

**Project:** Customer Support Expert System
**Team:** ProImpactNova Engineers

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
