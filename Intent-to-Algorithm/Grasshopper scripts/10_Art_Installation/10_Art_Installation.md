# 10 - Folded-paper art installation

## What this makes

`10_Art_Installation.py` creates a **visual model** inspired by the supplied
Matthew Shlian artwork: closely packed hexagonal modules, crisp triangular
folds, projecting pointed tips, a swirling direction field, and a red/orange/gold
colour distribution sampled from the reference photograph.

This is an approximation from one photograph, not a reconstruction of the
artist's original geometry. The photograph does not reveal the hidden folds or
exact depths. Each module is an open mesh shell, not a smooth circular cone,
solid object, developable folding pattern, or fabrication-ready part. Overhangs
and intersections between neighbouring modules are allowed for this visual model.

## 1. Grasshopper setup

Use **Rhino 8 -> Grasshopper -> Python 3 Script**, consistent with the other
lessons in this repository. Use **Script mode**, not SDK mode: the supplied code
runs at the top level, rather than inside a `RunScript` method. Legacy IronPython
components are not the target for this file.

1. Place a Python 3 Script component and open its editor.
2. Replace the existing code with the complete contents of
   `10_Art_Installation.py`.
3. Rename its inputs and outputs exactly as shown below. Remove unused default
   inputs such as `x` and `y`, and rename the default result output as needed.
4. Set every input to **Item Access**, not List or Tree Access. Give each input
   a single slider value; multiple values cause multiple component executions.
5. For inputs you add but leave unwired, enable **Optional** if necessary so the
   component runs without that input. Inputs not added at all use the script's
   built-in defaults. You can start with no inputs and add controls gradually.
6. Run the script and connect the preview as described in section 3.

There are no extra Python packages to install. The script uses RhinoCommon,
System.Drawing, and Python's standard library. The photograph is **not** read at
runtime: its sampled colour map is embedded in the script, so copying just the
code to another machine works.

## 2. Inputs and suggested sliders

### Main controls

All lengths are in the current Rhino model units. Defaults are intended for a
millimetre-scale model, but the code does not change the document's units.

| Input name | Type hint | Default | Suggested slider | Effect |
|---|---|---:|---|---|
| `cols` | `int` | 22 | Integers 1-60 | Number of hexagon columns |
| `rows` | `int` | 20 | Integers 1-60 | Number of hexagons in each column |
| `cell_size` | `float` | 70.0 | 10-150 | Nominal hexagon diameter, measured corner to opposite corner, before gaps |
| `height_min` | `float` | 12.0 | 1-100 | Lower bound for tip height above the base plane |
| `height_max` | `float` | 85.0 | 1-200 | Upper bound for tip height above the base plane |
| `rotation_deg` | `float` | 0.0 | -180 to 180 | Rotates every tip's direction by this many degrees |
| `twist_deg` | `float` | 100.0 | -360 to 360 | Adds progressively more directional rotation farther from the swirl centre |

For a minimal component, add just these seven inputs. For an even simpler start,
add `cols`, `rows`, `cell_size`, `height_max`, and `rotation_deg`; everything else
uses the defaults.

### Optional controls

| Input name | Type hint | Default | Suggested slider / connection | Effect |
|---|---|---:|---|---|
| `lean` | `float` | 0.75 | 0-1.5 | Horizontal tip displacement divided by height; zero makes upright tips |
| `fold` | `float` | 0.65 | 0-1 | Strength of alternating shoulder heights and shoulder-ring twist |
| `gap` | `float` | 0.025 | 0-0.20 | Fractional shrinkage of each base, keeping grid centres fixed |
| `flow_x` | `float` | 0.35 | 0-1 | Swirl-centre position: left to right across the centre grid |
| `flow_y` | `float` | 0.35 | 0-1 | Swirl-centre position: bottom to top across the centre grid |
| `seed` | `int` | 7 | Integers 0-100 | Repeatable small height variations |
| `base_plane` | `Plane` | World XY | Plane parameter | Positions and orients the whole relief |

`height_max` must be at least `height_min`, and both must be positive. Set them
equal for a **uniform height** across all modules. They are bounds, not a promise
that some cell will reach each bound. `cell_size` changes spacing and base sizes;
it does not automatically rescale the height sliders. Scale those too to preserve
proportions when changing the overall size.

`rotation_deg` is the **tip/fold direction**, not rotation of the hexagonal grid
or of each hexagon's outer boundary. Rotating every base individually would break
the close-packed tiling. Use `base_plane` to rotate the whole panel. `twist_deg = 0`
removes the extra distance-dependent twist but retains the tangent swirl.

The validator allows up to 200 rows or columns individually, but at most 10,000
cells in total. It also rejects non-finite values, fractional counts, negative
sizes, `lean` outside 0-2, `fold` outside 0-1, and `gap` outside 0-0.5.

## 3. Outputs and colour preview

Add these outputs using the exact names:

| Output | Contents | Suggested connection |
|---|---|---|
| `meshes` | One faceted mesh per hexagonal module | Custom Preview **G** |
| `colours` | One System.Drawing colour per module | The same Custom Preview **M** |
| `outlines` | Closed hexagon base curves | Optional Curve parameter |
| `centres` | Base-centre points | Optional Point parameter |
| `tips` | Projecting apex points | Optional Point parameter |
| `angles` | Actual tip directions, degrees in [0, 360), relative to the base-plane X axis | Panel |
| `heights` | Actual apex heights, measured along the base-plane normal | Panel |
| `info` | Counts, base footprint, height range, preview reminder | Panel |

The component's built-in `out` output also receives the printed summary. All
lists use the same order: bottom row first, then left to right within each row.
The zero-based index is `row * cols + column`; alternating columns are staggered.

**Preview wiring:**

```text
Python: meshes  ----------------> Custom Preview: G
Python: colours ----------------> Custom Preview: M
Python: info    ----------------> Panel
```

Disable preview on the Python component and on extra geometry parameters after
connecting Custom Preview. This avoids the default preview covering the colours
or showing all the helper curves and points over the artwork. Keep `meshes` and
`colours` paired; do not sort or filter just one of them.

Use a shaded perspective viewport and an oblique view to see the relief. A top
view is useful for checking colour placement but hides much of the height.
Colours are also stored on mesh vertices, although Custom Preview is the intended
Grasshopper display path. Baking and rendering workflows can handle those colours
differently; this script does not assign Rhino document materials or bake objects.

The model starts centred on World XY, with tips pointing toward +Z. To mount it
on a vertical wall, supply a plane whose normal points out from that wall. Local
plane +Y always corresponds to the photograph's top. For example, a plane with
X axis along world +X and Y axis along world +Z stands upright and faces world -Y.

## 4. How the geometry works

### A. Staggered hexagonal grid

For `radius = cell_size / 2`, the centre spacings are:

```text
column spacing = 1.5 * radius
row spacing    = sqrt(3) * radius
odd columns    = shifted upward by half a row
actual base radius = radius * (1 - gap)
```

These are flat-top hexagons. At `gap = 0`, neighbouring base boundaries meet.
The upper folded surfaces can still overlap. The boundary is scalloped, rather
than trimmed to a rectangle. The default base footprint is approximately
**1,171 x 1,241 model units**; tips can extend beyond that footprint.

### B. Swirling rotation field

The vector from the adjustable swirl centre to each cell is normalized by the
larger panel dimension. Its direction is turned 90 degrees to make a tangent.

```text
tangent angle = atan2(distance_y, distance_x) + 90 degrees
tip angle     = tangent angle + rotation_deg + twist_deg * distance
```

The actual implementation converts between radians and degrees explicitly.
Positive angles turn counterclockwise in local XY when viewed from the +normal
side looking toward the base plane. There is no physically defined tangent
exactly at the swirl centre; `atan2(0, 0)` gives a repeatable fallback there.

### C. Height distribution

The script combines a bottom-to-top height bias, a broad sine ripple, and a small
seeded random variation. It clamps the resulting strength to 0-1, then computes:

```text
height = height_min + (height_max - height_min) * strength
```

This makes the lower part generally more pointed, while the upper part stays
shallower. The reference photograph is not a depth map: these heights are a
design choice. The random seed makes repeated solves with the same inputs stable;
changing the grid dimensions can change which random value belongs to a cell.

### D. Folded module, rather than a smooth cone

Each module has six base corners, six raised shoulder points, and one displaced
tip. The shoulder is approximately halfway between the boundary and the centre,
with alternating heights and a slight rotation controlled by `fold`. Each of the
six sectors contains two base-to-shoulder triangles and one shoulder-to-tip
triangle: **18 triangles per module**.

The apex is displaced in the flow direction by `lean * height`. Triangle vertices
are deliberately duplicated so adjacent faces do not share averaged normals.
This retains the hard-edged, folded-paper appearance instead of making the mesh
look smoothly rounded. No back cap or material thickness is added. Even at
`fold = 0`, the shoulder and triangular facets remain.

### E. Colours sampled from the supplied artwork

The script embeds a 12 x 12 RGB sample map taken from the artwork region of the
supplied JPEG. During preparation, the image was normalized to 1538 x 1600 pixels;
sample centres span x = 190-1360 and y = 185-1410. Each sample uses a 55 x 55 pixel
patch, filters for warm saturated pixels, selects the 45th-80th luminance
percentiles, and takes channel medians to reduce the influence of deep shadows,
grey background, and bright highlights.

The embedded rows run **bottom to top**, so the low-Y portion of the model is red
and the high-Y portion is gold/yellow. Bilinear interpolation blends nearby map
samples when the grid resolution changes. The colouring stays attached to the
panel, independent of `rotation_deg` and `seed`.

These are photographic colour samples, not measured paper/material colours.
Some lighting remains in the samples, and Rhino's lighting will add its own
shading. The photo's cast shadows, texture, exposure, and exact appearance are not
recreated by the script.

## 5. Useful variations

| Look | Changes from the defaults |
|---|---|
| Reference-inspired starting point | Leave all defaults |
| Strong projecting spikes | `height_max = 110`, `lean = 1.1` |
| Shallower paper relief | `height_min = 8`, `height_max = 35`, `lean = 0.4` |
| Upright tips | `lean = 0` |
| Even-height folded field | `height_min = height_max = 55` |
| Change the direction of the sweep | Adjust `rotation_deg` |
| Change the winding | Change the sign and magnitude of `twist_deg` |
| Move the vortex | Adjust `flow_x` and `flow_y` |
| Separate the modules | `gap = 0.12` |
| Faster slider exploration | `cols = 12`, `rows = 12` |

Large height or lean values can create intersections; this is expected for a
visual model and is not collision-checked. For fabricated paper parts, a separate
design stage would be needed for developability, tabs, thickness, clearances,
unfolding, and assembly.

## 6. Troubleshooting

- **No geometry:** check exact parameter names, Script mode, Item Access, and
  whether unwired inputs are Optional. Connect `info` or `out` to a Panel.
- **All one colour:** connect `colours` to Custom Preview **M**, disable the
  Python/helper previews, and deselect the preview component.
- **Looks flat:** switch to an oblique shaded view; check height values and units.
- **Rotation seems subtle:** increase `lean`; upright tips cannot show a strong
  directional sweep, though the shoulders still respond to the direction field.
- **Height validation error:** ensure `0 < height_min <= height_max`.
- **Slow interaction:** lower the row and column counts while moving sliders.

The geometry must ultimately be previewed inside Rhino/Grasshopper; standalone
Python does not provide the RhinoCommon geometry runtime used by this script.
