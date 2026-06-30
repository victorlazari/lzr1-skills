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

---

## Adversarial Verification Panel

For each significant prompt engineering recommendation produced by the parallel sub-agents:

1. Spawn **3 independent Refuter Agents** per finding, each with:
   - The finding in full
   - Instruction: *"Assume this finding is wrong. Find the strongest argument against it."*
   - Default stance: `refuted=true` if evidence is insufficient or ambiguous
2. A finding is **confirmed** only if ≥2 refuters fail to refute it
3. A finding is **discarded** if ≥2 refuters succeed
4. When a confirmed finding had 1 successful refuter, include the dissenting argument in the output with a `CONTESTED` label

> This prevents plausible-but-wrong prompt engineering recommendations from reaching the final output. The 3-vote panel eliminates single-point hallucination without requiring unanimity.

## Cross-System Consistency Validator

After all parallel agents (Prompt Optimizer, Model Evaluator, Red Team Agent, Diagnostics Agent) complete, but **before** synthesis:

Run one **Consistency Validator Agent** with all parallel outputs that:
- Flags any pair of recommendations that logically contradict each other
  *(example: the Prompt Optimizer recommends aggressively compressing the system prompt to reduce token count while the Model Evaluator recommends expanding few-shot examples to improve accuracy on the same prompt)*
- Notes where one agent's output is a prerequisite for another agent's recommendation
- Passes contradictions to the Synthesis Agent as `MUST_RESOLVE` items
- Passes missing prerequisites as `SEQUENCING_REQUIRED` items

## Synthesis Agent (Upgraded)

The synthesis step actively resolves rather than aggregates:

1. **`MUST_RESOLVE` contradictions**: Pick the better recommendation, annotate the reasoning, preserve the dissenting view as a footnote
2. **`SEQUENCING_REQUIRED` items**: Re-order the unified prompt engineering output so prerequisites appear before the steps that depend on them
3. **Confidence calibration**: Label each finding `HIGH` / `MEDIUM` / `LOW` confidence based on refuter panel outcomes
4. **Gap analysis**: Note any analysis dimension not covered by any of the parallel agents — these are blind spots, not confirmed negatives
