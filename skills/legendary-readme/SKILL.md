---
name: legendary-readme
description: Build professional, visually stunning, dynamic, and scientifically rigorous GitHub README.md files. Use when asked to write, rewrite, theme, or polish a README (open source, enterprise, or pyOpenSci), including banners, badges, ASCII art, diagrams, tables, tone, and light/dark mode.
---

# Legendary README Architect

This skill builds world-class `README.md` files for open-source projects, enterprise software, and scientific Python packages. It uses dynamic media workflows (GIFs, charts, PDFs, videos, light/dark mode images) and adheres to strict formatting standards.

## Workflow

1. **Analyze Project Context:** Read the target repository's code, structure, and stated purpose.
2. **Select Target Template:** Ask the user to confirm the README type:
   - **Standard Open Source:** General-purpose projects.
   - **Enterprise/Tooling:** Complex applications requiring deep configuration sections.
   - **Scientific (pyOpenSci):** Packages undergoing pyOpenSci peer review.
3. **Design Visual Strategy:** Propose a visual hierarchy to the user.
   - Suggest where to use GIFs for demonstrations.
   - Suggest where to use charts or diagrams for architecture (see `references/tables-diagrams-workflows.md`).
   - Plan light/dark mode safe banners and badges (see `references/theme-engine.md` and `references/visual-style-system.md` in the Reference Map).
   - Suggest where PDFs or videos can be linked or embedded.
4. **Generate Content:** Write the README according to the selected template and visual strategy, pulling tone, readability, and ASCII/animation guidance from the Reference Map as needed.
5. **Review & Refine:** Validate against the `references/visual-arsenal.md` and `references/sections-encyclopedia.md`.

## Required References

You MUST read the following references before generating the README:
- `references/visual-arsenal.md`: Rules for badges, banners, GIFs, charts, and theme-safe images.
- `references/sections-encyclopedia.md`: Standardized section content, including pyOpenSci requirements.

## Reference Map

Read these on demand, only when the task matches:
- `references/complete-reference.md`: when starting on an unfamiliar codebase; discovery protocol (structure, stack, docs audit, workflow analysis) before writing.
- `references/reading-list.md`: when the audience is unclear; who uses the repo and what they need first.
- `references/theme-engine.md`: when the user wants a cohesive theme, mascot, palette, or light/dark mode identity.
- `references/visual-style-system.md`: when choosing hex colors, badge parameters, banner URLs, or stats widgets.
- `references/char-art-and-animation.md`: when the user asks for ASCII/Unicode art, animated banners, fake terminal sessions, or retro-CRT flourishes.
- `references/tables-diagrams-workflows.md`: when building tables, Mermaid or other diagrams, or step-by-step workflow sections.
- `references/tone-and-voice.md`: when adding humor, personality, or Easter eggs.
- `references/universal-readability.md`: when simplifying language so any reader can follow it.
- `references/hall-of-fame.md`: when you need real example READMEs per tone to borrow techniques from.

## Available Templates

Use these as structural starting points:
- `templates/standard-readme.md`: general open-source projects.
- `templates/scientific-readme.md`: pyOpenSci compliant.
- `templates/minimal-geek-readme.md`: short, terse, hacker-flavored README.
- `templates/themed-project-readme.md`: README built around a single cohesive theme.
- `templates/visual-showcase-readme.md`: visuals-first README for demos and galleries.
- `templates/full-legendary-readme.md`: the full-featured README with every section and flourish.
