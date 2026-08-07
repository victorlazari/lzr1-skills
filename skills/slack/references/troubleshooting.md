# Troubleshooting Slack Apps

Verified against upstream: 2026-08-07

This reference covers diagnostic commands and common failure modes for Slack apps.

## Common Failure Modes

### 1. `invalid_auth` or `not_authed`
- **Cause**: The token provided is invalid, expired, or missing.
- **Solution**: Verify the token is correct and has not been revoked. Ensure the token is passed correctly in the `Authorization` header (`Bearer xoxb-...`).

### 2. `missing_scope`
- **Cause**: The app does not have the required OAuth scope for the API method.
- **Solution**: Check the API documentation for the required scopes and update your app's configuration. Re-install the app to apply the new scopes.

### 3. `channel_not_found`
- **Cause**: The channel ID is incorrect, or the bot is not a member of the private channel.
- **Solution**: Verify the channel ID. If it's a private channel, ensure the bot has been invited to it.

### 4. `invalid_blocks`
- **Cause**: The Block Kit JSON payload is malformed or exceeds limits.
- **Solution**: Validate the JSON payload against the official Block Kit schema. Check for missing required fields or exceeding character limits.

### 5. Timeout Errors (Interactions)
- **Cause**: The app took longer than 3 seconds to acknowledge an interaction or event.
- **Solution**: Ensure your app acknowledges requests immediately (`ack()`) before performing long-running tasks asynchronously.

## Diagnostic Commands

Use the Slack CLI for debugging:

- `slack activity`: View app activity and logs.
- `slack activity --tail`: Stream activity in real-time.
- `slack manifest validate`: Validate your app's manifest file.
