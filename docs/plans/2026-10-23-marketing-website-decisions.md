# Marketing Website — Deviation Log

Plan: `2026-10-23-marketing-website-tasks.md`

## Deviations

One line per deviation: **what, why, which task.** New dependency, file outside a task's
`File:` header, changed public signature.

Pre-authorized by critique (replace each placeholder line with the real entry once executed; do not add a parallel section):
- Task 3: `terms.html` privacy href root → `privacy-policy.html` (legal text unchanged). Done; check 6 no longer flags bare-root link.
- Task 3: `privacy-policy.html` body rebuilt from `git show 5b38476:index.html`. Done; check 5 PASS (see TDD Evidence).

## TDD Evidence

Per task: the actual BEFORE (failing) and AFTER (passing) check output, pasted verbatim —
not paraphrased. No entries yet.

**Task 3 AFTER** (legal pages restyled; index/features not built yet):
```
PASS 5 legal text   (privacy-policy.html, terms.html contain 5b38476 baseline text)
PASS 2 colours / PASS 3 external loads
FAIL 1 links: privacy-policy.html, terms.html -> features.html missing (Task 5)
```

## Executor Cost Log

Per task: `Task N: <executor name> — <figure + unit, or "not exposed">`. No entries yet.

## Findings
- 2026-10-23 architect: `privacy-policy.html` (Oct 12) is stale vs `index.html` (Oct 22). Commit 5b38476 only touched `index.html`. Task 3 must copy legal text from `index.html` @5b38476. Also check `docs`/Play: any listing pointing at `/privacy-policy.html` has been serving the old text.
