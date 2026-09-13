---
name: site-improvements
description: Calculate the "as-is" value of site improvements for the cost approach in a Pinewood Appraisal report — the depreciated-cost, item-by-item buildup of driveways, walks, fencing, landscaping, outbuildings, pools, and well/septic. Produces a workfile document showing the inventory, cost new, percent good, and the arithmetic behind the single number that goes on the form. Use whenever Todd asks for the as-is value of site improvements, site improvements value, contributory value of site improvements, the site improvements line in the cost approach, or what a driveway / fence / landscaping / shed / pool contributes — even if he only says "I need the site improvements number for [address]."
---

# "As-is" value of site improvements

Read `C:\Users\toddp\.claude\appraisal\house-rules.md` first. Every rule there
applies — especially section 2 (the refusal gate), section 4 (workfile
documents), section 5 (where output goes), and section 9 (one assignment at
a time; nothing carries over from another file).

## What this number is

One line in the cost approach: the **contributory (depreciated) value** of
everything on the site that is not the dwelling and not the land itself.
Not cost new. Site improvements get their own line because they wear out
faster than the dwelling — a driveway or a fence does not live on a
125-year economic life.

**Read `references/whats-included.md` before building the inventory.** It
carries the full include/exclude list, the UAD 3.6 field rules (25.037 -
25.039 from Appendix F-1, which he holds locally in Desktop\UAD 3.6), the
three 3.6 routing rules — detached garage with no extra area goes IN this
line, outbuildings get their own subsection, attached anything stays in
dwelling cost-new — and the classroom disagreements with the defensible
resolution for each. The one-sentence rule: every dollar appears in
exactly one cost-approach bucket, and the workfile says which bucket got
what. In 3.6 the report displays the 25.037 descriptions, so what the
workfile includes and what the form says must match.

## Step 1 — Inventory from THIS assignment

Build the item list only from this subject's evidence: his inspection
photos, his notes, the sketch, the parcel record's outbuilding section,
MLS listing photos he supplied. Walk the photo set deliberately — front,
rear, street, and any site shots — and list what is actually visible.
Note condition evidence while you look: cracked or patched pavement,
leaning fence sections, overgrowth, a shed with a sagging roof. Those
observations set the percent-good figures and they must trace to a photo
or a note.

**Utilities gate his two biggest hidden items.** If the site is on a well
or septic, those systems carry real contributory value (septic commonly a
few thousand dollars as-is) and belong on the list. If public water and
sewer serve the site, they do not exist here. If utilities are unknown,
ask him — do not guess, and do not silently omit.

## Step 2 — Cost new, per item

Sources, in order of preference:

1. **His own recent appraisals in the same market.** He supplies these or
   they sit in the job folder. A figure he has already used and signed for
   in this market is the strongest support. Never pull numbers from
   another assignment he has not supplied for this one — isolation rule.
2. **Local contractor bids** in the job folder (a paving or fencing bid,
   even from a nearby comparable property he worked, if he supplied it).
3. **DwellingCost / his cost service**, which he runs himself — flag the
   item for him to price if precision matters.
4. **Published cost guides from the web** — retrieve fresh, cite the URL
   and retrieval date, and label them SCREENING ONLY per house-rules
   section 3. They bracket; they do not support report language alone.

Typical residential unit-cost shapes (verify against a current source,
never quote these as support): asphalt paving by the square foot, fencing
by the linear foot, concrete flatwork by the square foot, sheds by the
unit, septic by the system.

## Step 3 — Percent good, per item

Site improvements depreciate on short lives. Judge each item from the
photo evidence, and write the reason next to the number:

- Pavement with visible cracking or patching: well under half good.
- Fencing: half good is typical mid-life; leaning or missing sections
  push it down.
- **Landscaping is contributory value, not cost.** Mature trees and
  established shrubs cost enormous sums to install but contribute only
  what a buyer credits. Overgrown or unmaintained landscaping contributes
  LESS, not more — discount it and say why. This is also where this line
  must agree with the rest of the report: a report that describes
  deferred maintenance and overgrowth cannot carry a top-of-market
  landscaping figure two pages later (weak-spot rule: do not contradict
  the form).
- Wells and septic: as-is value depends on age and observed function;
  if he noted problems, reflect them.

## Step 4 — The buildup table and the cross-checks

Sum the items and round sensibly (nearest $500 is plenty of precision
for this line).

Then run two checks before the number stands:

1. **Against his own recent figures in this market.** If his comparable
   reports carried $13,500 and $15,500 for similar properties, and this
   subject shows a cracked drive and overgrown lot, the subject figure
   should land BELOW those, and the workfile should say so in one
   sentence. If it lands above, justify it item by item or fix it.
2. **Against the rest of this report.** The site-improvements figure must
   tell the same story as the condition section, the photos, and any
   cost-to-cure analysis. Reviewers read across pages.

## Step 5 — Write the workfile document

`Site improvements - WORKFILE.txt` in the job folder (house-rules
section 5 for finding it). Contents:

1. Header — address, effective date
2. Inventory, with the photo or record source for each item
3. Utilities finding (public sewer/water confirmed, or well/septic
   valued)
4. The buildup table: item | cost new | source | % good | reason | as-is
5. The two cross-checks, written out
6. The concluded figure, rounded
7. Sources with URLs and retrieval dates; anything from a web cost guide
   labeled screening
8. A CONFIRM list — items he should price in DwellingCost or verify
   before the form is final

Report back to him with the concluded number, the table, and every flag:
unknown utilities, an item visible in photos he did not mention, a
cross-check that failed, or an item that might already be inside his
dwelling cost-new (double-count risk).

## The refusal gate, applied here

If there are no photos, no inspection notes, and no supplied listing
media — there is no inventory, and a number built on an imagined
driveway is a liability. Say what is missing and stop. A partial
inventory with named gaps ("fence visible in rear photo; length not
measurable — measure on site") beats a confident total.

## Example shape (numbers are placeholders, never data)

```
Asphalt driveway  ~[AREA] sf @ $[RATE]/sf new, [PCT]% good
  ([OBSERVED CONDITION])                              $ [X]
Concrete walkway + stoops, [PCT]% good                $ [X]
Board fence, [SIDE], ~[LF] lf, [PCT]% good            $ [X]
Landscaping, contributory, discounted for
  [OBSERVED CONDITION]                                $ [X]
Misc                                                  $ [X]
                                                      -------
AS-IS VALUE OF SITE IMPROVEMENTS                      $ [TOTAL]
```
