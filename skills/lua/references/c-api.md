# Lua C API Integration

**Verified against upstream:** 2026-08-07
**Primary Source:** [Lua 5.4 Reference Manual - The Application Program Interface](https://www.lua.org/manual/5.4/manual.html#4)

## Overview
This reference covers the integration of Lua with C/C++ applications using the Lua C API, focusing on stack management, yielding, and userdata.

## Stack Management
- The Lua C API uses a virtual stack to pass values to and from C.
- Always ensure the stack is balanced after calling Lua functions from C.
- Use `lua_gettop` to check the stack size and `lua_settop` or `lua_pop` to adjust it.

## Yielding
- Lua coroutines can yield execution back to C.
- Use `lua_yield` in C functions called by Lua to yield the coroutine.
- Use `lua_resume` to resume a yielded coroutine.
- Be aware of the limitations of yielding across C boundaries (e.g., cannot yield across a C function that is not a continuation).

## Userdata
- Userdata allows C data structures to be represented in Lua.
- Use `lua_newuserdatauv` to create userdata and associate it with a metatable for object-oriented behavior.
- Ensure proper memory management and garbage collection for userdata.
