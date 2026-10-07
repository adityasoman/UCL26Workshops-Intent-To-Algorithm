#! python3
# ^ This first line tells Rhino 8 to run the script as Python 3. Never delete it.

# TECHNIQUE 2: PROMPT + IMAGE -> SCRIPT -> DEBUG | Grasshopper Python 3 Script component
# READ FIRST: Prompt_Image_Script_Debug.md (same folder)
# Example: rotated brick screen wall, built from Sketch.png
#
# Units: millimetres (set your Rhino file to mm)
# Inputs:  wall_length (float, Item), course_gap (float, Item),
#          bricks_per_course (int, Item), courses (int, Item),
#          brick_length (float, Item), brick_depth (float, Item),
#          brick_height (float, Item), max_rotation (float, Item)
# Outputs: out, bricks, centres, angles

# --- IMPORTS ---
import math                                   # maths tools: we use math.radians()
import Rhino.Geometry as rg                   # Rhino geometry: points, planes, boxes

# --- STEP 1: PRODUCER - work out the spacing from the sketch's dimensions ---
step_x = wall_length / bricks_per_course      # distance from one brick centre to the next
step_z = brick_height + course_gap          # one brick high plus the joint above it
half_l = brick_length / 2.0                   # half the brick length (for centring)
half_d = brick_depth / 2.0                    # half the brick depth (for centring)

bricks = []                                   # empty list that will hold the bricks
centres = []                                  # empty list that will hold each brick's centre
angles = []                                   # empty list that will hold each brick's angle

# --- STEP 2: PRODUCER - place bricks in stretcher bond, course by course ---
for row in range(courses):                    # repeat once for every course (bottom = 0)
    z = row * step_z                          # height of the bottom of this course
    if row % 2 == 0:                          # even course: 0, 2, 4...
        offset = 0.0                          # starts at the left edge of the wall
        count = bricks_per_course             # full number of bricks
    else:                                     # odd course: 1, 3, 5...
        offset = step_x / 2.0                 # shifted by half a brick (stretcher bond)
        count = bricks_per_course - 1         # one fewer brick so it fits inside the wall

    # --- STEP 3: OPERATOR - the higher the course, the more it rotates ---
    if courses > 1:                           # more than one course?
        t = row / (courses - 1)               # 0.0 at the bottom, 1.0 at the top
    else:                                     # only one course
        t = 0.0                               # no rotation
    angle = t * max_rotation                  # this course's angle, in degrees

    # --- STEP 4: CONSUMER - build and rotate each brick ---
    for i in range(count):                    # repeat once for every brick in the course
        x = offset + step_x / 2.0 + i * step_x  # X of this brick's centre along the wall
        centre = rg.Point3d(x, 0, z)          # brick centre on the bottom of the course
        plane = rg.Plane(centre, rg.Vector3d.ZAxis)  # flat base plane at that centre
        box = rg.Box(plane,                   # make a box on that plane...
                     rg.Interval(-half_l, half_l),  # ...long along the wall (X)
                     rg.Interval(-half_d, half_d),  # ...deep through the wall (Y)
                     rg.Interval(0, brick_height))  # ...and one brick high (Z)
        brick = box.ToBrep()                  # turn it into a Brep, which we can rotate
        brick.Rotate(math.radians(angle),     # rotate by this course's angle (in radians)...
                     rg.Vector3d.ZAxis,       # ...about a vertical axis...
                     centre)                  # ...through the brick's own centre
        bricks.append(brick)                  # store the finished brick
        centres.append(centre)                # store its centre
        angles.append(angle)                  # store its angle

print("{} courses, {} bricks".format(courses, len(bricks)))   # summary in the out panel
print("wall height: {:.0f} mm".format(courses * step_z))       # total height of the wall
print("top course rotation: {:.0f} deg".format(max_rotation))  # rotation of the top course

# --- OUTPUTS ---
bricks = bricks                               # rotated bricks -> 'bricks' output
centres = centres                             # brick centres -> 'centres' output
angles = angles                               # brick angles -> 'angles' output
