# Lesson 00 · Hello World

**Environment:** Rhino 8 Grasshopper, Script component (Python 3) · **Code:** [`00_hello_world.py`](00_hello_world.py) · **Role:** setup check

## What is this concept?

"Hello World" is traditionally the first program anyone writes in a new language. It does one thing: it shows a message. That proves three things work:

1. the component is a **Python 3 Script** component,
2. your pasted code runs,
3. you know where the results appear: the **outputs**.

Two ideas to notice:

- **Comments.** Lines starting with `#` are comments. Python ignores them; they are notes for humans. Every file in this workshop explains itself through short comments like these.
- **`print(...)`** is a **function**: a ready-made instruction. In Grasshopper, whatever you print appears on the **`out`** output. Text must be inside quotes, `"like this"`.

To send a result out of the component properly, you **store it in a variable with the same name as an output**. Here that output is `info`.

## Why does it matter for design?

`print()` and outputs are how a script talks back to you. You'll use them constantly to check what your design data and rules are doing.



## Component setup

Zoom in on the component and use **⊕ / ⊖** to add or remove parameters. Right-click each one to rename it.

**Inputs:** none. Remove the default `x` and `y` inputs with ⊖.

**Outputs**

| Name | Type | Notes |
|---|---|---|
| `info` | text | connect a Panel |
| `out` | built-in | `print()` messages; connect a Panel |

## How to run

1. Place a **Python 3 Script** component (Maths tab → Script panel).
2. Set up the outputs as listed above.
3. Double-click the component, paste the whole `.py` file, then **Run**.
4. You should see `Hello World` in both Panels.

## Try this

1. Change the text in `info` to your own name. Only one Panel changes. Which one, and why?
2. Add a second line, `print("Hello Bartlett")`, and run. Python runs lines from top to bottom, in order.
3. Delete one of the quote marks. The component turns red: that's your first error (lesson 03).

## Ask the AI

Paste one of these into any AI chat tool. See [`Prompt guidelines`](../../Prompt%20guidelines/README.md) for more.

```text
I'm learning Python in a Rhino 8 Grasshopper Script component (Python 3).
What is the difference between print() and assigning a value to an output variable?
```

```text
What is a comment in Python and why do programmers use them?
```
