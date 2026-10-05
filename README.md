# Intent to &lt;algorithm&gt;

*Turn design intentions into computational systems using Grasshopper, rule-based thinking and AI-assisted coding.*
Python module, The Bartlett School of Architecture

> 🚧 **Facilitator guide in progress.** Lesson order, timings and talking points will be added here once all the lessons are written.

## What's in this repository

| Folder | What's inside |
|--------|---------------|
| [`Intent-to-Algorithm/RhinoScript editor/`](Intent-to-Algorithm/RhinoScript%20editor/README.md) | 10 Python 3 lessons (00–09) to run in the Rhino 8 **ScriptEditor** |
| [`Intent-to-Algorithm/Grasshopper scripts/`](Intent-to-Algorithm/Grasshopper%20scripts/README.md) | The same concepts for the Rhino 8 Grasshopper **Script** component, with **different examples** from lesson 04 on |
| [`Intent-to-Algorithm/Prompt guidelines/`](Intent-to-Algorithm/Prompt%20guidelines/README.md) | How to prompt AI to clarify intent, develop logic, and generate or debug scripts |
| [`Intent-to-Algorithm/data/`](Intent-to-Algorithm/data/README.md) | Sample site data used in lessons 08 and 09 |
| [`Individual-Assignments/`](Individual-Assignments/README.md) | Where each student uploads their own work (folder per student, branch + pull request) |
| [`Group-Assignments/`](Group-Assignments/README.md) | Where each group uploads its shared work (folder per group, branch + pull request) |

## The framework used in every lesson

**Producer → Operator → Consumer**

- **Producer:** reads or extracts information (points, numbers, a file of site data).
- **Operator:** applies rules to that information (filter, compare, group, remap).
- **Consumer:** turns the result into something spatial or visual (geometry, colour).

Each lesson's header says which of these roles its code plays.

## Requirements

- **Rhino 8** (Windows or Mac). Lessons use **Python 3**, not IronPython 2.
- No extra Python packages are needed.
