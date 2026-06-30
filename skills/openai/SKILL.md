---
name: openai
description: Specialist in OpenAI API, GPT-4o, Assistants API, function calling, structured outputs, vision capabilities, and fine-tuning.
---

# OpenAI Specialist Skill

## When to Use

Use this skill when you need to:
- Interact with the OpenAI API for text generation, summarization, or chat completions.
- Leverage GPT-4o's multi-modal capabilities, including vision and extended context reasoning.
- Build intelligent conversational agents using the Assistants API with persistent state and custom personas.
- Implement function calling to allow language models to interact dynamically with external systems and APIs.
- Enforce structured outputs (e.g., JSON) for reliable and predictable model responses.
- Process and analyze images using vision capabilities (e.g., image captioning, VQA, OCR).
- Fine-tune OpenAI models for specific domains or specialized tasks.
- Use the OpenAI CLI for managing models, generating completions, or handling AI-powered tasks from the terminal.

## Sub-Agent Spawning

This skill supports spawning sub-agents for parallel execution when tasks can be decomposed:

| Trigger Condition | Sub-Agent Type | Purpose |
|---|---|---|
| Multiple prompts to optimize | Prompt Engineer | Parallel prompt design and testing |
| Multiple images to analyze | Vision Analyst | Parallel image processing and OCR |
| Multiple functions to define | Schema Architect | Parallel function schema creation |
| Bulk data extraction | Data Extractor | Parallel structured data extraction |
| Multiple fine-tuning datasets | Data Preparer | Parallel dataset formatting and validation |

### Spawning Rules
- Spawn when 3+ independent items need the same operation
- Each sub-agent receives: context, specific target, success criteria
- Results are aggregated and cross-referenced for conflicts
- Maximum concurrent sub-agents: 10

## Workflow

1. **Requirement Analysis**: Determine the specific OpenAI capability needed (e.g., basic completion, multi-modal analysis, conversational agent, structured data extraction).
2. **Model Selection**: Choose the appropriate model (e.g., `gpt-4o` for complex reasoning and vision, or specialized models for fine-tuning).
3. **Prompt Engineering**: Craft clear instructions, contextual backgrounds, and constraints. Use system messages to define personas.
4. **Implementation**:
   - For basic tasks: Use the standard Chat Completions API.
   - For complex agents: Configure the Assistants API with tools and knowledge bases.
   - For external integration: Define function schemas and handle `function_call` responses.
   - For structured data: Enforce JSON output via function calling or prompt instructions.
   - For vision: Encode images as base64 or provide URLs alongside text prompts.
5. **Token Management**: Monitor and optimize token usage by truncating history, summarizing context, and setting appropriate `max_tokens`.
6. **Testing and Refinement**: Evaluate responses, adjust temperature/prompts, and handle edge cases or errors.
7. **Deployment**: Integrate the solution into the target application or workflow, ensuring safety and compliance guardrails are in place.

## Core Principles

- **Clarity and Context**: Provide explicit instructions and sufficient context in prompts to guide the model effectively.
- **Reliability via Structure**: Use function calling to guarantee structured, machine-readable outputs instead of relying solely on prompt instructions.
- **Efficiency**: Manage tokens judiciously to balance cost and performance.
- **Multi-Modality**: Seamlessly combine text and vision inputs to solve complex, real-world problems.
- **State Management**: Leverage the Assistants API to handle conversation history automatically, reducing client-side complexity.
- **Continuous Improvement**: Use fine-tuning or RAG (Retrieval-Augmented Generation) to adapt models to niche domains when zero-shot performance is insufficient.

## Key References

- `references/reading-list.md`: Curated list of books and articles on OpenAI technologies and advanced AI concepts.
- `references/complete-reference.md`: Comprehensive guide covering API usage, GPT-4o, Assistants API, function calling, structured outputs, vision, fine-tuning, and CLI commands.

---

## Adversarial Verification Panel

For each significant API integration recommendation produced by the parallel sub-agents:

1. Spawn **3 independent Refuter Agents** per finding, each with:
   - The finding in full
   - Instruction: *"Assume this finding is wrong. Find the strongest argument against it."*
   - Default stance: `refuted=true` if evidence is insufficient or ambiguous
2. A finding is **confirmed** only if ≥2 refuters fail to refute it
3. A finding is **discarded** if ≥2 refuters succeed
4. When a confirmed finding had 1 successful refuter, include the dissenting argument in the output with a `CONTESTED` label

> This prevents plausible-but-wrong API integration recommendations from reaching the final output. The 3-vote panel eliminates single-point hallucination without requiring unanimity.

## Cross-System Consistency Validator

After all parallel agents (Prompt Engineer, Vision Analyst, Schema Architect, Data Extractor, Data Preparer) complete, but **before** synthesis:

Run one **Consistency Validator Agent** with all parallel outputs that:
- Flags any pair of recommendations that logically contradict each other
  *(example: Prompt Engineer recommending a high temperature value for creative flexibility while Schema Architect recommends a low temperature to ensure reliable structured JSON outputs)*
- Notes where one agent's output is a prerequisite for another agent's recommendation
- Passes contradictions to the Synthesis Agent as `MUST_RESOLVE` items
- Passes missing prerequisites as `SEQUENCING_REQUIRED` items

## Synthesis Agent (Upgraded)

The synthesis step actively resolves rather than aggregates:

1. **`MUST_RESOLVE` contradictions**: Pick the better recommendation, annotate the reasoning, preserve the dissenting view as a footnote
2. **`SEQUENCING_REQUIRED` items**: Re-order the unified integration plan so prerequisites appear before the steps that depend on them
3. **Confidence calibration**: Label each finding `HIGH` / `MEDIUM` / `LOW` confidence based on refuter panel outcomes
4. **Gap analysis**: Note any analysis dimension not covered by any of the parallel agents — these are blind spots, not confirmed negatives
