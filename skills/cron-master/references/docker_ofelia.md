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

## Why this is 100% Correct for Complex Setups:
- **Centralized Scheduling:** You manage all schedules via labels in your `docker-compose.yml`, making it highly visible.
- **Zero Image Modification:** You don't need to install `cron` or `supercronic` in your application images.
- **True Isolation:** Using `job-run` ensures heavy cron jobs don't steal resources from your running web servers.
