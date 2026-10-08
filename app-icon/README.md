# Pinewood Appraisal Tracker — phone app icon

One-line summary: logo/app-icon set and web-manifest files so the tracker at
`pinewood.taila3918b.ts.net` can be launched from a home-screen icon instead of an email link.

## The mark

A house outline with a pine tree inside — "Pinewood" + the appraisal subject, in the tracker's
own teal (`#2dd4bf`) on its dark navy (`#0d1a22` → `#17303c`). Reads at 48 px.

## Files

| File | What it is |
|---|---|
| `pinewood-icon.svg` | Vector master — edit this if the mark changes |
| `icon-512.png` | 512×512 app icon |
| `icon-192.png` | 192×192 app icon |
| `icon-512-maskable.png` | 512×512 with the art inside the 80% safe zone (Android adaptive icons) |
| `apple-touch-icon.png` | 180×180 for iPhone/iPad |
| `preview-96.png`, `preview-48.png` | Small previews, to check legibility |
| `manifest.webmanifest` | Web app manifest — name, colors, icons, standalone launch |
| `head-snippet.html` | The `<link>`/`<meta>` lines to paste into the page `<head>` |
| `render.py` | Script that generated the PNGs from the vector shapes |

## For Penny — serving it

1. Copy `icon-192.png`, `icon-512.png`, `icon-512-maskable.png` and `apple-touch-icon.png`
   into the app's static dir as `/icons/`.
2. Copy `manifest.webmanifest` to the site root (served as
   `application/manifest+json` if the server lets you set the type).
3. Paste `head-snippet.html` into `<head>` of the tracker's index page.
4. Reload once on the phone, then re-add to the home screen.

With the manifest in place the icon launches in standalone mode — no Chrome address bar,
no "pinewood.taila3918b.ts.net" warning strip.

## For Todd — putting it on the phone

Android / Chrome:
1. Open the tracker link once in Chrome.
2. ⋮ menu → **Add to Home screen** → **Install** (or **Add**).
3. The Pinewood icon lands on the home screen; tapping it opens the tracker directly.

iPhone / Safari: Share button → **Add to Home Screen**.

Note: the address is a Tailscale name, so the phone still needs Tailscale connected for the
icon to load — the icon replaces hunting for the email, not the VPN.
