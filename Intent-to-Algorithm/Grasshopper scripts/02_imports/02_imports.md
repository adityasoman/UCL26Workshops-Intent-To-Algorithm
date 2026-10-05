# Lesson 02 · Import statements

**Environment:** Rhino 8 Grasshopper, Script component (Python 3) · **Code:** [`02_imports.py`](02_imports.py) · **Role:** Producer

## What is this concept?

Python on its own knows only a few basic things. Extra tools are kept in **modules**: toolboxes you can borrow when you need them. An **import statement** says *"bring this toolbox into my script"*.

Almost every script, and nearly all AI-generated code, starts with a few imports. **Reading them tells you which tools the script depends on.**

There are three ways to write an import:

| You write | What it does | Then you use it as |
|---|---|---|
| `import math` | borrow the whole toolbox | `math.sqrt(...)` |
| `import Rhino.Geometry as rg` | borrow it and give it a short **nickname** | `rg.Point3d(...)` |
| `from math import sqrt` | take **one** tool out of the box | `sqrt(...)` |

The dot in `math.sqrt` means *"the sqrt tool that lives inside the math toolbox"*, like *Kitchen > Knife*.

The toolboxes in this lesson:

| Module | Comes with | Used for |
|---|---|---|
| `math` | Python | square roots, pi, angles |
| `random` | Python | random numbers |
| `Rhino.Geometry` | Rhino | geometry objects such as points (also called **RhinoCommon**, see lesson 07) |
| `rhinoscriptsyntax` | Rhino | simple commands; we only borrow its distance tool here |

## Why does it matter for design?

You don't need to write a square root or a random generator yourself; someone already built and tested them. Knowing **which toolbox to borrow from** lets you spend your effort on the design rules instead.

## Where this sits in Producer → Operator → Consumer

| Role | Meaning |
|---|---|
| **Producer** | reads or creates information |
| Operator | applies rules to that information |
| Consumer | turns the result into geometry or colour |

This lesson is mainly a **Producer**. We create a random scatter of plots on a site and measure how far each one is from a park.

## Component setup

Zoom in on the component and use **⊕ / ⊖** to add or remove parameters. Right-click each one to rename it, set its **Type hint**, and set **Item** or **List Access**.

**Inputs**

| Name | Type hint | Access | Connect to |
|---|---|---|---|
| `count` | `int` | Item Access | Number Slider, 1–200, default 10 |
| `seed` | `int` | Item Access | Number Slider, 0–100, default 1 |

**Outputs**

| Name | Type | Notes |
|---|---|---|
| `points` | list of Point3d | the scattered plots |
| `park_point` | Point3d | the park |
| `distances` | list of float | each plot's distance to the park; connect a Panel |
| `out` | built-in | `print()` messages; connect a Panel |

## How to run

1. Place a **Python 3 Script** component (Maths tab → Script panel).
2. Set up the inputs and outputs exactly as listed above.
3. Double-click the component, paste the whole `.py` file, then **Run**.
4. You should see 10 scattered points and a park point in Rhino, and their distances in the `distances` Panel. Move the `seed` slider away and back: the scatter comes back exactly the same.

> **Note:** normally **all imports go together at the very top** of a file. In this lesson we bring them in one at a time, so you can see what each one adds.

## Step by step

| Step | Import | What to point out |
|---|---|---|
| 1 | `import Rhino.Geometry as rg` | A nickname saves typing. `rg.Point3d` reads as "the Point3d tool from the rg toolbox". |
| 2 | `import math` | `math.pi` is a value stored in the toolbox. `dir(math)` lists everything inside, which is handy for exploring. Distance uses Pythagoras: `**` means "to the power of". The test plot is exactly **50.0 m** from the park. |
| 3 | `from math import sqrt` | Same answer, shorter to write. Trade-off: `sqrt(...)` is shorter, but `math.sqrt(...)` shows where the tool came from. `rs.Distance` gives the same 50.0 m: different toolboxes can do the same job. |
| 4 | `import random` | `random.seed(seed)` fixes the random sequence. **Grasshopper re-runs the script every time an input changes**, so seeding keeps the result stable. `random.uniform(a, b)` gives any decimal between a and b. |
| 5 | all together | The `for` loop repeats the indented lines `count` times. Loops are taught properly in lesson 06. `.append()` adds an item to the end of a list. |
| 6 | a missing toolbox | `numpy` is a popular maths toolbox but is **not installed in Rhino by default**. Uncommenting `import numpy` turns the component red with `ModuleNotFoundError: No module named 'numpy'`. AI tools often add imports like this. If you see that error, ask the AI to *"use only the Python standard library and Rhino.Geometry"*. |

## Try this

1. Move the `seed` slider to 2, then back to 1. Is the scatter exactly the same as before?
2. Move the `count` slider to 200. Connect `points` to a **Point List** or **Text Tag** component to see the numbering.
3. Change `import math` to `import math as m`. Which line turns the component red, and why?
4. Uncomment the `import numpy` line and read the error in `out`.

## Ask the AI

Paste one of these into any AI chat tool. See [`Prompt guidelines`](../../Prompt%20guidelines/README.md) for more.

```text
I'm learning Python in a Rhino 8 Grasshopper Script component (Python 3).
Explain the difference between 'import math', 'import math as m' and
'from math import sqrt'. When would I choose each?
```

```text
What's the difference between rhinoscriptsyntax and Rhino.Geometry when I
use them inside a Grasshopper Python 3 Script component? Explain for a
beginner, no code yet.
```

```text
Here are the imports at the top of a script an AI gave me: <paste them>.
For each one, tell me what it's for and whether it is available in
Rhino 8 Python 3 by default.
```
