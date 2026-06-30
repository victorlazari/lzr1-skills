---
name: one-page
description: Create perfect one-page presentations and reports tailored to specific audiences. Use for generating one-pagers, executive summaries, status updates, and business cases.
---

# One-Page Presentations

This skill guides the creation of highly effective, audience-tailored one-page presentations and reports. It enforces a structured discovery process to understand the target audience before generating the artifact, ensuring the right information density, focus, and tone.

## Workflow

### 1. Audience Discovery (Mandatory)

Before writing any content or designing the layout, you **MUST** ask the user to identify the target audience for the one-page presentation. 

Ask the user:
> "To ensure the presentation is perfectly tailored, who is the primary target audience for this one-pager?"
> - **Internal Teams** (Focus: Operational details, blockers, next steps)
> - **Managers** (Focus: Tactical performance, resource allocation, decisions)
> - **C-Level Executives** (Focus: Strategic impact, high-level metrics, recommendations)
> - **Customers** (Focus: Value proposition, benefits, proof points)

Wait for the user's response before proceeding to the next step.

### 2. Specification Alignment

Once the audience is identified, read the detailed specifications in `references/specifications.md` for the chosen audience.

Apply the specific rules for:
- **Focus:** Operational, Tactical, Strategic, or Value-driven.
- **Information Density:** High (Teams), Medium (Managers/Customers), or Low (C-Level).
- **Tone:** Informal, Professional, Formal, or Engaging.
- **Key Elements:** Ensure the required elements for that audience are present in the content outline.

### 3. Visual Generation

This skill relies on the `ring:visualize` skill to generate the final artifact. 

**IMPORTANT:** You must use the `ring:visualize` template and workflow to create the HTML output.

Follow these steps to generate the artifact:
1. Load the `ring:visualize` skill by reading `/home/ubuntu/skills/ring/default/skills/visualize/SKILL.md` (or the equivalent path if using the Ring marketplace). If the skill is not locally available, follow the `ring:visualize` workflow conceptually.
2. Draft an Artifact Brief as required by `ring:visualize` (Audience, Physical scene, Source facts, Entities, Relationships, Hierarchy, One-sentence message, Non-invention boundary).
3. Use the `standard.html` template foundation from `ring:visualize`.
4. Choose the appropriate diagram/layout type based on the audience specifications (e.g., operational dashboards for teams, high-level scorecards for C-levels).
5. Generate the self-contained HTML file and deliver it to the user.

If you cannot access the `ring:visualize` templates directly, ensure your generated HTML strictly follows these visual principles:
- **Visual Hierarchy:** Use size, weight, and color to guide the eye.
- **Strategic White Space:** Do not overcrowd the page.
- **Clear Typography:** Use sans-serif fonts (e.g., Inter, Arial, Helvetica).
- **Actionable Titles:** Use headlines that state a conclusion.
- **Self-Contained:** Generate a single `.html` file with inline styles or CDN links.

---

## Adversarial Verification Panel

For each significant audience-tailored one-page presentation recommendation produced by the parallel sub-agents:

1. Spawn **3 independent Refuter Agents** per finding, each with:
   - The finding in full
   - Instruction: *"Assume this finding is wrong. Find the strongest argument against it."*
   - Default stance: `refuted=true` if evidence is insufficient or ambiguous
2. A finding is **confirmed** only if ≥2 refuters fail to refute it
3. A finding is **discarded** if ≥2 refuters succeed
4. When a confirmed finding had 1 successful refuter, include the dissenting argument in the output with a `CONTESTED` label

> This prevents plausible-but-wrong audience-tailored one-page presentation recommendations from reaching the final output. The 3-vote panel eliminates single-point hallucination without requiring unanimity.

## Cross-System Consistency Validator

After all parallel agents (Audience Discovery Agent, Specification Alignment Agent, and Visual Generation Agent) complete, but **before** synthesis:

Run one **Consistency Validator Agent** with all parallel outputs that:
- Flags any pair of recommendations that logically contradict each other
  *(example: Specification Alignment Agent recommends high information density for an Internal Teams audience while the Visual Generation Agent recommends strategic white space and low density for visual clarity)*
- Notes where one agent's output is a prerequisite for another agent's recommendation
- Passes contradictions to the Synthesis Agent as `MUST_RESOLVE` items
- Passes missing prerequisites as `SEQUENCING_REQUIRED` items

## Synthesis Agent (Upgraded)

The synthesis step actively resolves rather than aggregates:

1. **`MUST_RESOLVE` contradictions**: Pick the better recommendation, annotate the reasoning, preserve the dissenting view as a footnote
2. **`SEQUENCING_REQUIRED` items**: Re-order the unified final one-page HTML presentation so prerequisites appear before the steps that depend on them
3. **Confidence calibration**: Label each finding `HIGH` / `MEDIUM` / `LOW` confidence based on refuter panel outcomes
4. **Gap analysis**: Note any analysis dimension not covered by any of the parallel agents — these are blind spots, not confirmed negatives
