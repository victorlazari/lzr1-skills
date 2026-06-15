# Specialist: 42-go-lua

## === FILE: 42-go-lua-advanced.md ===
# Advanced Go and Lua Topics: Performance Profiling, Memory Management, and Handling Huge Datasets

---

## Table of Contents

- [Introduction](#introduction)  
- [1. Go Performance Profiling with pprof](#1-go-performance-profiling-with-pprof)  
  - 1.1 What is pprof?  
  - 1.2 Setting up pprof in Production  
  - 1.3 Types of Profiles and Their Use Cases  
  - 1.4 Analyzing CPU Profiles  
  - 1.5 Heap Profiling and Memory Usage Analysis  
  - 1.6 Blocking, Mutex, and Goroutine Profiling  
  - 1.7 Practical Examples and Tools Integration  
  - 1.8 Troubleshooting and Worst-Case Scenarios  
- [2. Go Memory Management and Garbage Collection Tuning](#2-go-memory-management-and-garbage-collection-tuning)  
  - 2.1 Go’s Memory Model Overview  
  - 2.2 Garbage Collector Internals  
  - 2.3 Tuning GOGC and Its Impacts  
  - 2.4 Diagnosing Memory Leaks and Bloat  
  - 2.5 Advanced Techniques for Reducing GC Pressure  
  - 2.6 Strategies for Managing Large Memory Footprints  
- [3. Advanced Redis Lua Patterns](#3-advanced-redis-lua-patterns)  
  - 3.1 Why Use Lua Scripts in Redis?  
  - 3.2 Script Execution Model and Atomicity  
  - 3.3 Performance Implications and Best Practices  
  - 3.4 Handling Large Datasets in Lua Scripts  
  - 3.5 Common Pitfalls and Debugging Techniques  
  - 3.6 Advanced Patterns: Caching, Rate Limiting, and Distributed Locks  
- [4. CGO: Bridging Go with C for Performance-Critical Operations](#4-cgo-bridging-go-with-c-for-performance-critical-operations)  
  - 4.1 Introduction to CGO and When to Use It  
  - 4.2 CGO Performance Considerations  
  - 4.3 Memory Safety and Management Across Language Boundaries  
  - 4.4 Debugging CGO Issues in Production  
  - 4.5 Best Practices and Common Mistakes  
- [5. Handling Huge Datasets In-Memory](#5-handling-huge-datasets-in-memory)  
  - 5.1 Challenges with Large In-Memory Data  
  - 5.2 Data Structure Selection and Optimization  
  - 5.3 Memory Mapping Files and Zero-Copy Techniques  
  - 5.4 Go and Lua Approaches for Streaming and Chunking Data  
  - 5.5 Using External Tools and Services to Offload Memory Pressure  
- [Conclusion: Integration with Other Specialist Topics](#conclusion-integration-with-other-specialist-topics)  

---

## Introduction

This document is a comprehensive guide aimed at tech support engineers and operations specialists who handle advanced Go and Lua environments in production. It focuses on critical operational topics such as performance profiling with Go’s pprof tool, memory management, garbage collection tuning, advanced Redis Lua scripting patterns, CGO usage, and strategies for managing huge datasets in memory.

The content is crafted with an emphasis on practical, real-world scenarios, worst-case troubleshooting, and production-grade advice. It is designed to deepen your understanding of these advanced topics, enabling you to diagnose, tune, and optimize services built with Go and Lua, particularly when they are under heavy load or memory pressure.

---

# 1. Go Performance Profiling with pprof

## 1.1 What is pprof?

`pprof` is Go’s built-in profiling tool used to analyze CPU, memory, goroutine, mutex, and blocking profiles. It helps identify performance bottlenecks, memory leaks, and synchronization issues by collecting detailed runtime data.

It is essential in production environments to diagnose issues without heavy instrumentation or downtime, as profiles can be collected dynamically.

## 1.2 Setting up pprof in Production

To enable pprof in your Go service, you typically import the `net/http/pprof` package and expose an HTTP endpoint:

```go
import (
    _ "net/http/pprof"
    "net/http"
)

func main() {
    go func() {
        log.Println(http.ListenAndServe("localhost:6060", nil))
    }()
    // Your application code here
}
```

**Important considerations for production:**

- **Restrict Access:** The pprof HTTP endpoints expose sensitive runtime information. Bind to localhost or use firewall rules and authentication proxies.
- **Sampling Overhead:** pprof sampling introduces minimal overhead but running profiles continuously for long periods is not recommended.
- **On-Demand Profiling:** Use tools like `go tool pprof` to fetch profiles on demand or trigger them with signals.

## 1.3 Types of Profiles and Their Use Cases

| Profile Type      | Description                          | Use Case                                      |
|-------------------|------------------------------------|-----------------------------------------------|
| CPU Profile       | Samples CPU usage over time         | Identify CPU hotspots, inefficient code paths |
| Heap Profile      | Tracks live memory allocations      | Detect leaks, excessive memory usage           |
| Goroutine Profile | Snapshot of all goroutines          | Detect goroutine leaks, deadlocks               |
| Block Profile     | Tracks blocking on synchronization  | Diagnose contention and blocking calls          |
| Mutex Profile     | Tracks mutex contention             | Find lock contention hotspots                    |
| Threadcreate      | Tracks thread creation rates        | Debug thread explosion or leaks                  |

## 1.4 Analyzing CPU Profiles

### Collecting CPU Profile

```bash
go tool pprof http://localhost:6060/debug/pprof/profile?seconds=30
```

This command collects a 30-second CPU profile.

### Visualizing

```bash
(pprof) top
(pprof) web
(pprof) list FunctionName
```

- **top**: shows functions with highest CPU usage.
- **web**: generates a graphical call graph in SVG/PDF.
- **list**: shows annotated source code with CPU usage per line.

### Practical Tips

- Look for unexpected functions with high CPU time.
- Identify expensive system calls (e.g., syscalls, DNS lookups).
- Analyze call stacks to understand the context.
- Combine with tracing tools if needed for latency analysis.

## 1.5 Heap Profiling and Memory Usage Analysis

### Taking Heap Profile

```bash
go tool pprof http://localhost:6060/debug/pprof/heap
```

Heap profiles show where memory is allocated and retained.

### Key Commands

- `top`: shows top memory consumers.
- `list`: see code lines responsible for allocations.
- `peek`: dive into specific functions or allocations.

### Diagnosing Memory Leaks

- Compare multiple heap profiles over time.
- Look for increasing retained memory without release.
- Identify large objects or collections that do not shrink.

### Example: Detecting Unreleased Buffers

If buffers or slices grow indefinitely, check for references that prevent GC.

## 1.6 Blocking, Mutex, and Goroutine Profiling

### Block Profiles

```bash
go tool pprof http://localhost:6060/debug/pprof/block
```

Shows where goroutines are blocking, e.g., on channels, locks.

### Mutex Profiles

```bash
go tool pprof http://localhost:6060/debug/pprof/mutex
```

Shows contention on mutexes.

### Goroutine Profiles

```bash
go tool pprof http://localhost:6060/debug/pprof/goroutine?debug=2
```

Shows stack traces of all active goroutines.

### Diagnosing Deadlocks and Contention

- Look for goroutines stuck in channel receive/send.
- Identify "hot" mutexes with high contention.
- Detect goroutine leaks where goroutines never exit.

## 1.7 Practical Examples and Tools Integration

- Integrate pprof with Grafana via Prometheus exporters.
- Use `pprof` with Flamegraphs (`pprof -http=:8081` for interactive web UI).
- Automate periodic profiling and alert on anomalies.
- Combine with logging and tracing for holistic performance monitoring.

## 1.8 Troubleshooting and Worst-Case Scenarios

### Scenario: Sudden CPU Spike

- Capture CPU profile immediately.
- Identify runaway loops or excessive syscalls.
- Check for GC overhead spikes in parallel.

### Scenario: Memory Exhaustion

- Capture heap profiles at intervals.
- Identify leaks or large retained objects.
- Check for inefficient caching or data structure misuse.

### Scenario: Goroutine Explosion

- Use goroutine profile to find leak sources.
- Check channel buffers and blocking operations.
- Review third-party libraries for known issues.

---

# 2. Go Memory Management and Garbage Collection Tuning

## 2.1 Go’s Memory Model Overview

Go manages memory with a precise, concurrent garbage collector (GC) designed for low latency. It divides memory into:

- **Stack:** per-goroutine, dynamically sized.
- **Heap:** shared, dynamically allocated objects.
- **Span:** groups of pages used for allocation.

Understanding how Go allocates and frees memory helps in tuning performance.

## 2.2 Garbage Collector Internals

- Go uses a **concurrent mark-and-sweep** GC.
- GC cycles consist of several phases: mark, sweep, and sweep termination.
- The collector runs concurrently with application code but may introduce stop-the-world pauses.

**Key metrics:**

- **Pause times:** should be low; high pauses indicate GC pressure.
- **GC frequency:** high frequency may indicate excessive allocations.

## 2.3 Tuning GOGC and Its Impacts

The environment variable `GOGC` controls the GC target percentage:

- Default is 100: GC runs when heap size doubles since last GC.
- Lower GOGC values cause more frequent GC cycles (reduce memory usage but higher CPU).
- Higher values delay GC (reduce CPU but increase memory usage).

### Setting GOGC

```bash
GOGC=200 ./myapp
```

Doubles heap size before triggering GC.

### Use Cases

- Low-latency apps might lower GOGC to reduce pauses.
- Memory-constrained environments may raise GOGC to reduce CPU.

## 2.4 Diagnosing Memory Leaks and Bloat

Common causes:

- Holding references to objects unintentionally.
- Using global variables or caches without eviction.
- Goroutine leaks keeping data alive.
- Inefficient data structures with excessive allocations.

**Tools and approaches:**

- Heap profiles over time.
- `runtime.ReadMemStats()` for real-time stats.
- `pprof` for detailed allocation tracing.

## 2.5 Advanced Techniques for Reducing GC Pressure

- **Object pooling**: reuse buffers and objects to reduce allocations.
- **Avoid large objects**: break large structs into smaller pieces.
- **Use stack allocation**: let the compiler allocate short-lived objects on the stack.
- **Minimize boxing**: avoid unnecessary interface conversions.
- **Batch allocations**: allocate slices with capacity upfront.

## 2.6 Strategies for Managing Large Memory Footprints

- Use memory-mapped files (`mmap`) for large datasets.
- Offload rarely accessed data to external stores.
- Serialize and compress in-memory data.
- Monitor and alert on memory usage trends.

---

# 3. Advanced Redis Lua Patterns

## 3.1 Why Use Lua Scripts in Redis?

Lua scripts allow atomic execution of complex operations on Redis server-side, reducing network roundtrips and ensuring data consistency.

## 3.2 Script Execution Model and Atomicity

- Scripts run atomically and block other commands.
- Scripts have a 5-second execution timeout by default.
- Scripts should avoid long-running or blocking operations.

## 3.3 Performance Implications and Best Practices

- Keep scripts short and efficient.
- Avoid heavy computations inside scripts.
- Use `redis.call` vs `redis.pcall` wisely for error handling.
- Cache scripts using `SCRIPT LOAD` and `EVALSHA`.

## 3.4 Handling Large Datasets in Lua Scripts

- Avoid iterating over large keyspaces inside scripts.
- Use Redis commands like `SCAN` outside Lua to paginate.
- Pass only necessary data to scripts.
- Use Redis data structures (hashes, sorted sets) to minimize data transferred.

## 3.5 Common Pitfalls and Debugging Techniques

- Scripts blocking Redis leading to client timeouts.
- Scripts exceeding timeout limits.
- Lua errors causing partial failures.
- Use `redis-cli --eval` and logging to debug scripts.

## 3.6 Advanced Patterns: Caching, Rate Limiting, and Distributed Locks

- **Caching:** Use scripts to atomically check cache and set fallback values.
- **Rate Limiting:** Implement token bucket or leaky bucket algorithms inside Lua.
- **Distributed Locks:** Use `SET key value NX PX` with Lua for safe locking.

---

# 4. CGO: Bridging Go with C for Performance-Critical Operations

## 4.1 Introduction to CGO and When to Use It

CGO allows Go programs to call C code. Use cases:

- Accessing system libraries not available in Go.
- Performance-critical code where C is faster.
- Integration with legacy C code bases.

## 4.2 CGO Performance Considerations

- Crossing the Go-C boundary has overhead.
- Avoid frequent calls; batch operations when possible.
- Manage memory carefully as Go GC does not track C allocations.

## 4.3 Memory Safety and Management Across Language Boundaries

- Use `C.malloc` and `C.free` explicitly.
- Convert between Go pointers and C pointers carefully.
- Avoid passing Go pointers to C that outlive their scope.

## 4.4 Debugging CGO Issues in Production

- Use `GODEBUG=cgocheck=2` to detect invalid pointer passing.
- Use memory sanitizers for C code.
- Profile both Go and C code separately.
- Check for crashes caused by unsafe memory operations.

## 4.5 Best Practices and Common Mistakes

- Minimize CGO usage to isolated modules.
- Document ownership of memory clearly.
- Avoid global state in C code.
- Use Go wrappers to abstract C internals.

---

# 5. Handling Huge Datasets In-Memory

## 5.1 Challenges with Large In-Memory Data

- Memory exhaustion risks.
- GC overhead and latency spikes.
- Data fragmentation and slow access.
- Serialization and persistence complexity.

## 5.2 Data Structure Selection and Optimization

- Use compact data structures (e.g., slices vs maps when possible).
- Use specialized libraries for compressed or succinct data structures.
- Avoid redundant data copies.

## 5.3 Memory Mapping Files and Zero-Copy Techniques

- Use `syscall.Mmap` or third-party libraries to memory map large files.
- Access data directly from disk-backed memory.
- Reduces GC pressure and startup times.

## 5.4 Go and Lua Approaches for Streaming and Chunking Data

- Process data in chunks rather than loading fully.
- Use buffered readers/writers.
- In Lua scripts, paginate large sets with `SCAN` and process incrementally.

## 5.5 Using External Tools and Services to Offload Memory Pressure

- Use Redis or other in-memory databases as external caches.
- Employ distributed caching layers.
- Leverage disk-backed databases for cold data.

---

# Conclusion: Integration with Other Specialist Topics

This advanced guide on Go and Lua performance, memory management, and handling large datasets ties closely with the other six specialist topics in the repository:

- **Topic 1 (Basics of Go and Lua):** Provides foundational knowledge necessary before tackling advanced profiling and memory management.
- **Topic 3 (Distributed Systems):** Understanding Lua patterns and CGO helps optimize Redis-heavy distributed systems.
- **Topic 4 (Containerization and Orchestration):** Memory tuning and profiling are critical when running Go services in containerized environments.
- **Topic 5 (Security and Hardening):** Safe CGO usage and Lua scripts help avoid common vulnerabilities.
- **Topic 6 (Monitoring and Alerting):** Integrating pprof data and memory metrics into observability pipelines.
- **Topic 7 (Incident Response and Troubleshooting):** Techniques here directly assist in diagnosing production issues under stress.

Together, these topics form a holistic knowledge base empowering tech support specialists to maintain, troubleshoot, and optimize modern Go and Lua applications at scale.
## === FILE: 42-go-lua-cli-reference.md ===
# Comprehensive CLI Reference: Go Toolchain, golang-migrate, and Lua Interpreters

## 1. Introduction to Tech Support Operations for Go and Lua

In modern production environments, the ability to rapidly diagnose, debug, and resolve issues is paramount. Tech support operations often require deep knowledge of the underlying toolchains and interpreters used by the applications. This document serves as a comprehensive, highly detailed reference for the Go toolchain (`go build`, `go test`, `go tool pprof`, `go mod`), the `golang-migrate` CLI, and Lua interpreters. It is specifically tailored for production operations, worst-case scenarios, and advanced tech support.

The focus here is not on basic usage, but on the intricate details, undocumented flags, and advanced one-liners that can save a system during a critical outage. Whether you are dealing with memory leaks in a Go microservice, database migration failures, or needing to execute rapid Lua scripts for system diagnostics, this reference provides the necessary operational knowledge.

## 2. Go Toolchain: Advanced Production Operations

The Go toolchain is a powerful suite of utilities that goes far beyond simple compilation. For tech support and operations engineers, mastering these tools is essential for profiling, debugging, and optimizing Go applications in production.

### 2.1 `go build`: Compiling for Production and Debugging

While `go build` is typically used in CI/CD pipelines, operations engineers often need to recompile binaries with specific flags for debugging or to work around production constraints.

**Key Flags for Operations:**

*   `-x`: Prints the commands as they are executed. Crucial for debugging complex build failures in isolated environments.
*   `-gcflags`: Passes flags to the Go compiler.
    *   `-gcflags="all=-N -l"`: Disables optimizations (`-N`) and inlining (`-l`). This is absolutely critical when building a binary that will be attached to a debugger like `delve` in a production environment. Without this, variables may be optimized away, making debugging impossible.
    *   `-gcflags="-m -m"`: Prints optimization decisions, including escape analysis. Useful for diagnosing unexpected memory allocations causing garbage collection pressure.
*   `-ldflags`: Passes flags to the linker.
    *   `-ldflags="-s -w"`: Strips the symbol table (`-s`) and DWARF debugging information (`-w`). Use this to reduce binary size for constrained environments, but **never** use this if you plan to profile or debug the binary later.
    *   `-ldflags="-X main.Version=1.2.3"`: Injects build-time variables. Useful for hot-patching a binary with a specific version string during an emergency release.
*   `-tags`: Specifies build tags. Essential for compiling specific versions of a binary (e.g., enabling a mock database driver for testing in a staging environment).
*   `-race`: Enables the data race detector. While typically used in testing, compiling a canary binary with `-race` and deploying it to a small subset of production traffic can help identify elusive concurrency bugs that only manifest under real-world load. Note: This significantly impacts performance and memory usage.

**Worst-Case Scenario: Emergency Hotfix Compilation**

Imagine a critical bug in production, and the CI/CD pipeline is down. You need to compile a hotfix directly on a jump host and deploy it.

```bash
# Compile for Linux AMD64, injecting the emergency version, disabling optimizations for potential live debugging
GOOS=linux GOARCH=amd64 go build -gcflags="all=-N -l" -ldflags="-X main.Version=EMERGENCY-HOTFIX-01" -o myapp-hotfix ./cmd/myapp
```

### 2.2 `go test`: Beyond Basic Unit Testing

In operations, `go test` is often used to run integration tests against live staging environments or to execute specific benchmarks to validate performance fixes.

**Advanced Operational Usage:**

*   `-run <regexp>`: Runs only tests matching the regular expression. Crucial for isolating a specific failing test without running the entire suite.
*   `-bench <regexp>`: Runs benchmarks. Use this to validate that a performance hotfix actually improves throughput before deploying.
*   `-benchmem`: Prints memory allocation statistics for benchmarks. Essential for identifying memory leaks or excessive allocations.
*   `-cpuprofile <file>`, `-memprofile <file>`, `-mutexprofile <file>`, `-blockprofile <file>`: Generates profiles during test execution. This is often the safest way to profile a specific code path without impacting a live production system.
*   `-count N`: Runs tests multiple times. Useful for identifying flaky tests that only fail intermittently under specific timing conditions.

**Tech Support One-Liner: Isolating a Flaky Integration Test**

```bash
# Run a specific integration test 100 times, failing fast on the first error, to catch a race condition
go test -v -run TestCriticalDatabaseIntegration -count 100 -failfast ./integration
```

### 2.3 `go tool pprof`: The Ultimate Diagnostic Weapon

When a Go application in production is consuming excessive CPU, leaking memory, or deadlocking, `go tool pprof` is the primary diagnostic tool. It analyzes profile data generated by the Go runtime.

**Acquiring Profiles in Production:**

Most production Go applications should expose the `net/http/pprof` endpoints.

*   **CPU Profile:** `curl -o cpu.prof "http://localhost:6060/debug/pprof/profile?seconds=30"`
*   **Heap Profile:** `curl -o heap.prof "http://localhost:6060/debug/pprof/heap"`
*   **Goroutine Profile:** `curl -o goroutine.prof "http://localhost:6060/debug/pprof/goroutine"`
*   **Block Profile:** `curl -o block.prof "http://localhost:6060/debug/pprof/block"`
*   **Mutex Profile:** `curl -o mutex.prof "http://localhost:6060/debug/pprof/mutex"`

**Analyzing Profiles with `go tool pprof`:**

Once you have the profile, you analyze it interactively or generate reports.

```bash
go tool pprof cpu.prof
```

**Key Interactive Commands:**

*   `top`: Shows the top functions consuming resources.
*   `top -cum`: Shows the top functions, including the resources consumed by functions they call (cumulative). This is often more useful than flat `top` for finding the root cause.
*   `list <regexp>`: Shows the annotated source code for functions matching the regular expression, highlighting the exact lines consuming resources.
*   `web`: Generates an SVG graph and opens it in a web browser. This is the most intuitive way to understand complex call graphs.
*   `traces`: Shows the execution traces that led to the profiled events.

**Worst-Case Scenario: Diagnosing a Memory Leak**

The application is OOM-killing every few hours.

1.  Capture a heap profile immediately after startup: `curl -o heap_base.prof ...`
2.  Capture another heap profile right before the expected OOM: `curl -o heap_current.prof ...`
3.  Compare the profiles to see what grew:
    ```bash
    go tool pprof -base heap_base.prof heap_current.prof
    ```
4.  Inside pprof, use `top` and `list` to identify the objects being allocated and not garbage collected.

**Tech Support One-Liner: Generating a Flame Graph**

Flame graphs are excellent for visualizing CPU usage.

```bash
# Requires graphviz to be installed
go tool pprof -http=:8080 cpu.prof
# Navigate to http://localhost:8080/ui/flamegraph
```

### 2.4 `go mod`: Dependency Management in Crisis

Dependency issues can halt deployments and cause unpredictable behavior. Operations engineers must know how to manipulate `go.mod` and `go.sum` effectively.

**Critical Commands:**

*   `go mod tidy`: Adds missing and removes unused modules. Always run this after manually editing `go.mod`.
*   `go mod vendor`: Creates a `vendor` directory containing all dependencies. This is crucial for air-gapped environments or when upstream repositories are unavailable (e.g., GitHub is down).
*   `go mod verify`: Verifies that the dependencies in the module cache match the cryptographic hashes in `go.sum`. Use this if you suspect a dependency has been tampered with or corrupted.
*   `go mod graph`: Prints the module requirement graph. Useful for understanding complex transitive dependencies.
*   `go mod why -m <module>`: Explains why a specific module is in the dependency graph. Essential for tracking down unwanted or vulnerable transitive dependencies.

**Worst-Case Scenario: Upstream Dependency Disappears**

A critical deployment is failing because an upstream dependency repository was deleted.

1.  If you have a previous successful build, extract the dependency from the Go module cache (`$GOPATH/pkg/mod`) on the build server.
2.  Copy it to a local directory.
3.  Use the `replace` directive in `go.mod` to point to the local copy:
    ```go
    replace github.com/deleted/repo => ../local-copy-of-repo
    ```
4.  Run `go mod vendor` to ensure it's packaged with the application.

## 3. `golang-migrate` CLI: Database Operations and Recovery

Database migrations are often the most fragile part of a deployment. The `golang-migrate` CLI is a standard tool for managing these migrations. Operations engineers must be prepared to handle failed migrations, dirty database states, and rollbacks.

### 3.1 Core Migration Operations

*   `migrate -path ./migrations -database "$DB_URL" up`: Applies all pending up migrations.
*   `migrate -path ./migrations -database "$DB_URL" down`: Reverts all migrations. **Use with extreme caution in production.**
*   `migrate -path ./migrations -database "$DB_URL" up N`: Applies the next `N` up migrations.
*   `migrate -path ./migrations -database "$DB_URL" down N`: Reverts the last `N` down migrations. This is the standard way to rollback a specific failed deployment.

### 3.2 Handling the "Dirty" State

When a migration fails midway (e.g., due to a syntax error or a timeout), `golang-migrate` marks the database as "dirty". It will refuse to run further migrations until the state is resolved. This is the most common tech support scenario for migrations.

**The Recovery Process:**

1.  **Identify the Failure:** Check the application logs or the migration output to determine exactly which migration failed and why.
2.  **Manual Cleanup:** Connect to the database manually and revert any partial changes made by the failed migration. If the migration was creating a table, drop it. If it was adding a column, remove it. **This step requires deep SQL knowledge and extreme care.**
3.  **Force the Version:** Once the database schema is manually restored to the state *before* the failed migration, use the `force` command to tell `golang-migrate` the correct current version.
    ```bash
    # If migration 004 failed, force the version back to 003
    migrate -path ./migrations -database "$DB_URL" force 3
    ```
4.  **Fix and Retry:** Fix the SQL in the failed migration file, and then run `migrate up` again.

### 3.3 Advanced `golang-migrate` Techniques

*   **Creating Migrations:** `migrate create -ext sql -dir ./migrations -seq add_users_table`. Always use sequential naming (`-seq`) to avoid conflicts.
*   **Using TLS:** For production databases, always use TLS. The connection string must include the appropriate parameters (e.g., `sslmode=verify-full`).
*   **Timeouts:** Migrations on large tables can take a long time. Use the `statement-timeout` parameter in the connection string (if supported by the driver) to prevent migrations from hanging indefinitely and locking tables.

**Tech Support One-Liner: Checking Migration Status**

```bash
# Quickly check the current migration version and dirty state
migrate -path ./migrations -database "$DB_URL" version
```

## 4. Lua Interpreters: Advanced One-Liners for Operations

Lua is a lightweight, embeddable scripting language frequently used in infrastructure tools (like Redis, Nginx/OpenResty, and HAProxy) and for rapid system scripting. Operations engineers can leverage Lua one-liners for quick data manipulation, system checks, and interacting with these embedded environments.

### 4.1 Standard Lua Interpreter (`lua`)

The standard `lua` executable is excellent for quick text processing and system interactions when tools like `awk` or `sed` are insufficient or too complex.

**Advanced One-Liners:**

*   **Parsing JSON (requires `lua-cjson`):**
    ```bash
    cat data.json | lua -l cjson -e 'local d = cjson.decode(io.read("*a")); for k,v in pairs(d) do print(k,v) end'
    ```
*   **Calculating MD5 Hashes of Files in a Directory:**
    ```bash
    ls *.txt | lua -e 'for f in io.lines() do local h = io.popen("md5sum " .. f):read("*a"); print(h) end'
    ```
*   **Generating Random Passwords:**
    ```bash
    lua -e 'math.randomseed(os.time()); local chars="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()"; local pw=""; for i=1,16 do local r=math.random(1,#chars); pw=pw..chars:sub(r,r) end; print(pw)'
    ```
*   **Monitoring System Load (Linux):**
    ```bash
    lua -e 'while true do local f=io.open("/proc/loadavg","r"); print(f:read("*a")); f:close(); os.execute("sleep 1") end'
    ```

### 4.2 LuaJIT: High-Performance Scripting

LuaJIT is a Just-In-Time compiler for Lua, offering significantly higher performance. It is the engine behind OpenResty. It includes the FFI (Foreign Function Interface) library, allowing Lua to call C functions directly without writing C bindings.

**Advanced FFI One-Liners (Linux):**

*   **Calling `gettimeofday` directly via C for microsecond precision:**
    ```bash
    luajit -e 'local ffi = require("ffi"); ffi.cdef[[struct timeval { long tv_sec; long tv_usec; }; int gettimeofday(struct timeval *tv, void *tz);]]; local tv = ffi.new("struct timeval"); ffi.C.gettimeofday(tv, nil); print(tv.tv_sec .. "." .. string.format("%06d", tv.tv_usec))'
    ```
*   **Reading a file directly using C `open`/`read` (bypassing Lua's IO for specific low-level needs):**
    ```bash
    luajit -e 'local ffi = require("ffi"); ffi.cdef[[int open(const char *pathname, int flags); int read(int fd, void *buf, size_t count); int close(int fd);]]; local fd = ffi.C.open("/etc/hostname", 0); local buf = ffi.new("char[256]"); local n = ffi.C.read(fd, buf, 256); print(ffi.string(buf, n)); ffi.C.close(fd)'
    ```

### 4.3 Redis Lua Scripting (`EVAL`)

Redis uses Lua for atomic server-side scripting. This is crucial for complex operations that must be executed without race conditions.

**Tech Support Scenarios in Redis:**

*   **Atomic Rate Limiting (Token Bucket):**
    ```lua
    -- KEYS[1]: rate limit key, ARGV[1]: capacity, ARGV[2]: refill rate, ARGV[3]: current time
    local key = KEYS[1]
    local capacity = tonumber(ARGV[1])
    local refill_rate = tonumber(ARGV[2])
    local now = tonumber(ARGV[3])

    local last_tokens = tonumber(redis.call('hget', key, 'tokens') or capacity)
    local last_refreshed = tonumber(redis.call('hget', key, 'last_refreshed') or now)

    local delta = math.max(0, now - last_refreshed)
    local tokens = math.min(capacity, last_tokens + (delta * refill_rate))

    if tokens >= 1 then
        tokens = tokens - 1
        redis.call('hset', key, 'tokens', tokens)
        redis.call('hset', key, 'last_refreshed', now)
        return 1 -- Allowed
    else
        return 0 -- Rate limited
    end
    ```
    *Execution:* `redis-cli --eval ratelimit.lua mykey , 10 1 1678886400`

*   **Bulk Deletion by Pattern (Safer than `KEYS` in production):**
    Using `SCAN` inside a Lua script to delete keys matching a pattern without blocking the Redis server for a long time.
    ```lua
    local cursor = "0"
    local pattern = ARGV[1]
    local count = 0
    repeat
        local result = redis.call('SCAN', cursor, 'MATCH', pattern, 'COUNT', 1000)
        cursor = result[1]
        local keys = result[2]
        if #keys > 0 then
            redis.call('DEL', unpack(keys))
            count = count + #keys
        end
    until cursor == "0"
    return count
    ```
    *Execution:* `redis-cli --eval bulk_delete.lua , "session:*"`

## 5. Worst-Case Scenarios and Tech Support Operations

This section outlines comprehensive strategies for handling severe production incidents involving the technologies discussed.

### 5.1 Scenario: The "Zombie" Go Process

**Symptoms:** A Go application is running, consuming 100% CPU on multiple cores, but is completely unresponsive to network requests. It cannot be gracefully shut down.

**Diagnosis and Resolution:**

1.  **Attempt pprof:** Try to grab a CPU profile or goroutine dump via `net/http/pprof`. If the process is completely deadlocked, this might time out.
2.  **Send SIGQUIT:** If pprof fails, send a `SIGQUIT` signal to the process.
    ```bash
    kill -QUIT <pid>
    ```
    Unlike `SIGKILL` or `SIGTERM`, `SIGQUIT` forces the Go runtime to dump the stack traces of *all* currently running goroutines to standard error before exiting.
3.  **Analyze the Dump:** Redirect the standard error to a file and analyze the stack traces. Look for goroutines stuck in `runtime.gopark` (waiting on channels or mutexes) or in infinite loops. This is the definitive way to identify deadlocks.
4.  **Restart:** Once the dump is captured, the process will have exited. Restart the service.

### 5.2 Scenario: Corrupted Database Migrations During a Major Outage

**Symptoms:** A deployment failed, the database is in a dirty state, and the application is down. The original migration author is unavailable.

**Diagnosis and Resolution:**

1.  **Stop the Bleeding:** Ensure no automated systems are trying to retry the deployment or run migrations.
2.  **Assess the Damage:** Use `migrate version` to confirm the dirty state. Connect to the database and inspect the schema. Compare it to the expected schema of the failed migration.
3.  **Manual Intervention:** This is the critical step. You must manually execute SQL commands to revert the partial changes.
    *   *Example:* If the migration was `ALTER TABLE users ADD COLUMN phone VARCHAR(20); CREATE INDEX idx_phone ON users(phone);` and it failed on the index creation, you must manually run `ALTER TABLE users DROP COLUMN phone;`.
4.  **Force State:** Run `migrate force <previous_version>`.
5.  **Verify:** Run the application locally or in a staging environment against a snapshot of the production database to ensure the rollback was successful.
6.  **Deploy Previous Version:** Deploy the last known good version of the application.

### 5.3 Scenario: Redis Overload due to Bad Lua Script

**Symptoms:** Redis CPU is at 100%, and all commands are timing out. The `SLOWLOG` indicates a specific `EVAL` command is taking seconds to execute.

**Diagnosis and Resolution:**

1.  **Identify the Script:** Use `redis-cli SLOWLOG GET 10` to identify the problematic Lua script.
2.  **Kill the Script:** Redis is single-threaded. A long-running Lua script blocks everything. You cannot use normal commands. You must use `SCRIPT KILL`.
    ```bash
    redis-cli SCRIPT KILL
    ```
    *Note:* `SCRIPT KILL` only works if the script has not yet performed any write operations. If it has written data, Redis will refuse to kill it to maintain data consistency.
3.  **The Nuclear Option:** If `SCRIPT KILL` fails because writes have occurred, the only way to recover the Redis server is to shut it down forcefully.
    ```bash
    redis-cli SHUTDOWN NOSAVE
    ```
    **Warning:** This will result in data loss for any data not yet persisted to disk. This is a true worst-case scenario action.
4.  **Fix the Script:** Analyze the script. Common issues include infinite loops, iterating over massive datasets without yielding, or using inefficient algorithms. Rewrite the script to be O(1) or O(N) with a small N.

## 6. Relation to Other Specialist Files

This document (`42-go-lua-cli-reference.md`) serves as the deep-dive technical reference for specific execution environments (Go and Lua) and database state management (`golang-migrate`). It is a critical component of the broader specialist-teams repository.

*   **Relation to Incident Response (e.g., `01-incident-response-playbook.md`):** When the incident response playbook dictates that a deep technical investigation is required for a Go service or a database migration failure, the responder will consult this CLI reference for the exact commands and diagnostic techniques.
*   **Relation to Infrastructure as Code (e.g., `15-terraform-kubernetes-ops.md`):** While Terraform and Kubernetes manage the deployment of the applications, this document covers the internal operations of the applications themselves. If a Kubernetes pod running a Go application is crash-looping, this reference provides the tools (`go build -gcflags`, `pprof`) to figure out *why*.
*   **Relation to Monitoring and Observability (e.g., `22-prometheus-grafana-alerts.md`):** Observability tools will trigger alerts (e.g., "High Memory Usage"). This CLI reference provides the next step: how to use `go tool pprof` to capture a heap profile and identify the exact line of code causing the memory leak detected by Prometheus.
*   **Relation to Security Operations (e.g., `30-security-auditing-tools.md`):** The `go mod` commands detailed here are essential for security audits, specifically for verifying dependency integrity (`go mod verify`) and tracking down vulnerable transitive dependencies (`go mod why`).
*   **Relation to Database Administration (e.g., `18-postgresql-dba-guide.md`):** The `golang-migrate` section directly complements general DBA guides. While the DBA guide covers performance tuning and backups, this document covers the specific lifecycle of schema changes and how to recover when those changes fail during application deployments.
*   **Relation to General Scripting (e.g., `05-bash-python-automation.md`):** The Lua section provides an alternative to Bash and Python for specific high-performance or embedded scripting scenarios, particularly when interacting with systems like Redis or OpenResty where Lua is the native scripting language.

This comprehensive reference ensures that when operations engineers face complex, low-level issues in Go or Lua environments, they have the exact commands, flags, and strategies needed to diagnose and resolve the problem efficiently.

## === FILE: 42-go-lua-config-schemas.md ===
# Specialist Guide: Go Runtime, Golang-Migrate, and Redis Lua Configuration Schemas

## 1. Introduction and Scope

This document serves as the definitive tech support and operations guide for configuring, tuning, and troubleshooting the Go runtime environment, database migration pipelines using `golang-migrate`, and Redis Lua scripting limits. Designed for Site Reliability Engineers (SREs), DevOps professionals, and Tier 3 Tech Support, this guide dives deep into production-grade configurations, worst-case scenarios, and practical recovery strategies.

As part of the broader specialist-teams repository, this guide intersects with database connection pooling, memory management, and distributed caching strategies. It provides the necessary schemas and tuning recommendations to ensure high availability, optimal performance, and resilience under extreme load.

## 2. Go Runtime Tuning: GOGC and GOMAXPROCS

The Go runtime is highly optimized out of the box, but at scale, default settings often lead to suboptimal performance, excessive memory consumption, or CPU throttling. The two most critical environment variables for tuning the Go runtime are `GOGC` and `GOMAXPROCS`.

### 2.1. GOGC: Garbage Collection Tuning

The `GOGC` variable controls the aggressiveness of the Go garbage collector (GC). It sets the target percentage of heap growth before the next GC cycle is triggered. The default value is `100`, meaning the GC runs when the heap size doubles.

#### 2.1.1. Configuration Schema and Recommendations

| Setting | Value | Use Case | Pros | Cons |
|---------|-------|----------|------|------|
| Default | `100` | General purpose applications. | Balanced CPU and memory usage. | May cause latency spikes in high-throughput systems. |
| Aggressive | `50` | Memory-constrained environments (e.g., small containers). | Keeps memory footprint low. | High CPU overhead due to frequent GC cycles. |
| Relaxed | `200` - `1000` | High-throughput, latency-sensitive APIs with ample memory. | Reduces GC frequency, lowering CPU usage and latency. | Higher memory consumption; risk of OOM kills if unbounded. |
| Disabled | `off` | Short-lived batch jobs or highly specialized systems with manual memory management. | Zero GC overhead. | Guaranteed OOM if memory is not managed manually. |

#### 2.1.2. Production Operations and Worst-Case Scenarios

**Scenario: CPU Starvation due to GC Thrashing**
In high-throughput microservices, a default `GOGC=100` can lead to the GC running continuously, consuming up to 25% of available CPU resources. This is known as GC thrashing.
*   **Symptoms:** High CPU utilization, increased p99 latency, and frequent GC pauses visible in profiling tools (`pprof`).
*   **Resolution:** Increase `GOGC` to `200` or `400` to reduce GC frequency. Ensure the container has sufficient memory limits to accommodate the larger heap. Alternatively, implement the `GOMEMLIMIT` variable (introduced in Go 1.19) to set a soft memory limit, allowing you to safely increase `GOGC` without risking OOM kills.

**Scenario: OOM Kills in Kubernetes**
A service with `GOGC=200` experiences sudden spikes in traffic, causing the heap to grow rapidly. The container exceeds its Kubernetes memory limit and is OOMKilled before the GC can reclaim memory.
*   **Symptoms:** Pod restarts with `OOMKilled` status.
*   **Resolution:** Set `GOMEMLIMIT` to approximately 80-90% of the container's memory limit. This forces the GC to run aggressively as the memory approaches the limit, preventing the OOM kill while maintaining the benefits of a higher `GOGC` during normal operation.

### 2.2. GOMAXPROCS: Concurrency and CPU Allocation

The `GOMAXPROCS` variable determines the maximum number of operating system threads that can execute user-level Go code simultaneously. By default, it is set to the number of logical CPUs available to the process.

#### 2.2.1. Configuration Schema and Recommendations

| Environment | Recommended Setting | Rationale |
|-------------|---------------------|-----------|
| Bare Metal / VM | Default (Number of logical CPUs) | Maximizes hardware utilization. |
| Kubernetes / Docker (CPU Limits) | Use `automaxprocs` library or set manually to the CPU quota. | Prevents CPU throttling. The Go runtime is unaware of cgroup limits by default and may spawn too many threads, leading to severe context switching and throttling. |
| I/O Bound Services | Default or slightly higher | Go's scheduler handles I/O efficiently, but in extreme cases, increasing threads can help if many goroutines are blocked on CGO or syscalls. |

#### 2.2.2. Production Operations and Worst-Case Scenarios

**Scenario: Severe CPU Throttling in Kubernetes**
A Go application deployed in Kubernetes with a CPU limit of `2.0` (2 cores) is running on a node with 64 cores. By default, `GOMAXPROCS` is set to 64. The application spawns 64 threads, rapidly consuming its CPU quota and getting heavily throttled by the Linux CFS (Completely Fair Scheduler).
*   **Symptoms:** Extremely high latency, poor throughput, and high CPU throttling metrics in Prometheus (`container_cpu_cfs_throttled_seconds_total`).
*   **Resolution:** Integrate the `go.uber.org/automaxprocs` package, which automatically reads the cgroup CPU limits and sets `GOMAXPROCS` accordingly (in this case, to 2). This aligns the Go scheduler with the actual available resources, eliminating unnecessary context switching and throttling.

## 3. Golang-Migrate Configurations

`golang-migrate` is a popular tool for managing database schema migrations in Go applications. While powerful, improper configuration can lead to locked databases, failed deployments, and data corruption.

### 3.1. Configuration Schema and Best Practices

When configuring `golang-migrate`, several parameters are critical for production stability:

*   **`x-migrations-table`**: Customizes the name of the migrations tracking table. Useful for multi-tenant databases.
*   **`statement-timeout`**: Sets a timeout for individual migration statements. Crucial for preventing long-running migrations from locking tables indefinitely.
*   **`lock-timeout`**: Defines how long the tool should wait to acquire the migration lock.

#### 3.1.1. Connection String Examples

**PostgreSQL:**
```text
postgres://user:password@host:5432/dbname?sslmode=verify-full&x-migrations-table=schema_migrations&statement_timeout=60000
```

**MySQL:**
```text
mysql://user:password@tcp(host:3306)/dbname?multiStatements=true&x-migrations-table=schema_migrations&readTimeout=1m
```

### 3.2. Production Operations and Worst-Case Scenarios

**Scenario: The "Dirty" Database State**
A migration fails halfway through execution due to a syntax error or a timeout. `golang-migrate` marks the database as "dirty," preventing any further migrations or application startups.
*   **Symptoms:** Application fails to start, logging errors like `Dirty database version X. Fix and force version.`.
*   **Resolution:**
    1.  Investigate the cause of the failure (e.g., check database logs for timeouts or syntax errors).
    2.  Manually revert the partial changes made by the failed migration in the database.
    3.  Use the `golang-migrate` CLI to force the version back to the last successful state: `migrate -path ./migrations -database $DB_URL force <previous_version>`.
    4.  Fix the migration script and redeploy.

**Scenario: Distributed Lock Contention**
In a Kubernetes environment, multiple pods of a new application version start simultaneously and attempt to run migrations. One pod acquires the lock, but crashes before releasing it. Other pods are stuck waiting for the lock.
*   **Symptoms:** Pods are stuck in `CrashLoopBackOff` or readiness probes fail because migrations cannot proceed. Database shows an active lock in the `schema_migrations` table.
*   **Resolution:**
    1.  Identify and terminate the crashed pod or process holding the lock.
    2.  Manually clear the lock in the database. For PostgreSQL, this involves updating the `schema_migrations` table to set `is_locked = false`.
    3.  To prevent this, decouple migrations from application startup. Run migrations as a Kubernetes `Job` or an init container that executes before the main application pods are rolled out.

## 4. Redis Lua Script Limits and Tuning

Redis supports executing Lua scripts server-side, providing atomicity and reducing network round trips. However, because Redis is single-threaded, a poorly written or long-running Lua script can block the entire server, causing widespread outages.

### 4.1. Configuration Schema and Limits

Redis imposes several limits and configurations to manage Lua script execution:

*   **`lua-time-limit`**: The maximum execution time for a Lua script in milliseconds. The default is `5000` (5 seconds). If a script exceeds this limit, Redis starts logging warnings and accepting `SCRIPT KILL` commands.
*   **Memory Limits**: Lua scripts consume memory. Redis tracks this, and excessive memory usage within a script can lead to OOM errors.
*   **Deterministic Execution**: Prior to Redis 5.0, scripts had to be purely deterministic (e.g., no random numbers or time-based logic) to ensure safe replication. Redis 5.0 introduced script effects replication, relaxing this constraint.

### 4.2. Production Operations and Worst-Case Scenarios

**Scenario: The Blocking Script Outage**
A developer deploys a Lua script that iterates over a massive Redis set (e.g., millions of elements) using `SMEMBERS` instead of `SSCAN`. The script takes 15 seconds to execute. Because Redis is single-threaded, all other commands from all other clients are blocked for 15 seconds.
*   **Symptoms:** Massive spike in application latency, connection timeouts, and Redis slowlog entries showing the Lua script execution.
*   **Resolution:**
    1.  **Immediate Mitigation:** Connect to Redis via `redis-cli` and execute the `SCRIPT KILL` command. This terminates the running script (provided it hasn't performed any write operations yet). If the script has performed writes, `SCRIPT KILL` will fail, and the only option is to restart the Redis server (`SHUTDOWN NOSAVE`), which may result in data loss.
    2.  **Long-Term Fix:** Rewrite the Lua script to use iterative commands like `SSCAN`, `HSCAN`, or `ZSCAN`. Break large operations into smaller, paginated chunks that yield control back to the Redis event loop.

**Scenario: Script Cache Exhaustion**
An application dynamically generates Lua scripts with hardcoded values instead of using `KEYS` and `ARGV` arrays. Every execution results in a unique script being loaded into the Redis script cache via `EVAL`.
*   **Symptoms:** Redis memory usage grows unbounded until it hits the `maxmemory` limit, triggering evictions or OOM errors.
*   **Resolution:**
    1.  **Immediate Mitigation:** Execute the `SCRIPT FLUSH` command to clear the script cache and free up memory.
    2.  **Long-Term Fix:** Refactor the application code to use parameterized Lua scripts. Load the script once using `SCRIPT LOAD` and execute it using `EVALSHA`, passing dynamic values via the `KEYS` and `ARGV` arrays. This ensures only one copy of the script resides in the cache.

## 5. Integration with the Specialist Teams Ecosystem

This configuration schema guide is a critical component of the specialist-teams repository. It directly interacts with and supports the other operational domains:

1.  **Database Connection Pooling:** The `golang-migrate` configurations discussed here must align with the connection pooling settings to ensure migration scripts do not exhaust available connections or conflict with application traffic.
2.  **Distributed Caching:** The Redis Lua script limits are essential for maintaining the stability of the distributed caching layer. Blocking scripts directly impact cache retrieval latencies.
3.  **Incident Response:** The worst-case scenarios and recovery strategies outlined for Go runtime OOMs, dirty migrations, and blocked Redis instances form the basis of Tier 3 incident response playbooks.
4.  **Capacity Planning:** Understanding `GOGC` and `GOMAXPROCS` is fundamental for accurate capacity planning and Kubernetes resource allocation (requests and limits).
5.  **Security Operations:** Proper configuration of migration timeouts and Redis script limits prevents denial-of-service (DoS) vectors caused by resource exhaustion.
6.  **Observability:** The symptoms described in the worst-case scenarios dictate the metrics and alerts that must be configured in Prometheus and Grafana (e.g., GC pause times, CPU throttling, Redis slowlog length).

## 6. Conclusion

Mastering the configuration schemas for the Go runtime, `golang-migrate`, and Redis Lua scripting is non-negotiable for operating high-scale, resilient systems. By applying the tuning recommendations and understanding the worst-case scenarios detailed in this guide, operations teams can proactively prevent outages, optimize resource utilization, and respond effectively when complex failures occur. Continuous monitoring, profiling, and load testing are required to validate these configurations as application workloads evolve.

## === FILE: 42-go-lua-deep-dive.md ===
# Deep Dive into Go and Lua Internals: A Tech Support Specialist Guide

## 1. Introduction to Systems-Level Troubleshooting

In the realm of high-performance backend systems and embedded scripting, Go and Lua represent two fundamentally different but equally critical paradigms. Go provides a robust, statically typed, concurrent environment designed for scalable network services, while Lua offers a lightweight, embeddable, dynamically typed scripting engine. When these technologies intersect—or when they operate independently at massive scale—tech support operations and site reliability engineers (SREs) must possess a profound understanding of their internal mechanics. 

This document serves as a comprehensive, 2000+ word deep dive into the internals of Go and Lua. It is specifically tailored for production operations, focusing on worst-case scenarios, catastrophic failures, and advanced debugging techniques. We will explore the Go scheduler, channel implementation, map internals, the Lua virtual machine stack, Lua table mechanics, and the treacherous waters of Go-to-C interoperability (cgo).

## 2. Go Scheduler Internals: The M:N Model

The Go runtime does not rely on the operating system to schedule goroutines. Instead, it implements its own M:N scheduler, multiplexing `M` goroutines onto `N` OS threads. Understanding the triad of the Go scheduler—G, M, and P—is paramount for diagnosing CPU starvation, latency spikes, and deadlocks.

### 2.1 The G, M, and P Entities

*   **G (Goroutine):** Represents a single goroutine. It contains the stack, instruction pointer, and scheduling information (e.g., channel block status).
*   **M (Machine):** Represents an OS thread. It executes the Go code or native C code. An M must hold a P to execute Go code.
*   **P (Processor):** Represents a logical processor, bounded by `GOMAXPROCS`. It holds a local queue of runnable goroutines.

### 2.2 Work Stealing and Sysmon

When a P's local queue is empty, it attempts to "steal" half of the runnable goroutines from another P's queue. This work-stealing algorithm ensures load balancing across CPU cores. Additionally, a background thread called `sysmon` monitors the system. If it detects a goroutine running for more than 10ms without yielding, it attempts to preempt it. `sysmon` also reclaims P's from M's that are blocked in long-running system calls.

### 2.3 Worst-Case Scenarios and Tech Support Operations

**Scenario A: Goroutine Leaks**
A goroutine leak occurs when goroutines are blocked indefinitely, usually on a channel read/write or a network I/O operation that lacks a timeout. Over time, these leaked goroutines consume memory (minimum 2KB per goroutine stack), eventually leading to an Out-Of-Memory (OOM) crash.
*   **Diagnosis:** Use `runtime/pprof` to capture a goroutine profile. Look for thousands of goroutines stuck in `runtime.gopark` or `runtime.chanrecv`.
*   **Resolution:** Enforce context timeouts (`context.WithTimeout`) on all blocking operations.

**Scenario B: Preemption Failures (Pre-Go 1.14)**
Before Go 1.14, tight loops without function calls could not be preempted, causing CPU starvation and preventing garbage collection (GC) from starting (as GC requires all P's to reach a safe point).
*   **Diagnosis:** High CPU usage on specific cores, while other goroutines stall. `sysmon` logs may indicate preemption failures.
*   **Resolution:** Upgrade to Go 1.14+ (which introduced asynchronous preemption via signals), or manually insert `runtime.Gosched()` in tight loops.

## 3. Go Channel Implementation: Synchronization Primitives

Channels are the bedrock of Go's concurrency model, adhering to the philosophy: "Do not communicate by sharing memory; instead, share memory by communicating." Under the hood, a channel is a complex data structure (`hchan`) protected by a mutex.

### 3.1 The `hchan` Struct

The `hchan` struct contains:
*   `qcount`: Number of items in the queue.
*   `dataqsiz`: Size of the circular queue (for buffered channels).
*   `buf`: Pointer to the circular queue array.
*   `sendq` and `recvq`: Linked lists of waiting goroutines (G's).
*   `lock`: A mutex protecting all fields in `hchan`.

### 3.2 Send and Receive Mechanics

When a goroutine sends data to a channel:
1.  It acquires the `lock`.
2.  If a receiver is waiting in `recvq`, it copies the data directly to the receiver's stack and wakes it up.
3.  If the buffer has space, it copies the data to `buf`.
4.  If the buffer is full (or unbuffered), the goroutine is parked, added to `sendq`, and the lock is released.

### 3.3 Worst-Case Scenarios and Tech Support Operations

**Scenario A: Deadlocks**
A deadlock occurs when all goroutines are asleep, waiting on channels. The Go runtime detects this and panics with `fatal error: all goroutines are asleep - deadlock!`.
*   **Diagnosis:** Analyze the panic stack trace. Identify the circular dependency or the missing sender/receiver.
*   **Resolution:** Ensure every channel send has a corresponding receive path. Use `select` statements with `default` cases for non-blocking operations.

**Scenario B: Panic on Closed Channel**
Sending to a closed channel or closing an already closed channel triggers a panic.
*   **Diagnosis:** Stack trace points to `runtime.chansend` or `runtime.closechan`.
*   **Resolution:** Implement the "sender closes" principle. If multiple senders exist, use a synchronization mechanism (like `sync.WaitGroup` or a separate signal channel) to coordinate closure.

## 4. Go Map Internals: Hash Tables and Memory Management

Go's `map` is an implementation of a hash table. It is optimized for fast lookups but has specific memory characteristics that can cause severe issues in long-running applications.

### 4.1 The `hmap` and Buckets

A map is represented by the `hmap` struct, which points to an array of buckets (`bmap`). Each bucket holds up to 8 key-value pairs. When a bucket overflows due to hash collisions, Go allocates an overflow bucket and links it to the original bucket.

### 4.2 Rehashing and Evacuation

When the load factor (average items per bucket) exceeds 6.5, or when there are too many overflow buckets, the map grows. Go allocates a new array of buckets twice the size of the old one and incrementally "evacuates" data from the old buckets to the new ones during subsequent map operations.

### 4.3 Worst-Case Scenarios and Tech Support Operations

**Scenario A: Concurrent Map Writes**
Maps are not safe for concurrent use. If two goroutines access a map concurrently and at least one is writing, the runtime will detect the race and crash the program with `fatal error: concurrent map writes`.
*   **Diagnosis:** The crash is immediate and unrecoverable. The stack trace will clearly indicate the offending map access.
*   **Resolution:** Use `sync.RWMutex` to protect the map, or switch to `sync.Map` for specific use cases (e.g., append-only caches).

**Scenario B: Map Memory Leaks**
Deleting keys from a Go map does *not* shrink the underlying memory allocation. The buckets remain allocated, leading to memory bloat if a map grows large and is subsequently emptied.
*   **Diagnosis:** High memory usage despite a low number of active items in the map. Heap profiles will show large allocations in `runtime.makemap` or `runtime.mapassign`.
*   **Resolution:** Periodically create a new map and copy the active keys over, allowing the garbage collector to reclaim the old map's memory.

## 5. Lua Stack Internals: The Virtual Machine Heart

Lua is a register-based virtual machine, but it interacts with C via a strict stack-based API. Understanding this stack is crucial for debugging embedded Lua environments.

### 5.1 The Virtual Machine Stack

Every Lua coroutine (thread) has its own stack. This stack holds local variables, function arguments, and temporary values. When a function is called, a new call frame is pushed onto the stack, managing the base pointer for that function's execution.

### 5.2 The C API Stack

When C code interacts with Lua, it pushes and pops values onto the Lua stack. Indices can be positive (absolute, starting from 1 at the bottom) or negative (relative, starting from -1 at the top).

### 5.3 Worst-Case Scenarios and Tech Support Operations

**Scenario A: Stack Overflow**
If a Lua script recurses too deeply, or if C code pushes too many values without popping them, the stack overflows.
*   **Diagnosis:** Lua throws a `stack overflow` error. In C, failing to check `lua_checkstack` can lead to memory corruption and segmentation faults.
*   **Resolution:** Limit recursion depth. In C extensions, rigorously balance stack operations. Use `lua_gettop` and `lua_settop` to ensure the stack is clean before returning.

**Scenario B: Memory Corruption via Invalid Indices**
Accessing invalid stack indices from C (e.g., popping from an empty stack) causes undefined behavior, often resulting in silent data corruption or delayed crashes.
*   **Diagnosis:** Extremely difficult. Requires using tools like Valgrind or AddressSanitizer on the C host application.
*   **Resolution:** Implement strict assertions in C code. Wrap Lua API calls in macros that validate stack bounds.

## 6. Lua Table Implementation: Arrays and Hash Maps

Tables are the sole data structuring mechanism in Lua. They seamlessly act as arrays, dictionaries, objects, and modules.

### 6.1 The Array and Hash Parts

A Lua table consists of two parts:
*   **Array Part:** A contiguous block of memory optimized for integer keys from 1 to N.
*   **Hash Part:** A hash table for all other keys (strings, objects, sparse integers).

Lua dynamically resizes these parts based on usage. If you insert `t[1] = "a"`, it goes to the array part. If you insert `t[1000] = "b"`, it goes to the hash part to avoid allocating 999 empty slots.

### 6.2 Metatables and Metamethods

Metatables allow developers to override table behavior (e.g., addition, indexing). The `__index` and `__newindex` metamethods are heavily used for object-oriented programming in Lua.

### 6.3 Worst-Case Scenarios and Tech Support Operations

**Scenario A: Performance Pitfalls with Sparse Arrays**
Iterating over a sparse array using `ipairs` will stop at the first `nil` value. Using `#t` (the length operator) on a table with holes yields unpredictable results because Lua uses a binary search to find the boundary.
*   **Diagnosis:** Logic errors where loops terminate early, or incorrect array lengths are reported.
*   **Resolution:** Avoid creating arrays with holes. If sparse data is required, use `pairs` and treat the table strictly as a dictionary.

**Scenario B: Memory Bloat from Rehashing**
Repeatedly adding and removing keys from a table forces Lua to rehash and reallocate memory frequently, causing CPU spikes and memory fragmentation.
*   **Diagnosis:** Profiling shows high time spent in `luaH_newkey` or `rehash`.
*   **Resolution:** Pre-allocate tables if the size is known, or reuse tables by clearing them (setting values to `nil`) rather than creating new ones.

## 7. Go-to-C Interoperability: The Perils of cgo

`cgo` allows Go packages to call C code. While powerful, it bridges two entirely different memory management and scheduling domains, creating a minefield for tech support operations.

### 7.1 The cgo Boundary Overhead

Calling C from Go is not free. The Go runtime must transition the goroutine to a system stack, lock the OS thread (M), and disable preemption. This overhead can be hundreds of times slower than a native Go function call.

### 7.2 Memory Management Across the Boundary

Go uses a garbage collector; C requires manual memory management (`malloc`/`free`). Passing pointers between Go and C is strictly regulated. Go pointers passed to C must not contain other Go pointers, and C code must not hold onto Go pointers after the call returns.

### 7.3 Worst-Case Scenarios and Tech Support Operations

**Scenario A: C-Induced Deadlocks and Thread Exhaustion**
If a C function blocks indefinitely (e.g., waiting on a socket), the underlying OS thread (M) is locked. If this happens concurrently, Go will spawn new M's up to the `SetMaxThreads` limit (default 10,000), eventually crashing the application.
*   **Diagnosis:** The application becomes unresponsive. Goroutine dumps show many goroutines stuck in `cgocall`.
*   **Resolution:** Never perform long-blocking operations in C code called from Go. If necessary, use asynchronous C APIs and poll them from Go.

**Scenario B: Segmentation Faults and Memory Corruption**
If C code writes past the bounds of an array passed from Go, or if it frees memory that Go is still using, the application will crash with a segmentation fault.
*   **Diagnosis:** The Go runtime will print a C stack trace (if possible) and crash. Debugging requires `gdb` or `lldb` to inspect the core dump.
*   **Resolution:** Strictly adhere to cgo pointer passing rules. Use C memory for data that needs to persist in C, and explicitly free it from Go using `C.free`.

## 8. Production Operations & Tech Support Tooling

For a tech support specialist, theoretical knowledge must be backed by practical tooling.

### 8.1 Go Debugging Tools

*   **pprof:** The standard tool for profiling CPU, memory, goroutines, and mutex contention. SREs must be adept at reading pprof flame graphs.
*   **trace:** The `runtime/trace` package provides microsecond-level visibility into the scheduler, garbage collector, and network I/O. It is invaluable for diagnosing latency spikes.
*   **Delve (dlv):** The official Go debugger. Useful for attaching to running processes to inspect state, though less commonly used in production due to performance overhead.

### 8.2 Lua Debugging Tools

*   **The `debug` library:** Provides hooks for tracing execution, inspecting local variables, and profiling. However, it significantly degrades performance and should be used conditionally.
*   **Custom C-level Profilers:** In embedded environments, SREs often rely on custom C code to sample the Lua VM state and generate flame graphs.

## 9. Relation to Other Specialist Files

This document, **Topic 7: Deep dive into Go/Lua internals**, is a critical component of the broader tech support operations knowledge base. It interlocks with the other 6 specialist files in the following ways:

1.  **Topic 1: Incident Response Frameworks:** The debugging techniques outlined here (e.g., pprof analysis, core dump inspection) are the technical execution arms of the high-level incident response protocols.
2.  **Topic 2: Distributed Systems Tracing:** While Topic 2 covers macro-level tracing across microservices, this document provides the micro-level tracing required when a single Go node or Lua script becomes the bottleneck.
3.  **Topic 3: Database Performance Tuning:** Go applications frequently interact with databases. Understanding Go's connection pooling (which relies heavily on channels and goroutines) is essential for diagnosing database exhaustion issues discussed in Topic 3.
4.  **Topic 4: Network Protocol Deep Dives:** Network I/O in Go is tightly integrated with the `sysmon` thread and the `netpoller`. The scheduler internals discussed here explain how Go handles millions of concurrent network connections efficiently.
5.  **Topic 5: Security and Vulnerability Management:** Memory corruption in cgo or Lua C APIs often leads to exploitable vulnerabilities. The memory management sections here provide the foundation for identifying and mitigating these risks.
6.  **Topic 6: Cloud Infrastructure and Kubernetes:** When Go applications are deployed in Kubernetes, OS-level constraints (like CPU throttling) interact directly with the Go scheduler (GOMAXPROCS). Understanding the M:N model is crucial for right-sizing containers.

By mastering the internals of Go and Lua, tech support specialists elevate their capabilities from merely restarting crashed services to diagnosing and permanently resolving the most complex, low-level systemic failures.

## === FILE: 42-go-lua-security-audit.md ===
# Security Audit Procedures for Go and Lua: A Comprehensive Guide for Tech Support and Operations

## 1. Introduction to Go and Lua Security Auditing

In modern distributed systems, the combination of Go (Golang) for high-performance backend services and Lua for lightweight, embeddable scripting (often in Redis, Nginx, or game engines) is incredibly common. However, this dual-language architecture introduces unique security challenges. Tech support engineers, operations teams, and security auditors must be equipped to handle vulnerabilities that span both compiled and interpreted boundaries.

This document provides a massive, comprehensive guide to security audit procedures for Go and Lua environments. It focuses on dependency scanning, secure coding practices, preventing injection attacks in Lua scripts, and securing data migration pipelines. Designed for production operations and worst-case scenarios, this guide ensures that your tech support and incident response teams can effectively audit, mitigate, and resolve security issues.

---

## 2. Dependency Scanning and Management in Go

Go's module system is robust, but dependencies are a primary vector for supply chain attacks. Auditing Go dependencies requires a systematic approach using official tools and best practices.

### 2.1 Using `govulncheck`

`govulncheck` is the official Go vulnerability checker. Unlike standard scanners that only look at `go.mod`, `govulncheck` analyzes the actual call graph to determine if your code *calls* a vulnerable function.

#### 2.1.1 Installation and Basic Usage

To install `govulncheck`:
```bash
go install golang.org/x/vuln/cmd/govulncheck@latest
```

To run an audit on your codebase:
```bash
govulncheck ./...
```

#### 2.1.2 Interpreting `govulncheck` Output

When `govulncheck` identifies a vulnerability, it provides:
- The CVE/GO-ID.
- The specific package and version.
- The exact trace of function calls from your code to the vulnerable function.

**Tech Support Action Plan:**
1. **Verify the Call Trace:** If the vulnerability is in a function that is never executed in your production environment (e.g., a test helper), the priority is lower.
2. **Update the Dependency:** Run `go get package@version` to update to a patched version.
3. **Re-run the Scan:** Ensure the vulnerability is resolved.

### 2.2 Auditing `go.mod` and `go.sum`

The `go.sum` file contains cryptographic hashes of module versions. It ensures that the modules you download are identical to what the author published.

**Audit Checklist:**
- **Never ignore `go.sum` conflicts:** If a developer reports a `go.sum` mismatch, DO NOT simply delete the file and run `go mod tidy`. This could indicate a compromised upstream repository.
- **Use `GOSUMDB`:** Ensure the Go checksum database is enabled (`go env GOSUMDB` should be `sum.golang.org`).
- **Vendoring:** For highly secure environments, consider vendoring dependencies (`go mod vendor`) and auditing the vendored code.

### 2.3 Worst-Case Scenario: Compromised Upstream Dependency

If a critical dependency is compromised (e.g., malicious code injected into a popular logging library):
1. **Identify Impact:** Use `go list -m all | grep <package>` to find all services using the package.
2. **Isolate:** Block network egress for affected services if the malicious code attempts data exfiltration.
3. **Rollback:** Revert to a known good version in `go.mod` and update `go.sum`.
4. **Audit Logs:** Check application logs for unusual activity during the exposure window.

---

## 3. Secure Coding Practices in Go

Go's design prevents many common vulnerabilities (like buffer overflows), but logical errors, concurrency bugs, and improper input handling can still lead to severe security breaches.

### 3.1 Concurrency and Race Conditions

Go's goroutines make concurrency easy, but race conditions can lead to unpredictable behavior and security flaws (e.g., Time-of-Check to Time-of-Use (TOCTOU) vulnerabilities).

**Audit Procedures:**
- **Run the Race Detector:** Always run tests and, if possible, staging environments with the race detector enabled: `go test -race ./...` or `go build -race`.
- **Review Mutex Usage:** Ensure `sync.Mutex` or `sync.RWMutex` is used correctly to protect shared state.
- **Channel Security:** Verify that channels are closed properly to prevent goroutine leaks, which can lead to Denial of Service (DoS).

### 3.2 Input Validation and Sanitization

Never trust user input. In Go, this means validating data at the boundary before it reaches business logic.

**Best Practices:**
- **Use Struct Tags:** Use libraries like `go-playground/validator` to enforce validation rules via struct tags.
- **Sanitize HTML/SQL:** Use `html/template` instead of `text/template` to prevent XSS. Use parameterized queries (e.g., `database/sql` with `?` placeholders) to prevent SQL injection.

### 3.3 Error Handling and Information Disclosure

Improper error handling can leak sensitive information (e.g., database connection strings, internal file paths) to attackers.

**Audit Checklist:**
- **Do not expose raw errors to users:** Log the detailed error internally, but return a generic message to the client.
- **Use structured logging:** Ensure sensitive fields (passwords, tokens) are redacted before logging.

---

## 4. Preventing Injection in Lua Scripts

Lua is frequently used as an embedded scripting language, particularly in Redis (for atomic operations) and Nginx (via OpenResty). Because Lua scripts often execute with high privileges within the host application, injection attacks are catastrophic.

### 4.1 Understanding Lua Injection

Lua injection occurs when untrusted user input is concatenated directly into a Lua script that is then evaluated by the host environment.

**Example of Vulnerable Code (Redis/Node.js):**
```javascript
// VULNERABLE: User input directly concatenated into the script
const script = `return redis.call('get', '${userInput}')`;
redis.eval(script, 0);
```
If `userInput` is `') redis.call('flushall') --`, the script becomes:
```lua
return redis.call('get', '') redis.call('flushall') --')
```
This would wipe the entire Redis database.

### 4.2 Mitigation Strategies

#### 4.2.1 Parameterized Execution (KEYS and ARGV)

The primary defense against Lua injection in Redis is to pass user input as arguments (`KEYS` and `ARGV`), NEVER by concatenating strings.

**Secure Implementation:**
```javascript
// SECURE: Passing input via ARGV
const script = `return redis.call('get', ARGV[1])`;
redis.eval(script, 0, [userInput]);
```

**Audit Procedure:**
- Grep the codebase for `eval` or `evalsha` calls.
- Verify that the script string is a static constant and not dynamically generated.
- Ensure all dynamic data is passed via the `KEYS` or `ARGV` arrays.

#### 4.2.2 Sandboxing and Environment Restrictions

When embedding Lua in custom Go applications (e.g., using `gopher-lua`), you must restrict what the Lua script can do.

**Audit Checklist:**
- **Disable OS/IO Modules:** Ensure the `os` and `io` modules are not loaded in the Lua state unless absolutely necessary.
- **Limit Execution Time:** Implement timeouts to prevent Lua scripts from causing a DoS via infinite loops.
- **Memory Limits:** Restrict the amount of memory the Lua state can allocate.

### 4.3 Worst-Case Scenario: Malicious Lua Script Execution

If an attacker successfully injects a malicious Lua script into your Redis instance:
1. **Kill the Script:** Use the `SCRIPT KILL` command in Redis to stop long-running scripts.
2. **Audit Redis Logs:** Check the Redis slow log and command logs to identify what the script did.
3. **Rotate Credentials:** If the script accessed sensitive data, rotate relevant API keys or passwords.
4. **Patch the Vulnerability:** Immediately rewrite the vulnerable code to use parameterized execution.

---

## 5. Securing Migration Pipelines

Migration pipelines—whether moving data between databases, upgrading schemas, or transitioning from legacy systems—are high-risk operations. They often require elevated privileges and handle massive amounts of sensitive data.

### 5.1 Principle of Least Privilege

Migration scripts should only have the permissions necessary to perform their specific tasks.

**Audit Procedures:**
- **Dedicated Migration Roles:** Do not use the application's runtime database user for migrations. Create a dedicated role (e.g., `migration_user`) that can alter schemas but cannot access user data, or vice versa, depending on the migration type.
- **Temporary Credentials:** Use HashiCorp Vault or AWS Secrets Manager to generate short-lived, temporary credentials for the migration process.

### 5.2 Data Masking and Anonymization

When migrating data from production to staging or testing environments, sensitive data (PII, PHI, financial records) must be masked.

**Best Practices:**
- **In-Transit Masking:** Apply masking functions during the extraction phase, before the data is written to the destination.
- **Audit Masking Rules:** Regularly review the masking rules to ensure new sensitive columns are included.

### 5.3 Integrity Checks and Rollback Plans

A secure migration pipeline must guarantee data integrity and provide a safe rollback mechanism.

**Audit Checklist:**
- **Checksums:** Calculate checksums (e.g., SHA-256) of the data before and after migration to verify integrity.
- **Dry Runs:** Always perform a dry run of the migration in a staging environment that mirrors production.
- **Automated Rollbacks:** Ensure that every migration script has a corresponding rollback script. Test the rollback scripts regularly.

### 5.4 Securing the Migration Infrastructure

The servers and tools used to execute migrations must be hardened.

- **Network Isolation:** Run migration jobs in a secure, isolated subnet with strict security group rules.
- **Audit Logging:** Log every step of the migration process, including who initiated it, what scripts were run, and any errors encountered. Forward these logs to a centralized SIEM.

---

## 6. Comprehensive Audit Checklist for Tech Support

When conducting a security audit or responding to an incident involving Go and Lua, tech support and operations teams should follow this checklist:

### Phase 1: Dependency and Static Analysis
- [ ] Run `govulncheck ./...` and document all findings.
- [ ] Verify `go.sum` integrity and ensure `GOSUMDB` is enabled.
- [ ] Run static analysis tools (e.g., `golangci-lint` with security linters enabled).
- [ ] Review all third-party Lua libraries for known vulnerabilities.

### Phase 2: Code Review and Dynamic Analysis
- [ ] Grep for dynamic Lua script generation (e.g., string concatenation in `eval`).
- [ ] Verify that all Redis Lua scripts use `KEYS` and `ARGV`.
- [ ] Run Go tests with the `-race` flag to identify concurrency issues.
- [ ] Review input validation logic at all API boundaries.

### Phase 3: Infrastructure and Pipeline Security
- [ ] Audit database permissions for migration roles.
- [ ] Verify that temporary credentials are used for migration pipelines.
- [ ] Review data masking configurations for non-production environments.
- [ ] Ensure migration infrastructure is network-isolated and heavily logged.

### Phase 4: Incident Response Readiness
- [ ] Verify that Redis `SCRIPT KILL` procedures are documented and tested.
- [ ] Ensure Go application logs do not leak sensitive information.
- [ ] Confirm that rollback procedures for migrations are automated and tested.

---

## 7. Conclusion

Securing a Go and Lua architecture requires vigilance across multiple domains: dependency management, secure coding, script sandboxing, and operational pipelines. By implementing the procedures outlined in this massive guide, tech support and operations teams can proactively identify vulnerabilities, respond effectively to incidents, and maintain the integrity of their production systems. Continuous auditing, automated scanning with tools like `govulncheck`, and strict adherence to the principle of least privilege are the cornerstones of a robust security posture.

## === FILE: 42-go-lua-specialist.md ===
# Go and Lua Specialist: Tech Support Operations Guide

## Go Architecture and Its Role in Modern Backend Systems

Go (also known as Golang) has emerged as a premier programming language for backend development, particularly in large-scale, high-performance production environments. Its architectural design, runtime model, and concurrency primitives offer distinct advantages for building resilient, maintainable backend services. This section provides a deep dive into Go’s architecture with an emphasis on **production operations**, **worst-case scenarios**, and **technical support considerations**.

---

### 1. Core Architectural Components of Go

Understanding Go’s architecture is foundational to leveraging its strengths in backend systems.

| Component               | Description                                                                                     |
|-------------------------|-------------------------------------------------------------------------------------------------|
| **Go Compiler (gc)**    | Translates Go source code into optimized machine code. Supports cross-compilation out-of-the-box. |
| **Go Runtime**          | Manages goroutines, garbage collection, scheduling, and system calls.                           |
| **Goroutines**          | Lightweight threads managed by Go runtime, enabling massive concurrency without OS thread overhead. |
| **Channels**            | Typed conduits for communication between goroutines, facilitating safe concurrent data exchange. |
| **Garbage Collector**   | Concurrent, low-pause-time garbage collector optimized for server workloads.                    |
| **Standard Library**    | Rich, performant libraries for networking, cryptography, HTTP, and more, reducing external dependencies. |

---

### 2. Role of Go Architecture in Modern Backend Systems

Modern backend systems require **scalability**, **resilience**, **low latency**, and **ease of maintenance**—areas where Go’s architecture excels:

#### 2.1 Concurrency Model: Goroutines and Channels

Traditional multithreading often introduces complexity such as race conditions, deadlocks, and high context-switching overhead. Go’s goroutines are **lightweight user-space threads** that typically consume just a few kilobytes of stack memory, allowing tens of thousands to run concurrently within a single process.

- **Production Impact:** This enables backend services to handle **massive concurrent connections** (e.g., HTTP requests, streaming data) without spawning OS threads, reducing resource consumption.
- **Tech Support Note:** Goroutine leaks—goroutines blocked indefinitely—can degrade system performance. Tools like `pprof` and runtime tracing (`runtime/trace`) are essential for diagnosing goroutine-related issues.

Channels provide a **structured mechanism for synchronization and communication**, reducing the need for explicit locking and preventing many concurrency bugs.

#### 2.2 Efficient Garbage Collection

Go’s **concurrent garbage collector** is optimized for low latency, critical in production backends with strict SLAs.

- **Production Operations:** In latency-sensitive systems (e.g., financial trading platforms), GC pauses can cause performance spikes. Go’s GC aims for sub-millisecond pauses by performing most work concurrently with application goroutines.
- **Worst-Case Scenario:** Under heavy memory pressure or excessive allocations, GC overhead can increase, causing noticeable latency spikes or increased CPU usage. Monitoring metrics like `GOGC` (Garbage Collection target percentage) and heap size is essential.

#### 2.3 Static Compilation and Deployment

Go’s static compilation produces **self-contained binaries** with all dependencies included.

- **Benefits for Production:** Simplifies deployment pipelines, reduces runtime dependencies, and improves startup time—a key factor in microservices and containerized environments.
- **Tech Support Advantage:** When troubleshooting, having a single binary reduces complexity. However, embedded configuration and secrets require careful management to avoid security risks.

---

### 3. Production Operations: Best Practices and Challenges

#### 3.1 Monitoring and Observability

- **Profiling:** Use `net/http/pprof` for CPU, memory, and goroutine profiling in production.
- **Tracing:** Integrate with OpenTelemetry or similar frameworks to trace request lifecycles across distributed systems.
- **Metrics:** Expose Prometheus-compatible metrics via `expvar` or third-party libraries to monitor GC pauses, goroutine counts, and request latency.

#### 3.2 Resource Management

- Limit goroutine creation to avoid memory exhaustion.
- Tune `GOMAXPROCS` to match CPU cores for optimal scheduler efficiency.
- Control memory usage via environment variables (`GOGC`, `GOMEMLIMIT` in Go 1.19+).

#### 3.3 Configuration and Secrets

- Externalize configuration to environment variables or configuration services.
- Avoid embedding sensitive information in binaries.
- Use runtime flags for dynamic tuning without redeployment.

---

### 4. Handling Worst-Case Scenarios

#### 4.1 Goroutine Leaks and Deadlocks

**Symptom:** Application becomes unresponsive or resource consumption grows uncontrollably.

**Mitigation:**

- Use `runtime.NumGoroutine()` as a health check metric.
- Analyze stack traces and goroutine dumps.
- Implement timeouts and context cancellation to prevent indefinite blocking.

#### 4.2 Garbage Collection Pressure

**Symptom:** Increased latency spikes, CPU thrashing, or OOM kills.

**Mitigation:**

- Profile allocations and reduce heap fragmentation.
- Use object pooling to minimize allocations.
- Adjust `GOGC` tuning parameters.
- Upgrade Go runtime to latest stable version for GC improvements.

#### 4.3 Deadlocks in Channel Communication

**Symptom:** Application halts because goroutines wait indefinitely on channels.

**Mitigation:**

- Use buffered channels where applicable.
- Apply select statements with default cases or timeouts.
- Code reviews focused on communication patterns.

---

### 5. Technical Support Considerations

#### 5.1 Debugging Tools

- **`pprof`**: CPU, memory, and goroutine profiling.
- **`dlv` (Delve)**: Go debugger for live debugging and core dump analysis.
- **Runtime tracing**: Visualizing scheduler and GC behavior.

#### 5.2 Log Management

- Standardize structured logging (e.g., JSON format).
- Include goroutine IDs and context metadata for traceability.
- Correlate logs with metrics and traces for comprehensive root cause analysis.

#### 5.3 Incident Response

- Establish alerting on critical metrics (e.g., goroutine spike, GC pause time).
- Develop runbooks for common failure modes such as deadlocks or memory exhaustion.
- Automate graceful restarts and health checks to maintain service availability.

---

### Summary

Go’s architecture—centered around lightweight concurrency, efficient garbage collection, and static compilation—makes it an excellent choice for **modern backend systems requiring high scalability and reliability**. However, to maintain robust production operations and minimize downtime in worst-case scenarios, teams must implement comprehensive monitoring, resource management, and incident response strategies. Technical support engineers should leverage Go-specific tooling and best practices to diagnose and resolve performance issues rapidly, ensuring backend systems remain resilient under heavy load and complex operational conditions.

# Go Concurrency Models: Goroutines and Channels  
*An In-Depth Guide for Production Operations, Troubleshooting, and Worst-Case Scenario Handling*

---

## Introduction

Go (Golang) offers a powerful concurrency model centered around **goroutines** and **channels**. This model simplifies concurrent programming but introduces unique challenges in production, particularly around **deadlocks**, **race conditions**, and **performance bottlenecks**. This section provides a detailed exploration focused on practical production operations, worst-case scenarios, and technical support troubleshooting for systems built using Go's concurrency primitives.

---

## 1. Goroutines: Lightweight Concurrent Units

### 1.1 Overview

- Goroutines are lightweight, managed threads launched with the `go` keyword.
- They multiplex onto OS threads transparently.
- Stacks start small (~2KB) and grow dynamically.
- Ideal for high concurrency with minimal resource overhead.

### 1.2 Production Considerations

| Aspect                  | Details                                                                                  |
|-------------------------|------------------------------------------------------------------------------------------|
| Stack Growth            | Goroutine stacks grow automatically, but unbounded growth can cause memory exhaustion.   |
| Scheduling              | Go scheduler multiplexes goroutines onto OS threads; blocking syscalls can cause delays.|
| Resource Limits         | Excessive goroutine creation (>100k) may lead to high CPU/memory usage or scheduler stalls.|
| Panic Propagation       | Panics inside goroutines do not propagate to the parent goroutine and must be handled explicitly.|

### 1.3 Worst-Case Scenario: Goroutine Leak

```go
func leakyWorker() {
    for {
        go func() {
            time.Sleep(time.Hour) // Goroutine blocks indefinitely
        }()
        time.Sleep(time.Millisecond)
    }
}
```

- **Symptom**: Continuous growth in goroutine count, system memory exhaustion.
- **Detection**: Use `runtime.NumGoroutine()` and profiling tools like `pprof`.
- **Mitigation**: Implement cancellation contexts and bounded worker pools.

---

## 2. Channels: Typed Communication Pipes

### 2.1 Overview

- Channels provide typed communication between goroutines.
- Supports synchronous (unbuffered) and asynchronous (buffered) communication.
- Enables coordination and data exchange without explicit locks.

### 2.2 Channel Operations

| Operation          | Description                                          | Blocking Behavior                   |
|--------------------|----------------------------------------------------|-----------------------------------|
| `ch <- value`      | Send value to channel                               | Blocks if unbuffered or buffer full|
| `value := <- ch`   | Receive from channel                                | Blocks if empty                   |
| `close(ch)`        | Close channel signaling no more values will be sent| Sending on closed channel panics  |

---

## 3. Deadlocks in Go Concurrency

### 3.1 Common Deadlock Patterns

| Pattern                      | Description                                           | Example                                                         |
|------------------------------|-----------------------------------------------------|-----------------------------------------------------------------|
| All goroutines blocked on channel ops | No goroutine is able to proceed because of blocking sends/receives | Both sender and receiver waiting on each other                  |
| Sending on closed channel     | Panic causes program crash or deadlock in recovery  | Sending after `close(ch)`                                        |
| Unbuffered channel with no receiver | Send blocks indefinitely                            | Sender waits forever if no goroutine receives                   |

### 3.2 Deadlock Example

```go
func deadlockExample() {
    ch := make(chan int)
    ch <- 1 // Blocks forever, no receiver
}
```

- **Symptom**: Program hangs, 100% CPU usage on one thread, no progress.
- **Detection**: Go runtime panics with “all goroutines are asleep - deadlock!” or profiling goroutine stacks.
- **Mitigation**: Use buffered channels or ensure receiver goroutine is running before send.

---

## 4. Race Conditions and Data Races

### 4.1 Cause

- Concurrent goroutines access shared variables without synchronization.
- Leads to inconsistent or corrupted data states.

### 4.2 Detection

- Use Go race detector: `go run -race` or `go test -race`.
- Identifies unsynchronized read/write conflicts.

### 4.3 Example of Race Condition

```go
var counter int

func increment() {
    counter++ // Not atomic, unsafe in concurrent use
}

func main() {
    for i := 0; i < 1000; i++ {
        go increment()
    }
    time.Sleep(time.Second)
    fmt.Println(counter) // Output may be less than 1000
}
```

- **Symptom**: Unexpected values, crashes, or corrupted state.
- **Mitigation**: Use synchronization primitives (`sync.Mutex`, atomic operations) or design data exchange via channels.

---

## 5. Best Practices for Production Operations and Troubleshooting

| Category                  | Best Practice                                                                                                         | Rationale                                                                                      |
|---------------------------|----------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------|
| Goroutine Management      | Limit number of goroutines using worker pools or rate limiting                                                       | Avoid resource exhaustion and scheduler overhead                                             |
| Channel Usage             | Prefer buffered channels with capacity tuned to workload; avoid sending on closed channels                           | Prevent blocking and runtime panics                                                           |
| Deadlock Avoidance        | Always have receiver goroutine ready before sending; use `select` with `default` to avoid blocking sends/receives    | Enables non-blocking operations and deadlock prevention                                      |
| Panic Recovery            | Use `defer` with `recover()` inside goroutines to gracefully handle panics                                           | Prevents unexpected program termination                                                      |
| Race Detection            | Always run race detector during testing and CI pipelines                                                             | Early detection of concurrency bugs                                                          |
| Monitoring                | Use `runtime.NumGoroutine()`, `pprof`, and external tools (e.g., Prometheus) to monitor goroutine counts and CPU usage| Early detection of leaks, deadlocks, or performance bottlenecks                               |
| Logging                   | Correlate goroutine lifecycle and channel events with logs enriched with context IDs                                 | Facilitates root cause analysis during incidents                                              |

---

## 6. Troubleshooting Workflow for Concurrency Issues

| Step               | Action                                                                                     | Tools/Commands                                           |
|--------------------|--------------------------------------------------------------------------------------------|----------------------------------------------------------|
| 1. Identify Symptom | Application hang, crash, unexpected output                                                | Logs, monitoring dashboards                               |
| 2. Capture Stack   | Dump goroutine stacks to identify blocked goroutines                                       | `kill -QUIT <pid>`, `go tool pprof`, `runtime.Stack()`   |
| 3. Check Goroutine Count | Look for abnormal growth or stuck goroutines                                             | `runtime.NumGoroutine()`, pprof goroutine profile         |
| 4. Analyze Channels | Inspect channel usage and buffer states                                                    | Code review, trace logs, runtime channel debugging tools  |
| 5. Run Race Detector| Execute with `-race` to detect data races                                                  | `go run -race`, `go test -race`                           |
| 6. Use Profilers    | CPU and memory profiling to detect bottlenecks or leaks                                   | `pprof`, `trace`                                          |
| 7. Apply Fixes      | Add synchronization, buffer sizes, cancellation contexts, and panic recovery              | Code changes                                              |
| 8. Validate & Monitor| Deploy fixes to staging, monitor for recurrence                                           | Application monitoring, alerting                          |

---

## 7. Sample Code: Safe Concurrent Worker Pool Using Goroutines and Channels

```go
package main

import (
    "context"
    "fmt"
    "sync"
    "time"
)

func worker(ctx context.Context, id int, jobs <-chan int, wg *sync.WaitGroup) {
    defer wg.Done()
    for {
        select {
        case job, ok := <-jobs:
            if !ok {
                fmt.Printf("Worker %d: no more jobs, exiting\n", id)
                return
            }
            fmt.Printf("Worker %d: processing job %d\n", id, job)
            time.Sleep(100 * time.Millisecond) // Simulate work
        case <-ctx.Done():
            fmt.Printf("Worker %d: context cancelled, exiting\n", id)
            return
        }
    }
}

func main() {
    ctx, cancel := context.WithCancel(context.Background())
    defer cancel()

    jobs := make(chan int, 5)
    var wg sync.WaitGroup

    // Start 3 workers
    for i := 1; i <= 3; i++ {
        wg.Add(1)
        go worker(ctx, i, jobs, &wg)
    }

    // Send 10 jobs
    for j := 1; j <= 10; j++ {
        jobs <- j
    }
    close(jobs) // Signal no more jobs

    // Wait for all workers to finish
    wg.Wait()
    fmt.Println("All workers completed")
}
```

**Features:**

- Uses buffered channel to avoid blocking when sending jobs.
- Uses `context.Context` for cancellation support.
- Uses `sync.WaitGroup` to wait for all goroutines.
- Closes channel to signal no more jobs.
- Prevents deadlocks and goroutine leaks.

---

## Conclusion

Mastering Go’s concurrency model requires understanding the interplay between goroutines and channels, especially under production workloads. Key points to ensure robust systems include:

- **Proactive resource management** to prevent goroutine leaks.
- **Careful channel design** to avoid deadlocks and panics.
- **Vigilant race condition detection** using tools.
- **Comprehensive monitoring and logging** for early detection and troubleshooting.
- **Graceful panic recovery** and cancellation mechanisms.

By applying these principles and best practices, you can build resilient, performant concurrent applications in Go suitable for demanding production environments.

---

# Appendix: Useful Commands and Tools

| Tool/Command                    | Purpose                                         |
|--------------------------------|-------------------------------------------------|
| `go run -race main.go`          | Run with race detector                           |
| `pprof`                        | CPU/memory/goroutine profiling                    |
| `go tool trace`                | Visualize execution trace                          |
| `runtime.NumGoroutine()`       | Programmatic goroutine count                       |
| `kill -QUIT <pid>`             | Dump goroutine stack trace on Linux                |
| `GODEBUG=schedtrace=1000`      | Scheduler trace logging                            |
| `GODEBUG=scheddetail=1`        | Scheduler detail logging                           |

---

*End of Section*

# Lua Architecture and Lua Scripting in Redis: A Comprehensive Guide for Production Operations and Tech Support

---

## Introduction

Redis is a high-performance, in-memory data structure store widely used for caching, real-time analytics, messaging, and more. One of Redis's most powerful features is its support for **Lua scripting**, enabling atomic, complex operations to be executed server-side. This guide covers the architecture of Lua scripting in Redis, focusing on **atomicity**, **performance bottlenecks**, **production operations**, and **worst-case troubleshooting scenarios** from a tech support perspective.

---

## 1. Lua Scripting Architecture in Redis

### 1.1 Embedding Lua in Redis

Redis embeds the Lua 5.1 interpreter directly inside the server process. When a Lua script is executed:

- The script is parsed and compiled.
- The Lua environment is sandboxed with Redis-specific commands exposed as Lua functions.
- The entire script runs **synchronously and atomically** before returning control to the client.

This architecture avoids network round trips for multi-command transactions and ensures Redis commands within the script execute as a single isolated unit.

### 1.2 Execution Model

- Scripts run **single-threaded** on the Redis main thread.
- During script execution, **no other commands are processed** — this guarantees atomicity but can cause latency spikes.
- Scripts can call Redis commands via the `redis.call()` or `redis.pcall()` interfaces.

### 1.3 Script Caching and SHA1 Hashing

- Redis caches scripts by their SHA1 hash.
- Clients can send the SHA1 hash to invoke cached scripts, avoiding re-transmission of the entire script.
- If the script is missing (e.g., after Redis restart), clients fall back to sending full scripts (`EVAL` command).

---

## 2. Atomicity Guarantees

The **atomicity** of Lua scripts is one of the most critical properties:

| **Aspect**                     | **Behavior**                                                                                   |
|-------------------------------|-----------------------------------------------------------------------------------------------|
| Atomic execution               | Entire Lua script runs as a single atomic operation — no other commands interleaved.           |
| Isolation                     | Script sees a consistent snapshot of the data; no changes from other clients during execution |
| No partial updates             | Either all Redis commands in the script succeed or none are applied (if script errors occur)  |
| Failure handling              | Errors abort script execution and rollback partial changes made by Lua commands                |

**Implication for production:** Lua scripts provide a straightforward way to implement complex multi-key transactions without explicit locks or WATCH/MULTI blocks.

---

## 3. Performance Bottlenecks and Pitfalls

While Lua scripts are powerful, their architecture introduces potential bottlenecks and risks:

### 3.1 Blocking the Main Thread

- Lua scripts execute on the **single-threaded Redis main loop**.
- Long-running scripts block all other commands, causing increased latency and client timeouts.
- **Worst-case scenario:** A heavy script can cause Redis to become unresponsive, triggering failover or client disconnects.

### 3.2 Script Execution Time Limit

- Redis has a configurable **`lua-time-limit`** (default: 5 seconds).
- If a script runs longer, Redis logs a warning and may terminate the script.
- Long scripts should be optimized or broken down to avoid hitting this limit.

### 3.3 Memory Usage

- Large data processing inside Lua scripts can consume substantial memory.
- Lua scripts do not have access to Redis memory limits directly but can cause overall server memory pressure.
- Inefficient data structures or loops can exacerbate this.

### 3.4 Non-Deterministic Behavior

- Scripts must be **deterministic**, especially in Redis Cluster.
- Usage of non-deterministic functions or commands (e.g., time-based keys) can cause replication divergence.

---

## 4. Production Operations Best Practices

| **Category**           | **Recommendations**                                                                                         |
|-----------------------|-------------------------------------------------------------------------------------------------------------|
| Script Size           | Keep scripts concise; avoid embedding large data or complex logic that can be done client-side.              |
| Execution Time        | Monitor script execution using `SLOWLOG` and Redis logs to detect long-running scripts.                       |
| Script Caching        | Preload critical scripts on startup using `SCRIPT LOAD` to avoid initial latency spikes.                      |
| Error Handling        | Use `redis.pcall()` to safely execute commands inside scripts and handle errors gracefully.                   |
| Monitoring            | Enable and monitor `lua-time-limit` warnings; track `SLOWLOG` entries related to script execution.            |
| Cluster Compatibility | Ensure scripts access keys within the same hash slot to maintain cluster compatibility.                      |

---

## 5. Troubleshooting Worst-Case Scenarios

### 5.1 Scenario: Redis Becomes Unresponsive Due to Lua Script

- **Cause:** Long-running or infinite-loop Lua script blocking the main thread.
- **Detection:**
  - `SLOWLOG GET` shows Lua scripts with long duration.
  - Redis logs contain `lua-time-limit` warnings.
  - Client timeouts or connection resets.
- **Mitigation:**
  - Use `CLIENT KILL` to terminate problematic clients (if script runs via client).
  - Restart Redis if unresponsive.
  - Analyze script complexity; add execution time limits or break logic.
- **Prevention:**
  - Implement watchdog monitoring on scripts.
  - Enforce strict code reviews for Lua scripts.
  - Use Redis 6+ features such as `SCRIPT KILL` (available in newer versions) to terminate running scripts safely.

### 5.2 Scenario: Script Errors Causing Partial Data Updates

- **Cause:** Unhandled errors inside Lua script (e.g., invalid commands, nil references).
- **Symptoms:** Unexpected data state, partial writes.
- **Detection:**
  - Use `redis.pcall()` to catch errors without aborting the entire script.
  - Enable detailed logging and capture client error responses.
- **Mitigation:**
  - Refactor scripts to handle errors explicitly.
  - Test scripts thoroughly in staging environments.
- **Best Practice:**
  - Wrap critical commands with `pcall` and check error returns.

### 5.3 Scenario: Replication or Cluster Data Divergence

- **Cause:** Non-deterministic scripts or access to keys outside the same hash slot in cluster mode.
- **Symptoms:** Replicas lag, cluster failover issues.
- **Detection:**
  - Inconsistent datasets between master and replicas.
  - Cluster logs warning about key slot mismatches.
- **Mitigation:**
  - Ensure all keys accessed belong to the same hash slot.
  - Avoid non-deterministic commands (e.g., `TIME`, `RANDOM`).
  - Use Redis Cluster-aware client libraries and test scripts in cluster mode.

---

## 6. Example: Safe Lua Script with Error Handling

```lua
-- Increment a counter only if the key exists, else return an error
local key = KEYS[1]

-- Use pcall to catch errors
local exists = redis.call('EXISTS', key)
if exists == 1 then
    local ok, result = pcall(function()
        return redis.call('INCR', key)
    end)
    if ok then
        return result
    else
        return redis.error_reply("INCR command failed: " .. result)
    end
else
    return redis.error_reply("Key does not exist")
end
```

**Explanation:**

- Checks key existence before incrementing.
- Uses `pcall` to catch any runtime errors of `INCR`.
- Returns explicit error messages for the client.

---

## 7. Summary Table: Lua Scripting in Redis

| **Topic**                  | **Key Points**                                                                                             |
|----------------------------|------------------------------------------------------------------------------------------------------------|
| Architecture               | Embedded Lua 5.1 interpreter, synchronous single-threaded execution, script caching by SHA1                |
| Atomicity                 | Entire script runs atomically, no interleaving or partial writes, consistent snapshot for script execution |
| Performance Bottlenecks   | Blocking main thread, long-running scripts, memory usage, non-determinism in cluster mode                   |
| Production Best Practices | Monitor script times, keep scripts small, preload scripts, handle errors, ensure cluster-safe scripting     |
| Troubleshooting           | Use logs and SLOWLOG, handle script errors with pcall, watch for lua-time-limit warnings, avoid bad scripts |
| Worst-case Scenarios      | Unresponsive Redis due to scripts, partial writes, cluster divergence, mitigated with monitoring and limits  |

---

## Conclusion

Lua scripting in Redis is a powerful feature enabling atomic, complex operations with minimal client-server overhead. However, understanding the underlying architecture, performance implications, and operational risks is crucial for production reliability. By applying best practices, monitoring execution, and preparing for worst-case scenarios, operators and tech support engineers can leverage Lua scripts safely and efficiently in demanding environments.

---

**References:**

- Redis Official Documentation: https://redis.io/docs/manual/programmability/eval-intro/
- Redis Lua Scripting Guide: https://redis.io/docs/manual/programmability/eval-intro/
- Redis Cluster Scripting Caveats: https://redis.io/docs/manual/scaling/#lua-scripts-in-cluster-mode
- Redis `lua-time-limit` Configuration: https://redis.io/docs/manual/config/#lua-time-limit

---

*End of Section*

# Comprehensive Guide to Database Migrations Using `golang-migrate`

Database migrations are a critical part of modern application deployment, ensuring schema versioning, consistent data structures, and controlled rollouts. When using [golang-migrate](https://github.com/golang-migrate/migrate), a robust migration tool written in Go, understanding its operation in production environments, handling failures, and troubleshooting “dirty” states is essential for maintaining production stability and operational confidence.

---

## 1. Overview of `golang-migrate`

`golang-migrate` provides a CLI and Go library for applying versioned migrations to multiple database engines (PostgreSQL, MySQL, SQLite, etc.). It manages migration versions with an internal schema table (default: `schema_migrations`), tracking applied migration files.

### Key Concepts

| Term              | Description                                           |
|-------------------|-------------------------------------------------------|
| Migration         | A `.sql` or `.go` file that applies one step of schema change (up/down). |
| Version           | Unique integer (usually timestamp-based) identifying migration order. |
| Dirty State       | Database migration state where a previous migration failed and left the DB partially migrated. |
| Locking           | Mechanism to prevent concurrent migrations from running. |

---

## 2. Production Migration Workflow

In production, the migration process must be **idempotent**, **atomic where possible**, and **reliable**. Below is a recommended workflow for `golang-migrate` usage.

### Step-by-Step Production Migration

1. **Backup Database**  
   Always create a backup snapshot before applying migrations:
   ```bash
   pg_dump -Fc -f backup_before_migration.dump mydb
   ```

2. **Pre-Validate Migrations**  
   Run migrations against a staging environment identical to production.

3. **Run Migrations with Locking**  
   `golang-migrate` automatically locks the schema. Run migrations as a single atomic operation:
   ```bash
   migrate -database "postgres://user:pass@host:5432/dbname?sslmode=disable" -path ./migrations up
   ```

4. **Verify Migration Success**  
   Check the migration version and dirty flag:
   ```bash
   migrate -database "..." -path ./migrations version
   ```

5. **Monitor Application Logs**  
   For schema-dependent queries failing post-migration.

---

## 3. Handling Failed Migrations and Dirty States

### What is a Dirty State?

When a migration fails mid-application (e.g., syntax error in SQL, connectivity loss), `golang-migrate` marks the database as **dirty** at the failed version to prevent further migrations from running until manually resolved.

### Detecting Dirty State

Check current state:
```bash
migrate -database "postgres://..." -path ./migrations version
```

Output example:
```
14 dirty
```

This means migration version 14 failed and the schema is in an inconsistent state.

### Consequences of Dirty State

- **No further migrations** can be applied until the dirty state is cleared.
- Application queries may face schema inconsistencies or runtime errors.
- Manual intervention is mandatory to fix the state.

---

## 4. Operational Procedures for Dirty State Recovery

### Step 1: Assess the Damage

- Review the failed migration file (e.g., `14_add_new_column.up.sql`).
- Check database logs and error messages.
- If migration partially executed DDL/DML commands, determine what was applied.

### Step 2: Manual Database Fix (If Needed)

- Connect to the database and manually fix schema inconsistencies.
- Example: if a column was partially added or a constraint partially applied, DROP or FIX manually:
  
```sql
-- Example: Remove partially added column
ALTER TABLE users DROP COLUMN IF EXISTS new_feature_flag;
```

### Step 3: Reset Dirty Flag

Once the database is consistent, reset the dirty flag with:

```bash
migrate -database "postgres://..." -path ./migrations force <version>
```

- `<version>` is the last successfully applied migration before the dirty one.
- For example, if migration 14 is dirty, and 13 applied successfully:
  
```bash
migrate -database "..." -path ./migrations force 13
```

**This does not reapply migrations; it only clears the dirty flag to allow retrying or further migrations.**

### Step 4: Retry Migration or Rollback

- Retry the failed migration after fixing the problem (e.g., fix SQL errors).
- Or rollback if needed:
  
```bash
migrate -database "..." -path ./migrations down 1
```

- Confirm migration status again.

---

## 5. Worst-Case Scenario Handling

| Scenario                          | Description                                                | Recommended Action                                    |
|----------------------------------|------------------------------------------------------------|-----------------------------------------------------|
| Partial Migration Applied        | Migration partially executed some DDL/DML changes          | Restore backup, fix migration scripts, retry        |
| Lost Backup and Dirty DB         | No backup available, dirty migration, corrupted schema     | Manual forensic analysis, rebuild schema, data import |
| Concurrent Migrations Running    | Two migration processes run simultaneously causing lock issues | Kill one process, reset lock, coordinate deployment |
| Migration Script Bugs            | Syntax errors or logic bugs in migration SQL or Go files   | Revert migration, fix script, reapply carefully     |

---

## 6. Tech Support Troubleshooting Checklist

| Step                       | Action                                                        | Commands / Notes                                         |
|----------------------------|---------------------------------------------------------------|----------------------------------------------------------|
| 1. Confirm Migration Status | Check current version and dirty state                         | `migrate version`                                         |
| 2. Inspect Logs             | Review application and DB logs for migration errors           | `/var/log/app.log`, PostgreSQL logs                       |
| 3. Backup Current DB        | Create immediate backup before any manual intervention        | `pg_dump` or equivalent                                   |
| 4. Check Migration Files    | Validate SQL syntax & logic in migration files                 | `psql -f migration.sql` or linting tools                  |
| 5. Resolve Dirty State      | Reset dirty flag after manual fix                              | `migrate force <version>`                                 |
| 6. Retry Migration          | Re-run failing migration after fixes                           | `migrate up`                                             |
| 7. Coordinate with Dev Team | Communicate fixes and rollback plans                           | Documentation and incident reports                        |

---

## 7. Example: Handling a Dirty State in PostgreSQL

```bash
# Check version and dirty state
migrate -database "postgres://user:pass@localhost:5432/mydb?sslmode=disable" -path ./migrations version
# Output:
# 14 dirty

# Inspect failed migration file for errors
cat ./migrations/14_add_new_column.up.sql

# Fix schema manually if needed
psql "postgres://user:pass@localhost:5432/mydb?sslmode=disable"
mydb=> ALTER TABLE users DROP COLUMN IF EXISTS new_feature_flag;

# Reset dirty flag to prior version (13)
migrate -database "postgres://user:pass@localhost:5432/mydb?sslmode=disable" -path ./migrations force 13

# Retry migration
migrate -database "postgres://user:pass@localhost:5432/mydb?sslmode=disable" -path ./migrations up
```

---

## 8. Best Practices Summary

- **Pre-validate** migrations in staging before production.
- **Always backup** production databases before migration.
- Handle **dirty states immediately**; do not ignore.
- Use **version control** for migration files.
- Maintain **clear rollback plans** and thorough documentation.
- Automate migration runs in CI/CD pipelines with safe guards.
- Monitor application and DB logs closely post-migration.

---

# Conclusion

`golang-migrate` is a powerful tool, but production migrations require careful planning, monitoring, and operational discipline. Understanding and effectively handling dirty states, failed migrations, and worst-case scenarios is essential for minimizing downtime and ensuring database integrity.

By following the detailed procedures and troubleshooting steps outlined above, tech support and system engineers can confidently manage migrations and quickly recover from failures in production environments.

# Tech Support Operations and Client-Facing Guidance for Systems Built with Go and Lua

This section provides a comprehensive guide to managing tech support operations and client-facing communication for systems leveraging **Go** (Golang) and **Lua**. These languages often coexist in high-performance, extensible applications — Go for backend concurrency and system-level tasks, Lua for embedded scripting and configurability. Effective support demands deep understanding of both, robust incident response frameworks, and clear, empathetic client communication.

---

## 1. Incident Response Framework

A well-structured **Incident Response (IR)** process is critical for minimizing downtime and maintaining client trust in production systems that use Go and Lua.

### 1.1 Preparation

- **Documentation:** Maintain detailed runbooks covering:
  - Go service architecture, deployment, and configuration.
  - Lua script lifecycle, execution environment, and integration points.
  - Common failure modes (e.g., Go goroutine leaks, Lua script timeouts).
- **Monitoring & Alerting:**
  - Use tools like **Prometheus**, **Grafana**, **Sentry**, or **ELK Stack** for telemetry.
  - Track key metrics: Go routine counts, GC pauses, Lua script execution time, memory usage.
  - Set up alerts for anomalies (e.g., memory spikes, script errors).

### 1.2 Identification & Triage

- **Log Aggregation:** Centralize logs from Go backend and Lua scripts.
  - Go logs typically include structured JSON logs with error stacks.
  - Lua logs should capture execution errors, stack traces, and timeouts.
- **Error Classification:**
  - **Transient Errors:** Network timeouts, temporary resource exhaustion.
  - **Persistent Errors:** Crashes, memory leaks, Lua syntax errors.
- **Priority Assignment:**
  | Priority | Description                          | Response Time         |
  |----------|----------------------------------|----------------------|
  | P1       | System down, client impact severe | Immediate (within 15m)|
  | P2       | Partial degradation, moderate impact | Within 1 hour       |
  | P3       | Minor issues, no immediate impact | Within 4 hours       |

### 1.3 Containment & Mitigation

- **Go Runtime Issues:** 
  - Use pprof and runtime metrics to identify goroutine leaks or deadlocks.
  - Restart affected Go services gracefully to clear transient states.
- **Lua Script Failures:**
  - Isolate problematic scripts by disabling or rolling back recent changes.
  - Use Lua sandboxing to limit impact (e.g., timeout execution using `debug.sethook`).
- **Service Isolation:** If possible, isolate failing components to prevent cascading failures.

### 1.4 Root Cause Analysis (RCA)

- Collect detailed diagnostics:
  - Go core dumps, heap profiles.
  - Lua error logs, script versions.
- Reproduce issues in staging or test environments.
- Identify and patch bugs or misconfigurations.
- Document findings and update runbooks.

### 1.5 Recovery & Postmortem

- Restore full service functionality.
- Communicate resolution internally and with clients.
- Conduct postmortems focusing on:
  - Incident timeline.
  - Root cause.
  - Mitigations applied.
  - Preventive measures for future.

---

## 2. Communication Strategies with Clients

Client communication during incidents or routine support is as critical as technical remediation.

### 2.1 Transparency & Timeliness

- **Initial Acknowledgement:** Confirm receipt of the issue within 15 minutes for P1, 1 hour for P2.
- **Status Updates:** Provide regular, scheduled updates even if no new information is available.
- **Clear Language:** Avoid excessive technical jargon. Use clear, concise explanations focused on impact and next steps.

### 2.2 Managing Expectations

- Set realistic timelines for resolution.
- Explain complexities of Go concurrency or Lua scripting if relevant.
- Clarify what is in your control vs. what requires client action.

### 2.3 Documentation Sharing

- Provide clients with tailored runbooks or knowledge base articles.
- Share diagnostic steps clients can perform safely (e.g., enabling debug logs).
- Offer best practices for Lua script development or Go service interaction if clients extend/customize system behavior.

### 2.4 Escalation Paths

- Define clear escalation contacts and procedures.
- Include support tiers specialized in Go backend issues vs. Lua scripting challenges.

---

## 3. Handling Worst-Case Scenarios

### 3.1 Complete System Outage

- **Symptoms:** All Go backend services unresponsive, Lua scripts failing en masse.
- **Immediate Steps:**
  - Trigger incident response team.
  - Redirect traffic if possible (load balancers, failover clusters).
  - Roll back recent deployments or configuration changes.
- **Diagnostics:**
  - Analyze Go runtime panics or crashes.
  - Check Lua script compilation errors or infinite loops.
- **Client Communication:** 
  - Provide immediate acknowledgment.
  - Share mitigation steps and estimated recovery time.

### 3.2 Data Corruption Due to Script Errors

- Lua scripts sometimes modify critical data stores.
- If corruption suspected:
  - Stop affected Lua processes immediately.
  - Quarantine corrupted data.
  - Restore from backups if necessary.
- Conduct detailed script audits to prevent recurrence.
- Communicate impact and remediation plan clearly to clients.

### 3.3 Security Breach Exploiting Lua Sandbox or Go APIs

- **Detection:** Unusual Lua script behavior or Go API calls.
- **Containment:** Disable scripting engine if feasible.
- **Investigation:** Review audit logs, verify integrity.
- **Recovery:** Patch vulnerabilities, rotate credentials.
- **Client Notification:** Follow legal and contractual disclosure obligations promptly.

---

## 4. Tech Support Best Practices

### 4.1 Skillset Requirements

- Support engineers must be proficient in:
  - Go debugging tools (`delve`, `pprof`).
  - Lua runtime and debugging (`lua debug library`, sandboxing techniques).
  - Monitoring and log analysis tools.
- Familiarity with container orchestration (Kubernetes) and CI/CD pipelines.

### 4.2 Tooling and Automation

- Automate diagnostics collection scripts for Go and Lua components.
- Use script version control and deployment automation to track changes.
- Employ health check endpoints and readiness probes.

### 4.3 Knowledge Management

- Maintain a centralized knowledge base with:
  - Known issues and resolutions.
  - Go and Lua code snippets for common fixes.
  - Incident reports and lessons learned.
- Encourage continuous learning and cross-training on Go and Lua internals.

---

## Summary Table: Incident Response Checklist for Go and Lua Systems

| Step                  | Go-Specific Actions                  | Lua-Specific Actions                   | Communication Focus                   |
|-----------------------|------------------------------------|--------------------------------------|-------------------------------------|
| Preparation           | Monitor goroutines, GC, logs       | Monitor script timeouts, errors      | Share runbooks and best practices   |
| Identification & Triage | Analyze Go errors and stack traces | Check Lua error logs and script states | Confirm issue receipt, classify severity |
| Containment           | Restart services, isolate failures | Disable faulty scripts, use sandboxing | Inform clients of containment steps |
| RCA                   | Profiler data, core dumps          | Script audit, sandbox review         | Explain root cause in client-friendly terms |
| Recovery              | Redeploy stable builds             | Rollback scripts                     | Provide resolution and preventive guidance |

---

# Conclusion

Supporting production systems built with **Go and Lua** requires a dual-focus approach: mastering the intricacies of both languages and establishing rigorous incident response and communication protocols. By preparing detailed runbooks, leveraging robust monitoring, fostering transparent client communication, and planning for worst-case scenarios, tech support teams can maintain system reliability and client confidence even under significant operational stress.

# Relationship of the Go and Lua Specialist File to Other Specialist Files in the Specialist-Teams Repository

The **Go and Lua Specialist** file occupies a pivotal role within the broader ecosystem of the **specialist-teams** repository. This file is not an isolated knowledge base but a critical node in an interconnected network of seven specialist files, each dedicated to a particular technology stack or operational domain. Understanding its relationship with the other six files is essential for ensuring seamless **cross-functional collaboration**, efficient **incident escalation**, and robust **tech support operations**.

---

## 1. Cross-Functional Collaboration

The Go and Lua Specialist file details best practices, troubleshooting guides, and production hardening techniques for applications primarily written in Go and Lua. Given the polyglot nature of modern production environments, other specialist files cover technologies such as:

| Specialist File          | Primary Focus                   |
|-------------------------|--------------------------------|
| Python Specialist       | Python application services    |
| Java Specialist         | JVM-based systems and services |
| Database Specialist     | SQL and NoSQL databases        |
| Networking Specialist   | Network infrastructure and protocols |
| Security Specialist     | Security policies and incident response |
| DevOps Specialist       | CI/CD pipelines and infrastructure automation |

Because Go and Lua services often interact with components managed by these other teams — for example, a Go microservice querying a NoSQL database or a Lua script embedded within a networking appliance — the Go and Lua Specialist file includes detailed integration points such as API schemas, serialization formats, and communication protocols. This information enables developers and operators from different teams to establish shared context and reduce integration friction.

**Example:**  
When a Go service invokes a Lua-based plugin for runtime configuration, clear guidelines on data exchange formats (e.g., JSON, Protocol Buffers) and error handling are documented in both the Go and Lua Specialist and the DevOps Specialist files. This ensures consistent deployment practices and observability standards.

---

## 2. Incident Escalation Pathways

Incident escalation is a critical aspect of tech support operations. The Go and Lua Specialist file defines a **tiered escalation matrix**, specifying:

- **Level 1:** On-call developers familiar with basic Go and Lua runtime errors.
- **Level 2:** Specialists responsible for deep dives into Go concurrency issues, Lua VM internals, and performance bottlenecks.
- **Level 3:** Cross-team escalation to Security, Networking, or Database specialists if root causes span multiple domains.

This structured approach is cross-referenced with escalation protocols from the other six specialist files to maintain a unified incident response framework. For example, if a Go service exhibits latency due to database deadlocks, the Go and Lua team collaborates with the Database Specialist team to jointly diagnose and resolve the problem.

The repository includes a **shared incident escalation matrix**, linking contacts, SLAs, and communication channels between teams. This matrix is embedded within the Go and Lua Specialist file, ensuring rapid handoffs and minimizing mean time to resolution (MTTR).

---

## 3. Tech Support Operations and Knowledge Sharing

The Go and Lua Specialist file also acts as a knowledge exchange hub. It references:

- **Shared tooling** maintained by the DevOps Specialist file (e.g., distributed tracing, log aggregation).
- **Security checklists** from the Security Specialist file to ensure Go and Lua applications comply with mandatory policies.
- **Networking diagnostics** procedures for troubleshooting connectivity issues involving Lua scripts in network devices.

Regular sync-ups, documented in the repository’s **collaboration calendar**, facilitate knowledge transfer sessions among specialists. The Go and Lua Specialist file contains templates for **post-incident reviews (PIRs)** that incorporate inputs from all relevant teams, fostering a culture of continuous improvement.

---

# Summary

In production operations, the Go and Lua Specialist file is a cornerstone for:

- Facilitating **cross-team understanding** of polyglot application interactions.
- Providing a **clear escalation framework** aligned with other specialist teams.
- Enabling **cohesive tech support workflows** through shared tools, documentation, and communication standards.

This synergy ensures that complex incidents involving multiple technology domains are resolved swiftly and that production environments remain stable, secure, and performant.


## === FILE: 42-go-lua-troubleshooting.md ===
# Deep Troubleshooting Guide for Go and Lua: Production Operations & Tech Support

## 1. Introduction to Go and Lua Production Troubleshooting

In modern distributed systems, Go (Golang) and Lua (often embedded in Redis or API gateways) form a powerful combination for high-performance, concurrent, and low-latency operations. However, when these systems fail in production, they fail in spectacular and complex ways. Tech support and site reliability engineering (SRE) teams must be equipped to handle worst-case scenarios, such as cascading failures caused by goroutine leaks, deadlocks that freeze entire microservices, silent memory leaks that trigger Out-Of-Memory (OOM) kills, and Redis instances locked in a `BUSY` state due to runaway Lua scripts.

This comprehensive guide is designed for Level 3 (L3) tech support, SREs, and backend engineers. It provides deep, practical, and battle-tested troubleshooting methodologies for the most critical Go and Lua issues encountered in production environments. We will explore the root causes, detection mechanisms, and remediation strategies for goroutine leaks, deadlocks, race conditions, memory leaks, Redis Lua script timeouts, and complex migration failures.

### Relation to Other Specialist Files
*Note: This section explains how this troubleshooting guide integrates with the broader specialist-teams repository.*
- **01-architecture-overview.md**: Provides the high-level system design where Go microservices and Redis/Lua data stores interact.
- **15-incident-response-playbook.md**: Outlines the communication and escalation protocols when the issues described in this guide cause a Sev-1 incident.
- **23-redis-cluster-management.md**: Details the infrastructure side of Redis, complementing the Lua script troubleshooting covered here.
- **34-observability-and-metrics.md**: Defines the Prometheus and Grafana dashboards used to detect the anomalies (e.g., goroutine spikes, memory growth) discussed in this guide.
- **55-post-mortem-templates.md**: Used to document the root cause and remediation after resolving the deep technical issues outlined in this document.
- **67-database-migration-strategies.md**: Expands on the migration failure scenarios, focusing on relational databases, whereas this guide focuses on Go/Lua state migrations.

---

## 2. Goroutine Leaks: Detection and Remediation

Goroutines are lightweight, but they are not free. A goroutine leak occurs when a goroutine is started but never terminates, usually because it is blocked on a channel operation, waiting for a context that never cancels, or caught in an infinite loop. In production, a goroutine leak will eventually consume all available memory or exhaust system resources, leading to an OOM kill or severe performance degradation.

### 2.1. Root Causes of Goroutine Leaks

1.  **Abandoned Channels**: A goroutine is blocked sending to or receiving from an unbuffered channel that no other goroutine will ever read from or write to.
2.  **Missing Context Cancellation**: A goroutine initiates a long-running or blocking operation (like an HTTP request or database query) without a timeout or a cancellation context. If the external service hangs, the goroutine hangs forever.
3.  **Infinite Loops without Exit Conditions**: A background worker loop `for { ... }` lacks a `select` statement to listen for a shutdown signal or context cancellation.
4.  **Unclosed Response Bodies**: Failing to close `http.Response.Body` can keep the underlying connection and associated goroutines alive.

### 2.2. Detecting Goroutine Leaks in Production

When troubleshooting a suspected goroutine leak, the first indicator is usually a steady, linear increase in memory usage and the number of active goroutines on your Grafana dashboards.

**Step 1: Check Goroutine Count Metrics**
Query your Prometheus metrics for `go_goroutines`. If the graph shows a "staircase" pattern or a continuous upward trend without dropping during off-peak hours, you have a leak.

**Step 2: Capture a Goroutine Profile via pprof**
Go's `net/http/pprof` package is essential for production debugging. If pprof is exposed (e.g., on an internal admin port), capture the goroutine profile:

```bash
curl -s http://localhost:6060/debug/pprof/goroutine?debug=1 > goroutines_summary.txt
curl -s http://localhost:6060/debug/pprof/goroutine?debug=2 > goroutines_full.txt
```

The `debug=1` output provides a summary of goroutines grouped by their current execution point. Look for unusually high counts:

```text
goroutine profile: total 10543
10000 @ 0x435f0e 0x436433 0x46b895 0x4d5e21 0x4d69a5 0x4d698d
#	0x4d5e20	github.com/company/service/worker.processTask+0x120	/app/worker/worker.go:45
#	0x4d69a4	github.com/company/service/worker.Start.func1+0x44	/app/worker/worker.go:22
```

In this example, 10,000 goroutines are stuck at `worker.go:45`.

**Step 3: Analyze the Full Dump**
The `debug=2` output provides the exact stack trace and state of every single goroutine. Search for the function identified in Step 2. You will likely see states like `semacquire` (waiting on a mutex/channel) or `IO wait`.

### 2.3. Remediation and Worst-Case Scenarios

**Immediate Mitigation:**
If the service is critical and failing, the only immediate mitigation is a rolling restart of the affected pods/instances to clear the leaked goroutines. However, you must capture the pprof dump *before* restarting.

**Code-Level Fixes:**
-   **Implement Contexts:** Ensure every blocking operation uses `context.WithTimeout` or `context.WithCancel`.
-   **Audit Channel Operations:** Verify that every channel send/receive has a corresponding receiver/sender, or use `select` with a `default` or timeout case.

```go
// BAD: Can block forever if the channel is unbuffered and no one is reading
func sendResult(ch chan<- Result, res Result) {
    ch <- res
}

// GOOD: Uses a select with a context to prevent leaking
func sendResultSafe(ctx context.Context, ch chan<- Result, res Result) {
    select {
    case ch <- res:
        // Successfully sent
    case <-ctx.Done():
        // Context cancelled, exit to prevent leak
        log.Printf("Failed to send result: %v", ctx.Err())
    }
}
```

---

## 3. Deadlocks and Race Conditions in Go

Concurrency is Go's strongest feature, but improper synchronization leads to deadlocks (where the application freezes) and race conditions (where data becomes corrupted unpredictably).

### 3.1. Diagnosing Deadlocks

A deadlock occurs when two or more goroutines are waiting for each other to release resources, resulting in a complete standstill. In Go, a global deadlock (where *all* goroutines are asleep) will cause the runtime to panic and crash the program. However, a *partial deadlock* (where only some goroutines are stuck) will not crash the program but will degrade functionality.

**Symptoms of a Partial Deadlock:**
-   API endpoints suddenly stop responding and time out.
-   CPU usage drops to near zero, but memory remains allocated.
-   The number of active goroutines spikes and stays flat.

**Troubleshooting Steps:**
1.  **Trigger a Core Dump or Stack Trace:** If the application is unresponsive, send a `SIGQUIT` signal to the Go process. This forces the Go runtime to print the stack traces of all currently running goroutines to standard error and then exit.
    ```bash
    kill -SIGQUIT <pid>
    ```
2.  **Analyze the Stack Trace:** Look for goroutines in the `sync.Mutex.Lock` state.
    ```text
    goroutine 45 [semacquire]:
    sync.runtime_SemacquireMutex(0xc0000b4014, 0x0, 0x1)
        /usr/local/go/src/runtime/sema.go:71 +0x47
    sync.(*Mutex).lockSlow(0xc0000b4010)
        /usr/local/go/src/sync/mutex.go:138 +0x105
    sync.(*Mutex).Lock(...)
        /usr/local/go/src/sync/mutex.go:81
    main.updateCache()
        /app/main.go:120 +0x45
    ```
3.  **Identify the Lock Ordering:** Deadlocks almost always occur due to inconsistent lock ordering (e.g., Goroutine A locks Mutex 1 then Mutex 2; Goroutine B locks Mutex 2 then Mutex 1). Trace the code to ensure locks are always acquired in the exact same order globally.

### 3.2. Hunting Down Race Conditions

Race conditions are insidious because they do not always cause immediate crashes. They cause silent data corruption, inconsistent API responses, and bizarre logic failures.

**The Go Race Detector:**
The absolute best tool for finding race conditions is the built-in Go race detector. However, it introduces significant overhead (up to 10x CPU and memory usage), so it should **never** be run in production.

**Troubleshooting Workflow:**
1.  **Replicate in Staging:** Deploy a build of the application compiled with the `-race` flag to a staging environment that mirrors production traffic.
    ```bash
    go build -race -o myapp main.go
    ```
2.  **Monitor Logs:** When a race condition occurs, the runtime will print a detailed warning to stderr, showing the exact goroutines and memory addresses involved.
    ```text
    WARNING: DATA RACE
    Write at 0x00c0000b2040 by goroutine 7:
      main.incrementCounter()
          /app/main.go:45 +0x3a

    Previous read at 0x00c0000b2040 by goroutine 6:
      main.readCounter()
          /app/main.go:50 +0x2b
    ```
3.  **Fixing the Race:** Protect the shared resource using `sync.Mutex`, `sync.RWMutex`, or atomic operations (`sync/atomic`). Alternatively, refactor the code to use channels to pass data ownership rather than sharing memory.

---

## 4. Go Memory Leaks and Profiling

Unlike C/C++, Go is garbage-collected, meaning memory leaks are rarely caused by forgetting to free memory. Instead, Go memory leaks are usually "logical leaks"—holding onto references of objects that are no longer needed, preventing the garbage collector (GC) from reclaiming them.

### 4.1. Common Causes of Logical Memory Leaks

1.  **Global Maps and Slices:** Appending data to a global slice or map without ever deleting old entries. This is common in poorly implemented in-memory caches.
2.  **Substring and Subslice References:** Slicing a large array or string keeps the *entire* underlying array in memory. If you read a 10MB file into a string and keep only a 10-byte substring, the full 10MB remains in memory.
3.  **Time Tickers:** Creating a `time.Ticker` in a loop or function and failing to call `ticker.Stop()`. The runtime keeps the ticker alive.

### 4.2. Deep Profiling with pprof

When an OOM kill occurs, you must analyze the heap profile.

**Step 1: Capture the Heap Profile**
```bash
curl -s http://localhost:6060/debug/pprof/heap > heap.out
```

**Step 2: Analyze with `go tool pprof`**
```bash
go tool pprof heap.out
```

Inside the interactive pprof shell, use the following commands:
-   `top`: Shows the functions consuming the most memory.
-   `top -cum`: Shows the functions allocating the most memory (including their children).
-   `list <function_name>`: Shows the exact lines of code in a function where allocations occur.
-   `web`: Generates an SVG call graph and opens it in a browser (highly recommended for visual tracing).

**Step 3: Differentiate `inuse_space` vs `alloc_space`**
-   `inuse_space` (default): Shows memory currently allocated and not yet garbage collected. High `inuse_space` indicates a leak.
-   `alloc_space`: Shows all memory allocated since the program started, even if it was garbage collected. High `alloc_space` indicates high allocation churn, which causes high CPU usage due to GC pressure, but not necessarily a leak.

### 4.3. Fixing Subslice Leaks

If pprof shows high memory usage on a line that simply slices a byte array, you have a subslice leak.

```go
// BAD: Keeps the entire 10MB payload in memory
func extractHeader(payload []byte) []byte {
    return payload[0:100] 
}

// GOOD: Allocates a new, small slice and copies the data, allowing the large payload to be GC'd
func extractHeaderSafe(payload []byte) []byte {
    header := make([]byte, 100)
    copy(header, payload[0:100])
    return header
}
```

---

## 5. Redis Lua Script Timeouts (The BUSY State)

Redis is single-threaded. When a Lua script executes via `EVAL` or `EVALSHA`, it blocks all other Redis commands until it completes. This guarantees atomicity, but it also means a poorly written Lua script can take down your entire Redis cluster.

### 5.1. The `BUSY` State Explained

By default, Redis has a `lua-time-limit` configuration (usually 5000 milliseconds). If a Lua script runs longer than this limit, Redis does *not* automatically kill it. Instead, Redis enters a `BUSY` state.

In the `BUSY` state:
-   Redis stops processing normal commands.
-   Clients receive the error: `BUSY Redis is busy running a script. You can only call SCRIPT KILL or SHUTDOWN NOSAVE.`
-   Your Go microservices will start throwing connection timeouts, leading to cascading failures across the system.

### 5.2. Root Causes of Slow Lua Scripts

1.  **Infinite Loops:** A `while` or `repeat` loop in Lua that fails to meet its exit condition.
2.  **Massive Iterations:** Iterating over a massive Redis Set or Hash (e.g., using `SMEMBERS` or `HGETALL` on a key with millions of elements) inside the script.
3.  **Complex Logic:** Performing heavy computational tasks (like complex JSON parsing or cryptography) inside Lua instead of in the Go application layer.

### 5.3. Incident Response: Recovering from a BUSY State

When PagerDuty alerts you that Redis is `BUSY`, you must act immediately.

**Step 1: Attempt `SCRIPT KILL`**
Connect to the Redis instance via `redis-cli` and execute:
```bash
redis-cli SCRIPT KILL
```
*Note:* `SCRIPT KILL` only works if the Lua script has *not* yet performed any write operations (e.g., `SET`, `DEL`). If it has only performed reads, Redis will kill the script and resume normal operations.

**Step 2: The Worst-Case Scenario (`SHUTDOWN NOSAVE`)**
If the script has already performed a write operation, Redis refuses to kill it to prevent data inconsistency. `SCRIPT KILL` will return an error.

In this catastrophic scenario, your only option is to forcefully terminate the Redis instance:
```bash
redis-cli SHUTDOWN NOSAVE
```
This will kill the Redis process without saving the dataset to disk. You will lose any data written since the last RDB snapshot or AOF rewrite. The Redis instance will then be restarted by your orchestrator (e.g., Kubernetes or systemd), and it will load the last valid state from disk.

### 5.4. Prevention and Best Practices

To prevent Lua script timeouts:
-   **Never use `KEYS *`, `SMEMBERS`, or `HGETALL` on large datasets inside Lua.** Use `SSCAN` or `HSCAN` instead, or process the data in Go.
-   **Keep scripts small and fast.** Lua in Redis is for atomicity, not heavy computation.
-   **Test with production-sized data.** A script that runs in 1ms on a developer's machine might take 10 seconds on a production dataset.
-   **Use `EVALSHA` instead of `EVAL`.** Loading the script once and calling it by its SHA1 hash saves bandwidth and parsing time.

---

## 6. Migration Failures and Lua/Go Integration

Migrating data structures or logic that relies heavily on the Go/Lua boundary is fraught with peril. A common scenario is migrating from a legacy Go-based locking mechanism to a Redis Lua-based distributed lock, or changing the schema of data manipulated by Lua scripts.

### 6.1. The "Split-Brain" Migration Failure

When migrating logic, you often have a period where both the old Go logic and the new Lua logic are running simultaneously (e.g., during a canary deployment). If the two systems do not perfectly agree on the state of the data, you get a split-brain scenario.

**Example Scenario:**
You are migrating a rate-limiter. The old version uses Go's in-memory counters. The new version uses a Redis Lua script. During the rollout, some pods use the old logic, some use the new. A user's requests are routed to both, effectively doubling their allowed rate limit because the state is split between Go memory and Redis.

**Troubleshooting and Resolution:**
1.  **Halt the Rollout:** Immediately pause the deployment. Do not roll back yet, as rolling back might cause further state corruption depending on the migration design.
2.  **Analyze the State:** Inspect the Redis keys created by the Lua script and compare them to the logs/metrics of the Go in-memory state.
3.  **Force a Single Source of Truth:** The remediation requires forcing all traffic to use a single source of truth. If the Redis state is corrupted, you may need to flush the specific rate-limit keys and fail back to the Go implementation entirely until the bug is fixed.

### 6.2. Lua Script Versioning and Cache Poisoning

When you update a Lua script in your Go code, you change its SHA1 hash.

**The Failure Mode:**
1.  Go Service v1 uses Lua Script A (Hash A).
2.  You deploy Go Service v2, which uses Lua Script B (Hash B).
3.  During the rolling update, both v1 and v2 are running.
4.  If Script B modifies a Redis key in a way that Script A cannot understand (e.g., changing a value from an integer to a JSON string), Service v1 will start throwing errors when it tries to read that key. This is a form of cache poisoning.

**Troubleshooting:**
The logs will show Go services failing to unmarshal or parse Redis responses.
```text
ERR Error running script (call to f_8a7b...): @user_script:1: WRONGTYPE Operation against a key holding the wrong kind of value
```

**Safe Migration Strategy:**
To prevent this, Lua script migrations must be backward compatible.
-   **Phase 1:** Deploy Go Service v2. Script B writes to the *new* format but can read *both* the old and new formats. Script A continues to write and read the old format.
-   **Phase 2:** Once v1 is fully deprecated, deploy Go Service v3. Script C only reads and writes the new format.
-   **Phase 3:** Run a background Go worker to clean up any lingering old-format data.

### 6.3. Handling Network Partitions During Migrations

If a network partition occurs between your Go microservices and Redis during a critical Lua script execution, the Go context will time out, but the Lua script might still execute successfully on the Redis server.

**The Problem:**
The Go application thinks the operation failed and might retry it. If the Lua script is not idempotent, the retry will cause data duplication or corruption (e.g., charging a customer twice).

**The Solution:**
Every Lua script executed from Go **must be idempotent**.
Pass a unique transaction ID (UUID) from Go to the Lua script. The Lua script should check if this transaction ID has already been processed (e.g., by storing it in a Redis Set with an expiration).

```lua
-- Idempotent Lua Script Example
local tx_id = ARGV[1]
local key = KEYS[1]

-- Check if already processed
if redis.call("SISMEMBER", "processed_txs", tx_id) == 1 then
    return "ALREADY_PROCESSED"
end

-- Perform the actual operation
redis.call("INCR", key)

-- Mark as processed
redis.call("SADD", "processed_txs", tx_id)
redis.call("EXPIRE", "processed_txs", 3600)

return "SUCCESS"
```

---

## 7. Advanced Debugging Techniques

### 7.1. Using `strace` on Go Processes

When pprof isn't enough (e.g., the process is completely locked up and the HTTP server serving pprof is dead), you can use `strace` to see what the Go runtime is doing at the OS level.

```bash
strace -p <pid> -c
```
This provides a summary of system calls. If you see a massive number of `futex` calls, the application is heavily contending on locks (mutexes). If you see `epoll_wait` dominating, the application is mostly idle, waiting for network I/O.

### 7.2. Redis `MONITOR` and `SLOWLOG`

To debug Lua scripts interacting with Redis, use `SLOWLOG`.

```bash
redis-cli SLOWLOG GET 10
```
This shows the 10 slowest queries. It will reveal exactly which `EVALSHA` commands are taking too long, along with their arguments.

**Warning:** Never use the `MONITOR` command in a high-throughput production environment. It streams every single command processed by Redis to the client, which can reduce Redis throughput by over 50% and cause the very outages you are trying to prevent.

## 8. Conclusion

Troubleshooting Go and Lua in production requires a deep understanding of concurrency, memory management, and distributed state. By mastering pprof for goroutine and memory analysis, understanding the catastrophic implications of the Redis `BUSY` state, and designing idempotent, backward-compatible Lua scripts, SREs and tech support teams can rapidly mitigate Sev-1 incidents and build highly resilient systems. Always prioritize observability—you cannot fix what you cannot see.

