# Lesson 01 · Data types

**Environment:** Rhino 8 ScriptEditor (Python 3) · **Code:** [`01_data_types.py`](01_data_types.py) · **Role:** Producer

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

We store each value in a **variable**: a name that points to a value, like a label on a box. `floors = 12` means *"put 12 in a box labelled floors"*. The `=` sign means **store**, not "equals".

The type matters because it decides what is allowed: you can multiply two numbers, but you can't multiply a name by a height.

## Why does it matter for design?

Before we can write rules ("taller towers where there is more sun"), we have to **describe the design as data**. Choosing the right type for each property is the first step in turning an intention into something a computer can work with.

## Where this sits in Producer → Operator → Consumer

| Role | Meaning |
|---|---|
| **Producer** | reads or creates information |
| Operator | applies rules to that information |
| Consumer | turns the result into geometry or colour |

This lesson is mainly a **Producer**. We create the raw data that describes one tower, then draw two points from it at the end.

## How to run

1. Open `01_data_types.py` in the ScriptEditor (command: `ScriptEditor`).
2. Press the green **Run** button (or **F5**).
3. You should see each value and its type printed in the Console, plus two points and a label ("Tower A") on layer `Lesson_01`.

## Step by step

| Step | Type | What to point out |
|---|---|---|
| 1 | `int`, `float` | Whole vs. decimal numbers. `type()` reveals the kind of data. |
| 2 | `str` | Text always sits inside quotes. |
| 3 | `bool` | Only `True` or `False`, with a capital letter. |
| 4 | `None` | Means "no value yet". Not zero, not empty text. |
| 5 | `list` | Several values in order inside `[ ]`. Positions are counted **from 0**: `origin[0]` is x. `len()` counts the items. |
| 6 | mixing types | `int × float` gives a `float`. The raw result `38.400000000000006` is not a bug: computers store decimals approximately. `round()` tidies it. **f-strings** (`f"{name} is {total_height} m tall"`) mix any types into a sentence. |
| 7 | data → geometry | A list of 3 numbers becomes a point. Rhino objects have their own type, an ID called a **Guid**. |

## Try this

1. Change `floors` to `30` and run again. Watch the top point and the printed height change.
2. Change `floors = 12` to `floors = "12"` (with quotes) and run. You'll get a **TypeError**: Python can't multiply text by a float. Lesson 03 is all about reading errors like this.
3. Change `roof_garden = None` to `roof_garden = "intensive"`. What does `type()` print now?
4. Add a fourth number to the `origin` list. What does `len()` print? Does the point still work? (Rhino expects exactly 3.)

## Ask the AI

Paste one of these into any AI chat tool. See [`Prompt guidelines`](../../Prompt%20guidelines/README.md) for more.

```text
I'm learning Python in the Rhino 8 ScriptEditor (Python 3).
Using a building as the example, explain the difference between
int, float, str, bool, None and list in simple terms.
```

```text
Why does 12 * 3.2 give 38.400000000000006 in Python?
Explain it to an architecture student with no coding background.
```

```text
I'm describing a tower as data: floors (int), floor_height (float),
name (str), is_residential (bool), roof_garden (None), origin (list).
Suggest 3 more properties a designer might need, which Python type
each should be, and why. Don't write code yet.
```
