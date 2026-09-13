# Market analysis method

Everything here runs off the worked CSV from `scripts/prep.py`. Every number
produced here is a **screen**, and the document says so at the top.

## 1. Segment before you count

Report the data set as: total listings, closed, active, under contract, and the
date span. Then define the band that brackets the subject — usually a GLA range
around the subject's area — and report the counts again inside it. If the pattern
inside the band contradicts the pattern outside it, the band governs and you say
why.

Fewer than 8 sales in a segment: say the sample is thin, widen it, and report
what you widened it to.

## 2. The elements that matter on every assignment

Lead with these. On an ordinary 1004 they are the whole job:

**GLA, bath count, garage or carport, site size, age, central heat and air, and
time.** Every one of them gets a screen range and a confidence word. These are what
he tests his grid against on a normal house.

**Central air is carried in the export as free text**, so `prep.py` derives
`CentHeat`, `CentAir` and `HVAC` flags from the Heating and Cooling fields and
prints how many closed sales lack central air. `CentAir` is the discriminator that
matters — a house can have central heat and still cool on window units, and it is
the cooling that shows up in price. Where nearly every sale has it there is no
variation left to measure and the coefficient will be weak; in older small-house
stock it is one of the larger adjustments on the sheet. Watch the confound: if
every sale without central air also predates a certain year, the coefficient is
carrying age and obsolescence too, and the screen range has to widen to say so.
The MLS cooling field is agent-entered and is not always updated after a
renovation — verify it on any sale that drives the conclusion.

Condition matters too, but on ordinary stock it is a modest step between average
and updated — not the dominant variable. Size the analysis to that.

## 3. Condition tiers — and the thin-tier gate

Three tiers — distressed, average, renovated — classed from remarks by
`prep.py`, then **spot-checked by you**. For each tier report n, median $/SF,
mean $/SF, median sale price, median GLA, median days.

In a normal market export most sales land in **average**, a healthy minority in
**renovated**, and the distressed tier is small or empty. That is the expected
shape, not a problem with the data.

**The gate: a tier with fewer than 8 sales cannot carry a condition adjustment.**
Say the tier is thin, give its n, and either widen the segment and report what you
widened it to, or fall back to the regression coefficient — which uses every sale
rather than a handful. If neither supports it, write that no condition adjustment
is supported by this data set and stop. A $40,000 spread computed off five
distressed sales is the kind of number that looks authoritative and is not.

The tier medians are the first read on condition. They are also the softest number
in the document, because classing is a keyword read. Say that where the table
sits, not only in the limitations block.

## 4. The time-adjustment test — two methods, and they must agree

Run both:

1. **Quarterly and half-year medians** of $/SF across the span.
2. **The months coefficient** in the regression, with its standard error and t.

Then apply the gate:

| Result | What you write |
|---|---|
| Both point the same way, coefficient significant | A time adjustment is supported. Give the monthly rate and the model it came from |
| They disagree, or the coefficient is not significant | **No time adjustment is supported by this data set.** Report both results and say the market reads flat over the period |
| Medians drift but the recent quarter is thin | Name it as a mix-shift artifact and give the n for that quarter |

Never manufacture an adjustment from a median drift alone. If he needs a
defensible one, point him at the Market Conditions tool against a wider pull —
that is a different analysis with a different data set.

His time adjustments come from a GAM tool applied per comparable from **contract
date** to effective date. A screen that disagrees with it is not evidence the
tool is wrong; it is a different method on a smaller sample. Say which is which.

## 5. Regressions — a sequence, not one model

Build up, and report the sequence so the reader sees what each variable did:

| Model | Specification |
|---|---|
| M1 | GLA, bedrooms, full baths, half baths, condition |
| M2 | M1 + months |
| M3 | M2 + age |
| M4 | M3 + garage/carport + acres |
| M5 | M4 restricted to the GLA band |
| M6 | parsimonious: GLA, baths (full + ½ × half), condition, months |

```
python scripts/ols.py --csv "<worked>.csv" --y SP --x SF,Baths,Cond,Mon \
    --filter "Status=Closed" --label "M6 parsimonious"
```

Reading rules:

- **Print the standard error and t for every coefficient you quote.** A
  coefficient without its t is not support.
- t ≥ 2 significant; 1.5–2 marginal, label it; under 1.5 do not quote it as a
  screen at all.
- **A stable coefficient across specifications is the finding.** When one
  variable holds its value and its t across six models, that is the number worth
  leaning on, and say so.
- Dropping insignificant variables usually **sharpens** the ones that matter —
  collinear terms steal each other's explanatory power. If GLA looks weak in the
  full model and strong in the parsimonious one, report both and use the second.
- Watch for GLA going unstable against acres and garage: those three move
  together on small older houses.

## 6. Paired sales

Pair on whichever element is actually in question — most often bath count,
garage, or site size on an ordinary house. Hold everything else close: match on
bedroom count and GLA within a stated tolerance, vary only the element being
tested. Report the number of pairs, the median difference and the mean
difference.

Median beats mean here — a handful of odd pairs will drag the mean.

Condition is paired the same way when the tiers are large enough to allow it. See
the thin-tier gate in section 3.

## 7. The convergence rule — the most defensible finding in the document

When three independent methods land in the same range, that range is what he can
defend:

1. Regression coefficient
2. Paired-sales median
3. A median comparison across the groups being tested, applied at the subject's
   GLA

State all three, state the range they agree on, and say plainly that the
convergence is what makes it usable. When they **do not** converge, say that too
and give the widest of the three as the screen with low confidence.

## 8. The adjustment screen table

One row per element: regression value, median/paired value, the screen range to
test, and a confidence word tied to the evidence — not to a feeling.

| Confidence | Means |
|---|---|
| High | multiple methods agree, t well above 2, stable across specifications |
| Moderate | one method, significant, no contradiction |
| Low | not significant, unstable sign, or a single thin comparison |

## 9. Traps that produce confident wrong numbers

**Do not stack bedroom count on top of GLA.** Raw medians make a 3-bedroom look
worth far more than a 2-bedroom, but the 3-bedroom sales are also larger. Once
GLA is in the model the bedroom coefficient usually collapses and stops being
significant. Adjust for size, then treat bedroom count as a minor
functional-utility item — or the same difference gets paid for twice.

**Half baths are unstable in small samples.** The sign flips between
specifications. Label it low confidence or leave it out.

**Add age BEFORE trusting a bath or bedroom coefficient.** This is the same trap as
the bedroom/GLA one and it is easier to miss. In a market where the older houses
are the one-bath houses, bath count proxies for age: a model without age can show
a full bath at tens of thousands of dollars with a healthy t-statistic, and paired
sales will agree with it, because both are measuring the age gap. Put age in and
the bath coefficient can collapse to near zero while adjusted R-squared jumps.
Seen on a real export: full bath $34,253 (t = 3.9) without age, $3,806 (t = 0.5)
with it, adjusted R-squared 0.51 to 0.66, and 750 matched pairs pointing at
$45,050 the whole time. **Paired sales confirm a confound as happily as they
confirm a real difference.**

**Age and GLA fight.** In a market of small older houses, age often proxies for
everything else. A marginal age coefficient is not an age adjustment.

**$/SF medians are unadjusted.** They carry lot, bath count and location
differences inside them. A $/SF indication will usually sit below a hedonic one
for an inferior subject — say why rather than averaging them.

**A price per square foot conclusion is not an adjustment.** It is a screen for
whether an adjustment is the right order of magnitude.
