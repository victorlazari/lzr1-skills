---
name: speedtest
description: Comprehensive mastery of Speedtest (Ookla) methodologies, architecture, CLI integration, and network performance diagnostics. Use when testing 5G/fiber connections, configuring custom OoklaServer instances, analyzing latency/jitter, or troubleshooting network throughput issues.
---

# Speedtest (Ookla) Specialist

## When to Use

Use this skill when you need to:
- Measure or analyze network performance, including bandwidth, latency, and jitter.
- Troubleshoot slow speeds, inconsistency, or timeouts in network connections.
- Configure, automate, or integrate the Speedtest CLI into monitoring pipelines (e.g., Prometheus, Grafana).
- Understand or deploy custom OoklaServer instances for enterprise testing.
- Analyze 5G, fiber-optic, or super-fast connections (>10 Gbps) where traditional testing fails.
- Perform security audits or hardening of Speedtest infrastructure.

## Sub-Agent Spawning

This skill supports spawning sub-agents for parallel execution when tasks can be decomposed:

| Trigger Condition | Sub-Agent Type | Purpose |
|---|---|---|
| Multiple network paths to test | Network Tester | Parallel speed and latency tests across different interfaces or locations |
| Multiple servers to audit | Security Auditor | Parallel security review and hardening of OoklaServer instances |
| Bulk log analysis | Diagnostics Agent | Parallel parsing of Speedtest CLI JSON logs for anomaly detection |
| Multi-region monitoring setup | Config Deployer | Parallel deployment of automated Speedtest monitoring scripts |

### Spawning Rules
- Spawn when 3+ independent items need the same operation (e.g., testing 3+ network interfaces).
- Each sub-agent receives: context, specific target (e.g., server IP, interface name), and success criteria.
- Results are aggregated and cross-referenced for conflicts or network-wide patterns.
- Maximum concurrent sub-agents: 10.

## Workflow

1. **Requirement Analysis**: Determine the goal (e.g., basic bandwidth test, automated monitoring, server deployment, security audit).
2. **Methodology Selection**:
   - For basic tests: Use standard Speedtest CLI commands.
   - For high-speed (5G/Fiber): Ensure multi-threaded TCP testing is active to overcome TCP slow start.
   - For monitoring: Configure JSON output and schedule via cron/systemd.
3. **Execution & Diagnostics**:
   - Run tests and collect metrics (Download, Upload, Latency, Jitter, Packet Loss).
   - If issues arise (e.g., Error 100, 101), follow the troubleshooting steps (check connectivity, DNS, firewall).
4. **Analysis & Reporting**:
   - Parse JSON/CSV outputs.
   - Correlate metrics with network events (e.g., bufferbloat, ISP throttling).
   - Generate actionable insights or alerts.

## Core Principles

- **Foreground Testing**: Speedtest actively floods the network interface to measure realistic maximum Quality of Service (QoS), unlike passive background tests.
- **Dynamic Connection Scaling**: Overcomes TCP slow start by dynamically spawning multiple threads (TCP connections) to saturate high-bandwidth links.
- **Multi-Stage Latency**: Measures ping at Idle, Download, and Upload stages to accurately assess bufferbloat and network responsiveness under load.
- **Security First**: Speedtest infrastructure must be hardened against DDoS, secured via TLS, and compliant with data privacy regulations (GDPR, CCPA).

## Key References

For detailed technical information, refer to the bundled reference files:

- **[Complete Reference](references/complete-reference.md)**: Exhaustive documentation on Speedtest architecture, CLI commands, configuration schemas, deep-dive network analysis, security audit checklists, and troubleshooting guides.
- **[Reading List](references/reading-list.md)**: Curated list of 30+ books and 30+ articles (2023-2026) covering network performance, 5G, TCP optimization, and network security.

---

## Adversarial Verification Panel

For each significant network performance diagnostic finding produced by the parallel sub-agents:

1. Spawn **3 independent Refuter Agents** per finding, each with:
   - The finding in full
   - Instruction: *"Assume this finding is wrong. Find the strongest argument against it."*
   - Default stance: `refuted=true` if evidence is insufficient or ambiguous
2. A finding is **confirmed** only if ≥2 refuters fail to refute it
3. A finding is **discarded** if ≥2 refuters succeed
4. When a confirmed finding had 1 successful refuter, include the dissenting argument in the output with a `CONTESTED` label

> This prevents plausible-but-wrong network performance diagnostic findings from reaching the final output. The 3-vote panel eliminates single-point hallucination without requiring unanimity.

## Cross-System Consistency Validator

After all parallel agents (Network Tester, Security Auditor, Diagnostics Agent, Config Deployer) complete, but **before** synthesis:

Run one **Consistency Validator Agent** with all parallel outputs that:
- Flags any pair of recommendations that logically contradict each other
  *(example: the Security Auditor recommends disabling multi-threaded TCP connections to reduce attack surface while the Network Tester recommends enabling more TCP threads to saturate a high-bandwidth 5G link)*
- Notes where one agent's output is a prerequisite for another agent's recommendation
- Passes contradictions to the Synthesis Agent as `MUST_RESOLVE` items
- Passes missing prerequisites as `SEQUENCING_REQUIRED` items

## Synthesis Agent (Upgraded)

The synthesis step actively resolves rather than aggregates:

1. **`MUST_RESOLVE` contradictions**: Pick the better recommendation, annotate the reasoning, preserve the dissenting view as a footnote
2. **`SEQUENCING_REQUIRED` items**: Re-order the unified network performance report so prerequisites appear before the steps that depend on them
3. **Confidence calibration**: Label each finding `HIGH` / `MEDIUM` / `LOW` confidence based on refuter panel outcomes
4. **Gap analysis**: Note any analysis dimension not covered by any of the parallel agents — these are blind spots, not confirmed negatives
