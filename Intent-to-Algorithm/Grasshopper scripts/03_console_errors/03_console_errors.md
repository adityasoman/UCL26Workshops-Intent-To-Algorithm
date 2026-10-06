# Lesson 03 · Console errors

**Environment:** Rhino 8 Grasshopper, Script component (Python 3) · **Code:** [`03_console_errors.py`](03_console_errors.py) · **Role:** debugging skill (all three roles)

## What is this concept?

Every programmer, and every AI, writes code with mistakes. When Python can't do what a line asks, it stops and reports an **error message** (also called a **traceback**). The message isn't a judgement; it's a note telling you exactly **where** and **why** it stopped.

### Component colours

| Colour | Meaning |
|---|---|
| Grey | ran fine |
| **Orange** | **Warning**: it ran, but something needs attention (often an input with no data connected) |
| **Red** | **Error**: the code stopped |

Hover over the small **balloon** at the top of an orange or red component to read the message. The **`out`** output shows the full message, including the **line number**.

### Reading a traceback

```text
Traceback (most recent call last):
  File "...", line 62, in <module>                         <- 3. WHERE (line number)
    label = "Height: " + height                               <- 2. WHICH line of code
TypeError: can only concatenate str (not "float") to str      <- 1. WHAT went wrong
```

**Read it from the bottom up:**

1. The **last line** gives the **error type** (`TypeError`) and a message.
2. Just above it is the **line of code** that failed (if shown).
3. The **line number** tells you where to look in the editor.

### Two families of error

| Family | Errors | What happens |
|---|---|---|
| **Syntax** errors | `SyntaxError`, `IndentationError` | The code isn't written as valid Python, like a sentence with broken grammar. Python refuses to run **any** of it, so no outputs are produced. |
| **Runtime** errors | everything else | Python runs line by line and stops **at** the broken line. |

### The six errors you'll see most often

| Error | Usual cause |
|---|---|
| `SyntaxError` | broken grammar: a missing quote, bracket or colon |
| `IndentationError` | the spaces at the start of a line are wrong |
| `NameError` | a name Python doesn't know. **In Grasshopper this is very often an input named differently from the code.** |
| `TypeError` | mixing types that don't go together (text + number) |
| `IndexError` | asking a list for a position that doesn't exist |
| `AttributeError` | asking for a tool that doesn't exist (AI tools often invent ones) |

## Why does it matter for design?

AI-generated scripts often fail on the first run. If you can read the error, you can fix it yourself, or give the AI the **exact** message so it can fix it properly instead of guessing.

## Where this sits in the Workshop

Not a single role: this is the debugging skill you'll use in all three.

## Component setup

Zoom in on the component and use **⊕ / ⊖** to add or remove parameters. Right-click each one to rename it, set its **Type hint**, and set **Item** or **List Access**.

**Inputs**

| Name | Type hint | Access | Connect to |
|---|---|---|---|
| `floors` | `int` | Item Access | Number Slider, 1–30, default 10 |
| `floor_height` | `float` | Item Access | Number Slider, 2.5–5.0, default 3.5 |

**Outputs**

| Name | Type | Notes |
|---|---|---|
| `tower` | Box | the tower |
| `info` | text | connect a Panel |
| `out` | built-in | `print()` messages **and error details**; connect a Panel |

## How to run

1. Place a **Python 3 Script** component (Maths tab → Script panel).
2. Set up the inputs and outputs exactly as listed above.
3. Double-click the component, paste the whole `.py` file, then **Run**.
4. It should be **grey**, with a tower box in Rhino.
5. Move `floors` above 17: the component turns **orange** (our own warning, Step 2).
6. Go to **Step 3** and break the script **one block at a time** (see below).

## Step by step

### Step 1 · A working tower
`rg.Box` makes a box from a base plane and three size ranges (`Interval`s), one each for x, y and z. RhinoCommon is covered properly in lesson 07.

### Step 2 · Your own warning message
`ghenv` is a special variable meaning *this component*. `ghenv.Component.AddRuntimeMessage(level, text)` adds a balloon message. Level `Warning` turns the component **orange**; `Error` would turn it **red**. **A warning is a message you choose to send. It doesn't stop the script. An error does.** (`if` statements are taught in lesson 05.)

## Break it

For each block in Step 3: **delete the `# ` at the start of the marked line, run, watch the component turn red, read the balloon and the `out` Panel, then put the `# ` back** before trying the next one.

### Break it 1 · SyntaxError
```python
print("Tower A is tall)
```
- **You'll see:** `SyntaxError: EOL while scanning string literal` (newer Pythons say *unterminated string literal*)
- **Why:** the closing quote is missing, so Python can't tell where the text ends.
- **Notice:** **nothing** ran. Every output is empty, even the tower from Step 1.
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
print(Floors)
```
- **You'll see:** `NameError: name 'Floors' is not defined`
- **Why:** the input is called `floors` (small f). Names are **case-sensitive**. This is **the most common Grasshopper error**: the code uses a name that doesn't exactly match the input's name. Try the reverse too: rename the `floors` input to `Floors` and see which line breaks.
- **Fix:** `print(floors)`

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
- **Why:** text has a tool called `.upper()`, not `.uppercase()`. Python can't find a tool with that name. AI tools invent names like this surprisingly often.
- **Fix:** `name.upper()`. When unsure, check the docs or use `dir(name)`.

## Try this

1. Break each block one at a time and, **before** reading its explanation, say: the error type, the line number, and your guess at the cause.
2. Disconnect the `floors` slider. The component turns orange or red. Read the balloon: what is Grasshopper telling you?
3. Move `floors` above 17 to see our own orange warning. Change `Warning` to `Error` in Step 2. What changes, and does `tower` still have a box?

## Ask the AI

Paste one of these into any AI chat tool. See [`Prompt guidelines`](../../Prompt%20guidelines/README.md) for more.

**Template for any error, to get an explanation rather than just a fix:**

```text
I'm running a Python 3 script in a Rhino 8 Grasshopper Script component.
Its inputs are <names, type hints, access> and its outputs are <names>.
The component is red. Here is the full message from the 'out' output:
<paste it>
Here is the line it points to and the 5 lines above it:
<paste code>
Explain in plain English what the error means and why it happened,
THEN suggest a fix. Don't rewrite the whole script.
```

```text
What's the difference between an orange and a red Grasshopper component,
and how do I send my own warning from a Python 3 Script component?
```

```text
Why does Grasshopper say NameError when my code uses a variable that I can
see as an input on the component?
```
