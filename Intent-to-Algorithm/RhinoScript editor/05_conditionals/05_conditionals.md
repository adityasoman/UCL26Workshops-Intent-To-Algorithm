# Lesson 05 · Conditionals

**Environment:** Rhino 8 ScriptEditor (Python 3) · **Code:** [`05_conditionals.py`](05_conditionals.py) · **Role:** Operator

## What is this concept?

A **conditional** lets a script make decisions: *if* something is true, do this; otherwise do that. This is how a written design rule becomes code.

> *"Plots closer than 30 m to the park stay green. Plots closer than 48 m get a low-rise block. Everything else gets a high-rise tower."*

```python
if d < green_radius:        # rule 1
    label = "green"
elif d < low_radius:        # rule 2 (only checked if rule 1 was False)
    label = "low-rise"
else:                       # everything else
    label = "high-rise"
```

Decisions are built from **comparisons**, which always answer `True` or `False` (the `bool` type from lesson 01):

| Symbol | Question | Design sentence |
|---|---|---|
| `==` | equal to? | "is it exactly 12 storeys?" |
| `!=` | not equal to? | "is it anything except 10 storeys?" |
| `<` / `>` | less / greater than? | "is it under the height limit?" |
| `<=` / `>=` | less / greater than or equal? | "does it have 4 or more storeys?" |
| `and` | are **both** true? | "tall **and** residential" |
| `or` | is **at least one** true? | "has a garden **or** is over 10 storeys" |
| `not` | flip the answer | "does **not** have a garden" |

> ⚠️ `=` **stores** a value (`floors = 12`). `==` **compares** (`floors == 12`). Mixing them up is a classic error.

## Why does it matter for design?

A design intent like "more open space near the park" is vague. A conditional forces you to be exact: *how near?* *What happens at exactly 30 m?* Writing the rule as `if / elif / else` makes every decision explicit, testable and easy to change.

## Where this sits in Producer → Operator → Consumer

| Role | Meaning |
|---|---|
| Producer | reads or creates information |
| **Operator** | applies rules to that information |
| Consumer | turns the result into geometry or colour |

This lesson is mainly an **Operator**: it takes plot positions and applies rules to classify them.

## How to run

1. Open `05_conditionals.py` in the ScriptEditor (command: `ScriptEditor`).
2. Press the green **Run** button (or **F5**).
3. You should see the park with two rings (the 30 m and 48 m rules), and 12 plots on layer `Lesson_05`: flat green squares near the park, orange 9 m blocks further out, and red 36 m towers furthest away. Each is labelled with its class, and the Console shows the counts.

## Step by step

### Step 1 · Comparisons
Each `print` shows `True` or `False`. Read each line out loud as a question.

### Step 2 · and / or / not
Combine simple questions into a rule. Brackets help when rules get long: `(floors > 8 and is_residential) or has_garden`.

### Step 3 · if / elif / else
- The line ending in `:` asks the question. The **indented** lines underneath run only when the answer is `True`.
- Python checks from the top and **stops at the first True**. That's why `elif d < low_radius` doesn't need to say "and not green": it's only reached if the first rule failed.
- `else` has no question. It catches everything left over.
- **Order matters.** If you swapped the first two rules, nothing would ever be green.

### Step 4 · Every plot
The same rule chain runs once for each plot. The loop is explained in lesson 06; for now, read it as "for each plot in the list". Counters go up with `count = count + 1`.

Each rule sets three things: a `label`, a `colour` and a `height`. Then the drawing code uses them:

- `if height > 0:` is a **second, separate decision**. Low-rise and high-rise plots get a box (`rs.AddBox` with 8 corners, as in lesson 04). Green plots have height 0, so they get a flat square (`rs.AddSrfPt` with 4 corners) instead.
- This split is useful: **the rule decides, the drawing code draws**. To change what high-rise means, you only change `high_height`.
- `rs.ObjectColor(id, (r, g, b))` paints an object. Colours are three numbers from 0 to 255: red, green, blue.
- The two circles drawn at the start show the rules' boundaries, so you can check every plot visually.

### Step 5 · Report
A single `if` with no `else` is fine: if the answer is False, nothing happens.

## Try this

1. Change `green_radius` to `15.0` and run. How many plots stay green now?
2. Add a fourth class: plots further than `55.0` m become a `"landmark"` 60 m tall. Where in the chain must the new `elif` go?
3. Swap the first two rules (put the `low_radius` test first). Run and explain why nothing is green.
4. Change `floors > 8 and is_residential` to use `or`. When do the two give different answers?

## Ask the AI

Paste one of these into any AI chat tool. See [`Prompt guidelines`](../../Prompt%20guidelines/README.md) for more.

```text
My design intent is "more privacy for ground-floor flats". Suggest three
different if/elif/else rules that could express it, using values a
script could measure (distances, heights, angles). No code yet, just
the rules in plain English.
```

```text
Explain line by line what this if/elif/else chain does, and what happens
to a plot that is exactly 30.0 m from the park: <paste step 4>
```

```text
Rewrite my plot classification so the thresholds come from a small
table (a dictionary) instead of separate variables. Rhino 8, Python 3,
rhinoscriptsyntax, comment every line.
```
