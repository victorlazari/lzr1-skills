# Passkeys Security

## Threat Models

Consider the following threat models when implementing passkeys:
- **Phishing:** Passkeys are inherently resistant to phishing because the RP ID is bound to the origin.
- **Credential Stuffing:** Passkeys are not susceptible to credential stuffing because they are unique to each RP.
- **Device Theft:** Synced passkeys can be accessed if the user's cloud account is compromised. Device-bound passkeys are tied to the physical device.

## Security Checklists

- [ ] Verify the RP ID matches the origin.
- [ ] Ensure challenges are cryptographically secure and unique for each request.
- [ ] Validate the signature using the public key stored during registration.
- [ ] Check for cloned authenticators using the sign count.

## NIST SP 800-63-4 Compliance

- **Synced Authenticators:** Allowed for AAL2 if the sync fabric is secure.
- **Device-Bound Authenticators:** Required for AAL3.

*Verified against upstream: 2026-08-07*
