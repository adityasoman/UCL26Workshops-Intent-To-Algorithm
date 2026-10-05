# Lesson 06 · Loops

**Environment:** Rhino 8 Grasshopper, Script component (Python 3) · **Code:** [`06_loops.py`](06_loops.py) · **Role:** Producer + Consumer

> **Different example from the Rhino version.** The RhinoScript editor lesson makes a **site grid** and a **tower that grows to a height limit**. This one makes a **twisting tower**, a **façade panel grid** and a **staircase** that works out its own number of steps. The concept is the same, so you get two examples to compare.

## What is this concept?

A **loop** repeats the same lines many times. It's how one rule produces forty floors or two hundred façade panels.

There are two kinds:

| Loop | Means | Use it when |
|---|---|---|
| `for` | "for **each** item, do this" | you know what to repeat over: a count, a list |
| `while` | "**keep going while** this is true" | you don't know how many repeats in advance: "add risers until each one is low enough" |

```python
for level in range(floors):                      # each floor…
    angle = math.radians(level * twist)          # …turns a bit more

while storey_height / riser_count > max_riser:   # still too steep?
    riser_count = riser_count + 1                # add a riser: move towards the stop
```

Useful tools that come with loops:

| Tool | Does | Example |
|---|---|---|
| `range(n)` | the numbers 0 … n−1 | `range(3)` → 0, 1, 2 |
| `list.append(x)` | add `x` to the end of a list | `panels.append(panel)` |
| `len(list)` | how many items | `len(panels)` → 160 |

## Why does it matter for design?

Most design systems are **repetitive with variation**: floors that rotate a little each time, panels across a façade, steps up a stair. Loops let you write the rule once and apply it everywhere, and with sliders you can explore the whole family of designs.

## Where this sits in Producer → Operator → Consumer

| Role | Meaning |
|---|---|
| **Producer** | reads or creates information |
| Operator | applies rules to that information |
| **Consumer** | turns the result into geometry or colour |

This lesson is a **Producer + Consumer**: loops produce positions and counts, and turn them straight into geometry.

## Component setup

Zoom in on the component and use **⊕ / ⊖** to add or remove parameters. Right-click each one to rename it, set its **Type hint**, and set **Item** or **List Access**.

**Inputs**

| Name | Type hint | Access | Connect to |
|---|---|---|---|
| `floors` | `int` | Item Access | Number Slider, 1–60, default 25 |
| `twist` | `float` | Item Access | Number Slider, 0.0–10.0, default 3.0 (degrees per floor) |
| `columns` | `int` | Item Access | Number Slider, 1–40, default 16 |
| `rows` | `int` | Item Access | Number Slider, 1–20, default 10 |
| `storey_height` | `float` | Item Access | Number Slider, 2.5–6.0, default 3.2 |
| `max_riser` | `float` | Item Access | Number Slider, 0.12–0.25, default 0.18 |

**Outputs**

| Name | Type | Notes |
|---|---|---|
| `slabs` | list of Rectangle3d | the twisting tower's floors |
| `panels` | list of Rectangle3d | the façade grid |
| `steps` | list of Box | the staircase |
| `info` | str | one-line summary; connect a Panel |
| `out` | built-in | `print()` messages; connect a Panel |

## How to run

1. Place a **Python 3 Script** component (Maths tab → Script panel).
2. Set up the inputs and outputs exactly as listed above.
3. Double-click the component, paste the whole `.py` file, then **Run**.
4. You should see a twisting stack of floors at the origin, a grid of panels on a wall in front of it, and a staircase beside it. Move `twist`, `columns` and `max_riser` and watch each part update.

## Step by step

### Step 1 · `for` + `range`
`range` **starts at 0** and **stops before** the end number. Floor 0 doesn't turn; floor 1 turns `twist` degrees; floor 10 turns `10 × twist`. `math.radians` converts degrees to the radians Rhino expects.

### Step 2 · `for` over a list
You can loop directly over a list. The loop variable (`slab`) takes each item in turn. Choose a name that reads well: `for slab in slabs`, `for panel in panels`.

### Step 3 · Nested loops
The **inner** loop runs completely for **every** pass of the outer loop: 16 columns × 10 rows = 160 panels. Each panel is drawn on an upright plane (x across, z up), at 90% size so you can see the joints.

> Grasshopper has its own way of handling lists of lists, called **DataTrees**. They're outside this workshop. Here we keep everything in one flat list.

### Step 4 · `while`
How many steps does a stair need? You don't know in advance, so start with one riser and keep adding one **while** each riser is still too high. Two safety rules:

1. **Something inside the loop must move towards the stop.** Here `riser_count` grows every time, so the riser height keeps getting lower.
2. **Add a hard cap.** `riser_count < MAX_STEPS` stops the loop even if the main condition is wrong (for example if `max_riser` were 0).

> ⚠️ **An infinite loop freezes Grasshopper and Rhino.** Grasshopper re-runs your script on every slider move, so a bad `while` loop can lock things up the moment you touch a slider. Always add a cap.

### Step 5 · `while` then `for`
The `while` loop **found** a number; the `for` loop **uses** it to build the steps. Each step is a box from the ground up to its tread, one tread further along and one riser higher.

## Try this

1. Set `twist` to 0, then to 90. What happens at exactly 90° on a square plate?
2. Change the panel size to `panel_w * 0.5`. What kind of façade does it suggest?
3. Lower `max_riser` to 0.15. How many more steps do you need?
4. Make every second floor of the tower turn the other way. (Hint: `if level % 2 == 0:` from lesson 05.)

## Ask the AI

Paste one of these into any AI chat tool. See [`Prompt guidelines`](../../Prompt%20guidelines/README.md) for more.

```text
I'm learning Python in a Rhino 8 Grasshopper Script component (Python 3).
Explain step by step what these nested loops do, pass by pass, for
columns = 2 and rows = 3: <paste step 3>
```

```text
Change my twisting tower so floors also get smaller towards the top
(a taper). Add a 'taper' slider input, use Rhino.Geometry only,
comment every line. <paste step 1>
```

```text
Look at this while loop: <paste step 4>. List every way it could run
forever, and how the code guards against each one.
```
