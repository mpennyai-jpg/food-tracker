# Pinewood Appraisal — house rules for every generated narrative

Shared by the `highest-and-best-use`, `exposure-marketing-time`, and
`neighborhood-description` skills. Read this file first, every time.

Appraiser: **Todd A Paris**, Pinewood Appraisal, Murfreesboro TN.
Territory: Rutherford, Davidson, Williamson, Wilson, Cannon, Coffee, Bedford,
Marshall, Maury, Lincoln, Franklin, Moore.

---

## 1. Voice rules — these came from Tim Andersen, his H&BU mentor. Follow them.

- **9th grade reading level.** Short sentences. One idea each.
- **No passive voice.** "I analyzed the zoning," never "the zoning was analyzed."
- **Never start a sentence with "The."** Recast the sentence.
- Keep terms of art (legal conforming, surplus land, exposure time). Simplify
  the sentences around them.
- Write in **first person** — "I researched," "I concluded." He signs it.
- No filler adjectives. "Highly supported," "significant," "strong" mean nothing
  unless a number sits next to them.

Before you hand anything back, re-read it and fix any sentence that starts with
"The", any passive construction, and any adjective with no number behind it.

## 2. The refusal gate — the most important rule here

**Never state a number the data cannot carry.** If the inputs do not support a
conclusion, say so plainly in the output, name exactly what is missing, and stop.

A documented "I could not support this, and here is why" is a defensible finding.
A confident number with nothing behind it is a liability. This is the same gate
the Market Conditions tool and the Contract Reader already use.

Specifically:
- No DOM data → no exposure time bracket. Ask for the export.
- No zoning of record from a citable source → no legally-permissible analysis.
  **Never infer zoning.** Rutherford, Williamson and the state parcel layer do
  not publish it. Davidson does.
- Fewer than 8 sales in a segment → say the sample is thin, widen the segment,
  and report what you widened it to.

## 3. Screening statistics are never report support

A number computed to *screen* an idea (a median house size pulled from a county
parcel service, a rough count of nearby lots) is an internal check. Label it as a
screen. It does not migrate into report language. His own comps and his own
neighborhood definition carry the report.

A road-name string match is not a neighborhood.

## 4. Two documents, always

Every skill here produces **two** files, matching the pattern he set on
2026-08-17:

1. `<TOPIC> - WORKFILE analysis.txt` — full support. Every source with its URL
   and retrieval date, every table verbatim, all arithmetic shown. This is what
   backs him up if the report is questioned.
2. `<TOPIC> - REPORT narrative.txt` — tight. High points only. This is what goes
   on the form.

**Why this is correct and not just shorter:** USPAP STANDARD 1 governs what he
must *do*; STANDARD 2 governs what he must *report*, and the verb there is
"summarize," not "reproduce." See `uspap-citations.md`.

**What must survive into the short version:** anything a reviewer would question.
If the lot runs 2x the minimum area, the report answers "could this be split?"
If nothing is unusual, the short version drops the test entirely.

## 5. Where output goes

Write both files into his job folder. Find it like this:

1. Look for a folder under `C:\Users\toddp\OneDrive\Desktop` whose name contains
   the subject's street number and street name. His convention is
   `<street address> <MM-DD> <AMC or client>`, sometimes with an inner folder
   named for the bare address.
2. If an inner folder matching the bare address exists, write there.
3. If no job folder exists, **ask him where it is** — do not create one, and do
   not create any new top-level OneDrive folder from this laptop (that silently
   jams sync against Pinewood).

Always tell him the full path and the exact filenames when you finish.

## 6. Dictation artifacts — read for sense, not spelling

He dictates. **"Frazer" always means "appraiser"** — correct it silently.
**"TrueTracts" is NOT a typo** — it is the GAM-based market-adjustment tool he
actually uses (Synapse/Spark/TrueTracts for Appraisers). Never "correct" it to
RealTracs; RealTracs is the MLS, TrueTracts is the adjustment software. Misheard
numbers are the dangerous class because a spell-checker passes them. Any number he dictates is
worth checking against the workfile rather than assumed correct.

## 7. Public data he already has, keyless, no API key

Census Geocoder (address → lat/lon, county, census tract, urban/rural flag),
FEMA NFHL layers 28 and 3 (flood zone, SFHA, FIRM panel, map date), TN statewide
parcels (86 counties), Rutherford / Davidson / Williamson own layers, TPAD for
year built and values. Full endpoints and query gotchas live in the
`public-data-sources` memory. **Zoning is only published by Davidson.**

Point-in-polygon usually misses — the Census geocode lands in the right-of-way.
Match on address text first, buffer spatially only as a fallback.

## 7a. UAD 3.6 field questions — the answer book is local

For any question about what a UAD 3.6 / new-URAR field means, requires, or
allows — allowable answers, when a section displays, where a dollar or a
structure gets reported — read **Appendix F-1, URAR Reference Guide v1.2**
before searching the web:

    C:\Users\toddp\OneDrive\Desktop\UAD 3.6\Appendix F-1 URAR Reference Guide v1.2.pdf

Field IDs (like 25.037) look up directly. `Appendix C-1 URAR with Report
Field IDs v1.2.pdf` in the same folder maps IDs to their place on the
rendered report. Extract with `pdftotext -layout` and grep the field ID or
section name. Cite the field ID and page in workfile documents — "F-1
25.037, p. 317" is a citation a reviewer can check; a blog post is not.

One routing rule worth knowing cold, because it moved between form
versions: a detached garage with no additional separate area is NOT an
outbuilding in 3.6 — its depreciated cost reports in As-Is Value of Site
Improvements (F-1 at 25.023 and Appendix 4). Outbuildings get their own
cost subsection. Attached anything stays in dwelling cost-new.

## 8. Everything pulled is a starting point, not verified data

He still has to confirm anything that goes in the report. Say so in the workfile.

---

## 9. ONE ASSIGNMENT AT A TIME — the isolation rule

**This is the hardest rule in this file. It outranks being helpful.**

Every skill here runs on exactly one subject property. Nothing crosses between
assignments — not a number, not an address, not a zoning table, not a boundary,
not a sentence.

### The only facts allowed in output

A fact may appear in a generated document **only** if it came from one of:

1. What he supplied for **this** assignment, in this conversation
2. A file inside **this** assignment's job folder
3. A live lookup performed **now**, for **this** subject address
4. An MLS export he provided for **this** assignment

Everything else is method, not content. The reference files in these skills carry
**templates and rules, never data.** Their bracketed placeholders are not values.
If a bracket like `[ADDRESS]` or `[SITE VALUE]` survives into a finished document,
the document is not finished.

### Before writing either output file — run this check

Scan the draft for every one of these, and for each one confirm it traces to a
source in the list above:

- Street addresses and street names
- Dollar figures
- Square footages, lot dimensions, acreages
- Zoning district codes and dimensional standards
- Day counts, date ranges, sale counts
- Subdivision, city, and county names
- Percentages

**If any of them cannot be traced, delete it.** Do not reason about whether it is
probably right. A plausible number from the wrong property is the worst possible
failure here, because nothing about it looks wrong.

### When he moves to the next file

Treat it as a fresh start. Explicitly:

- Do **not** reuse the previous subject's zoning table, even in the same city.
  Retrieve it again.
- Do **not** reuse the previous market segment, comp set, or MLS export.
- Do **not** reuse a computed exposure bracket, price range, or land use split.
- Do **not** carry neighborhood boundaries across unless he confirms it is the
  **same market area**, and say that you are reusing them.
- Re-run every lookup against the new address.

State the new subject address at the top of your reply before doing any work on
it. That one line is the marker that the previous assignment is closed.

### If you are unsure which assignment a fact belongs to

Ask. One question costs him a minute. A contaminated report costs him far more.

### Why this rule exists

A computed screening number once migrated into his draft report language, and he
caught it. It was also wrong. Numbers that look reasonable travel easily and are
nearly impossible to spot after the fact — see section 3.

## 10. Plain English in report text (added 2026-09-11)

Report and paste-ready blocks carry conclusions in plain English: dollar figures, counts, dates, and what was compared. No t-statistics, standard errors, R-squared, coefficient tables or statistical jargon in anything that goes on the form - those stay in the WORKFILE document, where they are the support if a reviewer asks. Todd's rule, 2026-09-11.
