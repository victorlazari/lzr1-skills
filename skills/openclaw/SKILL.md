---
name: openclaw
description: Advanced OpenClaw (ZeroClaw) operations, architecture, and troubleshooting specialist.
---

# OpenClaw (ZeroClaw) Operations & Architecture Specialist

## When to Use

Use this skill when:
- Deploying, configuring, or troubleshooting OpenClaw (ZeroClaw) AI agent runtimes in production environments.
- Managing the `openclaw.json` configuration file, including LLM routing, channel credentials, and memory retention policies.
- Interacting with or modifying OpenClaw Workspace Files (`SOUL.md`, `IDENTITY.md`, `USER.md`, `AGENTS.md`, `BOOT.md`, `HEARTBEAT.md`, `MEMORY.md`, `TOOLS.md`).
- Diagnosing and resolving channel integration issues (e.g., WhatsApp 408 Timeouts, Signal RPC Failures, Telegram getUpdates Timeouts).
- Managing the 3-Layer Memory System (Context Window, Workspace Files, Vector DB with SQLite and Gemini embeddings).
- Orchestrating multi-agent background workers (Codex, Claude Code, Pi) and resolving "Cross-Context Messaging Denied" errors.
- Developing, auditing, or troubleshooting custom TypeScript extensions and ClawdHub marketplace skills.
- Performing security audits on OpenClaw deployments, including credential directory protection and cross-context messaging controls.

## Sub-Agent Spawning

This skill supports spawning sub-agents for parallel execution when tasks can be decomposed:

| Trigger Condition | Sub-Agent Type | Purpose |
|---|---|---|
| Multiple channel integrations to debug | Channel Specialist | Parallel troubleshooting of WhatsApp, Signal, and Telegram issues |
| Multiple extensions/skills to audit | Extension Auditor | Parallel security and performance review of custom TypeScript plugins and ClawdHub skills |
| Large JSONL session logs to analyze | Log Analyzer | Parallel parsing and extraction of insights from multiple session files |
| Multi-agent topology validation | Orchestration Checker | Parallel validation of routing rules and cross-context messaging permissions |

### Spawning Rules
- Spawn when 3+ independent items (channels, extensions, logs, agents) need the same operation.
- Each sub-agent receives: context (e.g., `openclaw.json` snippet), specific target (e.g., `whatsapp` channel config), success criteria.
- Results are aggregated and cross-referenced for conflicts (e.g., ensuring consistent timeout settings across channels).
- Maximum concurrent sub-agents: 10.

## Workflow

1.  **Configuration Assessment:** Always begin by validating the `openclaw.json` file against the official schema. This is the central nervous system of the runtime.
2.  **Workspace Inspection:** Review the core Workspace Files (`SOUL.md`, `IDENTITY.md`, `AGENTS.md`, `TOOLS.md`) to understand the agent's persona, multi-agent topology, and available capabilities.
3.  **Memory & State Verification:** Check the integrity of the 3-Layer Memory System. Use `sqlite3` to query the vector database and `jq` to parse JSONL session logs for anomalies.
4.  **Channel Diagnostics:** If dealing with connectivity issues, isolate the specific channel (WhatsApp, Signal, Telegram) and review its specific error signatures (e.g., 408 Timeouts, RPC Failures).
5.  **Orchestration & Routing:** For multi-agent setups, verify the routing pipeline and ensure cross-context messaging policies are correctly configured to prevent unauthorized data leakage.
6.  **Security & Compliance:** Continuously audit filesystem permissions, credential encryption, and extension sandboxing to maintain a hardened environment.

## Core Principles

-   **Configuration as Code:** Treat `openclaw.json` and Workspace Files as code. Version control them and validate changes before deployment.
-   **Strict Context Isolation:** Never disable context isolation in production. Ensure explicit communication pathways are defined in `AGENTS.md`.
-   **Asynchronous Operations:** Offload heavy synchronous operations (e.g., vector embeddings, complex data processing) from the main event loop to prevent event loop starvation and channel disconnects.
-   **Robust Error Handling:** Implement aggressive reconnection logic with exponential backoff for channel integrations, and strict execution timeouts for extensions and background workers.
-   **Continuous Monitoring:** Utilize JSONL session logs and the `HEARTBEAT.md` file to proactively monitor agent health, lane congestion, and memory synchronization.

## Key References

-   `/home/ubuntu/specialist-skills/openclaw/references/complete-reference.md`: The definitive, consolidated guide to OpenClaw architecture, configuration, security, and troubleshooting.
-   `/home/ubuntu/specialist-skills/openclaw/references/reading-list.md`: A curated list of books and articles relevant to AI agent runtimes, multi-agent orchestration, and production operations.

---

## Adversarial Verification Panel

For each significant operational and security finding produced by the parallel sub-agents:

1. Spawn **3 independent Refuter Agents** per finding, each with:
   - The finding in full
   - Instruction: *"Assume this finding is wrong. Find the strongest argument against it."*
   - Default stance: `refuted=true` if evidence is insufficient or ambiguous
2. A finding is **confirmed** only if ≥2 refuters fail to refute it
3. A finding is **discarded** if ≥2 refuters succeed
4. When a confirmed finding had 1 successful refuter, include the dissenting argument in the output with a `CONTESTED` label

> This prevents plausible-but-wrong operational and security findings from reaching the final output. The 3-vote panel eliminates single-point hallucination without requiring unanimity.

## Cross-System Consistency Validator

After all parallel agents (Channel Specialist, Extension Auditor, Log Analyzer, Orchestration Checker) complete, but **before** synthesis:

Run one **Consistency Validator Agent** with all parallel outputs that:
- Flags any pair of recommendations that logically contradict each other
  *(example: Channel Specialist recommending aggressive reconnection timeouts while Orchestration Checker recommends conservative timeout thresholds to prevent cross-context message flooding)*
- Notes where one agent's output is a prerequisite for another agent's recommendation
- Passes contradictions to the Synthesis Agent as `MUST_RESOLVE` items
- Passes missing prerequisites as `SEQUENCING_REQUIRED` items

## Synthesis Agent (Upgraded)

The synthesis step actively resolves rather than aggregates:

1. **`MUST_RESOLVE` contradictions**: Pick the better recommendation, annotate the reasoning, preserve the dissenting view as a footnote
2. **`SEQUENCING_REQUIRED` items**: Re-order the unified remediation plan so prerequisites appear before the steps that depend on them
3. **Confidence calibration**: Label each finding `HIGH` / `MEDIUM` / `LOW` confidence based on refuter panel outcomes
4. **Gap analysis**: Note any analysis dimension not covered by any of the parallel agents — these are blind spots, not confirmed negatives
