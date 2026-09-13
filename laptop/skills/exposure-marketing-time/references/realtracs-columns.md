# Reading a RealTracs export

Column names and parsing traps. **No assignment data in this file.**

RealTracs ships roughly **166 columns** per export.

## Columns that matter

| Need | RealTracs column |
|---|---|
| **Exposure time — use this** | **`ListToContractDays`** |
| MLS days on market (resets on relist — not the primary measure) | `DaysOnMarket` |
| List date | `ListingContractDate` / `OnMarketDate` — confirm which exists |
| Contract date | `BindingContractDate` |
| Close date | `ClosedDate` |
| Sale price | `SalesPrice` |
| List price | `ListPrice` |
| Original list price | `OriginalListPrice` |
| GLA | `SqFtTotal` |
| Cumulative days on market | check for a `CDOM`-style column |
| City | `City` |
| Free text | `Remarks` |

Dates arrive as `m/d/yy` — two-digit year. Status filters to `Closed` even though
the export file is named `All - <timestamp>.csv`.

## Two exports, not one

- **Closed sales**, 12 months back from the effective date — supports exposure
  time.
- **Active + under contract**, as of the effective date — supports marketing
  time: absorption, months of supply, pending ratio, median market time of unsold
  inventory, share of actives that have already cut price.

Exposure time rests on closed sales only. Marketing time cannot be properly
supported without the second export. Ask for both up front.

## Three parsing traps that produced silently wrong answers

1. **Quoted newlines.** `Remarks` contains line breaks inside its quotes.
   Splitting on newlines before handling quotes inflated a file by more than 50%
   in malformed rows *while still looking like it worked*. Parse with a single
   character-level pass that tracks quote state across row boundaries. Verify the
   row count against `Import-Csv`.

2. **Near-miss column names are lethal.** `SalesPricePerSqFt`,
   `ListPricePerSqFt`, `OriginalListPrice`, and nine `SqFt*` columns including the
   free-text `SqFtMeasurementSource` all match loose patterns. Match the exact
   name first; never accept a substring match without checking what else it hits.

3. **Never let stale results survive a failed run.** Over-filtering to zero sales
   must clear everything, not leave the previous segment's numbers in a draft.
   That is a straight path to the wrong analysis in a workfile — and, across two
   assignments in one sitting, the wrong analysis in the wrong report.

## The recent-months lag

Grouped by contract date, the most recent month is usually **empty** in a
closed-sale export — recent contracts have not closed, so they are not in the
file.

Check the last **two** months, not three. A three-month average lets one healthy
month mask an empty anchor month.

For exposure time this matters: the sample skews toward older market conditions.
Say so in the workfile.

## Do not assume a trend exists

Middle Tennessee markets have repeatedly returned **no statistically supported
price trend** over 24 months under testing. Flat and noisy is a normal result, in
price and in market time alike.

## Related tools he already has

- `C:\Users\toddp\OneDrive\Appraisal Tracker\Market Conditions.html` — drop the
  same closed-sale CSVs there for the time-adjustment analysis. If it has already
  run for **this** assignment, reuse its segment definition so exposure time and
  the time adjustments describe the same market.
- `C:\Users\toddp\OneDrive\Appraisal Tracker\Feature Finder.html` — searches the
  `Remarks` free text for barns, pools, ADUs and other features the checkbox
  fields miss.
