# Troubleshooting

## Overview
This reference provides a structured troubleshooting guide for networking, storage, and performance issues.

## Networking Issues
- Check container IP addresses and network attachments: `docker network inspect <network>`
- Verify port mappings: `docker port <container>`
- Test connectivity between containers using `ping` or `curl` from within a container.

## Storage Issues
- Inspect volume mounts: `docker inspect -f '{{ .Mounts }}' <container>`
- Check disk usage: `docker system df`
- Clean up unused data (requires confirmation): `docker system prune`

## Performance Issues
- Monitor container resource usage: `docker stats`
- Inspect container logs for errors or warnings: `docker logs <container>`

## Authoritative Source
- Docker Troubleshooting Documentation: https://docs.docker.com/engine/daemon/troubleshoot/
Verified against upstream: 2026-08-07.
