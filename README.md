# Intent to &lt;algorithm&gt;

*Turn design intentions into computational systems using Grasshopper, rule-based thinking and AI-assisted coding.*
Python module, The Bartlett School of Architecture (UCL)

![Intent to <algorithm>: from site data to a rule-built structure](Intent-to-Algorithm/Presentations/Poster.png)

## The core idea

AI can now write code in seconds. The **logic and intention** behind that code still have to be designed, and that is your job as the architect.

You start with an intention: *more privacy, more daylight, more density, more connection*. A computer cannot work with "more open" or "more interesting". Someone has to decide what those words mean in numbers, rules and relationships. **That middle step, turning intention into explicit rules, is what this workshop is about.**

We work through the three stages of computational thinking, and AI helps in each one:

| Stage | What you do | How AI helps |
|-------|-------------|--------------|
| **1. Clarify the intent** | Define the problem and understand the data you have | Asks you questions, spots missing information |
| **2. Develop the logic** | Turn the intent into rules and relationships | Suggests alternatives, writes pseudocode, tests your assumptions |
| **3. Implement and test** | Build the system in Rhino / Grasshopper | Generates, explains and debugs Python scripts |

You guide the process and choose the logic. You also judge whether the result meets your intention. AI is an assistant whose work you check, not a black box.

## The framework: Producer → Operator → Consumer

Every script in this repository is organised with one simple framework that scales:

- **Producer:** reads or extracts information (points, numbers, an image, a file of site data).
- **Operator:** applies rules to that information (filter, compare, group, remap, find relationships).
- **Consumer:** turns the result into something spatial or visual (geometry, colour).

It doesn't prescribe what the final design looks like. It gives you a structure for designing computational behaviour.

## How to use this repository

Work through the folders in this order. Everything lives in [`Intent-to-Algorithm/`](Intent-to-Algorithm/).

### 1. Ideate with AI
[`Ideation-Exercises/`](Intent-to-Algorithm/Ideation-Exercises/)
Use AI to clarify an intention before writing any code.
- **Exercise 01:** render a whitecard model by letting the AI ask you questions (prompts + example images).
- **Exercise 02:** [Ask Questions](Intent-to-Algorithm/Ideation-Exercises/Exercise-02/Ask_Questions.md). The AI interviews you, one question at a time, until your idea becomes a rule.

### 2. Learn enough Python to read and check the code
There are 10 short lessons (00–09), each written twice. Pick the environment you prefer, or do both.

| Environment | Folder |
|-------------|--------|
| Rhino 8 **ScriptEditor** | [`RhinoScript editor/`](Intent-to-Algorithm/RhinoScript%20editor/README.md) |
| Grasshopper **Python 3 Script** component | [`Grasshopper scripts/`](Intent-to-Algorithm/Grasshopper%20scripts/README.md) |

| # | Lesson | P/O/C role |
|---|--------|-----------|
| 00 | Hello world: `print()` and comments | setup check |
| 01 | Data types: numbers, text, true/false, lists | Producer |
| 02 | Imports: borrowing tools | Producer |
| 03 | Console errors: reading tracebacks | — |
| 04 | Functions: reusable recipes | Consumer |
| 05 | Conditionals: design rules with `if / elif / else` | Operator |
| 06 | Loops: grids and repetition | Producer + Consumer |
| 07 | Classes and RhinoCommon | Operator + Consumer |
| 08 | Reading and writing data files | Producer |
| 09 | Capstone: a full Producer → Operator → Consumer system | All three |

Lessons 00–03 use the same example in both environments. From 04 on, the Grasshopper version uses a **different architectural example** of the same concept, so you see every idea applied twice. Keep the [Python cheat sheet](Intent-to-Algorithm/Python-Cheat%20Sheet/python-cheatsheet.pdf) open while you work.

### 3. Script with AI
[`AI-Assisted Scripting/`](Intent-to-Algorithm/AI-Assisted%20Scripting/)
Three techniques for building Grasshopper scripts with an AI agent. Each one adds more visual input:

| Technique | Loop |
|-----------|------|
| [1. Prompt → Script → Debug](Intent-to-Algorithm/AI-Assisted%20Scripting/Technique%201/Prompt_Script_Debug.md) | Describe it in words, paste the script, send errors back |
| [2. Prompt + Image → Script → Debug](Intent-to-Algorithm/AI-Assisted%20Scripting/Technique%202/Prompt_Image_Script_Debug.md) | Add a sketch, then check the result against it |
| [3. Sketch Over Output → Modify → Debug](Intent-to-Algorithm/AI-Assisted%20Scripting/Technique%203/Sketch_Over_Output.md) | Draw your changes on a screenshot of the output |

[`Prompt guidelines/`](Intent-to-Algorithm/Prompt%20guidelines/README.md) collects how to prompt at each stage (in progress).

### 4. Study precedents
Worked Grasshopper examples that rebuild real projects as rule-based systems:

| # | Example |
|---|---------|
| 10 | [Folded-paper art installation](Intent-to-Algorithm/Grasshopper%20scripts/10_Art_Installation/10_Art_Installation.md) (after Matthew Shlian) |
| 11 | [BIG Serpentine Pavilion](Intent-to-Algorithm/Grasshopper%20scripts/11_BIG_SerpentinePavillion/11_BIG_SerpentinePavillion.md) |
| 12 | [MVRDV Valley](Intent-to-Algorithm/Grasshopper%20scripts/12_MVRDV_Valley/12_MVRDV_Valley.md) |

### 5. Submit your work
- [`Individual-Assignments/`](Individual-Assignments/README.md): one folder per student, uploaded through a branch + pull request.
- [`Group-Assignments/`](Group-Assignments/README.md): one folder per group, same workflow.

## Repository map

```
README.md                      ← you are here
Intent-to-Algorithm/
├── Presentations/             poster and workshop visuals
├── Ideation-Exercises/        1. clarify intent with AI
├── RhinoScript editor/        2. Python lessons 00–09 (ScriptEditor)
├── Grasshopper scripts/       2. Python lessons 00–09 (GH) + 4. precedents 10–12
├── Python-Cheat Sheet/        quick syntax reference (PDF)
├── AI-Assisted Scripting/     3. three prompt → script → debug techniques
├── Prompt guidelines/         prompting advice per stage (in progress)
└── data/                      sample site data for lessons 08–09
Individual-Assignments/        5. student submissions
Group-Assignments/             5. group submissions
```

## Requirements

- **Rhino 8** (Windows or Mac). All scripts use **Python 3**, not IronPython 2 or the legacy GhPython component.
- No extra Python packages are needed, only the standard library plus Rhino's own `rhinoscriptsyntax` and `Rhino.Geometry`.
- Any chat AI tool (Claude, ChatGPT, Copilot, Gemini…) for the ideation and AI-assisted scripting sections.
