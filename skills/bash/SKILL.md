---
name: bash
description: Specialist in advanced Bash and shell scripting, text processing, process management, and POSIX compliance.
---

# Bash Specialist Skill

## When to Use

Use this skill when you need to:
- Write, debug, or optimize Bash scripts for system automation.
- Perform complex text processing using utilities like `awk`, `sed`, and `grep`.
- Manage processes, job control, and signals in a UNIX-like environment.
- Ensure scripts are POSIX compliant for maximum portability across different systems.
- Handle file descriptors, redirections, and process substitutions efficiently.

## Sub-Agent Spawning

This skill supports spawning sub-agents for parallel execution when tasks can be decomposed:

| Trigger Condition | Sub-Agent Type | Purpose |
|---|---|---|
| Multiple scripts to review | Script Reviewer | Parallel code review and POSIX compliance check |
| Multiple log files to parse | Log Analyzer | Parallel text processing using awk/sed/grep |
| Multiple servers to configure | Config Deployer | Parallel execution of configuration scripts |
| Bulk data files to transform | Data Transformer | Parallel data extraction and transformation |

### Spawning Rules
- Spawn when 3+ independent items need the same operation
- Each sub-agent receives: context, specific target, success criteria
- Results are aggregated and cross-referenced for conflicts
- Maximum concurrent sub-agents: 10

## Workflow

1. **Requirement Analysis**: Understand the automation or processing task, target environment, and portability requirements.
2. **Script Design**: Outline the script structure, including functions, variables, and control flow. Choose appropriate tools (e.g., `awk` vs `sed`).
3. **Implementation**: Write the script using best practices (e.g., `set -euo pipefail`, proper quoting).
4. **Testing and Debugging**: Test the script in the target environment. Use `bash -x` for debugging.
5. **Optimization**: Refine text processing pipelines for performance and ensure robust error handling.
6. **Documentation**: Add comments and usage instructions to the script.

## Core Principles

- **Safety First**: Always use `set -euo pipefail` to catch errors early and prevent unintended consequences.
- **Quote Variables**: Always quote variables to prevent word splitting and globbing issues.
- **Prefer Built-ins**: Use shell built-ins over external commands when possible for better performance.
- **POSIX Compliance**: Write POSIX-compliant scripts (`#!/bin/sh`) when portability is a priority, avoiding Bash-specific extensions.
- **Modular Design**: Break down complex scripts into smaller, reusable functions.
- **Clear Error Messages**: Provide informative error messages and exit codes.

## Key References

- [Advanced Bash-Scripting Guide](https://tldp.org/LDP/abs/html/)
- [POSIX Shell Command Language](https://pubs.opengroup.org/onlinepubs/9699919799/utilities/V3_chap02.html)
- [GNU Bash Reference Manual](https://www.gnu.org/software/bash/manual/bash.html)
- `man bash`, `man awk`, `man sed`, `man grep`

---

## Adversarial Verification Panel

For each significant shell scripting issue (bugs, POSIX compliance violations, optimization opportunities) produced by the parallel sub-agents:

1. Spawn **3 independent Refuter Agents** per finding, each with:
   - The finding in full
   - Instruction: *"Assume this finding is wrong. Find the strongest argument against it."*
   - Default stance: `refuted=true` if evidence is insufficient or ambiguous
2. A finding is **confirmed** only if ≥2 refuters fail to refute it
3. A finding is **discarded** if ≥2 refuters succeed
4. When a confirmed finding had 1 successful refuter, include the dissenting argument in the output with a `CONTESTED` label

> This prevents plausible-but-wrong shell scripting issues (bugs, POSIX compliance violations, optimization opportunities) from reaching the final output. The 3-vote panel eliminates single-point hallucination without requiring unanimity.

## Cross-System Consistency Validator

After all parallel agents (Script Reviewer, Log Analyzer, Config Deployer, Data Transformer) complete, but **before** synthesis:

Run one **Consistency Validator Agent** with all parallel outputs that:
- Flags any pair of recommendations that logically contradict each other
  *(example: Script Reviewer recommending strict POSIX compliance while Config Deployer uses Bash-specific extensions for a configuration script)*
- Notes where one agent's output is a prerequisite for another agent's recommendation
- Passes contradictions to the Synthesis Agent as `MUST_RESOLVE` items
- Passes missing prerequisites as `SEQUENCING_REQUIRED` items

## Synthesis Agent (Upgraded)

The synthesis step actively resolves rather than aggregates:

1. **`MUST_RESOLVE` contradictions**: Pick the better recommendation, annotate the reasoning, preserve the dissenting view as a footnote
2. **`SEQUENCING_REQUIRED` items**: Re-order the unified script analysis report so prerequisites appear before the steps that depend on them
3. **Confidence calibration**: Label each finding `HIGH` / `MEDIUM` / `LOW` confidence based on refuter panel outcomes
4. **Gap analysis**: Note any analysis dimension not covered by any of the parallel agents — these are blind spots, not confirmed negatives
