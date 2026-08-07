# Timezone Handling Guide

When validating calendar events against external sources, timezone conversions are often the most complex and error-prone aspect. This guide provides procedures for handling complex conversions using IANA time zone identifiers, as required by the Google Calendar API.

## 1. Identify the Source Timezone

External sources often mix local time and standardized time in the same document. Identify the correct IANA time zone identifier for the source.

- **ET (Eastern Time)**: `America/New_York`
- **CT (Central Time)**: `America/Chicago` (Note: Mexico abolished DST in 2022, so most of Mexico is on `America/Mexico_City` year-round).
- **PT (Pacific Time)**: `America/Los_Angeles`
- **Local Time**: Determine the IANA time zone identifier for the specific venue (e.g., `Europe/London`, `Asia/Tokyo`).

## 2. Standardize to a Single Baseline

Convert all times from the source document into a single baseline timezone (e.g., UTC) before converting to the final target timezone. Use Python's `zoneinfo` module (available in Python 3.9+) for accurate conversions that automatically handle daylight saving time transitions.

```python
from datetime import datetime
from zoneinfo import ZoneInfo

# Example: Standardizing mixed source times to UTC
source_times = {
    "Match 1": {"time": "2026-06-11 15:00:00", "zone": "America/Los_Angeles"},
    "Match 2": {"time": "2026-06-11 13:00:00", "zone": "America/Mexico_City"},
}

utc_times = {}
for match, data in source_times.items():
    # Create a timezone-aware datetime object in the source timezone
    dt = datetime.strptime(data["time"], "%Y-%m-%d %H:%M:%S")
    dt_aware = dt.replace(tzinfo=ZoneInfo(data["zone"]))

    # Convert to UTC
    dt_utc = dt_aware.astimezone(ZoneInfo("UTC"))
    utc_times[match] = dt_utc
```

## 3. Convert to Target Timezone

Once you have a standardized baseline, convert to the user's target timezone using its IANA identifier.

```python
# Example: Convert UTC to BRT (America/Sao_Paulo)
target_zone = "America/Sao_Paulo"

brt_times = {}
for match, dt_utc in utc_times.items():
    dt_brt = dt_utc.astimezone(ZoneInfo(target_zone))
    brt_times[match] = dt_brt
```

## 4. Formatting for Google Calendar

The Google Calendar API expects times to be specified using the `dateTime` and `timeZone` fields in the `start` and `end` objects.

- **Correct**:
  ```json
  "start": {
    "dateTime": "2026-06-11T16:00:00",
    "timeZone": "America/Sao_Paulo"
  }
  ```
- **Incorrect**: Manually calculating offsets (e.g., `2026-06-11T16:00:00-03:00`).

When updating events, always provide the `dateTime` in the local time of the target timezone and specify the corresponding IANA `timeZone` identifier. The API will handle the offset calculation correctly, including daylight saving time rules.
