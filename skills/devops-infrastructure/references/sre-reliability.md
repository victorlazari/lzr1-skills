# SRE & Reliability

**Verified against upstream: 2026-08-07**

## Table of Contents
1. Service Level Objectives (SLOs)
2. Incident Management
3. Capacity Planning
4. Observability

---

## 1. Service Level Objectives (SLOs)

- **SLI (Service Level Indicator)**: A carefully defined quantitative measure of some aspect of the level of service that is provided.
- **SLO (Service Level Objective)**: A target value or range of values for a service level that is measured by an SLI.
- **SLA (Service Level Agreement)**: An explicit or implicit contract with your users that includes consequences of meeting (or missing) the SLOs they contain.
- **Error Budget**: 100% - SLO. The acceptable level of unreliability.

## 2. Incident Management

- Define severity levels (SEV-1 to SEV-5).
- Establish incident roles (Incident Commander, Operations Lead, Communications Lead).
- Blameless post-mortems.

## 3. Capacity Planning

- Load testing, stress testing.
- Auto-scaling strategies.

## 4. Observability

- Metrics, Logs, Traces (The Three Pillars).
- RED Method (Rate, Errors, Duration).
- USE Method (Utilization, Saturation, Errors).
