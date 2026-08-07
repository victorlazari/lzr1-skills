# Prompt Engineering Reading List (2025-2026)

This reading list serves as a source map for the prompt engineering skill. It identifies authoritative sources and explains what each source governs and when to consult it.

## Authoritative Guides and Frameworks

1. **[Prompt Engineering Guide by DAIR.AI](https://www.promptingguide.ai/)**
   - **Governs**: Core prompt engineering techniques, reasoning frameworks (CoT, ToT, ReAct), and model-specific prompting strategies.
   - **When to consult**: When designing new prompt architectures or seeking to understand the fundamental mechanics of different prompting techniques.
   - **Verified against upstream**: 2026-08-07

2. **[OpenAI Prompt Engineering Guide](https://platform.openai.com/docs/guides/prompt-engineering)**
   - **Governs**: Best practices for OpenAI models, including clear instructions, providing reference text, splitting complex tasks, and using external tools.
   - **When to consult**: When optimizing prompts specifically for GPT-4 or other OpenAI models, or when implementing tool use (function calling).
   - **Verified against upstream**: 2026-08-07

3. **[Anthropic Prompt Engineering Interactive Tutorial](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview)**
   - **Governs**: Best practices for Claude models, including XML tag usage, long context window management, and system prompt design.
   - **When to consult**: When optimizing prompts for Claude models, especially for tasks involving large documents or complex formatting requirements.
   - **Verified against upstream**: 2026-08-07

4. **[Braintrust: The Data-Driven Prompt Engineering Guide](https://www.braintrust.dev/docs/guides/prompt-engineering)**
   - **Governs**: Automated evaluation, LLM-as-a-judge methodologies, dataset management, and iterative prompt optimization.
   - **When to consult**: When setting up evaluation pipelines, defining scoring metrics, or transitioning from manual testing to automated, data-driven prompt optimization.
   - **Verified against upstream**: 2026-08-07

5. **[IBM: What is Prompt Engineering?](https://www.ibm.com/topics/prompt-engineering)**
   - **Governs**: Enterprise applications of prompt engineering, security considerations, and integration with broader AI strategies.
   - **When to consult**: When designing prompt systems for enterprise environments, focusing on security, compliance, and scalability.
   - **Verified against upstream**: 2026-08-07

## Key Papers and Research

1. **"Large Language Models are Zero-Shot Reasoners"** by Kojima et al. (2022)
   - **Governs**: The foundational concept of zero-shot Chain-of-Thought prompting ("Let's think step by step").

2. **"Chain-of-Thought Prompting Elicits Reasoning in Large Language Models"** by Wei et al. (2022)
   - **Governs**: The mechanics and benefits of few-shot Chain-of-Thought prompting for complex reasoning tasks.

3. **"Tree of Thoughts: Deliberate Problem Solving with Large Language Models"** by Yao et al. (2023)
   - **Governs**: Advanced reasoning architectures that explore multiple paths and evaluate intermediate steps.

4. **"ReAct: Synergizing Reasoning and Acting in Language Models"** by Yao et al. (2023)
   - **Governs**: The integration of reasoning traces with external tool use and action execution.
