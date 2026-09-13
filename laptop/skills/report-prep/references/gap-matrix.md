# The merged gap matrix

Every input the six bundled skills need, collapsed into one table so Todd is
asked once. This carries **no assignment data** — it is the question list, not
answers.

Source tables this merges, and which stay authoritative for their own detail:
`workup/references/inputs-and-gaps.md`, plus the Step 1 sections of
`neighborhood-description`, `highest-and-best-use`, `exposure-marketing-time`,
`site-improvements`, and `overall-quality-condition`.

Skill keys: **C** sales-contract-analysis · **W** workup · **N** neighborhood · **H** H&BU ·
**E** exposure/marketing · **S** site improvements · **Q** overall quality & condition

---

## Found automatically — never ask for any of these

Run the lookup instead. House-rules section 7. One pass serves all six.

| Input | Needed by | Where |
|---|---|---|
| Order number, client/AMC, lender, borrower, product, loan type, fee, due date | W | tracker record, or `Order.pdf` in the job folder |
| Inspection date and time | W Q | tracker record |
| Coordinates, county, census tract, urban/rural flag | W N H E | tracker `pub.geo`, or Census Geocoder now |
| Parcel number, owner of record, subdivision, plat, deed | W N H S | tracker `pub.parcel`, or the county/state parcel layer |
| Year built, assessor living area, land/improvement/total value | W N H S | same |
| Acreage and lot dimensions | H S | same |
| Flood zone, SFHA, FIRM panel, map date | W N H | tracker `pub.flood`, or FEMA NFHL layers 28 and 3 |
| Tax estimate, rate, city-limits code | W N | tracker `pub` |
| Outbuildings of record | S | parcel record's outbuilding section |
| Order, contract and bid PDFs | W E S | base64 in the tracker backup `attachments` — write them out, do not ask |
| UAD 3.6 field definitions | Q S | `OneDrive\Desktop\UAD 3.6\Appendix F-1 URAR Reference Guide v1.2.pdf` |

**The urban/rural flag is a real input to the Location checkbox.** Use it, but it
does not overrule what he observed on inspection.

**Point-in-polygon usually misses** — the Census geocode lands in the
right-of-way. Match on address text first, buffer spatially only as a fallback.

---

## Required — say plainly which sections stop

| Input | Needed by | Without it |
|---|---|---|
| **MLS export, closed sales**, 12 months back from the effective date | W E N | **Stop W and E.** No comp analysis, no condition tiers, no regression, no exposure bracket. N loses its price and age ranges and its market-conditions box. Tier A H&BU still runs |
| **Effective date** | W N H E S | Ask. **Do not assume the inspection date, and do not assume today.** It ages the data, sets the time origin, and fixes the exposure/marketing boundary |
| **Zoning district of record** | H | No legally-permissible test, so no four-test analysis. **Never infer it from surrounding use.** Davidson publishes it; Rutherford, Williamson and the state layer do not. For municipalities the code is usually retrievable — `highest-and-best-use/references/zoning-sources.md` |
| **Measured GLA and room count** | W H N | Run every indication across a GLA range and say the assessor and his measurement disagree, and by how much |
| **His inspection observations** — exterior rating, interior rating, per-kitchen and per-bath update status and time frame, defect list with each Recommended Action, as-is vs subject-to, any ADU or living-area outbuilding | Q | No Q&C section at all. Condition is his observation only — never from listing photos, public records, or a prior report |
| **Photos or inspection notes or supplied listing media** | S | No site-improvements inventory. A number built on an imagined driveway is a liability |
| **Opinion of value** | E H | SR 1-2(c) requires exposure time be linked to the value opinion. Without it there is no exposure conclusion to state |

---

## Strongly wanted — name the cost, then proceed without it

| Input | Needed by | Without it |
|---|---|---|
| **MLS export, active + under contract**, as of the effective date | E W N | Marketing time is **not supported** — no absorption, no months of supply, no pending ratio, no unsold inventory age. State it equals exposure time as a **disclosed assumption**, in the workfile and the report narrative and the 1004 grid checkbox. Never present it as a finding |
| **Utilities — well/septic or public water/sewer** | S H | Gates the two biggest hidden site-improvement items. Septic commonly carries a few thousand as-is. **Ask; do not guess and do not silently omit** |
| Sales contract | C W | No contract analysis section. FNMA requires the contract be analyzed on a purchase — flag it as an open item. Concessions, non-conveying items, binding date, financing, seller vs owner of record all go unanalyzed. When present, `sales-contract-analysis` (key C) reads it — every page rendered, counter offers first — and hands the workup its price, binding date and concessions |
| His own recent appraisals in this market | S | Loses the strongest cost-new support and cross-check #1. Web cost guides are **screening only** — cite URL and retrieval date and label them |
| Contractor bids | W S | No feasibility section. Say the scope is unpriced |
| Neighborhood boundaries he has drawn before | N | Nothing lost, but consistency across his files matters. **Confirm it is the same market area before reusing, and say that you are reusing them.** Never carry a boundary across a different city or submarket |
| Prior report or work file for this property | W H N | Nothing lost; note it was not available |
| Site value, cost new from his cost approach | H S | Only if the analysis escalates. Ask only then |

---

## Assignment-type branches — ask only when the type is actually this

Do not lead with the rare branch. Nearly all of his work is a 1004 on an ordinary
single-family house in average condition. A workup that opens with a
distressed-tier analysis on a normal refinance answers a question nobody asked.

| Type | Extra input | Why |
|---|---|---|
| Renovation / 203(k) / subject-to | work write-up, plans and specs | The value that sizes the loan is the **as-completed** value. Q also needs the as-is overall condition rating, and the two ratings must differ in the direction the repairs explain |
| Purchase | contract with concession detail | Concessions must be reported and analyzed for their effect on price |
| New construction | confirmation it meets the definition | Q: update statuses read Fully Updated and overall condition is C1. Flipped from UAD 2.6 |
| Rental / 1007 | rent roll, management-company rents | MLS rentals under-report management-company inventory — an MLS-only screen is a floor, never a ceiling |
| Land | zoning of record, utility availability | Legally permissible and physically possible both fail without them |
| Servicing / drive-by | scope of work from the client | Interior is unobserved; every indication must say so |

---

## The two failure modes this table exists to prevent

1. **Asking for what is already on his machine.** The tracker record and the
   `pub` block cover most of the assignment facts. Asking for them reads as not
   having looked — and in a six-skill run, asking six times reads worse.
2. **Silently substituting.** Exposure bracket used as marketing time without the
   active export. Assessor living area used as measured GLA. A prior file's
   neighborhood boundaries. Each produces a document that looks complete and is
   not. **Every substitution gets said out loud, in the document, at the place it
   happened.**
