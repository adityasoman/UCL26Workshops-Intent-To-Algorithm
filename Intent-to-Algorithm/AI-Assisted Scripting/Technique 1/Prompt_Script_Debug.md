# Technique 1: Prompt → Script → Debug

> **In one line:** ask an AI agent for a Grasshopper Python script, paste it into a component, wire it up, and send any errors back to the agent until it works.

---

## The loop

```
   ┌──────────┐      ┌──────────┐      ┌──────────┐
   │  PROMPT  │ ───► │  SCRIPT  │ ───► │  DEBUG   │
   │ ask the  │      │ paste +  │      │ errors?  │
   │  agent   │      │  wire up │      │ send back│
   └──────────┘      └──────────┘      └────┬─────┘
        ▲                                   │
        └───────────── repeat ──────────────┘
```

1. **Prompt:** describe what you want clearly, including *where* the code will run.
2. **Script:** copy the code into a Grasshopper **Python 3 Script** component and create the inputs and outputs it needs.
3. **Debug:** if the component turns **red** or **orange**, or the geometry looks wrong, copy the error back to the agent and ask for a fix. Repeat until it works.

You are not expected to write the code yourself. You **are** expected to set up the component correctly, read the error, and tell the agent exactly what happened.

---

## The task

Build a Grasshopper Python script that:

- makes a **grid of points**,
- places a **box** on each point,
- uses an **attractor point** to change each box's **height** and **rotation**: boxes near the attractor are taller and more rotated than boxes far away.

| Role | What it does in this script |
|------|-----------------------------|
| **Producer** | creates the grid of points |
| **Operator** | measures each point's distance to the attractor and remaps it to a height and an angle |
| **Consumer** | builds the rotated boxes |

---

## Step 1: Prompt

Copy this prompt into your AI agent (Claude, ChatGPT, Copilot, Gemini…) exactly as written.

```text
Write a Python script for the Grasshopper "Python 3 Script" component in Rhino 8.

What the script should do:
- Create a grid of points on the XY plane.
- Place a box on each grid point.
- Use an attractor point to control each box:
  boxes closer to the attractor are TALLER and MORE ROTATED,
  boxes further away are shorter and less rotated.
- Rotate each box around its own centre, about the Z axis.

Inputs I want as component parameters:
- count_x (int): number of points in X
- count_y (int): number of points in Y
- spacing (float): distance between points
- box_size (float): width and depth of each box
- attractor (Point3d): the attractor point, which I will set in Rhino
- min_height, max_height (float): the height range of the boxes
- max_rotation (float): the largest rotation, in degrees

Outputs I want:
- points: the grid points
- boxes: the box geometry
- heights: the height of each box

Rules:
- Python 3 only (start the script with #! python3). Not IronPython or GhPython.
- Use only Rhino.Geometry and the Python standard library (math). No rhinoscriptsyntax, no numpy.
- Return Rhino.Geometry objects, not GUIDs.
- Use simple, readable code with a short comment on every line. I am a beginner.
- If the attractor is not connected, show a warning on the component instead of crashing.

Before the code, give me a table of the component inputs with:
Name | Type hint | Access (Item or List) | What to connect (slider range or Rhino point).
Then list the output names.
```

> **Tip:** asking for the **table first** is the most important part. It tells you exactly how to set up the component in Step 2.

---

## Step 2: Script

### 2a. Place the component

1. In Grasshopper, double-click the canvas and type **`Python 3 Script`**. Place it.
2. Double-click the component to open the script editor.
3. Delete what's there, paste the agent's code, then click **OK**.

### 2b. Create the inputs

The component starts with inputs `x`, `y` and outputs `out`, `a`. You need to match the agent's table.

1. **Zoom in** on the component until you see small **⊕** and **⊖** signs at the inputs.
2. Click **⊕** to add inputs until there are **8**.
3. **Right-click each input → rename it** to match the table *exactly* (`count_x`, `count_y`, `spacing`, …). Names are case-sensitive.
4. **Right-click each input → Type hint** and pick the type from the table (`int`, `float`, `Point3d`).
5. Check **Item Access** is ticked (it is the default) for every input in this exercise.

### 2c. Create the outputs

1. Zoom in and click **⊕** on the output side to add outputs.
2. Rename them `points`, `boxes`, `heights`.
3. **Keep `out`**: it shows anything the script prints, plus error messages. Never rename it.

### 2d. Connect the inputs

The agent's table should look roughly like this. Use it to check what you were given.

| Name | Type hint | Access | Connect to |
|------|-----------|--------|------------|
| `count_x` | int | Item | Number Slider, integer, 2 – 30, start 10 |
| `count_y` | int | Item | Number Slider, integer, 2 – 30, start 10 |
| `spacing` | float | Item | Number Slider, 1 – 10, start 4 |
| `box_size` | float | Item | Number Slider, 0.5 – 5, start 2 |
| `attractor` | Point3d | Item | **Point** component → right-click → *Set one Point* → click in Rhino |
| `min_height` | float | Item | Number Slider, 0.5 – 5, start 1 |
| `max_height` | float | Item | Number Slider, 5 – 30, start 15 |
| `max_rotation` | float | Item | Number Slider, 0 – 90, start 45 |

Then connect a **Panel** to `out`, and look at `boxes` in the Rhino viewport. Move the attractor point in Rhino and the boxes should update.

---

## Step 3: Debug

It is normal for the first try not to work. The colour of the component tells you what happened:

| Colour | Meaning | What to do |
|--------|---------|-----------|
| **Grey** | It ran | Check the geometry looks right |
| **Orange** | Warning: it ran but something is missing or odd | Hover over the balloon and read the message |
| **Red** | Error: it crashed | Read the error in the balloon or the `out` panel |

### How to send an error back

Give the agent **three things**: the exact error, what you did, and what you expected. Use this prompt:

```text
The script gave this error in Grasshopper:

[paste the full error message from the red balloon or the out panel]

My component inputs are: [list the names and type hints you set up].
I expected: [what you thought would happen].
I see: [what actually happens].

Explain in one or two sentences what caused the error, then give me
the full corrected script. Keep the same input and output names.
```

> **Don't** just say *"it doesn't work"*. The agent can only fix what you tell it.

### Errors you are likely to see in this exercise

| Error / symptom | Usual cause | Fix it yourself, or tell the agent |
|-----------------|-------------|-------------------------------------|
| `NameError: name 'count_x' is not defined` | An input name doesn't match the code (typo or wrong case) | Rename the input to match the code exactly |
| `AttributeError: 'NoneType' object has no attribute 'DistanceTo'` | The attractor isn't connected, or its Point component is empty | Connect a Point and *Set one Point* in Rhino |
| `System.Guid value cannot be converted to Rhino.Geometry.Point3d in method Double DistanceTo(...)` | The `attractor` input has no type hint, so Grasshopper sends the Rhino point's **ID** (a GUID) instead of the point | Right-click `attractor` → **Type hint → Point3d** |
| `TypeError: 'float' object cannot be interpreted as an integer` | `count_x` / `count_y` arrived as decimals | Set the type hint to `int` and make the slider integer-only |
| Boxes are all the same height | The remap divides by zero, or max distance is wrong | Send the agent the code and say *"all boxes are the same height"* |
| Boxes rotate around the origin, not their own centre | Rotation uses the wrong centre point | Tell the agent *"rotate each box around its own centre"* |
| Rotation looks huge or random | Degrees passed where radians are expected | Tell the agent *"use math.radians for the rotation"* |
| `boxes` output shows GUIDs / nothing in the viewport | The code used `rhinoscriptsyntax` | Remind the agent: *"return Rhino.Geometry objects only"* |
| `ModuleNotFoundError: No module named 'numpy'` | The agent used a third-party library | Remind the agent: *"standard library and Rhino.Geometry only"* |
| `SyntaxError` on a `print` line | The code is old IronPython 2 style | Remind the agent: *"Python 3 for Rhino 8"* |

---

## Once it works

Try these follow-up prompts, one at a time, and repeat the Script → Debug steps after each:

1. `Colour the boxes from blue (far) to red (near the attractor). Add a colours output.`
2. `Let me connect several attractor points instead of one. Use the closest one for each box.`
3. `Make the boxes taper: the top face should be smaller than the bottom face.`
4. `Explain the line that calculates the height, as if I've never used Python.`

---

## Check yourself

- [ ] My prompt said **where** the code runs (Grasshopper, Python 3, Rhino 8) and named every input and output.
- [ ] My component's input names and type hints match the code exactly.
- [ ] When I got an error, I sent the agent the **exact message**, not just "it's broken".
- [ ] Moving the attractor in Rhino changes the heights and rotations of the boxes.
- [ ] I can point to the part of the code that is the Producer, the Operator and the Consumer.

---

## Tutor reference

A working version of this script is in [`Prompt_Script_Debug.py`](Prompt_Script_Debug.py) in this folder. Students should try the loop with their own agent first, then compare their result with it.
