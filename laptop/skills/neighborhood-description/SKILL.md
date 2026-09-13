---
name: neighborhood-description
description: Fill the entire 1004 Neighborhood section for a Pinewood Appraisal assignment — every checkbox, the price and age ranges, present land use percentages, the North/South/East/West boundaries, the neighborhood description narrative, and the market conditions support box — plus a workfile document showing where each answer came from. Use when Todd gives a subject address and wants the neighborhood section, neighborhood boundaries, neighborhood description, market conditions commentary, or the one-unit housing trends checkboxes. Triggers on "neighborhood description", "neighborhood section", "neighborhood boundaries", "market conditions comments", "one-unit housing trends", "present land use".
---

# Neighborhood section — 1004

Read `C:\Users\toddp\.claude\appraisal\house-rules.md` and
`C:\Users\toddp\.claude\appraisal\uspap-citations.md` first. Every rule there
applies.

**House rules section 9 is the isolation rule: one assignment at a time, and no
fact enters a document unless it came from THIS subject.** Reference files in this
skill carry method and templates only. Every bracketed placeholder must be filled
from this assignment or deleted.

Then read `references/fair-housing-language.md` **before writing a single
sentence of narrative.** It is the hardest constraint in this skill.

Produces two files in his job folder:

- `NEIGHBORHOOD - WORKFILE analysis.txt`
- `NEIGHBORHOOD - REPORT narrative.txt`

---

## Step 1 — Inputs

**He supplies:** subject address, effective date. That is the minimum to start.

**Helpful if he has them, ask for all of them in one message:** the MLS export he
is already using for comps, his neighborhood boundaries if he has drawn them
before, the subject's GLA and year built, and the concluded value.

**Pull yourself, do not ask** (house-rules section 7):

- Census Geocoder — lat/lon, county, **census tract**, urban/rural flag
- FEMA NFHL — flood zone, SFHA yes/no, FIRM panel, map date
- County parcel layer — subdivision name, lot, year built, acreage, assessor
  values, and **zoning where published** (Davidson only)

The census **urban/rural flag** is a real input to the Location checkbox. Use it,
but do not let it overrule what he observed on inspection.

## Step 2 — Draw the boundaries

Fannie B4-1.3-03: boundaries are outlined using **North, South, East, West**,
referencing streets, legally recognized neighborhood boundaries, waterways, or
other natural features.

Method:

1. Start from the subject's coordinates.
2. Find the nearest arterial roads, interstates, rivers, rail lines, and
   municipal or subdivision limits in each of the four directions.
3. Stop the boundary where the character of development actually changes — a
   commercial corridor, a different lot pattern, a jurisdiction line. Do not draw
   a box of convenience.
4. Write it in his existing form: *"On the north by [FEATURE], on the east
   [FEATURE], on the south [FEATURE], and on the west by [FEATURE]."*

**A subdivision name is not a neighborhood, and a road-name string match is not a
neighborhood** (house-rules section 3). Boundaries must enclose the area that
competes for the same buyer.

If he has already stated boundaries for **this same market area** on a prior
assignment, reusing them is good practice — consistency across his files matters
more than a marginally better polygon. But confirm with him first that it is the
same market area, and never carry a boundary across from a different city or
submarket just because it is the last one you saw.

## Step 3 — Answer every field in the grid

Work through all of these. Leave nothing blank.

**Neighborhood Characteristics**

| Field | Options | How to decide |
|---|---|---|
| Location | Urban / Suburban / Rural | Census urban-rural flag, density, lot sizes, his observation |
| Built-Up | Over 75% / 25-75% / Under 25% | Share of developable sites already improved |
| Growth | Rapid / Stable / Slow | New construction and permit activity in the boundaries |

**One-Unit Housing Trends** — Fannie requires a **minimum of 12 months** of data
behind each of these three.

| Field | Options | How to decide |
|---|---|---|
| Property Values | Increasing / Stable / Declining | The Market Conditions tool's result for this segment. If it returned no statistically supported trend, the answer is **Stable** — say that in the support box. |
| Demand/Supply | Shortage / In Balance / Over Supply | Months of supply, active listings against the 12-month absorption rate |
| Marketing Time | Under 3 mths / 3-6 mths / Over 6 mths | **Must match the `exposure-marketing-time` output.** See Step 6. |

**One-Unit Housing** — PRICE $(000) low / high / predominant, and AGE (yrs) low /
high / predominant.

- Predominant price and predominant age are each **one whole number** — the most
  frequently found value, not the average and not the median unless they coincide.
- If the subject's age falls outside the stated range, **Fannie requires an
  explanation.** Draft it.
- If he pulls the range from a wide distribution with loose parameters, carry his
  existing footnote: *"One Unit pricing is a distribution of properties in the
  subject's area with very little parameters."*

**Present Land Use %** — One-Unit, 2-4 Unit, Multi-Family, Commercial, Other.

- One-unit and 2-4 unit are reported **separately**, never combined.
- Undeveloped land is noted separately — his convention puts it under Other with
  the footnote *"Other represents vacant land, parking lots, and roads."*
- **The five percentages must total 100.** Check the arithmetic before writing.

## Step 4 — Write the Neighborhood Description narrative

**Short-summary style — his standing decision, set on H&BU 2026-08-24 and
extended here: the form carries conclusions; the research lives in the
workfile.** The checkboxes, ranges, percentages, and boundaries are form
requirements and stay on the form in full. The free-text narrative is
where the brevity applies: roughly 60 to 80 words, conclusions only, one
sentence each —

1. Where the subject sits — street, city, county, position relative to a
   named corridor
2. What development consists of — structure types and pattern, in one
   sentence
3. Land use mix and where the non-residential uses sit, in one sentence
4. Access/connectivity by named route, in one sentence
5. Close with: *"My workfile holds the boundary rationale, the land use
   counts, and the market data behind this section."*

Every count, derivation, n, and source stays in the workfile — the
narrative asserts nothing the workfile cannot defend line by line.

**The carve-out — same as H&BU: a clean neighborhood gets the short form;
an adverse finding does not.** Any external influence that affects
marketability, a subject outside the age or price range, declining
values, over-supply, or marketing time over six months goes ON the form,
stated factually — Fannie B4-1.3-03 requires the reasons in writing and
brevity never overrides that.

Obey the voice rules absolutely. His prior neighborhood paragraphs open
with *"The subject property is located..."* and run passive — *"is
characterized as."* Both break his own rules. Recast into the form
*"Subject fronts [STREET] in [CITY], [COUNTY] County, [DIRECTION] of the
[NAMED CORRIDOR]."*

## Step 5 — Write the Market Conditions support box

This box exists to support the three One-Unit Housing Trends checkboxes. It must
carry actual evidence, not a restatement of the checkbox.

Short-summary style applies here too: two or three sentences on the form,
the full statistical result in the workfile. Name on the form:

- The data source and tool — RealTracs, TrueTracts — and the segment
- The direction found, in plain words
- Where the support sits: *"My workfile holds the full analysis."*

The n, the period, the rate, the R-squared and t-statistic, and the
export date all live in the workfile, written out in full.

**Exception that always goes on the form: if values are declining, supply
is over-supplied, or marketing time exceeds six months, state the
reasons here.** Fannie B4-1.3-03 requires it and brevity never overrides
it.



If the Market Conditions tool returned **no statistically supported trend**, that
is the finding. Write it with the actual R-squared and t-statistic beside it.
Do not upgrade a flat market to "increasing" because the checkbox feels better.

## Step 6 — Cross-checks before you write anything out

- **Marketing Time** here must equal the `exposure-marketing-time` conclusion. If
  that skill has run for this file, read its output. If it has not, say the
  checkbox is provisional until it does.
- **Property Values** here must agree with the direction of any time adjustment
  applied in the sales comparison grid. Zero time adjustment with "Increasing"
  checked is an internal inconsistency a reviewer will find.
- **Present use percentages** must be consistent with the highest and best use
  conclusion. A neighborhood written as 70% one-unit supports a one-unit H&BU.
- Internal consistency across the whole report is one of his five documented weak
  spots. Check it here rather than after delivery.

## Step 7 — Write the two files

### `NEIGHBORHOOD - WORKFILE analysis.txt`

1. Header — address, effective date, date prepared
2. **Boundaries** — the four bounding features, why each was chosen, and what
   changes on the far side of it
3. **Every grid field**, each with the data behind it and the source
4. **Price and age ranges** — the underlying set, its n, and how low, high and
   predominant were each derived
5. **Land use percentages** — the method, the count, and the arithmetic totaling
   100
6. **Market conditions** — the full statistical result, including any finding of
   no supported trend
7. **Sources** — every URL and file with its retrieval date
8. Closing line: everything here is a starting point he must confirm; the report
   summarizes it

### `NEIGHBORHOOD - REPORT narrative.txt`

Laid out to match the form top to bottom so he can fill straight down the page:

```
Location:            [Urban / Suburban / Rural]
Built-Up:            [Over 75% / 25-75% / Under 25%]
Growth:              [Rapid / Stable / Slow]
Property Values:     [Increasing / Stable / Declining]
Demand/Supply:       [Shortage / In Balance / Over Supply]
Marketing Time:      [Under 3 mths / 3-6 mths / Over 6 mths]

One-Unit PRICE $(000)   Low __    High __    Pred. __
One-Unit AGE (yrs)      Low __    High __    Pred. __

Present Land Use %   One-Unit __   2-4 Unit __   Multi-Family __
                     Commercial __   Other __     (must total 100)

NEIGHBORHOOD BOUNDARIES
...

NEIGHBORHOOD DESCRIPTION
...

MARKET CONDITIONS (including support for the above conclusions)
...
```

## Step 8 — Report back

**Lead with anything that could be wrong — flags come FIRST, before the
answers:** subject age outside the range, land use not totaling 100, an
over-six-months marketing time needing an explanation, a disagreement
with the exposure time conclusion, a checkbox the data does not support,
or any input you could not verify. He wants problems called out on the
front end, every time.

Then give him the two full paths and the six checkbox answers in one
line each.
