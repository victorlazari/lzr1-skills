# Ideas behind animated-readme

The ideas this skill is built on. Each one says what to do and why. The process file turns them
into steps; the improve file turns them into an audit.

## About the reader

1. **A visitor gives a README ten seconds.** In that time they need three answers: what is it,
   is it for me, what does it look like working. Every section either serves one of those or moves down.
2. **Open with the problem the reader has**, in their words, then the project. "Sound familiar?"
   with three to six concrete moments beats a feature list. A time, a tool and a person beat an adjective.
3. **Say who it is not for.** It costs nothing and it builds trust.
4. **Install comes after the story.** A visitor who does not yet know what the project does will not install it.

## About the pictures

5. **Show it working.** A hero GIF in the first screen. Not a logo, not a diagram of boxes.
6. **Three scenes cover most projects:** hero (prompt, work, result), before and after (pain, then outcome),
   how it works (three or four steps, then the loop). More than three GIFs slows the page for little gain.
7. **Alt text is part of the work.** Describe what happens in the order it happens, with the words on screen
   that matter. Never "demo.gif".
8. **Illustrations say so.** A drawn scenario carries a caption like "Illustration of a typical project."
   Never pass a drawing off as a real screen. Where a real recording exists, link it next to the illustration.
9. **Keep GIFs under 4 MB.** A heavy README loads slowly on GitHub. Shorten the scene before you shrink the font.

## About trust

10. **Every claim comes from the repo.** If the copy says the project does something, a file, a command or a
    release shows it. A claim with no source is cut, or flagged to the user. Planned and half-done is not "what it does".
11. **Nothing is pushed without approval.** A README is public the moment it reaches the default branch.
12. **No hype words, no em-dashes.** The cut list lives in `writing-guide.md` and `scripts/audit_readme.py` checks it.

## About the machinery

13. **Copy lives in one file** (`readme-scenes.json`), never in the templates. One decision in one place:
    change the copy, render again, the GIFs follow.
14. **Same input, same GIF.** Every animation is paused and seeked to each frame, then screenshotted. No screen
    recording, no timing luck, so a re-render after a copy fix changes only what the copy changed.
15. **The user picks the look.** 17 styles, shown side by side in `assets/style-gallery.html`. Offer a suggestion
    when asked, never choose silently. The style key is stored in the scenes file so later renders keep it.
16. **Build the lever.** Checks that a machine can do (banned words, alt text, missing files, section order)
    live in `scripts/audit_readme.py`, so the judgment calls are all that is left for the model.

## Ideas worth trying next

Not built yet. Pick one only when a project asks for it.

- A dark and light pair of every GIF through `<picture>` so the README fits both GitHub themes.
- A fourth scene for a real recording of the tool, made with `record_html.py` against the live page.
- An audit that also reads the GIF frames for text that overflows its box.
- A per-language copy file for projects with a translated README.
