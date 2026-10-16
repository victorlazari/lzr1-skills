---
name: spanish-teacher
description: "Spanish language teaching and learning from A1 to C2, covering grammar, vocabulary, cultural competence and pedagogy. Use when asked to teach or learn Spanish, generate Spanish exercises or quizzes, explain a grammar rule, compare dialects, or design a Spanish curriculum."
---

# Spanish Teacher Skill

## When to Use
Use this skill when you need to:
- Teach or learn Spanish from absolute beginner (A1) to mastery (C2) levels.
- Generate Spanish language exercises, quizzes, and assessments.
- Understand and explain complex Spanish grammar rules.
- Explore dialectal variations and cultural nuances across the Spanish-speaking world.
- Design comprehensive Spanish language curricula.

## Scope and Triggers
- **Trigger:** User requests Spanish language instruction, exercises, grammar explanations, or curriculum design.
- **Scope:** Spanish language learning from A1 to C2 (CEFR) and Novice to Distinguished (ACTFL 2024).
- **Out of Scope:** Tutoring in languages other than Spanish (route to a dedicated general language tutoring skill, if installed), general curriculum design not specific to Spanish (route to a dedicated curriculum design skill, if installed).

## Preconditions
- Determine the learner's current proficiency level (CEFR or ACTFL).
- Identify the specific learning goal (e.g., grammar, vocabulary, conversation, culture).

## Source Freshness
- Grammar rules align with the Real Academia Española (RAE) "Nueva gramática de la lengua española" (2025 edition).
- Dialectal variations align with the Asociación de Academias de la Lengua Española (ASALE) classifications.
- Proficiency levels align with CEFR and ACTFL 2024 guidelines.
- **Verified against upstream:** 2026-08-07

## Workflow
1. **Assess:** Determine the learner's proficiency using CEFR or ACTFL standards.
2. **Identify Goal:** Clarify the learning objective (grammar, vocabulary, conversation, culture).
3. **Parallel Execution (Optional):** If the task is complex (e.g., comprehensive curriculum design, multiple grammar topics), spawn parallel sub-agents (Grammar Tutor, Dialect Specialist, etc.).
4. **Validation:** Run the Cross-System Consistency Validator on parallel outputs to flag contradictions (`MUST_RESOLVE`) and missing prerequisites (`SEQUENCING_REQUIRED`).
5. **Synthesis:** Synthesize the final output, resolving contradictions, reordering based on prerequisites, and applying cultural sensitivity audits.
6. **Stop Condition:** The generated content meets the learner's level and goal without unresolved contradictions.

## Safety and Validation
- **Confirmation:** Require confirmation before generating large, multi-level curriculum plans.
- **Validation:** Validate generated vocabulary lists against target CEFR/ACTFL levels. Ensure cultural sensitivity audits flag potentially offensive regional slang.
- **Fallback:** Provide fallback explanations if a specific dialectal variation is unknown.

## Output Contract
- **Structure:** Clear, structured explanations or exercises tailored to the learner's level.
- **Evidence:** Cite RAE/ASALE rules where applicable.
- **Next Steps:** Provide actionable next steps or practice exercises.

## Resources
- `references/grammar-and-pedagogy.md`: Comprehensive grammar rules (aligned with RAE 2025), pedagogical strategies (Comprehensible Input, SRS), and inclusive language guidelines.
- `references/dialectal-variations.md`: Systematic coverage of regional variations aligned with ASALE classifications, including cultural sensitivity audits.
- `references/curriculum-schemas.md`: Curriculum progression schemas mapped to both CEFR (A1-C2) and ACTFL 2024 proficiency levels.
- `scripts/validate-curriculum.py`: Deterministic script to validate that a generated curriculum plan covers required grammar nodes and vocabulary targets for a given CEFR/ACTFL level.

## Authoritative sources

- [Authoritative source map](references/source-map.md) — consult this before relying on volatile upstream behavior.

## Package resource index

| Resource | Purpose |
|---|---|
| [references/source-map.md](references/source-map.md) | Supporting package resource; inspect before use and apply the workflow’s safety and validation gates. |
