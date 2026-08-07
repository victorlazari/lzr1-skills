---
name: lua
description: Execute Lua tasks including syntax validation, C API integration, sandboxing, and Redis scripting.
---

# Lua Specialist Skill

## Scope and Triggers
Use this skill when you need to:
- Write, debug, or optimize Lua scripts for embedded systems, game engines, or Redis.
- Integrate Lua with C/C++ applications using the Lua C API.
- Secure Lua execution environments and implement sandboxing.
- Validate Lua script syntax.

**Escalation Boundaries:**
- For Redis cluster management or non-Lua Redis operations, route to `redis-admin`.
- For primary C/C++ application development rather than Lua embedding, route to `c-cpp-developer`.
- For building a complete browser game rather than specific Lua game logic, route to `game-dev`.

## Preconditions
- Identify the target environment (standalone, embedded, Redis, game engine).
- Verify installed Lua versions and available tools (`luac`, `luacheck`).
- Determine if the code to be executed is trusted or untrusted.

## Source Freshness
- Volatile facts such as C API yielding rules or Redis script limitations are documented in focused references with explicit verification dates.
- Verify current upstream documentation for specific version behaviors before applying destructive or production-impacting actions.

## Workflow
1. Analyze the target environment (standalone, embedded, Redis, game engine) and constraints.
2. Validate the Lua script syntax using `scripts/validate-lua.sh`.
3. If embedding in C/C++, consult `references/c-api.md` for stack management and yielding rules.
4. If executing untrusted code, apply sandboxing rules from `references/sandboxing.md`.
5. If deploying to Redis, verify script constraints against `references/redis.md`.
6. Execute the script or integration, capturing output and errors.
7. Stop when the script executes successfully or fails with a clear diagnostic.

## Safety
- Separate read-only discovery from mutations.
- Require confirmation before executing untrusted Lua code.
- Ensure strict sandboxing (removing `os`, `io`, `package`) when running external scripts.
- Verify stack balance in C API integrations.

## Validation
- Validate all Lua scripts using `scripts/validate-lua.sh` (`luac -p` or `luacheck`) before execution.
- Define syntax checks, dry runs, tests, evidence capture, and postcondition verification.

## Failure Handling
- If a script fails syntax validation, analyze the error message and correct the syntax.
- If execution fails, capture the error output, diagnose the issue, and apply a fix.
- Do not repeat a failed action unchanged.

## Output Contract
- Provide a clear summary of the executed Lua tasks.
- Include the output of syntax validation and execution.
- Specify any unresolved issues or required next steps.

## Resources
- [Lua C API Integration](references/c-api.md): Focused reference on Lua C API integration, stack management, and yielding.
- [Redis Lua Scripting](references/redis.md): Focused reference on Redis Lua scripting, performance, and security.
- [Lua Sandboxing](references/sandboxing.md): Focused reference on securing Lua execution and sandboxing.
- [Lua Performance](references/performance.md): Focused reference on Lua performance tuning, tables, and garbage collection.
- [Validate Lua Script](scripts/validate-lua.sh): Deterministic script to run `luac -p` or `luacheck` for syntax validation.

## Source Map
- Lua 5.4 Reference Manual: https://www.lua.org/manual/5.4/
- Programming in Lua: https://www.lua.org/pil/
- Redis Lua Scripting Documentation: https://redis.io/docs/manual/programmability/
