---
name: dockerfile
description: Dockerfile Architect & Container Optimization Specialist. Expertise in advanced BuildKit features, multi-stage builds, layer caching, package management optimization, and image security.
---

# Dockerfile Mastery

## When to Use

Use this skill when you need to:
- Design, write, or refactor Dockerfiles for production environments.
- Optimize Docker image sizes and build times using multi-stage builds and layer caching.
- Implement advanced BuildKit features like cache mounts and bind mounts.
- Perform security audits on Dockerfiles, including running as non-root, managing secrets securely, and minimizing attack surfaces.
- Troubleshoot Docker build failures, permission issues, and resource limitations.
- Integrate Dockerfile linting (e.g., Hadolint) and vulnerability scanning (e.g., Trivy) into CI/CD pipelines.

## Sub-Agent Spawning

This skill supports spawning sub-agents for parallel execution when tasks can be decomposed:

| Trigger Condition | Sub-Agent Type | Purpose |
|---|---|---|
| Multiple Dockerfiles to audit | Security Auditor | Parallel security review of each Dockerfile |
| Multiple base images to evaluate | Base Image Evaluator | Parallel base image size and vulnerability analysis |
| Multiple build stages to optimize | Build Optimizer | Parallel optimization of multi-stage builds |
| Bulk linting and compliance checks | Linter Agent | Parallel Hadolint and compliance checks |

### Spawning Rules
- Spawn when 3+ independent items need the same operation
- Each sub-agent receives: context, specific target, success criteria
- Results are aggregated and cross-referenced for conflicts
- Maximum concurrent sub-agents: 10

## Workflow

1. **Analyze Requirements:** Understand the application's runtime dependencies, build tools, and security constraints.
2. **Base Image Selection:** Choose the most appropriate minimal base image (e.g., Alpine, Debian Slim, Distroless) and pin to a specific version or digest.
3. **Multi-Stage Design:** Separate the build environment from the runtime environment to minimize the final image size.
4. **Layer Optimization:** Order instructions from least frequently changed to most frequently changed to maximize cache hits. Combine `RUN` commands where appropriate.
5. **Package Management:** Use optimized package manager commands (e.g., `npm ci`, `apt-get install --no-install-recommends`, `apk add --no-cache`) and clean up caches in the same layer.
6. **Security Hardening:** Ensure the container runs as a non-root user, handles secrets securely via BuildKit, and exposes only necessary ports.
7. **Validation:** Lint the Dockerfile with Hadolint, scan the resulting image for vulnerabilities, and verify graceful shutdown handling.

## Core Principles

- **Immutability:** Images should be immutable and stateless. Persistent data must be stored externally.
- **Least Privilege:** Always run containers as a non-root user and drop unnecessary capabilities.
- **Single Concern:** Each container should have only one concern. Do not run multiple services (e.g., web server and database) in a single container.
- **Determinism:** Pin all dependencies and base images to ensure reproducible builds.
- **Ephemeral Containers:** Containers should be designed to be stopped, destroyed, rebuilt, and replaced with minimal setup.

## Key References

- [Docker Build Best Practices](https://docs.docker.com/build/building/best-practices/)
- [Docker Multi-stage Builds](https://docs.docker.com/build/building/multi-stage/)
- [Hadolint GitHub Repository](https://github.com/hadolint/hadolint)
