# Lesson 08 · Data input and output

**Environment:** Rhino 8 ScriptEditor (Python 3) · **Code:** [`08_data_input_output.py`](08_data_input_output.py) · **Role:** Producer

## What is this concept?

So far every number has been typed into the script. Real projects start from **data**: survey points, sun studies, plot schedules, sensor readings. This lesson reads data from files, and writes results back out.

| Idea | What it is | In this lesson |
|---|---|---|
| **file path** | the address of a file on your computer | `os.path.join(DATA_FOLDER, "site_points.csv")` |
| `with open(...)` | open a file and close it automatically afterwards | reading and writing |
| **CSV** | a table as plain text, one row per line, values separated by commas | `site_points.csv` |
| **JSON** | structured text: lists `[...]` and dictionaries `{...}` | `plots.json` |
| **dictionary** | values looked up by **name** instead of by position | `row["sun_hours"]` |
| `try / except` | "try this; if it fails in this specific way, do that instead" | a friendly message if a file is missing |

A **dictionary** is like a labelled form: `{"id": "P01", "x": "5.0", "sun_hours": "2.1"}`. You read a value with its label: `row["sun_hours"]`. Compare a list, where you'd need to remember that sun hours is item `[3]`.

## Why does it matter for design?

Data lets your design respond to the real site instead of invented numbers. Writing results out lets you share them with consultants, check them in Excel, or feed them into the next tool. This is the **Producer** stage of a real system.

## Where this sits in Producer → Operator → Consumer

| Role | Meaning |
|---|---|
| **Producer** | reads or creates information |
| Operator | applies rules to that information |
| Consumer | turns the result into geometry or colour |

This lesson is mainly a **Producer**: it brings outside information into the script.

## How to run

1. Open `08_data_input_output.py` **from the workshop folder** in the ScriptEditor (command: `ScriptEditor` → File → Open) and press **Run** (F5). The script finds the `data` folder by itself, because it's always two folders up from the lesson file.
2. **Only if you moved the lesson file** somewhere else: find the line marked `# CHANGE THIS`, remove the `#` at its start, and type the path to the `data` folder. For example:
   - Windows: `DATA_FOLDER = r"C:\Users\you\Downloads\Intent-to-Algorithm\data"` (keep the `r` before the quotes)
   - Mac: `DATA_FOLDER = "/Users/you/Downloads/Intent-to-Algorithm/data"`
3. You should see 48 labelled points on layer `Lesson_08`, the rows and plots counts in the Console, and a new file `output_summary.csv` in the data folder.

If the path is wrong, the Console says so politely instead of crashing. Fix the path and run again.

## Step by step

### Settings · Finding the data folder
`__file__` is a special variable holding the full path of the script that's running. `os.path.dirname` takes the folder part, and `".."` means "up one folder". So `lesson folder → .. → .. → data` lands in `Intent-to-Algorithm/data`, wherever the workshop is on your computer. `os.path.normpath` tidies the `..` parts away.

If the script isn't saved as a file (for example, you pasted it into a new tab), `__file__` doesn't exist and Python raises a `NameError`. The `try / except NameError` catches that, and you set the path by hand instead. This is your first `try / except`; Step 2 explains it properly.

### Step 1 · File paths
`os.path.join` glues folder and file names together with the right slash for your computer (`\` on Windows, `/` on Mac). Always `print` the path you're using: most file problems are just a wrong path.

### Step 2 · Reading a CSV safely
- `with open(path) as f:` opens the file and **closes it automatically** when the indented block ends.
- `csv.DictReader` reads each row as a dictionary, using the header line (`id,x,y,sun_hours`) as the keys.
- `try / except FileNotFoundError` catches **only** a missing file. Any other error still shows normally, which is what you want, so real bugs aren't hidden.

### Step 3 · Dictionaries, and text vs numbers
Everything read from a CSV is **text**, even `"2.1"`. `"2.1" + 1` is a `TypeError`; `float("2.1") + 1` is `3.1`. Converting is the most common step when reading data.

### Step 4 · Using the data
Each row becomes a point with a label, plus one rule (lesson 05) to decide sunny or shaded. We build a list of results for the output file at the same time.

### Step 5 · Reading JSON
`json.load` turns a whole JSON file into Python lists and dictionaries in one line. `plots[0]["use"]` means "the first plot, its use".

### Step 6 · Writing a CSV
- `"w"` means **write**: it creates the file, or **replaces** it if it already exists.
- `writer.writerow` writes one row; `writer.writerows` writes many.
- If the file is open in Excel, Windows locks it and you get a `PermissionError`. We catch that too.

## Try this

1. Change `sunny_hours` to `7.0` and run. Open `output_summary.csv` in Excel: how many points are sunny now?
2. Break the path on purpose: un-comment the `CHANGE THIS` line, leave it pointing to `C:\Users\you\...`, and run. Read the message, then fix it.
3. Open `output_summary.csv` in Excel, keep it open, and run again. What happens?
4. Print every plot in `plots.json` whose `"use"` is `"housing"`.

## Ask the AI

Paste one of these into any AI chat tool. See [`Prompt guidelines`](../../Prompt%20guidelines/README.md) for more.

```text
I'm learning Python in the Rhino 8 ScriptEditor (Python 3).
Explain the difference between a list and a dictionary using a row
from this CSV as the example: id,x,y,sun_hours / P01,5.0,8.0,2.1
```

```text
I have a CSV of site points with columns id,x,y,sun_hours. Write a
Rhino 8 Python 3 script that reads it with csv.DictReader and colours
each point from blue (least sun) to yellow (most sun). Standard library
and rhinoscriptsyntax only, comment every line, handle a missing file.
```

```text
What else could go wrong when reading a CSV that a student made in
Excel? (e.g. extra spaces, empty rows, commas in numbers). For each
problem, show how to guard against it.
```
