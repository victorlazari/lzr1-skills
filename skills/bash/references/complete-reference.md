# Complete Reference: Bash and Shell Scripting

## Source Map and Authoritative References

- **GNU Bash Reference Manual**: Canonical source for Bash-specific features, built-ins, and syntax. [https://www.gnu.org/software/bash/manual/bash.html](https://www.gnu.org/software/bash/manual/bash.html) (Verified against upstream: 2026-08-07)
- **POSIX Shell Command Language**: Canonical source for POSIX compliance and portable shell scripting. [https://pubs.opengroup.org/onlinepubs/9699919799/utilities/V3_chap02.html](https://pubs.opengroup.org/onlinepubs/9699919799/utilities/V3_chap02.html) (Verified against upstream: 2026-08-07)
- **Advanced Bash-Scripting Guide**: Comprehensive guide for advanced scripting techniques. [https://tldp.org/LDP/abs/html/](https://tldp.org/LDP/abs/html/) (Verified against upstream: 2026-08-07)

## Normative Requirements

### 1. Safety and Robustness
- **Strict Mode**: All scripts MUST start with `set -euo pipefail` unless explicitly required otherwise.
  - `-e`: Exit immediately if a command exits with a non-zero status.
  - `-u`: Treat unset variables as an error when substituting.
  - `-o pipefail`: The return value of a pipeline is the status of the last command to exit with a non-zero status.
- **Quoting**: All variable expansions MUST be double-quoted (e.g., `"$var"`) to prevent word splitting and globbing, unless word splitting is explicitly desired.
- **Variable Scope**: Variables within functions MUST be declared as `local` to prevent unintended global scope pollution.

### 2. POSIX Compliance vs. Bash Extensions
- **Shebang**: Use `#!/bin/sh` for POSIX-compliant scripts and `#!/usr/bin/env bash` or `#!/bin/bash` for scripts utilizing Bash extensions.
- **Conditionals**: Use `[ ]` for POSIX compliance. Use `[[ ]]` for Bash-specific advanced pattern matching and logical operations.
- **Arrays**: Arrays are a Bash extension and MUST NOT be used in POSIX-compliant scripts.

### 3. Text Processing
- **Awk**: Use `awk` for column-based data extraction and complex text processing.
- **Sed**: Use `sed` for stream editing and regular expression-based substitutions.
- **Grep**: Use `grep` for searching text using regular expressions.

### 4. File Descriptors and Redirection
- **Standard Streams**: Understand `0` (stdin), `1` (stdout), and `2` (stderr).
- **Redirection**: Use `>` to overwrite, `>>` to append, and `2>&1` to redirect stderr to stdout.
- **Process Substitution**: Use `<(command)` or `>(command)` in Bash to treat command output/input as a file.

## Validation and Testing
- **Syntax Check**: Always run `bash -n script.sh` to check for syntax errors without executing the script.
- **Debugging**: Use `bash -x script.sh` to print commands and their arguments as they are executed.
