# SLA Configuration Guide

**Verified against upstream:** 2026-08-07

## Overview

Service Level Agreements (SLAs) are foundational to measuring service quality in Jira Service Management. Advanced SLA configurations enable organizations to tailor measurement criteria precisely, reflecting real-world operational constraints such as business hours, calendar hours, holidays, and multi-tiered escalation policies.

## Business Hours vs Calendar Hours

One of the most significant complexities in SLA configuration is differentiating between **business hours** and **calendar hours**. This distinction impacts how SLA timers count elapsed time toward resolution or response targets.

- **Calendar Hours:** SLA clocks run continuously, including nights, weekends, and holidays. This mode is simpler but may not reflect realistic expectations where support teams operate only during defined work periods.
- **Business Hours:** SLA clocks pause outside defined business hours, such as evenings, weekends, and public holidays. This requires configuring custom calendars that specify working days and hours per service or team.

For example, a support team operating Monday to Friday, 9 AM to 5 PM, with holidays excluded, would define a business calendar reflecting these constraints. The SLA timer would then only count elapsed time within those periods.

Jira Service Management supports multiple business calendars, each of which can be assigned to specific SLA metrics. This allows differentiated SLAs for various service lines or customer segments.

## Multi-tiered SLA Policies

Advanced SLA setups often involve multiple SLA metrics that track different aspects of incident management, such as:

- **Time to first response:** Measures the initial acknowledgement time.
- **Time to resolution:** Measures the total time to resolve the incident.
- **Time to restore service:** Tracks the actual time until the affected service is restored.

Each SLA metric can have unique goals depending on priority levels and impacted services. For instance, a critical incident might require a 15-minute response and a 2-hour resolution, while a low-priority ticket might have a 4-hour response goal and a 48-hour resolution target.

These SLA metrics can be nested or layered, where the violation of one SLA escalates the priority or triggers automated actions.

## Authoritative Sources

- [Jira Service Management Documentation](https://confluence.atlassian.com/servicedeskcloud)
