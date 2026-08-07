# Lua Sandboxing

**Verified against upstream:** 2026-08-07
**Primary Source:** [Programming in Lua - Environments](https://www.lua.org/pil/14.html)

## Overview
This reference covers securing Lua execution environments and implementing sandboxing for untrusted code.

## Environment Hardening
- When executing untrusted Lua code, it is crucial to restrict access to potentially dangerous functions and libraries.
- Remove or restrict access to the `os`, `io`, `package`, and `debug` libraries.
- Use `load` or `loadfile` with a restricted environment (using the `env` parameter in Lua 5.2+) to execute untrusted code.

## Sandboxing Techniques
- Create a clean environment table containing only safe functions (e.g., `math`, `string`, `table`).
- Set the environment of the loaded chunk to the clean environment table before execution.
- Implement resource limits (e.g., memory, execution time) if supported by the embedding environment.
