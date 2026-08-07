---
name: one-page
description: Create perfect one-page presentations and reports tailored to specific audiences and use cases. Use for generating one-pagers, executive summaries, status updates, business cases, startup pitches, and product launches.
---

# One-Page Presentations

This skill guides the creation of highly effective, audience-tailored one-page presentations and reports. It enforces a structured discovery process to understand the target audience and use case before generating the artifact, ensuring the right information density, focus, and tone.

## Scope and Triggers

- **Triggers:** When the user asks to create a one-pager, executive summary, status update, business case, startup pitch, or product launch document.
- **Scope:** Gathering requirements, determining audience and use case, aligning with specifications, and generating the final HTML or PDF artifact.
- **Non-goals:** This skill does not perform deep data analysis or generate multi-page reports.

## Preconditions

1.  Identify the user's intent and the core topic of the one-pager.
2.  Ensure you have enough context to draft the content. If not, ask the user for the necessary details.

## Source Freshness

The guidelines in this skill are based on authoritative sources (Adobe, Canva, Zapier) verified on 2026-08-07. See `references/specifications.md` for details.

## Workflow

### 1. Audience and Use Case Discovery (Mandatory)

Before writing any content or designing the layout, you **MUST** ask the user to identify the target audience and specific use case for the one-page presentation.

Ask the user:
> "To ensure the presentation is perfectly tailored, who is the primary target audience and what is the specific use case for this one-pager?"
>
> **Audiences:**
> - **Internal Teams** (Focus: Operational details, blockers, next steps)
> - **Managers** (Focus: Tactical performance, resource allocation, decisions)
> - **C-Level Executives** (Focus: Strategic impact, high-level metrics, recommendations)
> - **Customers/Investors** (Focus: Value proposition, benefits, proof points)
>
> **Use Cases:**
> - **Status Update / Operational Report**
> - **Executive Summary / Business Case**
> - **Startup Pitch**
> - **Product Launch**

Wait for the user's response before proceeding to the next step.

### 2. Specification Alignment

Once the audience and use case are identified, read the detailed specifications in `references/specifications.md`.

Apply the specific rules for:
- **Focus:** Operational, Tactical, Strategic, or Value-driven.
- **Information Density:** High (Teams), Medium (Managers/Customers), or Low (C-Level).
- **Tone:** Informal, Professional, Formal, or Engaging.
- **Key Elements:** Ensure the required elements for that audience and use case are present in the content outline.

### 3. Output Format Determination

Ask the user for their preferred output format:
> "Would you prefer the final output as an interactive HTML file or a printable PDF?"

### 4. Visual Generation and Routing

Based on the chosen output format, route to the appropriate skill:

**If HTML:**
1.  Use the appropriate template from `templates/` (e.g., `templates/startup_one_pager.html` or `templates/product_one_pager.html`) as a foundation.
2.  If complex interactive or visual layouts are needed, route to `ring:visualize`.
3.  Ensure the generated HTML strictly follows the visual principles in `references/specifications.md`.

**If PDF:**
1.  Route to `typst-pdf-maker` with the generated content.
2.  Instruct `typst-pdf-maker` to adhere to the visual principles in `references/specifications.md`.

### 5. Validation

Before delivering the final artifact, validate it against the following criteria:
- Includes all required elements for the selected use case (e.g., value proposition, problem/solution, proof points, CTA).
- Output format matches the user's request (HTML or PDF).
- Visual layout adheres to best practices (visual hierarchy, white space, typography).

### 6. Delivery

Deliver the final self-contained one-pager to the user.

## Safety

- **Read-only discovery:** Always gather requirements and confirm the audience/use case before generating content.
- **No untrusted execution:** Do not execute downloaded code or scripts from untrusted sources.

## Failure Handling

- If the user provides insufficient information, prompt them for the missing details.
- If generation fails, review the error, adjust the content or layout, and retry. Do not repeat the exact same failed action.

## Output Contract

The final output must be a self-contained HTML file or a PDF document that strictly adheres to the aligned specifications and visual best practices.

## Resources

- `references/specifications.md`: Detailed specifications for audiences, use cases, and visual best practices.
- `templates/startup_one_pager.html`: Template for startup pitch one-pagers.
- `templates/product_one_pager.html`: Template for product launch one-pagers.
- `scripts/validate_html.py`: Script to perform basic validation on generated HTML files.

## Orchestration

If using parallel agents for content generation and visual design, ensure the Synthesis Agent resolves any contradictions and enforces the required sequencing (content before design).
