---
name: legendary-readme
description: Build professional, visually stunning, dynamic, and scientifically rigorous GitHub README.md files.
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
   - Suggest where to use charts or diagrams for architecture.
   - Plan light/dark mode safe banners and badges.
   - Suggest where PDFs or videos can be linked or embedded.
4. **Generate Content:** Write the README according to the selected template and visual strategy.
5. **Review & Refine:** Validate against the `references/visual-arsenal.md` and `references/sections-encyclopedia.md`.

## Required References

You MUST read the following references before generating the README:
- `references/visual-arsenal.md`: Rules for badges, banners, GIFs, charts, and theme-safe images.
- `references/sections-encyclopedia.md`: Standardized section content, including pyOpenSci requirements.

## Available Templates

Use these as structural starting points:
- `templates/standard-readme.md`
- `templates/scientific-readme.md` (pyOpenSci compliant)
