#! python3
# ^ This first line tells Rhino 8 to run this file with Python 3. Never delete it.

# LESSON 01: DATA TYPES | Rhino 8 ScriptEditor (Python 3)
# READ FIRST: 01_data_types.md in this folder explains the concept, how to run,
#             exercises (Try this) and AI prompts (Ask the AI).


# --- IMPORTS ---------------------------------------------------
import rhinoscriptsyntax as rs  # Rhino's beginner-friendly toolbox of drawing commands (lesson 02 explains 'import')


# --- SETTINGS (change these and run again) --------------------
LESSON_LAYER = "Lesson_01"  # the layer this lesson draws on (a str, since it's text)


# --- STEP 0: Prepare a clean layer for this lesson ------------
if not rs.IsLayer(LESSON_LAYER):  # check whether the layer already exists
    rs.AddLayer(LESSON_LAYER)  # if it doesn't, create it
rs.CurrentLayer(LESSON_LAYER)  # make it the active layer so new objects land on it


# --- STEP 1: Numbers (int and float) --------------------------
floors = 12  # an int (integer): a whole number with no decimal point. You can't build 12.5 storeys
floor_height = 3.2  # a float: a number with a decimal point. Floor-to-floor height in metres

print("floors =", floors, "->", type(floors))  # print() shows values in the Console; type() tells us the kind of data
print("floor_height =", floor_height, "->", type(floor_height))  # this one should say <class 'float'>


# --- STEP 2: Text (str) ---------------------------------------
name = "Tower A"  # a str (string): text, always written inside quotes "..." or '...'

print("name =", name, "->", type(name))  # should say <class 'str'>


# --- STEP 3: Yes or no (bool) ---------------------------------
is_residential = True  # a bool (boolean): can only be True or False, written with a capital letter

print("is_residential =", is_residential, "->", type(is_residential))  # should say <class 'bool'>


# --- STEP 4: Nothing yet (None) -------------------------------
roof_garden = None  # None means "no value yet". It is not zero and not empty text, just "not decided"

print("roof_garden =", roof_garden, "->", type(roof_garden))  # should say <class 'NoneType'>


# --- STEP 5: A group of values (list) -------------------------
origin = [10.0, 5.0, 0.0]  # a list: several values in order, inside [ ]. Here the tower's x, y, z in metres

print("origin =", origin, "->", type(origin))  # should say <class 'list'>
print("x of origin =", origin[0])  # [0] fetches the FIRST item. Python counts positions from 0, not 1
print("y of origin =", origin[1])  # [1] fetches the second item
print("z of origin =", origin[2])  # [2] fetches the third item
print("items in origin =", len(origin))  # len() counts how many items a list holds (here 3)


# --- STEP 6: Mixing types (see .md → Step 6) ------------------
total_height = floors * floor_height  # int × float gives a float. * means multiply

print("raw total_height =", total_height)  # may show 38.400000000000006: computers store decimals approximately
total_height = round(total_height, 2)  # round() tidies it to 2 decimal places and we store it back in the same box
print(f"{name} is {total_height} m tall")  # an f-string: put f before the quotes and {variables} inside the text
print(f"Residential? {is_residential}. Roof garden: {roof_garden}")  # f-strings can mix any types into one sentence


# --- STEP 7: From data to geometry ----------------------------
top = [origin[0], origin[1], origin[2] + total_height]  # a new list: same x and y, z raised by the tower's height

base_id = rs.AddPoint(origin)  # Rhino turns our list of 3 numbers into a point at the tower's base
top_id = rs.AddPoint(top)  # a second point at the top of the tower
rs.AddTextDot(name, top)  # a text label in the viewport showing our str at the top point

print("Rhino's ID for the base point:", base_id, "->", type(base_id))  # Rhino objects have their own type: an ID (Guid)

rs.ZoomExtents()  # zoom the viewport so we can see what was drawn
