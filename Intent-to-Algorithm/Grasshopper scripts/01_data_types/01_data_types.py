#! python3
# ^ This first line tells the Script component to use Python 3. Never delete it.

# LESSON 01: DATA TYPES | Rhino 8 Grasshopper Script component (Python 3)
# READ FIRST: 01_data_types.md in this folder explains the concept, the full component
#             setup, how to run, exercises (Try this) and AI prompts (Ask the AI).
# Inputs:  floors (int, Item), floor_height (float, Item)
# Outputs: info, point, top_point, out


# --- IMPORTS ---------------------------------------------------
import Rhino.Geometry as rg  # Rhino's geometry toolbox; gives us Point3d (imports in lesson 02, RhinoCommon in lesson 07)


# --- STEP 1: Numbers (int and float), arriving from the sliders
# floors and floor_height already hold values, because the input sliders filled them in.
print("floors =", floors, "->", type(floors))  # print() goes to 'out'; type() tells us the kind of data. Should be int
print("floor_height =", floor_height, "->", type(floor_height))  # should say <class 'float'>


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
summary = f"{name} is {total_height} m tall"  # an f-string: put f before the quotes and {variables} inside the text
details = f"Residential? {is_residential}. Roof garden: {roof_garden}"  # f-strings can mix any types into one sentence


# --- STEP 7: From data to geometry ----------------------------
top = [origin[0], origin[1], origin[2] + total_height]  # a new list: same x and y, z raised by the tower's height

base_point = rg.Point3d(origin[0], origin[1], origin[2])  # build a Rhino point from the 3 numbers in our list
top_pt = rg.Point3d(top[0], top[1], top[2])  # a second point at the top of the tower

print("base_point =", base_point, "->", type(base_point))  # geometry has its own type: <class 'Rhino.Geometry.Point3d'>


# --- OUTPUTS: send results out of the component ---------------
info = [summary, details]  # a list of two texts: a Panel shows each item on its own line
point = base_point  # 'point' matches an output name, so the base point leaves through that output
top_point = top_pt  # same for the top point
