---
name: web-presentation-creator
description: "Design and build premium, high-performance landing pages. Use for: creating cinematic scrollytelling experiences, integrating GSAP animations, handling complex media, and generating complete HTML or ZIP packages with assets."
license: Complete terms in LICENSE.txt
---

# Web Presentation Creator Skill

This skill enables Manus to design, architect, and build premium landing pages inspired by industry leaders. It provides a complete workflow for generating production-ready HTML, CSS, and JavaScript, with a strong emphasis on scrollytelling, high-performance media handling, and complex animations.

## Scope and Triggers

- **Activates when:** The user requests a premium landing page, a cinematic scrollytelling experience, or a high-performance web presentation.
- **Non-goals:** This skill does not build slide decks or presentations (route to `frontend-slides`). It does not generate new visual assets or edit existing images (route to `imagegen`).

## Preconditions

- Detect the target audience, preferred aesthetic, and required media assets.
- Ensure the user has provided any necessary local images or videos.
- Confirm the user's intent before overwriting existing files or making destructive changes.

## Source Freshness

- Volatile facts, such as supported versions and configuration options, are documented in the reference files.
- Always verify the installed versions and current upstream documentation before applying destructive or production-impacting actions.
- Reference files include a `Verified against upstream` date to ensure the information remains current.

## Workflow

1. **Gather Requirements:** Assess the user's needs, preferred aesthetic, and required media assets.
2. **Establish Architecture:** Set up the HTML/CSS foundation for high performance, following the guidelines in `references/responsive-rules.md`.
3. **Implement Animation:** Integrate GSAP for complex timelines, following the guidelines in `references/animation-library.md`.
4. **Build Scrollytelling:** Create immersive scroll-driven sequences, following the guidelines in `references/media-handling.md`.
5. **Validate:** Run `scripts/validate-package.sh` to ensure the generated HTML/ZIP package meets the required structure and includes necessary assets.
6. **Preview (Optional):** Run `scripts/preview-server.py` to preview the generated landing page locally.
7. **Package and Deliver:** Deliver the final product as a single self-contained `index.html` file or a `.zip` archive containing the complete project. Stop when the user confirms receipt and satisfaction.

## Safety

- **Read-only discovery:** Always gather requirements and assess media assets before writing any code.
- **Confirmation:** Require user confirmation before overwriting existing files or making destructive changes.
- **Validation:** Validate the generated HTML syntax and ensure all referenced local assets exist before packaging.

## Validation

- Run `scripts/validate-package.sh` to validate the generated HTML/ZIP package.
- Ensure all referenced local assets exist before packaging.
- Provide a local preview option using `scripts/preview-server.py` before final delivery.

## Failure Handling

- If validation fails, diagnose the error using the output of `scripts/validate-package.sh` and attempt a fix.
- If the user is not satisfied with the preview, gather feedback and iterate on the design.
- Do not repeat a failed action unchanged; always attempt a different approach or tool.

## Output Contract

- The final product must be a single self-contained `index.html` file or a `.zip` archive containing the complete project.
- The output must include all necessary HTML, CSS, JavaScript, and media assets.
- The output must meet the performance and responsive rules outlined in `references/responsive-rules.md`.

## Resources

- [references/animation-library.md](references/animation-library.md): JavaScript and CSS implementations for complex animations.
- [references/media-handling.md](references/media-handling.md): Guidelines for handling user-provided media and scroll-driven transitions.
- [references/responsive-rules.md](references/responsive-rules.md): Responsive design principles and Core Web Vitals optimization.
- [references/style-presets.md](references/style-presets.md): Aesthetic presets inspired by industry leaders.
- [templates/base_template.html](templates/base_template.html): A starting point for building premium landing pages.
- [scripts/validate-package.sh](scripts/validate-package.sh): A script to validate the generated HTML/ZIP package.
- [scripts/preview-server.py](scripts/preview-server.py): A script to preview the generated landing page locally.

## Orchestration

- Use parallel work only for independent dimensions, such as generating different sections of the landing page.
- Define inputs, schemas, conflict handling, synthesis, and termination conditions for parallel work.
