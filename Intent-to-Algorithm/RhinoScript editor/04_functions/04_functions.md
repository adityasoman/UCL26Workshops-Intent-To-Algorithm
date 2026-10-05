# Lesson 04 · Functions

**Environment:** Rhino 8 ScriptEditor (Python 3) · **Code:** [`04_functions.py`](04_functions.py) · **Role:** Consumer

## What is this concept?

A **function** is a reusable recipe. You write the steps once with `def`, give the recipe a name, and then **call** it as many times as you like with different ingredients.

Think of a **typical floor plan**: you draw it once, then reuse it on every storey. A function does the same for code.

```python
def make_tower(x, y, floors, floor_height=3.0):   # the recipe
    ...
    return box, height                             # what the recipe hands back

make_tower(0, 0, 10)                               # use the recipe
```

| Word | Meaning | In this lesson |
|---|---|---|
| **define** (`def`) | write the recipe; nothing happens yet | `def make_tower(...)` |
| **parameter** | a blank in the recipe | `x`, `y`, `floors`, `floor_height` |
| **argument** | the value you put in the blank when you call it | `0, 0, 10` |
| **default** | a value used if you don't give one | `floor_height=3.0` |
| **call** | use the recipe | `make_tower(0, 0, 10)` |
| **return** | the result the recipe hands back | `box, height` |

You've already been calling functions: `print()`, `round()`, `rs.AddPoint()`. Now you write your own.

## Why does it matter for design?

A design rule you write once can be applied everywhere, and changed in one place. If the client wants a different footprint, you change the recipe, not twenty copies of the code. AI-generated scripts are almost always organised into functions, so reading `def` and `return` is essential.

## Where this sits in Producer → Operator → Consumer

| Role | Meaning |
|---|---|
| Producer | reads or creates information |
| Operator | applies rules to that information |
| **Consumer** | turns the result into geometry or colour |

This lesson is mainly a **Consumer**: `make_tower` turns plain numbers (position, floors) into geometry.

## How to run

1. Open `04_functions.py` in the ScriptEditor (command: `ScriptEditor`).
2. Press the green **Run** button (or **F5**).
3. You should see a street of 7 towers of different heights on layer `Lesson_04`, each labelled with its floor count, and the heights and floor area in the Console.

## Step by step

### Step 1 · Define
Running the `def` block **builds nothing**. Python only memorises the recipe. Point out that the indented lines belong to the function, and that the function uses `tower_width` from `SETTINGS`.

`rs.AddBox` needs **8 corners**: the 4 bottom ones, then the 4 top ones in the same order.

### Step 2 · Call once
`make_tower(0, 0, 10)` fills `x=0`, `y=0`, `floors=10`. `floor_height` isn't given, so the default `3.0` is used, giving 30 m.

The function returns **two** things. `first_box, first_height = ...` unpacks them into two variables, in order.

### Step 3 · Call many times
The same five lines of recipe now make a whole street. If you don't need the result, you can ignore it. `_` is a common name for "a value I don't care about".

### Step 4 · Override the default
Passing `floor_height=4.2` replaces the default. Arguments can also be given **by name** (`floors=10`), which makes long calls easier to read.

### Step 5 · Functions that only calculate
`tower_area` draws nothing; it just returns a number. Many useful functions are like this: they answer a question.

## Try this

1. Change `tower_width` to `12.0` and run. Every tower changes, because they all use the same recipe.
2. Add a call that makes a 30-storey tower at `step * 7`.
3. Change the default to `floor_height=3.5`. Which towers change height, and which don't? Why?
4. Put a `#` in front of the `return` line and run. Read the `TypeError: cannot unpack non-iterable NoneType object`. A function with no `return` gives back `None`, so there's nothing to unpack into two variables.

## Ask the AI

Paste one of these into any AI chat tool. See [`Prompt guidelines`](../../Prompt%20guidelines/README.md) for more.

```text
I'm learning Python in the Rhino 8 ScriptEditor (Python 3).
Explain the difference between a parameter and an argument, using this
function as the example: <paste make_tower>
```

```text
Add a parameter 'setback' to my make_tower function so each floor above
floor 6 is 1 m smaller on every side. Keep using rhinoscriptsyntax,
comment every line, and don't change how the existing calls work.
```

```text
Here is a script with the same code copied five times: <paste>.
Show me how to turn the repeated part into one function and call it
five times. Explain each change.
```
