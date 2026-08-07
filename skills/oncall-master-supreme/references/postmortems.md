# Post-Incident Reviews (Postmortems) and Jeli Integration

Verified against upstream: 2026-08-07

## Overview

Blameless post-incident reviews (postmortems) are essential for learning from failures and improving system reliability.

## Key Components

-   **Incident Summary:** A brief description of the incident, impact, and resolution.
-   **Timeline:** A detailed chronological sequence of events, including detection, diagnosis, and mitigation.
-   **Root Cause Analysis:** Identification of the underlying causes (e.g., using the "5 Whys" technique).
-   **Action Items:** Specific, assignable tasks to prevent recurrence or improve response times.

## Jeli Integration

Jeli (now part of PagerDuty) provides advanced incident analysis capabilities.

1.  **Data Ingestion:** Import incident data from PagerDuty, Slack, and other sources.
2.  **Narrative Building:** Use Jeli's interface to construct a comprehensive narrative of the incident.
3.  **Theme Extraction:** Identify recurring themes and systemic issues across multiple incidents.

## References

-   [Google SRE Book: Postmortem Culture](https://sre.google/sre-book/postmortem-culture/)
-   [Jeli Documentation](https://docs.jeli.io/)
