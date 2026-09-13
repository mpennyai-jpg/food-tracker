# The Claude appraisal system on Todd's laptop

One-line summary: the working digital twin of the practice lives on the Windows laptop under `C:\Users\toddp\.claude\` as house rules, skills, scripts, and data paths. This indexes it so any session knows what exists and where. Source: Penny's orientation file for Kenneth, 2026-09-13 (`source-2026-09-13-starting-a-file-for-kenneth.md`).

## Two named sessions

- **Kenneth**: Claude in the desktop app on the laptop.
- **Penny**: Claude in a terminal (WSL) session on the laptop. Penny wrote the orientation file. The Penny Share OneDrive folder is named for this session.
- Both read the same `C:\Users\toddp\.claude\` files. Cloud sessions (like the one that built this repo) read only this repo.

## Rules that override defaults, read every time

| File | What it holds |
|---|---|
| `appraisal\house-rules.md` | Voice rules; the refusal gate (never state a number the data cannot carry); the one-assignment-at-a-time isolation rule; where output goes; the plain-English rule for anything that goes on the form |
| `appraisal\uspap-citations.md` | Why every skill produces a WORKFILE document and a REPORT document |
| `appraisal\zoning\` | Local copies of county and city zoning ordinances. Read its README first: versions, source URLs, which counties are missing. Never infer zoning from surrounding use |

## Two entry points to start a file

**`/prep`**: drop an address and prep the whole file.
- `commands\prep.md`
- `skills\report-prep\SKILL.md`
- `skills\report-prep\references\run-order.md`
- `skills\report-prep\references\gap-matrix.md`

**workup**: the pre-report analysis package.
- `skills\workup\SKILL.md`
- `skills\workup\references\discovery.md`: the actual "how to start a file" document. Job folder, then tracker record, then MLS export, in that order, plus how to pull attachments out of the tracker backup.
- `references\inputs-and-gaps.md`
- `references\method-market.md`
- `references\method-comps.md`
- `references\document-shape.md`
- `scripts\` (stdlib only, no pandas or numpy):
  - `from_tracker.py` builds the Part 1 skeleton from the order
  - `prep.py` turns a RealTracs export into the worked CSV
  - `ols.py` regressions
  - `build_workup.py` builds WORKUP.html. Never hand-write the nav.

## Other skills

All under `skills\`: final-read, neighborhood-description, highest-and-best-use, exposure-marketing-time, site-improvements, overall-quality-condition, sales-contract-analysis, daily-brief, email.

## Where the data lives

| What | Where |
|---|---|
| Job folders | `C:\Users\toddp\OneDrive\Desktop\<address> <MM-DD> <client>` |
| Shared drop folder | `C:\Users\toddp\OneDrive\Penny Share\`. Todd drops MLS exports, orders, contracts, and field reports here; some job folders live here too |
| Tracker backups | `C:\Users\toddp\OneDrive\Appraisal Tracker\Appraisal Tracker - Backups\`. Take the newest file by modified time, not by name |
| Letterhead logo | `C:\Users\toddp\OneDrive\Appraisal Tracker\pinewood-logo.png` |
| UAD 3.6 answer book | `C:\Users\toddp\OneDrive\Desktop\UAD 3.6\Appendix F-1 URAR Reference Guide v1.2.pdf` |

## Hard rules

- Do not create a job folder, and never create a new top-level OneDrive folder from the laptop. It jams sync against the desktop machine. If no folder exists, ask where it is.
- One assignment at a time (house rules).
- Never state a number the data cannot carry (refusal gate).
- Gate the legally-permissible test on zoning rather than inferring it.

## Traps in terminal (WSL) sessions, not in the desktop app

- Skill docs use Windows paths. `build_workup.py --logo "C:/Users/..."` silently produces a logo-less document because os.path.exists returns False. Pass `/mnt/c/Users/toddp/OneDrive/Appraisal Tracker/pinewood-logo.png`.
- Chrome headless reads `C:\...\file.html#anchor` as a literal filename and renders a blank page. Use `file:///C:/.../file.html#anchor`.
- `build_workup.py` does not emit the Part 3 divider. End the body fragment with `<div class="part">Part 3 — The workfile analysis behind each narrative</div>` or the sidebar has only two nav groups.

## Document shape

WORKUP.html has three parts with a sidebar nav: Part 1 skeleton from the order, Part 2 (contents not yet captured here), Part 3 the workfile analysis behind each narrative. Every skill produces a WORKFILE document and a REPORT document.

## Systems named

- Appraisal Tracker: order tracking, backups on OneDrive feed the workup scripts.
- RealTracs: the MLS. Exports go to Penny Share and through prep.py.
- UAD 3.6 / URAR: the form standard in use.
- Two machines, laptop and desktop, synced by OneDrive.
- Public data endpoints: see `public-data-endpoints.md`.

## What this means for the brain

The laptop system is the real twin. As of 2026-09-13 the files themselves are mirrored in this repo under `laptop/`: the global `CLAUDE.md`, `appraisal/` (minus the zoning PDFs, listed in `laptop/appraisal/zoning/PDFS-NOT-IN-REPO.md`), `commands/`, and `skills/`. The laptop copy is live; `laptop/` is the versioned mirror. When they differ, the laptop wins until Kenneth re-copies.
