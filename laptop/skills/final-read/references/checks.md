# The check catalog

Run every section. Each check names its failure mode — most were caught
(or missed and then caught) on real files. Severity guide: a conflict
with a signed document or the report's own exhibit outranks a UAD
machine-check, which outranks a client-requirement gap, which outranks
housekeeping.

## 1. Contract section vs the signed contract

- Contract price field vs the contract's sales-price table.
- Date of Contract field vs the EXECUTED date on the signature page —
  and the narrative's date vs the field. They have drifted apart after a
  partial fix: narrative corrected, field left wrong.
- Closing date, earnest money, financing type (conventional/FHA/VA
  checkbox on the contract's financing page).
- Concessions: amount AND payer AND what for, vs the contract —
  including OTHER PROVISIONS, where FSBO credits hide. A disclosed
  concession has been wiped to "No / $0" by a later edit; on every
  delta pass re-verify it.
- Parties: seller matches owner of public record (see TPAD/parcel
  checks); buyers vs borrower field.
- **The leftover-deal test:** every number, date, and count in the
  contract-analysis narrative must exist in this file's documents. A
  price, a "counter 3," or a closing date that matches nothing is
  another assignment's text pasted in. This is the single most damaging
  error class — everything in it looks plausible.

## 2. Subject and site facts vs public record

- Owner of public record vs parcel layer (OWNER2 single-space rule) and
  vs the contract's seller.
- Prior sales: TPAD sale history WITH qualification codes vs the grid's
  subject column. Non-arm's-length codes (family sale, quitclaim)
  belong in the analysis when the current price sits far above an old
  transfer. Mind the 3-year window edge — a transfer 37 months back is
  outside Cert 5's duty but still worth a disclosing sentence if data
  vendors show it.
- Legal description book/page vs TPAD's deed reference (they have
  matched and thereby DATED the real transfer).
- Taxes: TPAD City # non-zero means city tax exists — a county-only
  figure understates.
- FEMA block, census tract, GLA-vs-courthouse (ANSI note should explain
  a difference), year built, lot size.

## 3. UAD machine checks (what CU reads)

- **Condition string vs condition narrative vs effective age.** The
  update-status phrase in the UAD string ("No updates in the prior 15
  years", "Kitchen-updated-one to five years ago") describes KITCHENS AND
  BATHROOMS ONLY - Todd's correction, 2026-09-10. Compare it only against
  what the narrative says about kitchens and baths: "No updates" beside a
  remodeled kitchen in the narrative is a contradiction; "No updates"
  beside a new HVAC, roof, windows or foundation work is NOT. Mechanical
  and structural work shows up in the C-rating and the narrative, never in
  that phrase. An effective age far under actual with no kitchen/bath
  update and no stated reason is still worth a question.
- **Same-rating adjustments.** A condition/quality adjustment between
  same-rated properties (C3 vs C3) needs explanatory commentary in the
  report; absent commentary, flag. With commentary, check it is applied
  CONSISTENTLY — same basis, same direction, across all comps sharing
  the trait.
- **Inconsistent treatment of equal features.** Same rating or same
  characteristic adjusted on some comps and zeroed on others with no
  stated reason (condition, site size). State the threshold or adjust
  all.
- **The livability / soundness / structural-integrity box is major-only.**
  Never flag "No" beside a repair list, a subject-to, or an MPR item; only
  beside a documented major condition (see section 4).
- **Both boxes checked** on a Yes/No question — TOTAL allows it; render
  to catch it. Also NEITHER box checked on required grids (Built-Up,
  Growth have both shipped empty).
- Room/bed/bath counts photo-page vs grid vs improvements section.
- UAD field formats: stray "$0;;", empty description halves.

## 4. The report against its own exhibits

Rasterize every exhibit and reconcile:

- Market analysis exhibit (TrueTracts) vs the form: its trend verdict
  vs Property Values checkbox; its months-of-supply CLASSIFICATION vs
  the Demand/Supply checkbox (the exhibit has printed "In Shortage"
  while the form said "In Balance" — one page turn apart); its DOM vs
  Marketing Time.
- **Time adjustments vs the exhibit's monthly table, keyed to each
  comp's CONTRACT month.** Multiply the month's percentage against the
  comp's price; the grid figure should match within rounding. Zeros
  where the table says a small number are fine if a rounding threshold
  is stated or evident — suggest one sentence naming it. Never flag
  shape (non-monotonic is normal); the only failure is no derivation
  at all.
- Location adjustments vs the heatmap (comps in "similar" zones support
  zeros).
- Sketch vs improvements section (rooms, GLA, porches/decks — anything
  with contributory value must appear on the sketch).
- **Repair lists vs photos and notes (the leftover test, applied to
  repairs).** Every item on an MPR sentence, a repair guide, or a subject-to
  line must trace to a photo caption or a sentence in his condition
  narrative. A plausible repair item with no photo and no note (a gutter, a
  switch plate, a door-trim hole, limbs on a roof) is presumed carried in
  from another file's addendum until he confirms it - the same rule as
  contract-section leftovers. Missed on 2161 Verona Caney, 2026-09-10: I
  built a repair list from a page-3 MPR sentence he did not recognize.
- Photo captions vs the form. A caption documenting a defect (broken
  handrail, deck rot, a roof patch) must appear in the condition narrative
  and, where warranted, on the repair list. It does NOT flip "physical
  deficiencies affecting livability, soundness or structural integrity" to
  Yes - Todd's rule, 2026-09-10: that box is for MAJOR conditions only (no
  windows, a hole in the roof, a failed system). Deferred maintenance, MPR
  items and subject-to letters live under a No. Flag a No only when the
  photo shows something at that threshold, and name the specific fact.

## 5. Internal consistency, form-to-form

- Range statements above the grid must bracket the comps actually used
  — sales range vs comp prices, listings range AND COUNT vs the actives
  and pendings in evidence.
- Neighborhood boundaries vs the neighborhood description vs where the
  comps sit. Comps outside the stated boundary need the search-radius
  comment, and the description must not name a different boundary than
  the boundary line.
- One-unit price/age range vs subject (outside-the-range needs the
  Fannie explanation) and vs the contract price.
- Present land use percentages total 100.
- Reconciliation vs the approaches: "cost approach was completed" with
  a blank cost page (or vice versa); income "$0" vs "not developed."
- Cost approach arithmetic: depreciation ÷ cost-new vs effective age /
  (effective age + REL) — age-life should roughly reconcile or a method
  note should say why not. Site value + DCI + site improvements = the
  indicated value. A $0 site-improvements line on a parcel with a
  driveway is a gap (the site-improvements skill produces the number).
- Car storage page 1 vs grid subject column vs photos vs assessor
  outbuilding/driveway lines.
- Value conclusion inside the adjusted range, bracketed; effective date
  consistent everywhere; file numbers consistent.

## 6. Client / order-sheet requirements

Extract the order sheet's requirement list on the first pass and keep
it in the review doc. Recurring Rocket/ServiceLink items, but re-read
each order's own list:

- 12-month statistical market-conditions data IN THE REPORT, supporting
  the trend boxes and the time adjustments or their absence.
- Adjustment support commentary beyond the generic tool-name paragraph
  (the Selling Guide quote: "a statement only recognizing that an
  adjustment has been made is not acceptable").
- Cosmetic deficiencies noted but NOT subject-to; health/safety items
  ARE subject-to.
- ANSI measurement, with the courthouse-vs-measured note.
- Which forms are and are not required (1004MC, cost approach, REL) —
  do not flag a missing form the order sheet waives, and do flag one it
  requires.
- Purchase-contract discrepancy instructions (verify address, owner,
  APN; report discrepancies).

## 7. Language

- No "average"/"mean"/central-tendency figure in narrative — ranges and
  brackets. Workfile-only stats stay in the workfile.
- Bias/fair-housing scan: no feel-words (quiet, desirable, safe, "good
  schools"), nothing demographic; factual and countable only.
- Dictation artifacts: read for SENSE — plausible wrong numbers and
  homophone proper nouns pass spell-check. Verify dictated numbers
  against the workfile.
- Broken sentences and orphaned fragments in explain fields (an
  "If not, explain" field with content beside a "did" answer).
- Voice on anything paste-ready: first person, active, no sentence
  starting with "The", no adjective without a number, one line, no
  hard wraps.

## 8. Draft-state blanks

List them so nothing ships empty, marking which are expected on a
draft: value opinion, signature date, and which are NOT expected:
required checkboxes, land-use percentages, cost-approach support
fields the order sheet asks for (quality rating, cost-data date).
