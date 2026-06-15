# Timezone Handling Guide

When validating calendar events against external sources, timezone conversions are often the most complex and error-prone aspect. This guide provides procedures for handling complex conversions, particularly between North American timezones and global timezones like GMT.

## 1. Identify the Source Timezone

External sources often mix local time and standardized time (like ET) in the same document.

- **ET (Eastern Time)**: Usually EDT (UTC-4) in summer, EST (UTC-5) in winter.
- **CT (Central Time)**: Usually CDT (UTC-5) in summer, CST (UTC-6) in winter. Note that Mexico abolished DST in 2022, so most of Mexico (including Mexico City and Guadalajara) is on CST (UTC-6) year-round.
- **PT (Pacific Time)**: Usually PDT (UTC-7) in summer, PST (UTC-8) in winter.
- **Local Time**: You must determine the timezone of the specific venue.

## 2. Standardize to a Single Baseline

Convert all times from the source document into a single baseline timezone (e.g., ET or UTC) before converting to the final target timezone.

```python
# Example: Standardizing mixed source times to ET (EDT = UTC-4)
source_times = {
    "Match 1": {"time": "15:00", "zone": "PDT"}, # 3 PM PDT
    "Match 2": {"time": "13:00", "zone": "CST"}, # 1 PM CST (Mexico)
}

et_times = {}
for match, data in source_times.items():
    if data["zone"] == "PDT":
        # PDT is UTC-7, EDT is UTC-4. PDT is 3 hours behind EDT.
        # To get EDT: PDT + 3
        et_times[match] = add_hours(data["time"], 3)
    elif data["zone"] == "CST":
        # CST is UTC-6, EDT is UTC-4. CST is 2 hours behind EDT.
        # To get EDT: CST + 2
        et_times[match] = add_hours(data["time"], 2)
```

## 3. Convert to Target Timezone

Once you have a standardized baseline, convert to the user's target timezone (e.g., GMT-3 / BRT).

```python
# Example: Convert ET (EDT = UTC-4) to BRT (UTC-3)
# BRT is 1 hour ahead of EDT.
# BRT = EDT + 1 hour

def convert_edt_to_brt(date_str, edt_time_str):
    edt_hour = int(edt_time_str.split(":")[0])
    edt_min = int(edt_time_str.split(":")[1])
    
    brt_hour = edt_hour + 1
    brt_date = date_str
    
    # Handle day rollover
    if brt_hour >= 24:
        brt_hour -= 24
        d = datetime.strptime(date_str, "%Y-%m-%d")
        d += timedelta(days=1)
        brt_date = d.strftime("%Y-%m-%d")
        
    brt_time = f"{brt_hour:02d}:{edt_min:02d}"
    return f"{brt_date}T{brt_time}:00-03:00"
```

## 4. Formatting for Google Calendar

Google Calendar expects times in RFC3339 format.

- **Correct**: `2026-06-11T16:00:00-03:00`
- **Correct (UTC)**: `2026-06-11T19:00:00Z`
- **Incorrect**: `2026-06-11 16:00:00`

When updating events, always ensure the timezone offset matches the target timezone you calculated.
