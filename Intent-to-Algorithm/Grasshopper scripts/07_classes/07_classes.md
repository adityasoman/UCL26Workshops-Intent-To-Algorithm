# Lesson 07 · Classes and RhinoCommon

**Environment:** Rhino 8 Grasshopper, Script component (Python 3) · **Code:** [`07_classes.py`](07_classes.py) · **Role:** Operator + Consumer

> **Different example from the Rhino version.** The RhinoScript editor lesson uses a **`Building`** class to place towers on a site. This one uses a **`Room`** class to lay out a **floor plan** from a list of room names and widths. The concept is the same, so you get two examples to compare.

## What is this concept?

This lesson has two new ideas.

### 1. Classes

A **class** is a blueprint for a kind of thing. It bundles **data** (what the thing *is*) with **behaviour** (what it can *do*).

Think of a **room type** in a brief versus **actual rooms** in a plan. "Bedroom" is a type: every bedroom has a width, a depth and a ceiling height. Each bedroom you draw is an **instance** of that type, with its own values.

| Word | Meaning | In this lesson |
|---|---|---|
| **class** | the blueprint / room type | `class Room:` |
| **instance** | one actual thing made from the blueprint | each item in `plan` |
| **attribute** | a value an instance stores about itself | `self.width`, `self.name` |
| **method** | a function that belongs to the class | `area()`, `to_box()`, `describe()` |
| `__init__` | the set-up method that runs when an instance is made | fills in the attributes |
| `self` | "this particular instance" | inside `area()`, `self.width` means *this* room's width |

```python
kitchen = Room("Kitchen", 0, 4.0, 5.0)   # make an instance (runs __init__)
kitchen.width                           # read an attribute: no brackets
kitchen.area()                          # run a method: brackets
```

### 2. RhinoCommon (`Rhino.Geometry`)

You've been using `Rhino.Geometry` (`rg`) in Grasshopper since lesson 02. Here's what makes it different from `rhinoscriptsyntax` (`rs`), which the Rhino version of these lessons used until now:

| | `rhinoscriptsyntax` (`rs`) | RhinoCommon (`Rhino.Geometry`, `rg`) |
|---|---|---|
| Style | simple commands: `rs.AddBox(corners)` | geometry **objects**: `rg.Box(...)` |
| Gives you back | an **ID** of an object in a document | the **geometry itself** |
| Points | lists `[x, y, z]` | `rg.Point3d(x, y, z)` with `.X`, `.Y`, `.Z` |
| In Grasshopper | writes to a hidden GH document; outputs are IDs, which confuses things | outputs are real geometry that previews and flows into other components |

That's why the Grasshopper versions use RhinoCommon: Grasshopper wants **geometry**, not document IDs.

## Why does it matter for design?

A plan is a set of rooms, each with data (size, name) and rules (is it big enough? what's its volume?). A class keeps each room's data and rules together, so the script reads like the brief. AI tools very often answer with classes, so you need to be able to read them.

## Component setup

Zoom in on the component and use **⊕ / ⊖** to add or remove parameters. Right-click each one to rename it, set its **Type hint**, and set **Item** or **List Access**.

**Inputs**

| Name | Type hint | Access | Connect to |
|---|---|---|---|
| `names` | `str` | **List Access** | Panel with one name per line: `Living`, `Kitchen`, `Bedroom`, `Bath`, `Study` (right-click the Panel → turn **Multiline Data** off) |
| `widths` | `float` | **List Access** | Panel with one number per line: `6`, `4`, `4.5`, `2.5`, `3.5` |
| `depth` | `float` | Item Access | Number Slider, 3.0–8.0, default 5.0 |
| `height` | `float` | Item Access | Number Slider, 2.4–4.0, default 2.8 |

**Outputs**

| Name | Type | Notes |
|---|---|---|
| `rooms` | list of Box | one box per room |
| `outlines` | list of Rectangle3d | plan outlines |
| `centres` | list of Point3d | connect to a **Text Tag** with `names` as the text |
| `info` | list of str | one description per room; connect a Panel |
| `out` | built-in | `print()` messages; connect a Panel |

> **List Access matters here.** With Item Access, the script would run once per name and make five separate one-room plans.

## How to run

1. Place a **Python 3 Script** component (Maths tab → Script panel).
2. Set up the inputs and outputs exactly as listed above.
3. Double-click the component, paste the whole `.py` file, then **Run**.
4. You should see five rooms in a row, and in `info` lines like `Living: 30.0 m², 84.0 m³ (large)`. Add a name to the `names` Panel and a new room appears.

## Step by step

### Step 1 · RhinoCommon objects
A `Point3d` knows its own coordinates: `corner.X` instead of `corner[0]`. An `Interval` is a range from one number to another, with a `.Length`. Objects carry their own **properties**.

### Step 2 · The class
- `class Room:` starts the blueprint. Everything indented belongs to it.
- `__init__` (two underscores each side) runs automatically when you make a room. It copies the arguments into `self.<name>` so the room remembers them.
- Every method has `self` as its first parameter. You never pass it yourself; Python fills it in.
- `"large" if self.is_large() else "small"` is a one-line `if/else` that picks one of two values.

### Step 3 · One instance
`Room("Test", 0, 4.0, depth)` makes one room. Changing `test_room.width` changes only that room, and `describe()` uses the new value straight away.

### Step 4 · Many instances
One `Room` per name. `cursor` remembers where the last room ended, so rooms sit side by side. If there are fewer widths than names, the last width is reused (`widths[-1]` is the last item).

### Step 5 · Ask every instance
Each room builds its own box, outline and label point, and describes itself. The main script just collects the results. That's the point of a class: **the room knows how to handle itself**.

## Try this

1. Add `Dining` to `names` and `3.5` to `widths`.
2. Change `is_large` so the threshold is 15 m². Which rooms change?
3. Add an attribute `use` (e.g. `"private"` or `"shared"`) and output only the shared rooms.
4. Remove `self.` from `return self.width * self.depth` and read the red error. Why does Python not know `width` here?

## Ask the AI

Paste one of these into any AI chat tool. See [`Prompt guidelines`](../../Prompt%20guidelines/README.md) for more.

```text
I'm learning Python in a Rhino 8 Grasshopper Script component (Python 3).
Explain 'self' in this class to a beginner using an architectural
analogy, then explain what happens step by step when I write
Room("Kitchen", 0, 4.0, 5.0): <paste class>
```

```text
Extend my Room class so rooms wrap onto a second row when the plan gets
longer than a 'max_length' input. Use Rhino.Geometry only, comment every
line, and list any new inputs with type hints and access. <paste script>
```

```text
Why does a Grasshopper Python 3 script that uses rhinoscriptsyntax output
GUIDs instead of geometry? Explain for a beginner and show the
RhinoCommon equivalent of rs.AddBox.
```
