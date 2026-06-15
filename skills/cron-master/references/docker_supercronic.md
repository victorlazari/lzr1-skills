# Docker Pattern A: Supercronic

When you need a container to act solely as a cron scheduler (or when you want to run cron alongside your app in a container, though less ideal), traditional cron (`crond`) fails because:
1. It drops environment variables.
2. It expects to run as PID 1 but doesn't handle signals properly.
3. It logs to syslog, making `docker logs` useless.

**Supercronic** is a cron replacement built specifically for containers that solves all these issues.

## Implementation Guide

### 1. Dockerfile

Here is the standard pattern for installing and running Supercronic:

```dockerfile
FROM alpine:3.19

# Define Supercronic version
ARG SUPERCRONIC_VERSION=0.2.29
ARG TARGETARCH=amd64

# Download and install Supercronic
RUN wget -q "https://github.com/aptible/supercronic/releases/download/v${SUPERCRONIC_VERSION}/supercronic-linux-${TARGETARCH}" \
    -O /usr/local/bin/supercronic && \
    chmod +x /usr/local/bin/supercronic

# Copy your crontab file
COPY crontab /etc/crontab

# Set Supercronic as the main process
CMD ["supercronic", "/etc/crontab"]
```

### 2. Crontab File

Your `crontab` file uses standard cron syntax. Because Supercronic inherits the container's environment variables, you can use them directly!

```bash
# /etc/crontab
# Supercronic passes environment variables properly
* * * * * echo "Connecting to database at: $DATABASE_URL"

# Standard scheduled tasks
0 2 * * * /app/scripts/backup.sh
```

### 3. Docker Compose Example

The best practice is to run your cron scheduler as a separate service that shares the same environment as your main application.

```yaml
services:
  app:
    image: myapp:latest
    environment:
      - DATABASE_URL=postgres://db:5432/app

  # Dedicated cron service
  cron:
    build:
      context: .
      dockerfile: Dockerfile.cron
    environment:
      # Shares the same env vars
      - DATABASE_URL=postgres://db:5432/app
    depends_on:
      - db
```

### Why this is 100% Correct for Production:
- **Environment Variables:** `DATABASE_URL` and others are fully available to the cron scripts.
- **Logging:** Supercronic logs job output directly to `stdout`/`stderr`, so `docker logs my_cron_container` works perfectly.
- **Graceful Shutdown:** Supercronic handles SIGTERM properly, allowing jobs to finish or terminate cleanly when the container stops.
