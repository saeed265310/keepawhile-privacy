# ADR: Keep Awhile marketing website

Date: 2026-10-23 · Branch: `feature/marketing-website` · Status: proposed (awaiting user review)

## Context
The repo is a three-file static site (`index.html`, `privacy-policy.html`, `terms.html`). `index.html` is currently a copy of the privacy policy. The goal is a full site that showcases the app (Keep Awhile / SuperContacts) and its features. Product truth lives in `SuperContacts-orca/docs/PROJECT_SCOPE.md`.

## Decision
Plain static HTML/CSS, no build step, no JS framework.

Pages:
- `index.html` — landing: hero (tagline, Play Store button), headline feature (temporary contacts), relationship memory, privacy-first strip, screenshots, FAQ, footer.
- `features.html` — each feature in depth, with screenshots.
- `privacy-policy.html`, `terms.html` — unchanged in content; get the shared header/footer.
- `assets/style.css` — one shared stylesheet. Reuses the existing light/dark tokens.
- `assets/` — app icon (from `SuperContacts-orca/docs/branding/icon`), feature graphic, screenshots.

Navigation: header with Home / Features / Privacy / Terms, repeated by hand in each file. Four pages makes that cheaper than a generator.

## Constraints
- Copy follows PROJECT_SCOPE §3. Say "your contacts stay on your device", never "we collect nothing" (the free tier carries ads). Hiding a contact removes it from the phone, and Keep Awhile holds the only copy.
- No claims about features, pricing or platforms that are not in PROJECT_SCOPE or a store listing. The tiers are unconfirmed.
- Play Store link `https://play.google.com/store/apps/details?id=app.keepawhile` is correct, but the app is NOT published yet. The button reads "Coming soon" and is not a link until launch. Swapping it for the live link is a one-line change, so keep it in one place per page.
- iOS: no link given. Show no App Store button.
- Screenshots: captured from the emulator into `assets/screenshots/`. Until then, use labelled placeholders.
- Responsive and accessible: semantic HTML, alt text, `prefers-color-scheme` dark mode, readable at 360px width.

## Alternatives rejected
- Static site generator (Astro/Eleventy): shared layouts are nice, but it adds a build and deploy pipeline for four pages.
- Single long page only: weaker for the store's "website" field and for linking to a specific feature.

## Decided
- Pricing and tiers are left off the site for now.
- Screenshots come from the emulator: `2026-10-23-website-screenshots-prompt.md`.

## Open items for the spec step
- Exact feature list and wording (pull from PROJECT_SCOPE and the wiki Roadmap).
- Contact/support email (currently saeed201@gmail.com in the policy).
- Domain/hosting and canonical URLs.
