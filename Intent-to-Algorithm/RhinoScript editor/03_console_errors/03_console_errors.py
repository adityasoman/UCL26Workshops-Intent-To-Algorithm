#! python3
# ^ This first line tells Rhino 8 to run this file with Python 3. Never delete it.

# LESSON 03: CONSOLE ERRORS | Rhino 8 ScriptEditor (Python 3)
# READ FIRST: 03_console_errors.md in this folder explains how to read errors, what each
#             BREAK IT block does, exercises (Try this) and AI prompts (Ask the AI).


# --- IMPORTS ---------------------------------------------------
import rhinoscriptsyntax as rs  # Rhino's beginner-friendly toolbox of drawing commands


# --- SETTINGS (change these and run again) --------------------
LESSON_LAYER = "Lesson_03"  # the layer this lesson draws on
name = "Tower A"  # the tower's name (str)
floors = 10  # number of storeys (int)
floor_height = 3.5  # metres per storey (float)
width = 20.0  # footprint size along x, in metres
depth = 15.0  # footprint size along y, in metres
origin = [0.0, 0.0, 0.0]  # where the tower's corner sits (x, y, z)
height_limit = 60.0  # a planning rule: towers above this height get a warning


# --- STEP 0: Prepare a clean layer for this lesson ------------
if not rs.IsLayer(LESSON_LAYER):  # check whether the layer already exists
    rs.AddLayer(LESSON_LAYER)  # if it doesn't, create it
rs.CurrentLayer(LESSON_LAYER)  # make it the active layer so new objects land on it


# --- STEP 1: A working tower (this part has no mistakes) ------
height = floors * floor_height  # total height in metres

x = origin[0]  # the tower's corner, x
y = origin[1]  # the tower's corner, y
z = origin[2]  # the tower's corner, z
corners = [  # a box needs 8 corners: 4 on the ground, then 4 on the roof
    [x, y, z],  # ground, corner 1
    [x + width, y, z],  # ground, corner 2
    [x + width, y + depth, z],  # ground, corner 3
    [x, y + depth, z],  # ground, corner 4
    [x, y, z + height],  # roof, above corner 1
    [x + width, y, z + height],  # roof, above corner 2
    [x + width, y + depth, z + height],  # roof, above corner 3
    [x, y + depth, z + height],  # roof, above corner 4
]  # the closing bracket ends the list of corners

rs.AddBox(corners)  # draw the tower as a box
rs.ZoomExtents()  # zoom so we can see it
print(f"{name}: {floors} floors, {height} m tall")  # report what we built


# --- STEP 2: Your own warning message (see .md → Step 2) ------
if height > height_limit:  # "if the tower is too tall…" (if statements: lesson 05)
    print(f"WARNING: {name} is {height} m, above the {height_limit} m limit")  # …tell the user, but keep running


# --- STEP 3: BREAK IT (see .md → Break it) --------------------
# Uncomment ONE marked line at a time (delete its "# "), run, read the error, then re-comment it.
print("Starting the BREAK IT section")  # a normal line at the left edge, so we can see where errors stop the script

# ---- BREAK IT 1: SyntaxError (.md → Break it 1) ----
# print("Tower A is tall)

# ---- BREAK IT 2: IndentationError (.md → Break it 2) ----
#     print("This line starts with spaces for no reason")

# ---- BREAK IT 3: NameError (.md → Break it 3) ----
# print(tower_heigth)

# ---- BREAK IT 4: TypeError (.md → Break it 4) ----
# label = "Height: " + height

# ---- BREAK IT 5: IndexError (.md → Break it 5) ----
# w = origin[3]

# ---- BREAK IT 6: AttributeError (.md → Break it 6) ----
# shout = name.uppercase()


# --- STEP 4: The finish line ----------------------------------
print("Script finished without errors")  # if you see this, nothing above stopped the script
