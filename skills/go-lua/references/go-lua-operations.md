# Go and Lua Operations Guide

**Verified against upstream: 2026-08-07**

## Table of Contents
- [1. Go Performance Profiling with pprof](#1-go-performance-profiling-with-pprof)
- [2. Go Memory Management and Garbage Collection Tuning](#2-go-memory-management-and-garbage-collection-tuning)
- [3. Advanced Redis Lua Patterns](#3-advanced-redis-lua-patterns)
- [4. CGO: Bridging Go with C](#4-cgo-bridging-go-with-c)
- [5. Handling Huge Datasets In-Memory](#5-handling-huge-datasets-in-memory)
- [6. Database Migrations with golang-migrate](#6-database-migrations-with-golang-migrate)
- [7. Security Audit Procedures](#7-security-audit-procedures)

## 1. Go Performance Profiling with pprof

`pprof` is Go’s built-in profiling tool used to analyze CPU, memory, goroutine, mutex, and blocking profiles.

### 1.1 Collecting Profiles

- **CPU Profile:** `curl -o cpu.prof "http://localhost:6060/debug/pprof/profile?seconds=30"`
- **Heap Profile:** `curl -o heap.prof "http://localhost:6060/debug/pprof/heap"`
- **Goroutine Profile:** `curl -o goroutine.prof "http://localhost:6060/debug/pprof/goroutine"`
- **Block Profile:** `curl -o block.prof "http://localhost:6060/debug/pprof/block"`
- **Mutex Profile:** `curl -o mutex.prof "http://localhost:6060/debug/pprof/mutex"`

### 1.2 Analyzing Profiles

Use `go tool pprof <profile_file>` to analyze the collected profiles. Key commands include `top`, `list <regexp>`, and `web`.

**Authoritative Source:** [Profiling Go Programs](https://go.dev/blog/pprof)

## 2. Go Memory Management and Garbage Collection Tuning

Go manages memory with a precise, concurrent garbage collector (GC).

### 2.1 Tuning GOGC and GOMEMLIMIT

- **`GOGC`:** Controls the GC target percentage. Default is 100. Lower values increase GC frequency; higher values delay GC.
- **`GOMEMLIMIT` (Go 1.19+):** Sets a soft memory limit. Crucial for preventing OOM kills in containerized environments. Set to approximately 80-90% of the container's memory limit.

**Authoritative Source:** [A Guide to the Go Garbage Collector](https://go.dev/doc/gc-guide)

## 3. Advanced Redis Lua Patterns

Lua scripts allow atomic execution of complex operations on Redis server-side.

### 3.1 Best Practices

- Keep scripts short and efficient.
- Use `EVALSHA` instead of `EVAL` to save bandwidth and parsing time.
- **Security:** Always use `KEYS` and `ARGV` to pass dynamic data. Never concatenate strings to prevent Lua injection.

### 3.2 Handling the BUSY State

If a Lua script exceeds the `lua-time-limit` (default 5000ms), Redis enters a `BUSY` state.
- **Attempt `SCRIPT KILL`:** `redis-cli SCRIPT KILL` (only works if no write operations have been performed).
- **Worst-Case Scenario:** `redis-cli SHUTDOWN NOSAVE` (results in data loss since the last snapshot).

**Authoritative Source:** [Scripting with Lua | Docs - Redis](https://redis.io/docs/latest/develop/programmability/eval-intro/)

## 4. CGO: Bridging Go with C

CGO allows Go programs to call C code.

### 4.1 Performance Considerations

- Crossing the Go-C boundary has overhead, though significantly reduced in Go 1.21+.
- Batch operations when possible to minimize overhead.
- Manage memory carefully as Go GC does not track C allocations.

**Authoritative Source:** [CGO: Performance and Batching](https://groups.google.com/g/golang-dev/c/XSkrp1_FdiU)

## 5. Handling Huge Datasets In-Memory

- Use memory-mapped files (`syscall.Mmap`) for large datasets.
- Process data in chunks rather than loading fully.
- Use specialized libraries for compressed or succinct data structures.

**Authoritative Source:** [Memory Management in Go: 4 Effective Approaches](https://www.twilio.com/en-us/blog/developers/community/memory-management-go-4-effective-approaches)

## 6. Database Migrations with golang-migrate

### 6.1 Handling the "Dirty" State

When a migration fails, `golang-migrate` marks the database as "dirty".
1. Investigate the cause of the failure.
2. Manually revert the partial changes in the database.
3. Force the version back to the last successful state: `migrate -path ./migrations -database $DB_URL force <previous_version>`.
4. Fix the migration script and redeploy.

## 7. Security Audit Procedures

### 7.1 Dependency Scanning

Use `govulncheck` to analyze the call graph for vulnerable functions.
`go install golang.org/x/vuln/cmd/govulncheck@latest`
`govulncheck ./...`

### 7.2 Preventing Lua Injection

Always use parameterized execution (`KEYS` and `ARGV`) in Redis Lua scripts.

### 7.3 Securing Migration Pipelines

Use dedicated migration roles and temporary credentials. Mask sensitive data in non-production environments.
