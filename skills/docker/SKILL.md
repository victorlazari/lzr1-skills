---
name: docker
description: Advanced Docker operations, multi-platform builds, security hardening, and production troubleshooting.
---

# Docker Super Specialist

## Scope and Triggers
Use this skill when you need to:
- Build multi-platform Docker images using Buildx.
- Write or validate Docker Compose configurations.
- Apply security hardening (Rootless Docker, seccomp, AppArmor, SELinux).
- Perform vulnerability scanning and policy evaluation using Docker Scout.
- Troubleshoot container networking, storage, or performance issues.

**Escalation Boundaries:**
- For deep vulnerability scanning, SBOM generation, or compliance checks beyond Docker Scout's capabilities, route to `trivy-scanner`.
- For a comprehensive security review of the entire application architecture, route to `security-review`.

## Preconditions
Before executing Docker operations, verify:
1. The target environment and installed Docker/Buildx/Compose versions.
2. User intent and permissions.
3. The presence of required files (e.g., `Dockerfile`, `docker-compose.yml`).

## Source Freshness
Volatile facts like supported versions or specific command flags must be verified at runtime or checked against the authoritative sources listed in `references/source-map.md`.
Verified against upstream: 2026-08-07.

## Workflow
1. **Analyze:** Determine the target Docker operation (build, compose, secure, troubleshoot).
2. **Verify:** Check the environment and installed Docker/Buildx/Compose versions.
3. **Build:** If building, apply multi-stage optimization, digest pinning, and use `--pull` and `--no-cache` for clean builds. See `references/build-optimization.md`.
4. **Compose:** If composing, validate the configuration against the Compose Specification using `docker compose config` or `scripts/validate-compose.sh`. See `references/compose-patterns.md`.
5. **Secure:** If securing, run Docker Scout for vulnerability scanning and policy evaluation (Up-to-Date Base Images). See `references/security-hardening.md`.
6. **Confirm:** Present proposed changes or commands to the user for confirmation, especially for destructive actions (e.g., `docker system prune -a`).
7. **Execute:** Execute the operation and verify postconditions (e.g., container health, image size, vulnerability report).
8. **Troubleshoot:** Stop when the operation is successful and validated, or provide a structured troubleshooting report if it fails. See `references/troubleshooting.md`.

## Safety
- **Read-only Discovery:** Separate read-only discovery from mutations.
- **Confirmation Required:** Require user confirmation before applying destructive actions (e.g., `docker system prune -a`), external actions, or privileged actions.
- **Rootless Docker:** Ensure Rootless Docker is recommended by default.

## Validation
- Use `docker compose config` to validate Compose files before deployment.
- Use `docker buildx bake --print` for dry-run builds.
- Validate base image digests before building.
- Run `scripts/validate-dockerfile.sh` for basic syntax and best practice checks on Dockerfiles.

## Failure Handling
- If an operation fails, diagnose the error using `references/troubleshooting.md`.
- Do not repeat a failed action unchanged.
- Provide rollback guidance if applicable.

## Output Contract
The result must include:
- A summary of the operation performed.
- Evidence of success (e.g., container status, image size, vulnerability report).
- Any actionable next steps or warnings.

## Resources
- `references/compose-patterns.md`: Advanced Compose patterns, multi-environment setups, and Compose Specification features.
- `references/security-hardening.md`: Security best practices, Rootless Docker, seccomp, AppArmor, SELinux, and Docker Scout policies.
- `references/build-optimization.md`: Multi-stage builds, Buildx, multi-platform builds, cache invalidation, and digest pinning.
- `references/troubleshooting.md`: Structured troubleshooting guide for networking, storage, and performance issues.
- `references/source-map.md`: Focused source map linking to authoritative documentation.
- `scripts/validate-compose.sh`: Script to validate Compose files against the latest Compose Specification.
- `scripts/validate-dockerfile.sh`: Script to perform basic syntax and best practice checks on Dockerfiles.
