# Marketing Website — Deviation Log

Plan: `2026-10-23-marketing-website-tasks.md`

## Deviations

One line per deviation: **what, why, which task.** New dependency, file outside a task's
`File:` header, changed public signature.

Pre-authorized by critique (replace each placeholder line with the real entry once executed; do not add a parallel section):
- [PLACEHOLDER Task 3] `terms.html` privacy href root → `privacy-policy.html` (legal text unchanged). Replace with: what changed, commit.
- [PLACEHOLDER Task 3] `privacy-policy.html` body rebuilt from `git show 5b38476:index.html`. Replace with: commit, check 5 output reference.

## TDD Evidence

Per task: the actual BEFORE (failing) and AFTER (passing) check output, pasted verbatim —
not paraphrased. No entries yet.

## Executor Cost Log

Per task: `Task N: <executor name> — <figure + unit, or "not exposed">`. No entries yet.

## Findings
- 2026-10-23 architect: `privacy-policy.html` (Oct 12) is stale vs `index.html` (Oct 22). Commit 5b38476 only touched `index.html`. Task 3 must copy legal text from `index.html` @5b38476. Also check `docs`/Play: any listing pointing at `/privacy-policy.html` has been serving the old text.
