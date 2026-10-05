# Lesson 02 · Import statements

**Environment:** Rhino 8 ScriptEditor (Python 3) · **Code:** [`02_imports.py`](02_imports.py) · **Role:** Producer

## What is this concept?

Python on its own knows only a few basic things. Extra tools are kept in **modules**: toolboxes you can borrow when you need them. An **import statement** says *"bring this toolbox into my script"*.

Almost every script, and nearly all AI-generated code, starts with a few imports. **Reading them tells you which tools the script depends on.**

There are three ways to write an import:

| You write | What it does | Then you use it as |
|---|---|---|
| `import math` | borrow the whole toolbox | `math.sqrt(...)` |
| `import rhinoscriptsyntax as rs` | borrow it and give it a short **nickname** | `rs.AddPoint(...)` |
| `from math import sqrt` | take **one** tool out of the box | `sqrt(...)` |

The dot in `math.sqrt` means *"the sqrt tool that lives inside the math toolbox"*, like *Kitchen > Knife*.

The toolboxes in this lesson:

| Module | Comes with | Used for |
|---|---|---|
| `math` | Python | square roots, pi, angles |
| `random` | Python | random numbers |
| `rhinoscriptsyntax` | Rhino | simple drawing commands |

Later lessons use another Rhino toolbox, `Rhino.Geometry` (also called **RhinoCommon**), for more precise geometry.

## Why does it matter for design?

You don't need to write a square root or a random generator yourself; someone already built and tested them. Knowing **which toolbox to borrow from** lets you spend your effort on the design rules instead.

## Where this sits in Producer → Operator → Consumer

| Role | Meaning |
|---|---|
| **Producer** | reads or creates information |
| Operator | applies rules to that information |
| Consumer | turns the result into geometry or colour |

This lesson is mainly a **Producer**. We create a random scatter of plots on a site and measure how far each one is from a park.

## How to run

1. Open `02_imports.py` in the ScriptEditor (command: `ScriptEditor`).
2. Press the green **Run** button (or **F5**).
3. You should see a park label and 10 scattered points on layer `Lesson_02`, and each plot's distance to the park in the Console.

> **Note:** normally **all imports go together at the very top** of a file. In this lesson we bring them in one at a time, so you can see what each one adds.

## Step by step

| Step | Import | What to point out |
|---|---|---|
| 1 | `import rhinoscriptsyntax as rs` | A nickname saves typing. `rs.IsLayer` reads as "the IsLayer tool from the rs toolbox". |
| 2 | `import math` | `math.pi` is a value stored in the toolbox. `dir(math)` lists everything inside, which is handy for exploring. Distance uses Pythagoras: `**` means "to the power of". The test plot is exactly **50.0 m** from the park. |
| 3 | `from math import sqrt` | Same answer, shorter to write. Trade-off: `sqrt(...)` is shorter, but `math.sqrt(...)` shows where the tool came from. `rs.Distance` gives the same 50.0 m: different toolboxes can do the same job. |
| 4 | `import random` | `random.seed(seed)` fixes the random sequence, so the same seed gives the same scatter every run. `random.uniform(a, b)` gives any decimal between a and b. |
| 5 | all together | The `for` loop repeats the indented lines `count` times. Loops are taught properly in lesson 06; for now read it as "do this 10 times". |
| 6 | a missing toolbox | `numpy` is a popular maths toolbox but is **not installed in Rhino by default**. Uncommenting `import numpy` gives `ModuleNotFoundError: No module named 'numpy'`. AI tools often add imports like this. If you see that error, ask the AI to *"use only the Python standard library and rhinoscriptsyntax"*. |

## Try this

1. Change `seed` to `2` and run. Then change it back to `1`. Is the scatter exactly the same as before?
2. Change `count` to `50` and `site_size` to `200.0`.
3. Change `import math` to `import math as m`. What else must you change for the script to run again?
4. Uncomment the `import numpy` line and read the error in the Console.

## Ask the AI

Paste one of these into any AI chat tool. See [`Prompt guidelines`](../../Prompt%20guidelines/README.md) for more.

```text
I'm learning Python in the Rhino 8 ScriptEditor (Python 3).
Explain the difference between 'import math', 'import math as m' and
'from math import sqrt'. When would I choose each?
```

```text
List the most useful tools in Python's random module for scattering points
on an architectural site, with one sentence each. Only the standard library,
no numpy.
```

```text
Here are the imports at the top of a script an AI gave me: <paste them>.
For each one, tell me what it's for and whether it is available in
Rhino 8 Python 3 by default.
```
