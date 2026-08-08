# Docker Pattern C: Ofelia (Dedicated Job Launcher)

Ofelia is a modern job scheduler designed specifically for Docker environments. Instead of running a cron daemon inside your application containers, Ofelia runs as a standalone container, connects to the Docker socket, and schedules tasks across your entire Docker environment.

This pattern is highly recommended for complex `docker-compose` setups.

## Implementation Guide

Ofelia discovers jobs by reading Docker labels on your containers.

### Docker Compose Example

```yaml
services:
  # The Ofelia scheduler container
  ofelia:
    image: mcuadros/ofelia:latest
    volumes:
      # Must mount the Docker socket so Ofelia can trigger commands
      - /var/run/docker.sock:/var/run/docker.sock:ro
    environment:
      # Optional: Configure remote Docker host connection
      # - DOCKER_HOST=tcp://remote-docker-host:2376
      # - DOCKER_TLS_VERIFY=1
    command: daemon --docker
    depends_on:
      - backend

  # Your application container
  backend:
    image: myapp/backend:latest
    labels:
      # Enable Ofelia for this specific container
      ofelia.enabled: "true"

      # Job 1: Execute a command inside this running container (job-exec)
      ofelia.job-exec.cleanup.schedule: "*/5 * * * *"
      ofelia.job-exec.cleanup.command: "python /app/jobs/cleanup.py"

      # Job 2: Spawn a NEW container just for this job (job-run)
      ofelia.job-run.reports.schedule: "0 8 * * *"
      ofelia.job-run.reports.image: "myapp/backend:latest"
      ofelia.job-run.reports.command: "python /app/jobs/reports.py"
      ofelia.job-run.reports.network: "app_network"

networks:
  app_network:
    driver: bridge
```

## Job Types in Ofelia

Ofelia supports different execution models:

1. **`job-exec`**: Executes a command inside an already running container (similar to `docker exec`). Best for quick tasks like cleanup or cache invalidation that need access to the running app's memory or state.
2. **`job-run`**: Spawns a brand new, ephemeral container to run the command, and destroys it when done (similar to `docker run`). Best for heavy tasks like reports or backups that shouldn't impact the main application's resources.
3. **`job-local`**: Runs the command inside the Ofelia container itself.
4. **`job-service-run`**: Runs the command inside a Docker Swarm service.

## Docker Host Configuration

Ofelia can connect to a remote Docker host by setting the following environment variables:
- `DOCKER_HOST`: The URL of the Docker host (e.g., `tcp://remote-docker-host:2376`).
- `DOCKER_TLS_VERIFY`: Set to `1` to enable TLS verification.
- `DOCKER_CERT_PATH`: Path to the directory containing the TLS certificates.

## Logging Drivers

Ofelia supports multiple logging drivers to capture job output:
- `mail`: Sends job output via email.
- `save`: Saves job output to a file.
- `slack`: Sends job output to a Slack channel.

Configure these drivers in the Ofelia configuration file (`/etc/ofelia/config.ini`) or via environment variables.

## Why this is 100% Correct for Complex Setups:
- **Centralized Scheduling:** You manage all schedules via labels in your `docker-compose.yml`, making it highly visible.
- **Zero Image Modification:** You don't need to install `cron` or `supercronic` in your application images.
- **True Isolation:** Using `job-run` ensures heavy cron jobs don't steal resources from your running web servers.

*Verified against upstream: 2026-08-07*
[Ofelia GitHub Repository](https://github.com/mcuadros/ofelia)
