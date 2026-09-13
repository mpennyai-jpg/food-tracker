# Northstar: Pinewood Appraisal

One-line summary: the business northstar. Pinewood Appraisal is Todd's one-person residential appraisal practice in Murfreesboro TN, and the goal is for Claude to absorb the typing, research, and writing that cap it at about 16 files a month. Personal life lives in `northstar-personal.md`.

Status: first synthesis from the 2026-09-13 brain dump. Sections marked (open) are unanswered.

## What the business is

Pinewood Appraisal, founded 2020, owner and sole appraiser Todd A. Paris, working from home in Murfreesboro, Tennessee. Certified residential, licensed since 2020, on the FHA roster, waiting on a VA roster slot. Todd started as a trainee around 2005, spent 14 years at H&H Appraisal, and went out on his own in 2020.

**Public positioning** (from pinewoodappraisal.com, as of 2026-09): appraisal services for real estate agents, homeowners, banks, and mortgage lenders. Property types listed: single-family, multi-family, townhomes, condos, HPRs (horizontal property regimes), manufactured homes, and vacant land. Also offers a sketching service for homeowners and agents who need an accurate gross living area measurement.

**Coverage** as stated on the website: Rutherford, Cannon, Coffee, Moore, Franklin, Lincoln, Marshall, and Davidson counties. The interview also named Bedford and Williamson and did not mention Moore or Marshall. Treat the union as the working list and confirm which is current. (unverified)

**Reality of the client mix**: mostly refinances and purchases for AMCs and big national banks. Very little of the private and agent work the website advertises. Named AMCs: Clarity, Class, Service, Trilateral.

**Edge**: will drive 25 to 50 miles for a property when many appraisers will not, and would rather turn down a fight than take a file already going sideways.

## What I am building toward

A practice where Claude does the data entry, the research retention, and eventually writes what it knows straight into the report, so that I can take more files without typing until 2 in the morning. Concretely: sustain 5 to 6 files a week without going underwater, and make 7 possible.

## Why it matters

Volume is capped by desk time, not by demand. I would love the money at 7 a week but the current workflow cannot carry it. Every workflow change is judged against one number: effective hourly rate, roughly $73 to $80 per desk hour, or $47 to $52 once drive and inspection time are counted. See `brain/reference/fees-volume-capacity.md`.

## Core values and non-negotiables

- **Never pick a comp to hit a number.** "Never that." Comps are chosen for correctness, and anything over about 10 miles gets explained in the report.
- **Adjustments reflect market reaction, not cost.** Depreciated cost is not an adjustment. Figuring out what the market actually pays is the whole job.
- **Bracket everything the data allows.** Skipping a bracket takes the data simply not existing.
- **The appraiser's judgment overrides the tool.** When TruTracts says $45,000 for a pool in Lincoln County, the answer is closer to $20,000, and I decide that.
- **No reviews. Flat out.** No no-comp subjects, no one-off multimillion properties, no files that are obviously going to be a fight.

## Current priorities

0. Bring the laptop system (`appraisal\`, `commands\`, `skills\`) into this repo so it is versioned and reachable from every session.
1. Get Claude reliably supporting adjustments, neighborhood description, and market conditions (already partly in place).
2. Build the workfile through Claude so research is saved and overrides are documented. This is the real audit exposure right now.
3. Teach Claude the data-entry role Laura currently fills, then wind that arrangement down.
4. Move reconciliation writing to Claude. It is the single biggest writing time sink.
5. Capture Rutherford County local knowledge (sides of town, school zones, where value lines fall). This is the highest-value knowledge that exists nowhere else. (open)

## The system already built

Months of work with Claude on the laptop have produced a working appraisal system, not just a starter file. It lives under `C:\Users\toddp\.claude\` and includes house rules (voice, a refusal gate that never states a number the data cannot carry, one assignment at a time, plain English on the form), USPAP citation rules that make every skill produce a workfile document, local zoning copies, a `/prep` command that preps a whole file from an address, a workup skill with regression scripts, and skills for neighborhood description, highest and best use, exposure and marketing time, site improvements, sales contract analysis, final read, daily brief, and email. Data lives in OneDrive: job folders, the Penny Share drop folder, Appraisal Tracker backups, the UAD 3.6 answer book. Full index in `brain/reference/claude-laptop-system.md`.

This changes the priority list. The twin is further along than the interview suggested. What is missing is that the system lives on one laptop and is not in this repo.

## How I operate

Bid the file, pull comps before the inspection, inspect and capture everything in the mobile app, download into TOTAL, pick comps, hand to Laura for typing, QC her return, run adjustments, write narratives, reconcile, deliver. Full detail in `brain/reference/appraisal-process.md`. I batch inspections by geography when I can. Nothing gets turned in early. The step that jams most often is my own QC pass after the file comes back, not waiting on Laura and not the adjustments.

## How I want my digital twin to act

- Act as an appraisal assistant that already knows my process, comp hierarchy, bracketing rules, and adjustment philosophy, and does not need them re-explained.
- Push me to document every override in the workfile at the moment it is made. The commission will ask "where is your reasoning?"
- Support adjustments with market evidence, never with cost.
- Write neighborhood, market conditions, and reconciliation narratives in my voice, from the starter file and TruTracts data.
- Flag anything I would turn down before I accept it.
- (open) What the twin should never touch.

## Key people

- **Laura**, data entry contractor, $30 per file, about 4 months in. See `brain/people/laura.md`.
- **Jae Davenport**, AMC director at Trilateral, very knowledgeable. See `brain/people/jae-davenport.md`.

## Open questions

Tracked in `brain/reference/open-questions.md`. The top three: Rutherford County local knowledge, a reconciliation walkthrough from first line to last, and what is in the Claude starter file today.

---

Maintenance: revisit at least quarterly. When updating, note the date and what changed below.

## Change log

- 2026-09-13: created as a skeleton.
- 2026-09-13: first synthesis written from the Pinewood Appraisal brain dump and interview transcript.
- 2026-09-13: renamed to the business northstar, added public positioning and coverage from the website, moved personal material to `northstar-personal.md`.
- 2026-09-13: added full name and the laptop Claude system from Todd's global CLAUDE.md. Priority 0 added: bring that system into the repo.
