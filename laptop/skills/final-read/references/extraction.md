# Getting at the documents — commands and the traps that produced wrong findings

Everything here was learned on real reviews. The machine-specific tool
locations live in the `reading-pdfs-on-this-pc` memory — check it if a
path below has moved.

## The draft report PDF (TOTAL / wPDF output)

Text first, then pictures for anything the text cannot carry:

```
& 'C:\Program Files\Git\mingw64\bin\pdftotext.exe' "<draft.pdf>" out.txt
```

Page count and info:

```
$bin='C:\Users\toddp\AppData\Local\Microsoft\WinGet\Packages\oschwartz10612.Poppler_Microsoft.Winget.Source_8wekyb3d8bbwe\poppler-25.07.0\Library\bin'
& "$bin\pdfinfo.exe" "<draft.pdf>"
& "$bin\pdftoppm.exe" -png -r 125 -f <first> -l <last> "<draft.pdf>" "<outdir>\page"
```

125 dpi reads form checkboxes and grid columns; 100 dpi is enough for
exhibit charts; 80 dpi for a quick skim of many pages.

### Trap 1 — checkboxes: the text layer prints BOTH options

"Yes  No" extracts identically whether Yes, No, both, or neither is
checked. Every finding about a checkbox state — including the surprising
ones like both boxes checked at once, which TOTAL happily allows —
comes from a rendered page, never from text.

### Trap 2 — grid columns: text order is not column order

The sales grid and the prior-sale/transfer grid extract as an
interleaved stream. A prior-sale date that appears right after the
subject's row label can sit in COMP 1's column on the rendered page.
A real review attributed a comp's $149,000 prior sale to the subject
this way and shipped a MAJOR finding that had to be retracted. Rule:
any finding that depends on WHICH column a value sits in requires the
rendered page.

### Trap 3 — exhibit pages have no text layer

TrueTracts market analyses, location maps, aerial/plat pages, sketches,
and license/E&O scans ride on form SCNLGL as embedded images. Text
extraction sees only the form footer (~60 chars). Two consequences:

- Never report an exhibit as missing from text evidence alone.
- The exhibits must be RENDERED AND READ, because the review has to
  check their numbers against the form (a TrueTracts supply page saying
  "In Shortage" while the form says "In Balance" is a top-tier finding,
  and it is only visible in the image).

## The sales contract

Contracts arrive as DocuSign scans or with broken glyph encodings. The
tracker's contract extractor flags these (`needsReview: true`, "price
is a guess"). If `pdftotext` output looks like cipher text — digits and
letters in nonsense runs — the ToUnicode maps are garbage. Do not try
to decode; rasterize every page and read the images. Handwritten or
checkbox-heavy pages (TN disclosure forms) need the image anyway to
cross-check numerals against written-out words.

What to pull from a TN FSBO/no-broker packet, page by page: parties and
price (p1), financing type checkbox (p2), earnest/as-is/utilities (p3),
closing date (p4), closing-cost split table (p5), OTHER PROVISIONS —
where concessions hide (p6), EXECUTED date + DocuSign dates (p7). The
property condition disclosure carries the seller's acquisition date and
disclosed defects — both feed the review.

## Documents missing from the job folder — the tracker backup

Order sheets and contracts he dropped on the tracker live in Pinewood's
IndexedDB, but every auto-backup JSON in
`OneDrive\Appraisal Tracker\Appraisal Tracker - Backups\` carries them
as base64 data-URLs. Find the newest backup, locate the attachment id
from the file's record, then:

```powershell
$raw = [System.IO.File]::ReadAllText($backupPath)
$pos = $raw.LastIndexOf('"<attachment-id>"')
$d = $raw.IndexOf('base64,', $pos)
$end = $raw.IndexOf('"', $d)
[System.IO.File]::WriteAllBytes($outPdf, [Convert]::FromBase64String($raw.Substring($d+7, $end-$d-7)))
```

The record itself also carries the tracker's parsed order fields and the
contract extractor's warnings — read those before trusting any of its
numbers.

## Public records for verification

All keyless; endpoints and gotchas in the `public-data-sources` memory.

- **TN statewide parcel layer** — owner, subdivision, GISLINK. OWNER2
  of a single space means NO co-owner; the tracker renders that as
  "NAME & " and the trailing ampersand has been misread as a second
  person on title. Check OWNER2 itself, not the rendering.
- **TPAD** (`LINK_TPAD` from the parcel record; needs a browser
  User-Agent) — assessor land/improvement values, living area, year
  built, City # (non-zero = inside city limits, which changes the tax
  math), and the SALE HISTORY WITH QUALIFICATION CODES. "B - FAMILY
  SALE" on a prior transfer reframes a price jump from flip-red-flag to
  non-arm's-length-plus-renovations. Always read the codes.
- **Census geocoder / FEMA NFHL** — tract and the whole FEMA block, to
  confirm the form's entries.

## The MLS export

RealTracs `All - <timestamp>.csv` exports mix Closed, Active, and Under
Contract rows — filter by `ListingStatus`, and filter
`PropertySubType = 'Site Built'` before computing anything (manufactured
rows contaminate medians). `BindingContractDate` is the Fannie-correct
date for anything time-related. `ListToContractDays` beats
`DaysOnMarket`, which resets on relist. Use the export to check the
grid's range statements ("N sales from $X to $Y" must actually bracket
the comps used), comp data (DOM, prior transfers), and the
supply/demand checkbox.
