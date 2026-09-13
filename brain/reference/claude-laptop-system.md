# The Claude appraisal system on Todd's laptop

One-line summary: months of work with Claude live on the Windows laptop under `C:\Users\toddp\.claude\`, as house rules, skills, scripts, and data paths. This file indexes that system so any session knows it exists and where to look. Recorded from Todd's global CLAUDE.md, pasted 2026-09-13; lines the paste cut off are marked (truncated).

## Rules that override defaults, read every time

- `C:\Users\toddp\.claude\appraisal\house-rules.md`: voice rules, the refusal gate (never state a number the data cannot carry), the one-assignment-at-a-time isolation rule, where output goes, and the plain-English rule for anything that goes on the form.
- `C:\Users\toddp\.claude\appraisal\uspap-citations.md`: why every skill produces a workfile document. (truncated)
- `C:\Users\toddp\.claude\appraisal\zoning\`: local copies of county and city zoning. Read the index there first; it lists versions, source URLs, and which counties are missing. Never infer zoning from surrounding parcels. (truncated)

## Two entry points to start a file

**`/prep`**: drop an address and prep the whole file.
- `C:\Users\toddp\.claude\commands\prep.md`
- `C:\Users\toddp\.claude\skills\report-prep\` with `references\run-order.md` (other references truncated)

**workup**: the pre-report analysis package.
- `C:\Users\toddp\.claude\skills\workup\SKILL.md`
- A reference doc that is the actual "how to start a file" procedure: job folder, then tracker record, then MLS export, then pulling attachments out of the tracker backup. (filename truncated)
- `references\method-market.md`
- `references\document-shape.md`
- Scripts (stdlib only, no pandas or numpy):
  - `from_tracker.py` builds the Part 1 skeleton from the order
  - `prep.py` turns a RealTracs export into working data (truncated)
  - `ols.py` regressions
  - `build_workup.py` builds the WORKUP document with nav

## Other skills

All under `C:\Users\toddp\.claude\skills\`: final-read, neighborhood-description, highest-and-best-use, exposure-marketing-time, site-improvements, sales-contract-analysis, daily-brief, email.

## Where the data lives

| What | Where |
|---|---|
| Job folders | `C:\Users\toddp\OneDrive\...\<client>` (path truncated) |
| Shared drop folder | `C:\Users\toddp\OneDrive\Penny Share\` (Todd drops MLS exports and reports here; some job folders live here too) |
| Tracker backups | `C:\Users\toddp\OneDrive\...\Appraisal Tracker - Backups\`. Take the newest file by date; sorting by filename picks the wrong one. |
| Letterhead logo | `C:\Users\toddp\OneDrive\Appraisal Tracker\pinewood-logo.png` |
| UAD 3.6 answer book | `C:\Users\toddp\OneDrive\Desktop\UAD 3.6\` including Appendix F-1 URAR reference |

## Hard rules

- Do not create a job folder, and never create one from this laptop. It jams OneDrive sync against the desktop machine. If no folder exists, ask where it is.
- One assignment at a time. Isolation rule from house-rules.

## Gotchas learned from real runs (WSL on the laptop)

- Paths in the skill docs are Windows-style. Passing `--logo "C:/Users/..."` to build_workup.py silently produces a logo-less document because os.path.exists returns False. Pass `/mnt/c/Users/toddp/OneDrive/Appraisal Tracker/pinewood-logo.png` instead.
- Opening a `file.html#anchor` argument gets read as a literal filename and renders a blank error page. Use a real `file:///C:/.../file.html#anchor` URL.
- The builder does not emit the Part 3 divider on its own. End the body fragment with `<div class="part">Part 3 — The workfile analysis behind each narrative</div>` or the document renders with only two nav groups.

## Document shape (as far as known)

Workup documents have three parts: Part 1 skeleton from the order, Part 2 (unknown), Part 3 the workfile analysis behind each narrative. Nav groups per part. Detail is in `document-shape.md` on the laptop.

## Systems named

- Appraisal Tracker: the order tracking system with backups on OneDrive. A tracker record is step two of starting a file.
- RealTracs: the MLS. Exports are dropped in Penny Share and consumed by prep.py.
- UAD 3.6 / URAR: the new form standard he is working under.
- Two machines: this laptop and a desktop, synced by OneDrive.

## What this means for the brain

The skills and rules on the laptop are the real digital twin of the practice today. This repo does not yet contain them. The next step is to copy `C:\Users\toddp\.claude\appraisal\`, `commands\`, and `skills\` into this repo so they are versioned, backed up, and available to web sessions. Until then, laptop sessions have the full system and web sessions have only this index.
