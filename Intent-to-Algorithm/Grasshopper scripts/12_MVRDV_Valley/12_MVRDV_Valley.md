# 12 - MVRDV Valley-inspired floor-wise model

## What this creates

`12_MVRDV_Valley.py` creates an approximate, automatically generated three-tower
layout with these agreed features:

- Independent height and floor count for each tower.
- A maximum number of angled setback cuts per tower.
- One separate massing block for every floor.
- Dark facade panels representing windows, with adjustable width and height.
- Green surfaces on exposed setback terraces and tower roofs.

The towers are arranged around an open central valley. Cuts face mainly toward
that valley, leaving the outer sides straighter. Warm stone-like floor blocks,
dark blue-grey panels, and green planting patches distinguish the three layers.

This is a **Valley-inspired visual interpretation**, not MVRDV's original
geometry. The real project combines a smooth glass outer shell with craggy,
stone-clad, planted inner faces. The script simplifies that contrast into
floor-wise massing, windows, and terrace gardens. It does not recreate the
shared podium, public circulation, exact footprints, cantilevers, balconies,
railings, structural system, detailed glazing, or individual plants.

To keep garden detection reliable, upper floors are always contained within
the floor below. The resulting towers step inward; they do not grow out again
into the original building's irregular cantilevers.

The three reference photographs in this folder are left unchanged. No images
or external packages are loaded when the Grasshopper component runs.

## 1. Grasshopper setup

1. Place a **Rhino 8 Grasshopper Python 3 Script** component.
2. Use **Script mode**, not SDK/`RunScript` mode, and paste in the entire Python
   file.
3. Remove unused default inputs such as `x` and `y`, or make them Optional.
4. **Keep the special output `out` unchanged.** Rename the regular output `a`
   to **`meshes`**. Add regular outputs **`colours`** and **`info`**.
5. Connect `meshes` to **Custom Preview G** and `colours` to **Custom Preview M**.
6. Connect `info` to a Panel. Turn off the Python component's own preview and
   the preview on other helper geometry parameters.
7. Run with defaults, then add the named inputs from section 2.

```text
Python meshes  -> Custom Preview G
Python colours -> Custom Preview M
Python info    -> Panel
Python out     -> Panel (optional console text)
```

**The script runs without inputs.** It supplies a complete default layout.
Inputs that you add but leave unwired must be marked **Optional** so the
component is allowed to execute and use the defaults.

If `meshes` contains a printed summary rather than geometry, you have probably
renamed the console socket. Rename that socket back to `out` and add or rename
a regular result socket to `meshes`. Renaming `out` does not change its function.

## 2. Inputs

Use **Item Access for all inputs**. Names are case-sensitive. Connect one slider
value per input to avoid Grasshopper running the entire model repeatedly.

### Independent tower controls

| Input name | Type hint | Default | Suggested slider |
|---|---|---:|---|
| `height_a` | `float` | 100000 | 30000-150000 |
| `floors_a` | `int` | 26 | Integers 5-40 |
| `height_b` | `float` | 81000 | 30000-150000 |
| `floors_b` | `int` | 23 | Integers 5-40 |
| `height_c` | `float` | 67000 | 30000-150000 |
| `floors_c` | `int` | 20 | Integers 5-40 |

Each tower starts at Z = 0. Its floor-to-floor height is exactly:

```text
floor-to-floor height = tower height / tower floor count
```

The defaults give approximately 3846.15, 3521.74, and 3350 model units for A, B,
and C respectively, with **69 separate floor blocks** in total. The floor counts
are modelling choices, not the project's documented floor counts.

The default heights correspond to the 100 m, 81 m, and 67 m tower heights in
MVRDV's project description when used in a millimetre document. Tower labels and
positions here are arbitrary modelling labels, not official tower identifiers.

### Setback and window controls

| Input name | Type hint | Default | Suggested slider | Meaning |
|---|---|---:|---|---|
| `max_setbacks` | `int` | 12 | Integers 0-25 | Maximum unique angled cut events applied to each tower |
| `window_width` | `float` | 1600 | 600-3500 | Width of each dark window panel |
| `window_height` | `float` | 2200 | 1000-2800 | Height of each dark window panel |

`max_setbacks` limits **cuts over a whole tower**, not the number of polygon
edges on every floor and not the number of mesh faces. Each event introduces
one angled inward cut at one selected level and keeps that cut on higher floors.
At most one new cut is introduced at each level. The actual count cannot exceed
`min(max_setbacks, floors - 1)` and can be lower if a cut is too small to resolve.

Set `max_setbacks = 0` for three simple rectangular towers with roof gardens.
Set it higher for more stepped levels. Every intermediate floor is still a
separate block even when several consecutive floors share the same outline.

### Optional controls

| Input name | Type hint | Default | Suggested slider | Meaning |
|---|---|---:|---|---|
| `footprint_width` | `float` | 30000 | 18000-45000 | Initial local-X width of each tower |
| `footprint_depth` | `float` | 26000 | 18000-40000 | Initial local-Y depth of each tower |
| `tower_gap` | `float` | 8000 | 0-25000 | Separation between bounding circles used to lay out the towers |
| `setback_depth` | `float` | 4500 | 0-8000 | Upper limit on the depth of a new cut |
| `seed` | `int` | 17 | Integers 0-100 | Repeatable cut levels, orientations and depths |
| `window_spacing` | `float` | 750 | 200-2000 | Horizontal gap between panels along each facade segment |
| `window_sill` | `float` | 800 | 0-1200 | Panel-bottom height above the floor base |
| `window_margin` | `float` | 250 | 100-700 | Minimum facade-end margin and required head margin |
| `garden_inset` | `float` | 200 | 0-1000 | Inward margin around each exposed garden patch |

The default layout is a triangular/U-shaped arrangement around the origin: A
front-left, B front-right, and C behind them. A and B have small opposite plan
rotations. Initial tower footprints share the width/depth inputs; their heights,
floor counts and cut sequences are independent.

`tower_gap` is not the exact wall-to-wall valley width. The centre spacing is
`sqrt(footprint_width^2 + footprint_depth^2) + tower_gap`, which keeps the initial
rotated rectangles from overlapping. Setbacks remain inside those rectangles.

### Units and window fit

**All lengths are in Rhino model units.** Defaults are millimetre-scale values;
the script does not automatically convert units. For metres, divide every
length input by 1000, including the optional footprint, spacing, sill, margin,
setback, tower-gap and garden-inset inputs. Keep floor counts, `max_setbacks`,
and `seed` unchanged.

The requested windows must fit vertically in **every** tower:

```text
window_sill + window_height + window_margin <= height / floors
```

The script gives a clear error naming the tower if they do not fit. It does not
silently resize windows or change your floor count. For example, raising a floor
count without increasing tower height may require a smaller window height.

## 3. Outputs: combined preview and separate floor-wise geometry

The minimum outputs are `meshes`, `colours`, and `info`. Add the other regular
outputs only if you want to inspect or use the layers separately.

| Output | Contents |
|---|---|
| `meshes` | Combined preview list: floor blocks, then window meshes, then gardens |
| `colours` | One matching colour per item in `meshes` |
| `info` | Per-tower dimensions, actual cut counts, panel count and garden summary |
| `floor_blocks` | One full-storey, closed massing mesh per floor |
| `block_colours` | Matching colours for `floor_blocks` |
| `windows` | Dark panel geometry grouped into at most one mesh per floor |
| `window_colours` | Matching colours for `windows` |
| `gardens` | Horizontal green terrace and roof patch meshes |
| `garden_colours` | Matching colours for `gardens` |
| `floor_outlines` | Closed base perimeter curve for each floor block |
| `tower_ids` | Tower number 1, 2 or 3, aligned with `floor_blocks` |
| `floor_ids` | Zero-based floor index within its tower, aligned with `floor_blocks` |
| `window_block_ids` | Zero-based index into `floor_blocks` for each window mesh |
| `garden_block_ids` | Zero-based index into `floor_blocks` supporting each garden |
| `storey_heights` | Three numbers, ordered A, B, C |
| `cut_counts` | Three actual setback counts, ordered A, B, C |

`floor_blocks` are ordered **A bottom-to-top, then B bottom-to-top, then C**.
At the defaults, block indices 0-25 belong to A, 26-48 to B, and 49-68 to C.
They are separate mesh objects, not Rhino block definitions and not thin slabs:
each represents the entire volume of one storey.

`tower_ids`, `floor_ids`, and `floor_outlines` correspond to `floor_blocks`,
**not** to the longer combined `meshes` list. Use `window_block_ids` and
`garden_block_ids` to associate those layers with a specific floor.

For separate control, use three Custom Preview components:

```text
floor_blocks + block_colours   -> first Custom Preview
windows + window_colours      -> second Custom Preview
gardens + garden_colours      -> third Custom Preview
```

Disable the combined preview if you use separate previews. Colour data are also
stored on mesh vertices, but the script does not bake anything or assign Rhino
render materials. Baked objects may need their display/materials configured.

## 4. How the model works

### A. Independent floor stacks

Each tower begins with a rectangular plan. Its assigned total height is divided
by its own floor count. Every polygon is extruded between successive floor
elevations, so changing the height of A does not change B or C.

### B. A capped sequence of angled setbacks

For each tower, the seeded generator selects up to `max_setbacks` distinct
levels above the ground floor. At each selected level it chooses a cut direction
within roughly 78 degrees either side of the direction toward the central
valley. The cut removes a portion of the current plan using a straight clipping
line. The remaining polygon carries forward to the next floor.

These are **angled plan cuts with stepped vertical transitions**, not continuous
sloping facade surfaces. Width and depth vary as the clipped outline evolves.
Cut depth is capped both by `setback_depth` and a protected central rectangle
44 percent of the initial footprint width and depth. That rectangle is a
geometric safeguard, not a designed or validated structural core.

Because every subsequent footprint is contained in the one before it, no tower
develops an overhang. This intentionally simplifies the real building. Changing
`seed` redistributes the levels and cuts. Each tower uses an independent seeded
sequence, so changing A's floor count does not regenerate B's or C's cuts.

### C. Dark window panels

For each floor and facade segment, the script calculates how many full-width
panels fit after reserving the end margins and gaps. The panel group is centred
along that segment. Panel height and sill position use your inputs directly.

An edge too short for a full window gets no panel; the script does not stretch
or crop it. All panels are combined into one window mesh per floor for a lighter
Grasshopper model. A floor with no panels is omitted from the `windows` list;
the `window_block_ids` mapping handles that case.

Panels sit a very small distance outside the facade to avoid flickering from
coincident faces. **There are no physical window holes** or Boolean wall cuts,
as requested. Frames, mullions, reveals and interiors are not modelled.

### D. Automatic exposed-terrace gardens

At the top of each floor, the garden candidate area is:

```text
current floor footprint minus next floor footprint
```

The script partitions this polygon difference into convex patches using 2D
half-plane clipping, without requiring mesh or Brep Booleans. Identical stacked
floors produce no garden. The top floor has no floor above it, so its entire
roof becomes a garden candidate.

Since upper floors are nested, the next floor also contains all floors above
it. A terrace not covered by the next floor cannot be covered by a later floor.
The separated tower layout prevents another tower overlapping it in plan.

Each patch is inset by `garden_inset` to leave a small edge margin. Thin pieces
that disappear after insetting are omitted and counted in `info`. Set
`garden_inset = 0` to colour the full resolved exposed area. These are simple
green horizontal surfaces, not individual planters or plant models.

Window and garden overlays use a small tolerance-aware offset. Floor-block
roofs match your tower heights; green roof overlays sit slightly above them
for display clarity and have no soil thickness.

## 5. Suggested variations

| Goal | Change |
|---|---|
| Three simple towers | `max_setbacks = 0` |
| A few larger terraces | Reduce `max_setbacks`, increase `setback_depth` |
| More stepped levels | Increase `max_setbacks`, within each tower's floor count |
| New but repeatable shape | Change `seed` |
| Wider central valley | Increase `tower_gap` |
| Taller A only | Increase `height_a` |
| More storeys in B | Increase `floors_b`, keeping the window-fit rule in mind |
| Wider openings visually | Increase `window_width` |
| More solid facade between windows | Increase `window_spacing` |
| Green all resolved terrace area | Set `garden_inset = 0` |

## 6. Troubleshooting and limits

- **Text instead of geometry:** keep the special `out` socket separate and use
  regular outputs named `meshes` and `colours`.
- **Unconnected input stops execution:** mark that input Optional or remove it
  so its default is used.
- **Window-height error:** adjust the named tower's height/floor count or reduce
  `window_height`, `window_sill`, or `window_margin`.
- **Missing windows on narrow facets:** no full-width panel fits there; reduce
  width or margins if needed.
- **Missing tiny garden strips:** reduce `garden_inset`. The script reports
  omitted exposed pieces.
- **No intermediate gardens:** set `max_setbacks` and `setback_depth` above zero.
  Towers with only one floor can have a roof garden but no setbacks.
- **Wrong colours:** wire `colours` to Custom Preview M, disable overlapping
  previews, and deselect highlighted geometry/components.
- **Model too big:** defaults assume millimetre-scale dimensions. Adjust all
  lengths consistently for your document.
- **Slow interaction:** increase panel width/spacing or reduce floor counts.
  The script allows at most 150 floors per tower, 360 floors in total, 40 cut
  events per tower, and 60,000 individual window panels.

This is a visual massing exercise, not a check of structure, facade construction,
fire safety, access, daylight, drainage, garden loads, or architectural
compliance. Preview the model in Rhino/Grasshopper before relying on the output.

## Reference basis

The architectural cues and approximate height defaults were checked against
MVRDV's official **Valley** project description and the three local photographs
credited to Ossip van Duivenbode. The generated footprints, floor counts,
setbacks, window dimensions and garden layouts are modelling assumptions.
