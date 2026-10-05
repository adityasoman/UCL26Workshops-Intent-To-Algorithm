#! python3
# ^ This first line tells the Script component to use Python 3. Never delete it.

# LESSON 09: CAPSTONE: PRODUCER → OPERATOR → CONSUMER | Rhino 8 Grasshopper Script component (Python 3)
# READ FIRST: 09_capstone_producer_operator_consumer.md in this folder explains the design
#             intent, the full component setup, how to run, exercises and AI prompts.
# Example: density follows transport, from plots.json
#          (the Rhino version builds a sun-driven massing from site_points.csv instead).
#
# DESIGN INTENT (see .md → Design intent)
#   "Plots near the station get their full allowed height."   → operator(): remap distance → floors
#   "Density fades with distance, down to one storey."        → operator(): remap + clamp
#   "Parks, and plots too close to the park, stay open."      → operator(): use + distance filter
#   "Schools keep their own low height."                      → operator(): use rule
#   "Show the result as massing, coloured by use."            → consumer()
#   "The information comes from the plot schedule."           → producer(): read plots.json
#
# Inputs:  folder (str, Item), station (Point3d, Item), park (Point3d, Item),
#          park_radius (float, Item), reach (float, Item), floor_height (float, Item)
# Outputs: masses, colours, labels, centres, open_space, out


# --- IMPORTS ---------------------------------------------------
import os  # file paths (lesson 08)
import json  # reading JSON (lesson 08)
import Rhino.Geometry as rg  # RhinoCommon geometry (lesson 07)
import System.Drawing as sd  # .NET colours, which Grasshopper's Custom Preview understands


# --- SETTINGS: fixed rules (the rest are sliders) -------------
USE_COLOURS = {  # a dictionary: use name → colour (lesson 08)
    "housing": sd.Color.FromArgb(230, 160, 60),  # orange
    "office": sd.Color.FromArgb(70, 120, 200),  # blue
    "retail": sd.Color.FromArgb(200, 60, 80),  # red
    "school": sd.Color.FromArgb(150, 90, 190),  # purple
}


# --- PRODUCER: read information (see .md → Producer) ----------
def producer(folder):  # returns a list of plot dictionaries
    path = os.path.join(folder, "plots.json")  # build the path
    try:  # a missing file shouldn't crash the component
        with open(path, encoding="utf-8") as f:  # open and auto-close
            return json.load(f)  # list of dictionaries, numbers already numbers
    except FileNotFoundError:  # friendly warning instead of a red component
        ghenv.Component.AddRuntimeMessage(  # orange balloon (lesson 03)
            ghenv.Component.RuntimeMessageLevel.Warning,  # level: Warning
            "plots.json not found. Check the 'folder' input.")  # the text in the balloon
        return []  # nothing to work with


# --- OPERATOR: apply the rules (see .md → Operator) -----------
def remap(value, old_min, old_max, new_min, new_max):  # stretch a number from one range to another
    if old_max == old_min:  # avoid dividing by zero
        return new_min  # nothing to stretch
    t = (value - old_min) / (old_max - old_min)  # position in the old range: 0.0 … 1.0
    t = max(0.0, min(1.0, t))  # CLAMP: anything beyond the range is held at its end
    return new_min + t * (new_max - new_min)  # same position in the new range


def operator(plots):  # decides what happens on each plot; returns two lists
    built = []  # plots that get a building, with a number of floors
    open_plots = []  # plots that stay open
    for p in plots:  # apply the rules to every plot
        centre = rg.Point3d(p["x"], p["y"], 0)  # the plot's centre as a point
        to_park = centre.DistanceTo(park)  # RhinoCommon points can measure distances themselves
        to_station = centre.DistanceTo(station)  # distance to the transport stop
        if p["use"] == "park" or to_park < park_radius:  # RULE 1: parks, and plots too close to the park
            open_plots.append(p)  # → open space
        elif p["use"] == "school":  # RULE 2: schools keep their own height
            p["floors"] = p["max_floors"]  # unchanged
            built.append(p)  # → built
        else:  # RULE 3: density follows transport
            f = remap(to_station, 0, reach, p["max_floors"], 1)  # near → max_floors, at 'reach' or beyond → 1
            p["floors"] = int(round(f))  # whole storeys only
            built.append(p)  # → built
    return built, open_plots  # two results at once (lesson 04)


# --- CONSUMER: geometry and colour (see .md → Consumer) -------
def consumer(built, open_plots):  # returns lists for the outputs
    boxes, cols, texts, points, opens = [], [], [], [], []  # five empty lists in one line
    for p in built:  # one mass per built plot
        h = p["floors"] * floor_height  # height in metres
        xs = rg.Interval(p["x"] - p["width"] / 2, p["x"] + p["width"] / 2)  # x range from centre and width
        ys = rg.Interval(p["y"] - p["depth"] / 2, p["y"] + p["depth"] / 2)  # y range from centre and depth
        boxes.append(rg.Box(rg.Plane.WorldXY, xs, ys, rg.Interval(0, h)))  # the mass (lesson 07)
        cols.append(USE_COLOURS.get(p["use"], sd.Color.Gray))  # colour by use; grey if the use is unknown
        texts.append(f"{p['id']} {p['use']} {p['floors']}/{p['max_floors']}fl")  # e.g. "PL03 office 9/12fl"
        points.append(rg.Point3d(p["x"], p["y"], h))  # label on the roof
    for p in open_plots:  # outline each open plot
        corner = rg.Point3d(p["x"] - p["width"] / 2, p["y"] - p["depth"] / 2, 0)  # its corner
        opens.append(rg.Rectangle3d(rg.Plane(corner, rg.Vector3d.ZAxis), p["width"], p["depth"]))  # its outline
    return boxes, cols, texts, points, opens  # everything the outputs need


# --- MAIN: run the system in order (see .md → Main) -----------
plots = producer(folder)  # 1. PRODUCER: information in
built, open_plots = operator(plots)  # 2. OPERATOR: rules applied
masses, colours, labels, centres, open_space = consumer(built, open_plots)  # 3. CONSUMER: geometry out

total_floors = 0  # running total
for p in built:  # add up every built plot's floors
    total_floors = total_floors + p["floors"]  # one plot at a time
print(f"{len(plots)} plots → {len(built)} built ({total_floors} storeys in total), {len(open_plots)} open")  # summary
