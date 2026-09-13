---
name: sales-contract-analysis
description: Read and analyze the sales contract on a Pinewood Appraisal purchase assignment — every page rendered, counter offers first — and produce a contract summary workfile plus the paste-ready 1004 contract-section comment. Pulls price, binding agreement date, closing date, financing type, earnest money, seller-paid concessions with the FHA/IPC test, buyer and seller names checked against the order and the owner of public record, as-is and resolution-period terms, appraisal contingency, personal property, lead paint, PUD/HOA. Use when Todd says "summarize the contract", "contract analysis", "read the sales contract", "what does the contract say", "what are the concessions", "is the seller the owner", or drops a purchase agreement, counter offer or amendment into a job folder. Runs automatically inside report-prep on every purchase.
---

# Sales contract analysis

Read `C:\Users\toddp\.claude\appraisal\house-rules.md` first. Every rule there
applies — the voice rules for the paste-ready block, the refusal gate, and
section 9's isolation rule: every figure in the summary traces to a page image
of THIS assignment's contract, or it is deleted.

Then read `references/form-landmarks.md` — where each fact sits on the
Tennessee REALTORS forms and the builder forms, and the traps that produced
wrong findings on real files.

Produces, in the job folder:

- `SALES CONTRACT - summary.txt` — the full read, document by document, every
  figure with its page and which document governs it
- inside it, a **paste-ready 1004 contract comment**, one line, no wraps

It does not write value conclusions. It hands facts to `workup`, to the
narrative skills, and to `final-read`.

---

## Why this skill exists

Three contract-section errors shipped in drafts in one week, and none of them
looked wrong: another file's lender and transaction type pasted into a
refinance; a concession narrative that said "$22,500 after a counter offer"
when the counter said $25,000 and nothing anywhere said $22,500; and a
seller who had taken title by executor's deed ten weeks before contracting,
visible only by matching the contract's deed reference to the parcel record.
Every number on the 1004 contract section is checkable against a signed page.
This skill does the checking before the draft exists.

## Step 1 — Get the documents, all of them

Look in the job folder for anything named contract, purchase, agreement,
counter, amendment, addendum, RF401, RF651, RF657, F9. If the folder holds
nothing, the tracker backup carries contracts as base64 attachments —
`final-read/references/extraction.md` has the snippet. Do not ask him for a
contract that is on his machine.

Count the documents and their pages before reading anything. A counter offer
is often the FIRST page of the same PDF as the agreement it modifies, and
amendments (RF657 closing-date amendments especially) arrive as separate
files later. The summary names every document read.

## Step 2 — Rasterize. Never trust the text layer.

Contracts arrive as fax scans, as vector-outlined text, or with scrambled
ToUnicode maps that extract as cipher text. Sometimes the counter offer page
extracts cleanly and the agreement behind it does not. Rule: **render every
page to PNG and read the images.** If the text layer happens to be clean,
use it only to locate pages; every figure still gets confirmed on the image.

```
& "<poppler>\pdftoppm.exe" -png -r 110 "<contract.pdf>" "<outdir>\k"
```

Checkboxes are pixels. The loan-type box, the appraisal-contingency box, the
financing-waived box, the greenbelt box, the ACCEPTS / COUNTERS / REJECTS
box — all read from the image, never from text.

## Step 3 — Read in the order that governs

1. **Counter offers and amendments first**, newest last. A counter's numbered
   exceptions REPLACE the matching terms in the original agreement
   (concessions, earnest money and its holder, title expenses, inspection
   and resolution terms, closing date). Terms the counter does not touch
   stay in force — a seller-paid buyer-agent commission in the original
   Special Stipulations survives a counter that only re-states concessions.
   Write down, for every figure, which document it came from.
2. **The agreement**, page by page, using `references/form-landmarks.md`.
3. **The signature page last**: who signed, which response box the seller
   checked, and the **acknowledgement-of-receipt line — that is the Binding
   Agreement Date.** The offer date is not the contract date.

## Step 4 — Pull these, every time

| Item | Where it goes | Check it against |
|---|---|---|
| Buyers (names on the deed line, not just the header) | 1004 Borrower | the order sheet — a difference needs an addendum comment (FCM requires it in writing) |
| Sellers | "Is the seller the owner of public record?" | parcel layer / TPAD owner. Surname match. A mismatch is a finding: estate, flip, assignment, or wrong parcel |
| Deed book/page or instrument on the contract | subject prior-transfer analysis | TPAD sale history — if the reference matches a recent deed, it DATES the seller's acquisition |
| Purchase price, numeral AND words | Contract Price | the two must agree; builder forms have a price table where the base price is not the price |
| Binding agreement date | Date of Contract | acknowledgement of receipt on the signature page |
| Closing date | contract narrative | RF401 4.A; amended by RF657 if one exists |
| Financing type box | narrative; the order's loan type | "Other: THDA" beside an FHA case number is normal — THDA is FHA-insured underneath. Conventional box beside a 96.5% loan figure is still conventional |
| Loan-to-price, financing contingency waived or not | narrative | |
| Appraisal contingency, which box | narrative | box 1 = NOT contingent; box 2 = contingent — read the pixels |
| Earnest money, holder, refundability | narrative | counter usually changes all three |
| Seller-paid concessions: amount, purpose, payer | Financial assistance Yes/No + amount + description | original Special Stipulations vs counter. Compute the share of price; FHA cap 6%; conventional IPC cap by LTV. Seller-paid buyer-agent commission is reported separately and named — let the lender classify it |
| Closing-cost and title-expense split | narrative | counter overrides |
| Personal property included / excluded | narrative | anything with value allocated to it adjusts price |
| As-is, inspection period, resolution period | narrative; feeds condition/subject-to logic | "no resolution period" means the buyer cannot compel repairs — FHA MPR still applies |
| Lead-based paint disclosure box | condition section on pre-1978 houses | |
| Greenbelt boxes | site section | |
| PUD / HOA / dues / transfer fees | 1004 PUD block — builder forms bury these | see `sales-contract-bridge` memory for the negation trap ("IS NOT") |
| Agents and brokerages | verification sources | |
| Anything unusual: assignments, seller financing, leasebacks, repair escrows, price adjustments, "special discounts" | flags | a builder "Sales Price Adjustment" is a price reduction, not seller-paid assistance — report it, do not put it in the concession amount |

## Step 5 — The tests

- **Numeral vs words.** If they disagree, say so; do not pick one.
- **Seller vs owner of record.** Run it; write the result either way.
- **Concession share.** amount / price, to two decimals, against the
  program cap. Say "inside" or "exceeds"; never round it away.
- **The leftover-deal test.** Every price, date, party and count you are
  about to write must exist on a page you rendered from THIS folder. If it
  came from memory of another file, it does not go in.
- **Order vs contract.** Loan type, borrower name, property address, lender —
  each pair either agrees or is written up as a difference.

## Step 6 — Refuse rather than guess

If price AND parties cannot be read from the images (handwriting, an
illegible fax), say exactly that, name the pages, and stop. A blank contract
price is a gap he can see; a guessed one is a liability. Partial reads are
normal — write what was read, list what was not, by page.

## Step 7 — Write the file

`SALES CONTRACT - summary.txt`, sections in this order: documents read (with
page counts and which governs); parties and property; price and dates;
financing; earnest money; seller concessions and seller-paid items (original
vs counter, share of price, cap test); closing costs and title; inspections
and condition terms; other (greenbelt, lead paint, warranty, FIRPTA, agents);
**"FOR THE 1004 CONTRACT SECTION — the figures that go on the form"**; then
the paste-ready comment.

The paste-ready comment: one line, first person, active, no sentence
starting with "The", every figure sourced, no wraps. Shape:

> I analyzed the executed [FORM] dated [OFFER DATE] and Counter Offer #[N]
> accepted [DATE], which is the binding agreement date. [BUYERS] agreed to
> purchase this property from [SELLERS] for $[PRICE] with a [CLOSING DATE]
> closing, [FINANCING], [as-is / inspection terms], and the seller agreed to
> pay $[AMOUNT] toward [PURPOSE], which is [X.XX] percent of the purchase
> price and [inside / above] the [PROGRAM] limit on seller contributions.
> [Seller-acquisition sentence if the deed reference dates it.]

## Step 8 — Report back

Flags first: anything that contradicts the order, the parcel record, or the
draft if one exists; any cap exceeded; any name or date that appears two
ways; anything unreadable. Then the figures that go on the form, one line
each. Then the path.
