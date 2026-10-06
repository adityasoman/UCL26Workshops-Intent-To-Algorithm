#! python3
# ^ This first line tells Rhino 8 to run this file with Python 3. Never delete it.

# LESSON 04: FUNCTIONS | Rhino 8 ScriptEditor (Python 3)
# READ FIRST: 04_functions.md in this folder explains the concept, how to run,
#             exercises (Try this) and AI prompts (Ask the AI).


# --- IMPORTS ---------------------------------------------------
import rhinoscriptsyntax as rs  


# --- SETTINGS (change these and run again) --------------------
LESSON_LAYER = "Lesson_04"  # the layer this lesson draws on
tower_width = 8.0  # every tower footprint is tower_width × tower_width metres
street_gap = 4.0  # metres of empty space between neighbouring towers


# --- STEP 0: Prepare a clean layer for this lesson ------------
if not rs.IsLayer(LESSON_LAYER):  # check whether the layer already exists
    rs.AddLayer(LESSON_LAYER)  # if it doesn't, create it
rs.CurrentLayer(LESSON_LAYER)  # make it the active layer so new objects land on it


# --- STEP 1: Define a function (see .md → Step 1) -------------
# 'def' writes a recipe. Nothing is built yet: Python only learns the recipe here.
# x, y and floors are PARAMETERS: blanks the recipe fills in each time it's used.
# floor_height=3.0 is a DEFAULT: if you don't give a value, 3.0 is used.
def make_tower(x, y, floors, floor_height=3.0):
    height = floors * floor_height  # total height in metres: storeys × storey height
    w = tower_width  # short name for the footprint width, to keep the next lines readable
    corners = [  # a box needs 8 corner points: 4 at the bottom, then 4 at the top
        [x, y, 0], [x + w, y, 0], [x + w, y + w, 0], [x, y + w, 0],  # bottom 4, anticlockwise
        [x, y, height], [x + w, y, height], [x + w, y + w, height], [x, y + w, height],  # top 4, same order
    ]
    box = rs.AddBox(corners)  # draw the box in Rhino; rs gives back its ID (a label for the object)
    rs.AddTextDot(f"{floors} fl", [x + w / 2, y + w / 2, height])  # label the roof with the floor count
    return box, height  # RETURN hands results back to whoever called the recipe


# --- STEP 2: Call the function once (see .md → Step 2) --------
first_box, first_height = make_tower(0, 0, 10)  # ARGUMENTS 0, 0, 10 fill the blanks x, y, floors
print(f"First tower: {first_height} m tall")  # 10 floors × 3.0 m default = 30.0 m


# --- STEP 3: Call it again and again: a street ----------------
step = tower_width + street_gap  # distance from one tower's corner to the next
make_tower(step * 1, 0, 4)  # a low 4-storey tower next door; we ignore what it returns
make_tower(step * 2, 0, 16)  # a 16-storey tower
make_tower(step * 3, 0, 7)  # a 7-storey tower
_, tall_height = make_tower(step * 4, 0, 22)  # keep only the height; '_' means "I don't need this one"
print(f"Tallest tower: {tall_height} m")  # 22 × 3.0 = 66.0 m


# --- STEP 4: Override the default (see .md → Step 4) ----------
_, office_height = make_tower(step * 5, 0, 10, floor_height=4.2)  # offices have taller storeys
print(f"Office tower with 10 floors: {office_height} m")  # same floors as the first, but 42.0 m tall
_, flat_height = make_tower(step * 6, 0, floors=10, floor_height=2.8)  # arguments can also be passed by NAME
print(f"Flats with 10 floors: {flat_height} m")  # 28.0 m


# --- STEP 5: A function that only calculates ------------------
def tower_area(floors):  # a recipe that draws nothing: it only works out a number
    return floors * tower_width * tower_width  # gross floor area = storeys × footprint area

print(f"Floor area of a 16-storey tower: {tower_area(16)} m²")  # the result goes straight into print()

rs.ZoomExtents()  # zoom so the whole street is visible
