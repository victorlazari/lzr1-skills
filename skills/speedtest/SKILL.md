---
name: speedtest
description: Execute Speedtest (Ookla) methodologies, architecture, CLI integration, and network performance diagnostics. Use when testing 5G/fiber connections, configuring custom OoklaServer instances, analyzing latency/jitter, or troubleshooting network throughput issues.
---

# Speedtest (Ookla) Specialist

## Scope and Triggers

Use this skill when you need to:
- Measure or analyze network performance, including bandwidth, latency (including UDP latency), and jitter.
- Troubleshoot slow speeds, inconsistency, or timeouts in network connections.
- Configure, automate, or integrate the Speedtest CLI into monitoring pipelines (e.g., Prometheus, Grafana).
- Understand or deploy custom OoklaServer instances for enterprise testing.
- Analyze 5G, fiber-optic, or super-fast connections (>10 Gbps) where traditional testing fails.
- Perform security audits or hardening of Speedtest infrastructure.

**Escalation Boundaries:**
- Do not perform destructive or configuration-changing actions (like modifying firewall rules or deploying OoklaServer) without explicit user confirmation.
- Do not execute untrusted downloaded artifacts.

## Preconditions

Before executing tests or deploying servers:
- Detect the target environment, OS, and network interfaces.
- Verify the installed Speedtest CLI version.
- Check firewall rules (ensure UDP 8080/5060 are open for UDP latency and server deployment).
- Ensure required permissions are available for network binding or server deployment.

## Source Freshness

Volatile facts such as OpenSSL versions (requires 3.5.5+) and required ports must be checked at runtime.
- Verify the current Speedtest CLI version and OoklaServer release notes before applying configurations.
- Consult official Ookla documentation for the latest requirements.
- Reference the bundled [Complete Reference](references/complete-reference.md) for architecture and commands.

## Workflow

1. **Analyze requirement**: Determine the goal (e.g., basic bandwidth test, automated monitoring, server deployment, security audit).
2. **Verify environment**: Check Speedtest CLI version, firewall rules for UDP 8080/5060, and OpenSSL version (3.5.5+ required).
3. **For server deployment**: Generate configuration using [templates/OoklaServer.properties](templates/OoklaServer.properties).
4. **Request user confirmation**: Explicitly ask the user before making firewall changes or deploying the server.
5. **Execute deployment or tests**: Run the required Speedtest CLI commands or start the server.
6. **Validation**: Run [scripts/verify-ooklaserver.sh](scripts/verify-ooklaserver.sh) to validate configuration, firewall rules, and security headers.
7. **Parse output and report**: Analyze findings, stopping if critical errors (e.g., Error 100) occur.

## Safety

- **Read-only discovery**: Always perform read-only checks (e.g., checking versions, reading firewall rules) before proposing changes.
- **Confirmation required**: Explicit user confirmation is required for destructive, external, privileged, or production-impacting actions (e.g., changing firewall rules, deploying OoklaServer).
- **Dry-run**: Dry-run firewall changes where possible.

## Validation and Failure Handling

- **Validation**: Use `scripts/verify-ooklaserver.sh` to validate the server configuration and security headers.
- **Failure handling**: If OoklaServer fails to start, rollback firewall rules. If tests fail with Error 100 or 101, check connectivity, DNS, and firewall. Do not repeat a failed action unchanged.

## Output Contract

The result must include:
- A structured summary of the network performance or deployment status.
- Evidence of the tests run (e.g., parsed JSON output, script execution results).
- Severity/confidence of any findings.
- Actionable next steps or recommendations.

## Resources

- **[Complete Reference](references/complete-reference.md)**: Exhaustive documentation on Speedtest architecture, CLI commands, configuration schemas, deep-dive network analysis, security audit checklists, and troubleshooting guides.
- **[verify-ooklaserver.sh](scripts/verify-ooklaserver.sh)**: Deterministic script to verify OoklaServer configuration, firewall rules (UDP 8080/5060), and security headers.
- **[OoklaServer.properties](templates/OoklaServer.properties)**: Reusable configuration template with secure defaults, log rotation, and connection limits.

## Orchestration

This skill supports spawning sub-agents for parallel execution when tasks can be decomposed (e.g., testing multiple network paths, auditing multiple servers).
- Spawn when 3+ independent items need the same operation.
- Define inputs, schemas, conflict handling, synthesis, and termination conditions for parallel work.
- Use a Consistency Validator Agent to flag contradictions before synthesis.
