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
