# Lesson 07 · Classes and RhinoCommon

**Environment:** Rhino 8 ScriptEditor (Python 3) · **Code:** [`07_classes.py`](07_classes.py) · **Role:** Operator + Consumer

## What is this concept?

This lesson has two new ideas.

### 1. Classes

A **class** is a blueprint for a kind of thing. It bundles **data** (what the thing *is*) with **behaviour** (what it can *do*).

Think of a **building type** versus **built buildings**. "Mid-rise housing block" is a type: it says every block has a footprint, a number of floors and a storey height. Each actual block on site is an **instance** of that type, with its own values.

| Word | Meaning | In this lesson |
|---|---|---|
| **class** | the blueprint / building type | `class Building:` |
| **instance** | one actual thing made from the blueprint | `library`, `housing`, `office` |
| **attribute** | a value an instance stores about itself | `self.floors`, `self.width` |
| **method** | a function that belongs to the class | `height()`, `to_box()`, `describe()` |
| `__init__` | the set-up method that runs when an instance is made | fills in the attributes |
| `self` | "this particular instance" | inside `height()`, `self.floors` means *this* building's floors |

```python
housing = Building("Housing", 40, 0, 15, 15, 12)   # make an instance (runs __init__)
housing.floors                                     # read an attribute: no brackets
housing.height()                                   # run a method: brackets
```

### 2. RhinoCommon (`Rhino.Geometry`)

Until now we've used `rhinoscriptsyntax` (`rs`). From now on we'll mostly use **RhinoCommon**, Rhino's full geometry library.

| | `rhinoscriptsyntax` (`rs`) | RhinoCommon (`Rhino.Geometry`, `rg`) |
|---|---|---|
| Style | simple commands: `rs.AddBox(corners)` | geometry **objects**: `rg.Box(...)` |
| Gives you back | an **ID** of an object already in the document | the **geometry itself**, not yet in the document |
| Points | lists `[x, y, z]` | `rg.Point3d(x, y, z)` with `.X`, `.Y`, `.Z` |
| Good for | quick scripts, beginners | Grasshopper, precise work, most AI-generated code |

`rs` is actually built *on top of* RhinoCommon. RhinoCommon lets you build and test geometry **before** adding it to the document, which is exactly what Grasshopper needs. To add RhinoCommon geometry to Rhino you use `scriptcontext`: `sc.doc.Objects.AddBox(box)`.

## Why does it matter for design?

Real design systems have many kinds of objects (plots, buildings, rooms, façades), each with data and rules. Classes keep each object's data and rules together, so large scripts stay readable. AI tools very often answer with classes, so you need to be able to read them.

## Where this sits in Producer → Operator → Consumer

| Role | Meaning |
|---|---|
| Producer | reads or creates information |
| **Operator** | applies rules to that information |
| **Consumer** | turns the result into geometry or colour |

This lesson is an **Operator + Consumer**: methods like `height()` and `floor_area()` apply rules, and `to_box()` turns a building into geometry.

## How to run

1. Open `07_classes.py` in the ScriptEditor (command: `ScriptEditor`).
2. Press the green **Run** button (or **F5**).
3. You should see three boxes of different sizes on layer `Lesson_07`, each labelled, and a description of each building in the Console.

## Step by step

### Step 1 · RhinoCommon objects
A `Point3d` knows its own coordinates: `corner.X` instead of `corner[0]`. An `Interval` is a range from one number to another, with a `.Length`. Objects carry their own **properties**.

### Step 2 · The class
- `class Building:` starts the blueprint. Everything indented belongs to it.
- `__init__` (two underscores each side) runs automatically when you make a building. It copies the arguments into `self.<name>` so the building remembers them.
- Every method has `self` as its first parameter. You never pass it yourself; Python fills it in.
- `to_box()` builds an `rg.Box` from a plane and three `Interval`s: x range, y range, z range.

### Step 3 · Instances
`Building("Library", 0, 0, 30, 20, 4, floor_height=4.5)` makes one building. Calling the class like a function runs `__init__`. Three calls give three independent buildings.

### Step 4 · Changing an attribute
`housing.floors = 16` changes **only** that building. Its `height()` and `describe()` update automatically, because they read `self.floors` every time.

### Step 5 · Drawing with RhinoCommon
`b.to_box()` returns geometry that is **not yet in Rhino**. `sc.doc.Objects.AddBox(box)` adds it. `sc.doc.Views.Redraw()` refreshes the screen.

## Try this

1. Add a fourth building, `Building("School", 0, 30, 40, 25, 3, floor_height=4.0)`, to the list.
2. Add a method `footprint_area(self)` that returns `self.width * self.depth`, and print it for each building.
3. Add an attribute `use` (e.g. `"housing"`) to `__init__`, and include it in `describe()`.
4. Remove `self.` from `return self.floors * self.floor_height` and run. Read the `NameError`. Why does Python not know `floors` here?

## Ask the AI

Paste one of these into any AI chat tool. See [`Prompt guidelines`](../../Prompt%20guidelines/README.md) for more.

```text
I'm learning Python in the Rhino 8 ScriptEditor (Python 3).
Explain 'self' in this class to a beginner using an architectural
analogy, then explain what happens step by step when I write
Building("Housing", 40, 0, 15, 15, 12): <paste class>
```

```text
Convert this rhinoscriptsyntax code to RhinoCommon (Rhino.Geometry +
scriptcontext). Explain each change in one line: <paste code>
```

```text
Add a method to my Building class that returns a list of floor-plate
rectangles (one Rectangle3d per floor). Use RhinoCommon, comment every
line, and show how to add them to the document. <paste class>
```
