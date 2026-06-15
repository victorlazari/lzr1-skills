# Cron Syntax Reference

Cron uses a 5-field time scheduling syntax followed by the command to execute.

## Format

```
*    *    *    *    *   /path/to/command
|    |    |    |    |
|    |    |    |    +-- Day of week (0-7, Sunday is 0 or 7)
|    |    |    +------- Month (1-12)
|    |    +------------ Day of month (1-31)
|    +----------------- Hour (0-23)
+---------------------- Minute (0-59)
```

## Operators

- `*` (Asterisk): Matches all values for that field. (e.g., `*` in the hour field means every hour).
- `,` (Comma): Separates items in a list. (e.g., `1,15` in the day of month field means the 1st and 15th of the month).
- `-` (Hyphen): Defines a range. (e.g., `1-5` in the day of week field means Monday through Friday).
- `/` (Slash): Defines a step value. (e.g., `*/5` in the minute field means every 5 minutes).

## Common Examples

| Expression | Description |
| :--- | :--- |
| `* * * * *` | Every minute |
| `0 * * * *` | Every hour, at minute 0 |
| `0 0 * * *` | Every day at midnight |
| `0 0 * * 0` | Every Sunday at midnight |
| `*/5 * * * *` | Every 5 minutes |
| `0 9-17 * * 1-5` | Every hour from 9 AM to 5 PM, Monday through Friday |
| `0 0 1,15 * *` | Midnight on the 1st and 15th of every month |

## Predefined Macros (if supported by the cron implementation)

Some cron implementations support special strings instead of the 5-field syntax:

- `@reboot`: Run once, at startup.
- `@yearly` or `@annually`: Run once a year, `0 0 1 1 *`.
- `@monthly`: Run once a month, `0 0 1 * *`.
- `@weekly`: Run once a week, `0 0 * * 0`.
- `@daily` or `@midnight`: Run once a day, `0 0 * * *`.
- `@hourly`: Run once an hour, `0 * * * *`.
