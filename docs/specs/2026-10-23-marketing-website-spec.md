# Keep Awhile Marketing Website Technical Requirements

ADR: `docs/specs/2026-10-23-marketing-website-adr.md`. Screenshot prompt: `docs/specs/2026-10-23-website-screenshots-prompt.md`.

## 1. Visuals & Layout
- Files: `index.html`, `features.html`, `privacy-policy.html`, `terms.html`, `assets/style.css`, `assets/fonts/`, `assets/icon.png`, `assets/screenshots/`.
- Look: match app. Tokens copied from `SuperContacts-orca/lib/core/theme/app_palette.dart`.
- Font: Plus Jakarta Sans 400/600/700/800, self-hosted `.ttf` from `SuperContacts-orca/assets/fonts/` (OFL, ship `OFL.txt`). `font-display: swap`. Fallback system-ui stack.
- Colour tokens (CSS custom properties on `:root`, dark under `prefers-color-scheme`):
  - light: `--bg #F1F5F9`, `--card #FFFFFF`, `--card-subtle #E8EEF5`, `--text #090E17`, `--muted #475569`, `--accent #2563EB`, `--accent-2 #0369A1`, `--border rgba(15,23,42,.13)`, `--on-accent #FFFFFF`.
  - dark: `--bg #0B0F17`, `--card #161E2B`, `--card-subtle #0F1520`, `--text #F1F5F9`, `--muted #94A3B8`, `--accent #2563EB`, `--accent-2 #38BDF8`, `--border rgba(255,255,255,.13)`.
  - no raw colours outside `:root`.
- Radius: card 12px, row 10px, button 8px, sheet/phone 20px.
- Layout: single column max-width 1040px, 16px side gutter. Sections stack. Feature rows: text + phone screenshot, 2 columns at ≥ 800px, 1 column below, screenshot under text.
- Pages:
  - `index.html`: header → hero → "Temporary contacts" (headline, shot 02) → "Remember everything" (shots 04, 05) → "Nothing leaves without you" (shot 03) → "Find anything" (shot 07) → "Your data stays yours" strip (text only) → FAQ → footer.
  - `features.html`: grouped list (below), each group with 1 screenshot where one exists.
  - policy/terms: keep body unchanged. Replace inline `<style>` with `style.css`; add header/footer. Verify text diff is zero.
- Header: icon + "Keep Awhile" wordmark, links Home / Features / Privacy / Terms. Current page `aria-current="page"`. Mobile: links wrap inline, no hamburger, no JS.
- Hero CTA: disabled-looking "Coming soon on Google Play" `<span>`, not a link. Marked in one place per page: `<!-- STORE-LINK -->`. Launch swap = replace span with `<a href="https://play.google.com/store/apps/details?id=app.keepawhile">`.
- No App Store button. No iOS claim. Footer states "Android first".
- No pricing, tiers, subscription, AI claims, ads-removal claims.
- New patterns: phone frame (CSS border + radius around `<img>`), none other.

### Content (source: PROJECT_SCOPE §1, §3, §5; only shipped / code-complete features)
Hero: "Keep them for a while. Then let them go." Sub: "A contacts app for the plumber, the hotel, the one-off electrician. Reachable now, out of the way later, never deleted."
Feature groups for `features.html`:
1. Temporary contacts: set time-to-live, time-left badge, Timed tab, bulk Make timed / Extend / Keep.
2. Asks before it acts: expiry notification sheet, deactivation removes contact from phone address book and keeps full copy in app, one-tap restore.
3. Relationship memory: per-contact timeline, free-form notes, typed notes (5 seeded + custom, 8 colours), pinned notes (max 3), photo/file attachments.
4. Find anything: search contacts, note text, note types; global Timeline with search; in-app settings search.
5. Smart Capture: share a place from Google Maps → name, phone, hours via "Get business info"; on-device OCR/entity extraction. Never mention Apple Maps (owner, 2026-10-23).
6. Safety: vCard safety backup (plaintext, on device), encrypted passphrase DB export, Recovery Center with snapshots, merge duplicates, cleanup suggestions.
7. Built for travel and language: country-aware numbers, travel mode with location tags on notes, Arabic/RTL support.
8. Two modes: Full CRM view or Safe Ledger (onboarding choice).
Claims rules:
- say "your contacts stay on your device". never "we collect nothing", "no ads", "no tracking".
- ads disclosure sentence in FAQ: free version shows ads; ad and analytics SDKs run on device; contact and note content stays on device.
- vCard backup copy: "plaintext, saved on your device" vs "encrypted export" never merged.
- no feature dates, no roadmap items (voice memo, reminders, projects, iOS).
- Platform: Android 10+. "iPhone version planned" omitted.
FAQ (5): Where is my data? Does it work offline? What happens when a contact expires? Does it cost anything? → answer "Free to start; details at launch" (no numbers). Can I get my contacts back?

## 2. State Machine
Static pages, no app state.
- Empty (no screenshots present): `<img>` files missing → page shows `alt` text in a bordered phone frame. No placeholder text visible to users. Pre-launch rule: all shipped `<img>` must exist (see §7).
- Loading: fonts swap, images `loading="lazy"` except hero; explicit `width`/`height` to avoid layout shift.
- Error: broken image → alt text. Broken link → none expected; checked in §7.
- Happy path: land on index → read hero → scroll features → open features.html or Privacy/Terms via header.
- Interactions: links only. Hover/focus underline + `:focus-visible` outline 2px `--accent`. No JS.
- Transitions: none. Respect `prefers-reduced-motion` (no animation added).

## 3. Data Integration
- Source: none. No forms, no analytics, no cookies, no third-party requests (fonts self-hosted).
- Models: none.
- Access: read-only.
- Contact: `mailto:saeed201@gmail.com` link in footer and policy (existing).

## 4. Accessibility & Localization
- RTL: English only now. Use logical CSS properties (`margin-inline`, `padding-inline`, `text-align: start`) so `dir=rtl` later is cheap. `<html lang="en">`.
- Semantics: `<header>`, `<nav aria-label="Main">`, `<main>`, `<section aria-labelledby>`, one `<h1>` per page, ordered headings. Screenshots: descriptive `alt` ("Temporary tab listing contacts with days left"). Decorative icon `alt=""`.
- Touch targets: nav links and buttons ≥ 44×44px.
- Contrast: all text ≥ 4.5:1 in both themes. Check `--muted` on `--card` and `--accent` text on `--bg` dark. Fallback: use `--accent-2` for dark link text.
- Text scale: layout survives 200% zoom and 320px width, no horizontal scroll.
- Fonts: Plus Jakarta Sans only.
- Skip link "Skip to content" first in body.
- SEO/meta per page: `<title>`, `meta description`, `og:title`, `og:description`, `og:image` (feature graphic 1024x500), `theme-color`, favicon from app icon.

## 5. Failure registry
| operation | fails how | user sees | state on disk | recovery |
|---|---|---|---|---|
| load `style.css` | 404 / path wrong | unstyled HTML, still readable | none | relative paths only, test via local server |
| load font | 404 | system font | none | fallback stack |
| load screenshot | missing | alt text in frame | none | §7 check |
| nav link | typo | 404 | none | §7 link check |
| policy page migration | style swap alters text | changed legal text | git history | diff body text before/after must be empty |

## 6. Async and ordering
None. No JS, no concurrent actions. Only deploy-order risk: publishing site before screenshots exist (see §7) and publishing before app launch with a live store link (placeholder is non-link).

## 7. Test matrix
| behaviour | unit | widget | integration | device |
|---|---|---|---|---|
| all internal links resolve | n/a | n/a | covered (script: grep hrefs, check files exist) | n/a |
| all `<img src>` exist | n/a | n/a | covered (same script) | n/a |
| policy/terms body text unchanged | n/a | n/a | covered (diff text of `<body>` before/after) | n/a |
| no raw colour outside `:root` | n/a | n/a | covered (grep) | n/a |
| no external requests | n/a | n/a | covered (grep `https://` in src/href/@import, allow store/mailto/policy links) | n/a |
| light/dark render | n/a | n/a | gap (manual in browser) | n/a |
| 320px, 200% zoom no h-scroll | n/a | n/a | gap (manual) | gap (real phone) |
| contrast 4.5:1 | n/a | n/a | gap (manual, devtools) | n/a |
| claims rules (no "we collect nothing", no pricing words) | n/a | n/a | covered (grep) | n/a |
No data-writing rows. Gaps are manual checks at verify step.

## 8. Open Questions for Architect
- Hosting: GitHub Pages from `main` root? Confirm no custom domain / canonical URL needed yet.
- `og:image` absolute URL needs final domain. Use relative until domain known?
- Screenshots arrive later: build with real filenames, ship page only when files present (or temporary 1-line `.gitkeep` + failing link check as gate).
- Keep `index.html` policy copy anywhere? Current `index.html` duplicates privacy text; `privacy-policy.html` remains canonical. Confirm old URL `/` content moving is fine for store listing (Play privacy-policy URL may point at `/`).
