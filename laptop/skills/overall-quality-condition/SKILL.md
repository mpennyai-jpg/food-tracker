---
name: overall-quality-condition
description: Reconcile the UAD 3.6 Overall Quality and Condition section for a Pinewood Appraisal assignment — take Todd's room-level observations, exterior/interior ratings, update statuses, and defects, check them for the consistency the GSE machine enforces, and produce the overall Q and C ratings with short supporting commentary. Use when Todd is working a UAD 3.6 / URAR report and asks about overall quality, overall condition, C-ratings, Q-ratings, condition reconciliation, update status, or whether his ratings are consistent. Triggers on "overall quality and condition", "condition reconciliation", "C rating", "Q rating", "update status", "as-is condition rating".
---

# Overall Quality and Condition — UAD 3.6 reconciliation

Read `C:\Users\toddp\.claude\appraisal\house-rules.md` first. Section 9 (one
assignment at a time) applies in full. Every rating below comes from what HE
observed on THIS inspection — never from a prior report, never assumed.

## What this section is

In UAD 3.6 the Overall Quality and Condition section is a **reconciliation of
every dwelling and living unit on the property** — main dwelling, ADU, any
outbuilding with living area. It is not a restatement of the main house alone.

The pieces that feed it, and that must already exist in the report:

- **Exterior condition rating** (Dwelling Exterior)
- **Interior condition rating** (Unit Interior — one per unit)
- **Per-kitchen and per-bathroom**: update status (Fully / Partially / Not
  updated), time frame, and condition status
- Overall update status for bathrooms and for flooring
- **Defects, Damages, and Deficiencies tables** (six possible locations: Site,
  Dwelling Exterior, Unit Interior, Outbuilding, Vehicle Storage, Amenities)
- The **as-is overall condition rating** when the appraisal is subject-to

The machine cross-checks all of it. This skill's job is to catch the
inconsistency before the UCDP does.

**Field authority:** when any check turns on what a field means, requires,
or allows — an allowable answer, a display condition, which section a
rating belongs to — read the local copy of **Appendix F-1, URAR Reference
Guide v1.2** (`C:\Users\toddp\OneDrive\Desktop\UAD 3.6\`) and cite the
field ID and page. House-rules section 7a has the extraction mechanics.
Do not settle a field-definition dispute from memory or a blog post when
the answer book is on the desk.

## Step 1 — Collect what he has

Ask for, in ONE message, whatever is missing:

- Exterior rating and interior rating he intends
- Kitchen/bath update statuses and time frames, per room
- The defects list with each row's Recommended Action
- Whether the assignment is as-is or subject-to
- Any ADU or living-area outbuilding, with its own interior rating
- Year built, and whether it is new construction

## Step 2 — Run the consistency checks. Every one, every time.

These are the documented GSE bounce patterns plus the rating definitions:

1. **Defect with action "None" forces the rating.** A deficiency affecting
   livability left as-is IS the condition. Missing floor coverings as-is = C5
   by definition — not C4 with a note. If he wants C4, the report must be
   subject-to the repair, and the action row must say Repair or Completion.
   This is about the C-RATING. It does not touch the 1004 page-1
   "physical deficiencies affecting livability, soundness or structural
   integrity" box, which Todd answers Yes only for major conditions (no
   windows, a hole in the roof) - deferred maintenance and subject-to items
   sit under a No (his rule, 2026-09-10).
2. **Soundness answers drive C5/C6 territory.** Any defect marked "affects
   soundness or structural integrity = Yes" cannot sit under a C3 overall.
3. **New construction = Fully Updated, C1.** Flipped from UAD 2.6's "Not
   Updated." If it meets the definition of new construction, update statuses
   read Fully Updated and overall condition is C1.
4. **Kitchens/baths against the interior rating.** "Not updated" kitchens and
   baths in a 1940 house cap how good the interior can plausibly be; a C2
   interior with every room "Not Updated / original" will read as inconsistent.
   Conversely a "Fully Updated 2023" kitchen supports — and needs — a rating
   that reflects it.
5. **Exterior vs interior vs overall.** Overall is a reconciliation, not an
   average and not a copy of the better one. State which side governs and why.
   When exterior and interior differ by 2+ ratings, the commentary must carry
   the reason.
6. **Subject-to needs the as-is rating too.** If any recommended action is
   Completion, Inspection, or Repair: the final value condition is subject-to,
   AND the as-is overall condition rating field is required, AND the two
   ratings must differ in the direction the repairs explain.
7. **Multiple units reconcile, not the best one.** ADU in C4 condition under a
   C3 main dwelling: overall reflects both, and commentary says how.
8. **Q-rating is construction quality, not condition** — it does not move with
   updates. A remodeled Q4 house is still Q4. Flag any draft where quality
   changed from a prior known state without a structural reason.
9. **Commentary must match the fields.** No "average condition" prose over a
   C5, no "well maintained" over an open defects table.

## Step 3 — Produce the output

Give him, in this order:

1. **The ratings**: exterior, interior (per unit), overall quality, overall
   condition — and the as-is rating if subject-to.
2. **Any check that failed**, stated plainly with the fix options (change the
   rating, change the action, or make it subject-to). Never silently pick one —
   the rating decision is his.
3. **Commentary**, 40–90 words, his voice (house-rules: first person, active,
   short sentences, no sentence starting with "The", no adjective without a
   fact behind it). Shape:

   > I rated the dwelling [C_] overall. Exterior stands at [C_] on [FACT].
   > Interior stands at [C_] — [kitchen/bath update facts]. [Which side
   > governs and why]. [Defect + action statement if any]. [ADU/outbuilding
   > reconciliation sentence if any].

4. **A workfile note** — the observations behind each rating, so the ratings
   trace to the inspection. Append-ready plain text.

## Refusal gate

No inspection observations = no ratings. If he has not told you what he saw,
ask — do not derive condition from listing photos, public records, or a prior
report. MLS photos of comparables support COMPARABLE ratings only, and that
sourcing gets said in the workfile.
