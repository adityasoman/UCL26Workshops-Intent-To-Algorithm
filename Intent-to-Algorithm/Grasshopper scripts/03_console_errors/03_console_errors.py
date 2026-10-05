#! python3
# ^ This first line tells the Script component to use Python 3. Never delete it.

# LESSON 03: CONSOLE ERRORS | Rhino 8 Grasshopper Script component (Python 3)
# READ FIRST: 03_console_errors.md in this folder explains how to read errors and component
#             colours, the full component setup, each BREAK IT block, and AI prompts.
# Inputs:  floors (int, Item), floor_height (float, Item)
# Outputs: tower, info, out


# --- IMPORTS ---------------------------------------------------
import Rhino.Geometry as rg  # Rhino's geometry toolbox, for making the box
import Grasshopper  # Grasshopper's own toolbox, needed to send our own warning to the component


# --- SETTINGS (fixed in the code; floors and floor_height come from the sliders)
name = "Tower A"  # the tower's name (str)
width = 20.0  # footprint size along x, in metres
depth = 15.0  # footprint size along y, in metres
origin = [0.0, 0.0, 0.0]  # where the tower's corner sits (x, y, z)
height_limit = 60.0  # a planning rule: towers above this height get a warning


# --- STEP 1: A working tower (this part has no mistakes) ------
height = floors * floor_height  # total height in metres

x = origin[0]  # the tower's corner, x
y = origin[1]  # the tower's corner, y
z = origin[2]  # the tower's corner, z
tower_box = rg.Box(  # make a box from a base plane and three size ranges (RhinoCommon: lesson 07)
    rg.Plane.WorldXY,  # the box sits on the world ground plane
    rg.Interval(x, x + width),  # it spans from x to x + width
    rg.Interval(y, y + depth),  # from y to y + depth
    rg.Interval(z, z + height),  # and from the ground up to the tower's height
)  # the closing bracket ends the Box(...) instruction

print(f"{name}: {floors} floors, {height} m tall")  # report what we built in 'out'


# --- STEP 2: Your own warning, turns the component ORANGE (see .md → Step 2)
if height > height_limit:  # "if the tower is too tall…" (if statements: lesson 05)
    ghenv.Component.AddRuntimeMessage(  # ghenv = this component; AddRuntimeMessage adds a balloon message
        Grasshopper.Kernel.GH_RuntimeMessageLevel.Warning,  # the level: Warning = orange (Error would be red)
        f"{name} is {height} m, above the {height_limit} m limit",  # the text shown in the balloon
    )  # closes the AddRuntimeMessage(...) instruction


# --- STEP 3: BREAK IT (see .md → Break it) --------------------
# Uncomment ONE marked line at a time (delete its "# "), run, read the error, then re-comment it.
print("Starting the BREAK IT section")  # a normal line at the left edge, so we can see where errors stop the script

# ---- BREAK IT 1: SyntaxError (.md → Break it 1) ----
# print("Tower A is tall)

# ---- BREAK IT 2: IndentationError (.md → Break it 2) ----
#     print("This line starts with spaces for no reason")

# ---- BREAK IT 3: NameError (.md → Break it 3) ----
# print(Floors)

# ---- BREAK IT 4: TypeError (.md → Break it 4) ----
# label = "Height: " + height

# ---- BREAK IT 5: IndexError (.md → Break it 5) ----
# w = origin[3]

# ---- BREAK IT 6: AttributeError (.md → Break it 6) ----
# shout = name.uppercase()


# --- OUTPUTS: send results out of the component ---------------
tower = tower_box  # the box leaves through the 'tower' output
info = f"{name}: {height} m tall. Script finished without errors"  # if you see this, nothing above stopped the script
