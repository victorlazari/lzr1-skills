# Process: apply the skill to a README

Run the steps in order. Each ends with something you can check. `KIT` is this skill's folder.

## 0. Pick the mode

| The user says | Mode |
| :--- | :--- |
| "make an animated README", a new README | **create**: steps 1 to 8 |
| "improve", "fix", "review my README", one exists already | **improve**: `references/improve.md`, then step 4 onward as needed |
| "re-render", "the copy changed" | **render**: steps 6 and 7 only |

## 1. Read the project

Read the README, `docs/`, the package file, entry points, the CHANGELOG and the last releases.
Write three lines: who uses it, what they do with it, what is true today.
**Check:** every feature you plan to mention has a file, command or release behind it.

## 2. Draft the copy in chat

Follow `KIT/references/writing-guide.md`: headline, one or two sentences, "Sound familiar?", who it is
for and not for, before and after, how it works, quick start. Keep it short. Show it before building anything.
**Check:** the headline passes the ten-second test: a stranger can say what it is and who it is for.

## 3. Ask which style

Copy `KIT/assets/style-gallery.html` somewhere the user can open and give the absolute path. Ask in plain words:
"Open this, click the style you like and paste me the line it gives you (for example `style: clay`).
Or tell me what the project is and I will suggest one."

- They name a style: set `"style"` in the scenes file.
- They ask for a suggestion: pick one and give one line of why. Developer tools fit `terminal`, `ascii`,
  `blueprint`, `holo`. A friendly product fits `clay`, `cutpaper`, `brutalist`. A serious or finance
  product fits `typographic`, `artdeco`, `glass`.
- They want to keep their colours: leave `"style"` out and use `theme`.
- They do not care: `brutalist` plus their `theme`, and say so.

## 4. Fill the scenes

Copy `KIT/templates/readme-scenes.example.json` to the project root as `readme-scenes.json` and replace every
`data` block with this project's copy. Sizes: hero 1600 x 800, before-after 1200 x 680, how-it-works 1200 x 660.
Delete the example `theme` block when a style is chosen, because `theme` wins over the style's palette.
Write the `alt` for every scene.
**Check:** `python3 KIT/scripts/render.py --check` prints no problems.

## 5. Render

`python3 KIT/scripts/render.py`. Needs Python 3.9+, `pip install playwright pillow`, and
`python3 -m playwright install chromium`. ffmpeg on PATH gives smaller GIFs.
Open the GIFs or the still PNGs and look at them. Fix overflowing text by shortening the copy, never by
shrinking the template.
**Check:** no size warning, no clipped text.

## 6. Assemble the README

Use `readme-snippets.md` (written next to the scenes file) for the image lines and alt text. Keep install and
usage sections that already work and move them below the story. Add a caption under any illustration.

## 7. Audit

`python3 -I KIT/scripts/audit_readme.py README.md`. Fix every ERROR. Read each WARN and decide.
**Check:** `0 error(s)`.

## 8. Show the user, then stop

Show the README and the GIFs. List the claims you flagged for lack of a source. Commit and push only after
the user approves.
