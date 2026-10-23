Plan confidence: 96% (minimum 96%)
Critique status: PASSED

# Marketing Website Tasks

TRD: `docs/specs/2026-10-23-marketing-website-spec.md`. ADR: `docs/specs/2026-10-23-marketing-website-adr.md`. Log: `docs/plans/2026-10-23-marketing-website-decisions.md`.
Branch: `feature/marketing-website`. No build step. No JS. No new deps.

## Decisions fixed at architect step
- Hosting = GitHub Pages legacy, `main` `/`, no custom domain. Base `https://saeed265310.github.io/keepawhile-privacy/`. All page links relative. `og:image`/`og:url` absolute with that base.
- Policy URL: `index.html` becomes landing. Policy canonical = `/privacy-policy.html`. App link in `SuperContacts-orca` (grep `saeed265310.github.io/keepawhile-privacy/`) + Play Console privacy URL must change BEFORE launch. Not this repo. Task 8 = checklist only.
- Check script = the "failing test". One file `scripts/check_site.py`, python3 stdlib only (`html.parser`, `re`, `subprocess` for `git show`). No bash wrapper. Ladder: needs to exist (no tests otherwise); not in repo; stdlib covers it.
- Screenshots arrive later from `docs/specs/2026-10-23-website-screenshots-prompt.md`. Pages reference final filenames. Check script has `--strict` (images must exist, used at launch) and default (missing screenshots reported as WARN only).
- FOUND at architect step: `index.html` = CURRENT policy (Last updated Oct 22, 2026, has vCard safety mirror section). `privacy-policy.html` = STALE (Oct 12, 61 diff lines behind). Last commit 5b38476 updated only `index.html`. Baseline for privacy text = `git show HEAD:index.html` (commit 5b38476). Baseline for terms = `git show HEAD:terms.html`. Never use old `privacy-policy.html` text.

## Task 0: Check script (failing test first)
File: `scripts/check_site.py`. Usage: `python3 scripts/check_site.py [--strict] [ROOT]` (ROOT default repo root). Self-check: `--selftest` builds a temp dir (tempfile) with one page holding a broken link, a raw colour outside `:root`, the phrase "no ads", and a page without `<h1>`; asserts checks 1,2,4,6 each FAIL on it; also calls the check-5 compare function with a baseline string and an altered copy (one sentence removed) and asserts FAIL, and with baseline wrapped in extra header/footer text and asserts PASS. Then exits 0. Prevents checks that pass trivially.
Checks, each prints PASS/FAIL, exit 1 on any FAIL:
1. every relative `href`/`src` in `*.html` resolves to existing file (anchors `#x` resolve to `id="x"` in target). Screenshots under `assets/screenshots/` = WARN unless `--strict`.
2. no colour literal (`#hex` 3/4/6/8 digits, `rgb(`, `rgba(`, `hsl(`) in `*.html` or `assets/style.css` outside `:root { }` blocks (incl. the ones inside the dark `@media`). Allowed exception: `<meta name="theme-color">` content. Ignore `#` in `href`/`id` (anchors) — match only inside `<style>`, `style=""`, and `.css`.
3. no external resource loads: FAIL on any `http(s)://` or `//` in `<link href>`, `<script src>`, `<img src>`, `<iframe>`, `@import`, CSS `url(`. `<a href>` and `<meta content>` external URLs are always allowed (links are not requests; legal pages need Google/Overture/Foursquare attribution links).
4. banned phrases (case-insens, visible text only, not attributes) in `index.html`, `features.html`: "we collect nothing", "collect no data", "no ads", "ad-free", "no tracking", "$", "per month", "/month", "subscription", "premium", "AI-powered", "iPhone", "iOS", "App Store", "Apple Maps".
5. legal text: for `privacy-policy.html` (baseline `git show 5b38476:index.html`) and `terms.html` (baseline `git show 5b38476:terms.html`): text of baseline `<body>` (drop `<style>`/`<script>`, strip tags, `html.unescape`, collapse whitespace) must be a contiguous substring of the same extraction of the working file. Header/footer/skip-link additions allowed only outside that span.
6. each page has: one `<h1>`, `<title>`, `meta description`, `lang="en"`, `viewport`, skip link, `<main>`, `aria-current="page"` on exactly one nav link (except none required if page not in nav).
7. every `<img>` has `alt`, `width`, `height`.
Checkpoint: (a) `--selftest` exits 0; (b) run on current tree → must FAIL check 6 on all pages (check 5 passes: hotfix 1691a73 already synced `privacy-policy.html`). Paste both outputs verbatim to decisions log TDD Evidence.

## Task 1: Assets
Files: `assets/icon.png` (from `SuperContacts-orca/distribution/assets/app_icon_512.png`), `assets/og.png` (from `.../feature_graphic_1024x500.png`), `assets/fonts/PlusJakartaSans-{Regular,SemiBold,Bold,ExtraBold}.ttf` + `assets/fonts/OFL.txt` (from `SuperContacts-orca/assets/fonts/`), `assets/screenshots/.gitkeep`.
Favicon = `assets/icon.png` directly (no downscaled copy; YAGNI). Test: Task 0 check 1 once pages link it. Verify file sizes > 0 and `file` reports PNG/TrueType.
Note: icon is git-excluded in app repo but present on disk. If missing → STOP, report.

## Task 2: Stylesheet
File: `assets/style.css`. Spec §1 tokens/radius/layout exactly. `@font-face` x4 (relative `fonts/`), `font-display: swap`. `:root` light, `@media (prefers-color-scheme: dark)` override. Logical properties only. Components: skip-link, header/nav (≥44px targets), hero, section, feature-row (2-col ≥800px), phone frame, card grid, faq (`<details>`), footer, `.legal` wrapper for policy/terms (preserve current look: 760px, tables, h2 borders). `:focus-visible` outline. Max-width 1040.
Link/text-accent colour: light `--accent` (#2563EB on #F1F5F9 ≈ 4.9:1 ok); dark MUST use `--accent-2` #38BDF8 for links (#2563EB on #0B0F17 ≈ 3.6:1 FAILS AA). Buttons: white on #2563EB ≈ 5.2:1 ok both themes.
Test: Task 0 checks 2,3 pass on css. Manual (Task 7): contrast incl. `--muted` on `--card-subtle`.

## Task 3: Migrate policy + terms
Files: `privacy-policy.html`, `terms.html`.
Order matters: do this BEFORE Task 4 overwrites `index.html`. First rebuild `privacy-policy.html` body from `git show 5b38476:index.html` (current policy), then restyle. Steps: remove inline `<style>`, link `assets/style.css`, wrap with shared header/footer, body content in `<main class="legal">`. Do NOT edit legal text. Add meta description, skip link.
REQUIRED link fix: `terms.html` has `href="https://saeed265310.github.io/keepawhile-privacy/"` (its privacy-policy link). After Task 4 that URL = landing page. Change href ONLY to `privacy-policy.html`; link text unchanged. Pre-authorized in decisions log. Check 5 compares text, so it still passes; add grep: no `href` in `terms.html`/`privacy-policy.html` equals the bare site root.
Test: Task 0 check 5 passes for both. Rerun after every edit.
Checkpoint: `git diff` shows no change to text nodes.

## Task 4: Landing page
File: `index.html` (replaces policy copy; policy lives in `privacy-policy.html`).
Sections/order/copy per TRD §1 Content. Hero CTA = `<span>` "Coming soon on Google Play" with `<!-- STORE-LINK -->`. Screenshot imgs: `assets/screenshots/02-temporary.png`, `04-contact-detail.png`, `05-note-view.png`, `03-expiry-nudge.png`, `07-global-timeline.png` with real alt, width/height 1080x2400 scaled via CSS. FAQ 5 Qs via `<details>`. Footer: Privacy, Terms, mailto, "Android first". OG meta (`og:title`, `og:description`, `og:image` = `https://saeed265310.github.io/keepawhile-privacy/assets/og.png`, `og:url`). No Twitter tags (OG covers it; YAGNI).
Test: checks 1-4,6,7 pass (screenshots WARN).

## Task 5: Features page
File: `features.html`. 8 groups from TRD §1. One `<h2>` each, bullet list, shot where mapped: g1→02, g2→03, g3→04/05/06, g4→07, g5→08, g6→09/10, g7→none, g8→none. Missing shots (08 may be skipped) → omit `<img>` for that group, do not leave dead src. Same header/footer/meta.
Test: checks 1-4,6,7 pass.

## Task 6: Screenshot wiring gate
Depends on user delivering PNGs. Steps: confirm files in `assets/screenshots/`, run `scripts/check-site.sh --strict`. Strip ad banner if reported visible (crop; note in decisions log). Compress PNGs only if total > 6MB (python3 stdlib cannot; use `pngquant`/`oxipng` if installed else flag).
Test: `--strict` passes.

## Task 7: Verify
Local serve: `python3 -m http.server` in repo, open all 4 pages. Manual: light/dark, 320px, 200% zoom, tab through links, contrast of `--muted` on `--card` and link colours both themes (≥4.5:1), no console errors. Record results in decisions log.

## Task 8: Launch checklist (no code here)
Write into decisions log, do not execute: (1) app repo link `https://saeed265310.github.io/keepawhile-privacy/` → `.../privacy-policy.html` (3 files seen in grep: README/docs + Dart settings link) and release; (2) Play Console privacy policy URL → `/privacy-policy.html`; (3) replace STORE-LINK span in index/features with `<a>` once listing is live; (4) re-run `--strict`.

## Task 9: Merge gate (merge = deploy)
GitHub Pages builds from `main` `/` on push. Merging the branch publishes immediately.
Merge only when ALL true: (1) `python3 scripts/check_site.py --strict` passes (all screenshots present) OR Task 6 fallback applied: imgs of missing shots removed from pages and default run passes with zero WARN; (2) Task 7 manual checks recorded; (3) owner confirmed User decision U2 (root URL switch timing). Executor never merges or pushes `main`; owner does.

## Ordering
0 → 1 → 2 → 3 → 4 → 5 → (6 when PNGs exist) → 7 → 8 → 9. Task 3 MUST precede Task 4 (Task 4 overwrites the only current copy of the policy in the working tree; baseline then comes from git `5b38476` regardless). Tasks 4,5 independent after 3. One commit per task on `feature/marketing-website`.

## Risks
- Root URL change breaks any already-installed build's policy link → app unpublished, accepted; do launch checklist first.
- Legal text drift → check 5 gate.
- GitHub Pages serves stale cache briefly after deploy.

## Plan Critique
Critique effort: HIGH
Critique status: PASSED
Restore point: 5b384766a2a25a12c535b1e655f7585267f369e9
Plan hash (pre-critique): 0c06d128e15f4deb4ed32c1edeb6173401311932c27e38377b3aecc1de23c89c
Plan hash (hardened): 84c0fded03db7871d4f82a3be0771c9d49488ab8746e54b5354905d1240b6068

### Mandatory probes
1. Partial state: all work on branch; stopping after any task leaves `main`/live site untouched. Only unsafe gap was Task 4 before Task 3 → ordering made mandatory; baseline is git `5b38476`, so even that is recoverable. Resume = rerun check script, continue at first failing task.
2. Both orders: no JS, no concurrency. Only order risk = owner merging (deploy) before vs after app/Play URL switch → U2, Task 9.
3. Version skip: no stored data. Any already-installed build (internal testing) links root as policy → after merge shows landing page with Privacy link one tap away → U2.
4. Evidence quotes: in each risk below.
5. Owner decisions: U1–U3 below.

### User decisions
- U1: ANSWERED yes 2026-10-23. Done: commit 1691a73 on `main` (pushed) — `privacy-policy.html` = Oct 22 policy, byte-identical to `index.html`. Branch fast-forwarded to it.
- U2: ANSWERED yes 2026-10-23 — merge only after the switch below. Original question: When to switch root to landing page: after app link + Play Console privacy URL (and Data safety form URL if set) change to `/privacy-policy.html`, and after any internal-test build is replaced? Merge waits for this.
- U3: ANSWERED 2026-10-23 — drop Apple Maps everywhere; keep on-device OCR/entity extraction and Arabic/RTL claims. TRD §1 group 5 updated; banned list gains "Apple Maps".

### Ranked Risks
### Risk 1: Terms page's privacy link lands on marketing page — Critical, score 80
- Failure mode: `terms.html` links `https://saeed265310.github.io/keepawhile-privacy/` as the privacy policy; after Task 4 that URL is the landing page. Legal cross-reference silently breaks.
- Evidence: plan Task 4 "`index.html` (replaces policy copy; policy lives in `privacy-policy.html`)"; `terms.html` href found by grep.
- Impact / likelihood / detection: 4 / 5 / 4.
- Plan weakness: Task 3 said "Do NOT edit legal text" and no task touched hrefs; check 1 only validates relative links, so absolute root link passes.
- Mitigation: Task 3 REQUIRED link fix + grep assertion; pre-authorized in decisions log.
- Plan changes: Task 3.
- Verification: Task 3 grep; check 5 still passes.
- Residual risk: external pages/emails quoting the root URL as "privacy policy" (out of repo).
### Risk 2: Stale policy published as canonical — High, score 60
- Failure mode: policy text taken from current `privacy-policy.html` (Oct 12) instead of `index.html` (Oct 22); vCard mirror disclosure lost.
- Evidence: plan "Baseline for legal text = git `HEAD` of `privacy-policy.html`" (pre-critique, already corrected at architect step).
- Impact / likelihood / detection: 5 / 3 / 4.
- Plan weakness: correctness relied on one sentence; nothing proved the check catches drift.
- Mitigation: Task 0 checkpoint must show check 5 FAILING on current `privacy-policy.html`; baseline pinned to commit `5b38476`.
- Plan changes: Task 0 checkpoint, check 5 definition.
- Verification: TDD Evidence entry for Task 0 and Task 3.
- Residual risk: future policy edits must go to `privacy-policy.html` (not `index.html`) — note for whoever syncs the policy.
### Risk 3: Checks pass trivially — Medium, score 36
- Failure mode: link/colour/claim checks never exercised (current pages have no relative links) → green with bugs.
- Evidence: Task 0 "Checkpoint: run on current tree → must FAIL on check 6".
- Impact / likelihood / detection: 3 / 3 / 4.
- Mitigation / changes: `--selftest` fixture forcing checks 1,2,4,6 to FAIL.
- Verification: Task 0 checkpoint (a). Residual: check 7 and 3 not in fixture (low).
### Risk 4: Merge deploys broken/early site — Medium, score 36
- Failure mode: merge before screenshots or before URL switch → broken images live, or policy URL shows landing.
- Evidence: plan "Task 6 ... Depends on user delivering PNGs"; no merge gate existed.
- Impact / likelihood / detection: 4 / 3 / 3.
- Mitigation / changes: Task 9 merge gate; executor never merges.
- Verification: Task 9 checklist. Residual: owner overrides gate.
### Risk 5: Claims about unverified features — Medium, score 36
- Failure mode: site promises Smart Capture/OCR/Arabic behaviour that is "Code-complete ... Not device-verified" (PROJECT_SCOPE §5).
- Evidence: TRD §1 group 5 "on-device OCR/entity extraction", group 7 "Arabic/RTL support".
- Impact / likelihood / detection: 3 / 3 / 4.
- Mitigation: owner decision U3 (answered: Apple Maps dropped, OCR + Arabic kept); banned list extended with iOS/App Store/Apple Maps.
- Verification: Task 5 copy reviewed against U3 answer. Residual: features regress before launch.
### Risk 6: Check 3 forces legal-link edits — Medium, score 30
- Failure mode: original check 3 allowed only google/play links → Overture/Foursquare attribution links fail → executor edits legal text or weakens check.
- Evidence: plan "`http(s)://` allowed only in `<a href>` to google/policies/play.google.com".
- Impact / likelihood / detection: 3 / 5 / 2.
- Mitigation / changes: check 3 now targets resource loads only.
- Verification: Task 3 run passes with attribution links intact. Residual: none known.
### Risk 7: Dark-mode link contrast fails AA — Medium, score 20
- Failure mode: `--accent` #2563EB text on #0B0F17 ≈ 3.6:1.
- Evidence: TRD §1 dark `--accent #2563EB`; TRD §4 "Fallback: use `--accent-2` for dark link text".
- Impact / likelihood / detection: 2 / 5 / 2.
- Mitigation / changes: Task 2 makes `--accent-2` mandatory for dark links.
- Verification: Task 7 contrast check. Residual: muted text on subtle cards unmeasured until Task 7.
### Other
Check 2 would flag `theme-color` meta and `#anchor` hrefs (fixed: scoped to style contexts); feature graphic 675KB as og image (acceptable, not on page); vCard folder name differs between PROJECT_SCOPE (`TidyContacts`) and policy (`KeepAwhile`) — site copy must not name the folder.

### Risk-to-Task Mitigation Map
| Risk | Mitigating task(s) | Verification | Residual risk |
|------|--------------------|--------------|---------------|
| 1 Terms link | 3 | grep + check 5 | external quotes of root URL |
| 2 Stale policy | 0, 3 | check 5 FAIL→PASS evidence | future edits to wrong file |
| 3 Trivial checks | 0 | `--selftest` | checks 3,7 unfixtured |
| 4 Early deploy | 6, 9 | merge gate | owner override |
| 5 Unverified claims | 5 (+U3) | copy review | regressions |
| 6 Check 3 scope | 0 | Task 3 run | none known |
| 7 Dark contrast | 2, 7 | manual contrast | muted-on-subtle |

### Critique Change Log
- Task 0: bash+python → single `scripts/check_site.py`; added `--selftest`; checks 2,3,4,5 tightened; checkpoint requires check 5 FAIL on stale policy.
- Task 1: dropped favicon downscale.
- Task 2: dark link token mandatory; contrast numbers recorded.
- Task 3: required `terms.html` privacy href fix.
- Task 4: dropped Twitter meta; OG URLs absolute.
- Added Task 9 merge gate; ordering 3 before 4 mandatory.

- Amendment 2026-10-23 (post-critique, owner answers U1–U3): check-5 proof moved into `--selftest` because hotfix 1691a73 removed the stale file; "Apple Maps" banned; plan hash recomputed. No risk re-ranked.

### Complexity Decision
**Removed:** bash wrapper, favicon copy, Twitter meta tags.
**Retained:** check script (only automated test layer; guards legal text), `--selftest` (prevents trivial pass), self-hosted fonts (TRD: no third-party requests), separate `features.html` (ADR).
