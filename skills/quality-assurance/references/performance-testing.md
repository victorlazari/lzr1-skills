# Performance Testing

## Table of Contents
1. Performance Test Types
2. Load Testing
3. Performance Metrics
4. Tools and Frameworks
5. Performance Optimization

---

## 1. Performance Test Types

| Type | Purpose | Approach |
|---|---|---|
| Load test | Verify under expected load | Simulate normal traffic |
| Stress test | Find breaking point | Increase load until failure |
| Spike test | Handle sudden traffic spikes | Sudden large increase |
| Soak/Endurance test | Stability over time | Sustained load for hours |
| Scalability test | How well system scales | Gradually increase load |
| Capacity test | Maximum capacity | Find upper limits |
| Baseline test | Establish performance baseline | Single user, measure response |

---

## 2. Load Testing

### Load Test Design

```
Scenario: E-commerce checkout flow
Users: 1,000 concurrent (peak)
Duration: 30 minutes sustained
Ramp-up: 5 minutes (0 → 1,000 users)
Think time: 3-5 seconds between actions

User journey:
1. Browse catalog (40% of users)
2. Search products (30% of users)
3. Add to cart (20% of users)
4. Checkout (10% of users)
```

### Load Profile Patterns

| Pattern | Description | Use Case |
|---|---|---|
| Constant | Fixed number of users | Baseline measurement |
| Ramp-up | Gradually increase users | Find breaking point |
| Step | Increase in steps, hold each | Identify thresholds |
| Spike | Sudden burst of users | Flash sale, viral event |
| Wave | Oscillating load | Simulate daily patterns |

### k6 Example

```javascript
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '2m', target: 100 },  // Ramp up
    { duration: '5m', target: 100 },  // Sustain
    { duration: '2m', target: 200 },  // Ramp up more
    { duration: '5m', target: 200 },  // Sustain
    { duration: '2m', target: 0 },    // Ramp down
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'],  // 95% under 500ms
    http_req_failed: ['rate<0.01'],    // <1% error rate
  },
};

export default function () {
  const res = http.get('https://api.example.com/products');
  check(res, {
    'status is 200': (r) => r.status === 200,
    'response time < 500ms': (r) => r.timings.duration < 500,
  });
  sleep(1);
}
```

---

## 3. Performance Metrics

### Key Metrics

| Metric | Description | Target (typical) |
|---|---|---|
| Response time (p50) | Median response time | <200ms |
| Response time (p95) | 95th percentile | <500ms |
| Response time (p99) | 99th percentile | <1000ms |
| Throughput | Requests per second | Depends on capacity |
| Error rate | % of failed requests | <1% |
| Concurrent users | Simultaneous active users | Depends on target |
| CPU utilization | Server CPU usage | <70% at peak |
| Memory utilization | Server memory usage | <80% at peak |
| Network I/O | Bandwidth consumption | Within limits |
| Database queries | Query time, connection pool | <50ms avg |

### Performance Budget

| Resource | Budget | Measurement |
|---|---|---|
| Page load (LCP) | <2.5 seconds | Largest Contentful Paint |
| Interactivity (INP) | <200ms | Interaction to Next Paint |
| Layout stability (CLS) | <0.1 | Cumulative Layout Shift |
| Time to First Byte | <600ms | Server response time |
| JavaScript bundle | <200KB (compressed) | Transfer size |
| Total page weight | <1MB | All resources |
| API response | <200ms (p95) | Backend latency |

---

## 4. Tools and Frameworks

### Performance Testing Tools

| Tool | Type | Language | Best For |
|---|---|---|---|
| k6 | Load testing | JavaScript | Modern, developer-friendly |
| JMeter | Load testing | Java/GUI | Enterprise, complex scenarios |
| Gatling | Load testing | Scala/Java | High performance, CI/CD |
| Locust | Load testing | Python | Python teams, distributed |
| Artillery | Load testing | JavaScript | Quick setup, YAML config |
| Lighthouse | Frontend perf | CLI/Chrome | Web vitals, audits |
| WebPageTest | Frontend perf | Web-based | Detailed waterfall analysis |
| Grafana + k6 | Monitoring | Dashboard | Real-time visualization |

### Monitoring Stack

```
Load Generator (k6/JMeter)
       ↓
Application Under Test
       ↓
Metrics Collection (Prometheus/DataDog)
       ↓
Visualization (Grafana)
       ↓
Alerting (PagerDuty/OpsGenie)
```

---

## 5. Performance Optimization

### Common Bottlenecks

| Layer | Bottleneck | Solution |
|---|---|---|
| Frontend | Large bundles | Code splitting, tree shaking |
| Frontend | Unoptimized images | WebP, lazy loading, CDN |
| Frontend | Render blocking | Async scripts, critical CSS |
| Network | High latency | CDN, edge caching |
| API | Slow queries | Query optimization, indexing |
| API | No caching | Redis, HTTP caching headers |
| API | Synchronous processing | Async queues, background jobs |
| Database | Missing indexes | Index analysis, query plans |
| Database | Connection exhaustion | Connection pooling |
| Infrastructure | Under-provisioned | Auto-scaling, right-sizing |

### Caching Strategy

| Layer | Cache Type | TTL | Use Case |
|---|---|---|---|
| Browser | HTTP cache headers | Minutes-hours | Static assets |
| CDN | Edge cache | Minutes-hours | Public content |
| Application | In-memory (Redis) | Seconds-minutes | API responses |
| Database | Query cache | Seconds | Frequent queries |
| DNS | DNS cache | Hours | Domain resolution |
