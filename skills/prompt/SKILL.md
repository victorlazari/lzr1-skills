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

## Preconditions

Before acting, verify:
- The target LLM model and its capabilities (e.g., context window size, supported features).
- The specific prompt engineering task (design, optimization, security, troubleshooting).
- Any constraints on latency, cost, or token usage.
- The availability of required tools or frameworks (e.g., DSPy, Braintrust).

## Source Freshness

Prompt engineering is a rapidly evolving field. Always verify the latest best practices and model capabilities against official documentation (e.g., OpenAI, Anthropic, Braintrust) before implementing complex architectures or security measures.

## Workflow

1. **Analyze the Request**: Determine the specific prompt engineering task (design, optimization, security, troubleshooting).
2. **Select the Architecture**: Choose the appropriate prompt pattern (e.g., zero-shot, few-shot, CoT, ToT, ReAct) based on the task complexity.
3. **Draft the Prompt**: Construct the prompt using clear system instructions, context injection, task definition, and output formatting.
4. **Optimize and Refine**: Apply token optimization, prompt caching strategies, and dynamic context management techniques.
5. **Secure the Prompt**: Implement defenses against prompt injection, ensure PII masking, and validate outputs.
6. **Test and Evaluate**: Use golden datasets, LLM-as-a-Judge, or A/B testing to measure prompt effectiveness.
7. **Deploy and Monitor**: Configure the prompt schema, set up health checks, and monitor for prompt drift or errors.

**Stop condition**: The prompt is successfully deployed and monitored without errors, and passes all automated evaluations.

## Safety

- **Read-only discovery**: Always analyze existing prompts and system configurations before making changes.
- **Mutation confirmation**: Require explicit confirmation before deploying new prompts to production or modifying critical system configurations.
- **Security**: Never embed sensitive information (PII, secrets) directly in prompts. Use dynamic injection and masking techniques.

## Validation

- **Syntax checks**: Ensure prompt templates are well-formed and valid according to the target schema (e.g., JSON, YAML).
- **Dry runs**: Test prompts in a staging environment or sandbox before deploying to production.
- **Automated evaluation**: Use LLM-as-a-judge or other automated metrics to evaluate prompt quality and consistency.

## Failure Handling

- **Diagnosis**: Analyze error logs, model outputs, and system metrics to identify the root cause of failures.
- **Alternatives**: If a specific prompt architecture fails, try alternative approaches (e.g., switching from zero-shot to few-shot, or using a different model).
- **Rollback**: Maintain version control for prompts and be prepared to roll back to a previous version if a new deployment causes issues.

## Output Contract

The final output must include:
- The complete, optimized prompt template.
- A summary of the chosen architecture and reasoning.
- Results of automated evaluations and security checks.
- Actionable recommendations for monitoring and future optimization.

## Resources

- [Complete Reference](./references/complete-reference.md): Comprehensive guide to advanced prompt engineering, CLI tools, configuration schemas, deep dives, and troubleshooting.
- [Reading List](./references/reading-list.md): Curated list of recent authoritative guides on prompt engineering and LLM architecture.
- [Modular Prompt Template](./templates/modular-prompt.yaml): A template demonstrating modular prompt architecture.
- [Evaluate Prompt Script](./scripts/evaluate-prompt.py): A script for automated prompt evaluation using LLM-as-a-judge.

## Orchestration

This skill supports spawning sub-agents for parallel execution when tasks can be decomposed:

| Trigger Condition | Sub-Agent Type | Purpose |
|---|---|---|
| Multiple prompts to optimize | Prompt Optimizer | Parallel optimization of different prompt templates |
| Multiple models to evaluate | Model Evaluator | Parallel evaluation of prompt performance across models |
| Multiple security vectors to test | Red Team Agent | Parallel adversarial testing and injection attempts |
| Bulk log analysis for troubleshooting | Diagnostics Agent | Parallel analysis of prompt system error logs |

### Spawning Rules
- Spawn when 3+ independent items need the same operation
- Each sub-agent receives: context, specific target, success criteria
- Results are aggregated and cross-referenced for conflicts
- Maximum concurrent sub-agents: 10

### Adversarial Verification Panel

For each significant prompt engineering recommendation produced by the parallel sub-agents:

1. Spawn **3 independent Refuter Agents** per finding, each with:
   - The finding in full
   - Instruction: *"Assume this finding is wrong. Find the strongest argument against it."*
   - Default stance: `refuted=true` if evidence is insufficient or ambiguous
2. A finding is **confirmed** only if ≥2 refuters fail to refute it
3. A finding is **discarded** if ≥2 refuters succeed
4. When a confirmed finding had 1 successful refuter, include the dissenting argument in the output with a `CONTESTED` label

### Cross-System Consistency Validator

After all parallel agents complete, but **before** synthesis:

Run one **Consistency Validator Agent** with all parallel outputs that:
- Flags any pair of recommendations that logically contradict each other
- Notes where one agent's output is a prerequisite for another agent's recommendation
- Passes contradictions to the Synthesis Agent as `MUST_RESOLVE` items
- Passes missing prerequisites as `SEQUENCING_REQUIRED` items

### Synthesis Agent (Upgraded)

The synthesis step actively resolves rather than aggregates:

1. **`MUST_RESOLVE` contradictions**: Pick the better recommendation, annotate the reasoning, preserve the dissenting view as a footnote
2. **`SEQUENCING_REQUIRED` items**: Re-order the unified prompt engineering output so prerequisites appear before the steps that depend on them
3. **Confidence calibration**: Label each finding `HIGH` / `MEDIUM` / `LOW` confidence based on refuter panel outcomes
4. **Gap analysis**: Note any analysis dimension not covered by any of the parallel agents — these are blind spots, not confirmed negatives
