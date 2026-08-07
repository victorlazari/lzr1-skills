# Security Patterns for Slack Apps

Verified against upstream: 2026-08-07

This reference covers guidelines for request signature validation, OAuth scopes, and token management.

## Request Signature Validation

All incoming requests from Slack (events, interactions, slash commands) must be verified using the `X-Slack-Signature` header and your app's Signing Secret.

1. Extract the `X-Slack-Request-Timestamp` and `X-Slack-Signature` headers.
2. Verify the timestamp is within 5 minutes of the current time to prevent replay attacks.
3. Concatenate the version number (`v0`), the timestamp, and the request body with colons (`:`).
4. Hash the resulting string using HMAC SHA256 with your Signing Secret.
5. Compare the resulting hash with the `X-Slack-Signature` header.

## OAuth Scopes

Use the principle of least privilege when requesting OAuth scopes. Only request the scopes necessary for your app's functionality.

- **Bot Scopes**: Use bot scopes (e.g., `chat:write`, `channels:read`) for actions performed by the bot user.
- **User Scopes**: Use user scopes (e.g., `search:read`, `users.profile:write`) for actions performed on behalf of a user.

## Token Management

- **Bot Tokens (`xoxb-`)**: Used for bot actions. Store securely and do not expose in client-side code.
- **User Tokens (`xoxp-`)**: Used for user actions. Store securely and associate with the specific user.
- **App-Level Tokens (`xapp-`)**: Used for Socket Mode connections. Store securely.
- **Signing Secret**: Used for request verification. Store securely.

Rotate tokens periodically and immediately if compromised.
