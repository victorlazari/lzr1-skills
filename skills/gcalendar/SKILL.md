---
name: gcalendar
description: Complete workflow for reading, validating, and managing Google Calendar events using MCP tools. Use for bulk event validation, duplicate removal, timezone conversions, and complex calendar scheduling tasks.
---

# Google Calendar Event Validation Workflow

This skill provides a robust, systematic workflow for validating, updating, and cleaning up Google Calendar events in bulk. It is specifically designed to handle complex timezone conversions, fuzzy matching of event names, and duplicate detection.

## Workflow Overview

Managing calendar events at scale involves five critical steps:

1. **Configure MCP and Fetch Events**: Set up the Google Calendar MCP connector and fetch the raw event data.
2. **Establish the Ground Truth**: Research or retrieve the correct schedule and convert it to the target timezone.
3. **Analyze and Map**: Compare the raw calendar events against the ground truth using fuzzy matching.
4. **Identify Anomalies**: Detect incorrect times, duplicate entries, and generic placeholders.
5. **Execute Updates**: Apply corrections and deletions in small batches to prevent timeouts.

## Step 1: Configure MCP and Fetch Events

Before interacting with Google Calendar, ensure the MCP connector is configured correctly.

1. Check the current configuration using `manus-config config load --search calendar`.
2. Identify the correct `accountUid` for the target email address.
3. Update `config.json` to set the `activeAccountUid` if necessary, then run `manus-config config save`.
4. Use the `google_calendar_search_events` MCP tool to fetch events within the target timeframe.

> **Important**: Always save the MCP output to a JSON file (e.g., `events.json`) using Python for structured analysis, rather than relying solely on the terminal output.

## Step 2: Establish the Ground Truth

When validating events against an external schedule (like sports fixtures, conferences, or flights), you must establish a reliable ground truth.

1. **Research**: Use the `search` tool to find official schedules.
2. **Cross-reference**: Verify times across multiple sources, as different outlets may use different timezones (e.g., ET vs. Local).
3. **Timezone Conversion**: Convert all ground truth times to the target timezone (e.g., GMT-3).

*See `references/timezone_handling.md` for detailed procedures on handling complex timezone conversions like EDT/CDT to GMT.*

## Step 3: Analyze and Map

Create a Python script to compare the calendar events against the ground truth.

1. **Normalize Names**: Strip prefixes, suffixes, and group information from calendar event summaries.
2. **Fuzzy Matching**: Implement logic to match teams or event names regardless of order (e.g., "Team A vs Team B" should match "Team B vs Team A").
3. **Alias Mapping**: Account for alternate names (e.g., "USA" vs "United States", "Côte d'Ivoire" vs "Ivory Coast").

*See `scripts/validate_events.py` for a complete reference implementation of the validation logic.*

## Step 4: Identify Anomalies

Categorize every calendar event into one of five states:

- **Correct**: Event exists in the ground truth and the time matches perfectly.
- **Incorrect**: Event exists in the ground truth but the time is wrong.
- **Duplicate**: Multiple calendar events map to the same ground truth event. Keep the one with the correct time (or the most detailed description) and mark the rest for deletion.
- **Generic/Placeholder**: Events that do not represent specific actionable items (e.g., "Group Stage schedule"). Mark for deletion.
- **Not Found/Orphan**: Events that cannot be mapped to the ground truth. Flag for manual review.

## Step 5: Execute Updates

Google Calendar MCP tools can timeout if asked to process too many events at once.

1. Generate an `action_plan.json` containing separate arrays for `updates` and `deletes`.
2. Execute `google_calendar_update_events` in batches of 5-10 events.
3. Execute `google_calendar_delete_events` in a single batch (or smaller batches if >20 events).
4. Verify the results by checking the MCP tool output for success.

*See `scripts/batch_updater.py` for a script that handles batched MCP updates.*
