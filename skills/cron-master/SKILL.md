---
name: cron-master
description: Master of cron and cron scheduling across local and Docker environments. Use for creating, troubleshooting, configuring, and executing scheduled tasks using cron syntax, system crontab, Docker cron solutions (like Supercronic and Ofelia), and host-to-container execution patterns.
---

# Cron Master

This skill provides comprehensive guidance on configuring, executing, and troubleshooting cron jobs in both local machine environments and Docker containerized environments. It guarantees 100% correct execution by following strict best practices and avoiding common pitfalls.

## Scope and Triggers

- **Handles:** Creating, troubleshooting, configuring, and executing scheduled tasks using cron syntax, system crontab, Docker cron solutions (Supercronic, Ofelia), and host-to-container execution patterns.
- **Activates:** When the user requests to schedule a task, troubleshoot a failing cron job, or configure cron in a Docker environment.
- **Non-goals:** Does not cover complex workflow orchestration (e.g., Airflow, Temporal) or application-level scheduling libraries (e.g., Celery, Quartz).
- **Escalation boundaries:** For complex automation, background execution, or event-triggered execution beyond simple time-based scheduling, consult the `automation-and-scheduling` skill. For long-running background jobs on persistent VMs, consult the `persistent-computing` skill.

## Preconditions

Before modifying any cron configuration, you must:
1. Identify the target environment (local machine, existing container, or complex Docker Compose setup).
2. Verify the current user's permissions (can they edit the crontab or deploy containers?).
3. Check for existing cron jobs to avoid conflicts.
4. Confirm the availability of required tools (e.g., `crontab`, `docker`, `supercronic`).

## Source Freshness

Cron syntax and basic local machine patterns are stable. However, Docker-based solutions (Supercronic, Ofelia) may evolve.
- Always verify the installed versions of Supercronic and Ofelia.
- Consult the official documentation for the most up-to-date configuration options.
- See the `Verified against upstream: 2026-08-07` markers in the reference files for the latest verified features.

## Workflow

1. **Identify Environment:** Determine if the target is a local machine, a single Docker container, or a multi-container setup.
2. **Select Pattern:**
   - Local Machine: Use standard `crontab`. See `references/local_machine.md`.
   - Single Container (Production): Use Supercronic. See `references/docker_supercronic.md`.
   - Existing Container (Host-to-Container): Use Host Cron with Docker Exec. See `scripts/docker-cron-wrapper.sh`.
   - Multi-Container (Docker Compose): Use Ofelia. See `references/docker_ofelia.md`.
3. **Read Reference:** Consult the appropriate reference file for syntax and configuration details. See `references/syntax.md` for standard cron syntax.
4. **Validate Syntax:** Validate the cron syntax and script permissions locally before applying.
5. **Apply Configuration:** Apply the configuration. **Require user confirmation before modifying system crontabs or deploying new scheduler containers.**
6. **Verify Execution:** Verify execution by checking logs or using a dry-run/simulated environment. See `references/troubleshooting.md` if issues arise.
7. **Stop:** Stop when the cron job is successfully scheduled and verified.

## Safety

- **Discovery vs. Mutation:** Always read existing crontabs (`crontab -l`) and container configurations before making changes.
- **Confirmation:** Require explicit user confirmation before applying any destructive, external, privileged, or production-impacting actions (e.g., `crontab -e`, `docker-compose up -d`).
- **Least Privilege:** Run jobs as a dedicated user, not root, unless absolutely necessary.

## Validation

- **Syntax Checks:** Use `bash -n` to check shell scripts.
- **Dry Runs:** If possible, run the script manually in a simulated environment (`env -i /bin/bash -c '/path/to/script.sh'`) before scheduling it.
- **Postcondition Verification:** Check the designated log files or syslog to confirm the job executed successfully at the scheduled time.

## Failure Handling

- If a cron job fails, consult `references/troubleshooting.md`.
- Diagnose errors by checking paths, permissions, environment variables, and logs.
- Do not repeat a failed action unchanged. Adjust the configuration based on the error logs and try again.
- If a new configuration fails, roll back to the previous working state.

## Output Contract

When completing a cron-related task, the output must include:
- **Structure:** A clear summary of the applied configuration (e.g., the crontab entry or Docker Compose snippet).
- **Evidence:** Log output or command results confirming the configuration was applied successfully.
- **Severity/Confidence:** High confidence if the job was verified to run; Medium if only the syntax was validated.
- **Actionable Next Steps:** Instructions for the user on how to monitor the job or modify it in the future.

## Resources

- [Local Machine Best Practices](references/local_machine.md): Guidance for standard Linux host cron.
- [Docker Pattern A: Supercronic](references/docker_supercronic.md): Best practice for running cron inside a container.
- [Docker Pattern C: Ofelia](references/docker_ofelia.md): Best practice for complex Docker Compose setups.
- [Cron Syntax Reference](references/syntax.md): Standard 5-field cron syntax and examples.
- [Troubleshooting Checklist](references/troubleshooting.md): Steps to diagnose and fix failing cron jobs.
- [Docker Cron Wrapper Script](scripts/docker-cron-wrapper.sh): Safe wrapper for executing commands in containers from the host.
