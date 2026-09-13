# Public data endpoints that work without a key

One-line summary: URLs Penny rediscovered on 2026-09-13 for parcels, assessor detail, flood, and census. Worth keeping; they took a while to find.

## Tennessee statewide parcels

`https://services1.arcgis.com/YuVBSS7Y1of2Qud1/arcgis/rest/services/Tennessee_Property_Boundaries_Public_Use/FeatureServer/0/query`

- Query: `where=COUNTY_NAME='LINCOLN' AND ADDRESS LIKE '%<street>%<number>%'`
- Address strings are stored street-first, e.g. `OLD ELKTON PIKE 839`.
- Returns GISLINK, PARCELID, deed acres, owner, subdivision, lot, and a LINK_TPAD URL.

## TPAD parcel detail (state assessor)

`https://assessment.cot.tn.gov/TPAD/Parcel/GIS?gislink=<GISLINK url-encoded>`

- Needs a browser User-Agent. urllib with the default UA gets a 403; curl with a Chrome UA works.
- Gives year built, living area, building areas, outbuildings, assessor values, utilities, sale history, and for some counties zoning.

## FEMA flood

`https://hazards.fema.gov/arcgis/rest/services/public/NFHL/MapServer/28/query` for the zone, layer `3` for the FIRM panel.

- Point geometry, `inSR=4326`.
- EFF_DATE comes back as epoch milliseconds.

## Census geocoder

`https://geocoding.geo.census.gov/geocoder/geographies/onelineaddress?address=...&benchmark=Public_AR_Current&vintage=Current_Current&format=json`

- An empty "Urban Areas" list is the support for the Rural checkbox.

## Zoning availability by county (as of 2026-09)

- Davidson: publishes zoning per parcel.
- Marshall: TPAD carries it, but the county posts only the cover page of its resolution online.
- Lincoln, Bedford, Marshall: no queryable zoning layer.
- Rule: gate the legally-permissible test rather than inferring it.
