---
name: prompt-master
description: "Prompt engineering, RAG, context optimization, and model-specific tuning mastery. Use for: organizing prompts and md files, designing prompting techniques (CoT, ToT, ReAct, self-consistency), building RAG/GraphRAG/Agentic-RAG pipelines, tuning Claude (Opus 4.7, Sonnet 4.6, Haiku 4.5) and OpenAI (GPT-4*, GPT-5*), reducing context/bootstrap size, and consulting the 2025-2026 research and book knowledge base."
---

# Prompt Master

This skill is the master knowledge base for prompt engineering, context engineering, Retrieval-Augmented Generation (RAG), and model-specific tuning. It distills guidance from official model documentation, 50 leading research papers, and 20 authoritative books (2025–2026) into targeted reference files. The main file stays lightweight; load reference files only when the task requires them, to minimize bootstrap size and context loading.

## How to Use This Skill

1. Identify the task type below.
2. Read **only** the reference file(s) relevant to that task.
3. Apply the patterns and cite the underlying research when designing prompts or pipelines.

## Reference Map

| If the task involves... | Read this reference |
| :--- | :--- |
| Tuning **Claude** models (Opus 4.7, Sonnet 4.6, Haiku 4.5): XML structure, effort calibration, thinking blocks | [references/anthropic_models.md](references/anthropic_models.md) |
| Tuning **OpenAI** models (GPT-4.1, GPT-4o, GPT-5 series): system messages, reasoning effort, structured outputs | [references/openai_models.md](references/openai_models.md) |
| Choosing or designing a **prompting technique** (zero/few-shot, CoT, ToT, GoT, ReAct, self-consistency, auto-optimization) | [references/prompting_techniques.md](references/prompting_techniques.md) |
| Building or improving a **RAG / GraphRAG / Agentic RAG** pipeline, chunking, retrieval, or evaluation | [references/rag_engineering.md](references/rag_engineering.md) |
| **Reducing context/bootstrap size**, prompt compression, context rot, or prompt caching | [references/context_reduction.md](references/context_reduction.md) |
| Looking up **empirical findings or papers** (2024–2026) on RAG, prompting, or LLM architectures | [references/research_index.md](references/research_index.md) |
| Recommending **books** or structured learning paths on AI engineering, prompting, or RAG | [references/reference_library.md](references/reference_library.md) |

## Core Operating Principles

1. **Match the model to the task.** Use the model references to select the right tier (speed vs. intelligence) and configure effort/reasoning parameters before writing the prompt.
2. **Structure before content.** Place static elements (system instructions, tools, canonical examples) first to maximize prompt caching; place dynamic data (query, history) last. See [references/context_reduction.md](references/context_reduction.md).
3. **Engineer context, not just prompts.** Counter context rot with progressive disclosure and Just-In-Time loading rather than pre-loading large files.
4. **Compress relentlessly.** Replace verbose instructions with dense heuristics; frontier models generalize well from them. State each rule exactly once.
5. **Ground and verify.** For knowledge tasks, prefer RAG patterns from [references/rag_engineering.md](references/rag_engineering.md) and apply self-verification to reduce hallucination.

## Reducing the Size of This Skill (Self-Application)

When asked to shrink this or any prompt/skill while preserving capability, apply the same rules it teaches: keep the router (this file) minimal, move depth into reference files loaded on demand, deduplicate instructions, and convert prose into tables and heuristics. The full procedure is in [references/context_reduction.md](references/context_reduction.md).

---

## Adversarial Verification Panel

For each significant prompt quality assessment produced by the parallel sub-agents:

1. Spawn **3 independent Refuter Agents** per finding, each with:
   - The finding in full
   - Instruction: *"Assume this finding is wrong. Find the strongest argument against it."*
   - Default stance: `refuted=true` if evidence is insufficient or ambiguous
2. A finding is **confirmed** only if ≥2 refuters fail to refute it
3. A finding is **discarded** if ≥2 refuters succeed
4. When a confirmed finding had 1 successful refuter, include the dissenting argument in the output with a `CONTESTED` label

> This prevents plausible-but-wrong prompt quality assessments from reaching the final output. The 3-vote panel eliminates single-point hallucination without requiring unanimity.

## Cross-System Consistency Validator

After all parallel agents (anthropic_models, openai_models, prompting_techniques, rag_engineering, context_reduction) complete, but **before** synthesis:

Run one **Consistency Validator Agent** with all parallel outputs that:
- Flags any pair of recommendations that logically contradict each other
  *(example: the rag_engineering agent recommends loading full document chunks for completeness while the context_reduction agent recommends aggressive truncation of the same retrieval payload to prevent context rot)*
- Notes where one agent's output is a prerequisite for another agent's recommendation
- Passes contradictions to the Synthesis Agent as `MUST_RESOLVE` items
- Passes missing prerequisites as `SEQUENCING_REQUIRED` items

## Synthesis Agent (Upgraded)

The synthesis step actively resolves rather than aggregates:

1. **`MUST_RESOLVE` contradictions**: Pick the better recommendation, annotate the reasoning, preserve the dissenting view as a footnote
2. **`SEQUENCING_REQUIRED` items**: Re-order the unified prompt engineering action plan so prerequisites appear before the steps that depend on them
3. **Confidence calibration**: Label each finding `HIGH` / `MEDIUM` / `LOW` confidence based on refuter panel outcomes
4. **Gap analysis**: Note any analysis dimension not covered by any of the parallel agents — these are blind spots, not confirmed negatives
