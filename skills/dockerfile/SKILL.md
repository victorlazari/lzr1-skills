---
name: dockerfile
description: Dockerfile Architect & Container Optimization Specialist. Triggers when designing, refactoring, or auditing Dockerfiles for production, optimizing image sizes, implementing BuildKit features, or integrating Trivy/CodeRabbit scanning.
---

# Dockerfile Mastery

## Scope and Triggers
Use this skill when you need to:
- Design, write, or refactor Dockerfiles for production environments.
- Optimize Docker image sizes and build times using multi-stage builds and layer caching.
- Implement advanced BuildKit features like cache mounts and bind mounts.
- Perform security audits on Dockerfiles, including running as non-root, managing secrets securely, and minimizing attack surfaces.
- Troubleshoot Docker build failures, permission issues, and resource limitations.
- Integrate Dockerfile linting (e.g., Hadolint) and vulnerability scanning (e.g., Trivy) into CI/CD pipelines.
- Use CodeRabbit for automated PR reviews of Dockerfiles.

## Preconditions
- Target Dockerfile must exist and be accessible.
- Environment must have Docker installed for building and testing.
- For linting and scanning, `hadolint` and `trivy` should be available.
- Verify user intent before applying destructive changes to production Dockerfiles.

## Source Freshness
- Volatile facts like supported versions or specific flags require runtime verification against authoritative sources (Docker docs, Trivy docs, CodeRabbit docs).
- Verified against upstream: 2026-08-07.

## Workflow
1. Analyze the target Dockerfile and application requirements.
2. Run `scripts/lint-dockerfile.sh` to identify syntax errors and basic vulnerabilities.
3. Evaluate base image selection, multi-stage build design, and layer caching.
4. Apply security hardening (non-root, secrets management).
5. Integrate CodeRabbit path instructions for automated review.
6. Run a comprehensive Trivy scan (including IaC and secrets).
7. Synthesize findings and propose an optimized, secure Dockerfile.
8. Stop when the Dockerfile passes all linting and security checks.

## Safety
- Require confirmation before applying destructive changes to production Dockerfiles.
- Use dry-runs for Trivy scans.
- Validate Dockerfile syntax with Hadolint before building.
- Ensure containers run as non-root.
- Verify multi-stage builds reduce image size.

## Validation
- Run `scripts/lint-dockerfile.sh` to validate syntax and basic security.
- Perform dry-run builds to verify multi-stage builds and caching.
- Check that the final image runs as non-root.

## Failure Handling
- If linting fails, review the Hadolint output and correct syntax errors.
- If Trivy scanning fails, check network connectivity and Trivy configuration.
- If the build fails, review the Docker build logs for missing dependencies or incorrect paths.
- Do not repeat a failed action unchanged; diagnose the root cause and apply a fix.

## Output Contract
- Provide a structured report of findings, including syntax errors, security vulnerabilities, and optimization opportunities.
- Deliver an optimized, secure Dockerfile that passes all linting and security checks.
- Include actionable next steps for integrating the Dockerfile into the CI/CD pipeline.

## Resources
- [Complete Reference](references/complete-reference.md): Detailed guidance on Dockerfile optimization, Trivy scanning, and CodeRabbit integration.
- [Lint Dockerfile Script](scripts/lint-dockerfile.sh): Deterministic script to run Hadolint and basic Trivy scans on a Dockerfile.
- [Dockerfile Template](templates/Dockerfile.template): A best-practice Dockerfile template demonstrating multi-stage builds, non-root execution, and caching.

## Orchestration
- Sub-agents can be spawned for parallel execution when tasks can be decomposed (e.g., auditing multiple Dockerfiles, evaluating multiple base images).
- Ensure parallel tasks have clear inputs, schemas, and synthesis steps.

## Authoritative sources

- [Authoritative source map](references/source-map.md) — consult this before relying on volatile upstream behavior.

## Package resource index

| Resource | Purpose |
|---|---|
| [references/source-map.md](references/source-map.md) | Supporting package resource; inspect before use and apply the workflow’s safety and validation gates. |
