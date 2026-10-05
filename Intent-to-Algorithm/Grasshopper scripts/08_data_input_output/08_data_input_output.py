#! python3
# ^ This first line tells the Script component to use Python 3. Never delete it.

# LESSON 08: DATA INPUT / OUTPUT | Rhino 8 Grasshopper Script component (Python 3)
# READ FIRST: 08_data_input_output.md in this folder explains the concept, the full component
#             setup, how to run, exercises (Try this) and AI prompts (Ask the AI).
# Example: a plot schedule from plots.json → massing, plus a CSV area schedule
#          (the Rhino version reads sun hours from site_points.csv instead).
# Inputs:  folder (str, Item), floor_height (float, Item), write (bool, Item)
# Outputs: outlines, masses, labels, centres, out


# --- IMPORTS ---------------------------------------------------
import os  # tools for file paths that work on Windows and Mac
import csv  # tools for writing CSV (spreadsheet-style) files
import json  # tools for reading JSON (structured text) files
import Rhino.Geometry as rg  # RhinoCommon geometry (lesson 07)


# --- STEP 1: Build file paths (see .md → Step 1) --------------
plots_path = os.path.join(folder, "plots.json")  # join the 'folder' input + file name with the right slash
schedule_path = os.path.join(folder, "plots_summary.csv")  # the file we may write
print("Reading from:", plots_path)  # always print paths: most file errors are wrong paths


# --- STEP 2: Read JSON safely with try / except (see .md → Step 2)
plots = []  # starts empty; stays empty if the file can't be read
try:  # TRY the indented lines; if one fails, jump to 'except' instead of crashing
    with open(plots_path, encoding="utf-8") as f:  # open the file; 'with' closes it for us afterwards
        plots = json.load(f)  # JSON becomes Python lists and dictionaries in one line
except FileNotFoundError:  # only this kind of error is caught here
    ghenv.Component.AddRuntimeMessage(  # turn the component orange with a message (lesson 03)
        ghenv.Component.RuntimeMessageLevel.Warning,  # level: Warning
        "plots.json not found. Check the 'folder' input.")  # the text in the balloon

print("plots read:", len(plots))  # 25 if everything worked


# --- STEP 3: Dictionaries (see .md → Step 3) ------------------
if len(plots) > 0:  # only if something was read
    first = plots[0]  # one plot is a DICTIONARY: values looked up by name
    print("first plot:", first)  # e.g. {'id': 'PL01', 'x': 10, 'y': 10, ... 'use': 'housing', 'max_floors': 6}
    print("its use:", first["use"])  # read one value by its key (name)
    print("keys:", list(first.keys()))  # every name this dictionary holds


# --- STEP 4: Turn each record into geometry -------------------
plot_outlines = []  # plot boundaries
plot_masses = []  # maximum building envelope per plot
plot_labels = []  # text for a Text Tag
plot_centres = []  # where to put each label
schedule = []  # rows for the output file
for p in plots:  # every plot in the file
    corner = rg.Point3d(p["x"] - p["width"] / 2, p["y"] - p["depth"] / 2, 0)  # x, y are centres; go back half a size
    plane = rg.Plane(corner, rg.Vector3d.ZAxis)  # a flat plane at that corner
    outline = rg.Rectangle3d(plane, p["width"], p["depth"])  # the plot boundary
    plot_outlines.append(outline)  # keep it
    height = p["max_floors"] * floor_height  # JSON numbers are already numbers: no float() needed
    gfa = p["width"] * p["depth"] * p["max_floors"]  # maximum gross floor area, m²
    if height > 0:  # parks have 0 floors: no mass to build (lesson 05)
        xs = rg.Interval(corner.X, corner.X + p["width"])  # extent along x
        ys = rg.Interval(corner.Y, corner.Y + p["depth"])  # extent along y
        plot_masses.append(rg.Box(rg.Plane.WorldXY, xs, ys, rg.Interval(0, height)))  # the envelope
    plot_labels.append(f"{p['id']} {p['use']} {p['max_floors']}fl")  # e.g. "PL01 housing 6fl"
    plot_centres.append(rg.Point3d(p["x"], p["y"], height))  # label sits on the roof
    schedule.append([p["id"], p["use"], p["max_floors"], round(height, 1), gfa])  # one output row


# --- STEP 5: Write a CSV only when asked (see .md → Step 5) ---
# Grasshopper re-runs this script every time ANY input changes. Without the 'write'
# toggle, every slider move would rewrite the file on disk.
if write and len(schedule) > 0:  # only when the Boolean Toggle is True AND we have data
    try:  # writing can fail, e.g. if the file is open in Excel
        with open(schedule_path, "w", newline="", encoding="utf-8") as f:  # "w" = write (replaces an old file)
            writer = csv.writer(f)  # a writer that turns lists into CSV lines
            writer.writerow(["id", "use", "max_floors", "height_m", "max_gfa_m2"])  # header row first
            writer.writerows(schedule)  # then every data row at once
        print(f"Wrote {len(schedule)} rows to {schedule_path}")  # confirm
    except PermissionError:  # the file is locked (often: it's open in Excel)
        ghenv.Component.AddRuntimeMessage(  # warn on the component
            ghenv.Component.RuntimeMessageLevel.Warning,  # level: Warning
            "Couldn't write plots_summary.csv. Is it open in Excel?")  # the text in the balloon
else:  # write is False
    print("write is off: no file written")  # remind the user how to save


# --- OUTPUTS: send results out of the component ---------------
outlines = plot_outlines  # plot boundaries
masses = plot_masses  # building envelopes
labels = plot_labels  # text for each plot
centres = plot_centres  # label positions
