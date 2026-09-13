# Source: STARTING A FILE, instructions for Kenneth (written by Penny, 2026-09-13)

One-line summary: verbatim copy of the orientation file Penny wrote for Kenneth. Kept as a source; the working index is `claude-laptop-system.md`.

---

# Starting a Pinewood Appraisal file — orientation for a fresh Claude session

Written by Penny (terminal session), 2026-09-13, for Kenneth or any other
Claude session that needs to pick up a file.

Paste the block below into a new session, or just point the session at this
file.

---

## The instruction block

```
You are working on Pinewood Appraisal files for Todd A. Paris, a certified
residential appraiser in Murfreesboro TN. Everything you need is already on
this machine under C:\Users\toddp\.claude\ — read it before you do anything.

READ FIRST, EVERY TIME — these override your defaults:
  C:\Users\toddp\.claude\appraisal\house-rules.md
      Voice rules, the refusal gate (never state a number the data cannot
      carry), the one-assignment-at-a-time isolation rule, where output goes,
      and the plain-English rule for anything that goes on the form.
  C:\Users\toddp\.claude\appraisal\uspap-citations.md
      Why every skill produces a WORKFILE document and a REPORT document.
  C:\Users\toddp\.claude\appraisal\zoning\
      Local copies of county and city zoning ordinances. Read the README
      there first — it lists versions, source URLs, and which counties are
      missing. Never infer zoning from surrounding use.

TO START A FILE, use one of two entry points:

  /prep  — drop an address and prep the whole file
      C:\Users\toddp\.claude\commands\prep.md
      C:\Users\toddp\.claude\skills\report-prep\SKILL.md
      C:\Users\toddp\.claude\skills\report-prep\references\run-order.md
      C:\Users\toddp\.claude\skills\report-prep\references\gap-matrix.md

  workup — the pre-report analysis package
      C:\Users\toddp\.claude\skills\workup\SKILL.md
      C:\Users\toddp\.claude\skills\workup\references\discovery.md   <-- THIS
          is the actual "how to start a file" document: job folder, then
          tracker record, then MLS export, in that order, plus how to pull
          attachments out of the tracker backup.
      C:\Users\toddp\.claude\skills\workup\references\inputs-and-gaps.md
      C:\Users\toddp\.claude\skills\workup\references\method-market.md
      C:\Users\toddp\.claude\skills\workup\references\method-comps.md
      C:\Users\toddp\.claude\skills\workup\references\document-shape.md
      C:\Users\toddp\.claude\skills\workup\scripts\
          from_tracker.py   builds the Part 1 skeleton from the order
          prep.py           turns a RealTracs export into the worked CSV
          ols.py            regressions, stdlib only (no pandas/numpy here)
          build_workup.py   builds the WORKUP.html — never hand-write the nav

OTHER SKILLS, all under C:\Users\toddp\.claude\skills\:
  final-read, neighborhood-description, highest-and-best-use,
  exposure-marketing-time, site-improvements, overall-quality-condition,
  sales-contract-analysis, daily-brief, email

WHERE THE DATA LIVES:
  Job folders          C:\Users\toddp\OneDrive\Desktop\<address> <MM-DD> <client>
  Shared drop folder   C:\Users\toddp\OneDrive\Penny Share\
                       (Todd drops MLS exports, orders, contracts and field
                        reports here; some job folders live here too)
  Tracker backups      C:\Users\toddp\OneDrive\Appraisal Tracker\
                       Appraisal Tracker - Backups\
                       Take the NEWEST file by modified time, not by name —
                       sorting by filename picks the wrong one.
  Letterhead logo      C:\Users\toddp\OneDrive\Appraisal Tracker\pinewood-logo.png
  UAD 3.6 answer book  C:\Users\toddp\OneDrive\Desktop\UAD 3.6\
                       Appendix F-1 URAR Reference Guide v1.2.pdf

DO NOT create a job folder, and never create a new top-level OneDrive folder
from this laptop — it jams sync against the desktop machine. If no folder
exists, ask where it is.
```

---

## Two traps that cost me time on 2026-09-13

**Paths in the skill docs are Windows-style, but a WSL terminal session needs
WSL paths.** `build_workup.py --logo "C:/Users/..."` silently produces a
logo-less document, because `os.path.exists` returns False. Pass
`/mnt/c/Users/toddp/OneDrive/Appraisal Tracker/pinewood-logo.png` instead.
Same trap in Chrome headless: a `C:\...\file.html#anchor` argument is read as a
literal filename and renders a blank error page — use a real
`file:///C:/.../file.html#anchor` URL. (Kenneth on the desktop app does not hit
this; it is a terminal-side problem.)

**`build_workup.py` does not emit the Part 3 divider on its own.** End the body
fragment with
`<div class="part">Part 3 — The workfile analysis behind each narrative</div>`
or the sidebar comes out with only two nav groups.

---

## Public data endpoints that work, keyless

Worth keeping — these took a while to rediscover.

- **TN statewide parcels:**
  `https://services1.arcgis.com/YuVBSS7Y1of2Qud1/arcgis/rest/services/Tennessee_Property_Boundaries_Public_Use/FeatureServer/0/query`
  Query `where=COUNTY_NAME='LINCOLN' AND ADDRESS LIKE '%<street>%<number>%'`.
  Address strings are stored street-first, e.g. `OLD ELKTON PIKE 839`.
  Returns GISLINK, PARCELID, deed acres, owner, subdivision, lot, and a
  LINK_TPAD URL.
- **TPAD parcel detail:**
  `https://assessment.cot.tn.gov/TPAD/Parcel/GIS?gislink=<GISLINK url-encoded>`
  Needs a browser User-Agent — urllib with the default UA gets a 403; curl with
  a Chrome UA works. Gives year built, living area, building areas,
  outbuildings, assessor values, utilities, sale history, and (for some
  counties) zoning.
- **FEMA flood:**
  `https://hazards.fema.gov/arcgis/rest/services/public/NFHL/MapServer/28/query`
  for the zone, layer `3` for the FIRM panel. Point geometry, `inSR=4326`.
  EFF_DATE comes back as epoch milliseconds.
- **Census geocoder:**
  `https://geocoding.geo.census.gov/geocoder/geographies/onelineaddress?address=...&benchmark=Public_AR_Current&vintage=Current_Current&format=json`
  An empty "Urban Areas" list is the support for the Rural checkbox.

Zoning is published per-parcel only by Davidson. TPAD carries it for Marshall.
Lincoln, Bedford and Marshall counties do **not** publish a queryable zoning
layer — Marshall posts only the cover page of its resolution online. Gate the
legally-permissible test rather than inferring it.
