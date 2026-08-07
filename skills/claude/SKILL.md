---
name: claude
description: Specialist skill for mastering Claude models (Fable 5, Mythos 5, Opus 5, Sonnet 5), including API integration, system prompts, tool use, vision capabilities, extended thinking, prompt caching, and Artifacts.
---

# Claude Specialist Skill

## Scope and Triggers

Use this skill when you need to interact with, configure, or optimize applications powered by Claude models (Fable 5, Mythos 5, Opus 5, Sonnet 5). This includes tasks such as:
- Integrating the Claude API into applications.
- Designing and refining system prompts for specific personas or constraints.
- Implementing tool use and external API integrations within Claude.
- Leveraging Claude's vision capabilities for multi-modal tasks.
- Managing extended context windows and complex reasoning chains.
- Optimizing performance and cost through prompt caching strategies.
- Utilizing Artifacts for collaborative workspaces.
- Troubleshooting and diagnosing issues with Claude deployments.
- Configuring Claude environments using the Claude CLI.

## Preconditions

- Detect the target environment, versions, permissions, inputs, constraints, and user intent before acting.
- Ensure the Claude CLI is installed and configured with the appropriate API keys and environment settings.
- Verify the specific Claude model required for the task (e.g., `claude-fable-5`, `claude-mythos-5`, `claude-opus-5`, `claude-sonnet-5`).

## Source Freshness

- Volatile facts such as model versions and API specifications must be verified against official Anthropic documentation.
- See `references/complete-reference.md` for verified API usage examples and specifications.

## Workflow

1. **Requirement Analysis:** Determine the specific Claude capabilities required for the task (e.g., text generation, vision, tool use, Artifacts) and select the appropriate model (Fable 5, Mythos 5, Opus 5, Sonnet 5).
2. **Environment Setup:** Ensure the Claude CLI is installed and configured with the appropriate API keys and environment settings.
3. **Prompt Engineering:** Design system prompts that clearly define the model's role, constraints, and output format, incorporating prompt caching if applicable.
4. **API Integration:** Construct API requests with the correct model names and parameters (`model`, `prompt`, `max_tokens_to_sample`, `temperature`, etc.).
5. **Tool Implementation:** If required, define tool schemas and implement middleware to handle tool invocations.
6. **Execution and Monitoring:** Execute the requests and monitor the responses, handling any errors or rate limits gracefully.
7. **Optimization:** Apply prompt caching and extended thinking techniques to improve performance and manage large contexts.
8. **Troubleshooting:** Use the Claude CLI and diagnostic guides to resolve any issues that arise during execution.
9. **Stop Condition:** Stop when the task is completed successfully or an unrecoverable error occurs.

## Safety

- Separate read-only discovery from mutations.
- Require confirmation for destructive, external, privileged, financial, legal, or production-impacting actions.
- Always adhere to constitutional AI principles and embed ethical guardrails in system prompts.
- Securely manage API keys and sensitive data, ensuring compliance with enterprise security standards.

## Validation

- Verify that all API examples use the correct model names.
- Ensure that prompt caching is implemented correctly in the examples.
- Check that vision and tool use examples match the latest API specifications.
- Define syntax checks, dry runs, tests, evidence capture, and postcondition verification.

## Failure Handling

- Explain how to diagnose errors, choose alternatives, roll back, and avoid repeating a failed action unchanged.
- Implement comprehensive error handling, retries, and fallback mechanisms for API integrations.

## Output Contract

- Specify the structure, evidence, severity/confidence, and actionable next steps expected in the result.
- The output must include a clear summary of the actions taken, any issues encountered, and the final state of the Claude integration.

## Resources

- [Complete Reference](./references/complete-reference.md): Comprehensive guide to Claude models, API usage, prompt caching, tool use, vision capabilities, and troubleshooting.

## Orchestration

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

### Adversarial Verification Panel

For each significant API integration issue, prompt engineering recommendation, and diagnostic finding produced by the parallel sub-agents:

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
2. **`SEQUENCING_REQUIRED` items**: Re-order the unified Claude deployment report so prerequisites appear before the steps that depend on them
3. **Confidence calibration**: Label each finding `HIGH` / `MEDIUM` / `LOW` confidence based on refuter panel outcomes
4. **Gap analysis**: Note any analysis dimension not covered by any of the parallel agents — these are blind spots, not confirmed negatives
