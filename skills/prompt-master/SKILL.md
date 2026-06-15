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
