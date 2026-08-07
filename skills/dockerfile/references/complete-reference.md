# Complete Reference: Dockerfile Optimization and Security

**Verified against upstream: 2026-08-07**

## Table of Contents
1. [Dockerfile Optimization](#dockerfile-optimization)
2. [Trivy Integration](#trivy-integration)
3. [CodeRabbit Integration](#coderabbit-integration)

## Dockerfile Optimization

### Multi-Stage Builds
Multi-stage builds allow you to use multiple `FROM` statements in your Dockerfile. Each `FROM` instruction can use a different base, and each of them begins a new stage of the build. You can selectively copy artifacts from one stage to another, leaving behind everything you don't want in the final image.

### Layer Caching
Docker caches the results of each instruction in a Dockerfile. To optimize build times, order instructions from least frequently changed to most frequently changed. For example, copy dependency files and install dependencies before copying the application source code.

### BuildKit Features
BuildKit provides advanced features like cache mounts and bind mounts. Cache mounts allow you to cache directories for compilers and package managers, speeding up subsequent builds. Bind mounts allow you to bind files or directories to the build container without copying them.

## Trivy Integration

Trivy is a comprehensive security scanner that can scan container images, file systems, and Git repositories for vulnerabilities, misconfigurations, secrets, and software licenses.

### IaC and Secrets Scanning
Trivy can scan Infrastructure as Code (IaC) files, including Dockerfiles, for misconfigurations and exposed secrets. This is crucial for identifying security issues early in the development lifecycle.

### Usage
To scan a Dockerfile with Trivy:
```bash
trivy config Dockerfile
```

To scan an image for vulnerabilities:
```bash
trivy image <image-name>
```

## CodeRabbit Integration

CodeRabbit is an AI-powered code review tool that integrates with GitHub and GitLab. It provides automated PR reviews, including path-based instructions for specific file types like Dockerfiles.

### Configuration
To configure CodeRabbit for Dockerfiles, add path-based instructions in the `.coderabbit.yaml` file:

```yaml
reviews:
  path_instructions:
    - path: "**/Dockerfile"
      instructions: |
        - Ensure multi-stage builds are used.
        - Verify that the final image runs as non-root.
        - Check for hardcoded secrets.
```

This configuration ensures that CodeRabbit specifically checks for Dockerfile best practices during PR reviews.
