# code-quality-testbed

A testbed repo for automated code quality safeguards. The branching model:

- **Feature branches** (`feature/*`): free to work on and commit to. CI runs but nothing blocks.
- **`staging`**: the quality gate. Every change arrives via PR, and the PR cannot merge
  unless the required checks pass (lint, format, type check, tests, secrets).
- **`main`**: receives `staging` via PR once staging is green.

See [docs/BRANCHING.md](docs/BRANCHING.md) for the full model, and [AGENTS.md](AGENTS.md)
for the instructions agents (Codex) follow when working in this repo.

## Quickstart

```bash
git checkout -b feature/my-change staging   # branch from staging
# ... work, commit, push freely ...
gh pr create --base staging                  # open PR into the gate
# required checks must be green before merge
gh pr merge --squash --delete-branch
```

## Quality gates (enforced on PRs to `staging`)

| Check | Tool |
|---|---|
| Python lint + format | `ruff check`, `ruff format --check` |
| Python types | `pyright` |
| Python tests | `pytest` |
| JS lint + format | `eslint`, `prettier --check` |
| Secrets | `gitleaks` |

Run locally before opening a PR:

```bash
ruff check src tests && ruff format --check src tests && pyright src && pytest -q
```
