#! python3
# ^ This first line tells Rhino 8 to run the script as Python 3. Never delete it.

# TECHNIQUE 1: PROMPT -> SCRIPT -> DEBUG | Grasshopper Python 3 Script component
# READ FIRST: Prompt_Script_Debug.md (same folder)
# Example: grid of boxes whose height and rotation follow an attractor point
#
# Inputs:  count_x (int, Item), count_y (int, Item), spacing (float, Item),
#          box_size (float, Item), attractor (Point3d, Item),
#          min_height (float, Item), max_height (float, Item),
#          max_rotation (float, Item)
# Outputs: out, points, boxes, heights

# --- IMPORTS ---
import math                                   # maths tools: we use math.radians()
import Rhino.Geometry as rg                   # Rhino geometry: points, planes, boxes
import Grasshopper                            # lets us show warnings on the component
import Rhino                                  # gives access to the Rhino document
import System                                 # .NET types: we check for System.Guid

# --- STEP 0: make sure the attractor is a point, not a Rhino object ID ---
# If the 'attractor' type hint is not set to Point3d, Grasshopper sends the
# point's ID (a GUID) instead of the point. We look the real point up here.
if isinstance(attractor, System.Guid):        # did we get an ID instead of a point?
    rhino_obj = Rhino.RhinoDoc.ActiveDoc.Objects.FindId(attractor)  # find that object in Rhino
    if rhino_obj is not None and isinstance(rhino_obj.Geometry, rg.Point):  # is it a point?
        attractor = rhino_obj.Geometry.Location  # use its location as a Point3d
    else:                                     # the ID is not a point (or was deleted)
        attractor = None                      # treat it as "not connected"

# --- STEP 1: PRODUCER - make the grid of points (see .md -> The task) ---
points = []                                   # empty list that will hold the grid points
for i in range(count_x):                      # repeat once for every column (X direction)
    for j in range(count_y):                  # repeat once for every row (Y direction)
        x = i * spacing                       # X position of this point
        y = j * spacing                       # Y position of this point
        points.append(rg.Point3d(x, y, 0))    # make the point on the ground and store it

boxes = []                                    # empty list that will hold the boxes
heights = []                                  # empty list that will hold each box's height

if attractor is None:                         # nothing connected to the attractor input?
    ghenv.Component.AddRuntimeMessage(        # show an orange warning balloon
        Grasshopper.Kernel.GH_RuntimeMessageLevel.Warning,  # warning level (orange)
        "Connect a point to 'attractor'.")    # the message the student will read
else:                                         # the attractor is connected, so carry on

    # --- STEP 2: OPERATOR - measure each point's distance to the attractor ---
    distances = []                            # empty list that will hold the distances
    for pt in points:                         # visit every grid point
        distances.append(pt.DistanceTo(attractor))  # store how far it is from the attractor
    far = max(distances)                      # the distance of the furthest point
    if far == 0:                              # only one point, sitting on the attractor?
        far = 1.0                             # use 1 so we never divide by zero

    # --- STEP 3: OPERATOR - remap distance to height and rotation ---
    for pt, d in zip(points, distances):      # visit each point together with its distance
        t = 1.0 - d / far                     # 1.0 = closest to attractor, 0.0 = furthest
        h = min_height + t * (max_height - min_height)  # close = tall, far = short
        angle = math.radians(t * max_rotation)          # close = more rotation (in radians)

        # --- STEP 4: CONSUMER - build the rotated box ---
        half = box_size / 2.0                 # half the width, so the box is centred
        plane = rg.Plane(pt, rg.Vector3d.ZAxis)          # flat base plane at the point
        box = rg.Box(plane,                   # make a box on that plane...
                     rg.Interval(-half, half),  # ...this wide in X, centred on the point
                     rg.Interval(-half, half),  # ...this deep in Y, centred on the point
                     rg.Interval(0, h))         # ...and this tall, from the ground up
        brep = box.ToBrep()                   # turn it into a Brep, which we can rotate
        brep.Rotate(angle, rg.Vector3d.ZAxis, pt)  # spin it about Z, around its own centre
        boxes.append(brep)                    # store the finished box
        heights.append(h)                     # store its height

    print("{} boxes made".format(len(boxes)))           # summary in the out panel
    print("tallest: {:.2f}".format(max(heights)))       # tallest box height
    print("shortest: {:.2f}".format(min(heights)))      # shortest box height

# --- OUTPUTS ---
points = points                               # grid points -> 'points' output
boxes = boxes                                 # rotated boxes -> 'boxes' output
heights = heights                             # box heights -> 'heights' output
