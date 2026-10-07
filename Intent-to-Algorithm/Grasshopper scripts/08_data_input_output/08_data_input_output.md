# Lesson 08 · Data input and output

**Environment:** Rhino 8 Grasshopper, Script component (Python 3) · **Code:** [`08_data_input_output.py`](08_data_input_output.py) · **Role:** Producer

> **Different example from the Rhino version.** The RhinoScript editor lesson reads **sun hours from `site_points.csv`**. This one reads a **plot schedule from `plots.json`**, builds the maximum massing for each plot, and writes an **area schedule** CSV. The concept is the same, so you get two examples to compare.

## What is this concept?

So far every number has come from a slider or been typed into the script. Real projects start from **data**: plot schedules, survey points, sun studies. This lesson reads data from a file, and writes results back out.

| Idea | What it is | In this lesson |
|---|---|---|
| **file path** | the address of a file on your computer | `os.path.join(folder, "plots.json")` |
| `with open(...)` | open a file and close it automatically afterwards | reading and writing |
| **JSON** | structured text: lists `[...]` and dictionaries `{...}` | `plots.json` |
| **CSV** | a table as plain text, one row per line, values separated by commas | `plots_summary.csv` |
| **dictionary** | values looked up by **name** instead of by position | `p["max_floors"]` |
| `try / except` | "try this; if it fails in this specific way, do that instead" | a warning if a file is missing |

A **dictionary** is like a labelled form: `{"id": "PL01", "use": "housing", "max_floors": 6}`. You read a value with its label: `p["use"]`. Compare a list, where you'd need to remember that use is item `[5]`.

## Why does it matter for design?

Data lets your design respond to the real brief instead of invented numbers. Here, a planning schedule (use and maximum floors per plot) instantly becomes a massing model, and an area schedule you can check in Excel.

## Component setup

Zoom in on the component and use **⊕ / ⊖** to add or remove parameters. Right-click each one to rename it, set its **Type hint**, and set **Item** or **List Access**.

**Inputs**

| Name | Type hint | Access | Connect to |
|---|---|---|---|
| `folder` | `str` | Item Access | **Panel** holding the full path to this workshop's `data` folder, e.g. `C:\Users\you\Downloads\Intent-to-Algorithm\data`. (Alternative: a **File Path** parameter, right-click → *Select one existing file* → pick `plots.json`, then use its folder.) |
| `floor_height` | `float` | Item Access | Number Slider, 2.8–4.5, default 3.2 |
| `write` | `bool` | Item Access | **Boolean Toggle**, default False |

**Outputs**

| Name | Type | Notes |
|---|---|---|
| `outlines` | list of Rectangle3d | plot boundaries |
| `masses` | list of Box | maximum building envelope per plot (parks have none) |
| `labels` | list of str | e.g. `PL01 housing 6fl` |
| `centres` | list of Point3d | connect to a **Text Tag** with `labels` |
| `out` | built-in | `print()` messages; connect a Panel |

## How to run

1. Place a **Python 3 Script** component (Maths tab → Script panel).
2. Set up the inputs and outputs exactly as listed above. Type your own path into the `folder` Panel.
3. Double-click the component, paste the whole `.py` file, then **Run**.
4. You should see 25 plot outlines and a massing model with towers of different heights. Flip `write` to **True**: `plots_summary.csv` appears in the data folder. Flip it back to **False**.

If the path is wrong, the component turns orange with a message instead of crashing. Fix the path in the Panel.

## Step by step

### Step 1 · File paths
`os.path.join` glues folder and file names together with the right slash for your computer (`\` on Windows, `/` on Mac). Always `print` the path you're using: most file problems are just a wrong path.

### Step 2 · Reading JSON safely
- `with open(path) as f:` opens the file and **closes it automatically** when the indented block ends.
- `json.load` turns the whole file into a Python **list of dictionaries** in one line.
- `try / except FileNotFoundError` catches **only** a missing file, and turns it into an orange warning. Other errors still show normally, so real bugs aren't hidden.

### Step 3 · Dictionaries
`first["use"]` reads one value by its key. `first.keys()` lists all the keys. Unlike CSV, **JSON keeps numbers as numbers**, so `p["max_floors"] * floor_height` works without `float()`.

### Step 4 · Records → geometry
For every plot: an outline from its centre and size, a box as high as its maximum floors allow (skipped for parks, which have 0 floors), a label, and a row for the schedule.

### Step 5 · Writing only when asked
Grasshopper **re-runs the script every time any input changes**. Without a guard, every slider move would rewrite the file on disk, which is slow and can clash with Excel. The `write` toggle means the file is written only when you deliberately switch it on.

- `"w"` means **write**: it creates the file, or **replaces** it.
- If the file is open in Excel, Windows locks it and you get a `PermissionError`, which we catch.

## Try this

1. Change `floor_height` and watch the masses grow. Flip `write` on and open the CSV: did `height_m` update?
2. Break the path in the Panel and read the orange balloon. Then fix it.
3. Output only the `office` plots. (Hint: `if p["use"] == "office":` inside the loop.)
4. Open `plots.json` in a text editor, change one plot's `max_floors`, save it, and re-run the component (right-click → **Recompute**).

## Ask the AI

Paste one of these into any AI chat tool. See [`Prompt guidelines`](../../Prompt%20guidelines/README.md) for more.

```text
I'm learning Python in a Rhino 8 Grasshopper Script component (Python 3).
Explain what a dictionary is, using one plot from this JSON as the
example: {"id": "PL01", "x": 10, "y": 10, "use": "housing", "max_floors": 6}
```

```text
Why should a Grasshopper Python script only write files when a Boolean
Toggle is True? Explain for a beginner, and suggest another safe pattern.
```

```text
Change my script so each plot's mass is coloured by its 'use'. Add a
'colours' output for a Custom Preview component. Rhino 8, Python 3,
Rhino.Geometry and System.Drawing only, comment every line. <paste script>
```
