# Intent to &lt;algorithm&gt;

*Turn design intentions into computational systems using Grasshopper, rule-based thinking and AI-assisted coding.*
Python module, The Bartlett School of Architecture

> 🚧 **Facilitator guide in progress.** Lesson order, timings and talking points will be added here once all the lessons are written.

## What's in this folder

| Folder | What's inside |
|--------|---------------|
| [`RhinoScript editor/`](RhinoScript%20editor/README.md) | 9 Python 3 lessons to run in the Rhino 8 **ScriptEditor** |
| [`Grasshopper scripts/`](Grasshopper%20scripts/README.md) | The same 9 lessons, set up for the Rhino 8 Grasshopper **Script** component |
| [`Prompt guidelines/`](Prompt%20guidelines/README.md) | How to prompt AI to clarify intent, develop logic, and generate or debug scripts |
| `data/` | Sample site data used in lessons 08 and 09 |

## The framework used in every lesson

**Producer → Operator → Consumer**

- **Producer:** reads or extracts information (points, numbers, a file of site data).
- **Operator:** applies rules to that information (filter, compare, group, remap).
- **Consumer:** turns the result into something spatial or visual (geometry, colour).

Each lesson's header says which of these roles its code plays.

## Requirements

- **Rhino 8** (Windows or Mac). Lessons use **Python 3**, not IronPython 2.
- No extra Python packages are needed.
