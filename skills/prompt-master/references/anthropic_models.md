# Anthropic Models Prompt Engineering Mastery

This reference covers prompt engineering, context engineering, and execution parameters for Anthropic's Claude models, including **Claude Opus 4.7**, **Claude Opus 4.6**, **Claude Sonnet 4.6**, and **Claude Haiku 4.5** [1].

---

## 1. Anthropic Model Family Specifications

Anthropic's models are optimized for distinct tiers of speed, cost, and intelligence. 

| Model Name | Claude API Alias | Context Window | Max Output | Key Strengths |
| :--- | :--- | :--- | :--- | :--- |
| **Claude Opus 4.7** | `claude-opus-4-7` | 1M tokens | 128k tokens | Long-horizon agentic workflows, deep knowledge work, advanced coding, complex vision, and high-fidelity memory tasks [1] [2]. |
| **Claude Sonnet 4.6** | `claude-sonnet-4-6` | 1M tokens | 64k tokens | Optimal balance of speed and intelligence. Excellent for general agentic tasks, coding, and tool-use pipelines [2]. |
| **Claude Haiku 4.5** | `claude-haiku-4-5` | 200k tokens | 64k tokens | High-speed, near-frontier intelligence. Perfect for short-horizon, latency-sensitive, and high-volume workloads [2]. |

---

## 2. Core Prompting Principles for Claude

### A. Use XML Tags for Structural Delineation
Claude is pre-trained to understand XML tags (e.g., `<instructions>`, `<example>`, `<context>`) as strong structural delimiters. Using XML tags prevents instruction-context confusion, especially in long prompts [3].
* **Hierarchy:** Nest XML tags logically to group related data.
* **Separation:** Wrap user inputs, reference documents, and system guidelines in separate, clearly named XML tags.
* **Referencing:** Refer to the tags in your instructions (e.g., "Analyze the text inside the `<document>` tag").

### B. Structural Order of Prompts
Claude is highly sensitive to the order of information. To minimize context rot and optimize recall, structure your prompt in the following sequence:
1. **System Prompt / High-Level Persona:** Establish the role and boundaries.
2. **Global Instructions / Rules:** Define what to do and what not to do.
3. **Reference Data / Documents:** Wrap in XML tags (e.g., `<documents>`).
4. **Few-Shot Examples:** Wrap in `<examples>` tags.
5. **Specific Task Instructions:** The final direct command to execute.
6. **Output Formatting / Guardrails:** Define constraints (JSON schema, XML tags, tone).

---

## 3. Model-Specific Tuning Guidelines

### Claude Opus 4.7 Mastery

Claude Opus 4.7 represents a major shift in agentic and long-horizon performance. It requires distinct prompt-tuning strategies [1].

#### A. Calibrating Effort and Thinking Depth
Opus 4.7 features a configurable `effort` parameter that controls the model's reasoning depth.
* **`max` / `xhigh`:** Best for complex coding and agentic work. Requires a larger output token budget (recommended: 64k+ tokens) [1].
* **`high`:** Balances token usage and intelligence. Standard for most intelligence-sensitive tasks [1].
* **`medium`:** Good for cost-sensitive tasks requiring moderate reasoning [1].
* **`low`:** Reserved for short, scoped tasks. The model scopes its work strictly to what was asked without generalizing or inferring [1].

> **Crucial Prompting Guideline for Low Effort:**
> Because Opus 4.7 is highly literal at `low` effort, you must explicitly state the scope of instructions:
> ```
> Apply this formatting rule to every section in the document, not just the first one.
> ```

#### B. Managing Response Length and Verbosity
Opus 4.7 calibrates response length to task complexity rather than defaulting to fixed verbosity.
* **To Decrease Verbosity:** Use positive examples showing concise communication instead of negative constraints.
* **Prompt Adjustment:**
  ```
  Provide concise, focused responses. Skip non-essential context, and keep examples minimal.
  ```

#### C. Steering Adaptive Thinking Latency
If the model is overthinking simple tasks due to complex system prompts, add steering instructions:
```
Thinking adds latency and should only be used when it will meaningfully improve answer quality—typically for problems that require multi-step reasoning. When in doubt, respond directly.
```

---

## 4. Context Engineering & Token Optimization

Context is a finite resource. As the context window grows, LLMs suffer from **context rot** (degraded recall and reasoning) [4].

```
[System Instructions] ──> [Minimal Tools] ──> [Canonical Examples] ──> [Dynamic JIT Context]
                                                                              │
                                                                       (Token Saving)
```

### A. Dynamic "Just-In-Time" (JIT) Context Loading
Instead of pre-loading massive files into the prompt, provide the agent with tools to fetch data dynamically [4].
* Keep the initial prompt lightweight by storing file paths, URLs, or query schemas.
* Empower the agent to use targeted search or viewing tools (e.g., `grep`, `head`, `tail`) to read only what is necessary [4].

### B. Extended Thinking and Tool Use Context Management
When combining **extended thinking** with **tool use**, follow these strict token management rules to prevent API errors and context bloat:
1. **Preserve Thinking Blocks:** When returning tool results to the API, you **must** include the unmodified `thinking` block (with its cryptographic signature) generated in the previous assistant turn [5].
2. **Strip Thinking on New Turns:** Once a tool use cycle is complete and a new user turn begins, the API automatically strips previous thinking blocks from the context window [5]. This prevents token waste and maintains a clean history.

---

## 5. References

* [1] [Anthropic Prompting Best Practices Guide](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices)
* [2] [Anthropic Models Overview](https://platform.claude.com/docs/en/about-claude/models/overview)
* [3] [Use XML Tags to Structure Prompts](https://community.openai.com/t/use-xml-tags-to-structure-my-prompts/1068871)
* [4] [Effective Context Engineering for AI Agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
* [5] [Anthropic Context Windows and Extended Thinking](https://platform.claude.com/docs/en/build-with-claude/context-windows)
