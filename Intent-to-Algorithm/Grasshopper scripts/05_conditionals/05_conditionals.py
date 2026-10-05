#! python3
# ^ This first line tells the Script component to use Python 3. Never delete it.

# LESSON 05: CONDITIONALS | Rhino 8 Grasshopper Script component (Python 3)
# READ FIRST: 05_conditionals.md in this folder explains the concept, the full component
#             setup, how to run, exercises (Try this) and AI prompts (Ask the AI).
# Example: stacking uses in a mixed-use tower (the Rhino version classifies plots by park distance).
# Inputs:  floors (int, Item), floor_height (float, Item), retail_floors (int, Item),
#          office_top (int, Item), terrace_every (int, Item)
# Outputs: slabs, uses, retail, office, residential, terraces, out


# --- IMPORTS ---------------------------------------------------
import Rhino.Geometry as rg  # Rhino's geometry toolbox, nicknamed 'rg' (lesson 02)


# --- SETTINGS (fixed in the code; the rest come from sliders) --
width = 24.0  # floor plate size along x, metres
depth = 16.0  # floor plate size along y, metres


# --- STEP 1: Comparisons give True or False (see .md → Step 1)
tower_height = floors * floor_height  # total height in metres
print("Exactly 20 storeys?", floors == 20)  # == asks "equal to?" (one = stores, two == compares)
print("Not a single-storey building?", floors != 1)  # != asks "not equal to?"
print("Under the 100 m height limit?", tower_height < 100)  # < asks "less than?"
print("Tall enough to need a second stair (30 m+)?", tower_height >= 30)  # >= "greater than or equal to?"


# --- STEP 2: Combine questions with and / or / not ------------
has_offices = office_top >= retail_floors  # True if at least one office floor fits above the retail
print("Tall AND has offices?", tower_height > 50 and has_offices)  # 'and': BOTH must be True
print("Needs sprinklers?", tower_height >= 30 or has_offices)  # 'or': AT LEAST ONE must be True
print("Purely residential above retail?", not has_offices)  # 'not': flips the answer


# --- STEP 3: if / elif / else on every floor (see .md → Step 3)
all_slabs = []  # every floor outline, bottom to top
all_uses = []  # the use of each floor, same order as all_slabs
retail_slabs = []  # floors sorted into one list per use, so each can be previewed in its own colour
office_slabs = []  # office floors
home_slabs = []  # residential and penthouse floors
terrace_slabs = []  # floors that get a roof terrace

for level in range(floors):  # level counts 0, 1, 2… up to floors - 1 (loops: lesson 06)
    z = level * floor_height  # height of this floor above the ground
    plane = rg.Plane(rg.Point3d(0, 0, z), rg.Vector3d.ZAxis)  # a flat drawing plane at that height
    slab = rg.Rectangle3d(plane, width, depth)  # the floor outline: a width × depth rectangle

    if level < retail_floors:  # RULE 1: the lowest floors are shops, close to the street
        use = "retail"  # the use for this floor
        retail_slabs.append(slab)  # sort the slab into the retail list
    elif level <= office_top:  # RULE 2: next come offices (only checked if rule 1 was False)
        use = "office"  # the use for this floor
        office_slabs.append(slab)  # sort into the office list
    elif level == floors - 1:  # RULE 3: the very top floor is special
        use = "penthouse"  # the use for this floor
        home_slabs.append(slab)  # penthouses are homes too
    else:  # RULE 4: everything else
        use = "residential"  # the use for this floor
        home_slabs.append(slab)  # sort into the homes list

    # --- STEP 4: a rule built from several questions (see .md → Step 4)
    every_nth = level % terrace_every == 0  # % gives the remainder: 0 means "level is a multiple of terrace_every"
    is_home = use == "residential" or use == "penthouse"  # True for both kinds of home
    if every_nth and is_home and level != 0:  # all three must be True
        terrace_slabs.append(slab)  # this floor gets a terrace
        use = use + " + terrace"  # add a note to its label

    all_slabs.append(slab)  # keep every floor
    all_uses.append(f"L{level:02d}: {use}")  # e.g. "L07: office"; :02d pads the number to 2 digits


# --- STEP 5: Report the result --------------------------------
print(f"retail {len(retail_slabs)}, office {len(office_slabs)}, homes {len(home_slabs)}, terraces {len(terrace_slabs)}")  # len() counts items
if len(office_slabs) == 0:  # a single if with no elif/else is fine
    ghenv.Component.AddRuntimeMessage(  # turn the component orange with a message (lesson 03)
        ghenv.Component.RuntimeMessageLevel.Warning,  # level: Warning
        "No office floors: office_top is below retail_floors.")  # the text in the balloon


# --- OUTPUTS: send results out of the component ---------------
slabs = all_slabs  # every floor outline
uses = all_uses  # the label for each floor (connect a Panel)
retail = retail_slabs  # retail floors only
office = office_slabs  # office floors only
residential = home_slabs  # residential + penthouse floors
terraces = terrace_slabs  # floors with a terrace
