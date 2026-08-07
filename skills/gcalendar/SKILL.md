---
name: gcalendar
description: Complete workflow for reading, validating, and managing Google Calendar events using MCP tools. Use for bulk event validation, duplicate removal, timezone conversions, and complex calendar scheduling tasks.
---

# Google Calendar Event Validation Workflow

This skill provides a robust, systematic workflow for validating, updating, and cleaning up Google Calendar events in bulk. It is specifically designed to handle complex timezone conversions, fuzzy matching of event names, and duplicate detection.

## Scope and Triggers

- **Handles**: Bulk event validation, duplicate removal, timezone conversions, and complex calendar scheduling tasks.
- **Activates**: When the user requests to validate, update, or clean up Google Calendar events in bulk.
- **Non-goals**: Creating single events, managing calendar sharing, or handling non-Google calendars.

## Preconditions

- The target Google Calendar account must be accessible via the MCP connector.
- The user must provide a clear goal or ground truth schedule for validation.

## Source Freshness

- Verified against upstream: 2026-08-07
- Official Google Calendar API overview: https://developers.google.com/workspace/calendar/api/guides/overview
- API Reference | Google Calendar: https://developers.google.com/workspace/calendar/api/v3/reference
- Configure the Calendar MCP server: https://developers.google.com/workspace/calendar/api/guides/configure-mcp-server
- MCP Reference: calendarmcp.googleapis.com: https://developers.google.com/workspace/calendar/api/v3/reference/mcp

## Workflow

1. **Configure MCP and Fetch Events**: Verify configuration and use `search_events` to fetch data.
2. **Establish Ground Truth**: Retrieve the correct schedule and determine the target IANA time zone.
3. **Analyze and Map**: Compare events using fuzzy matching and alias mapping.
4. **Identify Anomalies**: Categorize events as correct, incorrect, duplicate, generic, or not found.
5. **Generate Action Plan**: Create a JSON plan for updates and deletions.
6. **Dry Run and Confirm**: Present the action plan to the user for confirmation.
7. **Execute Updates**: Use `update_event` and `delete_event` in batches, respecting API rate limits.

## Step 1: Configure MCP and Fetch Events

Before interacting with Google Calendar, ensure the MCP connector is configured correctly.

1. Check the current configuration using `manus-config config load --search calendar`.
2. Identify the correct `accountUid` for the target email address.
3. Update `config.json` to set the `activeAccountUid` if necessary, then run `manus-config config save`.
4. Use the `search_events` MCP tool to fetch events within the target timeframe.

> **Important**: Always save the MCP output to a JSON file (e.g., `events.json`) using Python for structured analysis, rather than relying solely on the terminal output.

## Step 2: Establish the Ground Truth

When validating events against an external schedule (like sports fixtures, conferences, or flights), you must establish a reliable ground truth.

1. **Research**: Use the `search` tool to find official schedules.
2. **Cross-reference**: Verify times across multiple sources.
3. **Timezone Conversion**: Convert all ground truth times to the target timezone using IANA time zone identifiers.

*See `references/timezone_handling.md` for detailed procedures on handling complex timezone conversions.*

## Step 3: Analyze and Map

Create a Python script to compare the calendar events against the ground truth.

1. **Normalize Names**: Strip prefixes, suffixes, and group information from calendar event summaries.
2. **Fuzzy Matching**: Implement logic to match teams or event names regardless of order.
3. **Alias Mapping**: Account for alternate names.

*See `scripts/validate_events.py` for a complete reference implementation of the validation logic.*

## Step 4: Identify Anomalies

Categorize every calendar event into one of five states:

- **Correct**: Event exists in the ground truth and the time matches perfectly.
- **Incorrect**: Event exists in the ground truth but the time is wrong.
- **Duplicate**: Multiple calendar events map to the same ground truth event. Keep the one with the correct time (or the most detailed description) and mark the rest for deletion.
- **Generic/Placeholder**: Events that do not represent specific actionable items. Mark for deletion.
- **Not Found/Orphan**: Events that cannot be mapped to the ground truth. Flag for manual review.

## Step 5: Execute Updates

Google Calendar MCP tools can timeout if asked to process too many events at once.

1. Generate an `action_plan.json` containing separate arrays for `updates` and `deletes`.
2. **Dry Run and Confirm**: Present the action plan to the user for confirmation before executing any updates or deletions.
3. Execute `update_event` in batches of 5-10 events.
4. Execute `delete_event` in a single batch (or smaller batches if >20 events).
5. Verify the results by checking the MCP tool output for success.

*See `scripts/batch_updater.py` for a script that handles batched MCP updates.*

## Safety

- Separate read-only discovery from mutations.
- Require user confirmation before executing deletions or updates.
- Perform a dry run of the event mapping logic against a sample dataset.

## Validation

- Verify MCP server configuration before execution.
- Validate `action_plan.json` against the expected schema.
- Implement rate limiting in the batch updater.

## Failure Handling

- If an update fails, check the MCP tool output for error messages.
- If rate limits are exceeded, increase the delay between batches.
- Do not repeat a failed action unchanged.

## Output Contract

- The final output must include a summary of the actions taken, including the number of events updated and deleted.
- Any anomalies that could not be resolved automatically must be flagged for manual review.

## Resources

- `references/timezone_handling.md`: Guide for handling complex timezone conversions.
- `scripts/validate_events.py`: Reference implementation of the validation logic.
- `scripts/batch_updater.py`: Script for executing batched MCP updates.
