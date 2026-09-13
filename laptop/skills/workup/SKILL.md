---
name: workup
description: Workup — produce the full pre-report analysis package for a Pinewood Appraisal assignment from a job folder or a tracker file — inputs inventory and gap report, MLS adjustment screens with regression and paired sales, as-is and as-completed comp candidates, value indications, neighborhood description, highest and best use, exposure and marketing time, and the items to resolve before delivery. Use when Todd points at an address, a job folder, or an order in the Appraisal Tracker and wants it worked up, analyzed, screened, or prepared before he writes the report. Triggers on "workup", "run the workup", "work up", "run the analysis", "market analysis", "adjustment screen", "comp candidates", "what do you need for", "pre-appraisal analysis".
---

# Workup — the pre-report analysis package

Read `C:\Users\toddp\.claude\appraisal\house-rules.md` and
`C:\Users\toddp\.claude\appraisal\uspap-citations.md` first. Every rule there
applies.

**House rules section 9 is the isolation rule: one assignment at a time.** This
skill touches more files than any other one here — a job folder, a tracker
record, an MLS export, contracts, bids, photos — so it is also the easiest place
to mix two properties up. State the subject address at the top of the reply
before doing any work. Everything in `references/` is method and template, never
data.

## What he gives you, and what you do with it

He points at **one** of these and says go:

| He says | You find the rest |
|---|---|
| "work up 123 Main St" | job folder, tracker record, export — see `references/discovery.md` |
| a job folder path | the address from the order inside it, then the tracker record |
| "the tracker file for <street>" | the tracker record, then its job folder |

**Never ask him for something you can find yourself.** The tracker record alone
carries order number, client, lender, borrower, product, loan type, fee, due
date, inspection date and time, county, and the whole public-records block —
parcel, assessor values, TPAD, flood, census tract, tax estimate.

## What the ordinary assignment looks like — build for this one

Nearly all of his work is a **1004 on an ordinary single-family house**, purchase
or refinance, FHA or conventional, with an occasional 2055 exterior. The house is
in average condition. Nothing about it is unusual.

So the workup earns its keep on the things that move value on **every** report:

| Every assignment | Rare — a branch, not the spine |
|---|---|
| GLA, bath count, garage/carport, site size, age | distressed / investor / handyman stock |
| Condition, as a normal C3-to-C4 spread | renovation, 203(k), subject-to-completion |
| Time / market conditions | as-completed value sets |
| Comp selection and the same-subdivision peer set | contractor bids and feasibility |
| Neighborhood, exposure, marketing time | auction and multi-parcel sales |
| Contract terms on a purchase | |

**Do not lead with the rare branch.** A workup that opens with a distressed-tier
analysis on a normal refinance is answering a question nobody asked. Run the
renovation sections only when the assignment is actually one — the order says
203(k), or subject-to-completion, or he says so. When in doubt, ask; it is one
question.

## Step 1 — Inventory first. Always. Before any analysis.

Run discovery, then post the **gap report** as your first reply: what you found,
what is missing, and what each missing item costs him. `references/inputs-and-gaps.md`
is the table to work from — it names, for every input, where it lives, what it
unlocks, and what the document has to say instead when it is absent.

Rules for this step:

- **One message, everything you need.** Never trickle questions out one at a time.
- **Name what each gap costs.** Not "send me the export" but "without the
  active/pending export there is no marketing time analysis and I will have to
  say so in the document."
- **Start work on what you have.** A missing bid does not stop the market
  analysis. Only the missing MLS export stops everything.
- If a required file exists but is unreadable — an image-only PDF with no text
  layer — say which one and what it needs (OCR through the tracker helper, or
  his notes).

## Step 2 — Build the worked CSV. Everything downstream reads it.

```
python scripts/prep.py --csv "<export>.csv" --out "<subject> - MLS worked.csv" \
    --lat <subject lat> --lon <subject lon> --origin <YYYY-MM-DD> --effective <YYYY-MM-DD>
```

Coordinates come from the tracker's public-records block or a live Census
geocode. The script writes the canonical columns, classes condition from remarks,
records **why** in `CondWhy`, and reports how far `DaysOnMarket` and
`ListToContractDays` disagree on this export.

**Then spot-check `CondWhy` and fix what is wrong.** Condition classing is a
keyword read and it will misfire. Review at minimum every row flagged `review`,
every distressed sale you intend to use as a comp, and any listing whose class
disagrees with its price per square foot. Re-run after edits. Class counts moving
between passes is normal and expected.

## Step 3 — Run the analysis

`references/method-market.md` carries the method: the time-adjustment test, the
regression sequence and how to read it, paired sales, the convergence rule, and
the traps that produce confident wrong numbers. Use `scripts/ols.py` — Penny has
no pandas, numpy, statsmodels or sklearn, and this does the whole job in stdlib
with standard errors and t-statistics.

`references/method-comps.md` carries comp candidate selection: as-is and
as-completed sets, the same-subdivision peer set, and the verification cautions
that must travel with a candidate (auction sales, multi-parcel sales,
tenant-occupied, non-arm's-length).

## Step 4 — The narrative sections

These are **not** rewritten here. Each has its own skill, and this workup drives
it so that one export produces one set of numbers:

| Section | Skill | Cross-check that must hold |
|---|---|---|
| Neighborhood description | `neighborhood-description` | price and age ranges come from **this** export; land use supports the H&BU conclusion |
| Exposure time | `exposure-marketing-time` | bracket matches the segment analysis in the workup |
| Marketing time | `exposure-marketing-time` | equals the 1004 Neighborhood grid checkbox; needs the **active/pending** export |
| Highest and best use | `highest-and-best-use` | present use matches what the comps and the land use split actually show; any surplus or excess land finding agrees with the site size used in the adjustment screens |

**H&BU needs zoning of record, and only Davidson publishes it per-parcel.**
Check `C:\Users\toddp\.claude\appraisal\zoning\` first — it holds downloaded
county zoning ordinances (Bedford, Cannon, Franklin, Lincoln, Rutherford,
Williamson; README there has versions, source URLs, and the gaps — Moore is
missing, Davidson lives on Municode, cities zone separately). They are
snapshots: cite the ordinance section from the PDF, but verify currency at the
source URL when the finding is load-bearing. Anywhere the library doesn't
cover, retrieve from the city or county source and cite it, or say the
legally-permissible test cannot be completed. Never infer zoning from surrounding
use — that is the one refusal in that skill that matters most.

Read those skills' `references/` and follow them. They produce their own
`WORKFILE` / `REPORT` file pairs in the job folder, and the workup document
carries the REPORT narratives **in full, word for word, in Part 1** — not a
summary (see `references/document-shape.md`). The .txt files stay the paste
source; the workup is the reading copy. **If the two disagree, the workup is
wrong — fix it, do not paper over it.**

Site improvements ride along: when the as-is site-improvements number exists
(the `site-improvements` skill), its figure and open questions go in the
narratives section too — "all the narratives" always includes that number.

Marketing time without an active/pending export is not a finding. Say so in both
places.

## Step 5 — Write the document

`references/document-shape.md` has the section order, the voice, the mandatory
caveat and plain-terms blocks, and the build command. Two outputs in the job
folder:

- `<subject> - WORKUP.html` — the source, and the one file he actually works from
- `<subject> - WORKUP.pdf` — printed from it headless, Pinewood letterhead

Plus the narrative file pairs from step 4.

Three things about the HTML that are not optional:

1. **It carries everything.** Part 3 folds in every workfile .txt this assignment
   produced, in full. He should not have to open a second file to defend a number.
2. **You write the body fragment; `scripts/build_workup.py` builds the page.**
   It adds the sidebar contents, the collapsible sections, the filter box, the
   text-size control, the letterhead and the print CSS. Never hand-write the nav.
3. **Every statistic gets a `.plain` block.** He is not a statistician and should
   not have to be one to read his own workfile.

Rebuild and reprint whenever a narrative .txt changes — a stale section 4 against
a revised narrative is the failure this document exists to prevent.

## The gates — refuse rather than guess

These are house-rules section 2 applied to this skill. Each one is a real failure
that has happened:

1. **No MLS export → no workup.** Everything else is decoration on the comps.
2. **No time adjustment unless the data agrees with itself.** Quarterly medians
   and the regression coefficient must point the same way and the coefficient
   must reach significance. When they disagree, say no adjustment is supported
   and name both results. A median drift over a thin recent quarter is a
   mix-shift artifact, not a market trend.
3. **A coefficient that is not significant is not support.** Print the standard
   error and the t-statistic next to every coefficient you quote. Anything under
   t = 2 gets labelled, and anything under t = 1.5 does not get quoted as a
   screen at all.
4. **Screening numbers never become report language.** Label the whole document
   as a screen, in a block at the top. His verified comps carry the report.
5. **Every candidate comp carries its caution.** A court-ordered auction, a
   two-parcel sale, a tenant-occupied investor sale and a non-arm's-length
   transfer are not market transactions until he verifies them.
6. **When GLA is unresolved, run every indication across a GLA range.** Do not
   pick one. Say which source disagrees with which, and by how much.
7. **Do not stack a bedroom adjustment on top of a GLA adjustment.** See
   `method-market.md`.

## Finish

Tell him the full path of every file you wrote, the gaps that are still open, and
the three or four things that most affect the value conclusion. Keep that summary
shorter than the document.
