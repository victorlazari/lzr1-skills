---
name: french-teacher
description: Assess CEFR levels, generate targeted French exercises, and validate linguistic alignment using official Council of Europe descriptors.
---

# French Teacher Skill

This skill provides an operational workflow for generating, assessing, and validating French language materials strictly aligned with the Common European Framework of Reference for Languages (CEFR).

## Scope and Triggers

**Use this skill when:**
- Assessing a learner's French proficiency against CEFR levels (A1-C2).
- Generating targeted French exercises, reading passages, or grammar explanations for a specific CEFR level.
- Validating existing French materials for CEFR alignment.
- Analyzing French texts using CLI tools or NLP libraries.

**Do NOT use this skill for:**
- Deep linguistic analysis or corpus linguistics beyond standard CEFR assessment (route to `text-analyzer`).
- Generating generic language exercises not tied to a specific CEFR progression (route to `exercise-generator`).

## Preconditions

Before generating or assessing content, you must:
1. Identify the target CEFR level (A1, A2, B1, B2, C1, or C2).
2. Identify the pedagogical goal (e.g., grammar, vocabulary, reading comprehension).
3. Consult `references/grammar-curriculum.md` to ensure the target structures are appropriate for the level.

## Source Freshness

This skill relies on the official Council of Europe CEFR descriptors and established grammar curricula (e.g., CCFS Sorbonne, Lawless French). These are documented in `references/source-map.md` with verification dates. Always refer to these authoritative sources rather than relying on general knowledge.

## Workflow

1. **Assess Target Level:** Determine the target CEFR level using official descriptors in `references/source-map.md`.
2. **Identify Goal:** Define the pedagogical goal (e.g., teaching the subjunctive, practicing past tenses).
3. **Consult Curriculum:** Review `references/grammar-curriculum.md` for level-appropriate structures and vocabulary.
4. **Generate Content:** Create the materials, explanations, or assessments.
5. **Run Consistency Validator:** Ensure the generated content strictly aligns with the target CEFR level. Flag any mismatches (e.g., using B2 vocabulary in an A1 text).
6. **Run Refuter Agents:** If applicable, use Refuter Agents to challenge the content using CEFR criteria.
7. **Synthesize and Output:** Finalize the materials and output them according to the Output Contract.

## Safety and Validation

- **Read-only Discovery:** Always consult the curriculum and source map before generating content.
- **Validation:** Verify generated exercises against the CEFR grammar map. The Consistency Validator must flag level mismatches. Refuter Agents must cite official CEFR descriptors.
- **Dry Run:** When spawning sub-agents for CEFR criteria application, perform a dry run to ensure they understand the constraints.

## Failure Handling

- If the Consistency Validator flags a level mismatch, revise the content to use simpler (or more complex) structures as dictated by `references/grammar-curriculum.md`.
- If a Refuter Agent identifies an error, correct it and re-run the validation step.
- Do not repeat a failed generation attempt without adjusting the constraints or consulting the reference materials.

## Output Contract

The final output must include:
- The generated French materials (exercises, texts, explanations).
- The target CEFR level.
- A brief justification of how the materials align with the CEFR level, citing specific grammar points or vocabulary from `references/grammar-curriculum.md`.
- Any actionable next steps for the learner.

## Resources

- [Grammar Curriculum](references/grammar-curriculum.md): Detailed A1-C2 grammar progression map.
- [Advanced Linguistics](references/advanced-linguistics.md): Advanced topics (C1-C2), literature, and pragmatics.
- [CLI Tools](references/cli-tools.md): CLI and NLP tool reference for French text processing.
- [Source Map](references/source-map.md): Authoritative sources and verification rules.

## Package resource index

| Resource | Purpose |
|---|---|
| [scripts/validate-cefr.sh](scripts/validate-cefr.sh) | Supporting package resource; inspect before use and apply the workflow’s safety and validation gates. |
