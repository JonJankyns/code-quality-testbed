# AGENTS.md — code-quality-testbed

## Branching model (follow exactly)

- `staging` is the quality gate. **Never commit or push directly to `staging` or `main`.**
- Do all work on feature branches, always branched from `staging`:
  `git checkout -b feature/<short-name> staging`
- Feature branches are free: commit and push as often as you like. CI runs on
  feature branches but nothing blocks — no required checks there.
- When the feature is done, open a PR targeting `staging`:
  `gh pr create --base staging --title "<title>" --body "<summary>"`
- The PR **must** show all required checks green before merging:
  `quality / python`, `quality / javascript`, `quality / secrets`.
  If a check fails, fix it on the feature branch and push again. Never merge a red PR.
- Merge with `gh pr merge --squash --delete-branch <pr-number>`.
- `staging` → `main` is done by the human via PR after staging is green.

## Quality gates (enforced by CI on PRs to `staging`)

- Python: `ruff check src tests`, `ruff format --check src tests`, `pyright src`, `pytest -q`
- JS: `npx eslint web/`, `npx prettier --check "web/**/*.js"`
- Secrets: `gitleaks` (blocking; never commit real secrets, tokens, or keys)

Run the Python gates locally before opening the PR:

```bash
ruff check src tests && ruff format --check src tests && pyright src && pytest -q
```

## Proving the gate works

To verify the gate end to end: branch from `staging`, introduce a lint error
(e.g. an unused import), open a PR to `staging`, confirm the required checks
fail and the merge button is blocked, then fix the error on the branch, push,
confirm checks go green, and merge.
