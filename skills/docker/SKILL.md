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
