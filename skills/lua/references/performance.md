# Lua Performance Tuning

**Verified against upstream:** 2026-08-07
**Primary Source:** [Lua Performance Tips](https://www.lua.org/gems/sample.pdf)

## Overview
This reference covers Lua performance tuning, focusing on tables, garbage collection, and general optimization techniques.

## Tables
- Pre-allocate tables if the size is known in advance to avoid reallocation overhead.
- Use array-like tables (integer keys starting from 1) for better performance compared to hash-like tables.
- Avoid creating unnecessary tables in tight loops.

## Garbage Collection
- Lua uses an incremental garbage collector.
- Tune the garbage collector parameters (`collectgarbage("setpause")`, `collectgarbage("setstepmul")`) based on the application's memory usage patterns.
- Minimize the creation of short-lived objects to reduce garbage collection pressure.

## General Optimization
- Use `local` variables instead of global variables for faster access.
- Avoid string concatenation in loops; use `table.concat` instead.
- Profile the Lua code to identify performance bottlenecks before optimizing.
