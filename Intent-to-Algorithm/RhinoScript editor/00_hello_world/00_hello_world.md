# Lesson 00 · Hello World

**Environment:** Rhino 8 ScriptEditor (Python 3) · **Code:** [`00_hello_world.py`](00_hello_world.py) · **Role:** setup check

## What is this concept?

"Hello World" is traditionally the first program anyone writes in a new language. It does one thing: it shows a message. That proves three things work:

1. the editor is open and set to **Python 3**,
2. the **Run** button runs your code,
3. you know where the results appear: the **Console**.

Two ideas to notice:

- **Comments.** Lines starting with `#` are comments. Python ignores them; they are notes for humans. Every file in this workshop explains itself through short comments like these.
- **`print(...)`** is a **function**: a ready-made instruction. Whatever you put inside the brackets is shown in the Console. Text must be inside quotes, `"like this"`.

The first line of every file, `#! python3`, looks like a comment but is special: it tells Rhino to use Python 3. Never delete it.

## Why does it matter for design?

`print()` is how a script talks back to you. You'll use it constantly to check what your design data and rules are doing.

## Where this sits in Producer → Operator → Consumer

Not yet. This is a setup check before the real lessons start.

## How to run

1. Open `00_hello_world.py` in the ScriptEditor (command: `ScriptEditor`).
2. Press the green **Run** button (or **F5**).
3. You should see `Hello World` in the Console at the bottom.

## Try this

1. Change the text to your own name and run again.
2. Add a second line, `print("Hello Bartlett")`, and run. Python runs lines from top to bottom, in order.
3. Delete one of the quote marks and run. Read the red message in the Console: that's your first error (lesson 03).

## Ask the AI

Paste one of these into any AI chat tool. See [`Prompt guidelines`](../../Prompt%20guidelines/README.md) for more.

```text
I'm learning Python in the Rhino 8 ScriptEditor (Python 3).
Explain what print("Hello World") does, word by word.
```

```text
What is a comment in Python and why do programmers use them?
```
