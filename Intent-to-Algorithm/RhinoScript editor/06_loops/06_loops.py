#! python3
# ^ This first line tells Rhino 8 to run this file with Python 3. Never delete it.

# LESSON 06: LOOPS | Rhino 8 ScriptEditor (Python 3)
# READ FIRST: 06_loops.md in this folder explains the concept, how to run,
#             exercises (Try this) and AI prompts (Ask the AI).


# --- IMPORTS ---------------------------------------------------
import rhinoscriptsyntax as rs  # Rhino's beginner-friendly toolbox (lesson 02)


# --- SETTINGS (change these and run again) --------------------
LESSON_LAYER = "Lesson_06"  # the layer this lesson draws on
x_count = 10  # how many plots along x
y_count = 10  # how many plots along y
spacing = 10.0  # metres between plot centres
height_limit = 45.0  # planning limit for the tower in step 5, metres
ground_floor_height = 4.5  # the ground floor is taller (shops, lobby)
upper_floor_height = 3.1  # every other floor
tower_origin = [120.0, 0.0, 0.0]  # where the tower stands, beside the grid


# --- STEP 0: Prepare a clean layer for this lesson ------------
if not rs.IsLayer(LESSON_LAYER):  # check whether the layer already exists
    rs.AddLayer(LESSON_LAYER)  # if it doesn't, create it
rs.CurrentLayer(LESSON_LAYER)  # make it the active layer


# --- STEP 1: for + range: repeat a set number of times (see .md → Step 1)
for i in range(5):  # range(5) gives 0, 1, 2, 3, 4: five numbers, starting at 0
    print("counting:", i)  # the indented lines run once per number

for i in range(2, 11, 4):  # range(start, stop, step) gives 2, 6, 10 (stop itself is never included)
    print("every 4th floor from 2:", i)  # useful for "every nth floor" rules


# --- STEP 2: for over a list: repeat once per item ------------
uses = ["retail", "office", "housing"]  # a list from lesson 01
for use in uses:  # 'use' becomes each item in turn
    print("this block has", use)  # runs three times


# --- STEP 3: Nested loops make a grid (see .md → Step 3) -----
plots = []  # an empty list; we'll append one point per plot
for ix in range(x_count):  # OUTER loop: one pass per column
    for iy in range(y_count):  # INNER loop: runs fully for EACH column, one pass per row
        x = ix * spacing  # column number × spacing = x position
        y = iy * spacing  # row number × spacing = y position
        plots.append([x, y, 0.0])  # add this plot's point to the end of the list

print("plots made:", len(plots))  # len() counts the items: x_count × y_count
rs.AddPoints(plots)  # draw them all at once


# --- STEP 4: Loop over what you made -------------------------
corner_count = 0  # a counter, from lesson 05
for p in plots:  # visit every plot
    is_edge_x = p[0] == 0 or p[0] == (x_count - 1) * spacing  # on the left or right edge?
    is_edge_y = p[1] == 0 or p[1] == (y_count - 1) * spacing  # on the bottom or top edge?
    if is_edge_x and is_edge_y:  # both → it's a corner plot (conditionals: lesson 05)
        rs.AddTextDot("corner", p)  # mark it
        corner_count = corner_count + 1  # count it
print("corner plots:", corner_count)  # always 4 for a full grid


# --- STEP 5: while: repeat until a condition is met (see .md → Step 5)
# ⚠️ A while loop runs until its condition becomes False. If it never does, Rhino FREEZES.
#    Always make sure something inside the loop moves towards the stop condition,
#    and add a hard cap (MAX_FLOORS) as a safety net.
MAX_FLOORS = 200  # safety net: never build more than this, whatever happens
level_z = 0.0  # height of the floor we're about to place
floor_count = 0  # how many floors placed so far
w = 15.0  # tower footprint size, metres
while level_z + upper_floor_height <= height_limit and floor_count < MAX_FLOORS:  # room for another floor?
    x0, y0 = tower_origin[0], tower_origin[1]  # unpack the tower's corner position
    outline = [[x0, y0, level_z], [x0 + w, y0, level_z], [x0 + w, y0 + w, level_z],  # 3 corners…
               [x0, y0 + w, level_z], [x0, y0, level_z]]  # …4th corner, then back to the start to close it
    rs.AddPolyline(outline)  # draw this floor plate
    if floor_count == 0:  # the ground floor
        level_z = level_z + ground_floor_height  # MOVE TOWARDS THE STOP: raise the next floor's height
    else:  # every other floor
        level_z = level_z + upper_floor_height  # MOVE TOWARDS THE STOP
    floor_count = floor_count + 1  # one more floor placed

print(f"Tower: {floor_count} floors, roof at {round(level_z, 1)} m (limit {height_limit} m)")  # level_z is now the top of the last floor

rs.ZoomExtents()  # zoom to see the grid and the tower
