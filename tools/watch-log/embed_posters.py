"""Fetch each poster from Wikipedia, shrink it, and store it as a data URI.
Run only once en.wikipedia.org and upload.wikimedia.org are allowed."""
import base64, io, json, os, sys, time, urllib.error, urllib.parse, urllib.request
from concurrent.futures import ThreadPoolExecutor
from PIL import Image

BASE = os.path.dirname(os.path.abspath(__file__))
# Wikimedia returns 403 to clients that do not identify themselves with a
# contact address. See https://meta.wikimedia.org/wiki/User-Agent_policy
UA = ("WatchLogBuild/1.0 "
      "(+https://github.com/mpennyai-jpg/food-tracker; personal watch list) "
      "python-urllib")
W, H, QUALITY = 124, 186, 72          # 2x the 3.8rem display slot
API = "https://en.wikipedia.org/w/api.php"


def get(url):
    req = urllib.request.Request(url, headers={
        "User-Agent": UA,
        "Accept": "application/json,image/*;q=0.9,*/*;q=0.8",
        "Accept-Encoding": "identity",
    })
    for attempt in range(6):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < 5:
                ra = e.headers.get("Retry-After") or ""
                wait = int(ra) if ra.isdigit() else 2 ** (attempt + 1)
                time.sleep(min(wait, 60))
                continue
            _raise_http(e, url)
        except urllib.error.URLError as e:
            raise RuntimeError("cannot reach %s :: %s" % (url.split("?")[0], e.reason))


def _raise_http(e, url):
    body = ""
    try:
        body = e.read()[:200].decode("utf-8", "replace")
        if body.lstrip().startswith("<"):
            body = "(html error page)"
    except Exception:
        pass
    raise RuntimeError("HTTP %s from %s :: %s" % (e.code, url.split("?")[0], body))


def preflight():
    """Fail loudly and clearly before attempting 253 downloads."""
    print("checking reachability ...")
    try:
        get(API + "?action=query&format=json&titles=Sicario")
        print("  en.wikipedia.org OK")
    except Exception as e:
        print("  en.wikipedia.org FAILED: %s" % e)
        return False
    try:
        src = thumb_url("Sicario 2015 film")
        if not src:
            print("  no thumbnail returned for the test title")
            return False
        get(src)
        print("  upload.wikimedia.org OK (%s)" % src.split("/")[2])
    except Exception as e:
        print("  image download FAILED: %s" % e)
        return False
    return True


def thumb_url(query):
    qs = urllib.parse.urlencode({
        "action": "query", "format": "json", "generator": "search",
        "gsrsearch": query, "gsrlimit": "1",
        "prop": "pageimages", "piprop": "thumbnail", "pithumbsize": "400",
        "pilicense": "any",  # posters are non-free; default "free" hides them
    })
    pages = (json.loads(get(API + "?" + qs)).get("query") or {}).get("pages") or {}
    for p in pages.values():
        src = (p.get("thumbnail") or {}).get("source")
        if src:
            return src
    return None


def to_data_uri(raw):
    im = Image.open(io.BytesIO(raw))
    im = im.convert("RGB")
    # cover-crop to a 2:3 poster box, matching the CSS object-fit
    scale = max(W / im.width, H / im.height)
    im = im.resize((max(1, round(im.width * scale)), max(1, round(im.height * scale))), Image.LANCZOS)
    left, top = (im.width - W) // 2, (im.height - H) // 2
    im = im.crop((left, top, left + W, top + H))
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=QUALITY, optimize=True, progressive=True)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def one(item):
    for q in [item["q"], item.get("q2")]:
        if not q:
            continue
        try:
            src = thumb_url(q)
            if src:
                return item["q"], to_data_uri(get(src)), item["t"]
        except Exception as e:
            print("  ! %s (%s): %s" % (item["t"], q, e), file=sys.stderr)
    return item["q"], None, item["t"]


def main():
    if not preflight():
        print("\nStopping: the fetch cannot work from here. Send the lines above to Claude.")
        return 1
    d = json.load(open(os.path.join(BASE, "data.json"), encoding="utf-8"))
    items, seen = [], set()
    for grp in d["movies"] + d["tv"]:
        for it in grp["items"]:
            if it["q"] not in seen:
                seen.add(it["q"]); items.append(it)
    for it in d["queue"]:
        if it["q"] not in seen:
            seen.add(it["q"]); items.append(it)

    path = os.path.join(BASE, "posters.json")
    try:
        out = json.load(open(path, encoding="utf-8"))
    except Exception:
        out = {}
    kept = len([it for it in items if it["q"] in out])
    if kept:
        print("keeping %d posters already fetched" % kept)
    todo = [it for it in items if it["q"] not in out]
    misses = []
    with ThreadPoolExecutor(max_workers=2) as ex:
        for i, (q, uri, title) in enumerate(ex.map(one, todo), 1):
            if uri:
                out[q] = uri
            else:
                misses.append(title)
            if i % 25 == 0:
                print("  %d/%d" % (i, len(todo)))

    json.dump(out, open(path, "w", encoding="utf-8"), ensure_ascii=False)
    size = sum(len(v) for v in out.values())
    print("\nposters embedded: %d of %d" % (len(out), len(items)))
    print("payload: %.1f MB" % (size / 1e6))
    if misses:
        print("no match (%d): %s" % (len(misses), ", ".join(misses)))


if __name__ == "__main__":
    sys.exit(main() or 0)
