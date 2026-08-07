---
name: bash
description: Specialist in advanced Bash and shell scripting, text processing, process management, and POSIX compliance. Triggers on requests to write, debug, or optimize shell scripts, or when tasks require complex text processing, process management, or POSIX-compliant automation.
---

# Bash Specialist Skill

## Scope and Triggers

Use this skill when you need to:
- Write, debug, or optimize Bash scripts for system automation.
- Perform complex text processing using utilities like `awk`, `sed`, and `grep`.
- Manage processes, job control, and signals in a UNIX-like environment.
- Ensure scripts are POSIX compliant for maximum portability across different systems.
- Handle file descriptors, redirections, and process substitutions efficiently.

**Non-goals:**
- Do not use this skill for tasks requiring long-running services, Docker, or heavy compute (route to `persistent-computing`).
- Do not use this skill for recurring execution, background execution, or event-triggered execution (route to `automation-and-scheduling`).

## Preconditions

Before acting, ensure:
- The target environment supports Bash or POSIX shell.
- Required permissions are available for the intended operations.
- User intent is clear, especially for destructive or production-impacting actions.

## Source Freshness

For version-sensitive facts, commands, and supported features, consult the official documentation or the bundled verified references.
- GNU Bash Reference Manual
- POSIX Shell Command Language specifications
Verify installed versions (`bash --version`) before applying destructive actions.

## Workflow

1. **Analyze Requirements**: Understand the automation or processing task, target environment, and portability requirements.
2. **Design Script**: Outline the script structure, including functions, variables, and control flow. Choose appropriate tools (e.g., `awk` vs `sed`).
3. **Implement Script**: Write the script using robust templates (e.g., `templates/bash-script-template.sh` with `set -euo pipefail`).
4. **Validate Syntax**: Run `scripts/validate-bash.sh` to validate the script syntax using `bash -n` and other checks.
5. **Test/Dry-Run**: Test the script in a safe or dry-run mode where feasible.
6. **Execute**: Execute the script. **Require confirmation** for destructive, external, privileged, or production-impacting actions.
7. **Handle Failures**: Diagnose errors and adjust the approach. Do not repeat identical failed actions.
8. **Output Result**: Output the final script and execution results according to the output contract.

## Safety

- **Read-only Discovery**: Separate read-only discovery from mutations.
- **Confirmation Required**: Require user confirmation for destructive, external, privileged, financial, legal, or production-impacting actions.
- **Safe Defaults**: Always use `set -euo pipefail` in generated scripts to catch errors early. Quote variables to prevent word splitting and globbing issues.

## Validation

- Define syntax checks using `bash -n`.
- Use dry runs where applicable.
- Capture evidence of successful execution or validation.

## Failure Handling

- Diagnose errors using exit codes and stderr output.
- Choose alternative approaches if a command fails.
- Provide rollback guidance for destructive actions.
- Avoid repeating a failed action unchanged.

## Output Contract

The result must include:
- The generated or modified script.
- Evidence of validation (e.g., `bash -n` output).
- Execution results or dry-run output.
- Actionable next steps or rollback instructions if applicable.

## Resources

- [Complete Reference](references/complete-reference.md): Detailed technical guidance, commands, and POSIX compliance rules.
- [Validate Bash Script](scripts/validate-bash.sh): Deterministic script to run syntax checks.
- [Bash Script Template](templates/bash-script-template.sh): Reusable template for robust Bash scripts.

## Orchestration

This skill supports spawning sub-agents for parallel execution when tasks can be decomposed (e.g., multiple scripts to review, multiple log files to parse).
- Spawn when 3+ independent items need the same operation.
- Each sub-agent receives: context, specific target, success criteria.
- Results are aggregated and cross-referenced for conflicts.
- Maximum concurrent sub-agents: 10.
