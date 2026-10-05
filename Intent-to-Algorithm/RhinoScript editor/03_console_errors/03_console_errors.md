# Lesson 03 · Console errors

**Environment:** Rhino 8 ScriptEditor (Python 3) · **Code:** [`03_console_errors.py`](03_console_errors.py) · **Role:** debugging skill (all three roles)

## What is this concept?

Every programmer, and every AI, writes code with mistakes. When Python can't do what a line asks, it stops and prints an **error message** (also called a **traceback**) in the Console. The message isn't a judgement; it's a note telling you exactly **where** and **why** it stopped.

A traceback looks like this:

```text
Traceback (most recent call last):
  File "...03_console_errors.py", line 71, in <module>     <- 3. WHERE (line number)
    label = "Height: " + height                               <- 2. WHICH line of code
TypeError: can only concatenate str (not "float") to str      <- 1. WHAT went wrong
```

**Read it from the bottom up:**

1. The **last line** gives the **error type** (`TypeError`) and a message.
2. Just above it is the **line of code** that failed.
3. Above that is the **line number**, so you can find it in the editor.

### Two families of error

| Family | Errors | What happens |
|---|---|---|
| **Syntax** errors | `SyntaxError`, `IndentationError` | The code isn't written as valid Python, like a sentence with broken grammar. Python refuses to run **any** of the file, not even line 1. |
| **Runtime** errors | everything else | Python runs the file line by line and stops **at** the broken line. Everything **above** it has already happened. |

### The six errors you'll see most often

| Error | Usual cause |
|---|---|
| `SyntaxError` | broken grammar: a missing quote, bracket or colon |
| `IndentationError` | the spaces at the start of a line are wrong |
| `NameError` | a name Python doesn't know (often a typo) |
| `TypeError` | mixing types that don't go together (text + number) |
| `IndexError` | asking a list for a position that doesn't exist |
| `AttributeError` | asking for a tool that doesn't exist (AI tools often invent ones, such as `rs.AddCube`) |

## Why does it matter for design?

AI-generated scripts often fail on the first run. If you can read the error, you can fix it yourself, or give the AI the **exact** message so it can fix it properly instead of guessing.

## Where this sits in Producer → Operator → Consumer

Not a single role: this is the debugging skill you'll use in all three.

## How to run

1. Open `03_console_errors.py` in the ScriptEditor (command: `ScriptEditor`).
2. Press **Run**. It should work: a tower box appears on layer `Lesson_03` and the Console ends with `Script finished without errors`.
3. Go to **Step 3** and break the script **one block at a time** (see below).

## Step by step

### Step 1 · A working tower
A box needs **8 corners**: 4 on the ground, then the same 4 raised to the roof. This part has no mistakes.

### Step 2 · Your own warning message
If the tower is taller than `height_limit`, the script prints a `WARNING`. A **warning is a message you choose to print. It doesn't stop the script. An error does.** (`if` statements are taught in lesson 05.)

## Break it

For each block in Step 3: **delete the `# ` at the start of the marked line, run, read the error, then put the `# ` back** before trying the next one. Before reading the explanation below, say out loud the error type, the line number, and your guess at the cause.

### Break it 1 · SyntaxError
```python
print("Tower A is tall)
```
- **You'll see:** `SyntaxError: EOL while scanning string literal` (newer Pythons say *unterminated string literal*)
- **Why:** the closing quote is missing, so Python can't tell where the text ends.
- **Notice:** **nothing** ran. No box was drawn, not even from Step 1. A SyntaxError stops the whole file before it starts.
- **Fix:** add the missing quote: `print("Tower A is tall")`

### Break it 2 · IndentationError
```python
    print("This line starts with spaces for no reason")
```
- **You'll see:** `IndentationError: unexpected indent`
- **Why:** in Python, spaces at the **start** of a line have meaning: they show which lines belong inside an `if` or a loop. Random spaces confuse it.
- **Fix:** delete the spaces so the line starts at the left edge.

### Break it 3 · NameError
```python
print(tower_heigth)
```
- **You'll see:** `NameError: name 'tower_heigth' is not defined`
- **Why:** no variable has that name. It's a typo, and the real variable is just `height`. Names are also **case-sensitive**: `Height` and `height` are different.
- **Notice:** the box from Step 1 **was** drawn. Runtime errors stop at the broken line, after everything above it has run.
- **Fix:** `print(height)`

### Break it 4 · TypeError
```python
label = "Height: " + height
```
- **You'll see:** `TypeError: can only concatenate str (not "float") to str`
- **Why:** `+` can join two texts, or add two numbers, but not text + number.
- **Fix:** turn the number into text first, `"Height: " + str(height)`, or use an f-string, `f"Height: {height}"`.

### Break it 5 · IndexError
```python
w = origin[3]
```
- **You'll see:** `IndexError: list index out of range`
- **Why:** `origin` has 3 items, at positions 0, 1 and 2. There is no position 3.
- **Fix:** use a position that exists, e.g. `origin[2]` for z.

### Break it 6 · AttributeError
```python
shout = name.uppercase()
```
- **You'll see:** `AttributeError: 'str' object has no attribute 'uppercase'`
- **Why:** text has a tool called `.upper()`, not `.uppercase()`. Python can't find a tool with that name. AI tools invent names like this surprisingly often (for example `rs.AddCube`, which doesn't exist).
- **Fix:** `name.upper()`. When unsure, check the docs or use `dir(name)`.

## Try this

1. Break each block one at a time and, **before** reading its explanation, say: the error type, the line number, and your guess at the cause.
2. Change `floors` to `20`. The warning from Step 2 appears, but the script still finishes. What's the difference from an error?
3. Make two mistakes at once (e.g. blocks 3 and 4). Which one does Python report? Why only one?

## Ask the AI

Paste one of these into any AI chat tool. See [`Prompt guidelines`](../../Prompt%20guidelines/README.md) for more.

**Template for any error, to get an explanation rather than just a fix:**

```text
I'm running a Python 3 script in the Rhino 8 ScriptEditor.
Here is the full error from the Console:
<paste the whole traceback>
Here is the line it points to and the 5 lines above it:
<paste code>
Explain in plain English what the error means and why it happened,
THEN suggest a fix. Don't rewrite the whole script.
```

```text
What's the difference between a SyntaxError and a runtime error in Python?
Why does a SyntaxError stop the whole file?
```

```text
An AI gave me code that uses rs.AddCube and I get an AttributeError.
How can I check which functions really exist in rhinoscriptsyntax?
```
