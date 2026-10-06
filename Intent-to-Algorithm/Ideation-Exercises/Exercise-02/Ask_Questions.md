# Exercise 02: Ask Questions — let the AI interview you

> **In one line:** instead of asking the AI for an answer, ask it to **ask you questions, one at a time**, until your idea is clear enough to become a rule or a script.

---

## What it is

Most people use an AI chatbot like a vending machine: type a request, get a result. The problem is that a vague request forces the AI to **guess** what you mean, how big things are, and what you are allowed to change. You get *an* answer, but it is the AI's design, not yours.

The **Ask Questions** technique flips this around. You tell the AI:

1. what you are trying to do,
2. to **ask clarifying questions one at a time**, and
3. **not to make any assumptions**.

The AI then interviews you, like a tutor at a desk crit. Each answer you give turns a fuzzy intention into something explicit: a number, a rule, an input, an output. When you have answered enough, you ask it to summarise — and that summary is the plan for your script.

You already used this in **[Exercise 01](../Exercise-01/Prompts.md)** to render a whitecard image. Here we use the same move for **design logic and Python**.

---

## Why it matters for this workshop

The workshop is about going from **intent → algorithm**. A computer cannot run a feeling or an adjective. It can run a rule:

> *"If [something you can measure] is less than [a number], then change [a property of the geometry] by [an amount]."*

The gap between your intention and that sentence is a set of **decisions**. The Ask Questions technique makes the AI help you find those decisions — but **you** make them. That keeps the design yours and makes the final script something you can check line by line.


---

## The basic prompt

Copy this, fill in the brackets, paste it into any chat AI (Claude, ChatGPT, Copilot, Gemini…).

```text
I am an architecture student learning Python in Rhino 8 / Grasshopper.
My design intention is: [describe your idea in one or two sentences].

Before suggesting any solution or code, ask me clarifying questions
ONE AT A TIME. Wait for my answer before asking the next one.
Do not make any assumptions.

Focus your questions on:
- what information the script starts with (inputs),
- the rules that turn that information into decisions,
- what geometry or colour the script should produce (outputs).

When I type "SUMMARISE", stop asking and write my answers up as:
1. a one-paragraph design intent,
2. a table of inputs (name, type, example value),
3. the rules as numbered "if … then …" sentences,
4. the outputs.
Do not write any code yet.
```

### Useful follow-up lines

| When you want to… | Type this |
|-------------------|-----------|
| Stop the questions early | `Make assumptions for the rest of the questions, and list every assumption you made.` |
| Get unstuck on a question | `I don't know — give me 3 options with a short pro and con for each.` |
| Push back on a question | `That doesn't matter for this design. Skip it and ask the next one.` |
| See how far you are | `How many more questions do you think you need? What are they about?` |
| Finish | `SUMMARISE` |
| Move on to code | `Now write the Python 3 script for a Grasshopper Script component, using only the standard library and Rhino.Geometry. Comment every line.` |

---

## Example prompts

Each example is a starter prompt for a different moment in your work. Replace the `[brackets]` with your own project. The questions listed are the *kind* you should expect — every chat will be different, and that is the point.

### Example 1 — Clarify a vague intention

Use when you have a feeling about the design but no rule yet.

```text
My design intention is: [your intention, e.g. "the building should
respond to its surroundings"]. Ask me clarifying questions one at a
time. Do not make any assumptions. Do not write code until I say
"SUMMARISE".
```

Questions you might get:
- *What exactly should change in the design — size, position, shape, or colour?*
- *What should it respond to, and how could that be measured?*
- *Is the response on/off, or gradual?*
- *What stays fixed and what is the script allowed to change?*

### Example 2 — Turn a rule into steps (pseudocode)

Use when you know your rule but not how a script would carry it out.

```text
My rule is: [your rule, e.g. "elements closer to X get bigger"].
Ask me one question at a time about any missing detail needed to write
this as pseudocode (plain-English steps). Then write the pseudocode,
not Python.
```

Questions you might get:
- *What is X — a point, a curve, or a region you draw in Rhino?*
- *What are the smallest and largest values allowed?*
- *Is the change smooth, or in fixed steps?*
- *What happens exactly at the boundary?*

👉 That last question is an **edge case** — the kind of detail that breaks scripts. See lesson **05 (conditionals)**.

### Example 3 — Explore options before choosing

Use when you can imagine several ways to do something and want to compare them.

```text
I want to [your goal]. Ask me questions one at a time to understand
my priorities. Then give me 3 different rule sets that would achieve it,
with a short pro and con for each. Do not choose for me.
```

Questions you might get:
- *Which matters more to you: control, variety, or simplicity?*
- *Do you want the same inputs to always give the same result?*
- *How many sliders are you happy to manage in Grasshopper?*

### Example 4 — Learn from a reference

Use when you have an image, precedent or sketch you want to borrow logic from.

```text
I want to make a script inspired by [a reference image or project].
Ask me clarifying questions one at a time about what I want to borrow
from it and what I want to change. Do not make assumptions.
When I say SUMMARISE, list the sliders and inputs I will need.
```

Questions you might get:
- *Which quality of the reference matters most to you?*
- *What would you change to make it your own?*
- *Which parts should be controlled by a slider, and which are fixed?*

### Example 5 — Debug a script

Use when your script runs but does not do what you expected.

```text
My script runs but [describe what goes wrong]. Here is the code:
[paste code]. Before suggesting a fix, ask me questions one at a time
to find out what I expected and what I actually see.
```

Questions you might get:
- *What values are connected to each input, and is the access set to Item or List?*
- *What does the `out` panel print?*
- *What did you expect to see, and what do you see instead?*

👉 See lesson **03 (console errors)** and the Grasshopper README troubleshooting table.

### Example 6 — Understand code you were given

Use when the AI (or a classmate) gave you code you don't fully understand.

```text
Here is a script: [paste code]. Don't explain it all at once. Ask me
one question at a time to check whether I understand each part, and
explain only the parts I get wrong.
```

Questions you might get:
- *What do you think this line produces?*
- *Why do you think this loop runs that many times?*
- *Which part of the script would you change to make [something] bigger?*

---

## Tips for a good interview

- **Answer with numbers whenever you can.** "Quite big" leaves the AI guessing; "between 3 and 12 m" does not.
- **It's fine to say "I don't know".** Ask for options, choose one, and you've made a design decision.
- **Keep it to one question at a time.** If the AI sends a list of ten questions, reply: `One at a time please.`
- **Don't let it run forever.** 5–10 questions is usually enough. Then `SUMMARISE`, or tell it to make (and list) assumptions.
- **Read the summary critically.** Is every rule something *you* decided? If not, change it before asking for code.
- **Keep your summary.** Paste it at the top of your script as comments — it becomes the explanation of your code.

---

## Exercise (15 min)

1. Pick an intention from your own project.
2. Use **the basic prompt** above and answer at least 5 questions.
3. Type `SUMMARISE`.
4. In the summary, mark each line as **P** (Producer), **O** (Operator) or **C** (Consumer).
5. Compare with your neighbour: did the AI ask you the same questions? Which question changed your design the most?

**Upload:** save the chat summary as a `.md` file in your `Individual-Assignments/Firstname-Lastname/Assignment-NN/` folder.

---

## Check yourself

- [ ] I can say what my script **starts with**, what **rules** it applies, and what it **produces**.
- [ ] Every rule is written as **if … then …** with real numbers.
- [ ] I decided the important things myself; the AI's assumptions are listed and I agree with them.
- [ ] I could explain the summary to a tutor without the chat window open.
