---
name: french-teacher
description: Comprehensive French language course covering all CEFR levels from absolute beginner (A1) to mastery (C2), including pronunciation, grammar, vocabulary, conversation patterns, cultural context, linguistics, CLI tools, and NLP.
---

# French Teacher Skill

This skill provides a comprehensive guide to teaching and learning the French language, covering all Common European Framework of Reference for Languages (CEFR) levels from A1 to C2. It includes foundational grammar, advanced linguistics, computational tools for language education, and troubleshooting strategies for common learner errors.

## When to Use

Use this skill when you need to:
- Generate French language learning materials, exercises, or assessments for any CEFR level.
- Explain complex French grammar rules, such as the subjunctive mood, past tenses (passé composé vs. imparfait), or object pronouns.
- Provide guidance on French pronunciation, phonetics, and prosody (liaison, enchaînement).
- Analyze French texts for readability, vocabulary frequency, or grammatical complexity.
- Develop or configure language learning platforms, including LMS settings, spaced repetition algorithms, and automated grading rubrics.
- Troubleshoot common learner errors and provide targeted remediation strategies.
- Utilize CLI tools (grep, sed, awk) or NLP libraries (spaCy, NLTK, CamemBERT) for French text processing and corpus linguistics.

## Sub-Agent Spawning

This skill supports spawning sub-agents for parallel execution when tasks can be decomposed:

| Trigger Condition | Sub-Agent Type | Purpose |
|---|---|---|
| Multiple texts to analyze for CEFR level | Text Analyzer | Parallel readability and vocabulary profiling |
| Multiple grammar topics to generate exercises for | Exercise Generator | Parallel creation of targeted grammar drills |
| Multiple student essays to grade | Automated Grader | Parallel evaluation using specific rubrics |
| Bulk audio files to transcribe and assess | Pronunciation Scorer | Parallel speech-to-text and error detection |

### Spawning Rules
- Spawn when 3+ independent items need the same operation
- Each sub-agent receives: context, specific target, success criteria
- Results are aggregated and cross-referenced for conflicts
- Maximum concurrent sub-agents: 10

## Workflow

1. **Assess the Learner's Level:** Determine the target CEFR level (A1-C2) to ensure appropriate vocabulary, grammar, and complexity.
2. **Identify the Pedagogical Goal:** Determine whether the focus is on grammar, vocabulary, pronunciation, reading comprehension, or cultural competence.
3. **Select the Appropriate Tools:** Choose between manual explanation, CLI text processing, or advanced NLP analysis depending on the task's complexity.
4. **Generate Content/Analysis:** Create exercises, explanations, or analytical reports tailored to the specific goal and level.
5. **Review and Refine:** Ensure the content is culturally sensitive, accurate, and aligned with pedagogical best practices.

## Core Principles

- **CEFR Alignment:** All materials and assessments must be strictly aligned with the appropriate CEFR level criteria.
- **Communicative Approach:** Prioritize practical communication skills and authentic language use over rote memorization.
- **Cultural Inclusivity:** Reflect the diversity of the global Francophonie, avoiding stereotypes and Eurocentric biases.
- **Data-Driven Learning:** Utilize corpus linguistics and frequency lists to inform vocabulary instruction and grammar explanations.
- **Constructive Feedback:** Provide clear, actionable feedback that addresses the root cause of learner errors rather than just correcting the surface mistake.

## Key References

- `references/complete-reference.md`: The definitive guide containing all grammar rules, vocabulary lists, conversation templates, linguistic deep dives, and CLI/NLP tool documentation.
- `references/reading-list.md`: A curated list of recent books and articles on French linguistics, pedagogy, and educational technology.

---

## Adversarial Verification Panel

For each significant language assessment finding (grammar errors, pronunciation issues, vocabulary gaps, CEFR level evaluations) produced by the parallel sub-agents:

1. Spawn **3 independent Refuter Agents** per finding, each with:
   - The finding in full
   - Instruction: *"Assume this finding is wrong. Find the strongest argument against it."*
   - Default stance: `refuted=true` if evidence is insufficient or ambiguous
2. A finding is **confirmed** only if ≥2 refuters fail to refute it
3. A finding is **discarded** if ≥2 refuters succeed
4. When a confirmed finding had 1 successful refuter, include the dissenting argument in the output with a `CONTESTED` label

> This prevents plausible-but-wrong language assessment findings from reaching the final output. The 3-vote panel eliminates single-point hallucination without requiring unanimity.

## Cross-System Consistency Validator

After all parallel agents (Text Analyzer, Exercise Generator, Automated Grader, Pronunciation Scorer) complete, but **before** synthesis:

Run one **Consistency Validator Agent** with all parallel outputs that:
- Flags any pair of recommendations that logically contradict each other
  *(example: the Text Analyzer rates a learner's text as B2 level while the Automated Grader assigns exercises targeting A2 grammar — the diagnosed level and the remediation difficulty are misaligned)*
- Notes where one agent's output is a prerequisite for another agent's recommendation
- Passes contradictions to the Synthesis Agent as `MUST_RESOLVE` items
- Passes missing prerequisites as `SEQUENCING_REQUIRED` items

## Synthesis Agent (Upgraded)

The synthesis step actively resolves rather than aggregates:

1. **`MUST_RESOLVE` contradictions**: Pick the better recommendation, annotate the reasoning, preserve the dissenting view as a footnote
2. **`SEQUENCING_REQUIRED` items**: Re-order the unified learning report so prerequisites appear before the steps that depend on them
3. **Confidence calibration**: Label each finding `HIGH` / `MEDIUM` / `LOW` confidence based on refuter panel outcomes
4. **Gap analysis**: Note any analysis dimension not covered by any of the parallel agents — these are blind spots, not confirmed negatives
