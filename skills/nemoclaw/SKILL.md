---
name: nemoclaw
description: NVIDIA NemoClaw Platform Specialist for enterprise deployment, advanced security hardening, multi-sandbox orchestration, and GPU inference optimization.
---

# NemoClaw Advanced Guide

## When to Use

Use this skill when you need to:
- Deploy and orchestrate multiple AI agent sandboxes using NemoClaw.
- Implement advanced security hardening including Landlock filesystem policies, seccomp profiles, and capability drops.
- Configure remote GPU deployments, including DGX Spark optimization and cloud GPU integration.
- Deploy NemoClaw on Kubernetes clusters with Helm charts and network policies.
- Manage state, cross-machine migration, disaster recovery, and blue-green deployments.
- Configure advanced inference patterns like multi-provider failover, cost-optimized routing, and privacy-aware routing.
- Integrate with the broader NVIDIA AI ecosystem (NeMo Framework, NeMo Guardrails, NVIDIA NIMs).
- Troubleshoot complex distributed systems, analyze logs, and optimize performance.

## Sub-Agent Spawning

This skill supports spawning sub-agents for parallel execution when tasks can be decomposed:

| Trigger Condition | Sub-Agent Type | Purpose |
|---|---|---|
| Multiple sandboxes to deploy | Sandbox Orchestrator | Parallel deployment and configuration of sandboxes |
| Multiple security policies to validate | Security Validator | Parallel validation of Landlock, seccomp, and capabilities |
| Multiple regions to configure | Region Configurator | Parallel setup of multi-region replication and routing |
| Bulk log analysis | Diagnostics Agent | Parallel issue investigation across multiple components |

### Spawning Rules
- Spawn when 3+ independent items need the same operation
- Each sub-agent receives: context, specific target, success criteria
- Results are aggregated and cross-referenced for conflicts
- Maximum concurrent sub-agents: 10

## Workflow

1. **Assessment & Planning**: Evaluate the deployment requirements, including hardware, security policies, and inference needs. Determine if multi-sandbox orchestration or Kubernetes deployment is required.
2. **Blueprint Engineering**: Develop or customize the NemoClaw blueprint. Ensure the SHA-256 digest is verified to prevent supply chain attacks.
3. **Security Hardening**: Apply Landlock policies, seccomp profiles, and capability drops. Review MITRE ATLAS threat mitigations.
4. **Deployment**: Execute the deployment using `nemoclaw onboard` or Kubernetes Helm charts. Configure network policies and resource allocation.
5. **Inference Configuration**: Set up the inference router for multi-provider failover, cost optimization, or privacy-aware routing.
6. **Monitoring & Observability**: Configure health checks, key metrics monitoring, and structured logging.
7. **State Management**: Establish state snapshot schedules for disaster recovery and plan for cross-machine migration if necessary.
8. **Validation & Troubleshooting**: Use the NemoClaw CLI (`nemoclaw status`, `nemoclaw logs`, `nemoclaw top`) to verify the deployment and troubleshoot any issues.

## Core Principles

- **Zero-Trust Security**: Enforce strict isolation using Landlock, seccomp, and capability drops. Lock policies at sandbox creation.
- **Deterministic Execution**: Ensure blueprint execution follows a deterministic pipeline with digest verification.
- **Resource Isolation**: Allocate explicit CPU and memory limits to prevent resource contention in multi-sandbox environments.
- **High Availability**: Utilize active-active replication, multi-provider failover, and blue-green deployments for zero-downtime operations.
- **Observability**: Maintain comprehensive visibility through structured logging, metrics, and health checks.

## Key References

- [NVIDIA NemoClaw Official Documentation](https://docs.nvidia.com/nemoclaw/latest/)
- [NVIDIA NemoClaw GitHub Repository](https://github.com/NVIDIA/NemoClaw)
- NemoClaw CLI Command Reference
- NemoClaw Configuration Schemas Guide
- NemoClaw Deep Dive Architecture
- NemoClaw Security Audit Checklist & Deep-Dive Hardening Guide

---

## Adversarial Verification Panel

For each significant security vulnerability or deployment issue produced by the parallel sub-agents:

1. Spawn **3 independent Refuter Agents** per finding, each with:
   - The finding in full
   - Instruction: *"Assume this finding is wrong. Find the strongest argument against it."*
   - Default stance: `refuted=true` if evidence is insufficient or ambiguous
2. A finding is **confirmed** only if ≥2 refuters fail to refute it
3. A finding is **discarded** if ≥2 refuters succeed
4. When a confirmed finding had 1 successful refuter, include the dissenting argument in the output with a `CONTESTED` label

> This prevents plausible-but-wrong security vulnerabilities or deployment issues from reaching the final output. The 3-vote panel eliminates single-point hallucination without requiring unanimity.

## Cross-System Consistency Validator

After all parallel agents (Sandbox Orchestrator, Security Validator, Region Configurator, Diagnostics Agent) complete, but **before** synthesis:

Run one **Consistency Validator Agent** with all parallel outputs that:
- Flags any pair of recommendations that logically contradict each other
  *(example: Security Validator recommends dropping all capabilities for a sandbox while Sandbox Orchestrator requires NET_ADMIN capability for cross-region mesh networking in that same sandbox)*
- Notes where one agent's output is a prerequisite for another agent's recommendation
- Passes contradictions to the Synthesis Agent as `MUST_RESOLVE` items
- Passes missing prerequisites as `SEQUENCING_REQUIRED` items

## Synthesis Agent (Upgraded)

The synthesis step actively resolves rather than aggregates:

1. **`MUST_RESOLVE` contradictions**: Pick the better recommendation, annotate the reasoning, preserve the dissenting view as a footnote
2. **`SEQUENCING_REQUIRED` items**: Re-order the unified deployment and security hardening report so prerequisites appear before the steps that depend on them
3. **Confidence calibration**: Label each finding `HIGH` / `MEDIUM` / `LOW` confidence based on refuter panel outcomes
4. **Gap analysis**: Note any analysis dimension not covered by any of the parallel agents — these are blind spots, not confirmed negatives
