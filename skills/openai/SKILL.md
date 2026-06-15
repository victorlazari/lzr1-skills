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
