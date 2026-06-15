# OpenAI Models Prompt Engineering Mastery

This reference covers prompt engineering, context engineering, and reasoning configurations for OpenAI's model family, focusing on **GPT-4*** and **GPT-5*** models [1].

---

## 1. OpenAI Model Family Specifications

OpenAI models are divided into general-purpose multimodal models and specialized reasoning models [2].

| Model Series | Context Window | Max Output | Key Characteristics |
| :--- | :--- | :--- | :--- |
| **GPT-5** (`gpt-5`) | 400k tokens | 128k tokens | Frontier reasoning and agentic model. Configurable reasoning effort. Step-change in math, coding, and logical tasks [3] [4]. |
| **GPT-5 mini** | 272k tokens | 128k tokens | High-speed, cost-effective reasoning model for high-volume, low-latency workloads [5]. |
| **GPT-5 nano** | 400k tokens | 128k tokens | Ultra-lightweight, extremely cost-effective model for simple edge/agent operations [6]. |
| **GPT-4.1** (`gpt-4.1`) | 1M tokens | 32k tokens | Smartest non-reasoning model. Outstanding instruction following, structured output, and tool calling with zero reasoning latency [7]. |
| **GPT-4o** (`gpt-4o`) | 128k tokens | 4k tokens | Multimodal (text, vision, audio) real-time model with balanced speed and intelligence [8]. |

---

## 2. Core Prompting Principles for OpenAI

### A. Role Definition & System Message
OpenAI models rely heavily on the **System Message** (or Developer Message) to establish boundaries, personas, and behavioral constraints.
* Clearly define the role: "You are a senior systems engineer..."
* Place rules and constraints in the system message, and keep the user message focused on input data and direct execution commands [1].

### B. Delimiters and Structure
While OpenAI models do not strictly require XML tags like Anthropic models, they perform exceptionally well when structured using clear delimiters.
* Use triple quotes (`"""`), Markdown headers (`#`, `##`), or XML tags (`<context>`, `<rules>`) to separate instructions from data [1].
* Explicitly tell the model to pay attention to these sections (e.g., "Summarize the text delimited by triple backticks").

### C. Few-Shot Prompting & Canonical Examples
Provide clear, structured examples of inputs and desired outputs.
* Keep examples diverse and representative of edge cases.
* For structured output (JSON), provide a few-shot example that matches the target JSON schema [1].

---

## 3. Advanced Reasoning Configuration (GPT-5)

The GPT-5 series features native reasoning capabilities, allowing the model to think through complex problems before outputting a response. This behavior is controlled via the `reasoning_effort` API parameter [3].

### A. Reasoning Effort Levels
* **`high`:** Maximum reasoning depth. Ideal for complex mathematical proofs, deep code refactoring, and long-horizon planning [3].
* **`medium`:** Default setting. Balances reasoning quality with token latency [3].
* **`low` / `minimal`:** Reduces reasoning tokens, optimizing for speed and cost on straightforward tasks [3].

### B. Output Structure & Token Handling
When using GPT-5 models, the output contains both **reasoning tokens** and **visible output tokens** [3].
* **Do not assume output structure:** The output text may not always be at `output[0].content[0].text`. Always use official SDK helpers like `output_text` to aggregate text output [9].
* **Budgeting:** Ensure your `max_tokens` budget is large enough to accommodate both reasoning and final response tokens. GPT-5 supports up to 128k output tokens [3].

---

## 4. Context Reduction & Token Efficiency

To minimize bootstrap sizes and context loading overhead, apply the following optimization techniques:

### A. Leverage Prompt Caching
OpenAI automatically caches prompt prefixes that are identical across requests [10].
* **Structure for Caching:** Place static elements (system instructions, tool definitions, few-shot examples) at the **beginning** of the prompt. Place dynamic elements (user queries, current conversation turn) at the **end** [10].
* This maximizes prompt cache hits, reducing input costs by up to 50% and dramatically lowering latency [10].

### B. Strict JSON via Structured Outputs
Instead of writing verbose prompting instructions to force JSON formatting (which wastes tokens and is fragile), use the native `response_format` with JSON Schema [11].
* This guarantees 100% schema compliance without needing extensive prompt-based guardrails or few-shot examples, saving hundreds of context tokens [11].

---

## 5. References

* [1] [OpenAI Prompt Engineering Best Practices](https://developers.openai.com/api/docs/guides/prompt-engineering)
* [2] [OpenAI Models Overview](https://developers.openai.com/api/docs/models)
* [3] [OpenAI GPT-5 Model Specifications](https://developers.openai.com/api/docs/models/gpt-5)
* [4] [Introducing GPT-5](https://openai.com/index/introducing-gpt-5/)
* [5] [OpenAI GPT-5 mini Specifications](https://developers.openai.com/api/docs/models/gpt-5-mini)
* [6] [Introducing GPT-5 nano](https://openai.com/gpt-5/)
* [7] [OpenAI GPT-4.1 Specifications](https://developers.openai.com/api/docs/models/gpt-4.1)
* [8] [Announcing GPT-4o in the API](https://community.openai.com/t/announcing-gpt-4o-in-the-api/744700)
* [9] [OpenAI Responses API Guide](https://developers.openai.com/api/docs/guides/prompt-engineering)
* [10] [OpenAI Prompt Caching Developer Guide](https://developers.openai.com/api/docs/guides/prompt-engineering)
* [11] [OpenAI Structured Outputs Guide](https://developers.openai.com/api/docs/guides/prompt-engineering)
