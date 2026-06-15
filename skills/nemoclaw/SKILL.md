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
