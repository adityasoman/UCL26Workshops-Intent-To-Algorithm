# RhinoScript editor lessons

These lessons run in the **Rhino 8 ScriptEditor** using **Python 3**. Each lesson is a folder with a `.md` explanation and a `.py` script you can open and run as-is.

> **Before you start:** you need **Rhino 8**. Rhino 7 and earlier use an older editor and an older Python (IronPython 2.7), so these files won't run correctly there.

---

## How each lesson is organised

Every lesson has its own folder holding two files with the same name:

```
01_data_types/
├── 01_data_types.md   ← READ THIS: the concept in plain English, how to run, step notes, Try this, Ask the AI
└── 01_data_types.py   ← the code: every line has a short comment saying what it does
```

The code points back to the `.md` where a step needs more explanation (for example `see .md → Step 6`).

## 1. Open the ScriptEditor

1. Open Rhino 8 and start a new, empty model (metres is a good unit for these lessons).
2. In the command line, type **`ScriptEditor`** and press **Enter**.
3. The ScriptEditor window opens. It has three main areas:
   - **Explorer** (left): your open scripts and files.
   - **Editor** (centre): where the code is shown.
   - **Console** (bottom): where `print()` messages and **errors** appear. Keep this visible at all times.

> ⚠️ **Don't use `EditPythonScript`.** In Rhino 8 it is kept for older scripts and can open in **IronPython 2** mode, so our Python 3 lessons may fail there. Always use `ScriptEditor`.

## 2. Make sure the language is Python 3

Every lesson file starts with this line:

```python
#! python3
```

That line tells Rhino to run the file with Python 3. **Don't delete it.**

If you create a new script yourself, choose **Python 3** when the editor asks for a language (or use the language picker at the top of the editor). If you see **IronPython 2** or **Python 2**, switch it to Python 3.

## 3. Open and run a lesson

1. Read the lesson's `.md` file first (for example `01_data_types/01_data_types.md`). It tells you what to expect.
2. In the ScriptEditor, go to **File → Open** and choose the lesson's `.py` file, for example `01_data_types/01_data_types.py`.
3. Press the green **▶ Run** button (or **F5**).
4. Look in two places:
   - the **Console** for printed messages
   - the **Rhino viewport** for any geometry the script added

Each lesson puts its geometry on its own layer (for example `Lesson_04`), so you can hide or delete one lesson's output without touching anything else.

**Shortcut:** you can also run a file without opening the editor. Type **`RunPythonScript`** in Rhino's command line and choose the `.py` file.

## 4. Change things and re-run

Near the top of each file there is a **`SETTINGS`** block. These are the "inputs" of the script: numbers and names you are meant to change.

```python
# --- SETTINGS (change these and run again) ---
floors = 12          # how many storeys
floor_height = 3.2   # metres per storey
```

Change a value, press **Run** again, and see what changes. The **Try this** section in each lesson's `.md` suggests edits to make.

---

## Lesson index

| # | Lesson folder | Concept | Producer / Operator / Consumer | Status |
|---|------|---------|------------------|--------|
| 00 | [`00_hello_world/`](00_hello_world/00_hello_world.md) | Your first script: `print()` and comments | — (setup check) | ready |
| 01 | [`01_data_types/`](01_data_types/01_data_types.md) | Numbers, text, true/false, lists | Producer | ready |
| 02 | [`02_imports/`](02_imports/02_imports.md) | Borrowing tools with `import` | Producer | ready |
| 03 | [`03_console_errors/`](03_console_errors/03_console_errors.md) | Reading error messages | — | ready |
| 04 | `04_functions/` | Reusable recipes with `def` | Consumer | coming soon |
| 05 | `05_conditionals/` | Design rules with `if / elif / else` | Operator | coming soon |
| 06 | `06_loops/` | Repeating with `for` and `while` | Producer + Consumer | coming soon |
| 07 | `07_classes/` | Objects with `class`, plus RhinoCommon | Operator + Consumer | coming soon |
| 08 | `08_data_input_output/` | Reading and writing files | Producer | coming soon |
| 09 | `09_capstone_producer_operator_consumer/` | A full mini-system | All three | coming soon |

The same lessons are available for Grasshopper in [`../Grasshopper scripts/`](../Grasshopper%20scripts/README.md).

---

## Troubleshooting

| What you see | What it means | What to do |
|--------------|---------------|------------|
| `SyntaxError` on an f-string such as `f"{name}"`, or `print` behaving strangely | The script is running in **IronPython 2**, not Python 3 | Check that `#! python3` is the first line, and that you opened the file from `ScriptEditor` and not `EditPythonScript` |
| `ModuleNotFoundError: No module named 'numpy'` | The script imports a library that isn't installed | The lessons only use built-in modules. If AI-generated code imports extra libraries, ask it to use the standard library only |
| Nothing appears in the viewport | The geometry might be off-screen or on a hidden layer | Run `Zoom` → `Extents` and check the Layers panel |
| Rhino freezes | Usually a `while` loop that never stops | Press **Esc**, or close Rhino if that doesn't work. Lesson 06 explains how to avoid this |
| `FileNotFoundError` in lesson 08 | The data folder path is wrong on your computer | Edit the line marked `# CHANGE THIS` at the top of the file |
