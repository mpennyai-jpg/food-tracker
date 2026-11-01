# Watch log build

Builds Todd's watch log page: every film and series he has rated, grouped by
medium, then genre, then score. Source data comes from the brain entries
`me/2026-10-17-02-movie-ratings.md`, `me/2026-10-17-tv-show-ratings.md` and the
six individual rating captures dated 2026-10-18.

## Files

| File | What it is |
|---|---|
| `movies.psv`, `tv.psv`, `queue.psv` | The data. Pipe-delimited: title, year, rating, genre, description. |
| `build.py` | Turns the three .psv files into `data.json`, grouped and ranked. |
| `page_head.html`, `body.html`, `script.js` | The page: styles, markup, behaviour. |
| `assemble.py` | Writes `watch-log.html` (for publishing as an artifact) and `todd-watch-log.html` (standalone, opens in a browser). |
| `embed_posters.py` | Downloads each poster from Wikipedia and writes `posters.json` as data URIs. |

## Build

    python3 build.py        # data.json
    python3 assemble.py     # watch-log.html + todd-watch-log.html

## Posters

Claude artifacts block images from outside sites, so a shared page can only
show posters that are embedded in it. `embed_posters.py` fetches them and
writes `posters.json`; `assemble.py` inlines that file when it is present.

It needs `en.wikipedia.org` and `upload.wikimedia.org` reachable. A cloud
session picks up the environment's network policy when its container starts,
so a session that began before those domains were allowed cannot reach them —
start a new session instead.

    python3 embed_posters.py   # writes posters.json, prints hit count and payload size
