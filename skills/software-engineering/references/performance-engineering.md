# Performance Engineering

## Table of Contents
1. Performance Analysis Methodology
2. Profiling
3. Load Testing
4. Optimization Techniques
5. Benchmarking

---

## 1. Performance Analysis Methodology

### USE Method (Brendan Gregg)

For every resource (CPU, memory, disk, network), check:
- **U**tilization: Percentage of time the resource is busy
- **S**aturation: Degree of queued work (waiting)
- **E**rrors: Count of error events

### RED Method (Tom Wilkie)

For every service, monitor:
- **R**ate: Requests per second
- **E**rrors: Number of failed requests
- **D**uration: Distribution of request latency

### Performance Analysis Workflow

1. **Define the problem**: What is slow? What is the target?
2. **Measure baseline**: Establish current performance metrics
3. **Identify bottleneck**: Profile to find the constraint
4. **Hypothesize**: Form theory about the cause
5. **Test**: Apply fix and measure improvement
6. **Validate**: Confirm fix doesn't introduce regressions
7. **Document**: Record findings and optimization applied

---

## 2. Profiling

### CPU Profiling

| Tool | Language | Type |
|---|---|---|
| pprof | Go | CPU, memory, goroutine |
| py-spy | Python | Sampling profiler (low overhead) |
| perf | Linux (any) | System-wide profiling |
| async-profiler | Java/JVM | CPU, allocation, lock |
| flamegraph | Any | Visualization of stack traces |
| Chrome DevTools | JavaScript | CPU, memory, network |

### Memory Profiling

- **Heap profiling**: Track allocations, find memory leaks
- **Allocation profiling**: Identify hot allocation paths
- **GC analysis**: Monitor garbage collection pauses and frequency
- **Memory leak detection**: Growing memory over time without release

### Profiling Best Practices

- Profile in production-like environments (not development)
- Use sampling profilers for low overhead (<5%)
- Profile under realistic load (not idle or synthetic)
- Compare profiles before and after changes
- Focus on the top contributors (Pareto principle: 80/20)
- Profile regularly, not just when problems occur

---

## 3. Load Testing

### Load Testing Types

| Type | Purpose | Pattern |
|---|---|---|
| Smoke test | Verify system works under minimal load | 1-5 users, short duration |
| Load test | Verify performance under expected load | Normal traffic, 30-60 min |
| Stress test | Find breaking point | Gradually increase until failure |
| Spike test | Handle sudden traffic bursts | Sudden 10x increase |
| Soak test | Find memory leaks, resource exhaustion | Normal load, 4-24 hours |
| Breakpoint test | Find maximum capacity | Increase until SLO breach |

### Load Testing Tools

| Tool | Language | Strengths |
|---|---|---|
| k6 | JavaScript | Modern, scriptable, cloud option |
| Locust | Python | Distributed, code-based |
| Gatling | Scala | High performance, detailed reports |
| Artillery | JavaScript/YAML | Easy setup, serverless |
| wrk/wrk2 | C | Raw HTTP performance |
| hey | Go | Simple HTTP benchmarking |

### Load Test Design

```javascript
// k6 example: realistic load test
export const options = {
  stages: [
    { duration: '2m', target: 100 },   // Ramp up
    { duration: '5m', target: 100 },   // Steady state
    { duration: '2m', target: 200 },   // Peak load
    { duration: '5m', target: 200 },   // Sustained peak
    { duration: '2m', target: 0 },     // Ramp down
  ],
  thresholds: {
    http_req_duration: ['p(95)<500', 'p(99)<1000'],
    http_req_failed: ['rate<0.01'],
  },
};
```

---

## 4. Optimization Techniques

### Application-Level

| Technique | Impact | Complexity |
|---|---|---|
| Caching (Redis, CDN) | Very high | Low-Medium |
| Database query optimization | High | Medium |
| Connection pooling | High | Low |
| Async/non-blocking I/O | High | Medium |
| Batch processing | Medium | Low |
| Compression (gzip, brotli) | Medium | Low |
| Code-level optimization | Variable | High |

### Database Optimization

- Add missing indexes (based on EXPLAIN analysis)
- Optimize slow queries (rewrite, denormalize)
- Implement connection pooling (PgBouncer, HikariCP)
- Use read replicas for read-heavy workloads
- Implement query result caching
- Partition large tables
- Vacuum and analyze regularly (PostgreSQL)

### Network Optimization

- **HTTP/2 or HTTP/3**: Multiplexing, header compression
- **CDN**: Cache static assets close to users
- **Compression**: Brotli for text, WebP/AVIF for images
- **Connection reuse**: Keep-alive, connection pooling
- **DNS prefetching**: Resolve domains before navigation
- **Edge computing**: Process requests at the edge

### Memory Optimization

- Reduce object allocations (reuse buffers, pool objects)
- Use appropriate data structures (arrays vs linked lists)
- Implement pagination/streaming for large datasets
- Avoid loading entire files into memory
- Monitor and tune GC settings (JVM, Go, .NET)
- Use memory-mapped files for large read-only data

---

## 5. Benchmarking

### Microbenchmarking Rules

- Warm up the JIT/runtime before measuring
- Run enough iterations for statistical significance
- Measure variance, not just mean (report p50, p95, p99)
- Isolate the code under test (no I/O, no network)
- Beware of dead code elimination by optimizing compilers
- Compare against a baseline, not absolute numbers
- Use proper benchmarking frameworks (BenchmarkDotNet, JMH, Go testing.B)

### System Benchmarking

| What | Tool | Metric |
|---|---|---|
| Disk I/O | fio | IOPS, throughput, latency |
| Network | iperf3 | Bandwidth, jitter |
| CPU | sysbench | Operations/second |
| Memory | stream | Bandwidth |
| Database | pgbench, sysbench | TPS, latency |
| HTTP | wrk2, hey | RPS, latency distribution |

### Performance Regression Detection

- Run benchmarks in CI/CD pipeline
- Compare against baseline (previous release)
- Alert on >5% regression in critical paths
- Use statistical tests (not just threshold comparison)
- Track performance trends over time
- Maintain a performance budget for critical paths
