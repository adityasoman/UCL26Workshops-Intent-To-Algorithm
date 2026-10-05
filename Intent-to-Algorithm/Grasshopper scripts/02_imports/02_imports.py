#! python3
# ^ This first line tells the Script component to use Python 3. Never delete it.

# LESSON 02: IMPORT STATEMENTS | Rhino 8 Grasshopper Script component (Python 3)
# READ FIRST: 02_imports.md in this folder explains the concept, the full component
#             setup, how to run, exercises (Try this) and AI prompts (Ask the AI).
# Inputs:  count (int, Item), seed (int, Item)
# Outputs: points, park_point, distances, out
# NOTE: imports normally all go at the top. Here they're added one step at a time.


# --- SETTINGS (fixed in the code; count and seed come from the sliders)
site_size = 100.0  # our site is a square, site_size × site_size metres
park = [50.0, 50.0, 0.0]  # the park sits in the middle of the site (x, y, z)


# --- STEP 1: import ... as ... (a toolbox with a nickname) ----
import Rhino.Geometry as rg  # borrow Rhino's geometry toolbox and nickname it 'rg' to save typing

park_pt = rg.Point3d(park[0], park[1], park[2])  # rg.Point3d means "the Point3d tool from the rg toolbox"


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

import rhinoscriptsyntax as rs  # Rhino's simple-commands toolbox, nicknamed 'rs'
print("test plot to park (rs.Distance):", rs.Distance(test_plot, park), "m")  # Rhino's toolbox has its own distance tool


# --- STEP 4: import random (see .md → Step 4) -----------------
import random  # borrow Python's built-in randomness toolbox

random.seed(seed)  # set the starting point of the random sequence; Grasshopper re-runs often, so this keeps results stable
print("a random number between 0 and site_size:", random.uniform(0, site_size))  # uniform(a, b): any decimal between a and b


# --- STEP 5: Use all the toolboxes together -------------------
plot_points = []  # an empty list; we'll add one point to it each time round the loop
plot_distances = []  # an empty list for the matching distances

for i in range(count):  # repeat the indented lines below 'count' times; i counts 0, 1, 2… (loops: lesson 06)
    x = random.uniform(0, site_size)  # random x somewhere on the site (random toolbox)
    y = random.uniform(0, site_size)  # random y somewhere on the site
    d = sqrt((x - park[0]) ** 2 + (y - park[1]) ** 2)  # distance from this plot to the park (math toolbox)
    plot_points.append(rg.Point3d(x, y, 0.0))  # make a point (rg toolbox) and add it to the end of the list
    plot_distances.append(round(d, 1))  # store the distance, rounded to 1 decimal place
    print(f"plot {i}: {round(d, 1)} m from the park")  # report it in 'out'


# --- STEP 6: When a toolbox isn't there (see .md → Step 6) ----
# import numpy  # NOT installed in Rhino by default: uncommenting turns the component red (ModuleNotFoundError)


# --- OUTPUTS: send results out of the component ---------------
points = plot_points  # the scattered plots leave through the 'points' output
park_point = park_pt  # the park leaves through 'park_point'
distances = plot_distances  # the distances leave through 'distances' (same order as points)
