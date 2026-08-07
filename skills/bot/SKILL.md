---
name: bot
description: Advanced Bot Engineering with OpenClaw, NemoClaw, and OpenShell
---

# Bot Specialist Skill

## Scope and Triggers

Use this skill when tasked with designing, developing, deploying, or auditing advanced autonomous AI agents and bots using the OpenClaw, NemoClaw, and OpenShell ecosystems. This includes:
- Building and managing native or bundle plugins for OpenClaw.
- Configuring advanced memory systems (QMD, Honcho, LanceDB) and dreaming processes.
- Setting up secure sandboxes with OpenShell, including network policies, credential injection, and L7 proxying.
- Designing multi-agent routing architectures and complexity-based model routing.
- Conducting comprehensive security audits for bot deployments.
- Troubleshooting bot lifecycles, session locking, and plugin hooks.

**Escalation Boundaries:**
- For comprehensive code or application security audits beyond bot configuration, route to `security-review`.
- For setting up general automated workflows not specific to OpenClaw/NemoClaw bots, route to `automation-and-scheduling`.

## Preconditions

Before acting, verify:
- Target environment and bot configuration requirements.
- Permissions to modify network policies or deploy bots.
- User intent for destructive or production-impacting actions.

## Source Freshness

Bot ecosystems evolve rapidly. Always verify current capabilities and supported flags before executing commands:
- Run runtime checks (e.g., `bot --version`).
- Consult official upstream documentation for OpenClaw, NemoClaw, and OpenShell.
- Refer to `references/complete-reference.md` for verified facts.

## Workflow

1. **Discover**: Identify target environment and bot configuration requirements.
2. **Validate**: Use `scripts/validate-bot-config.sh` to dry-run and validate configurations before application.
3. **Confirm**: If deploying or modifying network policies, request explicit user confirmation.
4. **Execute**: Apply deployment or configuration changes using the `bot` CLI or OpenShell.
5. **Verify**: Confirm successful deployment via `bot status` and `bot logs`.
6. **Finalize**: Stop and report success, or rollback and report failure if verification fails.

## Safety

- **Read-only Discovery**: Always separate read-only discovery from mutations.
- **Confirmation Required**: Require explicit user confirmation before deploying bots, modifying network policies, or performing any destructive/external/privileged actions.
- **Credential Handling**: Ensure all credentials are injected via L7 proxy and never stored in the sandbox filesystem.

## Validation

- Use `scripts/validate-bot-config.sh` to validate bot configuration files (e.g., openclaw.json, bot-config.yml).
- Run safe local syntax checks on files created (`bash -n`, Python compilation, JSON/YAML parsing).

## Failure Handling

- If deployment fails, use `bot logs` and OpenShell diagnostics to identify the issue.
- Provide rollback instructions for failed deployments.
- Do not repeat a failed action unchanged.

## Output Contract

The final output must include:
- A summary of actions taken.
- Evidence of successful validation and deployment.
- Any known limits or unresolved uncertainties.
- Actionable next steps for the user.

## Resources

- [Complete Reference Guide](references/complete-reference.md): Technical knowledge for advanced bot engineering.
- [Validate Bot Config Script](scripts/validate-bot-config.sh): Deterministic validation of bot configuration files.
- [Network Policy Template](templates/network-policy.yaml): Reusable template for OpenShell network policies with safe defaults.

## Orchestration

This skill supports spawning sub-agents for parallel execution when tasks can be decomposed:

| Trigger Condition | Sub-Agent Type | Purpose |
|---|---|---|
| Multiple plugins to develop/audit | Plugin Engineer | Parallel development or review of native/bundle plugins |
| Multiple network policies to validate | Policy Validator | Parallel validation of OpenShell network policies |
| Multiple environments to deploy | Deployment Specialist | Parallel sandbox creation and configuration |
| Bulk security auditing | Security Auditor | Parallel security review of bot components (auth, data, network) |

### Spawning Rules
- Spawn when 3+ independent items need the same operation.
- Each sub-agent receives: context, specific target, success criteria.
- Results are aggregated and cross-referenced for conflicts.
- Maximum concurrent sub-agents: 10.

### Adversarial Verification Panel
For each significant security vulnerability produced by parallel sub-agents:
1. Spawn 3 independent Refuter Agents per finding.
2. A finding is confirmed only if ≥2 refuters fail to refute it.
3. A finding is discarded if ≥2 refuters succeed.
4. Include dissenting arguments for confirmed findings with 1 successful refuter (labeled `CONTESTED`).

### Cross-System Consistency Validator
Run one Consistency Validator Agent with all parallel outputs before synthesis to flag contradictions (`MUST_RESOLVE`) and missing prerequisites (`SEQUENCING_REQUIRED`).

### Synthesis Agent
1. Resolve `MUST_RESOLVE` contradictions.
2. Re-order `SEQUENCING_REQUIRED` items.
3. Label confidence (`HIGH` / `MEDIUM` / `LOW`).
4. Note gap analysis (blind spots).
