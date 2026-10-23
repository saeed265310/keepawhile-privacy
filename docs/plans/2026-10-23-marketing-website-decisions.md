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

**Tasks 4-5 AFTER** (`python3 scripts/check_site.py`):
```
PASS 1 links (WARN: 15 missing screenshot imgs, awaiting Task 6)
PASS 2 colours / 3 external loads / 4 claims / 5 legal text / 6 structure+7 img
```

## Findings (executor)
- Task 5: dropped "can change mode in Settings" and "simpler list" from the Safe Ledger bullet; PROJECT_SCOPE only supports an onboarding choice.

## Task 7 (partial, automated only)
Contrast (WCAG ratios computed from tokens): all 12 pairs >= 4.5 (lowest: light link on page bg 4.72; dark link 8.95). Local server returns 200 for all 4 pages, css, font, icon, og image.
NOT done (needs a browser/phone): visual light/dark check, 320px and 200% zoom no horizontal scroll, keyboard tab order, console errors. Task 8 launch checklist below.

## Task 8 Launch checklist (do not execute here)
1. SuperContacts-orca: change policy link `https://saeed265310.github.io/keepawhile-privacy/` -> `.../privacy-policy.html` (found in Dart settings link and docs); release/use before merge of this branch.
2. Play Console: privacy policy URL (and Data safety URL if set) -> `/privacy-policy.html`.
3. Replace `<!-- STORE-LINK -->` spans in index.html and features.html with the Play link once the listing is live.
4. Screenshots: run prompt, drop PNGs in assets/screenshots/, if 08 skipped remove its img from features.html, run `python3 scripts/check_site.py --strict`.
5. Merge only after 1, 2 and 4 (merge = deploy to GitHub Pages).

## Executor Cost Log
Task 0-5, 7: Claude Sonnet 5.5 — not exposed

Per task: `Task N: <executor name> — <figure + unit, or "not exposed">`. No entries yet.

## Findings
- 2026-10-23 architect: `privacy-policy.html` (Oct 12) is stale vs `index.html` (Oct 22). Commit 5b38476 only touched `index.html`. Task 3 must copy legal text from `index.html` @5b38476. Also check `docs`/Play: any listing pointing at `/privacy-policy.html` has been serving the old text.
