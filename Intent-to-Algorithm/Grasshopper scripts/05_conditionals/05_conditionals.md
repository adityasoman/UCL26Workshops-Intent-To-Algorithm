# Lesson 05 · Conditionals

**Environment:** Rhino 8 Grasshopper, Script component (Python 3) · **Code:** [`05_conditionals.py`](05_conditionals.py) · **Role:** Operator

> **Different example from the Rhino version.** The RhinoScript editor lesson classifies **plots by distance to a park**. This one decides the **use of each floor in a mixed-use tower**. The concept is the same, so you get two examples to compare.

## What is this concept?

A **conditional** lets a script make decisions: *if* something is true, do this; otherwise do that. This is how a written design rule becomes code.

> *"The lowest floors are retail. Above them come offices up to a set level. The top floor is a penthouse. Everything else is residential. Every few floors, homes get a terrace."*

```python
if level < retail_floors:      # rule 1
    use = "retail"
elif level <= office_top:      # rule 2 (only checked if rule 1 was False)
    use = "office"
elif level == floors - 1:      # rule 3
    use = "penthouse"
else:                          # everything else
    use = "residential"
```

Decisions are built from **comparisons**, which always answer `True` or `False` (the `bool` type from lesson 01):

| Symbol | Question | Design sentence |
|---|---|---|
| `==` | equal to? | "is this the top floor?" |
| `!=` | not equal to? | "is this any floor except the ground floor?" |
| `<` / `>` | less / greater than? | "is it under the 100 m limit?" |
| `<=` / `>=` | less / greater than or equal? | "is it 30 m or taller?" |
| `and` | are **both** true? | "tall **and** has offices" |
| `or` | is **at least one** true? | "residential **or** penthouse" |
| `not` | flip the answer | "has **no** offices" |

> ⚠️ `=` **stores** a value (`use = "office"`). `==` **compares** (`use == "office"`). Mixing them up is a classic error.

## Why does it matter for design?

"Active ground floor, homes above" is a design intent. A conditional forces you to be exact: *how many* retail floors? *What if* the office band is empty? Writing the rule as `if / elif / else` makes every decision explicit, and sliders let you test it instantly.

## Where this sits in Producer → Operator → Consumer

| Role | Meaning |
|---|---|
| Producer | reads or creates information |
| **Operator** | applies rules to that information |
| Consumer | turns the result into geometry or colour |

This lesson is mainly an **Operator**: it takes a stack of floors and applies rules to decide each floor's use.

## Component setup

Zoom in on the component and use **⊕ / ⊖** to add or remove parameters. Right-click each one to rename it, set its **Type hint**, and set **Item** or **List Access**.

**Inputs**

| Name | Type hint | Access | Connect to |
|---|---|---|---|
| `floors` | `int` | Item Access | Number Slider, 1–40, default 20 |
| `floor_height` | `float` | Item Access | Number Slider, 2.8–4.5, default 3.2 |
| `retail_floors` | `int` | Item Access | Number Slider, 0–5, default 2 |
| `office_top` | `int` | Item Access | Number Slider, 0–30, default 8 |
| `terrace_every` | `int` | Item Access | Number Slider, 1–10, default 4 |

**Outputs**

| Name | Type | Notes |
|---|---|---|
| `slabs` | list of Rectangle3d | every floor outline |
| `uses` | list of str | e.g. `L07: office`; connect a Panel |
| `retail` | list of Rectangle3d | retail floors only |
| `office` | list of Rectangle3d | office floors only |
| `residential` | list of Rectangle3d | residential and penthouse floors |
| `terraces` | list of Rectangle3d | floors that get a terrace |
| `out` | built-in | `print()` messages; connect a Panel |

**To see the uses in colour:** connect `retail`, `office` and `residential` to three **Custom Preview** components (Display tab), each with a **Colour Swatch** in its Material input. Or right-click the Script component → **Preview** off, and preview only the outputs you want.

## How to run

1. Place a **Python 3 Script** component (Maths tab → Script panel).
2. Set up the inputs and outputs exactly as listed above.
3. Double-click the component, paste the whole `.py` file, then **Run**.
4. You should see a stack of 20 floor outlines and a list of uses in the `uses` Panel. Move `office_top` below `retail_floors`: the component turns orange with a warning.

## Step by step

### Step 1 · Comparisons
Each `print` shows `True` or `False` in `out`. Read each line out loud as a question.

### Step 2 · and / or / not
Combine simple questions into a rule. Brackets help when rules get long: `(tower_height > 50 and has_offices) or floors == 1`.

### Step 3 · if / elif / else
- The line ending in `:` asks the question. The **indented** lines underneath run only when the answer is `True`.
- Python checks from the top and **stops at the first True**. That's why `elif level <= office_top` doesn't need to say "and not retail".
- `else` has no question. It catches everything left over.
- **Order matters.** Rule 3 (penthouse) only works because it comes after the office rule. If the office band reaches the top, the top floor becomes an office instead.

### Step 4 · A rule built from several questions
`%` gives the **remainder** after dividing: `8 % 4` is `0`, `9 % 4` is `1`. So `level % terrace_every == 0` is True on every 4th floor. The terrace rule only applies when **all three** parts are True: an nth floor, a home, and not the ground floor.

### Step 5 · Report
`len()` counts the items in a list. The warning uses `AddRuntimeMessage` from lesson 03, now wrapped in an `if`, so it only appears when the rule is broken.

## Try this

1. Set `retail_floors` to 0. What becomes the ground floor?
2. Move `office_top` up to 40. What happens to the penthouse, and why?
3. Change the terrace rule to use `or` instead of the second `and`. What changes?
4. Add a rule: if `level == 0` the use is `"lobby"`. Where in the chain must it go so that it wins?

## Ask the AI

Paste one of these into any AI chat tool. See [`Prompt guidelines`](../../Prompt%20guidelines/README.md) for more.

```text
My design intent is "an active, public base and private homes above".
Suggest three different sets of if/elif/else rules for assigning uses
to tower floors. Plain English only, no code yet.
```

```text
Explain line by line what this if/elif/else chain does, and what
happens when office_top is larger than floors: <paste step 3>
```

```text
Add a rule to my Grasshopper Python 3 script: floors above 60 m get a
'sky garden' every 6 floors. Add any new sliders as inputs, use
Rhino.Geometry only, and comment every line. <paste script>
```
