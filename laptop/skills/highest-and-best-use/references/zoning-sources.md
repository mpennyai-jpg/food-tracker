# Getting zoning of record — and the rule about never guessing

**Zoning drives the entire legally-permissible test. A guessed district poisons
the whole analysis.** If you cannot cite it, ask him for it.

## What is published, and what is not

| Source | Zoning? |
|---|---|
| Davidson County / Metro Nashville parcel layer | **Yes** — `Zoning` field, plus `LUDesc` and a full legal description |
| Rutherford County parcel layer | No |
| Williamson County parcel layer | No |
| Tennessee statewide parcel layer (86 counties) | No |
| TPAD (assessment.cot.tn.gov) | No zoning; has year built, values, class, City # |

Endpoints for all of these are in the `public-data-sources` memory.

So for everything outside Davidson, zoning comes from the municipality's code or
from him.

## Municipal codes — MTAS

Most Tennessee municipal codes are published in full by the University of
Tennessee's Municipal Technical Advisory Service:

```
https://www.mtas.tennessee.edu/system/files/codes/combined/<City>-code.pdf
```

Validated against a Tennessee municipal code of 600-plus pages. Try the city name with initial
capital and no spaces; check the MTAS codes index if the direct URL misses.

Download it and read the zoning title — usually Title 14, Zoning and Land Use
Control.

### The extraction trap — this one produced wrong numbers

`pdftotext -layout` **scrambles the dimensional tables and offsets the values by
one row.** A district's minimum lot area comes out reading as the row above or
below it. The output looks perfectly plausible.

**Use `-table` instead, and re-read the passage before quoting any number:**

```bash
pdftotext -table -f <first> -l <last> "<City>-code.pdf" out.txt
```

Then find the district heading in the text and confirm each figure sits under the
right label. Quote nothing you have not read in position.

## What to capture, verbatim

For the district that applies:

- Code section number and district name
- Uses permitted **by right**
- Uses permitted by **special exception or conditional use**
- Minimum lot area
- Minimum area per family (this differs from lot area in many districts)
- Minimum lot width at the building setback line
- Front yard setback — including any street-average rule and any maximum
- Side yard setback
- Rear yard setback
- Maximum lot coverage
- Maximum height, principal and accessory

Record the retrieval URL and the retrieval date beside the table. A reviewer must
be able to pull the same page. Nothing from a prior assignment carries forward — every district table is retrieved fresh for the subject actually being appraised.

## The local library FIRST — counties AND cities

`C:\Users\toddp\.claude\appraisal\zoning\` holds downloaded county zoning
ordinances for unincorporated **Bedford, Cannon, Franklin, Lincoln, Rutherford,
and Williamson**, plus Metro Nashville's land-use table. `zoning\cities\` holds
the city ordinances for **Shelbyville, Murfreesboro, Smyrna, La Vergne,
Tullahoma, Manchester, and Nolensville** (Brentwood and Franklin city are
online-only; Woodbury's is a pointer — see the README). Its `README.md` carries
each file's version, retrieval date, and source URL.

**Jurisdiction first, always.** The city-limits answer comes from the tracker's
public-records block (Census place + TPAD city code). Inside city limits the
city ordinance governs — city overlays, historic districts, and design
standards do not exist in the county document, so citing the county PDF for an
in-city subject is a wrong answer that looks right. Read the local PDF instead
of hunting the county site — but they are snapshots: when a finding is
load-bearing, verify currency at the README's source URL. **Moore County is not
in the library** — Metro Lynchburg–Moore has a zoning ordinance but publishes
nothing online; it comes from Todd or the Metro offices. The `-table` extraction
rule above applies to these county PDFs the same as to MTAS codes.

For a county outside the library, the zoning resolution is usually a PDF on the
county planning department's site, but there is no reliable pattern for the URL
and no service to query.

**Do not infer the district from surrounding land use, lot size, or the parcel
layer's land-use description.** Ask him. He knows, or he can call the planning
office, and that call is faster than a wrong answer.

## Unzoned property

Some Tennessee counties have unzoned areas. That is a real finding, not a gap —
write "no zoning" as the compliance answer and note that no district regulates
the site. Then the physically-possible and financially-feasible tests carry more
weight, and say so.

## Overlays and private restrictions

Check for a historic overlay, a floodplain overlay, and subdivision covenants.
Covenants can be more restrictive than the district and are not in any public
service — they come from the recorded plat or the deed. If the assignment turns
on one, tell him to pull it.
