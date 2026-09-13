# Inputs — what each one unlocks, and what to say when it is missing

This is the table behind the gap report in SKILL.md step 1. Post the gap report
**before** starting the analysis, in one message.

## Found automatically — never ask for these

| Input | Where | Gives |
|---|---|---|
| Order details | tracker record, or `Order.pdf` in the job folder | order #, client/AMC, lender, borrower, product, loan type, fee, due date, inspection date and time |
| Public records | tracker record's `pub` block, or a live lookup now | parcel #, owner of record, year built, assessor living area, land/improvement/total value, assessed value, city-limits code, plat, deed |
| Flood | same | zone, SFHA, FIRM panel, effective date |
| Census | same | tract, urban/rural, coordinates for the distance column |
| Tax estimate | same | annual estimate, rate, whether the city rate applied |
| Zoning | Davidson only | legally-permissible analysis. **Never infer zoning** anywhere else |

If the tracker record has no `pub` block, run the lookup rather than asking.

## Required from him — the analysis cannot proceed without them

| Input | Unlocks | Without it |
|---|---|---|
| **MLS export, closed sales** | everything: condition tiers, regressions, paired sales, comp candidates, exposure time | **Stop.** No workup. Ask for it and say why |
| **Effective date** | ages the data, sets the time origin, fixes the exposure/marketing boundary | Ask. Do not assume the inspection date or today |
| **Measured GLA and room count** | every value indication, and the bath/bedroom variables | Run all indications across a GLA range and say the assessor and his measurement disagree |

## Strongly wanted — name the cost when they are missing

| Input | Unlocks | Without it |
|---|---|---|
| **MLS export, active + under contract** | marketing time, absorption, months of supply, unsold inventory age, the as-is ceiling from current competition | Marketing time is **not supported**. State it equals exposure time only as a disclosed assumption, in both the workup and the report narrative |
| Sales contract | concessions, non-conveying items, buyer-side fees, binding date, financing type, seller identity vs owner of record — produced by the `sales-contract-analysis` skill; read its `SALES CONTRACT - summary.txt` rather than re-reading the PDF | No contract analysis section. FNMA requires the contract be analyzed on a purchase — flag it as an open item |
| His inspection notes or photo set | condition rating, defect list, what the renovation scope actually covers, photo-slot audit | Condition of the subject is his input only. Do not infer it from the listing remarks |
| Contractor bids | renovation scope, feasibility check, as-completed reconciliation | No feasibility section. Say the scope is unpriced |
| Prior report or work file for the same property | consistency with his earlier conclusions | Nothing lost; note it was not available |

## Assignment-type specific

| Type | Extra input | Why |
|---|---|---|
| Renovation / 203(k) / subject-to | work write-up, plans and specs | The value that sizes the loan is the **as-completed** value. Without the write-up the as-completed set is a guess at scope |
| Purchase | contract, plus concession detail | Concessions must be reported and analyzed for their effect on price |
| Rental / 1007 | rent roll, management-company rents | MLS rentals under-report management-company inventory. An MLS-only screen is a floor on the evidence, never a ceiling |
| Land | zoning of record, utility availability | Legally permissible and physically possible both fail without them |
| Servicing / drive-by | scope of work from the client | Interior condition is unobserved; every indication must say so |

## How to write the gap report

Three short lists, then stop and let him answer:

```
Found: <the files and records, with paths>
Missing, and what it costs:
  - <input> — <the specific section or conclusion that cannot be produced>
Starting now on: <what you can already do without the missing items>
```

Do not pad it. He reads this on a phone between inspections.

## The two failure modes this table exists to prevent

1. **Asking for what is already on his machine.** The tracker record and the
   public-records block cover most of the assignment facts. Asking for them
   reads as not having looked.
2. **Silently substituting.** Using the exposure bracket as marketing time
   without the active export, or the assessor's living area as measured GLA,
   produces a document that looks complete and is not. Every substitution gets
   said out loud, in the document, where it happened.
