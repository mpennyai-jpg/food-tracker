# Discovery — turning a pointer into a full input set

He points at one thing. Find the rest here, in this order, and report what you
found before analysing anything.

## 1. The job folder

Under `C:\Users\toddp\OneDrive\Desktop`. His convention is
`<street address> <city or client> <MM-DD>`, in any order, sometimes with the AMC
name appended. Match on **street number plus street name**, not the whole string.

If an inner folder named for the bare address exists, that is the one.

**Do not create a job folder, and never create a new top-level OneDrive folder
from this laptop** — it jams sync against the desktop machine permanently. If no
folder exists, ask where it is.

## 2. The tracker record

The Appraisal Tracker's live data sits in the desktop machine's browser, which is
not reachable from here. What **is** reachable is its automatic backup:

```
C:\Users\toddp\OneDrive\Appraisal Tracker\Appraisal Tracker - Backups\
    appraisal-tracker-auto-<date> <time>.json
```

Take the **newest** file. Structure:

```
{ "version": 2,
  "data": { "files": [ {record}, ... ], "notes": [...] },
  "attachments": { "<attachment id>": "data:application/pdf;base64,..." } }
```

Match the record on `address`. Useful fields on it:

`orderNo, loanNo, amc, lender, borrower, address, city, statezip, county,
product, loanType, assignmentType, fee, orderDate, inspectionDate,
inspectionTime, dueDate, status, notes[], attachments[], purchase, contract{},
pub{}`

`pub` holds the whole public-records block — `geo` (lat/lon, tract, urban/rural),
`parcel` (APN, owner, year built, living area, values, assessed, city code,
plat, deed, subdivision), and `flood`. **Use these coordinates for the distance
column** rather than geocoding again.

**The backup can be up to six hours behind.** If the record is missing or looks
older than what he describes, say so and work from the job folder instead — do
not assume he is wrong.

### Build the document from the record, first thing

`scripts/from_tracker.py` turns the record into the Part 1 skeleton — assignment,
contract items, subject public record — with every unknown rendered as a visible
open slot rather than left silently blank, and the record's attachments written
out as real files:

```
python3 ~/.claude/skills/workup/scripts/from_tracker.py "739 Lakeview" \
    --out body.html --attach-dir "<job folder>"
python3 ~/.claude/skills/workup/scripts/from_tracker.py --list      # recent orders
```

Run it **before** anything else, and build the HTML off it right away. The
document then exists from the order forward and the rest of the work appends to
it. It also does the cross-checks that are cheap here and expensive later: seller
on the contract against owner of record, status against inspection date, empty
concessions against a purchase.

Re-run it any time to pick the record back up; it overwrites the fragment, so
keep hand-written Part 1 edits somewhere else or make them after this runs.

### Pulling attachments out of the backup

The order PDF, sales contract and bids are embedded base64 in `attachments`,
keyed by the ids on the record. When the job folder is missing one, write it out
of the backup into the scratch directory rather than asking him to re-send it:

```python
import json, base64
d = json.load(open(backup, encoding="utf-8"))
rec = next(f for f in d["data"]["files"] if f["address"].startswith("<street>"))
for a in rec["attachments"]:
    blob = d["attachments"].get(a["id"])
    if blob:
        open(a["name"], "wb").write(base64.b64decode(blob.split(",", 1)[1]))
```

## 3. The MLS export

`C:\Users\toddp\OneDrive\Penny Share\` — he drops exports there, usually named
for the subject. Also check the job folder itself.

A RealTracs export is ~166 columns. The ones this workup uses:

| Purpose | Column |
|---|---|
| Identity | `MlsNumber, ListingStatus, Address, City, Subdivision, PropertySubType` |
| Physical | `YearBuilt, SqFtTotal, SqFtMainFloor, SqFtSecondFloor, SqFtMeasurementSource, TotalBedrooms, TotalFullBaths, TotalHalfBaths, Acres, LotSize, NumOfStories, Basement, GarageSpaces, CarportSpaces, RoofMaterial, ConstructionType` |
| Price | `ListPrice, OriginalListPrice, SalesPrice, SalesPricePerSqFt` |
| Timing | `ListDate, BindingContractDate, ClosedDate, DaysOnMarket, ListToContractDays, ContractToCloseDays, OffMarketDate, CancelledDate` |
| Terms | `BuyerFinancing, SellerParticipation, ClosingTerms, ContingencyType` |
| Location | `Latitude, Longitude, County, ParcelIdDisplay` |
| Everything else | `Remarks` |

**`ListToContractDays` is the measurement basis, `DaysOnMarket` is not.** DOM
resets when a listing is withdrawn and relisted. They disagree on most rows of a
typical export, and DOM understates real exposure. Carry both, report both
medians, and state the disagreement count for **this** export — `prep.py` counts
it for you.

`SellerParticipation` is the concessions field. `SqFtMeasurementSource` tells you
whether a comp's area came from an assessor or a measurement, which matters
before a GLA adjustment leans on it.

## 4. What the export cannot see

Say this in the document rather than leaving it implied:

- Expired and withdrawn listings are absent, so exposure looks shorter than it was.
- Relists reset DOM.
- The newest months under-report — sales still closing have not entered the data.
- Management-company rentals never appear at all.
- Remarks are marketing copy. They are evidence of how a property was presented,
  not a condition inspection.

## 5. Reading the PDFs in the folder

- Text-layer PDFs: `pdftotext -layout`.
- Scans: they have no text layer. The order and contract readers on the desktop
  helper handle those; from here, say which file is image-only and what it needs.
- **Photo audits:** count embedded images per page rather than trusting a visual
  skim — that is how empty labelled slots get caught before the client finds them.
