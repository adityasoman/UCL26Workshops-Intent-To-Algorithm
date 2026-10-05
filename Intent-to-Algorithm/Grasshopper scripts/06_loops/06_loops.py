#! python3
# ^ This first line tells the Script component to use Python 3. Never delete it.

# LESSON 06: LOOPS | Rhino 8 Grasshopper Script component (Python 3)
# READ FIRST: 06_loops.md in this folder explains the concept, the full component
#             setup, how to run, exercises (Try this) and AI prompts (Ask the AI).
# Example: a twisting tower, a façade panel grid and a staircase
#          (the Rhino version makes a site grid and a tower that grows to a height limit).
# Inputs:  floors (int, Item), twist (float, Item), columns (int, Item), rows (int, Item),
#          storey_height (float, Item), max_riser (float, Item)
# Outputs: slabs, panels, steps, info, out


# --- IMPORTS ---------------------------------------------------
import math  # maths toolbox, for converting degrees to radians (lesson 02)
import Rhino.Geometry as rg  # Rhino's geometry toolbox, nicknamed 'rg' (lesson 02)


# --- SETTINGS (fixed in the code; the rest come from sliders) --
floor_height = 3.5  # height of each floor of the twisting tower, metres
plate = 20.0  # tower floor plate size, metres (square)
panel_w = 1.5  # façade panel width, metres
panel_h = 3.0  # façade panel height, metres
wall_y = -30.0  # the façade wall stands at this y, in front of the tower
stair_x = 40.0  # the staircase starts at this x, beside the tower
tread = 0.28  # depth of each step, metres


# --- STEP 1: for + range: repeat a set number of times (see .md → Step 1)
twisting_slabs = []  # an empty list; we'll append one floor per pass
for level in range(floors):  # level counts 0, 1, 2… up to floors - 1
    z = level * floor_height  # this floor's height above ground
    centre = rg.Point3d(0, 0, z)  # the centre of this floor
    plane = rg.Plane(centre, rg.Vector3d.ZAxis)  # a flat plane at that height
    angle = math.radians(level * twist)  # each floor turns 'twist' degrees more than the one below
    plane.Rotate(angle, rg.Vector3d.ZAxis)  # turn the plane around the vertical axis
    half = plate / 2  # half the plate size, so the square is centred
    slab = rg.Rectangle3d(plane, rg.Interval(-half, half), rg.Interval(-half, half))  # a centred square
    twisting_slabs.append(slab)  # add it to the list
print("tower floors made:", len(twisting_slabs))  # len() counts the items


# --- STEP 2: for over a list: repeat once per item ------------
for slab in twisting_slabs:  # 'slab' becomes each floor in the list, in turn
    print("floor at", round(slab.Center.Z, 1), "m")  # .Center is the middle point of the rectangle; .Z its height


# --- STEP 3: Nested loops make a panel grid (see .md → Step 3)
facade_panels = []  # an empty list for every panel
for col in range(columns):  # OUTER loop: one pass per column
    for row in range(rows):  # INNER loop: runs fully for EACH column, one pass per row
        x = col * panel_w  # column number × panel width = x position
        z = row * panel_h  # row number × panel height = z position
        wall = rg.Plane(rg.Point3d(x, wall_y, z), rg.Vector3d.XAxis, rg.Vector3d.ZAxis)  # an upright plane on the wall
        panel = rg.Rectangle3d(wall, panel_w * 0.9, panel_h * 0.9)  # 90% size leaves a joint between panels
        facade_panels.append(panel)  # add it to the list
print("façade panels:", len(facade_panels), "=", columns, "×", rows)  # columns × rows


# --- STEP 4: while: repeat until a condition is met (see .md → Step 4)
# ⚠️ A while loop runs until its condition becomes False. If it never does, Grasshopper
#    (and Rhino) FREEZE. Something inside the loop must move towards the stop, and a
#    hard cap (MAX_STEPS) is a safety net.
MAX_STEPS = 100  # safety net: never make more than this many steps
riser_count = 1  # start with the fewest possible risers: one giant step
while storey_height / riser_count > max_riser and riser_count < MAX_STEPS:  # too steep?
    riser_count = riser_count + 1  # MOVE TOWARDS THE STOP: one more riser makes each one lower
riser = storey_height / riser_count  # the final riser height, now at or under max_riser
print(f"{riser_count} risers of {round(riser * 1000)} mm to climb {storey_height} m")  # e.g. 18 risers of 172 mm


# --- STEP 5: use the result of the while loop in a for loop ---
stair_steps = []  # an empty list for the steps
for n in range(riser_count):  # now we know how many: one pass per step
    x0 = stair_x + n * tread  # each step starts one tread further along
    z_top = (n + 1) * riser  # and is one riser higher
    box = rg.Box(rg.Plane.WorldXY, rg.Interval(x0, x0 + tread),  # step depth along x…
                 rg.Interval(0, 1.2), rg.Interval(0, z_top))  # …1.2 m wide along y, solid down to the ground
    stair_steps.append(box)  # add the step


# --- OUTPUTS: send results out of the component ---------------
slabs = twisting_slabs  # the twisting tower's floors
panels = facade_panels  # the façade grid
steps = stair_steps  # the staircase
info = f"{len(slabs)} floors, {len(panels)} panels, {riser_count} steps"  # a one-line summary
