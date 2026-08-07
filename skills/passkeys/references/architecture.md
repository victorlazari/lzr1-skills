# Passkeys Architecture

## Multi-Tenant Architecture

When designing a multi-tenant architecture for passkeys, consider the following:
- Use a single Relying Party (RP) ID for all tenants if they share the same domain.
- If tenants have custom domains, use related origins (WebAuthn Level 3) to allow passkeys to be used across domains.

## Related Origins (WebAuthn Level 3)

WebAuthn Level 3 introduces the concept of related origins, allowing passkeys to be used across multiple domains owned by the same entity.
- Define related origins in the `.well-known/webauthn` file.
- Ensure the RP ID is consistent across related origins.

## Zero Trust Integration

Integrate passkeys into a Zero Trust architecture by:
- Requiring passkeys for all authentication events.
- Using device-bound passkeys for high-security applications.
- Continuously monitoring for anomalous authentication patterns.

*Verified against upstream: 2026-08-07*
