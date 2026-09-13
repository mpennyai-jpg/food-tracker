---
name: exposure-marketing-time
description: Produce a supported exposure time and marketing time opinion for a Pinewood Appraisal assignment — a workfile document showing the list-to-contract analysis and a short form-ready narrative. Use when Todd gives a subject address with an effective date and an opinion of value and wants exposure time, marketing time, "how long would it have taken to sell", the reasonable exposure time bracket, or the 1004 marketing time checkbox. Triggers on "exposure time", "marketing time", "reasonable exposure", "DOM analysis", "months of supply", "how long on market".
---

# Exposure time & marketing time

Read `C:\Users\toddp\.claude\appraisal\house-rules.md` and
`C:\Users\toddp\.claude\appraisal\uspap-citations.md` first. Every rule there
applies — the voice rules, the refusal gate, and the two-file output pattern.

**House rules section 9 is the isolation rule: one assignment at a time, and no
fact enters a document unless it came from THIS subject.** Reference files in this
skill carry method and templates only. Every bracketed placeholder must be filled
from this assignment or deleted.

Then read `references/method.md`. That is the method to match. It carries no
assignment data — every figure in it is a placeholder or a property of MLS data
itself.

Produces two files in his job folder:

- `EXPOSURE - MARKETING TIME - WORKFILE analysis.txt`
- `EXPOSURE - MARKETING TIME - REPORT narrative.txt`

---

## Step 1 — Collect the inputs. Ask only for what you cannot get yourself.

**Required, and he must supply them:**

| Input | Why |
|---|---|
| Subject address | Everything keys off it |
| Effective date | Exposure time ends here; marketing time starts here |
| Opinion of value | SR 1-2(c) requires the exposure time be **linked to that value opinion** |
| **Two** MLS exports | See Step 2 |

**Get these yourself, do not ask:** county, census tract, flood zone, parcel data
— pull them from the keyless sources in house-rules section 7.

Ask for everything missing in **one message**. Never one question at a time.

## Step 2 — Get BOTH exports. One will not do the job.

| Export | Supports | Without it |
|---|---|---|
| **Closed sales**, 12 months back from the effective date | Exposure time | No exposure bracket. Refuse. |
| **Active + under contract**, as of the effective date | Marketing time — absorption, months of supply, pending ratio, unsold inventory age | Marketing time is unsupported. Say so; do not quietly reuse the exposure number. |

This is the correction that matters most. Exposure time rests on closed sales
only. **Marketing time is properly supported by current inventory and
absorption**, which only the active/pending export provides.

Fallbacks, in order:

1. Both exports — the real analysis.
2. Closed only — exposure time fully supported. State marketing time as equal to
   exposure time **and disclose in the workfile and the report that no
   active-inventory analysis was performed**. Do not present it as a finding.
3. His own comps' market times, typed. Thin. Say so.
4. Nothing. **Refuse to state a bracket:**

   > I cannot support an exposure time opinion without market-time data for this
   > segment. Export closed sales for the past 12 months from RealTracs, plus
   > actives and pendings as of the effective date, and give me the files.

   Never fall back to "typically 30 to 90 days."

## Step 3 — Define the market segment, and say what you defined

Exposure time is an opinion **for this property at this value**, not for the
county. Filter to sales sharing the subject's highest and best use:

- Same property type and rough configuration (bed/bath count, one-unit detached)
- Same market area — his neighborhood boundaries if drawn, else the city, stated
- GLA band around the subject
- Year-built band where the stock varies
- A price band around the concluded value
- Closed **on or before the effective date** — exclude anything closing after it,
  and say which records you dropped and why

Record the filter verbatim. A reviewer must be able to rerun it.

Report **more than one segment**. The all-sales figure, the subject's
configuration, and the subject's price band. Where they agree, the conclusion is
strong. Where a band is too thin (n under about 8), say so and do not lean on it.

## Step 4 — Measure list-to-contract, NOT the MLS days-on-market field

**This is the single most important mechanic in this skill.**

`DaysOnMarket` resets when a listing is withdrawn and relisted. It understates
actual calendar exposure. Measured on a real Tennessee export, the two fields
disagreed on 54 of 56 records and raw DOM understated exposure by roughly 25%; one
listing that ran 189 calendar days reported as 59.

That is a warning about the field, not a fact about any market. **Measure the
disagreement fresh on this assignment's export.**

So:

1. Use **`ListToContractDays`** where RealTracs provides it.
2. Otherwise compute **binding contract date minus list date** yourself.
3. Use `DaysOnMarket` only when neither is available, and **disclose that you
   did**, with the direction of the bias.
4. **Always report both medians side by side** and say how far apart they ran.
   That disagreement is itself evidence for the workfile.

## Step 5 — Compute, and separate pricing failures from slow absorption

For each segment report **n, minimum, Q1, median, Q3, maximum**, using linear
interpolation, and say so.

**The exposure bracket starts at Q1 to Q3**, rounded outward — nearest 5 days
below 60, nearest 15 days at 60 and above. Then adjust it with the two analyses
below before concluding.

### Pricing behavior — compute every time

- Median sale price to **list** price
- Median sale price to **original** list price
- Percentage of closed sales that took at least one price cut

### The pricing-failure principle — do not skip this

**Exposure time presumes the property is priced at the appraised value.** A sale
that sat 189 days because it was listed at double its worth is not evidence that
a correctly priced house needs 189 days.

So: look at the long tail. For each long-market-time sale, check whether the
original list price was far above the eventual sale price. If the long times in a
band are pricing failures, **say so with the specific addresses and numbers**, and
do not let them push the conclusion longer.

Shape of the paragraph — every bracket filled from THIS assignment's export:

> Both long market times in that band were pricing failures. [ADDRESS] listed at
> [ORIGINAL LIST] and sold at [SALE PRICE] after [N] days. [ADDRESS] cut from
> [PRICE] to [PRICE] over [N] days. Two priced correctly and sold fast —
> [ADDRESS] in [N] days, [ADDRESS] in [N] days. Exposure time presumes pricing at
> the appraised value, so mispriced outliers do not support a longer conclusion.

### Place the subject inside the bracket

- At or below the predominant price, average condition, conforming → near the
  median.
- Superior, atypical, over-improved, or narrow buyer pool → upper end, and say why.
- Inferior or carrying a known defect → upper end, and name the defect.

## Step 6 — Marketing time, from the active/pending export

Marketing time is **prospective** — AO-7. It starts at the effective date.

Compute from the active/pending export:

| Metric | How |
|---|---|
| Absorption rate | Closed sales divided by the months spanned |
| **Months of supply** | Active listings divided by the absorption rate |
| Pending ratio | Under contract divided by active |
| **Median market time of unsold active inventory** | Directly, as of the effective date |
| Actives that have already cut price | Count and percentage |

### The two corroborations — run both

1. **Unsold inventory age against the closed-sale median.** When actives have
   been sitting about as long as closed sales took to go under contract, the two
   sides of the market agree. That is real support.
2. **Price-cut rate, actives against closed sales.** Same logic — a similar share
   on both sides corroborates.

When these two agree, say so — it is the strongest support available. When they
disagree, that is a finding too: it means the market is turning, and it moves
marketing time off the exposure range.

### Direction of travel

- Quarterly median market times — is there directional lengthening, or just
  oscillation? Numbers bouncing without direction indicate no lengthening.
- Median sale-to-list ratio by quarter. A steady drift down is **mild softening**,
  and supports stating marketing time at the **upper end** of the exposure range
  rather than the middle.

### Concluding

State marketing time as a point or a range, positioned against the exposure
bracket, with the reason named — "exposure [LOW] to [HIGH] days; marketing time
[X] days, at the upper end because [NAMED REASON]."

**Default to equal only when the evidence genuinely shows no change**, and say
that with the numbers beside it.

Then give the **Fannie 1004 bracket**: Under 3 mths / 3-6 mths / Over 6 mths.

**If over 6 months, Fannie B4-1.3-03 requires him to state the reasons.** Flag it
and draft that explanation.

**Cross-check the neighborhood section.** Marketing Time in the 1004 Neighborhood
grid must equal this conclusion. If `neighborhood-description` has run for this
file, read its output and confirm. If they disagree, tell him which to change —
do not silently pick one.

## Step 7 — State what the data cannot do

In the workfile, always:

- **Closed-sale exports contain only listings that sold.** Expired and withdrawn
  listings are absent, so the sample understates time for everything offered.
- **Exposure time rests on closed sales only.** Marketing time rests on current
  inventory. Say which evidence carries which conclusion.
- **Closed-sale exports under-report the newest months** — recent contracts have
  not closed. Check the last two months by contract date; if thin or empty, say
  so, and note the sample skews toward older conditions.
- Both conclusions are ranges or points, not precise figures.

## Step 8 — Write the two files

### `EXPOSURE - MARKETING TIME - WORKFILE analysis.txt`

1. Header — address, effective date, opinion of value, date prepared
2. **Definitions** with authorities — SR 1-2(c) and AO-35; AO-7
3. **Data** — both exports named, pull dates, filters, record counts, exclusions
4. **Measurement basis** — list-to-contract versus MLS DOM, how far apart they
   ran, and which you used
5. **Segment table** — n, DOM median, list-to-contract median, Q1/Q3 per segment
6. **Pricing behavior** — sale/list, sale/original list, price-cut rate
7. **Pricing failures** — the specific outliers, by address, and why they are
   excluded from the conclusion
8. **Supply side** — the metrics table from Step 6
9. **Corroborations** — both, explicitly
10. **Trend** — quarterly market times and sale-to-list ratios
11. **CONCLUDED** — exposure bracket and marketing time, one line, bolded
12. **Limitations** — Step 7
13. **Sources** — every file and URL with its retrieval date
14. Closing line: the exposure opinion is stated in the report under SR
    2-2(a)(vi); this workfile holds the support

### `EXPOSURE - MARKETING TIME - REPORT narrative.txt`

Two labeled blocks, roughly 120 words each, in **his** voice — first person,
active, short sentences, no sentence starting with "The".

The analytical shorthand in `references/method.md` is not prose. Take the
analysis; write the sentences fresh in his voice.

**Exposure block**, in order: the retrospective definition; **the actual numbers**
(n, median, middle range); the measurement basis in one clause; the concluded
bracket; where the subject falls and why.

His current form boilerplate ends *"Based on this historical statistical data, a
highly supported opinion..."* with no statistical data anywhere in the report.
**Replace that sentence** with the real n and the real median.

**Marketing block**: prospective; months of supply and absorption; the range; the
Fannie bracket; the named reason it does or does not match exposure time.

## Step 9 — Report back

Two full paths, the exposure bracket, the marketing time, the Fannie bracket, and
every flag: thin segment, DOM-versus-list-to-contract gap, pricing failures
excluded, missing active/pending export, over-six-months explanation needed, or a
disagreement with the neighborhood section.
