# 11 - BIG Serpentine Pavilion: parametric visual model

## Design intent

This script creates a visual approximation of BIG's 2016 Serpentine Pavilion
using your reference photographs. It follows the key modelling idea described
by BIG: an orthogonal wall of hollow fibreglass frames pulled apart in a
checkerboard pattern, with two undulating sides converging into one wall above.

This is **not two complete walls of boxes**. Each position in a rectangular
column/course grid receives exactly one hollow box. Alternate positions move
toward opposite base curves; their lateral displacement reduces with height.
At the top course, they form one straight wall again.

The existing photographs and `BIG_Seprentine_Pavillion_nativeGrasshopper.gh`
are left untouched. The new Python script is standalone and does not require
that Grasshopper definition or any extra Python packages.

### Assumptions about your controls

- **Base curves:** two open ground-plan guides, one for each side of the wall.
- **Height:** the exact overall model height above World XY.
- **Depth:** the front-to-back extrusion length of each hollow box, not the
  overall pavilion footprint depth.
- **Module size:** independently adjustable nominal width and height.
- **Opening width:** the maximum sampled, nominal clear gap between the two
  ground-level wall envelopes, **not an entrance-door width**.

The whole pavilion's transverse extent depends on both curves, the opening
width, and the box depth. There is no separate overall-footprint-depth slider.
If you intend opening width to mean entrance width, this model's opening
control would need to be changed; it currently controls the widest internal gap.

This is a conceptual visual model, not surveyed geometry, a structural analysis,
an accessibility check, or a fabrication model. Connections, aluminium profiles,
foundations, paving, benches, texture, and detailed material translucency are not
included. Individual tubes have wall thickness, but the assembly is not checked
for collisions, support, or buildability.

## 1. Quick start in Grasshopper

1. Use **Rhino 8 -> Grasshopper -> Python 3 Script**, in **Script mode** rather
   than SDK/`RunScript` mode.
2. Paste the complete contents of `11_BIG_SerpentinePavillion.py` into the editor.
3. Remove unused default inputs such as `x` and `y`, or mark them Optional.
4. **Leave the special output `out` alone.** Rename the regular output `a` to
   **`meshes`**. Add regular outputs named **`colours`** and **`info`**.
5. Connect `meshes` to **Custom Preview G** and `colours` to **Custom Preview M**.
6. Connect `info` to a Panel. Disable the Python component's own preview so the
   default preview and helper geometry do not cover the Custom Preview result.
7. Run with defaults first; then add the inputs below, matching their names.

**You can run with no inputs.** The script generates a pair of S-shaped base
guides and uses default dimensions. If you add an input but leave it unwired,
mark it **Optional** so Grasshopper still executes the component.

The default model uses 56 columns and 35 courses: **1,960 hollow modules**.
This is a configurable interpretation, not an attempt to duplicate the original
building's exact module count.

## 2. Inputs

Use **Item Access for every input**, including the two curves. Supply one value
or curve to each input, not a list, unless you deliberately want Grasshopper to
run the entire script multiple times.

### Main controls

| Exact input name | Type hint | Default | Suggested slider / connection | Purpose |
|---|---|---:|---|---|
| `base_a` | `Curve` | Built-in guide | Curve parameter referencing one open Rhino curve | First side of the ground-level wall |
| `base_b` | `Curve` | Built-in guide | Curve parameter referencing a second open Rhino curve | Other side of the ground-level wall |
| `height` | `float` | 14000 | 3000-16000 | Overall pavilion height |
| `depth` | `float` | 1000 | 300-2000 | Hollow box extrusion depth |
| `module_width` | `float` | 500 | 250-1000 | Desired maximum box width along the pavilion axis |
| `module_height` | `float` | 400 | 200-800 | Desired maximum course/box height |
| `opening_width` | `float` | See below | 0-14000 | Maximum sampled nominal ground clear gap |

`opening_width` has two useful default behaviours:

- With the **built-in curves**, leaving it absent or unwired gives a maximum
  nominal clear gap of **10000** model units.
- With **your own curves**, leaving it absent or unwired preserves their spacing.
  Wiring a slider explicitly rescales their separation to set the requested gap.

Connect **both base curves or neither**. One missing curve is an error rather
than an invented or automatically offset second wall.

### Optional controls

| Exact input name | Type hint | Default | Suggested slider | Purpose |
|---|---|---:|---|---|
| `length` | `float` | 28000 | 10000-40000 | Length of the built-in guides; ignored for custom curves |
| `thickness` | `float` | 12 | 5-40 | Thickness of the four walls and end rims of each tube |
| `gap` | `float` | 0 | 0-30 | Additional joint spacing between columns and courses |
| `profile_power` | `float` | 1.7 | 0.2-5.0 | How quickly the wall closes toward the ridge with height |

All lengths use **Rhino model units**. Defaults are intended for **millimetres**:
28000 is 28 metres, not 28,000 metres. For a metre-based file, divide every length
value by 1000, including `length`, `thickness`, `gap`, and `opening_width`.
Keep `profile_power` unchanged. For example: height 14, depth 1, module width 0.5,
module height 0.4, opening width 10, length 28, thickness 0.012.

## 3. Drawing and connecting your base curves

1. In Rhino's Top view, draw **two open, non-crossing curves** running in roughly
   the same direction. S-curves, arcs and polylines can work.
2. Keep their start regions near one another and their end regions near one
   another. Each curve should progress continuously along the pavilion length.
3. Reference each through a Grasshopper Curve parameter and connect it to
   `base_a` or `base_b`.
4. Initially leave `opening_width` unwired to see the spacing you actually drew.
5. Add an `opening_width` slider if you want to widen or narrow the gap without
   redrawing the guides.

The script duplicates the curves, projects them to World XY, and aligns their
directions by comparing endpoint distances. It does **not** change the Rhino
curves themselves. Nonzero input elevations are ignored and reported in `info`.

The straight line between the average start and average end positions defines
the pavilion axis. Both curves must be **single-valued across cross-sections
perpendicular to that axis**: every working section must intersect each curve
once. Closed loops, curves that double back, and cross-section-aligned segments
are not suitable for this orthogonal-grid model.

If the curves have different extents, only their shared axial interval is used.
Their full arc lengths are not forced to match. This keeps all modules aligned
to one orthogonal grid instead of rotating or distorting boxes along a curve.

The `base_profiles` output shows the **working, sampled centre guides after any
opening-width override**. Those can differ from the original input curves.
They describe each side's envelope; because positions alternate between sides,
there is not a box on both guides at every column of a given course.

## 4. Outputs and preview

The special console output and regular geometry outputs are different:

```text
out             -> Panel, optional printed diagnostics only
meshes          -> Custom Preview G
colours         -> Custom Preview M
info            -> Panel
```

**If `meshes` returns text, you probably renamed the special `out` socket.**
Restore that socket to `out`, then rename the regular `a` output to `meshes`,
or add a new regular output named `meshes`. Alternatively, turn off **Standard
Output/Error Parameter** in the component context menu to remove the special
console socket. The Python geometry variables do not need to change.

| Regular output | Contents |
|---|---|
| `meshes` | One hollow rectangular tube mesh per grid position |
| `colours` | One pale grey-green preview colour per tube |
| `base_profiles` | The two working ground-level side guides |
| `ridge` | Straight guide along the top of the pavilion |
| `centres` | Tube-centre points |
| `module_planes` | Horizontal placement planes, with local Y along tube depth |
| `row_ids` | Zero-based course index for each tube |
| `side_ids` | 0 for the lower local-Y side, 1 for the upper side, -1 for the merged top course |
| `info` | Dimensions, fitted sizes, counts, nominal clearances, and warnings |

Output lists match: index `row * column_count + column` refers to the same tube
in `meshes`, `colours`, `centres`, `module_planes`, `row_ids`, and `side_ids`.
`base_profiles` and `ridge` are separate guide outputs, not per-module lists.

Use an oblique shaded view to see the unzipping and a view along tube depth to
see the open apertures. The ends are open; they are **not capped opaque boxes**.
Colours are stored on mesh vertices as well as provided separately for Custom
Preview. The preview is deliberately opaque for legibility; the original
fibreglass's translucency, woven texture and lighting would need render materials.

## 5. How the code works

### A. Fit the grid to the overall dimensions

The script determines a column count and course count from the desired maximum
module dimensions and joint gap:

```text
count = ceil((overall_span + gap) / (desired_module_size + gap))
actual_module_size = (overall_span - (count - 1) * gap) / count
```

Every box has the same fitted width and height. The fitted dimensions are no
larger than the requested dimensions and are printed in `info`. This preserves
the exact overall height and usable axial length without introducing sliver
modules at the top or ends. At certain slider values the count changes and the
fitted module size steps down; that is intentional.

Depth is not fitted: it stays exactly at the `depth` input value. Thickness must
leave a positive aperture after fitting: the actual width and height must each
exceed twice `thickness`, plus the Rhino document tolerance.

### B. Set opening width without removing the S-curve

For each sampled axial station, take the midpoint and separation between the
two base curves. If an opening override is supplied:

```text
scale = (opening_width + depth) / maximum_sampled_base_separation
new lower guide = midpoint - original_separation * scale / 2
new upper guide = midpoint + original_separation * scale / 2
```

This preserves the local midpoint while changing the width. Subtracting box
depth from centre-to-centre separation gives the nominal clear gap. Guides are
sampled at 129 uniformly spaced stations plus every module column centre.

This is an **envelope measure**, not a measured unobstructed route through the
actual checkerboard boxes. It does not account for human height, headroom,
neighbouring-course projections, or local intersections. `info` also reports
nominal start/end gaps so they are not confused with the maximum interior gap.
Setting `opening_width = 0` makes the maximum nominal base gap zero; it does not
guarantee a traversable entrance or a completely coincident pair of walls.

### C. Alternate sides and close toward the ridge

Each grid cell chooses a side using:

```text
side = (row + column) % 2
vertical_fraction = row / (row_count - 1)
spread = (1 - vertical_fraction) ** profile_power
module lateral position = working_base_guide_position * spread
```

At the lowest course, `spread = 1`: the boxes follow the working base guides.
At the highest course, `spread = 0`: all boxes share the straight ridge axis.
Larger powers close the wall faster at low levels; smaller powers keep it wider
until nearer the top. Modules stay horizontal and orthogonally aligned; they
do not tilt onto the implied wall surface.

A single course cannot form this enclosure. In that case the script shows the
base checkerboard course and prints a warning rather than dividing by zero.

### D. Make genuine hollow visual modules

`tube_mesh` creates outer and inner rectangular rings at both ends, connects the
outer and inner walls, and connects the end rims. Each tube has **16 quad faces**
and a hole passing all the way through its depth. Sharp edges are unwelded for
flat-faced shading. The geometry is generated once, duplicated, and moved to
each placement plane rather than rebuilt separately at every grid position.

## 6. Useful variations

| Goal | Change |
|---|---|
| Reference-inspired initial model | Leave the defaults |
| Faster exploration | `module_width = 1000`, `module_height = 800` |
| Lower pavilion | Reduce `height` |
| Stronger hollow-box appearance | Increase `depth` and view obliquely |
| Wider internal space | Increase `opening_width` |
| More slowly closing enclosure | Reduce `profile_power`, for example to 0.8 |
| Preserve exactly the supplied base spacing | Disconnect `opening_width` and mark it Optional |
| Change plan shape | Edit the two Rhino curves |
| Change default plan length | Adjust `length` with no custom base curves connected |

## 7. Troubleshooting and limitations

- **Text instead of meshes:** keep `out` separate from regular geometry outputs;
  see section 4.
- **No result:** check exact input/output names, Item Access, Curve type hints,
  and Optional status on unwired inputs. Read runtime errors and `info`.
- **Curve intersection error:** use two open, non-crossing plan curves that each
  cross a perpendicular section once. Loops and sideways folds are unsupported.
- **The boxes look solid:** look along their depth direction and use a shaded
  viewport. Oblique views can hide the openings behind the tube walls.
- **Dimension differs from the size slider:** module width and height are fitted
  uniformly to exact overall dimensions; read the actual dimensions in `info`.
- **Entrance is not the requested width:** `opening_width` controls the maximum
  nominal base gap, not either end opening or walk-through clearance.
- **Some tubes collide:** the visual assembly is not collision-checked. Narrow
  base gaps and aggressive profiles can cause overlaps; a negative nominal gap
  produces a warning.
- **Thickness error:** reduce `thickness` or `gap`, or increase fitted module
  width and height. Use sensible document units and tolerances.
- **Slow solves:** use larger modules. The script rejects more than 12,000 tubes
  before creating them. The default model has 31,360 quad faces.

Curve sampling validates the working sections, but is not a mathematical proof
that arbitrary input curves never cross between samples. The module geometry
and preview still need to be checked in Rhino/Grasshopper for your chosen inputs.

## Reference basis

The design concept was checked against BIG's official **Serpentine Pavilion**
project description and the Serpentine Galleries' **Serpentine Pavilion 2016
designed by Bjarke Ingels Group** project page, alongside the three local
reference photographs. The dimensions and profile formula here are modelling
defaults, not an assertion of the pavilion's original setting-out geometry.
