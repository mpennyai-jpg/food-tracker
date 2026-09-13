---
name: final-read
description: Final Read — review a draft appraisal report PDF for a Pinewood Appraisal assignment before delivery — check every fact against the signed contract, the AMC order sheet, MLS data, and public records, run the UAD and internal-consistency catalog, and hand back a flags-first review document with paste-ready fixes. Handles first drafts, revision deltas ("dropped in the newest version"), and the final pre-signature pass. Triggers on "final read", "run the final read", "read this draft". Use whenever Todd asks to review a report, start the review, check a draft, do the final review, look over a file before delivery, or says he dropped a new version of a report PDF in a job folder — even if he only names the address and says "start the review."
---

# Final Read — draft, delta, and pre-signature

Read `C:\Users\toddp\.claude\appraisal\house-rules.md` and
`C:\Users\toddp\.claude\appraisal\uspap-citations.md` first. Every rule
there applies — the voice rules for anything paste-ready, the refusal
gate, and section 9's isolation rule: this review runs on exactly one
assignment, and every fact checked must trace to THIS file's documents.

Then read `references/extraction.md` before opening the PDF (the
text-layer traps in there each cost a real review a wrong finding) and
`references/checks.md` for the full catalog to run.

The product is one file in the job folder — `Draft N Review - <address>.txt`
or `Final Review - <address>.txt` — plus a flags-first report in chat.
No form narrative comes out of this skill; it judges, it does not write
report sections (the narrative skills do that).

## What a review is

Todd signs what ships. A reviewer, an underwriter, and Fannie's CU model
will read the report cold and cross-check it against itself, its own
exhibits, and the public record. This skill does that reading first,
with more sources than a reviewer has: the signed contract, the AMC
order sheet's actual requirement list, the MLS export, the assessor
record, and the tracker. A finding is only worth raising if one of those
sources — or the report itself — contradicts the statement. "Looks
unusual" is not a finding; "the exhibit on page 33 says Shortage and the
checkbox says In Balance" is.

## Step 1 — Inventory before opening the draft

Find the job folder (house-rules section 5) and list everything in it:
the draft PDF (newest by timestamp — he saves over or beside old ones),
order sheet, sales contract, MLS export(s), narrative workfiles from the
other skills, and any PRIOR review documents. Also pull the tracker
record for the order (fee, due date, loan type, contract extractor
notes — its `needsReview` flag and price-is-a-guess warnings matter).

If a source document is missing from the folder, check the tracker
backup JSON — order PDFs and contracts ride along as base64 attachments
and can be extracted (`references/extraction.md` shows how). Reviewing
a contract section without the contract in hand is guessing; get the
document or say plainly that the contract terms are unverified.

## Step 1a - Run the mechanical checker first

`python "C:\Users\toddp\OneDrive\Appraisal Tracker\Check-Draft.py" "<draft.pdf>"`
writes `<draft> - CHECK.txt` beside the PDF (built 2026-09-10). It reads the
text layer only and catches the mechanical class: leftover text from other job
folders, the reconciliation quoting the cost-approach figure as the sales
comparison value, acreage or GLA stated two ways, "no location adjustment"
beside location adjustments, range statements that do not bracket the comps,
the 90-day and radius sentences against the grid, cost-approach arithmetic,
FHA case number coverage, blank exhibit pages, 2-2(b)(x), "average".

Read its output before the PDF. Every flag in it still has to be confirmed
against a rendered page before it goes in the review (checkbox states and grid
columns are invisible to it). Its VERIFIED CLEAN list is what you do not
re-check by hand. Anything it missed that a reviewer would catch is a new
check to add to the script, not just a finding in the review.

## Step 2 — Extract, and respect the text layer's limits

`references/extraction.md` has the commands and the traps. The three
that produce WRONG FINDINGS, not just missing ones:

1. **Checkbox states are invisible in extracted text.** Both options
   print. Any finding about which box is checked — or whether two are —
   requires rendering the page to PNG and looking.
2. **Grid columns lose their alignment in text.** A prior-sale date that
   reads as the subject's can belong to comp 1's column. Never attribute
   a grid value to a column from text order alone; render the page
   before flagging. This exact misread went to Todd once as a MAJOR
   finding and had to be retracted.
3. **Exhibit pages carry no text.** TrueTracts market analyses, maps,
   and sketches are image pages (form SCNLGL). Text extraction seeing
   ~60 characters does not mean the exhibit is missing — rasterize
   before claiming absence, and rasterize anyway: the exhibits carry
   numbers the review must check against the form.

## Step 3 — Verify against every outside source

Work through `references/checks.md` section by section. The spine of it:

- **Contract vs contract section** — price, execution date, closing
  date, concessions, parties, financing type. Leftover text from a
  different assignment is the most dangerous class of error because
  every number in it looks plausible; a date, price, or address that
  matches nothing in this file's documents is presumed to be another
  file's until shown otherwise.
- **Order sheet vs report** — AMCs bury real requirements in the
  boilerplate (market-conditions statistics in the report, adjustment
  support commentary, cosmetic-vs-subject-to rules, ANSI). Extract the
  requirement list once and check each item off.
- **Public record vs report** — TPAD for prior sales (with the
  qualification codes — a "family sale" changes the whole story of a
  price jump), parcel layer for owner (OWNER2 of one space means NO
  co-owner; the trailing "&" is a rendering artifact), FEMA for the
  flood block.
- **The report against itself and its own exhibits** — the largest
  section of the catalog, and where CU lives.

## Step 4 — Judgment gets deference; support gets checked

Two standing rules from his corrections, both load-bearing:

- **The form carries the final calculations.** Concluded figures may
  differ from workfile screens. Flag a workfile-vs-report difference
  only when it is a factual conflict, or when the report claims support
  of a magnitude the cited source does not provide.
- **Never flag a time adjustment for its shape.** Non-monotonic,
  negative, or a small one on an old comp — all can be right. Find the
  monthly table (TrueTracts prints one keyed to the comparable's
  CONTRACT month), multiply it out against each comp, and stop. The
  only valid concern is "no documented derivation," never "these don't
  scale with age."

When his number and a fresh analysis disagree but both are defensible,
present the conflict and the evidence; the call is his. When his own
exhibit contradicts his own checkbox, that is not a judgment call — flag
it as the top of the list, because a reviewer only has to turn the page.

## Step 5 — Delta reviews: hunt regressions, not just fixes

On a second or later draft, diff against the previous draft AND the
previous review document:

1. Walk the old flag list — fixed, partly fixed, untouched. "Partly"
   matters: a date corrected in the narrative but not in the field
   beside it is still a finding.
2. **Re-verify what was previously RIGHT.** Editing one section knocks
   over its neighbors: fixing a contract narrative has wiped a
   disclosed concession to "$0"; fixing a phantom garage has deleted a
   real driveway. Anything adjacent to an edited field gets re-checked
   even though it passed last time.
3. New content gets a full first-pass review (a newly developed cost
   approach, new exhibits, new addenda).

## Step 6 — Write the review document

Into the job folder, named `Draft N Review - <address>.txt` (or
`Final Review - ...`). Structure, always in this order:

1. **BLOCKERS / MUST FIX** — factual conflicts with signed documents,
   UAD contradictions the GSE machine reads, the report contradicting
   its own exhibits. Each finding: what the report says, what the
   source says, where both live. When the fix is a sentence, include it
   paste-ready — ONE line, no wraps (his TOTAL paste rule), voice rules
   applied.
2. **CLIENT REQUIREMENTS NOT MET** — cite the order sheet's own words.
3. **REQUIRED FIELDS STILL EMPTY** — listed so nothing ships blank;
   expected blanks on a draft (value, signature date) noted as such.
4. **HOUSEKEEPING** — typos, garbled sentences, stray fragments,
   removable pages. Dictation artifacts read for sense, not spelling.
5. **VERIFIED CLEAN** — what was checked and passed, so he does not
   re-check it. This section earns the flags their credibility.

Never write the word "average" into any paste-ready block, and check
every draft narrative sentence against the bias-language rule (no
feel-words; factual and countable only).

## Step 7 — Report back in chat

Flags FIRST, always — he wants problems on the front end, every time.
Order by bite, not by page number. Own any correction to your own prior
finding plainly and early. Close with the shortest path to
sign-and-deliver: which three fixes matter most if he does nothing else.

If a finding of yours is later shown wrong by a better source, the
retraction goes at the TOP of the next report-back, not buried.
