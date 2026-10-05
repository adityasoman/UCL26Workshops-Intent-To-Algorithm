#! python3
# ^ This first line tells Rhino 8 to run this file with Python 3. Never delete it.

# LESSON NN: TITLE | Rhino 8 ScriptEditor (Python 3)
# READ FIRST: NN_topic.md in this folder explains the concept, how to run,
#             exercises (Try this) and AI prompts (Ask the AI).


# --- IMPORTS ---------------------------------------------------
import rhinoscriptsyntax as rs  # Rhino's beginner-friendly toolbox (explained in lesson 02)


# --- SETTINGS (change these and run again) --------------------
LESSON_LAYER = "Lesson_NN"  # a text name for the layer this lesson draws on


# --- STEP 0: Prepare a clean layer for this lesson ------------
if not rs.IsLayer(LESSON_LAYER):  # check whether the layer already exists
    rs.AddLayer(LESSON_LAYER)  # if it doesn't, create it
rs.CurrentLayer(LESSON_LAYER)  # make it the active layer so new objects land on it


# --- STEP 1: First idea of the lesson (see .md → Step 1) ------
message = "Template ran successfully"  # store some text in a variable called 'message'
print(message)  # show that text in the Console at the bottom of the ScriptEditor


# --- STEP 2: Next idea ----------------------------------------
# (add code here, one commented line at a time)
