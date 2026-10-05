# Lesson 06 · Loops

**Environment:** Rhino 8 ScriptEditor (Python 3) · **Code:** [`06_loops.py`](06_loops.py) · **Role:** Producer + Consumer

## What is this concept?

A **loop** repeats the same lines many times. It's how one rule produces a hundred plots or forty floors.

There are two kinds:

| Loop | Means | Use it when |
|---|---|---|
| `for` | "for **each** item, do this" | you know what to repeat over: a count, a list |
| `while` | "**keep going while** this is true" | you don't know how many repeats in advance: "add floors until the height limit" |

```python
for ix in range(x_count):           # each column…
    for iy in range(y_count):       # …and each row inside it
        plots.append([ix * spacing, iy * spacing, 0])

while level_z + upper_floor_height <= height_limit:
    ...                              # place a floor
    level_z = level_z + upper_floor_height   # move towards the stop
```

Useful tools that come with loops:

| Tool | Does | Example |
|---|---|---|
| `range(n)` | the numbers 0 … n−1 | `range(3)` → 0, 1, 2 |
| `range(a, b, step)` | from a up to (not including) b | `range(2, 11, 4)` → 2, 6, 10 |
| `list.append(x)` | add `x` to the end of a list | `plots.append(p)` |
| `len(list)` | how many items | `len(plots)` → 100 |

You've already met loops briefly in lessons 02 and 05. This lesson explains them properly.

## Why does it matter for design?

Most design systems are **repetitive with variation**: a grid of plots, a stack of floors, a row of columns. Loops let you write the rule once and apply it everywhere, and change the whole system by editing one number.

## Where this sits in Producer → Operator → Consumer

| Role | Meaning |
|---|---|
| **Producer** | reads or creates information |
| Operator | applies rules to that information |
| **Consumer** | turns the result into geometry or colour |

This lesson is a **Producer + Consumer**: the grid loop produces plot positions, and the `while` loop consumes a height rule to build a tower.

## How to run

1. Open `06_loops.py` in the ScriptEditor (command: `ScriptEditor`).
2. Press the green **Run** button (or **F5**).
3. You should see a 10 × 10 grid of points with the 4 corners labelled, and next to it a stack of floor outlines on layer `Lesson_06`. The Console shows the counts and the tower height.

## Step by step

### Step 1 · `for` + `range`
`range` **starts at 0** and **stops before** the end number. `range(5)` is 0–4, five numbers. This trips up everyone at first.

### Step 2 · `for` over a list
You can loop directly over a list. The loop variable (`use`) takes each item in turn. Choose a name that reads well: `for plot in plots`, `for floor in floors`.

### Step 3 · Nested loops
The **inner** loop runs completely for **every** pass of the outer loop: 10 columns × 10 rows = 100 points. `.append()` grows the list one item at a time, starting from the empty list `[]`.

> Grasshopper has its own way of handling lists of lists, called **DataTrees**. They're outside this workshop. Here we keep everything in one flat list.

### Step 4 · Looping over results
Once you have a list, you can loop over it again to apply rules. This is where loops and conditionals (lesson 05) work together.

### Step 5 · `while`
`while` keeps going **as long as** its condition is True. Two safety rules:

1. **Something inside the loop must move towards the stop.** Here `level_z` grows every time. Delete those lines and the loop never ends.
2. **Add a hard cap.** `floor_count < MAX_FLOORS` stops the loop even if the main condition is wrong.

> ⚠️ **An infinite loop freezes Rhino.** If it happens, press **Esc** a few times. If that doesn't work, you'll have to close Rhino (save your work first!).

## Try this

1. Change `x_count` to `20` and `spacing` to `5.0`. Same site, finer grid.
2. Change `height_limit` to `100.0`. How many floors fit now?
3. Change the grid so only every second plot is made. (Hint: `range(0, x_count, 2)`.)
4. *Carefully:* comment out `MAX_FLOORS` from the while condition **and** set `upper_floor_height = 0`. Don't run it! Explain to a neighbour why it would freeze.

## Ask the AI

Paste one of these into any AI chat tool. See [`Prompt guidelines`](../../Prompt%20guidelines/README.md) for more.

```text
I'm learning Python in the Rhino 8 ScriptEditor (Python 3).
Explain step by step what happens in these nested loops, pass by pass,
for x_count = 2 and y_count = 3: <paste step 3>
```

```text
Change my grid so every other row is shifted by half the spacing
(a staggered grid). Rhino 8, Python 3, rhinoscriptsyntax only,
comment every line.
```

```text
Look at this while loop: <paste step 5>. List every way it could run
forever, and how the code guards against each one.
```
