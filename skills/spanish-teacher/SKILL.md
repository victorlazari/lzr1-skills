---
name: spanish-teacher
description: A comprehensive Spanish language teaching and learning skill covering A1 to C2 levels, including grammar, vocabulary, cultural competence, and pedagogical strategies.
---

# Spanish Teacher Skill

## When to Use
Use this skill when you need to:
- Teach or learn Spanish from absolute beginner (A1) to mastery (C2) levels.
- Generate Spanish language exercises, quizzes, and conversation templates.
- Explain complex Spanish grammar concepts (e.g., Subjunctive, Ser vs. Estar, Por vs. Para).
- Understand regional variations (e.g., Voseo, Caribbean aspiration, Castilian distinction).
- Audit Spanish text for cultural sensitivity and appropriateness.
- Troubleshoot common learner errors and provide pedagogical fixes.

## Sub-Agent Spawning

This skill supports spawning sub-agents for parallel execution when tasks can be decomposed:

| Trigger Condition | Sub-Agent Type | Purpose |
|---|---|---|
| Multiple grammar topics to explain | Grammar Tutor | Parallel generation of explanations and exercises for different grammar nodes |
| Multiple regional dialects to analyze | Dialect Specialist | Parallel analysis of text for regional variations and slang |
| Bulk vocabulary list generation | Vocabulary Builder | Parallel creation of thematic vocabulary lists with Anki flashcard syntax |
| Multiple conversation scenarios | Scenario Generator | Parallel creation of role-play dialogues for different situations |
| Comprehensive curriculum design | Curriculum Planner | Parallel development of lesson plans for different CEFR levels |

### Spawning Rules
- Spawn when 3+ independent items need the same operation (e.g., 3 different grammar rules, 3 different regional dialects).
- Each sub-agent receives: context (learner's CEFR level), specific target (e.g., Subjunctive mood), success criteria (e.g., 5 exercises with answers).
- Results are aggregated and cross-referenced for conflicts (e.g., ensuring vocabulary matches the target CEFR level).
- Maximum concurrent sub-agents: 10

## Workflow
1. **Assess Learner Level:** Determine the target CEFR level (A1-C2) to tailor vocabulary and grammar complexity.
2. **Identify the Goal:** Is the goal conversation practice, grammar drilling, reading comprehension, or cultural understanding?
3. **Select Pedagogical Strategy:** Apply appropriate strategies like Comprehensible Input (i+1), Spaced Repetition Systems (SRS), or Shadowing.
4. **Generate Content:** Create explanations, examples, and exercises using the comprehensive reference guide.
5. **Review and Correct:** Analyze learner output, identify common errors (e.g., Ser vs. Estar confusion), and provide gentle, constructive feedback.
6. **Cultural Audit:** Ensure the content is culturally appropriate for the target region (e.g., avoiding "coger" in Latin America).

## Core Principles
- **Comprehensible Input:** Provide input slightly above the learner's current level (i+1).
- **Contextual Learning:** Teach vocabulary and grammar in context (full sentences) rather than in isolation.
- **The Subjunctive State of Mind:** Teach the subjunctive not just as conjugations, but as a psychological state representing emotions, doubts, and desires (WEIRDO framework).
- **Cultural Competence:** Language and culture are inseparable. Teach regional variations, formality rules (tú vs. usted), and cultural norms.
- **Constructive Troubleshooting:** Diagnose the root cause of learner errors (e.g., direct translation from English) and provide specific fixes.

## Key References
- **Complete Reference:** `references/complete-reference.md` (Contains the full A1-C2 curriculum, grammar rules, vocabulary, and conversation templates).
- **Reading List:** `references/reading-list.md` (Recommended books and articles for Spanish learners and teachers).
