#! python3
# ^ This first line tells the Script component to use Python 3. Never delete it.

# LESSON 07: CLASSES + RHINOCOMMON | Rhino 8 Grasshopper Script component (Python 3)
# READ FIRST: 07_classes.md in this folder explains the concept, the full component
#             setup, how to run, exercises (Try this) and AI prompts (Ask the AI).
# Example: a Room class that lays out a simple floor plan (the Rhino version uses a Building class).
# Inputs:  names (str, List), widths (float, List), depth (float, Item), height (float, Item)
# Outputs: rooms, outlines, centres, info, out


# --- IMPORTS ---------------------------------------------------
import Rhino.Geometry as rg  # RhinoCommon: Rhino's full geometry toolbox (see .md → rs vs RhinoCommon)


# --- STEP 1: RhinoCommon in one minute (see .md → Step 1) -----
corner = rg.Point3d(0, 0, 0)  # a Point3d is a point OBJECT: it knows its .X, .Y, .Z
print("corner.X is", corner.X)  # read one coordinate by name instead of by position [0]
span = rg.Interval(0, 10)  # an Interval is a range of numbers, here from 0 to 10
print("span length is", span.Length)  # objects come with useful properties built in


# --- STEP 2: Define a class: the blueprint (see .md → Step 2) -
class Room:  # a class is a TYPE of thing, like "a room" in general
    """A rectangular room in a single-storey plan."""  # a docstring: a one-line description

    def __init__(self, name, x, width, depth, height=3.0):  # runs when a new room is made
        self.name = name  # ATTRIBUTE: a value each room stores about itself
        self.x = x  # where the room starts along the corridor, metres
        self.width = width  # size along x, metres
        self.depth = depth  # size along y, metres
        self.height = height  # ceiling height, with a default like lesson 04

    def area(self):  # METHOD: a function that belongs to the class; 'self' is "this room"
        return self.width * self.depth  # floor area, m²

    def volume(self):  # another method
        return self.area() * self.height  # a method can call another method of the same room

    def is_large(self):  # a method that answers a yes/no question (lesson 05)
        return self.area() >= 20  # True if the room is 20 m² or more

    def centre(self):  # the middle of the floor, for labels
        return rg.Point3d(self.x + self.width / 2, self.depth / 2, 0)  # a RhinoCommon point

    def to_box(self):  # turns the room into 3D geometry
        xs = rg.Interval(self.x, self.x + self.width)  # extent along x
        ys = rg.Interval(0, self.depth)  # extent along y
        zs = rg.Interval(0, self.height)  # floor to ceiling
        return rg.Box(rg.Plane.WorldXY, xs, ys, zs)  # a Box made from a plane and three ranges

    def to_outline(self):  # turns the room into a 2D plan outline
        plane = rg.Plane(rg.Point3d(self.x, 0, 0), rg.Vector3d.ZAxis)  # a flat plane at the room's corner
        return rg.Rectangle3d(plane, self.width, self.depth)  # a width × depth rectangle

    def describe(self):  # returns a readable sentence
        size = "large" if self.is_large() else "small"  # a one-line if/else: picks one of two values
        return f"{self.name}: {self.area():.1f} m², {self.volume():.1f} m³ ({size})"  # :.1f = 1 decimal place


# --- STEP 3: Make one instance (see .md → Step 3) -------------
test_room = Room("Test", 0, 4.0, depth)  # calling the class runs __init__; height uses the default
print(test_room.name, "has an area of", test_room.area(), "m²")  # dot + attribute / dot + method()
test_room.width = 6.0  # change an attribute of this one room
print("After widening:", test_room.describe())  # area and volume update automatically


# --- STEP 4: One room per name, side by side (see .md → Step 4)
plan = []  # an empty list to hold every Room instance
cursor = 0.0  # where the next room starts along x; moves along as rooms are added
for i in range(len(names)):  # one pass per room name (loops: lesson 06)
    w = widths[i] if i < len(widths) else widths[-1]  # matching width; reuse the last one if the list is short
    room = Room(names[i], cursor, w, depth, height)  # make a new, separate Room instance
    plan.append(room)  # keep it
    cursor = cursor + w  # the next room starts where this one ends


# --- STEP 5: Ask every instance for its data and geometry -----
room_boxes = []  # 3D boxes
room_outlines = []  # 2D plan rectangles
room_centres = []  # label positions
room_info = []  # one sentence per room
for room in plan:  # loop over the instances
    room_boxes.append(room.to_box())  # each room builds its own geometry
    room_outlines.append(room.to_outline())  # and its own outline
    room_centres.append(room.centre())  # and its own label point
    room_info.append(room.describe())  # and describes itself

total = 0.0  # running total of floor area
for room in plan:  # visit every room again
    total = total + room.area()  # add its area
print(f"{len(plan)} rooms, total {total:.1f} m², plan length {cursor:.1f} m")  # summary


# --- OUTPUTS: send results out of the component ---------------
rooms = room_boxes  # the rooms as boxes
outlines = room_outlines  # the plan outlines
centres = room_centres  # label points (connect to a Text Tag with 'names')
info = room_info  # the descriptions (connect a Panel)
