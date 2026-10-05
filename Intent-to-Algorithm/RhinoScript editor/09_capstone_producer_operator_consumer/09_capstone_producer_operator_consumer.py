#! python3
# ^ This first line tells Rhino 8 to run this file with Python 3. Never delete it.

# LESSON 09: CAPSTONE: PRODUCER → OPERATOR → CONSUMER | Rhino 8 ScriptEditor (Python 3)
# READ FIRST: 09_capstone_producer_operator_consumer.md in this folder explains the
#             design intent, how to run, exercises (Try this) and AI prompts (Ask the AI).
#
# DESIGN INTENT (see .md → Design intent)
#   "Spots with more sun get taller buildings."            → operator(): remap sun → height
#   "Spots too close to the park stay open space."         → operator(): distance filter
#   "Spots with too little sun aren't built on."           → operator(): sun filter
#   "Show the result as massing, coloured by height."      → consumer()
#   "The information comes from a sun study."              → producer(): read site_points.csv


# --- IMPORTS ---------------------------------------------------
import os  # file paths (lesson 08)
import csv  # reading CSV files (lesson 08)
import math  # square root for distances (lesson 02)
import rhinoscriptsyntax as rs  # layers, colours and labels (lessons 01–06)
import Rhino.Geometry as rg  # RhinoCommon geometry (lesson 07)
import scriptcontext as sc  # the Rhino document (lesson 07)


# --- SETTINGS: the design rules live here (change and run again)
LESSON_LAYER = "Lesson_09"  # the layer this lesson draws on
# CHANGE THIS: the folder on YOUR computer that holds site_points.csv
DATA_FOLDER = os.path.join(os.path.expanduser("~"), "Documents", "Intent-to-Algorithm", "data")  # see lesson 08
park = [50.0, 50.0]  # park centre (x, y)
park_radius = 20.0  # RULE: closer than this to the park → open space
min_sun = 3.5  # RULE: fewer sun hours than this → not built on
min_height = 6.0  # height given to the least sunny buildable spot, metres
max_height = 60.0  # height given to the sunniest spot, metres
footprint = 8.0  # every building is footprint × footprint metres


# --- PRODUCER: read or create information (see .md → Producer)
def producer(folder):  # returns a list of dictionaries with NUMBERS, not text
    path = os.path.join(folder, "site_points.csv")  # build the path
    spots = []  # one dictionary per site point
    try:  # a missing file shouldn't crash the script
        with open(path, newline="", encoding="utf-8") as f:  # open and auto-close
            for row in csv.DictReader(f):  # each row as a dictionary of text
                spots.append({  # convert the text to numbers once, here, so nobody else has to
                    "id": row["id"],  # the name stays text
                    "x": float(row["x"]),  # text → number
                    "y": float(row["y"]),  # text → number
                    "sun": float(row["sun_hours"]),  # text → number
                })
    except FileNotFoundError:  # friendly message instead of a crash
        print("Couldn't find", path, "— check DATA_FOLDER (CHANGE THIS).")  # tell the user what to fix
    return spots  # hand the information on


# --- OPERATOR: apply the rules (see .md → Operator) -----------
def remap(value, old_min, old_max, new_min, new_max):  # stretch a number from one range to another
    if old_max == old_min:  # avoid dividing by zero if every value is the same
        return new_min  # nothing to stretch
    t = (value - old_min) / (old_max - old_min)  # where the value sits in the old range: 0.0 … 1.0
    return new_min + t * (new_max - new_min)  # the same position in the new range


def operator(spots):  # decides what happens on each spot; returns two lists
    buildings = []  # spots that get a building, with a height
    open_spaces = []  # spots that stay open
    suns = []  # sun hours of every buildable spot, to find the range
    for s in spots:  # first pass: collect
        if s["sun"] >= min_sun:  # only spots that pass the sun rule
            suns.append(s["sun"])  # keep its sun hours
    lowest = min(suns) if suns else 0  # least sun among buildable spots (0 if the list is empty)
    highest = max(suns) if suns else 0  # most sun among buildable spots
    for s in spots:  # apply the rules to every spot
        d = math.sqrt((s["x"] - park[0]) ** 2 + (s["y"] - park[1]) ** 2)  # distance to the park
        if d < park_radius:  # RULE 1: too close to the park
            open_spaces.append(s)  # → open space
        elif s["sun"] < min_sun:  # RULE 2: too little sun
            open_spaces.append(s)  # → not built on
        else:  # RULE 3: buildable → height follows sun
            s["height"] = remap(s["sun"], lowest, highest, min_height, max_height)  # add a new key to the dictionary
            buildings.append(s)  # → gets a building
    return buildings, open_spaces  # two results at once (lesson 04)


# --- CONSUMER: turn the result into geometry and colour (see .md → Consumer)
def height_colour(h):  # blue for low, red for tall
    t = remap(h, min_height, max_height, 0.0, 1.0)  # 0.0 … 1.0
    return (int(255 * t), 80, int(255 * (1 - t)))  # (red, green, blue): more red as t grows


def consumer(buildings, open_spaces):  # draws everything; returns nothing
    for b in buildings:  # one box per building
        half = footprint / 2  # boxes are centred on the spot
        box = rg.Box(rg.Plane.WorldXY,  # a box from three ranges (lesson 07)
                     rg.Interval(b["x"] - half, b["x"] + half),  # x range
                     rg.Interval(b["y"] - half, b["y"] + half),  # y range
                     rg.Interval(0, b["height"]))  # z range: ground to roof
        box_id = sc.doc.Objects.AddBox(box)  # add it to Rhino; returns its ID
        rs.ObjectColor(box_id, height_colour(b["height"]))  # colour it by height (lesson 05)
    for s in open_spaces:  # mark the open spots
        dot = rs.AddPoint([s["x"], s["y"], 0])  # a point on the ground
        rs.ObjectColor(dot, (60, 170, 60))  # green
    circle = rs.AddCircle([park[0], park[1], 0], park_radius)  # show the park rule as a circle
    rs.ObjectColor(circle, (60, 170, 60))  # green
    sc.doc.Views.Redraw()  # refresh the viewport (lesson 07)


# --- MAIN: run the system in order (see .md → Main) -----------
if not rs.IsLayer(LESSON_LAYER):  # prepare the lesson layer
    rs.AddLayer(LESSON_LAYER)  # create it if needed
rs.CurrentLayer(LESSON_LAYER)  # make it active

spots = producer(DATA_FOLDER)  # 1. PRODUCER: information in
buildings, open_spaces = operator(spots)  # 2. OPERATOR: rules applied
consumer(buildings, open_spaces)  # 3. CONSUMER: geometry out

print(f"{len(spots)} spots → {len(buildings)} buildings, {len(open_spaces)} open")  # summary
if buildings:  # only if anything was built
    tallest = buildings[0]  # start by assuming the first building is the tallest…
    for b in buildings:  # …then check every building
        if b["height"] > tallest["height"]:  # taller than the tallest so far?
            tallest = b  # it's the new tallest
    print(f"Tallest: {tallest['id']} at {tallest['height']:.1f} m with {tallest['sun']} h of sun")  # report it
rs.ZoomExtents()  # zoom to see the result
