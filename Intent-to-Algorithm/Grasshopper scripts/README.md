# Grasshopper scripts lessons

These lessons run in the **Rhino 8 Grasshopper Script component** using **Python 3**. They teach the same concepts as the [RhinoScript editor](../RhinoScript%20editor/README.md) versions. Lessons 00–03 use the same example as the Rhino version. From lesson 04 on, **each Grasshopper lesson uses a different architectural example** (e.g. façade fins instead of a street of towers), so you see every concept applied twice. The other difference is how the script gets its inputs and returns its results.

| | RhinoScript editor | Grasshopper Script component |
|---|---|---|
| Inputs come from | a `SETTINGS` block of variables at the top of the file | **input parameters** on the left of the component (sliders, panels, points…) |
| Results go to | the Rhino document (objects you can select) | **output parameters** on the right of the component |
| `print()` goes to | the Console | the **`out`** output (connect a **Panel** to read it) |
| Re-runs when | you press Run | **any input changes** |

## How each lesson is organised

Every lesson has its own folder holding two files with the same name:

```
01_data_types/
├── 01_data_types.md   ← READ THIS: the concept in plain English, how to run, step notes, Try this, Ask the AI
└── 01_data_types.py   ← the code: every line has a short comment saying what it does
```

The code points back to the `.md` where a step needs more explanation (for example `see .md → Step 6`). Each `.md` also has the full **Component setup** table for that lesson.

> **Before you start:** you need **Rhino 8**. The `.py` files can't be opened directly in Grasshopper. You **paste them into a Script component** that you set up first.

---

## 1. Place the right component

1. Open Rhino 8 and type **`Grasshopper`** in the command line.
2. Go to the **Maths** tab → **Script** panel.
3. Drag the **Python 3 Script** component onto the canvas. (The generic **Script** component works too; you then choose **Python 3** as its language.)

> ⚠️ **Make sure it's the right one.** The same panel also has **IronPython 2** and legacy **GhPython** components. They run an older Python, and our lessons will fail there with confusing errors. To check:
> - **Correct:** double-clicking opens the new Rhino 8 **ScriptEditor**, and the code language shown is **Python 3**.
> - **Wrong:** the component is called *GhPython Script* or *IronPython 2 Script*, or a small old-style code window opens.

## 2. Set up inputs and outputs

Every lesson's `.md` has a **Component setup** section with a table like this:

| Name | Type hint | Access | Connect to |
|---|---|---|---|
| `floors` | `int` | Item Access | Number Slider, 1–40, default 12 |
| `floor_height` | `float` | Item Access | Number Slider, 2.5–5.0, default 3.2 |

The top of each `.py` file repeats it in short form, so you can check while wiring:

```python
# Inputs:  floors (int, Item), floor_height (float, Item)
# Outputs: info, point, top_point, out
```

Set the component up to match:

1. **Add or remove parameters.** Zoom in on the component until small **⊕ / ⊖** icons appear next to the inputs and outputs. Click ⊕ to add one and ⊖ to remove one.
2. **Rename each parameter** to the exact name in the setup table (right-click the parameter → type in the name field). Names must match the code exactly, including upper/lower case. `floors` and `Floors` are different.
3. **Set the type hint** (right-click the input → **Type hint** → e.g. `int`, `float`, `str`, `Point3d`). This tells Grasshopper what kind of data to send in.
4. **Set the access** (right-click the input → **Item Access** or **List Access**):
   - **Item Access**: the script runs once *for each* item that comes in.
   - **List Access**: the script runs *once* and receives the whole list.

   Getting this wrong is the most common cause of strange results.
5. **`out` output:** this is where `print()` messages appear. If you can't see it, right-click the component and turn on the standard output (`out`) parameter.

## 3. Paste the lesson code

1. Open the lesson `.py` file in any text editor (VS Code, Notepad, TextEdit) and copy all of it.
2. **Double-click** the Script component to open its editor.
3. Select all the existing code, then **paste** the lesson over it.
4. Press **▶ Run** or close the editor (the code is saved to the component).
5. Connect sliders, panels or points to the inputs as listed in the lesson's **Component setup** table.
6. Connect a **Panel** to `out` and to any text outputs so you can read the results.

## 4. Change things and watch

Move a slider and the component re-runs straight away. The **Try this** section in each lesson's `.md` suggests what to change.

---

## Component colours

| Colour | Meaning | What to do |
|--------|---------|------------|
| Grey | Ran successfully | — |
| **Orange** | Warning: it ran, but something may be missing (often an input with no data) | Hover over the small balloon at the top of the component to read the message |
| **Red** | Error: the code stopped | Hover over the balloon, and read the `out` panel for the full error message and **line number**. Lesson 03 teaches this step by step |

---

## Lesson index

| # | Lesson folder | Concept | Producer / Operator / Consumer | Status |
|---|------|---------|------------------|--------|
| 00 | [`00_hello_world/`](00_hello_world/00_hello_world.md) | Your first script: `print()` and comments | — (setup check) | ready |
| 01 | [`01_data_types/`](01_data_types/01_data_types.md) | Numbers, text, true/false, lists | Producer | ready |
| 02 | [`02_imports/`](02_imports/02_imports.md) | Borrowing tools with `import` | Producer | ready |
| 03 | [`03_console_errors/`](03_console_errors/03_console_errors.md) | Reading error messages and component colours | — | ready |
| 04 | [`04_functions/`](04_functions/04_functions.md) | Reusable recipes with `def` | Consumer | ready |
| 05 | [`05_conditionals/`](05_conditionals/05_conditionals.md) | Design rules with `if / elif / else` | Operator | ready |
| 06 | [`06_loops/`](06_loops/06_loops.md) | Repeating with `for` and `while` | Producer + Consumer | ready |
| 07 | [`07_classes/`](07_classes/07_classes.md) | Objects with `class`, plus RhinoCommon | Operator + Consumer | ready |
| 08 | [`08_data_input_output/`](08_data_input_output/08_data_input_output.md) | Reading and writing files | Producer | ready |
| 09 | [`09_capstone_producer_operator_consumer/`](09_capstone_producer_operator_consumer/09_capstone_producer_operator_consumer.md) | A full mini-system | All three | ready |

---

## Troubleshooting

| What you see | What it means | What to do |
|--------------|---------------|------------|
| `NameError: name 'floors' is not defined` | An input isn't named exactly as the code expects | Rename the input to match the lesson's **Component setup** table exactly |
| The output shows many results when you expected one (or the reverse) | The input **access** is wrong | Switch between **Item Access** and **List Access** as listed in the setup block |
| `SyntaxError` on an f-string, or odd `print` behaviour | You're in an **IronPython 2 / GhPython** component | Replace it with a **Python 3 Script** component |
| A number arrives as text (e.g. `'12'`), or `TypeError` | The input has no type hint, or the wrong one | Set the type hint (right-click → Type hint) |
| The component is orange and the outputs are empty | An input has no data connected | Connect a slider, panel or point to every input |
| Grasshopper becomes very slow | The script re-runs on every slider move and is doing a lot of work | Lower the slider ranges, or disable the component (right-click → Enable) while editing |
