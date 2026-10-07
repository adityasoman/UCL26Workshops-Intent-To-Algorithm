#! python3
# ^ This first line tells the Script component to use Python 3. Never delete it.

# LESSON 00: HELLO WORLD | Rhino 8 Grasshopper Script component (Python 3)
# READ FIRST: 00_hello_world.md in this folder explains the concept, the full component
#             setup, how to run, exercises (Try this) and AI prompts (Ask the AI).
# Inputs:  name (str, Item)
# Outputs: info, out


# --- STEP 1: Read the name typed into the Panel ---------------
if not name:  # if the Panel is empty or not connected… (if statements: lesson 05)
    name = "World"  # …use "World" instead, so the script still works


# --- STEP 2: Say hello ----------------------------------------
message = "Hello " + name + ", welcome to the Python workshop!"  # + joins pieces of text into one
print(message)  # show the message on the 'out' output


# --- OUTPUTS: send results out of the component ---------------
info = message  # 'info' matches an output name, so this text leaves through that output
