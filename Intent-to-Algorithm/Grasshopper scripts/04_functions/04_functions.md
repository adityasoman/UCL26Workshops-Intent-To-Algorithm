# Lesson 04 · Functions

**Environment:** Rhino 8 Grasshopper, Script component (Python 3) · **Code:** [`04_functions.py`](04_functions.py) · **Role:** Consumer

> **Different example from the Rhino version.** The RhinoScript editor lesson builds a street of towers with `make_tower()`. This one builds a **façade of vertical fins** with `make_fin()`. The concept is the same, so you get two examples to compare.

## What is this concept?

A **function** is a reusable recipe. You write the steps once with `def`, give the recipe a name, and then **call** it as many times as you like with different ingredients.

Think of a **façade fin**: you design one fin detail, then repeat it along the whole elevation with different heights. A function does the same for code.

```python
def make_fin(x, height, depth=0.6, thickness=0.15):   # the recipe
    ...
    return fin                                         # what the recipe hands back

make_fin(0.0, 6.0)                                     # use the recipe
```

| Word | Meaning | In this lesson |
|---|---|---|
| **define** (`def`) | write the recipe; nothing happens yet | `def make_fin(...)` |
| **parameter** | a blank in the recipe | `x`, `height`, `depth`, `thickness` |
| **argument** | the value you put in the blank when you call it | `0.0, base_height` |
| **default** | a value used if you don't give one | `depth=0.6` |
| **call** | use the recipe | `make_fin(0.0, base_height)` |
| **return** | the result the recipe hands back | `fin` |

## Why does it matter for design?

A design rule you write once can be applied everywhere, and changed in one place. Change the fin detail once and the whole façade updates. AI-generated scripts are almost always organised into functions, so reading `def` and `return` is essential.

## Where this sits in Producer → Operator → Consumer

| Role | Meaning |
|---|---|
| Producer | reads or creates information |
| Operator | applies rules to that information |
| **Consumer** | turns the result into geometry or colour |

This lesson is mainly a **Consumer**: `make_fin` turns numbers (position, height) into geometry.

## Component setup

Zoom in on the component and use **⊕ / ⊖** to add or remove parameters. Right-click each one to rename it, set its **Type hint**, and set **Item** or **List Access**.

**Inputs**

| Name | Type hint | Access | Connect to |
|---|---|---|---|
| `fin_count` | `int` | Item Access | Number Slider, 1–60, default 24 |
| `spacing` | `float` | Item Access | Number Slider, 0.3–3.0, default 0.8 |
| `base_height` | `float` | Item Access | Number Slider, 2.0–15.0, default 6.0 |
| `wave` | `float` | Item Access | Number Slider, 0.0–5.0, default 2.0 |

**Outputs**

| Name | Type | Notes |
|---|---|---|
| `fins` | list of Box | one box per fin; previews in Rhino |
| `heights` | list of float | each fin's height; connect a Panel |
| `out` | built-in | `print()` messages; connect a Panel |

## How to run

1. Place a **Python 3 Script** component (Maths tab → Script panel).
2. Set up the inputs and outputs exactly as listed above.
3. Double-click the component, paste the whole `.py` file, then **Run**.
4. You should see a row of thin vertical fins whose heights ripple like a wave. Move `wave` to 0: every fin becomes the same height.

## Step by step

### Step 1 · Define
Running the `def` block **builds nothing**. Python only memorises the recipe. `rg.Box` is made from a plane and three ranges (`rg.Interval`): along x, along y and up z. Boxes and RhinoCommon are explained properly in lesson 07.

### Step 2 · Call once
`make_fin(0.0, base_height)` fills `x` and `height`. `depth` and `thickness` aren't given, so the defaults are used. `test_fin.Y.Length` reads the box's size along y: 0.6.

### Step 3 · Override a default
Passing `depth=1.2` replaces the default for this one call only. Naming the argument makes it clear which blank you're filling.

### Step 4 · Functions that only calculate
`fin_height` draws nothing; it just returns a number. `math.sin` swings smoothly between −1 and +1, so multiplying by `wave` gives a ripple of ± `wave` metres around `base_height`.

### Step 5 · Many calls
Inside the loop, the two recipes work together: one decides **how tall**, the other **builds** the fin. That split (calculate, then build) is a very common pattern.

## Try this

1. Move `spacing` and `fin_count` until the fins read as a screen rather than separate elements.
2. In step 5, change `make_fin(i * spacing, h)` to `make_fin(i * spacing, h, depth=1.5)`. What changes?
3. Change `0.5` inside `fin_height` to `0.2`, then `1.5`. How does the rhythm of the façade change?
4. Put a `#` in front of `return fin` and re-run. What does the `fins` output show now? (A function with no `return` gives back `None`.)

## Ask the AI

Paste one of these into any AI chat tool. See [`Prompt guidelines`](../../Prompt%20guidelines/README.md) for more.

```text
I'm learning Python in a Rhino 8 Grasshopper Script component (Python 3).
Explain the difference between a parameter and an argument, using this
function as the example: <paste make_fin>
```

```text
Add a parameter 'angle' to my make_fin function that rotates each fin
around its own vertical axis. Use Rhino.Geometry only, comment every line,
and add a Grasshopper input 'twist' (float, Item Access) that sets the angle.
```

```text
Here's my fin_height function: <paste>. Suggest three other functions
that give different façade rhythms (e.g. stepped, random with a seed,
taller in the middle). Explain each in one sentence before the code.
```
