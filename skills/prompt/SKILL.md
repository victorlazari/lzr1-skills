---
name: prompt
description: Advanced prompt engineering, prompt architecture, and prompt system troubleshooting. Use when designing, optimizing, securing, or troubleshooting LLM prompts and prompt-based systems.
---

# Prompt Engineering Specialist

## When to Use

Use this skill when you need to:
- Design advanced prompt architectures (Chain-of-Thought, Tree-of-Thought, ReAct, etc.).
- Optimize prompts for performance, latency, and cost (token optimization, prompt caching).
- Implement dynamic context management and Retrieval-Augmented Generation (RAG) pipelines.
- Secure prompt systems against injection attacks, jailbreaks, and data leaks.
- Troubleshoot and diagnose issues in prompt-based systems (delayed responses, incorrect outputs, high error rates).
- Configure prompt schemas, templates, and variable substitutions.

## Sub-Agent Spawning

This skill supports spawning sub-agents for parallel execution when tasks can be decomposed:

| Trigger Condition | Sub-Agent Type | Purpose |
|---|---|---|
| Multiple prompts to optimize | Prompt Optimizer | Parallel optimization of different prompt templates |
| Multiple models to evaluate | Model Evaluator | Parallel A/B testing of prompts across different LLMs |
| Multiple security vectors to test | Red Team Agent | Parallel adversarial testing and injection attempts |
| Bulk log analysis for troubleshooting | Diagnostics Agent | Parallel analysis of prompt system error logs |

### Spawning Rules
- Spawn when 3+ independent items need the same operation
- Each sub-agent receives: context, specific target, success criteria
- Results are aggregated and cross-referenced for conflicts
- Maximum concurrent sub-agents: 10

## Workflow

1. **Analyze the Request**: Determine the specific prompt engineering task (design, optimization, security, troubleshooting).
2. **Select the Architecture**: Choose the appropriate prompt pattern (e.g., zero-shot, few-shot, CoT, ToT, ReAct) based on the task complexity.
3. **Draft the Prompt**: Construct the prompt using clear system instructions, context injection, task definition, and output formatting.
4. **Optimize and Refine**: Apply token optimization, prompt caching strategies, and dynamic context management techniques.
5. **Secure the Prompt**: Implement defenses against prompt injection, ensure PII masking, and validate outputs.
6. **Test and Evaluate**: Use golden datasets, LLM-as-a-Judge, or A/B testing to measure prompt effectiveness.
7. **Deploy and Monitor**: Configure the prompt schema, set up health checks, and monitor for prompt drift or errors.

## Core Principles

- **Clarity and Precision**: Instructions must be unambiguous and clearly separated from data/context.
- **Context Management**: Efficiently manage the context window using semantic chunking, dynamic assembly, and token budgeting.
- **Security First**: Always assume user input is potentially malicious; implement robust sanitization and output validation.
- **Iterative Optimization**: Prompt engineering is an iterative process requiring continuous testing, evaluation, and refinement.
- **Cost Awareness**: Balance accuracy with latency and cost by optimizing token usage and leveraging appropriate models.
- **Defensive Design**: Build systems that handle non-determinism gracefully through schema enforcement and retry logic with jitter.

## Key References

- [Complete Reference](./references/complete-reference.md): Comprehensive guide to advanced prompt engineering, CLI tools, configuration schemas, deep dives, and troubleshooting.
- [Reading List](./references/reading-list.md): Curated list of recent books and articles on prompt engineering and LLM architecture.
