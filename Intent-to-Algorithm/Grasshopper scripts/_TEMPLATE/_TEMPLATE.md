# Lesson NN · Title

**Environment:** Rhino 8 Grasshopper, Script component (Python 3) · **Code:** [`NN_topic.py`](NN_topic.py) · **Role:** Producer / Operator / Consumer

> **Author notes (delete in a real lesson)**
> Copy this whole `_TEMPLATE` folder, rename the folder and both files to `NN_topic`, and fill in every section.
>
> **Where things go**
> - **This `.md` file** holds the explanations: the concept, why it matters, P/O/C role, full component setup, how to run, step-by-step notes, *Try this* and *Ask the AI*.
> - **The `.py` file** holds the code, plus a two-line `Inputs:` / `Outputs:` summary at the top for wiring the component. Every line gets a short comment saying what it does. Step banners point back here (`see .md → Step 2`) when a step needs more explanation.
>
> **Commenting rules for the `.py`**
> 1. Every line of code gets a comment, either at the end of the line or on the line directly above it.
> 2. Keep inline comments short (one idea, plain English). Long explanations belong in this `.md`.
> 3. The first time a technical word appears, explain it briefly inline and fully here.
> 4. Use architectural examples: plots, towers, floors, sun, park.
> 5. One NEW concept per lesson. Earlier concepts may be reused.
> 6. Split the code into demo beats with `# --- STEP n ---` banners. Use the same step numbers here.
> 7. Keep variable names identical to the RhinoScript editor version.
> 8. Aim for 40–120 lines of code, 15–20 min demo.
>
> **Grasshopper-specific rules**
> 9. Inputs are not written in the code. They arrive from the component's input parameters, already holding values.
> 10. Results leave through outputs: assign to a variable with the **same name** as an output.
> 11. Return geometry through outputs. Don't add objects to the Rhino document.
> 12. `print()` messages appear on the `out` output.

## What is this concept?

Explain the concept in plain English, as if speaking to someone who has never written code. Use an architectural analogy where you can.

## Why does it matter for design?

Link the concept to turning a design intent into rules.

## Where this sits in Producer → Operator → Consumer

| Role | Meaning |
|---|---|
| Producer | reads or creates information |
| Operator | applies rules to that information |
| Consumer | turns the result into geometry or colour |

This lesson is mainly: **______**

## Component setup

Zoom in on the component and use **⊕ / ⊖** to add or remove parameters. Right-click each one to rename it, set its **Type hint**, and set **Item** or **List Access**.

**Inputs**

| Name | Type hint | Access | Connect to |
|---|---|---|---|
| (none in this template) | | | |

**Outputs**

| Name | Type | Notes |
|---|---|---|
| `info` | text | connect a Panel |
| `out` | built-in | `print()` messages; connect a Panel |

## How to run

1. Place a **Python 3 Script** component (Maths tab → Script panel).
2. Set up the inputs and outputs exactly as listed above.
3. Double-click the component, paste the whole `.py` file, then **Run**.
4. You should see: ______ in the `info` Panel.

## Step by step

### Step 1 · ______
Notes that don't fit in a one-line code comment.

## Try this

1. Move the ______ slider. What changes in the viewport?
2. ______

## Ask the AI

Paste one of these into any AI chat tool. See [`Prompt guidelines`](../../Prompt%20guidelines/README.md) for more.

```text
I'm learning Python in a Rhino 8 Grasshopper Script component (Python 3).
Its inputs are ______ and its outputs are ______.
Explain line by line what this script does: <paste code>
```
