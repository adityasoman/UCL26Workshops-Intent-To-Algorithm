# Lesson 00 · Hello World

**Environment:** Rhino 8 Grasshopper, Script component (Python 3) · **Code:** [`00_hello_world.py`](00_hello_world.py) · **Role:** setup check

## What is this concept?

"Hello World" is traditionally the first program anyone writes in a new language. It does one thing: it shows a message. Here it greets **you**: you type your name into a Panel, and the script answers `Hello <your name>, welcome to the Python workshop!`. That proves four things work:

1. the component is a **Python 3 Script** component,
2. your pasted code runs,
3. the script can read an **input** (your name),
4. you know where the results appear: the **outputs**.

Two ideas to notice:

- **Comments.** Lines starting with `#` are comments. Python ignores them; they are notes for humans. Every file in this workshop explains itself through short comments like these.
- **`print(...)`** is a **function**: a ready-made instruction. In Grasshopper, whatever you print appears on the **`out`** output. Text must be inside quotes, `"like this"`.

A **variable** is a name that holds a value. An input parameter called `name` arrives in the script as a variable called `name`, holding whatever text is in the Panel. In the same way, to send a result out of the component, you **store it in a variable with the same name as an output**. Here that output is `info`.

`"Hello " + name` uses `+` to **join pieces of text** into one longer piece of text. Lesson 01 shows a neater way (f-strings).

## Why does it matter for design?

`print()` and outputs are how a script talks back to you. You'll use them constantly to check what your design data and rules are doing.



## Component setup

Zoom in on the component and use **⊕ / ⊖** to add or remove parameters. Right-click each one to rename it.

**Inputs:** rename the default `x` to `name` and remove `y` with ⊖.

| Name | Type hint | Access | Connect to |
|---|---|---|---|
| `name` | `str` | Item Access | Panel with your name typed in (e.g. `Aditya`) |

**Outputs**

| Name | Type | Notes |
|---|---|---|
| `info` | text | connect a Panel |
| `out` | built-in | `print()` messages; connect a Panel |

## How to run

1. Place a **Python 3 Script** component (Maths tab → Script panel).
2. Set up the input and outputs as listed above.
3. Double-click the component, paste the whole `.py` file, then **Run**.
4. Type your name into the input Panel. You should see `Hello <your name>, welcome to the Python workshop!` in both output Panels.
5. Disconnect the input Panel: the script falls back to `Hello World, …`.

### Step notes

- **Step 1: Read the name.** `if not name:` checks whether the Panel is empty. If it is, `name` becomes `"World"`, so the script never breaks. You'll learn `if` properly in lesson 05.
- **Step 2: Say hello.** `+` joins three pieces of text into one `message`, and `print()` shows it on `out`.

## Try this

1. Change the line `info = message` to `info = "Goodbye"`. Only one Panel changes. Which one, and why?
2. Add a second line, `print("Hello Bartlett")`, and run. Python runs lines from top to bottom, in order.
3. Type a classmate's name into the input Panel. The script re-runs by itself: Grasshopper runs it again whenever an input changes.
4. Delete one of the quote marks. The component turns red: that's your first error (lesson 03).

## Ask the AI

Paste one of these into any AI chat tool. See [`Prompt guidelines`](../../Prompt%20guidelines/README.md) for more.

```text
I'm learning Python in a Rhino 8 Grasshopper Script component (Python 3).
What is the difference between print() and assigning a value to an output variable?
```

```text
What is a comment in Python and why do programmers use them?
```
