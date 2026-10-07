#! python3
# ^ This first line tells Rhino 8 to run the script as Python 3. Never delete it.

# TECHNIQUE 3: SKETCH OVER OUTPUT -> MODIFY -> DEBUG | Grasshopper Python 3 Script component
# READ FIRST: Sketch_Over_Output.md (same folder)
# Example: the Technique 2 brick screen, modified so a sine wave sets the top
#          profile of the wall (from "Edited sketch.png")
#
# Units: millimetres (set your Rhino file to mm)
# Inputs:  wall_length (float, Item), course_gap (float, Item),
#          bricks_per_course (int, Item),
#          brick_length (float, Item), brick_depth (float, Item),
#          brick_height (float, Item), max_rotation (float, Item),
#          base_height (float, Item), wave_amplitude (float, Item),
#          wave_count (float, Item), wave_shift (float, Item)
# Outputs: out, bricks, centres, angles, profile
#
# CHANGED from Technique 2:
#   removed input  'courses'  (the wave now decides how tall the wall is)
#   new inputs     base_height, wave_amplitude, wave_count, wave_shift
#   new output     profile    (the sine wave curve, to compare with the sketch)

# --- IMPORTS ---
import math                                   # maths tools: math.sin(), math.pi, math.radians()
import Rhino.Geometry as rg                   # Rhino geometry: points, planes, boxes, curves


# --- STEP 1: NEW - a function for the height of the wave at any point along the wall ---
def wave_height_at(x):                        # x = distance along the wall, in mm
    fraction = x / wall_length                # 0.0 at the left end, 1.0 at the right end
    angle = 2 * math.pi * wave_count * fraction + math.radians(wave_shift)  # position on the wave
    return base_height + wave_amplitude * math.sin(angle)  # middle height + up/down swing


# --- STEP 2: PRODUCER - spacing, and how many courses the tallest part needs ---
step_x = wall_length / bricks_per_course      # distance from one brick centre to the next
step_z = brick_height + course_gap            # one brick high plus the joint above it
half_l = brick_length / 2.0                   # half the brick length (for centring)
half_d = brick_depth / 2.0                    # half the brick depth (for centring)
tallest = base_height + abs(wave_amplitude)   # the highest point the wave can reach
courses = int(tallest // step_z) + 1          # enough courses to reach that height

bricks = []                                   # empty list that will hold the bricks
centres = []                                  # empty list that will hold each brick's centre
angles = []                                   # empty list that will hold each brick's angle

# --- STEP 3: PRODUCER - place bricks in stretcher bond, course by course ---
for row in range(courses):                    # repeat once for every course (bottom = 0)
    z = row * step_z                          # height of the bottom of this course
    if row % 2 == 0:                          # even course: 0, 2, 4...
        offset = 0.0                          # starts at the left edge of the wall
        count = bricks_per_course             # full number of bricks
    else:                                     # odd course: 1, 3, 5...
        offset = step_x / 2.0                 # shifted by half a brick (stretcher bond)
        count = bricks_per_course - 1         # one fewer brick so it fits inside the wall

    # --- STEP 4: OPERATOR - the higher the course, the more it rotates (as before) ---
    if courses > 1:                           # more than one course?
        t = row / (courses - 1)               # 0.0 at the bottom, 1.0 at the top
    else:                                     # only one course
        t = 0.0                               # no rotation
    angle = t * max_rotation                  # this course's angle, in degrees

    for i in range(count):                    # repeat once for every brick in the course
        x = offset + step_x / 2.0 + i * step_x  # X of this brick's centre along the wall

        # --- STEP 5: NEW OPERATOR - keep only bricks that sit below the wave ---
        if z + brick_height > wave_height_at(x):  # does the brick's top poke above the wave?
            continue                          # yes: skip it (the hatched area in the sketch)

        # --- STEP 6: CONSUMER - build and rotate each brick (as before) ---
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

# --- STEP 7: NEW CONSUMER - draw the wave so we can compare it with the sketch ---
wave_points = []                              # empty list for points along the wave
samples = 60                                  # how many points to draw the wave with
for k in range(samples + 1):                  # repeat for each sample, including the last end
    x = wall_length * k / samples             # X of this sample along the wall
    wave_points.append(rg.Point3d(x, 0, wave_height_at(x)))  # point on the wave, in the wall's plane
profile = rg.Curve.CreateInterpolatedCurve(wave_points, 3)  # smooth curve through the points

print("{} courses, {} bricks".format(courses, len(bricks)))         # summary in the out panel
print("wave: {:.0f} to {:.0f} mm high".format(base_height - abs(wave_amplitude), tallest))  # wave range
print("top course rotation: {:.0f} deg".format(max_rotation))        # rotation of the top course

# --- OUTPUTS ---
bricks = bricks                               # remaining bricks -> 'bricks' output
centres = centres                             # brick centres -> 'centres' output
angles = angles                               # brick angles -> 'angles' output
profile = profile                             # the wave curve -> 'profile' output
