---
name: openclaw
description: Deploy, configure, and troubleshoot OpenClaw (Node.js) and ZeroClaw (Rust) AI agent runtimes.
---

# OpenClaw and ZeroClaw Operations Specialist

## Scope and Triggers

Use this skill when:
- Deploying, configuring, or troubleshooting **OpenClaw** (Node.js) or **ZeroClaw** (Rust) AI agent runtimes.
- Managing OpenClaw workspace bootstrap files (`AGENTS.md`, `SOUL.md`, `IDENTITY.md`, `USER.md`, `BOOTSTRAP.md`, `MEMORY.md`).
- Managing ZeroClaw's `config.toml` configuration.
- Diagnosing runtime issues, channel integration failures, or state corruption.

**Non-goals:**
- Do not use this skill for general Node.js or Rust development unrelated to these specific runtimes.
- Do not conflate OpenClaw and ZeroClaw; they are distinct systems with different architectures.

## Preconditions

Before acting, determine the target runtime:
1. **Identify Runtime:** Check the environment or user request to determine if the target is OpenClaw (Node.js) or ZeroClaw (Rust).
2. **Locate Configuration:**
   - For OpenClaw: Locate the workspace directory containing the bootstrap `.md` files and the SQLite state database (typically `~/.openclaw/state/openclaw.sqlite`).
   - For ZeroClaw: Locate the `config.toml` file.
3. **Verify Binaries:** Ensure the `openclaw` or `zeroclaw` CLI tools are installed and accessible in the system path.

## Source Freshness

Volatile facts such as supported versions, configuration schemas, and specific CLI flags must be verified against official documentation at runtime.
- **OpenClaw:** Verify against the [OpenClaw GitHub Repository](https://github.com/openclaw/openclaw) and [Documentation](https://docs.openclaw.ai/concepts/agent).
- **ZeroClaw:** Verify against the [ZeroClaw GitHub Repository](https://github.com/zeroclaw-labs/zeroclaw) and [Official Website](https://zeroclaw.net/).
- Consult the bundled `references/complete-reference.md` for baseline architecture and troubleshooting patterns (Verified: 2026-08-07).

## Workflow

1. **Identify Target:** Determine if the task involves OpenClaw or ZeroClaw.
2. **Discovery (Read-Only):**
   - **OpenClaw:** Inspect the workspace bootstrap files (`AGENTS.md`, `SOUL.md`, etc.) and check SQLite database integrity using `sqlite3 ~/.openclaw/state/openclaw.sqlite "PRAGMA integrity_check;"`.
   - **ZeroClaw:** Inspect `config.toml` and run `zeroclaw doctor` to validate the configuration.
3. **Execution:** Perform the requested configuration, deployment, or troubleshooting task.
   - Apply changes to the appropriate configuration files.
   - Restart the runtime service if necessary.
4. **Validation:**
   - **OpenClaw:** Run `openclaw setup` to verify workspace initialization.
   - **ZeroClaw:** Run `zeroclaw doctor` again to ensure the configuration remains valid.
5. **Stop Condition:** The task is complete when the runtime is functioning correctly, configuration changes are applied and validated, and no errors are reported by the respective diagnostic tools.

## Safety

- **Read-Only First:** Always inspect configurations and run diagnostic commands (`zeroclaw doctor`, SQLite integrity checks) before making changes.
- **Confirmation Required:** Require user confirmation before modifying configuration files, restarting production services, or executing destructive database operations.
- **No Untrusted Code:** Do not download or execute untrusted extensions or skills without explicit user approval and verification.

## Validation

- **OpenClaw:** `openclaw setup` must complete without errors. SQLite integrity check must return `ok`.
- **ZeroClaw:** `zeroclaw doctor` must report a healthy configuration.
- **Syntax:** Any modified JSON or TOML files must pass syntax validation before restarting services.

## Failure Handling

- If `openclaw setup` or `zeroclaw doctor` fails, review the error output, correct the configuration syntax or missing dependencies, and retry.
- If SQLite database corruption is detected in OpenClaw, attempt to restore from a backup before proceeding with destructive recovery.
- Do not repeat the same failed command without modifying the configuration or environment.

## Output Contract

The final output must include:
- The target runtime identified (OpenClaw or ZeroClaw).
- A summary of configuration changes made or issues diagnosed.
- The results of validation commands (`openclaw setup`, `zeroclaw doctor`, or SQLite integrity checks).
- Any actionable next steps or unresolved warnings.

## Resources

- [Complete Reference Guide](references/complete-reference.md): Architecture, configuration, and troubleshooting for OpenClaw and ZeroClaw.
