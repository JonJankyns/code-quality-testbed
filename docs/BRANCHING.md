# Branching and quality-gate model

## The model

```
feature/*  ──(PR)──▶  staging  ──(PR)──▶  main
   free        gate       green        release
```

- **Feature branches** (`feature/*`, branched from `staging`): no required
  checks. Developers and agents commit and push freely; CI still runs so
  problems are visible early, but nothing blocks iteration.
- **`staging`**: protected by a GitHub ruleset (`staging-quality-gate`).
  Every change must arrive via pull request, and the PR cannot merge unless
  all required status checks pass:
  - `quality / python` — ruff lint, ruff format check, pyright, pytest
  - `quality / javascript` — eslint, prettier check
  - `quality / secrets` — gitleaks
  - `strict` required checks: the branch must be up to date with `staging`
    before merging.
  - Force pushes and branch deletion are disabled.
- **`main`**: receives `staging` via PR once staging is green. (Not gated yet;
  add the same ruleset if you want `main` protected too.)

## Why this shape

- Dev velocity is preserved: experiments, WIPs, and agent iterations live on
  feature branches with zero friction.
- Quality is enforced at exactly one choke point: the merge into `staging`.
  Nothing unlinted, unformatted, untyped, untested, or secret-leaking gets in.
- Agents (Codex) get a simple, mechanical loop: branch → commit → push →
  PR → fix red checks → merge. The full loop is documented in `AGENTS.md`.

## Pre-commit vs CI

- **CI (GitHub Actions)** is the real gate — it runs on every push and on
  every PR to `staging`, and its results are what block the merge.
- Local pre-commit hooks are optional for feature work (they must not slow
  down iteration). If you want them, install the hook config and let it
  auto-fix formatting only.

## Rollout checklist (for existing repos)

1. Copy `.github/workflows/quality.yml` into the repo.
2. Add a `pyproject.toml` (or extend the existing one) with the ruff config.
   For legacy codebases, start with a minimal rule set
   (`select = ["E","W","F","I","UP","B"]`) and ratchet stricter families
   (`S`, `D`, `PLR`) in later, instead of blocking everything on day one.
3. Create the `staging` branch from the current default branch and push it.
4. Recreate the `staging-quality-gate` ruleset (see below) with the exact
   check contexts from the workflow (`quality / <job>`).
5. Copy the branching section of `AGENTS.md` into the repo's agent
   instructions so Codex follows the same loop.
6. Prove it: open a PR with a deliberate lint error, confirm it blocks,
   fix, merge.

### Recreating the ruleset

```bash
gh api -X POST repos/<owner>/<repo>/rulesets \
  -f name='staging-quality-gate' -f target='branch' -f enforcement='active' \
  --raw-field conditions='{"ref_name":{"include":["refs/heads/staging"],"exclude":[]}}' \
  --raw-field rules='[
    {"type":"deletion"},
    {"type":"non_fast_forward"},
    {"type":"required_status_checks","parameters":{
      "strict_required_status_checks_policy":true,
      "required_status_checks":[
        {"context":"quality / python"},
        {"context":"quality / javascript"},
        {"context":"quality / secrets"}]}},
    {"type":"pull_request","parameters":{"required_approving_review_count":0}}]'
```

Note: `required_approving_review_count: 0` forces the PR workflow without
requiring a human reviewer — right for a solo-dev-plus-agents setup.
