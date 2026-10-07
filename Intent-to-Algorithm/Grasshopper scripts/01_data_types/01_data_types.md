# Lesson 01 · Data types

**Environment:** Rhino 8 Grasshopper, Script component (Python 3) · **Code:** [`01_data_types.py`](01_data_types.py) · **Role:** Producer

## What is this concept?

A program works with **data**: numbers, words, yes/no answers, collections of things. Every piece of data has a **type**, which tells Python what kind of thing it is and what you can do with it.

Think of a **building schedule** (a spreadsheet of building data). Each column holds one kind of information:

| Column | Kind of value | Python type | Example |
|---|---|---|---|
| Number of floors | whole numbers | `int` | `12` |
| Floor height (m) | decimal numbers | `float` | `3.2` |
| Building name | text | `str` | `"Tower A"` |
| Residential? | yes / no | `bool` | `True` |
| Roof garden | not decided yet | `None` | `None` |
| Position (x, y, z) | a group of values | `list` | `[10.0, 5.0, 0.0]` |

We store each value in a **variable**: a name that points to a value, like a label on a box. `name = "Tower A"` means *"put this text in a box labelled name"*. The `=` sign means **store**.

**In Grasshopper**, two of our variables (`floors` and `floor_height`) are **not written in the code**. They are the component's **inputs**: the sliders fill those boxes before the code runs. The **Type hint** you set on each input decides which type arrives.

## Why does it matter for design?

Before we can write rules ("taller towers where there is more sun"), we have to **describe the design as data**. Choosing the right type for each property is the first step in turning an intention into something a computer can work with.


This lesson is mainly a **Producer**. We create the raw data that describes one tower, then output two points from it at the end.

## Component setup

Zoom in on the component and use **⊕ / ⊖** to add or remove parameters. Right-click each one to rename it, set its **Type hint**, and set **Item** or **List Access**.

**Inputs**

| Name | Type hint | Access | Connect to |
|---|---|---|---|
| `floors` | `int` | Item Access | Number Slider, 1–40, default 12 |
| `floor_height` | `float` | Item Access | Number Slider, 2.5–5.0, default 3.2 |

**Outputs**

| Name | Type | Notes |
|---|---|---|
| `info` | text | connect a Panel |
| `point` | Point3d | the tower's base point |
| `top_point` | Point3d | the tower's top point |
| `out` | built-in | `print()` messages; connect a Panel |

## How to run

1. Place a **Python 3 Script** component (Maths tab → Script panel).
2. Set up the inputs and outputs exactly as listed above.
3. Double-click the component, paste the whole `.py` file, then **Run**.
4. You should see each value and its type in the `out` Panel, a short summary in the `info` Panel, and two points in Rhino. Move the sliders: everything updates straight away.

## Step by step

| Step | Type | What to point out |
|---|---|---|
| 1 | `int`, `float` | These arrive from the sliders. If `floors` shows `<class 'float'>`, the input's Type hint isn't set to `int` yet. |
| 2 | `str` | Text always sits inside quotes. |
| 3 | `bool` | Only `True` or `False`, with a capital letter. |
| 4 | `None` | Means "no value yet". Not zero, not empty text. |
| 5 | `list` | Several values in order inside `[ ]`. Positions are counted **from 0**: `origin[0]` is x. `len()` counts the items. |
| 6 | mixing types | `int × float` gives a `float`. The raw result `38.400000000000006` is not a bug: computers store decimals approximately. `round()` tidies it. **f-strings** mix any types into a sentence. |
| 7 | data → geometry | `rg.Point3d(x, y, z)` builds a point from three numbers. Geometry has its own type. `Rhino.Geometry` is covered properly in lesson 07. |
| Outputs | | `info` is a **list** of two texts, so a Panel shows each on its own line. |

## Try this

1. Move the `floors` slider to 30. Watch the top point move up and the `info` Panel update.
2. Right-click `floors` → **Type hint** → *No Type Hint* (or `str`), then move the slider. What does `type()` print in `out` now? Set it back to `int` afterwards.
3. Change `roof_garden = None` to `roof_garden = "intensive"`. What does `type()` print now?
4. Connect a Panel containing the text `12` (instead of a slider) to `floors`, with the Type hint set to `str`. You'll get a **TypeError**: Python can't multiply text by a float. Lesson 03 is all about errors.

## Ask the AI

Paste one of these into any AI chat tool. See [`Prompt guidelines`](../../Prompt%20guidelines/README.md) for more.

```text
I'm learning Python in a Rhino 8 Grasshopper Script component (Python 3).
What does the 'Type hint' on an input do, and what goes wrong if I don't
set it? Use an int slider as the example.
```

```text
Why does 12 * 3.2 give 38.400000000000006 in Python?
Explain it to an architecture student with no coding background.
```

```text
I'm describing a tower as data: floors (int), floor_height (float),
name (str), is_residential (bool), roof_garden (None), origin (list).
Suggest 3 more properties a designer might need, which Python type each
should be, and whether each one should be a Grasshopper input or a value
fixed in the code. Don't write code yet.
```
