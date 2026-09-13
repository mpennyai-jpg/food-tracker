# Exposure and marketing time — method

**Nothing in this file is data.** Placeholders are bracketed. The calibration
findings below are properties of MLS data generally, not facts about any
assignment, and none of them may appear as evidence in a report.

---

## Measurement basis — the mechanic that changes the answer

**MLS `DaysOnMarket` resets when a listing is withdrawn and relisted.** It
understates actual calendar exposure.

Calibration, measured on a real Tennessee export: `DaysOnMarket` and
`ListToContractDays` disagreed on **54 of 56 records**, and raw DOM understated
exposure by roughly **25%**. One listing that ran 189 calendar days from list to
contract reported as 59.

Treat that as a warning about the field, not as a market fact. **Measure the
disagreement fresh on every export** — it varies by market and by period.

Priority:

1. `ListToContractDays` where the export provides it
2. Otherwise binding contract date minus list date, computed yourself
3. `DaysOnMarket` only if neither exists, **with disclosure** and the direction
   of the bias

Report both medians side by side. The gap is workfile evidence.

## Segment table — the shape to reproduce

Report several segments so agreement between them carries the conclusion:

| Segment | n | DOM median | List-to-contract median | L2C Q1 / Q3 |
|---|---|---|---|---|
| All closed sales | [n] | [d] | **[d]** | [d] / [d] |
| Subject configuration | [n] | [d] | **[d]** | [d] / [d] |
| Subject price band | [n] | [d] | **[d]** | [d] / [d] |
| [Narrower band] | [n] | [d] | [d] | too thin to rely on |

A band under roughly n=8 is disclosed and set aside, never hidden and never
leaned on.

## Pricing behavior — compute every time

- Median sale price to **list** price
- Median sale price to **original** list price
- Percentage of closed sales taking at least one price cut

## The pricing-failure principle

**Exposure time presumes the property is priced at the appraised value.** A sale
that sat a long time because it was listed far above its worth is not evidence
that a correctly priced property needs that long.

Examine the long tail. For each long-market-time sale, compare original list to
eventual sale price. Where the long times are pricing failures, name them
specifically and exclude them from the conclusion.

Shape of the paragraph:

> Both long market times in that band were pricing failures. [ADDRESS] listed at
> [ORIGINAL LIST] and sold at [SALE PRICE] after [N] days. [ADDRESS] cut from
> [PRICE] to [PRICE] over [N] days. Two priced correctly and sold fast —
> [ADDRESS] in [N] days, [ADDRESS] in [N] days. Exposure time presumes pricing at
> the appraised value, so mispriced outliers do not support a longer conclusion.

Addresses in the finished document come from **this assignment's export** and
nowhere else.

## Supply side — requires the active/pending export

| Metric | How |
|---|---|
| Absorption rate | Closed sales divided by months spanned |
| **Months of supply** | Active listings divided by absorption rate |
| Pending ratio | Under contract divided by active |
| Median market time of unsold active inventory | Directly, as of the effective date |
| Actives having already cut price | Count and percentage |

## The two corroborations — run both

1. **Unsold inventory age against the closed-sale median.** When actives have
   been sitting about as long as closed sales took to go under contract, the two
   sides of the market agree.
2. **Price-cut rate, actives against closed sales.** Same logic.

Agreement is the strongest support available and costs nothing once both exports
are in hand. Disagreement is also a finding — it means the market is turning, and
it moves marketing time off the exposure range.

## Direction of travel

- Quarterly median market times — directional lengthening, or oscillation?
- Quarterly median sale-to-list ratio — a steady drift down is **mild softening**
  and supports marketing time at the **upper end** of the exposure range rather
  than the middle.

## Concluding

State the exposure bracket and the marketing time with the reason named:

> Exposure [LOW] to [HIGH] days; marketing time [X] days, at the upper end
> because [NAMED REASON].

The conclusion may sit above or below the raw Q1–Q3 midpoint. **Never hand back a
raw quartile range as the answer** — show what moved it.

## Stated limitations

- Closed-sale exports contain only listings that sold. Expired and withdrawn
  listings are absent, so the sample understates time for everything offered.
- Exposure time rests on closed sales. Marketing time rests on current inventory.
  Say which evidence carries which conclusion.
- Closed-sale exports under-report the newest months — recent contracts have not
  closed. Check the last two months by contract date.
- Both conclusions are ranges or points, not precise figures.

## Workfile practices worth carrying

- A **corrections log** of superseded analyses, so a reviewer sees what changed
  and why.
- An **open items** list resolved before delivery.
- When the subject's own sale was atypical (auction, REO, published legal
  notice), **reconcile it against the market-derived exposure time** rather than
  ignoring the difference.

## Prose

The method above is analytical shorthand. Finished narrative follows the voice
rules in `house-rules.md` — first person, active, short sentences, no sentence
starting with "The", no adjective without a number. Take the analysis; write the
sentences fresh.
