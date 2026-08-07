---
name: google-workspace-bot-integration
description: Comprehensive documentation for integrating a bot application with the Google Workspace stack. Use when designing, building, or documenting bot commands and workflows for Gmail, Calendar, Sheets, Slides, Docs, Drive, Forms, Contacts, Tasks, Chat, and Events.
---

# Google Workspace Bot Integration

This skill provides comprehensive documentation and reference material for integrating a bot application with the Google Workspace stack. It outlines all possible actions and capabilities your bot can execute across 11 different Google applications and APIs.

## Overview

The integration empowers the bot to handle communication workflows, seamless scheduling, data entry, automated document generation, and asset organization directly from chat interfaces or automated triggers.

## Available Integrations

For detailed capabilities, actions, and bot command examples, refer to the specific reference file for the application you are integrating with:

* **Communication & Scheduling**
  * **Gmail**: Read [references/gmail.md](references/gmail.md) for email sending, drafting, and inbox organization.
  * **Calendar**: Read [references/calendar.md](references/calendar.md) for event management and schedule coordination.
  * **Contacts (People API)**: Read [references/contacts.md](references/contacts.md) for address book and group management.
  * **Chat**: Read [references/chat.md](references/chat.md) for managing spaces, members, and messages using standard Markdown syntax.

* **Productivity & Documents**
  * **Docs**: Read [references/docs.md](references/docs.md) for document generation and template management.
  * **Sheets**: Read [references/sheets.md](references/sheets.md) for data entry, retrieval, and formatting.
  * **Slides**: Read [references/slides.md](references/slides.md) for presentation creation and template population.

* **Organization & Workflow**
  * **Drive**: Read [references/drive.md](references/drive.md) for file storage, organization, and access management.
  * **Forms**: Read [references/forms.md](references/forms.md) for survey creation and response analysis.
  * **Tasks**: Read [references/tasks.md](references/tasks.md) for to-do list management and tracking.

* **Events API**
  * **Events**: The Google Workspace Events API allows subscriptions to user read state updates in Google Chat and events in Google Drive.

## Usage Guidelines

1. **Identify the Target Application**: Determine which Google Workspace application the bot needs to interact with.
2. **Consult the Reference**: Open the corresponding reference file to understand the available actions and API capabilities.
3. **Verify Scopes**: Verify required API scopes and permissions before attempting operations.
4. **Construct Request**: Construct the API request, ensuring compliance with current syntax (e.g., standard Markdown for Chat).
5. **Execute**: Execute the request, handling any errors or rate limits with exponential backoff.
6. **Return Result**: Return the result to the user, confirming success or providing actionable error details.

## Safety and Validation

* **Confirmation**: Require explicit user confirmation before executing destructive actions (e.g., deleting files, transferring calendar ownership).
* **Dry-Run**: Implement dry-run logic for batch updates where supported by the API.
* **Verification**: Volatile facts, such as supported Markdown syntax or specific access levels, will be verified against the upstream documentation at runtime if necessary.

> Verified against upstream: 2026-08-07
