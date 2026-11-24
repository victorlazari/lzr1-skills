# Improve an existing README

Use this when a README exists. The aim is the smallest set of changes that makes the first ten seconds work,
not a rewrite for its own sake. `KIT` is this skill's folder.

## 1. Measure first

Run `python3 -I KIT/scripts/audit_readme.py README.md`. Save the output: it is the "before" and it goes in
the summary you give the user. Then read the first screen as a stranger would and answer in one line each:
what is it, who is it for, what does it look like working. Any answer you cannot give is a finding too.

## 2. Triage in this order

Fix in this order; the earlier ones change the most.

| Order | Finding | Fix |
| :--- | :--- | :--- |
| 1 | The first screen is install steps or a feature list (`install-first`) | Move the problem and the promise up, install down |
| 2 | No picture of it working (`no-hero`) | Add a hero scene |
| 3 | The tagline is jargon | Rewrite as the outcome, in the reader's words |
| 4 | No "Sound familiar?" | Three to six concrete moments the reader lives through |
| 5 | Alt text missing or generic (`alt-missing`, `alt-weak`) | Describe what happens, in order |
| 6 | No audience statement (`no-audience`) | One "good fit if" and one "not for you if" |
| 7 | Hype words and em-dashes | Replace with the plain thing the sentence meant |
| 8 | A stale or missing picture, a broken path (`image-missing`) | Re-render, fix the path |

Keep what already works: badges, a license line, working install steps, links others point to.

## 3. Apply

Take rows 1 to 4 through `process.md` steps 1 to 6, reusing the existing text where it is already clear.
Rows 5 to 8 are edits in place. Do not touch sections that passed.

## 4. Prove it

Run the audit again. Report before and after, for example "7 errors, 2 warnings before; 0 errors, 1 warning
after". Say what you left alone and why. Flag every claim you could not source in the repo.

## 5. Loop

If the user changes the copy later, edit `readme-scenes.json`, run `render.py`, run the audit. Do not edit
the GIFs by hand and do not edit the templates for one project.
