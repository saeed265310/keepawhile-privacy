# Prompt for the SuperContacts repo controller — website screenshots

Paste everything below the line into the controller session running in `~/projects/SuperContacts-orca`.

---

## Task
Capture 10 raw app screenshots from the Android emulator for the Keep Awhile marketing website. Do not publish or commit anything in SuperContacts-orca. Only write PNGs to the output folder below and report back.

Output folder (create it): `/home/saeed/projects/keepawhile-privacy/assets/screenshots/`
Format: PNG, portrait, one file per shot, named exactly as listed. Do not compose, frame or caption them. The website adds its own phone frames.

## Emulator setup
- Pixel-class phone, 1080x2400, API 34 or similar, light theme, English (en-US), 100% font scale.
- Clean status bar: `adb shell settings put global sysui_demo_allowed 1`, then demo-mode broadcasts. Use full battery, full Wi-Fi, 9:41 clock, no notification icons.
- Run the debug build. Hide the AdMob banner and interstitials if a flag, test build or debug setting allows it. Otherwise capture normally and tell me which shots show the banner so I can crop them.
- Use screencap, for example `adb exec-out screencap -p > file.png`. Do not use the Flutter driver's scaled output.

## Demo data
Seed fictional data only. No real names, numbers, photos or addresses. Use 555-01xx numbers and generated or illustrated avatars.

Contacts (about 14): Maria the Plumber (timed, 3 days left), Hotel Alhambra (timed, 12 days left), Sam, Electrician (timed, 1 day left), Dr. Okafor, Mom, Jess Rivera, Auto Repair Bay 7, and a few more. Pin 3 of them.
Notes on "Maria the Plumber", with these note types and colours:
- pinned: "Quoted $180 for the kitchen tap. Cash on the day."
- "Lent her my pipe wrench - she'll bring it back Friday."
- one note with a photo attachment (a serial-plate or receipt image, generated, not a real person)
- 5 or more notes so the date grouping is visible: Pinned, then Today, This week, Earlier.
Timeline needs at least 12 notes across 5 or more contacts.
One contact must have expired, so the expiry prompt is pending.
Two contacts must be deactivated, so the Recovery list is not empty.
Two duplicate contacts for Merge duplicates.

## Shots (name — screen — what must be visible)
1. `01-contacts-home.png` — Contacts tab, Recipe 02 main screen. Pinned grid at the top, alphabetical list below, bottom dock with the 4 tabs, search field with the bell.
2. `02-temporary.png` — Temporary (Timed) tab. Several contacts with their time-left badges (1 day, 3 days, 12 days). This is the headline feature.
3. `03-expiry-nudge.png` — Notifications sheet, open. The pending decision for the expired contact, with the ask-first wording and the Keep / Hide actions. The key point is that nothing happens without the user's say.
4. `04-contact-detail.png` — Maria the Plumber contact detail (Recipe 01): header, pinned note on top, notes grouped by date, coloured type brackets.
5. `05-note-view.png` — a note opened in the read-only note sheet, with its photo attachment showing.
6. `06-note-types.png` — Manage note types screen with the colour palette, or the composer showing the type picker. Pick whichever is more legible.
7. `07-global-timeline.png` — Timeline tab, with the search field containing a word like "wrench" and the matching notes plus the count chip visible.
8. `08-smart-capture.png` — Smart Capture from a shared map place: the "Get business info" candidate screen (name, phone, hours). Use a fictional business. If it needs the HERE backend and is not reachable from the emulator, skip it and say so.
9. `09-organize.png` — Organize tab: Backup, vCard safety backup, Recovery, Merge duplicates, Cleanup suggestions.
10. `10-recovery-restore.png` — Recovery Center, listing deactivated contacts with the one-tap Restore control.

Also capture `11-contacts-home-dark.png`, the same as shot 1 in dark theme. Skip it if it looks wrong.

## Rules
- Never show a real contact, the emulator's own address book, or a Google account.
- If a screen cannot be reached, skip it and list it with the reason. Do not fake it.
- Do not change app code. If seeding needs a script, put it in the scratchpad or `/tmp`, not in the repo.

## Report back
For each file: the path, the pixel size, and whether the ad banner is visible. Then a list of skipped shots with reasons.
