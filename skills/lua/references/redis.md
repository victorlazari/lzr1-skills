# Redis Lua Scripting

**Verified against upstream:** 2026-08-07
**Primary Source:** [Redis Programmability - Lua API](https://redis.io/docs/manual/programmability/lua-api/)

## Overview
This reference covers Redis Lua scripting, focusing on performance, security, and constraints.

## Constraints
- Redis Lua scripts are executed atomically. No other Redis commands can run while a script is executing.
- Scripts should be short and fast to avoid blocking the Redis server.
- The maximum execution time for a script is determined by the `lua-time-limit` configuration directive (default 5 seconds).

## Performance
- Use `EVALSHA` instead of `EVAL` to execute scripts by their SHA1 digest, reducing network bandwidth and parsing overhead.
- Avoid using global variables in Lua scripts. Use `local` variables for better performance and to prevent polluting the global environment.

## Security
- Redis Lua scripts run in a sandboxed environment.
- Access to the file system, network, and system commands is disabled.
- Use `redis.call` to execute Redis commands and `redis.pcall` to execute commands and catch errors.
