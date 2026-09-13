# The document — shape, voice, and how it gets built

One HTML file, printed to PDF. **This file is the whole job.** Everything that
gets written for the assignment goes in it — the report information, the analysis,
and the full workfile analysis behind every narrative. He should never have to
open a second document to answer a question about this property. The individual
.txt files still get written (they are the workfile of record, and he pastes
narrative from them because copying out of a PDF hard-wraps every line), but the
HTML carries a complete copy of all of it.

**It is a screen document first and a PDF second.** He reads it on a 34-inch
monitor while typing the report. It is built by `scripts/build_workup.py`, which
wraps the body in a reading shell: a sticky sidebar table of contents with
scroll-spy, collapsible sections, a filter box, and an A−/A+ text-size control
that remembers his setting. Print CSS puts it back into the 10.5pt letterhead
document, all sections forced open, so the PDF is unchanged.

Three parts, in this order: **the report information first** — everything he
types or pastes from — then the analysis behind it, then the workfile analysis in
full. He works Part 1 while typing the report; Part 2 is the support he reads
when a number needs defending; Part 3 is where he goes when a number gets
challenged. Drop any section the assignment does not have, and say in the gap
report why it is absent.

### Part 1 — The report information (every assignment)

Open with a `.part` divider line reading "Part 1 — The report information".

| # | Section | Contents |
|---|---|---|
| 1 | Assignment | order and client facts, product, dates, fee, contract price, transaction type |
| 2 | Contract items to address | purchases only: concessions, non-conveying items, buyer-side fees, financing box, seller vs owner of record, prior transfer |
| 3 | Subject — public record | parcel, owner, year built, assessor area, values, city-limits code, utilities, flood, census tract |
| 4 | Report narratives — form-ready | the FULL report text from the narrative skills, not a summary: neighborhood form entries (checkboxes, price/age ranges, land use %), boundaries, neighborhood description, market conditions comment, H&BU narrative, exposure time, marketing time, and the as-is site-improvements number with its open questions |
| 5 | Items to resolve before delivery | the checklist he works from |

The narratives section opens with a callout: **paste from the .txt files, not
from this PDF** — copying out of a PDF hard-wraps every printed line and TOTAL
keeps the breaks. Name the REPORT .txt files in the job folder; this section is
the reading copy, and each narrative's WORKFILE pair holds the full analysis.

### Part 2 — The analysis behind it

Open with a `.part` divider line reading "Part 2 — The analysis behind it".

| # | Section | Contents |
|---|---|---|
| 6 | Data set | export counts, date span, the segment, how distance was measured |
| 7 | Market conditions | the time-adjustment test and its verdict |
| 8 | Regression models | the sequence, with standard errors and t-statistics |
| 9 | Paired sales | pair count, median and mean difference |
| 10 | Recommended adjustment screens | GLA, baths, garage, site, age, condition, central heat/air, time — one row each, with confidence |
| 11 | Comp candidates | ranked table, the same-subdivision peer set, active competition |
| 12 | Value indications | method A, method B, reconciled range |
| — | Sources and limitations | every source with its date; the limitations block |

### Part 3 — The workfile analysis

Open with a `.part` divider line reading "Part 3 — The workfile analysis behind
each narrative".

**Every workfile .txt written for this assignment gets folded in here, in full**,
one `<h2>` section each — not summarized, not excerpted. That includes the four
standing ones (neighborhood, H&BU, exposure/marketing time, site improvements)
and every ad-hoc one the assignment generated: a dock adjustment, a land-sales
site value, a location/view test, a comp note, a bedroom-count comment. The
builder does the conversion — pass each file as
`--workfile "Section heading::/path/FILE.txt"` and it detects the headings,
preserves the column alignment, and adds each one to the sidebar with its
subheads.

Order them: the four standing narratives first, in Part 1 section 4 order, then
the assignment-specific analyses, then the short comp and report comments.

Do **not** fold in the `- REPORT narrative.txt` files. Their text already sits in
Part 1 section 4. Folding them in twice puts two copies of the same paragraph in
one document, and they drift.

**Rebuild the HTML whenever a narrative .txt changes.** A section 4 written on
the 2nd against a narrative revised on the 11th is the exact problem this
document exists to kill.

### Added only on a renovation / 203(k) / subject-to assignment — rare

| Section | Contents |
|---|---|
| Comp candidates — as-completed | the finished-condition set, plus the blueprint sale |
| Renovation scope and feasibility | bids, what they exclude, headroom against the as-completed range |

Nothing else changes. Do not restructure the core document around the renovation,
and do not open with it.

## Plain-terms blocks — required on every statistic

He is not a statistician and has said so. He knows closer to 1 is better on R²
and that is the right instinct; everything else has to be said in words. Use the
`.plain` block — it renders as a green-edged box headed "In plain terms".

Two are mandatory:

1. **A reading legend, once, at the top of the regression section.** What adj R²
   is, on a 0–1.00 scale, with the honest range for this property type and why a
   0.95 would mean overfitting rather than success. What t is, that it is
   unrelated to the size of the dollar figure, and the four-band scale the house
   rules already enforce: under 1.5 not support · 1.5–2.0 a hint · 2.0–3.0 solid ·
   over 3.0 strong.
2. **A reading of the model table, right under it.** Not what the numbers are —
   he can see them — but what the sequence *argues*: which term to use, which
   ones failed, and that a failed term is a finding, not a hole.

Then one after any other statistic that drives a decision: a paired-sales median,
a months-of-supply figure, a regression inside a Part 3 workfile. Name the number,
say what it means for this assignment, say how much weight it carries. If a figure
does not deserve a plain-terms sentence, it probably does not belong in the
document.

## Callout blocks — use them, they are what he reads first

Set these as boxed callouts, not body text:

- **The screening banner at the top.** Every figure is a screen; condition classes
  were machine-assigned and some will be wrong; his verified comps carry the
  report; nothing here is an appraisal or an opinion of value.
- **A disagreement between two sources** — assessor area against his room list,
  DOM against list-to-contract, medians against the regression.
- **The convergence finding**, when three methods agree.
- **A blueprint comp** — renovation assignments only, when one sale is the same
  finished product nearby.
- **A trap**, such as not stacking bedrooms on GLA.
- **Anything that will trigger a revision request** — missing photos, an
  unaddressed concession, an assignment-condition question for the client.

## Voice

House rules section 1 applies: ninth-grade reading level, short sentences, active
voice, first person, no sentence starting with "The", no adjective without a
number behind it.

Two additions for this document:

- **Write to the appraiser, not to a file.** "Check your GLA against the
  assessor" beats "a discrepancy was noted."
- **Say what a number means, immediately after it.** A coefficient with no
  sentence after it is a number he has to interpret while driving.

## Building it

Write the **body fragment only** — `<div class="part">` dividers, `<h2>`, `<h3>`,
tables, `.callout`, `.plain`. No `<html>`, no `<head>`, no CSS, no letterhead, no
table of contents. Then run the builder, which adds all of that and generates the
sidebar from your headings:

```
python3 ~/.claude/skills/workup/scripts/build_workup.py \
  --out "<job folder>/<subject> - WORKUP.html" \
  --body body.html \
  --heading "Pre-Report Workup — <full address>" \
  --sub "<market · county · effective date · prepared date>" \
  --title "<subject> — Workup" --addr "<full address>" \
  --logo "C:/Users/toddp/OneDrive/Appraisal Tracker/pinewood-logo.png" \
  --workfile "Neighborhood — workfile analysis::<path>/NEIGHBORHOOD - WORKFILE analysis.txt" \
  --workfile "..."
```

Never hand-write the nav — it goes stale the first time a heading is renamed.
Never paste the 268 KB logo data URI onto the command line; pass `--logo` and let
the builder embed it.

Then print it:

```
"C:\Program Files\Google\Chrome\Application\chrome.exe" --headless --disable-gpu \
  --no-pdf-header-footer --print-to-pdf="<subject> - WORKUP.pdf" "file:///<path>.html"
```

Then confirm the PDF exists and has a sane page count. A zero-byte or one-page
PDF means the print failed — do not report it as written.

## Letterhead and print CSS

All of this is already in the builder — it is recorded here so the spec survives
if the script is ever rewritten. Do not restate it in the body fragment.

Match his real letterhead — the spec came from his own letter, so do not guess:

- Logo centred, about 74 px tall in print. Use `Appraisal Tracker\pinewood-logo.png`
  (already trimmed and white-backed), embedded as a base64 data URI so the file
  works from `file://`.
- Two left-aligned contact lines, pipe-separated:
  `Todd A. Paris | P.O. Box 330326 | Murfreesboro, TN 37133-0326`
  `Phone: (615) 956-2099 | Email: PinewoodAppraisal@gmail.com`
- No horizontal rule under the letterhead.
- Headings in `#0F4761`, sans-serif, no underline. Part dividers as a
  `.part` class: same blue, ~13 pt bold, 2 pt bottom border. `h3` for the
  narrative subheads, ~10.8 pt in the same blue.
- Body sans-serif, ragged right. Around 10.5–11 pt with tight line height —
  this document is dense and he prints it.
- `@page { margin: 0.5in }`, tables with `border-collapse` and hairline rules,
  `page-break-inside: avoid` on every table and callout.
- Repeat table headers across page breaks: `thead { display: table-header-group }`.

**Check the printed PDF, not the HTML.** Wide tables that look fine in a browser
split badly in print, and a table that breaks across a page with no header is
unreadable in the field.
