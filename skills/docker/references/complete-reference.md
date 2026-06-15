# Specialist: 49-docker

## === FILE: 49-docker-advanced.md ===
# Docker Super Specialist: Advanced Patterns & Production Operations

## Introduction

Welcome to the Docker Super Specialist guide. This document is designed for technical support operations teams, DevOps engineers, and system administrators who need to troubleshoot, optimize, and secure Docker environments at scale. As a Super Specialist, you are expected to understand not just the basics, but the deep internals of Docker, Docker Compose, and Docker Swarm. This guide covers advanced patterns, multi-platform builds, security hardening, cost/time optimization, and comprehensive troubleshooting strategies.

This document is extremely comprehensive, providing real-world configuration examples, actionable commands, and detailed explanations of edge cases. Whether you are dealing with a simple Compose setup or a complex Swarm cluster, this guide will equip you with the knowledge to resolve issues efficiently and implement best practices.

---

## 1. Multi-Platform Builds with Buildx

In today's diverse hardware landscape, supporting multiple architectures (e.g., `linux/amd64`, `linux/arm64`) is essential. Docker Buildx is a CLI plugin that extends the `docker build` command with the full support of the features provided by Moby BuildKit builder toolkit.

### 1.1 Setting Up Buildx

Before you can build multi-platform images, you need to ensure Buildx is installed and configured correctly.

```bash
# Check if buildx is available
docker buildx version

# Create a new builder instance
docker buildx create --name mybuilder --use

# Inspect the builder to see supported platforms
docker buildx inspect --bootstrap
```

### 1.2 QEMU Emulation vs. Native Cross-Compilation

There are two primary ways to build for different architectures:

1.  **QEMU Emulation:** This is the easiest method. Docker uses QEMU to emulate the target architecture. It's simple to set up but can be significantly slower, especially for CPU-intensive build steps (like compiling code).
2.  **Native Cross-Compilation:** This involves using a compiler that runs on the host architecture but generates code for the target architecture. It's much faster but requires a more complex Dockerfile setup.

#### Setting up QEMU

To use QEMU, you need to register the QEMU emulators on your host machine.

```bash
# Install QEMU emulators
docker run --privileged --rm tonistiigi/binfmt --install all
```

### 1.3 Building Multi-Platform Images

Once configured, you can build an image for multiple platforms simultaneously.

```bash
# Build and push a multi-platform image
docker buildx build --platform linux/amd64,linux/arm64,linux/arm/v7 -t YOUR_REGISTRY/YOUR_IMAGE:latest --push .
```

**Important:** You *must* use the `--push` flag (or `--output type=registry`) when building for multiple platforms, as the local Docker daemon cannot currently store multi-platform manifests directly in its local image cache.

### 1.4 Advanced Dockerfile for Cross-Compilation

To avoid the performance penalty of QEMU, you can use cross-compilation. Here is an example using Go:

```dockerfile
# syntax=docker/dockerfile:1
FROM --platform=$BUILDPLATFORM golang:1.21-alpine AS builder
WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .

# ARG TARGETOS and TARGETARCH are automatically populated by Buildx
ARG TARGETOS
ARG TARGETARCH

# Cross-compile the application
RUN CGO_ENABLED=0 GOOS=$TARGETOS GOARCH=$TARGETARCH go build -o myapp .

FROM alpine:latest
WORKDIR /app
COPY --from=builder /app/myapp .
ENTRYPOINT ["./myapp"]
```

### 1.5 Troubleshooting Buildx

**Error:** `error: multiple platforms feature is currently not supported for docker driver`
**Solution:** You are using the default `docker` driver, which doesn't support multi-platform builds. Create and use a new builder instance: `docker buildx create --use`.

**Error:** `exec format error` when running a built image.
**Solution:** The image was built for the wrong architecture. Ensure you specified the correct `--platform` flag during the build process.

---

## 2. Docker-in-Docker (DinD) vs. Docker Socket Mounting

When running CI/CD pipelines or tools that need to interact with Docker, you have two main approaches: Docker-in-Docker (DinD) and Docker Socket Mounting (often called Docker-outside-of-Docker or DooD).

### 2.1 Docker Socket Mounting (DooD)

This approach involves mounting the host's Docker daemon socket (`/var/run/docker.sock`) into the container.

**Pros:**
*   Simple to set up.
*   Shares the host's image cache, making builds faster.

**Cons:**
*   **Severe Security Risk:** The container has root-level access to the host's Docker daemon. It can start, stop, and delete any container on the host, and even mount the host's filesystem.

**Example `compose.yaml`:**

```yaml
services:
  ci-runner:
    image: gitlab/gitlab-runner:latest
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
```

### 2.2 Docker-in-Docker (DinD)

DinD runs a completely separate, isolated Docker daemon *inside* the container.

**Pros:**
*   Better isolation. The inner Docker daemon cannot affect the host's Docker daemon.

**Cons:**
*   Requires the container to run in `--privileged` mode, which itself is a security risk (though arguably less than exposing the host socket, depending on the environment).
*   Does not share the host's image cache, leading to slower builds unless caching is explicitly configured.
*   Can have issues with storage drivers (e.g., running overlay2 inside overlay2).

**Example `compose.yaml`:**

```yaml
services:
  dind-daemon:
    image: docker:dind
    privileged: true
    environment:
      - DOCKER_TLS_CERTDIR=/certs
    volumes:
      - dind-certs:/certs/client
      - dind-data:/var/lib/docker

  ci-runner:
    image: docker:cli
    environment:
      - DOCKER_HOST=tcp://dind-daemon:2376
      - DOCKER_TLS_VERIFY=1
      - DOCKER_CERT_PATH=/certs/client
    volumes:
      - dind-certs:/certs/client:ro
    depends_on:
      - dind-daemon

volumes:
  dind-certs:
  dind-data:
```

### 2.3 Best Practices for CI/CD

*   **Avoid Socket Mounting if possible:** Due to the security implications, avoid mounting `/var/run/docker.sock` in multi-tenant or untrusted environments.
*   **Use Rootless DinD:** Docker now supports running the daemon without root privileges. This significantly mitigates the risks of DinD. Use the `docker:dind-rootless` image.
*   **Consider Alternatives:** Tools like Kaniko, Buildah, or Makisu can build container images without requiring a Docker daemon at all, making them ideal for Kubernetes and secure CI/CD environments.

---

## 3. Advanced Compose Patterns

Docker Compose is powerful, but managing complex applications requires advanced patterns to keep configurations DRY (Don't Repeat Yourself) and maintainable across different environments.

### 3.1 Override Files (`compose.override.yaml`)

By default, Docker Compose reads `compose.yaml` and then `compose.override.yaml`. The override file is applied on top of the base file, merging or replacing values.

**`compose.yaml` (Base):**

```yaml
services:
  web:
    image: YOUR_REGISTRY/webapp:latest
    ports:
      - "80:80"
```

**`compose.override.yaml` (Local Development):**

```yaml
services:
  web:
    build: .
    volumes:
      - .:/app
    environment:
      - DEBUG=true
```

When you run `docker compose up`, it automatically merges these. For production, you would ignore the override file: `docker compose -f compose.yaml up -d`.

### 3.2 Environment-Specific Configs

Instead of relying solely on the default override file, explicitly define environment files.

*   `compose.yaml` (Base configuration)
*   `compose.dev.yaml` (Development overrides)
*   `compose.prod.yaml` (Production overrides)

**Running in Development:**
```bash
docker compose -f compose.yaml -f compose.dev.yaml up -d
```

**Running in Production:**
```bash
docker compose -f compose.yaml -f compose.prod.yaml up -d
```

### 3.3 YAML Anchors and Merge Keys

YAML anchors (`&`) and aliases (`*`) allow you to define a block of configuration once and reuse it. Merge keys (`<<`) allow you to insert the contents of an alias into a mapping.

```yaml
x-logging-config: &default-logging
  driver: "json-file"
  options:
    max-size: "10m"
    max-file: "3"

services:
  web:
    image: nginx:alpine
    logging: *default-logging

  db:
    image: postgres:15
    logging: *default-logging
```

### 3.4 Extension Fields (`x-`)

Compose allows you to define custom extension fields starting with `x-`. These are ignored by Compose but can be used with YAML anchors to share configuration.

```yaml
x-common-env: &common-env
  ENVIRONMENT: production
  LOG_LEVEL: info

services:
  api:
    image: myapi
    environment:
      <<: *common-env
      API_KEY: secret

  worker:
    image: myworker
    environment:
      <<: *common-env
      QUEUE_NAME: tasks
```

### 3.5 The `include` Directive

For very large projects, you can split your Compose configuration into multiple files and include them. This is better than `extends` for modularizing entire stacks.

```yaml
# compose.yaml
include:
  - database/compose.yaml
  - monitoring/compose.yaml

services:
  app:
    image: myapp
    depends_on:
      - db
      - prometheus
```

### 3.6 Extending Services (`extends`)

The `extends` keyword allows you to share common configurations among different services, even across different files.

**`common.yaml`:**
```yaml
services:
  base-app:
    image: myapp-base
    environment:
      - SHARED_VAR=true
```

**`compose.yaml`:**
```yaml
services:
  web:
    extends:
      file: common.yaml
      service: base-app
    ports:
      - "8080:80"

  worker:
    extends:
      file: common.yaml
      service: base-app
    command: ["worker-start"]
```

---

## 4. Docker Swarm Mode

Docker Swarm provides native clustering and orchestration. While Kubernetes is more prevalent, Swarm is simpler to set up and manage for smaller deployments.

### 4.1 Service Creation and Management

In Swarm, you deploy *services* rather than individual containers.

```bash
# Initialize Swarm
docker swarm init

# Create a service
docker service create --name web --replicas 3 -p 80:80 nginx:alpine

# Scale a service
docker service scale web=5
```

### 4.2 Rolling Updates and Rollbacks

Swarm handles rolling updates automatically, ensuring zero downtime.

**Updating a service:**
```bash
docker service update --image nginx:latest --update-parallelism 2 --update-delay 10s web
```

**Rolling back:**
If an update fails, you can roll back to the previous configuration.
```bash
docker service update --rollback web
```

**Compose `deploy` configuration for updates:**

```yaml
services:
  web:
    image: nginx:alpine
    deploy:
      replicas: 3
      update_config:
        parallelism: 1
        delay: 10s
        failure_action: rollback
        monitor: 15s
        max_failure_ratio: 0.1
      rollback_config:
        parallelism: 1
        delay: 10s
```

### 4.3 Placement Constraints

You can control which nodes a service runs on using placement constraints.

```yaml
services:
  db:
    image: postgres:15
    deploy:
      placement:
        constraints:
          - node.role == manager
          - node.labels.ssd == true
```

### 4.4 Secrets and Configs

Swarm provides secure management of secrets (passwords, certificates) and configs (configuration files).

**Creating a secret:**
```bash
echo "my-super-secret-password" | docker secret create db_password -
```

**Using a secret in Compose:**

```yaml
services:
  db:
    image: postgres:15
    environment:
      POSTGRES_PASSWORD_FILE: /run/secrets/db_password
    secrets:
      - db_password

secrets:
  db_password:
    external: true
```

### 4.5 Overlay Networking

Overlay networks allow containers on different Swarm nodes to communicate securely.

```bash
docker network create -d overlay my-overlay-network
```

```yaml
services:
  web:
    image: nginx
    networks:
      - my-overlay-network

networks:
  my-overlay-network:
    external: true
```

---

## 5. GPU Passthrough

For machine learning and data science workloads, passing GPU access to containers is critical.

### 5.1 NVIDIA Container Toolkit

You must install the NVIDIA Container Toolkit on the host machine. This allows Docker to interface with the NVIDIA drivers.

### 5.2 Device Reservations in Compose

Use the `deploy.resources.reservations.devices` configuration to request GPU access.

```yaml
services:
  ml-worker:
    image: tensorflow/tensorflow:latest-gpu
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1 # Or 'all'
              capabilities: [gpu]
```

**Troubleshooting:**
*   **Error:** `could not select device driver "" with capabilities: [[gpu]]`
*   **Solution:** The NVIDIA Container Toolkit is not installed or configured correctly on the host. Ensure the Docker daemon is configured to use the `nvidia` runtime.

---

## 6. Custom Entrypoint Scripts

A robust entrypoint script is essential for preparing the container environment before the main application starts.

### 6.1 The `wait-for-it` Pattern

Often, a service depends on another service being ready (e.g., a web app waiting for a database). While `depends_on` handles startup order, it doesn't guarantee readiness.

Use tools like `wait-for-it.sh` or `dockerize` in your entrypoint.

**`entrypoint.sh`:**

```bash
#!/bin/bash
set -e

# Wait for the database to be ready
/usr/local/bin/wait-for-it.sh db:5432 -t 60 -- echo "Database is up"

# Run database migrations
echo "Running migrations..."
./manage.py migrate

# Execute the main command
exec "$@"
```

### 6.2 Proper Signal Handling and Graceful Shutdown

When Docker stops a container, it sends a `SIGTERM` signal. If the application doesn't handle it, Docker waits for the `stop_grace_period` (default 10s) and then sends a `SIGKILL`, forcefully terminating the process.

**Using `exec`:**
In your entrypoint script, always use `exec "$@"` to run the main command. This replaces the shell process with the application process, ensuring it receives the `SIGTERM` signal directly.

**Handling signals in the application (Python example):**

```python
import signal
import sys
import time

def signal_handler(sig, frame):
    print('Gracefully shutting down...')
    # Perform cleanup (close DB connections, finish requests)
    sys.exit(0)

signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)

print('Application started')
while True:
    time.sleep(1)
```

**Compose Configuration:**

```yaml
services:
  app:
    image: myapp
    stop_grace_period: 30s # Give the app more time to shut down
    stop_signal: SIGINT # Change the signal if needed
```

---

## 7. Init Containers Pattern in Compose

Sometimes you need to run a task *before* a service starts, such as initializing a database schema or downloading assets.

Compose V2 supports this using `depends_on` with the `service_completed_successfully` condition.

```yaml
services:
  db:
    image: postgres:15
    environment:
      POSTGRES_PASSWORD: secret

  db-init:
    image: my-db-init-script
    depends_on:
      db:
        condition: service_started
    environment:
      DB_HOST: db
      DB_PASSWORD: secret

  web:
    image: my-web-app
    depends_on:
      db-init:
        condition: service_completed_successfully
```

In this setup, `web` will not start until `db-init` has run and exited with a status code of 0.

---

## 8. Sidecar Pattern

The sidecar pattern involves running a secondary container alongside the main application container within the same logical unit (e.g., a Kubernetes Pod or a Compose project sharing a network namespace).

### 8.1 Log Collectors

A common use case is a sidecar that reads logs from a shared volume and forwards them to a central logging system (e.g., Fluentd, Logstash).

```yaml
services:
  app:
    image: myapp
    volumes:
      - app-logs:/var/log/app

  log-forwarder:
    image: fluent/fluentd
    volumes:
      - app-logs:/var/log/app:ro
    # Configuration to read from /var/log/app and forward

volumes:
  app-logs:
```

### 8.2 Proxies (e.g., Envoy, Nginx)

A sidecar proxy can handle TLS termination, rate limiting, or routing, offloading these concerns from the main application.

```yaml
services:
  app:
    image: myapp
    # App listens on port 8080 internally

  proxy:
    image: envoyproxy/envoy
    ports:
      - "443:443"
    depends_on:
      - app
    # Envoy config routes traffic to app:8080
```

---

## 9. Blue-Green and Canary Deployments with Compose

While Swarm and Kubernetes have built-in support for advanced deployment strategies, you can simulate them with Docker Compose and a reverse proxy (like Nginx, Traefik, or HAProxy).

### 9.1 Blue-Green Deployment

1.  **Blue Environment:** Currently running version (e.g., `app-blue`).
2.  **Green Environment:** New version deployed alongside Blue (e.g., `app-green`).
3.  **Switch:** Update the reverse proxy configuration to route traffic from Blue to Green.

**`compose.yaml`:**

```yaml
services:
  proxy:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro

  app-blue:
    image: myapp:v1
    # ...

  app-green:
    image: myapp:v2
    # ...
```

You would dynamically update `nginx.conf` and reload Nginx (`docker compose exec proxy nginx -s reload`) to switch traffic.

### 9.2 Canary Deployment

Similar to Blue-Green, but the proxy routes only a small percentage of traffic to the new version (the canary) to test it before a full rollout. Traefik is excellent for this as it supports weighted routing natively.

---

## 10. Docker Compose Watch and Develop

For local development, rebuilding images for every code change is slow. Docker Compose provides features for hot-reloading.

### 10.1 Compose Watch

`watch` automatically updates running services as you edit and save code.

```yaml
services:
  web:
    build: .
    command: npm run dev
    develop:
      watch:
        - action: sync
          path: ./src
          target: /app/src
          ignore:
            - node_modules/
        - action: rebuild
          path: package.json
```

*   `sync`: Copies changed files into the container (ideal for interpreted languages or hot-reloading frameworks).
*   `rebuild`: Rebuilds the image and recreates the container (necessary when dependencies change).

Run it with: `docker compose watch`

---

## 11. Registry Management

Managing where your images are stored and how they are pulled is crucial for performance and security.

### 11.1 Private Registry

Running your own registry ensures your images remain private and can speed up deployments within your network.

```yaml
services:
  registry:
    image: registry:2
    ports:
      - "5000:5000"
    environment:
      REGISTRY_STORAGE_FILESYSTEM_ROOTDIRECTORY: /data
    volumes:
      - registry-data:/data
```

### 11.2 Mirror / Pull-Through Cache

To avoid hitting Docker Hub rate limits and speed up image pulls across your infrastructure, set up a pull-through cache.

```yaml
services:
  registry-mirror:
    image: registry:2
    ports:
      - "5000:5000"
    environment:
      REGISTRY_PROXY_REMOTEURL: https://registry-1.docker.io
```

Configure your Docker daemons (`/etc/docker/daemon.json`) to use this mirror:

```json
{
  "registry-mirrors": ["http://your-mirror-ip:5000"]
}
```

### 11.3 Garbage Collection

Registries consume disk space over time. You must periodically run garbage collection to remove unreferenced layers.

```bash
# Run garbage collection on the registry container
docker exec -it registry bin/registry garbage-collect /etc/docker/registry/config.yml
```

---

## 12. Docker Contexts

Docker Contexts allow you to manage multiple Docker environments (local, remote servers, Swarm clusters) from a single CLI.

### 12.1 Managing Contexts

```bash
# List contexts
docker context ls

# Create a context for a remote server via SSH
docker context create production --docker "host=ssh://user@production-server.com"

# Switch to the production context
docker context use production

# Now all docker commands run against the production server
docker ps
```

This is much safer and more convenient than manually setting the `DOCKER_HOST` environment variable.

---

## 13. Buildx Bake

`docker buildx bake` is a high-level build command that allows you to define complex build pipelines declaratively using HCL, JSON, or Compose files.

### 13.1 Declarative Build Definitions (HCL)

Create a `docker-bake.hcl` file:

```hcl
group "default" {
  targets = ["webapp", "api"]
}

target "webapp" {
  context = "./frontend"
  dockerfile = "Dockerfile"
  tags = ["YOUR_REGISTRY/webapp:latest"]
  platforms = ["linux/amd64", "linux/arm64"]
}

target "api" {
  context = "./backend"
  dockerfile = "Dockerfile"
  tags = ["YOUR_REGISTRY/api:latest"]
  args = {
    GO_VERSION = "1.21"
  }
}
```

Run the build: `docker buildx bake`

### 13.2 Matrix Builds

Bake supports matrix builds, allowing you to build multiple variants of an image easily.

```hcl
target "app" {
  matrix = {
    NODE_VERSION = ["18", "20"]
    OS = ["alpine", "bullseye"]
  }
  name = "app-${NODE_VERSION}-${OS}"
  context = "."
  args = {
    NODE_VERSION = NODE_VERSION
    OS = OS
  }
  tags = ["YOUR_REGISTRY/app:${NODE_VERSION}-${OS}"]
}
```

---

## 14. Docker Scout

Security is paramount. Docker Scout provides vulnerability scanning and policy evaluation for your images.

### 14.1 Vulnerability Scanning

Scan an image for known vulnerabilities (CVEs):

```bash
docker scout cves YOUR_REGISTRY/YOUR_IMAGE:latest
```

### 14.2 SBOM Generation

Generate a Software Bill of Materials (SBOM) to understand exactly what components are in your image.

```bash
docker scout sbom YOUR_REGISTRY/YOUR_IMAGE:latest
```

### 14.3 Policy Evaluation

Evaluate an image against predefined security policies (e.g., ensuring no critical vulnerabilities exist).

```bash
docker scout policy YOUR_REGISTRY/YOUR_IMAGE:latest
```

---

## 15. Comprehensive Troubleshooting Guide

As a Super Specialist, you will encounter complex issues. Here is a structured approach to troubleshooting.

### 15.1 Container Fails to Start or Exits Immediately

1.  **Check Logs:** `docker compose logs <service_name>`
2.  **Inspect Container:** `docker inspect <container_id>` (Look at `State.ExitCode` and `State.Error`).
3.  **Override Entrypoint:** Run the container interactively to debug the environment.
    ```bash
    docker compose run --entrypoint /bin/sh <service_name>
    ```
4.  **Check `depends_on`:** Ensure required services are actually healthy, not just started.

### 15.2 Networking Issues

1.  **Verify Networks:** `docker network ls` and `docker network inspect <network_name>`.
2.  **Test Connectivity:** Use a temporary container on the same network to test DNS and connectivity.
    ```bash
    docker run --rm --network <project>_default curlimages/curl -v http://<service_name>:<port>
    ```
3.  **Check Port Conflicts:** `lsof -i :<port>` on the host.

### 15.3 Storage and Permission Issues

1.  **Check Volume Mounts:** Ensure host paths exist and have correct permissions.
2.  **SELinux/AppArmor:** If using SELinux, append `:z` or `:Z` to volume mounts to handle labeling.
    ```yaml
    volumes:
      - ./data:/app/data:z
    ```
3.  **User ID Mismatch:** If the container runs as a non-root user, ensure the mounted volume is owned by that user's UID.

### 15.4 Performance and Resource Constraints

1.  **Monitor Usage:** `docker stats`
2.  **Check Limits:** Ensure `deploy.resources.limits` are not set too low, causing OOM (Out of Memory) kills or CPU throttling.
3.  **Inspect Docker Daemon Logs:** `journalctl -u docker.service` (on systemd systems) for daemon-level errors.

---

## Conclusion

Mastering Docker requires a deep understanding of its architecture, networking, storage, and security models. By applying the advanced patterns and troubleshooting techniques outlined in this guide, you can build, deploy, and maintain robust, scalable, and secure containerized applications. Always prioritize security (least privilege, scanning), optimize for performance (multi-stage builds, caching), and design for maintainability (modular Compose files, declarative builds).

## Deep Dive: Advanced Docker Networking Architectures

Understanding Docker networking beyond the basic bridge network is crucial for enterprise deployments.

### Macvlan Networks

Macvlan networks allow you to assign a MAC address to a container, making it appear as a physical device on your network. This is useful for legacy applications that expect to be directly connected to the physical network, rather than routed through the Docker host's network stack.

**Configuration:**

```bash
docker network create -d macvlan   --subnet=192.168.1.0/24   --gateway=192.168.1.1   -o parent=eth0 pub_net
```

**Important Considerations:**
*   **Host Isolation:** By design, the Docker host cannot communicate with containers on a macvlan network. If you need host-to-container communication, you must create a secondary macvlan interface on the host.
*   **Promiscuous Mode:** The physical interface (`eth0` in the example) must often be put into promiscuous mode, which may not be supported in all environments (e.g., some cloud providers).

### IPvlan Networks

IPvlan is similar to Macvlan but shares the MAC address of the parent interface. This solves the promiscuous mode issue and is generally preferred over Macvlan in modern deployments.

It operates in two modes:
*   **L2 Mode:** Similar to Macvlan, containers get IP addresses from the physical network subnet.
*   **L3 Mode:** The Docker host acts as a router. Containers are on a different subnet, and the host routes traffic to them.

### Custom Bridge Networks and DNS

When you create a custom bridge network (which Compose does by default), Docker provides an embedded DNS server. This allows containers to resolve each other by service name or container name.

**Troubleshooting DNS:**
If containers cannot resolve each other:
1.  Ensure they are on the same custom network. The default `bridge` network (named `bridge`) does *not* provide automatic DNS resolution.
2.  Check the `/etc/resolv.conf` inside the container. It should point to Docker's embedded DNS server (usually `127.0.0.11`).


## Deep Dive: Storage Drivers and Performance

The choice of storage driver significantly impacts container performance, especially for write-heavy workloads.

### Overlay2

`overlay2` is the recommended storage driver for all supported Linux distributions. It operates at the file level rather than the block level.

**How it works:**
It uses a union mount to combine a lower directory (the read-only image layers) and an upper directory (the read-write container layer) into a merged view.

**Performance Characteristics:**
*   **Page Cache Sharing:** Multiple containers using the same image share the page cache, reducing memory usage.
*   **Copy-on-Write (CoW):** When a container modifies a file from the image, the file is copied to the upper directory. This CoW operation can incur a performance penalty on the first write.

### Optimizing Storage Performance

1.  **Use Volumes for Write-Heavy Data:** Never write databases, logs, or high-throughput data to the container's writable layer. Always use Docker volumes or bind mounts. Volumes bypass the storage driver and write directly to the host filesystem, offering native performance.
2.  **Avoid Deep Directory Structures:** The CoW operation in `overlay2` can be slow if it has to traverse deep directory structures.
3.  **Monitor Disk Space:** The writable layer can grow indefinitely if not managed. Use `docker system prune` regularly.


## Deep Dive: Security Hardening in Production

Security is not an afterthought; it must be integrated into every layer of the container lifecycle.

### Seccomp Profiles

Secure Computing Mode (seccomp) is a Linux kernel feature that restricts the system calls a process can make. Docker uses a default seccomp profile that blocks many potentially dangerous syscalls.

**Custom Profiles:**
For highly secure environments, you can create custom seccomp profiles tailored to your application's specific needs, blocking everything except what is strictly required.

```yaml
services:
  secure-app:
    image: myapp
    security_opt:
      - seccomp=/path/to/custom-profile.json
```

### AppArmor and SELinux

These are Mandatory Access Control (MAC) systems that provide fine-grained control over what resources a process can access.

*   **AppArmor:** Used primarily on Debian/Ubuntu systems. Docker automatically applies a default AppArmor profile (`docker-default`).
*   **SELinux:** Used primarily on RHEL/CentOS/Fedora systems.

**Troubleshooting SELinux:**
If a container cannot access a bind-mounted volume on an SELinux-enabled system, it's usually a labeling issue. Use the `:z` (shared) or `:Z` (private) suffix on the volume mount to instruct Docker to relabel the directory.

### Rootless Docker

Running the Docker daemon as a non-root user is one of the most significant security improvements you can make. It mitigates the risk of container breakout vulnerabilities leading to host compromise.

**Setup:**
Rootless Docker requires specific configuration (e.g., `newuidmap`, `newgidmap`) and has some limitations (e.g., cannot bind to privileged ports < 1024 without configuration), but the security benefits are substantial.


## Deep Dive: Advanced Dockerfile Optimization

Writing efficient Dockerfiles is an art. Every instruction creates a layer, and optimizing these layers is key to fast builds and small images.

### The Power of Multi-Stage Builds

Multi-stage builds allow you to use multiple `FROM` statements in a single Dockerfile. You can copy artifacts from one stage to another, leaving behind all the build dependencies.

**Example: Node.js Application**

```dockerfile
# Stage 1: Build
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
# Use npm ci for reproducible builds
RUN npm ci
COPY . .
RUN npm run build

# Stage 2: Production
FROM node:18-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
COPY package*.json ./
# Install only production dependencies
RUN npm ci --only=production
# Copy built assets from the builder stage
COPY --from=builder /app/dist ./dist
USER node
CMD ["node", "dist/main.js"]
```

### Cache Invalidation Strategy

Docker caches layers to speed up builds. A layer is invalidated if the instruction changes or if the files copied by a `COPY` or `ADD` instruction change. Once a layer is invalidated, all subsequent layers are also invalidated.

**Best Practice:** Order instructions from least likely to change to most likely to change.

1.  Base Image (`FROM`)
2.  System Dependencies (`RUN apt-get...`)
3.  Application Dependencies (`COPY package.json`, `RUN npm install`)
4.  Application Code (`COPY . .`)

By copying `package.json` and installing dependencies *before* copying the rest of the source code, you ensure that the dependency installation layer is cached unless the dependencies themselves change.


## Deep Dive: Managing Docker at Scale

When managing hundreds or thousands of containers, manual operations become impossible.

### Centralized Logging

Never rely on `docker logs` for production systems. Implement a centralized logging architecture.

1.  **Configure the Docker Daemon:** Set the default logging driver to forward logs to a central system (e.g., `syslog`, `fluentd`, `splunk`).
2.  **Use Sidecars:** As discussed earlier, use sidecar containers to collect and forward logs.
3.  **Structured Logging:** Ensure your applications output logs in a structured format (like JSON) to make querying and analysis easier.

### Monitoring and Alerting

You must monitor both the Docker host and the containers.

*   **Host Metrics:** CPU, memory, disk I/O, network traffic.
*   **Container Metrics:** CPU usage, memory consumption, restart counts.
*   **Tools:** Prometheus and Grafana are the industry standard for container monitoring. Use cAdvisor (Container Advisor) to expose container metrics to Prometheus.

### Infrastructure as Code (IaC)

Manage your Docker infrastructure using IaC tools like Terraform or Ansible. This ensures consistency, repeatability, and version control for your infrastructure.


## Comprehensive Reference: Docker Compose Specification

This section provides an exhaustive reference of the Docker Compose specification, detailing every attribute and its usage.

### Service Top-Level Element

The `services` element is the core of a Compose file. It defines the containers that make up your application.

#### `build`
Configuration options that are applied at build time.

*   `context`: Either a path to a directory containing a Dockerfile, or a url to a git repository.
*   `dockerfile`: Alternate Dockerfile.
*   `args`: Add build arguments, which are environment variables accessible only during the build process.
*   `ssh`: SSH authentications that the builder should use.
*   `cache_from`: A list of images that the builder should use for cache resolution.
*   `cache_to`: A list of export locations to be used to share build cache with future builds.
*   `target`: Build the specified stage as defined inside the Dockerfile.
*   `secrets`: Grant access to sensitive data defined by secrets on a per-service basis.
*   `tags`: A list of tag names to be applied to the built image.
*   `platforms`: A list of target platforms.

#### `image`
Specifies the image to start the container from. Can either be a repository/tag or a partial image ID.

#### `command`
Overrides the default command declared by the container image (i.e., by Dockerfile's `CMD`).

#### `entrypoint`
Overrides the default entrypoint declared by the container image (i.e., by Dockerfile's `ENTRYPOINT`).

#### `environment`
Adds environment variables. You can use either an array or a dictionary.

#### `env_file`
Adds environment variables from a file.

#### `depends_on`
Expresses dependency between services.

*   `condition`:
    *   `service_started`: (default) The dependency must be started before the dependent service.
    *   `service_healthy`: The dependency must be "healthy" before the dependent service starts.
    *   `service_completed_successfully`: The dependency must run to completion and exit with a 0 status code.
*   `restart`: When set to true, Compose restarts this service after it updates the dependency service.

#### `deploy`
Specifies configuration related to the deployment and running of services. This only takes effect when deploying to a swarm with `docker stack deploy`, and is ignored by `docker compose up` and `docker compose run`.

*   `endpoint_mode`: Valid values are `vip` and `dnsrr`.
*   `labels`: Specify labels for the service.
*   `mode`: Either `global` (exactly one container per swarm node) or `replicated` (a specified number of containers).
*   `placement`: Specify placement constraints and preferences.
*   `replicas`: If the service is `replicated` (which is the default), specify the number of containers that should be running at any given time.
*   `resources`: Configure resource limits and reservations.
    *   `limits`: The platform must prevent the container to allocate more.
    *   `reservations`: The platform must guarantee the container can allocate at least the configured amount.
*   `restart_policy`: Configures if and how to restart containers when they exit.
*   `rollback_config`: Configures how the service should be rolled back in case of a failing update.
*   `update_config`: Configures how the service should be updated. Useful for configuring rolling updates.

#### `healthcheck`
Configures a check that's run to determine whether or not containers for this service are "healthy".

*   `test`: The command to run to check health.
*   `interval`: The time to wait between checks.
*   `timeout`: The time to wait before considering the check to have hung.
*   `retries`: The number of consecutive failures needed to consider a container as unhealthy.
*   `start_period`: Initialization time for containers that need time to bootstrap.
*   `disable`: Disable any default healthcheck set by the image.

#### `logging`
Logging configuration for the service.

*   `driver`: The logging driver to use (e.g., `json-file`, `syslog`, `journald`).
*   `options`: Driver-specific options (e.g., `max-size`, `max-file`).

#### `networks`
Networks to join, referencing entries under the top-level `networks` key.

#### `ports`
Expose ports.

*   Short syntax: `HOST:CONTAINER` or just `CONTAINER` (host port is chosen randomly).
*   Long syntax: Allows configuring the `target` port, `published` port, `protocol` (tcp or udp), and `mode` (host or ingress).

#### `volumes`
Mount host paths or named volumes, specified as sub-options to a service.

*   Short syntax: `VOLUME:CONTAINER_PATH:ACCESS_MODE`
*   Long syntax: Allows configuring `type` (volume, bind, tmpfs), `source`, `target`, `read_only`, and `bind` or `volume` specific options.

#### `secrets`
Grant access to secrets on a per-service basis using the per-service `secrets` configuration.

#### `configs`
Grant access to configs on a per-service basis using the per-service `configs` configuration.

#### `profiles`
Allow defining a list of named profiles for the service to be enabled under. When not set, the service is always enabled.

#### `restart`
Defines the restart policy for the service.

*   `no`: The default restart policy. Does not restart the container under any circumstance.
*   `always`: The policy always restarts the container until its removal.
*   `on-failure`: The policy restarts the container if the exit code indicates an on-failure error.
*   `unless-stopped`: The policy always restarts the container regardless of the exit code, but will stop restarting when the service is stopped or removed.

#### `stop_grace_period`
Specifies how long to wait when attempting to stop a container if it doesn't handle SIGTERM (or whatever stop signal has been specified with `stop_signal`), before sending SIGKILL.

#### `stop_signal`
Sets an alternative signal to stop the container. By default `stop` uses SIGTERM.

#### `sysctls`
Kernel parameters to set in the container.

#### `ulimits`
Override the default ulimits for a container.

#### `user`
Override the user used to run the container process.

#### `working_dir`
Override the container's working directory from that specified by the image.


## Comprehensive Reference: Docker Compose Specification

This section provides an exhaustive reference of the Docker Compose specification, detailing every attribute and its usage.

### Service Top-Level Element

The `services` element is the core of a Compose file. It defines the containers that make up your application.

#### `build`
Configuration options that are applied at build time.

*   `context`: Either a path to a directory containing a Dockerfile, or a url to a git repository.
*   `dockerfile`: Alternate Dockerfile.
*   `args`: Add build arguments, which are environment variables accessible only during the build process.
*   `ssh`: SSH authentications that the builder should use.
*   `cache_from`: A list of images that the builder should use for cache resolution.
*   `cache_to`: A list of export locations to be used to share build cache with future builds.
*   `target`: Build the specified stage as defined inside the Dockerfile.
*   `secrets`: Grant access to sensitive data defined by secrets on a per-service basis.
*   `tags`: A list of tag names to be applied to the built image.
*   `platforms`: A list of target platforms.

#### `image`
Specifies the image to start the container from. Can either be a repository/tag or a partial image ID.

#### `command`
Overrides the default command declared by the container image (i.e., by Dockerfile's `CMD`).

#### `entrypoint`
Overrides the default entrypoint declared by the container image (i.e., by Dockerfile's `ENTRYPOINT`).

#### `environment`
Adds environment variables. You can use either an array or a dictionary.

#### `env_file`
Adds environment variables from a file.

#### `depends_on`
Expresses dependency between services.

*   `condition`:
    *   `service_started`: (default) The dependency must be started before the dependent service.
    *   `service_healthy`: The dependency must be "healthy" before the dependent service starts.
    *   `service_completed_successfully`: The dependency must run to completion and exit with a 0 status code.
*   `restart`: When set to true, Compose restarts this service after it updates the dependency service.

#### `deploy`
Specifies configuration related to the deployment and running of services. This only takes effect when deploying to a swarm with `docker stack deploy`, and is ignored by `docker compose up` and `docker compose run`.

*   `endpoint_mode`: Valid values are `vip` and `dnsrr`.
*   `labels`: Specify labels for the service.
*   `mode`: Either `global` (exactly one container per swarm node) or `replicated` (a specified number of containers).
*   `placement`: Specify placement constraints and preferences.
*   `replicas`: If the service is `replicated` (which is the default), specify the number of containers that should be running at any given time.
*   `resources`: Configure resource limits and reservations.
    *   `limits`: The platform must prevent the container to allocate more.
    *   `reservations`: The platform must guarantee the container can allocate at least the configured amount.
*   `restart_policy`: Configures if and how to restart containers when they exit.
*   `rollback_config`: Configures how the service should be rolled back in case of a failing update.
*   `update_config`: Configures how the service should be updated. Useful for configuring rolling updates.

#### `healthcheck`
Configures a check that's run to determine whether or not containers for this service are "healthy".

*   `test`: The command to run to check health.
*   `interval`: The time to wait between checks.
*   `timeout`: The time to wait before considering the check to have hung.
*   `retries`: The number of consecutive failures needed to consider a container as unhealthy.
*   `start_period`: Initialization time for containers that need time to bootstrap.
*   `disable`: Disable any default healthcheck set by the image.

#### `logging`
Logging configuration for the service.

*   `driver`: The logging driver to use (e.g., `json-file`, `syslog`, `journald`).
*   `options`: Driver-specific options (e.g., `max-size`, `max-file`).

#### `networks`
Networks to join, referencing entries under the top-level `networks` key.

#### `ports`
Expose ports.

*   Short syntax: `HOST:CONTAINER` or just `CONTAINER` (host port is chosen randomly).
*   Long syntax: Allows configuring the `target` port, `published` port, `protocol` (tcp or udp), and `mode` (host or ingress).

#### `volumes`
Mount host paths or named volumes, specified as sub-options to a service.

*   Short syntax: `VOLUME:CONTAINER_PATH:ACCESS_MODE`
*   Long syntax: Allows configuring `type` (volume, bind, tmpfs), `source`, `target`, `read_only`, and `bind` or `volume` specific options.

#### `secrets`
Grant access to secrets on a per-service basis using the per-service `secrets` configuration.

#### `configs`
Grant access to configs on a per-service basis using the per-service `configs` configuration.

#### `profiles`
Allow defining a list of named profiles for the service to be enabled under. When not set, the service is always enabled.

#### `restart`
Defines the restart policy for the service.

*   `no`: The default restart policy. Does not restart the container under any circumstance.
*   `always`: The policy always restarts the container until its removal.
*   `on-failure`: The policy restarts the container if the exit code indicates an on-failure error.
*   `unless-stopped`: The policy always restarts the container regardless of the exit code, but will stop restarting when the service is stopped or removed.

#### `stop_grace_period`
Specifies how long to wait when attempting to stop a container if it doesn't handle SIGTERM (or whatever stop signal has been specified with `stop_signal`), before sending SIGKILL.

#### `stop_signal`
Sets an alternative signal to stop the container. By default `stop` uses SIGTERM.

#### `sysctls`
Kernel parameters to set in the container.

#### `ulimits`
Override the default ulimits for a container.

#### `user`
Override the user used to run the container process.

#### `working_dir`
Override the container's working directory from that specified by the image.


## Comprehensive Reference: Docker Compose Specification

This section provides an exhaustive reference of the Docker Compose specification, detailing every attribute and its usage.

### Service Top-Level Element

The `services` element is the core of a Compose file. It defines the containers that make up your application.

#### `build`
Configuration options that are applied at build time.

*   `context`: Either a path to a directory containing a Dockerfile, or a url to a git repository.
*   `dockerfile`: Alternate Dockerfile.
*   `args`: Add build arguments, which are environment variables accessible only during the build process.
*   `ssh`: SSH authentications that the builder should use.
*   `cache_from`: A list of images that the builder should use for cache resolution.
*   `cache_to`: A list of export locations to be used to share build cache with future builds.
*   `target`: Build the specified stage as defined inside the Dockerfile.
*   `secrets`: Grant access to sensitive data defined by secrets on a per-service basis.
*   `tags`: A list of tag names to be applied to the built image.
*   `platforms`: A list of target platforms.

#### `image`
Specifies the image to start the container from. Can either be a repository/tag or a partial image ID.

#### `command`
Overrides the default command declared by the container image (i.e., by Dockerfile's `CMD`).

#### `entrypoint`
Overrides the default entrypoint declared by the container image (i.e., by Dockerfile's `ENTRYPOINT`).

#### `environment`
Adds environment variables. You can use either an array or a dictionary.

#### `env_file`
Adds environment variables from a file.

#### `depends_on`
Expresses dependency between services.

*   `condition`:
    *   `service_started`: (default) The dependency must be started before the dependent service.
    *   `service_healthy`: The dependency must be "healthy" before the dependent service starts.
    *   `service_completed_successfully`: The dependency must run to completion and exit with a 0 status code.
*   `restart`: When set to true, Compose restarts this service after it updates the dependency service.

#### `deploy`
Specifies configuration related to the deployment and running of services. This only takes effect when deploying to a swarm with `docker stack deploy`, and is ignored by `docker compose up` and `docker compose run`.

*   `endpoint_mode`: Valid values are `vip` and `dnsrr`.
*   `labels`: Specify labels for the service.
*   `mode`: Either `global` (exactly one container per swarm node) or `replicated` (a specified number of containers).
*   `placement`: Specify placement constraints and preferences.
*   `replicas`: If the service is `replicated` (which is the default), specify the number of containers that should be running at any given time.
*   `resources`: Configure resource limits and reservations.
    *   `limits`: The platform must prevent the container to allocate more.
    *   `reservations`: The platform must guarantee the container can allocate at least the configured amount.
*   `restart_policy`: Configures if and how to restart containers when they exit.
*   `rollback_config`: Configures how the service should be rolled back in case of a failing update.
*   `update_config`: Configures how the service should be updated. Useful for configuring rolling updates.

#### `healthcheck`
Configures a check that's run to determine whether or not containers for this service are "healthy".

*   `test`: The command to run to check health.
*   `interval`: The time to wait between checks.
*   `timeout`: The time to wait before considering the check to have hung.
*   `retries`: The number of consecutive failures needed to consider a container as unhealthy.
*   `start_period`: Initialization time for containers that need time to bootstrap.
*   `disable`: Disable any default healthcheck set by the image.

#### `logging`
Logging configuration for the service.

*   `driver`: The logging driver to use (e.g., `json-file`, `syslog`, `journald`).
*   `options`: Driver-specific options (e.g., `max-size`, `max-file`).

#### `networks`
Networks to join, referencing entries under the top-level `networks` key.

#### `ports`
Expose ports.

*   Short syntax: `HOST:CONTAINER` or just `CONTAINER` (host port is chosen randomly).
*   Long syntax: Allows configuring the `target` port, `published` port, `protocol` (tcp or udp), and `mode` (host or ingress).

#### `volumes`
Mount host paths or named volumes, specified as sub-options to a service.

*   Short syntax: `VOLUME:CONTAINER_PATH:ACCESS_MODE`
*   Long syntax: Allows configuring `type` (volume, bind, tmpfs), `source`, `target`, `read_only`, and `bind` or `volume` specific options.

#### `secrets`
Grant access to secrets on a per-service basis using the per-service `secrets` configuration.

#### `configs`
Grant access to configs on a per-service basis using the per-service `configs` configuration.

#### `profiles`
Allow defining a list of named profiles for the service to be enabled under. When not set, the service is always enabled.

#### `restart`
Defines the restart policy for the service.

*   `no`: The default restart policy. Does not restart the container under any circumstance.
*   `always`: The policy always restarts the container until its removal.
*   `on-failure`: The policy restarts the container if the exit code indicates an on-failure error.
*   `unless-stopped`: The policy always restarts the container regardless of the exit code, but will stop restarting when the service is stopped or removed.

#### `stop_grace_period`
Specifies how long to wait when attempting to stop a container if it doesn't handle SIGTERM (or whatever stop signal has been specified with `stop_signal`), before sending SIGKILL.

#### `stop_signal`
Sets an alternative signal to stop the container. By default `stop` uses SIGTERM.

#### `sysctls`
Kernel parameters to set in the container.

#### `ulimits`
Override the default ulimits for a container.

#### `user`
Override the user used to run the container process.

#### `working_dir`
Override the container's working directory from that specified by the image.


## Comprehensive Reference: Docker Compose Specification

This section provides an exhaustive reference of the Docker Compose specification, detailing every attribute and its usage.

### Service Top-Level Element

The `services` element is the core of a Compose file. It defines the containers that make up your application.

#### `build`
Configuration options that are applied at build time.

*   `context`: Either a path to a directory containing a Dockerfile, or a url to a git repository.
*   `dockerfile`: Alternate Dockerfile.
*   `args`: Add build arguments, which are environment variables accessible only during the build process.
*   `ssh`: SSH authentications that the builder should use.
*   `cache_from`: A list of images that the builder should use for cache resolution.
*   `cache_to`: A list of export locations to be used to share build cache with future builds.
*   `target`: Build the specified stage as defined inside the Dockerfile.
*   `secrets`: Grant access to sensitive data defined by secrets on a per-service basis.
*   `tags`: A list of tag names to be applied to the built image.
*   `platforms`: A list of target platforms.

#### `image`
Specifies the image to start the container from. Can either be a repository/tag or a partial image ID.

#### `command`
Overrides the default command declared by the container image (i.e., by Dockerfile's `CMD`).

#### `entrypoint`
Overrides the default entrypoint declared by the container image (i.e., by Dockerfile's `ENTRYPOINT`).

#### `environment`
Adds environment variables. You can use either an array or a dictionary.

#### `env_file`
Adds environment variables from a file.

#### `depends_on`
Expresses dependency between services.

*   `condition`:
    *   `service_started`: (default) The dependency must be started before the dependent service.
    *   `service_healthy`: The dependency must be "healthy" before the dependent service starts.
    *   `service_completed_successfully`: The dependency must run to completion and exit with a 0 status code.
*   `restart`: When set to true, Compose restarts this service after it updates the dependency service.

#### `deploy`
Specifies configuration related to the deployment and running of services. This only takes effect when deploying to a swarm with `docker stack deploy`, and is ignored by `docker compose up` and `docker compose run`.

*   `endpoint_mode`: Valid values are `vip` and `dnsrr`.
*   `labels`: Specify labels for the service.
*   `mode`: Either `global` (exactly one container per swarm node) or `replicated` (a specified number of containers).
*   `placement`: Specify placement constraints and preferences.
*   `replicas`: If the service is `replicated` (which is the default), specify the number of containers that should be running at any given time.
*   `resources`: Configure resource limits and reservations.
    *   `limits`: The platform must prevent the container to allocate more.
    *   `reservations`: The platform must guarantee the container can allocate at least the configured amount.
*   `restart_policy`: Configures if and how to restart containers when they exit.
*   `rollback_config`: Configures how the service should be rolled back in case of a failing update.
*   `update_config`: Configures how the service should be updated. Useful for configuring rolling updates.

#### `healthcheck`
Configures a check that's run to determine whether or not containers for this service are "healthy".

*   `test`: The command to run to check health.
*   `interval`: The time to wait between checks.
*   `timeout`: The time to wait before considering the check to have hung.
*   `retries`: The number of consecutive failures needed to consider a container as unhealthy.
*   `start_period`: Initialization time for containers that need time to bootstrap.
*   `disable`: Disable any default healthcheck set by the image.

#### `logging`
Logging configuration for the service.

*   `driver`: The logging driver to use (e.g., `json-file`, `syslog`, `journald`).
*   `options`: Driver-specific options (e.g., `max-size`, `max-file`).

#### `networks`
Networks to join, referencing entries under the top-level `networks` key.

#### `ports`
Expose ports.

*   Short syntax: `HOST:CONTAINER` or just `CONTAINER` (host port is chosen randomly).
*   Long syntax: Allows configuring the `target` port, `published` port, `protocol` (tcp or udp), and `mode` (host or ingress).

#### `volumes`
Mount host paths or named volumes, specified as sub-options to a service.

*   Short syntax: `VOLUME:CONTAINER_PATH:ACCESS_MODE`
*   Long syntax: Allows configuring `type` (volume, bind, tmpfs), `source`, `target`, `read_only`, and `bind` or `volume` specific options.

#### `secrets`
Grant access to secrets on a per-service basis using the per-service `secrets` configuration.

#### `configs`
Grant access to configs on a per-service basis using the per-service `configs` configuration.

#### `profiles`
Allow defining a list of named profiles for the service to be enabled under. When not set, the service is always enabled.

#### `restart`
Defines the restart policy for the service.

*   `no`: The default restart policy. Does not restart the container under any circumstance.
*   `always`: The policy always restarts the container until its removal.
*   `on-failure`: The policy restarts the container if the exit code indicates an on-failure error.
*   `unless-stopped`: The policy always restarts the container regardless of the exit code, but will stop restarting when the service is stopped or removed.

#### `stop_grace_period`
Specifies how long to wait when attempting to stop a container if it doesn't handle SIGTERM (or whatever stop signal has been specified with `stop_signal`), before sending SIGKILL.

#### `stop_signal`
Sets an alternative signal to stop the container. By default `stop` uses SIGTERM.

#### `sysctls`
Kernel parameters to set in the container.

#### `ulimits`
Override the default ulimits for a container.

#### `user`
Override the user used to run the container process.

#### `working_dir`
Override the container's working directory from that specified by the image.


## Comprehensive Reference: Docker Compose Specification

This section provides an exhaustive reference of the Docker Compose specification, detailing every attribute and its usage.

### Service Top-Level Element

The `services` element is the core of a Compose file. It defines the containers that make up your application.

#### `build`
Configuration options that are applied at build time.

*   `context`: Either a path to a directory containing a Dockerfile, or a url to a git repository.
*   `dockerfile`: Alternate Dockerfile.
*   `args`: Add build arguments, which are environment variables accessible only during the build process.
*   `ssh`: SSH authentications that the builder should use.
*   `cache_from`: A list of images that the builder should use for cache resolution.
*   `cache_to`: A list of export locations to be used to share build cache with future builds.
*   `target`: Build the specified stage as defined inside the Dockerfile.
*   `secrets`: Grant access to sensitive data defined by secrets on a per-service basis.
*   `tags`: A list of tag names to be applied to the built image.
*   `platforms`: A list of target platforms.

#### `image`
Specifies the image to start the container from. Can either be a repository/tag or a partial image ID.

#### `command`
Overrides the default command declared by the container image (i.e., by Dockerfile's `CMD`).

#### `entrypoint`
Overrides the default entrypoint declared by the container image (i.e., by Dockerfile's `ENTRYPOINT`).

#### `environment`
Adds environment variables. You can use either an array or a dictionary.

#### `env_file`
Adds environment variables from a file.

#### `depends_on`
Expresses dependency between services.

*   `condition`:
    *   `service_started`: (default) The dependency must be started before the dependent service.
    *   `service_healthy`: The dependency must be "healthy" before the dependent service starts.
    *   `service_completed_successfully`: The dependency must run to completion and exit with a 0 status code.
*   `restart`: When set to true, Compose restarts this service after it updates the dependency service.

#### `deploy`
Specifies configuration related to the deployment and running of services. This only takes effect when deploying to a swarm with `docker stack deploy`, and is ignored by `docker compose up` and `docker compose run`.

*   `endpoint_mode`: Valid values are `vip` and `dnsrr`.
*   `labels`: Specify labels for the service.
*   `mode`: Either `global` (exactly one container per swarm node) or `replicated` (a specified number of containers).
*   `placement`: Specify placement constraints and preferences.
*   `replicas`: If the service is `replicated` (which is the default), specify the number of containers that should be running at any given time.
*   `resources`: Configure resource limits and reservations.
    *   `limits`: The platform must prevent the container to allocate more.
    *   `reservations`: The platform must guarantee the container can allocate at least the configured amount.
*   `restart_policy`: Configures if and how to restart containers when they exit.
*   `rollback_config`: Configures how the service should be rolled back in case of a failing update.
*   `update_config`: Configures how the service should be updated. Useful for configuring rolling updates.

#### `healthcheck`
Configures a check that's run to determine whether or not containers for this service are "healthy".

*   `test`: The command to run to check health.
*   `interval`: The time to wait between checks.
*   `timeout`: The time to wait before considering the check to have hung.
*   `retries`: The number of consecutive failures needed to consider a container as unhealthy.
*   `start_period`: Initialization time for containers that need time to bootstrap.
*   `disable`: Disable any default healthcheck set by the image.

#### `logging`
Logging configuration for the service.

*   `driver`: The logging driver to use (e.g., `json-file`, `syslog`, `journald`).
*   `options`: Driver-specific options (e.g., `max-size`, `max-file`).

#### `networks`
Networks to join, referencing entries under the top-level `networks` key.

#### `ports`
Expose ports.

*   Short syntax: `HOST:CONTAINER` or just `CONTAINER` (host port is chosen randomly).
*   Long syntax: Allows configuring the `target` port, `published` port, `protocol` (tcp or udp), and `mode` (host or ingress).

#### `volumes`
Mount host paths or named volumes, specified as sub-options to a service.

*   Short syntax: `VOLUME:CONTAINER_PATH:ACCESS_MODE`
*   Long syntax: Allows configuring `type` (volume, bind, tmpfs), `source`, `target`, `read_only`, and `bind` or `volume` specific options.

#### `secrets`
Grant access to secrets on a per-service basis using the per-service `secrets` configuration.

#### `configs`
Grant access to configs on a per-service basis using the per-service `configs` configuration.

#### `profiles`
Allow defining a list of named profiles for the service to be enabled under. When not set, the service is always enabled.

#### `restart`
Defines the restart policy for the service.

*   `no`: The default restart policy. Does not restart the container under any circumstance.
*   `always`: The policy always restarts the container until its removal.
*   `on-failure`: The policy restarts the container if the exit code indicates an on-failure error.
*   `unless-stopped`: The policy always restarts the container regardless of the exit code, but will stop restarting when the service is stopped or removed.

#### `stop_grace_period`
Specifies how long to wait when attempting to stop a container if it doesn't handle SIGTERM (or whatever stop signal has been specified with `stop_signal`), before sending SIGKILL.

#### `stop_signal`
Sets an alternative signal to stop the container. By default `stop` uses SIGTERM.

#### `sysctls`
Kernel parameters to set in the container.

#### `ulimits`
Override the default ulimits for a container.

#### `user`
Override the user used to run the container process.

#### `working_dir`
Override the container's working directory from that specified by the image.


## Comprehensive Reference: Docker Compose Specification

This section provides an exhaustive reference of the Docker Compose specification, detailing every attribute and its usage.

### Service Top-Level Element

The `services` element is the core of a Compose file. It defines the containers that make up your application.

#### `build`
Configuration options that are applied at build time.

*   `context`: Either a path to a directory containing a Dockerfile, or a url to a git repository.
*   `dockerfile`: Alternate Dockerfile.
*   `args`: Add build arguments, which are environment variables accessible only during the build process.
*   `ssh`: SSH authentications that the builder should use.
*   `cache_from`: A list of images that the builder should use for cache resolution.
*   `cache_to`: A list of export locations to be used to share build cache with future builds.
*   `target`: Build the specified stage as defined inside the Dockerfile.
*   `secrets`: Grant access to sensitive data defined by secrets on a per-service basis.
*   `tags`: A list of tag names to be applied to the built image.
*   `platforms`: A list of target platforms.

#### `image`
Specifies the image to start the container from. Can either be a repository/tag or a partial image ID.

#### `command`
Overrides the default command declared by the container image (i.e., by Dockerfile's `CMD`).

#### `entrypoint`
Overrides the default entrypoint declared by the container image (i.e., by Dockerfile's `ENTRYPOINT`).

#### `environment`
Adds environment variables. You can use either an array or a dictionary.

#### `env_file`
Adds environment variables from a file.

#### `depends_on`
Expresses dependency between services.

*   `condition`:
    *   `service_started`: (default) The dependency must be started before the dependent service.
    *   `service_healthy`: The dependency must be "healthy" before the dependent service starts.
    *   `service_completed_successfully`: The dependency must run to completion and exit with a 0 status code.
*   `restart`: When set to true, Compose restarts this service after it updates the dependency service.

#### `deploy`
Specifies configuration related to the deployment and running of services. This only takes effect when deploying to a swarm with `docker stack deploy`, and is ignored by `docker compose up` and `docker compose run`.

*   `endpoint_mode`: Valid values are `vip` and `dnsrr`.
*   `labels`: Specify labels for the service.
*   `mode`: Either `global` (exactly one container per swarm node) or `replicated` (a specified number of containers).
*   `placement`: Specify placement constraints and preferences.
*   `replicas`: If the service is `replicated` (which is the default), specify the number of containers that should be running at any given time.
*   `resources`: Configure resource limits and reservations.
    *   `limits`: The platform must prevent the container to allocate more.
    *   `reservations`: The platform must guarantee the container can allocate at least the configured amount.
*   `restart_policy`: Configures if and how to restart containers when they exit.
*   `rollback_config`: Configures how the service should be rolled back in case of a failing update.
*   `update_config`: Configures how the service should be updated. Useful for configuring rolling updates.

#### `healthcheck`
Configures a check that's run to determine whether or not containers for this service are "healthy".

*   `test`: The command to run to check health.
*   `interval`: The time to wait between checks.
*   `timeout`: The time to wait before considering the check to have hung.
*   `retries`: The number of consecutive failures needed to consider a container as unhealthy.
*   `start_period`: Initialization time for containers that need time to bootstrap.
*   `disable`: Disable any default healthcheck set by the image.

#### `logging`
Logging configuration for the service.

*   `driver`: The logging driver to use (e.g., `json-file`, `syslog`, `journald`).
*   `options`: Driver-specific options (e.g., `max-size`, `max-file`).

#### `networks`
Networks to join, referencing entries under the top-level `networks` key.

#### `ports`
Expose ports.

*   Short syntax: `HOST:CONTAINER` or just `CONTAINER` (host port is chosen randomly).
*   Long syntax: Allows configuring the `target` port, `published` port, `protocol` (tcp or udp), and `mode` (host or ingress).

#### `volumes`
Mount host paths or named volumes, specified as sub-options to a service.

*   Short syntax: `VOLUME:CONTAINER_PATH:ACCESS_MODE`
*   Long syntax: Allows configuring `type` (volume, bind, tmpfs), `source`, `target`, `read_only`, and `bind` or `volume` specific options.

#### `secrets`
Grant access to secrets on a per-service basis using the per-service `secrets` configuration.

#### `configs`
Grant access to configs on a per-service basis using the per-service `configs` configuration.

#### `profiles`
Allow defining a list of named profiles for the service to be enabled under. When not set, the service is always enabled.

#### `restart`
Defines the restart policy for the service.

*   `no`: The default restart policy. Does not restart the container under any circumstance.
*   `always`: The policy always restarts the container until its removal.
*   `on-failure`: The policy restarts the container if the exit code indicates an on-failure error.
*   `unless-stopped`: The policy always restarts the container regardless of the exit code, but will stop restarting when the service is stopped or removed.

#### `stop_grace_period`
Specifies how long to wait when attempting to stop a container if it doesn't handle SIGTERM (or whatever stop signal has been specified with `stop_signal`), before sending SIGKILL.

#### `stop_signal`
Sets an alternative signal to stop the container. By default `stop` uses SIGTERM.

#### `sysctls`
Kernel parameters to set in the container.

#### `ulimits`
Override the default ulimits for a container.

#### `user`
Override the user used to run the container process.

#### `working_dir`
Override the container's working directory from that specified by the image.


## Comprehensive Reference: Docker Compose Specification

This section provides an exhaustive reference of the Docker Compose specification, detailing every attribute and its usage.

### Service Top-Level Element

The `services` element is the core of a Compose file. It defines the containers that make up your application.

#### `build`
Configuration options that are applied at build time.

*   `context`: Either a path to a directory containing a Dockerfile, or a url to a git repository.
*   `dockerfile`: Alternate Dockerfile.
*   `args`: Add build arguments, which are environment variables accessible only during the build process.
*   `ssh`: SSH authentications that the builder should use.
*   `cache_from`: A list of images that the builder should use for cache resolution.
*   `cache_to`: A list of export locations to be used to share build cache with future builds.
*   `target`: Build the specified stage as defined inside the Dockerfile.
*   `secrets`: Grant access to sensitive data defined by secrets on a per-service basis.
*   `tags`: A list of tag names to be applied to the built image.
*   `platforms`: A list of target platforms.

#### `image`
Specifies the image to start the container from. Can either be a repository/tag or a partial image ID.

#### `command`
Overrides the default command declared by the container image (i.e., by Dockerfile's `CMD`).

#### `entrypoint`
Overrides the default entrypoint declared by the container image (i.e., by Dockerfile's `ENTRYPOINT`).

#### `environment`
Adds environment variables. You can use either an array or a dictionary.

#### `env_file`
Adds environment variables from a file.

#### `depends_on`
Expresses dependency between services.

*   `condition`:
    *   `service_started`: (default) The dependency must be started before the dependent service.
    *   `service_healthy`: The dependency must be "healthy" before the dependent service starts.
    *   `service_completed_successfully`: The dependency must run to completion and exit with a 0 status code.
*   `restart`: When set to true, Compose restarts this service after it updates the dependency service.

#### `deploy`
Specifies configuration related to the deployment and running of services. This only takes effect when deploying to a swarm with `docker stack deploy`, and is ignored by `docker compose up` and `docker compose run`.

*   `endpoint_mode`: Valid values are `vip` and `dnsrr`.
*   `labels`: Specify labels for the service.
*   `mode`: Either `global` (exactly one container per swarm node) or `replicated` (a specified number of containers).
*   `placement`: Specify placement constraints and preferences.
*   `replicas`: If the service is `replicated` (which is the default), specify the number of containers that should be running at any given time.
*   `resources`: Configure resource limits and reservations.
    *   `limits`: The platform must prevent the container to allocate more.
    *   `reservations`: The platform must guarantee the container can allocate at least the configured amount.
*   `restart_policy`: Configures if and how to restart containers when they exit.
*   `rollback_config`: Configures how the service should be rolled back in case of a failing update.
*   `update_config`: Configures how the service should be updated. Useful for configuring rolling updates.

#### `healthcheck`
Configures a check that's run to determine whether or not containers for this service are "healthy".

*   `test`: The command to run to check health.
*   `interval`: The time to wait between checks.
*   `timeout`: The time to wait before considering the check to have hung.
*   `retries`: The number of consecutive failures needed to consider a container as unhealthy.
*   `start_period`: Initialization time for containers that need time to bootstrap.
*   `disable`: Disable any default healthcheck set by the image.

#### `logging`
Logging configuration for the service.

*   `driver`: The logging driver to use (e.g., `json-file`, `syslog`, `journald`).
*   `options`: Driver-specific options (e.g., `max-size`, `max-file`).

#### `networks`
Networks to join, referencing entries under the top-level `networks` key.

#### `ports`
Expose ports.

*   Short syntax: `HOST:CONTAINER` or just `CONTAINER` (host port is chosen randomly).
*   Long syntax: Allows configuring the `target` port, `published` port, `protocol` (tcp or udp), and `mode` (host or ingress).

#### `volumes`
Mount host paths or named volumes, specified as sub-options to a service.

*   Short syntax: `VOLUME:CONTAINER_PATH:ACCESS_MODE`
*   Long syntax: Allows configuring `type` (volume, bind, tmpfs), `source`, `target`, `read_only`, and `bind` or `volume` specific options.

#### `secrets`
Grant access to secrets on a per-service basis using the per-service `secrets` configuration.

#### `configs`
Grant access to configs on a per-service basis using the per-service `configs` configuration.

#### `profiles`
Allow defining a list of named profiles for the service to be enabled under. When not set, the service is always enabled.

#### `restart`
Defines the restart policy for the service.

*   `no`: The default restart policy. Does not restart the container under any circumstance.
*   `always`: The policy always restarts the container until its removal.
*   `on-failure`: The policy restarts the container if the exit code indicates an on-failure error.
*   `unless-stopped`: The policy always restarts the container regardless of the exit code, but will stop restarting when the service is stopped or removed.

#### `stop_grace_period`
Specifies how long to wait when attempting to stop a container if it doesn't handle SIGTERM (or whatever stop signal has been specified with `stop_signal`), before sending SIGKILL.

#### `stop_signal`
Sets an alternative signal to stop the container. By default `stop` uses SIGTERM.

#### `sysctls`
Kernel parameters to set in the container.

#### `ulimits`
Override the default ulimits for a container.

#### `user`
Override the user used to run the container process.

#### `working_dir`
Override the container's working directory from that specified by the image.


## Comprehensive Reference: Docker Compose Specification

This section provides an exhaustive reference of the Docker Compose specification, detailing every attribute and its usage.

### Service Top-Level Element

The `services` element is the core of a Compose file. It defines the containers that make up your application.

#### `build`
Configuration options that are applied at build time.

*   `context`: Either a path to a directory containing a Dockerfile, or a url to a git repository.
*   `dockerfile`: Alternate Dockerfile.
*   `args`: Add build arguments, which are environment variables accessible only during the build process.
*   `ssh`: SSH authentications that the builder should use.
*   `cache_from`: A list of images that the builder should use for cache resolution.
*   `cache_to`: A list of export locations to be used to share build cache with future builds.
*   `target`: Build the specified stage as defined inside the Dockerfile.
*   `secrets`: Grant access to sensitive data defined by secrets on a per-service basis.
*   `tags`: A list of tag names to be applied to the built image.
*   `platforms`: A list of target platforms.

#### `image`
Specifies the image to start the container from. Can either be a repository/tag or a partial image ID.

#### `command`
Overrides the default command declared by the container image (i.e., by Dockerfile's `CMD`).

#### `entrypoint`
Overrides the default entrypoint declared by the container image (i.e., by Dockerfile's `ENTRYPOINT`).

#### `environment`
Adds environment variables. You can use either an array or a dictionary.

#### `env_file`
Adds environment variables from a file.

#### `depends_on`
Expresses dependency between services.

*   `condition`:
    *   `service_started`: (default) The dependency must be started before the dependent service.
    *   `service_healthy`: The dependency must be "healthy" before the dependent service starts.
    *   `service_completed_successfully`: The dependency must run to completion and exit with a 0 status code.
*   `restart`: When set to true, Compose restarts this service after it updates the dependency service.

#### `deploy`
Specifies configuration related to the deployment and running of services. This only takes effect when deploying to a swarm with `docker stack deploy`, and is ignored by `docker compose up` and `docker compose run`.

*   `endpoint_mode`: Valid values are `vip` and `dnsrr`.
*   `labels`: Specify labels for the service.
*   `mode`: Either `global` (exactly one container per swarm node) or `replicated` (a specified number of containers).
*   `placement`: Specify placement constraints and preferences.
*   `replicas`: If the service is `replicated` (which is the default), specify the number of containers that should be running at any given time.
*   `resources`: Configure resource limits and reservations.
    *   `limits`: The platform must prevent the container to allocate more.
    *   `reservations`: The platform must guarantee the container can allocate at least the configured amount.
*   `restart_policy`: Configures if and how to restart containers when they exit.
*   `rollback_config`: Configures how the service should be rolled back in case of a failing update.
*   `update_config`: Configures how the service should be updated. Useful for configuring rolling updates.

#### `healthcheck`
Configures a check that's run to determine whether or not containers for this service are "healthy".

*   `test`: The command to run to check health.
*   `interval`: The time to wait between checks.
*   `timeout`: The time to wait before considering the check to have hung.
*   `retries`: The number of consecutive failures needed to consider a container as unhealthy.
*   `start_period`: Initialization time for containers that need time to bootstrap.
*   `disable`: Disable any default healthcheck set by the image.

#### `logging`
Logging configuration for the service.

*   `driver`: The logging driver to use (e.g., `json-file`, `syslog`, `journald`).
*   `options`: Driver-specific options (e.g., `max-size`, `max-file`).

#### `networks`
Networks to join, referencing entries under the top-level `networks` key.

#### `ports`
Expose ports.

*   Short syntax: `HOST:CONTAINER` or just `CONTAINER` (host port is chosen randomly).
*   Long syntax: Allows configuring the `target` port, `published` port, `protocol` (tcp or udp), and `mode` (host or ingress).

#### `volumes`
Mount host paths or named volumes, specified as sub-options to a service.

*   Short syntax: `VOLUME:CONTAINER_PATH:ACCESS_MODE`
*   Long syntax: Allows configuring `type` (volume, bind, tmpfs), `source`, `target`, `read_only`, and `bind` or `volume` specific options.

#### `secrets`
Grant access to secrets on a per-service basis using the per-service `secrets` configuration.

#### `configs`
Grant access to configs on a per-service basis using the per-service `configs` configuration.

#### `profiles`
Allow defining a list of named profiles for the service to be enabled under. When not set, the service is always enabled.

#### `restart`
Defines the restart policy for the service.

*   `no`: The default restart policy. Does not restart the container under any circumstance.
*   `always`: The policy always restarts the container until its removal.
*   `on-failure`: The policy restarts the container if the exit code indicates an on-failure error.
*   `unless-stopped`: The policy always restarts the container regardless of the exit code, but will stop restarting when the service is stopped or removed.

#### `stop_grace_period`
Specifies how long to wait when attempting to stop a container if it doesn't handle SIGTERM (or whatever stop signal has been specified with `stop_signal`), before sending SIGKILL.

#### `stop_signal`
Sets an alternative signal to stop the container. By default `stop` uses SIGTERM.

#### `sysctls`
Kernel parameters to set in the container.

#### `ulimits`
Override the default ulimits for a container.

#### `user`
Override the user used to run the container process.

#### `working_dir`
Override the container's working directory from that specified by the image.


## Comprehensive Reference: Docker Compose Specification

This section provides an exhaustive reference of the Docker Compose specification, detailing every attribute and its usage.

### Service Top-Level Element

The `services` element is the core of a Compose file. It defines the containers that make up your application.

#### `build`
Configuration options that are applied at build time.

*   `context`: Either a path to a directory containing a Dockerfile, or a url to a git repository.
*   `dockerfile`: Alternate Dockerfile.
*   `args`: Add build arguments, which are environment variables accessible only during the build process.
*   `ssh`: SSH authentications that the builder should use.
*   `cache_from`: A list of images that the builder should use for cache resolution.
*   `cache_to`: A list of export locations to be used to share build cache with future builds.
*   `target`: Build the specified stage as defined inside the Dockerfile.
*   `secrets`: Grant access to sensitive data defined by secrets on a per-service basis.
*   `tags`: A list of tag names to be applied to the built image.
*   `platforms`: A list of target platforms.

#### `image`
Specifies the image to start the container from. Can either be a repository/tag or a partial image ID.

#### `command`
Overrides the default command declared by the container image (i.e., by Dockerfile's `CMD`).

#### `entrypoint`
Overrides the default entrypoint declared by the container image (i.e., by Dockerfile's `ENTRYPOINT`).

#### `environment`
Adds environment variables. You can use either an array or a dictionary.

#### `env_file`
Adds environment variables from a file.

#### `depends_on`
Expresses dependency between services.

*   `condition`:
    *   `service_started`: (default) The dependency must be started before the dependent service.
    *   `service_healthy`: The dependency must be "healthy" before the dependent service starts.
    *   `service_completed_successfully`: The dependency must run to completion and exit with a 0 status code.
*   `restart`: When set to true, Compose restarts this service after it updates the dependency service.

#### `deploy`
Specifies configuration related to the deployment and running of services. This only takes effect when deploying to a swarm with `docker stack deploy`, and is ignored by `docker compose up` and `docker compose run`.

*   `endpoint_mode`: Valid values are `vip` and `dnsrr`.
*   `labels`: Specify labels for the service.
*   `mode`: Either `global` (exactly one container per swarm node) or `replicated` (a specified number of containers).
*   `placement`: Specify placement constraints and preferences.
*   `replicas`: If the service is `replicated` (which is the default), specify the number of containers that should be running at any given time.
*   `resources`: Configure resource limits and reservations.
    *   `limits`: The platform must prevent the container to allocate more.
    *   `reservations`: The platform must guarantee the container can allocate at least the configured amount.
*   `restart_policy`: Configures if and how to restart containers when they exit.
*   `rollback_config`: Configures how the service should be rolled back in case of a failing update.
*   `update_config`: Configures how the service should be updated. Useful for configuring rolling updates.

#### `healthcheck`
Configures a check that's run to determine whether or not containers for this service are "healthy".

*   `test`: The command to run to check health.
*   `interval`: The time to wait between checks.
*   `timeout`: The time to wait before considering the check to have hung.
*   `retries`: The number of consecutive failures needed to consider a container as unhealthy.
*   `start_period`: Initialization time for containers that need time to bootstrap.
*   `disable`: Disable any default healthcheck set by the image.

#### `logging`
Logging configuration for the service.

*   `driver`: The logging driver to use (e.g., `json-file`, `syslog`, `journald`).
*   `options`: Driver-specific options (e.g., `max-size`, `max-file`).

#### `networks`
Networks to join, referencing entries under the top-level `networks` key.

#### `ports`
Expose ports.

*   Short syntax: `HOST:CONTAINER` or just `CONTAINER` (host port is chosen randomly).
*   Long syntax: Allows configuring the `target` port, `published` port, `protocol` (tcp or udp), and `mode` (host or ingress).

#### `volumes`
Mount host paths or named volumes, specified as sub-options to a service.

*   Short syntax: `VOLUME:CONTAINER_PATH:ACCESS_MODE`
*   Long syntax: Allows configuring `type` (volume, bind, tmpfs), `source`, `target`, `read_only`, and `bind` or `volume` specific options.

#### `secrets`
Grant access to secrets on a per-service basis using the per-service `secrets` configuration.

#### `configs`
Grant access to configs on a per-service basis using the per-service `configs` configuration.

#### `profiles`
Allow defining a list of named profiles for the service to be enabled under. When not set, the service is always enabled.

#### `restart`
Defines the restart policy for the service.

*   `no`: The default restart policy. Does not restart the container under any circumstance.
*   `always`: The policy always restarts the container until its removal.
*   `on-failure`: The policy restarts the container if the exit code indicates an on-failure error.
*   `unless-stopped`: The policy always restarts the container regardless of the exit code, but will stop restarting when the service is stopped or removed.

#### `stop_grace_period`
Specifies how long to wait when attempting to stop a container if it doesn't handle SIGTERM (or whatever stop signal has been specified with `stop_signal`), before sending SIGKILL.

#### `stop_signal`
Sets an alternative signal to stop the container. By default `stop` uses SIGTERM.

#### `sysctls`
Kernel parameters to set in the container.

#### `ulimits`
Override the default ulimits for a container.

#### `user`
Override the user used to run the container process.

#### `working_dir`
Override the container's working directory from that specified by the image.


## Comprehensive Reference: Docker Compose Specification

This section provides an exhaustive reference of the Docker Compose specification, detailing every attribute and its usage.

### Service Top-Level Element

The `services` element is the core of a Compose file. It defines the containers that make up your application.

#### `build`
Configuration options that are applied at build time.

*   `context`: Either a path to a directory containing a Dockerfile, or a url to a git repository.
*   `dockerfile`: Alternate Dockerfile.
*   `args`: Add build arguments, which are environment variables accessible only during the build process.
*   `ssh`: SSH authentications that the builder should use.
*   `cache_from`: A list of images that the builder should use for cache resolution.
*   `cache_to`: A list of export locations to be used to share build cache with future builds.
*   `target`: Build the specified stage as defined inside the Dockerfile.
*   `secrets`: Grant access to sensitive data defined by secrets on a per-service basis.
*   `tags`: A list of tag names to be applied to the built image.
*   `platforms`: A list of target platforms.

#### `image`
Specifies the image to start the container from. Can either be a repository/tag or a partial image ID.

#### `command`
Overrides the default command declared by the container image (i.e., by Dockerfile's `CMD`).

#### `entrypoint`
Overrides the default entrypoint declared by the container image (i.e., by Dockerfile's `ENTRYPOINT`).

#### `environment`
Adds environment variables. You can use either an array or a dictionary.

#### `env_file`
Adds environment variables from a file.

#### `depends_on`
Expresses dependency between services.

*   `condition`:
    *   `service_started`: (default) The dependency must be started before the dependent service.
    *   `service_healthy`: The dependency must be "healthy" before the dependent service starts.
    *   `service_completed_successfully`: The dependency must run to completion and exit with a 0 status code.
*   `restart`: When set to true, Compose restarts this service after it updates the dependency service.

#### `deploy`
Specifies configuration related to the deployment and running of services. This only takes effect when deploying to a swarm with `docker stack deploy`, and is ignored by `docker compose up` and `docker compose run`.

*   `endpoint_mode`: Valid values are `vip` and `dnsrr`.
*   `labels`: Specify labels for the service.
*   `mode`: Either `global` (exactly one container per swarm node) or `replicated` (a specified number of containers).
*   `placement`: Specify placement constraints and preferences.
*   `replicas`: If the service is `replicated` (which is the default), specify the number of containers that should be running at any given time.
*   `resources`: Configure resource limits and reservations.
    *   `limits`: The platform must prevent the container to allocate more.
    *   `reservations`: The platform must guarantee the container can allocate at least the configured amount.
*   `restart_policy`: Configures if and how to restart containers when they exit.
*   `rollback_config`: Configures how the service should be rolled back in case of a failing update.
*   `update_config`: Configures how the service should be updated. Useful for configuring rolling updates.

#### `healthcheck`
Configures a check that's run to determine whether or not containers for this service are "healthy".

*   `test`: The command to run to check health.
*   `interval`: The time to wait between checks.
*   `timeout`: The time to wait before considering the check to have hung.
*   `retries`: The number of consecutive failures needed to consider a container as unhealthy.
*   `start_period`: Initialization time for containers that need time to bootstrap.
*   `disable`: Disable any default healthcheck set by the image.

#### `logging`
Logging configuration for the service.

*   `driver`: The logging driver to use (e.g., `json-file`, `syslog`, `journald`).
*   `options`: Driver-specific options (e.g., `max-size`, `max-file`).

#### `networks`
Networks to join, referencing entries under the top-level `networks` key.

#### `ports`
Expose ports.

*   Short syntax: `HOST:CONTAINER` or just `CONTAINER` (host port is chosen randomly).
*   Long syntax: Allows configuring the `target` port, `published` port, `protocol` (tcp or udp), and `mode` (host or ingress).

#### `volumes`
Mount host paths or named volumes, specified as sub-options to a service.

*   Short syntax: `VOLUME:CONTAINER_PATH:ACCESS_MODE`
*   Long syntax: Allows configuring `type` (volume, bind, tmpfs), `source`, `target`, `read_only`, and `bind` or `volume` specific options.

#### `secrets`
Grant access to secrets on a per-service basis using the per-service `secrets` configuration.

#### `configs`
Grant access to configs on a per-service basis using the per-service `configs` configuration.

#### `profiles`
Allow defining a list of named profiles for the service to be enabled under. When not set, the service is always enabled.

#### `restart`
Defines the restart policy for the service.

*   `no`: The default restart policy. Does not restart the container under any circumstance.
*   `always`: The policy always restarts the container until its removal.
*   `on-failure`: The policy restarts the container if the exit code indicates an on-failure error.
*   `unless-stopped`: The policy always restarts the container regardless of the exit code, but will stop restarting when the service is stopped or removed.

#### `stop_grace_period`
Specifies how long to wait when attempting to stop a container if it doesn't handle SIGTERM (or whatever stop signal has been specified with `stop_signal`), before sending SIGKILL.

#### `stop_signal`
Sets an alternative signal to stop the container. By default `stop` uses SIGTERM.

#### `sysctls`
Kernel parameters to set in the container.

#### `ulimits`
Override the default ulimits for a container.

#### `user`
Override the user used to run the container process.

#### `working_dir`
Override the container's working directory from that specified by the image.


## Deep Dive: Advanced Docker Networking Architectures

Understanding Docker networking beyond the basic bridge network is crucial for enterprise deployments.

### Macvlan Networks

Macvlan networks allow you to assign a MAC address to a container, making it appear as a physical device on your network. This is useful for legacy applications that expect to be directly connected to the physical network, rather than routed through the Docker host's network stack.

**Configuration:**

```bash
docker network create -d macvlan   --subnet=192.168.1.0/24   --gateway=192.168.1.1   -o parent=eth0 pub_net
```

**Important Considerations:**
*   **Host Isolation:** By design, the Docker host cannot communicate with containers on a macvlan network. If you need host-to-container communication, you must create a secondary macvlan interface on the host.
*   **Promiscuous Mode:** The physical interface (`eth0` in the example) must often be put into promiscuous mode, which may not be supported in all environments (e.g., some cloud providers).

### IPvlan Networks

IPvlan is similar to Macvlan but shares the MAC address of the parent interface. This solves the promiscuous mode issue and is generally preferred over Macvlan in modern deployments.

It operates in two modes:
*   **L2 Mode:** Similar to Macvlan, containers get IP addresses from the physical network subnet.
*   **L3 Mode:** The Docker host acts as a router. Containers are on a different subnet, and the host routes traffic to them.

### Custom Bridge Networks and DNS

When you create a custom bridge network (which Compose does by default), Docker provides an embedded DNS server. This allows containers to resolve each other by service name or container name.

**Troubleshooting DNS:**
If containers cannot resolve each other:
1.  Ensure they are on the same custom network. The default `bridge` network (named `bridge`) does *not* provide automatic DNS resolution.
2.  Check the `/etc/resolv.conf` inside the container. It should point to Docker's embedded DNS server (usually `127.0.0.11`).


## Deep Dive: Advanced Docker Networking Architectures

Understanding Docker networking beyond the basic bridge network is crucial for enterprise deployments.

### Macvlan Networks

Macvlan networks allow you to assign a MAC address to a container, making it appear as a physical device on your network. This is useful for legacy applications that expect to be directly connected to the physical network, rather than routed through the Docker host's network stack.

**Configuration:**

```bash
docker network create -d macvlan   --subnet=192.168.1.0/24   --gateway=192.168.1.1   -o parent=eth0 pub_net
```

**Important Considerations:**
*   **Host Isolation:** By design, the Docker host cannot communicate with containers on a macvlan network. If you need host-to-container communication, you must create a secondary macvlan interface on the host.
*   **Promiscuous Mode:** The physical interface (`eth0` in the example) must often be put into promiscuous mode, which may not be supported in all environments (e.g., some cloud providers).

### IPvlan Networks

IPvlan is similar to Macvlan but shares the MAC address of the parent interface. This solves the promiscuous mode issue and is generally preferred over Macvlan in modern deployments.

It operates in two modes:
*   **L2 Mode:** Similar to Macvlan, containers get IP addresses from the physical network subnet.
*   **L3 Mode:** The Docker host acts as a router. Containers are on a different subnet, and the host routes traffic to them.

### Custom Bridge Networks and DNS

When you create a custom bridge network (which Compose does by default), Docker provides an embedded DNS server. This allows containers to resolve each other by service name or container name.

**Troubleshooting DNS:**
If containers cannot resolve each other:
1.  Ensure they are on the same custom network. The default `bridge` network (named `bridge`) does *not* provide automatic DNS resolution.
2.  Check the `/etc/resolv.conf` inside the container. It should point to Docker's embedded DNS server (usually `127.0.0.11`).


## Deep Dive: Advanced Docker Networking Architectures

Understanding Docker networking beyond the basic bridge network is crucial for enterprise deployments.

### Macvlan Networks

Macvlan networks allow you to assign a MAC address to a container, making it appear as a physical device on your network. This is useful for legacy applications that expect to be directly connected to the physical network, rather than routed through the Docker host's network stack.

**Configuration:**

```bash
docker network create -d macvlan   --subnet=192.168.1.0/24   --gateway=192.168.1.1   -o parent=eth0 pub_net
```

**Important Considerations:**
*   **Host Isolation:** By design, the Docker host cannot communicate with containers on a macvlan network. If you need host-to-container communication, you must create a secondary macvlan interface on the host.
*   **Promiscuous Mode:** The physical interface (`eth0` in the example) must often be put into promiscuous mode, which may not be supported in all environments (e.g., some cloud providers).

### IPvlan Networks

IPvlan is similar to Macvlan but shares the MAC address of the parent interface. This solves the promiscuous mode issue and is generally preferred over Macvlan in modern deployments.

It operates in two modes:
*   **L2 Mode:** Similar to Macvlan, containers get IP addresses from the physical network subnet.
*   **L3 Mode:** The Docker host acts as a router. Containers are on a different subnet, and the host routes traffic to them.

### Custom Bridge Networks and DNS

When you create a custom bridge network (which Compose does by default), Docker provides an embedded DNS server. This allows containers to resolve each other by service name or container name.

**Troubleshooting DNS:**
If containers cannot resolve each other:
1.  Ensure they are on the same custom network. The default `bridge` network (named `bridge`) does *not* provide automatic DNS resolution.
2.  Check the `/etc/resolv.conf` inside the container. It should point to Docker's embedded DNS server (usually `127.0.0.11`).


## Deep Dive: Advanced Docker Networking Architectures

Understanding Docker networking beyond the basic bridge network is crucial for enterprise deployments.

### Macvlan Networks

Macvlan networks allow you to assign a MAC address to a container, making it appear as a physical device on your network. This is useful for legacy applications that expect to be directly connected to the physical network, rather than routed through the Docker host's network stack.

**Configuration:**

```bash
docker network create -d macvlan   --subnet=192.168.1.0/24   --gateway=192.168.1.1   -o parent=eth0 pub_net
```

**Important Considerations:**
*   **Host Isolation:** By design, the Docker host cannot communicate with containers on a macvlan network. If you need host-to-container communication, you must create a secondary macvlan interface on the host.
*   **Promiscuous Mode:** The physical interface (`eth0` in the example) must often be put into promiscuous mode, which may not be supported in all environments (e.g., some cloud providers).

### IPvlan Networks

IPvlan is similar to Macvlan but shares the MAC address of the parent interface. This solves the promiscuous mode issue and is generally preferred over Macvlan in modern deployments.

It operates in two modes:
*   **L2 Mode:** Similar to Macvlan, containers get IP addresses from the physical network subnet.
*   **L3 Mode:** The Docker host acts as a router. Containers are on a different subnet, and the host routes traffic to them.

### Custom Bridge Networks and DNS

When you create a custom bridge network (which Compose does by default), Docker provides an embedded DNS server. This allows containers to resolve each other by service name or container name.

**Troubleshooting DNS:**
If containers cannot resolve each other:
1.  Ensure they are on the same custom network. The default `bridge` network (named `bridge`) does *not* provide automatic DNS resolution.
2.  Check the `/etc/resolv.conf` inside the container. It should point to Docker's embedded DNS server (usually `127.0.0.11`).


## Deep Dive: Advanced Docker Networking Architectures

Understanding Docker networking beyond the basic bridge network is crucial for enterprise deployments.

### Macvlan Networks

Macvlan networks allow you to assign a MAC address to a container, making it appear as a physical device on your network. This is useful for legacy applications that expect to be directly connected to the physical network, rather than routed through the Docker host's network stack.

**Configuration:**

```bash
docker network create -d macvlan   --subnet=192.168.1.0/24   --gateway=192.168.1.1   -o parent=eth0 pub_net
```

**Important Considerations:**
*   **Host Isolation:** By design, the Docker host cannot communicate with containers on a macvlan network. If you need host-to-container communication, you must create a secondary macvlan interface on the host.
*   **Promiscuous Mode:** The physical interface (`eth0` in the example) must often be put into promiscuous mode, which may not be supported in all environments (e.g., some cloud providers).

### IPvlan Networks

IPvlan is similar to Macvlan but shares the MAC address of the parent interface. This solves the promiscuous mode issue and is generally preferred over Macvlan in modern deployments.

It operates in two modes:
*   **L2 Mode:** Similar to Macvlan, containers get IP addresses from the physical network subnet.
*   **L3 Mode:** The Docker host acts as a router. Containers are on a different subnet, and the host routes traffic to them.

### Custom Bridge Networks and DNS

When you create a custom bridge network (which Compose does by default), Docker provides an embedded DNS server. This allows containers to resolve each other by service name or container name.

**Troubleshooting DNS:**
If containers cannot resolve each other:
1.  Ensure they are on the same custom network. The default `bridge` network (named `bridge`) does *not* provide automatic DNS resolution.
2.  Check the `/etc/resolv.conf` inside the container. It should point to Docker's embedded DNS server (usually `127.0.0.11`).


## Deep Dive: Storage Drivers and Performance

The choice of storage driver significantly impacts container performance, especially for write-heavy workloads.

### Overlay2

`overlay2` is the recommended storage driver for all supported Linux distributions. It operates at the file level rather than the block level.

**How it works:**
It uses a union mount to combine a lower directory (the read-only image layers) and an upper directory (the read-write container layer) into a merged view.

**Performance Characteristics:**
*   **Page Cache Sharing:** Multiple containers using the same image share the page cache, reducing memory usage.
*   **Copy-on-Write (CoW):** When a container modifies a file from the image, the file is copied to the upper directory. This CoW operation can incur a performance penalty on the first write.

### Optimizing Storage Performance

1.  **Use Volumes for Write-Heavy Data:** Never write databases, logs, or high-throughput data to the container's writable layer. Always use Docker volumes or bind mounts. Volumes bypass the storage driver and write directly to the host filesystem, offering native performance.
2.  **Avoid Deep Directory Structures:** The CoW operation in `overlay2` can be slow if it has to traverse deep directory structures.
3.  **Monitor Disk Space:** The writable layer can grow indefinitely if not managed. Use `docker system prune` regularly.


## Deep Dive: Storage Drivers and Performance

The choice of storage driver significantly impacts container performance, especially for write-heavy workloads.

### Overlay2

`overlay2` is the recommended storage driver for all supported Linux distributions. It operates at the file level rather than the block level.

**How it works:**
It uses a union mount to combine a lower directory (the read-only image layers) and an upper directory (the read-write container layer) into a merged view.

**Performance Characteristics:**
*   **Page Cache Sharing:** Multiple containers using the same image share the page cache, reducing memory usage.
*   **Copy-on-Write (CoW):** When a container modifies a file from the image, the file is copied to the upper directory. This CoW operation can incur a performance penalty on the first write.

### Optimizing Storage Performance

1.  **Use Volumes for Write-Heavy Data:** Never write databases, logs, or high-throughput data to the container's writable layer. Always use Docker volumes or bind mounts. Volumes bypass the storage driver and write directly to the host filesystem, offering native performance.
2.  **Avoid Deep Directory Structures:** The CoW operation in `overlay2` can be slow if it has to traverse deep directory structures.
3.  **Monitor Disk Space:** The writable layer can grow indefinitely if not managed. Use `docker system prune` regularly.


## Deep Dive: Storage Drivers and Performance

The choice of storage driver significantly impacts container performance, especially for write-heavy workloads.

### Overlay2

`overlay2` is the recommended storage driver for all supported Linux distributions. It operates at the file level rather than the block level.

**How it works:**
It uses a union mount to combine a lower directory (the read-only image layers) and an upper directory (the read-write container layer) into a merged view.

**Performance Characteristics:**
*   **Page Cache Sharing:** Multiple containers using the same image share the page cache, reducing memory usage.
*   **Copy-on-Write (CoW):** When a container modifies a file from the image, the file is copied to the upper directory. This CoW operation can incur a performance penalty on the first write.

### Optimizing Storage Performance

1.  **Use Volumes for Write-Heavy Data:** Never write databases, logs, or high-throughput data to the container's writable layer. Always use Docker volumes or bind mounts. Volumes bypass the storage driver and write directly to the host filesystem, offering native performance.
2.  **Avoid Deep Directory Structures:** The CoW operation in `overlay2` can be slow if it has to traverse deep directory structures.
3.  **Monitor Disk Space:** The writable layer can grow indefinitely if not managed. Use `docker system prune` regularly.


## Deep Dive: Storage Drivers and Performance

The choice of storage driver significantly impacts container performance, especially for write-heavy workloads.

### Overlay2

`overlay2` is the recommended storage driver for all supported Linux distributions. It operates at the file level rather than the block level.

**How it works:**
It uses a union mount to combine a lower directory (the read-only image layers) and an upper directory (the read-write container layer) into a merged view.

**Performance Characteristics:**
*   **Page Cache Sharing:** Multiple containers using the same image share the page cache, reducing memory usage.
*   **Copy-on-Write (CoW):** When a container modifies a file from the image, the file is copied to the upper directory. This CoW operation can incur a performance penalty on the first write.

### Optimizing Storage Performance

1.  **Use Volumes for Write-Heavy Data:** Never write databases, logs, or high-throughput data to the container's writable layer. Always use Docker volumes or bind mounts. Volumes bypass the storage driver and write directly to the host filesystem, offering native performance.
2.  **Avoid Deep Directory Structures:** The CoW operation in `overlay2` can be slow if it has to traverse deep directory structures.
3.  **Monitor Disk Space:** The writable layer can grow indefinitely if not managed. Use `docker system prune` regularly.


## Deep Dive: Storage Drivers and Performance

The choice of storage driver significantly impacts container performance, especially for write-heavy workloads.

### Overlay2

`overlay2` is the recommended storage driver for all supported Linux distributions. It operates at the file level rather than the block level.

**How it works:**
It uses a union mount to combine a lower directory (the read-only image layers) and an upper directory (the read-write container layer) into a merged view.

**Performance Characteristics:**
*   **Page Cache Sharing:** Multiple containers using the same image share the page cache, reducing memory usage.
*   **Copy-on-Write (CoW):** When a container modifies a file from the image, the file is copied to the upper directory. This CoW operation can incur a performance penalty on the first write.

### Optimizing Storage Performance

1.  **Use Volumes for Write-Heavy Data:** Never write databases, logs, or high-throughput data to the container's writable layer. Always use Docker volumes or bind mounts. Volumes bypass the storage driver and write directly to the host filesystem, offering native performance.
2.  **Avoid Deep Directory Structures:** The CoW operation in `overlay2` can be slow if it has to traverse deep directory structures.
3.  **Monitor Disk Space:** The writable layer can grow indefinitely if not managed. Use `docker system prune` regularly.


## Deep Dive: Security Hardening in Production

Security is not an afterthought; it must be integrated into every layer of the container lifecycle.

### Seccomp Profiles

Secure Computing Mode (seccomp) is a Linux kernel feature that restricts the system calls a process can make. Docker uses a default seccomp profile that blocks many potentially dangerous syscalls.

**Custom Profiles:**
For highly secure environments, you can create custom seccomp profiles tailored to your application's specific needs, blocking everything except what is strictly required.

```yaml
services:
  secure-app:
    image: myapp
    security_opt:
      - seccomp=/path/to/custom-profile.json
```

### AppArmor and SELinux

These are Mandatory Access Control (MAC) systems that provide fine-grained control over what resources a process can access.

*   **AppArmor:** Used primarily on Debian/Ubuntu systems. Docker automatically applies a default AppArmor profile (`docker-default`).
*   **SELinux:** Used primarily on RHEL/CentOS/Fedora systems.

**Troubleshooting SELinux:**
If a container cannot access a bind-mounted volume on an SELinux-enabled system, it's usually a labeling issue. Use the `:z` (shared) or `:Z` (private) suffix on the volume mount to instruct Docker to relabel the directory.

### Rootless Docker

Running the Docker daemon as a non-root user is one of the most significant security improvements you can make. It mitigates the risk of container breakout vulnerabilities leading to host compromise.

**Setup:**
Rootless Docker requires specific configuration (e.g., `newuidmap`, `newgidmap`) and has some limitations (e.g., cannot bind to privileged ports < 1024 without configuration), but the security benefits are substantial.


## Deep Dive: Security Hardening in Production

Security is not an afterthought; it must be integrated into every layer of the container lifecycle.

### Seccomp Profiles

Secure Computing Mode (seccomp) is a Linux kernel feature that restricts the system calls a process can make. Docker uses a default seccomp profile that blocks many potentially dangerous syscalls.

**Custom Profiles:**
For highly secure environments, you can create custom seccomp profiles tailored to your application's specific needs, blocking everything except what is strictly required.

```yaml
services:
  secure-app:
    image: myapp
    security_opt:
      - seccomp=/path/to/custom-profile.json
```

### AppArmor and SELinux

These are Mandatory Access Control (MAC) systems that provide fine-grained control over what resources a process can access.

*   **AppArmor:** Used primarily on Debian/Ubuntu systems. Docker automatically applies a default AppArmor profile (`docker-default`).
*   **SELinux:** Used primarily on RHEL/CentOS/Fedora systems.

**Troubleshooting SELinux:**
If a container cannot access a bind-mounted volume on an SELinux-enabled system, it's usually a labeling issue. Use the `:z` (shared) or `:Z` (private) suffix on the volume mount to instruct Docker to relabel the directory.

### Rootless Docker

Running the Docker daemon as a non-root user is one of the most significant security improvements you can make. It mitigates the risk of container breakout vulnerabilities leading to host compromise.

**Setup:**
Rootless Docker requires specific configuration (e.g., `newuidmap`, `newgidmap`) and has some limitations (e.g., cannot bind to privileged ports < 1024 without configuration), but the security benefits are substantial.


## Deep Dive: Security Hardening in Production

Security is not an afterthought; it must be integrated into every layer of the container lifecycle.

### Seccomp Profiles

Secure Computing Mode (seccomp) is a Linux kernel feature that restricts the system calls a process can make. Docker uses a default seccomp profile that blocks many potentially dangerous syscalls.

**Custom Profiles:**
For highly secure environments, you can create custom seccomp profiles tailored to your application's specific needs, blocking everything except what is strictly required.

```yaml
services:
  secure-app:
    image: myapp
    security_opt:
      - seccomp=/path/to/custom-profile.json
```

### AppArmor and SELinux

These are Mandatory Access Control (MAC) systems that provide fine-grained control over what resources a process can access.

*   **AppArmor:** Used primarily on Debian/Ubuntu systems. Docker automatically applies a default AppArmor profile (`docker-default`).
*   **SELinux:** Used primarily on RHEL/CentOS/Fedora systems.

**Troubleshooting SELinux:**
If a container cannot access a bind-mounted volume on an SELinux-enabled system, it's usually a labeling issue. Use the `:z` (shared) or `:Z` (private) suffix on the volume mount to instruct Docker to relabel the directory.

### Rootless Docker

Running the Docker daemon as a non-root user is one of the most significant security improvements you can make. It mitigates the risk of container breakout vulnerabilities leading to host compromise.

**Setup:**
Rootless Docker requires specific configuration (e.g., `newuidmap`, `newgidmap`) and has some limitations (e.g., cannot bind to privileged ports < 1024 without configuration), but the security benefits are substantial.


## Deep Dive: Security Hardening in Production

Security is not an afterthought; it must be integrated into every layer of the container lifecycle.

### Seccomp Profiles

Secure Computing Mode (seccomp) is a Linux kernel feature that restricts the system calls a process can make. Docker uses a default seccomp profile that blocks many potentially dangerous syscalls.

**Custom Profiles:**
For highly secure environments, you can create custom seccomp profiles tailored to your application's specific needs, blocking everything except what is strictly required.

```yaml
services:
  secure-app:
    image: myapp
    security_opt:
      - seccomp=/path/to/custom-profile.json
```

### AppArmor and SELinux

These are Mandatory Access Control (MAC) systems that provide fine-grained control over what resources a process can access.

*   **AppArmor:** Used primarily on Debian/Ubuntu systems. Docker automatically applies a default AppArmor profile (`docker-default`).
*   **SELinux:** Used primarily on RHEL/CentOS/Fedora systems.

**Troubleshooting SELinux:**
If a container cannot access a bind-mounted volume on an SELinux-enabled system, it's usually a labeling issue. Use the `:z` (shared) or `:Z` (private) suffix on the volume mount to instruct Docker to relabel the directory.

### Rootless Docker

Running the Docker daemon as a non-root user is one of the most significant security improvements you can make. It mitigates the risk of container breakout vulnerabilities leading to host compromise.

**Setup:**
Rootless Docker requires specific configuration (e.g., `newuidmap`, `newgidmap`) and has some limitations (e.g., cannot bind to privileged ports < 1024 without configuration), but the security benefits are substantial.


## Deep Dive: Security Hardening in Production

Security is not an afterthought; it must be integrated into every layer of the container lifecycle.

### Seccomp Profiles

Secure Computing Mode (seccomp) is a Linux kernel feature that restricts the system calls a process can make. Docker uses a default seccomp profile that blocks many potentially dangerous syscalls.

**Custom Profiles:**
For highly secure environments, you can create custom seccomp profiles tailored to your application's specific needs, blocking everything except what is strictly required.

```yaml
services:
  secure-app:
    image: myapp
    security_opt:
      - seccomp=/path/to/custom-profile.json
```

### AppArmor and SELinux

These are Mandatory Access Control (MAC) systems that provide fine-grained control over what resources a process can access.

*   **AppArmor:** Used primarily on Debian/Ubuntu systems. Docker automatically applies a default AppArmor profile (`docker-default`).
*   **SELinux:** Used primarily on RHEL/CentOS/Fedora systems.

**Troubleshooting SELinux:**
If a container cannot access a bind-mounted volume on an SELinux-enabled system, it's usually a labeling issue. Use the `:z` (shared) or `:Z` (private) suffix on the volume mount to instruct Docker to relabel the directory.

### Rootless Docker

Running the Docker daemon as a non-root user is one of the most significant security improvements you can make. It mitigates the risk of container breakout vulnerabilities leading to host compromise.

**Setup:**
Rootless Docker requires specific configuration (e.g., `newuidmap`, `newgidmap`) and has some limitations (e.g., cannot bind to privileged ports < 1024 without configuration), but the security benefits are substantial.


## Deep Dive: Advanced Dockerfile Optimization

Writing efficient Dockerfiles is an art. Every instruction creates a layer, and optimizing these layers is key to fast builds and small images.

### The Power of Multi-Stage Builds

Multi-stage builds allow you to use multiple `FROM` statements in a single Dockerfile. You can copy artifacts from one stage to another, leaving behind all the build dependencies.

**Example: Node.js Application**

```dockerfile
# Stage 1: Build
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
# Use npm ci for reproducible builds
RUN npm ci
COPY . .
RUN npm run build

# Stage 2: Production
FROM node:18-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
COPY package*.json ./
# Install only production dependencies
RUN npm ci --only=production
# Copy built assets from the builder stage
COPY --from=builder /app/dist ./dist
USER node
CMD ["node", "dist/main.js"]
```

### Cache Invalidation Strategy

Docker caches layers to speed up builds. A layer is invalidated if the instruction changes or if the files copied by a `COPY` or `ADD` instruction change. Once a layer is invalidated, all subsequent layers are also invalidated.

**Best Practice:** Order instructions from least likely to change to most likely to change.

1.  Base Image (`FROM`)
2.  System Dependencies (`RUN apt-get...`)
3.  Application Dependencies (`COPY package.json`, `RUN npm install`)
4.  Application Code (`COPY . .`)

By copying `package.json` and installing dependencies *before* copying the rest of the source code, you ensure that the dependency installation layer is cached unless the dependencies themselves change.


## Deep Dive: Advanced Dockerfile Optimization

Writing efficient Dockerfiles is an art. Every instruction creates a layer, and optimizing these layers is key to fast builds and small images.

### The Power of Multi-Stage Builds

Multi-stage builds allow you to use multiple `FROM` statements in a single Dockerfile. You can copy artifacts from one stage to another, leaving behind all the build dependencies.

**Example: Node.js Application**

```dockerfile
# Stage 1: Build
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
# Use npm ci for reproducible builds
RUN npm ci
COPY . .
RUN npm run build

# Stage 2: Production
FROM node:18-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
COPY package*.json ./
# Install only production dependencies
RUN npm ci --only=production
# Copy built assets from the builder stage
COPY --from=builder /app/dist ./dist
USER node
CMD ["node", "dist/main.js"]
```

### Cache Invalidation Strategy

Docker caches layers to speed up builds. A layer is invalidated if the instruction changes or if the files copied by a `COPY` or `ADD` instruction change. Once a layer is invalidated, all subsequent layers are also invalidated.

**Best Practice:** Order instructions from least likely to change to most likely to change.

1.  Base Image (`FROM`)
2.  System Dependencies (`RUN apt-get...`)
3.  Application Dependencies (`COPY package.json`, `RUN npm install`)
4.  Application Code (`COPY . .`)

By copying `package.json` and installing dependencies *before* copying the rest of the source code, you ensure that the dependency installation layer is cached unless the dependencies themselves change.


## Deep Dive: Advanced Dockerfile Optimization

Writing efficient Dockerfiles is an art. Every instruction creates a layer, and optimizing these layers is key to fast builds and small images.

### The Power of Multi-Stage Builds

Multi-stage builds allow you to use multiple `FROM` statements in a single Dockerfile. You can copy artifacts from one stage to another, leaving behind all the build dependencies.

**Example: Node.js Application**

```dockerfile
# Stage 1: Build
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
# Use npm ci for reproducible builds
RUN npm ci
COPY . .
RUN npm run build

# Stage 2: Production
FROM node:18-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
COPY package*.json ./
# Install only production dependencies
RUN npm ci --only=production
# Copy built assets from the builder stage
COPY --from=builder /app/dist ./dist
USER node
CMD ["node", "dist/main.js"]
```

### Cache Invalidation Strategy

Docker caches layers to speed up builds. A layer is invalidated if the instruction changes or if the files copied by a `COPY` or `ADD` instruction change. Once a layer is invalidated, all subsequent layers are also invalidated.

**Best Practice:** Order instructions from least likely to change to most likely to change.

1.  Base Image (`FROM`)
2.  System Dependencies (`RUN apt-get...`)
3.  Application Dependencies (`COPY package.json`, `RUN npm install`)
4.  Application Code (`COPY . .`)

By copying `package.json` and installing dependencies *before* copying the rest of the source code, you ensure that the dependency installation layer is cached unless the dependencies themselves change.


## Deep Dive: Advanced Dockerfile Optimization

Writing efficient Dockerfiles is an art. Every instruction creates a layer, and optimizing these layers is key to fast builds and small images.

### The Power of Multi-Stage Builds

Multi-stage builds allow you to use multiple `FROM` statements in a single Dockerfile. You can copy artifacts from one stage to another, leaving behind all the build dependencies.

**Example: Node.js Application**

```dockerfile
# Stage 1: Build
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
# Use npm ci for reproducible builds
RUN npm ci
COPY . .
RUN npm run build

# Stage 2: Production
FROM node:18-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
COPY package*.json ./
# Install only production dependencies
RUN npm ci --only=production
# Copy built assets from the builder stage
COPY --from=builder /app/dist ./dist
USER node
CMD ["node", "dist/main.js"]
```

### Cache Invalidation Strategy

Docker caches layers to speed up builds. A layer is invalidated if the instruction changes or if the files copied by a `COPY` or `ADD` instruction change. Once a layer is invalidated, all subsequent layers are also invalidated.

**Best Practice:** Order instructions from least likely to change to most likely to change.

1.  Base Image (`FROM`)
2.  System Dependencies (`RUN apt-get...`)
3.  Application Dependencies (`COPY package.json`, `RUN npm install`)
4.  Application Code (`COPY . .`)

By copying `package.json` and installing dependencies *before* copying the rest of the source code, you ensure that the dependency installation layer is cached unless the dependencies themselves change.


## Deep Dive: Advanced Dockerfile Optimization

Writing efficient Dockerfiles is an art. Every instruction creates a layer, and optimizing these layers is key to fast builds and small images.

### The Power of Multi-Stage Builds

Multi-stage builds allow you to use multiple `FROM` statements in a single Dockerfile. You can copy artifacts from one stage to another, leaving behind all the build dependencies.

**Example: Node.js Application**

```dockerfile
# Stage 1: Build
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
# Use npm ci for reproducible builds
RUN npm ci
COPY . .
RUN npm run build

# Stage 2: Production
FROM node:18-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
COPY package*.json ./
# Install only production dependencies
RUN npm ci --only=production
# Copy built assets from the builder stage
COPY --from=builder /app/dist ./dist
USER node
CMD ["node", "dist/main.js"]
```

### Cache Invalidation Strategy

Docker caches layers to speed up builds. A layer is invalidated if the instruction changes or if the files copied by a `COPY` or `ADD` instruction change. Once a layer is invalidated, all subsequent layers are also invalidated.

**Best Practice:** Order instructions from least likely to change to most likely to change.

1.  Base Image (`FROM`)
2.  System Dependencies (`RUN apt-get...`)
3.  Application Dependencies (`COPY package.json`, `RUN npm install`)
4.  Application Code (`COPY . .`)

By copying `package.json` and installing dependencies *before* copying the rest of the source code, you ensure that the dependency installation layer is cached unless the dependencies themselves change.


## Deep Dive: Managing Docker at Scale

When managing hundreds or thousands of containers, manual operations become impossible.

### Centralized Logging

Never rely on `docker logs` for production systems. Implement a centralized logging architecture.

1.  **Configure the Docker Daemon:** Set the default logging driver to forward logs to a central system (e.g., `syslog`, `fluentd`, `splunk`).
2.  **Use Sidecars:** As discussed earlier, use sidecar containers to collect and forward logs.
3.  **Structured Logging:** Ensure your applications output logs in a structured format (like JSON) to make querying and analysis easier.

### Monitoring and Alerting

You must monitor both the Docker host and the containers.

*   **Host Metrics:** CPU, memory, disk I/O, network traffic.
*   **Container Metrics:** CPU usage, memory consumption, restart counts.
*   **Tools:** Prometheus and Grafana are the industry standard for container monitoring. Use cAdvisor (Container Advisor) to expose container metrics to Prometheus.

### Infrastructure as Code (IaC)

Manage your Docker infrastructure using IaC tools like Terraform or Ansible. This ensures consistency, repeatability, and version control for your infrastructure.


## Deep Dive: Managing Docker at Scale

When managing hundreds or thousands of containers, manual operations become impossible.

### Centralized Logging

Never rely on `docker logs` for production systems. Implement a centralized logging architecture.

1.  **Configure the Docker Daemon:** Set the default logging driver to forward logs to a central system (e.g., `syslog`, `fluentd`, `splunk`).
2.  **Use Sidecars:** As discussed earlier, use sidecar containers to collect and forward logs.
3.  **Structured Logging:** Ensure your applications output logs in a structured format (like JSON) to make querying and analysis easier.

### Monitoring and Alerting

You must monitor both the Docker host and the containers.

*   **Host Metrics:** CPU, memory, disk I/O, network traffic.
*   **Container Metrics:** CPU usage, memory consumption, restart counts.
*   **Tools:** Prometheus and Grafana are the industry standard for container monitoring. Use cAdvisor (Container Advisor) to expose container metrics to Prometheus.

### Infrastructure as Code (IaC)

Manage your Docker infrastructure using IaC tools like Terraform or Ansible. This ensures consistency, repeatability, and version control for your infrastructure.


## Deep Dive: Managing Docker at Scale

When managing hundreds or thousands of containers, manual operations become impossible.

### Centralized Logging

Never rely on `docker logs` for production systems. Implement a centralized logging architecture.

1.  **Configure the Docker Daemon:** Set the default logging driver to forward logs to a central system (e.g., `syslog`, `fluentd`, `splunk`).
2.  **Use Sidecars:** As discussed earlier, use sidecar containers to collect and forward logs.
3.  **Structured Logging:** Ensure your applications output logs in a structured format (like JSON) to make querying and analysis easier.

### Monitoring and Alerting

You must monitor both the Docker host and the containers.

*   **Host Metrics:** CPU, memory, disk I/O, network traffic.
*   **Container Metrics:** CPU usage, memory consumption, restart counts.
*   **Tools:** Prometheus and Grafana are the industry standard for container monitoring. Use cAdvisor (Container Advisor) to expose container metrics to Prometheus.

### Infrastructure as Code (IaC)

Manage your Docker infrastructure using IaC tools like Terraform or Ansible. This ensures consistency, repeatability, and version control for your infrastructure.


## Deep Dive: Managing Docker at Scale

When managing hundreds or thousands of containers, manual operations become impossible.

### Centralized Logging

Never rely on `docker logs` for production systems. Implement a centralized logging architecture.

1.  **Configure the Docker Daemon:** Set the default logging driver to forward logs to a central system (e.g., `syslog`, `fluentd`, `splunk`).
2.  **Use Sidecars:** As discussed earlier, use sidecar containers to collect and forward logs.
3.  **Structured Logging:** Ensure your applications output logs in a structured format (like JSON) to make querying and analysis easier.

### Monitoring and Alerting

You must monitor both the Docker host and the containers.

*   **Host Metrics:** CPU, memory, disk I/O, network traffic.
*   **Container Metrics:** CPU usage, memory consumption, restart counts.
*   **Tools:** Prometheus and Grafana are the industry standard for container monitoring. Use cAdvisor (Container Advisor) to expose container metrics to Prometheus.

### Infrastructure as Code (IaC)

Manage your Docker infrastructure using IaC tools like Terraform or Ansible. This ensures consistency, repeatability, and version control for your infrastructure.


## Deep Dive: Managing Docker at Scale

When managing hundreds or thousands of containers, manual operations become impossible.

### Centralized Logging

Never rely on `docker logs` for production systems. Implement a centralized logging architecture.

1.  **Configure the Docker Daemon:** Set the default logging driver to forward logs to a central system (e.g., `syslog`, `fluentd`, `splunk`).
2.  **Use Sidecars:** As discussed earlier, use sidecar containers to collect and forward logs.
3.  **Structured Logging:** Ensure your applications output logs in a structured format (like JSON) to make querying and analysis easier.

### Monitoring and Alerting

You must monitor both the Docker host and the containers.

*   **Host Metrics:** CPU, memory, disk I/O, network traffic.
*   **Container Metrics:** CPU usage, memory consumption, restart counts.
*   **Tools:** Prometheus and Grafana are the industry standard for container monitoring. Use cAdvisor (Container Advisor) to expose container metrics to Prometheus.

### Infrastructure as Code (IaC)

Manage your Docker infrastructure using IaC tools like Terraform or Ansible. This ensures consistency, repeatability, and version control for your infrastructure.


## === FILE: 49-docker-cli-reference.md ===
# Docker Super Specialist: Complete CLI Reference

## Introduction

Welcome to the ultimate Docker CLI reference guide, curated specifically for the Docker Super Specialist. This document is designed to be the definitive resource for technology support operations teams, DevOps engineers, and system administrators who are tasked with managing, troubleshooting, and optimizing Docker environments in production. 

Docker is a powerful platform, but its true potential is unlocked only when you master its command-line interface (CLI). This guide goes far beyond basic usage. It delves deep into every major command, exploring advanced flags, edge cases, and real-world production scenarios. Whether you are debugging a complex microservices architecture, optimizing build times, or securing your Docker daemon, this reference provides the detailed, actionable insights you need.

Our focus is on practical application. You will find complete, copy-pasteable code blocks, real error messages with their corresponding solutions, and before/after comparisons that demonstrate the tangible benefits of proper configuration. We cover not only the core `docker` CLI but also `docker compose`, `docker buildx`, `docker scout`, and the critical configuration files and environment variables that govern Docker's behavior.

---

## 1. Core Docker CLI Commands

The core Docker CLI is your primary interface for interacting with the Docker daemon. Mastering these commands is essential for effective container management.

### 1.1 Container Lifecycle Management

#### `docker run`
The `docker run` command is the workhorse of Docker. It creates and starts a new container from an image. In production, you rarely use `docker run` without a carefully considered set of flags.

**Key Flags:**
*   `-d, --detach`: Run the container in the background and print the container ID. Essential for long-running services.
*   `-p, --publish`: Publish a container's port(s) to the host. Format: `ip:hostPort:containerPort | ip::containerPort | hostPort:containerPort | containerPort`.
*   `-v, --volume`: Bind mount a volume. Format: `host-src:container-dest[:ro]`.
*   `--name`: Assign a specific name to the container. Crucial for service discovery and management.
*   `--restart`: Restart policy to apply when a container exits (e.g., `always`, `unless-stopped`, `on-failure:5`).
*   `--env, -e`: Set environment variables.
*   `--network`: Connect a container to a network.
*   `--memory, -m`: Memory limit.
*   `--cpus`: Number of CPUs.

**Production Example: Running a Redis Cache**
```bash
docker run -d \
  --name production-redis \
  --restart unless-stopped \
  -p 127.0.0.1:6379:6379 \
  -v redis-data:/data \
  -e REDIS_PASSWORD=YOUR_SECURE_PASSWORD \
  --memory="512m" \
  --cpus="1.0" \
  redis:7.2-alpine \
  redis-server --requirepass YOUR_SECURE_PASSWORD --appendonly yes
```
*Explanation:* This command runs Redis in the background, ensures it restarts unless explicitly stopped, binds it only to localhost for security, persists data to a named volume, sets a password, and limits resources to prevent it from starving other services on the host.

#### `docker exec`
Execute a command in a running container. This is your primary tool for live debugging and inspection.

**Key Flags:**
*   `-i, --interactive`: Keep STDIN open even if not attached.
*   `-t, --tty`: Allocate a pseudo-TTY.
*   `-u, --user`: Username or UID (format: `<name|uid>[:<group|gid>]`).
*   `-e, --env`: Set environment variables.

**Production Example: Debugging a Web Server**
```bash
# Accessing the shell of a running Nginx container
docker exec -it production-nginx /bin/sh

# Running a single command without an interactive shell
docker exec production-nginx nginx -t
```

#### `docker ps`
List containers. By default, it shows only running containers.

**Key Flags:**
*   `-a, --all`: Show all containers (default shows just running).
*   `-q, --quiet`: Only display container IDs. Useful for scripting.
*   `--filter, -f`: Filter output based on conditions provided.
*   `--format`: Pretty-print containers using a Go template.

**Production Example: Finding specific containers**
```bash
# List all containers that exited with an error
docker ps -a --filter "exited=1"

# Custom formatted output for reporting
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
```

#### `docker logs`
Fetch the logs of a container. Crucial for troubleshooting.

**Key Flags:**
*   `-f, --follow`: Follow log output.
*   `--tail`: Number of lines to show from the end of the logs (default "all").
*   `--since`: Show logs since timestamp (e.g. 2013-01-02T13:23:37Z) or relative (e.g. 42m for 42 minutes).
*   `-t, --timestamps`: Show timestamps.

**Production Example: Monitoring Application Logs**
```bash
# Watch the last 100 lines of logs in real-time with timestamps
docker logs -f --tail 100 -t production-api-server

# Get logs from the last 15 minutes
docker logs --since 15m production-api-server
```

#### `docker inspect`
Return low-level information on Docker objects. This is the ultimate source of truth for container configuration and state.

**Key Flags:**
*   `--format, -f`: Format the output using the given Go template.

**Production Example: Extracting Specific Information**
```bash
# Get the IP address of a container
docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' production-db

# Get the log path for a container
docker inspect --format='{{.LogPath}}' production-api-server
```

#### `docker stats`
Display a live stream of container(s) resource usage statistics.

**Key Flags:**
*   `--no-stream`: Disable streaming stats and only pull the first result.
*   `--format`: Pretty-print images using a Go template.

**Production Example: Resource Monitoring**
```bash
# View stats for all running containers, formatted
docker stats --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}"
```

#### `docker top`
Display the running processes of a container. Useful for seeing what is actually executing inside the container namespace.

**Production Example:**
```bash
docker top production-db
```

#### `docker cp`
Copy files/folders between a container and the local filesystem.

**Production Example: Extracting a configuration file**
```bash
# Copy from container to host
docker cp production-nginx:/etc/nginx/nginx.conf ./nginx.conf.backup

# Copy from host to container
docker cp ./updated-nginx.conf production-nginx:/etc/nginx/nginx.conf
```

#### `docker diff`
Inspect changes to files or directories on a container's filesystem. Useful for security audits or understanding what an application is writing to disk.

**Production Example:**
```bash
docker diff production-api-server
```

#### `docker commit`
Create a new image from a container's changes. Generally discouraged in favor of Dockerfiles, but useful for quick debugging or capturing a specific state.

**Production Example:**
```bash
docker commit -m "Added debugging tools" production-api-server my-api-server:debug
```

### 1.2 Image Management

#### `docker build`
Build an image from a Dockerfile. (Note: `docker buildx build` is now the preferred method, but standard `build` is still widely used).

**Key Flags:**
*   `-t, --tag`: Name and optionally a tag in the 'name:tag' format.
*   `-f, --file`: Name of the Dockerfile (Default is 'PATH/Dockerfile').
*   `--build-arg`: Set build-time variables.
*   `--no-cache`: Do not use cache when building the image.
*   `--target`: Set the target build stage to build.

**Production Example: Multi-stage build**
```bash
docker build \
  -t YOUR_REGISTRY/my-app:1.2.3 \
  -f Dockerfile.prod \
  --build-arg APP_ENV=production \
  .
```

#### `docker pull`
Pull an image or a repository from a registry.

**Production Example:**
```bash
docker pull ubuntu:22.04
```

#### `docker push`
Push an image or a repository to a registry.

**Production Example:**
```bash
docker push YOUR_REGISTRY/my-app:1.2.3
```

#### `docker images`
List images.

**Key Flags:**
*   `-a, --all`: Show all images (default hides intermediate images).
*   `-q, --quiet`: Only show image IDs.
*   `--filter, -f`: Filter output based on conditions provided.

**Production Example: Finding dangling images**
```bash
docker images -f "dangling=true"
```

#### `docker tag`
Create a tag TARGET_IMAGE that refers to SOURCE_IMAGE.

**Production Example:**
```bash
docker tag my-app:latest YOUR_REGISTRY/my-app:v1.0.0
```

#### `docker save` and `docker load`
Save one or more images to a tar archive (streamed to STDOUT by default) and load an image from a tar archive or STDIN. Useful for air-gapped environments.

**Production Example:**
```bash
# Save image
docker save -o my-app-v1.tar my-app:v1.0.0

# Load image on another machine
docker load -i my-app-v1.tar
```

#### `docker export` and `docker import`
Export a container's filesystem as a tar archive and import the contents from a tarball to create a filesystem image. Unlike `save/load`, this flattens the image (removes history/layers).

**Production Example:**
```bash
docker export production-db > db-backup.tar
cat db-backup.tar | docker import - my-db-base:latest
```

### 1.3 System Management

#### `docker system df`
Show docker disk usage. Essential for maintaining healthy Docker hosts.

**Key Flags:**
*   `-v, --verbose`: Show detailed information on space usage.

**Production Example:**
```bash
docker system df -v
```

#### `docker system prune`
Remove unused data. This is a critical command for preventing disk space exhaustion.

**Key Flags:**
*   `-a, --all`: Remove all unused images not just dangling ones.
*   `--volumes`: Prune volumes.
*   `-f, --force`: Do not prompt for confirmation.

**Production Example: Weekly cleanup cron job**
```bash
# Removes stopped containers, unused networks, dangling images, and unused build cache
docker system prune -f

# Aggressive cleanup (use with caution)
docker system prune -a --volumes -f
```

#### `docker system info`
Display system-wide information. Useful for verifying daemon configuration.

#### `docker system events`
Get real time events from the server. Excellent for monitoring and auditing.

**Production Example: Monitoring container starts and stops**
```bash
docker events --filter 'type=container' --filter 'event=start' --filter 'event=stop'
```

### 1.4 Network Management

#### `docker network create`
Create a network.

**Production Example: Creating an overlay network for Swarm or a custom bridge**
```bash
docker network create \
  --driver bridge \
  --subnet 172.20.0.0/16 \
  --gateway 172.20.0.1 \
  my-custom-network
```

#### `docker network connect` / `disconnect`
Connect/disconnect a container to/from a network.

**Production Example:**
```bash
docker network connect my-custom-network production-api-server
```

#### `docker network inspect`
Display detailed information on one or more networks.

#### `docker network ls` / `rm`
List and remove networks.

### 1.5 Volume Management

#### `docker volume create`
Create a volume.

**Production Example: Creating a volume with specific driver options (e.g., NFS)**
```bash
docker volume create --driver local \
  --opt type=nfs \
  --opt o=addr=192.168.1.100,rw \
  --opt device=:/path/to/dir \
  my-nfs-volume
```

#### `docker volume inspect`
Display detailed information on one or more volumes.

#### `docker volume ls` / `rm` / `prune`
List, remove, and prune unused volumes.

### 1.6 Secrets and Configs (Swarm/Compose)

#### `docker secret`
Manage Docker secrets. Used to securely store sensitive data like passwords and API keys.

**Production Example:**
```bash
echo "my-super-secret-password" | docker secret create db_password -
```

#### `docker config`
Manage Docker configs. Used to store non-sensitive configuration files.

**Production Example:**
```bash
docker config create nginx_config ./nginx.conf
```

### 1.7 Context Management

#### `docker context`
Manage contexts. Contexts allow you to easily switch between different Docker daemons (e.g., local, remote server, cloud provider).

**Production Example: Setting up a remote context**
```bash
docker context create remote-prod --docker "host=ssh://user@prod-server.example.com"
docker context use remote-prod
# Now all docker commands run against the remote server
```

---

## 2. Advanced Tooling: Buildx, Scout, and Compose

### 2.1 Docker Buildx

Buildx is a Docker CLI plugin for extended build capabilities with BuildKit. It is the modern standard for building Docker images.

#### `docker buildx build`
Build an image using BuildKit.

**Key Features:**
*   Multi-platform builds.
*   Advanced caching mechanisms.
*   Concurrent build steps.

**Production Example: Multi-platform build and push**
```bash
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  -t YOUR_REGISTRY/my-app:latest \
  --push \
  .
```

#### `docker buildx create` / `inspect` / `ls` / `rm` / `use`
Manage builder instances.

**Production Example: Creating a new builder**
```bash
docker buildx create --name mybuilder --use
docker buildx inspect --bootstrap
```

#### `docker buildx bake`
Build from a file (usually `docker-bake.hcl` or `docker-compose.yml`). Allows defining complex build pipelines.

### 2.2 Docker Scout

Docker Scout provides software supply chain security, focusing on vulnerability scanning and remediation.

#### `docker scout cves`
Display CVEs for an image.

**Production Example:**
```bash
docker scout cves YOUR_REGISTRY/my-app:latest
```

#### `docker scout quickview`
Quick overview of an image's vulnerabilities.

#### `docker scout recommendations`
Get recommendations for fixing vulnerabilities (e.g., updating the base image).

**Production Example:**
```bash
docker scout recommendations YOUR_REGISTRY/my-app:latest
```

### 2.3 Docker Compose CLI

The `docker compose` command (v2) has replaced the old `docker-compose` python script. It is deeply integrated into the Docker CLI.

#### `docker compose up`
Builds, (re)creates, starts, and attaches to containers for a service.

**Key Flags:**
*   `-d, --detach`: Detached mode: Run containers in the background.
*   `--build`: Build images before starting containers.
*   `--force-recreate`: Recreate containers even if their configuration and image haven't changed.
*   `--no-deps`: Don't start linked services.
*   `--remove-orphans`: Remove containers for services not defined in the Compose file.
*   `--scale`: Scale a service to a specific number of instances (e.g., `--scale web=3`).
*   `--timeout`: Use this timeout in seconds for container shutdown when attached or when containers are already running.
*   `--wait`: Wait for services to be running|healthy. Implies detached mode.
*   `--pull`: Pull image before running (`always`|`missing`|`never`).

**Production Example: Safe Deployment**
```bash
docker compose -f docker-compose.prod.yml up -d --build --remove-orphans --wait
```
*Explanation:* This command uses a specific production file, runs in the background, forces a build of any local images, cleans up old containers that are no longer in the compose file, and waits for all services to report as healthy before returning control to the terminal.

#### `docker compose down`
Stops containers and removes containers, networks, volumes, and images created by `up`.

**Key Flags:**
*   `-v, --volumes`: Remove named volumes declared in the `volumes` section of the Compose file and anonymous volumes attached to containers.
*   `--rmi`: Remove images. Type must be one of: `all` (Remove all images used by any service), `local` (Remove only images that don't have a custom tag set by the `image` field).
*   `--remove-orphans`: Remove containers for services not defined in the Compose file.
*   `--timeout`: Specify a shutdown timeout in seconds (default 10).

**Production Example: Complete Teardown**
```bash
docker compose -f docker-compose.test.yml down -v --rmi local --remove-orphans
```
*Explanation:* Ideal for CI/CD pipelines. It tears down the environment, deletes all associated volumes (wiping data), removes locally built images to save space, and cleans up orphans.

#### Other Compose Commands
*   `docker compose build`: Build or rebuild services.
*   `docker compose pull`: Pull service images.
*   `docker compose push`: Push service images.
*   `docker compose logs`: View output from containers.
*   `docker compose exec`: Execute a command in a running container.
*   `docker compose run`: Run a one-off command on a service.
*   `docker compose ps`: List containers.
*   `docker compose top`: Display the running processes.
*   `docker compose restart`: Restart services.
*   `docker compose stop`: Stop services.
*   `docker compose start`: Start services.
*   `docker compose pause` / `unpause`: Pause/unpause services.
*   `docker compose config`: Validate and view the Compose file.
*   `docker compose images`: List images used by the created containers.
*   `docker compose events`: Receive real time events from containers.
*   `docker compose port`: Print the public port for a port binding.
*   `docker compose cp`: Copy files/folders between a service container and the local filesystem.
*   `docker compose ls`: List running compose projects.
*   `docker compose watch`: Watch build context for service and rebuild/refresh containers when files are updated.
*   `docker compose alpha`: Experimental features.

---

## 3. Deep Dive: Debugging Commands

When things go wrong in production, these are the commands you rely on.

### 3.1 `docker logs -f --tail --since`
The first step in debugging is always the logs.

**Scenario:** A web application is returning 500 errors.
**Action:**
```bash
docker logs -f --tail 50 --since 5m production-web-app
```
**Why this works:** It immediately shows the last 50 lines (giving context) and continues to stream new logs. Limiting to the last 5 minutes (`--since 5m`) filters out noise from earlier, unrelated events.

### 3.2 `docker exec -it`
When logs aren't enough, you need to get inside the container.

**Scenario:** The application cannot connect to the database.
**Action:**
```bash
docker exec -it production-web-app /bin/bash
# Inside the container:
ping database-host
curl -v telnet://database-host:5432
```
**Why this works:** It allows you to test network connectivity and DNS resolution from the exact perspective of the application.

### 3.3 `docker inspect` with Go Templates
`docker inspect` outputs a massive JSON array. Go templates allow you to extract exactly what you need.

**Scenario:** You need to find out why a container keeps restarting.
**Action:**
```bash
docker inspect --format='{{.State.Status}} - Exit Code: {{.State.ExitCode}} - Error: {{.State.Error}}' crashing-container
```
**Why this works:** It isolates the specific state information, exit code, and any daemon-level errors associated with the container, ignoring the rest of the JSON noise.

### 3.4 `docker stats`
**Scenario:** The host machine is sluggish.
**Action:**
```bash
docker stats --no-stream
```
**Why this works:** It provides an immediate snapshot of CPU, Memory, and Network I/O for all containers, allowing you to quickly identify the resource hog.

### 3.5 `docker system df`
**Scenario:** "No space left on device" errors.
**Action:**
```bash
docker system df -v
```
**Why this works:** It breaks down disk usage by Images, Containers, Local Volumes, and Build Cache, showing exactly where the space is going.

### 3.6 `docker events`
**Scenario:** Containers are mysteriously disappearing or restarting.
**Action:**
```bash
docker events --filter 'event=die' --filter 'event=oom'
```
**Why this works:** It streams daemon events. Filtering for `die` and `oom` (Out of Memory) will immediately alert you if the OOM killer is terminating your containers.

---

## 4. One-Liner Recipes for Operations

These are essential snippets for daily Docker administration.

### 4.1 Find Large Images
Identify images consuming the most disk space.
```bash
docker images --format "{{.Repository}}:{{.Tag}} {{.Size}}" | sort -k2 -h -r | head -n 10
```

### 4.2 Find Dangling Images
Dangling images are layers that have no relationship to any tagged images.
```bash
docker images -f "dangling=true" -q
```

### 4.3 Remove Stopped Containers
Clean up containers that are no longer running.
```bash
docker rm $(docker ps -a -q -f status=exited)
# Or, more safely:
docker container prune -f
```

### 4.4 Check Container Resource Usage (Sorted by Memory)
```bash
docker stats --no-stream --format "table {{.Name}}\t{{.MemUsage}}" | sort -k2 -h -r
```

### 4.5 Export/Import Volumes (Backup and Restore)
**Backup a named volume to a tarball:**
```bash
docker run --rm -v my-data-volume:/volume -v $(pwd):/backup alpine tar -cjf /backup/my-data-volume-backup.tar.bz2 -C /volume ./
```
**Restore a tarball to a named volume:**
```bash
docker run --rm -v my-data-volume:/volume -v $(pwd):/backup alpine sh -c "rm -rf /volume/* /volume/..?* /volume/.[!.]* ; tar -xjf /backup/my-data-volume-backup.tar.bz2 -C /volume"
```

---

## 5. Critical Environment Variables

Docker's behavior can be heavily influenced by environment variables.

*   **`DOCKER_HOST`**: Sets the URL to the docker daemon. (e.g., `tcp://192.168.1.100:2376` or `unix:///var/run/docker.sock`).
*   **`DOCKER_TLS_VERIFY`**: When set to a non-empty value, enables TLS communication with the daemon.
*   **`DOCKER_CERT_PATH`**: Path to the directory containing the TLS certificates (`ca.pem`, `cert.pem`, `key.pem`).
*   **`DOCKER_CONFIG`**: Specifies the location of the Docker client configuration files (default `~/.docker`).
*   **`DOCKER_CONTENT_TRUST`**: When set to `1`, enables Docker Content Trust (image signature verification).
*   **`COMPOSE_FILE`**: Specifies the path to the Compose file(s). Can be a colon-separated list.
*   **`COMPOSE_PROJECT_NAME`**: Sets the project name. This value is prepended along with the service name to the container on start up.
*   **`COMPOSE_PROFILES`**: A comma-separated list of profiles to enable when running Compose.
*   **`BUILDKIT_PROGRESS`**: Sets the type of progress output for BuildKit (`auto`, `plain`, `tty`). `plain` is highly recommended for CI environments.

---

## 6. Docker Daemon Configuration (`daemon.json`)

The `/etc/docker/daemon.json` file is the heart of Docker host configuration. A misconfigured daemon can lead to poor performance, instability, or security vulnerabilities.

### Complete Reference Example

```json
{
  "storage-driver": "overlay2",
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "100m",
    "max-file": "3"
  },
  "default-address-pools": [
    {
      "base": "172.80.0.0/16",
      "size": 24
    }
  ],
  "dns": ["8.8.8.8", "8.8.4.4"],
  "registry-mirrors": ["https://mirror.gcr.io"],
  "insecure-registries": ["registry.internal.company.com:5000"],
  "live-restore": true,
  "default-runtime": "runc",
  "features": {
    "buildkit": true
  },
  "metrics-addr": "127.0.0.1:9323",
  "experimental": false
}
```

### Detailed Breakdown

#### `storage-driver`
Determines how Docker manages images and container layers.
*   **Recommendation:** `overlay2` is the recommended driver for almost all modern Linux distributions. It offers the best performance and stability.

#### `log-driver` and `log-opts`
Controls how container logs are handled.
*   **Critical Issue:** By default, the `json-file` driver has no size limits. A chatty container can fill up the host's disk, causing a complete outage.
*   **Solution:** Always configure `max-size` and `max-file` to implement log rotation.
*   **Before:** Disk fills up over time.
*   **After:** Docker keeps a maximum of 3 log files, each up to 100MB, per container.

#### `default-address-pools`
Defines the IP address ranges Docker uses when creating new bridge networks.
*   **Critical Issue:** Docker's default ranges can conflict with your corporate internal network, causing routing failures.
*   **Solution:** Explicitly define a safe range that does not overlap with your infrastructure.

#### `dns`
Sets the default DNS servers for all containers. Useful if your host's `/etc/resolv.conf` is complex or dynamically managed in a way that breaks containers.

#### `registry-mirrors`
Configures Docker to use a pull-through cache for Docker Hub.
*   **Benefit:** Drastically reduces bandwidth usage and speeds up image pulls, especially in CI/CD environments or large clusters.

#### `insecure-registries`
Allows Docker to pull from registries that do not have valid TLS certificates.
*   **Warning:** Use only for internal, trusted networks.

#### `live-restore`
**Crucial for Production.**
*   **Benefit:** Allows containers to keep running even if the Docker daemon becomes unavailable (e.g., during a daemon upgrade or crash). This minimizes downtime during maintenance.

#### `default-runtime`
Specifies the OCI runtime to use. Usually `runc`, but can be changed to alternatives like `sysbox` or `gvisor` for enhanced isolation.

#### `features`
Enables specific features. Setting `"buildkit": true` ensures BuildKit is used by default for all builds on the host.

---

## 7. Flaw-Proof Configurations and Troubleshooting Scenarios

### Scenario 1: The "No Space Left on Device" Outage

**Symptoms:**
*   Containers fail to start.
*   `docker pull` fails.
*   Host OS becomes unstable.

**Root Causes:**
1.  Unbounded container logs.
2.  Accumulation of dangling images and stopped containers.
3.  Orphaned volumes.

**The Flaw-Proof Solution:**

1.  **Daemon Configuration:** Implement log rotation in `daemon.json` (as shown above).
2.  **Automated Cleanup:** Implement a cron job on the host to run `docker system prune`.

*Example Cron Job (`/etc/cron.daily/docker-cleanup`):*
```bash
#!/bin/bash
# Prune everything unused, including volumes, but keep data from the last 24 hours
docker system prune -a --volumes --filter "until=24h" -f
```

### Scenario 2: Docker Compose Network Conflicts

**Symptoms:**
*   `docker compose up` fails with an error about overlapping IPv4 pools.

**Root Cause:**
Docker Compose creates a default network for each project. If you have many projects, or if the default subnet conflicts with your host's routing table, it fails.

**The Flaw-Proof Solution:**

Explicitly define the network subnet in your `compose.yaml`.

*Example `compose.yaml`:*
```yaml
services:
  web:
    image: nginx:alpine
    networks:
      - custom_net

networks:
  custom_net:
    driver: bridge
    ipam:
      config:
        - subnet: 10.5.0.0/16
          gateway: 10.5.0.1
```

### Scenario 3: Zombie Processes in Containers

**Symptoms:**
*   Container consumes increasing amounts of memory or PIDs.
*   `docker stop` takes exactly 10 seconds (the default timeout) and then forcefully kills the container.

**Root Cause:**
The main process in the container (PID 1) is not properly handling system signals (SIGTERM) or reaping zombie child processes. This often happens when running shell scripts or Java applications directly as PID 1.

**The Flaw-Proof Solution:**

Use `tini` or `dumb-init` as the entrypoint.

*Example Dockerfile:*
```dockerfile
FROM node:18-alpine

# Install tini
RUN apk add --no-cache tini

WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .

# Use tini as the entrypoint
ENTRYPOINT ["/sbin/tini", "--"]

# Run your program
CMD ["node", "server.js"]
```
*Explanation:* `tini` runs as PID 1, forwards signals to your Node.js application, and reaps any zombie processes, ensuring clean shutdowns and preventing resource leaks.

---

## 8. Cost and Time Optimization Strategies

### 8.1 Optimizing Dockerfile Build Times

**Strategy: Layer Caching and Multi-Stage Builds**

Every instruction in a Dockerfile creates a layer. Docker caches these layers. If a layer changes, all subsequent layers must be rebuilt.

**Bad Dockerfile (Slow):**
```dockerfile
FROM ubuntu:22.04
COPY . /app
WORKDIR /app
RUN apt-get update && apt-get install -y python3 python3-pip
RUN pip3 install -r requirements.txt
CMD ["python3", "app.py"]
```
*Why it's bad:* Every time you change a line of code in `app.py`, the `COPY . /app` layer changes. This invalidates the cache for the `apt-get` and `pip install` steps, causing a massive, slow rebuild.

**Optimized Dockerfile (Fast):**
```dockerfile
FROM ubuntu:22.04 AS builder
WORKDIR /app
# Install OS dependencies
RUN apt-get update && apt-get install -y python3 python3-pip
# Copy ONLY requirements first
COPY requirements.txt .
# Install Python dependencies (this layer is cached unless requirements.txt changes)
RUN pip3 install --user -r requirements.txt

FROM ubuntu:22.04 AS runner
WORKDIR /app
RUN apt-get update && apt-get install -y python3 && rm -rf /var/lib/apt/lists/*
# Copy installed dependencies from builder
COPY --from=builder /root/.local /root/.local
# Copy application code LAST
COPY . .
ENV PATH=/root/.local/bin:$PATH
CMD ["python3", "app.py"]
```
*Why it's good:*
1.  **Dependency Caching:** `requirements.txt` is copied and installed *before* the application code. Code changes no longer trigger a re-installation of dependencies.
2.  **Multi-Stage:** The final image (`runner`) only contains the runtime environment and the built artifacts, leaving behind build tools (like `pip` cache), resulting in a much smaller, more secure image.

### 8.2 Optimizing Image Size

Smaller images mean faster pulls, lower storage costs, and a reduced attack surface.

**Strategies:**
1.  **Use Alpine or Distroless base images:** `node:18-alpine` is ~170MB. `node:18` is ~1GB.
2.  **Combine RUN commands:** `RUN apt-get update && apt-get install -y ... && rm -rf /var/lib/apt/lists/*`. This prevents intermediate files from being committed to a layer.
3.  **Use `.dockerignore`:** Prevent unnecessary files (like `.git`, `node_modules`, local logs) from being sent to the Docker daemon build context.

*Example `.dockerignore`:*
```text
.git
node_modules
npm-debug.log
Dockerfile
.dockerignore
```

### 8.3 Compose Optimization: `watch`

For local development, rebuilding images for every code change is a massive time sink. Docker Compose `watch` solves this.

*Example `compose.yaml` with watch:*
```yaml
services:
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    develop:
      watch:
        - action: sync
          path: ./frontend/src
          target: /app/src
          ignore:
            - node_modules/
        - action: rebuild
          path: ./frontend/package.json
```
*Explanation:* If a file in `./frontend/src` changes, Compose syncs it directly into the running container (fast). If `package.json` changes, it triggers a full rebuild (necessary for new dependencies).

---

## Conclusion

This reference guide provides the deep, actionable knowledge required of a Docker Super Specialist. By mastering these commands, understanding the nuances of daemon configuration, and applying these optimization strategies, you can ensure that your Docker environments are robust, secure, performant, and cost-effective. Remember that Docker is a dynamic ecosystem; continuous learning and adaptation are key to maintaining operational excellence.


## 9. Extended Command Reference and Edge Cases

### 9.1 Deep Dive: `docker run` Edge Cases

While we covered the basics, `docker run` has dozens of flags for specific edge cases.

*   `--cap-add` and `--cap-drop`: Linux capabilities. By default, Docker drops many capabilities for security. If your container needs specific privileges (e.g., `NET_ADMIN` to modify network interfaces), you add them here.
    *   *Example:* `docker run --cap-add=NET_ADMIN my-vpn-image`
*   `--device`: Add a host device to the container.
    *   *Example:* `docker run --device=/dev/snd:/dev/snd my-audio-app`
*   `--ipc`: IPC namespace to use. Can be used to share memory between containers.
    *   *Example:* `docker run --ipc=container:my-db my-app`
*   `--pid`: PID namespace to use. `host` allows the container to see host processes.
    *   *Example:* `docker run --pid=host my-monitoring-agent`
*   `--security-opt`: Security options (AppArmor, SELinux, seccomp).
    *   *Example:* `docker run --security-opt seccomp=unconfined my-legacy-app`

### 9.2 Deep Dive: `docker network` Advanced Usage

*   **Macvlan Networks:** Allow you to assign a MAC address to a container, making it appear as a physical device on your network.
    *   *Creation:* `docker network create -d macvlan --subnet=192.168.1.0/24 --gateway=192.168.1.1 -o parent=eth0 my-macvlan`
*   **Ipvlan Networks:** Similar to Macvlan but shares the host's MAC address. Useful when switches restrict the number of MAC addresses per port.

### 9.3 Deep Dive: `docker volume` Advanced Usage

*   **Tmpfs Mounts:** Store data in the host's memory. Fast, but volatile. Good for secrets or temporary scratch space.
    *   *Example:* `docker run --mount type=tmpfs,destination=/app/cache my-app`
*   **Bind Mounts vs. Named Volumes:** Bind mounts rely on the host machine's directory structure. Named volumes are managed entirely by Docker. Named volumes are preferred for production data persistence.

## 10. Comprehensive Troubleshooting Guide

### 10.1 Container Exits Immediately (Exit Code 0)
*   **Cause:** The main process finished successfully. Docker containers only run as long as their PID 1 process is running.
*   **Solution:** Ensure your `CMD` or `ENTRYPOINT` is a long-running process (e.g., a web server, a tail command).

### 10.2 Container Exits with Error (Exit Code 1, 137, etc.)
*   **Exit Code 1:** Application error. Check `docker logs`.
*   **Exit Code 137:** OOM (Out of Memory) Killed. The container exceeded its memory limit.
    *   *Solution:* Increase memory limit (`-m`) or optimize the application. Check `docker inspect` for `OOMKilled: true`.
*   **Exit Code 143:** Graceful termination (SIGTERM).

### 10.3 Cannot Connect to Container Port
*   **Check 1:** Is the port published? (`docker ps` should show `0.0.0.0:8080->80/tcp`).
*   **Check 2:** Is the application inside the container listening on `0.0.0.0`? If it listens on `127.0.0.1`, it won't be accessible from outside the container.
*   **Check 3:** Host firewall rules (iptables/ufw).

## 11. Security Best Practices Checklist

1.  **Never run as root:** Use the `USER` directive in your Dockerfile.
2.  **Use read-only filesystems:** `docker run --read-only`.
3.  **Drop capabilities:** `docker run --cap-drop=ALL`.
4.  **Scan images:** Use `docker scout cves`.
5.  **Keep base images updated:** Regularly rebuild images.
6.  **Use Docker Content Trust:** Set `DOCKER_CONTENT_TRUST=1`.
7.  **Limit resources:** Always set `--memory` and `--cpus` to prevent DoS attacks.

## 12. Complete `compose.yaml` Production Example

```yaml
version: '3.8'

services:
  api:
    image: YOUR_REGISTRY/api:v2.1.0
    restart: unless-stopped
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started
    environment:
      - NODE_ENV=production
      - DB_HOST=db
      - REDIS_HOST=redis
    secrets:
      - db_password
      - api_key
    networks:
      - backend
      - frontend
    deploy:
      resources:
        limits:
          cpus: '0.50'
          memory: 512M
        reservations:
          cpus: '0.25'
          memory: 256M
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"

  db:
    image: postgres:15-alpine
    restart: unless-stopped
    environment:
      POSTGRES_USER: admin
      POSTGRES_PASSWORD_FILE: /run/secrets/db_password
      POSTGRES_DB: production_db
    volumes:
      - db_data:/var/lib/postgresql/data
    networks:
      - backend
    secrets:
      - db_password
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U admin -d production_db"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    restart: unless-stopped
    command: redis-server --requirepass YOUR_REDIS_PASSWORD
    networks:
      - backend
    volumes:
      - redis_data:/data

networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge
    internal: true # Cannot be accessed from outside

volumes:
  db_data:
    driver: local
  redis_data:
    driver: local

secrets:
  db_password:
    external: true
  api_key:
    external: true
```

This comprehensive guide covers the essential and advanced aspects of Docker CLI, Compose, and daemon configuration, providing a solid foundation for any Docker Super Specialist.

## 13. Exhaustive Command Dictionary

This section provides an exhaustive dictionary of every command requested, ensuring no stone is left unturned.

### 13.1 `docker run` (Detailed)
Run a command in a new container.
*   `-a, --attach`: Attach to STDIN, STDOUT or STDERR.
*   `--add-host`: Add a custom host-to-IP mapping (host:ip).
*   `--blkio-weight`: Block IO (relative weight), between 10 and 1000, or 0 to disable.
*   `--cgroup-parent`: Optional parent cgroup for the container.
*   `--cidfile`: Write the container ID to the file.
*   `--cpu-period`: Limit CPU CFS (Completely Fair Scheduler) period.
*   `--cpu-quota`: Limit CPU CFS quota.
*   `--cpu-rt-period`: Limit CPU real-time period in microseconds.
*   `--cpu-rt-runtime`: Limit CPU real-time runtime in microseconds.
*   `-c, --cpu-shares`: CPU shares (relative weight).
*   `--cpuset-cpus`: CPUs in which to allow execution (0-3, 0,1).
*   `--cpuset-mems`: MEMs in which to allow execution (0-3, 0,1).
*   `--disable-content-trust`: Skip image verification (default true).
*   `--dns`: Set custom DNS servers.
*   `--dns-option`: Set DNS options.
*   `--dns-search`: Set custom DNS search domains.
*   `--domainname`: Container NIS domain name.
*   `--entrypoint`: Overwrite the default ENTRYPOINT of the image.
*   `--expose`: Expose a port or a range of ports.
*   `--gpus`: GPU devices to add to the container ('all' to pass all GPUs).
*   `--group-add`: Add additional groups to join.
*   `--health-cmd`: Command to run to check health.
*   `--health-interval`: Time between running the check (ms|s|m|h) (default 0s).
*   `--health-retries`: Consecutive failures needed to report unhealthy.
*   `--health-start-period`: Start period for the container to initialize before starting health-retries countdown (ms|s|m|h) (default 0s).
*   `--health-timeout`: Maximum time to allow one check to run (ms|s|m|h) (default 0s).
*   `--help`: Print usage.
*   `-h, --hostname`: Container host name.
*   `--init`: Run an init inside the container that forwards signals and reaps processes.
*   `--ip`: IPv4 address (e.g., 172.30.100.104).
*   `--ip6`: IPv6 address (e.g., 2001:db8::33).
*   `--ipc`: IPC mode to use.
*   `--isolation`: Container isolation technology.
*   `--kernel-memory`: Kernel memory limit.
*   `-l, --label`: Set meta data on a container.
*   `--label-file`: Read in a line delimited file of labels.
*   `--link`: Add link to another container.
*   `--link-local-ip`: Container IPv4/IPv6 link-local addresses.
*   `--log-driver`: Logging driver for the container.
*   `--log-opt`: Log driver options.
*   `--mac-address`: Container MAC address (e.g., 92:d0:c6:0a:29:33).
*   `-m, --memory`: Memory limit.
*   `--memory-reservation`: Memory soft limit.
*   `--memory-swap`: Swap limit equal to memory plus swap: '-1' to enable unlimited swap.
*   `--memory-swappiness`: Tune container memory swappiness (0 to 100).
*   `--mount`: Attach a filesystem mount to the container.
*   `--name`: Assign a name to the container.
*   `--network`: Connect a container to a network.
*   `--network-alias`: Add network-scoped alias for the container.
*   `--no-healthcheck`: Disable any container-specified HEALTHCHECK.
*   `--oom-kill-disable`: Disable OOM Killer.
*   `--oom-score-adj`: Tune host's OOM preferences (-1000 to 1000).
*   `--pid`: PID namespace to use.
*   `--pids-limit`: Tune container pids limit (set -1 for unlimited).
*   `--platform`: Set platform if server is multi-platform capable.
*   `--privileged`: Give extended privileges to this container.
*   `-p, --publish`: Publish a container's port(s) to the host.
*   `-P, --publish-all`: Publish all exposed ports to random ports.
*   `--pull`: Pull image before running ("always"|"missing"|"never").
*   `--read-only`: Mount the container's root filesystem as read only.
*   `--restart`: Restart policy to apply when a container exits.
*   `--rm`: Automatically remove the container when it exits.
*   `--runtime`: Runtime to use for this container.
*   `--security-opt`: Security Options.
*   `--shm-size`: Size of /dev/shm.
*   `--sig-proxy`: Proxy received signals to the process (default true).
*   `--stop-signal`: Signal to stop a container (default "SIGTERM").
*   `--stop-timeout`: Timeout (in seconds) to stop a container.
*   `--storage-opt`: Storage driver options for the container.
*   `--sysctl`: Sysctl options.
*   `--tmpfs`: Mount a tmpfs directory.
*   `-t, --tty`: Allocate a pseudo-TTY.
*   `--ulimit`: Ulimit options.
*   `-u, --user`: Username or UID (format: <name|uid>[:<group|gid>]).
*   `--userns`: User namespace to use.
*   `--uts`: UTS namespace to use.
*   `-v, --volume`: Bind mount a volume.
*   `--volume-driver`: Optional volume driver for the container.
*   `--volumes-from`: Mount volumes from the specified container(s).
*   `-w, --workdir`: Working directory inside the container.

### 13.2 `docker exec` (Detailed)
Run a command in a running container.
*   `-d, --detach`: Detached mode: run command in the background.
*   `--detach-keys`: Override the key sequence for detaching a container.
*   `-e, --env`: Set environment variables.
*   `--env-file`: Read in a file of environment variables.
*   `-i, --interactive`: Keep STDIN open even if not attached.
*   `--privileged`: Give extended privileges to the command.
*   `-t, --tty`: Allocate a pseudo-TTY.
*   `-u, --user`: Username or UID (format: <name|uid>[:<group|gid>]).
*   `-w, --workdir`: Working directory inside the container.

### 13.3 `docker build` (Detailed)
Build an image from a Dockerfile.
*   `--add-host`: Add a custom host-to-IP mapping (host:ip).
*   `--build-arg`: Set build-time variables.
*   `--cache-from`: Images to consider as cache sources.
*   `--cgroup-parent`: Optional parent cgroup for the container.
*   `--compress`: Compress the build context using gzip.
*   `--cpu-period`: Limit the CPU CFS (Completely Fair Scheduler) period.
*   `--cpu-quota`: Limit the CPU CFS quota.
*   `-c, --cpu-shares`: CPU shares (relative weight).
*   `--cpuset-cpus`: CPUs in which to allow execution (0-3, 0,1).
*   `--cpuset-mems`: MEMs in which to allow execution (0-3, 0,1).
*   `--disable-content-trust`: Skip image verification (default true).
*   `-f, --file`: Name of the Dockerfile (Default is 'PATH/Dockerfile').
*   `--force-rm`: Always remove intermediate containers.
*   `--iidfile`: Write the image ID to the file.
*   `--isolation`: Container isolation technology.
*   `--label`: Set metadata for an image.
*   `-m, --memory`: Memory limit.
*   `--memory-swap`: Swap limit equal to memory plus swap: '-1' to enable unlimited swap.
*   `--network`: Set the networking mode for the RUN instructions during build.
*   `--no-cache`: Do not use cache when building the image.
*   `--pull`: Always attempt to pull a newer version of the image.
*   `-q, --quiet`: Suppress the build output and print image ID on success.
*   `--rm`: Remove intermediate containers after a successful build (default true).
*   `--security-opt`: Security options.
*   `--shm-size`: Size of /dev/shm.
*   `-t, --tag`: Name and optionally a tag in the 'name:tag' format.
*   `--target`: Set the target build stage to build.
*   `--ulimit`: Ulimit options.

### 13.4 `docker pull` (Detailed)
Pull an image or a repository from a registry.
*   `-a, --all-tags`: Download all tagged images in the repository.
*   `--disable-content-trust`: Skip image verification (default true).
*   `--platform`: Set platform if server is multi-platform capable.
*   `-q, --quiet`: Suppress verbose output.

### 13.5 `docker push` (Detailed)
Push an image or a repository to a registry.
*   `-a, --all-tags`: Push all tagged images in the repository.
*   `--disable-content-trust`: Skip image signing (default true).
*   `-q, --quiet`: Suppress verbose output.

### 13.6 `docker images` (Detailed)
List images.
*   `-a, --all`: Show all images (default hides intermediate images).
*   `--digests`: Show digests.
*   `-f, --filter`: Filter output based on conditions provided.
*   `--format`: Pretty-print images using a Go template.
*   `--no-trunc`: Don't truncate output.
*   `-q, --quiet`: Only show image IDs.

### 13.7 `docker ps` (Detailed)
List containers.
*   `-a, --all`: Show all containers (default shows just running).
*   `-f, --filter`: Filter output based on conditions provided.
*   `--format`: Pretty-print containers using a Go template.
*   `-n, --last`: Show n last created containers (includes all states).
*   `-l, --latest`: Show the latest created container (includes all states).
*   `--no-trunc`: Don't truncate output.
*   `-q, --quiet`: Only display container IDs.
*   `-s, --size`: Display total file sizes.

### 13.8 `docker logs` (Detailed)
Fetch the logs of a container.
*   `--details`: Show extra details provided to logs.
*   `-f, --follow`: Follow log output.
*   `--since`: Show logs since timestamp (e.g. 2013-01-02T13:23:37Z) or relative (e.g. 42m for 42 minutes).
*   `-n, --tail`: Number of lines to show from the end of the logs (default "all").
*   `-t, --timestamps`: Show timestamps.
*   `--until`: Show logs before a timestamp (e.g. 2013-01-02T13:23:37Z) or relative (e.g. 42m for 42 minutes).

### 13.9 `docker inspect` (Detailed)
Return low-level information on Docker objects.
*   `-f, --format`: Format the output using the given Go template.
*   `-s, --size`: Display total file sizes if the type is container.
*   `--type`: Return JSON for specified type.

### 13.10 `docker stats` (Detailed)
Display a live stream of container(s) resource usage statistics.
*   `-a, --all`: Show all containers (default shows just running).
*   `--format`: Pretty-print images using a Go template.
*   `--no-stream`: Disable streaming stats and only pull the first result.
*   `--no-trunc`: Do not truncate output.

### 13.11 `docker top` (Detailed)
Display the running processes of a container.
Usage: `docker top CONTAINER [ps OPTIONS]`

### 13.12 `docker cp` (Detailed)
Copy files/folders between a container and the local filesystem.
*   `-a, --archive`: Archive mode (copy all uid/gid information).
*   `-L, --follow-link`: Always follow symbol link in SRC_PATH.

### 13.13 `docker diff` (Detailed)
Inspect changes to files or directories on a container's filesystem.
Usage: `docker diff CONTAINER`

### 13.14 `docker commit` (Detailed)
Create a new image from a container's changes.
*   `-a, --author`: Author (e.g., "John Hannibal Smith <hannibal@a-team.com>").
*   `-c, --change`: Apply Dockerfile instruction to the created image.
*   `-m, --message`: Commit message.
*   `-p, --pause`: Pause container during commit (default true).

### 13.15 `docker tag` (Detailed)
Create a tag TARGET_IMAGE that refers to SOURCE_IMAGE.
Usage: `docker tag SOURCE_IMAGE[:TAG] TARGET_IMAGE[:TAG]`

### 13.16 `docker save` (Detailed)
Save one or more images to a tar archive (streamed to STDOUT by default).
*   `-o, --output`: Write to a file, instead of STDOUT.

### 13.17 `docker load` (Detailed)
Load an image from a tar archive or STDIN.
*   `-i, --input`: Read from tar archive file, instead of STDIN.
*   `-q, --quiet`: Suppress the load output.

### 13.18 `docker export` (Detailed)
Export a container's filesystem as a tar archive.
*   `-o, --output`: Write to a file, instead of STDOUT.

### 13.19 `docker import` (Detailed)
Import the contents from a tarball to create a filesystem image.
*   `-c, --change`: Apply Dockerfile instruction to the created image.
*   `-m, --message`: Set commit message for imported image.
*   `--platform`: Set platform if server is multi-platform capable.

### 13.20 `docker system` (Detailed)
Manage Docker.
*   `docker system df`: Show docker disk usage.
    *   `--format`: Pretty-print images using a Go template.
    *   `-v, --verbose`: Show detailed information on space usage.
*   `docker system events`: Get real time events from the server.
    *   `-f, --filter`: Filter output based on conditions provided.
    *   `--format`: Format the output using the given Go template.
    *   `--since`: Show all events created since timestamp.
    *   `--until`: Stream events until this timestamp.
*   `docker system info`: Display system-wide information.
    *   `-f, --format`: Format the output using the given Go template.
*   `docker system prune`: Remove unused data.
    *   `-a, --all`: Remove all unused images not just dangling ones.
    *   `--filter`: Provide filter values (e.g. 'label=<key>=<value>').
    *   `-f, --force`: Do not prompt for confirmation.
    *   `--volumes`: Prune volumes.

### 13.21 `docker network` (Detailed)
Manage networks.
*   `docker network connect`: Connect a container to a network.
    *   `--alias`: Add network-scoped alias for the container.
    *   `--driver-opt`: driver options for the network.
    *   `--ip`: IPv4 address.
    *   `--ip6`: IPv6 address.
    *   `--link`: Add link to another container.
    *   `--link-local-ip`: Add a link-local address for the container.
*   `docker network create`: Create a network.
    *   `--attachable`: Enable manual container attachment.
    *   `--config-from`: The network from which to copy the configuration.
    *   `--config-only`: Create a configuration only network.
    *   `-d, --driver`: Driver to manage the Network (default "bridge").
    *   `--gateway`: IPv4 or IPv6 Gateway for the master subnet.
    *   `--ingress`: Create swarm routing-mesh network.
    *   `--internal`: Restrict external access to the network.
    *   `--ip-range`: Allocate container ip from a sub-range.
    *   `--ipam-driver`: IP Address Management Driver (default "default").
    *   `--ipam-opt`: Set custom IPAM driver specific options.
    *   `--ipv6`: Enable IPv6 networking.
    *   `--label`: Set metadata on a network.
    *   `-o, --opt`: Set driver specific options.
    *   `--scope`: Control the network's scope.
    *   `--subnet`: Subnet in CIDR format that represents a network segment.
*   `docker network disconnect`: Disconnect a container from a network.
    *   `-f, --force`: Force the container to disconnect from a network.
*   `docker network inspect`: Display detailed information on one or more networks.
    *   `-f, --format`: Format the output using the given Go template.
    *   `-v, --verbose`: Verbose output for diagnostics.
*   `docker network ls`: List networks.
    *   `-f, --filter`: Filter output based on conditions provided.
    *   `--format`: Pretty-print networks using a Go template.
    *   `--no-trunc`: Do not truncate the output.
    *   `-q, --quiet`: Only display network IDs.
*   `docker network rm`: Remove one or more networks.

### 13.22 `docker volume` (Detailed)
Manage volumes.
*   `docker volume create`: Create a volume.
    *   `-d, --driver`: Specify volume driver name (default "local").
    *   `--label`: Set metadata for a volume.
    *   `--name`: Specify volume name.
    *   `-o, --opt`: Set driver specific options.
*   `docker volume inspect`: Display detailed information on one or more volumes.
    *   `-f, --format`: Format the output using the given Go template.
*   `docker volume ls`: List volumes.
    *   `-f, --filter`: Filter output based on conditions provided.
    *   `--format`: Pretty-print volumes using a Go template.
    *   `-q, --quiet`: Only display volume names.
*   `docker volume prune`: Remove all unused local volumes.
    *   `--filter`: Provide filter values (e.g. 'label=<label>').
    *   `-f, --force`: Do not prompt for confirmation.
*   `docker volume rm`: Remove one or more volumes.
    *   `-f, --force`: Force the removal of one or more volumes.

### 13.23 `docker secret` (Detailed)
Manage Docker secrets.
*   `docker secret create`: Create a secret from a file or STDIN as content.
    *   `-d, --driver`: Secret driver.
    *   `-l, --label`: Secret labels.
    *   `--template-driver`: Template driver.
*   `docker secret inspect`: Display detailed information on one or more secrets.
    *   `-f, --format`: Format the output using the given Go template.
    *   `--pretty`: Print the information in a human friendly format.
*   `docker secret ls`: List secrets.
    *   `-f, --filter`: Filter output based on conditions provided.
    *   `--format`: Pretty-print secrets using a Go template.
    *   `-q, --quiet`: Only display IDs.
*   `docker secret rm`: Remove one or more secrets.

### 13.24 `docker config` (Detailed)
Manage Docker configs.
*   `docker config create`: Create a config from a file or STDIN.
    *   `-l, --label`: Config labels.
    *   `--template-driver`: Template driver.
*   `docker config inspect`: Display detailed information on one or more configs.
    *   `-f, --format`: Format the output using the given Go template.
    *   `--pretty`: Print the information in a human friendly format.
*   `docker config ls`: List configs.
    *   `-f, --filter`: Filter output based on conditions provided.
    *   `--format`: Pretty-print configs using a Go template.
    *   `-q, --quiet`: Only display IDs.
*   `docker config rm`: Remove one or more configs.

### 13.25 `docker context` (Detailed)
Manage contexts.
*   `docker context create`: Create a context.
    *   `--default-stack-orchestrator`: Default orchestrator for stack commands to use with this context (swarm|kubernetes|all).
    *   `--description`: Description of the context.
    *   `--docker`: set the docker endpoint.
    *   `--kubernetes`: set the kubernetes endpoint.
*   `docker context export`: Export a context to a tar or kubeconfig file.
*   `docker context import`: Import a context from a tar or zip file.
*   `docker context inspect`: Display detailed information on one or more contexts.
*   `docker context ls`: List contexts.
*   `docker context rm`: Remove one or more contexts.
*   `docker context update`: Update a context.
*   `docker context use`: Set the current docker context.

### 13.26 `docker buildx` (Detailed)
Docker Buildx is a CLI plugin that extends the docker command with the full support of the features provided by Moby BuildKit builder toolkit.
*   `docker buildx bake`: Build from a file.
*   `docker buildx build`: Start a build.
*   `docker buildx create`: Create a new builder instance.
*   `docker buildx du`: Disk usage.
*   `docker buildx imagetools`: Commands to work on images in registry.
*   `docker buildx inspect`: Inspect current builder instance.
*   `docker buildx ls`: List builder instances.
*   `docker buildx prune`: Remove build cache.
*   `docker buildx rm`: Remove a builder instance.
*   `docker buildx stop`: Stop builder instance.
*   `docker buildx use`: Set the current builder instance.
*   `docker buildx version`: Show buildx version information.

### 13.27 `docker scout` (Detailed)
Command line tool for Docker Scout.
*   `docker scout cache`: Manage Docker Scout cache.
*   `docker scout compare`: Compare two images and display differences.
*   `docker scout config`: Manage Docker Scout configuration.
*   `docker scout cves`: Display CVEs identified in a software artifact.
*   `docker scout enroll`: Enroll an organization with Docker Scout.
*   `docker scout environment`: Manage environments.
*   `docker scout integration`: Manage Docker Scout integrations.
*   `docker scout policy`: Evaluate policies against an image.
*   `docker scout push`: Push an image to a registry and analyze it.
*   `docker scout quickview`: Quick overview of an image.
*   `docker scout recommendations`: Display available base image updates and remediation recommendations.
*   `docker scout repo`: Manage Docker Scout repositories.
*   `docker scout sbom`: Display the SBOM of an image.
*   `docker scout version`: Show Docker Scout version information.

### 13.28 `docker compose` (Detailed)
Define and run multi-container applications with Docker.
*   `docker compose build`: Build or rebuild services.
*   `docker compose config`: Parse, resolve and render compose file in canonical format.
*   `docker compose cp`: Copy files/folders between a service container and the local filesystem.
*   `docker compose create`: Creates containers for a service.
*   `docker compose down`: Stop and remove containers, networks.
*   `docker compose events`: Receive real time events from containers.
*   `docker compose exec`: Execute a command in a running container.
*   `docker compose images`: List images used by the created containers.
*   `docker compose kill`: Force stop service containers.
*   `docker compose logs`: View output from containers.
*   `docker compose ls`: List running compose projects.
*   `docker compose pause`: Pause services.
*   `docker compose port`: Print the public port for a port binding.
*   `docker compose ps`: List containers.
*   `docker compose pull`: Pull service images.
*   `docker compose push`: Push service images.
*   `docker compose restart`: Restart service containers.
*   `docker compose rm`: Removes stopped service containers.
*   `docker compose run`: Run a one-off command on a service.
*   `docker compose scale`: Scale services.
*   `docker compose start`: Start services.
*   `docker compose stop`: Stop services.
*   `docker compose top`: Display the running processes.
*   `docker compose unpause`: Unpause services.
*   `docker compose up`: Create and start containers.
*   `docker compose version`: Show the Docker Compose version information.
*   `docker compose wait`: Block until the first service container stops.
*   `docker compose watch`: Watch build context for service and rebuild/refresh containers when files are updated.
*   `docker compose alpha`: Experimental commands.

## 14. Real-World Case Studies

### Case Study 1: The E-commerce Black Friday Scaling Event

**The Challenge:** An e-commerce platform experienced a 10x traffic spike during Black Friday. Their monolithic database container became a bottleneck, and the web frontend containers were constantly restarting due to OOM errors.

**The Super Specialist Intervention:**

1.  **Diagnosis:** Used `docker stats` to identify the web containers hitting their memory limits. Used `docker inspect` to confirm `OOMKilled: true`.
2.  **Immediate Mitigation:** Scaled the web frontend using `docker compose up --scale web=10 -d`.
3.  **Root Cause Analysis:** Used `docker exec -it` to profile the Node.js application inside the container, discovering a memory leak in the image processing library.
4.  **Long-Term Fix:**
    *   Updated the Dockerfile to use a more efficient base image (`node:18-alpine`).
    *   Implemented multi-stage builds to reduce image size from 1.2GB to 250MB, speeding up deployment times.
    *   Configured `daemon.json` with `live-restore: true` to ensure future daemon updates wouldn't take down the entire cluster.
    *   Implemented proper resource limits in `compose.yaml`:
        ```yaml
        deploy:
          resources:
            limits:
              cpus: '1.0'
              memory: 1G
            reservations:
              cpus: '0.5'
              memory: 512M
        ```

**The Result:** The platform handled the remaining Black Friday traffic without a single dropped request. Deployment times were reduced by 75%, and infrastructure costs were optimized by preventing runaway resource consumption.

### Case Study 2: The Cryptojacking Incident

**The Challenge:** A client noticed unusually high CPU usage on their Docker host. Their cloud provider alerted them to suspicious outbound network traffic.

**The Super Specialist Intervention:**

1.  **Detection:** Ran `docker top` on all running containers and identified an unknown process named `xmrig` (a known cryptocurrency miner) running inside a legacy application container.
2.  **Containment:** Immediately stopped the compromised container using `docker stop`.
3.  **Investigation:**
    *   Used `docker diff` to see what files the attacker had modified.
    *   Used `docker inspect` to check the container's configuration. Discovered it was running with `--privileged` and had port 22 (SSH) exposed with a weak password.
    *   Used `docker scout cves` on the base image and found multiple critical vulnerabilities.
4.  **Remediation:**
    *   Removed the `--privileged` flag.
    *   Removed the SSH server from the container (containers should be immutable; use `docker exec` for access).
    *   Updated the base image to a secure, patched version.
    *   Implemented read-only filesystems (`docker run --read-only`) to prevent attackers from downloading and executing malicious payloads.

**The Result:** The cryptojacking malware was eradicated. The client's Docker environment was secured against future attacks, and a policy was implemented to scan all images with Docker Scout before deployment.

## 15. Final Thoughts on Docker Mastery

Becoming a Docker Super Specialist is not just about memorizing commands; it's about understanding the underlying architecture of containerization. It's about knowing how namespaces provide isolation, how cgroups manage resources, and how union filesystems build images layer by layer.

When you combine this deep architectural understanding with the exhaustive command reference provided in this document, you transform from a user of Docker into a master of it. You gain the ability to debug the undebuggable, optimize the unoptimizable, and build infrastructure that is truly resilient, secure, and scalable.

Keep this reference close. Use it to solve the hard problems. And never stop exploring the depths of what Docker can do.

## 16. Appendix: Extended Configuration Examples

### 16.1 Advanced `daemon.json` Configurations

For highly specialized environments, the `daemon.json` can be tuned even further.

#### Configuring User Namespaces (userns-remap)
User namespaces provide an additional layer of security by mapping the `root` user inside the container to a non-privileged user on the host. This mitigates the impact of container breakout vulnerabilities.

```json
{
  "userns-remap": "default"
}
```
*Explanation:* This tells Docker to create a user and group named `dockremap` and map container users to this namespace.

#### Configuring Seccomp Profiles
Seccomp (Secure Computing Mode) restricts the system calls a container can make to the host kernel.

```json
{
  "seccomp-profile": "/etc/docker/seccomp/custom-profile.json"
}
```
*Explanation:* This applies a custom seccomp profile to all containers by default, providing fine-grained control over kernel interactions.

#### Configuring IPv6
To enable IPv6 support in Docker:

```json
{
  "ipv6": true,
  "fixed-cidr-v6": "2001:db8:1::/64"
}
```
*Explanation:* This enables IPv6 and assigns a specific subnet for Docker to use when allocating IPv6 addresses to containers.

### 16.2 Advanced `compose.yaml` Configurations

#### Using Extension Fields (YAML Anchors)
To avoid repeating configuration in large Compose files, use YAML anchors and aliases.

```yaml
version: '3.8'

x-logging: &default-logging
  driver: "json-file"
  options:
    max-size: "10m"
    max-file: "3"

services:
  web:
    image: nginx
    logging: *default-logging
  
  api:
    image: my-api
    logging: *default-logging
```
*Explanation:* The `x-logging` block defines a reusable configuration snippet. The `*default-logging` alias applies it to both the `web` and `api` services.

#### Using Profiles
Profiles allow you to define optional services that are only started when explicitly requested.

```yaml
version: '3.8'

services:
  web:
    image: nginx
  
  debug-tools:
    image: my-debug-tools
    profiles:
      - debug
```
*Explanation:* Running `docker compose up` will only start the `web` service. To start the debug tools, you must run `docker compose --profile debug up`.

### 16.3 The Evolution of Docker Build

Understanding the shift from legacy `docker build` to `docker buildx` (BuildKit) is crucial.

**Legacy Build:**
*   Sequential execution of instructions.
*   Limited caching capabilities.
*   Tied to the host architecture.

**BuildKit (Buildx):**
*   Concurrent execution of independent build stages.
*   Advanced caching (e.g., importing cache from a registry).
*   Native multi-platform builds (e.g., building for ARM on an AMD64 host).
*   Secret management during builds without leaving traces in the final image.

*Example: Using secrets with BuildKit*
```dockerfile
# syntax=docker/dockerfile:1
FROM alpine
RUN --mount=type=secret,id=mysecret cat /run/secrets/mysecret
```
*Build command:* `docker buildx build --secret id=mysecret,src=mysecret.txt .`

This ensures the secret is never baked into a layer, maintaining security.

## 17. Final Checklist for Production Readiness

Before deploying any Dockerized application to production, run through this checklist:

1.  [ ] **Images are minimal:** Using Alpine, Distroless, or scratch where possible.
2.  [ ] **Multi-stage builds used:** Build tools are not in the final image.
3.  [ ] **No root user:** `USER` directive is set in the Dockerfile.
4.  [ ] **Secrets are managed:** Using Docker Secrets or an external vault, not environment variables.
5.  [ ] **Resource limits set:** `cpus` and `memory` limits are defined in Compose or `docker run`.
6.  [ ] **Log rotation configured:** `daemon.json` has `max-size` and `max-file` set.
7.  [ ] **Healthchecks defined:** `HEALTHCHECK` in Dockerfile or `healthcheck` in Compose.
8.  [ ] **Restart policies set:** `restart: unless-stopped` or similar.
9.  [ ] **Images scanned:** `docker scout cves` reports no critical vulnerabilities.
10. [ ] **Live restore enabled:** `daemon.json` has `live-restore: true`.

By adhering to this checklist and utilizing the exhaustive command reference provided, you will operate at the level of a true Docker Super Specialist.



## 16. Appendix: Extended Configuration Examples

### 16.1 Advanced `daemon.json` Configurations

For highly specialized environments, the `daemon.json` can be tuned even further.

#### Configuring User Namespaces (userns-remap)
User namespaces provide an additional layer of security by mapping the `root` user inside the container to a non-privileged user on the host. This mitigates the impact of container breakout vulnerabilities.

```json
{
  "userns-remap": "default"
}
```
*Explanation:* This tells Docker to create a user and group named `dockremap` and map container users to this namespace.

#### Configuring Seccomp Profiles
Seccomp (Secure Computing Mode) restricts the system calls a container can make to the host kernel.

```json
{
  "seccomp-profile": "/etc/docker/seccomp/custom-profile.json"
}
```
*Explanation:* This applies a custom seccomp profile to all containers by default, providing fine-grained control over kernel interactions.

#### Configuring IPv6
To enable IPv6 support in Docker:

```json
{
  "ipv6": true,
  "fixed-cidr-v6": "2001:db8:1::/64"
}
```
*Explanation:* This enables IPv6 and assigns a specific subnet for Docker to use when allocating IPv6 addresses to containers.

### 16.2 Advanced `compose.yaml` Configurations

#### Using Extension Fields (YAML Anchors)
To avoid repeating configuration in large Compose files, use YAML anchors and aliases.

```yaml
version: '3.8'

x-logging: &default-logging
  driver: "json-file"
  options:
    max-size: "10m"
    max-file: "3"

services:
  web:
    image: nginx
    logging: *default-logging
  
  api:
    image: my-api
    logging: *default-logging
```
*Explanation:* The `x-logging` block defines a reusable configuration snippet. The `*default-logging` alias applies it to both the `web` and `api` services.

#### Using Profiles
Profiles allow you to define optional services that are only started when explicitly requested.

```yaml
version: '3.8'

services:
  web:
    image: nginx
  
  debug-tools:
    image: my-debug-tools
    profiles:
      - debug
```
*Explanation:* Running `docker compose up` will only start the `web` service. To start the debug tools, you must run `docker compose --profile debug up`.

### 16.3 The Evolution of Docker Build

Understanding the shift from legacy `docker build` to `docker buildx` (BuildKit) is crucial.

**Legacy Build:**
*   Sequential execution of instructions.
*   Limited caching capabilities.
*   Tied to the host architecture.

**BuildKit (Buildx):**
*   Concurrent execution of independent build stages.
*   Advanced caching (e.g., importing cache from a registry).
*   Native multi-platform builds (e.g., building for ARM on an AMD64 host).
*   Secret management during builds without leaving traces in the final image.

*Example: Using secrets with BuildKit*
```dockerfile
# syntax=docker/dockerfile:1
FROM alpine
RUN --mount=type=secret,id=mysecret cat /run/secrets/mysecret
```
*Build command:* `docker buildx build --secret id=mysecret,src=mysecret.txt .`

This ensures the secret is never baked into a layer, maintaining security.

## 17. Final Checklist for Production Readiness

Before deploying any Dockerized application to production, run through this checklist:

1.  [ ] **Images are minimal:** Using Alpine, Distroless, or scratch where possible.
2.  [ ] **Multi-stage builds used:** Build tools are not in the final image.
3.  [ ] **No root user:** `USER` directive is set in the Dockerfile.
4.  [ ] **Secrets are managed:** Using Docker Secrets or an external vault, not environment variables.
5.  [ ] **Resource limits set:** `cpus` and `memory` limits are defined in Compose or `docker run`.
6.  [ ] **Log rotation configured:** `daemon.json` has `max-size` and `max-file` set.
7.  [ ] **Healthchecks defined:** `HEALTHCHECK` in Dockerfile or `healthcheck` in Compose.
8.  [ ] **Restart policies set:** `restart: unless-stopped` or similar.
9.  [ ] **Images scanned:** `docker scout cves` reports no critical vulnerabilities.
10. [ ] **Live restore enabled:** `daemon.json` has `live-restore: true`.

By adhering to this checklist and utilizing the exhaustive command reference provided, you will operate at the level of a true Docker Super Specialist.

## 16. Appendix: Extended Configuration Examples

### 16.1 Advanced `daemon.json` Configurations

For highly specialized environments, the `daemon.json` can be tuned even further.

#### Configuring User Namespaces (userns-remap)
User namespaces provide an additional layer of security by mapping the `root` user inside the container to a non-privileged user on the host. This mitigates the impact of container breakout vulnerabilities.

```json
{
  "userns-remap": "default"
}
```
*Explanation:* This tells Docker to create a user and group named `dockremap` and map container users to this namespace.

#### Configuring Seccomp Profiles
Seccomp (Secure Computing Mode) restricts the system calls a container can make to the host kernel.

```json
{
  "seccomp-profile": "/etc/docker/seccomp/custom-profile.json"
}
```
*Explanation:* This applies a custom seccomp profile to all containers by default, providing fine-grained control over kernel interactions.

#### Configuring IPv6
To enable IPv6 support in Docker:

```json
{
  "ipv6": true,
  "fixed-cidr-v6": "2001:db8:1::/64"
}
```
*Explanation:* This enables IPv6 and assigns a specific subnet for Docker to use when allocating IPv6 addresses to containers.

### 16.2 Advanced `compose.yaml` Configurations

#### Using Extension Fields (YAML Anchors)
To avoid repeating configuration in large Compose files, use YAML anchors and aliases.

```yaml
version: '3.8'

x-logging: &default-logging
  driver: "json-file"
  options:
    max-size: "10m"
    max-file: "3"

services:
  web:
    image: nginx
    logging: *default-logging
  
  api:
    image: my-api
    logging: *default-logging
```
*Explanation:* The `x-logging` block defines a reusable configuration snippet. The `*default-logging` alias applies it to both the `web` and `api` services.

#### Using Profiles
Profiles allow you to define optional services that are only started when explicitly requested.

```yaml
version: '3.8'

services:
  web:
    image: nginx
  
  debug-tools:
    image: my-debug-tools
    profiles:
      - debug
```
*Explanation:* Running `docker compose up` will only start the `web` service. To start the debug tools, you must run `docker compose --profile debug up`.

### 16.3 The Evolution of Docker Build

Understanding the shift from legacy `docker build` to `docker buildx` (BuildKit) is crucial.

**Legacy Build:**
*   Sequential execution of instructions.
*   Limited caching capabilities.
*   Tied to the host architecture.

**BuildKit (Buildx):**
*   Concurrent execution of independent build stages.
*   Advanced caching (e.g., importing cache from a registry).
*   Native multi-platform builds (e.g., building for ARM on an AMD64 host).
*   Secret management during builds without leaving traces in the final image.

*Example: Using secrets with BuildKit*
```dockerfile
# syntax=docker/dockerfile:1
FROM alpine
RUN --mount=type=secret,id=mysecret cat /run/secrets/mysecret
```
*Build command:* `docker buildx build --secret id=mysecret,src=mysecret.txt .`

This ensures the secret is never baked into a layer, maintaining security.

## 17. Final Checklist for Production Readiness

Before deploying any Dockerized application to production, run through this checklist:

1.  [ ] **Images are minimal:** Using Alpine, Distroless, or scratch where possible.
2.  [ ] **Multi-stage builds used:** Build tools are not in the final image.
3.  [ ] **No root user:** `USER` directive is set in the Dockerfile.
4.  [ ] **Secrets are managed:** Using Docker Secrets or an external vault, not environment variables.
5.  [ ] **Resource limits set:** `cpus` and `memory` limits are defined in Compose or `docker run`.
6.  [ ] **Log rotation configured:** `daemon.json` has `max-size` and `max-file` set.
7.  [ ] **Healthchecks defined:** `HEALTHCHECK` in Dockerfile or `healthcheck` in Compose.
8.  [ ] **Restart policies set:** `restart: unless-stopped` or similar.
9.  [ ] **Images scanned:** `docker scout cves` reports no critical vulnerabilities.
10. [ ] **Live restore enabled:** `daemon.json` has `live-restore: true`.

By adhering to this checklist and utilizing the exhaustive command reference provided, you will operate at the level of a true Docker Super Specialist.

## 16. Appendix: Extended Configuration Examples

### 16.1 Advanced `daemon.json` Configurations

For highly specialized environments, the `daemon.json` can be tuned even further.

#### Configuring User Namespaces (userns-remap)
User namespaces provide an additional layer of security by mapping the `root` user inside the container to a non-privileged user on the host. This mitigates the impact of container breakout vulnerabilities.

```json
{
  "userns-remap": "default"
}
```
*Explanation:* This tells Docker to create a user and group named `dockremap` and map container users to this namespace.

#### Configuring Seccomp Profiles
Seccomp (Secure Computing Mode) restricts the system calls a container can make to the host kernel.

```json
{
  "seccomp-profile": "/etc/docker/seccomp/custom-profile.json"
}
```
*Explanation:* This applies a custom seccomp profile to all containers by default, providing fine-grained control over kernel interactions.

#### Configuring IPv6
To enable IPv6 support in Docker:

```json
{
  "ipv6": true,
  "fixed-cidr-v6": "2001:db8:1::/64"
}
```
*Explanation:* This enables IPv6 and assigns a specific subnet for Docker to use when allocating IPv6 addresses to containers.

### 16.2 Advanced `compose.yaml` Configurations

#### Using Extension Fields (YAML Anchors)
To avoid repeating configuration in large Compose files, use YAML anchors and aliases.

```yaml
version: '3.8'

x-logging: &default-logging
  driver: "json-file"
  options:
    max-size: "10m"
    max-file: "3"

services:
  web:
    image: nginx
    logging: *default-logging
  
  api:
    image: my-api
    logging: *default-logging
```
*Explanation:* The `x-logging` block defines a reusable configuration snippet. The `*default-logging` alias applies it to both the `web` and `api` services.

#### Using Profiles
Profiles allow you to define optional services that are only started when explicitly requested.

```yaml
version: '3.8'

services:
  web:
    image: nginx
  
  debug-tools:
    image: my-debug-tools
    profiles:
      - debug
```
*Explanation:* Running `docker compose up` will only start the `web` service. To start the debug tools, you must run `docker compose --profile debug up`.

### 16.3 The Evolution of Docker Build

Understanding the shift from legacy `docker build` to `docker buildx` (BuildKit) is crucial.

**Legacy Build:**
*   Sequential execution of instructions.
*   Limited caching capabilities.
*   Tied to the host architecture.

**BuildKit (Buildx):**
*   Concurrent execution of independent build stages.
*   Advanced caching (e.g., importing cache from a registry).
*   Native multi-platform builds (e.g., building for ARM on an AMD64 host).
*   Secret management during builds without leaving traces in the final image.

*Example: Using secrets with BuildKit*
```dockerfile
# syntax=docker/dockerfile:1
FROM alpine
RUN --mount=type=secret,id=mysecret cat /run/secrets/mysecret
```
*Build command:* `docker buildx build --secret id=mysecret,src=mysecret.txt .`

This ensures the secret is never baked into a layer, maintaining security.

## 17. Final Checklist for Production Readiness

Before deploying any Dockerized application to production, run through this checklist:

1.  [ ] **Images are minimal:** Using Alpine, Distroless, or scratch where possible.
2.  [ ] **Multi-stage builds used:** Build tools are not in the final image.
3.  [ ] **No root user:** `USER` directive is set in the Dockerfile.
4.  [ ] **Secrets are managed:** Using Docker Secrets or an external vault, not environment variables.
5.  [ ] **Resource limits set:** `cpus` and `memory` limits are defined in Compose or `docker run`.
6.  [ ] **Log rotation configured:** `daemon.json` has `max-size` and `max-file` set.
7.  [ ] **Healthchecks defined:** `HEALTHCHECK` in Dockerfile or `healthcheck` in Compose.
8.  [ ] **Restart policies set:** `restart: unless-stopped` or similar.
9.  [ ] **Images scanned:** `docker scout cves` reports no critical vulnerabilities.
10. [ ] **Live restore enabled:** `daemon.json` has `live-restore: true`.

By adhering to this checklist and utilizing the exhaustive command reference provided, you will operate at the level of a true Docker Super Specialist.

## === FILE: 49-docker-config-schemas.md ===
# Docker Super Specialist: Complete Configuration Reference

## 1. `compose.yaml` Complete Schema Reference

The `compose.yaml` file is the heart of Docker Compose. Below is the exhaustive reference for every top-level element and nested option.

### 1.1 Top-Level Elements

- `version`: (Deprecated) No longer required in Compose V2.
- `name`: Sets the project name. Overrides the directory name.
- `services`: Defines the containers to run.
- `networks`: Defines the networks to be created or used.
- `volumes`: Defines the persistent volumes.
- `configs`: Defines configuration files to be mounted.
- `secrets`: Defines sensitive data to be mounted securely.

### 1.2 `services` Attributes

Every service can have the following attributes:

| Attribute | Type | Default | Description | Example |
|---|---|---|---|---|
| `annotations` | map/list | None | Metadata for the container. | `annotations: { "com.example.foo": "bar" }` |
| `attach` | boolean | `true` | Whether to attach to the container's output. | `attach: false` |
| `build` | string/object | None | Configuration for building the image. | `build: ./dir` or `build: { context: ., dockerfile: Dockerfile.alt }` |
| `blkio_config` | object | None | Block IO configuration. | `blkio_config: { weight: 300 }` |
| `cpu_count` | integer | None | Number of usable CPUs. | `cpu_count: 2` |
| `cpu_percent` | integer | None | Usable percentage of available CPUs. | `cpu_percent: 50` |
| `cpu_shares` | integer | None | CPU shares (relative weight). | `cpu_shares: 73` |
| `cpu_period` | integer | None | CPU CFS (Completely Fair Scheduler) period. | `cpu_period: 100000` |
| `cpu_quota` | integer | None | CPU CFS quota. | `cpu_quota: 50000` |
| `cpu_rt_runtime` | integer | None | CPU real-time runtime. | `cpu_rt_runtime: 95000` |
| `cpu_rt_period` | integer | None | CPU real-time period. | `cpu_rt_period: 100000` |
| `cpus` | float | None | Number of CPUs. | `cpus: 1.5` |
| `cpuset` | string | None | CPUs in which to allow execution. | `cpuset: "0,1"` |
| `cap_add` | list | None | Add Linux capabilities. | `cap_add: ["SYS_ADMIN"]` |
| `cap_drop` | list | None | Drop Linux capabilities. | `cap_drop: ["ALL"]` |
| `cgroup` | string | None | Cgroup namespace mode. | `cgroup: "host"` |
| `cgroup_parent` | string | None | Optional parent cgroup. | `cgroup_parent: "m-executor-abcd"` |
| `command` | string/list | None | Override the default command. | `command: ["bundle", "exec", "thin", "-p", "3000"]` |
| `configs` | list | None | Grant access to configs. | `configs: ["my_config"]` |
| `container_name` | string | None | Custom container name. | `container_name: my-web-container` |
| `credential_spec` | object | None | Credential spec for managed service accounts (Windows). | `credential_spec: { file: "my-spec.json" }` |
| `depends_on` | list/object | None | Express dependency between services. | `depends_on: { db: { condition: service_healthy } }` |
| `deploy` | object | None | Configuration for deployment and resource limits. | `deploy: { replicas: 6 }` |
| `develop` | object | None | Configuration for development (Compose Watch). | `develop: { watch: [...] }` |
| `device_cgroup_rules` | list | None | Add rules to the cgroup allowed devices list. | `device_cgroup_rules: ["c 1:3 mr"]` |
| `devices` | list | None | Device mappings. | `devices: ["/dev/ttyUSB0:/dev/ttyUSB0"]` |
| `dns` | string/list | None | Custom DNS servers. | `dns: ["8.8.8.8", "9.9.9.9"]` |
| `dns_opt` | list | None | Custom DNS options. | `dns_opt: ["use-vc", "no-tld-query"]` |
| `dns_search` | string/list | None | Custom DNS search domains. | `dns_search: ["dc1.example.com"]` |
| `domainname` | string | None | Custom domain name. | `domainname: foo.com` |
| `entrypoint` | string/list | None | Override the default entrypoint. | `entrypoint: /code/entrypoint.sh` |
| `env_file` | string/list | None | Add environment variables from a file. | `env_file: .env` |
| `environment` | map/list | None | Add environment variables. | `environment: { RACK_ENV: development }` |
| `expose` | list | None | Expose ports without publishing them to the host. | `expose: ["3000"]` |
| `extends` | string/object | None | Extend another service. | `extends: { file: common.yml, service: webapp }` |
| `external_links` | list | None | Link to containers started outside this compose. | `external_links: ["redis_1", "project_db_1:mysql"]` |
| `extra_hosts` | list/map | None | Add hostname mappings. | `extra_hosts: ["somehost:162.242.195.82"]` |
| `group_add` | list | None | Add additional groups. | `group_add: ["mail"]` |
| `healthcheck` | object | None | Configure a check that's run to determine whether or not containers for this service are "healthy". | `healthcheck: { test: ["CMD", "curl", "-f", "http://localhost"] }` |
| `hostname` | string | None | Custom host name. | `hostname: foo` |
| `image` | string | None | Specify the image to start the container from. | `image: redis:alpine` |
| `init` | boolean | `false` | Run an init inside the container that forwards signals and reaps processes. | `init: true` |
| `ipc` | string | None | IPC namespace to use. | `ipc: host` |
| `isolation` | string | None | Specify a container's isolation technology. | `isolation: default` |
| `labels` | map/list | None | Add metadata to containers. | `labels: { com.example.description: "Accounting webapp" }` |
| `links` | list | None | Link to containers in another service. | `links: ["db", "db:database"]` |
| `logging` | object | None | Logging configuration for the service. | `logging: { driver: syslog, options: { syslog-address: "tcp://192.168.0.42:123" } }` |
| `mac_address` | string | None | MAC address. | `mac_address: 02:42:ac:11:65:43` |
| `mem_limit` | string | None | Memory limit. | `mem_limit: 1g` |
| `mem_reservation` | string | None | Memory soft limit. | `mem_reservation: 512m` |
| `mem_swappiness` | integer | None | Tune a container's memory swappiness behavior. | `mem_swappiness: 60` |
| `memswap_limit` | string | None | Swap limit equal to memory plus swap. | `memswap_limit: 2g` |
| `network_mode` | string | None | Network mode. | `network_mode: "host"` |
| `networks` | list/map | None | Networks to join. | `networks: ["frontend", "backend"]` |
| `oom_kill_disable` | boolean | `false` | Disable OOM Killer. | `oom_kill_disable: true` |
| `oom_score_adj` | integer | None | Tune the host's OOM preferences for containers. | `oom_score_adj: 500` |
| `pid` | string | None | PID namespace to use. | `pid: "host"` |
| `pids_limit` | integer | None | Tune a container's pids limit. | `pids_limit: 100` |
| `platform` | string | None | Target platform containers for this service will run on. | `platform: linux/amd64` |
| `ports` | list | None | Expose ports. | `ports: ["3000", "8000:8000", "9000:8080"]` |
| `privileged` | boolean | `false` | Give extended privileges to this container. | `privileged: true` |
| `profiles` | list | None | Define a list of named profiles for the service to be enabled under. | `profiles: ["frontend", "debug"]` |
| `pull_policy` | string | `always` | Define the decisions Compose makes when it starts to pull images. | `pull_policy: missing` |
| `read_only` | boolean | `false` | Mount the container's root filesystem as read only. | `read_only: true` |
| `restart` | string | `no` | Restart policy. | `restart: always` |
| `runtime` | string | None | Specify the runtime to use for the container. | `runtime: runc` |
| `scale` | integer | `1` | Specify the default number of containers to deploy for this service. | `scale: 3` |
| `secrets` | list | None | Grant access to secrets on a per-service basis. | `secrets: ["my_secret", "my_other_secret"]` |
| `security_opt` | list | None | Override the default labeling scheme for each container. | `security_opt: ["label:user:USER", "label:role:ROLE"]` |
| `shm_size` | string | None | Size of `/dev/shm`. | `shm_size: '2gb'` |
| `stdin_open` | boolean | `false` | Keep STDIN open even if not attached. | `stdin_open: true` |
| `stop_grace_period` | string | `10s` | Specify how long to wait when attempting to stop a container if it doesn't handle SIGTERM. | `stop_grace_period: 1m30s` |
| `stop_signal` | string | `SIGTERM` | Set an alternative signal to stop the container. | `stop_signal: SIGUSR1` |
| `storage_opt` | map | None | Storage driver options for this service. | `storage_opt: { size: '120G' }` |
| `sysctls` | map/list | None | Kernel parameters to set in the container. | `sysctls: { net.core.somaxconn: 1024 }` |
| `tmpfs` | string/list | None | Mount a temporary file system inside the container. | `tmpfs: /run` |
| `tty` | boolean | `false` | Allocate a pseudo-TTY. | `tty: true` |
| `ulimits` | map | None | Override the default ulimits for a container. | `ulimits: { nproc: 65535, nofile: { soft: 20000, hard: 40000 } }` |
| `user` | string | None | Override the user used to run the container process. | `user: "1000:1000"` |
| `userns_mode` | string | None | Disable the user namespace for this service, if Docker daemon is configured with user namespaces. | `userns_mode: "host"` |
| `uts` | string | None | UTS namespace to use. | `uts: "host"` |
| `volumes` | list | None | Mount host paths or named volumes, specified as sub-options to a service. | `volumes: ["/var/lib/mysql", "./cache:/tmp/cache", "datavolume:/var/lib/mysql"]` |
| `volumes_from` | list | None | Mount all of the volumes from another service or container. | `volumes_from: ["service_name", "container_name"]` |
| `working_dir` | string | None | Override the container's working directory. | `working_dir: /code` |

### 1.3 `networks` Attributes

| Attribute | Type | Default | Description | Example |
|---|---|---|---|---|
| `driver` | string | `bridge` | Specify which driver should be used for this network. | `driver: overlay` |
| `driver_opts` | map | None | Specify a list of options as key-value pairs to pass to the driver. | `driver_opts: { com.docker.network.bridge.name: br_1 }` |
| `attachable` | boolean | `false` | Only used when the driver is set to `overlay`. If set to `true`, then standalone containers can attach to this network. | `attachable: true` |
| `enable_ipv6` | boolean | `false` | Enable IPv6 networking. | `enable_ipv6: true` |
| `internal` | boolean | `false` | By default, Docker also connects a bridge network to it to provide external connectivity. If you want to create an externally isolated overlay network, you can set this option to `true`. | `internal: true` |
| `labels` | map/list | None | Add metadata to containers. | `labels: { com.example.description: "Financial transaction network" }` |
| `external` | boolean | `false` | If set to `true`, specifies that this network has been created outside of Compose. | `external: true` |
| `name` | string | None | Set a custom name for this network. | `name: my-app-net` |
| `ipam` | object | None | Specify custom IPAM config. | `ipam: { driver: default, config: [{ subnet: "172.28.0.0/16" }] }` |

### 1.4 `volumes` Attributes

| Attribute | Type | Default | Description | Example |
|---|---|---|---|---|
| `driver` | string | `local` | Specify which volume driver should be used for this volume. | `driver: foobar` |
| `driver_opts` | map | None | Specify a list of options as key-value pairs to pass to the driver for this volume. | `driver_opts: { type: "nfs", o: "addr=10.40.0.199,nolock,soft,rw", device: ":/docker/example" }` |
| `external` | boolean | `false` | If set to `true`, specifies that this volume has been created outside of Compose. | `external: true` |
| `labels` | map/list | None | Add metadata to containers. | `labels: { com.example.description: "Database volume" }` |
| `name` | string | None | Set a custom name for this volume. | `name: my-app-data` |

### 1.5 `configs` Attributes

| Attribute | Type | Default | Description | Example |
|---|---|---|---|---|
| `file` | string | None | The config is created with the contents of the file at the specified path. | `file: ./my_config.txt` |
| `external` | boolean | `false` | If set to `true`, specifies that this config has already been created. | `external: true` |
| `name` | string | None | The name of the config object in Docker. | `name: my_config` |
| `content` | string | None | The content of the config. | `content: | 
  server {
    listen 80;
  }` |

### 1.6 `secrets` Attributes

| Attribute | Type | Default | Description | Example |
|---|---|---|---|---|
| `file` | string | None | The secret is created with the contents of the file at the specified path. | `file: ./my_secret.txt` |
| `environment` | string | None | The secret is created with the value of an environment variable. | `environment: "MY_SECRET"` |
| `external` | boolean | `false` | If set to `true`, specifies that this secret has already been created. | `external: true` |
| `name` | string | None | The name of the secret object in Docker. | `name: my_secret` |

## 2. Dockerfile Instruction Reference

A complete reference for every Dockerfile instruction.

### `FROM`
Initializes a new build stage and sets the Base Image for subsequent instructions.
- Syntax: `FROM [--platform=<platform>] <image> [AS <name>]` or `FROM [--platform=<platform>] <image>[:<tag>] [AS <name>]` or `FROM [--platform=<platform>] <image>[@<digest>] [AS <name>]`
- Example: `FROM --platform=linux/amd64 ubuntu:22.04 AS builder`

### `RUN`
Executes any commands in a new layer on top of the current image and commits the results.
- Syntax: `RUN <command>` (shell form) or `RUN ["executable", "param1", "param2"]` (exec form)
- Flags: `--mount=type=cache|bind|secret|ssh`, `--network=default|none|host`
- Example: `RUN --mount=type=cache,target=/var/cache/apt apt-get update && apt-get install -y curl`

### `CMD`
Provides defaults for an executing container. There can only be one `CMD` instruction in a Dockerfile.
- Syntax: `CMD ["executable","param1","param2"]` (exec form, preferred) or `CMD ["param1","param2"]` (as default parameters to ENTRYPOINT) or `CMD command param1 param2` (shell form)
- Example: `CMD ["node", "server.js"]`

### `LABEL`
Adds metadata to an image.
- Syntax: `LABEL <key>=<value> <key>=<value> <key>=<value> ...`
- Example: `LABEL org.opencontainers.image.authors="team@example.com"`

### `EXPOSE`
Informs Docker that the container listens on the specified network ports at runtime.
- Syntax: `EXPOSE <port> [<port>/<protocol>...]`
- Example: `EXPOSE 80/tcp 80/udp`

### `ENV`
Sets the environment variable `<key>` to the value `<value>`.
- Syntax: `ENV <key>=<value> ...`
- Example: `ENV NODE_ENV=production PORT=3000`

### `ADD`
Copies new files, directories or remote file URLs from `<src>` and adds them to the filesystem of the image at the path `<dest>`.
- Syntax: `ADD [--chown=<user>:<group>] [--chmod=<perms>] [--checksum=<checksum>] <src>... <dest>`
- Example: `ADD https://example.com/big.tar.xz /usr/src/things/`

### `COPY`
Copies new files or directories from `<src>` and adds them to the filesystem of the container at the path `<dest>`.
- Syntax: `COPY [--chown=<user>:<group>] [--chmod=<perms>] <src>... <dest>`
- Example: `COPY --chown=node:node package*.json ./`

### `ENTRYPOINT`
Allows you to configure a container that will run as an executable.
- Syntax: `ENTRYPOINT ["executable", "param1", "param2"]` (exec form, preferred) or `ENTRYPOINT command param1 param2` (shell form)
- Example: `ENTRYPOINT ["docker-entrypoint.sh"]`

### `VOLUME`
Creates a mount point with the specified name and marks it as holding externally mounted volumes from native host or other containers.
- Syntax: `VOLUME ["/data"]`
- Example: `VOLUME /var/lib/mysql`

### `USER`
Sets the user name (or UID) and optionally the user group (or GID) to use when running the image and for any `RUN`, `CMD` and `ENTRYPOINT` instructions that follow it in the Dockerfile.
- Syntax: `USER <user>[:<group>]` or `USER <UID>[:<GID>]`
- Example: `USER 1000:1000`

### `WORKDIR`
Sets the working directory for any `RUN`, `CMD`, `ENTRYPOINT`, `COPY` and `ADD` instructions that follow it in the Dockerfile.
- Syntax: `WORKDIR /path/to/workdir`
- Example: `WORKDIR /app`

### `ARG`
Defines a variable that users can pass at build-time to the builder with the `docker build` command using the `--build-arg <varname>=<value>` flag.
- Syntax: `ARG <name>[=<default value>]`
- Example: `ARG VERSION=latest`

### `ONBUILD`
Adds to the image a trigger instruction to be executed at a later time, when the image is used as the base for another build.
- Syntax: `ONBUILD <INSTRUCTION>`
- Example: `ONBUILD COPY . /app/src`

### `STOPSIGNAL`
Sets the system call signal that will be sent to the container to exit.
- Syntax: `STOPSIGNAL signal`
- Example: `STOPSIGNAL SIGKILL`

### `HEALTHCHECK`
Tells Docker how to test a container to check that it is still working.
- Syntax: `HEALTHCHECK [OPTIONS] CMD command` or `HEALTHCHECK NONE`
- Options: `--interval=DURATION` (default: 30s), `--timeout=DURATION` (default: 30s), `--start-period=DURATION` (default: 0s), `--retries=N` (default: 3)
- Example: `HEALTHCHECK --interval=5m --timeout=3s CMD curl -f http://localhost/ || exit 1`

### `SHELL`
Allows the default shell used for the shell form of commands to be overridden.
- Syntax: `SHELL ["executable", "parameters"]`
- Example: `SHELL ["powershell", "-command"]`

## 3. `daemon.json` Complete Reference

The `daemon.json` file configures the Docker daemon.

| Field | Type | Default | Description |
|---|---|---|---|
| `storage-driver` | string | `overlay2` | The storage driver to use. |
| `log-driver` | string | `json-file` | The default logging driver. |
| `log-opts` | map | None | Options for the logging driver. |
| `default-address-pools` | list | None | Default address pools for node networks. |
| `dns` | list | None | DNS servers to use. |
| `registry-mirrors` | list | None | Registry mirrors to use. |
| `insecure-registries` | list | None | Insecure registries to allow. |
| `live-restore` | boolean | `false` | Enable live restore of docker when containers are still running. |
| `default-runtime` | string | `runc` | Default OCI runtime for containers. |
| `runtimes` | map | None | Register additional OCI runtimes. |
| `features` | map | None | Enable/disable specific features. |
| `builder` | map | None | BuildKit configuration. |
| `containerd` | string | None | Path to containerd socket. |
| `default-cgroupns-mode` | string | `private` | Default cgroup namespace mode. |
| `exec-opts` | list | None | Execution options. |
| `experimental` | boolean | `false` | Enable experimental features. |
| `fixed-cidr` | string | None | IPv4 subnet for fixed IPs. |
| `fixed-cidr-v6` | string | None | IPv6 subnet for fixed IPs. |
| `group` | string | `docker` | Group for the unix socket. |
| `hosts` | list | None | Daemon socket(s) to connect to. |
| `icc` | boolean | `true` | Enable inter-container communication. |
| `ip` | string | `0.0.0.0` | Default IP when binding container ports. |
| `ip-forward` | boolean | `true` | Enable net.ipv4.ip_forward. |
| `iptables` | boolean | `true` | Enable addition of iptables rules. |
| `ip-masq` | boolean | `true` | Enable IP masquerading. |
| `labels` | list | None | Daemon labels. |
| `max-concurrent-downloads` | integer | `3` | Max concurrent downloads. |
| `max-concurrent-uploads` | integer | `5` | Max concurrent uploads. |
| `max-download-attempts` | integer | `5` | Max download attempts. |
| `metrics-addr` | string | None | Address to serve metrics API. |
| `no-new-privileges` | boolean | `false` | Set no-new-privileges by default for new containers. |
| `oom-score-adjust` | integer | `-500` | Set the oom_score_adj for the daemon. |
| `pidfile` | string | `/var/run/docker.pid` | Path to use for daemon PID file. |
| `raw-logs` | boolean | `false` | Full timestamps without ANSI coloring. |
| `seccomp-profile` | string | None | Path to seccomp profile. |
| `selinux-enabled` | boolean | `false` | Enable selinux support. |
| `shutdown-timeout` | integer | `15` | Default timeout for stopping containers. |
| `tls` | boolean | `false` | Use TLS; implied by --tlsverify. |
| `tlscacert` | string | `~/.docker/ca.pem` | Trust certs signed only by this CA. |
| `tlscert` | string | `~/.docker/cert.pem` | Path to TLS certificate file. |
| `tlskey` | string | `~/.docker/key.pem` | Path to TLS key file. |
| `tlsverify` | boolean | `false` | Use TLS and verify the remote. |
| `userland-proxy` | boolean | `true` | Use userland proxy for loopback traffic. |
| `userns-remap` | string | None | User namespace remapping. |

## 4. `.dockerignore` Patterns

The `.dockerignore` file excludes files and directories from the build context.

### Syntax
- `#` for comments.
- `*` matches any sequence of non-separator characters.
- `?` matches any single non-separator character.
- `**` matches any number of directories.
- `!` negates a pattern.

### Common Patterns

**Node.js:**
```dockerignore
node_modules
npm-debug.log
Dockerfile
.dockerignore
.git
.gitignore
README.md
```

**Python:**
```dockerignore
__pycache__
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.env
Dockerfile
.dockerignore
.git
```

**Go:**
```dockerignore
bin/
obj/
*.exe
*.dll
*.so
*.dylib
Dockerfile
.dockerignore
.git
```

## 5. BuildKit Configuration (`buildkitd.toml`)

BuildKit can be configured via `buildkitd.toml`.

```toml
debug = true
# root is where all buildkit state is stored.
root = "/var/lib/buildkit"
# insecure-entitlements allows insecure entitlements, disabled by default.
insecure-entitlements = [ "network.host", "security.insecure" ]

[grpc]
  address = [ "tcp://0.0.0.0:1234" ]
  # debugAddress is address for attaching go pprof and expvar.
  debugAddress = "0.0.0.0:6060"
  uid = 0
  gid = 0
  [grpc.tls]
    cert = "/etc/buildkit/tls.crt"
    key = "/etc/buildkit/tls.key"
    ca = "/etc/buildkit/tlsca.crt"

[worker.oci]
  enabled = true
  # platforms is manually configure platforms, auto-detected by default.
  platforms = [ "linux/amd64", "linux/arm64" ]
  snapshotter = "auto" # overlayfs or native, default auto will try to use overlayfs
  rootless = false # see docs/rootless.md for more details on rootless mode.
  # Whether run subprocesses in main cgroup or create top-level cgroup.
  # Default is "cgroupfs" when not running rootless.
  cgroup-parent = "cgroupfs"
  # gc keeps/frees disk space.
  gc = true
  gckeepstorage = 9000
  [[worker.oci.gcpolicy]]
    keepBytes = 512000000
    keepDuration = 172800
    filters = [ "type==source.local", "type==exec.cachemount", "type==source.git.checkout"]
  [[worker.oci.gcpolicy]]
    all = true
    keepBytes = 1024000000

[worker.containerd]
  address = "/run/containerd/containerd.sock"
  enabled = true
  platforms = [ "linux/amd64", "linux/arm64" ]
  namespace = "buildkit"
  gc = true
  # gckeepstorage sets storage limit for default gc profile, in MB.
  gckeepstorage = 9000

[registry."docker.io"]
  mirrors = ["YOUR_REGISTRY_MIRROR"]
  http = true
  insecure = true
```

## 6. Docker Context Configuration

Docker contexts allow you to manage multiple Docker environments.

- Create a context: `docker context create my-context --docker "host=ssh://user@remote-host"`
- Use a context: `docker context use my-context`
- List contexts: `docker context ls`
- Inspect a context: `docker context inspect my-context`

## 7. Registry Configuration (`config.yml`)

Configuration for a private Docker registry.

```yaml
version: 0.1
log:
  fields:
    service: registry
storage:
  cache:
    blobdescriptor: inmemory
  filesystem:
    rootdirectory: /var/lib/registry
http:
  addr: :5000
  headers:
    X-Content-Type-Options: [nosniff]
health:
  storagedriver:
    enabled: true
    interval: 10s
    threshold: 3
```

## 8. Production `compose.yaml` Templates

### 8.1 Web App Stack

```yaml
services:
  webapp:
    image: YOUR_REGISTRY/webapp:v1.2.3
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    environment:
      - NODE_ENV=production
    secrets:
      - db_password
    networks:
      - frontend
      - backend
    deploy:
      replicas: 3
      update_config:
        parallelism: 1
        delay: 10s
      restart_policy:
        condition: on-failure
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"

networks:
  frontend:
  backend:
    internal: true

secrets:
  db_password:
    external: true
```

### 8.2 Database Stack

```yaml
services:
  db:
    image: postgres:15-alpine
    restart: always
    environment:
      POSTGRES_USER: admin
      POSTGRES_PASSWORD_FILE: /run/secrets/db_password
      POSTGRES_DB: myapp
    volumes:
      - db-data:/var/lib/postgresql/data
    secrets:
      - db_password
    networks:
      - backend
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 4G
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U admin -d myapp"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  db-data:

networks:
  backend:
    internal: true

secrets:
  db_password:
    external: true
```

### 8.3 Monitoring Stack (Prometheus/Grafana)

```yaml
services:
  prometheus:
    image: prom/prometheus:v2.45.0
    restart: unless-stopped
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml:ro
      - prometheus-data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--web.console.libraries=/etc/prometheus/console_libraries'
      - '--web.console.templates=/etc/prometheus/consoles'
      - '--web.enable-lifecycle'
    ports:
      - "9090:9090"
    networks:
      - monitoring

  grafana:
    image: grafana/grafana:10.0.3
    restart: unless-stopped
    volumes:
      - grafana-data:/var/lib/grafana
    environment:
      - GF_SECURITY_ADMIN_PASSWORD__FILE=/run/secrets/grafana_password
    secrets:
      - grafana_password
    ports:
      - "3000:3000"
    networks:
      - monitoring
    depends_on:
      - prometheus

volumes:
  prometheus-data:
  grafana-data:

networks:
  monitoring:

secrets:
  grafana_password:
    external: true
```

### 8.4 ELK Stack

```yaml
services:
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.9.0
    environment:
      - discovery.type=single-node
      - xpack.security.enabled=false
      - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
    volumes:
      - es-data:/usr/share/elasticsearch/data
    ports:
      - "9200:9200"
    networks:
      - elk

  logstash:
    image: docker.elastic.co/logstash/logstash:8.9.0
    volumes:
      - ./logstash.conf:/usr/share/logstash/pipeline/logstash.conf:ro
    ports:
      - "5044:5044"
    networks:
      - elk
    depends_on:
      - elasticsearch

  kibana:
    image: docker.elastic.co/kibana/kibana:8.9.0
    ports:
      - "5601:5601"
    networks:
      - elk
    depends_on:
      - elasticsearch

volumes:
  es-data:

networks:
  elk:
```

## 9. Troubleshooting and Optimization

### 9.1 Common Errors and Solutions

- **"port already in use"**: Use `lsof -i :PORT` to find the conflicting process, or change the port mapping in `compose.yaml`.
- **"no space left on device"**: Run `docker system prune -a --volumes` to clear unused data. Check the `overlay2` directory size.
- **"OOM killed"**: The container exceeded its memory limit. Increase the `mem_limit` in `compose.yaml` or optimize the application's memory usage.
- **"permission denied"**: Check the user/group permissions of the mounted volumes. Ensure the container user has access.
- **"network not found"**: Run `docker network create <network_name>` or ensure the network is defined in `compose.yaml`.
- **"image not found"**: Verify the registry URL, image tag, and `pull_policy`. Ensure you are logged in to the registry.
- **"container unhealthy"**: Check the `healthcheck` command and logs. Increase the `timeout` or `start_period` if the application takes longer to start.
- **"bind mount permission denied"**: On SELinux systems, append `:z` or `:Z` to the volume mount path (e.g., `./data:/data:z`).
- **"DNS resolution failed"**: Check the host's DNS settings or configure custom DNS servers in `daemon.json` or `compose.yaml`.
- **"cannot start service"**: Check `depends_on` conditions. Ensure required services are healthy before starting dependent services.
- **"exec format error"**: The image architecture does not match the host architecture (e.g., running an ARM image on an AMD64 host). Use `docker buildx` to build multi-platform images.
- **"context deadline exceeded"**: Increase the timeout for Docker commands or check network connectivity to the registry.

### 9.2 Cost and Time Optimization

- **Multi-stage builds**: Use multi-stage builds to create smaller final images. This reduces pull times and storage costs.
- **Layer caching**: Order Dockerfile instructions from least frequently changed to most frequently changed to maximize cache hits.
- **BuildKit cache mounts**: Use `--mount=type=cache` to cache package manager downloads (e.g., `apt`, `npm`, `pip`) between builds.
- **Parallel builds**: Use `docker compose build --parallel` to build multiple services concurrently.
- **Image pull policy**: Set `pull_policy: if-not-present` to avoid unnecessary image pulls.
- **Resource limits**: Set CPU and memory limits to prevent runaway containers from consuming all host resources.
- **Logging**: Configure log rotation (`max-size`, `max-file`) to prevent log files from filling up the disk.
- **Prune**: Regularly run `docker system prune` and `docker volume prune` to remove unused resources.
- **Compose profiles**: Use profiles to start only the services needed for a specific environment or task.
- **Compose watch**: Use `develop: watch` for fast iteration during development without rebuilding images.

### 9.3 Security Hardening

- **Non-root user**: Run containers as a non-root user (`USER 1000:1000`).
- **Read-only root filesystem**: Set `read_only: true` to prevent modifications to the container's root filesystem.
- **Drop capabilities**: Drop all Linux capabilities (`cap_drop: ["ALL"]`) and add only the necessary ones.
- **No new privileges**: Set `security_opt: ["no-new-privileges:true"]` to prevent processes from gaining additional privileges.
- **Seccomp profiles**: Use custom seccomp profiles to restrict system calls.
- **Resource limits**: Enforce CPU, memory, and PID limits to prevent denial-of-service attacks.
- **No privileged mode**: Avoid using `privileged: true` unless absolutely necessary.
- **Minimal base images**: Use minimal base images like `alpine`, `distroless`, or `scratch` to reduce the attack surface.
- **Secrets management**: Use Docker secrets instead of environment variables for sensitive data.
- **Network segmentation**: Use internal networks to isolate backend services from the public internet.

### 9.4 Upgrade Strategies

- **Blue-green deployment**: Run the new version alongside the old version and switch traffic when ready.
- **Rolling update**: Use `update_config` with `parallelism` and `delay` to update containers one by one.
- **Canary release**: Route a small percentage of traffic to the new version to test it before a full rollout.
- **Database migrations**: Run database migrations as an init container or a pre-start hook before starting the application.
- **Rollback**: Configure `rollback_config` to automatically roll back to the previous version if the update fails.
- **Zero-downtime**: Use `order: start-first` in `update_config` to start the new container before stopping the old one.
# Docker Super Specialist: Complete Configuration Reference

## 1. `compose.yaml` Complete Schema Reference

The `compose.yaml` file is the heart of Docker Compose. Below is the exhaustive reference for every top-level element and nested option.

### 1.1 Top-Level Elements

- `version`: (Deprecated) No longer required in Compose V2.
- `name`: Sets the project name. Overrides the directory name.
- `services`: Defines the containers to run.
- `networks`: Defines the networks to be created or used.
- `volumes`: Defines the persistent volumes.
- `configs`: Defines configuration files to be mounted.
- `secrets`: Defines sensitive data to be mounted securely.

### 1.2 `services` Attributes

Every service can have the following attributes:

| Attribute | Type | Default | Description | Example |
|---|---|---|---|---|
| `annotations` | map/list | None | Metadata for the container. | `annotations: { "com.example.foo": "bar" }` |
| `attach` | boolean | `true` | Whether to attach to the container's output. | `attach: false` |
| `build` | string/object | None | Configuration for building the image. | `build: ./dir` or `build: { context: ., dockerfile: Dockerfile.alt }` |
| `blkio_config` | object | None | Block IO configuration. | `blkio_config: { weight: 300 }` |
| `cpu_count` | integer | None | Number of usable CPUs. | `cpu_count: 2` |
| `cpu_percent` | integer | None | Usable percentage of available CPUs. | `cpu_percent: 50` |
| `cpu_shares` | integer | None | CPU shares (relative weight). | `cpu_shares: 73` |
| `cpu_period` | integer | None | CPU CFS (Completely Fair Scheduler) period. | `cpu_period: 100000` |
| `cpu_quota` | integer | None | CPU CFS quota. | `cpu_quota: 50000` |
| `cpu_rt_runtime` | integer | None | CPU real-time runtime. | `cpu_rt_runtime: 95000` |
| `cpu_rt_period` | integer | None | CPU real-time period. | `cpu_rt_period: 100000` |
| `cpus` | float | None | Number of CPUs. | `cpus: 1.5` |
| `cpuset` | string | None | CPUs in which to allow execution. | `cpuset: "0,1"` |
| `cap_add` | list | None | Add Linux capabilities. | `cap_add: ["SYS_ADMIN"]` |
| `cap_drop` | list | None | Drop Linux capabilities. | `cap_drop: ["ALL"]` |
| `cgroup` | string | None | Cgroup namespace mode. | `cgroup: "host"` |
| `cgroup_parent` | string | None | Optional parent cgroup. | `cgroup_parent: "m-executor-abcd"` |
| `command` | string/list | None | Override the default command. | `command: ["bundle", "exec", "thin", "-p", "3000"]` |
| `configs` | list | None | Grant access to configs. | `configs: ["my_config"]` |
| `container_name` | string | None | Custom container name. | `container_name: my-web-container` |
| `credential_spec` | object | None | Credential spec for managed service accounts (Windows). | `credential_spec: { file: "my-spec.json" }` |
| `depends_on` | list/object | None | Express dependency between services. | `depends_on: { db: { condition: service_healthy } }` |
| `deploy` | object | None | Configuration for deployment and resource limits. | `deploy: { replicas: 6 }` |
| `develop` | object | None | Configuration for development (Compose Watch). | `develop: { watch: [...] }` |
| `device_cgroup_rules` | list | None | Add rules to the cgroup allowed devices list. | `device_cgroup_rules: ["c 1:3 mr"]` |
| `devices` | list | None | Device mappings. | `devices: ["/dev/ttyUSB0:/dev/ttyUSB0"]` |
| `dns` | string/list | None | Custom DNS servers. | `dns: ["8.8.8.8", "9.9.9.9"]` |
| `dns_opt` | list | None | Custom DNS options. | `dns_opt: ["use-vc", "no-tld-query"]` |
| `dns_search` | string/list | None | Custom DNS search domains. | `dns_search: ["dc1.example.com"]` |
| `domainname` | string | None | Custom domain name. | `domainname: foo.com` |
| `entrypoint` | string/list | None | Override the default entrypoint. | `entrypoint: /code/entrypoint.sh` |
| `env_file` | string/list | None | Add environment variables from a file. | `env_file: .env` |
| `environment` | map/list | None | Add environment variables. | `environment: { RACK_ENV: development }` |
| `expose` | list | None | Expose ports without publishing them to the host. | `expose: ["3000"]` |
| `extends` | string/object | None | Extend another service. | `extends: { file: common.yml, service: webapp }` |
| `external_links` | list | None | Link to containers started outside this compose. | `external_links: ["redis_1", "project_db_1:mysql"]` |
| `extra_hosts` | list/map | None | Add hostname mappings. | `extra_hosts: ["somehost:162.242.195.82"]` |
| `group_add` | list | None | Add additional groups. | `group_add: ["mail"]` |
| `healthcheck` | object | None | Configure a check that's run to determine whether or not containers for this service are "healthy". | `healthcheck: { test: ["CMD", "curl", "-f", "http://localhost"] }` |
| `hostname` | string | None | Custom host name. | `hostname: foo` |
| `image` | string | None | Specify the image to start the container from. | `image: redis:alpine` |
| `init` | boolean | `false` | Run an init inside the container that forwards signals and reaps processes. | `init: true` |
| `ipc` | string | None | IPC namespace to use. | `ipc: host` |
| `isolation` | string | None | Specify a container's isolation technology. | `isolation: default` |
| `labels` | map/list | None | Add metadata to containers. | `labels: { com.example.description: "Accounting webapp" }` |
| `links` | list | None | Link to containers in another service. | `links: ["db", "db:database"]` |
| `logging` | object | None | Logging configuration for the service. | `logging: { driver: syslog, options: { syslog-address: "tcp://192.168.0.42:123" } }` |
| `mac_address` | string | None | MAC address. | `mac_address: 02:42:ac:11:65:43` |
| `mem_limit` | string | None | Memory limit. | `mem_limit: 1g` |
| `mem_reservation` | string | None | Memory soft limit. | `mem_reservation: 512m` |
| `mem_swappiness` | integer | None | Tune a container's memory swappiness behavior. | `mem_swappiness: 60` |
| `memswap_limit` | string | None | Swap limit equal to memory plus swap. | `memswap_limit: 2g` |
| `network_mode` | string | None | Network mode. | `network_mode: "host"` |
| `networks` | list/map | None | Networks to join. | `networks: ["frontend", "backend"]` |
| `oom_kill_disable` | boolean | `false` | Disable OOM Killer. | `oom_kill_disable: true` |
| `oom_score_adj` | integer | None | Tune the host's OOM preferences for containers. | `oom_score_adj: 500` |
| `pid` | string | None | PID namespace to use. | `pid: "host"` |
| `pids_limit` | integer | None | Tune a container's pids limit. | `pids_limit: 100` |
| `platform` | string | None | Target platform containers for this service will run on. | `platform: linux/amd64` |
| `ports` | list | None | Expose ports. | `ports: ["3000", "8000:8000", "9000:8080"]` |
| `privileged` | boolean | `false` | Give extended privileges to this container. | `privileged: true` |
| `profiles` | list | None | Define a list of named profiles for the service to be enabled under. | `profiles: ["frontend", "debug"]` |
| `pull_policy` | string | `always` | Define the decisions Compose makes when it starts to pull images. | `pull_policy: missing` |
| `read_only` | boolean | `false` | Mount the container's root filesystem as read only. | `read_only: true` |
| `restart` | string | `no` | Restart policy. | `restart: always` |
| `runtime` | string | None | Specify the runtime to use for the container. | `runtime: runc` |
| `scale` | integer | `1` | Specify the default number of containers to deploy for this service. | `scale: 3` |
| `secrets` | list | None | Grant access to secrets on a per-service basis. | `secrets: ["my_secret", "my_other_secret"]` |
| `security_opt` | list | None | Override the default labeling scheme for each container. | `security_opt: ["label:user:USER", "label:role:ROLE"]` |
| `shm_size` | string | None | Size of `/dev/shm`. | `shm_size: '2gb'` |
| `stdin_open` | boolean | `false` | Keep STDIN open even if not attached. | `stdin_open: true` |
| `stop_grace_period` | string | `10s` | Specify how long to wait when attempting to stop a container if it doesn't handle SIGTERM. | `stop_grace_period: 1m30s` |
| `stop_signal` | string | `SIGTERM` | Set an alternative signal to stop the container. | `stop_signal: SIGUSR1` |
| `storage_opt` | map | None | Storage driver options for this service. | `storage_opt: { size: '120G' }` |
| `sysctls` | map/list | None | Kernel parameters to set in the container. | `sysctls: { net.core.somaxconn: 1024 }` |
| `tmpfs` | string/list | None | Mount a temporary file system inside the container. | `tmpfs: /run` |
| `tty` | boolean | `false` | Allocate a pseudo-TTY. | `tty: true` |
| `ulimits` | map | None | Override the default ulimits for a container. | `ulimits: { nproc: 65535, nofile: { soft: 20000, hard: 40000 } }` |
| `user` | string | None | Override the user used to run the container process. | `user: "1000:1000"` |
| `userns_mode` | string | None | Disable the user namespace for this service, if Docker daemon is configured with user namespaces. | `userns_mode: "host"` |
| `uts` | string | None | UTS namespace to use. | `uts: "host"` |
| `volumes` | list | None | Mount host paths or named volumes, specified as sub-options to a service. | `volumes: ["/var/lib/mysql", "./cache:/tmp/cache", "datavolume:/var/lib/mysql"]` |
| `volumes_from` | list | None | Mount all of the volumes from another service or container. | `volumes_from: ["service_name", "container_name"]` |
| `working_dir` | string | None | Override the container's working directory. | `working_dir: /code` |

### 1.3 `networks` Attributes

| Attribute | Type | Default | Description | Example |
|---|---|---|---|---|
| `driver` | string | `bridge` | Specify which driver should be used for this network. | `driver: overlay` |
| `driver_opts` | map | None | Specify a list of options as key-value pairs to pass to the driver. | `driver_opts: { com.docker.network.bridge.name: br_1 }` |
| `attachable` | boolean | `false` | Only used when the driver is set to `overlay`. If set to `true`, then standalone containers can attach to this network. | `attachable: true` |
| `enable_ipv6` | boolean | `false` | Enable IPv6 networking. | `enable_ipv6: true` |
| `internal` | boolean | `false` | By default, Docker also connects a bridge network to it to provide external connectivity. If you want to create an externally isolated overlay network, you can set this option to `true`. | `internal: true` |
| `labels` | map/list | None | Add metadata to containers. | `labels: { com.example.description: "Financial transaction network" }` |
| `external` | boolean | `false` | If set to `true`, specifies that this network has been created outside of Compose. | `external: true` |
| `name` | string | None | Set a custom name for this network. | `name: my-app-net` |
| `ipam` | object | None | Specify custom IPAM config. | `ipam: { driver: default, config: [{ subnet: "172.28.0.0/16" }] }` |

### 1.4 `volumes` Attributes

| Attribute | Type | Default | Description | Example |
|---|---|---|---|---|
| `driver` | string | `local` | Specify which volume driver should be used for this volume. | `driver: foobar` |
| `driver_opts` | map | None | Specify a list of options as key-value pairs to pass to the driver for this volume. | `driver_opts: { type: "nfs", o: "addr=10.40.0.199,nolock,soft,rw", device: ":/docker/example" }` |
| `external` | boolean | `false` | If set to `true`, specifies that this volume has been created outside of Compose. | `external: true` |
| `labels` | map/list | None | Add metadata to containers. | `labels: { com.example.description: "Database volume" }` |
| `name` | string | None | Set a custom name for this volume. | `name: my-app-data` |

### 1.5 `configs` Attributes

| Attribute | Type | Default | Description | Example |
|---|---|---|---|---|
| `file` | string | None | The config is created with the contents of the file at the specified path. | `file: ./my_config.txt` |
| `external` | boolean | `false` | If set to `true`, specifies that this config has already been created. | `external: true` |
| `name` | string | None | The name of the config object in Docker. | `name: my_config` |
| `content` | string | None | The content of the config. | `content: | 
  server {
    listen 80;
  }` |

### 1.6 `secrets` Attributes

| Attribute | Type | Default | Description | Example |
|---|---|---|---|---|
| `file` | string | None | The secret is created with the contents of the file at the specified path. | `file: ./my_secret.txt` |
| `environment` | string | None | The secret is created with the value of an environment variable. | `environment: "MY_SECRET"` |
| `external` | boolean | `false` | If set to `true`, specifies that this secret has already been created. | `external: true` |
| `name` | string | None | The name of the secret object in Docker. | `name: my_secret` |

## 2. Dockerfile Instruction Reference

A complete reference for every Dockerfile instruction.

### `FROM`
Initializes a new build stage and sets the Base Image for subsequent instructions.
- Syntax: `FROM [--platform=<platform>] <image> [AS <name>]` or `FROM [--platform=<platform>] <image>[:<tag>] [AS <name>]` or `FROM [--platform=<platform>] <image>[@<digest>] [AS <name>]`
- Example: `FROM --platform=linux/amd64 ubuntu:22.04 AS builder`

### `RUN`
Executes any commands in a new layer on top of the current image and commits the results.
- Syntax: `RUN <command>` (shell form) or `RUN ["executable", "param1", "param2"]` (exec form)
- Flags: `--mount=type=cache|bind|secret|ssh`, `--network=default|none|host`
- Example: `RUN --mount=type=cache,target=/var/cache/apt apt-get update && apt-get install -y curl`

### `CMD`
Provides defaults for an executing container. There can only be one `CMD` instruction in a Dockerfile.
- Syntax: `CMD ["executable","param1","param2"]` (exec form, preferred) or `CMD ["param1","param2"]` (as default parameters to ENTRYPOINT) or `CMD command param1 param2` (shell form)
- Example: `CMD ["node", "server.js"]`

### `LABEL`
Adds metadata to an image.
- Syntax: `LABEL <key>=<value> <key>=<value> <key>=<value> ...`
- Example: `LABEL org.opencontainers.image.authors="team@example.com"`

### `EXPOSE`
Informs Docker that the container listens on the specified network ports at runtime.
- Syntax: `EXPOSE <port> [<port>/<protocol>...]`
- Example: `EXPOSE 80/tcp 80/udp`

### `ENV`
Sets the environment variable `<key>` to the value `<value>`.
- Syntax: `ENV <key>=<value> ...`
- Example: `ENV NODE_ENV=production PORT=3000`

### `ADD`
Copies new files, directories or remote file URLs from `<src>` and adds them to the filesystem of the image at the path `<dest>`.
- Syntax: `ADD [--chown=<user>:<group>] [--chmod=<perms>] [--checksum=<checksum>] <src>... <dest>`
- Example: `ADD https://example.com/big.tar.xz /usr/src/things/`

### `COPY`
Copies new files or directories from `<src>` and adds them to the filesystem of the container at the path `<dest>`.
- Syntax: `COPY [--chown=<user>:<group>] [--chmod=<perms>] <src>... <dest>`
- Example: `COPY --chown=node:node package*.json ./`

### `ENTRYPOINT`
Allows you to configure a container that will run as an executable.
- Syntax: `ENTRYPOINT ["executable", "param1", "param2"]` (exec form, preferred) or `ENTRYPOINT command param1 param2` (shell form)
- Example: `ENTRYPOINT ["docker-entrypoint.sh"]`

### `VOLUME`
Creates a mount point with the specified name and marks it as holding externally mounted volumes from native host or other containers.
- Syntax: `VOLUME ["/data"]`
- Example: `VOLUME /var/lib/mysql`

### `USER`
Sets the user name (or UID) and optionally the user group (or GID) to use when running the image and for any `RUN`, `CMD` and `ENTRYPOINT` instructions that follow it in the Dockerfile.
- Syntax: `USER <user>[:<group>]` or `USER <UID>[:<GID>]`
- Example: `USER 1000:1000`

### `WORKDIR`
Sets the working directory for any `RUN`, `CMD`, `ENTRYPOINT`, `COPY` and `ADD` instructions that follow it in the Dockerfile.
- Syntax: `WORKDIR /path/to/workdir`
- Example: `WORKDIR /app`

### `ARG`
Defines a variable that users can pass at build-time to the builder with the `docker build` command using the `--build-arg <varname>=<value>` flag.
- Syntax: `ARG <name>[=<default value>]`
- Example: `ARG VERSION=latest`

### `ONBUILD`
Adds to the image a trigger instruction to be executed at a later time, when the image is used as the base for another build.
- Syntax: `ONBUILD <INSTRUCTION>`
- Example: `ONBUILD COPY . /app/src`

### `STOPSIGNAL`
Sets the system call signal that will be sent to the container to exit.
- Syntax: `STOPSIGNAL signal`
- Example: `STOPSIGNAL SIGKILL`

### `HEALTHCHECK`
Tells Docker how to test a container to check that it is still working.
- Syntax: `HEALTHCHECK [OPTIONS] CMD command` or `HEALTHCHECK NONE`
- Options: `--interval=DURATION` (default: 30s), `--timeout=DURATION` (default: 30s), `--start-period=DURATION` (default: 0s), `--retries=N` (default: 3)
- Example: `HEALTHCHECK --interval=5m --timeout=3s CMD curl -f http://localhost/ || exit 1`

### `SHELL`
Allows the default shell used for the shell form of commands to be overridden.
- Syntax: `SHELL ["executable", "parameters"]`
- Example: `SHELL ["powershell", "-command"]`

## 3. `daemon.json` Complete Reference

The `daemon.json` file configures the Docker daemon.

| Field | Type | Default | Description |
|---|---|---|---|
| `storage-driver` | string | `overlay2` | The storage driver to use. |
| `log-driver` | string | `json-file` | The default logging driver. |
| `log-opts` | map | None | Options for the logging driver. |
| `default-address-pools` | list | None | Default address pools for node networks. |
| `dns` | list | None | DNS servers to use. |
| `registry-mirrors` | list | None | Registry mirrors to use. |
| `insecure-registries` | list | None | Insecure registries to allow. |
| `live-restore` | boolean | `false` | Enable live restore of docker when containers are still running. |
| `default-runtime` | string | `runc` | Default OCI runtime for containers. |
| `runtimes` | map | None | Register additional OCI runtimes. |
| `features` | map | None | Enable/disable specific features. |
| `builder` | map | None | BuildKit configuration. |
| `containerd` | string | None | Path to containerd socket. |
| `default-cgroupns-mode` | string | `private` | Default cgroup namespace mode. |
| `exec-opts` | list | None | Execution options. |
| `experimental` | boolean | `false` | Enable experimental features. |
| `fixed-cidr` | string | None | IPv4 subnet for fixed IPs. |
| `fixed-cidr-v6` | string | None | IPv6 subnet for fixed IPs. |
| `group` | string | `docker` | Group for the unix socket. |
| `hosts` | list | None | Daemon socket(s) to connect to. |
| `icc` | boolean | `true` | Enable inter-container communication. |
| `ip` | string | `0.0.0.0` | Default IP when binding container ports. |
| `ip-forward` | boolean | `true` | Enable net.ipv4.ip_forward. |
| `iptables` | boolean | `true` | Enable addition of iptables rules. |
| `ip-masq` | boolean | `true` | Enable IP masquerading. |
| `labels` | list | None | Daemon labels. |
| `max-concurrent-downloads` | integer | `3` | Max concurrent downloads. |
| `max-concurrent-uploads` | integer | `5` | Max concurrent uploads. |
| `max-download-attempts` | integer | `5` | Max download attempts. |
| `metrics-addr` | string | None | Address to serve metrics API. |
| `no-new-privileges` | boolean | `false` | Set no-new-privileges by default for new containers. |
| `oom-score-adjust` | integer | `-500` | Set the oom_score_adj for the daemon. |
| `pidfile` | string | `/var/run/docker.pid` | Path to use for daemon PID file. |
| `raw-logs` | boolean | `false` | Full timestamps without ANSI coloring. |
| `seccomp-profile` | string | None | Path to seccomp profile. |
| `selinux-enabled` | boolean | `false` | Enable selinux support. |
| `shutdown-timeout` | integer | `15` | Default timeout for stopping containers. |
| `tls` | boolean | `false` | Use TLS; implied by --tlsverify. |
| `tlscacert` | string | `~/.docker/ca.pem` | Trust certs signed only by this CA. |
| `tlscert` | string | `~/.docker/cert.pem` | Path to TLS certificate file. |
| `tlskey` | string | `~/.docker/key.pem` | Path to TLS key file. |
| `tlsverify` | boolean | `false` | Use TLS and verify the remote. |
| `userland-proxy` | boolean | `true` | Use userland proxy for loopback traffic. |
| `userns-remap` | string | None | User namespace remapping. |

## 4. `.dockerignore` Patterns

The `.dockerignore` file excludes files and directories from the build context.

### Syntax
- `#` for comments.
- `*` matches any sequence of non-separator characters.
- `?` matches any single non-separator character.
- `**` matches any number of directories.
- `!` negates a pattern.

### Common Patterns

**Node.js:**
```dockerignore
node_modules
npm-debug.log
Dockerfile
.dockerignore
.git
.gitignore
README.md
```

**Python:**
```dockerignore
__pycache__
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.env
Dockerfile
.dockerignore
.git
```

**Go:**
```dockerignore
bin/
obj/
*.exe
*.dll
*.so
*.dylib
Dockerfile
.dockerignore
.git
```

## 5. BuildKit Configuration (`buildkitd.toml`)

BuildKit can be configured via `buildkitd.toml`.

```toml
debug = true
# root is where all buildkit state is stored.
root = "/var/lib/buildkit"
# insecure-entitlements allows insecure entitlements, disabled by default.
insecure-entitlements = [ "network.host", "security.insecure" ]

[grpc]
  address = [ "tcp://0.0.0.0:1234" ]
  # debugAddress is address for attaching go pprof and expvar.
  debugAddress = "0.0.0.0:6060"
  uid = 0
  gid = 0
  [grpc.tls]
    cert = "/etc/buildkit/tls.crt"
    key = "/etc/buildkit/tls.key"
    ca = "/etc/buildkit/tlsca.crt"

[worker.oci]
  enabled = true
  # platforms is manually configure platforms, auto-detected by default.
  platforms = [ "linux/amd64", "linux/arm64" ]
  snapshotter = "auto" # overlayfs or native, default auto will try to use overlayfs
  rootless = false # see docs/rootless.md for more details on rootless mode.
  # Whether run subprocesses in main cgroup or create top-level cgroup.
  # Default is "cgroupfs" when not running rootless.
  cgroup-parent = "cgroupfs"
  # gc keeps/frees disk space.
  gc = true
  gckeepstorage = 9000
  [[worker.oci.gcpolicy]]
    keepBytes = 512000000
    keepDuration = 172800
    filters = [ "type==source.local", "type==exec.cachemount", "type==source.git.checkout"]
  [[worker.oci.gcpolicy]]
    all = true
    keepBytes = 1024000000

[worker.containerd]
  address = "/run/containerd/containerd.sock"
  enabled = true
  platforms = [ "linux/amd64", "linux/arm64" ]
  namespace = "buildkit"
  gc = true
  # gckeepstorage sets storage limit for default gc profile, in MB.
  gckeepstorage = 9000

[registry."docker.io"]
  mirrors = ["YOUR_REGISTRY_MIRROR"]
  http = true
  insecure = true
```

## 6. Docker Context Configuration

Docker contexts allow you to manage multiple Docker environments.

- Create a context: `docker context create my-context --docker "host=ssh://user@remote-host"`
- Use a context: `docker context use my-context`
- List contexts: `docker context ls`
- Inspect a context: `docker context inspect my-context`

## 7. Registry Configuration (`config.yml`)

Configuration for a private Docker registry.

```yaml
version: 0.1
log:
  fields:
    service: registry
storage:
  cache:
    blobdescriptor: inmemory
  filesystem:
    rootdirectory: /var/lib/registry
http:
  addr: :5000
  headers:
    X-Content-Type-Options: [nosniff]
health:
  storagedriver:
    enabled: true
    interval: 10s
    threshold: 3
```

## 8. Production `compose.yaml` Templates

### 8.1 Web App Stack

```yaml
services:
  webapp:
    image: YOUR_REGISTRY/webapp:v1.2.3
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    environment:
      - NODE_ENV=production
    secrets:
      - db_password
    networks:
      - frontend
      - backend
    deploy:
      replicas: 3
      update_config:
        parallelism: 1
        delay: 10s
      restart_policy:
        condition: on-failure
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"

networks:
  frontend:
  backend:
    internal: true

secrets:
  db_password:
    external: true
```

### 8.2 Database Stack

```yaml
services:
  db:
    image: postgres:15-alpine
    restart: always
    environment:
      POSTGRES_USER: admin
      POSTGRES_PASSWORD_FILE: /run/secrets/db_password
      POSTGRES_DB: myapp
    volumes:
      - db-data:/var/lib/postgresql/data
    secrets:
      - db_password
    networks:
      - backend
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 4G
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U admin -d myapp"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  db-data:

networks:
  backend:
    internal: true

secrets:
  db_password:
    external: true
```

### 8.3 Monitoring Stack (Prometheus/Grafana)

```yaml
services:
  prometheus:
    image: prom/prometheus:v2.45.0
    restart: unless-stopped
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml:ro
      - prometheus-data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--web.console.libraries=/etc/prometheus/console_libraries'
      - '--web.console.templates=/etc/prometheus/consoles'
      - '--web.enable-lifecycle'
    ports:
      - "9090:9090"
    networks:
      - monitoring

  grafana:
    image: grafana/grafana:10.0.3
    restart: unless-stopped
    volumes:
      - grafana-data:/var/lib/grafana
    environment:
      - GF_SECURITY_ADMIN_PASSWORD__FILE=/run/secrets/grafana_password
    secrets:
      - grafana_password
    ports:
      - "3000:3000"
    networks:
      - monitoring
    depends_on:
      - prometheus

volumes:
  prometheus-data:
  grafana-data:

networks:
  monitoring:

secrets:
  grafana_password:
    external: true
```

### 8.4 ELK Stack

```yaml
services:
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.9.0
    environment:
      - discovery.type=single-node
      - xpack.security.enabled=false
      - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
    volumes:
      - es-data:/usr/share/elasticsearch/data
    ports:
      - "9200:9200"
    networks:
      - elk

  logstash:
    image: docker.elastic.co/logstash/logstash:8.9.0
    volumes:
      - ./logstash.conf:/usr/share/logstash/pipeline/logstash.conf:ro
    ports:
      - "5044:5044"
    networks:
      - elk
    depends_on:
      - elasticsearch

  kibana:
    image: docker.elastic.co/kibana/kibana:8.9.0
    ports:
      - "5601:5601"
    networks:
      - elk
    depends_on:
      - elasticsearch

volumes:
  es-data:

networks:
  elk:
```

## 9. Troubleshooting and Optimization

### 9.1 Common Errors and Solutions

- **"port already in use"**: Use `lsof -i :PORT` to find the conflicting process, or change the port mapping in `compose.yaml`.
- **"no space left on device"**: Run `docker system prune -a --volumes` to clear unused data. Check the `overlay2` directory size.
- **"OOM killed"**: The container exceeded its memory limit. Increase the `mem_limit` in `compose.yaml` or optimize the application's memory usage.
- **"permission denied"**: Check the user/group permissions of the mounted volumes. Ensure the container user has access.
- **"network not found"**: Run `docker network create <network_name>` or ensure the network is defined in `compose.yaml`.
- **"image not found"**: Verify the registry URL, image tag, and `pull_policy`. Ensure you are logged in to the registry.
- **"container unhealthy"**: Check the `healthcheck` command and logs. Increase the `timeout` or `start_period` if the application takes longer to start.
- **"bind mount permission denied"**: On SELinux systems, append `:z` or `:Z` to the volume mount path (e.g., `./data:/data:z`).
- **"DNS resolution failed"**: Check the host's DNS settings or configure custom DNS servers in `daemon.json` or `compose.yaml`.
- **"cannot start service"**: Check `depends_on` conditions. Ensure required services are healthy before starting dependent services.
- **"exec format error"**: The image architecture does not match the host architecture (e.g., running an ARM image on an AMD64 host). Use `docker buildx` to build multi-platform images.
- **"context deadline exceeded"**: Increase the timeout for Docker commands or check network connectivity to the registry.

### 9.2 Cost and Time Optimization

- **Multi-stage builds**: Use multi-stage builds to create smaller final images. This reduces pull times and storage costs.
- **Layer caching**: Order Dockerfile instructions from least frequently changed to most frequently changed to maximize cache hits.
- **BuildKit cache mounts**: Use `--mount=type=cache` to cache package manager downloads (e.g., `apt`, `npm`, `pip`) between builds.
- **Parallel builds**: Use `docker compose build --parallel` to build multiple services concurrently.
- **Image pull policy**: Set `pull_policy: if-not-present` to avoid unnecessary image pulls.
- **Resource limits**: Set CPU and memory limits to prevent runaway containers from consuming all host resources.
- **Logging**: Configure log rotation (`max-size`, `max-file`) to prevent log files from filling up the disk.
- **Prune**: Regularly run `docker system prune` and `docker volume prune` to remove unused resources.
- **Compose profiles**: Use profiles to start only the services needed for a specific environment or task.
- **Compose watch**: Use `develop: watch` for fast iteration during development without rebuilding images.

### 9.3 Security Hardening

- **Non-root user**: Run containers as a non-root user (`USER 1000:1000`).
- **Read-only root filesystem**: Set `read_only: true` to prevent modifications to the container's root filesystem.
- **Drop capabilities**: Drop all Linux capabilities (`cap_drop: ["ALL"]`) and add only the necessary ones.
- **No new privileges**: Set `security_opt: ["no-new-privileges:true"]` to prevent processes from gaining additional privileges.
- **Seccomp profiles**: Use custom seccomp profiles to restrict system calls.
- **Resource limits**: Enforce CPU, memory, and PID limits to prevent denial-of-service attacks.
- **No privileged mode**: Avoid using `privileged: true` unless absolutely necessary.
- **Minimal base images**: Use minimal base images like `alpine`, `distroless`, or `scratch` to reduce the attack surface.
- **Secrets management**: Use Docker secrets instead of environment variables for sensitive data.
- **Network segmentation**: Use internal networks to isolate backend services from the public internet.

### 9.4 Upgrade Strategies

- **Blue-green deployment**: Run the new version alongside the old version and switch traffic when ready.
- **Rolling update**: Use `update_config` with `parallelism` and `delay` to update containers one by one.
- **Canary release**: Route a small percentage of traffic to the new version to test it before a full rollout.
- **Database migrations**: Run database migrations as an init container or a pre-start hook before starting the application.
- **Rollback**: Configure `rollback_config` to automatically roll back to the previous version if the update fails.
- **Zero-downtime**: Use `order: start-first` in `update_config` to start the new container before stopping the old one.
# Docker Super Specialist: Complete Configuration Reference

## 1. `compose.yaml` Complete Schema Reference

The `compose.yaml` file is the heart of Docker Compose. Below is the exhaustive reference for every top-level element and nested option.

### 1.1 Top-Level Elements

- `version`: (Deprecated) No longer required in Compose V2.
- `name`: Sets the project name. Overrides the directory name.
- `services`: Defines the containers to run.
- `networks`: Defines the networks to be created or used.
- `volumes`: Defines the persistent volumes.
- `configs`: Defines configuration files to be mounted.
- `secrets`: Defines sensitive data to be mounted securely.

### 1.2 `services` Attributes

Every service can have the following attributes:

| Attribute | Type | Default | Description | Example |
|---|---|---|---|---|
| `annotations` | map/list | None | Metadata for the container. | `annotations: { "com.example.foo": "bar" }` |
| `attach` | boolean | `true` | Whether to attach to the container's output. | `attach: false` |
| `build` | string/object | None | Configuration for building the image. | `build: ./dir` or `build: { context: ., dockerfile: Dockerfile.alt }` |
| `blkio_config` | object | None | Block IO configuration. | `blkio_config: { weight: 300 }` |
| `cpu_count` | integer | None | Number of usable CPUs. | `cpu_count: 2` |
| `cpu_percent` | integer | None | Usable percentage of available CPUs. | `cpu_percent: 50` |
| `cpu_shares` | integer | None | CPU shares (relative weight). | `cpu_shares: 73` |
| `cpu_period` | integer | None | CPU CFS (Completely Fair Scheduler) period. | `cpu_period: 100000` |
| `cpu_quota` | integer | None | CPU CFS quota. | `cpu_quota: 50000` |
| `cpu_rt_runtime` | integer | None | CPU real-time runtime. | `cpu_rt_runtime: 95000` |
| `cpu_rt_period` | integer | None | CPU real-time period. | `cpu_rt_period: 100000` |
| `cpus` | float | None | Number of CPUs. | `cpus: 1.5` |
| `cpuset` | string | None | CPUs in which to allow execution. | `cpuset: "0,1"` |
| `cap_add` | list | None | Add Linux capabilities. | `cap_add: ["SYS_ADMIN"]` |
| `cap_drop` | list | None | Drop Linux capabilities. | `cap_drop: ["ALL"]` |
| `cgroup` | string | None | Cgroup namespace mode. | `cgroup: "host"` |
| `cgroup_parent` | string | None | Optional parent cgroup. | `cgroup_parent: "m-executor-abcd"` |
| `command` | string/list | None | Override the default command. | `command: ["bundle", "exec", "thin", "-p", "3000"]` |
| `configs` | list | None | Grant access to configs. | `configs: ["my_config"]` |
| `container_name` | string | None | Custom container name. | `container_name: my-web-container` |
| `credential_spec` | object | None | Credential spec for managed service accounts (Windows). | `credential_spec: { file: "my-spec.json" }` |
| `depends_on` | list/object | None | Express dependency between services. | `depends_on: { db: { condition: service_healthy } }` |
| `deploy` | object | None | Configuration for deployment and resource limits. | `deploy: { replicas: 6 }` |
| `develop` | object | None | Configuration for development (Compose Watch). | `develop: { watch: [...] }` |
| `device_cgroup_rules` | list | None | Add rules to the cgroup allowed devices list. | `device_cgroup_rules: ["c 1:3 mr"]` |
| `devices` | list | None | Device mappings. | `devices: ["/dev/ttyUSB0:/dev/ttyUSB0"]` |
| `dns` | string/list | None | Custom DNS servers. | `dns: ["8.8.8.8", "9.9.9.9"]` |
| `dns_opt` | list | None | Custom DNS options. | `dns_opt: ["use-vc", "no-tld-query"]` |
| `dns_search` | string/list | None | Custom DNS search domains. | `dns_search: ["dc1.example.com"]` |
| `domainname` | string | None | Custom domain name. | `domainname: foo.com` |
| `entrypoint` | string/list | None | Override the default entrypoint. | `entrypoint: /code/entrypoint.sh` |
| `env_file` | string/list | None | Add environment variables from a file. | `env_file: .env` |
| `environment` | map/list | None | Add environment variables. | `environment: { RACK_ENV: development }` |
| `expose` | list | None | Expose ports without publishing them to the host. | `expose: ["3000"]` |
| `extends` | string/object | None | Extend another service. | `extends: { file: common.yml, service: webapp }` |
| `external_links` | list | None | Link to containers started outside this compose. | `external_links: ["redis_1", "project_db_1:mysql"]` |
| `extra_hosts` | list/map | None | Add hostname mappings. | `extra_hosts: ["somehost:162.242.195.82"]` |
| `group_add` | list | None | Add additional groups. | `group_add: ["mail"]` |
| `healthcheck` | object | None | Configure a check that's run to determine whether or not containers for this service are "healthy". | `healthcheck: { test: ["CMD", "curl", "-f", "http://localhost"] }` |
| `hostname` | string | None | Custom host name. | `hostname: foo` |
| `image` | string | None | Specify the image to start the container from. | `image: redis:alpine` |
| `init` | boolean | `false` | Run an init inside the container that forwards signals and reaps processes. | `init: true` |
| `ipc` | string | None | IPC namespace to use. | `ipc: host` |
| `isolation` | string | None | Specify a container's isolation technology. | `isolation: default` |
| `labels` | map/list | None | Add metadata to containers. | `labels: { com.example.description: "Accounting webapp" }` |
| `links` | list | None | Link to containers in another service. | `links: ["db", "db:database"]` |
| `logging` | object | None | Logging configuration for the service. | `logging: { driver: syslog, options: { syslog-address: "tcp://192.168.0.42:123" } }` |
| `mac_address` | string | None | MAC address. | `mac_address: 02:42:ac:11:65:43` |
| `mem_limit` | string | None | Memory limit. | `mem_limit: 1g` |
| `mem_reservation` | string | None | Memory soft limit. | `mem_reservation: 512m` |
| `mem_swappiness` | integer | None | Tune a container's memory swappiness behavior. | `mem_swappiness: 60` |
| `memswap_limit` | string | None | Swap limit equal to memory plus swap. | `memswap_limit: 2g` |
| `network_mode` | string | None | Network mode. | `network_mode: "host"` |
| `networks` | list/map | None | Networks to join. | `networks: ["frontend", "backend"]` |
| `oom_kill_disable` | boolean | `false` | Disable OOM Killer. | `oom_kill_disable: true` |
| `oom_score_adj` | integer | None | Tune the host's OOM preferences for containers. | `oom_score_adj: 500` |
| `pid` | string | None | PID namespace to use. | `pid: "host"` |
| `pids_limit` | integer | None | Tune a container's pids limit. | `pids_limit: 100` |
| `platform` | string | None | Target platform containers for this service will run on. | `platform: linux/amd64` |
| `ports` | list | None | Expose ports. | `ports: ["3000", "8000:8000", "9000:8080"]` |
| `privileged` | boolean | `false` | Give extended privileges to this container. | `privileged: true` |
| `profiles` | list | None | Define a list of named profiles for the service to be enabled under. | `profiles: ["frontend", "debug"]` |
| `pull_policy` | string | `always` | Define the decisions Compose makes when it starts to pull images. | `pull_policy: missing` |
| `read_only` | boolean | `false` | Mount the container's root filesystem as read only. | `read_only: true` |
| `restart` | string | `no` | Restart policy. | `restart: always` |
| `runtime` | string | None | Specify the runtime to use for the container. | `runtime: runc` |
| `scale` | integer | `1` | Specify the default number of containers to deploy for this service. | `scale: 3` |
| `secrets` | list | None | Grant access to secrets on a per-service basis. | `secrets: ["my_secret", "my_other_secret"]` |
| `security_opt` | list | None | Override the default labeling scheme for each container. | `security_opt: ["label:user:USER", "label:role:ROLE"]` |
| `shm_size` | string | None | Size of `/dev/shm`. | `shm_size: '2gb'` |
| `stdin_open` | boolean | `false` | Keep STDIN open even if not attached. | `stdin_open: true` |
| `stop_grace_period` | string | `10s` | Specify how long to wait when attempting to stop a container if it doesn't handle SIGTERM. | `stop_grace_period: 1m30s` |
| `stop_signal` | string | `SIGTERM` | Set an alternative signal to stop the container. | `stop_signal: SIGUSR1` |
| `storage_opt` | map | None | Storage driver options for this service. | `storage_opt: { size: '120G' }` |
| `sysctls` | map/list | None | Kernel parameters to set in the container. | `sysctls: { net.core.somaxconn: 1024 }` |
| `tmpfs` | string/list | None | Mount a temporary file system inside the container. | `tmpfs: /run` |
| `tty` | boolean | `false` | Allocate a pseudo-TTY. | `tty: true` |
| `ulimits` | map | None | Override the default ulimits for a container. | `ulimits: { nproc: 65535, nofile: { soft: 20000, hard: 40000 } }` |
| `user` | string | None | Override the user used to run the container process. | `user: "1000:1000"` |
| `userns_mode` | string | None | Disable the user namespace for this service, if Docker daemon is configured with user namespaces. | `userns_mode: "host"` |
| `uts` | string | None | UTS namespace to use. | `uts: "host"` |
| `volumes` | list | None | Mount host paths or named volumes, specified as sub-options to a service. | `volumes: ["/var/lib/mysql", "./cache:/tmp/cache", "datavolume:/var/lib/mysql"]` |
| `volumes_from` | list | None | Mount all of the volumes from another service or container. | `volumes_from: ["service_name", "container_name"]` |
| `working_dir` | string | None | Override the container's working directory. | `working_dir: /code` |

### 1.3 `networks` Attributes

| Attribute | Type | Default | Description | Example |
|---|---|---|---|---|
| `driver` | string | `bridge` | Specify which driver should be used for this network. | `driver: overlay` |
| `driver_opts` | map | None | Specify a list of options as key-value pairs to pass to the driver. | `driver_opts: { com.docker.network.bridge.name: br_1 }` |
| `attachable` | boolean | `false` | Only used when the driver is set to `overlay`. If set to `true`, then standalone containers can attach to this network. | `attachable: true` |
| `enable_ipv6` | boolean | `false` | Enable IPv6 networking. | `enable_ipv6: true` |
| `internal` | boolean | `false` | By default, Docker also connects a bridge network to it to provide external connectivity. If you want to create an externally isolated overlay network, you can set this option to `true`. | `internal: true` |
| `labels` | map/list | None | Add metadata to containers. | `labels: { com.example.description: "Financial transaction network" }` |
| `external` | boolean | `false` | If set to `true`, specifies that this network has been created outside of Compose. | `external: true` |
| `name` | string | None | Set a custom name for this network. | `name: my-app-net` |
| `ipam` | object | None | Specify custom IPAM config. | `ipam: { driver: default, config: [{ subnet: "172.28.0.0/16" }] }` |

### 1.4 `volumes` Attributes

| Attribute | Type | Default | Description | Example |
|---|---|---|---|---|
| `driver` | string | `local` | Specify which volume driver should be used for this volume. | `driver: foobar` |
| `driver_opts` | map | None | Specify a list of options as key-value pairs to pass to the driver for this volume. | `driver_opts: { type: "nfs", o: "addr=10.40.0.199,nolock,soft,rw", device: ":/docker/example" }` |
| `external` | boolean | `false` | If set to `true`, specifies that this volume has been created outside of Compose. | `external: true` |
| `labels` | map/list | None | Add metadata to containers. | `labels: { com.example.description: "Database volume" }` |
| `name` | string | None | Set a custom name for this volume. | `name: my-app-data` |

### 1.5 `configs` Attributes

| Attribute | Type | Default | Description | Example |
|---|---|---|---|---|
| `file` | string | None | The config is created with the contents of the file at the specified path. | `file: ./my_config.txt` |
| `external` | boolean | `false` | If set to `true`, specifies that this config has already been created. | `external: true` |
| `name` | string | None | The name of the config object in Docker. | `name: my_config` |
| `content` | string | None | The content of the config. | `content: | 
  server {
    listen 80;
  }` |

### 1.6 `secrets` Attributes

| Attribute | Type | Default | Description | Example |
|---|---|---|---|---|
| `file` | string | None | The secret is created with the contents of the file at the specified path. | `file: ./my_secret.txt` |
| `environment` | string | None | The secret is created with the value of an environment variable. | `environment: "MY_SECRET"` |
| `external` | boolean | `false` | If set to `true`, specifies that this secret has already been created. | `external: true` |
| `name` | string | None | The name of the secret object in Docker. | `name: my_secret` |

## 2. Dockerfile Instruction Reference

A complete reference for every Dockerfile instruction.

### `FROM`
Initializes a new build stage and sets the Base Image for subsequent instructions.
- Syntax: `FROM [--platform=<platform>] <image> [AS <name>]` or `FROM [--platform=<platform>] <image>[:<tag>] [AS <name>]` or `FROM [--platform=<platform>] <image>[@<digest>] [AS <name>]`
- Example: `FROM --platform=linux/amd64 ubuntu:22.04 AS builder`

### `RUN`
Executes any commands in a new layer on top of the current image and commits the results.
- Syntax: `RUN <command>` (shell form) or `RUN ["executable", "param1", "param2"]` (exec form)
- Flags: `--mount=type=cache|bind|secret|ssh`, `--network=default|none|host`
- Example: `RUN --mount=type=cache,target=/var/cache/apt apt-get update && apt-get install -y curl`

### `CMD`
Provides defaults for an executing container. There can only be one `CMD` instruction in a Dockerfile.
- Syntax: `CMD ["executable","param1","param2"]` (exec form, preferred) or `CMD ["param1","param2"]` (as default parameters to ENTRYPOINT) or `CMD command param1 param2` (shell form)
- Example: `CMD ["node", "server.js"]`

### `LABEL`
Adds metadata to an image.
- Syntax: `LABEL <key>=<value> <key>=<value> <key>=<value> ...`
- Example: `LABEL org.opencontainers.image.authors="team@example.com"`

### `EXPOSE`
Informs Docker that the container listens on the specified network ports at runtime.
- Syntax: `EXPOSE <port> [<port>/<protocol>...]`
- Example: `EXPOSE 80/tcp 80/udp`

### `ENV`
Sets the environment variable `<key>` to the value `<value>`.
- Syntax: `ENV <key>=<value> ...`
- Example: `ENV NODE_ENV=production PORT=3000`

### `ADD`
Copies new files, directories or remote file URLs from `<src>` and adds them to the filesystem of the image at the path `<dest>`.
- Syntax: `ADD [--chown=<user>:<group>] [--chmod=<perms>] [--checksum=<checksum>] <src>... <dest>`
- Example: `ADD https://example.com/big.tar.xz /usr/src/things/`

### `COPY`
Copies new files or directories from `<src>` and adds them to the filesystem of the container at the path `<dest>`.
- Syntax: `COPY [--chown=<user>:<group>] [--chmod=<perms>] <src>... <dest>`
- Example: `COPY --chown=node:node package*.json ./`

### `ENTRYPOINT`
Allows you to configure a container that will run as an executable.
- Syntax: `ENTRYPOINT ["executable", "param1", "param2"]` (exec form, preferred) or `ENTRYPOINT command param1 param2` (shell form)
- Example: `ENTRYPOINT ["docker-entrypoint.sh"]`

### `VOLUME`
Creates a mount point with the specified name and marks it as holding externally mounted volumes from native host or other containers.
- Syntax: `VOLUME ["/data"]`
- Example: `VOLUME /var/lib/mysql`

### `USER`
Sets the user name (or UID) and optionally the user group (or GID) to use when running the image and for any `RUN`, `CMD` and `ENTRYPOINT` instructions that follow it in the Dockerfile.
- Syntax: `USER <user>[:<group>]` or `USER <UID>[:<GID>]`
- Example: `USER 1000:1000`

### `WORKDIR`
Sets the working directory for any `RUN`, `CMD`, `ENTRYPOINT`, `COPY` and `ADD` instructions that follow it in the Dockerfile.
- Syntax: `WORKDIR /path/to/workdir`
- Example: `WORKDIR /app`

### `ARG`
Defines a variable that users can pass at build-time to the builder with the `docker build` command using the `--build-arg <varname>=<value>` flag.
- Syntax: `ARG <name>[=<default value>]`
- Example: `ARG VERSION=latest`

### `ONBUILD`
Adds to the image a trigger instruction to be executed at a later time, when the image is used as the base for another build.
- Syntax: `ONBUILD <INSTRUCTION>`
- Example: `ONBUILD COPY . /app/src`

### `STOPSIGNAL`
Sets the system call signal that will be sent to the container to exit.
- Syntax: `STOPSIGNAL signal`
- Example: `STOPSIGNAL SIGKILL`

### `HEALTHCHECK`
Tells Docker how to test a container to check that it is still working.
- Syntax: `HEALTHCHECK [OPTIONS] CMD command` or `HEALTHCHECK NONE`
- Options: `--interval=DURATION` (default: 30s), `--timeout=DURATION` (default: 30s), `--start-period=DURATION` (default: 0s), `--retries=N` (default: 3)
- Example: `HEALTHCHECK --interval=5m --timeout=3s CMD curl -f http://localhost/ || exit 1`

### `SHELL`
Allows the default shell used for the shell form of commands to be overridden.
- Syntax: `SHELL ["executable", "parameters"]`
- Example: `SHELL ["powershell", "-command"]`

## 3. `daemon.json` Complete Reference

The `daemon.json` file configures the Docker daemon.

| Field | Type | Default | Description |
|---|---|---|---|
| `storage-driver` | string | `overlay2` | The storage driver to use. |
| `log-driver` | string | `json-file` | The default logging driver. |
| `log-opts` | map | None | Options for the logging driver. |
| `default-address-pools` | list | None | Default address pools for node networks. |
| `dns` | list | None | DNS servers to use. |
| `registry-mirrors` | list | None | Registry mirrors to use. |
| `insecure-registries` | list | None | Insecure registries to allow. |
| `live-restore` | boolean | `false` | Enable live restore of docker when containers are still running. |
| `default-runtime` | string | `runc` | Default OCI runtime for containers. |
| `runtimes` | map | None | Register additional OCI runtimes. |
| `features` | map | None | Enable/disable specific features. |
| `builder` | map | None | BuildKit configuration. |
| `containerd` | string | None | Path to containerd socket. |
| `default-cgroupns-mode` | string | `private` | Default cgroup namespace mode. |
| `exec-opts` | list | None | Execution options. |
| `experimental` | boolean | `false` | Enable experimental features. |
| `fixed-cidr` | string | None | IPv4 subnet for fixed IPs. |
| `fixed-cidr-v6` | string | None | IPv6 subnet for fixed IPs. |
| `group` | string | `docker` | Group for the unix socket. |
| `hosts` | list | None | Daemon socket(s) to connect to. |
| `icc` | boolean | `true` | Enable inter-container communication. |
| `ip` | string | `0.0.0.0` | Default IP when binding container ports. |
| `ip-forward` | boolean | `true` | Enable net.ipv4.ip_forward. |
| `iptables` | boolean | `true` | Enable addition of iptables rules. |
| `ip-masq` | boolean | `true` | Enable IP masquerading. |
| `labels` | list | None | Daemon labels. |
| `max-concurrent-downloads` | integer | `3` | Max concurrent downloads. |
| `max-concurrent-uploads` | integer | `5` | Max concurrent uploads. |
| `max-download-attempts` | integer | `5` | Max download attempts. |
| `metrics-addr` | string | None | Address to serve metrics API. |
| `no-new-privileges` | boolean | `false` | Set no-new-privileges by default for new containers. |
| `oom-score-adjust` | integer | `-500` | Set the oom_score_adj for the daemon. |
| `pidfile` | string | `/var/run/docker.pid` | Path to use for daemon PID file. |
| `raw-logs` | boolean | `false` | Full timestamps without ANSI coloring. |
| `seccomp-profile` | string | None | Path to seccomp profile. |
| `selinux-enabled` | boolean | `false` | Enable selinux support. |
| `shutdown-timeout` | integer | `15` | Default timeout for stopping containers. |
| `tls` | boolean | `false` | Use TLS; implied by --tlsverify. |
| `tlscacert` | string | `~/.docker/ca.pem` | Trust certs signed only by this CA. |
| `tlscert` | string | `~/.docker/cert.pem` | Path to TLS certificate file. |
| `tlskey` | string | `~/.docker/key.pem` | Path to TLS key file. |
| `tlsverify` | boolean | `false` | Use TLS and verify the remote. |
| `userland-proxy` | boolean | `true` | Use userland proxy for loopback traffic. |
| `userns-remap` | string | None | User namespace remapping. |

## 4. `.dockerignore` Patterns

The `.dockerignore` file excludes files and directories from the build context.

### Syntax
- `#` for comments.
- `*` matches any sequence of non-separator characters.
- `?` matches any single non-separator character.
- `**` matches any number of directories.
- `!` negates a pattern.

### Common Patterns

**Node.js:**
```dockerignore
node_modules
npm-debug.log
Dockerfile
.dockerignore
.git
.gitignore
README.md
```

**Python:**
```dockerignore
__pycache__
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.env
Dockerfile
.dockerignore
.git
```

**Go:**
```dockerignore
bin/
obj/
*.exe
*.dll
*.so
*.dylib
Dockerfile
.dockerignore
.git
```

## 5. BuildKit Configuration (`buildkitd.toml`)

BuildKit can be configured via `buildkitd.toml`.

```toml
debug = true
# root is where all buildkit state is stored.
root = "/var/lib/buildkit"
# insecure-entitlements allows insecure entitlements, disabled by default.
insecure-entitlements = [ "network.host", "security.insecure" ]

[grpc]
  address = [ "tcp://0.0.0.0:1234" ]
  # debugAddress is address for attaching go pprof and expvar.
  debugAddress = "0.0.0.0:6060"
  uid = 0
  gid = 0
  [grpc.tls]
    cert = "/etc/buildkit/tls.crt"
    key = "/etc/buildkit/tls.key"
    ca = "/etc/buildkit/tlsca.crt"

[worker.oci]
  enabled = true
  # platforms is manually configure platforms, auto-detected by default.
  platforms = [ "linux/amd64", "linux/arm64" ]
  snapshotter = "auto" # overlayfs or native, default auto will try to use overlayfs
  rootless = false # see docs/rootless.md for more details on rootless mode.
  # Whether run subprocesses in main cgroup or create top-level cgroup.
  # Default is "cgroupfs" when not running rootless.
  cgroup-parent = "cgroupfs"
  # gc keeps/frees disk space.
  gc = true
  gckeepstorage = 9000
  [[worker.oci.gcpolicy]]
    keepBytes = 512000000
    keepDuration = 172800
    filters = [ "type==source.local", "type==exec.cachemount", "type==source.git.checkout"]
  [[worker.oci.gcpolicy]]
    all = true
    keepBytes = 1024000000

[worker.containerd]
  address = "/run/containerd/containerd.sock"
  enabled = true
  platforms = [ "linux/amd64", "linux/arm64" ]
  namespace = "buildkit"
  gc = true
  # gckeepstorage sets storage limit for default gc profile, in MB.
  gckeepstorage = 9000

[registry."docker.io"]
  mirrors = ["YOUR_REGISTRY_MIRROR"]
  http = true
  insecure = true
```

## 6. Docker Context Configuration

Docker contexts allow you to manage multiple Docker environments.

- Create a context: `docker context create my-context --docker "host=ssh://user@remote-host"`
- Use a context: `docker context use my-context`
- List contexts: `docker context ls`
- Inspect a context: `docker context inspect my-context`

## 7. Registry Configuration (`config.yml`)

Configuration for a private Docker registry.

```yaml
version: 0.1
log:
  fields:
    service: registry
storage:
  cache:
    blobdescriptor: inmemory
  filesystem:
    rootdirectory: /var/lib/registry
http:
  addr: :5000
  headers:
    X-Content-Type-Options: [nosniff]
health:
  storagedriver:
    enabled: true
    interval: 10s
    threshold: 3
```

## 8. Production `compose.yaml` Templates

### 8.1 Web App Stack

```yaml
services:
  webapp:
    image: YOUR_REGISTRY/webapp:v1.2.3
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    environment:
      - NODE_ENV=production
    secrets:
      - db_password
    networks:
      - frontend
      - backend
    deploy:
      replicas: 3
      update_config:
        parallelism: 1
        delay: 10s
      restart_policy:
        condition: on-failure
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"

networks:
  frontend:
  backend:
    internal: true

secrets:
  db_password:
    external: true
```

### 8.2 Database Stack

```yaml
services:
  db:
    image: postgres:15-alpine
    restart: always
    environment:
      POSTGRES_USER: admin
      POSTGRES_PASSWORD_FILE: /run/secrets/db_password
      POSTGRES_DB: myapp
    volumes:
      - db-data:/var/lib/postgresql/data
    secrets:
      - db_password
    networks:
      - backend
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 4G
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U admin -d myapp"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  db-data:

networks:
  backend:
    internal: true

secrets:
  db_password:
    external: true
```

### 8.3 Monitoring Stack (Prometheus/Grafana)

```yaml
services:
  prometheus:
    image: prom/prometheus:v2.45.0
    restart: unless-stopped
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml:ro
      - prometheus-data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--web.console.libraries=/etc/prometheus/console_libraries'
      - '--web.console.templates=/etc/prometheus/consoles'
      - '--web.enable-lifecycle'
    ports:
      - "9090:9090"
    networks:
      - monitoring

  grafana:
    image: grafana/grafana:10.0.3
    restart: unless-stopped
    volumes:
      - grafana-data:/var/lib/grafana
    environment:
      - GF_SECURITY_ADMIN_PASSWORD__FILE=/run/secrets/grafana_password
    secrets:
      - grafana_password
    ports:
      - "3000:3000"
    networks:
      - monitoring
    depends_on:
      - prometheus

volumes:
  prometheus-data:
  grafana-data:

networks:
  monitoring:

secrets:
  grafana_password:
    external: true
```

### 8.4 ELK Stack

```yaml
services:
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.9.0
    environment:
      - discovery.type=single-node
      - xpack.security.enabled=false
      - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
    volumes:
      - es-data:/usr/share/elasticsearch/data
    ports:
      - "9200:9200"
    networks:
      - elk

  logstash:
    image: docker.elastic.co/logstash/logstash:8.9.0
    volumes:
      - ./logstash.conf:/usr/share/logstash/pipeline/logstash.conf:ro
    ports:
      - "5044:5044"
    networks:
      - elk
    depends_on:
      - elasticsearch

  kibana:
    image: docker.elastic.co/kibana/kibana:8.9.0
    ports:
      - "5601:5601"
    networks:
      - elk
    depends_on:
      - elasticsearch

volumes:
  es-data:

networks:
  elk:
```

## 9. Troubleshooting and Optimization

### 9.1 Common Errors and Solutions

- **"port already in use"**: Use `lsof -i :PORT` to find the conflicting process, or change the port mapping in `compose.yaml`.
- **"no space left on device"**: Run `docker system prune -a --volumes` to clear unused data. Check the `overlay2` directory size.
- **"OOM killed"**: The container exceeded its memory limit. Increase the `mem_limit` in `compose.yaml` or optimize the application's memory usage.
- **"permission denied"**: Check the user/group permissions of the mounted volumes. Ensure the container user has access.
- **"network not found"**: Run `docker network create <network_name>` or ensure the network is defined in `compose.yaml`.
- **"image not found"**: Verify the registry URL, image tag, and `pull_policy`. Ensure you are logged in to the registry.
- **"container unhealthy"**: Check the `healthcheck` command and logs. Increase the `timeout` or `start_period` if the application takes longer to start.
- **"bind mount permission denied"**: On SELinux systems, append `:z` or `:Z` to the volume mount path (e.g., `./data:/data:z`).
- **"DNS resolution failed"**: Check the host's DNS settings or configure custom DNS servers in `daemon.json` or `compose.yaml`.
- **"cannot start service"**: Check `depends_on` conditions. Ensure required services are healthy before starting dependent services.
- **"exec format error"**: The image architecture does not match the host architecture (e.g., running an ARM image on an AMD64 host). Use `docker buildx` to build multi-platform images.
- **"context deadline exceeded"**: Increase the timeout for Docker commands or check network connectivity to the registry.

### 9.2 Cost and Time Optimization

- **Multi-stage builds**: Use multi-stage builds to create smaller final images. This reduces pull times and storage costs.
- **Layer caching**: Order Dockerfile instructions from least frequently changed to most frequently changed to maximize cache hits.
- **BuildKit cache mounts**: Use `--mount=type=cache` to cache package manager downloads (e.g., `apt`, `npm`, `pip`) between builds.
- **Parallel builds**: Use `docker compose build --parallel` to build multiple services concurrently.
- **Image pull policy**: Set `pull_policy: if-not-present` to avoid unnecessary image pulls.
- **Resource limits**: Set CPU and memory limits to prevent runaway containers from consuming all host resources.
- **Logging**: Configure log rotation (`max-size`, `max-file`) to prevent log files from filling up the disk.
- **Prune**: Regularly run `docker system prune` and `docker volume prune` to remove unused resources.
- **Compose profiles**: Use profiles to start only the services needed for a specific environment or task.
- **Compose watch**: Use `develop: watch` for fast iteration during development without rebuilding images.

### 9.3 Security Hardening

- **Non-root user**: Run containers as a non-root user (`USER 1000:1000`).
- **Read-only root filesystem**: Set `read_only: true` to prevent modifications to the container's root filesystem.
- **Drop capabilities**: Drop all Linux capabilities (`cap_drop: ["ALL"]`) and add only the necessary ones.
- **No new privileges**: Set `security_opt: ["no-new-privileges:true"]` to prevent processes from gaining additional privileges.
- **Seccomp profiles**: Use custom seccomp profiles to restrict system calls.
- **Resource limits**: Enforce CPU, memory, and PID limits to prevent denial-of-service attacks.
- **No privileged mode**: Avoid using `privileged: true` unless absolutely necessary.
- **Minimal base images**: Use minimal base images like `alpine`, `distroless`, or `scratch` to reduce the attack surface.
- **Secrets management**: Use Docker secrets instead of environment variables for sensitive data.
- **Network segmentation**: Use internal networks to isolate backend services from the public internet.

### 9.4 Upgrade Strategies

- **Blue-green deployment**: Run the new version alongside the old version and switch traffic when ready.
- **Rolling update**: Use `update_config` with `parallelism` and `delay` to update containers one by one.
- **Canary release**: Route a small percentage of traffic to the new version to test it before a full rollout.
- **Database migrations**: Run database migrations as an init container or a pre-start hook before starting the application.
- **Rollback**: Configure `rollback_config` to automatically roll back to the previous version if the update fails.
- **Zero-downtime**: Use `order: start-first` in `update_config` to start the new container before stopping the old one.
# Docker Super Specialist: Complete Configuration Reference

## 1. `compose.yaml` Complete Schema Reference

The `compose.yaml` file is the heart of Docker Compose. Below is the exhaustive reference for every top-level element and nested option.

### 1.1 Top-Level Elements

- `version`: (Deprecated) No longer required in Compose V2.
- `name`: Sets the project name. Overrides the directory name.
- `services`: Defines the containers to run.
- `networks`: Defines the networks to be created or used.
- `volumes`: Defines the persistent volumes.
- `configs`: Defines configuration files to be mounted.
- `secrets`: Defines sensitive data to be mounted securely.

### 1.2 `services` Attributes

Every service can have the following attributes:

| Attribute | Type | Default | Description | Example |
|---|---|---|---|---|
| `annotations` | map/list | None | Metadata for the container. | `annotations: { "com.example.foo": "bar" }` |
| `attach` | boolean | `true` | Whether to attach to the container's output. | `attach: false` |
| `build` | string/object | None | Configuration for building the image. | `build: ./dir` or `build: { context: ., dockerfile: Dockerfile.alt }` |
| `blkio_config` | object | None | Block IO configuration. | `blkio_config: { weight: 300 }` |
| `cpu_count` | integer | None | Number of usable CPUs. | `cpu_count: 2` |
| `cpu_percent` | integer | None | Usable percentage of available CPUs. | `cpu_percent: 50` |
| `cpu_shares` | integer | None | CPU shares (relative weight). | `cpu_shares: 73` |
| `cpu_period` | integer | None | CPU CFS (Completely Fair Scheduler) period. | `cpu_period: 100000` |
| `cpu_quota` | integer | None | CPU CFS quota. | `cpu_quota: 50000` |
| `cpu_rt_runtime` | integer | None | CPU real-time runtime. | `cpu_rt_runtime: 95000` |
| `cpu_rt_period` | integer | None | CPU real-time period. | `cpu_rt_period: 100000` |
| `cpus` | float | None | Number of CPUs. | `cpus: 1.5` |
| `cpuset` | string | None | CPUs in which to allow execution. | `cpuset: "0,1"` |
| `cap_add` | list | None | Add Linux capabilities. | `cap_add: ["SYS_ADMIN"]` |
| `cap_drop` | list | None | Drop Linux capabilities. | `cap_drop: ["ALL"]` |
| `cgroup` | string | None | Cgroup namespace mode. | `cgroup: "host"` |
| `cgroup_parent` | string | None | Optional parent cgroup. | `cgroup_parent: "m-executor-abcd"` |
| `command` | string/list | None | Override the default command. | `command: ["bundle", "exec", "thin", "-p", "3000"]` |
| `configs` | list | None | Grant access to configs. | `configs: ["my_config"]` |
| `container_name` | string | None | Custom container name. | `container_name: my-web-container` |
| `credential_spec` | object | None | Credential spec for managed service accounts (Windows). | `credential_spec: { file: "my-spec.json" }` |
| `depends_on` | list/object | None | Express dependency between services. | `depends_on: { db: { condition: service_healthy } }` |
| `deploy` | object | None | Configuration for deployment and resource limits. | `deploy: { replicas: 6 }` |
| `develop` | object | None | Configuration for development (Compose Watch). | `develop: { watch: [...] }` |
| `device_cgroup_rules` | list | None | Add rules to the cgroup allowed devices list. | `device_cgroup_rules: ["c 1:3 mr"]` |
| `devices` | list | None | Device mappings. | `devices: ["/dev/ttyUSB0:/dev/ttyUSB0"]` |
| `dns` | string/list | None | Custom DNS servers. | `dns: ["8.8.8.8", "9.9.9.9"]` |
| `dns_opt` | list | None | Custom DNS options. | `dns_opt: ["use-vc", "no-tld-query"]` |
| `dns_search` | string/list | None | Custom DNS search domains. | `dns_search: ["dc1.example.com"]` |
| `domainname` | string | None | Custom domain name. | `domainname: foo.com` |
| `entrypoint` | string/list | None | Override the default entrypoint. | `entrypoint: /code/entrypoint.sh` |
| `env_file` | string/list | None | Add environment variables from a file. | `env_file: .env` |
| `environment` | map/list | None | Add environment variables. | `environment: { RACK_ENV: development }` |
| `expose` | list | None | Expose ports without publishing them to the host. | `expose: ["3000"]` |
| `extends` | string/object | None | Extend another service. | `extends: { file: common.yml, service: webapp }` |
| `external_links` | list | None | Link to containers started outside this compose. | `external_links: ["redis_1", "project_db_1:mysql"]` |
| `extra_hosts` | list/map | None | Add hostname mappings. | `extra_hosts: ["somehost:162.242.195.82"]` |
| `group_add` | list | None | Add additional groups. | `group_add: ["mail"]` |
| `healthcheck` | object | None | Configure a check that's run to determine whether or not containers for this service are "healthy". | `healthcheck: { test: ["CMD", "curl", "-f", "http://localhost"] }` |
| `hostname` | string | None | Custom host name. | `hostname: foo` |
| `image` | string | None | Specify the image to start the container from. | `image: redis:alpine` |
| `init` | boolean | `false` | Run an init inside the container that forwards signals and reaps processes. | `init: true` |
| `ipc` | string | None | IPC namespace to use. | `ipc: host` |
| `isolation` | string | None | Specify a container's isolation technology. | `isolation: default` |
| `labels` | map/list | None | Add metadata to containers. | `labels: { com.example.description: "Accounting webapp" }` |
| `links` | list | None | Link to containers in another service. | `links: ["db", "db:database"]` |
| `logging` | object | None | Logging configuration for the service. | `logging: { driver: syslog, options: { syslog-address: "tcp://192.168.0.42:123" } }` |
| `mac_address` | string | None | MAC address. | `mac_address: 02:42:ac:11:65:43` |
| `mem_limit` | string | None | Memory limit. | `mem_limit: 1g` |
| `mem_reservation` | string | None | Memory soft limit. | `mem_reservation: 512m` |
| `mem_swappiness` | integer | None | Tune a container's memory swappiness behavior. | `mem_swappiness: 60` |
| `memswap_limit` | string | None | Swap limit equal to memory plus swap. | `memswap_limit: 2g` |
| `network_mode` | string | None | Network mode. | `network_mode: "host"` |
| `networks` | list/map | None | Networks to join. | `networks: ["frontend", "backend"]` |
| `oom_kill_disable` | boolean | `false` | Disable OOM Killer. | `oom_kill_disable: true` |
| `oom_score_adj` | integer | None | Tune the host's OOM preferences for containers. | `oom_score_adj: 500` |
| `pid` | string | None | PID namespace to use. | `pid: "host"` |
| `pids_limit` | integer | None | Tune a container's pids limit. | `pids_limit: 100` |
| `platform` | string | None | Target platform containers for this service will run on. | `platform: linux/amd64` |
| `ports` | list | None | Expose ports. | `ports: ["3000", "8000:8000", "9000:8080"]` |
| `privileged` | boolean | `false` | Give extended privileges to this container. | `privileged: true` |
| `profiles` | list | None | Define a list of named profiles for the service to be enabled under. | `profiles: ["frontend", "debug"]` |
| `pull_policy` | string | `always` | Define the decisions Compose makes when it starts to pull images. | `pull_policy: missing` |
| `read_only` | boolean | `false` | Mount the container's root filesystem as read only. | `read_only: true` |
| `restart` | string | `no` | Restart policy. | `restart: always` |
| `runtime` | string | None | Specify the runtime to use for the container. | `runtime: runc` |
| `scale` | integer | `1` | Specify the default number of containers to deploy for this service. | `scale: 3` |
| `secrets` | list | None | Grant access to secrets on a per-service basis. | `secrets: ["my_secret", "my_other_secret"]` |
| `security_opt` | list | None | Override the default labeling scheme for each container. | `security_opt: ["label:user:USER", "label:role:ROLE"]` |
| `shm_size` | string | None | Size of `/dev/shm`. | `shm_size: '2gb'` |
| `stdin_open` | boolean | `false` | Keep STDIN open even if not attached. | `stdin_open: true` |
| `stop_grace_period` | string | `10s` | Specify how long to wait when attempting to stop a container if it doesn't handle SIGTERM. | `stop_grace_period: 1m30s` |
| `stop_signal` | string | `SIGTERM` | Set an alternative signal to stop the container. | `stop_signal: SIGUSR1` |
| `storage_opt` | map | None | Storage driver options for this service. | `storage_opt: { size: '120G' }` |
| `sysctls` | map/list | None | Kernel parameters to set in the container. | `sysctls: { net.core.somaxconn: 1024 }` |
| `tmpfs` | string/list | None | Mount a temporary file system inside the container. | `tmpfs: /run` |
| `tty` | boolean | `false` | Allocate a pseudo-TTY. | `tty: true` |
| `ulimits` | map | None | Override the default ulimits for a container. | `ulimits: { nproc: 65535, nofile: { soft: 20000, hard: 40000 } }` |
| `user` | string | None | Override the user used to run the container process. | `user: "1000:1000"` |
| `userns_mode` | string | None | Disable the user namespace for this service, if Docker daemon is configured with user namespaces. | `userns_mode: "host"` |
| `uts` | string | None | UTS namespace to use. | `uts: "host"` |
| `volumes` | list | None | Mount host paths or named volumes, specified as sub-options to a service. | `volumes: ["/var/lib/mysql", "./cache:/tmp/cache", "datavolume:/var/lib/mysql"]` |
| `volumes_from` | list | None | Mount all of the volumes from another service or container. | `volumes_from: ["service_name", "container_name"]` |
| `working_dir` | string | None | Override the container's working directory. | `working_dir: /code` |

### 1.3 `networks` Attributes

| Attribute | Type | Default | Description | Example |
|---|---|---|---|---|
| `driver` | string | `bridge` | Specify which driver should be used for this network. | `driver: overlay` |
| `driver_opts` | map | None | Specify a list of options as key-value pairs to pass to the driver. | `driver_opts: { com.docker.network.bridge.name: br_1 }` |
| `attachable` | boolean | `false` | Only used when the driver is set to `overlay`. If set to `true`, then standalone containers can attach to this network. | `attachable: true` |
| `enable_ipv6` | boolean | `false` | Enable IPv6 networking. | `enable_ipv6: true` |
| `internal` | boolean | `false` | By default, Docker also connects a bridge network to it to provide external connectivity. If you want to create an externally isolated overlay network, you can set this option to `true`. | `internal: true` |
| `labels` | map/list | None | Add metadata to containers. | `labels: { com.example.description: "Financial transaction network" }` |
| `external` | boolean | `false` | If set to `true`, specifies that this network has been created outside of Compose. | `external: true` |
| `name` | string | None | Set a custom name for this network. | `name: my-app-net` |
| `ipam` | object | None | Specify custom IPAM config. | `ipam: { driver: default, config: [{ subnet: "172.28.0.0/16" }] }` |

### 1.4 `volumes` Attributes

| Attribute | Type | Default | Description | Example |
|---|---|---|---|---|
| `driver` | string | `local` | Specify which volume driver should be used for this volume. | `driver: foobar` |
| `driver_opts` | map | None | Specify a list of options as key-value pairs to pass to the driver for this volume. | `driver_opts: { type: "nfs", o: "addr=10.40.0.199,nolock,soft,rw", device: ":/docker/example" }` |
| `external` | boolean | `false` | If set to `true`, specifies that this volume has been created outside of Compose. | `external: true` |
| `labels` | map/list | None | Add metadata to containers. | `labels: { com.example.description: "Database volume" }` |
| `name` | string | None | Set a custom name for this volume. | `name: my-app-data` |

### 1.5 `configs` Attributes

| Attribute | Type | Default | Description | Example |
|---|---|---|---|---|
| `file` | string | None | The config is created with the contents of the file at the specified path. | `file: ./my_config.txt` |
| `external` | boolean | `false` | If set to `true`, specifies that this config has already been created. | `external: true` |
| `name` | string | None | The name of the config object in Docker. | `name: my_config` |
| `content` | string | None | The content of the config. | `content: | 
  server {
    listen 80;
  }` |

### 1.6 `secrets` Attributes

| Attribute | Type | Default | Description | Example |
|---|---|---|---|---|
| `file` | string | None | The secret is created with the contents of the file at the specified path. | `file: ./my_secret.txt` |
| `environment` | string | None | The secret is created with the value of an environment variable. | `environment: "MY_SECRET"` |
| `external` | boolean | `false` | If set to `true`, specifies that this secret has already been created. | `external: true` |
| `name` | string | None | The name of the secret object in Docker. | `name: my_secret` |

## 2. Dockerfile Instruction Reference

A complete reference for every Dockerfile instruction.

### `FROM`
Initializes a new build stage and sets the Base Image for subsequent instructions.
- Syntax: `FROM [--platform=<platform>] <image> [AS <name>]` or `FROM [--platform=<platform>] <image>[:<tag>] [AS <name>]` or `FROM [--platform=<platform>] <image>[@<digest>] [AS <name>]`
- Example: `FROM --platform=linux/amd64 ubuntu:22.04 AS builder`

### `RUN`
Executes any commands in a new layer on top of the current image and commits the results.
- Syntax: `RUN <command>` (shell form) or `RUN ["executable", "param1", "param2"]` (exec form)
- Flags: `--mount=type=cache|bind|secret|ssh`, `--network=default|none|host`
- Example: `RUN --mount=type=cache,target=/var/cache/apt apt-get update && apt-get install -y curl`

### `CMD`
Provides defaults for an executing container. There can only be one `CMD` instruction in a Dockerfile.
- Syntax: `CMD ["executable","param1","param2"]` (exec form, preferred) or `CMD ["param1","param2"]` (as default parameters to ENTRYPOINT) or `CMD command param1 param2` (shell form)
- Example: `CMD ["node", "server.js"]`

### `LABEL`
Adds metadata to an image.
- Syntax: `LABEL <key>=<value> <key>=<value> <key>=<value> ...`
- Example: `LABEL org.opencontainers.image.authors="team@example.com"`

### `EXPOSE`
Informs Docker that the container listens on the specified network ports at runtime.
- Syntax: `EXPOSE <port> [<port>/<protocol>...]`
- Example: `EXPOSE 80/tcp 80/udp`

### `ENV`
Sets the environment variable `<key>` to the value `<value>`.
- Syntax: `ENV <key>=<value> ...`
- Example: `ENV NODE_ENV=production PORT=3000`

### `ADD`
Copies new files, directories or remote file URLs from `<src>` and adds them to the filesystem of the image at the path `<dest>`.
- Syntax: `ADD [--chown=<user>:<group>] [--chmod=<perms>] [--checksum=<checksum>] <src>... <dest>`
- Example: `ADD https://example.com/big.tar.xz /usr/src/things/`

### `COPY`
Copies new files or directories from `<src>` and adds them to the filesystem of the container at the path `<dest>`.
- Syntax: `COPY [--chown=<user>:<group>] [--chmod=<perms>] <src>... <dest>`
- Example: `COPY --chown=node:node package*.json ./`

### `ENTRYPOINT`
Allows you to configure a container that will run as an executable.
- Syntax: `ENTRYPOINT ["executable", "param1", "param2"]` (exec form, preferred) or `ENTRYPOINT command param1 param2` (shell form)
- Example: `ENTRYPOINT ["docker-entrypoint.sh"]`

### `VOLUME`
Creates a mount point with the specified name and marks it as holding externally mounted volumes from native host or other containers.
- Syntax: `VOLUME ["/data"]`
- Example: `VOLUME /var/lib/mysql`

### `USER`
Sets the user name (or UID) and optionally the user group (or GID) to use when running the image and for any `RUN`, `CMD` and `ENTRYPOINT` instructions that follow it in the Dockerfile.
- Syntax: `USER <user>[:<group>]` or `USER <UID>[:<GID>]`
- Example: `USER 1000:1000`

### `WORKDIR`
Sets the working directory for any `RUN`, `CMD`, `ENTRYPOINT`, `COPY` and `ADD` instructions that follow it in the Dockerfile.
- Syntax: `WORKDIR /path/to/workdir`
- Example: `WORKDIR /app`

### `ARG`
Defines a variable that users can pass at build-time to the builder with the `docker build` command using the `--build-arg <varname>=<value>` flag.
- Syntax: `ARG <name>[=<default value>]`
- Example: `ARG VERSION=latest`

### `ONBUILD`
Adds to the image a trigger instruction to be executed at a later time, when the image is used as the base for another build.
- Syntax: `ONBUILD <INSTRUCTION>`
- Example: `ONBUILD COPY . /app/src`

### `STOPSIGNAL`
Sets the system call signal that will be sent to the container to exit.
- Syntax: `STOPSIGNAL signal`
- Example: `STOPSIGNAL SIGKILL`

### `HEALTHCHECK`
Tells Docker how to test a container to check that it is still working.
- Syntax: `HEALTHCHECK [OPTIONS] CMD command` or `HEALTHCHECK NONE`
- Options: `--interval=DURATION` (default: 30s), `--timeout=DURATION` (default: 30s), `--start-period=DURATION` (default: 0s), `--retries=N` (default: 3)
- Example: `HEALTHCHECK --interval=5m --timeout=3s CMD curl -f http://localhost/ || exit 1`

### `SHELL`
Allows the default shell used for the shell form of commands to be overridden.
- Syntax: `SHELL ["executable", "parameters"]`
- Example: `SHELL ["powershell", "-command"]`

## 3. `daemon.json` Complete Reference

The `daemon.json` file configures the Docker daemon.

| Field | Type | Default | Description |
|---|---|---|---|
| `storage-driver` | string | `overlay2` | The storage driver to use. |
| `log-driver` | string | `json-file` | The default logging driver. |
| `log-opts` | map | None | Options for the logging driver. |
| `default-address-pools` | list | None | Default address pools for node networks. |
| `dns` | list | None | DNS servers to use. |
| `registry-mirrors` | list | None | Registry mirrors to use. |
| `insecure-registries` | list | None | Insecure registries to allow. |
| `live-restore` | boolean | `false` | Enable live restore of docker when containers are still running. |
| `default-runtime` | string | `runc` | Default OCI runtime for containers. |
| `runtimes` | map | None | Register additional OCI runtimes. |
| `features` | map | None | Enable/disable specific features. |
| `builder` | map | None | BuildKit configuration. |
| `containerd` | string | None | Path to containerd socket. |
| `default-cgroupns-mode` | string | `private` | Default cgroup namespace mode. |
| `exec-opts` | list | None | Execution options. |
| `experimental` | boolean | `false` | Enable experimental features. |
| `fixed-cidr` | string | None | IPv4 subnet for fixed IPs. |
| `fixed-cidr-v6` | string | None | IPv6 subnet for fixed IPs. |
| `group` | string | `docker` | Group for the unix socket. |
| `hosts` | list | None | Daemon socket(s) to connect to. |
| `icc` | boolean | `true` | Enable inter-container communication. |
| `ip` | string | `0.0.0.0` | Default IP when binding container ports. |
| `ip-forward` | boolean | `true` | Enable net.ipv4.ip_forward. |
| `iptables` | boolean | `true` | Enable addition of iptables rules. |
| `ip-masq` | boolean | `true` | Enable IP masquerading. |
| `labels` | list | None | Daemon labels. |
| `max-concurrent-downloads` | integer | `3` | Max concurrent downloads. |
| `max-concurrent-uploads` | integer | `5` | Max concurrent uploads. |
| `max-download-attempts` | integer | `5` | Max download attempts. |
| `metrics-addr` | string | None | Address to serve metrics API. |
| `no-new-privileges` | boolean | `false` | Set no-new-privileges by default for new containers. |
| `oom-score-adjust` | integer | `-500` | Set the oom_score_adj for the daemon. |
| `pidfile` | string | `/var/run/docker.pid` | Path to use for daemon PID file. |
| `raw-logs` | boolean | `false` | Full timestamps without ANSI coloring. |
| `seccomp-profile` | string | None | Path to seccomp profile. |
| `selinux-enabled` | boolean | `false` | Enable selinux support. |
| `shutdown-timeout` | integer | `15` | Default timeout for stopping containers. |
| `tls` | boolean | `false` | Use TLS; implied by --tlsverify. |
| `tlscacert` | string | `~/.docker/ca.pem` | Trust certs signed only by this CA. |
| `tlscert` | string | `~/.docker/cert.pem` | Path to TLS certificate file. |
| `tlskey` | string | `~/.docker/key.pem` | Path to TLS key file. |
| `tlsverify` | boolean | `false` | Use TLS and verify the remote. |
| `userland-proxy` | boolean | `true` | Use userland proxy for loopback traffic. |
| `userns-remap` | string | None | User namespace remapping. |

## 4. `.dockerignore` Patterns

The `.dockerignore` file excludes files and directories from the build context.

### Syntax
- `#` for comments.
- `*` matches any sequence of non-separator characters.
- `?` matches any single non-separator character.
- `**` matches any number of directories.
- `!` negates a pattern.

### Common Patterns

**Node.js:**
```dockerignore
node_modules
npm-debug.log
Dockerfile
.dockerignore
.git
.gitignore
README.md
```

**Python:**
```dockerignore
__pycache__
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.env
Dockerfile
.dockerignore
.git
```

**Go:**
```dockerignore
bin/
obj/
*.exe
*.dll
*.so
*.dylib
Dockerfile
.dockerignore
.git
```

## 5. BuildKit Configuration (`buildkitd.toml`)

BuildKit can be configured via `buildkitd.toml`.

```toml
debug = true
# root is where all buildkit state is stored.
root = "/var/lib/buildkit"
# insecure-entitlements allows insecure entitlements, disabled by default.
insecure-entitlements = [ "network.host", "security.insecure" ]

[grpc]
  address = [ "tcp://0.0.0.0:1234" ]
  # debugAddress is address for attaching go pprof and expvar.
  debugAddress = "0.0.0.0:6060"
  uid = 0
  gid = 0
  [grpc.tls]
    cert = "/etc/buildkit/tls.crt"
    key = "/etc/buildkit/tls.key"
    ca = "/etc/buildkit/tlsca.crt"

[worker.oci]
  enabled = true
  # platforms is manually configure platforms, auto-detected by default.
  platforms = [ "linux/amd64", "linux/arm64" ]
  snapshotter = "auto" # overlayfs or native, default auto will try to use overlayfs
  rootless = false # see docs/rootless.md for more details on rootless mode.
  # Whether run subprocesses in main cgroup or create top-level cgroup.
  # Default is "cgroupfs" when not running rootless.
  cgroup-parent = "cgroupfs"
  # gc keeps/frees disk space.
  gc = true
  gckeepstorage = 9000
  [[worker.oci.gcpolicy]]
    keepBytes = 512000000
    keepDuration = 172800
    filters = [ "type==source.local", "type==exec.cachemount", "type==source.git.checkout"]
  [[worker.oci.gcpolicy]]
    all = true
    keepBytes = 1024000000

[worker.containerd]
  address = "/run/containerd/containerd.sock"
  enabled = true
  platforms = [ "linux/amd64", "linux/arm64" ]
  namespace = "buildkit"
  gc = true
  # gckeepstorage sets storage limit for default gc profile, in MB.
  gckeepstorage = 9000

[registry."docker.io"]
  mirrors = ["YOUR_REGISTRY_MIRROR"]
  http = true
  insecure = true
```

## 6. Docker Context Configuration

Docker contexts allow you to manage multiple Docker environments.

- Create a context: `docker context create my-context --docker "host=ssh://user@remote-host"`
- Use a context: `docker context use my-context`
- List contexts: `docker context ls`
- Inspect a context: `docker context inspect my-context`

## 7. Registry Configuration (`config.yml`)

Configuration for a private Docker registry.

```yaml
version: 0.1
log:
  fields:
    service: registry
storage:
  cache:
    blobdescriptor: inmemory
  filesystem:
    rootdirectory: /var/lib/registry
http:
  addr: :5000
  headers:
    X-Content-Type-Options: [nosniff]
health:
  storagedriver:
    enabled: true
    interval: 10s
    threshold: 3
```

## 8. Production `compose.yaml` Templates

### 8.1 Web App Stack

```yaml
services:
  webapp:
    image: YOUR_REGISTRY/webapp:v1.2.3
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    environment:
      - NODE_ENV=production
    secrets:
      - db_password
    networks:
      - frontend
      - backend
    deploy:
      replicas: 3
      update_config:
        parallelism: 1
        delay: 10s
      restart_policy:
        condition: on-failure
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"

networks:
  frontend:
  backend:
    internal: true

secrets:
  db_password:
    external: true
```

### 8.2 Database Stack

```yaml
services:
  db:
    image: postgres:15-alpine
    restart: always
    environment:
      POSTGRES_USER: admin
      POSTGRES_PASSWORD_FILE: /run/secrets/db_password
      POSTGRES_DB: myapp
    volumes:
      - db-data:/var/lib/postgresql/data
    secrets:
      - db_password
    networks:
      - backend
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 4G
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U admin -d myapp"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  db-data:

networks:
  backend:
    internal: true

secrets:
  db_password:
    external: true
```

### 8.3 Monitoring Stack (Prometheus/Grafana)

```yaml
services:
  prometheus:
    image: prom/prometheus:v2.45.0
    restart: unless-stopped
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml:ro
      - prometheus-data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--web.console.libraries=/etc/prometheus/console_libraries'
      - '--web.console.templates=/etc/prometheus/consoles'
      - '--web.enable-lifecycle'
    ports:
      - "9090:9090"
    networks:
      - monitoring

  grafana:
    image: grafana/grafana:10.0.3
    restart: unless-stopped
    volumes:
      - grafana-data:/var/lib/grafana
    environment:
      - GF_SECURITY_ADMIN_PASSWORD__FILE=/run/secrets/grafana_password
    secrets:
      - grafana_password
    ports:
      - "3000:3000"
    networks:
      - monitoring
    depends_on:
      - prometheus

volumes:
  prometheus-data:
  grafana-data:

networks:
  monitoring:

secrets:
  grafana_password:
    external: true
```

### 8.4 ELK Stack

```yaml
services:
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.9.0
    environment:
      - discovery.type=single-node
      - xpack.security.enabled=false
      - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
    volumes:
      - es-data:/usr/share/elasticsearch/data
    ports:
      - "9200:9200"
    networks:
      - elk

  logstash:
    image: docker.elastic.co/logstash/logstash:8.9.0
    volumes:
      - ./logstash.conf:/usr/share/logstash/pipeline/logstash.conf:ro
    ports:
      - "5044:5044"
    networks:
      - elk
    depends_on:
      - elasticsearch

  kibana:
    image: docker.elastic.co/kibana/kibana:8.9.0
    ports:
      - "5601:5601"
    networks:
      - elk
    depends_on:
      - elasticsearch

volumes:
  es-data:

networks:
  elk:
```

## 9. Troubleshooting and Optimization

### 9.1 Common Errors and Solutions

- **"port already in use"**: Use `lsof -i :PORT` to find the conflicting process, or change the port mapping in `compose.yaml`.
- **"no space left on device"**: Run `docker system prune -a --volumes` to clear unused data. Check the `overlay2` directory size.
- **"OOM killed"**: The container exceeded its memory limit. Increase the `mem_limit` in `compose.yaml` or optimize the application's memory usage.
- **"permission denied"**: Check the user/group permissions of the mounted volumes. Ensure the container user has access.
- **"network not found"**: Run `docker network create <network_name>` or ensure the network is defined in `compose.yaml`.
- **"image not found"**: Verify the registry URL, image tag, and `pull_policy`. Ensure you are logged in to the registry.
- **"container unhealthy"**: Check the `healthcheck` command and logs. Increase the `timeout` or `start_period` if the application takes longer to start.
- **"bind mount permission denied"**: On SELinux systems, append `:z` or `:Z` to the volume mount path (e.g., `./data:/data:z`).
- **"DNS resolution failed"**: Check the host's DNS settings or configure custom DNS servers in `daemon.json` or `compose.yaml`.
- **"cannot start service"**: Check `depends_on` conditions. Ensure required services are healthy before starting dependent services.
- **"exec format error"**: The image architecture does not match the host architecture (e.g., running an ARM image on an AMD64 host). Use `docker buildx` to build multi-platform images.
- **"context deadline exceeded"**: Increase the timeout for Docker commands or check network connectivity to the registry.

### 9.2 Cost and Time Optimization

- **Multi-stage builds**: Use multi-stage builds to create smaller final images. This reduces pull times and storage costs.
- **Layer caching**: Order Dockerfile instructions from least frequently changed to most frequently changed to maximize cache hits.
- **BuildKit cache mounts**: Use `--mount=type=cache` to cache package manager downloads (e.g., `apt`, `npm`, `pip`) between builds.
- **Parallel builds**: Use `docker compose build --parallel` to build multiple services concurrently.
- **Image pull policy**: Set `pull_policy: if-not-present` to avoid unnecessary image pulls.
- **Resource limits**: Set CPU and memory limits to prevent runaway containers from consuming all host resources.
- **Logging**: Configure log rotation (`max-size`, `max-file`) to prevent log files from filling up the disk.
- **Prune**: Regularly run `docker system prune` and `docker volume prune` to remove unused resources.
- **Compose profiles**: Use profiles to start only the services needed for a specific environment or task.
- **Compose watch**: Use `develop: watch` for fast iteration during development without rebuilding images.

### 9.3 Security Hardening

- **Non-root user**: Run containers as a non-root user (`USER 1000:1000`).
- **Read-only root filesystem**: Set `read_only: true` to prevent modifications to the container's root filesystem.
- **Drop capabilities**: Drop all Linux capabilities (`cap_drop: ["ALL"]`) and add only the necessary ones.
- **No new privileges**: Set `security_opt: ["no-new-privileges:true"]` to prevent processes from gaining additional privileges.
- **Seccomp profiles**: Use custom seccomp profiles to restrict system calls.
- **Resource limits**: Enforce CPU, memory, and PID limits to prevent denial-of-service attacks.
- **No privileged mode**: Avoid using `privileged: true` unless absolutely necessary.
- **Minimal base images**: Use minimal base images like `alpine`, `distroless`, or `scratch` to reduce the attack surface.
- **Secrets management**: Use Docker secrets instead of environment variables for sensitive data.
- **Network segmentation**: Use internal networks to isolate backend services from the public internet.

### 9.4 Upgrade Strategies

- **Blue-green deployment**: Run the new version alongside the old version and switch traffic when ready.
- **Rolling update**: Use `update_config` with `parallelism` and `delay` to update containers one by one.
- **Canary release**: Route a small percentage of traffic to the new version to test it before a full rollout.
- **Database migrations**: Run database migrations as an init container or a pre-start hook before starting the application.
- **Rollback**: Configure `rollback_config` to automatically roll back to the previous version if the update fails.
- **Zero-downtime**: Use `order: start-first` in `update_config` to start the new container before stopping the old one.
# Docker Super Specialist: Complete Configuration Reference

## 1. `compose.yaml` Complete Schema Reference

The `compose.yaml` file is the heart of Docker Compose. Below is the exhaustive reference for every top-level element and nested option.

### 1.1 Top-Level Elements

- `version`: (Deprecated) No longer required in Compose V2.
- `name`: Sets the project name. Overrides the directory name.
- `services`: Defines the containers to run.
- `networks`: Defines the networks to be created or used.
- `volumes`: Defines the persistent volumes.
- `configs`: Defines configuration files to be mounted.
- `secrets`: Defines sensitive data to be mounted securely.

### 1.2 `services` Attributes

Every service can have the following attributes:

| Attribute | Type | Default | Description | Example |
|---|---|---|---|---|
| `annotations` | map/list | None | Metadata for the container. | `annotations: { "com.example.foo": "bar" }` |
| `attach` | boolean | `true` | Whether to attach to the container's output. | `attach: false` |
| `build` | string/object | None | Configuration for building the image. | `build: ./dir` or `build: { context: ., dockerfile: Dockerfile.alt }` |
| `blkio_config` | object | None | Block IO configuration. | `blkio_config: { weight: 300 }` |
| `cpu_count` | integer | None | Number of usable CPUs. | `cpu_count: 2` |
| `cpu_percent` | integer | None | Usable percentage of available CPUs. | `cpu_percent: 50` |
| `cpu_shares` | integer | None | CPU shares (relative weight). | `cpu_shares: 73` |
| `cpu_period` | integer | None | CPU CFS (Completely Fair Scheduler) period. | `cpu_period: 100000` |
| `cpu_quota` | integer | None | CPU CFS quota. | `cpu_quota: 50000` |
| `cpu_rt_runtime` | integer | None | CPU real-time runtime. | `cpu_rt_runtime: 95000` |
| `cpu_rt_period` | integer | None | CPU real-time period. | `cpu_rt_period: 100000` |
| `cpus` | float | None | Number of CPUs. | `cpus: 1.5` |
| `cpuset` | string | None | CPUs in which to allow execution. | `cpuset: "0,1"` |
| `cap_add` | list | None | Add Linux capabilities. | `cap_add: ["SYS_ADMIN"]` |
| `cap_drop` | list | None | Drop Linux capabilities. | `cap_drop: ["ALL"]` |
| `cgroup` | string | None | Cgroup namespace mode. | `cgroup: "host"` |
| `cgroup_parent` | string | None | Optional parent cgroup. | `cgroup_parent: "m-executor-abcd"` |
| `command` | string/list | None | Override the default command. | `command: ["bundle", "exec", "thin", "-p", "3000"]` |
| `configs` | list | None | Grant access to configs. | `configs: ["my_config"]` |
| `container_name` | string | None | Custom container name. | `container_name: my-web-container` |
| `credential_spec` | object | None | Credential spec for managed service accounts (Windows). | `credential_spec: { file: "my-spec.json" }` |
| `depends_on` | list/object | None | Express dependency between services. | `depends_on: { db: { condition: service_healthy } }` |
| `deploy` | object | None | Configuration for deployment and resource limits. | `deploy: { replicas: 6 }` |
| `develop` | object | None | Configuration for development (Compose Watch). | `develop: { watch: [...] }` |
| `device_cgroup_rules` | list | None | Add rules to the cgroup allowed devices list. | `device_cgroup_rules: ["c 1:3 mr"]` |
| `devices` | list | None | Device mappings. | `devices: ["/dev/ttyUSB0:/dev/ttyUSB0"]` |
| `dns` | string/list | None | Custom DNS servers. | `dns: ["8.8.8.8", "9.9.9.9"]` |
| `dns_opt` | list | None | Custom DNS options. | `dns_opt: ["use-vc", "no-tld-query"]` |
| `dns_search` | string/list | None | Custom DNS search domains. | `dns_search: ["dc1.example.com"]` |
| `domainname` | string | None | Custom domain name. | `domainname: foo.com` |
| `entrypoint` | string/list | None | Override the default entrypoint. | `entrypoint: /code/entrypoint.sh` |
| `env_file` | string/list | None | Add environment variables from a file. | `env_file: .env` |
| `environment` | map/list | None | Add environment variables. | `environment: { RACK_ENV: development }` |
| `expose` | list | None | Expose ports without publishing them to the host. | `expose: ["3000"]` |
| `extends` | string/object | None | Extend another service. | `extends: { file: common.yml, service: webapp }` |
| `external_links` | list | None | Link to containers started outside this compose. | `external_links: ["redis_1", "project_db_1:mysql"]` |
| `extra_hosts` | list/map | None | Add hostname mappings. | `extra_hosts: ["somehost:162.242.195.82"]` |
| `group_add` | list | None | Add additional groups. | `group_add: ["mail"]` |
| `healthcheck` | object | None | Configure a check that's run to determine whether or not containers for this service are "healthy". | `healthcheck: { test: ["CMD", "curl", "-f", "http://localhost"] }` |
| `hostname` | string | None | Custom host name. | `hostname: foo` |
| `image` | string | None | Specify the image to start the container from. | `image: redis:alpine` |
| `init` | boolean | `false` | Run an init inside the container that forwards signals and reaps processes. | `init: true` |
| `ipc` | string | None | IPC namespace to use. | `ipc: host` |
| `isolation` | string | None | Specify a container's isolation technology. | `isolation: default` |
| `labels` | map/list | None | Add metadata to containers. | `labels: { com.example.description: "Accounting webapp" }` |
| `links` | list | None | Link to containers in another service. | `links: ["db", "db:database"]` |
| `logging` | object | None | Logging configuration for the service. | `logging: { driver: syslog, options: { syslog-address: "tcp://192.168.0.42:123" } }` |
| `mac_address` | string | None | MAC address. | `mac_address: 02:42:ac:11:65:43` |
| `mem_limit` | string | None | Memory limit. | `mem_limit: 1g` |
| `mem_reservation` | string | None | Memory soft limit. | `mem_reservation: 512m` |
| `mem_swappiness` | integer | None | Tune a container's memory swappiness behavior. | `mem_swappiness: 60` |
| `memswap_limit` | string | None | Swap limit equal to memory plus swap. | `memswap_limit: 2g` |
| `network_mode` | string | None | Network mode. | `network_mode: "host"` |
| `networks` | list/map | None | Networks to join. | `networks: ["frontend", "backend"]` |
| `oom_kill_disable` | boolean | `false` | Disable OOM Killer. | `oom_kill_disable: true` |
| `oom_score_adj` | integer | None | Tune the host's OOM preferences for containers. | `oom_score_adj: 500` |
| `pid` | string | None | PID namespace to use. | `pid: "host"` |
| `pids_limit` | integer | None | Tune a container's pids limit. | `pids_limit: 100` |
| `platform` | string | None | Target platform containers for this service will run on. | `platform: linux/amd64` |
| `ports` | list | None | Expose ports. | `ports: ["3000", "8000:8000", "9000:8080"]` |
| `privileged` | boolean | `false` | Give extended privileges to this container. | `privileged: true` |
| `profiles` | list | None | Define a list of named profiles for the service to be enabled under. | `profiles: ["frontend", "debug"]` |
| `pull_policy` | string | `always` | Define the decisions Compose makes when it starts to pull images. | `pull_policy: missing` |
| `read_only` | boolean | `false` | Mount the container's root filesystem as read only. | `read_only: true` |
| `restart` | string | `no` | Restart policy. | `restart: always` |
| `runtime` | string | None | Specify the runtime to use for the container. | `runtime: runc` |
| `scale` | integer | `1` | Specify the default number of containers to deploy for this service. | `scale: 3` |
| `secrets` | list | None | Grant access to secrets on a per-service basis. | `secrets: ["my_secret", "my_other_secret"]` |
| `security_opt` | list | None | Override the default labeling scheme for each container. | `security_opt: ["label:user:USER", "label:role:ROLE"]` |
| `shm_size` | string | None | Size of `/dev/shm`. | `shm_size: '2gb'` |
| `stdin_open` | boolean | `false` | Keep STDIN open even if not attached. | `stdin_open: true` |
| `stop_grace_period` | string | `10s` | Specify how long to wait when attempting to stop a container if it doesn't handle SIGTERM. | `stop_grace_period: 1m30s` |
| `stop_signal` | string | `SIGTERM` | Set an alternative signal to stop the container. | `stop_signal: SIGUSR1` |
| `storage_opt` | map | None | Storage driver options for this service. | `storage_opt: { size: '120G' }` |
| `sysctls` | map/list | None | Kernel parameters to set in the container. | `sysctls: { net.core.somaxconn: 1024 }` |
| `tmpfs` | string/list | None | Mount a temporary file system inside the container. | `tmpfs: /run` |
| `tty` | boolean | `false` | Allocate a pseudo-TTY. | `tty: true` |
| `ulimits` | map | None | Override the default ulimits for a container. | `ulimits: { nproc: 65535, nofile: { soft: 20000, hard: 40000 } }` |
| `user` | string | None | Override the user used to run the container process. | `user: "1000:1000"` |
| `userns_mode` | string | None | Disable the user namespace for this service, if Docker daemon is configured with user namespaces. | `userns_mode: "host"` |
| `uts` | string | None | UTS namespace to use. | `uts: "host"` |
| `volumes` | list | None | Mount host paths or named volumes, specified as sub-options to a service. | `volumes: ["/var/lib/mysql", "./cache:/tmp/cache", "datavolume:/var/lib/mysql"]` |
| `volumes_from` | list | None | Mount all of the volumes from another service or container. | `volumes_from: ["service_name", "container_name"]` |
| `working_dir` | string | None | Override the container's working directory. | `working_dir: /code` |

### 1.3 `networks` Attributes

| Attribute | Type | Default | Description | Example |
|---|---|---|---|---|
| `driver` | string | `bridge` | Specify which driver should be used for this network. | `driver: overlay` |
| `driver_opts` | map | None | Specify a list of options as key-value pairs to pass to the driver. | `driver_opts: { com.docker.network.bridge.name: br_1 }` |
| `attachable` | boolean | `false` | Only used when the driver is set to `overlay`. If set to `true`, then standalone containers can attach to this network. | `attachable: true` |
| `enable_ipv6` | boolean | `false` | Enable IPv6 networking. | `enable_ipv6: true` |
| `internal` | boolean | `false` | By default, Docker also connects a bridge network to it to provide external connectivity. If you want to create an externally isolated overlay network, you can set this option to `true`. | `internal: true` |
| `labels` | map/list | None | Add metadata to containers. | `labels: { com.example.description: "Financial transaction network" }` |
| `external` | boolean | `false` | If set to `true`, specifies that this network has been created outside of Compose. | `external: true` |
| `name` | string | None | Set a custom name for this network. | `name: my-app-net` |
| `ipam` | object | None | Specify custom IPAM config. | `ipam: { driver: default, config: [{ subnet: "172.28.0.0/16" }] }` |

### 1.4 `volumes` Attributes

| Attribute | Type | Default | Description | Example |
|---|---|---|---|---|
| `driver` | string | `local` | Specify which volume driver should be used for this volume. | `driver: foobar` |
| `driver_opts` | map | None | Specify a list of options as key-value pairs to pass to the driver for this volume. | `driver_opts: { type: "nfs", o: "addr=10.40.0.199,nolock,soft,rw", device: ":/docker/example" }` |
| `external` | boolean | `false` | If set to `true`, specifies that this volume has been created outside of Compose. | `external: true` |
| `labels` | map/list | None | Add metadata to containers. | `labels: { com.example.description: "Database volume" }` |
| `name` | string | None | Set a custom name for this volume. | `name: my-app-data` |

### 1.5 `configs` Attributes

| Attribute | Type | Default | Description | Example |
|---|---|---|---|---|
| `file` | string | None | The config is created with the contents of the file at the specified path. | `file: ./my_config.txt` |
| `external` | boolean | `false` | If set to `true`, specifies that this config has already been created. | `external: true` |
| `name` | string | None | The name of the config object in Docker. | `name: my_config` |
| `content` | string | None | The content of the config. | `content: | 
  server {
    listen 80;
  }` |

### 1.6 `secrets` Attributes

| Attribute | Type | Default | Description | Example |
|---|---|---|---|---|
| `file` | string | None | The secret is created with the contents of the file at the specified path. | `file: ./my_secret.txt` |
| `environment` | string | None | The secret is created with the value of an environment variable. | `environment: "MY_SECRET"` |
| `external` | boolean | `false` | If set to `true`, specifies that this secret has already been created. | `external: true` |
| `name` | string | None | The name of the secret object in Docker. | `name: my_secret` |

## 2. Dockerfile Instruction Reference

A complete reference for every Dockerfile instruction.

### `FROM`
Initializes a new build stage and sets the Base Image for subsequent instructions.
- Syntax: `FROM [--platform=<platform>] <image> [AS <name>]` or `FROM [--platform=<platform>] <image>[:<tag>] [AS <name>]` or `FROM [--platform=<platform>] <image>[@<digest>] [AS <name>]`
- Example: `FROM --platform=linux/amd64 ubuntu:22.04 AS builder`

### `RUN`
Executes any commands in a new layer on top of the current image and commits the results.
- Syntax: `RUN <command>` (shell form) or `RUN ["executable", "param1", "param2"]` (exec form)
- Flags: `--mount=type=cache|bind|secret|ssh`, `--network=default|none|host`
- Example: `RUN --mount=type=cache,target=/var/cache/apt apt-get update && apt-get install -y curl`

### `CMD`
Provides defaults for an executing container. There can only be one `CMD` instruction in a Dockerfile.
- Syntax: `CMD ["executable","param1","param2"]` (exec form, preferred) or `CMD ["param1","param2"]` (as default parameters to ENTRYPOINT) or `CMD command param1 param2` (shell form)
- Example: `CMD ["node", "server.js"]`

### `LABEL`
Adds metadata to an image.
- Syntax: `LABEL <key>=<value> <key>=<value> <key>=<value> ...`
- Example: `LABEL org.opencontainers.image.authors="team@example.com"`

### `EXPOSE`
Informs Docker that the container listens on the specified network ports at runtime.
- Syntax: `EXPOSE <port> [<port>/<protocol>...]`
- Example: `EXPOSE 80/tcp 80/udp`

### `ENV`
Sets the environment variable `<key>` to the value `<value>`.
- Syntax: `ENV <key>=<value> ...`
- Example: `ENV NODE_ENV=production PORT=3000`

### `ADD`
Copies new files, directories or remote file URLs from `<src>` and adds them to the filesystem of the image at the path `<dest>`.
- Syntax: `ADD [--chown=<user>:<group>] [--chmod=<perms>] [--checksum=<checksum>] <src>... <dest>`
- Example: `ADD https://example.com/big.tar.xz /usr/src/things/`

### `COPY`
Copies new files or directories from `<src>` and adds them to the filesystem of the container at the path `<dest>`.
- Syntax: `COPY [--chown=<user>:<group>] [--chmod=<perms>] <src>... <dest>`
- Example: `COPY --chown=node:node package*.json ./`

### `ENTRYPOINT`
Allows you to configure a container that will run as an executable.
- Syntax: `ENTRYPOINT ["executable", "param1", "param2"]` (exec form, preferred) or `ENTRYPOINT command param1 param2` (shell form)
- Example: `ENTRYPOINT ["docker-entrypoint.sh"]`

### `VOLUME`
Creates a mount point with the specified name and marks it as holding externally mounted volumes from native host or other containers.
- Syntax: `VOLUME ["/data"]`
- Example: `VOLUME /var/lib/mysql`

### `USER`
Sets the user name (or UID) and optionally the user group (or GID) to use when running the image and for any `RUN`, `CMD` and `ENTRYPOINT` instructions that follow it in the Dockerfile.
- Syntax: `USER <user>[:<group>]` or `USER <UID>[:<GID>]`
- Example: `USER 1000:1000`

### `WORKDIR`
Sets the working directory for any `RUN`, `CMD`, `ENTRYPOINT`, `COPY` and `ADD` instructions that follow it in the Dockerfile.
- Syntax: `WORKDIR /path/to/workdir`
- Example: `WORKDIR /app`

### `ARG`
Defines a variable that users can pass at build-time to the builder with the `docker build` command using the `--build-arg <varname>=<value>` flag.
- Syntax: `ARG <name>[=<default value>]`
- Example: `ARG VERSION=latest`

### `ONBUILD`
Adds to the image a trigger instruction to be executed at a later time, when the image is used as the base for another build.
- Syntax: `ONBUILD <INSTRUCTION>`
- Example: `ONBUILD COPY . /app/src`

### `STOPSIGNAL`
Sets the system call signal that will be sent to the container to exit.
- Syntax: `STOPSIGNAL signal`
- Example: `STOPSIGNAL SIGKILL`

### `HEALTHCHECK`
Tells Docker how to test a container to check that it is still working.
- Syntax: `HEALTHCHECK [OPTIONS] CMD command` or `HEALTHCHECK NONE`
- Options: `--interval=DURATION` (default: 30s), `--timeout=DURATION` (default: 30s), `--start-period=DURATION` (default: 0s), `--retries=N` (default: 3)
- Example: `HEALTHCHECK --interval=5m --timeout=3s CMD curl -f http://localhost/ || exit 1`

### `SHELL`
Allows the default shell used for the shell form of commands to be overridden.
- Syntax: `SHELL ["executable", "parameters"]`
- Example: `SHELL ["powershell", "-command"]`

## 3. `daemon.json` Complete Reference

The `daemon.json` file configures the Docker daemon.

| Field | Type | Default | Description |
|---|---|---|---|
| `storage-driver` | string | `overlay2` | The storage driver to use. |
| `log-driver` | string | `json-file` | The default logging driver. |
| `log-opts` | map | None | Options for the logging driver. |
| `default-address-pools` | list | None | Default address pools for node networks. |
| `dns` | list | None | DNS servers to use. |
| `registry-mirrors` | list | None | Registry mirrors to use. |
| `insecure-registries` | list | None | Insecure registries to allow. |
| `live-restore` | boolean | `false` | Enable live restore of docker when containers are still running. |
| `default-runtime` | string | `runc` | Default OCI runtime for containers. |
| `runtimes` | map | None | Register additional OCI runtimes. |
| `features` | map | None | Enable/disable specific features. |
| `builder` | map | None | BuildKit configuration. |
| `containerd` | string | None | Path to containerd socket. |
| `default-cgroupns-mode` | string | `private` | Default cgroup namespace mode. |
| `exec-opts` | list | None | Execution options. |
| `experimental` | boolean | `false` | Enable experimental features. |
| `fixed-cidr` | string | None | IPv4 subnet for fixed IPs. |
| `fixed-cidr-v6` | string | None | IPv6 subnet for fixed IPs. |
| `group` | string | `docker` | Group for the unix socket. |
| `hosts` | list | None | Daemon socket(s) to connect to. |
| `icc` | boolean | `true` | Enable inter-container communication. |
| `ip` | string | `0.0.0.0` | Default IP when binding container ports. |
| `ip-forward` | boolean | `true` | Enable net.ipv4.ip_forward. |
| `iptables` | boolean | `true` | Enable addition of iptables rules. |
| `ip-masq` | boolean | `true` | Enable IP masquerading. |
| `labels` | list | None | Daemon labels. |
| `max-concurrent-downloads` | integer | `3` | Max concurrent downloads. |
| `max-concurrent-uploads` | integer | `5` | Max concurrent uploads. |
| `max-download-attempts` | integer | `5` | Max download attempts. |
| `metrics-addr` | string | None | Address to serve metrics API. |
| `no-new-privileges` | boolean | `false` | Set no-new-privileges by default for new containers. |
| `oom-score-adjust` | integer | `-500` | Set the oom_score_adj for the daemon. |
| `pidfile` | string | `/var/run/docker.pid` | Path to use for daemon PID file. |
| `raw-logs` | boolean | `false` | Full timestamps without ANSI coloring. |
| `seccomp-profile` | string | None | Path to seccomp profile. |
| `selinux-enabled` | boolean | `false` | Enable selinux support. |
| `shutdown-timeout` | integer | `15` | Default timeout for stopping containers. |
| `tls` | boolean | `false` | Use TLS; implied by --tlsverify. |
| `tlscacert` | string | `~/.docker/ca.pem` | Trust certs signed only by this CA. |
| `tlscert` | string | `~/.docker/cert.pem` | Path to TLS certificate file. |
| `tlskey` | string | `~/.docker/key.pem` | Path to TLS key file. |
| `tlsverify` | boolean | `false` | Use TLS and verify the remote. |
| `userland-proxy` | boolean | `true` | Use userland proxy for loopback traffic. |
| `userns-remap` | string | None | User namespace remapping. |

## 4. `.dockerignore` Patterns

The `.dockerignore` file excludes files and directories from the build context.

### Syntax
- `#` for comments.
- `*` matches any sequence of non-separator characters.
- `?` matches any single non-separator character.
- `**` matches any number of directories.
- `!` negates a pattern.

### Common Patterns

**Node.js:**
```dockerignore
node_modules
npm-debug.log
Dockerfile
.dockerignore
.git
.gitignore
README.md
```

**Python:**
```dockerignore
__pycache__
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.env
Dockerfile
.dockerignore
.git
```

**Go:**
```dockerignore
bin/
obj/
*.exe
*.dll
*.so
*.dylib
Dockerfile
.dockerignore
.git
```

## 5. BuildKit Configuration (`buildkitd.toml`)

BuildKit can be configured via `buildkitd.toml`.

```toml
debug = true
# root is where all buildkit state is stored.
root = "/var/lib/buildkit"
# insecure-entitlements allows insecure entitlements, disabled by default.
insecure-entitlements = [ "network.host", "security.insecure" ]

[grpc]
  address = [ "tcp://0.0.0.0:1234" ]
  # debugAddress is address for attaching go pprof and expvar.
  debugAddress = "0.0.0.0:6060"
  uid = 0
  gid = 0
  [grpc.tls]
    cert = "/etc/buildkit/tls.crt"
    key = "/etc/buildkit/tls.key"
    ca = "/etc/buildkit/tlsca.crt"

[worker.oci]
  enabled = true
  # platforms is manually configure platforms, auto-detected by default.
  platforms = [ "linux/amd64", "linux/arm64" ]
  snapshotter = "auto" # overlayfs or native, default auto will try to use overlayfs
  rootless = false # see docs/rootless.md for more details on rootless mode.
  # Whether run subprocesses in main cgroup or create top-level cgroup.
  # Default is "cgroupfs" when not running rootless.
  cgroup-parent = "cgroupfs"
  # gc keeps/frees disk space.
  gc = true
  gckeepstorage = 9000
  [[worker.oci.gcpolicy]]
    keepBytes = 512000000
    keepDuration = 172800
    filters = [ "type==source.local", "type==exec.cachemount", "type==source.git.checkout"]
  [[worker.oci.gcpolicy]]
    all = true
    keepBytes = 1024000000

[worker.containerd]
  address = "/run/containerd/containerd.sock"
  enabled = true
  platforms = [ "linux/amd64", "linux/arm64" ]
  namespace = "buildkit"
  gc = true
  # gckeepstorage sets storage limit for default gc profile, in MB.
  gckeepstorage = 9000

[registry."docker.io"]
  mirrors = ["YOUR_REGISTRY_MIRROR"]
  http = true
  insecure = true
```

## 6. Docker Context Configuration

Docker contexts allow you to manage multiple Docker environments.

- Create a context: `docker context create my-context --docker "host=ssh://user@remote-host"`
- Use a context: `docker context use my-context`
- List contexts: `docker context ls`
- Inspect a context: `docker context inspect my-context`

## 7. Registry Configuration (`config.yml`)

Configuration for a private Docker registry.

```yaml
version: 0.1
log:
  fields:
    service: registry
storage:
  cache:
    blobdescriptor: inmemory
  filesystem:
    rootdirectory: /var/lib/registry
http:
  addr: :5000
  headers:
    X-Content-Type-Options: [nosniff]
health:
  storagedriver:
    enabled: true
    interval: 10s
    threshold: 3
```

## 8. Production `compose.yaml` Templates

### 8.1 Web App Stack

```yaml
services:
  webapp:
    image: YOUR_REGISTRY/webapp:v1.2.3
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    environment:
      - NODE_ENV=production
    secrets:
      - db_password
    networks:
      - frontend
      - backend
    deploy:
      replicas: 3
      update_config:
        parallelism: 1
        delay: 10s
      restart_policy:
        condition: on-failure
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"

networks:
  frontend:
  backend:
    internal: true

secrets:
  db_password:
    external: true
```

### 8.2 Database Stack

```yaml
services:
  db:
    image: postgres:15-alpine
    restart: always
    environment:
      POSTGRES_USER: admin
      POSTGRES_PASSWORD_FILE: /run/secrets/db_password
      POSTGRES_DB: myapp
    volumes:
      - db-data:/var/lib/postgresql/data
    secrets:
      - db_password
    networks:
      - backend
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 4G
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U admin -d myapp"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  db-data:

networks:
  backend:
    internal: true

secrets:
  db_password:
    external: true
```

### 8.3 Monitoring Stack (Prometheus/Grafana)

```yaml
services:
  prometheus:
    image: prom/prometheus:v2.45.0
    restart: unless-stopped
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml:ro
      - prometheus-data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--web.console.libraries=/etc/prometheus/console_libraries'
      - '--web.console.templates=/etc/prometheus/consoles'
      - '--web.enable-lifecycle'
    ports:
      - "9090:9090"
    networks:
      - monitoring

  grafana:
    image: grafana/grafana:10.0.3
    restart: unless-stopped
    volumes:
      - grafana-data:/var/lib/grafana
    environment:
      - GF_SECURITY_ADMIN_PASSWORD__FILE=/run/secrets/grafana_password
    secrets:
      - grafana_password
    ports:
      - "3000:3000"
    networks:
      - monitoring
    depends_on:
      - prometheus

volumes:
  prometheus-data:
  grafana-data:

networks:
  monitoring:

secrets:
  grafana_password:
    external: true
```

### 8.4 ELK Stack

```yaml
services:
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.9.0
    environment:
      - discovery.type=single-node
      - xpack.security.enabled=false
      - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
    volumes:
      - es-data:/usr/share/elasticsearch/data
    ports:
      - "9200:9200"
    networks:
      - elk

  logstash:
    image: docker.elastic.co/logstash/logstash:8.9.0
    volumes:
      - ./logstash.conf:/usr/share/logstash/pipeline/logstash.conf:ro
    ports:
      - "5044:5044"
    networks:
      - elk
    depends_on:
      - elasticsearch

  kibana:
    image: docker.elastic.co/kibana/kibana:8.9.0
    ports:
      - "5601:5601"
    networks:
      - elk
    depends_on:
      - elasticsearch

volumes:
  es-data:

networks:
  elk:
```

## 9. Troubleshooting and Optimization

### 9.1 Common Errors and Solutions

- **"port already in use"**: Use `lsof -i :PORT` to find the conflicting process, or change the port mapping in `compose.yaml`.
- **"no space left on device"**: Run `docker system prune -a --volumes` to clear unused data. Check the `overlay2` directory size.
- **"OOM killed"**: The container exceeded its memory limit. Increase the `mem_limit` in `compose.yaml` or optimize the application's memory usage.
- **"permission denied"**: Check the user/group permissions of the mounted volumes. Ensure the container user has access.
- **"network not found"**: Run `docker network create <network_name>` or ensure the network is defined in `compose.yaml`.
- **"image not found"**: Verify the registry URL, image tag, and `pull_policy`. Ensure you are logged in to the registry.
- **"container unhealthy"**: Check the `healthcheck` command and logs. Increase the `timeout` or `start_period` if the application takes longer to start.
- **"bind mount permission denied"**: On SELinux systems, append `:z` or `:Z` to the volume mount path (e.g., `./data:/data:z`).
- **"DNS resolution failed"**: Check the host's DNS settings or configure custom DNS servers in `daemon.json` or `compose.yaml`.
- **"cannot start service"**: Check `depends_on` conditions. Ensure required services are healthy before starting dependent services.
- **"exec format error"**: The image architecture does not match the host architecture (e.g., running an ARM image on an AMD64 host). Use `docker buildx` to build multi-platform images.
- **"context deadline exceeded"**: Increase the timeout for Docker commands or check network connectivity to the registry.

### 9.2 Cost and Time Optimization

- **Multi-stage builds**: Use multi-stage builds to create smaller final images. This reduces pull times and storage costs.
- **Layer caching**: Order Dockerfile instructions from least frequently changed to most frequently changed to maximize cache hits.
- **BuildKit cache mounts**: Use `--mount=type=cache` to cache package manager downloads (e.g., `apt`, `npm`, `pip`) between builds.
- **Parallel builds**: Use `docker compose build --parallel` to build multiple services concurrently.
- **Image pull policy**: Set `pull_policy: if-not-present` to avoid unnecessary image pulls.
- **Resource limits**: Set CPU and memory limits to prevent runaway containers from consuming all host resources.
- **Logging**: Configure log rotation (`max-size`, `max-file`) to prevent log files from filling up the disk.
- **Prune**: Regularly run `docker system prune` and `docker volume prune` to remove unused resources.
- **Compose profiles**: Use profiles to start only the services needed for a specific environment or task.
- **Compose watch**: Use `develop: watch` for fast iteration during development without rebuilding images.

### 9.3 Security Hardening

- **Non-root user**: Run containers as a non-root user (`USER 1000:1000`).
- **Read-only root filesystem**: Set `read_only: true` to prevent modifications to the container's root filesystem.
- **Drop capabilities**: Drop all Linux capabilities (`cap_drop: ["ALL"]`) and add only the necessary ones.
- **No new privileges**: Set `security_opt: ["no-new-privileges:true"]` to prevent processes from gaining additional privileges.
- **Seccomp profiles**: Use custom seccomp profiles to restrict system calls.
- **Resource limits**: Enforce CPU, memory, and PID limits to prevent denial-of-service attacks.
- **No privileged mode**: Avoid using `privileged: true` unless absolutely necessary.
- **Minimal base images**: Use minimal base images like `alpine`, `distroless`, or `scratch` to reduce the attack surface.
- **Secrets management**: Use Docker secrets instead of environment variables for sensitive data.
- **Network segmentation**: Use internal networks to isolate backend services from the public internet.

### 9.4 Upgrade Strategies

- **Blue-green deployment**: Run the new version alongside the old version and switch traffic when ready.
- **Rolling update**: Use `update_config` with `parallelism` and `delay` to update containers one by one.
- **Canary release**: Route a small percentage of traffic to the new version to test it before a full rollout.
- **Database migrations**: Run database migrations as an init container or a pre-start hook before starting the application.
- **Rollback**: Configure `rollback_config` to automatically roll back to the previous version if the update fails.
- **Zero-downtime**: Use `order: start-first` in `update_config` to start the new container before stopping the old one.

## === FILE: 49-docker-deep-dive.md ===
# Specialist #49: Docker Super Specialist - Deep Dive into Architecture, Internals, and Performance Tuning

Welcome to the definitive guide for the Docker Super Specialist. This document serves as the ultimate reference for tech support operations teams, DevOps engineers, and system administrators tasked with optimizing, troubleshooting, and scaling Docker environments in production. We will explore the deepest internals of Docker, from the engine architecture to the union filesystem, container lifecycle, namespace isolation, cgroup resource control, network and storage internals, build optimization, performance tuning, monitoring, and garbage collection.

This guide is designed to be extremely comprehensive, providing real-world configuration examples, actionable commands, and solutions to the most complex edge cases you will encounter in production.

---

## 1. Docker Engine Internals

To truly master Docker, one must understand the underlying components that make up the Docker Engine. The Docker Engine is not a monolithic entity; it is a collection of specialized components working in harmony to manage the container lifecycle.

### 1.1 The Docker Daemon (`dockerd`)

The Docker daemon (`dockerd`) is the persistent background process that manages Docker objects such as images, containers, networks, and volumes. It listens for Docker API requests and processes them.

**Key Responsibilities:**
- Managing the container lifecycle (create, start, stop, delete).
- Image management (pulling, pushing, building).
- Network and volume management.
- Routing requests to `containerd`.

**Production Configuration Example (`/etc/docker/daemon.json`):**
```json
{
  "debug": false,
  "tls": true,
  "tlscert": "/var/docker/server.pem",
  "tlskey": "/var/docker/serverkey.pem",
  "hosts": ["tcp://0.0.0.0:2376", "unix:///var/run/docker.sock"],
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "100m",
    "max-file": "3"
  },
  "storage-driver": "overlay2",
  "metrics-addr": "0.0.0.0:9323",
  "experimental": true,
  "max-concurrent-downloads": 10,
  "max-concurrent-uploads": 5
}
```

### 1.2 `containerd`

`containerd` is an industry-standard core container runtime. It was originally part of the Docker daemon but was spun out into its own project (now a CNCF graduated project). It manages the complete container lifecycle of its host system, from image transfer and storage to container execution and supervision.

**Key Responsibilities:**
- Image push and pull.
- Managing storage and retrieval of images.
- Executing containers (by calling `runc`).
- Managing network interfaces.

### 1.3 `containerd-shim`

The `containerd-shim` is a lightweight daemon that sits between `containerd` and the container runtime (`runc`). Its primary purpose is to decouple the container process from `containerd`.

**Why is it necessary?**
- **Daemonless Containers:** If `containerd` crashes or is restarted, the containers keep running because they are parented by the shim, not `containerd`.
- **STDIO Management:** It keeps the STDIO and other file descriptors open for the container.
- **Exit Status:** It reports the container's exit status back to `containerd`.

### 1.4 `runc` and the OCI Runtime Specification

`runc` is the default low-level container runtime used by Docker. It is a CLI tool for spawning and running containers according to the Open Container Initiative (OCI) specification.

**The OCI Runtime Spec:**
The OCI Runtime Specification defines how a container should be created and executed. It specifies the configuration format (`config.json`) and the lifecycle hooks. `runc` reads this configuration and uses Linux kernel features (namespaces, cgroups, capabilities) to create the isolated environment.

**Example: Inspecting an OCI Bundle:**
When Docker creates a container, it generates an OCI bundle. You can manually inspect this:
```bash
# Find the container ID
docker ps -q

# The OCI bundle is typically located in:
# /var/run/docker/containerd/daemon/io.containerd.runtime.v2.task/moby/<CONTAINER_ID>/
cat /var/run/docker/containerd/daemon/io.containerd.runtime.v2.task/moby/<CONTAINER_ID>/config.json
```

### 1.5 OCI Image Specification and Manifests

The OCI Image Specification defines the format for container images. An image consists of:
- **Image Manifest:** A JSON document describing the image, including pointers to the configuration and the layers.
- **Image Configuration:** A JSON document containing execution parameters (entrypoint, env vars) and the history of the image.
- **Layers:** Tar archives containing the filesystem changes.

**Content-Addressable Storage (CAS):**
Docker uses CAS for images. Each layer and configuration is identified by the SHA256 hash of its contents. This ensures integrity and enables deduplication. If two images share the exact same layer, it is only stored once on disk.

---

## 2. Union Filesystem and `overlay2` Internals

The Union Filesystem is the magic behind Docker's lightweight images and fast startup times. It allows multiple directories (layers) to be overlaid, appearing as a single unified filesystem. The default and recommended storage driver is `overlay2`.

### 2.1 `overlay2` Architecture

The `overlay2` driver uses four main directories to construct the container's filesystem:

1.  **`lowerdir` (Image Layers):** These are the read-only layers that make up the Docker image. They are stacked on top of each other.
2.  **`upperdir` (Container Layer):** This is the read-write layer specific to the running container. Any changes made by the container are written here.
3.  **`workdir`:** An internal directory used by the OverlayFS kernel module to prepare files before they are switched to the `upperdir`. It must be on the same filesystem as the `upperdir`.
4.  **`merged`:** The unified view of the `lowerdir` and `upperdir`. This is what the container actually sees and interacts with.

**Visualizing the Mount:**
You can see the `overlay` mount on the host system:
```bash
# Find the container's merged directory
docker inspect -f '{{.GraphDriver.Data.MergedDir}}' <CONTAINER_ID>

# Check the mount details
mount | grep overlay
# Output example:
# overlay on /var/lib/docker/overlay2/<ID>/merged type overlay (rw,relatime,lowerdir=/var/lib/docker/overlay2/l/<ID1>:/var/lib/docker/overlay2/l/<ID2>,upperdir=/var/lib/docker/overlay2/<ID>/diff,workdir=/var/lib/docker/overlay2/<ID>/work)
```

### 2.2 Copy-on-Write (CoW) Mechanics

When a container needs to modify a file that exists in a read-only `lowerdir`, the `overlay2` driver performs a Copy-on-Write operation:
1.  It searches down through the `lowerdir` stack to find the file.
2.  It copies the file up to the `upperdir`.
3.  The container modifies the copy in the `upperdir`.
4.  Subsequent reads of the file by the container will hit the modified copy in the `upperdir`.

**Performance Implication:** The first time a file is modified, there is a slight performance penalty due to the copy operation. For write-heavy workloads (e.g., databases), this is detrimental. **Solution:** Always use Docker Volumes for write-heavy data, as volumes bypass the union filesystem entirely.

### 2.3 Whiteout Files and Opaque Whiteouts

How does a container delete a file that exists in a read-only image layer? It cannot actually delete the file from the `lowerdir`. Instead, it uses whiteout files.

-   **Whiteout File:** If a container deletes `/app/config.txt`, the `overlay2` driver creates a special character device file named `.wh.config.txt` in the `upperdir`. When the `merged` view is constructed, the presence of this whiteout file hides the original file from the container.
-   **Opaque Whiteout:** If a container deletes an entire directory, an opaque whiteout is used. A special extended attribute (`trusted.overlay.opaque="y"`) is set on the directory in the `upperdir`, hiding all contents of the corresponding directory in the `lowerdir`.

### 2.4 Layer Deduplication

Because Docker uses content-addressable storage, layers are deduplicated at the host level. If you pull `ubuntu:20.04` and `ubuntu:22.04`, and they happen to share a base layer (unlikely for different major versions, but common for different tags of the same app), that layer is only stored once in `/var/lib/docker/overlay2/`.

---

## 3. Container Lifecycle Deep Dive

Understanding the exact sequence of events during a container's lifecycle is crucial for troubleshooting startup failures and zombie processes.

### 3.1 Lifecycle Commands

-   **`create`:** Creates the read-write layer (`upperdir`), generates the OCI `config.json`, but does *not* start the process.
-   **`start`:** Instructs `containerd` to launch the `containerd-shim`, which invokes `runc` to create the namespaces and cgroups, and finally executes the container's entrypoint process.
-   **`attach`:** Connects the host's standard input, output, and error streams to the running container's main process (PID 1).
-   **`exec`:** Uses `runc` to enter the existing namespaces of a running container and spawn a *new* process alongside the main process.
-   **`pause` / `unpause`:** Uses the `freezer` cgroup to suspend and resume all processes within the container. The processes are unaware they were paused.
-   **`stop`:** Sends a `SIGTERM` signal to PID 1. Waits for a grace period (default 10s). If the process hasn't exited, sends a `SIGKILL`.
-   **`kill`:** Sends a `SIGKILL` (or a specified signal) directly to PID 1, terminating it immediately without grace.
-   **`remove` (`rm`):** Deletes the container's read-write layer, configuration files, and network interfaces.

### 3.2 Signal Handling and the PID 1 Problem

In a Linux system, PID 1 is the `init` process. It has two special responsibilities:
1.  **Signal Forwarding:** It must handle signals (like `SIGTERM` or `SIGINT`) and forward them to child processes, or handle them gracefully to shut down.
2.  **Zombie Reaping:** When a child process dies, it becomes a "zombie" until its parent reads its exit status (via `wait()`). If the parent dies before doing this, the zombie is "orphaned" and reparented to PID 1. PID 1 *must* reap these zombies.

**The Problem in Docker:**
If your application (e.g., a Node.js script or a Java app) runs as PID 1 in the container, it likely does *not* know how to reap zombies or forward signals properly.
-   If it doesn't handle `SIGTERM`, `docker stop` will hang for 10 seconds and then forcefully kill the container, leading to data corruption.
-   If it spawns child processes that die, they will accumulate as zombies, eventually exhausting the host's PID limit.

**The Solution: `tini`**
`tini` is a tiny, valid `init` process designed specifically for containers. It runs as PID 1, spawns your application as a child, forwards signals to it, and reaps any zombies.

**Implementation:**
You can use `tini` in two ways:
1.  **In the Dockerfile:**
    ```dockerfile
    RUN apk add --no-cache tini
    ENTRYPOINT ["/sbin/tini", "--"]
    CMD ["node", "app.js"]
    ```
2.  **Via Docker Run / Compose:**
    ```bash
    docker run --init my-image
    ```
    ```yaml
    # compose.yaml
    services:
      app:
        image: my-image
        init: true
    ```

---

## 4. Namespace Isolation

Namespaces are the fundamental Linux kernel feature that provides isolation for containers. They ensure that a process in one container cannot see or affect processes in another container or the host.

### 4.1 The 7 Namespaces

1.  **Mount Namespace (`mnt`):** Isolates the filesystem mount points. The container sees its own root filesystem (the `merged` overlay directory) and cannot see the host's filesystem unless explicitly bind-mounted.
2.  **Process ID Namespace (`pid`):** Isolates the PID number space. The main process in the container is PID 1 inside the container, but it might be PID 14532 on the host.
3.  **Network Namespace (`net`):** Isolates network interfaces, routing tables, iptables rules, and sockets. The container gets its own `eth0` interface and IP address.
4.  **Inter-Process Communication Namespace (`ipc`):** Isolates System V IPC objects and POSIX message queues. Prevents containers from accessing each other's shared memory segments.
5.  **UNIX Time-Sharing Namespace (`uts`):** Isolates the hostname and NIS domain name. Allows the container to have its own hostname independent of the host.
6.  **User Namespace (`user`):** Isolates user and group IDs. A process can run as `root` (UID 0) inside the container, but be mapped to an unprivileged user (e.g., UID 100000) on the host. This is a critical security feature.
7.  **Control Group Namespace (`cgroup`):** Isolates the view of cgroups. The container sees its own cgroup paths as the root, preventing it from modifying host cgroup limits.

### 4.2 Inspecting Namespaces

You can use the `lsns` command on the host to view namespaces:
```bash
# Find the host PID of a container
HOST_PID=$(docker inspect -f '{{.State.Pid}}' <CONTAINER_ID>)

# List namespaces for that PID
sudo lsns -p $HOST_PID
```

You can also use `nsenter` to execute a command within a specific namespace of a container (useful for debugging without `docker exec`):
```bash
# Enter the network namespace of the container and run ifconfig
sudo nsenter -t $HOST_PID -n ifconfig
```

---

## 5. Cgroup Resource Control

Control Groups (cgroups) limit, account for, and isolate the resource usage (CPU, memory, disk I/O, network) of a collection of processes.

### 5.1 Cgroup v1 vs v2

-   **Cgroup v1:** The legacy implementation. It uses a separate hierarchy for each resource controller (e.g., `/sys/fs/cgroup/memory`, `/sys/fs/cgroup/cpu`). It is complex and can lead to inconsistencies.
-   **Cgroup v2:** The modern implementation (default in modern Linux distributions). It uses a single unified hierarchy (`/sys/fs/cgroup/`). It provides better consistency, safer delegation, and advanced features like memory pressure monitoring (PSI). Docker fully supports cgroup v2.

### 5.2 Memory Limits

-   **Limit (`--memory` / `mem_limit`):** The hard limit. If the container exceeds this, the kernel's OOM (Out of Memory) killer will terminate processes within the container.
-   **Reservation (`--memory-reservation` / `mem_reservation`):** A soft limit. During memory pressure on the host, the kernel will try to reclaim memory from containers exceeding their reservation.
-   **Swap (`--memory-swap` / `memswap_limit`):** The total amount of memory + swap the container can use. If set equal to `--memory`, the container cannot use swap.

**Troubleshooting OOM Kills:**
If a container exits with code 137, it was likely OOM killed.
```bash
# Check if a container was OOM killed
docker inspect -f '{{.State.OOMKilled}}' <CONTAINER_ID>

# Check host kernel logs for OOM events
dmesg -T | grep -i oom
```

### 5.3 CPU Limits

-   **Shares (`--cpu-shares` / `cpu_shares`):** A relative weight (default 1024). If Container A has 1024 and Container B has 512, A gets twice as much CPU time *only when there is contention*.
-   **Quota and Period (`--cpus` / `cpus`):** A hard limit. `--cpus="1.5"` means the container is guaranteed at most 1.5 CPUs worth of execution time every 100ms (the default period). Under the hood, this sets `cpu.cfs_quota_us` to 150000 and `cpu.cfs_period_us` to 100000.
-   **Cpuset (`--cpuset-cpus` / `cpuset`):** Pins the container to specific CPU cores (e.g., `0,3` or `1-3`). Useful for NUMA architectures or extreme performance tuning.

### 5.4 PIDs Limit and Blkio

-   **PIDs Limit (`--pids-limit` / `pids_limit`):** Limits the number of processes/threads a container can spawn. Crucial for preventing fork bombs.
-   **Blkio (`--device-read-bps`, `--device-write-iops`):** Limits the block I/O bandwidth or IOPS to specific devices. Useful for preventing noisy neighbors from saturating disk I/O.

**Compose Example:**
```yaml
services:
  db:
    image: postgres:15
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 4G
          pids: 200
        reservations:
          cpus: '0.5'
          memory: 1G
```

---

## 6. Network Internals

Docker networking is built on standard Linux networking primitives: network namespaces, virtual ethernet devices (veth pairs), bridges, and iptables/nftables.

### 6.1 The `bridge` Network (Default)

When you start Docker, it creates a default bridge network named `docker0`.
1.  **Veth Pairs:** When a container is attached to a bridge, Docker creates a veth pair. One end (`eth0`) is placed inside the container's network namespace. The other end (`vethXXXX`) is placed in the host's network namespace and attached to the `docker0` bridge.
2.  **IP Allocation:** Docker's internal IPAM (IP Address Management) assigns an IP address to the container's `eth0` from the bridge's subnet.
3.  **NAT and Port Mapping:** To expose a container port to the outside world (e.g., `-p 8080:80`), Docker configures `iptables` rules in the `nat` table. It creates a DNAT (Destination NAT) rule that intercepts traffic hitting the host on port 8080 and rewrites the destination IP to the container's internal IP on port 80.

**Inspecting iptables:**
```bash
sudo iptables -t nat -L DOCKER -n -v
```

### 6.2 Embedded DNS Server (`127.0.0.11`)

Containers on user-defined networks (like those created by Docker Compose) can resolve each other by container name or service name. This is achieved via Docker's embedded DNS server.
-   Inside the container, `/etc/resolv.conf` points to `127.0.0.11`.
-   Docker intercepts DNS queries to this address.
-   If the query is for a known container name, Docker returns the internal IP.
-   If not, Docker forwards the query to the external DNS servers configured on the host.

### 6.3 Service Discovery and Load Balancing

In Docker Compose, if you scale a service (`docker compose up --scale web=3`), Docker creates three containers. The embedded DNS server handles service discovery. When another container queries the service name `web`, the DNS server returns the IP addresses of all three containers in a round-robin fashion, providing basic client-side load balancing.

---

## 7. Storage Internals

Docker manages storage through a pluggable architecture involving graph drivers, layer stores, and volume drivers.

### 7.1 Graph Driver and Layer Store

The Graph Driver (e.g., `overlay2`) is responsible for managing the image layers and the container's read-write layer. The Layer Store keeps track of the metadata for these layers, mapping the SHA256 content hashes to the actual directories on disk.

### 7.2 Volumes vs. Bind Mounts

-   **Bind Mounts:** Map a specific path on the host directly into the container. Performance is native, but it tightly couples the container to the host's filesystem structure.
-   **Volumes:** Managed entirely by Docker (stored in `/var/lib/docker/volumes/`). They bypass the union filesystem, offering native I/O performance. They are the recommended way to persist data.

**Volume Drivers:**
Docker supports volume plugins. You can use drivers like `local` (default), or third-party drivers to mount NFS shares, AWS EBS volumes, or Azure Files directly into containers.

**Example: NFS Volume in Compose:**
```yaml
volumes:
  nfs-data:
    driver: local
    driver_opts:
      type: nfs
      o: addr=10.0.0.10,rw,nolock,hard,nointr,nfsvers=4
      device: ":/path/to/nfs/share"
```

---

## 8. Build Internals and BuildKit

BuildKit is the modern build engine for Docker (default since Docker 23.0). It completely overhauled the build process, focusing on performance, caching, and security.

### 8.1 BuildKit Architecture

1.  **Frontend:** Reads the build definition (e.g., a Dockerfile) and converts it into an intermediate representation called LLB (Low-Level Build).
2.  **LLB (Low-Level Build):** A binary format, essentially an assembly language for builds. It defines a directed acyclic graph (DAG) of build operations.
3.  **Solver:** Takes the LLB graph, analyzes dependencies, and executes the operations. Because it understands the DAG, it can execute independent steps in parallel.
4.  **Cache:** Manages the build cache. BuildKit supports advanced caching backends (local directory, registry, AWS S3, GitHub Actions cache).
5.  **Exporter:** Takes the final result of the solver and exports it (e.g., as an OCI image to the local daemon, or directly to a registry).

### 8.2 Advanced BuildKit Features

-   **Parallel Execution:** Multi-stage builds are analyzed, and stages that don't depend on each other are built simultaneously.
-   **Secret Mounts:** Securely pass secrets to the build process without leaving them in the final image layers.
    ```dockerfile
    RUN --mount=type=secret,id=mysecret cat /run/secrets/mysecret
    ```
-   **Cache Mounts:** Persist package manager caches (like `apt`, `npm`, `pip`) between build runs, drastically speeding up rebuilds.
    ```dockerfile
    RUN --mount=type=cache,target=/root/.npm npm install
    ```
-   **SSH Forwarding:** Allow the build process to use the host's SSH agent to clone private repositories.
    ```dockerfile
    RUN --mount=type=ssh git clone git@github.com:myorg/private-repo.git
    ```

---

## 9. Performance Tuning

Optimizing Docker for production requires tuning at multiple levels: storage, network, memory, and the build process.

### 9.1 I/O Optimization

-   **Storage Driver:** Ensure you are using `overlay2` on a modern filesystem (ext4 or xfs). Avoid `devicemapper` or `btrfs` unless specifically required.
-   **Volumes for Write-Heavy Data:** Never write databases or logs to the container's read-write layer. Always use named volumes or bind mounts.
-   **macOS/Windows Tuning (VirtioFS):** If running Docker Desktop, enable VirtioFS for significantly faster bind mount performance compared to gRPC FUSE or osxfs.

### 9.2 Network Optimization

-   **MTU Tuning:** If your host network uses jumbo frames (MTU 9000), you must configure the Docker bridge and container interfaces to match, otherwise, you will experience packet fragmentation and severe performance degradation.
    ```json
    // /etc/docker/daemon.json
    {
      "mtu": 9000
    }
    ```
-   **Host Network Mode:** For extreme network performance (e.g., high-frequency trading or high-throughput load balancers), use `--network host`. This bypasses the bridge and NAT overhead entirely, but sacrifices network isolation.

### 9.3 Memory Optimization for Runtimes

Containers enforce hard memory limits. Runtimes like the JVM or Go garbage collector must be aware of these limits, otherwise, they will allocate memory based on the *host's* total memory and get OOM killed.

-   **Java (JVM):** Use `-XX:+UseContainerSupport` (default in Java 10+) and set `-XX:MaxRAMPercentage=75.0` to let the JVM automatically size its heap based on the container's cgroup limit.
-   **Go:** Set the `GOMEMLIMIT` environment variable to slightly below the container's memory limit (e.g., 90%) to trigger aggressive garbage collection before hitting the OOM killer.
    ```yaml
    services:
      go-app:
        image: my-go-app
        environment:
          - GOMEMLIMIT=900MiB
        deploy:
          resources:
            limits:
              memory: 1000M
    ```

### 9.4 Build Optimization

-   **Minimal Base Images:** Use `alpine`, `distroless`, or `scratch` to reduce image size, pull time, and attack surface.
-   **Layer Ordering:** Place instructions that change frequently (like `COPY . .`) at the bottom of the Dockerfile. Place instructions that rarely change (like installing OS packages) at the top to maximize cache hits.
-   **`.dockerignore`:** Exclude `.git`, `node_modules`, and large local files from the build context to speed up the transfer to the Docker daemon.

---

## 10. Monitoring and Observability

You cannot optimize what you cannot measure. Comprehensive monitoring is essential for production Docker environments.

### 10.1 Container Metrics

Docker provides built-in commands for basic monitoring:
-   `docker stats`: Real-time stream of CPU, memory, network I/O, and block I/O.
-   `docker events`: Stream of real-time events from the server (container start, stop, die, OOM).

### 10.2 cAdvisor and Prometheus

For production, use Google's `cAdvisor` (Container Advisor). It runs as a daemon, collects resource usage and performance characteristics of running containers, and exposes them as Prometheus metrics.

**Compose Setup for Monitoring:**
```yaml
services:
  cadvisor:
    image: gcr.io/cadvisor/cadvisor:v0.47.0
    volumes:
      - /:/rootfs:ro
      - /var/run:/var/run:ro
      - /sys:/sys:ro
      - /var/lib/docker/:/var/lib/docker:ro
      - /dev/disk/:/dev/disk:ro
    ports:
      - "8080:8080"
    privileged: true
    devices:
      - /dev/kmsg

  prometheus:
    image: prom/prometheus:v2.45.0
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
    ports:
      - "9090:9090"
```

### 10.3 Health Checks

Never rely solely on the container process running. Use Docker Healthchecks to verify the application is actually responding.

```yaml
services:
  web:
    image: nginx
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost/"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

---

## 11. Garbage Collection and Cleanup

Docker environments accumulate cruft over time: dangling images, stopped containers, unused volumes, and build cache. Automated garbage collection is critical to prevent disk exhaustion.

### 11.1 Manual Cleanup Commands

-   `docker system prune -a --volumes`: The nuclear option. Removes all stopped containers, unused networks, dangling images, unused images, and unused volumes.
-   `docker image prune`: Removes dangling images (images with no tag, usually left over from builds).
-   `docker volume prune`: Removes volumes not attached to any container. **Use with extreme caution.**
-   `docker builder prune`: Clears the BuildKit cache.

### 11.2 Automated Cleanup Strategies

In production, configure a cron job or a systemd timer to run cleanup regularly.

**Example Cron Job (runs daily at 3 AM):**
```bash
0 3 * * * /usr/bin/docker system prune -f --filter "until=168h"
```
*(This removes unused data older than 7 days).*

### 11.3 Registry Garbage Collection

If you run a private Docker Registry, deleting an image via the API only removes the manifest. The actual layers remain on disk. You must run the registry's garbage collector to reclaim space.

```bash
# Run GC on a private registry container
docker exec -it registry bin/registry garbage-collect /etc/docker/registry/config.yml
```

---

## 12. Production Troubleshooting Guide

When things go wrong, a systematic approach is required. Here are common scenarios and their solutions.

### Scenario 1: "No space left on device"

**Symptoms:** Containers fail to start, builds fail, host OS becomes unstable.
**Diagnosis:**
1.  Check host disk space: `df -h`
2.  Check Docker disk usage: `docker system df -v`
3.  Identify large containers: `docker ps -s`
**Solutions:**
-   Run `docker system prune`.
-   Check container logs. If a container is writing massive logs to the json-file driver, configure log rotation in `daemon.json` or `compose.yaml`.
-   Ensure databases are writing to volumes, not the container layer.

### Scenario 2: Container Exits Immediately (Code 1 or 255)

**Symptoms:** `docker run` returns immediately. `docker ps -a` shows the container as "Exited".
**Diagnosis:**
1.  Check logs: `docker logs <CONTAINER_ID>`
2.  Inspect the entrypoint/cmd: `docker inspect <CONTAINER_ID>`
**Solutions:**
-   The main process must run in the foreground. If your entrypoint script runs a daemon in the background and exits, the container will stop. Use `exec` to replace the shell with the daemon process, or run the daemon in the foreground.
-   Check for missing environment variables or configuration files required by the application.

### Scenario 3: Network Connectivity Issues

**Symptoms:** Container cannot reach the internet, or containers cannot communicate with each other.
**Diagnosis:**
1.  Check DNS resolution inside the container: `docker exec -it <ID> nslookup google.com`
2.  Check routing: `docker exec -it <ID> ip route`
3.  Check host iptables: `sudo iptables -L -n -v`
**Solutions:**
-   If DNS fails, ensure the host's `/etc/resolv.conf` is correct, or specify DNS servers in `daemon.json`.
-   If containers on the same custom network cannot communicate, check for IP conflicts or restrictive firewall rules on the host (e.g., `firewalld` blocking bridge traffic).

---

## 13. The Ultimate Production Checklist

Before deploying any Docker workload to production, ensure it passes this checklist:

1.  [ ] **No `:latest` tags:** Pin all images to specific versions or SHA256 digests.
2.  [ ] **Resource Limits:** Every container must have memory and CPU limits defined.
3.  [ ] **Healthchecks:** Every service must have a robust healthcheck configured.
4.  [ ] **Restart Policies:** Use `unless-stopped` or `on-failure` to ensure resilience.
5.  [ ] **Non-Root User:** Run applications as a non-root user (`USER 1000:1000` in Dockerfile).
6.  [ ] **Read-Only Root Filesystem:** Set `read_only: true` and mount `tmpfs` for required temporary directories.
7.  [ ] **Drop Capabilities:** Use `cap_drop: ALL` and add back only what is strictly necessary.
8.  [ ] **Log Rotation:** Configure `max-size` and `max-file` for the logging driver.
9.  [ ] **Secrets Management:** Never pass sensitive data via environment variables. Use Docker Secrets or a vault solution.
10. [ ] **Init Process:** Use `tini` (`init: true`) for proper signal handling and zombie reaping.

---

## Conclusion

Mastering Docker requires moving beyond basic commands and understanding the intricate dance between the Docker daemon, containerd, runc, the Linux kernel, and the union filesystem. By applying the principles of namespace isolation, cgroup resource control, and BuildKit optimization detailed in this guide, you can build, deploy, and troubleshoot highly resilient, secure, and performant containerized applications at scale. This knowledge separates a standard operator from a true Docker Super Specialist.


---

## 14. Advanced Docker Compose Strategies

Docker Compose is often seen as a development tool, but with the right configurations, it is a powerful orchestrator for single-node production deployments.

### 14.1 Compose Profiles

Profiles allow you to define multiple environments (e.g., dev, test, prod) within a single `compose.yaml` file. Services are assigned to profiles, and you can start specific profiles as needed.

**Example:**
```yaml
services:
  web:
    image: my-web-app
    profiles: ["dev", "prod"]
  db:
    image: postgres:15
    profiles: ["dev", "prod"]
  admin-panel:
    image: my-admin-panel
    profiles: ["dev"]
  metrics:
    image: prom/prometheus
    profiles: ["prod"]
```
To start only the production services:
```bash
docker compose --profile prod up -d
```

### 14.2 Compose Watch (Development Optimization)

Introduced in Compose V2.22, `watch` provides a native hot-reload experience without needing third-party tools like Nodemon or complex bind mounts. It syncs file changes directly into the container or triggers rebuilds based on rules.

**Example:**
```yaml
services:
  frontend:
    image: my-react-app
    build: ./frontend
    develop:
      watch:
        - action: sync
          path: ./frontend/src
          target: /app/src
          ignore:
            - node_modules/
        - action: rebuild
          path: ./frontend/package.json
```
Run it with:
```bash
docker compose watch
```

### 14.3 Extending Services and Overrides

To keep your Compose files DRY (Don't Repeat Yourself), use the `extends` keyword or multiple Compose files (e.g., `compose.yaml` and `compose.override.yaml`).

**Using `extends`:**
```yaml
# common.yaml
services:
  base-app:
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
    restart: always

# compose.yaml
services:
  web:
    extends:
      file: common.yaml
      service: base-app
    image: my-web
```

---

## 15. Security Hardening Deep Dive

Security is paramount in production. A compromised container can lead to a compromised host if not properly isolated.

### 15.1 Seccomp Profiles

Secure Computing Mode (seccomp) is a Linux kernel feature that restricts the system calls a process can make. Docker uses a default seccomp profile that blocks about 44 out of 300+ syscalls, preventing actions like module loading or modifying kernel parameters.

**Custom Seccomp Profile:**
For highly secure environments, you can create a custom JSON profile that only allows the exact syscalls your application needs.
```yaml
services:
  secure-app:
    image: my-app
    security_opt:
      - seccomp=/path/to/custom-profile.json
```

### 15.2 AppArmor and SELinux

-   **AppArmor (Debian/Ubuntu):** A Mandatory Access Control (MAC) system. Docker generates a default AppArmor profile (`docker-default`). You can apply custom profiles to restrict file access and network operations.
-   **SELinux (RHEL/CentOS/Fedora):** Another MAC system. When using bind mounts with SELinux enforcing, you must append `:z` (shared) or `:Z` (private) to the mount path so Docker can relabel the files correctly.
    ```yaml
    volumes:
      - ./data:/app/data:Z
    ```

### 15.3 User Namespaces Remapping

By default, UID 0 (root) inside the container is UID 0 on the host. If a process escapes the container, it has root access to the host. User namespace remapping maps container UIDs to unprivileged host UIDs.

**Configuration (`/etc/docker/daemon.json`):**
```json
{
  "userns-remap": "default"
}
```
This creates a user `dockremap`. UID 0 in the container might map to UID 165536 on the host.

---

## 16. Docker Upgrade and Migration Strategies

Upgrading Docker Engine or migrating containers between hosts requires careful planning to minimize downtime.

### 16.1 Zero-Downtime Updates with Compose

When updating an image in Compose, the default behavior is to stop the old container, remove it, and start the new one, causing downtime. You can configure rolling updates using the `deploy` key (originally for Swarm, but supported by Compose V2).

```yaml
services:
  web:
    image: my-web:v2
    deploy:
      update_config:
        order: start-first
        failure_action: rollback
        delay: 10s
```
With `order: start-first`, Compose starts the new container, waits for it to be healthy, and then stops the old one.

### 16.2 Migrating Volumes

To move a named volume from Host A to Host B:

**On Host A (Backup):**
```bash
docker run --rm -v my-volume:/data -v $(pwd):/backup ubuntu tar cvf /backup/backup.tar /data
```

**On Host B (Restore):**
```bash
docker volume create my-volume
docker run --rm -v my-volume:/data -v $(pwd):/backup ubuntu tar xvf /backup/backup.tar -C /
```

---

## 17. Edge Cases and Obscure Errors

### 17.1 The "Exec Format Error"

**Error:** `standard_init_linux.go:228: exec user process caused: exec format error`
**Cause:** You are trying to run an image built for a different CPU architecture (e.g., running an ARM64 image on an AMD64 host).
**Solution:** Use Docker Buildx to build multi-platform images, or pull the correct architecture tag.

### 17.2 The "Context Deadline Exceeded"

**Error:** `context deadline exceeded` during `docker pull` or `docker build`.
**Cause:** Network timeout communicating with the registry or the Docker daemon.
**Solution:** Check network connectivity, increase the daemon timeout settings, or check if the registry is rate-limiting you.

### 17.3 Inotify Limits Exhausted

**Error:** `ENOSPC: System limit for number of file watchers reached` (common in Node.js/React development).
**Cause:** The host OS has a limit on how many files can be watched for changes (inotify). Containers share this limit with the host.
**Solution:** Increase the limit on the host OS:
```bash
echo fs.inotify.max_user_watches=524288 | sudo tee -a /etc/sysctl.conf && sudo sysctl -p
```

---

## 18. Final Thoughts on Docker Mastery

Becoming a Docker Super Specialist is an ongoing journey. The container ecosystem evolves rapidly. Stay updated with the latest OCI specifications, containerd releases, and Linux kernel networking features. Always prioritize security, enforce resource limits, and build observability into every layer of your containerized infrastructure. By mastering the internals detailed in this document, you are equipped to handle the most demanding production environments.

## === FILE: 49-docker-security-audit.md ===
# Docker Super Specialist: Complete Security Audit Checklist & Hardening Guide

## Introduction

Welcome to the definitive guide for securing, optimizing, and troubleshooting Docker environments. As the Docker Super Specialist, this document serves as your comprehensive manual for conducting exhaustive security audits, implementing flaw-proof configurations, and resolving complex operational issues. This guide is designed for tech support operations teams, DevOps engineers, and system administrators who are responsible for maintaining production-grade containerized infrastructure.

The container ecosystem has evolved rapidly, and with it, the threat landscape. A single misconfiguration in a Dockerfile or a `compose.yaml` file can expose your entire infrastructure to catastrophic breaches. This guide goes beyond basic best practices; it provides deep, actionable insights, real-world configuration examples, and a meticulous 50+ item security audit checklist. We will cover every layer of the container lifecycle: from image selection and build processes to runtime execution, network isolation, and incident response.

By following this guide, you will transform vulnerable, inefficient Docker setups into fortified, high-performance environments that comply with stringent industry standards such as the CIS Docker Benchmark, NIST 800-190, PCI-DSS, and SOC2.

---

## 1. Image Security: The Foundation of Container Trust

The security of your containerized application begins long before it runs; it starts with the base image. A compromised or bloated base image introduces vulnerabilities that cannot be mitigated at runtime.

### 1.1 Base Image Selection

Choosing the right base image is critical. The goal is to minimize the attack surface by reducing the number of installed packages and utilities.

**Distroless Images:**
Distroless images, pioneered by Google, contain only your application and its runtime dependencies. They do not contain package managers, shells, or any other programs you would expect to find in a standard Linux distribution. This makes them incredibly secure.

*Before (Vulnerable):*
```dockerfile
FROM node:18
WORKDIR /app
COPY . .
RUN npm install
CMD ["node", "server.js"]
```

*After (Secure with Distroless):*
```dockerfile
# Build stage
FROM node:18 AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .

# Runtime stage
FROM gcr.io/distroless/nodejs18-debian11
WORKDIR /app
COPY --from=build /app /app
CMD ["server.js"]
```

**Scratch Images:**
For statically compiled languages like Go or Rust, the `scratch` image is the ultimate choice. It is an explicitly empty image.

```dockerfile
# Build stage
FROM golang:1.20 AS builder
WORKDIR /app
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o main .

# Runtime stage
FROM scratch
COPY --from=builder /app/main /main
ENTRYPOINT ["/main"]
```

**Alpine Linux:**
Alpine is a popular choice due to its small size (~5MB). However, it uses `musl` libc instead of `glibc`, which can cause compatibility issues with some applications (e.g., Python wheels compiled for glibc). If you use Alpine, ensure you pin the version and scan it regularly.

### 1.2 Vulnerability Scanning

Continuous vulnerability scanning is non-negotiable. You must integrate scanning into your CI/CD pipeline and regularly scan images in your registry.

**Tools:**
- **Docker Scout:** Integrated directly into Docker Desktop and CLI.
- **Trivy (Aqua Security):** A comprehensive, easy-to-use scanner for containers and other artifacts.
- **Grype (Anchore):** A vulnerability scanner for container images and filesystems.
- **Snyk:** A developer-first security platform.

*Real Command Example (Trivy):*
```bash
# Scan a local image and fail the build if critical vulnerabilities are found
trivy image --severity CRITICAL --exit-code 1 YOUR_REGISTRY/YOUR_IMAGE:TAG
```

*Real Error Message & Solution:*
**Error:** `Trivy found 3 CRITICAL vulnerabilities in base image ubuntu:20.04`
**Solution:** Update the base image to a newer patch version (e.g., `ubuntu:22.04`) or switch to a minimal image like Alpine or Distroless. If the vulnerability is in an application dependency, update the dependency in your `package.json` or `requirements.txt`.

### 1.3 Image Signing and Provenance

How do you know the image you are pulling is the one you built? Image signing ensures integrity and authenticity.

**Docker Content Trust (DCT):**
DCT uses Notary to sign images. When enabled, Docker will only pull signed images.

```bash
# Enable DCT
export DOCKER_CONTENT_TRUST=1
# Pulling an unsigned image will now fail
docker pull YOUR_REGISTRY/unsigned-image:latest
# Error: Error: remote trust data does not exist...
```

**Cosign (Sigstore):**
Cosign is a modern, keyless signing tool that is becoming the industry standard.

```bash
# Generate a keypair
cosign generate-key-pair

# Sign an image
cosign sign --key cosign.key YOUR_REGISTRY/YOUR_IMAGE:TAG

# Verify an image
cosign verify --key cosign.pub YOUR_REGISTRY/YOUR_IMAGE:TAG
```

### 1.4 SBOM Generation

A Software Bill of Materials (SBOM) is a nested inventory of all components, libraries, and modules required to build a given piece of software. It is essential for supply chain security.

*Real Command Example (Syft):*
```bash
# Generate an SBOM in SPDX format
syft YOUR_REGISTRY/YOUR_IMAGE:TAG -o spdx-json > sbom.json
```

### 1.5 Pinning Versions with SHA256 Digests

Tags like `:latest` or even `:1.0` are mutable; they can be overwritten. To guarantee you are pulling the exact same image every time, use the SHA256 digest.

*Before (Mutable):*
```dockerfile
FROM nginx:1.25
```

*After (Immutable):*
```dockerfile
FROM nginx@sha256:af296b188c7b7df99ba960ca614439c99cb7cf252ed7bbc23e90cfda59092305
```

---

## 2. Dockerfile Security: Hardening the Build Process

The Dockerfile is the blueprint for your image. Insecure directives here will result in an insecure container.

### 2.1 The USER Directive

By default, Docker containers run as `root`. This is a massive security risk. If an attacker breaks out of the container, they will have root access to the host (unless user namespaces are configured).

**Rule:** Always specify a non-root user. Use a numeric UID to ensure Kubernetes and other orchestrators can verify the user without needing to parse the `/etc/passwd` file inside the container.

*Before (Runs as root):*
```dockerfile
FROM ubuntu:22.04
COPY app /app
CMD ["/app/start.sh"]
```

*After (Runs as non-root):*
```dockerfile
FROM ubuntu:22.04
RUN groupadd -r appgroup && useradd -r -g appgroup -u 10001 appuser
COPY --chown=appuser:appgroup app /app
USER 10001
CMD ["/app/start.sh"]
```

### 2.2 COPY vs. ADD

The `ADD` instruction has hidden features: it can download files from URLs and automatically extract tar archives. This unpredictability is a security risk.

**Rule:** Always use `COPY` unless you specifically need the extraction feature of `ADD`.

*Before (Insecure):*
```dockerfile
ADD https://example.com/malicious-script.sh /usr/local/bin/
```

*After (Secure):*
```dockerfile
# Download explicitly and verify checksum
RUN curl -sSL https://example.com/safe-script.sh -o /usr/local/bin/safe-script.sh     && echo "EXPECTED_SHA256  /usr/local/bin/safe-script.sh" | sha256sum -c -     && chmod +x /usr/local/bin/safe-script.sh
```

### 2.3 Avoiding curl | bash Patterns

Piping `curl` directly into `bash` is a classic security anti-pattern. It executes arbitrary code from the internet without verification.

*Before (Dangerous):*
```dockerfile
RUN curl -sL https://deb.nodesource.com/setup_18.x | bash -
```

*After (Safer):*
```dockerfile
# Download, verify, then execute
RUN curl -sL -o setup.sh https://deb.nodesource.com/setup_18.x     && echo "EXPECTED_SHA256  setup.sh" | sha256sum -c -     && bash setup.sh     && rm setup.sh
```

### 2.4 Minimal Packages and Cache Removal

Every installed package increases the attack surface. Furthermore, package manager caches bloat the image size and can contain stale data.

**Rule:** Install only what is necessary, use `--no-install-recommends` (for apt), and clean the cache in the *same* `RUN` layer.

*Before (Bloated):*
```dockerfile
RUN apt-get update
RUN apt-get install -y python3
```

*After (Optimized and Secure):*
```dockerfile
RUN apt-get update && apt-get install -y --no-install-recommends     python3     && rm -rf /var/lib/apt/lists/*
```

### 2.5 Removing SUID/SGID Binaries

SUID (Set owner User ID up on execution) and SGID (Set Group ID up on execution) binaries allow users to execute a file with the permissions of the file owner or group. This is a common privilege escalation vector.

**Rule:** Find and remove SUID/SGID bits from binaries that don't need them.

```dockerfile
# Remove SUID/SGID bits from all files
RUN find / -xdev -perm /6000 -type f -exec chmod a-s {} \; || true
```

---

## 3. Runtime Security: Confining the Container

Even with a secure image, the runtime environment must be locked down to prevent container breakouts and resource exhaustion.

### 3.1 Read-Only Root Filesystem

A compromised container often attempts to download malware or modify configuration files. By mounting the root filesystem as read-only, you block these actions.

**Rule:** Set `read_only: true` in your `compose.yaml`. Use `tmpfs` for directories that require write access (e.g., `/tmp`, `/var/run`).

*compose.yaml Example:*
```yaml
services:
  webapp:
    image: YOUR_REGISTRY/webapp:v1.2.3
    read_only: true
    tmpfs:
      - /tmp
      - /var/run
```

### 3.2 Linux Capabilities (cap_drop and cap_add)

By default, Docker drops many Linux capabilities but retains a subset (e.g., `CAP_CHOWN`, `CAP_NET_BIND_SERVICE`). Most applications do not need even these.

**Rule:** Drop ALL capabilities, and explicitly add back only the ones strictly required.

*compose.yaml Example:*
```yaml
services:
  webapp:
    image: YOUR_REGISTRY/webapp:v1.2.3
    cap_drop:
      - ALL
    cap_add:
      - NET_BIND_SERVICE # Only if binding to ports < 1024
```

### 3.3 No New Privileges

The `no-new-privileges` flag prevents a process from gaining new privileges through `execve`. This mitigates SUID binary attacks.

*compose.yaml Example:*
```yaml
services:
  webapp:
    image: YOUR_REGISTRY/webapp:v1.2.3
    security_opt:
      - no-new-privileges:true
```

### 3.4 Seccomp and AppArmor Profiles

**Seccomp (Secure Computing Mode):** Restricts the system calls a container can make. Docker applies a default seccomp profile that blocks ~44 system calls. You can create custom profiles for stricter control.

**AppArmor:** A Linux kernel security module that restricts programs' capabilities with per-program profiles.

*compose.yaml Example:*
```yaml
services:
  webapp:
    image: YOUR_REGISTRY/webapp:v1.2.3
    security_opt:
      - seccomp=/path/to/custom-profile.json
      - apparmor=docker-default
```

### 3.5 Resource Limits (Cgroups)

Without resource limits, a single compromised or buggy container can consume all host resources (CPU, memory), causing a Denial of Service (DoS) for all other containers.

**Rule:** Always set memory and CPU limits.

*compose.yaml Example:*
```yaml
services:
  webapp:
    image: YOUR_REGISTRY/webapp:v1.2.3
    deploy:
      resources:
        limits:
          cpus: '0.50'
          memory: 512M
        reservations:
          cpus: '0.25'
          memory: 256M
```

*Real Error Message & Solution:*
**Error:** Container exits unexpectedly with status code 137.
**Solution:** Status 137 indicates the container was killed by the OOM (Out of Memory) killer. Check the host logs (`dmesg -T | grep -i oom`). Increase the memory limit in `compose.yaml` or optimize the application's memory usage.

### 3.6 No Privileged Mode and Host Namespaces

**Rule:** NEVER use `privileged: true` in production. It gives the container almost full access to the host.
**Rule:** NEVER share host namespaces (`network_mode: host`, `pid: host`, `ipc: host`) unless absolutely necessary for specific infrastructure tools, and even then, proceed with extreme caution.

---

## 4. Network Security: Isolating Communications

Network segmentation is crucial for limiting the blast radius of a compromise.

### 4.1 Internal Networks

Backend services (databases, caches) should never be exposed to the public internet or even the default bridge network.

*compose.yaml Example:*
```yaml
services:
  frontend:
    image: YOUR_REGISTRY/frontend:v1
    ports:
      - "443:443"
    networks:
      - public_net
      - private_net

  database:
    image: postgres:15
    networks:
      - private_net
    # No ports exposed!

networks:
  public_net:
  private_net:
    internal: true # Completely isolated from external networks
```

### 4.2 Encrypted Overlay Networks (Swarm)

If using Docker Swarm, ensure overlay networks are encrypted to protect data in transit between nodes.

```bash
docker network create --opt encrypted --driver overlay my-secure-network
```

### 4.3 TLS for All Service Communication

Even within internal networks, implement mutual TLS (mTLS) between services. This ensures that even if an attacker breaches the internal network, they cannot intercept or spoof traffic. Tools like Istio or Linkerd (in Kubernetes) or Traefik (in Docker) can manage this.

---

## 5. Secrets Management: Protecting Sensitive Data

Hardcoding secrets in Dockerfiles, environment variables, or source code is a critical vulnerability.

### 5.1 Docker Secrets (Swarm) and Compose Secrets

Docker provides a native secrets management mechanism. Secrets are mounted as in-memory files (tmpfs) at `/run/secrets/` and are never stored on disk.

*compose.yaml Example:*
```yaml
services:
  database:
    image: postgres:15
    environment:
      POSTGRES_PASSWORD_FILE: /run/secrets/db_password
    secrets:
      - db_password

secrets:
  db_password:
    file: ./secrets/db_password.txt # Ensure this file has strict permissions (chmod 600)
```

### 5.2 External Secret Managers

For enterprise environments, integrate with external secret managers like HashiCorp Vault, AWS Secrets Manager, or Azure Key Vault. Do not pass secrets as environment variables; instead, have the application fetch them at runtime or use an init container to populate a shared volume.

### 5.3 The Danger of ENV and Build Args

**Rule:** NEVER use `ENV` or `ARG` for secrets in a Dockerfile. They are baked into the image layers and can be easily extracted using `docker history`.

*Before (Insecure):*
```dockerfile
ARG API_KEY
ENV API_KEY=$API_KEY
```

*After (Secure - using BuildKit secrets):*
```dockerfile
# syntax=docker/dockerfile:1
FROM alpine
RUN --mount=type=secret,id=mysecret cat /run/secrets/mysecret > /app/config
```
Build command: `docker build --secret id=mysecret,src=mysecret.txt .`

---

## 6. Supply Chain Security: Securing the Pipeline

The software supply chain is a prime target. You must secure every step from code commit to container deployment.

### 6.1 Trusted Base Images and Registries

Only pull images from trusted, verified registries. Implement Role-Based Access Control (RBAC) on your private registries to restrict who can push images.

### 6.2 Build Provenance Attestations

Use Docker Buildx to generate provenance attestations. This provides a verifiable record of how an image was built, including the source code repository, commit SHA, and build environment.

```bash
docker buildx build --provenance=true --sbom=true -t YOUR_REGISTRY/YOUR_IMAGE:TAG .
```

### 6.3 CI/CD Pipeline Security

- **Least Privilege:** CI/CD runners should have minimal permissions.
- **Ephemeral Runners:** Use ephemeral runners that are destroyed after each build.
- **Secret Scanning:** Implement tools like GitGuardian or TruffleHog to scan repositories for accidentally committed secrets.

---

## 7. Docker Daemon Security: Protecting the Engine

The Docker daemon runs as root. Securing it is paramount.

### 7.1 TLS for Remote Access

If you must expose the Docker daemon API over a network, ALWAYS use mutual TLS.

```bash
dockerd --tlsverify --tlscacert=ca.pem --tlscert=server-cert.pem --tlskey=server-key.pem -H=0.0.0.0:2376
```

### 7.2 Rootless Mode

Rootless mode allows running the Docker daemon and containers as a non-root user. This drastically reduces the impact of a daemon vulnerability.

*Installation:*
```bash
dockerd-rootless-setuptool.sh install
```

### 7.3 User Namespaces

If rootless mode is not feasible, enable user namespaces. This maps the `root` user inside the container to a non-privileged user on the host.

*daemon.json:*
```json
{
  "userns-remap": "default"
}
```

### 7.4 Audit Logging

Configure the host's audit daemon (`auditd`) to monitor Docker files and directories.

*/etc/audit/rules.d/docker.rules:*
```text
-w /usr/bin/dockerd -k docker
-w /var/lib/docker -k docker
-w /etc/docker -k docker
-w /lib/systemd/system/docker.service -k docker
-w /lib/systemd/system/docker.socket -k docker
-w /etc/default/docker -k docker
-w /etc/docker/daemon.json -k docker
-w /usr/bin/docker-containerd -k docker
-w /usr/bin/docker-runc -k docker
```

---

## 8. Compliance Frameworks

Adhering to established frameworks provides a structured approach to security.

### 8.1 CIS Docker Benchmark

The Center for Internet Security (CIS) provides the gold standard for Docker security. It covers 7 sections:
1. Host Configuration
2. Docker Daemon Configuration
3. Docker Daemon Configuration Files
4. Container Images and Build File
5. Container Runtime
6. Docker Security Operations
7. Docker Swarm Configuration

**Tool:** Use `docker-bench-security` to automate the audit.
```bash
git clone https://github.com/docker/docker-bench-security.git
cd docker-bench-security
sudo sh docker-bench-security.sh
```

### 8.2 NIST 800-190

The National Institute of Standards and Technology (NIST) Special Publication 800-190 provides an Application Container Security Guide. Key areas include:
- Image vulnerabilities
- Registry access
- Orchestrator security
- Container isolation

### 8.3 PCI-DSS and SOC2

For environments handling credit card data (PCI-DSS) or requiring strict operational controls (SOC2), container security must include:
- Strict network segmentation (CDE isolation).
- Comprehensive logging and monitoring.
- Regular vulnerability scanning and penetration testing.
- Strict access controls (RBAC).

---

## 9. Complete Security Audit Checklist

This checklist is designed for tech support operations teams to evaluate client environments.

### Category 1: Host & Daemon Configuration
| ID | Check | Pass Criteria | Fail Criteria |
|---|---|---|---|
| 1.1 | Docker Daemon Auditing | `auditd` rules exist for `/var/lib/docker`, `/etc/docker`, etc. | No audit rules configured. |
| 1.2 | Rootless Mode / User Namespaces | Daemon runs rootless OR `userns-remap` is enabled. | Daemon runs as root without user namespaces. |
| 1.3 | Remote API TLS | Remote API (if enabled) requires mTLS. | API exposed on port 2375 without TLS. |
| 1.4 | Authorization Plugin | AuthZ plugin (e.g., OPA) is configured. | No authorization plugin used. |
| 1.5 | Daemon Log Level | Log level is set to `info` or higher. | Log level is `debug` in production. |

### Category 2: Image & Build Security
| ID | Check | Pass Criteria | Fail Criteria |
|---|---|---|---|
| 2.1 | Base Image Selection | Minimal images (Distroless, Scratch, Alpine) used. | Full OS images (Ubuntu, Debian) used unnecessarily. |
| 2.2 | Vulnerability Scanning | Automated scanning in CI/CD; 0 critical/high vulns. | No scanning; known vulnerabilities exist. |
| 2.3 | Image Signing | Docker Content Trust or Cosign enforced. | Unsigned images are allowed in production. |
| 2.4 | Multi-stage Builds | Build tools excluded from final runtime image. | Compilers and build tools present in runtime image. |
| 2.5 | Immutable Tags | Images referenced by SHA256 digest. | Images referenced by `:latest` or mutable tags. |
| 2.6 | Secrets in Dockerfile | No `ENV` or `ARG` used for secrets. | Passwords/keys found in Dockerfile or image history. |
| 2.7 | USER Directive | Non-root numeric UID specified in Dockerfile. | Container runs as root (UID 0). |
| 2.8 | COPY vs ADD | `COPY` used exclusively (unless tar extraction needed). | `ADD` used to fetch remote resources. |
| 2.9 | SUID/SGID Binaries | Unnecessary SUID/SGID bits removed. | SUID binaries present and accessible. |

### Category 3: Runtime Security
| ID | Check | Pass Criteria | Fail Criteria |
|---|---|---|---|
| 3.1 | Read-Only Root FS | `read_only: true` set for all applicable containers. | Root filesystem is writable. |
| 3.2 | Capabilities | `cap_drop: ALL` used; minimal `cap_add`. | Default capabilities retained or `cap_add: ALL`. |
| 3.3 | No New Privileges | `security_opt: no-new-privileges:true` applied. | Flag is missing. |
| 3.4 | Seccomp/AppArmor | Custom or default profiles applied. | Profiles explicitly disabled (`unconfined`). |
| 3.5 | Resource Limits | CPU and Memory limits/reservations defined. | No resource limits set (unbounded consumption). |
| 3.6 | Privileged Mode | `privileged: true` is NOT used. | Container runs in privileged mode. |
| 3.7 | Host Namespaces | `network_mode: host`, `pid: host`, `ipc: host` NOT used. | Container shares host namespaces. |
| 3.8 | Healthchecks | `healthcheck` defined for all services. | No healthchecks configured. |
| 3.9 | Restart Policies | `unless-stopped` or `on-failure` configured. | No restart policy or `always` used inappropriately. |

### Category 4: Network & Data Security
| ID | Check | Pass Criteria | Fail Criteria |
|---|---|---|---|
| 4.1 | Internal Networks | Backend services on `internal: true` networks. | Databases exposed to default bridge or host. |
| 4.2 | Port Mapping | Only necessary ports exposed; bound to specific IPs. | Ports bound to `0.0.0.0` unnecessarily. |
| 4.3 | Secrets Management | Docker Secrets or external manager used. | Secrets passed via environment variables. |
| 4.4 | Volume Mounts | Bind mounts restricted; named volumes preferred. | Sensitive host directories mounted into container. |

*(Note: A full audit would expand this to 50+ detailed checks based on the CIS Benchmark).*

---

## 10. Incident Response: Handling Compromised Containers

When a breach occurs, rapid and structured response is critical.

### 10.1 Isolation

Do NOT stop or kill the container immediately. This destroys volatile evidence in memory.

**Step 1: Isolate from the network.**
Disconnect the container from all networks to stop data exfiltration and command-and-control (C2) communication.
```bash
docker network disconnect <network_name> <container_name>
```

**Step 2: Pause the container.**
Freeze the container's processes.
```bash
docker pause <container_name>
```

### 10.2 Forensic Image Capture

Capture the state of the container for analysis.

**Step 1: Commit the container to an image.**
```bash
docker commit <container_name> forensic-image:<container_name>-<timestamp>
```

**Step 2: Export the filesystem.**
```bash
docker export <container_name> > forensic-fs-<timestamp>.tar
```

**Step 3: Capture memory (Advanced).**
Use tools like LiME or Volatility on the host to capture the memory space of the container's cgroup.

### 10.3 Log Preservation

Collect all relevant logs immediately.

```bash
# Container logs
docker logs <container_name> > container-<timestamp>.log

# Docker daemon logs
journalctl -u docker > dockerd-<timestamp>.log

# Host audit logs
cp /var/log/audit/audit.log audit-<timestamp>.log
```

### 10.4 Eradication and Recovery

Once evidence is secured:
1. Kill and remove the compromised container (`docker kill`, `docker rm`).
2. Identify the root cause (e.g., vulnerable dependency, leaked secret).
3. Patch the vulnerability in the source code/Dockerfile.
4. Rebuild the image and deploy the updated version.
5. Rotate all secrets that were accessible to the compromised container.

---

## Conclusion

Securing a Docker environment is not a one-time task; it is a continuous process of auditing, hardening, and monitoring. By implementing the strategies outlined in this Super Specialist guide—from minimal base images and strict runtime constraints to robust secrets management and incident response protocols—you can build resilient, production-ready container infrastructure that withstands modern threats.

## References
[1] CIS Docker Benchmark v1.6.0
[2] NIST Special Publication 800-190: Application Container Security Guide
[3] Docker Documentation: Security


---

## 11. Advanced Troubleshooting Scenarios

As a Super Specialist, you will encounter complex issues that go beyond basic misconfigurations. Here are deep dives into common production incidents.

### Scenario A: The "Zombie" Container (High CPU, Unresponsive)

**Symptoms:** A container is consuming 100% CPU but is not responding to health checks or network requests. `docker stop` hangs indefinitely.

**Diagnosis:**
1. Identify the container PID on the host:
   ```bash
   docker inspect --format '{{.State.Pid}}' <container_name>
   ```
2. Check the process tree on the host:
   ```bash
   ps -ef | grep <PID>
   ```
3. Use `strace` to see what the process is doing (requires root on host):
   ```bash
   strace -p <PID>
   ```
   *Result:* You might see it stuck in an infinite loop of failing system calls or deadlocked waiting for a resource.

**Resolution:**
1. If `docker stop` fails, the daemon sends a SIGTERM. If the app ignores it, it waits for the grace period (default 10s) then sends SIGKILL.
2. If it's completely wedged, force kill it from the host:
   ```bash
   kill -9 <PID>
   ```
3. **Prevention:** Ensure the application handles SIGTERM correctly. Use `init: true` in `compose.yaml` to run an init process (like `tini`) that reaps zombie processes and forwards signals properly.

*compose.yaml Example:*
```yaml
services:
  app:
    image: YOUR_REGISTRY/app:v1
    init: true
    stop_grace_period: 30s
```

### Scenario B: Intermittent DNS Resolution Failures

**Symptoms:** Containers randomly fail to resolve external hostnames or internal service names. Logs show `Temporary failure in name resolution`.

**Diagnosis:**
1. Check the container's DNS configuration:
   ```bash
   docker exec <container_name> cat /etc/resolv.conf
   ```
   *Note:* Docker uses an embedded DNS server at `127.0.0.11` for user-defined networks.
2. Check host DNS resolution and firewall rules. Sometimes, aggressive firewall rules drop UDP DNS packets.
3. Monitor DNS traffic using `tcpdump` on the Docker bridge interface.

**Resolution:**
1. If the host's DNS is unstable, explicitly define reliable DNS servers in `compose.yaml` or `daemon.json`.
2. Ensure the `ndots` option in `/etc/resolv.conf` isn't causing excessive DNS queries (common in Kubernetes, but can happen in complex Compose setups).

*compose.yaml Example:*
```yaml
services:
  app:
    image: YOUR_REGISTRY/app:v1
    dns:
      - 8.8.8.8
      - 1.1.1.1
    dns_opt:
      - ndots:1
```

### Scenario C: Overlay2 Storage Driver Exhaustion

**Symptoms:** Host disk space is full. `docker system df` shows massive space used by images or local volumes. `docker system prune` doesn't free enough space.

**Diagnosis:**
1. Find the largest directories in the Docker root:
   ```bash
   sudo du -sh /var/lib/docker/* | sort -h
   ```
2. If `/var/lib/docker/overlay2` is huge, you have orphaned layers or containers writing massive amounts of data to their writable layer instead of a volume.
3. Identify containers with large writable layers:
   ```bash
   docker ps -s
   ```

**Resolution:**
1. **Immediate fix:** Stop containers and run a deep prune:
   ```bash
   docker system prune -a --volumes
   ```
2. **Root Cause Fix:** Ensure applications write logs to `stdout`/`stderr` (handled by Docker logging driver) or to mounted volumes, NEVER to the container filesystem.
3. Configure log rotation in `compose.yaml` to prevent log files from filling the disk.

*compose.yaml Example:*
```yaml
services:
  app:
    image: YOUR_REGISTRY/app:v1
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

---

## 12. Cost and Time Optimization Strategies

Efficiency is just as important as security. Bloated images and inefficient builds waste CI/CD minutes, bandwidth, and storage costs.

### 12.1 Layer Caching Optimization

Docker builds images layer by layer. If a layer changes, all subsequent layers must be rebuilt.

**Rule:** Order your Dockerfile instructions from least frequently changed to most frequently changed.

*Before (Inefficient):*
```dockerfile
FROM node:18
WORKDIR /app
COPY . .
# If ANY file in the repo changes, npm install runs again!
RUN npm install
CMD ["npm", "start"]
```

*After (Optimized):*
```dockerfile
FROM node:18
WORKDIR /app
# Copy only package files first
COPY package*.json ./
# This layer is cached unless package.json changes
RUN npm ci
# Now copy the rest of the code
COPY . .
CMD ["npm", "start"]
```

### 12.2 BuildKit Cache Mounts

For languages that use package managers (npm, pip, apt), downloading dependencies repeatedly is a massive time sink. BuildKit cache mounts solve this.

*Dockerfile Example (Python):*
```dockerfile
# syntax=docker/dockerfile:1
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
# Cache the pip download directory
RUN --mount=type=cache,target=/root/.cache/pip     pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

### 12.3 Compose Profiles for Local Development

Running a full microservices stack locally can melt a developer's laptop. Use Compose profiles to group services.

*compose.yaml Example:*
```yaml
services:
  frontend:
    image: my-frontend
    profiles: ["ui", "full"]
  backend-api:
    image: my-api
    profiles: ["api", "full"]
  database:
    image: postgres
    profiles: ["api", "full", "db-only"]
```
*Usage:* `docker compose --profile api up -d` (Starts only backend-api and database).

### 12.4 Docker Compose Watch (Hot Reloading)

Introduced in Compose V2.22.0, `watch` automatically updates running services as you edit code, eliminating the need to manually rebuild images during development.

*compose.yaml Example:*
```yaml
services:
  web:
    build: .
    command: npm run dev
    develop:
      watch:
        - action: sync
          path: ./src
          target: /app/src
        - action: rebuild
          path: package.json
```
*Usage:* `docker compose watch`

---

## 13. Comprehensive Upgrade Strategies

Upgrading containerized applications in production requires careful planning to avoid downtime.

### 13.1 Rolling Updates (Swarm)

Docker Swarm natively supports rolling updates, updating a specified number of replicas at a time.

*compose.yaml Example:*
```yaml
services:
  web:
    image: YOUR_REGISTRY/web:v2
    deploy:
      replicas: 4
      update_config:
        parallelism: 1
        delay: 10s
        order: start-first # Start new container before stopping old one
        failure_action: rollback
```

### 13.2 Blue-Green Deployments (Compose)

In a standard Docker Compose environment, you can simulate blue-green deployments using a reverse proxy (like Traefik or Nginx).

1. Run `web-blue` (v1) and route traffic to it via the proxy.
2. Deploy `web-green` (v2) alongside it.
3. Update the proxy configuration to route traffic to `web-green`.
4. Monitor for errors. If successful, tear down `web-blue`.

### 13.3 Database Migrations

Never run database migrations automatically on container startup in a multi-replica environment (race conditions).

**Best Practice:** Run migrations as a separate, short-lived container (a Kubernetes Job or a specific Compose profile) *before* updating the application containers.

```bash
# Run migration
docker compose run --rm app-migration
# If successful, update the app
docker compose up -d app
```

---

## 14. Extended Security Audit Checklist (Continued)

### Category 5: Secrets & Configuration
| ID | Check | Pass Criteria | Fail Criteria |
|---|---|---|---|
| 5.1 | Hardcoded Secrets | Source code and configs scanned; no secrets found. | API keys/passwords found in plaintext. |
| 5.2 | Environment Variables | `.env` files excluded from version control (`.gitignore`). | `.env` committed to repository. |
| 5.3 | Secret Permissions | Mounted secret files have strict permissions (e.g., 400). | Secrets readable by all users. |

### Category 6: Supply Chain & CI/CD
| ID | Check | Pass Criteria | Fail Criteria |
|---|---|---|---|
| 6.1 | Registry Access | RBAC implemented; pull-only access for production nodes. | Anonymous pull/push allowed. |
| 6.2 | SBOM Generation | SBOM generated and archived for every release. | No software bill of materials exists. |
| 6.3 | Base Image Provenance | Base images sourced from official, verified publishers. | Base images pulled from unknown personal repositories. |

### Category 7: Monitoring & Logging
| ID | Check | Pass Criteria | Fail Criteria |
|---|---|---|---|
| 7.1 | Centralized Logging | Container logs forwarded to a central SIEM/Log aggregator. | Logs only stored locally on the host. |
| 7.2 | Alerting | Alerts configured for container crashes (OOM, exit code != 0). | No proactive alerting in place. |
| 7.3 | Performance Monitoring | Metrics (CPU, Mem, Net) collected via Prometheus/cAdvisor. | No visibility into container resource usage. |

---
## Final Thoughts for the Operations Team

As a Docker Super Specialist, your role is to bridge the gap between development velocity and operational stability. Security is not a roadblock; it is a fundamental property of a well-engineered system. By enforcing these strict guidelines, utilizing the provided configurations, and understanding the deep mechanics of the Docker engine, you will ensure that your clients' infrastructure remains robust, performant, and impenetrable.


# Docker Super Specialist: Complete Security Audit Checklist & Hardening Guide

## Introduction

Welcome to the definitive guide for securing, optimizing, and troubleshooting Docker environments. As the Docker Super Specialist, this document serves as your comprehensive manual for conducting exhaustive security audits, implementing flaw-proof configurations, and resolving complex operational issues. This guide is designed for tech support operations teams, DevOps engineers, and system administrators who are responsible for maintaining production-grade containerized infrastructure.

The container ecosystem has evolved rapidly, and with it, the threat landscape. A single misconfiguration in a Dockerfile or a `compose.yaml` file can expose your entire infrastructure to catastrophic breaches. This guide goes beyond basic best practices; it provides deep, actionable insights, real-world configuration examples, and a meticulous 50+ item security audit checklist. We will cover every layer of the container lifecycle: from image selection and build processes to runtime execution, network isolation, and incident response.

By following this guide, you will transform vulnerable, inefficient Docker setups into fortified, high-performance environments that comply with stringent industry standards such as the CIS Docker Benchmark, NIST 800-190, PCI-DSS, and SOC2.

---

## 1. Image Security: The Foundation of Container Trust

The security of your containerized application begins long before it runs; it starts with the base image. A compromised or bloated base image introduces vulnerabilities that cannot be mitigated at runtime.

### 1.1 Base Image Selection

Choosing the right base image is critical. The goal is to minimize the attack surface by reducing the number of installed packages and utilities.

**Distroless Images:**
Distroless images, pioneered by Google, contain only your application and its runtime dependencies. They do not contain package managers, shells, or any other programs you would expect to find in a standard Linux distribution. This makes them incredibly secure.

*Before (Vulnerable):*
```dockerfile
FROM node:18
WORKDIR /app
COPY . .
RUN npm install
CMD ["node", "server.js"]
```

*After (Secure with Distroless):*
```dockerfile
# Build stage
FROM node:18 AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .

# Runtime stage
FROM gcr.io/distroless/nodejs18-debian11
WORKDIR /app
COPY --from=build /app /app
CMD ["server.js"]
```

**Scratch Images:**
For statically compiled languages like Go or Rust, the `scratch` image is the ultimate choice. It is an explicitly empty image.

```dockerfile
# Build stage
FROM golang:1.20 AS builder
WORKDIR /app
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o main .

# Runtime stage
FROM scratch
COPY --from=builder /app/main /main
ENTRYPOINT ["/main"]
```

**Alpine Linux:**
Alpine is a popular choice due to its small size (~5MB). However, it uses `musl` libc instead of `glibc`, which can cause compatibility issues with some applications (e.g., Python wheels compiled for glibc). If you use Alpine, ensure you pin the version and scan it regularly.

### 1.2 Vulnerability Scanning

Continuous vulnerability scanning is non-negotiable. You must integrate scanning into your CI/CD pipeline and regularly scan images in your registry.

**Tools:**
- **Docker Scout:** Integrated directly into Docker Desktop and CLI.
- **Trivy (Aqua Security):** A comprehensive, easy-to-use scanner for containers and other artifacts.
- **Grype (Anchore):** A vulnerability scanner for container images and filesystems.
- **Snyk:** A developer-first security platform.

*Real Command Example (Trivy):*
```bash
# Scan a local image and fail the build if critical vulnerabilities are found
trivy image --severity CRITICAL --exit-code 1 YOUR_REGISTRY/YOUR_IMAGE:TAG
```

*Real Error Message & Solution:*
**Error:** `Trivy found 3 CRITICAL vulnerabilities in base image ubuntu:20.04`
**Solution:** Update the base image to a newer patch version (e.g., `ubuntu:22.04`) or switch to a minimal image like Alpine or Distroless. If the vulnerability is in an application dependency, update the dependency in your `package.json` or `requirements.txt`.

### 1.3 Image Signing and Provenance

How do you know the image you are pulling is the one you built? Image signing ensures integrity and authenticity.

**Docker Content Trust (DCT):**
DCT uses Notary to sign images. When enabled, Docker will only pull signed images.

```bash
# Enable DCT
export DOCKER_CONTENT_TRUST=1
# Pulling an unsigned image will now fail
docker pull YOUR_REGISTRY/unsigned-image:latest
# Error: Error: remote trust data does not exist...
```

**Cosign (Sigstore):**
Cosign is a modern, keyless signing tool that is becoming the industry standard.

```bash
# Generate a keypair
cosign generate-key-pair

# Sign an image
cosign sign --key cosign.key YOUR_REGISTRY/YOUR_IMAGE:TAG

# Verify an image
cosign verify --key cosign.pub YOUR_REGISTRY/YOUR_IMAGE:TAG
```

### 1.4 SBOM Generation

A Software Bill of Materials (SBOM) is a nested inventory of all components, libraries, and modules required to build a given piece of software. It is essential for supply chain security.

*Real Command Example (Syft):*
```bash
# Generate an SBOM in SPDX format
syft YOUR_REGISTRY/YOUR_IMAGE:TAG -o spdx-json > sbom.json
```

### 1.5 Pinning Versions with SHA256 Digests

Tags like `:latest` or even `:1.0` are mutable; they can be overwritten. To guarantee you are pulling the exact same image every time, use the SHA256 digest.

*Before (Mutable):*
```dockerfile
FROM nginx:1.25
```

*After (Immutable):*
```dockerfile
FROM nginx@sha256:af296b188c7b7df99ba960ca614439c99cb7cf252ed7bbc23e90cfda59092305
```

---

## 2. Dockerfile Security: Hardening the Build Process

The Dockerfile is the blueprint for your image. Insecure directives here will result in an insecure container.

### 2.1 The USER Directive

By default, Docker containers run as `root`. This is a massive security risk. If an attacker breaks out of the container, they will have root access to the host (unless user namespaces are configured).

**Rule:** Always specify a non-root user. Use a numeric UID to ensure Kubernetes and other orchestrators can verify the user without needing to parse the `/etc/passwd` file inside the container.

*Before (Runs as root):*
```dockerfile
FROM ubuntu:22.04
COPY app /app
CMD ["/app/start.sh"]
```

*After (Runs as non-root):*
```dockerfile
FROM ubuntu:22.04
RUN groupadd -r appgroup && useradd -r -g appgroup -u 10001 appuser
COPY --chown=appuser:appgroup app /app
USER 10001
CMD ["/app/start.sh"]
```

### 2.2 COPY vs. ADD

The `ADD` instruction has hidden features: it can download files from URLs and automatically extract tar archives. This unpredictability is a security risk.

**Rule:** Always use `COPY` unless you specifically need the extraction feature of `ADD`.

*Before (Insecure):*
```dockerfile
ADD https://example.com/malicious-script.sh /usr/local/bin/
```

*After (Secure):*
```dockerfile
# Download explicitly and verify checksum
RUN curl -sSL https://example.com/safe-script.sh -o /usr/local/bin/safe-script.sh     && echo "EXPECTED_SHA256  /usr/local/bin/safe-script.sh" | sha256sum -c -     && chmod +x /usr/local/bin/safe-script.sh
```

### 2.3 Avoiding curl | bash Patterns

Piping `curl` directly into `bash` is a classic security anti-pattern. It executes arbitrary code from the internet without verification.

*Before (Dangerous):*
```dockerfile
RUN curl -sL https://deb.nodesource.com/setup_18.x | bash -
```

*After (Safer):*
```dockerfile
# Download, verify, then execute
RUN curl -sL -o setup.sh https://deb.nodesource.com/setup_18.x     && echo "EXPECTED_SHA256  setup.sh" | sha256sum -c -     && bash setup.sh     && rm setup.sh
```

### 2.4 Minimal Packages and Cache Removal

Every installed package increases the attack surface. Furthermore, package manager caches bloat the image size and can contain stale data.

**Rule:** Install only what is necessary, use `--no-install-recommends` (for apt), and clean the cache in the *same* `RUN` layer.

*Before (Bloated):*
```dockerfile
RUN apt-get update
RUN apt-get install -y python3
```

*After (Optimized and Secure):*
```dockerfile
RUN apt-get update && apt-get install -y --no-install-recommends     python3     && rm -rf /var/lib/apt/lists/*
```

### 2.5 Removing SUID/SGID Binaries

SUID (Set owner User ID up on execution) and SGID (Set Group ID up on execution) binaries allow users to execute a file with the permissions of the file owner or group. This is a common privilege escalation vector.

**Rule:** Find and remove SUID/SGID bits from binaries that don't need them.

```dockerfile
# Remove SUID/SGID bits from all files
RUN find / -xdev -perm /6000 -type f -exec chmod a-s {} \; || true
```

---

## 3. Runtime Security: Confining the Container

Even with a secure image, the runtime environment must be locked down to prevent container breakouts and resource exhaustion.

### 3.1 Read-Only Root Filesystem

A compromised container often attempts to download malware or modify configuration files. By mounting the root filesystem as read-only, you block these actions.

**Rule:** Set `read_only: true` in your `compose.yaml`. Use `tmpfs` for directories that require write access (e.g., `/tmp`, `/var/run`).

*compose.yaml Example:*
```yaml
services:
  webapp:
    image: YOUR_REGISTRY/webapp:v1.2.3
    read_only: true
    tmpfs:
      - /tmp
      - /var/run
```

### 3.2 Linux Capabilities (cap_drop and cap_add)

By default, Docker drops many Linux capabilities but retains a subset (e.g., `CAP_CHOWN`, `CAP_NET_BIND_SERVICE`). Most applications do not need even these.

**Rule:** Drop ALL capabilities, and explicitly add back only the ones strictly required.

*compose.yaml Example:*
```yaml
services:
  webapp:
    image: YOUR_REGISTRY/webapp:v1.2.3
    cap_drop:
      - ALL
    cap_add:
      - NET_BIND_SERVICE # Only if binding to ports < 1024
```

### 3.3 No New Privileges

The `no-new-privileges` flag prevents a process from gaining new privileges through `execve`. This mitigates SUID binary attacks.

*compose.yaml Example:*
```yaml
services:
  webapp:
    image: YOUR_REGISTRY/webapp:v1.2.3
    security_opt:
      - no-new-privileges:true
```

### 3.4 Seccomp and AppArmor Profiles

**Seccomp (Secure Computing Mode):** Restricts the system calls a container can make. Docker applies a default seccomp profile that blocks ~44 system calls. You can create custom profiles for stricter control.

**AppArmor:** A Linux kernel security module that restricts programs' capabilities with per-program profiles.

*compose.yaml Example:*
```yaml
services:
  webapp:
    image: YOUR_REGISTRY/webapp:v1.2.3
    security_opt:
      - seccomp=/path/to/custom-profile.json
      - apparmor=docker-default
```

### 3.5 Resource Limits (Cgroups)

Without resource limits, a single compromised or buggy container can consume all host resources (CPU, memory), causing a Denial of Service (DoS) for all other containers.

**Rule:** Always set memory and CPU limits.

*compose.yaml Example:*
```yaml
services:
  webapp:
    image: YOUR_REGISTRY/webapp:v1.2.3
    deploy:
      resources:
        limits:
          cpus: '0.50'
          memory: 512M
        reservations:
          cpus: '0.25'
          memory: 256M
```

*Real Error Message & Solution:*
**Error:** Container exits unexpectedly with status code 137.
**Solution:** Status 137 indicates the container was killed by the OOM (Out of Memory) killer. Check the host logs (`dmesg -T | grep -i oom`). Increase the memory limit in `compose.yaml` or optimize the application's memory usage.

### 3.6 No Privileged Mode and Host Namespaces

**Rule:** NEVER use `privileged: true` in production. It gives the container almost full access to the host.
**Rule:** NEVER share host namespaces (`network_mode: host`, `pid: host`, `ipc: host`) unless absolutely necessary for specific infrastructure tools, and even then, proceed with extreme caution.

---

## 4. Network Security: Isolating Communications

Network segmentation is crucial for limiting the blast radius of a compromise.

### 4.1 Internal Networks

Backend services (databases, caches) should never be exposed to the public internet or even the default bridge network.

*compose.yaml Example:*
```yaml
services:
  frontend:
    image: YOUR_REGISTRY/frontend:v1
    ports:
      - "443:443"
    networks:
      - public_net
      - private_net

  database:
    image: postgres:15
    networks:
      - private_net
    # No ports exposed!

networks:
  public_net:
  private_net:
    internal: true # Completely isolated from external networks
```

### 4.2 Encrypted Overlay Networks (Swarm)

If using Docker Swarm, ensure overlay networks are encrypted to protect data in transit between nodes.

```bash
docker network create --opt encrypted --driver overlay my-secure-network
```

### 4.3 TLS for All Service Communication

Even within internal networks, implement mutual TLS (mTLS) between services. This ensures that even if an attacker breaches the internal network, they cannot intercept or spoof traffic. Tools like Istio or Linkerd (in Kubernetes) or Traefik (in Docker) can manage this.

---

## 5. Secrets Management: Protecting Sensitive Data

Hardcoding secrets in Dockerfiles, environment variables, or source code is a critical vulnerability.

### 5.1 Docker Secrets (Swarm) and Compose Secrets

Docker provides a native secrets management mechanism. Secrets are mounted as in-memory files (tmpfs) at `/run/secrets/` and are never stored on disk.

*compose.yaml Example:*
```yaml
services:
  database:
    image: postgres:15
    environment:
      POSTGRES_PASSWORD_FILE: /run/secrets/db_password
    secrets:
      - db_password

secrets:
  db_password:
    file: ./secrets/db_password.txt # Ensure this file has strict permissions (chmod 600)
```

### 5.2 External Secret Managers

For enterprise environments, integrate with external secret managers like HashiCorp Vault, AWS Secrets Manager, or Azure Key Vault. Do not pass secrets as environment variables; instead, have the application fetch them at runtime or use an init container to populate a shared volume.

### 5.3 The Danger of ENV and Build Args

**Rule:** NEVER use `ENV` or `ARG` for secrets in a Dockerfile. They are baked into the image layers and can be easily extracted using `docker history`.

*Before (Insecure):*
```dockerfile
ARG API_KEY
ENV API_KEY=$API_KEY
```

*After (Secure - using BuildKit secrets):*
```dockerfile
# syntax=docker/dockerfile:1
FROM alpine
RUN --mount=type=secret,id=mysecret cat /run/secrets/mysecret > /app/config
```
Build command: `docker build --secret id=mysecret,src=mysecret.txt .`

---

## 6. Supply Chain Security: Securing the Pipeline

The software supply chain is a prime target. You must secure every step from code commit to container deployment.

### 6.1 Trusted Base Images and Registries

Only pull images from trusted, verified registries. Implement Role-Based Access Control (RBAC) on your private registries to restrict who can push images.

### 6.2 Build Provenance Attestations

Use Docker Buildx to generate provenance attestations. This provides a verifiable record of how an image was built, including the source code repository, commit SHA, and build environment.

```bash
docker buildx build --provenance=true --sbom=true -t YOUR_REGISTRY/YOUR_IMAGE:TAG .
```

### 6.3 CI/CD Pipeline Security

- **Least Privilege:** CI/CD runners should have minimal permissions.
- **Ephemeral Runners:** Use ephemeral runners that are destroyed after each build.
- **Secret Scanning:** Implement tools like GitGuardian or TruffleHog to scan repositories for accidentally committed secrets.

---

## 7. Docker Daemon Security: Protecting the Engine

The Docker daemon runs as root. Securing it is paramount.

### 7.1 TLS for Remote Access

If you must expose the Docker daemon API over a network, ALWAYS use mutual TLS.

```bash
dockerd --tlsverify --tlscacert=ca.pem --tlscert=server-cert.pem --tlskey=server-key.pem -H=0.0.0.0:2376
```

### 7.2 Rootless Mode

Rootless mode allows running the Docker daemon and containers as a non-root user. This drastically reduces the impact of a daemon vulnerability.

*Installation:*
```bash
dockerd-rootless-setuptool.sh install
```

### 7.3 User Namespaces

If rootless mode is not feasible, enable user namespaces. This maps the `root` user inside the container to a non-privileged user on the host.

*daemon.json:*
```json
{
  "userns-remap": "default"
}
```

### 7.4 Audit Logging

Configure the host's audit daemon (`auditd`) to monitor Docker files and directories.

*/etc/audit/rules.d/docker.rules:*
```text
-w /usr/bin/dockerd -k docker
-w /var/lib/docker -k docker
-w /etc/docker -k docker
-w /lib/systemd/system/docker.service -k docker
-w /lib/systemd/system/docker.socket -k docker
-w /etc/default/docker -k docker
-w /etc/docker/daemon.json -k docker
-w /usr/bin/docker-containerd -k docker
-w /usr/bin/docker-runc -k docker
```

---

## 8. Compliance Frameworks

Adhering to established frameworks provides a structured approach to security.

### 8.1 CIS Docker Benchmark

The Center for Internet Security (CIS) provides the gold standard for Docker security. It covers 7 sections:
1. Host Configuration
2. Docker Daemon Configuration
3. Docker Daemon Configuration Files
4. Container Images and Build File
5. Container Runtime
6. Docker Security Operations
7. Docker Swarm Configuration

**Tool:** Use `docker-bench-security` to automate the audit.
```bash
git clone https://github.com/docker/docker-bench-security.git
cd docker-bench-security
sudo sh docker-bench-security.sh
```

### 8.2 NIST 800-190

The National Institute of Standards and Technology (NIST) Special Publication 800-190 provides an Application Container Security Guide. Key areas include:
- Image vulnerabilities
- Registry access
- Orchestrator security
- Container isolation

### 8.3 PCI-DSS and SOC2

For environments handling credit card data (PCI-DSS) or requiring strict operational controls (SOC2), container security must include:
- Strict network segmentation (CDE isolation).
- Comprehensive logging and monitoring.
- Regular vulnerability scanning and penetration testing.
- Strict access controls (RBAC).

---

## 9. Complete Security Audit Checklist

This checklist is designed for tech support operations teams to evaluate client environments.

### Category 1: Host & Daemon Configuration
| ID | Check | Pass Criteria | Fail Criteria |
|---|---|---|---|
| 1.1 | Docker Daemon Auditing | `auditd` rules exist for `/var/lib/docker`, `/etc/docker`, etc. | No audit rules configured. |
| 1.2 | Rootless Mode / User Namespaces | Daemon runs rootless OR `userns-remap` is enabled. | Daemon runs as root without user namespaces. |
| 1.3 | Remote API TLS | Remote API (if enabled) requires mTLS. | API exposed on port 2375 without TLS. |
| 1.4 | Authorization Plugin | AuthZ plugin (e.g., OPA) is configured. | No authorization plugin used. |
| 1.5 | Daemon Log Level | Log level is set to `info` or higher. | Log level is `debug` in production. |

### Category 2: Image & Build Security
| ID | Check | Pass Criteria | Fail Criteria |
|---|---|---|---|
| 2.1 | Base Image Selection | Minimal images (Distroless, Scratch, Alpine) used. | Full OS images (Ubuntu, Debian) used unnecessarily. |
| 2.2 | Vulnerability Scanning | Automated scanning in CI/CD; 0 critical/high vulns. | No scanning; known vulnerabilities exist. |
| 2.3 | Image Signing | Docker Content Trust or Cosign enforced. | Unsigned images are allowed in production. |
| 2.4 | Multi-stage Builds | Build tools excluded from final runtime image. | Compilers and build tools present in runtime image. |
| 2.5 | Immutable Tags | Images referenced by SHA256 digest. | Images referenced by `:latest` or mutable tags. |
| 2.6 | Secrets in Dockerfile | No `ENV` or `ARG` used for secrets. | Passwords/keys found in Dockerfile or image history. |
| 2.7 | USER Directive | Non-root numeric UID specified in Dockerfile. | Container runs as root (UID 0). |
| 2.8 | COPY vs ADD | `COPY` used exclusively (unless tar extraction needed). | `ADD` used to fetch remote resources. |
| 2.9 | SUID/SGID Binaries | Unnecessary SUID/SGID bits removed. | SUID binaries present and accessible. |

### Category 3: Runtime Security
| ID | Check | Pass Criteria | Fail Criteria |
|---|---|---|---|
| 3.1 | Read-Only Root FS | `read_only: true` set for all applicable containers. | Root filesystem is writable. |
| 3.2 | Capabilities | `cap_drop: ALL` used; minimal `cap_add`. | Default capabilities retained or `cap_add: ALL`. |
| 3.3 | No New Privileges | `security_opt: no-new-privileges:true` applied. | Flag is missing. |
| 3.4 | Seccomp/AppArmor | Custom or default profiles applied. | Profiles explicitly disabled (`unconfined`). |
| 3.5 | Resource Limits | CPU and Memory limits/reservations defined. | No resource limits set (unbounded consumption). |
| 3.6 | Privileged Mode | `privileged: true` is NOT used. | Container runs in privileged mode. |
| 3.7 | Host Namespaces | `network_mode: host`, `pid: host`, `ipc: host` NOT used. | Container shares host namespaces. |
| 3.8 | Healthchecks | `healthcheck` defined for all services. | No healthchecks configured. |
| 3.9 | Restart Policies | `unless-stopped` or `on-failure` configured. | No restart policy or `always` used inappropriately. |

### Category 4: Network & Data Security
| ID | Check | Pass Criteria | Fail Criteria |
|---|---|---|---|
| 4.1 | Internal Networks | Backend services on `internal: true` networks. | Databases exposed to default bridge or host. |
| 4.2 | Port Mapping | Only necessary ports exposed; bound to specific IPs. | Ports bound to `0.0.0.0` unnecessarily. |
| 4.3 | Secrets Management | Docker Secrets or external manager used. | Secrets passed via environment variables. |
| 4.4 | Volume Mounts | Bind mounts restricted; named volumes preferred. | Sensitive host directories mounted into container. |

*(Note: A full audit would expand this to 50+ detailed checks based on the CIS Benchmark).*

---

## 10. Incident Response: Handling Compromised Containers

When a breach occurs, rapid and structured response is critical.

### 10.1 Isolation

Do NOT stop or kill the container immediately. This destroys volatile evidence in memory.

**Step 1: Isolate from the network.**
Disconnect the container from all networks to stop data exfiltration and command-and-control (C2) communication.
```bash
docker network disconnect <network_name> <container_name>
```

**Step 2: Pause the container.**
Freeze the container's processes.
```bash
docker pause <container_name>
```

### 10.2 Forensic Image Capture

Capture the state of the container for analysis.

**Step 1: Commit the container to an image.**
```bash
docker commit <container_name> forensic-image:<container_name>-<timestamp>
```

**Step 2: Export the filesystem.**
```bash
docker export <container_name> > forensic-fs-<timestamp>.tar
```

**Step 3: Capture memory (Advanced).**
Use tools like LiME or Volatility on the host to capture the memory space of the container's cgroup.

### 10.3 Log Preservation

Collect all relevant logs immediately.

```bash
# Container logs
docker logs <container_name> > container-<timestamp>.log

# Docker daemon logs
journalctl -u docker > dockerd-<timestamp>.log

# Host audit logs
cp /var/log/audit/audit.log audit-<timestamp>.log
```

### 10.4 Eradication and Recovery

Once evidence is secured:
1. Kill and remove the compromised container (`docker kill`, `docker rm`).
2. Identify the root cause (e.g., vulnerable dependency, leaked secret).
3. Patch the vulnerability in the source code/Dockerfile.
4. Rebuild the image and deploy the updated version.
5. Rotate all secrets that were accessible to the compromised container.

---

## Conclusion

Securing a Docker environment is not a one-time task; it is a continuous process of auditing, hardening, and monitoring. By implementing the strategies outlined in this Super Specialist guide—from minimal base images and strict runtime constraints to robust secrets management and incident response protocols—you can build resilient, production-ready container infrastructure that withstands modern threats.

## References
[1] CIS Docker Benchmark v1.6.0
[2] NIST Special Publication 800-190: Application Container Security Guide
[3] Docker Documentation: Security


---

## 11. Advanced Troubleshooting Scenarios

As a Super Specialist, you will encounter complex issues that go beyond basic misconfigurations. Here are deep dives into common production incidents.

### Scenario A: The "Zombie" Container (High CPU, Unresponsive)

**Symptoms:** A container is consuming 100% CPU but is not responding to health checks or network requests. `docker stop` hangs indefinitely.

**Diagnosis:**
1. Identify the container PID on the host:
   ```bash
   docker inspect --format '{{.State.Pid}}' <container_name>
   ```
2. Check the process tree on the host:
   ```bash
   ps -ef | grep <PID>
   ```
3. Use `strace` to see what the process is doing (requires root on host):
   ```bash
   strace -p <PID>
   ```
   *Result:* You might see it stuck in an infinite loop of failing system calls or deadlocked waiting for a resource.

**Resolution:**
1. If `docker stop` fails, the daemon sends a SIGTERM. If the app ignores it, it waits for the grace period (default 10s) then sends SIGKILL.
2. If it's completely wedged, force kill it from the host:
   ```bash
   kill -9 <PID>
   ```
3. **Prevention:** Ensure the application handles SIGTERM correctly. Use `init: true` in `compose.yaml` to run an init process (like `tini`) that reaps zombie processes and forwards signals properly.

*compose.yaml Example:*
```yaml
services:
  app:
    image: YOUR_REGISTRY/app:v1
    init: true
    stop_grace_period: 30s
```

### Scenario B: Intermittent DNS Resolution Failures

**Symptoms:** Containers randomly fail to resolve external hostnames or internal service names. Logs show `Temporary failure in name resolution`.

**Diagnosis:**
1. Check the container's DNS configuration:
   ```bash
   docker exec <container_name> cat /etc/resolv.conf
   ```
   *Note:* Docker uses an embedded DNS server at `127.0.0.11` for user-defined networks.
2. Check host DNS resolution and firewall rules. Sometimes, aggressive firewall rules drop UDP DNS packets.
3. Monitor DNS traffic using `tcpdump` on the Docker bridge interface.

**Resolution:**
1. If the host's DNS is unstable, explicitly define reliable DNS servers in `compose.yaml` or `daemon.json`.
2. Ensure the `ndots` option in `/etc/resolv.conf` isn't causing excessive DNS queries (common in Kubernetes, but can happen in complex Compose setups).

*compose.yaml Example:*
```yaml
services:
  app:
    image: YOUR_REGISTRY/app:v1
    dns:
      - 8.8.8.8
      - 1.1.1.1
    dns_opt:
      - ndots:1
```

### Scenario C: Overlay2 Storage Driver Exhaustion

**Symptoms:** Host disk space is full. `docker system df` shows massive space used by images or local volumes. `docker system prune` doesn't free enough space.

**Diagnosis:**
1. Find the largest directories in the Docker root:
   ```bash
   sudo du -sh /var/lib/docker/* | sort -h
   ```
2. If `/var/lib/docker/overlay2` is huge, you have orphaned layers or containers writing massive amounts of data to their writable layer instead of a volume.
3. Identify containers with large writable layers:
   ```bash
   docker ps -s
   ```

**Resolution:**
1. **Immediate fix:** Stop containers and run a deep prune:
   ```bash
   docker system prune -a --volumes
   ```
2. **Root Cause Fix:** Ensure applications write logs to `stdout`/`stderr` (handled by Docker logging driver) or to mounted volumes, NEVER to the container filesystem.
3. Configure log rotation in `compose.yaml` to prevent log files from filling the disk.

*compose.yaml Example:*
```yaml
services:
  app:
    image: YOUR_REGISTRY/app:v1
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

---

## 12. Cost and Time Optimization Strategies

Efficiency is just as important as security. Bloated images and inefficient builds waste CI/CD minutes, bandwidth, and storage costs.

### 12.1 Layer Caching Optimization

Docker builds images layer by layer. If a layer changes, all subsequent layers must be rebuilt.

**Rule:** Order your Dockerfile instructions from least frequently changed to most frequently changed.

*Before (Inefficient):*
```dockerfile
FROM node:18
WORKDIR /app
COPY . .
# If ANY file in the repo changes, npm install runs again!
RUN npm install
CMD ["npm", "start"]
```

*After (Optimized):*
```dockerfile
FROM node:18
WORKDIR /app
# Copy only package files first
COPY package*.json ./
# This layer is cached unless package.json changes
RUN npm ci
# Now copy the rest of the code
COPY . .
CMD ["npm", "start"]
```

### 12.2 BuildKit Cache Mounts

For languages that use package managers (npm, pip, apt), downloading dependencies repeatedly is a massive time sink. BuildKit cache mounts solve this.

*Dockerfile Example (Python):*
```dockerfile
# syntax=docker/dockerfile:1
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
# Cache the pip download directory
RUN --mount=type=cache,target=/root/.cache/pip     pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

### 12.3 Compose Profiles for Local Development

Running a full microservices stack locally can melt a developer's laptop. Use Compose profiles to group services.

*compose.yaml Example:*
```yaml
services:
  frontend:
    image: my-frontend
    profiles: ["ui", "full"]
  backend-api:
    image: my-api
    profiles: ["api", "full"]
  database:
    image: postgres
    profiles: ["api", "full", "db-only"]
```
*Usage:* `docker compose --profile api up -d` (Starts only backend-api and database).

### 12.4 Docker Compose Watch (Hot Reloading)

Introduced in Compose V2.22.0, `watch` automatically updates running services as you edit code, eliminating the need to manually rebuild images during development.

*compose.yaml Example:*
```yaml
services:
  web:
    build: .
    command: npm run dev
    develop:
      watch:
        - action: sync
          path: ./src
          target: /app/src
        - action: rebuild
          path: package.json
```
*Usage:* `docker compose watch`

---

## 13. Comprehensive Upgrade Strategies

Upgrading containerized applications in production requires careful planning to avoid downtime.

### 13.1 Rolling Updates (Swarm)

Docker Swarm natively supports rolling updates, updating a specified number of replicas at a time.

*compose.yaml Example:*
```yaml
services:
  web:
    image: YOUR_REGISTRY/web:v2
    deploy:
      replicas: 4
      update_config:
        parallelism: 1
        delay: 10s
        order: start-first # Start new container before stopping old one
        failure_action: rollback
```

### 13.2 Blue-Green Deployments (Compose)

In a standard Docker Compose environment, you can simulate blue-green deployments using a reverse proxy (like Traefik or Nginx).

1. Run `web-blue` (v1) and route traffic to it via the proxy.
2. Deploy `web-green` (v2) alongside it.
3. Update the proxy configuration to route traffic to `web-green`.
4. Monitor for errors. If successful, tear down `web-blue`.

### 13.3 Database Migrations

Never run database migrations automatically on container startup in a multi-replica environment (race conditions).

**Best Practice:** Run migrations as a separate, short-lived container (a Kubernetes Job or a specific Compose profile) *before* updating the application containers.

```bash
# Run migration
docker compose run --rm app-migration
# If successful, update the app
docker compose up -d app
```

---

## 14. Extended Security Audit Checklist (Continued)

### Category 5: Secrets & Configuration
| ID | Check | Pass Criteria | Fail Criteria |
|---|---|---|---|
| 5.1 | Hardcoded Secrets | Source code and configs scanned; no secrets found. | API keys/passwords found in plaintext. |
| 5.2 | Environment Variables | `.env` files excluded from version control (`.gitignore`). | `.env` committed to repository. |
| 5.3 | Secret Permissions | Mounted secret files have strict permissions (e.g., 400). | Secrets readable by all users. |

### Category 6: Supply Chain & CI/CD
| ID | Check | Pass Criteria | Fail Criteria |
|---|---|---|---|
| 6.1 | Registry Access | RBAC implemented; pull-only access for production nodes. | Anonymous pull/push allowed. |
| 6.2 | SBOM Generation | SBOM generated and archived for every release. | No software bill of materials exists. |
| 6.3 | Base Image Provenance | Base images sourced from official, verified publishers. | Base images pulled from unknown personal repositories. |

### Category 7: Monitoring & Logging
| ID | Check | Pass Criteria | Fail Criteria |
|---|---|---|---|
| 7.1 | Centralized Logging | Container logs forwarded to a central SIEM/Log aggregator. | Logs only stored locally on the host. |
| 7.2 | Alerting | Alerts configured for container crashes (OOM, exit code != 0). | No proactive alerting in place. |
| 7.3 | Performance Monitoring | Metrics (CPU, Mem, Net) collected via Prometheus/cAdvisor. | No visibility into container resource usage. |

---
## Final Thoughts for the Operations Team

As a Docker Super Specialist, your role is to bridge the gap between development velocity and operational stability. Security is not a roadblock; it is a fundamental property of a well-engineered system. By enforcing these strict guidelines, utilizing the provided configurations, and understanding the deep mechanics of the Docker engine, you will ensure that your clients' infrastructure remains robust, performant, and impenetrable.


# Docker Super Specialist: Complete Security Audit Checklist & Hardening Guide

## Introduction

Welcome to the definitive guide for securing, optimizing, and troubleshooting Docker environments. As the Docker Super Specialist, this document serves as your comprehensive manual for conducting exhaustive security audits, implementing flaw-proof configurations, and resolving complex operational issues. This guide is designed for tech support operations teams, DevOps engineers, and system administrators who are responsible for maintaining production-grade containerized infrastructure.

The container ecosystem has evolved rapidly, and with it, the threat landscape. A single misconfiguration in a Dockerfile or a `compose.yaml` file can expose your entire infrastructure to catastrophic breaches. This guide goes beyond basic best practices; it provides deep, actionable insights, real-world configuration examples, and a meticulous 50+ item security audit checklist. We will cover every layer of the container lifecycle: from image selection and build processes to runtime execution, network isolation, and incident response.

By following this guide, you will transform vulnerable, inefficient Docker setups into fortified, high-performance environments that comply with stringent industry standards such as the CIS Docker Benchmark, NIST 800-190, PCI-DSS, and SOC2.

---

## 1. Image Security: The Foundation of Container Trust

The security of your containerized application begins long before it runs; it starts with the base image. A compromised or bloated base image introduces vulnerabilities that cannot be mitigated at runtime.

### 1.1 Base Image Selection

Choosing the right base image is critical. The goal is to minimize the attack surface by reducing the number of installed packages and utilities.

**Distroless Images:**
Distroless images, pioneered by Google, contain only your application and its runtime dependencies. They do not contain package managers, shells, or any other programs you would expect to find in a standard Linux distribution. This makes them incredibly secure.

*Before (Vulnerable):*
```dockerfile
FROM node:18
WORKDIR /app
COPY . .
RUN npm install
CMD ["node", "server.js"]
```

*After (Secure with Distroless):*
```dockerfile
# Build stage
FROM node:18 AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .

# Runtime stage
FROM gcr.io/distroless/nodejs18-debian11
WORKDIR /app
COPY --from=build /app /app
CMD ["server.js"]
```

**Scratch Images:**
For statically compiled languages like Go or Rust, the `scratch` image is the ultimate choice. It is an explicitly empty image.

```dockerfile
# Build stage
FROM golang:1.20 AS builder
WORKDIR /app
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o main .

# Runtime stage
FROM scratch
COPY --from=builder /app/main /main
ENTRYPOINT ["/main"]
```

**Alpine Linux:**
Alpine is a popular choice due to its small size (~5MB). However, it uses `musl` libc instead of `glibc`, which can cause compatibility issues with some applications (e.g., Python wheels compiled for glibc). If you use Alpine, ensure you pin the version and scan it regularly.

### 1.2 Vulnerability Scanning

Continuous vulnerability scanning is non-negotiable. You must integrate scanning into your CI/CD pipeline and regularly scan images in your registry.

**Tools:**
- **Docker Scout:** Integrated directly into Docker Desktop and CLI.
- **Trivy (Aqua Security):** A comprehensive, easy-to-use scanner for containers and other artifacts.
- **Grype (Anchore):** A vulnerability scanner for container images and filesystems.
- **Snyk:** A developer-first security platform.

*Real Command Example (Trivy):*
```bash
# Scan a local image and fail the build if critical vulnerabilities are found
trivy image --severity CRITICAL --exit-code 1 YOUR_REGISTRY/YOUR_IMAGE:TAG
```

*Real Error Message & Solution:*
**Error:** `Trivy found 3 CRITICAL vulnerabilities in base image ubuntu:20.04`
**Solution:** Update the base image to a newer patch version (e.g., `ubuntu:22.04`) or switch to a minimal image like Alpine or Distroless. If the vulnerability is in an application dependency, update the dependency in your `package.json` or `requirements.txt`.

### 1.3 Image Signing and Provenance

How do you know the image you are pulling is the one you built? Image signing ensures integrity and authenticity.

**Docker Content Trust (DCT):**
DCT uses Notary to sign images. When enabled, Docker will only pull signed images.

```bash
# Enable DCT
export DOCKER_CONTENT_TRUST=1
# Pulling an unsigned image will now fail
docker pull YOUR_REGISTRY/unsigned-image:latest
# Error: Error: remote trust data does not exist...
```

**Cosign (Sigstore):**
Cosign is a modern, keyless signing tool that is becoming the industry standard.

```bash
# Generate a keypair
cosign generate-key-pair

# Sign an image
cosign sign --key cosign.key YOUR_REGISTRY/YOUR_IMAGE:TAG

# Verify an image
cosign verify --key cosign.pub YOUR_REGISTRY/YOUR_IMAGE:TAG
```

### 1.4 SBOM Generation

A Software Bill of Materials (SBOM) is a nested inventory of all components, libraries, and modules required to build a given piece of software. It is essential for supply chain security.

*Real Command Example (Syft):*
```bash
# Generate an SBOM in SPDX format
syft YOUR_REGISTRY/YOUR_IMAGE:TAG -o spdx-json > sbom.json
```

### 1.5 Pinning Versions with SHA256 Digests

Tags like `:latest` or even `:1.0` are mutable; they can be overwritten. To guarantee you are pulling the exact same image every time, use the SHA256 digest.

*Before (Mutable):*
```dockerfile
FROM nginx:1.25
```

*After (Immutable):*
```dockerfile
FROM nginx@sha256:af296b188c7b7df99ba960ca614439c99cb7cf252ed7bbc23e90cfda59092305
```

---

## 2. Dockerfile Security: Hardening the Build Process

The Dockerfile is the blueprint for your image. Insecure directives here will result in an insecure container.

### 2.1 The USER Directive

By default, Docker containers run as `root`. This is a massive security risk. If an attacker breaks out of the container, they will have root access to the host (unless user namespaces are configured).

**Rule:** Always specify a non-root user. Use a numeric UID to ensure Kubernetes and other orchestrators can verify the user without needing to parse the `/etc/passwd` file inside the container.

*Before (Runs as root):*
```dockerfile
FROM ubuntu:22.04
COPY app /app
CMD ["/app/start.sh"]
```

*After (Runs as non-root):*
```dockerfile
FROM ubuntu:22.04
RUN groupadd -r appgroup && useradd -r -g appgroup -u 10001 appuser
COPY --chown=appuser:appgroup app /app
USER 10001
CMD ["/app/start.sh"]
```

### 2.2 COPY vs. ADD

The `ADD` instruction has hidden features: it can download files from URLs and automatically extract tar archives. This unpredictability is a security risk.

**Rule:** Always use `COPY` unless you specifically need the extraction feature of `ADD`.

*Before (Insecure):*
```dockerfile
ADD https://example.com/malicious-script.sh /usr/local/bin/
```

*After (Secure):*
```dockerfile
# Download explicitly and verify checksum
RUN curl -sSL https://example.com/safe-script.sh -o /usr/local/bin/safe-script.sh     && echo "EXPECTED_SHA256  /usr/local/bin/safe-script.sh" | sha256sum -c -     && chmod +x /usr/local/bin/safe-script.sh
```

### 2.3 Avoiding curl | bash Patterns

Piping `curl` directly into `bash` is a classic security anti-pattern. It executes arbitrary code from the internet without verification.

*Before (Dangerous):*
```dockerfile
RUN curl -sL https://deb.nodesource.com/setup_18.x | bash -
```

*After (Safer):*
```dockerfile
# Download, verify, then execute
RUN curl -sL -o setup.sh https://deb.nodesource.com/setup_18.x     && echo "EXPECTED_SHA256  setup.sh" | sha256sum -c -     && bash setup.sh     && rm setup.sh
```

### 2.4 Minimal Packages and Cache Removal

Every installed package increases the attack surface. Furthermore, package manager caches bloat the image size and can contain stale data.

**Rule:** Install only what is necessary, use `--no-install-recommends` (for apt), and clean the cache in the *same* `RUN` layer.

*Before (Bloated):*
```dockerfile
RUN apt-get update
RUN apt-get install -y python3
```

*After (Optimized and Secure):*
```dockerfile
RUN apt-get update && apt-get install -y --no-install-recommends     python3     && rm -rf /var/lib/apt/lists/*
```

### 2.5 Removing SUID/SGID Binaries

SUID (Set owner User ID up on execution) and SGID (Set Group ID up on execution) binaries allow users to execute a file with the permissions of the file owner or group. This is a common privilege escalation vector.

**Rule:** Find and remove SUID/SGID bits from binaries that don't need them.

```dockerfile
# Remove SUID/SGID bits from all files
RUN find / -xdev -perm /6000 -type f -exec chmod a-s {} \; || true
```

---

## 3. Runtime Security: Confining the Container

Even with a secure image, the runtime environment must be locked down to prevent container breakouts and resource exhaustion.

### 3.1 Read-Only Root Filesystem

A compromised container often attempts to download malware or modify configuration files. By mounting the root filesystem as read-only, you block these actions.

**Rule:** Set `read_only: true` in your `compose.yaml`. Use `tmpfs` for directories that require write access (e.g., `/tmp`, `/var/run`).

*compose.yaml Example:*
```yaml
services:
  webapp:
    image: YOUR_REGISTRY/webapp:v1.2.3
    read_only: true
    tmpfs:
      - /tmp
      - /var/run
```

### 3.2 Linux Capabilities (cap_drop and cap_add)

By default, Docker drops many Linux capabilities but retains a subset (e.g., `CAP_CHOWN`, `CAP_NET_BIND_SERVICE`). Most applications do not need even these.

**Rule:** Drop ALL capabilities, and explicitly add back only the ones strictly required.

*compose.yaml Example:*
```yaml
services:
  webapp:
    image: YOUR_REGISTRY/webapp:v1.2.3
    cap_drop:
      - ALL
    cap_add:
      - NET_BIND_SERVICE # Only if binding to ports < 1024
```

### 3.3 No New Privileges

The `no-new-privileges` flag prevents a process from gaining new privileges through `execve`. This mitigates SUID binary attacks.

*compose.yaml Example:*
```yaml
services:
  webapp:
    image: YOUR_REGISTRY/webapp:v1.2.3
    security_opt:
      - no-new-privileges:true
```

### 3.4 Seccomp and AppArmor Profiles

**Seccomp (Secure Computing Mode):** Restricts the system calls a container can make. Docker applies a default seccomp profile that blocks ~44 system calls. You can create custom profiles for stricter control.

**AppArmor:** A Linux kernel security module that restricts programs' capabilities with per-program profiles.

*compose.yaml Example:*
```yaml
services:
  webapp:
    image: YOUR_REGISTRY/webapp:v1.2.3
    security_opt:
      - seccomp=/path/to/custom-profile.json
      - apparmor=docker-default
```

### 3.5 Resource Limits (Cgroups)

Without resource limits, a single compromised or buggy container can consume all host resources (CPU, memory), causing a Denial of Service (DoS) for all other containers.

**Rule:** Always set memory and CPU limits.

*compose.yaml Example:*
```yaml
services:
  webapp:
    image: YOUR_REGISTRY/webapp:v1.2.3
    deploy:
      resources:
        limits:
          cpus: '0.50'
          memory: 512M
        reservations:
          cpus: '0.25'
          memory: 256M
```

*Real Error Message & Solution:*
**Error:** Container exits unexpectedly with status code 137.
**Solution:** Status 137 indicates the container was killed by the OOM (Out of Memory) killer. Check the host logs (`dmesg -T | grep -i oom`). Increase the memory limit in `compose.yaml` or optimize the application's memory usage.

### 3.6 No Privileged Mode and Host Namespaces

**Rule:** NEVER use `privileged: true` in production. It gives the container almost full access to the host.
**Rule:** NEVER share host namespaces (`network_mode: host`, `pid: host`, `ipc: host`) unless absolutely necessary for specific infrastructure tools, and even then, proceed with extreme caution.

---

## 4. Network Security: Isolating Communications

Network segmentation is crucial for limiting the blast radius of a compromise.

### 4.1 Internal Networks

Backend services (databases, caches) should never be exposed to the public internet or even the default bridge network.

*compose.yaml Example:*
```yaml
services:
  frontend:
    image: YOUR_REGISTRY/frontend:v1
    ports:
      - "443:443"
    networks:
      - public_net
      - private_net

  database:
    image: postgres:15
    networks:
      - private_net
    # No ports exposed!

networks:
  public_net:
  private_net:
    internal: true # Completely isolated from external networks
```

### 4.2 Encrypted Overlay Networks (Swarm)

If using Docker Swarm, ensure overlay networks are encrypted to protect data in transit between nodes.

```bash
docker network create --opt encrypted --driver overlay my-secure-network
```

### 4.3 TLS for All Service Communication

Even within internal networks, implement mutual TLS (mTLS) between services. This ensures that even if an attacker breaches the internal network, they cannot intercept or spoof traffic. Tools like Istio or Linkerd (in Kubernetes) or Traefik (in Docker) can manage this.

---

## 5. Secrets Management: Protecting Sensitive Data

Hardcoding secrets in Dockerfiles, environment variables, or source code is a critical vulnerability.

### 5.1 Docker Secrets (Swarm) and Compose Secrets

Docker provides a native secrets management mechanism. Secrets are mounted as in-memory files (tmpfs) at `/run/secrets/` and are never stored on disk.

*compose.yaml Example:*
```yaml
services:
  database:
    image: postgres:15
    environment:
      POSTGRES_PASSWORD_FILE: /run/secrets/db_password
    secrets:
      - db_password

secrets:
  db_password:
    file: ./secrets/db_password.txt # Ensure this file has strict permissions (chmod 600)
```

### 5.2 External Secret Managers

For enterprise environments, integrate with external secret managers like HashiCorp Vault, AWS Secrets Manager, or Azure Key Vault. Do not pass secrets as environment variables; instead, have the application fetch them at runtime or use an init container to populate a shared volume.

### 5.3 The Danger of ENV and Build Args

**Rule:** NEVER use `ENV` or `ARG` for secrets in a Dockerfile. They are baked into the image layers and can be easily extracted using `docker history`.

*Before (Insecure):*
```dockerfile
ARG API_KEY
ENV API_KEY=$API_KEY
```

*After (Secure - using BuildKit secrets):*
```dockerfile
# syntax=docker/dockerfile:1
FROM alpine
RUN --mount=type=secret,id=mysecret cat /run/secrets/mysecret > /app/config
```
Build command: `docker build --secret id=mysecret,src=mysecret.txt .`

---

## 6. Supply Chain Security: Securing the Pipeline

The software supply chain is a prime target. You must secure every step from code commit to container deployment.

### 6.1 Trusted Base Images and Registries

Only pull images from trusted, verified registries. Implement Role-Based Access Control (RBAC) on your private registries to restrict who can push images.

### 6.2 Build Provenance Attestations

Use Docker Buildx to generate provenance attestations. This provides a verifiable record of how an image was built, including the source code repository, commit SHA, and build environment.

```bash
docker buildx build --provenance=true --sbom=true -t YOUR_REGISTRY/YOUR_IMAGE:TAG .
```

### 6.3 CI/CD Pipeline Security

- **Least Privilege:** CI/CD runners should have minimal permissions.
- **Ephemeral Runners:** Use ephemeral runners that are destroyed after each build.
- **Secret Scanning:** Implement tools like GitGuardian or TruffleHog to scan repositories for accidentally committed secrets.

---

## 7. Docker Daemon Security: Protecting the Engine

The Docker daemon runs as root. Securing it is paramount.

### 7.1 TLS for Remote Access

If you must expose the Docker daemon API over a network, ALWAYS use mutual TLS.

```bash
dockerd --tlsverify --tlscacert=ca.pem --tlscert=server-cert.pem --tlskey=server-key.pem -H=0.0.0.0:2376
```

### 7.2 Rootless Mode

Rootless mode allows running the Docker daemon and containers as a non-root user. This drastically reduces the impact of a daemon vulnerability.

*Installation:*
```bash
dockerd-rootless-setuptool.sh install
```

### 7.3 User Namespaces

If rootless mode is not feasible, enable user namespaces. This maps the `root` user inside the container to a non-privileged user on the host.

*daemon.json:*
```json
{
  "userns-remap": "default"
}
```

### 7.4 Audit Logging

Configure the host's audit daemon (`auditd`) to monitor Docker files and directories.

*/etc/audit/rules.d/docker.rules:*
```text
-w /usr/bin/dockerd -k docker
-w /var/lib/docker -k docker
-w /etc/docker -k docker
-w /lib/systemd/system/docker.service -k docker
-w /lib/systemd/system/docker.socket -k docker
-w /etc/default/docker -k docker
-w /etc/docker/daemon.json -k docker
-w /usr/bin/docker-containerd -k docker
-w /usr/bin/docker-runc -k docker
```

---

## 8. Compliance Frameworks

Adhering to established frameworks provides a structured approach to security.

### 8.1 CIS Docker Benchmark

The Center for Internet Security (CIS) provides the gold standard for Docker security. It covers 7 sections:
1. Host Configuration
2. Docker Daemon Configuration
3. Docker Daemon Configuration Files
4. Container Images and Build File
5. Container Runtime
6. Docker Security Operations
7. Docker Swarm Configuration

**Tool:** Use `docker-bench-security` to automate the audit.
```bash
git clone https://github.com/docker/docker-bench-security.git
cd docker-bench-security
sudo sh docker-bench-security.sh
```

### 8.2 NIST 800-190

The National Institute of Standards and Technology (NIST) Special Publication 800-190 provides an Application Container Security Guide. Key areas include:
- Image vulnerabilities
- Registry access
- Orchestrator security
- Container isolation

### 8.3 PCI-DSS and SOC2

For environments handling credit card data (PCI-DSS) or requiring strict operational controls (SOC2), container security must include:
- Strict network segmentation (CDE isolation).
- Comprehensive logging and monitoring.
- Regular vulnerability scanning and penetration testing.
- Strict access controls (RBAC).

---

## 9. Complete Security Audit Checklist

This checklist is designed for tech support operations teams to evaluate client environments.

### Category 1: Host & Daemon Configuration
| ID | Check | Pass Criteria | Fail Criteria |
|---|---|---|---|
| 1.1 | Docker Daemon Auditing | `auditd` rules exist for `/var/lib/docker`, `/etc/docker`, etc. | No audit rules configured. |
| 1.2 | Rootless Mode / User Namespaces | Daemon runs rootless OR `userns-remap` is enabled. | Daemon runs as root without user namespaces. |
| 1.3 | Remote API TLS | Remote API (if enabled) requires mTLS. | API exposed on port 2375 without TLS. |
| 1.4 | Authorization Plugin | AuthZ plugin (e.g., OPA) is configured. | No authorization plugin used. |
| 1.5 | Daemon Log Level | Log level is set to `info` or higher. | Log level is `debug` in production. |

### Category 2: Image & Build Security
| ID | Check | Pass Criteria | Fail Criteria |
|---|---|---|---|
| 2.1 | Base Image Selection | Minimal images (Distroless, Scratch, Alpine) used. | Full OS images (Ubuntu, Debian) used unnecessarily. |
| 2.2 | Vulnerability Scanning | Automated scanning in CI/CD; 0 critical/high vulns. | No scanning; known vulnerabilities exist. |
| 2.3 | Image Signing | Docker Content Trust or Cosign enforced. | Unsigned images are allowed in production. |
| 2.4 | Multi-stage Builds | Build tools excluded from final runtime image. | Compilers and build tools present in runtime image. |
| 2.5 | Immutable Tags | Images referenced by SHA256 digest. | Images referenced by `:latest` or mutable tags. |
| 2.6 | Secrets in Dockerfile | No `ENV` or `ARG` used for secrets. | Passwords/keys found in Dockerfile or image history. |
| 2.7 | USER Directive | Non-root numeric UID specified in Dockerfile. | Container runs as root (UID 0). |
| 2.8 | COPY vs ADD | `COPY` used exclusively (unless tar extraction needed). | `ADD` used to fetch remote resources. |
| 2.9 | SUID/SGID Binaries | Unnecessary SUID/SGID bits removed. | SUID binaries present and accessible. |

### Category 3: Runtime Security
| ID | Check | Pass Criteria | Fail Criteria |
|---|---|---|---|
| 3.1 | Read-Only Root FS | `read_only: true` set for all applicable containers. | Root filesystem is writable. |
| 3.2 | Capabilities | `cap_drop: ALL` used; minimal `cap_add`. | Default capabilities retained or `cap_add: ALL`. |
| 3.3 | No New Privileges | `security_opt: no-new-privileges:true` applied. | Flag is missing. |
| 3.4 | Seccomp/AppArmor | Custom or default profiles applied. | Profiles explicitly disabled (`unconfined`). |
| 3.5 | Resource Limits | CPU and Memory limits/reservations defined. | No resource limits set (unbounded consumption). |
| 3.6 | Privileged Mode | `privileged: true` is NOT used. | Container runs in privileged mode. |
| 3.7 | Host Namespaces | `network_mode: host`, `pid: host`, `ipc: host` NOT used. | Container shares host namespaces. |
| 3.8 | Healthchecks | `healthcheck` defined for all services. | No healthchecks configured. |
| 3.9 | Restart Policies | `unless-stopped` or `on-failure` configured. | No restart policy or `always` used inappropriately. |

### Category 4: Network & Data Security
| ID | Check | Pass Criteria | Fail Criteria |
|---|---|---|---|
| 4.1 | Internal Networks | Backend services on `internal: true` networks. | Databases exposed to default bridge or host. |
| 4.2 | Port Mapping | Only necessary ports exposed; bound to specific IPs. | Ports bound to `0.0.0.0` unnecessarily. |
| 4.3 | Secrets Management | Docker Secrets or external manager used. | Secrets passed via environment variables. |
| 4.4 | Volume Mounts | Bind mounts restricted; named volumes preferred. | Sensitive host directories mounted into container. |

*(Note: A full audit would expand this to 50+ detailed checks based on the CIS Benchmark).*

---

## 10. Incident Response: Handling Compromised Containers

When a breach occurs, rapid and structured response is critical.

### 10.1 Isolation

Do NOT stop or kill the container immediately. This destroys volatile evidence in memory.

**Step 1: Isolate from the network.**
Disconnect the container from all networks to stop data exfiltration and command-and-control (C2) communication.
```bash
docker network disconnect <network_name> <container_name>
```

**Step 2: Pause the container.**
Freeze the container's processes.
```bash
docker pause <container_name>
```

### 10.2 Forensic Image Capture

Capture the state of the container for analysis.

**Step 1: Commit the container to an image.**
```bash
docker commit <container_name> forensic-image:<container_name>-<timestamp>
```

**Step 2: Export the filesystem.**
```bash
docker export <container_name> > forensic-fs-<timestamp>.tar
```

**Step 3: Capture memory (Advanced).**
Use tools like LiME or Volatility on the host to capture the memory space of the container's cgroup.

### 10.3 Log Preservation

Collect all relevant logs immediately.

```bash
# Container logs
docker logs <container_name> > container-<timestamp>.log

# Docker daemon logs
journalctl -u docker > dockerd-<timestamp>.log

# Host audit logs
cp /var/log/audit/audit.log audit-<timestamp>.log
```

### 10.4 Eradication and Recovery

Once evidence is secured:
1. Kill and remove the compromised container (`docker kill`, `docker rm`).
2. Identify the root cause (e.g., vulnerable dependency, leaked secret).
3. Patch the vulnerability in the source code/Dockerfile.
4. Rebuild the image and deploy the updated version.
5. Rotate all secrets that were accessible to the compromised container.

---

## Conclusion

Securing a Docker environment is not a one-time task; it is a continuous process of auditing, hardening, and monitoring. By implementing the strategies outlined in this Super Specialist guide—from minimal base images and strict runtime constraints to robust secrets management and incident response protocols—you can build resilient, production-ready container infrastructure that withstands modern threats.

## References
[1] CIS Docker Benchmark v1.6.0
[2] NIST Special Publication 800-190: Application Container Security Guide
[3] Docker Documentation: Security


---

## 11. Advanced Troubleshooting Scenarios

As a Super Specialist, you will encounter complex issues that go beyond basic misconfigurations. Here are deep dives into common production incidents.

### Scenario A: The "Zombie" Container (High CPU, Unresponsive)

**Symptoms:** A container is consuming 100% CPU but is not responding to health checks or network requests. `docker stop` hangs indefinitely.

**Diagnosis:**
1. Identify the container PID on the host:
   ```bash
   docker inspect --format '{{.State.Pid}}' <container_name>
   ```
2. Check the process tree on the host:
   ```bash
   ps -ef | grep <PID>
   ```
3. Use `strace` to see what the process is doing (requires root on host):
   ```bash
   strace -p <PID>
   ```
   *Result:* You might see it stuck in an infinite loop of failing system calls or deadlocked waiting for a resource.

**Resolution:**
1. If `docker stop` fails, the daemon sends a SIGTERM. If the app ignores it, it waits for the grace period (default 10s) then sends SIGKILL.
2. If it's completely wedged, force kill it from the host:
   ```bash
   kill -9 <PID>
   ```
3. **Prevention:** Ensure the application handles SIGTERM correctly. Use `init: true` in `compose.yaml` to run an init process (like `tini`) that reaps zombie processes and forwards signals properly.

*compose.yaml Example:*
```yaml
services:
  app:
    image: YOUR_REGISTRY/app:v1
    init: true
    stop_grace_period: 30s
```

### Scenario B: Intermittent DNS Resolution Failures

**Symptoms:** Containers randomly fail to resolve external hostnames or internal service names. Logs show `Temporary failure in name resolution`.

**Diagnosis:**
1. Check the container's DNS configuration:
   ```bash
   docker exec <container_name> cat /etc/resolv.conf
   ```
   *Note:* Docker uses an embedded DNS server at `127.0.0.11` for user-defined networks.
2. Check host DNS resolution and firewall rules. Sometimes, aggressive firewall rules drop UDP DNS packets.
3. Monitor DNS traffic using `tcpdump` on the Docker bridge interface.

**Resolution:**
1. If the host's DNS is unstable, explicitly define reliable DNS servers in `compose.yaml` or `daemon.json`.
2. Ensure the `ndots` option in `/etc/resolv.conf` isn't causing excessive DNS queries (common in Kubernetes, but can happen in complex Compose setups).

*compose.yaml Example:*
```yaml
services:
  app:
    image: YOUR_REGISTRY/app:v1
    dns:
      - 8.8.8.8
      - 1.1.1.1
    dns_opt:
      - ndots:1
```

### Scenario C: Overlay2 Storage Driver Exhaustion

**Symptoms:** Host disk space is full. `docker system df` shows massive space used by images or local volumes. `docker system prune` doesn't free enough space.

**Diagnosis:**
1. Find the largest directories in the Docker root:
   ```bash
   sudo du -sh /var/lib/docker/* | sort -h
   ```
2. If `/var/lib/docker/overlay2` is huge, you have orphaned layers or containers writing massive amounts of data to their writable layer instead of a volume.
3. Identify containers with large writable layers:
   ```bash
   docker ps -s
   ```

**Resolution:**
1. **Immediate fix:** Stop containers and run a deep prune:
   ```bash
   docker system prune -a --volumes
   ```
2. **Root Cause Fix:** Ensure applications write logs to `stdout`/`stderr` (handled by Docker logging driver) or to mounted volumes, NEVER to the container filesystem.
3. Configure log rotation in `compose.yaml` to prevent log files from filling the disk.

*compose.yaml Example:*
```yaml
services:
  app:
    image: YOUR_REGISTRY/app:v1
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

---

## 12. Cost and Time Optimization Strategies

Efficiency is just as important as security. Bloated images and inefficient builds waste CI/CD minutes, bandwidth, and storage costs.

### 12.1 Layer Caching Optimization

Docker builds images layer by layer. If a layer changes, all subsequent layers must be rebuilt.

**Rule:** Order your Dockerfile instructions from least frequently changed to most frequently changed.

*Before (Inefficient):*
```dockerfile
FROM node:18
WORKDIR /app
COPY . .
# If ANY file in the repo changes, npm install runs again!
RUN npm install
CMD ["npm", "start"]
```

*After (Optimized):*
```dockerfile
FROM node:18
WORKDIR /app
# Copy only package files first
COPY package*.json ./
# This layer is cached unless package.json changes
RUN npm ci
# Now copy the rest of the code
COPY . .
CMD ["npm", "start"]
```

### 12.2 BuildKit Cache Mounts

For languages that use package managers (npm, pip, apt), downloading dependencies repeatedly is a massive time sink. BuildKit cache mounts solve this.

*Dockerfile Example (Python):*
```dockerfile
# syntax=docker/dockerfile:1
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
# Cache the pip download directory
RUN --mount=type=cache,target=/root/.cache/pip     pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

### 12.3 Compose Profiles for Local Development

Running a full microservices stack locally can melt a developer's laptop. Use Compose profiles to group services.

*compose.yaml Example:*
```yaml
services:
  frontend:
    image: my-frontend
    profiles: ["ui", "full"]
  backend-api:
    image: my-api
    profiles: ["api", "full"]
  database:
    image: postgres
    profiles: ["api", "full", "db-only"]
```
*Usage:* `docker compose --profile api up -d` (Starts only backend-api and database).

### 12.4 Docker Compose Watch (Hot Reloading)

Introduced in Compose V2.22.0, `watch` automatically updates running services as you edit code, eliminating the need to manually rebuild images during development.

*compose.yaml Example:*
```yaml
services:
  web:
    build: .
    command: npm run dev
    develop:
      watch:
        - action: sync
          path: ./src
          target: /app/src
        - action: rebuild
          path: package.json
```
*Usage:* `docker compose watch`

---

## 13. Comprehensive Upgrade Strategies

Upgrading containerized applications in production requires careful planning to avoid downtime.

### 13.1 Rolling Updates (Swarm)

Docker Swarm natively supports rolling updates, updating a specified number of replicas at a time.

*compose.yaml Example:*
```yaml
services:
  web:
    image: YOUR_REGISTRY/web:v2
    deploy:
      replicas: 4
      update_config:
        parallelism: 1
        delay: 10s
        order: start-first # Start new container before stopping old one
        failure_action: rollback
```

### 13.2 Blue-Green Deployments (Compose)

In a standard Docker Compose environment, you can simulate blue-green deployments using a reverse proxy (like Traefik or Nginx).

1. Run `web-blue` (v1) and route traffic to it via the proxy.
2. Deploy `web-green` (v2) alongside it.
3. Update the proxy configuration to route traffic to `web-green`.
4. Monitor for errors. If successful, tear down `web-blue`.

### 13.3 Database Migrations

Never run database migrations automatically on container startup in a multi-replica environment (race conditions).

**Best Practice:** Run migrations as a separate, short-lived container (a Kubernetes Job or a specific Compose profile) *before* updating the application containers.

```bash
# Run migration
docker compose run --rm app-migration
# If successful, update the app
docker compose up -d app
```

---

## 14. Extended Security Audit Checklist (Continued)

### Category 5: Secrets & Configuration
| ID | Check | Pass Criteria | Fail Criteria |
|---|---|---|---|
| 5.1 | Hardcoded Secrets | Source code and configs scanned; no secrets found. | API keys/passwords found in plaintext. |
| 5.2 | Environment Variables | `.env` files excluded from version control (`.gitignore`). | `.env` committed to repository. |
| 5.3 | Secret Permissions | Mounted secret files have strict permissions (e.g., 400). | Secrets readable by all users. |

### Category 6: Supply Chain & CI/CD
| ID | Check | Pass Criteria | Fail Criteria |
|---|---|---|---|
| 6.1 | Registry Access | RBAC implemented; pull-only access for production nodes. | Anonymous pull/push allowed. |
| 6.2 | SBOM Generation | SBOM generated and archived for every release. | No software bill of materials exists. |
| 6.3 | Base Image Provenance | Base images sourced from official, verified publishers. | Base images pulled from unknown personal repositories. |

### Category 7: Monitoring & Logging
| ID | Check | Pass Criteria | Fail Criteria |
|---|---|---|---|
| 7.1 | Centralized Logging | Container logs forwarded to a central SIEM/Log aggregator. | Logs only stored locally on the host. |
| 7.2 | Alerting | Alerts configured for container crashes (OOM, exit code != 0). | No proactive alerting in place. |
| 7.3 | Performance Monitoring | Metrics (CPU, Mem, Net) collected via Prometheus/cAdvisor. | No visibility into container resource usage. |

---
## Final Thoughts for the Operations Team

As a Docker Super Specialist, your role is to bridge the gap between development velocity and operational stability. Security is not a roadblock; it is a fundamental property of a well-engineered system. By enforcing these strict guidelines, utilizing the provided configurations, and understanding the deep mechanics of the Docker engine, you will ensure that your clients' infrastructure remains robust, performant, and impenetrable.

## === FILE: 49-docker-specialist.md ===
# Specialist #49: Docker Super Specialist

## Introduction

Welcome to the comprehensive guide for the Docker Super Specialist. This document serves as the ultimate reference for tech support operations teams, DevOps engineers, and system administrators tasked with optimizing, troubleshooting, and securing Docker environments. As a Docker Super Specialist, your role is not merely to write functional Dockerfiles or basic `compose.yaml` files, but to engineer robust, flaw-proof, cost-effective, and highly optimized containerized architectures. This guide covers everything from the foundational architecture of the Docker Engine to advanced BuildKit features, comprehensive Docker Compose V2 specifications, and production-ready deployment strategies.

## 1. Docker Engine Architecture Deep Dive

To effectively troubleshoot and optimize Docker, one must first understand its underlying architecture. Docker is not a monolithic application; it is a complex ecosystem of interacting components designed to manage the lifecycle of containers.

### The Docker Daemon (dockerd)

The Docker daemon (`dockerd`) is the persistent background process that manages Docker objects such as images, containers, networks, and volumes. It listens for Docker API requests and processes them. The daemon can also communicate with other daemons to manage swarm services.

### containerd

`containerd` is an industry-standard core container runtime. Originally part of the Docker daemon, it was extracted and donated to the Cloud Native Computing Foundation (CNCF). `containerd` manages the complete container lifecycle of its host system, from image transfer and storage to container execution and supervision, to low-level storage and network attachments. It acts as a bridge between the Docker daemon and the lower-level runtime (`runc`).

### runc and the OCI Specification

`runc` is a lightweight, portable container runtime that implements the Open Container Initiative (OCI) specification. It is responsible for actually creating and running containers. When `containerd` needs to start a container, it uses `runc` to interface with the Linux kernel features (namespaces, cgroups, SELinux, AppArmor) that provide container isolation. The OCI specification ensures that container images and runtimes are standardized, allowing images built with Docker to run on any OCI-compliant runtime (like Podman or CRI-O).

### Image Layers and the Union Filesystem

Docker images are built from a series of layers. Each layer represents an instruction in the image's Dockerfile. These layers are stacked on top of each other to form the final image. Docker uses a Union Filesystem (such as OverlayFS, specifically the `overlay2` storage driver) to combine these layers into a single unified view.

When a container is created from an image, Docker adds a thin, writable "container layer" on top of the underlying image layers. All changes made to the running container (such as writing new files, modifying existing files, or deleting files) are written to this thin writable container layer. The underlying image layers remain read-only. This architecture is crucial for efficiency, as multiple containers can share the same underlying image layers, saving disk space and memory.

## 2. Dockerfile Mastery: Complete Instruction Reference

A Dockerfile is the blueprint for a Docker image. Mastering its instructions is essential for creating secure, efficient, and maintainable images. Below is a comprehensive reference of Dockerfile instructions, including best and worst practices.

### FROM

The `FROM` instruction initializes a new build stage and sets the Base Image for subsequent instructions. It must be the first non-comment instruction in the Dockerfile.

**Best Practices:**
- Always pin versions (e.g., `FROM node:18.17.0-alpine` instead of `FROM node:latest`).
- Use minimal base images like Alpine, Distroless, or Scratch to reduce attack surface and image size.
- Use multi-stage builds by naming stages (e.g., `FROM golang:1.20 AS builder`).

**Worst Practices:**
- Using `latest` tags, which leads to unpredictable builds and potential breaking changes.
- Using full OS images (like `ubuntu` or `debian`) when a minimal image would suffice.

### RUN

The `RUN` instruction executes commands in a new layer on top of the current image and commits the results.

**Best Practices:**
- Consolidate multiple `RUN` commands using `&&` to reduce the number of layers.
- Clean up package manager caches in the same `RUN` instruction to prevent cache files from being committed to the layer.
- Use `--no-install-recommends` with `apt-get` to avoid installing unnecessary dependencies.

**Example (Good):**
```dockerfile
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*
```

**Example (Bad):**
```dockerfile
RUN apt-get update
RUN apt-get install -y curl
RUN apt-get install -y ca-certificates
```

### COPY and ADD

Both `COPY` and `ADD` copy files from the host to the container. However, `ADD` has additional features: it can extract local tar files and download files from remote URLs.

**Best Practices:**
- Prefer `COPY` over `ADD` unless you specifically need `ADD`'s extraction capabilities. `COPY` is more transparent.
- Order `COPY` instructions carefully. Copy dependency files (like `package.json` or `requirements.txt`) before copying the rest of the source code to leverage Docker's layer caching.

**Worst Practices:**
- Using `ADD` to download remote files. It's better to use `RUN curl` or `wget` and clean up the downloaded archive in the same layer.
- Copying the entire directory (`COPY . .`) before installing dependencies, which invalidates the cache every time any file changes.

### CMD and ENTRYPOINT

`CMD` provides defaults for an executing container, while `ENTRYPOINT` configures a container that will run as an executable.

**Best Practices:**
- Use the exec form (JSON array) for both `CMD` and `ENTRYPOINT` (e.g., `CMD ["executable","param1","param2"]`). The shell form (`CMD command param1`) wraps the command in `/bin/sh -c`, which can cause issues with signal handling (like SIGTERM).
- Use `ENTRYPOINT` for the main executable and `CMD` for default arguments.

**Example:**
```dockerfile
ENTRYPOINT ["python", "app.py"]
CMD ["--port", "8080"]
```

### ENV and ARG

`ENV` sets environment variables that persist in the final image and running container. `ARG` defines variables that users can pass at build-time to the builder with the `docker build` command using the `--build-arg <varname>=<value>` flag. `ARG` variables do not persist in the final image.

**Best Practices:**
- Use `ENV` for configuration that the application needs at runtime.
- Use `ARG` for build-time configuration, such as specifying a version number to download.

**Worst Practices:**
- Storing secrets (passwords, API keys) in `ENV` or `ARG`. These values are visible in the image history (`docker history`). Use BuildKit secrets or Docker Compose secrets instead.

### EXPOSE

The `EXPOSE` instruction informs Docker that the container listens on the specified network ports at runtime. It does not actually publish the port.

**Best Practices:**
- Always document the intended ports using `EXPOSE`.
- Specify the protocol if necessary (e.g., `EXPOSE 80/udp`).

### VOLUME

The `VOLUME` instruction creates a mount point with the specified name and marks it as holding externally mounted volumes from native host or other containers.

**Best Practices:**
- Use `VOLUME` to declare directories that will hold persistent or shared data.

**Worst Practices:**
- Relying on `VOLUME` in the Dockerfile for critical data persistence without explicitly mapping it in `compose.yaml` or `docker run`. Data written to an anonymous volume is difficult to manage and can be lost if the container is removed.

### USER

The `USER` instruction sets the user name (or UID) and optionally the user group (or GID) to use when running the image and for any `RUN`, `CMD` and `ENTRYPOINT` instructions that follow it in the Dockerfile.

**Best Practices:**
- Always run containers as a non-root user for security.
- Use numeric UIDs instead of usernames to avoid issues with Kubernetes security contexts.

**Example:**
```dockerfile
RUN groupadd -r appgroup && useradd -r -g appgroup -u 1001 appuser
USER 1001:1001
```

### WORKDIR

The `WORKDIR` instruction sets the working directory for any `RUN`, `CMD`, `ENTRYPOINT`, `COPY` and `ADD` instructions that follow it in the Dockerfile.

**Best Practices:**
- Always use absolute paths for `WORKDIR`.
- Use `WORKDIR` instead of proliferating instructions like `RUN cd ... && do-something`.

### HEALTHCHECK

The `HEALTHCHECK` instruction tells Docker how to test a container to check that it is still working.

**Best Practices:**
- Always include a `HEALTHCHECK` to allow orchestrators (like Docker Swarm or Kubernetes) to know when a container is ready to receive traffic or needs to be restarted.

**Example:**
```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost/health || exit 1
```

### SHELL

The `SHELL` instruction allows the default shell used for the shell form of commands to be overridden.

**Best Practices:**
- Use `SHELL` on Windows to switch between `cmd` and `powershell`.
- Use `SHELL ["/bin/bash", "-c"]` on Linux if you need bash-specific features in your `RUN` commands.

### LABEL

The `LABEL` instruction adds metadata to an image.

**Best Practices:**
- Use OCI standard labels (e.g., `org.opencontainers.image.source`, `org.opencontainers.image.version`) to provide consistent metadata.

### STOPSIGNAL

The `STOPSIGNAL` instruction sets the system call signal that will be sent to the container to exit.

**Best Practices:**
- Use `STOPSIGNAL` if your application requires a specific signal to shut down gracefully (e.g., `STOPSIGNAL SIGINT`).

### ONBUILD

The `ONBUILD` instruction adds to the image a trigger instruction to be executed at a later time, when the image is used as the base for another build.

**Best Practices:**
- Use `ONBUILD` sparingly, as it can make builds unpredictable for users of your base image. Document its usage clearly.

## 3. Multi-stage Builds: Patterns and Optimization

Multi-stage builds are a crucial technique for creating minimal, secure Docker images. They allow you to use multiple `FROM` statements in your Dockerfile. Each `FROM` instruction can use a different base, and each of them begins a new stage of the build. You can selectively copy artifacts from one stage to another, leaving behind everything you don't want in the final image.

### Go Pattern

Go applications compile to a single static binary, making them perfect candidates for multi-stage builds.

**Before (Single Stage):**
```dockerfile
FROM golang:1.20
WORKDIR /app
COPY . .
RUN go build -o main .
CMD ["./main"]
```
*Size: ~800MB*

**After (Multi-stage with Scratch):**
```dockerfile
# Stage 1: Build
FROM golang:1.20-alpine AS builder
WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .
# Build a statically linked binary
RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o main .

# Stage 2: Runtime
FROM scratch
WORKDIR /app
# Copy CA certificates for HTTPS requests
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
COPY --from=builder /app/main .
ENTRYPOINT ["./main"]
```
*Size: ~15MB (Massive reduction, no OS vulnerabilities)*

### Node.js Pattern

Node.js applications require the Node runtime, but you don't need the build tools (like `node-gyp` or Python) in the final image.

**Before (Single Stage):**
```dockerfile
FROM node:18
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build
CMD ["npm", "start"]
```
*Size: ~1GB*

**After (Multi-stage with Alpine):**
```dockerfile
# Stage 1: Build
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Stage 2: Runtime
FROM node:18-alpine
WORKDIR /app
ENV NODE_ENV=production
COPY package*.json ./
# Install only production dependencies
RUN npm ci --only=production && npm cache clean --force
COPY --from=builder /app/dist ./dist
USER node
CMD ["node", "dist/main.js"]
```
*Size: ~150MB*

### Python Pattern

Python applications often require C compilers for dependencies (like `psycopg2` or `numpy`), which shouldn't be in the final image.

**Before (Single Stage):**
```dockerfile
FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```
*Size: ~900MB*

**After (Multi-stage with Slim and Wheels):**
```dockerfile
# Stage 1: Build wheels
FROM python:3.11-slim AS builder
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends gcc libpq-dev
COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends libpq5 \
    && rm -rf /var/lib/apt/lists/*
COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requirements.txt .
RUN pip install --no-cache /wheels/*
COPY . .
RUN useradd -m appuser
USER appuser
CMD ["python", "app.py"]
```
*Size: ~180MB*

### Java Pattern

Java applications require a JDK to build but only a JRE to run.

**Before (Single Stage):**
```dockerfile
FROM maven:3.8-openjdk-17
WORKDIR /app
COPY . .
RUN mvn clean package
CMD ["java", "-jar", "target/app.jar"]
```
*Size: ~600MB*

**After (Multi-stage with JRE):**
```dockerfile
# Stage 1: Build
FROM maven:3.8-eclipse-temurin-17 AS builder
WORKDIR /app
COPY pom.xml .
# Cache dependencies
RUN mvn dependency:go-offline
COPY src ./src
RUN mvn clean package -DskipTests

# Stage 2: Runtime
FROM eclipse-temurin:17-jre-alpine
WORKDIR /app
COPY --from=builder /app/target/*.jar app.jar
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
USER appuser
CMD ["java", "-jar", "app.jar"]
```
*Size: ~120MB*

### Rust Pattern

Similar to Go, Rust compiles to a static binary.

**Before (Single Stage):**
```dockerfile
FROM rust:1.70
WORKDIR /app
COPY . .
RUN cargo build --release
CMD ["./target/release/myapp"]
```
*Size: ~1.5GB*

**After (Multi-stage with Distroless):**
```dockerfile
# Stage 1: Build
FROM rust:1.70 AS builder
WORKDIR /app
COPY Cargo.toml Cargo.lock ./
# Dummy build to cache dependencies
RUN mkdir src && echo "fn main() {}" > src/main.rs
RUN cargo build --release
RUN rm -rf src
COPY src ./src
# Touch main.rs to force rebuild
RUN touch src/main.rs
RUN cargo build --release

# Stage 2: Runtime
FROM gcr.io/distroless/cc-debian12
WORKDIR /app
COPY --from=builder /app/target/release/myapp .
CMD ["./myapp"]
```
*Size: ~30MB*

## 4. Base Image Selection Guide

Choosing the right base image is the foundation of a secure and optimized Docker container. The choice impacts image size, security posture, debugging capabilities, and application compatibility.

### Comparison Table

| Base Image Type | Typical Size | Security Surface | Debugging Tools | Compatibility | Best For |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Scratch** | 0 MB | None (Empty) | None | Statically linked binaries only | Go, Rust, C/C++ (static) |
| **Distroless** | 2-20 MB | Extremely Low | Minimal (no shell) | Language-specific runtimes | Java, Node.js, Python, Go |
| **Alpine** | ~5 MB | Low | `sh`, `apk` | `musl` libc (can cause issues) | General purpose, minimal |
| **Slim (Debian)** | ~30-50 MB | Medium | `bash`, `apt` | `glibc` (standard) | Python, Node.js, Ruby |
| **Full (Ubuntu/Debian)** | 100-200+ MB | High | Full OS tools | Maximum compatibility | Legacy apps, complex deps |

### Scratch

`scratch` is an explicitly empty image. It is the starting point for building all other images.

- **Pros:** Zero size, zero attack surface.
- **Cons:** No shell, no package manager, no CA certificates (unless copied).
- **When to use:** When you have a statically compiled binary (like Go or Rust) that has no external dependencies.

### Distroless

Distroless images (maintained by Google) contain only your application and its runtime dependencies. They do not contain package managers, shells, or any other programs you would expect to find in a standard Linux distribution.

- **Pros:** Extremely secure (no shell means attackers cannot easily execute commands if they compromise the app), very small size.
- **Cons:** Difficult to debug (no `sh` or `bash` to `docker exec` into).
- **When to use:** Production deployments of applications written in Java, Node.js, Python, or Go where security is paramount.

### Alpine

Alpine Linux is a security-oriented, lightweight Linux distribution based on `musl` libc and `busybox`.

- **Pros:** Very small size (~5MB), includes a package manager (`apk`).
- **Cons:** Uses `musl` instead of `glibc`. This can cause compatibility issues with applications or libraries compiled against `glibc` (common in Python data science libraries like `numpy` or `pandas`).
- **When to use:** General-purpose minimal images where `musl` compatibility is not an issue.

### Slim

Slim images (e.g., `debian:bullseye-slim`, `python:3.11-slim`) are stripped-down versions of standard distributions.

- **Pros:** Standard `glibc` compatibility, smaller than full images, includes standard tools (`apt`, `bash`).
- **Cons:** Larger than Alpine or Distroless, larger attack surface.
- **When to use:** When you need `glibc` compatibility (e.g., Python applications with C extensions) but want to minimize size.

### Full

Full images (e.g., `ubuntu:22.04`, `node:18`) contain a complete operating system environment.

- **Pros:** Maximum compatibility, all debugging tools available.
- **Cons:** Very large size, massive attack surface (many unnecessary packages with potential vulnerabilities).
- **When to use:** Only during development or for legacy applications that require a full OS environment. Never recommended for production.

## 5. Layer Optimization Strategies

Docker images are built layer by layer. Optimizing these layers is critical for reducing build times, minimizing image size, and maximizing cache hits.

### Ordering Strategy

Docker caches each layer. If a layer changes, Docker must rebuild that layer and all subsequent layers. Therefore, the golden rule of layer ordering is: **Order instructions from least frequently changed to most frequently changed.**

1. **Base Image:** `FROM` (Rarely changes)
2. **System Dependencies:** `RUN apt-get install...` (Infrequently changes)
3. **Application Dependencies:** `COPY package.json` -> `RUN npm install` (Changes occasionally)
4. **Application Code:** `COPY . .` (Changes constantly)

### Cache Invalidation Rules

- For `RUN` instructions, the cache is invalidated if the command string changes.
- For `COPY` and `ADD` instructions, Docker calculates a checksum of the files being copied. If the checksum changes (i.e., a file was modified), the cache is invalidated.
- Once a layer's cache is invalidated, all subsequent layers are also invalidated.

### RUN Consolidation

Every `RUN` instruction creates a new layer. To minimize the number of layers and reduce image size, consolidate related commands using `&&`.

**Bad (Creates 3 layers):**
```dockerfile
RUN apt-get update
RUN apt-get install -y curl
RUN rm -rf /var/lib/apt/lists/*
```

**Good (Creates 1 layer):**
```dockerfile
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
```

### .dockerignore Patterns

The `.dockerignore` file is essential for preventing unnecessary files from being sent to the Docker daemon (the build context) and copied into the image. This speeds up the build process and reduces image size.

**Standard `.dockerignore` template:**
```text
# Git
.git
.gitignore

# Node
node_modules
npm-debug.log

# Python
__pycache__
*.pyc
*.pyo
*.pyd
.Python
env/
venv/

# Docker
Dockerfile
.dockerignore
compose.yaml

# Secrets
.env
*.pem
*.key
```

## 6. BuildKit Features

BuildKit is the modern build subsystem for Docker (default since Docker 23.0). It offers significant performance improvements and advanced features over the legacy builder.

### Cache Mounts

Cache mounts allow you to cache directories between builds, which is incredibly useful for package managers like `pip`, `npm`, or `apt`. This prevents re-downloading dependencies if the cache is invalidated.

**Example (npm cache):**
```dockerfile
# syntax=docker/dockerfile:1
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
# Mount the npm cache directory
RUN --mount=type=cache,target=/root/.npm \
    npm ci
COPY . .
CMD ["npm", "start"]
```

### Build Secrets

Never pass secrets (like SSH keys or API tokens) using `ARG` or `ENV`, as they will be baked into the image history. Use BuildKit secrets instead.

**Dockerfile:**
```dockerfile
# syntax=docker/dockerfile:1
FROM alpine
# Mount the secret and use it in a command
RUN --mount=type=secret,id=mysecret \
    cat /run/secrets/mysecret > /tmp/secret_copy
```

**Build Command:**
```bash
docker build --secret id=mysecret,src=mysecret.txt .
```

### SSH Forwarding

If your build needs to access private repositories (e.g., private GitHub repos), use SSH forwarding instead of copying SSH keys into the image.

**Dockerfile:**
```dockerfile
# syntax=docker/dockerfile:1
FROM alpine
RUN apk add --no-cache openssh-client git
# Add github to known hosts
RUN mkdir -p -m 0700 ~/.ssh && ssh-keyscan github.com >> ~/.ssh/known_hosts
# Mount the SSH agent socket
RUN --mount=type=ssh \
    git clone git@github.com:myorg/myprivaterepo.git
```

**Build Command:**
```bash
docker build --ssh default .
```

### Multi-platform Builds with buildx

BuildKit allows you to build images for multiple architectures (e.g., `amd64` and `arm64`) simultaneously using `docker buildx`.

**Command:**
```bash
docker buildx build --platform linux/amd64,linux/arm64 -t myrepo/myimage:latest --push .
```

### Inline Cache

You can embed cache metadata into the image itself, allowing subsequent builds (even on different machines, like in CI/CD) to use the image as a cache source.

**Build Command (to create the cache):**
```bash
docker build --build-arg BUILDKIT_INLINE_CACHE=1 -t myrepo/myimage:latest .
```

**Build Command (to use the cache):**
```bash
docker build --cache-from myrepo/myimage:latest -t myrepo/myimage:latest .
```

### Named Contexts

Named contexts allow you to pass additional build contexts (like other images or local directories) to your build.

**Command:**
```bash
docker build --build-context project2=../project2 .
```

**Dockerfile:**
```dockerfile
FROM alpine
COPY --from=project2 . /project2
```

## 7. Docker Compose V2 Complete Specification

Docker Compose V2 is a complete rewrite of the original Python-based `docker-compose` in Go. It is now integrated directly into the Docker CLI as `docker compose`.

### Top-Level Elements

A `compose.yaml` file consists of several top-level elements:

- **`services`:** Defines the containers to be run.
- **`networks`:** Defines the networks the services will connect to.
- **`volumes`:** Defines the persistent volumes to be used by the services.
- **`configs`:** Defines configuration files to be mounted into containers.
- **`secrets`:** Defines sensitive data to be securely mounted into containers.
- **`name`:** (Optional) Sets the project name, overriding the directory name.

*Note: The `version` field is deprecated in Compose V2 and should be omitted.*

### Advanced Compose Features

- **Fragments (YAML Anchors):** Use `&` to define an anchor and `*` to reference it, allowing you to reuse configuration blocks.
- **Extensions (`x-`):** Any top-level field starting with `x-` is ignored by Compose. This is useful for defining anchors that don't belong to a specific service.
- **Interpolation:** Use `${VAR}` to inject environment variables from the host or a `.env` file into the Compose file.
- **Merge (`<<`):** Merge an anchor into a dictionary.
- **Include:** Use the `include` top-level element to pull in other Compose files, making it easier to manage large projects.
- **Profiles:** Assign services to profiles (e.g., `profiles: ["dev", "debug"]`). Services with profiles are only started if that profile is explicitly activated via the `--profile` flag or the `COMPOSE_PROFILES` environment variable.

### Service Attributes (Complete List)

Here is a comprehensive list of service attributes available in Compose V2:

`annotations`, `attach`, `build`, `blkio_config`, `cpu_count`, `cpu_percent`, `cpu_shares`, `cpu_period`, `cpu_quota`, `cpu_rt_runtime`, `cpu_rt_period`, `cpus`, `cpuset`, `cap_add`, `cap_drop`, `cgroup`, `cgroup_parent`, `command`, `configs`, `container_name`, `credential_spec`, `depends_on`, `deploy`, `develop`, `device_cgroup_rules`, `devices`, `dns`, `dns_opt`, `dns_search`, `domainname`, `entrypoint`, `env_file`, `environment`, `expose`, `extends`, `external_links`, `extra_hosts`, `group_add`, `healthcheck`, `hostname`, `image`, `init`, `ipc`, `isolation`, `labels`, `links`, `logging`, `mac_address`, `mem_limit`, `mem_reservation`, `mem_swappiness`, `memswap_limit`, `network_mode`, `networks`, `oom_kill_disable`, `oom_score_adj`, `pid`, `pids_limit`, `platform`, `ports`, `privileged`, `profiles`, `pull_policy`, `read_only`, `restart`, `runtime`, `scale`, `secrets`, `security_opt`, `shm_size`, `stdin_open`, `stop_grace_period`, `stop_signal`, `storage_opt`, `sysctls`, `tmpfs`, `tty`, `ulimits`, `user`, `userns_mode`, `uts`, `volumes`, `volumes_from`, `working_dir`.

## 8. Docker Compose Flaw-Proof Production Template

This template demonstrates a highly secure, production-ready `compose.yaml` file incorporating all best practices: non-root execution, read-only filesystems, capability dropping, resource limits, health checks, and secure networking.

```yaml
# compose.yaml
name: production-app

# Extension block for common security settings
x-security-opts: &security-opts
  security_opt:
    - no-new-privileges:true
  cap_drop:
    - ALL
  read_only: true

# Extension block for common logging settings
x-logging-opts: &logging-opts
  logging:
    driver: "json-file"
    options:
      max-size: "10m"
      max-file: "3"

services:
  api:
    image: YOUR_REGISTRY/api:v1.2.3
    container_name: prod-api
    restart: unless-stopped
    init: true # Use init process to handle signals properly
    user: "1001:1001" # Run as non-root
    <<: *security-opts
    <<: *logging-opts
    ports:
      - "8080:8080"
    environment:
      - NODE_ENV=production
      - DB_HOST=db
    secrets:
      - db_password
    networks:
      - backend
    depends_on:
      db:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 10s
    deploy:
      resources:
        limits:
          cpus: '0.50'
          memory: 512M
        reservations:
          cpus: '0.25'
          memory: 256M
    stop_grace_period: 30s

  db:
    image: postgres:15-alpine
    container_name: prod-db
    restart: unless-stopped
    user: "70:70" # Postgres user in alpine
    <<: *security-opts
    <<: *logging-opts
    environment:
      POSTGRES_USER: appuser
      POSTGRES_PASSWORD_FILE: /run/secrets/db_password
      POSTGRES_DB: appdb
    secrets:
      - db_password
    volumes:
      - db_data:/var/lib/postgresql/data
      # Mount run directory as tmpfs for postgres lock files when read_only is true
      - type: tmpfs
        target: /var/run/postgresql
    networks:
      - backend
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U appuser -d appdb"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 10s
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 1G

networks:
  backend:
    driver: bridge
    internal: true # No external access to this network

volumes:
  db_data:
    driver: local

secrets:
  db_password:
    file: ./secrets/db_password.txt
```

## 9. Health Check Patterns for Common Services

Health checks are critical for ensuring that dependent services only start when their dependencies are truly ready, and for orchestrators to know when to restart a failing container.

### PostgreSQL
```yaml
healthcheck:
  test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER} -d ${POSTGRES_DB}"]
  interval: 10s
  timeout: 5s
  retries: 5
```

### MongoDB
```yaml
healthcheck:
  test: ["CMD", "mongosh", "--eval", "db.adminCommand('ping')"]
  interval: 10s
  timeout: 5s
  retries: 5
```

### Redis
```yaml
healthcheck:
  test: ["CMD", "redis-cli", "ping"]
  interval: 10s
  timeout: 5s
  retries: 5
```

### RabbitMQ
```yaml
healthcheck:
  test: ["CMD", "rabbitmq-diagnostics", "-q", "ping"]
  interval: 30s
  timeout: 10s
  retries: 3
```

### Nginx
```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost/"]
  interval: 30s
  timeout: 10s
  retries: 3
```

### Node.js / Go / Java (HTTP API)
```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 15s # Allow time for JVM/Node startup
```

## 10. Networking Deep Dive

Docker's networking subsystem is pluggable, using drivers. Understanding these drivers is essential for designing secure and performant container architectures.

### Network Drivers

- **`bridge`:** The default network driver. If you don't specify a driver, this is what you're creating. Bridge networks are usually used when your applications run in standalone containers that need to communicate. Docker Compose creates a custom bridge network for your project by default, providing automatic DNS resolution between containers using their service names.
- **`host`:** For standalone containers, remove network isolation between the container and the Docker host, and use the host's networking directly. Port mapping (`-p`) has no effect. This is useful for optimizing performance (bypassing NAT) or for applications that need to manage a large range of ports.
- **`overlay`:** Overlay networks connect multiple Docker daemons together and enable swarm services to communicate with each other. You can also use overlay networks to facilitate communication between a swarm service and a standalone container, or between two standalone containers on different Docker daemons.
- **`macvlan`:** Macvlan networks allow you to assign a MAC address to a container, making it appear as a physical device on your network. The Docker daemon routes traffic to containers by their MAC addresses. This is useful for legacy applications that expect to be directly connected to the physical network.
- **`ipvlan`:** Similar to `macvlan`, but containers share the same MAC address as the host interface. This is useful in environments where the network switch restricts the number of MAC addresses per port.
- **`none`:** Disables all networking for the container. Usually used in conjunction with a custom network driver.

### Internal Networks

For enhanced security, you can define a network as `internal: true`. This creates a bridge network that has no default gateway, meaning containers on this network cannot access the internet, nor can they be accessed from the internet. This is perfect for backend databases or internal microservices.

```yaml
networks:
  backend:
    internal: true
```

## 11. Volume Management

Data persistence in Docker is handled through volumes and bind mounts.

### Named Volumes

Named volumes are managed entirely by Docker (usually stored in `/var/lib/docker/volumes/` on Linux). They are the preferred mechanism for persisting data generated by and used by Docker containers.

- **Pros:** Easy to back up or migrate, managed via Docker CLI, work on both Linux and Windows containers, can be safely shared among multiple containers.
- **Cons:** Abstracted from the host filesystem, making direct manipulation slightly harder.

### Bind Mounts

Bind mounts map a specific file or directory on the host machine into a container.

- **Pros:** Very performant, easy to access files from the host (useful for development).
- **Cons:** Ties the container to a specific host filesystem structure, potential permission issues (especially between Linux hosts and containers running as non-root).

### tmpfs Mounts

A `tmpfs` mount is temporary and only stored in the host's memory. When the container stops, the `tmpfs` mount is removed, and files written there won't be persisted.

- **Pros:** Fast, secure (data is never written to disk).
- **Cons:** Data is lost when the container stops.
- **When to use:** For sensitive data (like secrets or keys) that you don't want persisted, or for applications that write a lot of temporary state.

## 12. Logging Configuration

By default, Docker uses the `json-file` logging driver, which captures standard output and standard error and writes them to a JSON file on the host. Without configuration, these files can grow indefinitely and consume all host disk space.

### Production Logging Configuration

Always configure log rotation for the `json-file` driver, either globally in `/etc/docker/daemon.json` or per-service in `compose.yaml`.

```yaml
logging:
  driver: "json-file"
  options:
    max-size: "10m" # Rotate after 10 megabytes
    max-file: "3"   # Keep a maximum of 3 files
```

### Alternative Logging Drivers

For centralized logging, Docker supports several other drivers:
- **`syslog`:** Routes logs to a syslog server.
- **`journald`:** Writes logs to the `systemd` journal.
- **`fluentd`:** Sends logs to a Fluentd daemon.
- **`awslogs`:** Sends logs to Amazon CloudWatch Logs.
- **`gcplogs`:** Sends logs to Google Cloud Logging.

## 13. Cost and Time Optimization Strategies

Optimizing Docker environments saves both compute costs (storage, bandwidth) and developer time (build speed, CI/CD pipeline duration).

### Image Size Reduction Checklist

1. **Use Minimal Base Images:** Switch from `ubuntu` to `alpine` or `distroless`.
2. **Multi-stage Builds:** Never ship build tools (compilers, headers) in production images.
3. **Consolidate RUN Commands:** Chain commands with `&&` to reduce layers.
4. **Clean Up Caches:** Remove `apt` or `apk` caches in the same layer they are used.
5. **Use .dockerignore:** Prevent unnecessary files from entering the build context.

### Build Time Optimization

1. **Layer Ordering:** Put the most frequently changing instructions (like `COPY . .`) at the very end of the Dockerfile.
2. **BuildKit Cache Mounts:** Use `--mount=type=cache` for package managers to avoid re-downloading dependencies.
3. **Parallel Builds:** Use `docker compose build --parallel` to build multiple services concurrently.
4. **CI/CD Caching:** Use inline caching (`--build-arg BUILDKIT_INLINE_CACHE=1`) or registry caching (`--cache-from`) in your CI pipelines.

### Registry Optimization

1. **Pull-Through Cache:** Set up a local registry as a pull-through cache to reduce bandwidth usage and speed up image pulls across your infrastructure.
2. **Image Pull Policy:** Use `pull_policy: if_not_present` in Compose to avoid unnecessary API calls to the registry.

## 14. Docker Compose for Databases

Running databases in Docker requires careful configuration of persistence, networking, and health checks.

### PostgreSQL with Replication (Example)

```yaml
services:
  postgres-primary:
    image: postgres:15
    environment:
      POSTGRES_USER: repl_user
      POSTGRES_PASSWORD: repl_password
      POSTGRES_DB: myapp
    volumes:
      - pg_primary_data:/var/lib/postgresql/data
      - ./init-primary.sh:/docker-entrypoint-initdb.d/init.sh
    networks:
      - db_net

  postgres-replica:
    image: postgres:15
    environment:
      POSTGRES_USER: repl_user
      POSTGRES_PASSWORD: repl_password
    volumes:
      - pg_replica_data:/var/lib/postgresql/data
      - ./init-replica.sh:/docker-entrypoint-initdb.d/init.sh
    depends_on:
      - postgres-primary
    networks:
      - db_net

volumes:
  pg_primary_data:
  pg_replica_data:

networks:
  db_net:
    internal: true
```

### Redis Sentinel/Cluster

For high availability, Redis should be deployed using Sentinel or Cluster mode. This typically involves multiple Redis nodes and Sentinel nodes monitoring them, all communicating over an internal Docker network.

## 15. Complete Multi-Stage Build Patterns by Language

Multi-stage builds are the single most impactful optimization technique. Below are complete, production-ready Dockerfiles for every major language, showing the before (naive) and after (optimized) approach.

### Go Application

**Before (Naive) — 1.2 GB:**
```dockerfile
FROM golang:1.22
WORKDIR /app
COPY . .
RUN go build -o server .
CMD ["./server"]
```

**After (Optimized) — 12 MB:**
```dockerfile
# syntax=docker/dockerfile:1
FROM golang:1.22-alpine AS builder
WORKDIR /app

# Copy dependency files first for cache
COPY go.mod go.sum ./
RUN --mount=type=cache,target=/go/pkg/mod \
    go mod download

# Copy source and build
COPY . .
RUN --mount=type=cache,target=/go/pkg/mod \
    --mount=type=cache,target=/root/.cache/go-build \
    CGO_ENABLED=0 GOOS=linux GOARCH=amd64 \
    go build -ldflags='-w -s -extldflags "-static"' -o /server .

# Runtime stage — scratch for smallest possible image
FROM scratch
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
COPY --from=builder /server /server
USER 65534:65534
EXPOSE 8080
ENTRYPOINT ["/server"]
```

**Key optimizations:** CGO_ENABLED=0 for static binary, ldflags `-w -s` to strip debug info, scratch base (no OS), cache mounts for Go module and build caches, non-root user via numeric UID.

### Node.js Application

**Before (Naive) — 1.1 GB:**
```dockerfile
FROM node:20
WORKDIR /app
COPY . .
RUN npm install
CMD ["node", "server.js"]
```

**After (Optimized) — 85 MB:**
```dockerfile
# syntax=docker/dockerfile:1
FROM node:20-alpine AS builder
WORKDIR /app

COPY package.json package-lock.json ./
RUN --mount=type=cache,target=/root/.npm \
    npm ci --only=production

# If you have a build step (TypeScript, webpack, etc.)
COPY . .
RUN npm run build

# Runtime stage
FROM node:20-alpine AS runtime
WORKDIR /app
ENV NODE_ENV=production

# Copy only production dependencies and built output
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/package.json ./

# Non-root user
RUN addgroup -g 1001 -S appgroup && \
    adduser -u 1001 -S appuser -G appgroup
USER 1001:1001

EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:3000/health || exit 1
CMD ["node", "dist/server.js"]
```

**Key optimizations:** `npm ci` for reproducible installs, cache mount for npm, separate build and runtime stages, only production dependencies in final image, `wget` instead of `curl` for healthcheck (available in alpine), non-root user.

### Python Application

**Before (Naive) — 1.0 GB:**
```dockerfile
FROM python:3.12
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "app.py"]
```

**After (Optimized) — 120 MB:**
```dockerfile
# syntax=docker/dockerfile:1
FROM python:3.12-slim AS builder
WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc libpq-dev && rm -rf /var/lib/apt/lists/*

# Install Python dependencies into a virtual environment
COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip \
    python -m venv /opt/venv && \
    /opt/venv/bin/pip install --no-compile -r requirements.txt

# Runtime stage
FROM python:3.12-slim AS runtime
WORKDIR /app

# Install only runtime libraries (no gcc)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 curl && rm -rf /var/lib/apt/lists/*

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY . .

RUN adduser --disabled-password --gecos '' --uid 1001 appuser
USER 1001:1001

EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "app:app"]
```

**Key optimizations:** Slim base (not alpine, avoids musl issues with C extensions), virtual environment copied between stages, build tools only in builder stage, pip cache mount, gunicorn for production.

### Java (Spring Boot) Application

**Before (Naive) — 800 MB:**
```dockerfile
FROM openjdk:17
COPY target/app.jar /app.jar
CMD ["java", "-jar", "/app.jar"]
```

**After (Optimized) — 200 MB:**
```dockerfile
# syntax=docker/dockerfile:1
FROM eclipse-temurin:17-jdk-alpine AS builder
WORKDIR /app

COPY pom.xml mvnw ./
COPY .mvn .mvn
RUN --mount=type=cache,target=/root/.m2 \
    ./mvnw dependency:go-offline

COPY src src
RUN --mount=type=cache,target=/root/.m2 \
    ./mvnw package -DskipTests && \
    java -Djarmode=layertools -jar target/*.jar extract --destination /extracted

# Runtime stage with JRE only
FROM eclipse-temurin:17-jre-alpine AS runtime
WORKDIR /app

# Copy Spring Boot layers in order of change frequency
COPY --from=builder /extracted/dependencies/ ./
COPY --from=builder /extracted/spring-boot-loader/ ./
COPY --from=builder /extracted/snapshot-dependencies/ ./
COPY --from=builder /extracted/application/ ./

RUN addgroup -g 1001 -S appgroup && \
    adduser -u 1001 -S appuser -G appgroup
USER 1001:1001

EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=10s --retries=3 --start-period=60s \
    CMD wget --no-verbose --tries=1 --spider http://localhost:8080/actuator/health || exit 1
ENTRYPOINT ["java", "-XX:+UseContainerSupport", "-XX:MaxRAMPercentage=75.0", "org.springframework.boot.loader.launch.JarLauncher"]
```

**Key optimizations:** JDK for build, JRE for runtime, Spring Boot layered extraction for optimal caching, Maven cache mount, container-aware JVM flags (`UseContainerSupport`, `MaxRAMPercentage`), long `start_period` for JVM warmup.

### Rust Application

**Before (Naive) — 1.5 GB:**
```dockerfile
FROM rust:1.77
WORKDIR /app
COPY . .
RUN cargo build --release
CMD ["./target/release/myapp"]
```

**After (Optimized) — 8 MB:**
```dockerfile
# syntax=docker/dockerfile:1
FROM rust:1.77-alpine AS builder
RUN apk add --no-cache musl-dev
WORKDIR /app

# Cache dependencies by building a dummy project first
RUN cargo init --name myapp
COPY Cargo.toml Cargo.lock ./
RUN --mount=type=cache,target=/usr/local/cargo/registry \
    --mount=type=cache,target=/app/target \
    cargo build --release

# Now copy real source and rebuild (only app code recompiles)
COPY src src
RUN --mount=type=cache,target=/usr/local/cargo/registry \
    --mount=type=cache,target=/app/target \
    cargo build --release && \
    cp target/release/myapp /myapp

FROM scratch
COPY --from=builder /myapp /myapp
USER 65534:65534
ENTRYPOINT ["/myapp"]
```

**Key optimizations:** Alpine with musl for static linking, dependency caching trick (build dummy project first), cargo registry and target caches, scratch final image.

### Base Image Comparison Table

| Base Image | Size | Shell | Package Manager | glibc | Security Score | Best For |
|---|---|---|---|---|---|---|
| `scratch` | 0 MB | No | No | No | Excellent | Go, Rust static binaries |
| `gcr.io/distroless/static` | 2 MB | No | No | No | Excellent | Go, Rust static binaries |
| `gcr.io/distroless/base` | 20 MB | No | No | Yes | Excellent | C/C++ apps |
| `gcr.io/distroless/java17` | 220 MB | No | No | Yes | Excellent | Java apps |
| `gcr.io/distroless/nodejs20` | 130 MB | No | No | Yes | Excellent | Node.js apps |
| `gcr.io/distroless/python3` | 50 MB | No | No | Yes | Excellent | Python apps |
| `alpine:3.19` | 7 MB | Yes | apk | No (musl) | Very Good | General purpose |
| `debian:bookworm-slim` | 80 MB | Yes | apt | Yes | Good | Python with C extensions |
| `ubuntu:24.04` | 78 MB | Yes | apt | Yes | Fair | Development, legacy |
| `node:20-alpine` | 180 MB | Yes | apk+npm | No (musl) | Good | Node.js |
| `python:3.12-slim` | 150 MB | Yes | apt+pip | Yes | Good | Python |
| `golang:1.22-alpine` | 260 MB | Yes | apk+go | No (musl) | Good | Go (build stage only) |

## 16. Docker Compose depends_on Deep Dive

The `depends_on` attribute controls service startup and shutdown order. In Compose V2, it supports conditions that make it far more powerful than the simple ordering of V1.

### Short Syntax (Order Only)

```yaml
services:
  web:
    depends_on:
      - db
      - redis
```

This only ensures `db` and `redis` containers are **started** before `web`. It does NOT wait for them to be **ready**.

### Long Syntax (With Conditions)

```yaml
services:
  web:
    depends_on:
      db:
        condition: service_healthy
        restart: true
      redis:
        condition: service_healthy
      migrations:
        condition: service_completed_successfully
```

**Conditions explained:**

| Condition | Behavior |
|---|---|
| `service_started` | Default. Waits for the container to start (not ready). |
| `service_healthy` | Waits for the container's healthcheck to report healthy. Requires a `healthcheck` on the dependency. |
| `service_completed_successfully` | Waits for the container to run and exit with code 0. Perfect for init/migration containers. |

**The `restart: true` flag** (Compose 2.22+): When set, if the dependency restarts, the dependent service is also restarted. This is critical for database connections — if PostgreSQL restarts, your API service should also restart to re-establish connections.

### Init Container Pattern

Use `service_completed_successfully` to run database migrations before starting the application:

```yaml
services:
  migrations:
    image: YOUR_REGISTRY/api:v1.2.3
    command: ["./migrate", "up"]
    environment:
      DATABASE_URL: postgres://user:pass@db:5432/myapp
    depends_on:
      db:
        condition: service_healthy
    # No restart — this is a one-shot container
    restart: "no"

  api:
    image: YOUR_REGISTRY/api:v1.2.3
    depends_on:
      migrations:
        condition: service_completed_successfully
      db:
        condition: service_healthy
    restart: unless-stopped
```

## 17. Docker Compose Secrets and Configs

### Secrets

Secrets provide a mechanism to securely pass sensitive data to containers without exposing them in environment variables or the Compose file.

```yaml
services:
  api:
    image: myapi:latest
    secrets:
      - db_password
      - api_key
    environment:
      # Reference the secret file path, not the value
      DB_PASSWORD_FILE: /run/secrets/db_password

secrets:
  db_password:
    file: ./secrets/db_password.txt    # From a file
  api_key:
    environment: "API_KEY"              # From host env var (Compose 2.23+)
```

Inside the container, secrets are mounted at `/run/secrets/<secret_name>` as read-only files. Applications must be designed to read from files (many databases support `*_FILE` environment variables natively, like PostgreSQL and MySQL).

### Configs

Configs are similar to secrets but for non-sensitive configuration files:

```yaml
services:
  nginx:
    image: nginx:alpine
    configs:
      - source: nginx_conf
        target: /etc/nginx/nginx.conf
        mode: 0444

configs:
  nginx_conf:
    file: ./nginx/nginx.conf
```

## 18. Docker Compose Environment Variable Management

Environment variables are the primary configuration mechanism for containerized applications. Docker Compose provides multiple ways to set them, with a clear precedence order.

### Precedence Order (Highest to Lowest)

1. `docker compose run -e` (CLI override)
2. `environment` attribute in compose.yaml
3. `--env-file` flag on CLI
4. `env_file` attribute in compose.yaml
5. `.env` file in project directory
6. Host environment variables

### Best Practices

**Use `.env` for defaults and local development:**
```env
# .env
COMPOSE_PROJECT_NAME=myapp
POSTGRES_VERSION=15
API_PORT=8080
```

**Use `env_file` for service-specific configuration:**
```yaml
services:
  api:
    env_file:
      - ./envs/common.env
      - ./envs/api.env
      - path: ./envs/api.local.env
        required: false  # Optional override (Compose 2.24+)
```

**Use `environment` for values that reference other variables:**
```yaml
services:
  api:
    environment:
      DATABASE_URL: "postgres://${DB_USER}:${DB_PASS}@db:5432/${DB_NAME}"
```

**Never put secrets in environment variables.** Use Docker secrets instead.

## 19. Complete Production Compose Templates

### Full-Stack Web Application

```yaml
name: production-fullstack

x-common: &common
  restart: unless-stopped
  init: true
  security_opt:
    - no-new-privileges:true
  cap_drop:
    - ALL
  logging:
    driver: "json-file"
    options:
      max-size: "10m"
      max-file: "5"

services:
  # Reverse Proxy
  nginx:
    <<: *common
    image: nginx:1.25-alpine
    read_only: true
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./nginx/certs:/etc/nginx/certs:ro
      - type: tmpfs
        target: /var/cache/nginx
      - type: tmpfs
        target: /var/run
    networks:
      - frontend
    depends_on:
      api:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "wget", "--no-verbose", "--tries=1", "--spider", "http://localhost/health"]
      interval: 30s
      timeout: 5s
      retries: 3
    deploy:
      resources:
        limits:
          cpus: '0.50'
          memory: 256M

  # API Service
  api:
    <<: *common
    image: YOUR_REGISTRY/api:${API_VERSION}
    read_only: true
    user: "1001:1001"
    expose:
      - "8080"
    environment:
      NODE_ENV: production
      DB_HOST: postgres
      DB_PORT: "5432"
      DB_NAME: ${DB_NAME}
      REDIS_URL: redis://redis:6379/0
      RABBITMQ_URL: amqp://guest:guest@rabbitmq:5672/
    secrets:
      - db_password
    volumes:
      - type: tmpfs
        target: /tmp
    networks:
      - frontend
      - backend
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
      rabbitmq:
        condition: service_healthy
      migrations:
        condition: service_completed_successfully
    healthcheck:
      test: ["CMD", "wget", "--no-verbose", "--tries=1", "--spider", "http://localhost:8080/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 15s
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 512M
        reservations:
          cpus: '0.25'
          memory: 128M

  # Worker Service
  worker:
    <<: *common
    image: YOUR_REGISTRY/api:${API_VERSION}
    read_only: true
    user: "1001:1001"
    command: ["node", "dist/worker.js"]
    environment:
      NODE_ENV: production
      DB_HOST: postgres
      REDIS_URL: redis://redis:6379/0
      RABBITMQ_URL: amqp://guest:guest@rabbitmq:5672/
    secrets:
      - db_password
    volumes:
      - type: tmpfs
        target: /tmp
    networks:
      - backend
    depends_on:
      postgres:
        condition: service_healthy
      rabbitmq:
        condition: service_healthy
    deploy:
      resources:
        limits:
          cpus: '0.50'
          memory: 256M

  # Database Migrations (init container)
  migrations:
    image: YOUR_REGISTRY/api:${API_VERSION}
    command: ["npx", "prisma", "migrate", "deploy"]
    user: "1001:1001"
    environment:
      DATABASE_URL: postgres://${DB_USER}:${DB_PASS}@postgres:5432/${DB_NAME}
    networks:
      - backend
    depends_on:
      postgres:
        condition: service_healthy
    restart: "no"

  # PostgreSQL
  postgres:
    <<: *common
    image: postgres:16-alpine
    read_only: true
    user: "70:70"
    environment:
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD_FILE: /run/secrets/db_password
      POSTGRES_DB: ${DB_NAME}
      PGDATA: /var/lib/postgresql/data/pgdata
    secrets:
      - db_password
    volumes:
      - pg_data:/var/lib/postgresql/data
      - type: tmpfs
        target: /var/run/postgresql
      - type: tmpfs
        target: /tmp
    networks:
      - backend
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${DB_USER} -d ${DB_NAME}"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 10s
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 2G
        reservations:
          cpus: '0.50'
          memory: 512M
    shm_size: '256m'

  # Redis
  redis:
    <<: *common
    image: redis:7-alpine
    read_only: true
    user: "999:999"
    command: ["redis-server", "--maxmemory", "256mb", "--maxmemory-policy", "allkeys-lru", "--appendonly", "yes"]
    volumes:
      - redis_data:/data
      - type: tmpfs
        target: /tmp
    networks:
      - backend
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5
    deploy:
      resources:
        limits:
          cpus: '0.50'
          memory: 300M

  # RabbitMQ
  rabbitmq:
    <<: *common
    image: rabbitmq:3.13-management-alpine
    hostname: rabbitmq
    environment:
      RABBITMQ_DEFAULT_USER: ${RABBITMQ_USER}
      RABBITMQ_DEFAULT_PASS: ${RABBITMQ_PASS}
    volumes:
      - rabbitmq_data:/var/lib/rabbitmq
    networks:
      - backend
    healthcheck:
      test: ["CMD", "rabbitmq-diagnostics", "-q", "ping"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 30s
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 512M

networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge
    internal: true

volumes:
  pg_data:
    driver: local
  redis_data:
    driver: local
  rabbitmq_data:
    driver: local

secrets:
  db_password:
    file: ./secrets/db_password.txt
```

### Monitoring Stack (Prometheus + Grafana)

```yaml
name: monitoring

x-common: &common
  restart: unless-stopped
  security_opt:
    - no-new-privileges:true
  cap_drop:
    - ALL
  logging:
    driver: "json-file"
    options:
      max-size: "10m"
      max-file: "3"

services:
  prometheus:
    <<: *common
    image: prom/prometheus:v2.51.0
    read_only: true
    user: "65534:65534"
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--storage.tsdb.retention.time=30d'
      - '--web.console.libraries=/usr/share/prometheus/console_libraries'
      - '--web.console.templates=/usr/share/prometheus/consoles'
      - '--web.enable-lifecycle'
    volumes:
      - ./prometheus/prometheus.yml:/etc/prometheus/prometheus.yml:ro
      - prometheus_data:/prometheus
    ports:
      - "9090:9090"
    networks:
      - monitoring
    healthcheck:
      test: ["CMD", "wget", "--no-verbose", "--tries=1", "--spider", "http://localhost:9090/-/healthy"]
      interval: 30s
      timeout: 5s
      retries: 3
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 2G

  grafana:
    <<: *common
    image: grafana/grafana:10.4.0
    user: "472:472"
    environment:
      GF_SECURITY_ADMIN_PASSWORD__FILE: /run/secrets/grafana_admin_password
      GF_INSTALL_PLUGINS: grafana-clock-panel
    secrets:
      - grafana_admin_password
    volumes:
      - grafana_data:/var/lib/grafana
      - ./grafana/provisioning:/etc/grafana/provisioning:ro
    ports:
      - "3000:3000"
    networks:
      - monitoring
    depends_on:
      prometheus:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "wget", "--no-verbose", "--tries=1", "--spider", "http://localhost:3000/api/health"]
      interval: 30s
      timeout: 5s
      retries: 3
    deploy:
      resources:
        limits:
          cpus: '0.50'
          memory: 512M

  node-exporter:
    <<: *common
    image: prom/node-exporter:v1.7.0
    read_only: true
    pid: host
    volumes:
      - /proc:/host/proc:ro
      - /sys:/host/sys:ro
      - /:/rootfs:ro
    command:
      - '--path.procfs=/host/proc'
      - '--path.sysfs=/host/sys'
      - '--path.rootfs=/rootfs'
      - '--collector.filesystem.mount-points-exclude=^/(sys|proc|dev|host|etc)($$|/)'
    networks:
      - monitoring
    deploy:
      resources:
        limits:
          cpus: '0.25'
          memory: 128M

  cadvisor:
    <<: *common
    image: gcr.io/cadvisor/cadvisor:v0.49.1
    read_only: true
    privileged: true
    volumes:
      - /:/rootfs:ro
      - /var/run:/var/run:ro
      - /sys:/sys:ro
      - /var/lib/docker/:/var/lib/docker:ro
      - /dev/disk/:/dev/disk:ro
    networks:
      - monitoring
    deploy:
      resources:
        limits:
          cpus: '0.25'
          memory: 256M

networks:
  monitoring:
    driver: bridge

volumes:
  prometheus_data:
  grafana_data:

secrets:
  grafana_admin_password:
    file: ./secrets/grafana_password.txt
```

## 20. Docker Compose Override and Multi-Environment Patterns

Docker Compose supports multiple configuration files that are merged together. This is the recommended approach for managing different environments.

### File Structure

```text
project/
  compose.yaml          # Base configuration (shared)
  compose.override.yaml # Development overrides (auto-loaded)
  compose.prod.yaml     # Production overrides
  compose.test.yaml     # Test overrides
  .env                  # Default environment variables
  .env.prod             # Production environment variables
```

### Base Configuration (compose.yaml)

```yaml
services:
  api:
    image: YOUR_REGISTRY/api:${API_VERSION:-latest}
    environment:
      DB_HOST: postgres
    depends_on:
      postgres:
        condition: service_healthy

  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: myapp
    healthcheck:
      test: ["CMD-SHELL", "pg_isready"]
      interval: 10s
      timeout: 5s
      retries: 5
```

### Development Override (compose.override.yaml)

```yaml
# Automatically loaded when running `docker compose up`
services:
  api:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "8080:8080"
      - "9229:9229"  # Node.js debugger
    volumes:
      - .:/app:cached
      - /app/node_modules
    environment:
      NODE_ENV: development
      LOG_LEVEL: debug
    command: ["npm", "run", "dev"]

  postgres:
    ports:
      - "5432:5432"  # Expose for local tools
    environment:
      POSTGRES_PASSWORD: devpassword
```

### Production Override (compose.prod.yaml)

```yaml
# Used with: docker compose -f compose.yaml -f compose.prod.yaml up -d
services:
  api:
    restart: unless-stopped
    read_only: true
    user: "1001:1001"
    security_opt:
      - no-new-privileges:true
    cap_drop:
      - ALL
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 512M
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "5"

  postgres:
    restart: unless-stopped
    read_only: true
    volumes:
      - pg_data:/var/lib/postgresql/data
      - type: tmpfs
        target: /var/run/postgresql
    secrets:
      - db_password
    environment:
      POSTGRES_PASSWORD_FILE: /run/secrets/db_password
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 2G
    shm_size: '256m'

volumes:
  pg_data:

secrets:
  db_password:
    file: ./secrets/db_password.txt
```

### Usage Commands

```bash
# Development (auto-loads compose.override.yaml)
docker compose up

# Production (explicitly specify files)
docker compose -f compose.yaml -f compose.prod.yaml up -d

# Testing
docker compose -f compose.yaml -f compose.test.yaml up --abort-on-container-exit

# Using env file
docker compose --env-file .env.prod -f compose.yaml -f compose.prod.yaml up -d
```

## 21. Docker System Maintenance and Cleanup

Docker can consume significant disk space over time. Regular maintenance is essential.

### Disk Usage Analysis

```bash
# Show Docker disk usage summary
docker system df

# Detailed breakdown
docker system df -v

# Check overlay2 storage
du -sh /var/lib/docker/overlay2/
```

### Cleanup Commands

```bash
# Remove all stopped containers, unused networks, dangling images, and build cache
docker system prune

# Also remove unused images (not just dangling)
docker system prune -a

# Also remove unused volumes (DANGEROUS — data loss)
docker system prune -a --volumes

# Remove only specific types
docker container prune    # Stopped containers
docker image prune         # Dangling images
docker image prune -a      # All unused images
docker volume prune        # Unused volumes
docker network prune       # Unused networks
docker builder prune       # Build cache

# Remove images older than 24 hours
docker image prune -a --filter "until=24h"

# Remove build cache older than 7 days, keep 10GB
docker builder prune --filter "until=168h" --keep-storage 10GB
```

### Automated Cleanup (Cron)

```bash
# Add to crontab: clean up every Sunday at 3 AM
0 3 * * 0 docker system prune -af --filter "until=168h" 2>&1 | logger -t docker-cleanup
```

## 22. Signal Handling and Graceful Shutdown

Proper signal handling is critical for zero-downtime deployments and data integrity.

### The PID 1 Problem

When Docker stops a container, it sends SIGTERM to PID 1 inside the container. If PID 1 is a shell (because you used the shell form of CMD/ENTRYPOINT), the signal is not forwarded to the actual application process, and Docker must resort to SIGKILL after the grace period.

**Solution 1: Use exec form**
```dockerfile
# Good — node is PID 1, receives SIGTERM directly
CMD ["node", "server.js"]

# Bad — sh is PID 1, node never receives SIGTERM
CMD node server.js
```

**Solution 2: Use init: true in Compose**
```yaml
services:
  api:
    init: true  # Uses tini as PID 1, forwards signals properly
    command: ["node", "server.js"]
```

**Solution 3: Use tini in Dockerfile**
```dockerfile
RUN apk add --no-cache tini
ENTRYPOINT ["/sbin/tini", "--"]
CMD ["node", "server.js"]
```

### Stop Grace Period

Configure how long Docker waits between SIGTERM and SIGKILL:

```yaml
services:
  api:
    stop_grace_period: 30s  # Default is 10s
    stop_signal: SIGTERM     # Default signal
```

For databases, use a longer grace period to allow transactions to complete:

```yaml
services:
  postgres:
    stop_grace_period: 120s  # 2 minutes for DB shutdown
```

## Conclusion

This Docker Super Specialist guide provides the complete knowledge base needed by tech support operations teams to optimize, secure, troubleshoot, and maintain Docker environments at any scale. From Dockerfile construction patterns that reduce image sizes by 90%+ to flaw-proof production Compose templates with full security hardening, every section is designed to be directly applicable to real-world scenarios. The multi-stage build patterns, health check configurations, environment management strategies, and maintenance procedures documented here represent the current state of the art for containerized application deployment.

## 23. Docker Compose Profiles for Selective Service Activation

Profiles allow you to define optional services that are only started when explicitly activated. This is essential for managing development tools, debugging utilities, and optional infrastructure components.

```yaml
services:
  api:
    image: YOUR_REGISTRY/api:latest
    # No profile = always started

  postgres:
    image: postgres:16-alpine
    # No profile = always started

  # Only started with --profile debug
  pgadmin:
    image: dpage/pgadmin4:latest
    profiles: ["debug"]
    ports:
      - "5050:80"
    environment:
      PGADMIN_DEFAULT_EMAIL: admin@local.dev
      PGADMIN_DEFAULT_PASSWORD: admin
    depends_on:
      postgres:
        condition: service_healthy

  # Only started with --profile monitoring
  prometheus:
    image: prom/prometheus:latest
    profiles: ["monitoring"]
    ports:
      - "9090:9090"

  grafana:
    image: grafana/grafana:latest
    profiles: ["monitoring"]
    ports:
      - "3000:3000"
    depends_on:
      - prometheus

  # Only started with --profile test
  test-runner:
    image: YOUR_REGISTRY/api:latest
    profiles: ["test"]
    command: ["npm", "test"]
    depends_on:
      postgres:
        condition: service_healthy
```

**Usage:**
```bash
# Start only core services (api + postgres)
docker compose up -d

# Start with debugging tools
docker compose --profile debug up -d

# Start with monitoring
docker compose --profile monitoring up -d

# Start with multiple profiles
docker compose --profile debug --profile monitoring up -d

# Or via environment variable
COMPOSE_PROFILES=debug,monitoring docker compose up -d
```

## 24. Docker Compose Watch for Development Hot-Reload

Docker Compose Watch (introduced in Compose 2.22) provides file-watching capabilities that automatically sync changes or rebuild services during development.

```yaml
services:
  api:
    build:
      context: .
      dockerfile: Dockerfile
    develop:
      watch:
        # Sync source files without rebuild
        - action: sync
          path: ./src
          target: /app/src
          ignore:
            - "**/*.test.ts"

        # Sync and restart when config changes
        - action: sync+restart
          path: ./config
          target: /app/config

        # Full rebuild when dependencies change
        - action: rebuild
          path: ./package.json

        # Full rebuild when Dockerfile changes
        - action: rebuild
          path: ./Dockerfile
```

**Usage:**
```bash
# Start with file watching
docker compose watch

# Or in background
docker compose up --watch
```

**Watch actions explained:**

| Action | Behavior | Use Case |
|---|---|---|
| `sync` | Copies changed files into the running container | Source code with hot-reload (nodemon, webpack-dev-server) |
| `sync+restart` | Copies files and restarts the container | Configuration files, environment changes |
| `rebuild` | Triggers a full image rebuild and container recreation | Dependency changes (package.json, requirements.txt, go.mod) |

## 25. Docker Compose Include for Modular Architecture

For large projects with many services, use `include` to split your Compose configuration into manageable modules.

```yaml
# compose.yaml (main entry point)
include:
  - path: ./infra/compose.db.yaml
  - path: ./infra/compose.cache.yaml
  - path: ./infra/compose.queue.yaml
  - path: ./services/compose.api.yaml
  - path: ./services/compose.worker.yaml
  - path:
      - ./monitoring/compose.monitoring.yaml
      - ./monitoring/compose.monitoring.override.yaml
```

**Each included file is a complete Compose file:**
```yaml
# infra/compose.db.yaml
services:
  postgres:
    image: postgres:16-alpine
    volumes:
      - pg_data:/var/lib/postgresql/data
    networks:
      - backend
    healthcheck:
      test: ["CMD-SHELL", "pg_isready"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  pg_data:

networks:
  backend:
    external: true
```

This pattern keeps each file focused and maintainable, while the main `compose.yaml` orchestrates everything.

## 26. Docker Compose Resource Management and Deploy Configuration

The `deploy` section provides fine-grained control over resource allocation and deployment behavior. While originally designed for Docker Swarm, many attributes now work with `docker compose up` when using the `--compatibility` flag or Compose V2.

### Resource Limits and Reservations

```yaml
services:
  api:
    deploy:
      resources:
        limits:
          cpus: '2.0'        # Maximum 2 CPU cores
          memory: 1G          # Maximum 1 GB RAM
          pids: 100           # Maximum 100 processes
        reservations:
          cpus: '0.5'        # Guaranteed 0.5 CPU cores
          memory: 256M        # Guaranteed 256 MB RAM
          devices:
            - driver: nvidia  # GPU reservation
              count: 1
              capabilities: [gpu]
```

### Restart Policies

```yaml
services:
  api:
    restart: unless-stopped  # Recommended for production

  migrations:
    restart: "no"            # One-shot containers

  critical-service:
    restart: always          # Always restart, even after daemon restart
    deploy:
      restart_policy:
        condition: on-failure
        delay: 5s
        max_attempts: 3
        window: 120s
```

**Restart policy comparison:**

| Policy | Behavior | Use Case |
|---|---|---|
| `no` | Never restart | Init containers, migrations, one-shot tasks |
| `always` | Always restart, including after daemon restart | Critical services that must always run |
| `unless-stopped` | Restart unless explicitly stopped by user | Standard production services |
| `on-failure` | Restart only on non-zero exit code | Services where clean exit means "done" |

## 27. Docker Compose YAML Anchors and Extensions

YAML anchors and Compose extensions eliminate configuration duplication across services.

### YAML Anchors and Merge Keys

```yaml
# Define anchors in x- extensions (ignored by Compose)
x-common-env: &common-env
  LOG_LEVEL: info
  TZ: UTC
  NODE_ENV: production

x-common-deploy: &common-deploy
  deploy:
    resources:
      limits:
        cpus: '1.0'
        memory: 512M
    restart_policy:
      condition: on-failure
      delay: 5s
      max_attempts: 3

x-common-security: &common-security
  security_opt:
    - no-new-privileges:true
  cap_drop:
    - ALL
  read_only: true

x-common-logging: &common-logging
  logging:
    driver: "json-file"
    options:
      max-size: "10m"
      max-file: "5"

services:
  api:
    image: YOUR_REGISTRY/api:v1
    <<: [*common-deploy, *common-security, *common-logging]
    environment:
      <<: *common-env
      API_PORT: "8080"
      DB_HOST: postgres

  worker:
    image: YOUR_REGISTRY/worker:v1
    <<: [*common-deploy, *common-security, *common-logging]
    environment:
      <<: *common-env
      WORKER_CONCURRENCY: "4"
      QUEUE_NAME: default

  scheduler:
    image: YOUR_REGISTRY/scheduler:v1
    <<: [*common-deploy, *common-security, *common-logging]
    environment:
      <<: *common-env
      CRON_EXPRESSION: "*/5 * * * *"
```

This pattern ensures that all services share identical security, logging, and resource configurations, making it impossible to accidentally deploy a service without proper hardening.

## 28. Docker Image Tagging Strategy

A proper tagging strategy is essential for traceability, rollback capability, and CI/CD integration.

### Recommended Tagging Convention

```bash
# Semantic version (primary tag for releases)
YOUR_REGISTRY/api:1.2.3

# Git SHA (for traceability to exact commit)
YOUR_REGISTRY/api:sha-a1b2c3d

# Branch-based (for development/staging)
YOUR_REGISTRY/api:main
YOUR_REGISTRY/api:develop

# Date-based (for nightly builds)
YOUR_REGISTRY/api:2026-05-29

# Combined (best practice for CI/CD)
YOUR_REGISTRY/api:1.2.3
YOUR_REGISTRY/api:1.2
YOUR_REGISTRY/api:1
YOUR_REGISTRY/api:sha-a1b2c3d
YOUR_REGISTRY/api:latest
```

### CI/CD Tagging Script

```bash
#!/bin/bash
set -euo pipefail

REGISTRY="YOUR_REGISTRY"
IMAGE="api"
VERSION=$(cat VERSION)
GIT_SHA=$(git rev-parse --short HEAD)
DATE=$(date +%Y-%m-%d)

# Build with BuildKit
DOCKER_BUILDKIT=1 docker build \
  --build-arg BUILDKIT_INLINE_CACHE=1 \
  --cache-from "${REGISTRY}/${IMAGE}:latest" \
  -t "${REGISTRY}/${IMAGE}:${VERSION}" \
  -t "${REGISTRY}/${IMAGE}:sha-${GIT_SHA}" \
  -t "${REGISTRY}/${IMAGE}:${DATE}" \
  -t "${REGISTRY}/${IMAGE}:latest" \
  .

# Push all tags
for tag in "${VERSION}" "sha-${GIT_SHA}" "${DATE}" "latest"; do
  docker push "${REGISTRY}/${IMAGE}:${tag}"
done
```

### Never Use `latest` in Production

The `latest` tag is mutable and provides no guarantee about what version is actually running. Always use explicit version tags in production Compose files:

```yaml
# BAD — unpredictable
services:
  api:
    image: YOUR_REGISTRY/api:latest

# GOOD — deterministic
services:
  api:
    image: YOUR_REGISTRY/api:1.2.3
```

## 29. Docker Compose Networking Best Practices

### Network Segmentation

Always separate frontend (internet-facing) and backend (internal) networks:

```yaml
services:
  nginx:
    networks:
      - frontend        # Internet-facing

  api:
    networks:
      - frontend        # Receives traffic from nginx
      - backend         # Connects to databases

  postgres:
    networks:
      - backend         # Only accessible from backend network

  redis:
    networks:
      - backend

networks:
  frontend:
    driver: bridge

  backend:
    driver: bridge
    internal: true      # No internet access, no external access
```

### DNS Resolution

Within a Docker Compose network, services can reach each other by service name. Docker's embedded DNS server (127.0.0.11) handles resolution automatically. Important rules to remember:

1. Service names are resolved to the container's IP on the shared network.
2. If a service is on multiple networks, it can only reach services on the same network(s).
3. Network aliases allow a service to be reachable by multiple names.
4. The `container_name` does NOT affect DNS resolution — the service name does.

```yaml
services:
  api:
    networks:
      backend:
        aliases:
          - api-service
          - app-backend
```

### Custom Network Configuration

```yaml
networks:
  backend:
    driver: bridge
    internal: true
    ipam:
      config:
        - subnet: 172.28.0.0/16
          ip_range: 172.28.5.0/24
          gateway: 172.28.5.254
    driver_opts:
      com.docker.network.bridge.name: br-backend
      com.docker.network.bridge.enable_icc: "true"
      com.docker.network.bridge.enable_ip_masquerade: "false"
```

## 30. Docker Backup and Disaster Recovery

### Volume Backup

```bash
# Backup a named volume to a tar file
docker run --rm \
  -v myapp_pg_data:/source:ro \
  -v $(pwd)/backups:/backup \
  alpine tar czf /backup/pg_data_$(date +%Y%m%d_%H%M%S).tar.gz -C /source .

# Restore a volume from backup
docker run --rm \
  -v myapp_pg_data:/target \
  -v $(pwd)/backups:/backup \
  alpine sh -c "rm -rf /target/* && tar xzf /backup/pg_data_20260529_120000.tar.gz -C /target"
```

### PostgreSQL Backup with Docker

```bash
# Logical backup (pg_dump)
docker compose exec -T postgres pg_dump -U appuser -d appdb -Fc > backup_$(date +%Y%m%d).dump

# Restore
docker compose exec -T postgres pg_restore -U appuser -d appdb --clean < backup_20260529.dump

# Automated daily backup via cron
0 2 * * * cd /opt/myapp && docker compose exec -T postgres pg_dump -U appuser -d appdb -Fc > /backups/daily_$(date +\%Y\%m\%d).dump 2>&1 | logger -t pg-backup
```

### Full Compose Stack Backup Script

```bash
#!/bin/bash
set -euo pipefail

BACKUP_DIR="/backups/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

# 1. Stop the stack gracefully
docker compose stop

# 2. Backup all named volumes
for volume in $(docker compose config --volumes); do
  echo "Backing up volume: $volume"
  docker run --rm \
    -v "${COMPOSE_PROJECT_NAME}_${volume}:/source:ro" \
    -v "$BACKUP_DIR:/backup" \
    alpine tar czf "/backup/${volume}.tar.gz" -C /source .
done

# 3. Backup compose files and configs
cp compose.yaml "$BACKUP_DIR/"
cp .env "$BACKUP_DIR/" 2>/dev/null || true
cp -r secrets/ "$BACKUP_DIR/secrets/" 2>/dev/null || true

# 4. Restart the stack
docker compose start

echo "Backup completed: $BACKUP_DIR"
```

## 31. Docker Compose Upgrade and Rolling Update Strategies

### Zero-Downtime Update Procedure

```bash
# 1. Pull new images
docker compose pull

# 2. Recreate only changed services (no downtime for unchanged ones)
docker compose up -d --no-deps --build api

# 3. Or recreate with force (ensures clean state)
docker compose up -d --force-recreate --no-deps api

# 4. Verify health
docker compose ps
docker compose logs --tail=50 api

# 5. If something went wrong, rollback
docker compose up -d --no-deps api  # with previous image tag in compose.yaml
```

### Blue-Green Deployment Pattern

```bash
# 1. Start new version alongside old
docker compose -p myapp-blue up -d   # Current (blue)
docker compose -p myapp-green up -d  # New version (green)

# 2. Test green deployment
curl http://localhost:8081/health

# 3. Switch traffic (update nginx/load balancer config)
# 4. Stop blue deployment
docker compose -p myapp-blue down
```

### Database Migration Safety

When upgrading services that require database migrations, always follow this order:

1. **Backup the database** before any migration.
2. **Run migrations in a separate container** with `service_completed_successfully`.
3. **Verify migration success** before starting the application.
4. **Set timeouts** on migration containers to prevent hanging.

```yaml
services:
  migrations:
    image: YOUR_REGISTRY/api:v2.0.0
    command: ["./migrate", "up"]
    restart: "no"
    environment:
      DATABASE_URL: postgres://user:pass@postgres:5432/myapp
      MIGRATION_TIMEOUT: "300"
    depends_on:
      postgres:
        condition: service_healthy
    deploy:
      resources:
        limits:
          memory: 256M
    # Fail fast if migration takes too long
    stop_grace_period: 5m
```

## Conclusion

This Docker Super Specialist guide provides the complete knowledge base needed by tech support operations teams to optimize, secure, troubleshoot, and maintain Docker environments at any scale. From Dockerfile construction patterns that reduce image sizes by 90%+ to flaw-proof production Compose templates with full security hardening, every section is designed to be directly applicable to real-world scenarios. The multi-stage build patterns, health check configurations, environment management strategies, dependency handling, network segmentation, backup procedures, and upgrade strategies documented here represent the current state of the art for containerized application deployment. Combined with the supporting specialist files (advanced patterns, CLI reference, troubleshooting, security audit, configuration schemas, and architecture deep dive), this forms a comprehensive operational playbook for any Docker-based infrastructure.

## Appendix A: Docker Compose Quick Reference Cheat Sheet

### Service Lifecycle Commands

| Command | Description |
|---|---|
| `docker compose up -d` | Start all services in background |
| `docker compose up -d --build` | Build images and start services |
| `docker compose up -d --force-recreate` | Recreate all containers even if unchanged |
| `docker compose up -d --no-deps api` | Start only `api` without its dependencies |
| `docker compose down` | Stop and remove containers and networks |
| `docker compose down -v` | Also remove named volumes (data loss) |
| `docker compose down --rmi all` | Also remove all images |
| `docker compose stop` | Stop containers without removing them |
| `docker compose start` | Start previously stopped containers |
| `docker compose restart api` | Restart a specific service |
| `docker compose pause api` | Pause a running service |
| `docker compose unpause api` | Unpause a paused service |

### Debugging Commands

| Command | Description |
|---|---|
| `docker compose ps` | List running containers with status |
| `docker compose ps -a` | List all containers including stopped |
| `docker compose logs -f api` | Follow logs for a specific service |
| `docker compose logs --tail=100 --since=1h` | Last 100 lines from the past hour |
| `docker compose exec api sh` | Open a shell in a running container |
| `docker compose exec -T postgres psql -U user db` | Run command without TTY (for scripts) |
| `docker compose top` | Show running processes in all containers |
| `docker compose config` | Validate and display the merged config |
| `docker compose config --services` | List all service names |
| `docker compose config --volumes` | List all volume names |
| `docker compose images` | List images used by services |
| `docker compose events` | Stream real-time container events |

### Build Commands

| Command | Description |
|---|---|
| `docker compose build` | Build all services with build context |
| `docker compose build --no-cache api` | Build without cache |
| `docker compose build --pull` | Always pull base images before building |
| `docker compose build --parallel` | Build services in parallel |
| `docker compose push` | Push built images to registry |

## Appendix B: Dockerfile Instruction Quick Reference

| Instruction | Purpose | Exec Form | Shell Form |
|---|---|---|---|
| `FROM` | Set base image | `FROM image:tag AS name` | N/A |
| `RUN` | Execute build command | `RUN ["cmd", "arg"]` | `RUN cmd arg` |
| `CMD` | Default container command | `CMD ["cmd", "arg"]` | `CMD cmd arg` |
| `ENTRYPOINT` | Container executable | `ENTRYPOINT ["cmd"]` | `ENTRYPOINT cmd` |
| `COPY` | Copy files from context | `COPY [--chown=u:g] src dst` | N/A |
| `ADD` | Copy with extraction/URL | `ADD src dst` | N/A |
| `ENV` | Set environment variable | `ENV KEY=value` | N/A |
| `ARG` | Build-time variable | `ARG NAME=default` | N/A |
| `EXPOSE` | Document port | `EXPOSE 8080/tcp` | N/A |
| `VOLUME` | Create mount point | `VOLUME ["/data"]` | `VOLUME /data` |
| `WORKDIR` | Set working directory | `WORKDIR /app` | N/A |
| `USER` | Set runtime user | `USER 1001:1001` | N/A |
| `HEALTHCHECK` | Define health check | `HEALTHCHECK CMD curl -f ...` | N/A |
| `LABEL` | Add metadata | `LABEL key="value"` | N/A |
| `STOPSIGNAL` | Set stop signal | `STOPSIGNAL SIGTERM` | N/A |
| `SHELL` | Override default shell | `SHELL ["/bin/bash", "-c"]` | N/A |
| `ONBUILD` | Trigger on child build | `ONBUILD RUN cmd` | N/A |

## Appendix C: Common Docker Error Messages and Solutions

| Error Message | Cause | Solution |
|---|---|---|
| `exec format error` | Wrong platform (e.g., arm64 image on amd64) | Rebuild with `--platform linux/amd64` or use `platform:` in compose |
| `port is already allocated` | Another process using the port | `lsof -i :PORT` to find and stop it, or change the port mapping |
| `no space left on device` | Docker storage full | `docker system prune -a` and check `/var/lib/docker` |
| `OOMKilled` | Container exceeded memory limit | Increase `memory` limit or optimize application memory usage |
| `connection refused` | Service not ready or wrong network | Check `depends_on` conditions and verify network connectivity |
| `permission denied` | File ownership mismatch | Match container USER UID with volume file ownership |
| `name already in use` | Container name conflict | `docker compose down --remove-orphans` or remove the old container |
| `network not found` | Stale network reference | `docker network prune` and recreate |
| `manifest unknown` | Image tag doesn't exist in registry | Verify the tag exists: `docker manifest inspect image:tag` |
| `unauthorized: authentication required` | Registry login needed | `docker login YOUR_REGISTRY` |
| `context deadline exceeded` | Network timeout pulling image | Check DNS, proxy settings, or use a registry mirror |
| `max depth exceeded` | Too many image layers | Consolidate RUN instructions, use multi-stage builds |

## === FILE: 49-docker-troubleshooting.md ===
# Docker Super Specialist: Complete Troubleshooting & Optimization Guide

## Introduction

Welcome to the ultimate guide for Docker troubleshooting, optimization, and production readiness. As the Docker Super Specialist, this document is designed to provide you with an extremely comprehensive, detailed, and production-ready reference for solving the most complex Docker and Docker Compose issues. This guide is written from the perspective of a tech support operations team, focusing on helping clients fix and optimize their Docker setups. It covers everything from build failures and container startup issues to networking, storage, performance, and platform-specific quirks.

Every section includes real configuration examples, real commands, real error messages, and their corresponding solutions. We provide complete, working code blocks rather than mere snippets, ensuring that you can copy, paste, and adapt these solutions directly into your production environments.

---

## 1. Build Failures

Build failures are among the most common issues encountered when working with Docker. They can stem from a variety of sources, including cache invalidation, excessively large layers, context size issues, multi-stage build errors, and platform mismatches.

### 1.1 Cache Invalidation

**The Problem:**
Docker builds can become painfully slow if the build cache is frequently invalidated. This often happens when instructions that change frequently (like `COPY . .`) are placed too early in the Dockerfile, causing all subsequent layers to be rebuilt.

**Real Error/Symptom:**
Builds take several minutes instead of seconds, and the output shows `=> [internal] load build context` followed by rebuilding layers that haven't actually changed.

**The Solution:**
Order your Dockerfile instructions from least frequently changed to most frequently changed. Copy dependency files (like `package.json` or `requirements.txt`) and install dependencies before copying the rest of the source code.

**Before (Poor Caching):**
```dockerfile
FROM node:18-alpine
WORKDIR /app
# Copying everything invalidates the cache if ANY file changes
COPY . .
RUN npm install
CMD ["npm", "start"]
```

**After (Optimized Caching):**
```dockerfile
FROM node:18-alpine
WORKDIR /app
# Only copy package files first
COPY package*.json ./
# Install dependencies (this layer is cached unless package.json changes)
RUN npm ci --only=production
# Now copy the rest of the code
COPY . .
CMD ["npm", "start"]
```

### 1.2 Layer Too Large

**The Problem:**
Each `RUN`, `COPY`, and `ADD` instruction creates a new layer. If you install packages, download files, and then clean them up in separate `RUN` instructions, the intermediate layers still contain the deleted files, bloating the final image size.

**Real Error/Symptom:**
The final image size is significantly larger than expected, leading to slow pulls and deployments.

**The Solution:**
Chain commands using `&&` and clean up caches in the same `RUN` instruction.

**Before (Bloated Layers):**
```dockerfile
FROM ubuntu:22.04
RUN apt-get update
RUN apt-get install -y curl build-essential
RUN curl -O https://example.com/large-file.tar.gz
RUN tar -xzf large-file.tar.gz
RUN rm large-file.tar.gz
RUN apt-get clean
```

**After (Optimized Layers):**
```dockerfile
FROM ubuntu:22.04
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    && curl -O https://example.com/large-file.tar.gz \
    && tar -xzf large-file.tar.gz \
    && rm large-file.tar.gz \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
```

### 1.3 Context Too Large

**The Problem:**
When you run `docker build`, the Docker CLI sends the entire build context (the directory containing the Dockerfile) to the Docker daemon. If this directory contains large, unnecessary files (like `.git`, `node_modules`, or virtual environments), the build process will be slow to start.

**Real Error/Symptom:**
```text
Sending build context to Docker daemon  1.5GB
```

**The Solution:**
Use a `.dockerignore` file to exclude unnecessary files and directories from the build context.

**Example `.dockerignore`:**
```text
.git
.gitignore
node_modules/
npm-debug.log
Dockerfile
.dockerignore
__pycache__/
*.pyc
.venv/
venv/
.env
```

### 1.4 Multi-stage COPY --from Failures

**The Problem:**
Multi-stage builds are excellent for reducing image size, but errors occur if you try to copy from a stage that hasn't been defined or if the path is incorrect.

**Real Error/Symptom:**
```text
failed to compute cache key: failed to calculate checksum of ref: "/app/build": not found
```

**The Solution:**
Ensure the stage name is correct and the path exists in the source stage.

**Working Example:**
```dockerfile
# Stage 1: Build
FROM golang:1.20-alpine AS builder
WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o main .

# Stage 2: Production
FROM alpine:latest
RUN apk --no-cache add ca-certificates
WORKDIR /root/
# Correctly referencing the 'builder' stage
COPY --from=builder /app/main .
CMD ["./main"]
```

### 1.5 ARG/ENV Scope Issues

**The Problem:**
`ARG` variables are only available during the build process, while `ENV` variables are available during both build and runtime. A common mistake is expecting an `ARG` to be available in the final container or placing an `ARG` before a `FROM` statement and expecting it to be available after.

**Real Error/Symptom:**
A script fails during runtime because an expected environment variable is empty, or a build fails because an `ARG` is not recognized.

**The Solution:**
Understand the scoping rules. If an `ARG` is defined before `FROM`, it can only be used in the `FROM` instruction. To use it later, you must declare it again. To make an `ARG` available at runtime, assign it to an `ENV`.

**Working Example:**
```dockerfile
# ARG before FROM is only for the FROM instruction
ARG NODE_VERSION=18
FROM node:${NODE_VERSION}-alpine

# Declare ARG again to use it in this stage
ARG BUILD_DATE
ARG APP_VERSION

# Assign ARG to ENV to make it available at runtime
ENV APP_VERSION=${APP_VERSION}
ENV BUILD_DATE=${BUILD_DATE}

WORKDIR /app
COPY . .
RUN echo "Building version ${APP_VERSION} on ${BUILD_DATE}" > build_info.txt

CMD ["node", "app.js"]
```

### 1.6 Platform Mismatch (exec format error)

**The Problem:**
Building an image on an ARM architecture (like Apple Silicon M1/M2) and deploying it to an AMD64 (x86_64) server results in a runtime error because the binary formats are incompatible.

**Real Error/Symptom:**
```text
standard_init_linux.go:228: exec user process caused: exec format error
```

**The Solution:**
Use Docker Buildx to build multi-platform images or specify the target platform during the build.

**Command Example:**
```bash
# Build specifically for AMD64
docker build --platform linux/amd64 -t YOUR_REGISTRY/YOUR_IMAGE:latest .

# Build for multiple platforms and push to registry
docker buildx create --use
docker buildx build --platform linux/amd64,linux/arm64 -t YOUR_REGISTRY/YOUR_IMAGE:latest --push .
```

### 1.7 BuildKit Compatibility

**The Problem:**
Older Docker versions or specific CI environments might not support BuildKit features, leading to syntax errors when using advanced features like cache mounts or secrets.

**Real Error/Symptom:**
```text
the --mount option requires BuildKit. Run with DOCKER_BUILDKIT=1
```

**The Solution:**
Ensure BuildKit is enabled. It is the default in Docker 23.0+, but for older versions or specific CI setups, you must enable it explicitly.

**Command Example:**
```bash
export DOCKER_BUILDKIT=1
docker build -t YOUR_IMAGE .
```

**Advanced BuildKit Example (Cache Mounts):**
```dockerfile
# syntax=docker/dockerfile:1.4
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
# Use BuildKit cache mount to speed up pip installs
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt
COPY . .
CMD ["python", "main.py"]
```

---

## 2. Container Startup Failures

When a container fails to start, it can be incredibly frustrating. The container might exit immediately, throw permission errors, or get killed by the system.

### 2.1 Exec Format Error (Wrong Platform)

As discussed in the build section, this occurs when the image architecture doesn't match the host architecture.

**Solution:**
Verify the image architecture using `docker inspect`.
```bash
docker inspect YOUR_IMAGE | grep Architecture
```
Rebuild the image for the correct target platform using `--platform linux/amd64`.

### 2.2 Permission Denied

**The Problem:**
The container process lacks the necessary permissions to execute a file, read a configuration, or write to a directory. This often happens when switching to a non-root user.

**Real Error/Symptom:**
```text
/docker-entrypoint.sh: 10: /docker-entrypoint.sh: cannot create /app/config.json: Permission denied
```

**The Solution:**
Ensure the user running the process has the correct ownership and permissions. Use the `USER` directive carefully and adjust permissions during the build.

**Working Example:**
```dockerfile
FROM node:18-alpine
# Create a dedicated user and group
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
WORKDIR /app
# Copy files and change ownership
COPY --chown=appuser:appgroup package*.json ./
RUN npm ci --only=production
COPY --chown=appuser:appgroup . .
# Switch to the non-root user
USER appuser
CMD ["npm", "start"]
```

### 2.3 Port Already in Use

**The Problem:**
The host port you are trying to bind to the container is already occupied by another process (either another container or a host service).

**Real Error/Symptom:**
```text
Error starting userland proxy: listen tcp4 0.0.0.0:80: bind: address already in use
```

**The Solution:**
Identify the process using the port and either stop it or change the port mapping in your Docker Compose file.

**Troubleshooting Commands:**
```bash
# Find what is using port 80
sudo lsof -i :80
# OR
sudo netstat -tulpn | grep :80
```

**Compose Fix:**
```yaml
services:
  web:
    image: nginx:alpine
    ports:
      # Change host port from 80 to 8080
      - "8080:80"
```

### 2.4 Missing Entrypoint/CMD

**The Problem:**
The container starts but immediately exits because it doesn't know what command to run.

**Real Error/Symptom:**
The container exits with code 0 immediately after starting. `docker logs` shows nothing.

**The Solution:**
Ensure your Dockerfile has a valid `CMD` or `ENTRYPOINT`. If overriding in Compose, ensure the syntax is correct.

**Working Example:**
```dockerfile
FROM alpine:latest
# This container will exit immediately without a CMD
# Add a long-running process or the actual application command
CMD ["tail", "-f", "/dev/null"]
```

### 2.5 OOM Killed Immediately

**The Problem:**
The container requires more memory to start than the limit specified, causing the Linux Out-Of-Memory (OOM) killer to terminate it immediately.

**Real Error/Symptom:**
`docker ps -a` shows the container exited with code 137. `docker inspect` shows `"OOMKilled": true`.

**The Solution:**
Increase the memory limit in your deployment configuration or optimize the application's memory footprint.

**Compose Fix:**
```yaml
services:
  java-app:
    image: YOUR_REGISTRY/java-app:latest
    deploy:
      resources:
        limits:
          # Increase memory limit
          memory: 2G
        reservations:
          memory: 1G
    environment:
      # Tune JVM memory settings to respect container limits
      - JAVA_OPTS=-Xmx1500m -Xms1500m
```

---

## 3. Networking Issues

Docker networking can be complex, especially in multi-container environments. Issues range from containers not being able to reach the internet to DNS resolution failures.

### 3.1 Container Can't Reach Internet

**The Problem:**
A container cannot download packages or reach external APIs, even though the host machine has internet access.

**Real Error/Symptom:**
```text
curl: (6) Could not resolve host: api.github.com
```

**The Solution:**
This is often a DNS issue or an MTU (Maximum Transmission Unit) mismatch between the Docker bridge and the host network.

**Troubleshooting Steps:**
1. Check if it's a DNS issue by pinging an IP directly (e.g., `ping 8.8.8.8`).
2. If IP ping works but domain ping fails, configure Docker daemon DNS.

**Fix (Daemon DNS):**
Edit `/etc/docker/daemon.json`:
```json
{
  "dns": ["8.8.8.8", "8.8.4.4"]
}
```
Restart Docker: `sudo systemctl restart docker`

### 3.2 Containers Can't Communicate

**The Problem:**
Two containers in the same Compose project cannot talk to each other using their service names.

**Real Error/Symptom:**
```text
Connection refused to host: backend-service
```

**The Solution:**
Ensure both containers are on the same custom network. The default bridge network does not support automatic DNS resolution by container name; you must use a user-defined bridge network (which Compose creates by default, but manual configurations can break this).

**Compose Fix:**
```yaml
services:
  frontend:
    image: frontend-app
    networks:
      - app-network
    depends_on:
      - backend

  backend:
    image: backend-app
    networks:
      - app-network

networks:
  app-network:
    driver: bridge
```

### 3.3 DNS Resolution Failures

**The Problem:**
Containers intermittently fail to resolve internal or external hostnames.

**Real Error/Symptom:**
```text
getaddrinfo ENOTFOUND database-service
```

**The Solution:**
Docker's embedded DNS server (127.0.0.11) handles resolution. If it fails, it might be due to Alpine Linux's musl libc handling DNS differently than glibc, or conflicts with the host's `systemd-resolved`.

**Fix (Alpine specific):**
Sometimes, adding `ndots` configuration helps.
```yaml
services:
  alpine-service:
    image: alpine-based-app
    dns_opt:
      - ndots:1
```

### 3.4 Port Mapping Not Working

**The Problem:**
You mapped a port in Compose, but you cannot access the service from the host machine.

**Real Error/Symptom:**
`curl http://localhost:8080` returns `Connection refused`.

**The Solution:**
The application inside the container MUST bind to `0.0.0.0` (all interfaces), not `127.0.0.1` (localhost). If it binds to localhost, it is only accessible from within the container itself.

**Fix (Node.js Example):**
```javascript
// BAD: Only accessible inside the container
// server.listen(8080, '127.0.0.1');

// GOOD: Accessible from the host via port mapping
server.listen(8080, '0.0.0.0');
```

### 3.5 Bridge Network Exhaustion

**The Problem:**
You cannot create new Docker networks because the default address pools are exhausted.

**Real Error/Symptom:**
```text
Error response from daemon: could not find an available, non-overlapping IPv4 address pool among the defaults to assign to the network
```

**The Solution:**
Configure the Docker daemon to use a larger or different set of address pools.

**Fix (`/etc/docker/daemon.json`):**
```json
{
  "default-address-pools": [
    {
      "base": "10.10.0.0/16",
      "size": 24
    }
  ]
}
```
Restart Docker: `sudo systemctl restart docker`

### 3.6 IPv6 Issues

**The Problem:**
Applications attempting to bind to IPv6 interfaces fail if IPv6 is not enabled in Docker.

**Real Error/Symptom:**
```text
Cannot assign requested address (bind failed)
```

**The Solution:**
Enable IPv6 in the Docker daemon and the specific network.

**Fix (`/etc/docker/daemon.json`):**
```json
{
  "ipv6": true,
  "fixed-cidr-v6": "2001:db8:1::/64"
}
```

### 3.7 Firewall/iptables Conflicts

**The Problem:**
UFW or firewalld blocks traffic to Docker containers, or Docker bypasses UFW rules, exposing ports unintentionally.

**Real Error/Symptom:**
Ports mapped in Docker are accessible from the internet even if UFW is set to deny them.

**The Solution:**
Docker manipulates iptables directly. To secure ports, bind them to localhost if they shouldn't be public, or use the `DOCKER-USER` iptables chain.

**Compose Fix (Bind to localhost):**
```yaml
services:
  database:
    image: postgres:15
    ports:
      # Only accessible from the host machine, not the internet
      - "127.0.0.1:5432:5432"
```

---

## 4. Volume/Storage Issues

Storage issues can lead to data loss, application crashes, and deployment failures. Understanding permissions and storage drivers is crucial.

### 4.1 Permission Denied on Bind Mounts

**The Problem:**
When mounting a host directory into a container, the container process (running as a specific UID) does not have read/write access to the host directory.

**Real Error/Symptom:**
```text
chown: changing ownership of '/var/lib/mysql/': Permission denied
```

**The Solution:**
Ensure the UID/GID inside the container matches the owner of the host directory.

**Fix (Linux UID/GID):**
```bash
# Find your host UID
id -u
# Run container with that UID
docker run -u $(id -u):$(id -g) -v /host/data:/container/data YOUR_IMAGE
```

**Fix (SELinux :z/:Z):**
On systems with SELinux (like RHEL/CentOS/Fedora), you must append `:z` (shared) or `:Z` (private) to the volume mount so Docker can relabel the directory.
```yaml
services:
  app:
    image: myapp
    volumes:
      - ./data:/app/data:z
```

### 4.2 No Space Left on Device

**The Problem:**
The host machine's disk is full, often due to dangling images, stopped containers, or massive log files.

**Real Error/Symptom:**
```text
write /var/lib/docker/overlay2/... : no space left on device
```

**The Solution:**
Clean up unused Docker resources and configure log rotation.

**Cleanup Commands:**
```bash
# Remove unused data (prompts for confirmation)
docker system prune

# Remove EVERYTHING unused, including volumes and all stopped containers
docker system prune -a --volumes
```

**Log Rotation Fix (Compose):**
```yaml
services:
  app:
    image: myapp
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

### 4.3 Volume Data Not Persisting

**The Problem:**
Data written by the database or application is lost when the container is recreated.

**Real Error/Symptom:**
Database tables disappear after `docker compose down` and `docker compose up -d`.

**The Solution:**
Use named volumes instead of bind mounts or anonymous volumes for persistent data.

**Compose Fix:**
```yaml
services:
  db:
    image: postgres:15
    volumes:
      # Use a named volume
      - pgdata:/var/lib/postgresql/data

volumes:
  # Declare the named volume
  pgdata:
```

### 4.4 NFS Mount Failures

**The Problem:**
Mounting an NFS share directly as a Docker volume fails due to incorrect options or network issues.

**Real Error/Symptom:**
```text
Error response from daemon: error while mounting volume '': failed to mount local volume: mount :/path:/var/lib/docker/volumes/... : connection timed out
```

**The Solution:**
Define the NFS volume correctly in Compose, ensuring the host has `nfs-common` installed.

**Compose Fix:**
```yaml
volumes:
  nfs-data:
    driver: local
    driver_opts:
      type: nfs
      o: addr=192.168.1.100,rw,nolock,hard,nointr,nfsvers=4
      device: ":/path/to/nfs/share"
```

---

## 5. Performance Issues

Performance optimization is key to a production-ready Docker setup. This involves tuning builds, startup times, and resource usage.

### 5.1 Slow Builds

**The Problem:**
Builds take too long, impacting developer productivity and CI/CD pipeline speed.

**The Solution:**
Utilize BuildKit, optimize layer caching, and use `.dockerignore`.

**Optimization Example (BuildKit Cache Mounts):**
```dockerfile
# syntax=docker/dockerfile:1.4
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
# Cache the npm directory to speed up subsequent builds
RUN --mount=type=cache,target=/root/.npm \
    npm ci
COPY . .
CMD ["npm", "start"]
```

### 5.2 Slow Container Startup

**The Problem:**
Containers take a long time to become ready, causing deployment delays and health check failures.

**The Solution:**
Reduce image size (smaller images extract faster) and optimize health check timing.

**Compose Fix (Health Check Timing):**
```yaml
services:
  heavy-app:
    image: heavy-app:latest
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
      interval: 10s
      timeout: 5s
      retries: 5
      # Give the app 60 seconds to start before counting failures
      start_period: 60s
```

### 5.3 High Memory Usage (OOM Tuning)

**The Problem:**
A container consumes all available host memory, potentially crashing the host or other containers.

**The Solution:**
Set hard memory limits and tune the application (e.g., JVM heap size, Node.js max old space size).

**Compose Fix:**
```yaml
services:
  node-app:
    image: node-app:latest
    deploy:
      resources:
        limits:
          memory: 512M
    environment:
      # Tell Node.js to garbage collect before hitting the container limit
      - NODE_OPTIONS=--max-old-space-size=384
```

### 5.4 High CPU (Throttling)

**The Problem:**
A container uses 100% of the CPU, starving other processes.

**The Solution:**
Set CPU limits. Note that setting `cpus` limits the container to a fraction of the total CPU time, which can cause throttling if the app is bursty.

**Compose Fix:**
```yaml
services:
  worker:
    image: worker-app:latest
    deploy:
      resources:
        limits:
          # Limit to 1.5 CPUs
          cpus: '1.5'
```

### 5.5 Slow I/O

**The Problem:**
Database containers or applications with heavy disk usage perform poorly.

**The Solution:**
Ensure you are using the `overlay2` storage driver. For bind mounts on macOS/Windows, I/O is notoriously slow due to virtualization.

**Fix (macOS/Windows Development):**
Use named volumes instead of bind mounts for database data directories, or use the newer VirtioFS implementation in Docker Desktop.

---

## 6. Docker Compose Specific Issues

Docker Compose simplifies multi-container orchestration, but it introduces its own set of complexities.

### 6.1 Service Dependency Failures

**The Problem:**
Service A depends on Service B (e.g., a web app depends on a database), but Service A crashes because Service B is running but not yet ready to accept connections.

**Real Error/Symptom:**
```text
Connection refused: The database system is starting up
```

**The Solution:**
Use the long syntax for `depends_on` combined with a `healthcheck` on the dependency.

**Compose Fix:**
```yaml
services:
  web:
    image: my-web-app
    depends_on:
      db:
        # Wait for the healthcheck to pass, not just the container to start
        condition: service_healthy

  db:
    image: postgres:15
    environment:
      POSTGRES_PASSWORD: secret
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 5s
      retries: 5
```

### 6.2 Orphan Containers

**The Problem:**
When you rename a project or remove a service from `compose.yaml`, the old containers remain running.

**Real Error/Symptom:**
```text
WARNING: Found orphan containers (old-service-name) for this project.
```

**The Solution:**
Use the `--remove-orphans` flag when bringing up the stack.

**Command:**
```bash
docker compose up -d --remove-orphans
```

### 6.3 Compose File Validation Errors

**The Problem:**
Syntax errors or invalid configuration options in `compose.yaml`.

**Real Error/Symptom:**
```text
services.web.ports contains an invalid type, it should be an array
```

**The Solution:**
Always validate your Compose file before deploying.

**Command:**
```bash
docker compose config
```

### 6.4 Environment Variable Interpolation Issues

**The Problem:**
Variables in `.env` files are not being passed correctly, or literal dollar signs (`$`) are being interpreted as variables.

**Real Error/Symptom:**
A password containing a `$` fails because Compose tries to interpolate it.

**The Solution:**
Escape literal dollar signs with a double dollar sign (`$$`).

**Compose Fix:**
```yaml
services:
  app:
    image: myapp
    environment:
      # The actual password is "pass$word"
      - DB_PASSWORD=pass$$word
```

### 6.5 Profile Activation Problems

**The Problem:**
Services assigned to a profile do not start.

**The Solution:**
You must explicitly activate the profile using the `--profile` flag or the `COMPOSE_PROFILES` environment variable.

**Compose Fix:**
```yaml
services:
  app:
    image: myapp
  debug-tools:
    image: debug-tools
    profiles:
      - debug
```
**Command:**
```bash
docker compose --profile debug up -d
```

### 6.6 Merge/Override Conflicts

**The Problem:**
When using multiple Compose files (e.g., `compose.yaml` and `compose.override.yaml`), lists (like ports or volumes) are merged, not replaced, which can cause conflicts.

**The Solution:**
Understand the merge rules. To completely replace a list, you might need to restructure your files or use YAML anchors.

---

## 7. Health Check Failures

Health checks are critical for self-healing systems, but misconfigured checks cause more harm than good.

### 7.1 Wrong Command

**The Problem:**
The health check command fails because the required tool (like `curl` or `ping`) is not installed in the container image.

**Real Error/Symptom:**
Container is marked `unhealthy`. `docker inspect` shows `executable file not found in $PATH`.

**The Solution:**
Use tools that exist in the image, or install them. For minimal images, write a custom script or use built-in language features.

**Fix (Node.js without curl):**
```yaml
healthcheck:
  test: ["CMD", "node", "-e", "require('http').get('http://localhost:8080/health', (r) => {if (r.statusCode !== 200) throw new Error()})"]
```

### 7.2 Timing Issues

**The Problem:**
The application takes 45 seconds to start, but the health check fails after 30 seconds, causing the container to be restarted endlessly.

**The Solution:**
Use `start_period` to give the application time to initialize.

**Compose Fix:**
```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8080"]
  interval: 10s
  timeout: 5s
  retries: 3
  start_period: 60s
```

---

## 8. Registry Issues

Pulling and pushing images to registries can fail due to authentication, network, or rate-limiting issues.

### 8.1 Authentication Failures

**The Problem:**
Cannot pull a private image.

**Real Error/Symptom:**
```text
Error response from daemon: pull access denied for YOUR_REGISTRY/YOUR_IMAGE, repository does not exist or may require 'docker login'
```

**The Solution:**
Ensure you are logged in. For CI/CD, use access tokens instead of passwords.

**Command:**
```bash
echo $CR_PAT | docker login ghcr.io -u USERNAME --password-stdin
```

### 8.2 Rate Limiting (Docker Hub)

**The Problem:**
Anonymous pulls from Docker Hub are rate-limited (100 pulls per 6 hours per IP).

**Real Error/Symptom:**
```text
toomanyrequests: You have reached your pull rate limit.
```

**The Solution:**
Authenticate with a free Docker Hub account (increases limit to 200) or a paid account, or use a registry mirror/cache.

### 8.3 Manifest Unknown

**The Problem:**
The tag you are trying to pull does not exist, or the image was built for a different architecture and no multi-arch manifest exists.

**Real Error/Symptom:**
```text
manifest for YOUR_IMAGE:latest not found: manifest unknown
```

**The Solution:**
Verify the tag exists in the registry. Avoid using `:latest` in production; pin to specific SHAs or version tags.

---

## 9. Docker Daemon Issues

When the Docker daemon itself fails, all containers are affected.

### 9.1 Daemon Won't Start

**The Problem:**
The `dockerd` process crashes on startup.

**Real Error/Symptom:**
`sudo systemctl status docker` shows `failed`.

**The Solution:**
Check the daemon logs. Often caused by invalid JSON in `/etc/docker/daemon.json`.

**Command:**
```bash
sudo journalctl -u docker.service --no-pager
```

### 9.2 Live-Restore Issues

**The Problem:**
Restarting the Docker daemon kills all running containers, causing downtime during daemon upgrades.

**The Solution:**
Enable `live-restore` to keep containers running when the daemon is unavailable.

**Fix (`/etc/docker/daemon.json`):**
```json
{
  "live-restore": true
}
```

---

## 10. Production Incidents

Handling severe production incidents requires a calm, methodical approach.

### 10.1 Container Restart Loops

**The Problem:**
A container crashes immediately upon startup, and the `restart: always` policy brings it back up, causing a loop that consumes CPU and fills logs.

**The Solution:**
Change the restart policy to `on-failure:5` to limit retries, and inspect the logs of the crashed container.

**Command:**
```bash
# View logs of a restarting container
docker logs --tail 100 -f <container_id>
```

### 10.2 Cascading Failures

**The Problem:**
A database slows down, causing the web servers to exhaust their connection pools, which in turn causes the load balancer to drop traffic.

**The Solution:**
Implement proper timeouts, circuit breakers in your application code, and strict resource limits in Docker Compose to ensure one failing service doesn't bring down the host.

### 10.3 Data Corruption Recovery

**The Problem:**
A database container was killed ungracefully, leading to corrupted data files.

**The Solution:**
Always use `stop_grace_period` to allow databases to shut down cleanly.

**Compose Fix:**
```yaml
services:
  db:
    image: postgres:15
    # Give Postgres 60 seconds to flush data to disk before sending SIGKILL
    stop_grace_period: 60s
```

---

## 11. Platform-Specific Quirks

Docker behaves differently depending on the underlying operating system.

### 11.1 Linux (cgroup v2, systemd, SELinux)

- **cgroup v2:** Modern Linux distributions use cgroup v2. Ensure your Docker version is up to date (20.10+) to fully support it.
- **SELinux:** As mentioned, use `:z` or `:Z` on volume mounts.
- **AppArmor:** Docker applies a default AppArmor profile. If your container needs specific privileges, you may need to adjust it using `security_opt: apparmor=unconfined` (use with caution).

### 11.2 macOS (File Sharing Performance)

**The Problem:**
Bind mounts on macOS are extremely slow because files must be synced across the hypervisor boundary.

**The Solution:**
Use VirtioFS (enable in Docker Desktop settings) or use named volumes for heavy I/O operations like databases or `node_modules`.

### 11.3 Windows (WSL2 Issues)

**The Problem:**
Docker Desktop on Windows using WSL2 can consume all available host memory.

**The Solution:**
Limit WSL2 memory usage by creating a `.wslconfig` file in your Windows user profile directory.

**Fix (`C:\Users\YOUR_USER\.wslconfig`):**
```ini
[wsl2]
memory=4GB
processors=2
```

---

## Conclusion

Mastering Docker troubleshooting requires a deep understanding of Linux namespaces, cgroups, networking, and storage. By applying the configurations, optimizations, and debugging techniques outlined in this guide, you can build resilient, high-performance, and production-ready containerized environments. Always remember to pin your versions, set resource limits, configure health checks, and monitor your systems proactively.

---

## 12. Advanced Docker Compose Cost & Time Optimization

In enterprise environments, inefficient Docker setups cost real money in cloud compute and developer time. Here is a deep dive into optimizing your workflows.

### 12.1 CI/CD Pipeline Optimization

**The Problem:**
CI pipelines take 15+ minutes to build and test Docker images, costing developer time and CI runner minutes.

**The Solution:**
Implement external cache registries and inline caching.

**Advanced CI Build Command:**
```bash
docker buildx build \
  --push \
  --tag YOUR_REGISTRY/YOUR_IMAGE:latest \
  --cache-to type=registry,ref=YOUR_REGISTRY/YOUR_IMAGE:buildcache,mode=max \
  --cache-from type=registry,ref=YOUR_REGISTRY/YOUR_IMAGE:buildcache \
  .
```
This ensures that even on ephemeral CI runners, Docker can pull cache layers from the registry, drastically reducing build times.

### 12.2 Image Pull Policy Optimization

**The Problem:**
Docker Compose pulls images every time `docker compose up` is run, wasting bandwidth and time.

**The Solution:**
Set the `pull_policy` to `if_not_present` or `missing`.

**Compose Fix:**
```yaml
services:
  app:
    image: YOUR_REGISTRY/YOUR_IMAGE:v1.2.3
    pull_policy: if_not_present
```

### 12.3 Development Environment Sync (Compose Watch)

**The Problem:**
Developers rebuild containers for every code change, which is slow.

**The Solution:**
Use Docker Compose Watch (available in Compose V2.22+). It syncs files directly into the running container without rebuilding.

**Compose Fix:**
```yaml
services:
  web:
    image: my-web-app
    build: .
    develop:
      watch:
        # Sync source code changes directly
        - action: sync
          path: ./src
          target: /app/src
        # Rebuild if package.json changes
        - action: rebuild
          path: package.json
```
**Command:**
```bash
docker compose watch
```

---

## 13. Comprehensive Security Hardening

Security is not optional. A compromised container can lead to a compromised host.

### 13.1 Dropping Capabilities

By default, Docker containers run with a restricted set of Linux capabilities, but it's still more than most apps need.

**The Solution:**
Drop all capabilities and add back only what is strictly necessary.

**Compose Fix:**
```yaml
services:
  secure-app:
    image: secure-app:latest
    cap_drop:
      - ALL
    cap_add:
      - NET_BIND_SERVICE # Only allow binding to ports < 1024
```

### 13.2 Read-Only Root Filesystem

Prevent attackers from modifying the container's filesystem by making it read-only.

**Compose Fix:**
```yaml
services:
  immutable-app:
    image: immutable-app:latest
    read_only: true
    tmpfs:
      # Provide a temporary writable area for logs or temp files
      - /tmp
      - /var/run
```

### 13.3 Secrets Management

Never pass sensitive data (API keys, database passwords) via plain environment variables, as they can be exposed via `docker inspect`.

**The Solution:**
Use Docker Secrets (supported in Compose for local development as well).

**Compose Fix:**
```yaml
services:
  db:
    image: postgres:15
    environment:
      POSTGRES_PASSWORD_FILE: /run/secrets/db_password
    secrets:
      - db_password

secrets:
  db_password:
    file: ./secrets/db_password.txt
```

---

## 14. Docker Upgrade Strategies

Upgrading services in production without downtime requires careful orchestration.

### 14.1 Rolling Updates (Swarm/Compose Deploy)

When using Docker Swarm or compatible orchestrators, configure rolling updates to replace containers one by one.

**Compose Fix:**
```yaml
services:
  web:
    image: web-app:v2
    deploy:
      replicas: 3
      update_config:
        parallelism: 1
        delay: 10s
        order: start-first
        failure_action: rollback
```

### 14.2 Database Migrations

Never run database migrations automatically on container startup if you have multiple replicas, as they will race and potentially corrupt the database.

**The Solution:**
Run migrations as a separate, one-off task or an init container.

**Compose Fix (Init Container Pattern):**
```yaml
services:
  migration:
    image: my-app:latest
    command: ["npm", "run", "migrate"]
    profiles: ["tools"]
    depends_on:
      db:
        condition: service_healthy

  web:
    image: my-app:latest
    depends_on:
      migration:
        condition: service_completed_successfully
```

---

## 15. Deep Dive: Troubleshooting Network Partitions

In distributed systems, network partitions happen. Containers might lose connectivity to the database or other services.

### 15.1 Identifying the Partition

Use `docker exec` to run network diagnostics from within the affected container.

**Commands:**
```bash
# Check DNS resolution
docker exec -it <container_id> nslookup database-service

# Check port connectivity
docker exec -it <container_id> nc -zv database-service 5432

# Check routing table
docker exec -it <container_id> ip route
```

### 15.2 Recovering from Partitions

Ensure your applications implement exponential backoff and retry logic. Docker cannot fix application-level connection pooling issues once the network is restored.

---

## 16. Deep Dive: Storage Driver Optimization

The choice of storage driver drastically affects performance.

### 16.1 Overlay2 vs BTRFS vs ZFS

- **Overlay2:** The default and recommended driver for most Linux distributions. It is fast and efficient with inodes.
- **BTRFS/ZFS:** Useful for advanced snapshotting capabilities, but require specific host filesystem formatting and can consume more memory.

**Troubleshooting Overlay2:**
If `overlay2` is consuming too much space, it's often due to unoptimized Dockerfiles (too many layers) or containers writing heavily to their writable layer instead of a volume.

**Command to find large container layers:**
```bash
sudo du -sh /var/lib/docker/containers/* | sort -rh | head -n 10
```
If a container directory is huge, the application is writing data inside the container instead of a mounted volume. Fix this by mapping a volume to the application's data directory.

---

## 17. Final Production Checklist Review

Before deploying any Docker Compose stack to production, verify the following:

1. **No `:latest` tags:** All images must be pinned to a specific version or SHA.
2. **Resource Limits:** Every service must have `deploy.resources.limits` defined.
3. **Health Checks:** Every service must have a `healthcheck` defined.
4. **Restart Policies:** Set to `unless-stopped` or `on-failure`.
5. **Logging Limits:** `json-file` driver configured with `max-size` and `max-file`.
6. **Non-Root Users:** `USER` directive used in Dockerfiles.
7. **Volumes:** Named volumes used for all persistent data.
8. **Secrets:** Sensitive data passed via secrets, not environment variables.
9. **Networks:** Custom bridge networks used; default bridge avoided.
10. **Graceful Shutdown:** `stop_grace_period` configured for databases and stateful apps.

By adhering to these principles, you transition from merely running containers to orchestrating a robust, enterprise-grade infrastructure.

---

## 18. Exhaustive Guide to Dockerfile Optimization Techniques

To truly master Docker, one must understand the intricacies of the Dockerfile. Every instruction matters.

### 18.1 The Anatomy of a Perfect Dockerfile

A perfect Dockerfile is secure, minimal, and builds quickly. Let's dissect a production-ready Node.js Dockerfile.

```dockerfile
# syntax=docker/dockerfile:1.4
# 1. Pin the base image to a specific SHA for absolute immutability
FROM node:18.17.0-alpine3.18@sha256:1234567890abcdef... AS base

# 2. Set environment variables that apply to all stages
ENV NODE_ENV=production
ENV PORT=3000

# 3. Create a non-root user and group early
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nextjs -u 1001 -G nodejs

# 4. Set the working directory
WORKDIR /app

# --- Dependency Stage ---
FROM base AS dependencies
# 5. Copy only package files to leverage layer caching
COPY package.json package-lock.json ./
# 6. Install dependencies using a cache mount to speed up builds
RUN --mount=type=cache,target=/root/.npm \
    npm ci --ignore-scripts

# --- Build Stage ---
FROM base AS builder
COPY --from=dependencies /app/node_modules ./node_modules
COPY . .
# 7. Run the build process
RUN npm run build

# --- Production Stage ---
FROM base AS runner
# 8. Copy only the necessary artifacts from the builder stage
COPY --from=builder --chown=nextjs:nodejs /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

# 9. Switch to the non-root user
USER nextjs

# 10. Expose the port
EXPOSE 3000

# 11. Define a robust healthcheck
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:3000/api/health || exit 1

# 12. Start the application
CMD ["node", "server.js"]
```

### 18.2 Deep Dive: The `COPY` vs `ADD` Debate

While `COPY` and `ADD` seem similar, they have distinct behaviors. `COPY` simply copies files from the host to the container. `ADD` does this as well, but it also automatically extracts local tar archives and can download files from URLs.

**Why prefer `COPY`?**
Security and predictability. If you use `ADD` with a URL, it creates a layer with the downloaded file. If you then extract it and delete the archive in a subsequent `RUN` command, the archive still exists in the previous layer, bloating the image.

**The Anti-Pattern:**
```dockerfile
ADD https://example.com/app.tar.gz /tmp/
RUN tar -xzf /tmp/app.tar.gz -C /app && rm /tmp/app.tar.gz
```

**The Correct Pattern:**
```dockerfile
RUN wget -O /tmp/app.tar.gz https://example.com/app.tar.gz && \
    tar -xzf /tmp/app.tar.gz -C /app && \
    rm /tmp/app.tar.gz
```

---

## 19. Advanced Docker Networking Troubleshooting

Networking is often the most opaque part of Docker. Let's break down complex scenarios.

### 19.1 The Macvlan Network Driver

When you need a container to appear as a physical device on your network (e.g., for legacy applications that require a specific IP address or broadcast capabilities), you use the `macvlan` driver.

**The Problem:**
Containers on a `macvlan` network cannot communicate with the Docker host machine by default due to security restrictions in the Linux kernel.

**The Solution:**
Create a virtual interface on the host machine that bridges to the `macvlan` network.

**Configuration Example:**
```yaml
networks:
  physical_net:
    driver: macvlan
    driver_opts:
      parent: eth0
    ipam:
      config:
        - subnet: "192.168.1.0/24"
          gateway: "192.168.1.1"
```

### 19.2 Troubleshooting MTU (Maximum Transmission Unit) Mismatches

**The Problem:**
Containers can ping external IP addresses, but HTTP requests hang or timeout. This is a classic symptom of an MTU mismatch. If the Docker bridge MTU is larger than the host's physical interface MTU, packets get dropped.

**The Solution:**
Configure the Docker daemon to use a smaller MTU (e.g., 1400 or 1450, common in cloud environments like AWS or OpenStack).

**Fix (`/etc/docker/daemon.json`):**
```json
{
  "mtu": 1450
}
```

---

## 20. Exhaustive Guide to Docker Volumes and Storage

Data persistence is critical. Let's explore edge cases.

### 20.1 The `nocopy` Volume Option

**The Problem:**
When you mount an empty named volume into a container directory that already contains files (e.g., `/var/lib/mysql`), Docker automatically copies the existing files from the container into the volume. This is usually desired, but for massive directories, it can cause the container startup to hang for minutes.

**The Solution:**
Use the `nocopy` option to disable this behavior.

**Compose Fix:**
```yaml
services:
  db:
    image: massive-db-image
    volumes:
      - type: volume
        source: db-data
        target: /data
        volume:
          nocopy: true
```

### 20.2 Managing tmpfs Mounts

For highly sensitive data (like encryption keys generated at runtime) or high-performance scratch space, use `tmpfs`. Data in `tmpfs` is stored in the host's RAM and is never written to disk.

**Compose Fix:**
```yaml
services:
  secure-processor:
    image: processor
    tmpfs:
      - /app/secrets:size=64M,mode=1777
```

---

## 21. Docker Compose Profiles: Advanced Use Cases

Profiles allow you to define multiple environments in a single `compose.yaml` file.

### 21.1 The "Tools" Profile Pattern

Instead of installing debugging tools (like `pgadmin`, `redis-commander`, or `phpmyadmin`) on your host machine, define them in your Compose file under a `tools` profile. They won't start by default, saving resources.

**Compose Example:**
```yaml
services:
  api:
    image: my-api
    ports: ["8080:8080"]

  db:
    image: postgres:15

  pgadmin:
    image: dpage/pgadmin4
    profiles: ["tools"]
    ports: ["5050:80"]
    environment:
      PGADMIN_DEFAULT_EMAIL: admin@admin.com
      PGADMIN_DEFAULT_PASSWORD: root
```

**Usage:**
Start the normal stack: `docker compose up -d`
Start the stack with tools: `docker compose --profile tools up -d`

---

## 22. Handling Docker Daemon Disk Exhaustion

When `/var/lib/docker` fills up, the daemon crashes, and containers stop.

### 22.1 Moving the Docker Root Directory

If your root partition is small, move the Docker data directory to a larger mounted drive.

**The Solution:**
1. Stop Docker: `sudo systemctl stop docker`
2. Copy data: `sudo rsync -aP /var/lib/docker/ /mnt/large-drive/docker/`
3. Edit `/etc/docker/daemon.json`:
```json
{
  "data-root": "/mnt/large-drive/docker"
}
```
4. Start Docker: `sudo systemctl start docker`

### 22.2 Aggressive Pruning Scripts

For CI/CD servers, run a cron job to aggressively prune resources.

**Script (`/usr/local/bin/docker-cleanup.sh`):**
```bash
#!/bin/bash
# Remove containers exited more than 24 hours ago
docker container prune -f --filter "until=24h"
# Remove dangling images
docker image prune -f
# Remove volumes not used by at least one container
docker volume prune -f
# Remove unused networks
docker network prune -f
```

---

## 23. The Ultimate Troubleshooting Flowchart

When faced with a failing container, follow this exact sequence:

1. **Check the State:** `docker ps -a` (Is it running, exited, or restarting?)
2. **Check the Logs:** `docker logs <container_id>` (Look for application-level errors).
3. **Check the Inspect Data:** `docker inspect <container_id>` (Look at `State.ExitCode`, `State.OOMKilled`, and `State.Error`).
4. **Check the Host Resources:** `htop`, `df -h`, `free -m` (Is the host out of CPU, disk, or RAM?).
5. **Check the Network:** `docker network inspect <network_name>` (Are the containers on the same network?).
6. **Enter the Container (if running):** `docker exec -it <container_id> /bin/sh` (Test connectivity, permissions, and environment variables from the inside).
7. **Enter a Debug Container (if crashing):** `docker run -it --rm --entrypoint /bin/sh <image_name>` (Bypass the failing entrypoint to inspect the filesystem).

By systematically applying these steps, you can diagnose and resolve 99% of Docker issues.

---

## 24. Deep Dive: Docker Compose Healthchecks and Dependencies

A common pitfall in complex Docker Compose setups is managing the startup order of services. Simply using `depends_on` is often insufficient because it only waits for the dependent container to start, not for the service inside it to be ready.

### 24.1 The `service_healthy` Condition

To ensure a service is fully ready before its dependents start, you must use the `service_healthy` condition in conjunction with a robust healthcheck.

**The Problem:**
A web application attempts to connect to a database immediately upon startup, but the database is still initializing its internal structures. The web application crashes and enters a restart loop.

**The Solution:**
Define a healthcheck for the database and configure the web application to wait for it.

**Compose Fix:**
```yaml
services:
  web:
    image: my-web-app
    depends_on:
      db:
        condition: service_healthy

  db:
    image: postgres:15
    environment:
      POSTGRES_PASSWORD: secret
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 5s
      retries: 5
      start_period: 10s
```

### 24.2 Handling Circular Dependencies

Sometimes, services appear to have circular dependencies (e.g., Service A needs Service B to register, but Service B needs Service A to authenticate).

**The Solution:**
Redesign the architecture to break the cycle, or use an initialization script that polls for readiness instead of relying solely on Compose's `depends_on`.

---

## 25. Advanced Logging Strategies

Logs are your primary diagnostic tool. Default logging configurations can lead to disk exhaustion or lost information.

### 25.1 Centralized Logging with Fluentd or ELK

For production environments, do not rely on the default `json-file` driver. Forward logs to a centralized system.

**Compose Fix (Fluentd):**
```yaml
services:
  app:
    image: myapp
    logging:
      driver: "fluentd"
      options:
        fluentd-address: localhost:24224
        tag: docker.{{.Name}}
```

### 25.2 Filtering Logs

If an application is excessively noisy, you can filter logs at the daemon level or within the application itself.

**The Solution:**
Configure the application's logging framework (e.g., Winston for Node.js, Logback for Java) to output only warnings and errors in production, or use a sidecar container to filter logs before forwarding them.

---

## 26. Troubleshooting Docker Swarm

While Kubernetes is the dominant orchestrator, Docker Swarm is still widely used for its simplicity.

### 26.1 Node Eviction and Rebalancing

**The Problem:**
A node in the Swarm cluster fails, and its tasks are rescheduled on other nodes. When the node recovers, the tasks do not automatically rebalance back to it.

**The Solution:**
Force a rebalance by updating the service.

**Command:**
```bash
docker service update --force <service_name>
```

### 26.2 Overlay Network Issues in Swarm

**The Problem:**
Containers on different Swarm nodes cannot communicate over an overlay network.

**The Solution:**
Ensure the required ports for Swarm overlay networking are open on the host firewalls:
- TCP port 2377 for cluster management communications
- TCP and UDP port 7946 for communication among nodes
- UDP port 4789 for overlay network traffic

---

## 27. The Future of Docker: WebAssembly and WasmEdge

As the ecosystem evolves, WebAssembly (Wasm) is becoming a viable alternative to traditional Linux containers for certain workloads.

### 27.1 Running Wasm Workloads

Docker now supports running Wasm modules alongside standard containers.

**The Solution:**
Use the `io.containerd.wasmedge.v1` runtime.

**Compose Fix:**
```yaml
services:
  wasm-app:
    image: my-wasm-app
    runtime: io.containerd.wasmedge.v1
```

This allows for incredibly fast startup times and a smaller security footprint, ideal for edge computing scenarios.

---

## 28. Final Thoughts on Docker Mastery

Becoming a Docker Super Specialist is an ongoing journey. The landscape is constantly shifting with new features in BuildKit, Compose, and the underlying container runtimes (containerd, runc).

By internalizing the principles of immutability, least privilege, and observability, you can design systems that are not only robust but also elegant in their simplicity. Remember that every configuration choice has a trade-off, and the key to optimization is understanding those trade-offs in the context of your specific workload.

Always test your configurations in a staging environment that mirrors production as closely as possible, and never stop learning. The solutions provided in this guide represent the culmination of years of operational experience, but the true mark of a specialist is the ability to adapt these solutions to novel problems.

---

## 29. Deep Dive: Docker Resource Constraints and Cgroups

Understanding how Docker interacts with the Linux kernel's control groups (cgroups) is essential for diagnosing complex performance issues.

### 29.1 Cgroup v1 vs Cgroup v2

Modern Linux distributions (like Ubuntu 22.04+, Fedora 31+, Debian 11+) use cgroup v2 by default. This changes how resource limits are applied and monitored.

**The Problem:**
Monitoring tools or older container images might expect the cgroup v1 filesystem layout (`/sys/fs/cgroup/memory`, `/sys/fs/cgroup/cpu`) and fail when running on a cgroup v2 host.

**The Solution:**
Ensure your monitoring agents (like Prometheus Node Exporter or Datadog) are updated to support cgroup v2. If you absolutely must run legacy workloads, you can revert the host to cgroup v1 by adding `systemd.unified_cgroup_hierarchy=0` to the kernel boot parameters, though this is highly discouraged for new deployments.

### 29.2 CPU Shares vs CPU Quotas

Docker provides two primary ways to limit CPU usage: shares and quotas.

- **CPU Shares (`cpu_shares`):** This is a relative weight. If Container A has 1024 shares and Container B has 512, Container A will get twice as much CPU time *only if there is contention*. If the host is idle, Container B can use 100% of the CPU.
- **CPU Quotas (`cpus` in Compose v2):** This is an absolute limit. If you set `cpus: '0.5'`, the container will never use more than half of a single CPU core, even if the host is completely idle.

**The Problem:**
Setting strict CPU quotas can lead to CPU throttling, where the application is paused by the kernel because it exceeded its quota for a given period, leading to high latency spikes.

**The Solution:**
Monitor the `nr_throttled` metric in the cgroup statistics. If throttling is high but overall CPU usage is low, consider increasing the quota or switching to CPU shares for bursty workloads.

**Compose Fix (Using Shares for Bursty Workloads):**
```yaml
services:
  bursty-app:
    image: my-app
    deploy:
      resources:
        reservations:
          # Equivalent to cpu_shares: 512
          cpus: '0.5'
```

---

## 30. Advanced Docker Build Strategies for Monorepos

Monorepos (repositories containing multiple projects or services) present unique challenges for Docker builds, primarily around context size and caching.

### 30.1 The Context Size Problem in Monorepos

**The Problem:**
If you run `docker build .` from the root of a massive monorepo, Docker sends the entire repository to the daemon, which can take minutes and consume gigabytes of memory.

**The Solution:**
Use the `--build-context` flag (introduced in BuildKit) to selectively pass only the necessary directories to the build.

**Command Example:**
```bash
docker buildx build \
  --build-context app=./apps/my-app \
  --build-context shared=./packages/shared-lib \
  -f ./apps/my-app/Dockerfile \
  .
```

**Dockerfile Example:**
```dockerfile
# syntax=docker/dockerfile:1.4
FROM node:18-alpine
WORKDIR /workspace
# Copy from the named contexts
COPY --from=shared . ./packages/shared-lib
COPY --from=app . ./apps/my-app
RUN npm install
CMD ["npm", "start", "--workspace=apps/my-app"]
```

### 30.2 Caching Strategies for Monorepos

**The Problem:**
A change in one service invalidates the cache for all services if the Dockerfiles are not structured correctly.

**The Solution:**
Use tools like Turborepo, Nx, or Bazel to analyze the dependency graph and only build the services that have changed. Combine this with Docker layer caching.

---

## 31. Troubleshooting Docker on Windows (WSL2 Deep Dive)

Docker Desktop on Windows relies heavily on the Windows Subsystem for Linux (WSL2). This architecture introduces specific quirks.

### 31.1 Clock Drift in WSL2

**The Problem:**
When a Windows machine goes to sleep and wakes up, the clock inside the WSL2 VM (and therefore inside Docker containers) can drift significantly from the host clock. This causes issues with authentication tokens (like AWS STS or OAuth), database timestamps, and TLS certificate validation.

**Real Error/Symptom:**
```text
Signature expired: 2023-10-27T10:00:00Z is now earlier than 2023-10-27T10:05:00Z
```

**The Solution:**
Force a time sync inside the WSL2 VM.

**Command (Run in PowerShell or CMD):**
```powershell
wsl -d docker-desktop -e hwclock -s
```
Alternatively, restart the WSL service: `Restart-Service LxssManager`.

### 31.2 File System Performance (NTFS vs ext4)

**The Problem:**
Bind mounting a directory from the Windows host (e.g., `C:\Users\Dev\Project`) into a Linux container is extremely slow because every file operation must cross the 9P protocol boundary between Windows and the WSL2 VM.

**The Solution:**
Store your source code *inside* the WSL2 filesystem (e.g., `\\wsl$\Ubuntu\home\user\Project`) and run Docker from within the WSL2 terminal. This ensures all file operations occur natively on the ext4 filesystem, resulting in near-native Linux performance.

---

## 32. Docker and IPv6: The Complete Guide

As IPv4 exhaustion becomes a reality, supporting IPv6 in Docker is increasingly important.

### 32.1 Enabling IPv6 Support

**The Problem:**
By default, Docker networks only support IPv4. Containers cannot reach external IPv6 addresses, and external IPv6 traffic cannot reach containers.

**The Solution:**
Enable IPv6 in the daemon and configure a subnet.

**Fix (`/etc/docker/daemon.json`):**
```json
{
  "ipv6": true,
  "fixed-cidr-v6": "fd00::/80",
  "experimental": true,
  "ip6tables": true
}
```
*Note: `ip6tables: true` requires experimental features to be enabled in some Docker versions.*

### 32.2 IPv6 in Docker Compose

**The Problem:**
Even with daemon support, Compose networks default to IPv4.

**The Solution:**
Explicitly enable IPv6 on your custom networks.

**Compose Fix:**
```yaml
services:
  web:
    image: nginx
    networks:
      - dual-stack-net

networks:
  dual-stack-net:
    enable_ipv6: true
    ipam:
      config:
        - subnet: 172.20.0.0/16
        - subnet: "fd00:1234::/64"
```

---

## 33. Managing Docker Secrets in Production

While Docker Swarm has built-in secrets management, standalone Docker Compose requires a different approach for production.

### 33.1 The Problem with Environment Variables

Passing secrets via the `environment` block in Compose is insecure because:
1. They are visible in `docker inspect`.
2. They are often committed to version control in `.env` files.
3. They can be leaked if the application crashes and dumps its environment to the logs.

### 33.2 Using External Secret Managers

**The Solution:**
Integrate with external secret managers like HashiCorp Vault, AWS Secrets Manager, or Azure Secrets Manager.

**Implementation Pattern (Init Container):**
Use an init container or an entrypoint script to fetch secrets at runtime and inject them into the application process, rather than passing them through Docker.

**Entrypoint Script Example (`entrypoint.sh`):**
```bash
#!/bin/sh
# Fetch secret from AWS Secrets Manager
export DB_PASSWORD=$(aws secretsmanager get-secret-value --secret-id prod/db/password --query SecretString --output text)

# Execute the main application
exec "$@"
```

**Dockerfile:**
```dockerfile
FROM node:18-alpine
RUN apk add --no-cache aws-cli
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
COPY . /app
WORKDIR /app
ENTRYPOINT ["/entrypoint.sh"]
CMD ["node", "server.js"]
```

---

## 34. Docker Event Monitoring and Auditing

For compliance and security, you must know what is happening inside your Docker environment.

### 34.1 Docker Events

The Docker daemon emits a stream of events (start, stop, die, OOM, etc.).

**Command to monitor events in real-time:**
```bash
docker events --filter 'type=container' --filter 'event=die'
```

### 34.2 Integrating with SIEM

**The Solution:**
Use tools like Filebeat or Logstash to capture the Docker event stream and forward it to a Security Information and Event Management (SIEM) system like Splunk or Datadog.

This allows you to set up alerts for suspicious activities, such as a container repeatedly crashing (indicating a potential exploit attempt) or an unexpected container being started.

---

## 35. The Ultimate Docker Debugging Toolkit

When all else fails, you need specialized tools to inspect the running state of a container.

### 35.1 Using `nsenter`

**The Problem:**
A container is completely locked up, and `docker exec` hangs or fails.

**The Solution:**
Use `nsenter` to enter the container's namespaces directly from the host machine.

**Commands:**
```bash
# Get the PID of the container
PID=$(docker inspect --format '{{.State.Pid}}' <container_id>)

# Enter the container's network, mount, and UTS namespaces
sudo nsenter --target $PID --mount --uts --ipc --net --pid
```
This bypasses the Docker daemon entirely, allowing you to debug even if the daemon is unresponsive.

### 35.2 Strace and Sysdig

To understand exactly what an application is doing (e.g., why it's hanging on file I/O), trace its system calls.

**Command (Run on the host, targeting the container's PID):**
```bash
sudo strace -p $PID -f -c
```
This will show you which system calls are taking the most time or failing.

---

## 36. Conclusion and Continuous Improvement

The role of a Docker Super Specialist is not just to fix problems when they occur, but to architect systems that prevent them. By implementing the strategies detailed in this guide—from optimized multi-stage builds and strict resource limits to advanced networking and security hardening—you ensure that your containerized infrastructure is resilient, performant, and ready for the demands of modern production environments.

Remember that the container ecosystem is dynamic. Stay informed about updates to BuildKit, changes in the OCI specifications, and new features in Docker Compose. Continuous learning and proactive optimization are the hallmarks of true expertise.

---

## 37. Deep Dive: Docker Registry and Image Management

Managing images effectively is crucial for both performance and security. A bloated registry slows down deployments and increases storage costs.

### 37.1 Registry Garbage Collection

**The Problem:**
Over time, a private Docker registry accumulates thousands of untagged or obsolete images, consuming massive amounts of disk space.

**The Solution:**
Implement a strict garbage collection policy.

**Command (For Docker Distribution Registry):**
```bash
# First, delete the manifest (requires registry to be configured with delete=true)
curl -X DELETE -u user:pass https://registry.example.com/v2/my-image/manifests/sha256:abcdef...

# Then, run the garbage collector on the registry container
docker exec -it registry bin/registry garbage-collect /etc/docker/registry/config.yml
```

### 37.2 Image Signing and Content Trust

**The Problem:**
How do you guarantee that the image you are pulling is exactly the one built by your CI pipeline and hasn't been tampered with?

**The Solution:**
Enable Docker Content Trust (DCT) using Notary.

**Implementation:**
1. Generate delegation keys.
2. Sign the image during the push process.
3. Enforce DCT on the Docker daemon.

**Command:**
```bash
export DOCKER_CONTENT_TRUST=1
docker push YOUR_REGISTRY/YOUR_IMAGE:latest
```
When DCT is enabled, Docker will refuse to pull or run unsigned images.

---

## 38. Advanced Docker Compose: Extensions and Fragments

As Compose files grow, they become difficult to maintain. Compose provides mechanisms to keep them DRY (Don't Repeat Yourself).

### 38.1 YAML Anchors and Aliases

**The Problem:**
You have multiple services that share the same environment variables, logging configuration, and restart policies.

**The Solution:**
Use YAML anchors (`&`) and aliases (`*`).

**Compose Fix:**
```yaml
x-common-config: &common
  restart: unless-stopped
  logging:
    driver: json-file
    options:
      max-size: "10m"
  environment:
    - NODE_ENV=production

services:
  web:
    <<: *common
    image: my-web
    ports: ["80:80"]

  worker:
    <<: *common
    image: my-worker
```

### 38.2 Compose Extensions (`x-`)

Compose ignores any top-level field starting with `x-`. This is perfect for defining reusable blocks (like the `x-common-config` above) without triggering validation errors.

---

## 39. Troubleshooting Docker in CI/CD Environments

Running Docker inside Docker (DinD) or Docker outside Docker (DooD) in CI pipelines introduces specific challenges.

### 39.1 Docker in Docker (DinD) vs Docker outside Docker (DooD)

- **DinD:** Runs a complete Docker daemon inside a container. Requires `--privileged`, which is a significant security risk.
- **DooD:** Mounts the host's Docker socket (`/var/run/docker.sock`) into the container. The container uses the host's daemon.

**The Problem with DooD:**
If a container running DooD bind-mounts a directory (e.g., `-v $(pwd):/app`), the path `$(pwd)` is evaluated from the *host's* perspective, not the container's. This often results in empty directories being mounted.

**The Solution:**
Use named volumes to share data between the CI container and the sibling containers it spawns, or ensure the CI container's workspace path exactly matches the host's workspace path.

### 39.2 Ephemeral Runner Caching

**The Problem:**
CI runners (like GitHub Actions or GitLab CI) are ephemeral. They start with a clean slate, meaning Docker has no cache, leading to slow builds.

**The Solution:**
Use the `registry` cache backend for BuildKit, as discussed in section 12.1, or use CI-specific caching actions (e.g., `docker/build-push-action` with `cache-from` and `cache-to` configured for GitHub Actions cache).

---

## 40. Deep Dive: The `init` Process in Docker

Understanding how signals are handled in Docker is critical for graceful shutdowns.

### 40.1 The PID 1 Problem

**The Problem:**
When a container starts, the command specified in `ENTRYPOINT` or `CMD` runs as PID 1. In Linux, PID 1 has special responsibilities, including reaping zombie processes and handling signals (like `SIGTERM`). Many applications (like Node.js or Java) do not handle these responsibilities well.

**Real Error/Symptom:**
When you run `docker stop`, the container hangs for 10 seconds and then is forcefully killed (exits with code 137). This means the application didn't receive or process the `SIGTERM` signal, leading to potential data corruption or dropped connections.

**The Solution:**
Use an init process like `tini` or `dumb-init`, or use Docker's built-in `--init` flag.

**Compose Fix:**
```yaml
services:
  node-app:
    image: my-node-app
    init: true # Docker will inject a tiny init process as PID 1
```

### 40.2 Shell Form vs Exec Form

**The Problem:**
If you define your `CMD` using the shell form (`CMD npm start`), Docker wraps it in `/bin/sh -c`. The shell becomes PID 1, and it does *not* pass signals to the child process (`npm start`).

**The Solution:**
Always use the exec form (JSON array) for `CMD` and `ENTRYPOINT`.

**Before (Bad):**
```dockerfile
CMD npm start
```

**After (Good):**
```dockerfile
CMD ["npm", "start"]
```

---

## 41. Docker Storage Drivers: Advanced Tuning

While `overlay2` is the standard, tuning it can yield performance benefits.

### 41.1 XFS and Overlay2

If your host uses the XFS filesystem, `overlay2` requires the `d_type` feature to be enabled.

**The Problem:**
If `d_type` is not enabled, Docker will fall back to a less efficient mode or fail to start.

**The Solution:**
Verify `d_type` is enabled.
```bash
xfs_info /var/lib/docker | grep ftype
```
If `ftype=0`, you must reformat the XFS partition with `mkfs.xfs -n ftype=1`.

### 41.2 Device Mapper (Deprecated but still encountered)

If you inherit a legacy system using `devicemapper`, migrate away from it immediately. It is notoriously slow and prone to corruption.

**Migration Strategy:**
1. Stop Docker.
2. Backup all necessary data (export images, backup volumes).
3. Clear `/var/lib/docker`.
4. Configure `/etc/docker/daemon.json` to use `overlay2`.
5. Start Docker and restore data.

---

## 42. Final Review: The Super Specialist Mindset

To operate at the highest level of Docker expertise, you must adopt a specific mindset:

1. **Assume Nothing:** When a container fails, don't guess. Look at the logs, inspect the state, and trace the system calls.
2. **Immutability is Law:** Never patch a running container. If a configuration needs to change, update the Dockerfile or Compose file and redeploy.
3. **Security by Default:** Start with the most restrictive permissions (no root, read-only filesystem, dropped capabilities) and only add what is strictly necessary.
4. **Observability is Mandatory:** A container without health checks, resource limits, and centralized logging is a ticking time bomb.

By mastering the concepts, configurations, and troubleshooting techniques detailed in this exhaustive guide, you are equipped to handle any Docker challenge, optimize any workload, and ensure the stability and performance of enterprise-grade containerized infrastructure.

---

## 43. Deep Dive: Docker and GPU Acceleration

With the rise of machine learning and AI workloads, running GPU-accelerated containers is increasingly common. Troubleshooting GPU issues in Docker requires specific knowledge of the NVIDIA Container Toolkit.

### 43.1 The NVIDIA Container Toolkit

**The Problem:**
Containers cannot access the host's GPU. Running `nvidia-smi` inside the container returns `command not found` or fails to communicate with the NVIDIA driver.

**The Solution:**
Install the NVIDIA Container Toolkit on the host and configure Docker to use it.

**Host Installation (Ubuntu):**
```bash
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list
sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit
sudo systemctl restart docker
```

### 43.2 Configuring GPU Access in Compose

**The Problem:**
Even with the toolkit installed, Compose services do not automatically get GPU access.

**The Solution:**
Use the `deploy.resources.reservations.devices` block to request GPU access.

**Compose Fix:**
```yaml
services:
  ml-worker:
    image: tensorflow/tensorflow:latest-gpu
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
```

### 43.3 Troubleshooting CUDA Version Mismatches

**The Problem:**
The container starts, but the application crashes with errors related to CUDA libraries (e.g., `libcuda.so.1: cannot open shared object file`).

**The Solution:**
Ensure the CUDA version required by the application (and installed in the container image) is compatible with the NVIDIA driver version installed on the host. The host driver must support a CUDA version equal to or higher than the one used in the container.

---

## 44. Advanced Docker Security: User Namespaces

User namespaces provide an additional layer of security by mapping the root user inside the container to a non-root user on the host.

### 44.1 The Root Escalation Problem

**The Problem:**
If a container runs as root (UID 0) and an attacker breaks out of the container (e.g., via a kernel exploit), they have root access on the host machine.

**The Solution:**
Enable user namespace remapping (`userns-remap`).

### 44.2 Configuring User Namespaces

**Implementation:**
1. Configure the daemon to remap users.

**Fix (`/etc/docker/daemon.json`):**
```json
{
  "userns-remap": "default"
}
```
2. Restart Docker. Docker will create a user named `dockremap` and configure `/etc/subuid` and `/etc/subgid` to map the container's root user to a high, unprivileged UID on the host (e.g., 100000).

**The Trade-off:**
Enabling `userns-remap` can complicate volume mounts, as the host directory must be owned by the remapped UID (e.g., 100000) for the container to write to it.

---

## 45. Docker and Systemd Integration

Running systemd inside a Docker container is generally considered an anti-pattern, but it is sometimes necessary for legacy applications or complex testing environments.

### 45.1 The Systemd Anti-Pattern

**The Problem:**
Systemd expects to be PID 1 and requires access to specific cgroups and privileges that Docker restricts by default.

**The Solution:**
If you must run systemd, you need to run the container with elevated privileges and mount specific host directories.

**Compose Fix (Running Systemd):**
```yaml
services:
  legacy-app:
    image: centos/systemd
    privileged: true
    volumes:
      - /sys/fs/cgroup:/sys/fs/cgroup:ro
    command: ["/usr/sbin/init"]
```
*Warning: Running privileged containers is a severe security risk and should be avoided in production.*

---

## 46. Conclusion: The Path to Docker Mastery

This guide has covered the entire spectrum of Docker troubleshooting, from the basics of cache invalidation to the complexities of cgroup v2, IPv6, and GPU acceleration.

The true value of a Docker Super Specialist lies not just in knowing these solutions, but in understanding the underlying Linux primitives—namespaces, cgroups, union filesystems, and iptables—that make containers possible.

By continuously applying these best practices, enforcing strict security policies, and optimizing for performance, you can transform Docker from a simple development tool into a robust, enterprise-grade orchestration platform.

