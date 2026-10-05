# Sample site data

Small, made-up data for lessons 08 and 09. Both files describe the same **100 m × 100 m site** (x and y from 0 to 100 m) as the lesson 06 grid, so results line up in the viewport. Both are plain UTF-8 text. They open in Excel, VS Code or Notepad.

## `site_points.csv`

48 sample points across the site with the hours of direct sun each one gets. Sun increases from the south-west corner (shaded) to the north-east corner (open).

| Column | Type | Unit | Meaning |
|--------|------|------|---------|
| `id` | text | — | point name, `P01` … `P48` |
| `x` | number | metres | east–west position |
| `y` | number | metres | north–south position |
| `sun_hours` | number | hours/day | average hours of direct sun |

Used by: RhinoScript editor lessons 08 and 09.

## `plots.json`

25 plots in a 5 × 5 grid (20 m apart, centres from 10 m to 90 m). Each plot is a **dictionary** of named values.

| Field | Type | Unit | Meaning |
|-------|------|------|---------|
| `id` | text | — | plot name, `PL01` … `PL25` |
| `x`, `y` | number | metres | centre of the plot |
| `width`, `depth` | number | metres | plot size along x and y |
| `use` | text | — | `housing`, `office`, `retail`, `school` or `park` |
| `max_floors` | whole number | storeys | planning limit (0 for parks) |

Used by: Grasshopper lessons 08 and 09 (and briefly by RhinoScript editor lesson 08).

## Output files

Lessons 08 and 09 write their results here, e.g. `output_summary.csv` and `plots_summary.csv`. You can delete these at any time; running the lesson creates them again.
