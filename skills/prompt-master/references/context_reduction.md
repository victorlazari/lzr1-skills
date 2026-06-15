# Context Reduction & Bootstrap Optimization

This reference outlines advanced strategies for minimizing bootstrap sizes, reducing context loading latency, and managing the attention budget of large language models [1].

---

## 1. The Token Economy & Context Rot

Language models suffer from **context rot**: as the context window grows, recall accuracy and logical reasoning degrade [1] [2]. Every token in context has a marginal cost in latency, API billing, and cognitive attention [1]. Empirical studies show that massive context windows lead to "attention decay" and factual recall failure [2].

```
[Attention Focus]  100% | * * *
                        |       * *
                    50% |           * *
                        |               * * *
                     0% |_____________________ * *
                        0k    50k   100k  200k  1M
                             [Context Size (Tokens)]
```

### Key Metrics of Context Rot [2]:
* **Under 10k tokens:** Near-perfect recall and reasoning.
* **10k - 50k tokens:** Gentle degradation; requires clear structuring (XML tags, headers) [3].
* **50k - 200k tokens:** Moderate degradation; "lost in the middle" effects become prominent.
* **200k - 1M tokens:** High risk of context rot; requires aggressive context engineering and dynamic loading [1].

---

## 2. Prompt Compression & Token Pruning

Before sending a prompt, it should be compressed to its absolute minimal high-signal form [1].

### A. Semantic Pruning Techniques
1. **Remove Conversational Filler:** Eliminate polite phrases, introductory text, and transition sentences.
2. **De-duplicate Instructions:** Ensure each rule or constraint is stated exactly once. Duplicate instructions do not increase adherence and waste attention budget.
3. **Use Dense Heuristics:** Replace verbose step-by-step rules with high-level heuristics or mental models. Smarter models (Claude Opus 4.7, GPT-5) generalize beautifully from heuristics [1].

| Verbose Instruction (35 tokens) | Compressed Heuristic (11 tokens) |
| :--- | :--- |
| "When you write the code, please make sure you write comprehensive unit tests for every function you create to ensure there are no bugs in the implementation." | "Write unit tests for all implemented functions to ensure coverage." |

### B. Structural Compression
* **XML Tag Minimization:** Use short, descriptive XML tags (e.g., `<doc>` instead of `<reference_document_from_database>`).
* **Few-Shot Selection:** Never include more than 2-3 canonical few-shot examples. Ensure examples are diverse and illustrate complex edge cases, not simple happy paths [1].

---

## 3. Optimizing Bootstrap Size for Agentic Loops

When an agent runs in a loop, the system prompt and tool definitions are loaded on **every single turn** [1]. This is the **bootstrap context**.

```
Turn 1: [Bootstrap (5k)] + [User Query (1k)] = 6k tokens
Turn 2: [Bootstrap (5k)] + [User Query (1k)] + [Turn 1 History (2k)] = 8k tokens
Turn 3: [Bootstrap (5k)] + [User Query (1k)] + [History (4k)] = 10k tokens
```

If the bootstrap size is too large, it rapidly inflates API costs and latency [1].

### Strategies to Reduce Bootstrap Size:
1. **Tool Definition Pruning:** Only expose tools that are strictly relevant to the current phase of the task. Do not load a "database write" tool during a "read-only research" phase [1].
2. **Dynamic System Prompts:** Update the system prompt dynamically as the agent progresses through different phases of a task. Keep instructions focused only on the current phase.
3. **Reference Offloading:** Move static documentation, API schemas, and reference material out of the system prompt. Provide the agent with a `view_reference` tool to fetch this data only when needed [1].
4. **Context Reuse (RAGBoost):** In multi-turn sessions, implement caching mechanisms that detect and reuse overlapping retrieved context items across concurrent turns to preserve prefill speed [4].

---

## 4. Prompt Caching Architecture

Both Anthropic and OpenAI support prompt caching, which dramatically reduces costs and latency for static context prefixes [5] [6].

```
[Static Prefix - CACHED]
├── System Instructions
├── Tool Definitions
└── Few-Shot Examples
──────────────────────── <--- Cache Boundary (Must be >1024 tokens)
[Dynamic Suffix - UNCACHED]
├── Message History
└── Current User Query
```

### Rules for Cache Optimization:
* **Keep the Prefix Static:** Any change to the cached prefix invalidates the entire cache. Ensure all dynamic data (dates, user IDs, current query) is placed at the very end of the prompt [6].
* **Minimum Token Thresholds:** 
  * **Anthropic:** Cache triggers at 1024 tokens (Sonnet/Opus) [5].
  * **OpenAI:** Cache triggers automatically in 1024-token blocks [6].
* **Structure:** Always structure prompts as: `[System Instructions] -> [Tools] -> [Examples] -> [Cache Boundary] -> [Dynamic Context/History]`.

---

## 5. References

* [1] Anthropic. (2025). Effective Context Engineering for AI Agents. *Anthropic Engineering Blog*.
* [2] Chroma Research. (2025). Context Rot: How Increasing Input Tokens Impacts LLM Performance. *Chroma Research Report*.
* [3] Anthropic. (2025). Anthropic Prompting Best Practices. *Anthropic Developer Documentation*.
* [4] UCSD Systems Lab. (2025). RAGBoost: Efficient RAG with Accuracy-Preserving Context Reuse. *arXiv preprint arXiv:2511.03475*.
* [5] Anthropic. (2025). Anthropic Prompt Caching Guide. *Anthropic Developer Documentation*.
* [6] OpenAI. (2025). OpenAI Prompt Caching Developer Guide. *OpenAI Developer Documentation*.
