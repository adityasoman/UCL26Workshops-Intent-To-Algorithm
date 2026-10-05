# Group assignments

Upload your **group's** work here. Each group has one folder, and inside it there is one subfolder per assignment.

> Individual work goes in [`../Individual-Assignments/`](../Individual-Assignments/README.md), not here.

## Folder structure

```
Group-Assignments/
└── Group-01-GroupName/                ← one folder per group
    ├── Members.md                    ← required: who is in the group
    ├── Assignment-01/
    │   ├── Assignment-01.md          ← required: describes your work (template below)
    │   ├── system.py                 ← your code
    │   └── diagram.png               ← images of the result
    └── Assignment-02/
        ├── Assignment-02.md
        └── ...
```

## Rules

1. **Create one folder per group:** `Group-NN-GroupName`, e.g. `Group-03-Daylight`. Use the group number the tutor gave you, two digits, hyphens and no spaces.
2. **Add a `Members.md`** in the group folder listing every member's full name.
3. **Create one subfolder per assignment:** `Assignment-01`, `Assignment-02`, … Always use two-digit numbers.
4. **Every assignment subfolder needs a Markdown file** with the same name as the folder, e.g. `Assignment-01/Assignment-01.md`. Use the template below.
5. **One upload per group.** Agree on one person to upload, or each member can add their part to the same group branch.
6. **Only change files inside your group's folder.** Don't edit, move or delete anyone else's work, the lessons, or these READMEs.
7. **Keep files small and useful:**
   - Code: `.py` files (and `.gh` Grasshopper files if the assignment asks for them).
   - Images: `.png` or `.jpg`, under 5 MB each.
   - Don't upload `.3dm` files over 25 MB, `.zip` files, or temporary files (`.rhl`, `.3dmbak`, `__pycache__/`).
8. **File names:** no spaces. Use `snake_case` for code (`site_system.py`) and hyphens or underscores for images.
9. **Never upload passwords, API keys, or personal data.**

## Uploading with a branch and pull request

Don't upload straight to `main`. Work on **a branch for your group** and open a **pull request (PR)** so the tutor can review it before it's merged.

**Branch name:** `group-NN-groupname` in lowercase, e.g. `group-03-daylight`. Everyone in the group pushes to this one branch.

### Option A: GitHub website (no install needed)

1. Open the repository on GitHub.
2. Click the **branch dropdown** (it says `main`). Type the branch name (e.g. `group-03-daylight`) and click **Create branch … from main**. If a teammate already created it, just select it.
3. With your group branch selected, go into `Intent-to-Algorithm/Group-Assignments/`.
4. Click **Add file → Upload files**. Drag in your files.
   - To create folders, type the path in **Add file → Create new file**, e.g. `Group-03-Daylight/Assignment-01/Assignment-01.md`. Each `/` creates a folder.
5. At the bottom, choose **Commit directly to the `group-03-daylight` branch** and click **Commit changes**.
6. Click **Compare & pull request** (or go to **Pull requests → New pull request**, base: `main`, compare: `group-03-daylight`).
7. Title the PR `Group 03 Daylight – Assignment 01`, and list the members in the description. Click **Create pull request**.

### Option B: Command line / VS Code

```bash
git checkout main
git pull                                    # get the latest version first
git checkout -b group-03-daylight           # first member only; others: git fetch && git checkout group-03-daylight
# ...add your files under Group-Assignments/Group-03-Daylight/Assignment-01/
git add Intent-to-Algorithm/Group-Assignments/Group-03-Daylight
git commit -m "Group 03 Daylight - Assignment 01"
git push -u origin group-03-daylight
```

Then open a pull request on GitHub from `group-03-daylight` into `main`. Only one PR per group per assignment is needed.

Before you push, run `git pull` so you have your teammates' latest commits.

### After you open the PR

- The tutor will review it, may leave comments, and will merge it into `main`.
- If changes are requested, push more commits to the **same branch**. The PR updates automatically.
- Don't merge your own PR.

## `Members.md` template

```markdown
# Group NN · GroupName

| Name | Role / contribution |
|------|---------------------|
| Firstname Lastname | e.g. data and Producer scripts |
| Firstname Lastname | e.g. rules and Operator logic |
| Firstname Lastname | e.g. geometry, visuals, Consumer |
```

## Assignment Markdown template

Copy this into `Assignment-NN.md` and fill it in:

```markdown
# Assignment NN · <Title>

**Group:** Group NN · GroupName
**Date:** YYYY-MM-DD

## Design intent
What was the group trying to achieve?

## Rules / logic
How did you turn the intent into rules? Pseudocode or a short list is fine.

## Producer → Operator → Consumer
- **Producer:** what information does the system read or create?
- **Operator:** what rules does it apply?
- **Consumer:** what geometry or colour does it produce?

## Files
| File | What it is | Made by |
|------|------------|---------|
| `system.py` | ... | ... |

## How to run
Which environment (ScriptEditor or Grasshopper), inputs to set, what to expect.

## AI use
Which prompts did you use? What did the AI get right or wrong, and what did you change?

## Reflection
What worked, what didn't, what would you try next?
```
