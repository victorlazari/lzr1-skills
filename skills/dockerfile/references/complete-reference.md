# Dockerfile Mastery — Complete Reference

## 1. Advanced BuildKit Features

BuildKit is the modern execution engine for Docker builds. Beyond parallel execution, it unlocks powerful advanced features that transform how Dockerfiles are structured.

### 1.1 Cache Mounts for Package Managers

Standard Docker layer caching is binary — if a `package.json` changes, the entire `npm ci` layer is invalidated, and all packages are downloaded again from the internet. BuildKit introduces cache mounts, which preserve package manager caches across builds, even when the Docker layer is invalidated.

```dockerfile
# syntax=docker/dockerfile:1
FROM node:22-alpine AS deps
WORKDIR /app
COPY package*.json ./
# The cache mount persists the npm cache directory between builds
RUN --mount=type=cache,target=/root/.npm \
    npm ci
```

When a dependency is added, the layer is invalidated, but `npm ci` will find the previously downloaded packages in the `/root/.npm` cache mount, drastically reducing network I/O and build time.

### 1.2 Bind Mounts for Source Code

Traditionally, source code is copied into the image using `COPY src/ ./` before a build step. This creates a permanent layer containing the raw source code. If the final image only needs the compiled binary, copying the source code creates unnecessary intermediate layers.

BuildKit allows bind-mounting the build context directly into a `RUN` instruction:

```dockerfile
# syntax=docker/dockerfile:1
FROM golang:1.21-alpine AS build
WORKDIR /app
# Mount the source code temporarily without creating a layer
RUN --mount=type=bind,target=. \
    --mount=type=cache,target=/root/.cache/go-build \
    go build -o /bin/server ./cmd/server
```

This pattern ensures the raw source code never exists as a layer in the image history, saving disk space and preventing source code leakage in intermediate builder images.

## 2. Dockerfile Linting and Code Review

A Dockerfile should be treated as production code, subject to static analysis, linting, and peer review. Integrating automated linting into the CI/CD pipeline prevents anti-patterns and security vulnerabilities from reaching production.

### 2.1 Hadolint Integration

[Hadolint](https://github.com/hadolint/hadolint) is the industry-standard Haskell-based Dockerfile linter. It parses the Dockerfile into an Abstract Syntax Tree (AST) and applies rules based on official Docker best practices.

Hadolint enforces rules such as:
- **DL3008:** Pin versions in `apt-get install` (prevents unrepeatable builds).
- **DL3009:** Pin versions in `apk add` (prevents unrepeatable builds).
- **DL3002:** Last `USER` should not be root (enforces non-root execution).
- **DL3020:** Use `COPY` instead of `ADD` (reduces attack surface).

Hadolint should be integrated into GitHub Actions or GitLab CI to fail pull requests that violate best practices:

```yaml
# GitHub Actions Example
name: Dockerfile Lint
on: [push, pull_request]
jobs:
  hadolint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run Hadolint
        uses: hadolint/hadolint-action@v3.1.0
        with:
          dockerfile: Dockerfile
          failure-threshold: warning
```

### 2.2 Container Vulnerability Scanning

Linting analyzes the Dockerfile syntax, but vulnerability scanning analyzes the resulting image for known CVEs (Common Vulnerabilities and Exposures) in OS packages and application dependencies.

**Trivy** (by Aqua Security) and **Docker Scout** are the leading tools for this purpose. They generate a Software Bill of Materials (SBOM) and check it against vulnerability databases.

The CI pipeline should build the image, scan it with Trivy, and block the deployment if critical or high vulnerabilities are detected:

```yaml
# GitHub Actions Example with Trivy
      - name: Build image
        run: docker build -t my-app:${{ github.sha }} .
        
      - name: Run Trivy vulnerability scanner
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: 'my-app:${{ github.sha }}'
          format: 'table'
          exit-code: '1'
          ignore-unfixed: true
          vuln-type: 'os,library'
          severity: 'CRITICAL,HIGH'
```

## 3. The Ephemeral Container Paradigm

The image defined by a Dockerfile should generate containers that are as ephemeral as possible. Ephemeral means that the container can be stopped, destroyed, rebuilt, and replaced with an absolute minimum of setup and configuration.

### 3.1 Stateless Architecture

Containers must not store persistent state within their own filesystem. Any data that must survive a container restart (databases, user uploads, logs) must be written to external volumes, object storage (like S3), or external logging services. The Dockerfile should configure the application to output logs to `stdout` and `stderr` rather than local files, allowing the container runtime to handle log routing.

### 3.2 Single Concern Principle

Each container should have only one concern. Decoupling applications into multiple containers makes it easier to scale horizontally and reuse containers. 

A Dockerfile should not attempt to run a web server, a database, and a background worker simultaneously using process managers like `supervisord`. Instead, these should be split into three separate Dockerfiles (or three different entrypoints using the same image), managed via Docker Compose or Kubernetes.

### 3.3 Graceful Shutdown Handling

A robust Dockerfile must ensure the application handles termination signals correctly. When a container orchestrator (like Kubernetes) stops a container, it sends a `SIGTERM` signal. If the application does not exit within a grace period, it sends a `SIGKILL`, forcefully terminating the process and potentially corrupting data or dropping active requests.

The `CMD` instruction must use the **exec form** (`CMD ["node", "server.js"]`) rather than the **shell form** (`CMD node server.js`). The shell form wraps the command in `/bin/sh -c`, which does not pass signals to the underlying child process, preventing graceful shutdowns.

Furthermore, applications like Node.js do not handle `SIGTERM` automatically. Tools like `tini` or `dumb-init` should be used as the `ENTRYPOINT` to act as a lightweight init system, reaping zombie processes and properly forwarding signals to the application.

```dockerfile
RUN apk add --no-cache dumb-init
ENTRYPOINT ["/usr/bin/dumb-init", "--"]
CMD ["node", "server.js"]
```

## 4. Dockerfile Instruction and CLI Command Reference

### 4.1. FROM

The `FROM` instruction initializes a new build stage and sets the Base Image for subsequent instructions.

**Syntax:**
```dockerfile
FROM [--platform=<platform>] <image> [AS <name>]
FROM [--platform=<platform>] <image>[:<tag>] [AS <name>]
FROM [--platform=<platform>] <image>[@<digest>] [AS <name>]
```

### 4.2. RUN

The `RUN` instruction executes any commands in a new layer on top of the current image and commits the results.

**Syntax:**
```dockerfile
# Shell form
RUN <command>

# Exec form
RUN ["executable", "param1", "param2"]
```

### 4.3. CMD

The `CMD` instruction provides defaults for an executing container.

**Syntax:**
```dockerfile
# Exec form (preferred)
CMD ["executable","param1","param2"]

# Default parameters to ENTRYPOINT
CMD ["param1","param2"]

# Shell form
CMD command param1 param2
```

### 4.4. LABEL

The `LABEL` instruction adds metadata to an image.

**Syntax:**
```dockerfile
LABEL <key>=<value> <key>=<value> <key>=<value> ...
```

### 4.5. EXPOSE

The `EXPOSE` instruction informs Docker that the container listens on the specified network ports at runtime.

**Syntax:**
```dockerfile
EXPOSE <port> [<port>/<protocol>...]
```

### 4.6. ENV

The `ENV` instruction sets the environment variable `<key>` to the value `<value>`.

**Syntax:**
```dockerfile
ENV <key>=<value> ...
```

### 4.7. ADD

The `ADD` instruction copies new files, directories, or remote file URLs from `<src>` and adds them to the filesystem of the image at the path `<dest>`.

**Syntax:**
```dockerfile
ADD [--chown=<user>:<group>] [--chmod=<perms>] [--checksum=<checksum>] <src>... <dest>
```

### 4.8. COPY

The `COPY` instruction copies new files or directories from `<src>` and adds them to the filesystem of the container at the path `<dest>`.

**Syntax:**
```dockerfile
COPY [--chown=<user>:<group>] [--chmod=<perms>] <src>... <dest>
```

### 4.9. ENTRYPOINT

An `ENTRYPOINT` allows you to configure a container that will run as an executable.

**Syntax:**
```dockerfile
# Exec form (preferred)
ENTRYPOINT ["executable", "param1", "param2"]

# Shell form
ENTRYPOINT command param1 param2
```

### 4.10. VOLUME

The `VOLUME` instruction creates a mount point with the specified name and marks it as holding externally mounted volumes.

**Syntax:**
```dockerfile
VOLUME ["/data"]
```

### 4.11. USER

The `USER` instruction sets the user name (or UID) and optionally the user group (or GID) to use as the default user and group.

**Syntax:**
```dockerfile
USER <user>[:<group>]
```

### 4.12. WORKDIR

The `WORKDIR` instruction sets the working directory for any `RUN`, `CMD`, `ENTRYPOINT`, `COPY`, and `ADD` instructions that follow it.

**Syntax:**
```dockerfile
WORKDIR /path/to/workdir
```

### 4.13. ARG

The `ARG` instruction defines a variable that users can pass at build-time to the builder.

**Syntax:**
```dockerfile
ARG <name>[=<default value>]
```

### 4.14. ONBUILD

The `ONBUILD` instruction adds to the image a trigger instruction to be executed at a later time.

**Syntax:**
```dockerfile
ONBUILD <INSTRUCTION>
```

### 4.15. STOPSIGNAL

The `STOPSIGNAL` instruction sets the system call signal that will be sent to the container to exit.

**Syntax:**
```dockerfile
STOPSIGNAL signal
```

### 4.16. HEALTHCHECK

The `HEALTHCHECK` instruction tells Docker how to test a container to check that it is still working.

**Syntax:**
```dockerfile
HEALTHCHECK [OPTIONS] CMD command
HEALTHCHECK NONE
```

### 4.17. SHELL

The `SHELL` instruction allows the default shell used for the shell form of commands to be overridden.

**Syntax:**
```dockerfile
SHELL ["executable", "parameters"]
```

## 5. Dockerfile Security Audit Checklist

### 5.1. Base Image Selection and Verification
- Use Official and Trusted Images.
- Specify Exact Image Tags (avoid `latest`).
- Minimize the Attack Surface (use Alpine, Distroless, or Scratch).

### 5.2. User Management and Privilege Escalation
- Run as a Non-Root User.
- Prevent Privilege Escalation (`--security-opt=no-new-privileges:true`).

### 5.3. Package Management and Dependencies
- Keep Packages Updated.
- Remove Package Manager Caches.
- Pin Dependency Versions.

### 5.4. Secrets Management and Sensitive Data
- Never Hardcode Secrets.
- Use Docker BuildKit Secrets (`--mount=type=secret`).
- Handle SSH Keys Securely (`--mount=type=ssh`).

### 5.5. File System and Permissions
- Set Appropriate Ownership and Permissions (`COPY --chown`).
- Make the Root Filesystem Read-Only.

### 5.6. Network Configuration and Exposure
- Expose Only Necessary Ports.
- Bind to Specific Interfaces.

### 5.7. Build Context and .dockerignore
- Use a `.dockerignore` File to exclude sensitive files and large directories.

### 5.8. Multi-stage Builds
- Separate Build and Runtime Environments.

### 5.9. Container Runtime Configuration
- Define a Clear ENTRYPOINT and CMD (use exec form).
- Implement Health Checks.

### 5.10. Security Scanning and CI/CD Integration
- Integrate Image Scanning (e.g., Trivy).
- Linting Dockerfiles (e.g., Hadolint).

## 6. Comprehensive Troubleshooting & Diagnostics

### 6.1. Common Dockerfile Errors
- **Syntax Errors:** Misplaced instructions, case sensitivity, missing arguments.
- **Permission Issues:** Running commands as non-root users without sufficient privileges, incorrect file permissions.
- **Network Issues:** DNS resolution failures, proxy configurations.
- **Resource Limitations:** Memory limits, CPU usage.

### 6.2. Error Codes and Their Meanings
- **Docker Build Errors:** Code 1 (General build failure), Code 125 (Docker command failure), Code 137 (Out of memory).
- **Docker Run Errors:** Code 1 (Application-specific error), Code 139 (Segmentation fault), Code 143 (Container stopped with SIGTERM).

### 6.3. Recovery Strategies
- **Debugging Build Failures:** Step-by-step execution (`--progress=plain`), interactive shell.
- **Optimizing Dockerfile:** Layer minimization, explicit versioning.
- **Handling Layer Caching:** Leverage caching, invalidate cache sparingly.

### 6.4. Common Issues and Solutions
- **Image Bloat:** Use multi-stage builds, Alpine base images.
- **Security Vulnerabilities:** Regular updates, least privilege.
- **Versioning and Compatibility:** Pin versions, use environment variables.

### 6.5. Advanced Troubleshooting Techniques
- **Using Docker Inspect:** Inspect images and containers.
- **Log Analysis:** Container logs (`docker logs`), host logs.
- **Integrating with CI/CD:** Automated testing, versioning strategy.
