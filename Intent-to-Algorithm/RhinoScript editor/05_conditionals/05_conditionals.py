#! python3
# ^ This first line tells Rhino 8 to run this file with Python 3. Never delete it.

# LESSON 05: CONDITIONALS | Rhino 8 ScriptEditor (Python 3)
# READ FIRST: 05_conditionals.md in this folder explains the concept, how to run,
#             exercises (Try this) and AI prompts (Ask the AI).


# --- IMPORTS ---------------------------------------------------
import rhinoscriptsyntax as rs  # Rhino's beginner-friendly toolbox (lesson 02)


# --- SETTINGS (change these and run again) --------------------
LESSON_LAYER = "Lesson_05"  # the layer this lesson draws on
park = [50.0, 50.0, 0.0]  # the park sits in the middle of the site
green_radius = 30.0  # DESIGN RULE: plots closer than this to the park stay green
low_radius = 48.0  # DESIGN RULE: plots closer than this become low-rise; further away, high-rise
low_height = 9.0  # height of a low-rise block, metres (3 storeys)
high_height = 36.0  # height of a high-rise tower, metres (12 storeys)
plot_size = 10.0  # each plot is plot_size × plot_size metres
plots = [  # a short, hand-typed list of plot centres (lesson 06 generates these with a loop)
    [45.0, 60.0, 0.0], [70.0, 55.0, 0.0], [20.0, 40.0, 0.0], [85.0, 85.0, 0.0],
    [10.0, 10.0, 0.0], [55.0, 25.0, 0.0], [95.0, 40.0, 0.0], [30.0, 80.0, 0.0],
    [60.0, 95.0, 0.0], [5.0, 60.0, 0.0], [40.0, 45.0, 0.0], [90.0, 5.0, 0.0],
]


# --- STEP 0: Prepare a clean layer for this lesson ------------
if not rs.IsLayer(LESSON_LAYER):  # 'not' flips True to False: "if the layer does NOT exist"
    rs.AddLayer(LESSON_LAYER)  # then create it
rs.CurrentLayer(LESSON_LAYER)  # make it the active layer
rs.AddTextDot("Park", park)  # label the park
green_ring = rs.AddCircle(park, green_radius)  # show RULE 1's boundary as a circle around the park
rs.ObjectColor(green_ring, (60, 170, 60))  # green
low_ring = rs.AddCircle(park, low_radius)  # show RULE 2's boundary
rs.ObjectColor(low_ring, (240, 170, 40))  # orange


# --- STEP 1: Comparisons give True or False (see .md → Step 1)
floors = 12  # a test tower
print("Is it exactly 12 storeys?", floors == 12)  # == asks "equal to?" (one = stores, two == compares)
print("Is it NOT 10 storeys?", floors != 10)  # != asks "not equal to?"
print("Is it under the 20-storey limit?", floors < 20)  # < asks "less than?"
print("Does it need a lift (4+ storeys)?", floors >= 4)  # >= asks "greater than or equal to?"


# --- STEP 2: Combine questions with and / or / not ------------
is_residential = True  # from lesson 01: a bool
has_garden = False  # another bool
print("Tall housing?", floors > 8 and is_residential)  # 'and': BOTH must be True
print("Needs outdoor space?", has_garden or floors > 10)  # 'or': AT LEAST ONE must be True
print("Missing a garden?", not has_garden)  # 'not': flips the answer


# --- STEP 3: if / elif / else: one rule, one plot (see .md → Step 3)
test_distance = rs.Distance(plots[0], park)  # how far the first plot is from the park
if test_distance < green_radius:  # IF this question is True, run the indented line below…
    print("Plot 0 is green space")  # …and skip the rest of the chain
elif test_distance < low_radius:  # ELSE IF: only asked when the first question was False
    print("Plot 0 is low-rise")  # runs only if this plot is between the two radii
else:  # ELSE: runs when every question above was False
    print("Plot 0 is high-rise")  # runs only if both questions were False


# --- STEP 4: Apply the rule to every plot (see .md → Step 4) --
green_count = 0  # counters start at zero…
low_count = 0  # …and go up by one each time a plot falls in that class
high_count = 0  # (three separate counters, one per class)
for plot in plots:  # repeat for each plot in the list (loops: lesson 06)
    d = rs.Distance(plot, park)  # measure this plot to the park
    if d < green_radius:  # RULE 1: close to the park → keep it green
        label = "green"  # the class name, used for the label
        colour = (60, 170, 60)  # (red, green, blue), each 0–255
        height = 0.0  # nothing is built on a green plot
        green_count = green_count + 1  # one more green plot
    elif d < low_radius:  # RULE 2: middle distance → low-rise
        label = "low-rise"  # the class name
        colour = (240, 170, 40)  # orange
        height = low_height  # a short block
        low_count = low_count + 1  # one more low-rise plot
    else:  # RULE 3: everything else → high-rise
        label = "high-rise"  # the class name
        colour = (200, 50, 50)  # red
        height = high_height  # a tower
        high_count = high_count + 1  # one more high-rise plot

    # --- draw the result of the rule (see .md → Step 4) ---
    x0 = plot[0] - plot_size / 2  # south-west corner of the plot, x (the point is the plot's centre)
    y0 = plot[1] - plot_size / 2  # south-west corner of the plot, y
    x1 = x0 + plot_size  # north-east corner, x
    y1 = y0 + plot_size  # north-east corner, y
    if height > 0:  # a second, separate decision: is there anything to build?
        shape_id = rs.AddBox([[x0, y0, 0], [x1, y0, 0], [x1, y1, 0], [x0, y1, 0],  # bottom 4 corners
                              [x0, y0, height], [x1, y0, height], [x1, y1, height], [x0, y1, height]])  # top 4 corners
    else:  # green plot: no building, just a flat square of lawn
        shape_id = rs.AddSrfPt([[x0, y0, 0], [x1, y0, 0], [x1, y1, 0], [x0, y1, 0]])  # a flat surface from 4 corners
    rs.ObjectColor(shape_id, colour)  # paint it in its class colour
    rs.AddTextDot(label, [plot[0], plot[1], height])  # write the class on top
    print(f"{plot[:2]} → {round(d, 1)} m → {label}")  # [:2] shows only x and y


# --- STEP 5: Report the result --------------------------------
print(f"green: {green_count}, low-rise: {low_count}, high-rise: {high_count}")  # the counts
if high_count == 0:  # a single if with no elif/else is fine too
    print("Warning: no plots are far enough from the park for high-rise.")  # only printed when the count is 0

rs.ZoomExtents()  # zoom to see everything
