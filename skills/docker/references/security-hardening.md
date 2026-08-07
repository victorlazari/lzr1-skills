# Security Hardening

## Overview
This reference covers security best practices, Rootless Docker, seccomp, AppArmor, SELinux, and Docker Scout policies.

## Rootless Docker
Run the Docker daemon and containers as a non-root user to mitigate potential vulnerabilities in the daemon and the container runtime.
- Recommended by default for enhanced security.

## Security Profiles
- **seccomp:** Restrict the system calls a container can make.
- **AppArmor:** Apply mandatory access control (MAC) profiles to containers.
- **SELinux:** Use SELinux labels to isolate containers.

## Docker Scout
Use Docker Scout for vulnerability scanning and policy evaluation.
- **Up-to-Date Base Images:** Ensure base images are up-to-date to minimize vulnerabilities.
- Command example:
```bash
docker scout cves <image>
docker scout policy <image>
```

## Authoritative Source
- Docker Security Documentation: https://docs.docker.com/engine/security/
Verified against upstream: 2026-08-07.
