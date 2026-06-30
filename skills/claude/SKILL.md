---
name: claude
description: Specialist skill for mastering Claude 3.5 and beyond, including API integration, system prompts, tool use, vision capabilities, extended thinking, and prompt caching.
---

# Claude Specialist Skill

## When to Use

Use this skill when you need to interact with, configure, or optimize applications powered by Claude 3.5. This includes tasks such as:
- Integrating the Claude 3.5 API into applications.
- Designing and refining system prompts for specific personas or constraints.
- Implementing tool use and external API integrations within Claude.
- Leveraging Claude's vision capabilities for multi-modal tasks.
- Managing extended context windows and complex reasoning chains.
- Optimizing performance and cost through prompt caching strategies.
- Troubleshooting and diagnosing issues with Claude deployments.
- Configuring Claude environments using the Claude CLI.

## Sub-Agent Spawning

This skill supports spawning sub-agents for parallel execution when tasks can be decomposed:

| Trigger Condition | Sub-Agent Type | Purpose |
|---|---|---|
| Multiple prompts to optimize | Prompt Engineer | Parallel refinement of system and user prompts |
| Multiple tools to integrate | Integration Specialist | Parallel development of custom tool middleware |
| Multiple images to analyze | Vision Analyst | Parallel processing of visual inputs |
| Bulk log analysis | Diagnostics Agent | Parallel investigation of error logs and performance metrics |

### Spawning Rules
- Spawn when 3+ independent items need the same operation
- Each sub-agent receives: context, specific target, success criteria
- Results are aggregated and cross-referenced for conflicts
- Maximum concurrent sub-agents: 10

## Workflow

1. **Requirement Analysis:** Determine the specific Claude capabilities required for the task (e.g., text generation, vision, tool use).
2. **Environment Setup:** Ensure the Claude CLI is installed and configured with the appropriate API keys and environment settings.
3. **Prompt Engineering:** Design system prompts that clearly define the model's role, constraints, and output format.
4. **API Integration:** Construct API requests with the necessary parameters (`model`, `prompt`, `max_tokens_to_sample`, `temperature`, etc.).
5. **Tool Implementation:** If required, define tool schemas and implement middleware to handle tool invocations.
6. **Execution and Monitoring:** Execute the requests and monitor the responses, handling any errors or rate limits gracefully.
7. **Optimization:** Apply prompt caching and extended thinking techniques to improve performance and manage large contexts.
8. **Troubleshooting:** Use the Claude CLI and diagnostic guides to resolve any issues that arise during execution.

## Core Principles

- **Safety and Alignment:** Always adhere to constitutional AI principles and embed ethical guardrails in system prompts.
- **Efficiency:** Utilize prompt caching and batch requests to minimize latency and API costs.
- **Clarity:** Be explicit and specific in prompt design to reduce ambiguity and hallucinations.
- **Robustness:** Implement comprehensive error handling, retries, and fallback mechanisms for API integrations.
- **Security:** Securely manage API keys and sensitive data, ensuring compliance with enterprise security standards.

## Key References

- [Claude 3.5 Technical Overview and API Documentation](https://docs.anthropic.com/claude-3-5)
- [Constitutional AI: Principles for Safe AI Systems](https://www.anthropic.com/research)
- [Prompt Engineering: Patterns and Best Practices](https://docs.anthropic.com/claude/docs/prompt-engineering)
- [Claude CLI Command Reference](./references/complete-reference.md#claude-cli-command-reference)
- [Claude Configuration Schemas Guide](./references/complete-reference.md#claude-configuration-schemas-guide)
- [Claude Troubleshooting & Diagnostics Guide](./references/complete-reference.md#claude-troubleshooting--diagnostics-guide)

---

## Adversarial Verification Panel

For each significant API integration issue, prompt engineering recommendation, and diagnostic finding produced by the parallel sub-agents:

1. Spawn **3 independent Refuter Agents** per finding, each with:
   - The finding in full
   - Instruction: *"Assume this finding is wrong. Find the strongest argument against it."*
   - Default stance: `refuted=true` if evidence is insufficient or ambiguous
2. A finding is **confirmed** only if ≥2 refuters fail to refute it
3. A finding is **discarded** if ≥2 refuters succeed
4. When a confirmed finding had 1 successful refuter, include the dissenting argument in the output with a `CONTESTED` label

> This prevents plausible-but-wrong API integration issues, prompt engineering recommendations, and diagnostic findings from reaching the final output. The 3-vote panel eliminates single-point hallucination without requiring unanimity.

## Cross-System Consistency Validator

After all parallel agents (Prompt Engineer, Integration Specialist, Vision Analyst, Diagnostics Agent) complete, but **before** synthesis:

Run one **Consistency Validator Agent** with all parallel outputs that:
- Flags any pair of recommendations that logically contradict each other
  *(example: Prompt Engineer recommends increasing temperature for creativity while Diagnostics Agent flags high temperature as a source of hallucinations in production logs)*
- Notes where one agent's output is a prerequisite for another agent's recommendation
- Passes contradictions to the Synthesis Agent as `MUST_RESOLVE` items
- Passes missing prerequisites as `SEQUENCING_REQUIRED` items

## Synthesis Agent (Upgraded)

The synthesis step actively resolves rather than aggregates:

1. **`MUST_RESOLVE` contradictions**: Pick the better recommendation, annotate the reasoning, preserve the dissenting view as a footnote
2. **`SEQUENCING_REQUIRED` items**: Re-order the unified Claude deployment report so prerequisites appear before the steps that depend on them
3. **Confidence calibration**: Label each finding `HIGH` / `MEDIUM` / `LOW` confidence based on refuter panel outcomes
4. **Gap analysis**: Note any analysis dimension not covered by any of the parallel agents — these are blind spots, not confirmed negatives
