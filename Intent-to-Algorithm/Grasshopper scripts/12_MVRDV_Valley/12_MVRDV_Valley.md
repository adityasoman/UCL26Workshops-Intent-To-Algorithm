# 12 - Valley-inspired faceted towers and connected podium

## What changed

The revised default model includes **shared, connected lower floors** below all
three towers. Those floors are constructed once across the site, not as three
overlapping tower bases. The podium roof between the towers receives gardens.

The original cumulative inward taper has also been replaced. Upper floors are
cut with **height-limited, sloping planes**. Recesses can stop and the floors
above can project back out, creating angular facets, setbacks and cantilever-like
volumes. Window panels are placed on the actual inclined faces, not on vertical
walls left over from the earlier model.

**This is still a designed visual approximation, not exact MVRDV geometry.**
The default facet bands are a fixed, photo-inspired composition, not traced or
surveyed dimensions. Original floor profiles, the intricate podium landscape,
circulation, glass curtain-wall detailing and the building's precise cantilevers
are not reconstructed from the photographs.

## 1. Install or update the component

1. Use a **Rhino 8 Grasshopper Python 3 Script** component in **Script mode**.
2. Replace the entire script with `12_MVRDV_Valley.py` from this folder.
3. Keep the special console output **`out`** unchanged. Rename the regular
   output **`a` to `meshes`** and add **`colours`** and **`info`**.
4. Connect `meshes` to **Custom Preview G**, `colours` to **Custom Preview M**,
   and `info` to a Panel.
5. Disable the Python component's own preview and previews on helper outputs.
6. Keep all inputs on **Item Access**. Unwired inputs must be Optional, or can
   be omitted entirely to use the built-in defaults.

The existing height, floor-count, window and `max_setbacks` input names still
work. Add the new podium and tilt controls below if desired; they also have
defaults, so no extra inputs are necessary to see the connected base.

If the `meshes` socket returns text, restore the renamed console socket to
`out`, then add a regular output named `meshes`. The special `out` socket never
becomes a geometry output just because its label changes.

## 2. Height and floor-count semantics

**Tower heights and floor counts INCLUDE the shared podium.** The common
floors are geometrically shared, while the upper storey heights are calculated
independently for A, B and C:

```text
common storey height = podium_height / podium_floors
upper tower floors  = floors_a - podium_floors
upper storey height = (height_a - podium_height) / upper tower floors
```

The same calculation applies independently to B and C. There is no longer one
uniform `height / floors` value throughout a tower: common levels must align
under all three towers.

Default counts and dimensions, in millimetre-scale model units:

| Portion | Floor count | Elevation range | Storey height |
|---|---:|---:|---:|
| Shared podium | 4, constructed once | 0-14000 | 3500 |
| A above podium | 22 | 14000-100000 | 3909.09 |
| B above podium | 19 | 14000-81000 | 3526.32 |
| C above podium | 16 | 14000-67000 | 3312.50 |

This produces **61 separate floor blocks**, not 69: the four common floors are
not duplicated for each tower. Tower counts remain 26, 23 and 20 respectively
when their shared floors are included. The roof of each massing tower still
matches its height input exactly.

The four-floor podium and its height are modelling assumptions, not a claim
about the original building's exact connected-floor configuration.

## 3. Inputs and defaults

All inputs use **Item Access**. Names are case-sensitive. Use integer sliders
for inputs marked `int` and decimal sliders for `float`.

### Tower and window controls

| Exact input | Type hint | Default | Meaning |
|---|---|---:|---|
| `height_a` | `float` | 100000 | A's total height, including podium |
| `floors_a` | `int` | 26 | A's total floor count, including shared floors |
| `height_b` | `float` | 81000 | B's total height, including podium |
| `floors_b` | `int` | 23 | B's total floor count, including shared floors |
| `height_c` | `float` | 67000 | C's total height, including podium |
| `floors_c` | `int` | 20 | C's total floor count, including shared floors |
| `max_setbacks` | `int` | 12 | Maximum bounded facet-cut patches per tower |
| `window_width` | `float` | 1600 | Width of each dark panel |
| `window_height` | `float` | 2200 | Vertical height of each panel |

### New connected-base and facet controls

| Exact input | Type hint | Default | Suggested slider | Meaning |
|---|---|---:|---|---|
| `podium_floors` | `int` | 4 | 0-8 | Shared connected lower storeys |
| `podium_height` | `float` | 14000 | 6000-28000 | Combined height of those storeys |
| `podium_margin` | `float` | 2000 | 0-6000 | Extra X/Y padding around the common footprint |
| `facet_tilt` | `float` | 0.85 | 0-1 | Difference in cut depth over a facet band's height |

Set `podium_floors = 0` to disable the connected base; `podium_height` is then
ignored and towers use their original full-height/floor-count calculation.
With the podium enabled, each tower must have at least one floor and positive
height above it. The podium needs a positive total height.

### Other optional controls

| Exact input | Type hint | Default | Meaning |
|---|---|---:|---|
| `footprint_width` | `float` | 30000 | Initial local-X width of each tower |
| `footprint_depth` | `float` | 26000 | Initial local-Y depth of each tower |
| `tower_gap` | `float` | 8000 | Extra separation in the tower layout |
| `setback_depth` | `float` | 7000 | Maximum facet-cut depth before additional geometric limits |
| `seed` | `int` | 17 | 17 uses the fixed default bands; other values vary them |
| `window_spacing` | `float` | 750 | Horizontal space between panels |
| `window_sill` | `float` | 800 | Panel-bottom elevation above its floor base |
| `window_margin` | `float` | 250 | End margin and minimum window head allowance |
| `garden_inset` | `float` | 200 | Margin around each exposed planting patch |

The default towers now form a **shallow staggered row**: A at the left, B set
back in the middle, and C at the right. This replaces the previous equilateral
triangle. The common footprint is a convex hull around their uncut envelopes,
expanded by the podium padding. Its footprint is continuous, though it does not
reproduce the real project's site boundary or fine-grained valley circulation.

### Units and fitting windows

All lengths use Rhino model units; defaults assume a millimetre-scale model.
For metres, divide **every length input**, including optional defaults, by 1000.
Do not divide counts, `seed`, or `facet_tilt`. Geometry uses the document tolerance.

Windows must fit in the podium storeys and in each tower's upper storeys:

```text
window_sill + window_height + window_margin <= relevant storey height
```

The script reports an error rather than silently changing your inputs when this
fails. An inclined facet may also be too narrow for a full panel; those panels
are omitted rather than drawn across an edge.

## 4. Outputs and floor-wise organisation

| Output | Contents |
|---|---|
| `meshes` | Combined floor-block, window and garden meshes for preview |
| `colours` | Matching colours for `meshes` |
| `info` | Podium, tower, facet, panel and garden diagnostics |
| `floor_blocks` | One closed massing mesh per physically distinct storey |
| `block_colours` | Matching floor-block colours |
| `podium_blocks` | Shared floors only; a subset of `floor_blocks` |
| `podium_colours` | Matching colours for `podium_blocks` |
| `windows` | Dark panels grouped into at most one mesh per floor |
| `window_colours` | Matching window colours |
| `gardens` | Green terrace, podium-roof and tower-roof patches |
| `garden_colours` | Matching garden colours |
| `floor_outlines` | The bottom perimeter of each floor block |
| `tower_ids` | 0 for shared podium; 1, 2 or 3 for A, B or C |
| `floor_ids` | Zero-based overall floor index, including common levels |
| `window_block_ids` | Index into `floor_blocks` supporting each window mesh |
| `garden_block_ids` | Index into `floor_blocks` supporting each garden patch |
| `storey_heights` | Upper-tower storey heights, ordered A, B, C |
| `cut_counts` | Number of facet patches that actually affect each tower |

Ordering is **shared podium bottom-to-top, A upper floors, B upper floors,
C upper floors**. At default values, block indices 0-3 are common floors,
4-25 belong to A, 26-44 to B, and 45-60 to C. The upper floors have `floor_ids`
starting at 4, not zero.

Do not separately preview `podium_blocks` over the combined `meshes` preview:
they are the same objects, provided as a convenient selection subset. Likewise,
`tower_ids`, `floor_ids` and `floor_outlines` align with `floor_blocks`, not with
the longer combined preview list.

Blocks are full-storey mesh volumes, not Rhino block definitions or thin slabs.
The script does not bake objects, assign render materials or cut window holes.

## 5. How the facets and common floors are built

### Bounded, sloping cuts instead of a taper

The default `FACET_BANDS` table defines a start level, end level, plan angle,
strength and slope direction for each cut patch. Fractions of the tower's upper
floor count are rounded to floor boundaries. Each tower has a small preset
variation, and its seed sequence is independent of the others.

Within a band, a plane's cut depth changes linearly with elevation. The script
clips a floor's three-dimensional volume against that plane, creating actual
inclined facade faces. Its bottom and top outlines can differ. Outside that
band the cut is absent: volumes can project back out above recesses rather than
shrinking cumulatively forever.

`max_setbacks` retains its existing input name for compatibility, but now caps
**bounded cut patches** rather than cumulative single-level setbacks. A patch
can affect several floors and create several mesh faces. It is not a cap on
triangle count. Extra patches beyond the 12-entry preset use seeded variations.

Set `facet_tilt = 0` for vertical cut faces while retaining the level-bounded
recesses and projections. Set `max_setbacks = 0` or `setback_depth = 0` for plain
towers above the podium. Cut depths are additionally limited to protect a central
rectangle 44 percent of the original width and depth. This is a geometric
safeguard, not a validated structural core.

### Connected base with no duplicate volumes

Each podium storey is a single extrusion of the common hull. There are no tower
floor volumes inside those storeys. The first independent tower floors begin
at exactly `podium_height`, and their total number and height are the remaining
portion of the corresponding tower inputs.

The shared roof is therefore a real connected horizontal level, not three
disconnected pads or an extra slab superimposed on the tower bases.

### Windows follow the real facets

For every non-horizontal face, the script constructs a horizontal direction and
a second direction within the face plane. It fits full rectangular panels
between the available face intervals at sill and head height. Panels are kept
inside the facet, even when its edges are trapezoidal or sloping.

Panel height is measured vertically in world Z. Panels are offset slightly
outward from the face to avoid display flickering. They are still dark surface
representations, not openings through a wall.

### Gardens use the top and bottom outlines at the same level

For a tower terrace, the candidate region is its floor's **top** outline minus
the next floor's **bottom** outline. These are no longer necessarily the same
as either floor's ground-plane outline because the faces can slope.

For the shared roof, the script subtracts **all three first-tower-floor
footprints** from the podium roof. This leaves the connecting areas available
for garden patches without filling under tower bases. Top tower roofs have no
cover and also receive green patches.

The polygon differences are partitioned into convex pieces, then inset. This
can create seams between planting patches. Narrow pieces that disappear after
insetting are counted in `info`; setting `garden_inset = 0` retains the full
resolved terrace area.

Garden detection checks the immediately adjacent storey, **not exposure to the
sky**. A higher projecting volume can partially shelter a terrace below. This
is deliberate and is not a daylight, headroom, planting or accessibility check.
Gardens have no soil thickness and sit slightly above the massing surface for
display clarity.

## 6. Validation and limits

The revised pure-geometry calculations were checked for closed face topology,
outward normals, planar facets, window containment, garden area balance,
deterministic defaults and several edge-case controls. The default calculation
produces 61 blocks, 12 effective cut patches per tower, and 27 tower terrace
levels before garden insetting. These checks do **not** execute the RhinoCommon
mesh implementation or Grasshopper UI; preview the result there as well.

Limits remain 150 total floors per tower, 360 summed tower floor counts,
40 facet patches per tower, and 60,000 individual window panels. Podium floors
are limited to 10. Large counts and tiny dimensions can be slow or fail at the
document's modelling tolerance.

- **Missing common floors:** re-paste the updated script; make sure
  `podium_floors` is greater than zero and show the combined `meshes` output.
- **Podium/tower dimension error:** heights and counts include common floors;
  leave at least one upper floor and positive upper height for each tower.
- **Window-fit error:** adjust storey heights or panel height/sill/margin.
- **No jagged cuts:** use positive `max_setbacks` and `setback_depth`.
- **No inclined faces:** raise `facet_tilt` above zero.
- **Missing tiny gardens:** lower `garden_inset`; read the omitted-piece count.
- **Text instead of geometry:** keep `out` separate from regular outputs.

The existing reference photographs remain unchanged. This model is not an
architectural, structural, fabrication, safety or regulatory validation of the
real building. Exact reconstruction would require measured source geometry.
