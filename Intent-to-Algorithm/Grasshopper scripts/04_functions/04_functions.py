#! python3
# ^ This first line tells the Script component to use Python 3. Never delete it.

# LESSON 04: FUNCTIONS | Rhino 8 Grasshopper Script component (Python 3)
# READ FIRST: 04_functions.md in this folder explains the concept, the full component
#             setup, how to run, exercises (Try this) and AI prompts (Ask the AI).
# Example: a façade of vertical fins (the Rhino version builds a street of towers instead).
# Inputs:  fin_count (int, Item), spacing (float, Item), base_height (float, Item), wave (float, Item)
# Outputs: fins, heights, out


# --- IMPORTS ---------------------------------------------------
import math  # maths toolbox, for the sine wave in step 4 (lesson 02)
import Rhino.Geometry as rg  # Rhino's geometry toolbox, nicknamed 'rg' (lesson 02)


# --- STEP 1: Define a function (see .md → Step 1) -------------
# 'def' writes a recipe. Nothing is built yet: Python only learns the recipe here.
# x and height are PARAMETERS: blanks the recipe fills in each time it's used.
# depth=0.6 and thickness=0.15 are DEFAULTS: used if you don't give a value.
def make_fin(x, height, depth=0.6, thickness=0.15):
    along = rg.Interval(x, x + thickness)  # the fin's extent along the façade (x), from x to x + thickness
    out_from_wall = rg.Interval(0, depth)  # how far the fin sticks out from the wall (y)
    up = rg.Interval(0, height)  # from the ground up to the fin's height (z)
    fin = rg.Box(rg.Plane.WorldXY, along, out_from_wall, up)  # a box from three ranges (Box is explained in lesson 07)
    return fin  # RETURN hands the finished fin back to whoever called the recipe


# --- STEP 2: Call the function once ---------------------------
test_fin = make_fin(0.0, base_height)  # ARGUMENTS 0.0 and base_height fill the blanks x and height
print(f"Test fin is {test_fin.Z.Length} m tall and {test_fin.Y.Length} m deep")  # depth used the 0.6 default


# --- STEP 3: Override a default (see .md → Step 3) ------------
deep_fin = make_fin(0.0, base_height, depth=1.2)  # same recipe, but this time the fin sticks out 1.2 m
print(f"Deep fin is {deep_fin.Y.Length} m deep")  # 1.2 instead of 0.6


# --- STEP 4: A function that only calculates (see .md → Step 4)
def fin_height(index, base, amount):  # works out one fin's height; it draws nothing
    ripple = math.sin(index * 0.5) * amount  # sin() swings smoothly between -1 and +1 as index grows
    return base + ripple  # the base height plus (or minus) the ripple

print(f"Fin 3 would be {round(fin_height(3, base_height, wave), 2)} m tall")  # calling it inside print()


# --- STEP 5: Call both functions many times: a façade ---------
all_fins = []  # an empty list to collect every fin (lists: lesson 01, append: lesson 02)
all_heights = []  # an empty list for the matching heights
for i in range(fin_count):  # repeat fin_count times; i counts 0, 1, 2… (loops: lesson 06)
    h = fin_height(i, base_height, wave)  # recipe 1: work out this fin's height
    fin = make_fin(i * spacing, h)  # recipe 2: build the fin at its position along the façade
    all_fins.append(fin)  # keep the fin
    all_heights.append(round(h, 2))  # keep its height, rounded to 2 decimals

print(f"Built {fin_count} fins from one recipe")  # one definition, many calls


# --- OUTPUTS: send results out of the component ---------------
fins = all_fins  # the fins leave through the 'fins' output
heights = all_heights  # their heights leave through 'heights' (same order as fins)
