# Technique 3: Sketch Over Output → Modify → Debug

> **In one line:** run your script, take a screenshot of the result in Rhino, **draw your changes on top of it**, and send the marked-up image to the AI agent with your current script so it can modify it.

---

## The loop

```
   ┌──────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────┐
   │   RUN    │ ─► │ SKETCH OVER  │ ─► │ PROMPT +     │ ─► │  DEBUG   │
   │ current  │    │ screenshot + │    │ markup +     │    │ does it  │
   │ script   │    │ draw changes │    │ current code │    │ match?   │
   └──────────┘    └──────────────┘    └──────────────┘    └────┬─────┘
        ▲                                                       │
        └──────────────────────── repeat ───────────────────────┘
```

**What's new compared with Techniques 1 and 2:**

| | Technique 1 | Technique 2 | **Technique 3** |
|-|-------------|-------------|-----------------|
| You start from | nothing | nothing | **a script that already works** |
| You send | words | words + a sketch | words + **your output with changes drawn on it** + **the current code** |
| You ask for | a new script | a new script | a **modified** script |

This is how designers usually work: you rarely start from a blank page. You look at what you have, draw over it ("this bit higher, remove this, curve this"), and iterate. The markup is a **design crit on your own output**.

---

## The task

Start from the **rotated brick screen** from [Technique 2](../Technique%202/Prompt_Image_Script_Debug.md). The design change is:

> **A sine wave controls the top profile of the wall.** Bricks above the wave are removed, so the top edge of the wall rises and falls.

This is the markup used for this example: a Rhino screenshot with the change drawn in green.

![Brick wall with a sine wave sketched over it](Edited%20sketch.png)

| Role | What the **new** part of the script does |
|------|------------------------------------------|
| **Producer** | works out the wave's height at any point along the wall |
| **Operator** | keeps a brick only if its top sits below the wave |
| **Consumer** | draws the wave as a curve so you can compare it with your markup |

Everything from Technique 2 (stretcher bond, rotation per course) stays the same.

---

## Step 1: Capture your output

1. Run the Technique 2 script so the wall is in the viewport.
2. Pick a view that shows the change clearly. For a change to the **top profile**, a **Front** view is clearest. A Perspective view (like the example) looks nicer but makes heights harder to read.
3. Capture the view:
   - Rhino command **`ViewCaptureToFile`**, or
   - Windows **Snipping Tool** (`Win + Shift + S`) / Mac **`Cmd + Shift + 4`**.

> **Tip:** to make the bricks show up in the capture, right-click the Python component's `bricks` output and choose **Bake**, or just capture with the Grasshopper preview on.

---

## Step 2: Sketch over it

Draw your change on top of the screenshot. Use any tool: a tablet and pen, an iPad, Paint, PowerPoint's draw pens, or a phone photo of a printout you drew on. You can also draw curves **in Rhino** on a bright-coloured layer and capture again.

Rules for a markup the AI can read:

| Do | Why |
|----|-----|
| Use **one bright colour** that isn't in the model | The AI can tell your markup from the geometry |
| **Hatch** areas to remove (like the left and right of the example) | Hatching is the standard drawing sign for "this area" |
| Add a **short label** that names the idea ("Sine wave to control top profile") | The label tells the AI *what* the line means, not just where it is |
| Make **one change per markup** | Two changes at once are hard to debug when one goes wrong |
| Keep **leader lines** (label pointers) short and clearly separate from the main line | In the example, the leader from the label runs into the wave. The AI may read it as part of the wave |

### Read your markup before you send it

Look at `Edited sketch.png` as if you were the AI. Some things are clear, and some are **ambiguous**:

| What the markup shows | Question it leaves open | Decision used in the reference script |
|-----------------------|-------------------------|----------------------------------------|
| Hatching above the wave on the left and right | Clear: remove those bricks | Remove every brick whose top is above the wave |
| The wave rises **above** the current top of the wall in the middle | Should the wall **grow** there, or only be cut down? | Grow: the wall gets as many courses as the highest point needs |
| About **one** full wave along the wall, starting low on the left | How many waves, and where does it start? | `wave_count = 1`, `wave_shift = -60°` so it starts low |
| Peak and trough heights | Not dimensioned (and it's a perspective view) | Middle height 600 mm, ±250 mm swing: 350 mm to 850 mm |
| A whole brick sticks out above the curve | Remove whole bricks, or **cut** bricks along the curve? | Whole bricks only: real bricks aren't sliced |
| Nothing drawn about rotation | Should rotation change? | No. Keep Technique 2's rotation per course |
| The tail running to the label | Is that part of the wave? | No, it's a leader line. Ignore it |

> **Lesson:** a markup says *where* and roughly *what*. Write the rest (numbers, whole vs cut, grow vs cut, what must **not** change) in your prompt.

---

## Step 3: Prompt + markup + current code

Attach `Edited sketch.png` to your AI agent (Claude, ChatGPT, Copilot, Gemini…) and send this prompt. **Paste your current script** where it says so: the agent can only modify code it can see.

```text
Below is my current Grasshopper Python 3 script. It builds a rotated brick
screen wall in stretcher bond (units: mm, wall in the XZ plane, Z up).

The attached image is a screenshot of its output in Rhino, with my design
change sketched over it in green:
- The green wave is a SINE WAVE that controls the TOP PROFILE of the wall.
- Hatched areas above the wave mean: remove those bricks.
- The green line running to the text label is only a leader line. Ignore it.

Please modify the script so that:
- The top edge of the wall follows a sine wave along the wall's length (X).
- A brick is kept only if its top is below the wave. Remove whole bricks; do not cut them.
- Where the wave is higher than the current wall, the wall grows: work out
  the number of courses from the highest point of the wave, and remove the
  'courses' input.
- Add inputs: base_height (middle height of the wave), wave_amplitude
  (how far it swings up and down), wave_count (how many waves along the wall),
  wave_shift (where the wave starts, in degrees).
- Add an output 'profile': the wave as a curve in the plane of the wall.

Keep everything else the same: stretcher bond, rotation per course, all other
input and output names, Python 3, Rhino.Geometry and math only, a comment on
every line.

Before the code:
1. List exactly what you changed, and what you kept.
2. Give me a table of NEW or REMOVED component inputs and outputs only:
   Name | Type hint | Access | What to connect.

My current script:
[paste your Technique 2 script here]
```

> **Why "list exactly what you changed"?** When you modify a working script, the risk is that the AI quietly rewrites things you didn't ask about. The list lets you check that it did only what you asked.

---

## Step 4: Update the component

Paste the modified code into the **same** Python 3 Script component, then update its parameters. Only the changed ones need touching:

| Change | Name | Type hint | Access | Connect to |
|--------|------|-----------|--------|------------|
| **Remove** | `courses` | — | — | Zoom in, click **⊖** next to it (or right-click → Remove) |
| **Add** | `base_height` | float | Item | Number Slider, 100 – 1500, start 600 |
| **Add** | `wave_amplitude` | float | Item | Number Slider, 0 – 500, start 250 |
| **Add** | `wave_count` | float | Item | Number Slider, 0.5 – 5, start 1 |
| **Add** | `wave_shift` | float | Item | Number Slider, -180 – 180, start -60 (degrees) |
| **Add output** | `profile` | — | — | Shows the wave curve; leave it previewing |

These stay exactly as in Technique 2: `wall_length`, `course_gap`, `bricks_per_course`, `brick_length`, `brick_depth`, `brick_height`, `max_rotation`, and the outputs `out`, `bricks`, `centres`, `angles`.

With the start values, `out` should show **12 courses, 97 bricks** and a wave from **350 to 850 mm**.

---

## Step 5: Debug

### 5a. Errors (red or orange component)

Same as [Technique 1](../Technique%201/Prompt_Script_Debug.md#step-3-debug): send the exact message, your input names and type hints, what you expected and what you see. One error is especially common in this technique:

| Error | Usual cause | Fix |
|-------|-------------|-----|
| `NameError: name 'base_height' is not defined` | You pasted the new code but didn't add the new input, or named it differently | Add the input with exactly the name in the code |
| `NameError: name 'courses' is not defined` | The agent removed `courses` from the inputs but still uses it somewhere | Send the error back: *"courses is still used on line N but is no longer an input"* |

### 5b. Mismatches: compare the new output with your markup

Capture the **same view** again and send both images:

```text
Image 1 is my markup. Image 2 is what the modified script produces from
the same view. List the differences, most important first, then fix only
those. Keep all other behaviour the same.
```

### Mismatches you are likely to see in this exercise

| What you see | Usual cause | Tell the agent |
|--------------|-------------|----------------|
| The wall **bends in plan**, snaking left and right in the Top view | The wave was applied to Y (depth), not to the top edge | *"The wave controls the wall's HEIGHT along X, not its position in plan."* |
| Bricks are **sliced** along the curve | The agent trimmed the geometry with the curve | *"Remove whole bricks whose top is above the wave. Don't cut bricks."* |
| Bricks get **taller or shorter** instead of disappearing | The wave scaled the bricks | *"Every brick stays 65 mm high. The wave only decides which bricks exist."* |
| The wall is **cut** but never **grows** above its old height | The number of courses is still fixed | *"Work out the number of courses from the highest point of the wave."* |
| The wave is **upside down** or starts in the wrong place | Phase or sign of the sine | Change `wave_shift` yourself first. It's a slider for exactly this |
| An odd **kink or extra tail** at the right end | The agent read the leader line as part of the wave | *"The line to the label is a leader line, not part of the wave."* |
| The **rotation is gone**, or other inputs were renamed | The agent rewrote more than asked | *"Restore the rotation per course and the original input names. Only add the wave."* |
| `profile` curve appears **on the ground** | Wave drawn in the XY plane | *"Draw the profile in the XZ plane, on the wall."* |

---

## Once it works

Sketch a new change over the new output and go around the loop again. Ideas:

1. Draw a curve **in Rhino** and ask: `Replace the sine wave with a curve input I draw in Rhino, called top_curve.` (Your own sketched line now drives the wall directly.)
2. Circle an area of the wall and write "more open here": `Bricks inside the circled area should rotate more.`
3. Draw an arrow along the wall and write "rotation follows the wave": `Make each brick's rotation follow the wave height instead of the course number.`
4. Draw a doorway-shaped hatch at the bottom: `Leave an opening 900 mm wide and 2100 mm tall where I hatched.`

---

## Check yourself

- [ ] I captured my output from a view that shows the change clearly.
- [ ] My markup uses one bright colour, hatching for "remove", and a short label.
- [ ] I wrote down the decisions my markup didn't show (numbers, whole vs cut, grow vs cut) in my prompt.
- [ ] I sent the **current code** with the markup, and asked the agent to list what it changed.
- [ ] I updated only the changed inputs and outputs on the component, and checked the result against the markup from the same view.
- [ ] I can point to the **new** lines in the script and say which are Producer, Operator and Consumer.

---

## Tutor reference

A working version of the modified script is in [`Sketch_Over_Output.py`](Sketch_Over_Output.py) in this folder. Its header lists exactly what changed from the Technique 2 script. Students should try the loop with their own agent first, then compare their result with it.
