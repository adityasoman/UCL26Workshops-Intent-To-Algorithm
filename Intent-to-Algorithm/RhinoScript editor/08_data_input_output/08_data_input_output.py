#! python3
# ^ This first line tells Rhino 8 to run this file with Python 3. Never delete it.

# LESSON 08: DATA INPUT / OUTPUT | Rhino 8 ScriptEditor (Python 3)
# READ FIRST: 08_data_input_output.md in this folder explains the concept, how to run,
#             exercises (Try this) and AI prompts (Ask the AI).


# --- IMPORTS ---------------------------------------------------
import os  # tools for file paths that work on Windows and Mac
import csv  # tools for reading and writing CSV (spreadsheet-style) files
import json  # tools for reading JSON (structured text) files
import rhinoscriptsyntax as rs  # Rhino's beginner-friendly toolbox


# --- SETTINGS (change these and run again) --------------------
LESSON_LAYER = "Lesson_08"  # the layer this lesson draws on
# The data folder is found automatically from where this .py file is saved:
#   Intent-to-Algorithm/RhinoScript editor/<lesson folder>/<this file>  →  up 2 folders  →  data/
try:  # __file__ is this script's own path; it only exists when the script is saved as a file
    LESSON_FOLDER = os.path.dirname(os.path.abspath(__file__))  # the folder this .py file is in
    DATA_FOLDER = os.path.normpath(os.path.join(LESSON_FOLDER, "..", "..", "data"))  # ".." = up one folder
except NameError:  # the script isn't saved as a file (e.g. pasted into a new, unsaved tab)
    DATA_FOLDER = ""  # nothing found: set it by hand on the line below
# CHANGE THIS only if your data files are somewhere else (remove the # and edit the path):
# DATA_FOLDER = r"C:\Users\you\Downloads\Intent-to-Algorithm\data"  # keep the r before the quotes
sunny_hours = 5.0  # DESIGN RULE: points with at least this many sun hours count as "sunny"


# --- STEP 0: Prepare a clean layer for this lesson ------------
if not rs.IsLayer(LESSON_LAYER):  # check whether the layer already exists
    rs.AddLayer(LESSON_LAYER)  # if it doesn't, create it
rs.CurrentLayer(LESSON_LAYER)  # make it the active layer


# --- STEP 1: Build file paths (see .md → Step 1) --------------
points_path = os.path.join(DATA_FOLDER, "site_points.csv")  # join folder + file name with the right slash
plots_path = os.path.join(DATA_FOLDER, "plots.json")  # the second input file
summary_path = os.path.join(DATA_FOLDER, "output_summary.csv")  # the file we will write
print("Reading from:", points_path)  # always print paths: most file errors are wrong paths


# --- STEP 2: Read a CSV safely with try / except (see .md → Step 2)
rows = []  # starts empty; stays empty if the file can't be read
try:  # TRY the indented lines; if one fails, jump to 'except' instead of crashing
    with open(points_path, newline="", encoding="utf-8") as f:  # open the file; 'with' closes it for us afterwards
        reader = csv.DictReader(f)  # reads each row as a dictionary, using the header row as keys
        for row in reader:  # one row at a time
            rows.append(row)  # keep it
except FileNotFoundError:  # only this kind of error is caught here
    print("Couldn't find the file. Is this lesson still inside the workshop folder? If not, set DATA_FOLDER (CHANGE THIS).")  # friendly message

print("rows read:", len(rows))  # 48 if everything worked


# --- STEP 3: Dictionaries and text → numbers (see .md → Step 3)
if len(rows) > 0:  # only if something was read
    first = rows[0]  # the first row is a DICTIONARY: values looked up by name
    print("first row:", first)  # e.g. {'id': 'P01', 'x': '5.0', 'y': '8.0', 'sun_hours': '2.1'}
    print("its sun hours:", first["sun_hours"], type(first["sun_hours"]))  # CSV gives TEXT, even for numbers
    print("as a number:", float(first["sun_hours"]) + 1)  # float() converts text to a decimal number


# --- STEP 4: Use the data: draw it (Producer → geometry) ------
summary = []  # rows for the output file
sunny_count = 0  # how many sunny points
for row in rows:  # every point in the file
    x = float(row["x"])  # text → number
    y = float(row["y"])  # text → number
    sun = float(row["sun_hours"])  # text → number
    rs.AddTextDot(f"{sun}h", [x, y, 0])  # show the sun hours on site
    if sun >= sunny_hours:  # apply a rule (lesson 05)
        category = "sunny"  # enough sun
        sunny_count = sunny_count + 1  # count it
    else:  # not enough sun
        category = "shaded"  # label it shaded
    summary.append([row["id"], x, y, sun, category])  # one output row: a list of values


# --- STEP 5: Read JSON (see .md → Step 5) ---------------------
try:  # same safety net as step 2
    with open(plots_path, encoding="utf-8") as f:  # open the JSON file
        plots = json.load(f)  # JSON becomes Python lists and dictionaries in one line
    print("plots in JSON:", len(plots))  # 25
    print("first plot:", plots[0]["id"], "is", plots[0]["use"], "with max", plots[0]["max_floors"], "floors")  # [0] then ["key"]
except FileNotFoundError:  # file missing
    print("plots.json not found in", DATA_FOLDER)  # friendly message


# --- STEP 6: Write a CSV (see .md → Step 6) -------------------
if len(summary) > 0:  # only write if we have results
    try:  # writing can fail too, e.g. if the file is open in Excel
        with open(summary_path, "w", newline="", encoding="utf-8") as f:  # "w" = write (replaces an old file)
            writer = csv.writer(f)  # a writer that turns lists into CSV lines
            writer.writerow(["id", "x", "y", "sun_hours", "category"])  # header row first
            writer.writerows(summary)  # then every data row at once
        print(f"Wrote {len(summary)} rows to {summary_path} ({sunny_count} sunny)")  # confirm
    except PermissionError:  # the file is locked (often: it's open in Excel)
        print("Couldn't write the file. Is output_summary.csv open in Excel? Close it and run again.")  # friendly message

rs.ZoomExtents()  # zoom to see the points
