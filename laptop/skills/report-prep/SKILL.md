---
name: report-prep
description: Prep an entire Pinewood Appraisal file from one address — a single discovery pass, one merged gap report naming everything that is missing and what each gap costs, then the full narrative package (neighborhood, highest and best use, exposure and marketing time, site improvements, overall quality and condition) driven off one market analysis so every section carries the same numbers. Use when Todd drops an address because he is starting to type a report and wants the whole package prepped at once, or wants to know in one message what he still has to supply. Triggers on "prep", "prep this file", "start my file", "run the narratives", "run everything on", "drop in an address", "what do you need for", "get this file ready", "I'm starting to type".
---

# Report prep — one address in, the whole package out

Read `C:\Users\toddp\.claude\appraisal\house-rules.md` and
`C:\Users\toddp\.claude\appraisal\uspap-citations.md` first. Every rule there
applies to every document this produces.

**State the subject address on the first line of your reply, before any work.**
House-rules section 9 is the isolation rule and this skill touches more files
than any other one here — a job folder, a tracker record, two MLS exports,
contracts, bids, photos, and six downstream skills. It is therefore the easiest
place in the whole system to mix two properties up. That one address line is the
marker that the previous assignment is closed.

Everything in `references/` is method and merged requirements. It carries no
assignment data. Every bracketed placeholder gets filled from this assignment or
deleted.

---

## What this skill is for

Todd is at his desk with the form open, starting to type. He should not discover
on page four that he never pulled the active/pending export. This skill front-loads
that: one discovery pass, one gap report, then it drives everything that can run.

**What it does NOT do:** it does not rewrite any of the narrative skills. Each
one owns its own method, its own gates, and its own output files. This skill
resolves the address once, asks once, sequences them, and holds them to one set
of numbers.

## The bundle

| Skill | Produces | Hard requirement |
|---|---|---|
| `sales-contract-analysis` | `SALES CONTRACT - summary.txt` + the paste-ready 1004 contract comment | the contract PDF (purchase only); the parcel owner of record |
| `workup` | worked CSV, regressions, paired sales, comp candidates, `WORKUP.html` / `.pdf` | **MLS closed export.** No export, no workup |
| `neighborhood-description` | `NEIGHBORHOOD - WORKFILE analysis.txt` + `- REPORT narrative.txt` | address, effective date |
| `highest-and-best-use` | `HBU - WORKFILE analysis.txt` + `HBU - REPORT narrative.txt` | zoning of record from a citable source |
| `exposure-marketing-time` | `EXPOSURE - MARKETING TIME - WORKFILE analysis.txt` + `- REPORT narrative.txt` | closed export + effective date + opinion of value |
| `site-improvements` | `Site improvements - WORKFILE.txt` | photos or inspection notes; utilities answer |
| `overall-quality-condition` | ratings, commentary, appendable workfile note | his inspection observations |

## Step 1 — Discovery. Once, for all six.

Follow `workup/references/discovery.md` — it is the authority and this
skill does not duplicate it. Run it **one time** and hand the result to everything
downstream. In order: the job folder under `C:\Users\toddp\OneDrive\Desktop`, the
newest tracker auto-backup JSON, then the MLS exports in `OneDrive\Penny Share\`
and the job folder itself.

Three things that matter more here than they do in a single-skill run:

- **The tracker `pub` block feeds four of the six skills.** Parcel, assessor
  values, year built, flood, census tract, coordinates, subdivision. Pull it once.
  Asking Todd for any of it "reads as not having looked" — and asking him six
  times is worse.
- **Write attachments out of the backup rather than asking for them.** The order,
  contract and bids sit base64-embedded in the backup JSON. `discovery.md` has the
  extraction snippet.
- **Do not create a job folder, and never create a new top-level OneDrive folder
  from this laptop.** It jams sync against Pinewood permanently. If no folder
  exists, ask where it is — that is one of the few questions worth asking.

**The backup can be up to six hours behind.** If the record is missing or looks
older than what he describes, say so and work from the job folder. Do not assume
he is wrong.

## Step 2 — The merged gap report. This is the point of the skill.

`references/gap-matrix.md` is the merged table: every input, which of the six
skills need it, where it comes from, and what its absence costs. Work from it.

Post the gap report as your **first substantive reply**, before any analysis, in
the house format:

```
Subject: <address>

Found:
  <file or record> — <path>

Missing, and what it costs:
  - <input> — <the specific section or conclusion that cannot be produced>

Starting now on: <the skills that can already run>
```

Rules for this step, and they are the whole reason the skill exists:

1. **One message. Everything.** Six skills each have a "collect the inputs" step
   that says ask in one message. Six one-message asks is six interruptions. Merge
   them. He must never be asked twice for the same effective date.
2. **Name the cost, not the item.** Not "send the active export" but "without the
   active/pending export there is no marketing time analysis, the 1004 grid
   checkbox becomes a disclosed assumption instead of a finding, and both
   documents have to say so."
3. **Never ask for what you can get yourself.** House-rules section 7 sources are
   keyless. Zoning is the exception, and only Davidson publishes it.
4. **Start on what you have.** A missing contractor bid does not stop the market
   analysis. Only the missing closed export stops everything.
5. **Unreadable counts as missing.** An image-only PDF with no text layer gets
   named, with what it needs — OCR through the tracker helper, or his notes.
6. **Keep it short.** He reads this on a phone between inspections. Do not pad it.

## Step 3 — Run order

`references/run-order.md` carries the sequencing, the tier definitions, and the
one trap that matters. Summary:

- **Tier A — runs on discovery alone.** `sales-contract-analysis` (on every
  purchase — first, because its price, binding date and concessions feed the
  workup and the review), `neighborhood-description`,
  `highest-and-best-use`. Start these immediately; do not hold them for the
  export.
- **Tier B — needs the closed export.** `workup` steps 2 and 3, then
  `exposure-marketing-time`.
- **Tier C — needs his inspection input.** `overall-quality-condition`,
  `site-improvements`. These wait on his answer and that is expected. Run
  `site-improvements` on the photo set if the photos are in the folder even when
  his notes are not, and name the unresolved items.
- **Last** — `workup` step 5, the WORKUP document, because it
  summarizes conclusions the other five produce.

**The trap:** `workup` step 4 dispatches three of these narrative
skills itself. In a bundled run **this skill owns the dispatch** — run the workup
through step 3, take its worked CSV and its analysis, then drive all five
narratives from here, then come back for step 5. Otherwise neighborhood, H&BU and
exposure each run twice and can land on two different sets of numbers in the same
job folder.

## Step 4 — Cross-checks that must hold before you report done

One export, one set of numbers, six documents. Verify these, and say in your
summary that you did:

| Check | Between |
|---|---|
| Price and age ranges come from **this** export | neighborhood ↔ workup |
| Land use split supports the H&BU conclusion | neighborhood ↔ H&BU |
| Exposure bracket matches the segment analysis | exposure ↔ workup |
| Marketing time equals the 1004 Neighborhood grid checkbox | exposure ↔ neighborhood |
| Surplus/excess land finding agrees with the site size used in the adjustment screens | H&BU ↔ workup |
| Site-improvements total tells the same condition story as the ratings and photos | site-improvements ↔ overall-quality-condition |
| Contract price, binding date, concessions and seller identity are the ones the workup and the 1004 contract section carry — one source, the signed pages | sales-contract-analysis ↔ workup ↔ final-read |
| GLA and year built identical everywhere they appear | all six |
| Detached garage with no separate area counted **once**, in site improvements | site-improvements ↔ workup cost approach |

That last one is F-1 25.023 and Appendix 4 — it moved between form versions and
it is a live double-count risk. House-rules section 7a.

**If two documents disagree, the workup is wrong. Fix it. Do not paper over it.**

## The gates — refuse rather than guess

House-rules section 2 applied to a bundled run:

1. **No closed export → no workup and no exposure time.** Tier A still runs. Say
   plainly which sections stopped and why.
2. **No active/pending export → marketing time is not a finding.** State it equals
   exposure time as a disclosed assumption, in the workfile and in the report
   narrative. Never quietly reuse the exposure number.
3. **Never infer zoning.** Retrieve it from a citable source or say the
   legally-permissible test cannot be completed. This is the refusal in the H&BU
   skill that matters most.
4. **Never derive condition from listing photos, public records, or a prior
   report.** Condition of the subject is his observation only. MLS photos of
   comparables support comparable ratings only, and that sourcing gets written down.
5. **No photos and no notes → no site-improvements inventory.** A number built on
   an imagined driveway is a liability. A partial inventory with named gaps beats
   a confident total.
6. **When GLA is unresolved, run every indication across a range.** Do not pick
   one. Name which source disagrees with which, and by how much.
7. **Screening numbers never become report language.** Label the screen.
8. **A coefficient under t = 1.5 is not a screen.** Print standard errors and
   t-statistics next to every coefficient quoted.

## Finish

Tell him:

- Every file written, with full paths and exact filenames.
- Which gaps are still open, and which section each one is still blocking.
- The three or four things that most affect the value conclusion.
- Any cross-check that failed, and what you did about it.

Keep that summary shorter than any document in it.
