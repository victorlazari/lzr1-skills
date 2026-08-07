# ChatOps Integration and Incident War Rooms

Verified against upstream: 2026-08-07

## Overview

ChatOps integrates incident management workflows directly into collaboration platforms like Slack or Microsoft Teams, enabling faster communication and resolution.

## Key Features

-   **Incident War Rooms:** Dedicated channels created automatically for each incident.
-   **Automated Notifications:** Alerts and updates routed to specific channels based on severity and service.
-   **Inline Actions:** Acknowledging, resolving, or escalating incidents directly from the chat interface.
-   **Runbook Execution:** Triggering automated runbooks via chat commands.

## Implementation Steps

1.  **Platform Integration:** Connect the on-call system (e.g., PagerDuty, incident.io) to the chat platform.
2.  **Channel Mapping:** Configure rules to route alerts to appropriate channels (e.g., `#alerts-database`, `#incidents-sev1`).
3.  **Command Configuration:** Define and test chat commands for common actions (e.g., `/incident declare`, `/runbook execute`).
4.  **Access Control:** Restrict sensitive actions to authorized users or roles within the chat platform.

## References

-   [PagerDuty Slack Integration](https://support.pagerduty.com/docs/slack-integration-guide)
-   [incident.io Slack Integration](https://help.incident.io/en/articles/5400000-slack-integration)
