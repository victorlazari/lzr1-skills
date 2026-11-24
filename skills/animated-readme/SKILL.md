---
name: animated-readme
description: Write, improve or re-render a GitHub README so a visitor gets it in ten seconds, with animated GIFs rendered from HTML (hero, before and after, how it works), alt text, and an audit of the copy. Use when someone wants a better README, a README with GIFs or a demo, a project page that shows what the project does, a review of an existing README, or to re-render README animations after the copy changed.
---

# animated-readme

Read the project, write copy a visitor gets in ten seconds, render the GIFs from one scenes file, audit the
README, and show it to the user before anything is committed or pushed. Same input, same GIF.

`KIT` means this skill's folder (for example `~/.claude/skills/animated-readme`).

## Modes

- **create**: no README worth keeping. Run `references/process.md` from step 1.
- **improve**: a README exists. Run `references/improve.md`: audit, triage, fix, audit again.
- **render**: only the copy changed. Edit `readme-scenes.json`, then `render.py`, then the audit.

## Files

- `references/ideas.md`: the ideas behind the skill and why each holds. Read it once per project.
- `references/process.md`: the steps to apply it, each with a check.
- `references/improve.md`: how to improve a README that exists, with a triage table.
- `references/writing-guide.md`: README order, voice, words to cut, scene copy rules, alt text.
- `scripts/render.py`: renders every scene to a GIF (and an optional still PNG), warns over 4 MB, writes
  `readme-snippets.md`. Flags: `--config PATH`, `--only NAME`, `--check`, `--list-styles`.
- `scripts/record_html.py`: records any animated HTML page to a GIF frame by frame:
  `record_html.py page.html out.gif --w W --h H --dur S` (`--still S` writes one PNG).
- `scripts/audit_readme.py`: checks a README for em-dashes, hype words, weak alt text, missing images,
  install-first, no hero, no audience. Exit 1 on any ERROR.
- `templates/hero.html`, `templates/before-after.html`, `templates/how-it-works.html`, `templates/skins.css`:
  the three scenes and the 17 styles. Never edit them per project.
- `templates/readme-scenes.example.json`: copy to the project root as `readme-scenes.json` and fill in.
- `assets/style-gallery.html`: one page with a live sample of every style, to choose from by eye.
- `tests/test_render.py` (needs Playwright) and `tests/test_audit.py` (stdlib): the skill's own checks.

## Rules

- **Every claim comes from the repo.** A claim with no file, command or release behind it is cut or flagged.
- **Copy lives in `readme-scenes.json`, never in the templates.**
- **The user chooses the style.** Show the gallery and ask. Never pick silently unless they say to choose for them.
- **Illustrations say so.** A drawn scenario carries a caption. Never present a drawing as a real screen.
- **Every GIF has alt text** that describes what happens, not "demo".
- **No em-dash, no hype words.** The audit enforces it.
- **Nothing is committed or pushed without approval.** A README is public once it reaches the default branch.
- Fix overflowing text by shortening the copy, never by shrinking the template.

License: Apache-2.0, from the original animated-readme kit (see `LICENSE` and `NOTICE` in this folder).
