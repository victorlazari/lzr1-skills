# Multi-Region Team Handoffs (Follow-the-Sun Models)

Verified against upstream: 2026-08-07

## Overview

A "follow-the-sun" model distributes on-call responsibilities across multiple geographic regions to ensure 24/7 coverage without requiring engineers to work outside normal business hours.

## Key Considerations

-   **Schedule Configuration:** Define shifts that align with the working hours of each region.
-   **Handoff Procedures:** Establish clear protocols for transferring active incidents and context between shifts.
-   **Communication:** Ensure seamless communication channels across regions (e.g., shared Slack channels, standardized documentation).
-   **Escalation Policies:** Configure escalation paths that account for regional availability and expertise.

## Implementation Steps

1.  **Define Regions:** Identify the geographic locations of the on-call teams.
2.  **Create Schedules:** Configure schedules in the on-call platform (e.g., PagerDuty) with appropriate shift rotations and handoff times.
3.  **Establish Handoff Meetings:** Schedule brief daily meetings for teams to discuss ongoing issues and transfer context.
4.  **Document Procedures:** Maintain clear, accessible documentation for all on-call procedures and runbooks.

## References

-   [PagerDuty Schedule Configuration](https://support.pagerduty.com/docs/schedules)
-   [Atlassian Incident Management Handbook](https://www.atlassian.com/incident-management/handbook)
