# Skill: Git Main Hygiene (AirBnB_NLP4socialscience)

## Goal
Keep `main` clean and reproducible by preventing generated result artifacts from being committed.

## When to use
- Before committing notebook or pipeline changes.
- When generated files appear in `git status`.
- Before pushing to `main`.

## Policy
- Generated result files must not be committed to `main`.
- Keep source/static inputs versioned only when explicitly required.
- If a result file appears in `git status`, add or refine ignore rules first.

## Result Files to Exclude
- `results_*.csv`
- `data/results_*.csv`
- `data/*_summary*.csv`
- `data/*_per_review*.csv`
- `data/*_annotations*.csv`

## Standard Workflow
1. Check working tree:
   - `git status --short`
2. Inspect suspicious generated files:
   - `git ls-files "data/results*"`
   - `git ls-files "results*"`
3. Update `.gitignore` if needed.
4. If already tracked, untrack while keeping local file:
   - `git rm --cached <path>`
5. Verify ignore behavior:
   - `git check-ignore -v <path>`
6. Commit only source/notebook/code changes.

## LFS Safety
- Do not add generated result CSVs to Git LFS.
- Keep LFS for notebooks or explicitly approved large assets.
- If push fails with LFS size errors, inspect pending LFS objects:
  - `git lfs status`
  - `git lfs ls-files --size`

## Pre-Push Checklist
- `git status --short` has no generated result files.
- `.gitignore` includes current result patterns.
- `git push origin main` completes without LFS size errors.

## Emergency Recovery (local commits not pushed)
If generated results were committed locally:
1. Reset to remote base while keeping changes:
   - `git reset --soft origin/main`
2. Unstage generated files:
   - `git restore --staged <result_file>`
3. Commit again with clean staging.
