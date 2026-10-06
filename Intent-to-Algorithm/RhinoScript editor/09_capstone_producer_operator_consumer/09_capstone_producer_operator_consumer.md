# Lesson 09 · Capstone: Producer → Operator → Consumer

**Environment:** Rhino 8 ScriptEditor (Python 3) · **Code:** [`09_capstone_producer_operator_consumer.py`](09_capstone_producer_operator_consumer.py) · **Role:** all three

## What is this concept?

Nothing new. This lesson **combines everything** from lessons 01–08 into one small computational design system, split into the workshop's three roles:

| Role | Function | What it does here | Lessons used |
|---|---|---|---|
| **Producer** | `producer()` | reads the sun study from `site_points.csv` | 01 data types, 08 files, dictionaries |
| **Operator** | `operator()` | filters spots by park distance and sun, and remaps sun hours to height | 02 `math`, 04 functions, 05 rules, 06 loops |
| **Consumer** | `consumer()` | builds coloured boxes and marks open spaces | 07 RhinoCommon, 05 colour rules |

A short **main** section at the bottom calls them in order. Each function only does its own job, and hands its result to the next.

## Design intent

> *"Spots with more sun get taller buildings. Spots too close to the park stay open space. Spots with too little sun aren't built on. Show the result as massing, coloured by height."*

Each sentence becomes code:

| Sentence | Where | Code |
|---|---|---|
| "too close to the park stay open" | `operator()` rule 1 | `if d < park_radius:` |
| "too little sun aren't built on" | `operator()` rule 2 | `elif s["sun"] < min_sun:` |
| "more sun → taller" | `operator()` rule 3 | `remap(sun, lowest, highest, min_height, max_height)` |
| "massing, coloured by height" | `consumer()` | `rg.Box` + `height_colour()` |
| "from a sun study" | `producer()` | `csv.DictReader` |

**The design rules are all in `SETTINGS`.** Changing a number there changes the design, without touching the logic.

## Why does it matter for design?

This is the whole point of the workshop: a vague intent ("respond to sun, respect the park") becomes **explicit rules** that you can test, question and change. Splitting the system into Producer / Operator / Consumer means you can swap one part without breaking the others: different data, different rules, or a different way of drawing the result.

## How to run

1. Open the file **from the workshop folder** in the ScriptEditor (command: `ScriptEditor`) and press **Run** (F5). It finds the `data` folder by itself, as in lesson 08. (Only if you moved the file: set `DATA_FOLDER` on the line marked `# CHANGE THIS`.)
3. You should see boxes of different heights coloured from blue (low) to red (tall), green points for open spots, and a green circle showing the park rule, all on layer `Lesson_09`. The Console reports the counts and the tallest building.

## Step by step

### Producer
Reads the CSV and **converts text to numbers once**, so the rest of the system never has to think about it. If the file is missing, it returns an empty list and the rest of the system simply builds nothing.

### Operator
- `remap()` is a small helper you'll use again and again: it stretches a value from one range (e.g. 3.5–8.3 sun hours) to another (6–60 m).
- The first loop finds the lowest and highest sun among **buildable** spots, so heights use the full range.
- The rules run in order, like lesson 05. **Order matters:** a sunny spot inside the park radius is still open space, because rule 1 is checked first.
- `s["height"] = ...` adds a new key to that spot's dictionary.
- The function returns **two** lists (lesson 04).

### Consumer
Turns each building into an `rg.Box` (lesson 07), adds it to the document and colours it. `height_colour` mixes red and blue: `t` goes from 0 (lowest) to 1 (tallest).

### Main
Three lines run the whole system: information in → rules → geometry out. Reading these three lines tells you what the script does.

## Try this

1. Change `park_radius` to `35.0`. How many buildings are lost?
2. Change `min_sun` to `5.0`. Where does the development move to?
3. Flip the rule: make **less** sun give **taller** buildings (a tower that shades itself less?). Which single line do you change?
4. Add a rule 4: spots within 10 m of the site edge (x or y below 10 or above 90) are limited to 15 m. Where does it go?

## Ask the AI

Paste one of these into any AI chat tool. See [`Prompt guidelines`](../../Prompt%20guidelines/README.md) for more.

```text
Here is my design system: <paste the DESIGN INTENT block and the
operator() function>. Propose three alternative Operator rule sets that
respond to the same data (x, y, sun_hours) but express different design
intents. For each, give the intent in one sentence and the rules in
plain English. No code yet.
```

```text
Implement option <n> from your last answer as a new operator() function
that returns (buildings, open_spaces) exactly like mine, so producer()
and consumer() don't need to change. Rhino 8, Python 3, comment every line.
```

```text
Review my capstone script as a tutor would: is each function doing only
its own job (Producer / Operator / Consumer)? Point out anything in the
wrong place, and any rule that could give a surprising result at the edges.
```
