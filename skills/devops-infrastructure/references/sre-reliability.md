# Site Reliability Engineering

## Table of Contents
1. SLO Framework
2. Incident Management
3. Capacity Planning
4. Observability
5. Chaos Engineering
6. On-Call and Runbooks

---

## 1. SLO Framework

### SLI/SLO/SLA Hierarchy

| Concept | Definition | Owner |
|---|---|---|
| SLI (Indicator) | Quantitative measure of service level | Engineering |
| SLO (Objective) | Target value for an SLI | Engineering + Product |
| SLA (Agreement) | Contract with consequences | Business + Legal |
| Error Budget | Allowed unreliability (1 - SLO) | Engineering |

### Common SLIs

| Category | SLI | Measurement |
|---|---|---|
| Availability | Successful requests / total requests | 5xx errors excluded |
| Latency | Proportion of requests faster than threshold | p50, p95, p99 |
| Throughput | Requests processed per second | Under normal load |
| Correctness | Proportion of correct responses | Validation checks |
| Freshness | Proportion of data updated within threshold | Data pipeline lag |

### Error Budget Policy

```
Error Budget = 1 - SLO

Example: 99.9% availability SLO
- Error budget: 0.1% = 43.8 minutes/month
- If budget exhausted: freeze feature releases, focus on reliability
- If budget healthy: ship features faster, take more risks
```

**Error Budget Actions**:
- >50% remaining: Normal development velocity
- 25-50% remaining: Increase review rigor, add reliability work
- <25% remaining: Prioritize reliability over features
- Exhausted: Feature freeze until budget replenishes

---

## 2. Incident Management

### Incident Severity Levels

| Severity | Impact | Response Time | Example |
|---|---|---|---|
| SEV1 (Critical) | Complete outage, data loss | <5 min | Service down, data corruption |
| SEV2 (Major) | Significant degradation | <15 min | Partial outage, slow responses |
| SEV3 (Minor) | Limited impact | <1 hour | Single feature broken |
| SEV4 (Low) | Minimal impact | Next business day | Cosmetic issue |

### Incident Response Process

1. **Detect**: Automated alerting or user report
2. **Triage**: Assess severity, assign incident commander
3. **Communicate**: Status page update, stakeholder notification
4. **Mitigate**: Restore service (rollback, failover, scale)
5. **Resolve**: Fix root cause
6. **Post-mortem**: Blameless review, action items

### Post-Mortem Template

```markdown
# Incident Post-Mortem: [Title]
Date: [Date] | Duration: [Duration] | Severity: [SEV]

## Summary
One-paragraph description of what happened and impact.

## Timeline (UTC)
- HH:MM - First alert fired
- HH:MM - Incident declared, IC assigned
- HH:MM - Root cause identified
- HH:MM - Mitigation applied
- HH:MM - Service restored

## Root Cause
Technical explanation of what went wrong.

## Impact
- Users affected: X
- Revenue impact: $Y
- Error budget consumed: Z%

## Action Items
| Action | Owner | Priority | Due Date |
|---|---|---|---|
| Add monitoring for X | @engineer | P1 | [date] |
| Implement circuit breaker | @team | P2 | [date] |

## Lessons Learned
What went well, what didn't, where we got lucky.
```

---

## 3. Capacity Planning

### Capacity Planning Process

1. **Measure current usage**: CPU, memory, storage, network, connections
2. **Identify growth drivers**: User growth, feature launches, seasonal patterns
3. **Model future demand**: Linear projection, seasonal adjustment, event-based
4. **Determine headroom**: Typically 30-50% above peak for safety
5. **Plan provisioning**: Lead time for procurement or scaling
6. **Review regularly**: Monthly capacity reviews

### Key Capacity Metrics

| Resource | Metric | Warning Threshold | Critical Threshold |
|---|---|---|---|
| CPU | Utilization | 70% sustained | 85% sustained |
| Memory | Usage | 80% | 90% |
| Disk | Usage | 75% | 85% |
| Network | Bandwidth utilization | 60% | 80% |
| Connections | Pool utilization | 70% | 85% |
| Queue depth | Messages pending | Growing trend | Unbounded growth |

---

## 4. Observability

### Observability Stack

| Layer | Tool | Purpose |
|---|---|---|
| Metrics | Prometheus + Grafana | Time-series metrics, dashboards |
| Logs | Loki / ELK / Datadog | Log aggregation, search |
| Traces | Jaeger / Tempo / Datadog | Distributed tracing |
| Profiling | Pyroscope / Parca | Continuous profiling |
| Alerting | Alertmanager / PagerDuty | Alert routing, escalation |
| Status | Statuspage / Instatus | External status communication |

### Alerting Best Practices

- Alert on symptoms (user impact), not causes
- Every alert must be actionable (linked to a runbook)
- Use multi-window, multi-burn-rate alerts for SLOs
- Implement alert routing by severity and team
- Avoid alert fatigue: review and prune regularly
- Use pages for urgent issues, tickets for non-urgent
- Implement escalation policies (if not acked in X min, escalate)

### Dashboard Design

| Dashboard Type | Audience | Content |
|---|---|---|
| Service overview | On-call engineer | RED metrics, SLO status, recent deploys |
| Infrastructure | Platform team | Node health, resource usage, capacity |
| Business | Stakeholders | Revenue, user activity, conversion |
| Incident | Incident commander | Real-time system status, error rates |

---

## 5. Chaos Engineering

### Chaos Engineering Principles

1. Build a hypothesis about steady-state behavior
2. Vary real-world events (server failure, network partition, disk full)
3. Run experiments in production (start small)
4. Automate experiments to run continuously
5. Minimize blast radius (start with small scope)

### Chaos Experiments

| Experiment | Tests | Tools |
|---|---|---|
| Pod kill | Self-healing, replicas | Chaos Monkey, Litmus |
| Network latency | Timeout handling, retries | tc, Chaos Mesh |
| Network partition | Split-brain handling | iptables, Chaos Mesh |
| CPU stress | Autoscaling, degradation | stress-ng, Litmus |
| Disk full | Alerting, cleanup | dd, fallocate |
| DNS failure | Fallback, caching | Chaos Mesh |
| Dependency failure | Circuit breakers, fallbacks | Toxiproxy |

---

## 6. On-Call and Runbooks

### On-Call Best Practices

- Limit on-call rotation to 1 week maximum
- Ensure adequate rest between on-call shifts
- Compensate on-call fairly (time off or pay)
- Provide clear escalation paths
- Review on-call load monthly (reduce pages)
- Shadow new on-call engineers before solo shifts
- Maintain up-to-date runbooks for all alerts

### Runbook Template

```markdown
# Runbook: [Alert Name]

## Alert Description
What this alert means and why it fires.

## Impact
What users/services are affected.

## Investigation Steps
1. Check [dashboard URL] for current state
2. Run `kubectl get pods -n <namespace>` to check pod health
3. Check logs: `kubectl logs -l app=<service> --tail=100`
4. Verify database connectivity: [command]

## Mitigation Steps
1. If caused by traffic spike: Scale up deployment
2. If caused by bad deploy: Rollback with `helm rollback`
3. If caused by dependency: Check dependency status page

## Escalation
- If not resolved in 15 min: Page [team]
- If data loss suspected: Page [database team]

## Related Resources
- Service documentation: [link]
- Architecture diagram: [link]
- Previous incidents: [link]
```
