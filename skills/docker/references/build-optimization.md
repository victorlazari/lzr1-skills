# Build Optimization

## Overview
This reference covers multi-stage builds, Buildx, multi-platform builds, cache invalidation, and digest pinning.

## Multi-Stage Builds
Use multi-stage builds to keep the final image size small by separating the build environment from the runtime environment.

## Buildx and Multi-Platform Builds
Use Docker Buildx to build images for multiple platforms (e.g., `linux/amd64`, `linux/arm64`) simultaneously.
- Command example:
```bash
docker buildx build --platform linux/amd64,linux/arm64 -t <image> .
```

## Clean Builds
Emphasize the use of `--pull` and `--no-cache` flags for clean builds to ensure the latest base images and dependencies are used.
- Command example:
```bash
docker build --pull --no-cache -t <image> .
```

## Digest Pinning
Explicitly require pinning base image versions using digests to ensure reproducible builds and mitigate supply chain attacks.
- Example: `FROM ubuntu@sha256:abcdef...`

## Authoritative Source
- Docker Build Documentation: https://docs.docker.com/build/
Verified against upstream: 2026-08-07.
