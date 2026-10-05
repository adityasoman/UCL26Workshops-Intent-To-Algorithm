# Individual assignments

Upload your **own** work here. Each student has one folder, and inside it there is one subfolder per assignment.

> Group work goes in [`../Group-Assignments/`](../Group-Assignments/README.md), not here.

## Folder structure

```
Individual-Assignments/
└── Firstname-Lastname/                ← one folder per student, named after you
    ├── Assignment-01/
    │   ├── Assignment-01.md          ← required: describes your work (template below)
    │   ├── my_script.py              ← your code
    │   └── screenshot.png            ← images of the result
    └── Assignment-02/
        ├── Assignment-02.md
        └── ...
```

## Rules

1. **Create one folder named after yourself:** `Firstname-Lastname`, e.g. `Jane-Smith`. Use hyphens, not spaces, and use the same name every time.
2. **Create one subfolder per assignment:** `Assignment-01`, `Assignment-02`, … Always use two-digit numbers.
3. **Every assignment subfolder needs a Markdown file** with the same name as the folder, e.g. `Assignment-01/Assignment-01.md`. Use the template below.
4. **Only change files inside your own folder.** Don't edit, move or delete anyone else's work, the lessons, or these READMEs.
5. **Keep files small and useful:**
   - Code: `.py` files (and `.gh` Grasshopper files if the assignment asks for them).
   - Images: `.png` or `.jpg`, under 5 MB each.
   - Don't upload `.3dm` files over 25 MB, `.zip` files, or temporary files (`.rhl`, `.3dmbak`, `__pycache__/`).
6. **File names:** no spaces. Use `snake_case` for code (`tower_grid.py`) and hyphens or underscores for images.
7. **Never upload passwords, API keys, or personal data.**

## Uploading with a branch and pull request

Don't upload straight to `main`. Work on **your own branch** and open a **pull request (PR)** so the tutor can review it before it's merged.

**Branch name:** your name in lowercase with hyphens, e.g. `jane-smith`.

### Option A: GitHub website (no install needed)

1. Open the repository on GitHub.
2. Click the **branch dropdown** (it says `main`), type your branch name (e.g. `jane-smith`), and click **Create branch: jane-smith from main**.
3. Make sure your branch is selected, then go into `Individual-Assignments/`.
4. Click **Add file → Upload files**. Drag in your files.
   - To create folders, type the path in **Add file → Create new file**, e.g. `Jane-Smith/Assignment-01/Assignment-01.md`. Each `/` creates a folder.
5. At the bottom, choose **Commit directly to the `jane-smith` branch** and click **Commit changes**.
6. Click **Compare & pull request** (or go to **Pull requests → New pull request**, base: `main`, compare: `jane-smith`).
7. Title the PR `Jane Smith – Assignment 01` and click **Create pull request**.

### Option B: Command line / VS Code

```bash
git checkout main
git pull                                # get the latest version first
git checkout -b jane-smith              # create your branch (only the first time)
# ...add your files under Individual-Assignments/Jane-Smith/Assignment-01/
git add Individual-Assignments/Jane-Smith
git commit -m "Jane Smith - Assignment 01"
git push -u origin jane-smith
```

Then open a pull request on GitHub from `jane-smith` into `main`.

For later assignments you can reuse the same branch. Run `git checkout jane-smith` and `git merge main` first so you have the latest files.

### After you open the PR

- The tutor will review it, may leave comments, and will merge it into `main`.
- If changes are requested, push more commits to the **same branch**. The PR updates automatically.
- Don't merge your own PR.

## Assignment Markdown template

Copy this into `Assignment-NN.md` and fill it in:

```markdown
# Assignment NN · <Title>

**Student:** Firstname Lastname
**Date:** YYYY-MM-DD

## Design intent
What were you trying to achieve? (e.g. "maximise daylight to the courtyard")

## Rules / logic
How did you turn the intent into rules? Pseudocode or a short list is fine.

## Producer → Operator → Consumer
- **Producer:** what information does the script read or create?
- **Operator:** what rules does it apply?
- **Consumer:** what geometry or colour does it produce?

## Files
| File | What it is |
|------|------------|
| `my_script.py` | ... |
| `result.png` | ... |

## How to run
Which environment (ScriptEditor or Grasshopper), inputs to set, what to expect.

## AI use
Which prompts did you use? What did the AI get right or wrong, and what did you change?

## Reflection
What worked, what didn't, what would you try next?
```
