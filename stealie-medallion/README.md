# Stealie LOVE medallion — 3D print files

Traced from the photo of the window sticker (`source/original_photo.jpg`).
Everything is modelled at **120 mm diameter**, flat-backed, no supports needed.

```
Base plate        0.0 → 2.4 mm
Colour / relief   2.4 → 3.2 mm
Total                   3.2 mm
```

## What to print

### A. Multi-colour (AMS / MMU / multi-tool)  →  `stealie_medallion_multicolour.3mf`
One file, five parts, colours already assigned. Open it, map each material to a
real filament, slice. If your slicer won't read the 3MF colours, use the STLs
in `multicolor_stl/` instead (below).

| Part | Suggested filament |
|---|---|
| `01_base_disc` | black |
| `02_black` | black |
| `03_white` | white / bone |
| `04_blue` | cornflower blue |
| `05_pink` | dusty rose / light mauve |

**Importing the STLs by hand:** load `01_base_disc.stl` first, then load the
other four **as parts of that same object** (Orca/Bambu: right-click → *Add part*;
PrusaSlicer: right-click → *Add part → Load*; Cura: select all → *Merge models*).
They share one origin, so they land in register — do **not** re-centre them
individually. Then assign a filament per part.

Swap `01_base_disc.stl` for `01b_base_disc_with_keyring_loop.stl` if you want a
hanging loop (7 mm boss, 6 mm hole) at the top. Use one or the other, not both.

### B. Single colour (any printer)  →  `single_color_stl/B_raised_line_art_*.stl`
Woodcut style: the backgrounds step down and the line work stands proud, one
solid part, no colour changes. Supplied at two sizes — print one.

| Artwork | Height above base |
|---|---|
| blue (outer field, sky) | 0.0 mm |
| pink (behind the skeletons) | 0.4 mm |
| white (skull, bones, clouds, LOVE) | 0.8 mm |
| black line work | 1.2 mm |

3.6 mm thick either way. Every step is 0.4 mm, so the terraces land on whole
layers at 0.1, 0.2 **and** 0.4 mm layer heights. Don't use a layer height that
doesn't divide 0.4 — 0.15 and 0.3 will blur the steps together.

Raised ribs print far better than sunk grooves: a rib narrower than the nozzle
still gets laid down as one clean extrusion, whereas a narrow groove just fills
in. Turn on **Arachne / variable-width perimeters** (default in current Orca,
PrusaSlicer and Cura) so the thinnest line work isn't dropped. The handful of
ribs that fall under 0.5 mm have been nudged out to that width in the mesh;
everything already wide enough is exactly as traced.

`A_tonal_relief.stl` is the inverse — white highest, line work sunk — kept in
case you want the softer, more graphic read. 120 mm only.

## Slicer settings

- **Layer height 0.10–0.16 mm.** The colour band is 0.8 mm, so 0.1 mm gives you
  8 layers of colour over the base — plenty of coverage over black.
- **Nozzle 0.4 mm** or smaller. The thinnest line in the artwork is about
  0.45 mm wide at 120 mm diameter, so 0.4 mm is the practical floor.
- **Print flat, artwork up. No supports, no brim needed.** First layer is a
  solid 120 mm circle.
- **Walls 2, top layers 5, infill 15 %.**
- Multi-colour: turn on a **prime tower**, and expect a lot of purge — this
  design changes colour on nearly every layer of the top band.

### Scaling and how much detail survives

0.4 mm of height is 2–4 layers — a hard shadow line under any lighting, so the
levels are never the limiting factor. Sideways detail is, and it holds up
better than you might expect. Measuring how much of the line art actually sits
in strokes narrower than a given width:

| Diameter | Median stroke | Art in strokes < 0.4 mm | < 0.6 mm |
|---|---|---|---|
| 100 mm | 0.62 mm | 5.7 % | 18 % |
| **120 mm** | **0.75 mm** | **1.0 %** | 12 % |
| **150 mm** | **0.94 mm** | **1.0 %** | 5.7 % |
| 180 mm | 1.12 mm | 0.1 % | 1.0 % |

At 120 mm only about 1 % of the line work is genuinely under a 0.4 mm nozzle,
and that 1 % has been thickened in the mesh. **120 mm prints fine.** 150 mm is
a little more comfortable and shows the rib and hatching detail more clearly,
which is why both are included.

If you want a different size, scale the 120 mm file uniformly — but note that
doing so scales the 0.4 mm steps too, which breaks the layer alignment above.
The 150 mm file was rebuilt rather than scaled so its steps stay at 0.4 mm.

## Notes on the trace

The source was a sunlit photo on curved glass, so the pipeline was: fit the
disc, warp it back to a true circle, divide out the lighting gradient to kill
the glare, cluster the colours into four, then hand-repair reflections and
scratches in the plain blue field. `source/flattened_disc.jpg` is the corrected
photo and `source/colour_separation.png` is the final four-colour map the
geometry was cut from.

Contours are simplified to 0.064 mm, which leaves a handful of self-touching
vertices per part (8–44 edges out of ~70 000). Every slicer repairs these
silently; nothing needs fixing before you print.

## Vectors

`vector/` holds the same artwork as SVG at 1:1 mm scale — one file per colour
plus a combined full-colour version. Useful for laser cutting, vinyl, stencils,
or re-modelling the thing from scratch in CAD.

## A note on the art

This is Grateful Dead "Steal Your Face" artwork with a LOVE logo and the Bertha
and Uncle Sam skeletons — someone else's copyrighted design. Fine to print for
yourself; don't sell them.
