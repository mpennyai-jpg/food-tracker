# Run order — sequencing six skills off one address

Method only. No assignment data.

---

## The trap, first, because it is the expensive one

`workup` step 4 dispatches `neighborhood-description`,
`exposure-marketing-time` and `highest-and-best-use` itself. That is correct when
the workup runs alone. In a bundled run it double-dispatches.

**In a bundled run, `report-prep` owns the dispatch.**

```
report-prep discovery
        │
        ├─ workup steps 2-3 ──► worked CSV + regression + comp candidates
        │                             │
        │                             ▼
        ├─ neighborhood-description ──┤
        ├─ highest-and-best-use ──────┤  all five read the SAME worked CSV
        ├─ exposure-marketing-time ───┤  and the SAME discovery result
        ├─ site-improvements ─────────┤
        └─ overall-quality-condition ─┘
                                      │
                                      ▼
                          workup step 5 ──► WORKUP.html / .pdf
```

Run the workup through step 3, take the worked CSV and the analysis, drive all
five narratives from here, then return for step 5. Skip step 4's dispatch — but
**keep its cross-check column**, which is reproduced in SKILL.md step 4.

If you let both layers dispatch, three narratives run twice, land in the same job
folder, and can carry two different sets of numbers. Nothing about the second set
looks wrong. That is house-rules section 9's whole warning.

---

## Tiers

### Tier A — runs on discovery alone. Start immediately.

| Skill | Needs | Note |
|---|---|---|
| `sales-contract-analysis` | the contract PDF; owner of record from the parcel layer | Purchases only. Run FIRST — counter offers supersede the original, and the price, binding date and concessions it settles are inputs to everything after it. Rasterize; the text layer is never trusted |
| `neighborhood-description` | address, effective date | Read `references/fair-housing-language.md` **before writing a single sentence of narrative.** Hardest constraint in that skill |
| `highest-and-best-use` | address, effective date, zoning, lot dimensions, improvements, opinion of value | Escalate only on a trigger — acreage well above minimum, a second potential lot, mixed or commercial-adjacent district, an easement, a non-conforming improvement, a proposed use, a lender question about site size |

Do not hold Tier A waiting for the MLS export. Both improve with it; neither
stops without it. Neighborhood loses its price and age ranges and its market
conditions box — say so in the document rather than leaving it implied.

### Tier B — needs the closed export.

1. `workup` step 2 — build the worked CSV.

   ```
   python scripts/prep.py --csv "<export>.csv" --out "<subject> - MLS worked.csv" \
       --lat <lat> --lon <lon> --origin <YYYY-MM-DD> --effective <YYYY-MM-DD>
   ```

   Coordinates come from the tracker `pub.geo` block. Do not geocode again.

2. **Spot-check `CondWhy` and fix what is wrong before anything downstream reads
   it.** Condition classing is a keyword read and it will misfire. Review every
   row flagged `review`, every distressed sale headed for the comp set, and any
   listing whose class disagrees with its price per square foot. Re-run after
   edits. Class counts moving between passes is normal.

3. `workup` step 3 — the analysis. `scripts/ols.py` does regression in
   stdlib; Penny has no pandas, numpy, statsmodels or sklearn.

4. `exposure-marketing-time`. Needs the opinion of value as well — SR 1-2(c) ties
   the exposure conclusion to it.

`ListToContractDays` is the measurement basis. `DaysOnMarket` is not — it resets
on withdraw-and-relist and understates real exposure. Carry both, report both
medians, and state the disagreement count for **this** export. `prep.py` counts it.

### Tier C — needs his inspection input. Waiting here is expected.

| Skill | Runs when |
|---|---|
| `site-improvements` | Photos in the job folder are enough to start the inventory. Walk the set deliberately — front, rear, street, site shots — and note condition evidence as you go: cracked or patched pavement, leaning fence sections, overgrowth, a sagging shed roof. Those observations set percent-good and each must trace to a photo. Flag every item you cannot measure |
| `overall-quality-condition` | Only on his observations. There is no partial version — no observations, no ratings |

Do not stall the whole run on Tier C. Deliver Tiers A and B, name what Tier C is
waiting on, and pick it up when he answers.

### Last

`workup` step 5 — the WORKUP document. It summarizes conclusions the
other five produce, so it goes after them. `references/document-shape.md` has the
section order, voice, mandatory caveat blocks, and the build command.

---

## Background running

He is typing the report while this runs. That is the point.

- Post the gap report **in the foreground, first**, always. A gap he learns about
  four minutes later is a gap that already cost him.
- Tier A and Tier B parallelize cleanly — they share the discovery result and the
  worked CSV and write to different files.
- **Nothing survives the session.** He does not need it to; he keeps the terminal
  open and checks back. Do not build cron or cloud scheduling for this.
- When background work finishes, report file paths and open gaps, not narrative.
  He will read the files.

## Isolation, in a multi-skill run

The isolation rule gets harder the more skills run at once. Before writing any
output file, scan the draft for street addresses, dollar figures, square
footages, lot dimensions, acreages, zoning codes and dimensional standards, day
counts and date ranges and sale counts, subdivision and city and county names,
and percentages. Each one traces to: what he supplied for **this** assignment,
a file in **this** job folder, a lookup run **now** for **this** address, or the
export he provided for **this** assignment.

**If it cannot be traced, delete it.** Do not reason about whether it is probably
right.

Bracketed placeholders in any skill's reference files are not values. A surviving
`[ADDRESS]` or `[SITE VALUE]` means the document is not finished.
