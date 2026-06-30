---
name: docker
description: Advanced Docker operations, multi-platform builds, security hardening, and production troubleshooting.
---

# Docker Super Specialist

## When to Use
Use this skill when you need to:
- Build multi-platform Docker images using Buildx.
- Configure and troubleshoot Docker-in-Docker (DinD) or Docker Socket Mounting (DooD) for CI/CD pipelines.
- Design advanced Docker Compose patterns (overrides, environment-specific configs, YAML anchors, includes).
- Manage Docker Swarm clusters, services, secrets, and overlay networks.
- Implement GPU passthrough for machine learning workloads.
- Write custom entrypoint scripts with proper signal handling and graceful shutdown.
- Implement Init Containers and Sidecar patterns in Compose.
- Perform Blue-Green or Canary deployments using Compose and a reverse proxy.
- Optimize Dockerfiles with multi-stage builds and cache invalidation strategies.
- Secure Docker environments using seccomp, AppArmor, SELinux, and Rootless Docker.
- Troubleshoot complex container networking, storage, and performance issues.

## Sub-Agent Spawning

This skill supports spawning sub-agents for parallel execution when tasks can be decomposed:

| Trigger Condition | Sub-Agent Type | Purpose |
|---|---|---|
| Multiple Dockerfiles to optimize | Dockerfile Optimizer | Parallel optimization of multi-stage builds and caching |
| Multiple Compose files to validate | Compose Validator | Parallel validation of advanced Compose patterns |
| Multiple images to scan for vulnerabilities | Security Scanner | Parallel execution of `docker scout cves` and policy evaluation |
| Multiple Swarm nodes to inspect | Swarm Inspector | Parallel health checks and troubleshooting of Swarm nodes |

### Spawning Rules
- Spawn when 3+ independent items need the same operation
- Each sub-agent receives: context, specific target, success criteria
- Results are aggregated and cross-referenced for conflicts
- Maximum concurrent sub-agents: 10

## Workflow
1. **Analyze the Request:** Determine if the task involves building images, configuring Compose/Swarm, securing the environment, or troubleshooting an issue.
2. **Select the Pattern:** Choose the appropriate Docker pattern (e.g., multi-stage build, sidecar, init container) based on the requirements.
3. **Implement Configuration:** Write or modify Dockerfiles, `compose.yaml` files, or Swarm deployment scripts.
4. **Apply Security Best Practices:** Ensure least privilege, use rootless Docker where possible, and configure seccomp/AppArmor/SELinux profiles.
5. **Test and Validate:** Use `docker compose config` to validate Compose files, run test builds, and verify container health and networking.
6. **Troubleshoot (if necessary):** Follow the structured troubleshooting guide (check logs, inspect containers, test connectivity, monitor resources).

## Core Principles
- **Security First:** Never mount `/var/run/docker.sock` in untrusted environments. Use Rootless Docker and scan images for vulnerabilities.
- **Optimize for Performance:** Use multi-stage builds to keep images small. Order Dockerfile instructions to maximize layer caching. Use volumes for write-heavy data instead of the container's writable layer.
- **Design for Maintainability:** Keep Compose configurations DRY using overrides, environment files, and YAML anchors.
- **Graceful Shutdown:** Ensure applications handle `SIGTERM` signals properly to avoid forceful termination and data corruption.
- **Centralized Logging and Monitoring:** Never rely solely on `docker logs` in production. Forward logs to a central system and monitor host/container metrics.

## Key References
- **Multi-Platform Builds:** Use `docker buildx build --platform ... --push .`
- **Docker-in-Docker (DinD):** Use `docker:dind-rootless` for better security.
- **Compose Overrides:** Use `compose.override.yaml` or explicit environment files (`-f compose.yaml -f compose.prod.yaml`).
- **Swarm Updates:** Use `docker service update --image ...` for rolling updates.
- **GPU Passthrough:** Use `deploy.resources.reservations.devices` with the `nvidia` driver.
- **Signal Handling:** Use `exec "$@"` in entrypoint scripts to pass signals to the main application.
- **Storage Drivers:** Use `overlay2` and manage disk space with `docker system prune`.

---

## Adversarial Verification Panel

For each significant security vulnerabilities produced by the parallel sub-agents:

1. Spawn **3 independent Refuter Agents** per finding, each with:
   - The finding in full
   - Instruction: *"Assume this finding is wrong. Find the strongest argument against it."*
   - Default stance: `refuted=true` if evidence is insufficient or ambiguous
2. A finding is **confirmed** only if ≥2 refuters fail to refute it
3. A finding is **discarded** if ≥2 refuters succeed
4. When a confirmed finding had 1 successful refuter, include the dissenting argument in the output with a `CONTESTED` label

> This prevents plausible-but-wrong security vulnerabilities from reaching the final output. The 3-vote panel eliminates single-point hallucination without requiring unanimity.

## Cross-System Consistency Validator

After all parallel agents (Dockerfile Optimizer, Compose Validator, Security Scanner, Swarm Inspector) complete, but **before** synthesis:

Run one **Consistency Validator Agent** with all parallel outputs that:
- Flags any pair of recommendations that logically contradict each other
  *(example: the Dockerfile Optimizer recommends running the application as root to bind to port 80 for performance, while the Security Scanner flags running as root as a critical vulnerability requiring an unprivileged user and port remapping)*
- Notes where one agent's output is a prerequisite for another agent's recommendation
- Passes contradictions to the Synthesis Agent as `MUST_RESOLVE` items
- Passes missing prerequisites as `SEQUENCING_REQUIRED` items

## Synthesis Agent (Upgraded)

The synthesis step actively resolves rather than aggregates:

1. **`MUST_RESOLVE` contradictions**: Pick the better recommendation, annotate the reasoning, preserve the dissenting view as a footnote
2. **`SEQUENCING_REQUIRED` items**: Re-order the unified Docker Hardening Report so prerequisites appear before the steps that depend on them
3. **Confidence calibration**: Label each finding `HIGH` / `MEDIUM` / `LOW` confidence based on refuter panel outcomes
4. **Gap analysis**: Note any analysis dimension not covered by any of the parallel agents — these are blind spots, not confirmed negatives
