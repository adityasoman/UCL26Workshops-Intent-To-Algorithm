#! python3
# ^ This first line tells Rhino 8 to run this file with Python 3. Never delete it.

# LESSON 07: CLASSES + RHINOCOMMON | Rhino 8 ScriptEditor (Python 3)
# READ FIRST: 07_classes.md in this folder explains the concept, how to run,
#             exercises (Try this) and AI prompts (Ask the AI).


# --- IMPORTS ---------------------------------------------------
import rhinoscriptsyntax as rs  # Rhino's beginner-friendly toolbox (still used for layers)
import Rhino.Geometry as rg  # RhinoCommon: Rhino's full geometry toolbox (see .md → rs vs RhinoCommon)
import scriptcontext as sc  # gives us 'sc.doc': the Rhino document we add objects to


# --- SETTINGS (change these and run again) --------------------
LESSON_LAYER = "Lesson_07"  # the layer this lesson draws on


# --- STEP 0: Prepare a clean layer for this lesson ------------
if not rs.IsLayer(LESSON_LAYER):  # check whether the layer already exists
    rs.AddLayer(LESSON_LAYER)  # if it doesn't, create it
rs.CurrentLayer(LESSON_LAYER)  # new objects land on the current layer


# --- STEP 1: RhinoCommon in one minute (see .md → Step 1) -----
corner = rg.Point3d(0, 0, 0)  # a Point3d is a point OBJECT, not a list: it knows its .X, .Y, .Z
print("corner.X is", corner.X)  # read one coordinate by name instead of by position [0]
span = rg.Interval(0, 10)  # an Interval is a range of numbers, here from 0 to 10
print("span length is", span.Length)  # objects come with useful properties built in


# --- STEP 2: Define a class: the blueprint (see .md → Step 2) -
class Building:  # a class is a TYPE of thing, like "a building" in general
    """A simple rectangular building."""  # a docstring: a one-line description of the class

    def __init__(self, name, x, y, width, depth, floors, floor_height=3.0):  # runs when a new building is made
        self.name = name  # ATTRIBUTE: a value each building stores about itself
        self.x = x  # position of the south-west corner, x
        self.y = y  # position of the south-west corner, y
        self.width = width  # size along x, metres
        self.depth = depth  # size along y, metres
        self.floors = floors  # number of storeys
        self.floor_height = floor_height  # storey height, with a default like lesson 04

    def height(self):  # METHOD: a function that belongs to the class; 'self' is "this building"
        return self.floors * self.floor_height  # uses this building's own attributes

    def floor_area(self):  # another method
        return self.width * self.depth * self.floors  # gross floor area, m²

    def to_box(self):  # method that turns the building into RhinoCommon geometry
        xs = rg.Interval(self.x, self.x + self.width)  # extent along x
        ys = rg.Interval(self.y, self.y + self.depth)  # extent along y
        zs = rg.Interval(0, self.height())  # from ground to roof; a method can call another method
        return rg.Box(rg.Plane.WorldXY, xs, ys, zs)  # a Box made from a plane and three ranges

    def describe(self):  # method that returns a readable sentence
        return f"{self.name}: {self.floors} floors, {self.height()} m, {self.floor_area()} m²"  # f-string, lesson 01


# --- STEP 3: Make instances: actual buildings (see .md → Step 3)
library = Building("Library", 0, 0, 30, 20, 4, floor_height=4.5)  # calling the class runs __init__
housing = Building("Housing", 40, 0, 15, 15, 12)  # a second, separate building from the same blueprint
office = Building("Office", 65, 0, 25, 25, 18, floor_height=3.6)  # a third

print(library.name, "is", library.height(), "m tall")  # dot + attribute name reads a value
print(housing.describe())  # dot + method name + () runs a method


# --- STEP 4: Change an attribute ------------------------------
housing.floors = 16  # the client wants more homes: change this one building only
print("After the change:", housing.describe())  # height and area update automatically
print("The library is unchanged:", library.describe())  # each instance keeps its own data


# --- STEP 5: Many buildings in a list, drawn with RhinoCommon -
buildings = [library, housing, office]  # instances can go in a list like any other value
for b in buildings:  # loop over them (lesson 06)
    box = b.to_box()  # ask each building for its geometry
    sc.doc.Objects.AddBox(box)  # RhinoCommon way of adding geometry to the document
    rs.AddTextDot(b.name, [b.x + b.width / 2, b.y + b.depth / 2, b.height()])  # label the roof
    print(b.describe())  # report it

sc.doc.Views.Redraw()  # RhinoCommon doesn't redraw by itself: refresh the viewport
rs.ZoomExtents()  # zoom to see all buildings
