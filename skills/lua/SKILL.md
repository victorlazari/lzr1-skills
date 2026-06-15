---
name: lua
description: Comprehensive Lua specialist skill covering fundamentals, advanced tables, metatables, coroutines, C API integration, Redis Lua scripting, game development, security auditing, and performance tuning.
---

# Lua Specialist Skill

## When to Use

Use this skill when you need to:
- Write, debug, or optimize Lua scripts for embedded systems, game engines (e.g., Love2D, Defold, Corona SDK), or Redis.
- Design advanced Lua architectures using tables, metatables, and metamethods for object-oriented or data-driven patterns.
- Implement cooperative multitasking and asynchronous workflows using Lua coroutines.
- Integrate Lua with C/C++ applications using the Lua C API, including stack management and userdata.
- Perform security audits on Lua codebases, including sandboxing, environment hardening, and preventing injection attacks.
- Troubleshoot performance bottlenecks, memory leaks, or garbage collection issues in Lua applications.
- Create robust configuration schemas using Lua.

## Sub-Agent Spawning

This skill supports spawning sub-agents for parallel execution when tasks can be decomposed:

| Trigger Condition | Sub-Agent Type | Purpose |
|---|---|---|
| Multiple Lua scripts to audit | Security Auditor | Parallel security review of each script for vulnerabilities and sandbox escapes |
| Multiple game entities/components | Logic Implementer | Parallel implementation of entity behaviors or state machines |
| Multiple Redis Lua scripts | Script Optimizer | Parallel optimization and validation of Redis scripts |
| Bulk configuration files | Config Validator | Parallel schema validation and type checking of Lua config files |

### Spawning Rules
- Spawn when 3+ independent items need the same operation
- Each sub-agent receives: context, specific target, success criteria
- Results are aggregated and cross-referenced for conflicts
- Maximum concurrent sub-agents: 10

## Workflow

1. **Requirement Analysis**: Determine the target environment (e.g., standalone CLI, embedded in C/C++, Redis, game engine) and specific constraints (e.g., memory limits, execution time limits).
2. **Architecture Design**: 
   - Choose appropriate data structures (arrays vs. hash tables).
   - Decide on the use of metatables for custom behaviors or object-oriented patterns.
   - Plan coroutine usage for asynchronous tasks.
3. **Implementation**:
   - Write clean, modular Lua code using local variables for performance.
   - Implement error handling using `pcall` or `xpcall`.
   - For C API integration, ensure strict stack balance and use `luaL_check*` for validation.
4. **Security & Sandboxing**:
   - If executing untrusted code, set up a secure sandbox by removing dangerous functions (`os`, `io`, `package`) and limiting memory/execution time.
   - Validate all inputs crossing the C/Lua boundary or network.
5. **Testing & Validation**:
   - Use static analysis tools like `luacheck`.
   - Write unit tests using frameworks like `busted`.
6. **Performance Tuning**:
   - Profile code to identify bottlenecks.
   - Optimize table allocations (pre-sizing) and minimize global variable access.
   - Tune garbage collection parameters (`collectgarbage`) if necessary.

## Core Principles

- **Simplicity and Efficiency**: Leverage Lua's lightweight nature. Prefer simple procedural or functional approaches unless complex object-oriented patterns are strictly necessary.
- **Local Over Global**: Always use `local` variables to prevent global namespace pollution and improve access speed.
- **Table Optimization**: Understand the dual nature of Lua tables (array part vs. hash part). Use dense integer keys for arrays and pre-allocate tables when sizes are known.
- **Safe C Integration**: When using the C API, meticulously manage the virtual stack. Every push must have a corresponding pop. Never yield across C boundaries unless using Lua 5.4 yieldable C functions.
- **Secure Execution**: Treat all external Lua scripts as untrusted. Implement strict sandboxing and resource limits.
- **Graceful Error Handling**: Use `pcall`/`xpcall` to catch runtime errors and prevent application crashes.

## Key References

- [Lua 5.4 Reference Manual](https://www.lua.org/manual/5.4/)
- [Programming in Lua (Fourth Edition)](https://www.lua.org/pil/contents.html)
- [Redis Lua Scripting Documentation](https://redis.io/docs/manual/programmability/eval-intro/)
- [Lua C API Guide](https://www.lua.org/manual/5.4/manual.html#4)
- [LuaJIT Performance Tips](http://luajit.org/performance.html)
