---
name: cron-master
description: Master of cron and cron scheduling across local and Docker environments. Use for creating, troubleshooting, configuring, and executing scheduled tasks using cron syntax, system crontab, Docker cron solutions (like Supercronic and Ofelia), and host-to-container execution patterns.
---

# Cron Master

This skill provides comprehensive guidance on configuring, executing, and troubleshooting cron jobs in both local machine environments and Docker containerized environments. It guarantees 100% correct execution by following strict best practices and avoiding common pitfalls.

## Core Concepts & Syntax

Cron uses a 5-field time scheduling syntax followed by the command to execute:

```
*    *    *    *    *   /path/to/command
|    |    |    |    |
|    |    |    |    +-- Day of week (0-7, Sunday is 0 or 7)
|    |    |    +------- Month (1-12)
|    |    +------------ Day of month (1-31)
|    +----------------- Hour (0-23)
+---------------------- Minute (0-59)
```

**Syntax Operators:**
- `*`: Any value (e.g., `*` in hour means every hour)
- `,`: Value list separator (e.g., `1,15` in day means 1st and 15th)
- `-`: Range of values (e.g., `1-5` in day of week means Monday to Friday)
- `/`: Step values (e.g., `*/5` in minute means every 5 minutes)

For detailed syntax examples, see `references/syntax.md`.

## Environment 1: Local Machine (Host OS)

When running on a standard Linux host, cron jobs are managed via the system cron daemon (`crond`).

### Execution Workflow (100% Correct Pattern)

1. **Verify Environment Variables:** Cron runs with a minimal environment. ALWAYS use absolute paths for executables (e.g., `/usr/bin/node` instead of `node`).
2. **Handle Output:** NEVER discard output blindly. Always redirect `stdout` and `stderr` to a log file or to `syslog`.
3. **Use Dedicated Users:** Apply the principle of least privilege. Run jobs as a specific user, not root, unless necessary.
4. **Prevent Overlaps:** Use a lock mechanism (like `flock`) for long-running jobs to prevent multiple instances.

### Standard Local Crontab Pattern

```bash
# Set essential environment variables at the top
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
MAILTO=admin@example.com

# Use absolute paths and redirect output correctly
*/5 * * * * /usr/bin/flock -n /tmp/myjob.lock /opt/myapp/script.sh >> /var/log/myapp/cron.log 2>&1
```

For complete local machine best practices, see `references/local_machine.md`.

## Environment 2: Docker Containers

Running cron inside Docker requires special handling because traditional cron violates container principles (single process per container) and loses environment variables.

### The OpenClaw / Production Pattern

When running systems like OpenClaw inside Docker, you MUST choose one of the three robust patterns depending on your architecture.

### Pattern A: Supercronic (Recommended for Production)

Supercronic is a cron replacement designed specifically for containers. It solves environment variable loss, logs to stdout/stderr naturally, and handles graceful shutdowns.

**Execution Workflow:**
1. Use an image that installs `supercronic`.
2. Write a standard crontab file.
3. Set `supercronic /etc/crontab` as the container's CMD.

See `references/docker_supercronic.md` for the exact Dockerfile and implementation details.

### Pattern B: Host Cron with Docker Exec (The OpenClaw Example)

If you have a running container (e.g., OpenClaw) and want to trigger tasks inside it without modifying its image, use the host machine's cron to trigger `docker exec`.

**Execution Workflow:**
1. Ensure the target container is running with a stable name (e.g., `openclaw_app`).
2. On the **host machine**, create a cron job that executes the command inside the container.
3. Always check if the container is running before executing to avoid errors.

**Example Implementation for OpenClaw:**

```bash
# On the HOST machine's crontab:
# Run data sync inside the OpenClaw container every hour
0 * * * * /usr/bin/docker exec openclaw_app /usr/local/bin/python /app/sync_data.py >> /var/log/openclaw_cron.log 2>&1
```

For a robust wrapper script that checks container state first, see `scripts/docker-cron-wrapper.sh`.

### Pattern C: Dedicated Job Launcher (Ofelia)

For complex multi-container setups (like Docker Compose), use a dedicated scheduler container like Ofelia that mounts the Docker socket and triggers jobs via labels.

See `references/docker_ofelia.md` for Docker Compose configuration.

## Troubleshooting

If a cron job fails:
1. **Check paths:** Are you using absolute paths?
2. **Check permissions:** Does the script have `+x` execution rights?
3. **Check environment:** Did you rely on an env var that cron doesn't have?
4. **Check logs:** Look at `/var/log/syslog` or the specific redirected log file.
5. **Check newline:** Does the crontab file end with an empty newline (LF)?

For a complete troubleshooting checklist, see `references/troubleshooting.md`.

---

## Adversarial Verification Panel

For each significant scheduling issues and configuration errors produced by the parallel sub-agents:

1. Spawn **3 independent Refuter Agents** per finding, each with:
   - The finding in full
   - Instruction: *"Assume this finding is wrong. Find the strongest argument against it."*
   - Default stance: `refuted=true` if evidence is insufficient or ambiguous
2. A finding is **confirmed** only if ≥2 refuters fail to refute it
3. A finding is **discarded** if ≥2 refuters succeed
4. When a confirmed finding had 1 successful refuter, include the dissenting argument in the output with a `CONTESTED` label

> This prevents plausible-but-wrong scheduling issues and configuration errors from reaching the final output. The 3-vote panel eliminates single-point hallucination without requiring unanimity.

## Cross-System Consistency Validator

After all parallel agents (Supercronic Agent, Host Cron with Docker Exec Agent, Ofelia Agent) complete, but **before** synthesis:

Run one **Consistency Validator Agent** with all parallel outputs that:
- Flags any pair of recommendations that logically contradict each other
  *(example: the Supercronic Agent recommends making cron the container's sole CMD process, while the Host Cron with Docker Exec Agent recommends keeping the existing container image unchanged and triggering jobs from the host — these conflict when the container already runs a primary service)*
- Notes where one agent's output is a prerequisite for another agent's recommendation
- Passes contradictions to the Synthesis Agent as `MUST_RESOLVE` items
- Passes missing prerequisites as `SEQUENCING_REQUIRED` items

## Synthesis Agent (Upgraded)

The synthesis step actively resolves rather than aggregates:

1. **`MUST_RESOLVE` contradictions**: Pick the better recommendation, annotate the reasoning, preserve the dissenting view as a footnote
2. **`SEQUENCING_REQUIRED` items**: Re-order the unified cron configuration plan so prerequisites appear before the steps that depend on them
3. **Confidence calibration**: Label each finding `HIGH` / `MEDIUM` / `LOW` confidence based on refuter panel outcomes
4. **Gap analysis**: Note any analysis dimension not covered by any of the parallel agents — these are blind spots, not confirmed negatives
