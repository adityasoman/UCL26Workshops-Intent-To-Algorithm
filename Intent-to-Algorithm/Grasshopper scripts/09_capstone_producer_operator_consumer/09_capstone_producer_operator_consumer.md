# Lesson 09 · Capstone: Producer → Operator → Consumer

**Environment:** Rhino 8 Grasshopper, Script component (Python 3) · **Code:** [`09_capstone_producer_operator_consumer.py`](09_capstone_producer_operator_consumer.py) · **Role:** all three

> **Different example from the Rhino version.** The RhinoScript editor capstone builds a **sun-driven massing** from `site_points.csv`. This one builds a **transport-driven density model** from the plot schedule in `plots.json`. The concept is the same, so you get two complete systems to compare.

## What is this concept?

Nothing new. This lesson **combines everything** from lessons 01–08 into one small computational design system, split into the workshop's three roles:

| Role | Function | What it does here | Lessons used |
|---|---|---|---|
| **Producer** | `producer()` | reads the plot schedule from `plots.json` | 08 files, dictionaries |
| **Operator** | `operator()` | keeps parks open, keeps schools low, and sets each plot's floors from its distance to the station | 04 functions, 05 rules, 06 loops |
| **Consumer** | `consumer()` | builds a mass per plot, coloured by use, with labels and open-space outlines | 07 RhinoCommon |

A short **main** section at the bottom calls them in order. Each function only does its own job, and hands its result to the next.

## Design intent

> *"Density follows transport. Plots near the station get their full allowed height, fading to one storey further away. Parks, and plots too close to the park, stay open. Schools keep their own low height. Show the result as massing, coloured by use."*

Each sentence becomes code:

| Sentence | Where | Code |
|---|---|---|
| "parks and plots near the park stay open" | `operator()` rule 1 | `if p["use"] == "park" or to_park < park_radius:` |
| "schools keep their own height" | `operator()` rule 2 | `elif p["use"] == "school":` |
| "near the station → full height, fading to 1 storey" | `operator()` rule 3 | `remap(to_station, 0, reach, p["max_floors"], 1)` |
| "massing, coloured by use" | `consumer()` | `rg.Box` + `USE_COLOURS` |
| "from the plot schedule" | `producer()` | `json.load` |

**The design rules are sliders.** Drag the station point or a slider and the whole system re-runs, so you can explore the design space live.

## Why does it matter for design?

This is the whole point of the workshop: a vague intent ("density near transport, respect the park") becomes **explicit rules** that you can test, question and change. Splitting the system into Producer / Operator / Consumer means you can swap one part without breaking the others: a different data file, a different rule set, or a different way of drawing the result.

## Component setup

Zoom in on the component and use **⊕ / ⊖** to add or remove parameters. Right-click each one to rename it, set its **Type hint**, and set **Item** or **List Access**.

**Inputs**

| Name | Type hint | Access | Connect to |
|---|---|---|---|
| `folder` | `str` | Item Access | Panel with the full path to this workshop's `data` folder (as in lesson 08) |
| `station` | `Point3d` | Item Access | **Point** parameter → right-click → *Set one Point* → click at about (85, 15) in Rhino |
| `park` | `Point3d` | Item Access | **Point** parameter → *Set one Point* → click at about (40, 50) |
| `park_radius` | `float` | Item Access | Number Slider, 0–50, default 25 |
| `reach` | `float` | Item Access | Number Slider, 10–150, default 80 |
| `floor_height` | `float` | Item Access | Number Slider, 2.8–4.5, default 3.2 |

**Outputs**

| Name | Type | Notes |
|---|---|---|
| `masses` | list of Box | one mass per built plot |
| `colours` | list of Colour | one colour per mass, same order |
| `labels` | list of str | e.g. `PL03 office 9/12fl` (floors built / allowed) |
| `centres` | list of Point3d | connect to a **Text Tag** with `labels` |
| `open_space` | list of Rectangle3d | outlines of plots left open |
| `out` | built-in | `print()` messages; connect a Panel |

**To see the colours:** add a **Custom Preview** component (Display tab). Connect `masses` → **G** (geometry) and `colours` → **M** (material). Then right-click the Script component and turn **Preview** off, so you only see the coloured version.

## How to run

1. Place a **Python 3 Script** component (Maths tab → Script panel).
2. Set up the inputs, outputs and Custom Preview exactly as listed above.
3. Double-click the component, paste the whole `.py` file, then **Run**.
4. You should see coloured masses that are tallest near the station and lower further away, with outlines where plots stay open. Drag the station point (right-click → *Set one Point* again) and the city reshapes itself.

## Step by step

### Producer
Reads the JSON and returns a list of plot dictionaries. If the file is missing, it shows an orange warning and returns an empty list, so the rest of the system simply builds nothing.

### Operator
- `remap()` stretches a value from one range (0 → `reach` metres) to another (`max_floors` → 1 storey). Note the order: **near gives more**, so the new range runs from high to low.
- **Clamping** (`max(0.0, min(1.0, t))`) holds anything beyond `reach` at 1 storey instead of going below it.
- `centre.DistanceTo(station)` is RhinoCommon measuring the distance for us (lesson 07).
- Rules are checked in order, like lesson 05. A housing plot inside `park_radius` stays open, because rule 1 is checked first.
- `p["floors"] = ...` adds a new key to that plot's dictionary.

### Consumer
Builds the masses, picks each colour from the `USE_COLOURS` dictionary (`.get(key, default)` gives grey for an unknown use instead of an error), and makes labels and outlines. `System.Drawing` colours are what Grasshopper's Custom Preview expects.

### Main
Three lines run the whole system: information in → rules → geometry out. Reading these three lines tells you what the script does.

## Try this

1. Set `park_radius` to 0. Which plots still stay open, and why?
2. Shrink `reach` to 20. What kind of city does that make?
3. Add a rule: `retail` plots are never taller than 3 floors. Where in `operator()` does it go?
4. Add a second input, `station_2` (Point3d), and use whichever station is closer. (Hint: `min(a, b)` returns the smaller of two numbers.)

## Ask the AI

Paste one of these into any AI chat tool. See [`Prompt guidelines`](../../Prompt%20guidelines/README.md) for more.

```text
Here is my design system: <paste the DESIGN INTENT block and the
operator() function>. Propose three alternative Operator rule sets that
use the same plot data (x, y, use, max_floors) but express different
design intents. For each, give the intent in one sentence and the rules
in plain English. No code yet.
```

```text
Implement option <n> from your last answer as a new operator() function
that returns (built, open_plots) exactly like mine, so producer() and
consumer() don't need to change. Rhino 8 Grasshopper Script component,
Python 3, Rhino.Geometry only, comment every line, and list any new
inputs with type hint and access.
```

```text
Review my capstone script as a tutor would: is each function doing only
its own job (Producer / Operator / Consumer)? Point out anything in the
wrong place, and any rule that could give a surprising result at the edges.
```
