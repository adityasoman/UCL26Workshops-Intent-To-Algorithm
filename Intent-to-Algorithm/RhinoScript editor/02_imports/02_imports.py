#! python3
# ^ This first line tells Rhino 8 to run this file with Python 3. Never delete it.

# LESSON 02: IMPORT STATEMENTS | Rhino 8 ScriptEditor (Python 3)
# READ FIRST: 02_imports.md in this folder explains the concept, how to run,
#             exercises (Try this) and AI prompts (Ask the AI).
# NOTE: imports normally all go at the top. Here they're added one step at a time.


# --- SETTINGS (change these and run again) --------------------
LESSON_LAYER = "Lesson_02"  # the layer this lesson draws on
count = 10  # how many random plots to scatter (int)
seed = 1  # a 'seed' fixes the random sequence: the same seed gives the same scatter every run
site_size = 100.0  # our site is a square, site_size × site_size metres
park = [50.0, 50.0, 0.0]  # the park sits in the middle of the site (x, y, z)


# --- STEP 1: import ... as ... (a toolbox with a nickname) ----
import rhinoscriptsyntax as rs  # borrow Rhino's drawing toolbox and nickname it 'rs' to save typing

if not rs.IsLayer(LESSON_LAYER):  # rs.IsLayer means "the IsLayer tool from the rs toolbox"
    rs.AddLayer(LESSON_LAYER)  # create the lesson layer if it doesn't exist yet
rs.CurrentLayer(LESSON_LAYER)  # make it the active layer

rs.AddPoint(park)  # draw the park as a point
rs.AddTextDot("Park", park)  # and label it in the viewport


# --- STEP 2: import ... (a whole toolbox) ---------------------
import math  # borrow Python's built-in maths toolbox. Its tools are used as math.<tool>

print("pi from the math toolbox:", math.pi)  # math.pi is a value stored inside the toolbox
print("tools inside math:", dir(math))  # dir() lists everything in a toolbox, handy for exploring

test_plot = [80.0, 90.0, 0.0]  # one plot to measure first, before we scatter many
dx = test_plot[0] - park[0]  # how far apart they are along x
dy = test_plot[1] - park[1]  # how far apart they are along y
distance = math.sqrt(dx ** 2 + dy ** 2)  # Pythagoras: ** means "to the power of", sqrt is square root
print("test plot to park (math.sqrt):", distance, "m")  # should print 50.0 m


# --- STEP 3: from ... import ... (see .md → Step 3) -----------
from math import sqrt  # take only sqrt out of math, so we can write sqrt(...) without "math."

distance_again = sqrt(dx ** 2 + dy ** 2)  # same calculation, shorter to write
print("test plot to park (sqrt):", distance_again, "m")  # same answer as step 2
print("test plot to park (rs.Distance):", rs.Distance(test_plot, park), "m")  # Rhino's toolbox has its own distance tool


# --- STEP 4: import random (numbers by chance) ----------------
import random  # borrow Python's built-in randomness toolbox

random.seed(seed)  # set the starting point of the random sequence, so results can be repeated
print("a random number between 0 and site_size:", random.uniform(0, site_size))  # uniform(a, b): any decimal between a and b


# --- STEP 5: Use all the toolboxes together -------------------
for i in range(count):  # repeat the indented lines below 'count' times; i counts 0, 1, 2… (loops: lesson 06)
    x = random.uniform(0, site_size)  # random x somewhere on the site (random toolbox)
    y = random.uniform(0, site_size)  # random y somewhere on the site
    plot = [x, y, 0.0]  # put them together as a point on the ground (a list, from lesson 01)
    d = sqrt((x - park[0]) ** 2 + (y - park[1]) ** 2)  # distance from this plot to the park (math toolbox)
    rs.AddPoint(plot)  # draw the plot (rs toolbox)
    print(f"plot {i}: {round(d, 1)} m from the park")  # report it, rounded to 1 decimal place

rs.ZoomExtents()  # zoom so we can see the whole site


# --- STEP 6: When a toolbox isn't there (see .md → Step 6) ----
# import numpy  # NOT installed in Rhino by default: uncommenting gives ModuleNotFoundError
