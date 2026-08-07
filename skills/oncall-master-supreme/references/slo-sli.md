# SLO/SLI Tracking and Reporting Metrics

Verified against upstream: 2026-08-07

## Overview

Service Level Objectives (SLOs) and Service Level Indicators (SLIs) provide a quantitative measure of system reliability and user experience.

## Definitions

-   **SLI (Service Level Indicator):** A quantitative measure of some aspect of the level of service that is provided (e.g., error rate, latency).
-   **SLO (Service Level Objective):** A target value or range of values for a service level that is measured by an SLI (e.g., 99.9% availability).
-   **Error Budget:** The acceptable amount of unreliability allowed by an SLO before consequences are triggered (e.g., halting feature releases).

## Implementation Steps

1.  **Identify Critical User Journeys:** Determine the most important interactions users have with the system.
2.  **Define SLIs:** Select appropriate metrics to measure the success of those journeys.
3.  **Set SLOs:** Establish realistic targets based on business requirements and historical performance.
4.  **Monitor and Alert:** Configure monitoring tools to track SLIs and alert when error budgets are at risk.

## References

-   [Google SRE Book: Service Level Objectives](https://sre.google/sre-book/service-level-objectives/)
-   [Datadog SLO Tracking](https://docs.datadoghq.com/service_management/service_level_objectives/)
