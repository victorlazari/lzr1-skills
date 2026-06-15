# Specialist: 51-passkeys

## === FILE: 51-passkeys-advanced.md ===
# Passkeys Advanced Patterns and Enterprise Architecture

## 1. Multi-Tenant Passkey Architecture

In multi-tenant SaaS applications, passkey architecture must account for the relationship between tenants, domains, and RP IDs. The RP ID is bound to a single registrable domain, meaning all tenants sharing a domain (e.g., `tenant1.app.com`, `tenant2.app.com`) will share the same RP ID (`app.com`). This has critical implications for credential isolation.

### 1.1 Tenant Isolation Strategies

If tenants are accessed via subdomains of a shared domain, passkeys registered under one tenant are technically valid for all tenants (since they share the RP ID). The relying party must implement application-level isolation by associating each credential with both a user ID and a tenant ID, and rejecting assertions where the credential's tenant does not match the requested tenant.

If tenants have custom domains (e.g., `login.customer1.com`), each custom domain constitutes a separate RP ID, providing natural cryptographic isolation. However, this means a user who accesses multiple tenants must register separate passkeys for each custom domain.

### 1.2 Related Origins (WebAuthn Level 3)

WebAuthn Level 3 introduces the "related origins" concept, allowing a relying party to specify additional origins that are authorized to use credentials registered under the primary RP ID. This is configured via a `.well-known/webauthn` file hosted at the RP ID's domain. This feature enables SSO-like experiences where a passkey registered at `example.com` can be used to authenticate at `auth.example.com` or `login.example.com`.

## 2. Passkeys with Risk-Based Authentication

Advanced deployments combine passkeys with risk-based authentication (RBA) engines to dynamically adjust security requirements based on contextual signals.

### 2.1 Signal Collection

During a passkey authentication, the relying party collects contextual signals including: the IP address and geolocation, the device fingerprint, the time of day, the authenticator model (via AAGUID), whether the credential is synced or device-bound (via BE/BS flags), and the user's historical authentication patterns.

### 2.2 Dynamic Policy Enforcement

Based on these signals, the RBA engine can make real-time decisions:

If the user is authenticating from a recognized device, at a normal time, from a familiar location, the passkey assertion alone is sufficient. If the user is authenticating from a new device or unusual location, the system may require step-up authentication (a second passkey assertion with `userVerification: required`) or trigger an out-of-band verification (push notification to a registered device).

If the RBA engine detects indicators of compromise (e.g., the assertion originates from a known malicious IP, or the authenticator model has a known vulnerability published in the FIDO MDS), the system can reject the authentication entirely and lock the account pending manual review.

## 3. Passkeys in Zero Trust Architecture

In a Zero Trust security model, no user or device is inherently trusted, regardless of network location. Passkeys serve as a foundational component of Zero Trust by providing continuous, phishing-resistant identity verification.

### 3.1 Continuous Authentication

Traditional session-based authentication verifies identity once and then trusts the session cookie for the duration. Zero Trust architectures require periodic re-verification, particularly before accessing sensitive resources.

Passkeys enable frictionless continuous authentication because the biometric gesture is fast and familiar. Applications can silently request a passkey assertion at defined intervals (e.g., every 30 minutes) or before specific actions, without significantly disrupting the user's workflow.

### 3.2 Device Trust Integration

In enterprise Zero Trust deployments, passkey authentication is often combined with device trust signals from MDM (Mobile Device Management) or EDR (Endpoint Detection and Response) solutions. The authentication decision considers not only the passkey assertion but also whether the device is managed, compliant with security policies (encrypted, patched, no jailbreak detected), and free of active threats.

## 4. Advanced Attestation Workflows

### 4.1 Enterprise Attestation

Enterprise attestation is a special attestation mode available on managed devices. When enabled via MDM policy, the authenticator includes the device's unique identifier in the attestation statement, allowing the relying party to verify that the credential was created on a specific, organization-managed device.

This is particularly valuable for organizations that need to maintain an inventory of authorized authenticators and ensure that credentials are only created on approved hardware.

### 4.2 Attestation Verification Pipeline

For relying parties that enforce attestation, the verification pipeline must:

1. Extract the attestation format from the attestation object (packed, tpm, android-key, apple, fido-u2f, none).
2. Parse the attestation statement according to the format-specific rules defined in the WebAuthn specification.
3. Verify the attestation signature using the appropriate trust anchor (manufacturer root certificate, FIDO MDS root, or Apple WebAuthn root CA).
4. Validate the certificate chain, checking for revocation via CRL or OCSP.
5. Extract the AAGUID and query the FIDO Metadata Service to verify the authenticator's certification level and security status.
6. Apply organizational policy (e.g., reject if certification level is below L2, or if the authenticator model has a published vulnerability).

## 5. Passkeys and Account Linking

### 5.1 The Duplicate Account Problem

When organizations introduce passkeys alongside existing authentication methods, they must handle the scenario where a user has multiple accounts (e.g., one created with email/password and another created via social login). Passkey registration must be integrated with account linking workflows to prevent credential fragmentation.

### 5.2 Linking Strategy

The recommended approach is to require identity verification before allowing passkey registration. If a user authenticates via a social provider (Google, Apple) and then attempts to register a passkey, the system should first verify that the social identity is linked to the correct internal account. This prevents scenarios where a user accidentally registers a passkey against the wrong account.

## 6. Passkeys for Machine-to-Machine Authentication

While passkeys are primarily designed for human authentication (requiring biometric verification), emerging patterns extend the concept to machine-to-machine (M2M) scenarios using the underlying FIDO2 infrastructure.

### 6.1 Hardware-Bound Service Credentials

In high-security environments, service accounts can be authenticated using hardware security modules (HSMs) or TPMs that implement the CTAP protocol. The service's private key is stored in the HSM, and authentication is performed programmatically without human interaction. This provides the same phishing-resistance and non-exportability guarantees as human passkeys, but for automated systems.

### 6.2 Attestation for Supply Chain Security

The attestation mechanism can be repurposed for software supply chain security. Build systems can use hardware-bound credentials to sign build artifacts, providing cryptographic proof that the artifact was produced on a specific, trusted build machine with a verified secure enclave.

## 7. Performance Benchmarks

Based on production deployments, the following performance characteristics are typical:

| Operation | Latency (P50) | Latency (P95) | Notes |
|-----------|---------------|---------------|-------|
| Registration (platform authenticator) | 2-4 seconds | 6-8 seconds | Includes biometric prompt |
| Authentication (platform, conditional UI) | 1-2 seconds | 3-5 seconds | Fastest path |
| Authentication (cross-device/hybrid) | 8-15 seconds | 20-30 seconds | Includes QR scan + BLE |
| Server-side verification | 1-3 ms | 5-10 ms | ES256 signature verification |
| Challenge generation + storage | < 1 ms | 2-3 ms | Redis-backed |
| Credential lookup by ID | 1-2 ms | 5-8 ms | Indexed PostgreSQL |

## 8. Disaster Recovery and Business Continuity

### 8.1 IdP Outage Scenarios

If the organization's Identity Provider experiences an outage, passkey authentication will fail for applications that delegate authentication. Mitigation strategies include maintaining a local authentication fallback (direct WebAuthn endpoints that bypass the IdP) or implementing IdP redundancy with automatic failover.

### 8.2 Cloud Keychain Outage

If Apple iCloud, Google Password Manager, or another cloud keychain provider experiences an outage, users with synced passkeys may be unable to authenticate. The relying party cannot control this scenario but must ensure that fallback authentication methods (password, backup codes, hardware keys) remain available during such events.

### 8.3 Database Recovery

If the credentials database is corrupted or lost, all registered passkeys become permanently unusable (the server can no longer verify assertions without the stored public keys). This makes the credentials table one of the most critical datasets in the application. It must be included in all backup strategies, with point-in-time recovery capability and regular backup verification testing.

## === FILE: 51-passkeys-cli-reference.md ===
# Passkeys CLI Reference and API Commands

## 1. WebAuthn JavaScript API Reference

### 1.1 Registration (navigator.credentials.create)

```javascript
// Full PublicKeyCredentialCreationOptions specification
const options = {
  publicKey: {
    // REQUIRED: Server-generated cryptographic challenge (min 16 bytes)
    challenge: new Uint8Array(32), // Must be crypto.getRandomValues() on server

    // REQUIRED: Relying Party information
    rp: {
      id: "example.com",        // Registrable domain (NOT full URL)
      name: "Example Corp"       // Human-readable display name
    },

    // REQUIRED: User information
    user: {
      id: new Uint8Array(64),    // Opaque user handle (NOT email, max 64 bytes)
      name: "user@example.com",  // Username/email for display
      displayName: "Jane Doe"    // Friendly name for UI
    },

    // REQUIRED: Supported algorithms (ordered by preference)
    pubKeyCredParams: [
      { type: "public-key", alg: -7 },    // ES256 (ECDSA w/ SHA-256) - RECOMMENDED
      { type: "public-key", alg: -257 },   // RS256 (RSASSA-PKCS1-v1_5 w/ SHA-256)
      { type: "public-key", alg: -8 },     // EdDSA
      { type: "public-key", alg: -35 },    // ES384
      { type: "public-key", alg: -36 }     // ES512
    ],

    // OPTIONAL: Authenticator requirements
    authenticatorSelection: {
      authenticatorAttachment: "platform",  // "platform" | "cross-platform" | undefined
      residentKey: "required",             // "required" | "preferred" | "discouraged"
      requireResidentKey: true,            // Deprecated, use residentKey instead
      userVerification: "required"         // "required" | "preferred" | "discouraged"
    },

    // OPTIONAL: Credentials to exclude (prevent duplicate registration)
    excludeCredentials: [
      {
        type: "public-key",
        id: existingCredentialId,           // ArrayBuffer of existing credential
        transports: ["internal", "hybrid"]  // Hint for authenticator selection
      }
    ],

    // OPTIONAL: Timeout in milliseconds (default varies by browser)
    timeout: 60000,

    // OPTIONAL: Attestation preference
    attestation: "none",  // "none" | "indirect" | "direct" | "enterprise"

    // OPTIONAL: Attestation formats preference (Level 3)
    attestationFormats: ["packed", "tpm"],

    // OPTIONAL: Extensions
    extensions: {
      credProps: true,           // Request credential properties
      minPinLength: true,        // Request minimum PIN length
      credBlob: new Uint8Array() // Store small blob with credential
    }
  }
};

const credential = await navigator.credentials.create(options);
```

### 1.2 Authentication (navigator.credentials.get)

```javascript
// Full PublicKeyCredentialRequestOptions specification
const options = {
  publicKey: {
    // REQUIRED: Server-generated cryptographic challenge
    challenge: new Uint8Array(32),

    // OPTIONAL: Relying Party ID (defaults to current origin's effective domain)
    rpId: "example.com",

    // OPTIONAL: Allowed credentials (omit for discoverable credentials)
    allowCredentials: [
      {
        type: "public-key",
        id: credentialId,                    // ArrayBuffer
        transports: ["internal", "hybrid"]   // Performance hint
      }
    ],

    // OPTIONAL: User verification requirement
    userVerification: "required",  // "required" | "preferred" | "discouraged"

    // OPTIONAL: Timeout
    timeout: 60000,

    // OPTIONAL: Extensions
    extensions: {
      appid: "https://legacy-u2f.example.com",  // U2F backward compatibility
      getCredBlob: true                          // Retrieve stored blob
    }
  },

  // OPTIONAL: Mediation behavior
  mediation: "conditional"  // "conditional" | "optional" | "required" | "silent"
};

const assertion = await navigator.credentials.get(options);
```

### 1.3 Capability Detection (Level 3)

```javascript
// Check if WebAuthn is supported
if (window.PublicKeyCredential) {
  console.log("WebAuthn supported");
}

// Check Conditional UI support
const conditionalSupported = await PublicKeyCredential.isConditionalMediationAvailable();

// Check User Verifying Platform Authenticator availability
const platformAvailable = await PublicKeyCredential.isUserVerifyingPlatformAuthenticatorAvailable();

// Get client capabilities (Level 3)
const capabilities = await PublicKeyCredential.getClientCapabilities();
// Returns: { conditionalCreate: true, conditionalGet: true, hybridTransport: true, ... }

// Signal methods (Level 3)
await PublicKeyCredential.signalUnknownCredential({ rpId: "example.com", credentialId: id });
await PublicKeyCredential.signalAllAcceptedCredentials({ rpId: "example.com", userId: uid, allAcceptedCredentialIds: [...] });
await PublicKeyCredential.signalCurrentUserDetails({ rpId: "example.com", userId: uid, name: "new@email.com", displayName: "New Name" });
```

## 2. Server-Side API Endpoints

### 2.1 Registration Endpoints

```bash
# Request registration options
curl -X POST https://api.example.com/webauthn/register/options \
  -H "Authorization: Bearer <session_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "jane.doe@example.com",
    "displayName": "Jane Doe",
    "authenticatorType": "platform"
  }'

# Response:
# {
#   "challenge": "base64url_encoded_challenge",
#   "rp": { "id": "example.com", "name": "Example Corp" },
#   "user": { "id": "base64url_user_id", "name": "jane.doe@example.com", "displayName": "Jane Doe" },
#   "pubKeyCredParams": [{ "type": "public-key", "alg": -7 }],
#   "timeout": 60000,
#   "excludeCredentials": [],
#   "authenticatorSelection": { "residentKey": "required", "userVerification": "required" }
# }

# Submit registration response
curl -X POST https://api.example.com/webauthn/register/verify \
  -H "Authorization: Bearer <session_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "base64url_credential_id",
    "rawId": "base64url_raw_id",
    "type": "public-key",
    "response": {
      "attestationObject": "base64url_attestation_object",
      "clientDataJSON": "base64url_client_data",
      "transports": ["internal", "hybrid"]
    },
    "clientExtensionResults": { "credProps": { "rk": true } }
  }'
```

### 2.2 Authentication Endpoints

```bash
# Request authentication options
curl -X POST https://api.example.com/webauthn/authenticate/options \
  -H "Content-Type: application/json" \
  -d '{ "username": "jane.doe@example.com" }'

# For discoverable credentials (no username required):
curl -X POST https://api.example.com/webauthn/authenticate/options \
  -H "Content-Type: application/json" \
  -d '{}'

# Submit authentication response
curl -X POST https://api.example.com/webauthn/authenticate/verify \
  -H "Content-Type: application/json" \
  -d '{
    "id": "base64url_credential_id",
    "rawId": "base64url_raw_id",
    "type": "public-key",
    "response": {
      "authenticatorData": "base64url_auth_data",
      "clientDataJSON": "base64url_client_data",
      "signature": "base64url_signature",
      "userHandle": "base64url_user_handle"
    }
  }'
```

## 3. SimpleWebAuthn Server Commands (Node.js)

```javascript
// Installation
// npm install @simplewebauthn/server @simplewebauthn/browser

// Generate Registration Options
import { generateRegistrationOptions } from '@simplewebauthn/server';

const options = await generateRegistrationOptions({
  rpName: 'Example Corp',
  rpID: 'example.com',
  userName: 'jane.doe@example.com',
  userDisplayName: 'Jane Doe',
  attestationType: 'none',
  excludeCredentials: existingCredentials.map(cred => ({
    id: cred.credentialID,
    transports: cred.transports,
  })),
  authenticatorSelection: {
    residentKey: 'required',
    userVerification: 'required',
  },
});

// Verify Registration Response
import { verifyRegistrationResponse } from '@simplewebauthn/server';

const verification = await verifyRegistrationResponse({
  response: registrationBody,
  expectedChallenge: storedChallenge,
  expectedOrigin: 'https://example.com',
  expectedRPID: 'example.com',
});

// Generate Authentication Options
import { generateAuthenticationOptions } from '@simplewebauthn/server';

const options = await generateAuthenticationOptions({
  rpID: 'example.com',
  userVerification: 'required',
  allowCredentials: [], // Empty for discoverable credentials
});

// Verify Authentication Response
import { verifyAuthenticationResponse } from '@simplewebauthn/server';

const verification = await verifyAuthenticationResponse({
  response: authenticationBody,
  expectedChallenge: storedChallenge,
  expectedOrigin: 'https://example.com',
  expectedRPID: 'example.com',
  credential: {
    id: storedCredential.credentialID,
    publicKey: storedCredential.publicKey,
    counter: storedCredential.counter,
  },
});
```

## 4. py_webauthn Server Commands (Python)

```python
# pip install webauthn

from webauthn import generate_registration_options, verify_registration_response
from webauthn import generate_authentication_options, verify_authentication_response
from webauthn.helpers.structs import (
    AuthenticatorSelectionCriteria, ResidentKeyRequirement,
    UserVerificationRequirement, PublicKeyCredentialDescriptor
)

# Generate Registration Options
options = generate_registration_options(
    rp_id="example.com",
    rp_name="Example Corp",
    user_id=b"unique_user_id_bytes",
    user_name="jane.doe@example.com",
    user_display_name="Jane Doe",
    authenticator_selection=AuthenticatorSelectionCriteria(
        resident_key=ResidentKeyRequirement.REQUIRED,
        user_verification=UserVerificationRequirement.REQUIRED,
    ),
    exclude_credentials=[
        PublicKeyCredentialDescriptor(id=cred.credential_id)
        for cred in existing_credentials
    ],
)

# Verify Registration Response
verification = verify_registration_response(
    credential=registration_response,
    expected_challenge=stored_challenge,
    expected_origin="https://example.com",
    expected_rp_id="example.com",
)

# Generate Authentication Options
options = generate_authentication_options(
    rp_id="example.com",
    user_verification=UserVerificationRequirement.REQUIRED,
)

# Verify Authentication Response
verification = verify_authentication_response(
    credential=authentication_response,
    expected_challenge=stored_challenge,
    expected_origin="https://example.com",
    expected_rp_id="example.com",
    credential_public_key=stored_credential.public_key,
    credential_current_sign_count=stored_credential.sign_count,
)
```

## 5. Database Operations

```sql
-- PostgreSQL schema for passkey credentials
CREATE TABLE webauthn_credentials (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    credential_id BYTEA NOT NULL UNIQUE,
    public_key BYTEA NOT NULL,
    public_key_algorithm INTEGER NOT NULL DEFAULT -7,
    sign_count BIGINT NOT NULL DEFAULT 0,
    transports TEXT[] DEFAULT '{}',
    backup_eligible BOOLEAN NOT NULL DEFAULT false,
    backup_state BOOLEAN NOT NULL DEFAULT false,
    authenticator_attachment TEXT,
    aaguid UUID,
    device_name TEXT DEFAULT 'Unknown Device',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    last_used_at TIMESTAMPTZ,
    revoked_at TIMESTAMPTZ
);

CREATE INDEX idx_credentials_user_id ON webauthn_credentials(user_id);
CREATE INDEX idx_credentials_credential_id ON webauthn_credentials(credential_id);

-- Query: Get all active credentials for a user
SELECT * FROM webauthn_credentials
WHERE user_id = $1 AND revoked_at IS NULL
ORDER BY last_used_at DESC NULLS LAST;

-- Query: Find credential by ID for authentication
SELECT * FROM webauthn_credentials
WHERE credential_id = $1 AND revoked_at IS NULL;

-- Update: Increment sign count after successful authentication
UPDATE webauthn_credentials
SET sign_count = $2, last_used_at = NOW()
WHERE credential_id = $1;

-- Revoke: Soft-delete a credential
UPDATE webauthn_credentials
SET revoked_at = NOW()
WHERE id = $1 AND user_id = $2;
```

## 6. Testing Commands

```bash
# Chrome DevTools Protocol - Virtual Authenticator
# Enable WebAuthn in Chrome DevTools
chrome://flags/#enable-web-authentication-testing-api

# Playwright virtual authenticator setup
npx playwright test --project=chromium

# FIDO Conformance Testing Tool
# Download from: https://fidoalliance.org/certification/functional-certification/conformance/
java -jar fido2-conformance-tools.jar --rp-url https://example.com

# OpenSSL - Verify ES256 signature manually
openssl dgst -sha256 -verify public_key.pem -signature signature.bin signed_data.bin

# Generate test challenge (32 bytes, base64url)
openssl rand -base64 32 | tr '+/' '-_' | tr -d '='

# Decode CBOR attestation object (using cbor-diag tool)
echo "<base64_attestation>" | base64 -d | cbor2diag.rb
```

## 7. Environment Variables

```bash
# Server configuration
WEBAUTHN_RP_ID=example.com
WEBAUTHN_RP_NAME="Example Corp"
WEBAUTHN_RP_ORIGIN=https://example.com
WEBAUTHN_TIMEOUT=60000
WEBAUTHN_ATTESTATION=none
WEBAUTHN_USER_VERIFICATION=required
WEBAUTHN_RESIDENT_KEY=required

# Challenge storage (Redis)
REDIS_URL=redis://localhost:6379/0
CHALLENGE_TTL_SECONDS=120

# FIDO Metadata Service
FIDO_MDS_URL=https://mds3.fidoalliance.org
FIDO_MDS_TOKEN=<your_mds_access_token>
FIDO_MDS_CACHE_TTL=86400
```

## === FILE: 51-passkeys-config-schemas.md ===
# Passkeys Configuration Schemas Reference

## 1. PublicKeyCredentialCreationOptions Schema

The complete JSON schema for the registration options object:

```json
{
  "publicKey": {
    "rp": {
      "id": "string (registrable domain, e.g., 'example.com')",
      "name": "string (human-readable RP name, e.g., 'Example Corp')"
    },
    "user": {
      "id": "BufferSource (max 64 bytes, opaque user handle)",
      "name": "string (username or email for display)",
      "displayName": "string (friendly name, e.g., 'Jane Doe')"
    },
    "challenge": "BufferSource (min 16 bytes, cryptographically random)",
    "pubKeyCredParams": [
      { "type": "public-key", "alg": -7 },
      { "type": "public-key", "alg": -257 },
      { "type": "public-key", "alg": -8 }
    ],
    "timeout": "unsigned long (milliseconds, recommended: 60000-300000)",
    "excludeCredentials": [
      {
        "type": "public-key",
        "id": "BufferSource (credential ID)",
        "transports": ["internal", "hybrid", "usb", "ble", "nfc"]
      }
    ],
    "authenticatorSelection": {
      "authenticatorAttachment": "platform | cross-platform | (omit for any)",
      "residentKey": "required | preferred | discouraged",
      "requireResidentKey": "boolean (deprecated, use residentKey)",
      "userVerification": "required | preferred | discouraged"
    },
    "attestation": "none | indirect | direct | enterprise",
    "attestationFormats": ["packed", "tpm", "android-key", "apple", "fido-u2f", "none"],
    "extensions": {
      "credProps": true,
      "minPinLength": true,
      "credBlob": "BufferSource (max 32 bytes)",
      "largeBlob": { "support": "required | preferred" },
      "prf": { "eval": { "first": "BufferSource", "second": "BufferSource" } }
    }
  }
}
```

## 2. PublicKeyCredentialRequestOptions Schema

```json
{
  "publicKey": {
    "challenge": "BufferSource (min 16 bytes, cryptographically random)",
    "rpId": "string (registrable domain, defaults to current origin's effective domain)",
    "timeout": "unsigned long (milliseconds)",
    "allowCredentials": [
      {
        "type": "public-key",
        "id": "BufferSource (credential ID)",
        "transports": ["internal", "hybrid", "usb", "ble", "nfc"]
      }
    ],
    "userVerification": "required | preferred | discouraged",
    "extensions": {
      "appid": "string (legacy U2F AppID for backward compatibility)",
      "getCredBlob": true,
      "largeBlob": { "read": true },
      "prf": { "eval": { "first": "BufferSource", "second": "BufferSource" } }
    }
  },
  "mediation": "conditional | optional | required | silent"
}
```

## 3. Credential Storage Schema (Database)

### 3.1 PostgreSQL Schema

```sql
CREATE TABLE webauthn_credentials (
    -- Primary key
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Foreign key to users table
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    
    -- WebAuthn credential data
    credential_id BYTEA NOT NULL,
    public_key BYTEA NOT NULL,
    public_key_algorithm INTEGER NOT NULL DEFAULT -7,
    sign_count BIGINT NOT NULL DEFAULT 0,
    
    -- Transport hints
    transports TEXT[] NOT NULL DEFAULT '{}',
    
    -- Backup state (WebAuthn Level 2+)
    backup_eligible BOOLEAN NOT NULL DEFAULT false,
    backup_state BOOLEAN NOT NULL DEFAULT false,
    
    -- Authenticator metadata
    authenticator_attachment TEXT CHECK (authenticator_attachment IN ('platform', 'cross-platform')),
    aaguid UUID,
    
    -- User-facing metadata
    device_name TEXT NOT NULL DEFAULT 'Unknown Device',
    
    -- Lifecycle timestamps
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    last_used_at TIMESTAMPTZ,
    revoked_at TIMESTAMPTZ,
    
    -- Constraints
    CONSTRAINT unique_credential_id UNIQUE (credential_id),
    CONSTRAINT valid_algorithm CHECK (public_key_algorithm IN (-7, -8, -35, -36, -257, -258, -259))
);

-- Performance indexes
CREATE INDEX idx_cred_user_id ON webauthn_credentials(user_id) WHERE revoked_at IS NULL;
CREATE INDEX idx_cred_credential_id ON webauthn_credentials(credential_id) WHERE revoked_at IS NULL;
CREATE INDEX idx_cred_last_used ON webauthn_credentials(last_used_at) WHERE revoked_at IS NULL;
```

### 3.2 MongoDB Schema

```javascript
{
  $jsonSchema: {
    bsonType: "object",
    required: ["userId", "credentialId", "publicKey", "algorithm", "signCount", "createdAt"],
    properties: {
      userId: { bsonType: "objectId" },
      credentialId: { bsonType: "binData" },
      publicKey: { bsonType: "binData" },
      algorithm: { bsonType: "int", enum: [-7, -8, -35, -36, -257, -258, -259] },
      signCount: { bsonType: "long", minimum: 0 },
      transports: { bsonType: "array", items: { bsonType: "string" } },
      backupEligible: { bsonType: "bool" },
      backupState: { bsonType: "bool" },
      authenticatorAttachment: { bsonType: "string", enum: ["platform", "cross-platform"] },
      aaguid: { bsonType: "string" },
      deviceName: { bsonType: "string" },
      createdAt: { bsonType: "date" },
      lastUsedAt: { bsonType: "date" },
      revokedAt: { bsonType: "date" }
    }
  }
}
```

## 4. COSE Key Format Reference

### 4.1 ES256 (ECDSA with P-256 and SHA-256)

```cbor
{
  1: 2,        // kty: EC2
  3: -7,       // alg: ES256
  -1: 1,       // crv: P-256
  -2: bytes,   // x-coordinate (32 bytes)
  -3: bytes    // y-coordinate (32 bytes)
}
```

### 4.2 RS256 (RSASSA-PKCS1-v1_5 with SHA-256)

```cbor
{
  1: 3,        // kty: RSA
  3: -257,     // alg: RS256
  -1: bytes,   // n (modulus, 256 bytes for RSA-2048)
  -2: bytes    // e (exponent, typically 3 bytes: 01 00 01)
}
```

### 4.3 EdDSA (Ed25519)

```cbor
{
  1: 1,        // kty: OKP
  3: -8,       // alg: EdDSA
  -1: 6,       // crv: Ed25519
  -2: bytes    // x (public key, 32 bytes)
}
```

## 5. AuthenticatorData Format

```
+------------------+------+------+------+------+------------------+------------------+
| rpIdHash (32B)   | flags| signCount    | attestedCredData   | extensions (CBOR) |
+------------------+------+------+------+------+------------------+------------------+

Flags byte (bit field):
  Bit 0 (UP): User Present
  Bit 2 (UV): User Verified
  Bit 3 (BE): Backup Eligible
  Bit 4 (BS): Backup State
  Bit 6 (AT): Attested Credential Data present
  Bit 7 (ED): Extension Data present

Attested Credential Data (only in registration):
  +----------+-------------------+-------------------+
  | aaguid   | credentialIdLen   | credentialId      | credentialPublicKey (COSE) |
  | (16B)    | (2B, big-endian)  | (variable)        | (variable CBOR)            |
  +----------+-------------------+-------------------+
```

## 6. ClientDataJSON Schema

```json
{
  "type": "webauthn.create | webauthn.get",
  "challenge": "base64url-encoded challenge",
  "origin": "https://example.com",
  "crossOrigin": false,
  "tokenBinding": {
    "status": "present | supported | not-supported",
    "id": "base64url-encoded token binding ID"
  }
}
```

## 7. Server Configuration Templates

### 7.1 Node.js (SimpleWebAuthn)

```javascript
// config/webauthn.js
module.exports = {
  rpName: process.env.WEBAUTHN_RP_NAME || 'My Application',
  rpID: process.env.WEBAUTHN_RP_ID || 'example.com',
  origin: process.env.WEBAUTHN_ORIGIN || 'https://example.com',
  challengeTTL: parseInt(process.env.CHALLENGE_TTL || '120', 10),
  timeout: parseInt(process.env.WEBAUTHN_TIMEOUT || '60000', 10),
  attestation: process.env.WEBAUTHN_ATTESTATION || 'none',
  userVerification: process.env.WEBAUTHN_UV || 'required',
  residentKey: process.env.WEBAUTHN_RK || 'required',
  algorithms: [-7, -257], // ES256, RS256
};
```

### 7.2 Python (py_webauthn)

```python
# config/webauthn.py
import os

WEBAUTHN_CONFIG = {
    "rp_id": os.getenv("WEBAUTHN_RP_ID", "example.com"),
    "rp_name": os.getenv("WEBAUTHN_RP_NAME", "My Application"),
    "origin": os.getenv("WEBAUTHN_ORIGIN", "https://example.com"),
    "challenge_ttl": int(os.getenv("CHALLENGE_TTL", "120")),
    "timeout": int(os.getenv("WEBAUTHN_TIMEOUT", "60000")),
    "attestation": os.getenv("WEBAUTHN_ATTESTATION", "none"),
    "user_verification": os.getenv("WEBAUTHN_UV", "required"),
    "resident_key": os.getenv("WEBAUTHN_RK", "required"),
}
```

### 7.3 Go (go-webauthn)

```go
// config/webauthn.go
package config

import (
    "github.com/go-webauthn/webauthn/webauthn"
)

func NewWebAuthnConfig() *webauthn.Config {
    return &webauthn.Config{
        RPDisplayName: getEnv("WEBAUTHN_RP_NAME", "My Application"),
        RPID:          getEnv("WEBAUTHN_RP_ID", "example.com"),
        RPOrigins:     []string{getEnv("WEBAUTHN_ORIGIN", "https://example.com")},
        Timeouts: webauthn.TimeoutsConfig{
            Login: webauthn.TimeoutConfig{
                Enforce: true,
                Timeout: 60 * time.Second,
            },
            Registration: webauthn.TimeoutConfig{
                Enforce: true,
                Timeout: 60 * time.Second,
            },
        },
    }
}
```

## 8. Well-Known Files

### 8.1 Related Origins (WebAuthn Level 3)

File: `https://<rp-id>/.well-known/webauthn`

```json
{
  "origins": [
    "https://login.example.com",
    "https://auth.example.com",
    "https://app.example.com"
  ]
}
```

### 8.2 Apple App Site Association

File: `https://<rp-id>/.well-known/apple-app-site-association`

```json
{
  "webcredentials": {
    "apps": [
      "TEAMID.com.example.myapp"
    ]
  }
}
```

### 8.3 Android Digital Asset Links

File: `https://<rp-id>/.well-known/assetlinks.json`

```json
[
  {
    "relation": ["delegate_permission/common.get_login_creds"],
    "target": {
      "namespace": "android_app",
      "package_name": "com.example.myapp",
      "sha256_cert_fingerprints": [
        "AA:BB:CC:DD:EE:FF:..."
      ]
    }
  }
]
```

## 9. FIDO Metadata Service (MDS) Response Schema

```json
{
  "aaguid": "00000000-0000-0000-0000-000000000000",
  "description": "Authenticator Model Name",
  "authenticatorVersion": 5,
  "protocolFamily": "fido2",
  "schema": 3,
  "upv": [{ "major": 1, "minor": 1 }],
  "authenticationAlgorithms": ["secp256r1_ecdsa_sha256_raw"],
  "publicKeyAlgAndEncodings": ["cose"],
  "attestationTypes": ["basic_full"],
  "userVerificationDetails": [
    [{ "userVerificationMethod": "fingerprint_internal" }],
    [{ "userVerificationMethod": "passcode_internal" }]
  ],
  "keyProtection": ["hardware", "secure_element"],
  "matcherProtection": ["on_chip"],
  "cryptoStrength": 128,
  "attachmentHint": ["internal"],
  "tcDisplay": [],
  "attestationRootCertificates": ["MIIBfz..."],
  "statusReports": [
    {
      "status": "FIDO_CERTIFIED_L2",
      "effectiveDate": "2024-01-15",
      "certificationDescriptor": "FIDO2 L2"
    }
  ]
}
```

## === FILE: 51-passkeys-deep-dive.md ===
# Passkeys Deep Dive: Internals and Architecture

## 1. Cryptographic Foundations

### 1.1 Public Key Cryptography in WebAuthn

Passkeys are built on asymmetric (public key) cryptography. During registration, the authenticator generates a key pair: a private key that never leaves the secure hardware, and a public key that is sent to the relying party for storage.

During authentication, the relying party sends a challenge. The authenticator signs the challenge (along with additional context data) using the private key. The relying party verifies the signature using the stored public key. If the signature is valid, the user is authenticated.

The critical security property is that possession of the public key provides zero advantage in forging signatures. Even if the relying party's database is completely compromised, the attacker cannot impersonate users because they lack the private keys.

### 1.2 Supported Algorithms

**ES256 (ECDSA with P-256 and SHA-256):** The most widely supported algorithm. Uses the NIST P-256 elliptic curve. Key size: 256-bit private key, 512-bit public key (x + y coordinates). Signature size: ~64 bytes. Performance: fast on hardware with ECC acceleration.

**RS256 (RSASSA-PKCS1-v1_5 with SHA-256):** Legacy algorithm primarily supported for backward compatibility with older Windows Hello implementations. Key size: 2048-bit minimum. Signature size: 256 bytes. Performance: slower than ES256, larger keys and signatures.

**EdDSA (Ed25519):** Modern algorithm with excellent performance and small key/signature sizes. Not yet universally supported by all authenticators but gaining adoption. Key size: 256-bit. Signature size: 64 bytes. Performance: fastest of the three.

### 1.3 The Signature Verification Process

During authentication, the signed data is constructed as:

```
signedData = authenticatorData || SHA-256(clientDataJSON)
```

The `authenticatorData` contains the RP ID hash (proving the credential is for this domain), flags (UP, UV, BE, BS), and the sign counter. The `clientDataJSON` contains the challenge, origin, and type. By signing both together, the authenticator cryptographically binds the authentication to a specific challenge from a specific origin.

The server verifies:
1. Parse `clientDataJSON` and verify `type`, `challenge`, and `origin`
2. Compute `SHA-256(clientDataJSON)`
3. Concatenate `authenticatorData || hash`
4. Verify the signature over this concatenation using the stored public key

## 2. Authenticator Architecture

### 2.1 Platform Authenticators

Platform authenticators are built into the device's operating system and hardware. They leverage the device's secure enclave (Apple), Trusted Platform Module (Windows), or Titan M chip (Android) to generate and store private keys.

**Apple Secure Enclave:** A dedicated hardware security processor present in all modern Apple devices. Private keys are generated inside the Secure Enclave and never leave it. The Secure Enclave performs all cryptographic operations internally, only outputting the resulting signature. Even the main processor cannot access the raw key material.

**Windows TPM (Trusted Platform Module):** A dedicated security chip (or firmware-based equivalent) that stores keys in hardware-protected storage. Windows Hello uses the TPM to generate and protect passkey private keys. The TPM provides attestation capabilities that can prove the key was generated in certified hardware.

**Android Hardware Security Module:** Modern Android devices use a dedicated security chip (Titan M on Pixel, Samsung Knox Vault on Galaxy) or ARM TrustZone to protect key material. The Android Keystore API provides access to hardware-backed key storage.

### 2.2 Roaming Authenticators

Roaming authenticators are external devices that communicate with the client via USB, NFC, or BLE. The most common examples are YubiKeys and other FIDO2 security keys.

**CTAP2 Protocol:** Communication between the client (browser/OS) and the roaming authenticator uses the Client to Authenticator Protocol version 2 (CTAP2). This protocol defines commands for making credentials, getting assertions, managing PINs, and querying authenticator capabilities.

**Transport Protocols:**
- USB HID: Direct wired connection, fastest and most reliable
- NFC: Contactless, requires physical proximity (< 4cm)
- BLE: Wireless, used for hybrid/cross-device flows
- Internal: Platform authenticator (no external transport)

### 2.3 Synced vs. Device-Bound Credentials

**Device-Bound Credentials:** The private key exists on exactly one device and cannot be exported or backed up. If the device is lost, the credential is permanently lost. Provides the highest security guarantee (AAL3 eligible) but worst recovery story.

**Synced Credentials (Passkeys):** The private key is encrypted and synchronized across devices via a cloud service (iCloud Keychain, Google Password Manager, or third-party managers). Provides excellent usability (survives device loss) but the security depends on the cloud account's protection.

The `BE` (Backup Eligible) flag in authenticatorData indicates whether the credential CAN be synced. The `BS` (Backup State) flag indicates whether it IS currently backed up. These flags allow relying parties to make policy decisions based on the credential's backup status.

## 3. The Hybrid Transport Protocol (Cross-Device)

### 3.1 Protocol Overview

The hybrid transport protocol enables authentication using a smartphone when the user is signing in on a different device (e.g., a laptop). The protocol uses a combination of QR codes, BLE advertisements, and a cloud relay to establish a secure channel.

### 3.2 Flow Sequence

1. **QR Code Generation:** The client device (laptop) generates a QR code containing a one-time pairing key and the cloud relay's endpoint URL.

2. **QR Code Scanning:** The user scans the QR code with their smartphone's camera.

3. **BLE Proximity Verification:** The smartphone broadcasts a BLE advertisement. The laptop detects this advertisement, confirming that both devices are in physical proximity (preventing remote relay attacks).

4. **Cloud Relay Connection:** Both devices connect to the cloud relay service via WebSocket. The relay facilitates encrypted communication between the devices.

5. **CTAP2 Tunnel:** A CTAP2 session is established over the encrypted tunnel. The laptop sends the WebAuthn request through the tunnel to the smartphone.

6. **User Verification:** The smartphone prompts the user for biometric verification (Face ID, fingerprint).

7. **Assertion Return:** The signed assertion is sent back through the tunnel to the laptop, which forwards it to the relying party.

### 3.3 Security Properties

The hybrid protocol provides:
- **Proximity binding:** BLE ensures devices are physically close
- **End-to-end encryption:** The cloud relay cannot read the CTAP2 messages
- **One-time pairing:** Each QR code is single-use
- **No persistent pairing required:** (Unlike legacy BLE pairing)

## 4. Conditional UI (Autofill) Internals

### 4.1 Browser Implementation

When a page calls `navigator.credentials.get()` with `mediation: "conditional"`, the browser enters a special mode:

1. The browser does NOT immediately show a modal dialog.
2. Instead, it queries the credential manager for discoverable credentials matching the RP ID.
3. If matching credentials exist, they are added to the autofill dropdown of any input field with `autocomplete="username webauthn"`.
4. The Promise remains pending until the user either selects a credential from the dropdown or the page calls `abort()`.
5. When the user selects a credential, the browser prompts for biometric verification and resolves the Promise with the assertion.

### 4.2 Implementation Requirements

For Conditional UI to work correctly:
- The `navigator.credentials.get()` call must be made on page load (not in a click handler)
- Only one conditional request can be active at a time
- The input field must have the `webauthn` token in its `autocomplete` attribute
- The page must check `PublicKeyCredential.isConditionalMediationAvailable()` before attempting

### 4.3 Abort Controller Pattern

```javascript
let abortController = new AbortController();

// Start conditional UI on page load
async function startConditionalUI() {
  try {
    const assertion = await navigator.credentials.get({
      publicKey: { challenge, rpId, userVerification: "required" },
      mediation: "conditional",
      signal: abortController.signal
    });
    // User selected a passkey from autofill
    await verifyAssertion(assertion);
  } catch (e) {
    if (e.name === "AbortError") {
      // Request was aborted (user clicked explicit login button)
    }
  }
}

// If user clicks "Sign in with passkey" button explicitly
function onExplicitPasskeyClick() {
  abortController.abort(); // Cancel conditional UI
  abortController = new AbortController(); // Create new controller
  // Start modal (non-conditional) WebAuthn flow
  navigator.credentials.get({
    publicKey: { challenge, rpId, userVerification: "required" },
    signal: abortController.signal
  });
}
```

## 5. Attestation Internals

### 5.1 Attestation Object Structure

The attestation object returned during registration is a CBOR-encoded map:

```cbor
{
  "fmt": "packed",           // Attestation format
  "attStmt": {              // Attestation statement (format-specific)
    "alg": -7,             // Algorithm used to sign
    "sig": bytes,          // Signature over authData || clientDataHash
    "x5c": [bytes]         // Certificate chain (optional)
  },
  "authData": bytes         // Authenticator data (contains public key)
}
```

### 5.2 Attestation Formats

**Packed:** The most common format for FIDO2 authenticators. Can be self-attestation (no certificate, the credential key signs itself) or full attestation (includes a manufacturer certificate chain).

**TPM:** Used by Windows Hello when the device has a TPM. Includes TPM-specific structures (TPMS_ATTEST, TPMT_SIGNATURE) that prove the key was generated in a certified TPM.

**Android Key:** Used by Android devices with hardware-backed keystores. Includes a certificate chain rooted in Google's hardware attestation root CA.

**Apple:** Used by Apple devices. Includes a certificate chain rooted in Apple's WebAuthn root CA. The attestation proves the key was generated in the Secure Enclave.

**FIDO U2F:** Legacy format for backward compatibility with U2F authenticators. Contains a simple ECDSA signature and a single attestation certificate.

**None:** No attestation provided. The relying party receives no proof of the authenticator's provenance. This is the recommended default for consumer applications.

## 6. The FIDO Alliance Ecosystem

### 6.1 Standards Hierarchy

```
W3C WebAuthn (Browser API)
    ↕
FIDO2 (Umbrella specification)
    ├── CTAP2 (Client to Authenticator Protocol)
    ├── CTAP2.1 (PIN/UV, credential management)
    └── CTAP2.2 (Hybrid transport, enterprise attestation)
    
FIDO UAF (Legacy mobile biometric)
FIDO U2F (Legacy second-factor, predecessor to FIDO2)
```

### 6.2 Certification Levels

**Level 1 (L1):** Software-only implementation. No hardware security requirements. Suitable for platform authenticators on devices without secure enclaves.

**Level 2 (L2):** Restricted Operating Environment. The authenticator must run in a trusted execution environment (TEE) or equivalent isolation.

**Level 3 (L3):** Hardware-based security. The authenticator must use dedicated security hardware (secure element, TPM) for key storage and cryptographic operations.

**Level 3+ (L3+):** Enhanced hardware security with additional physical attack resistance (side-channel protection, tamper detection).

## 7. WebAuthn Level 3 New Features

### 7.1 Signal Methods

WebAuthn Level 3 introduces signal methods that allow relying parties to communicate credential state changes to the client/authenticator:

- `signalUnknownCredential()`: Tells the credential manager that a credential ID is not recognized by the RP (useful for cleaning up stale credentials)
- `signalAllAcceptedCredentials()`: Tells the credential manager which credentials the RP still recognizes for a user (allows cleanup of revoked credentials)
- `signalCurrentUserDetails()`: Updates the credential manager with the user's current name/displayName

### 7.2 PRF Extension (Pseudo-Random Function)

The PRF extension allows the relying party to derive symmetric keys from the passkey authentication process. This enables use cases like end-to-end encryption where the encryption key is derived from the passkey itself, without the relying party ever seeing the key.

### 7.3 Supplemental Public Keys

Allows an authenticator to generate additional key pairs during registration that can be used for purposes other than authentication (e.g., signing documents, encrypting data).

## 8. Performance Characteristics

### 8.1 Cryptographic Operation Timing

| Operation | Hardware (Secure Enclave) | Software (WebCrypto) |
|-----------|--------------------------|---------------------|
| ES256 Key Generation | 50-200ms | 5-20ms |
| ES256 Sign | 20-100ms | 2-10ms |
| ES256 Verify | N/A (server-side) | 1-5ms |
| RS256 Key Generation | 500-2000ms | 100-500ms |
| RS256 Sign | 50-200ms | 10-50ms |
| RS256 Verify | N/A (server-side) | 1-3ms |

### 8.2 End-to-End Latency Breakdown

| Phase | Duration | Notes |
|-------|----------|-------|
| Options request (network) | 50-200ms | Server generates challenge |
| Browser UI rendering | 100-500ms | Modal or conditional UI |
| User biometric gesture | 500-3000ms | Depends on user speed |
| Authenticator crypto | 50-200ms | Key generation or signing |
| Assertion response (network) | 50-200ms | Server verifies |
| Server verification | 1-10ms | Signature check + DB lookup |
| **Total (platform, happy path)** | **1-4 seconds** | |
| **Total (cross-device/hybrid)** | **8-30 seconds** | Includes QR scan + BLE |

## 9. Credential Lifecycle Management

### 9.1 State Machine

```
[Created] → [Active] → [Revoked]
                ↑           ↓
                └── [Suspended] (temporary disable)
```

### 9.2 Lifecycle Events

| Event | Trigger | Action |
|-------|---------|--------|
| Creation | User completes registration | Store credential, set active |
| Authentication | User signs in | Update last_used_at, increment sign_count |
| Rename | User changes device name | Update device_name |
| Suspend | Admin action or policy | Set suspended flag, reject assertions |
| Revoke | User deletes, admin action, or compromise | Set revoked_at, permanently reject |
| Cleanup | Credential unused for 12+ months | Notify user, suggest removal |

### 9.3 Credential Recovery

When a user loses access to all their passkeys (lost all devices, cloud account compromised), the relying party must provide an alternative recovery path. Common approaches:

1. **Recovery codes:** Pre-generated one-time codes stored offline by the user
2. **Email/SMS verification:** Lower security but widely available
3. **Identity verification:** Manual process involving ID documents (highest friction, highest assurance)
4. **Trusted contact:** Another verified user vouches for the account owner

The recovery flow must be carefully designed to resist social engineering while remaining accessible to legitimate users who have genuinely lost access.

## === FILE: 51-passkeys-security-audit.md ===
# Passkeys Security Audit Guide

## 1. Threat Model

### 1.1 Threats Mitigated by Passkeys

**Phishing:** Passkeys are cryptographically bound to the RP ID (domain). Even if a user visits a convincing phishing site (`examp1e.com`), the browser will not offer credentials registered for `example.com`. The private key never leaves the authenticator, so there is nothing to steal.

**Credential Stuffing:** Passkeys eliminate shared secrets. There is no password to reuse across sites. Each credential is unique to the relying party.

**Server-Side Breach:** The server stores only public keys. If the credentials database is compromised, attackers obtain public keys that cannot be used to impersonate users. This is fundamentally different from password hashes, which can be cracked offline.

**Man-in-the-Middle:** The `origin` field in `clientDataJSON` is set by the browser and cannot be spoofed. The server verifies that the origin matches its expected value, detecting any interception.

**Replay Attacks:** Each authentication ceremony uses a fresh, single-use challenge. Replaying a captured assertion will fail because the challenge will not match.

### 1.2 Residual Threats

**Social Engineering:** An attacker may convince a user to register a passkey on the attacker's device (e.g., by gaining physical access during registration). Mitigate with session binding and out-of-band confirmation.

**Malware on Endpoint:** If the user's device is compromised with a keylogger or screen-capture malware, the attacker may be able to observe the authentication flow. However, they still cannot extract the private key from the secure enclave.

**Synced Passkey Compromise:** If a user's cloud account (Apple ID, Google Account) is compromised, the attacker gains access to all synced passkeys. Mitigate by requiring device-bound credentials for high-risk operations.

**Authenticator Vulnerabilities:** Hardware or firmware vulnerabilities in specific authenticator models may allow key extraction. Monitor the FIDO MDS for security advisories.

## 2. Registration Security Checklist

| # | Check | Risk if Missing | Priority |
|---|-------|-----------------|----------|
| 1 | Challenge is cryptographically random (≥16 bytes) | Replay attacks | CRITICAL |
| 2 | Challenge is single-use (deleted after verification) | Replay attacks | CRITICAL |
| 3 | Challenge has short TTL (60-300 seconds) | Extended attack window | HIGH |
| 4 | RP ID is correctly set to registrable domain | All credentials bound to wrong domain | CRITICAL |
| 5 | User ID is opaque (not email or username) | Information leakage | MEDIUM |
| 6 | `excludeCredentials` prevents duplicate registration | Credential confusion | MEDIUM |
| 7 | Origin is verified against expected values | MitM attacks | CRITICAL |
| 8 | Attestation is verified if required by policy | Unauthorized authenticator types | VARIES |
| 9 | User is authenticated before registering additional credentials | Credential hijacking | HIGH |
| 10 | Transports are stored for future `allowCredentials` | UX degradation | LOW |
| 11 | Backup eligibility flags (BE/BS) are stored | Cannot enforce device-bound policies | MEDIUM |
| 12 | Public key algorithm is validated against allowed list | Algorithm downgrade | HIGH |

## 3. Authentication Security Checklist

| # | Check | Risk if Missing | Priority |
|---|-------|-----------------|----------|
| 1 | Challenge is fresh and single-use | Replay attacks | CRITICAL |
| 2 | Origin matches expected value(s) | MitM, phishing | CRITICAL |
| 3 | RP ID hash in authenticatorData matches expected | Cross-site credential use | CRITICAL |
| 4 | Signature is cryptographically verified | Complete authentication bypass | CRITICAL |
| 5 | User Presence (UP) flag is set | Automated attacks without user | HIGH |
| 6 | User Verification (UV) flag is set (if required) | Authentication without biometric | HIGH |
| 7 | Sign count is validated (for device-bound credentials) | Credential cloning | MEDIUM |
| 8 | Credential is not revoked | Use of compromised credential | HIGH |
| 9 | User handle matches expected user | Account confusion | CRITICAL |
| 10 | Type field is "public-key" | Protocol confusion | LOW |

## 4. Configuration Security

### 4.1 RP ID Configuration

The RP ID MUST be set to the most restrictive value possible. If the application is served exclusively from `app.example.com`, the RP ID should be `app.example.com`, not `example.com`. Using the broader domain allows any subdomain to potentially use the credentials, expanding the attack surface.

However, if the application needs credentials to work across multiple subdomains (e.g., `app.example.com` and `admin.example.com`), the RP ID must be set to the common parent domain (`example.com`).

### 4.2 User Verification Policy

| Context | Recommended Setting | Rationale |
|---------|-------------------|-----------|
| Standard login | `required` | Ensures biometric/PIN verification |
| Step-up authentication | `required` | Must prove user presence |
| Low-risk operations | `preferred` | Allows graceful degradation |
| Never use | `discouraged` | Removes the multi-factor benefit |

### 4.3 Attestation Policy

| Context | Recommended Setting | Rationale |
|---------|-------------------|-----------|
| Consumer applications | `none` | Maximum compatibility, no privacy concerns |
| Enterprise (standard) | `none` or `indirect` | Balance of security and compatibility |
| Enterprise (high security) | `direct` | Verify authenticator provenance |
| Government/regulated | `enterprise` | Full device identification |

## 5. Data Protection

### 5.1 Stored Credential Data Classification

| Field | Sensitivity | Protection Required |
|-------|-------------|-------------------|
| credential_id | LOW | Standard database security |
| public_key | LOW | Standard database security (public by definition) |
| user_id (handle) | MEDIUM | Should be opaque, not PII |
| sign_count | LOW | Standard database security |
| transports | LOW | Standard database security |
| aaguid | LOW | Reveals authenticator model |
| created_at / last_used_at | MEDIUM | Usage patterns, encrypt at rest |

### 5.2 Data Minimization

The relying party should store only the minimum data required for authentication. Do not store the full attestation object after verification (unless required for audit). Do not store clientDataJSON after verification. Do not log raw assertion data in application logs.

### 5.3 Backup and Recovery

The credentials table is the single most critical table for authentication. If lost, ALL users lose access via passkeys. Requirements:
- Point-in-time recovery (PITR) enabled
- Cross-region replication for disaster recovery
- Regular backup verification (restore and test)
- Encrypted backups at rest and in transit
- Retention policy aligned with credential lifecycle

## 6. Token and Session Security

### 6.1 Post-Authentication Session

After successful passkey verification, the server issues a session token. This session must be:
- Bound to the client (IP address, user agent, or device fingerprint)
- Short-lived with refresh capability
- Invalidated on logout, password change, or credential revocation
- Stored securely (HttpOnly, Secure, SameSite=Strict cookies)

### 6.2 API Token Security for WebAuthn Endpoints

The registration endpoint MUST require an existing authenticated session (the user must already be logged in to add a passkey). The authentication endpoint is public by nature but must be rate-limited to prevent enumeration attacks.

## 7. Rate Limiting and Abuse Prevention

| Endpoint | Rate Limit | Rationale |
|----------|-----------|-----------|
| `/webauthn/authenticate/options` | 10 req/min per IP | Prevent challenge exhaustion |
| `/webauthn/authenticate/verify` | 5 req/min per credential | Prevent brute-force |
| `/webauthn/register/options` | 3 req/min per user | Prevent credential spam |
| `/webauthn/register/verify` | 3 req/min per user | Prevent credential spam |

## 8. Compliance Mapping

### 8.1 NIST SP 800-63B (Digital Identity Guidelines)

| AAL Level | Passkey Configuration | Requirements Met |
|-----------|----------------------|-----------------|
| AAL1 | Any passkey, UV: discouraged | Single-factor cryptographic |
| AAL2 | Passkey with UV: required | Multi-factor cryptographic (something you have + something you are) |
| AAL3 | Device-bound passkey + attestation + hardware key | Hardware-bound multi-factor with verifier impersonation resistance |

### 8.2 PCI DSS 4.0

Passkeys satisfy PCI DSS 4.0 Requirement 8.3 (multi-factor authentication) when configured with `userVerification: required`. The biometric constitutes "something you are" and the private key in the secure enclave constitutes "something you have."

### 8.3 GDPR Considerations

Passkeys are privacy-preserving by design. The credential ID is a random value that does not reveal user identity across relying parties. No biometric data leaves the device. However, the relying party must still document the processing of credential metadata (creation time, last used time, authenticator model) in their Records of Processing Activities.

## 9. Incident Response Procedures

### 9.1 Suspected Credential Compromise

1. Immediately revoke the affected credential (set `revoked_at` timestamp)
2. Notify the user via out-of-band channel (email, SMS)
3. Force re-authentication via alternative method
4. Prompt user to register new credentials
5. Review access logs for unauthorized activity during the compromise window
6. If clone detection triggered: investigate all sessions authenticated with that credential

### 9.2 Mass Credential Database Breach

1. Assess impact: public keys alone cannot be used for authentication
2. However, credential IDs and user mappings are exposed
3. Rotate all active sessions
4. Notify affected users (regulatory requirement in most jurisdictions)
5. Consider: if attestation data was stored, authenticator models are exposed
6. No need to force credential re-registration (public keys are not secrets)

### 9.3 Authenticator Model Vulnerability (FIDO MDS Advisory)

1. Query the FIDO MDS for the affected AAGUID
2. Identify all credentials in the database with the matching AAGUID
3. Assess severity based on the MDS advisory
4. For critical vulnerabilities: proactively notify affected users and prompt re-registration
5. For moderate vulnerabilities: add monitoring and require step-up for sensitive operations

## === FILE: 51-passkeys-specialist.md ===
# Passkeys Master Specialist

## 1. Role Definition and Expertise

The Passkeys Master Specialist possesses comprehensive knowledge of the FIDO2 and WebAuthn (Web Authentication) standards, covering the complete lifecycle of passkey implementation, registration, authentication, and recovery. This specialist guides engineering and security teams through the transition from password-based systems to modern passwordless architectures. Expertise includes cryptography fundamentals, conditional UI implementation, synced versus device-bound credentials, enterprise deployment strategies, NIST AAL2/AAL3 compliance, and the intricacies of the WebAuthn Level 3 specification.

This specialist ensures that authentication flows are not only highly secure and phishing-resistant but also optimized for user adoption and conversion. By applying business rules, UX best practices, and fallback mechanisms, the specialist helps organizations achieve the documented performance benefits of passkeys: significantly faster login times, dramatic reductions in help desk tickets, and substantial improvements in authentication success rates.

## 2. Core Architecture and Standards

Passkeys represent a fundamental shift in how digital identity is verified, moving away from shared secrets toward public-key cryptography. This architecture is governed by a set of interconnected standards that define how devices communicate with browsers and how browsers communicate with relying parties.

### 2.1 The Standards Framework

The passkey ecosystem is built upon three primary pillars that work in concert:

The **FIDO2** framework serves as the umbrella standard created by the FIDO Alliance. It defines the overall architecture for passwordless authentication, ensuring that credentials are mathematically bound to specific domains and resistant to phishing attacks. FIDO2 encompasses both the web-facing APIs and the hardware communication protocols.

**WebAuthn (Web Authentication)** is the W3C standard that defines the JavaScript API used by web applications to create and manage public key credentials. WebAuthn operates at the application layer, providing the `navigator.credentials.create()` and `navigator.credentials.get()` methods that browsers expose to websites. The recently published WebAuthn Level 3 Candidate Recommendation (January 2026) formalizes multi-device credential behaviors, introduces JSON serialization helpers, and standardizes client capability detection.

**CTAP (Client to Authenticator Protocol)**, currently at version 2.2, defines how the browser or operating system communicates with the authenticator hardware. Whether the authenticator is a built-in secure enclave (platform authenticator) or an external security key connected via USB, NFC, or Bluetooth (roaming authenticator), CTAP handles the secure transmission of challenges and cryptographic signatures between the client device and the secure hardware.

### 2.2 Cryptographic Foundation

The security model of passkeys relies entirely on asymmetric cryptography. When a user registers a passkey, the authenticator generates a unique public-private key pair specifically for that relying party.

The private key remains securely stored within the authenticator's secure enclave or is encrypted and synchronized through a cloud provider's keychain infrastructure. It is never transmitted across the network, never stored on the relying party's servers, and cannot be extracted by malicious software running on the host device.

The public key is transmitted to the relying party's server during the registration phase and stored in the application's database. During subsequent authentication attempts, the server generates a cryptographically secure random challenge. The authenticator signs this challenge using the private key, and the server verifies the signature using the stored public key.

This architecture eliminates the fundamental vulnerabilities of passwords. Because there is no shared secret stored on the server, a database breach yields only public keys, which are useless to an attacker. Because the credential is cryptographically bound to the relying party's exact domain (the RP ID), phishing sites cannot trick the authenticator into signing a challenge for a fraudulent domain.

## 3. Passkey Typology and Compliance

The passkey ecosystem categorizes credentials based on their storage mechanism and mobility. Understanding these distinctions is critical for meeting compliance requirements and designing appropriate recovery workflows.

### 3.1 Synced Passkeys (Multi-Device Credentials)

Synced passkeys are stored in a cloud-based keychain and automatically synchronized across all devices within a user's ecosystem. Major implementations include Apple iCloud Keychain, Google Password Manager, Windows Hello cloud backup, and third-party password managers like 1Password and Bitwarden.

These credentials provide consumer-grade user experience by ensuring that a passkey created on a smartphone is immediately available on the user's tablet and laptop. They survive device loss and hardware failure, significantly reducing the burden of account recovery.

From a compliance perspective, the finalization of NIST SP 800-63-4 in July 2025 formally recognized synced passkeys as meeting Authenticator Assurance Level 2 (AAL2). The standard acknowledges that the synchronization mechanism itself is protected by the cloud account's authentication, which typically requires a second factor. However, the security guarantee ultimately depends on the strength of the underlying cloud account; if a user's Apple ID or Google Account is compromised without MFA protection, the synced passkeys could potentially be accessed by an attacker.

### 3.2 Device-Bound Passkeys (Single-Device Credentials)

Device-bound passkeys are hardware-bound credentials that never leave the physical device where they were created. They are stored within the secure enclave of a smartphone or within dedicated hardware security keys such as YubiKeys or Google Titan Keys.

These credentials cannot be extracted, backed up, or synchronized. While this provides the highest level of security, it introduces significant operational overhead. Device loss equates to permanent credential loss, necessitating robust out-of-band recovery procedures or the registration of multiple backup keys.

Device-bound passkeys meet AAL2 requirements by default and can achieve AAL3—the highest assurance level—when combined with hardware attestation that proves the credential resides in an approved, certified hardware module. They are the required standard for highly privileged administrative access, critical financial infrastructure, and specific healthcare applications.

### 3.3 The Enterprise Hybrid Model

Extensive deployment data indicates that nearly half of enterprise organizations implement a hybrid model tailored to specific risk profiles. In this architecture, consumer-facing applications and standard employee productivity tools utilize synced passkeys to maximize adoption and minimize friction. Conversely, privileged access management, production infrastructure access, and highly regulated workflows mandate the use of device-bound passkeys, often deployed via smart cards or dedicated security tokens managed by the organization's PKI infrastructure.

## 4. Implementation Workflows

The implementation of passkeys requires coordination between the client application, the browser's WebAuthn API, and the relying party's backend server. The following sections detail the standard registration and authentication workflows.

### 4.1 The Registration Workflow

The registration process establishes the initial cryptographic relationship between the user's authenticator and the relying party.

The workflow begins when the client application requests registration options from the server. The server generates a cryptographic challenge, assigns a unique user identifier, and specifies the Relying Party ID (which must match the domain exactly). The server also defines parameters such as acceptable authenticator types and whether user verification (biometrics) is required or merely preferred. Crucially, the server provides an `excludeCredentials` list containing any passkeys already registered to the user, preventing the creation of duplicate credentials on the same authenticator.

The client receives these options and invokes `navigator.credentials.create()`. The browser intercepts this call, verifies the domain matches the RP ID, and prompts the user to authenticate using their platform or roaming authenticator. Upon successful biometric or PIN verification, the authenticator generates the key pair and returns an attestation object to the browser.

The client transmits this attestation object back to the server. The server must rigorously validate the response: it must verify that the challenge matches the one originally sent, confirm the origin matches the expected domain, validate the relying party ID hash, and verify the attestation signature. Once validated, the server extracts the credential ID, the public key, and the signature counter, storing them securely in the database alongside the user's record.

### 4.2 The Authentication Workflow

The authentication process verifies the user's identity by proving possession of the private key associated with the registered credential.

The client requests authentication options from the server. The server generates a new cryptographic challenge and provides the Relying Party ID. The server may optionally provide an `allowCredentials` list containing the specific credential IDs registered to the user, though this is often omitted when implementing discoverable credentials (resident keys) where the authenticator identifies the user based on the relying party domain.

The client invokes `navigator.credentials.get()` with these options. The browser prompts the user to authenticate, typically using biometric verification. The authenticator signs the challenge using the private key associated with the relying party and returns an assertion object containing the signature and authenticator data.

The client sends this assertion to the server. The server performs comprehensive validation: verifying the challenge, confirming the origin and RP ID, and ensuring the signature counter has incremented (to detect potential credential cloning). Finally, the server uses the stored public key to verify the cryptographic signature over the client data and authenticator data. Upon successful verification, the server issues a session token, completing the authentication process.

## 5. User Experience and Adoption Strategies

The technological superiority of passkeys is irrelevant if users fail to adopt them. Deployment data consistently demonstrates that user experience decisions dictate adoption rates. Organizations that treat passkeys as a primary authentication path achieve remarkable success, while those that bury passkeys in security settings see negligible enrollment.

### 5.1 Conditional UI (Autofill)

Conditional UI is the most critical feature for driving passkey adoption. Instead of requiring users to explicitly click a "Sign in with Passkey" button, Conditional UI integrates passkeys directly into the browser's native autofill mechanisms.

When implemented correctly, the browser detects the username input field and automatically suggests available passkeys in a dropdown menu, exactly as it does for saved passwords. The user selects their account, performs a biometric gesture, and is immediately authenticated. This creates a frictionless experience that requires zero typing and eliminates the cognitive load of remembering credentials.

Implementing Conditional UI requires adding the `mediation: "conditional"` parameter to the `navigator.credentials.get()` call as soon as the login page loads. The browser silently waits for the user to interact with the designated input field before presenting the passkey options. It is crucial to note that while Conditional UI provides the optimal experience, relying parties must always provide a fallback explicit button, as some older browsers or specific operating system configurations may not support the conditional mediation flow.

### 5.2 Enrollment Timing

The timing of passkey enrollment significantly impacts adoption metrics. The optimal strategy is to integrate passkey creation directly into the initial account registration flow. When users are prompted to create a passkey immediately after verifying their email address or phone number, adoption rates frequently exceed ninety percent.

Attempting to drive enrollment post-registration—such as prompting users during subsequent logins or relying on account settings pages—yields dramatically lower results. Users are focused on completing their intended tasks and view security prompts as interruptions. If post-registration enrollment is necessary, the most effective pattern is to prompt for passkey creation immediately following a successful biometric or high-friction authentication event, framing the passkey as a method to simplify future logins.

### 5.3 Communication and Microcopy

The terminology used to describe passkeys must be carefully considered. Most users do not understand public-key cryptography or the WebAuthn standard. Effective implementations avoid technical jargon and focus entirely on the user benefit and the physical action required.

Microcopy should emphasize convenience and security using familiar concepts. Phrases such as "Sign in with your fingerprint or face" or "Use your device to sign in safely" perform significantly better than technical explanations of cryptographic keys. The goal is to map the passkey experience to the biometric unlock process the user already performs dozens of times daily on their smartphone.
## 6. WebAuthn Level 3 Advancements

The WebAuthn Level 3 specification, which reached Candidate Recommendation status in January 2026, introduces several critical enhancements that formalize features previously treated as vendor-specific extensions. These advancements significantly improve the developer experience and the interoperability of passkey implementations.

### 6.1 Client Capability Detection

Prior to Level 3, relying parties had to employ complex heuristics and user-agent sniffing to determine if a browser supported specific passkey features. The new `getClientCapabilities()` method provides a standardized mechanism to query the browser's capabilities before initiating registration or authentication flows. This allows applications to dynamically adjust their user interface, offering conditional UI only when supported, or guiding users toward appropriate fallback mechanisms when passkeys are unavailable.

### 6.2 JSON Serialization Helpers

One of the most persistent pain points in WebAuthn development has been the requirement to convert between standard JSON and the binary ArrayBuffer formats required by the browser API. Level 3 introduces native JSON serialization helpers: `parseCreationOptionsFromJSON()` and `parseRequestOptionsFromJSON()`. These methods allow relying parties to transmit configuration options as standard JSON objects, significantly simplifying the client-side code and reducing the reliance on third-party decoding libraries.

### 6.3 Enhanced Signal Methods

Level 3 introduces new signal methods that allow relying parties to transmit contextual information to authenticators. This includes the ability to provide updated user details or lists of known credentials, improving the efficiency of discoverable credential flows and reducing user friction during the authentication process.

### 6.4 Attestation and Related-Origin Rules

The specification provides clarified and tightened rules regarding attestation formats and certificate validation. Relying parties that enforce attestation must update their verification logic to comply with the new requirements for packed, TPM, and Android attestation formats. Furthermore, Level 3 explicitly addresses the handling of iframes and related origins, providing formal guidance for applications that embed authentication flows or utilize cross-origin login architectures for single sign-on (SSO) deployments.

## 7. Security and Attestation

While passkeys inherently provide robust security through asymmetric cryptography, enterprise deployments often require additional validation to ensure that credentials meet specific organizational standards.

### 7.1 Attestation Formats

Attestation is the process by which an authenticator cryptographically proves its provenance and capabilities to the relying party during registration. The relying party can request different types of attestation based on its security requirements.

"None" attestation is the most common configuration for consumer applications. In this mode, the authenticator provides no provenance information, maximizing privacy and ensuring broad compatibility across all devices.

"Packed" attestation is a WebAuthn-optimized format that provides a compact encoding of the authenticator's certificate chain. It is commonly used by hardware security keys to prove their manufacturer and model.

Platform-specific attestations include TPM (Trusted Platform Module) for Windows devices, Android Key for Android devices, and Apple Anonymous Attestation for iOS and macOS devices. These formats allow the relying party to verify that the credential was generated within a recognized secure hardware enclave.

### 7.2 Security Considerations and Anti-Cloning

To detect potential credential cloning or unauthorized extraction, the WebAuthn specification utilizes a signature counter (`sign_count`). During each authentication event, the authenticator increments this counter and includes the new value in the signed assertion. The relying party stores the last known counter value and compares it against the incoming assertion. If the received counter is less than or equal to the stored value, the relying party must assume the credential has been cloned and should immediately invalidate it, triggering a security alert.

It is important to note that many modern platform authenticators, particularly those implementing synced passkeys, do not maintain a global signature counter and instead return a static value of zero. Relying parties must handle this gracefully, disabling clone detection logic for credentials that consistently return a zero counter.

## 8. Database Schema and Credential Management

Properly modeling passkey credentials within the application database is essential for supporting multiple devices, facilitating credential revocation, and managing the user lifecycle.

### 8.1 The Credential Record

A robust passkey implementation requires a dedicated credentials table linked to the primary user record via a foreign key relationship. A single user must be able to register multiple credentials to support different devices and backup strategies.

The essential fields for a credential record include:
- `credential_id`: A unique binary identifier generated by the authenticator.
- `public_key`: The cryptographic public key, typically stored in COSE format.
- `sign_count`: An integer tracking the number of authentication events, used for clone detection.
- `user_id`: The foreign key linking the credential to the user account.
- `transports`: An array indicating the supported communication methods (e.g., internal, usb, nfc, ble).
- `backup_eligible` and `backup_state`: Boolean flags indicating whether the credential can be synchronized and whether it is currently backed up.
- `created_at` and `last_used_at`: Timestamps for lifecycle management and auditing.
- `device_name`: A user-friendly label (e.g., "Personal iPhone" or "YubiKey 5 NFC") to aid in credential management.
- `aaguid`: The Authenticator Attestation Globally Unique Identifier, identifying the specific make and model of the hardware.

### 8.2 Credential Management UI

Users must be provided with a comprehensive interface to manage their registered passkeys. This interface should display all active credentials, indicating the device name, creation date, and last usage timestamp. Users must have the ability to rename credentials for easier identification and, crucially, to revoke specific credentials if a device is lost or compromised.

## 9. Recovery and Fallback Strategies

The most complex aspect of deploying passkeys is designing robust recovery mechanisms for users who lose access to their authenticators. Because passkeys eliminate shared secrets, a forgotten password flow is no longer applicable.

### 9.1 Primary Recovery Mechanisms

For consumer applications utilizing synced passkeys, the primary recovery mechanism is inherently handled by the cloud provider. If a user replaces their iPhone, their passkeys are automatically restored from iCloud Keychain upon authenticating with their Apple ID.

However, relying parties must account for scenarios where a user loses access to their entire cloud ecosystem or transitions to a different platform (e.g., moving from iOS to Android). In these cases, secondary recovery mechanisms are required.

Email-based recovery links, often combined with SMS or authenticator app OTPs, provide a familiar fallback. While these methods are susceptible to phishing, they offer a practical balance of security and usability for low-risk applications.

For higher security requirements, organizations can mandate the registration of backup security keys. Users register a primary platform authenticator and a secondary hardware key, storing the latter in a secure location. This approach maintains high assurance levels but requires significant user education and hardware investment.

### 9.2 Enterprise Account Recovery

In enterprise environments utilizing device-bound passkeys, recovery procedures must align with the organization's identity verification policies. If an employee loses their smart card or security key, they must undergo a formal identity proofing process—such as an in-person verification with HR or a video call with the IT service desk—before a new credential can be issued and bound to their account.

### 9.3 The Password Fallback

During the transitional phase of passkey adoption, most organizations must maintain passwords as a fallback mechanism. While the ultimate goal is a fully passwordless architecture, prematurely removing passwords can lock out users on older operating systems, shared devices, or corporate networks that restrict WebAuthn traffic. The recommended approach is to position passkeys as the primary, frictionless authentication path while retaining passwords as a secondary option, progressively phasing them out as ecosystem support reaches ubiquity.

## 10. Conclusion

Passkeys represent the definitive future of digital authentication, offering unparalleled security against phishing and credential stuffing while simultaneously delivering a superior user experience. By mastering the WebAuthn and FIDO2 standards, implementing conditional UI, designing robust recovery flows, and aligning deployment strategies with organizational compliance requirements, engineering teams can successfully navigate the transition to a passwordless architecture. The transition requires careful planning, rigorous testing, and thoughtful user communication, but the resulting improvements in security posture and conversion rates justify the investment.
## 11. Detailed Implementation Patterns

To truly master passkeys, one must understand the exact payload structures and implementation patterns required by the WebAuthn API. This section provides a deep dive into the technical implementation, covering both the client-side JavaScript execution and the server-side validation logic.

### 11.1 The Registration Payload Deep Dive

When initiating a registration, the server must construct a `PublicKeyCredentialCreationOptions` object. This object defines the parameters for the new credential.

```javascript
const publicKeyCredentialCreationOptions = {
  // The cryptographic challenge. Must be a cryptographically secure random buffer,
  // generated on the server, at least 16 bytes long.
  challenge: Uint8Array.from("random_server_generated_buffer", c => c.charCodeAt(0)),

  // Information about the relying party (your application)
  rp: {
    name: "Acme Corporation",
    id: "acme.com" // Must match the domain exactly
  },

  // Information about the user registering the credential
  user: {
    id: Uint8Array.from("internal_user_id_12345", c => c.charCodeAt(0)),
    name: "jane.doe@example.com",
    displayName: "Jane Doe"
  },

  // Cryptographic algorithms the server supports (e.g., ES256, RS256)
  pubKeyCredParams: [
    { alg: -7, type: "public-key" }, // ES256
    { alg: -257, type: "public-key" } // RS256
  ],

  // Authenticator requirements
  authenticatorSelection: {
    authenticatorAttachment: "platform", // Require a built-in authenticator (e.g., FaceID)
    requireResidentKey: true, // Require a discoverable credential
    userVerification: "required" // Require biometric or PIN verification
  },

  // Timeout in milliseconds
  timeout: 60000,

  // Requested attestation format
  attestation: "none" // "none" is recommended for consumer apps to maximize privacy
};
```

The client receives this object and invokes the API:

```javascript
try {
  const credential = await navigator.credentials.create({
    publicKey: publicKeyCredentialCreationOptions
  });
  
  // Send the credential to the server for verification and storage
  await sendRegistrationToServer(credential);
} catch (error) {
  console.error("Registration failed:", error);
}
```

### 11.2 The Authentication Payload Deep Dive

For authentication, the server constructs a `PublicKeyCredentialRequestOptions` object.

```javascript
const publicKeyCredentialRequestOptions = {
  // A new, unique cryptographic challenge
  challenge: Uint8Array.from("new_random_server_generated_buffer", c => c.charCodeAt(0)),

  // The relying party ID
  rpId: "acme.com",

  // Timeout in milliseconds
  timeout: 60000,

  // User verification requirement
  userVerification: "required"
};
```

Notice that `allowCredentials` is omitted here. This is the pattern for "discoverable credentials" (synced passkeys), where the authenticator determines which credential to use based on the `rpId`.

The client invokes the API, utilizing conditional mediation for the autofill experience:

```javascript
try {
  const assertion = await navigator.credentials.get({
    publicKey: publicKeyCredentialRequestOptions,
    // Enable Conditional UI (autofill)
    mediation: "conditional"
  });
  
  // Send the assertion to the server for cryptographic verification
  await sendAssertionToServer(assertion);
} catch (error) {
  console.error("Authentication failed:", error);
}
```

### 11.3 Server-Side Verification Logic

The most critical security boundary in a passkey implementation is the server-side verification of the assertion payload. The server must never trust the client. When receiving an authentication assertion, the server must perform the following validation steps:

1. **Retrieve the stored challenge**: Verify that the challenge in the assertion matches the challenge generated for this specific authentication session. This prevents replay attacks.
2. **Verify the Origin**: Extract the `origin` from the `clientDataJSON` and ensure it strictly matches the expected origin of your application (e.g., `https://acme.com`).
3. **Verify the RP ID Hash**: Calculate the SHA-256 hash of your expected RP ID (`acme.com`) and verify it matches the `rpIdHash` contained within the `authenticatorData`.
4. **Verify User Presence and Verification**: Check the flags within the `authenticatorData`. The User Present (UP) bit must be set. If your application requires biometrics, the User Verified (UV) bit must also be set.
5. **Signature Verification**: This is the core cryptographic check. The server must reconstruct the signed data (the concatenation of `authenticatorData` and the SHA-256 hash of `clientDataJSON`) and verify the assertion signature using the public key stored during registration.
6. **Clone Detection (Optional)**: If the authenticator supports signature counters, verify that the incoming `signCount` is strictly greater than the stored `signCount`. If it is less than or equal, the credential may have been cloned.

## 12. Enterprise Deployment Playbook

Deploying passkeys at an enterprise scale requires a structured approach that goes beyond technical implementation. It demands change management, phased rollouts, and alignment with corporate security policies.

### 12.1 Phase 1: Audit and Policy Alignment

Before writing code, enterprise security teams must audit their existing identity infrastructure. This involves determining the required Authenticator Assurance Level (AAL). If the organization operates under strict regulatory frameworks that mandate AAL3, the deployment must focus exclusively on device-bound hardware keys. If AAL2 is sufficient, synced passkeys can be utilized, significantly reducing operational overhead.

The team must also define the fallback policies. If a user loses their device, what is the approved recovery workflow? Will the IT helpdesk perform video verification? Will managers be authorized to approve credential resets? These policies must be documented and integrated into the identity management system.

### 12.2 Phase 2: Technical Integration and Pilot

The technical integration phase involves connecting the WebAuthn endpoints to the existing Identity Provider (IdP) or Single Sign-On (SSO) solution. Many modern IdPs (e.g., Okta, Microsoft Entra ID, Ping Identity) offer native passkey support, reducing the implementation burden.

The pilot phase should target a technically proficient cohort, such as the engineering or IT departments. This phase is critical for identifying edge cases, such as compatibility issues with specific corporate VPNs, proxy servers, or legacy operating systems that may interfere with CTAP traffic.

### 12.3 Phase 3: Phased Rollout and Adoption Campaigns

A successful enterprise rollout relies on clear communication. Users must understand what passkeys are, why the organization is adopting them, and how the registration process works.

The rollout should be phased by department or risk profile. The most effective adoption strategy is to enforce registration at the point of authentication. When a user logs in using their legacy password, the system should immediately prompt them to register a passkey, framing it as a mandatory security upgrade that will simplify their future access.

### 12.4 Phase 4: Deprecation of Legacy Methods

The final phase is the systematic deprecation of legacy authentication methods. Once passkey adoption reaches a defined threshold (e.g., 90%), the organization can begin disabling password access for enrolled users. This is often accompanied by the removal of weaker MFA methods, such as SMS OTPs, further hardening the organization's security posture against phishing and SIM-swapping attacks.

## 13. Advanced Architecture: Cross-Device Authentication (FIDO Cross-Device API)

One of the most powerful features of the passkey ecosystem is cross-device authentication (CDA), often referred to as "hybrid transport" or "caBLE" (Cloud-Assisted Bluetooth Low Energy). This allows a user to authenticate on a device that does not hold their passkey (e.g., a public library computer or a smart TV) using a device that does (e.g., their smartphone).

### 13.1 The CDA Workflow

1. The user attempts to log in on the desktop browser.
2. The desktop browser displays a QR code.
3. The user scans the QR code with their smartphone's camera.
4. The QR code contains routing information and a session key. The smartphone and the desktop browser establish a secure, end-to-end encrypted connection using Bluetooth Low Energy (BLE) to verify physical proximity, while the actual data is routed through a cloud relay service.
5. The smartphone prompts the user for biometric verification.
6. The smartphone signs the authentication challenge and transmits the assertion back to the desktop browser over the encrypted channel.
7. The desktop browser submits the assertion to the relying party server.

### 13.2 Implementation Considerations for CDA

From the relying party's perspective, CDA requires no specific code changes; it is handled entirely by the browser and the operating system. However, relying parties must ensure that their authentication timeouts are sufficiently long to accommodate the cross-device flow, which typically takes longer than a local platform authentication. A timeout of at least 60 seconds is recommended.

Furthermore, relying parties should be aware that CDA relies on BLE for proximity detection. If the desktop computer lacks Bluetooth hardware, or if corporate policies disable Bluetooth, the cross-device flow will fail.

## 14. References and Specifications

1. [Web Authentication: An API for accessing Public Key Credentials - Level 3 (W3C Candidate Recommendation, Jan 2026)](https://www.w3.org/TR/webauthn-3/)
2. [FIDO Alliance: Client to Authenticator Protocol (CTAP) 2.2](https://fidoalliance.org/specs/fido-v2.2-ps-20250714/fido-client-to-authenticator-protocol-v2.2-ps-20250714.html)
3. [NIST Special Publication 800-63-4: Digital Identity Guidelines](https://pages.nist.gov/800-63-4/)
4. [Google Identity: Passkeys developer guide for relying parties](https://developers.google.com/identity/passkeys/developer-guides)
5. [FIDO Alliance: Passkey Index 2025 Performance Metrics](https://fidoalliance.org/passkeys/)
## 15. Business Rules and Edge Case Management

A successful passkey implementation requires rigorous business rules to handle the myriad of edge cases that arise in real-world deployments. Authentication is the front door to your application; if the logic fails, users are locked out.

### 15.1 Handling Multiple Credentials

Users will inevitably register multiple passkeys. They may have a synced passkey on their Apple devices, another synced passkey on their Windows laptop, and a YubiKey for backup. 

**Business Rule:** The application must support an arbitrary number of passkeys per user account. The database schema must allow a one-to-many relationship between users and credentials. 

**Business Rule:** When requesting authentication, the server should generally omit the `allowCredentials` list to enable discoverable credentials (allowing the user to choose any passkey they possess). If the server must restrict the user to specific devices (e.g., in a high-security context requiring hardware keys), it must populate `allowCredentials` with the specific credential IDs authorized for that transaction.

### 15.2 The "Lost Device" Scenario

When a user loses a device containing a device-bound passkey, or loses access to their entire cloud ecosystem containing synced passkeys, the system must handle the recovery gracefully without compromising security.

**Business Rule:** Upon initiating an account recovery flow, the system must authenticate the user via the highest available secondary method (e.g., email verification link + SMS OTP, or an identity verification process).

**Business Rule:** Once the user successfully recovers their account, the system must explicitly prompt them to review their registered passkeys. The user must be forced to revoke the passkey associated with the lost device to prevent unauthorized access.

### 15.3 Revocation and Lifecycle Management

Passkeys, like any credential, have a lifecycle. They are created, used, and eventually must be destroyed.

**Business Rule:** When a user revokes a passkey via the application's security settings, the server must immediately delete the public key and credential ID from the database, or mark the record as logically deleted. Any active sessions established using that specific passkey should be immediately terminated.

**Business Rule:** Relying parties cannot delete the private key from the user's authenticator. The WebAuthn API provides no mechanism for a server to command a device to delete a credential. Therefore, users may still see the revoked passkey in their browser's autofill suggestions. Relying parties must handle this gracefully: if a user attempts to authenticate with a revoked passkey, the server must return a clear, user-friendly error message indicating that the credential is no longer valid and prompting them to register a new one or use an alternative method.

### 15.4 Browser and OS Inconsistencies

The WebAuthn standard is implemented differently across various operating systems and browsers. Relying parties must anticipate and handle these discrepancies.

**Business Rule:** The application must utilize feature detection (`window.PublicKeyCredential` and `getClientCapabilities()`) before attempting to invoke WebAuthn APIs. If the environment does not support passkeys, the UI must gracefully degrade to traditional authentication methods without throwing JavaScript errors.

**Business Rule:** Timeout handling must be robust. If a user closes the biometric prompt without authenticating, the browser will throw a `NotAllowedError`. The application must catch this specific error and return the user to the login screen, rather than displaying a generic system failure message.

## 16. Migration Strategies: From Passwords to Passkeys

Migrating an existing user base from passwords to passkeys is a complex operational challenge. It cannot be achieved via a hard cutover; it requires a strategic, phased approach that respects user behavior and technical constraints.

### 16.1 The "Passkey First" Strategy

The most effective migration strategy is "Passkey First." In this approach, the application's authentication interface is redesigned to prioritize passkeys, while retaining passwords as a secondary, slightly hidden option.

When a user navigates to the login page, the primary call-to-action is a biometric prompt triggered by Conditional UI or a prominent "Sign in with Passkey" button. The traditional username and password fields are either placed below the passkey prompt or moved to a secondary screen accessed via a "Use Password Instead" link.

This architectural shift signals to the user that passkeys are the preferred and superior method, driving adoption without completely blocking users who have not yet enrolled.

### 16.2 The "Upgrade Prompt" Strategy

For users who continue to authenticate via passwords, the application must actively campaign for them to upgrade.

Immediately following a successful password login, the application should intercept the user before granting access to the dashboard. A full-screen interstitial should appear, explaining that the application now supports passkeys and highlighting the benefits (faster login, no passwords to remember). The interstitial must contain a prominent "Create Passkey" button that immediately invokes the WebAuthn registration flow.

To prevent user fatigue, this interstitial should include a "Not Now" option, and the application should implement backoff logic (e.g., only showing the prompt once every 30 days) if the user repeatedly declines.

### 16.3 The "Security Checkup" Strategy

Organizations can leverage routine security events to drive passkey adoption. When a user requests a password reset, or when the system detects a login from a new device or unrecognized IP address, the resolution workflow should culminate in passkey registration.

For example, after a user successfully resets their password via an email link, the final screen of the flow should not simply state "Password Updated." Instead, it should state "Password Updated. Now, secure your account with a Passkey," seamlessly transitioning into the WebAuthn registration process.

## 17. Security Threat Modeling

While passkeys eliminate the threat of phishing and credential stuffing, they introduce new attack vectors that organizations must model and mitigate.

### 17.1 Cloud Account Compromise

The primary vulnerability of synced passkeys is the security of the underlying cloud account (Apple ID, Google Account, Microsoft Account). If an attacker compromises a user's iCloud account, they can potentially access the synced passkeys and authenticate to any relying party where those passkeys are registered.

**Mitigation:** Relying parties cannot directly secure a user's cloud account. However, for high-risk applications (e.g., banking, cryptocurrency exchanges), relying parties should mandate the use of device-bound hardware keys (AAL3) rather than synced passkeys, entirely bypassing the cloud synchronization risk.

### 17.2 The "Evil Maid" Attack

An "Evil Maid" attack occurs when an adversary gains physical access to a user's unlocked device. If the device is unlocked, the adversary can potentially use the resident passkeys to authenticate to relying parties.

**Mitigation:** Relying parties must enforce strict session timeouts. Furthermore, the WebAuthn specification allows relying parties to request `userVerification: "required"` during authentication. This forces the operating system to demand a fresh biometric gesture or PIN entry before signing the assertion, even if the device is already unlocked, neutralizing the Evil Maid attack.

### 17.3 Attestation Bypass and Emulators

Sophisticated attackers may attempt to use software emulators or modified operating systems to generate fraudulent WebAuthn assertions, bypassing the requirement for secure hardware.

**Mitigation:** For applications requiring high assurance, relying parties must strictly enforce attestation verification during registration. By rejecting "none" or "self" attestation and demanding cryptographically verified hardware attestation (e.g., TPM, Android Key, Apple Anonymous), the relying party ensures that the credential was generated within a genuine, certified secure enclave, thwarting software-based emulation attacks.

## 18. Regulatory Compliance Mapping

Passkeys align strongly with emerging global cybersecurity regulations, often serving as the optimal technical solution for compliance mandates.

### 18.1 Payment Services Directive 2 (PSD2) and Strong Customer Authentication (SCA)

In the European Union, PSD2 mandates Strong Customer Authentication (SCA) for electronic payments. SCA requires authentication using two or more independent factors: knowledge (something only the user knows), possession (something only the user possesses), and inherence (something the user is).

Passkeys satisfy the SCA requirement natively. The device itself satisfies the "possession" factor, while the biometric unlock satisfies the "inherence" factor (or the device PIN satisfies the "knowledge" factor). By deploying passkeys, financial institutions can meet PSD2 compliance without relying on vulnerable SMS OTPs.

### 18.2 Healthcare Insurance Portability and Accountability Act (HIPAA)

HIPAA requires covered entities to implement technical safeguards to ensure the confidentiality and integrity of electronic protected health information (ePHI). While HIPAA does not explicitly mandate specific technologies, it requires robust access controls.

Device-bound passkeys, particularly when deployed via smart cards or FIDO2 security keys, provide the high-assurance access control necessary for HIPAA compliance in clinical environments, ensuring that only authorized personnel physically possessing the credential can access patient records.

### 18.3 Emerging Global Mandates

Governments worldwide are actively deprecating SMS OTPs due to their vulnerability to SIM-swapping and SS7 routing attacks. Regulations in the UAE, India, and the Philippines taking effect in 2026 explicitly prohibit SMS OTPs for high-risk financial transactions. Passkeys represent the primary technical path for financial institutions operating in these jurisdictions to maintain compliance while preserving user experience.
## 19. Platform-Specific Implementation Guides

The WebAuthn standard is implemented through platform-specific APIs and SDKs. Each major platform has unique considerations that affect both the developer experience and the end-user flow.

### 19.1 Apple Ecosystem (iOS, macOS, iPadOS)

Apple's passkey implementation is deeply integrated into the operating system through the `ASAuthorizationController` framework within the AuthenticationServices module. Passkeys are stored in iCloud Keychain and automatically synchronized across all devices signed into the same Apple ID.

On iOS 16 and later, passkey creation and authentication are handled natively by the system. The developer creates an `ASAuthorizationPlatformPublicKeyCredentialProvider` and configures it with the relying party identifier. The system handles the biometric prompt (Face ID or Touch ID), key generation, and attestation response.

For web applications running in Safari, the standard WebAuthn JavaScript API is fully supported. Safari also supports Conditional UI (autofill-assisted passkey authentication) starting from Safari 16. A critical implementation detail is that Safari requires the WebAuthn call to be triggered by a user gesture (a click or tap event); calling `navigator.credentials.create()` or `navigator.credentials.get()` without a preceding user interaction will be rejected by the browser.

Apple's implementation also supports cross-device authentication via QR code scanning. If a user attempts to sign in on a non-Apple device (e.g., a Windows laptop), they can scan a QR code displayed on the screen using their iPhone's camera, authenticate via Face ID, and the assertion is transmitted back to the requesting device via the hybrid transport protocol.

### 19.2 Google Ecosystem (Android, Chrome)

Google's passkey implementation on Android is managed through the Credential Manager API, which provides a unified interface for passwords, passkeys, and federated sign-in. Passkeys are stored in Google Password Manager and synchronized across all Android devices and Chrome browsers signed into the same Google Account.

The Credential Manager API simplifies the developer experience by abstracting the underlying WebAuthn complexity. Developers create a `CreatePublicKeyCredentialRequest` for registration or a `GetCredentialRequest` for authentication, and the system handles the biometric prompt and cryptographic operations.

On Chrome for desktop, the standard WebAuthn JavaScript API is fully supported, including Conditional UI. Chrome also supports the hybrid transport protocol, allowing users to authenticate using their Android phone as a roaming authenticator via QR code and BLE proximity verification.

A notable Android-specific consideration is the handling of multiple credential providers. Unlike iOS where iCloud Keychain is the sole system provider, Android allows third-party password managers (1Password, Bitwarden, Dashlane) to register as credential providers. When multiple providers are available, the system presents a selection dialog, which can confuse users who are unfamiliar with the concept of credential providers.

### 19.3 Microsoft Ecosystem (Windows, Edge)

Microsoft's passkey implementation on Windows is built upon Windows Hello, which provides biometric authentication (facial recognition, fingerprint) or PIN-based verification. Starting with Windows 11 23H2, passkeys are synchronized across Windows devices via the user's Microsoft Account.

On older versions of Windows (Windows 10, Windows 11 pre-23H2), passkeys created with Windows Hello are device-bound and do not synchronize. This is a critical consideration for enterprise deployments targeting Windows environments, as users on older OS versions will lose their passkeys if they reimage their machine or switch devices.

Microsoft Edge supports the full WebAuthn API, including Conditional UI. Edge also supports the hybrid transport protocol for cross-device authentication using a smartphone.

### 19.4 Third-Party Password Managers

Third-party password managers (1Password, Bitwarden, Dashlane, LastPass) have rapidly adopted passkey storage and synchronization. These providers offer cross-platform passkey synchronization that transcends ecosystem boundaries, allowing a user to create a passkey on their iPhone and use it on their Windows laptop via the password manager's browser extension.

From the relying party's perspective, passkeys stored in third-party managers behave identically to platform-native passkeys. The WebAuthn API abstracts the storage provider, and the relying party receives the same attestation and assertion payloads regardless of where the private key resides.

However, relying parties should be aware that third-party managers may not support all WebAuthn features (e.g., certain attestation types or extensions). Testing against major password managers is recommended during the QA phase.

## 20. Testing and Quality Assurance

Passkey implementations require comprehensive testing strategies that go beyond standard unit and integration tests. The authentication flow involves hardware, operating systems, browsers, and network conditions, all of which can introduce failures.

### 20.1 Automated Testing with Virtual Authenticators

Modern browser automation frameworks (Playwright, Puppeteer, Selenium with Chrome DevTools Protocol) support virtual authenticators that simulate the behavior of real hardware without requiring physical devices.

In Playwright, a virtual authenticator can be configured as follows:

```javascript
const authenticator = await page.context().addInitScript(() => {
  // Configure virtual authenticator via Chrome DevTools Protocol
});

// Or using the CDP session directly
const cdpSession = await page.context().newCDPSession(page);
await cdpSession.send('WebAuthn.enable');
await cdpSession.send('WebAuthn.addVirtualAuthenticator', {
  options: {
    protocol: 'ctap2',
    transport: 'internal',
    hasResidentKey: true,
    hasUserVerification: true,
    isUserVerified: true
  }
});
```

Virtual authenticators allow CI/CD pipelines to execute full registration and authentication flows without human interaction, enabling regression testing of the entire passkey lifecycle.

### 20.2 Manual Testing Matrix

Despite the availability of virtual authenticators, manual testing across real devices and browsers is essential. The testing matrix should cover:

| Platform | Browser | Authenticator | Test Scenarios |
|----------|---------|---------------|----------------|
| iOS 17+ | Safari | iCloud Keychain | Registration, authentication, conditional UI, cross-device via QR |
| iOS 17+ | Chrome | iCloud Keychain | Registration, authentication, third-party provider selection |
| Android 14+ | Chrome | Google PM | Registration, authentication, conditional UI, cross-device via QR |
| Android 14+ | Firefox | Google PM | Registration, authentication (conditional UI support varies) |
| Windows 11 | Edge | Windows Hello | Registration, authentication, conditional UI, PIN fallback |
| Windows 11 | Chrome | Windows Hello | Registration, authentication, conditional UI |
| macOS 14+ | Safari | iCloud Keychain | Registration, authentication, conditional UI, Touch ID |
| macOS 14+ | Chrome | iCloud Keychain / 1Password | Registration, authentication, provider selection |
| Any | Any | YubiKey 5 (USB) | Registration, authentication, cross-device roaming |
| Any | Any | YubiKey 5 (NFC) | Registration via NFC tap on mobile |

### 20.3 Edge Case Testing

Beyond the standard happy-path flows, testers must explicitly validate the following edge cases:

The user cancels the biometric prompt mid-flow. The application must gracefully handle the `NotAllowedError` and return to the login screen without displaying a stack trace or generic error page.

The user's device does not have biometric hardware configured. The system should fall back to PIN verification or guide the user to set up biometrics in their device settings.

The user attempts to register a duplicate passkey. The `excludeCredentials` parameter must correctly prevent the creation of a second credential on the same authenticator, and the application must display a helpful message indicating the passkey already exists.

The user's signature counter is zero (common with synced passkeys). The server's clone detection logic must not incorrectly flag the credential as compromised.

The network connection drops between the client sending the assertion and the server responding. The application must implement idempotent verification logic to handle retries without creating duplicate sessions.

## 21. Server-Side Library Ecosystem

The passkey ecosystem benefits from a robust set of open-source server-side libraries that handle the complex cryptographic verification logic. Choosing the right library significantly reduces implementation time and the risk of security vulnerabilities.

### 21.1 JavaScript/TypeScript

**SimpleWebAuthn** (`@simplewebauthn/server` and `@simplewebauthn/browser`) is the most widely adopted library in the Node.js ecosystem. It provides a clean, well-documented API for generating registration and authentication options, and for verifying the corresponding responses. It supports all attestation formats and is actively maintained.

### 21.2 Python

**py_webauthn** is the standard library for Python applications. It integrates cleanly with Django and Flask frameworks and provides comprehensive support for all WebAuthn operations, including attestation verification and credential management.

### 21.3 Go

**go-webauthn** provides a Go-native implementation of the WebAuthn server-side logic. It is designed for high-performance applications and integrates with Go's standard `net/http` package as well as popular frameworks like Gin and Echo.

### 21.4 Java

**java-webauthn-server** by Yubico is the reference implementation for Java applications. It is production-grade, extensively tested, and supports all attestation formats. It integrates with Spring Security and Jakarta EE.

### 21.5 Ruby

**webauthn-ruby** provides a comprehensive Ruby implementation suitable for Rails applications. It handles the full registration and authentication lifecycle and supports the FIDO Metadata Service for authenticator trust evaluation.

### 21.6 Rust

**webauthn-rs** is a high-performance Rust implementation that provides both a low-level API for custom integrations and a high-level API for rapid development. It is suitable for applications where performance and memory safety are critical.

## 22. Monitoring and Observability

A production passkey deployment requires comprehensive monitoring to detect issues before they impact users.

### 22.1 Key Metrics to Track

The following metrics should be instrumented and monitored via dashboards (e.g., Grafana, Datadog):

**Registration Success Rate:** The percentage of users who successfully complete the passkey registration flow. A sudden drop may indicate a browser update breaking compatibility or a server-side configuration error.

**Authentication Success Rate:** The percentage of passkey authentication attempts that succeed. This should be segmented by platform, browser, and authenticator type to identify platform-specific regressions.

**Conditional UI Engagement Rate:** The percentage of login page visits where the user interacts with the conditional UI autofill prompt versus clicking the explicit login button. Low engagement may indicate that the conditional UI implementation is not triggering correctly.

**Authentication Latency (P50, P95, P99):** The time from the user initiating authentication to the server issuing a session token. Passkey authentication should consistently be under 10 seconds at P95. Elevated latency may indicate server-side verification bottlenecks or network issues affecting the cross-device protocol.

**Clone Detection Alerts:** The number of times the server detects a potential credential clone (signature counter regression). While false positives are common with synced passkeys (which report zero counters), alerts on device-bound credentials with non-zero counters should trigger immediate investigation.

**Fallback Rate:** The percentage of users who abandon the passkey flow and fall back to password authentication. A high fallback rate indicates UX friction or technical compatibility issues that must be addressed.

### 22.2 Alerting Thresholds

Critical alerts should fire when the authentication success rate drops below 90% (indicating a systemic issue), when the registration success rate drops below 80%, or when clone detection alerts spike above the historical baseline by more than two standard deviations.

## 23. Complete Glossary of Terms

Understanding the precise terminology of the passkey ecosystem is essential for clear communication between engineering, security, and product teams.

**AAL (Authenticator Assurance Level):** A NIST-defined metric indicating the strength of an authentication mechanism. AAL1 is single-factor, AAL2 is multi-factor (passkeys meet this), and AAL3 requires hardware-bound credentials with attestation.

**AAGUID (Authenticator Attestation Globally Unique Identifier):** A 128-bit identifier that uniquely identifies the make and model of an authenticator (e.g., "YubiKey 5 NFC" or "iCloud Keychain").

**Attestation:** The process by which an authenticator proves its provenance and capabilities to the relying party during registration.

**CBOR (Concise Binary Object Representation):** The binary encoding format used to serialize WebAuthn data structures, including the attestation object and authenticator data.

**Conditional UI:** A browser feature that integrates passkey authentication into the native autofill mechanism, allowing users to select a passkey from the username field dropdown.

**COSE (CBOR Object Signing and Encryption):** The format used to encode the public key within WebAuthn credentials.

**CTAP (Client to Authenticator Protocol):** The protocol governing communication between the browser/OS and the authenticator hardware.

**Discoverable Credential (Resident Key):** A credential stored on the authenticator that can be used without the server providing the credential ID in `allowCredentials`.

**RP ID (Relying Party Identifier):** The domain scope of a passkey, typically the registrable domain (e.g., `example.com`).

**User Presence (UP):** A flag indicating the user physically interacted with the authenticator (e.g., touched a button).

**User Verification (UV):** A flag indicating the user was verified by the authenticator using biometrics or a PIN, providing a higher level of assurance than mere presence.
## 24. Integration Patterns with Identity Providers

Most enterprise and SaaS applications do not implement authentication from scratch. Instead, they rely on Identity Providers (IdPs) and Single Sign-On (SSO) solutions. Passkeys must integrate seamlessly with these existing architectures.

### 24.1 OIDC (OpenID Connect) Integration

In an OIDC-based architecture, the relying party delegates authentication to an IdP (e.g., Okta, Auth0, Microsoft Entra ID, Keycloak). The passkey registration and authentication flows occur entirely within the IdP's hosted login page. The relying party receives the standard OIDC tokens (ID token, access token) upon successful authentication, regardless of whether the user authenticated via passkey, password, or any other method.

This pattern is the simplest to implement for relying parties, as the WebAuthn integration is handled entirely by the IdP. The relying party's responsibility is limited to configuring the IdP to enable passkeys and ensuring that the OIDC redirect URIs are correctly configured.

### 24.2 Direct WebAuthn Integration with Session Management

For applications that manage their own authentication (without delegating to an external IdP), the WebAuthn endpoints must be integrated directly into the application's backend. The typical architecture involves:

A `/webauthn/register/options` endpoint that generates and returns the `PublicKeyCredentialCreationOptions` to the client. A `/webauthn/register/verify` endpoint that receives the attestation response, validates it, and stores the credential. A `/webauthn/authenticate/options` endpoint that generates and returns the `PublicKeyCredentialRequestOptions`. A `/webauthn/authenticate/verify` endpoint that receives the assertion, validates the signature, and issues a session token (typically a JWT or an opaque session cookie).

### 24.3 Passkeys with Step-Up Authentication

For high-risk operations within an already-authenticated session (e.g., changing account settings, initiating a large financial transfer, or accessing sensitive data), applications can implement "step-up authentication" using passkeys.

In this pattern, the user is already logged in with a valid session. When they attempt a sensitive action, the application interrupts the flow and demands a fresh passkey authentication. This is implemented by calling `navigator.credentials.get()` with `userVerification: "required"`, ensuring the user performs a fresh biometric gesture. The resulting assertion is sent to the server, which verifies it and grants elevated privileges for a limited time window.

This pattern provides the security equivalent of re-entering a password before changing account settings, but with the superior UX of a biometric gesture.

## 25. The FIDO Metadata Service (MDS)

The FIDO Metadata Service is a centralized repository maintained by the FIDO Alliance that contains detailed information about every certified FIDO authenticator. Relying parties can query the MDS to obtain metadata about a specific authenticator model, including its certification level, supported algorithms, known vulnerabilities, and security status.

### 25.1 Using MDS for Trust Decisions

When a relying party receives an attestation response during registration, it can extract the AAGUID from the authenticator data and query the MDS to determine the authenticator's trust level. This allows the relying party to make informed decisions about which authenticators to accept.

For example, a banking application might configure its policy to only accept credentials from authenticators that have achieved FIDO L2 certification (which requires hardware-level security evaluation). If a user attempts to register a passkey from an authenticator that only has L1 certification (software-based), the relying party can reject the registration and inform the user that a higher-assurance authenticator is required.

### 25.2 Handling Compromised Authenticators

The MDS also publishes security advisories when vulnerabilities are discovered in specific authenticator models. Relying parties that integrate with the MDS can automatically detect if any of their registered credentials are stored on a compromised authenticator model and proactively notify affected users, prompting them to register replacement credentials.

## 26. Performance Optimization

While passkey authentication is inherently fast from the user's perspective (a single biometric gesture), the server-side processing must be optimized to maintain low latency at scale.

### 26.1 Challenge Generation and Storage

Challenges must be cryptographically secure random values, at least 16 bytes long. They must be stored server-side (in a database or cache like Redis) with a short TTL (typically 60-120 seconds) and must be single-use. After verification, the challenge must be immediately deleted to prevent replay attacks.

For high-traffic applications, storing challenges in an in-memory cache (Redis, Memcached) with automatic TTL expiration is significantly more performant than database storage, as it avoids write amplification and garbage collection overhead.

### 26.2 Public Key Verification Performance

The cryptographic signature verification performed during authentication is computationally inexpensive (typically sub-millisecond for ES256 or RS256 on modern hardware). However, the database lookup to retrieve the stored public key based on the credential ID can become a bottleneck at scale.

Relying parties should ensure that the `credential_id` column is properly indexed in the database. For applications with millions of registered credentials, consider partitioning the credentials table or using a dedicated key-value store for credential lookups.

### 26.3 Caching Authenticator Metadata

If the relying party integrates with the FIDO Metadata Service, the MDS responses should be cached locally with a reasonable TTL (e.g., 24 hours). Querying the MDS on every registration request introduces unnecessary latency and creates a dependency on an external service.

## 27. Passkeys in Native Mobile Applications

While the WebAuthn API is designed for web browsers, native mobile applications have their own platform-specific APIs for passkey management.

### 27.1 iOS Native Implementation

On iOS, passkey operations are handled through the `ASAuthorizationController` class. The developer creates an `ASAuthorizationPlatformPublicKeyCredentialProvider` configured with the relying party identifier and requests either registration or assertion.

A critical requirement for iOS native apps is the Associated Domains entitlement. The app must declare the `webcredentials` associated domain in its entitlements file, and the relying party's server must host an `apple-app-site-association` file at `https://<rp-id>/.well-known/apple-app-site-association` that lists the app's bundle identifier. Without this bidirectional association, the operating system will reject passkey operations.

### 27.2 Android Native Implementation

On Android, the Credential Manager API provides a unified interface. The developer creates a `CreatePublicKeyCredentialRequest` (for registration) or a `GetCredentialRequest` (for authentication) and passes it to the `CredentialManager.createCredential()` or `CredentialManager.getCredential()` methods.

Similar to iOS, Android requires a Digital Asset Links file hosted at `https://<rp-id>/.well-known/assetlinks.json` that associates the app's package name and signing certificate fingerprint with the relying party domain.

### 27.3 Cross-Platform Considerations

For applications that exist on both web and native mobile platforms, the same passkey can be used across all surfaces, provided the RP ID is consistent. A passkey registered via the web application at `example.com` will be available in the native iOS app (if the Associated Domains are correctly configured) and the native Android app (if the Digital Asset Links are correctly configured).

This cross-platform availability is a significant advantage of passkeys over platform-specific biometric APIs, which typically create credentials that are only usable within the specific application that created them.

## 28. Future Directions

The passkey ecosystem continues to evolve rapidly. Several emerging developments will shape the next generation of passwordless authentication.

**Credential Exchange Protocol:** The FIDO Alliance is developing a protocol to allow users to securely transfer passkeys between different credential providers (e.g., from iCloud Keychain to 1Password, or from Google Password Manager to Bitwarden). This addresses the current vendor lock-in concern and will further accelerate adoption.

**Verifiable Credentials Integration:** The convergence of passkeys with Verifiable Credentials (VCs) and decentralized identity standards will enable new use cases where authentication is combined with attribute verification (e.g., proving age without revealing date of birth).

**Passkeys for IoT and Embedded Devices:** As the CTAP protocol evolves, passkey authentication will extend to IoT devices, smart home systems, and automotive interfaces, providing phishing-resistant authentication for the growing ecosystem of connected devices.

**Enterprise Managed Passkeys:** Platform vendors are developing enterprise management capabilities that allow organizations to provision, manage, and revoke passkeys centrally through MDM (Mobile Device Management) solutions, providing the same lifecycle management capabilities currently available for certificates and hardware tokens.
## 29. Common Implementation Mistakes and Anti-Patterns

The following section catalogs the most frequently observed mistakes in passkey implementations, drawn from production audits and community reports.

### 29.1 Hardcoding the RP ID Incorrectly

The most devastating implementation error is configuring the Relying Party ID incorrectly. The RP ID must be the registrable domain (e.g., `example.com`), not a full URL (`https://example.com`), not a subdomain (`auth.example.com` unless intentionally scoping), and not an IP address. If the RP ID is set incorrectly, all registered passkeys become permanently unusable if the RP ID is later corrected, because the authenticator binds the credential to the original RP ID hash.

### 29.2 Not Storing Transports

When a user registers a passkey, the attestation response includes a `transports` array indicating how the authenticator communicates (e.g., `["internal"]` for a platform authenticator, `["usb", "nfc"]` for a YubiKey). Relying parties must store this array and include it in the `allowCredentials` list during authentication. If transports are omitted, the browser cannot optimize the authenticator selection process, potentially prompting the user to insert a USB key when they should be using their built-in fingerprint reader.

### 29.3 Ignoring the Backup Eligibility Flags

WebAuthn Level 2 introduced the `BE` (Backup Eligible) and `BS` (Backup State) flags in the authenticator data. These flags indicate whether a credential is eligible for synchronization and whether it is currently backed up. Relying parties that ignore these flags cannot differentiate between synced and device-bound credentials, making it impossible to enforce policies that require hardware-bound credentials for high-risk operations.

### 29.4 Using Predictable Challenges

The challenge must be a cryptographically secure random value generated fresh for each ceremony. Using predictable values (timestamps, sequential integers, user IDs) allows attackers to pre-compute valid assertions, completely undermining the security model. Always use `crypto.getRandomValues()` (client-side) or `os.urandom()` / `crypto.randomBytes()` (server-side) to generate challenges.

### 29.5 Not Implementing Timeout Handling

WebAuthn ceremonies have configurable timeouts. If the timeout expires (because the user walked away, got distracted, or is using a slow cross-device flow), the browser throws an error. Many implementations fail to handle this gracefully, displaying cryptic error messages or crashing the login flow. The application must catch timeout errors specifically and offer the user a clear "Try Again" option.

### 29.6 Requiring Attestation Unnecessarily

Requesting attestation (especially "direct" or "enterprise" conveyance) when it is not needed introduces friction and reduces compatibility. Many authenticators do not support all attestation formats, and some users may be prompted with additional consent dialogs when attestation is requested. Unless the relying party has a specific, documented need to verify the authenticator's provenance (e.g., for AAL3 compliance or hardware key inventory management), attestation should be set to "none."

### 29.7 Not Testing Cross-Browser Behavior

The WebAuthn API behaves differently across browsers, particularly in edge cases. Safari requires user gestures before WebAuthn calls. Firefox has historically lagged behind Chrome in Conditional UI support. Brave browser may block certain WebAuthn features. Relying parties that only test on Chrome will encounter production failures when users arrive from other browsers.

## 30. Quick Reference Decision Matrix

The following decision matrix helps engineering teams quickly determine the appropriate passkey configuration based on their application's requirements.

| Requirement | Recommended Configuration |
|-------------|--------------------------|
| Consumer app, maximum adoption | Synced passkeys, attestation: none, userVerification: preferred, Conditional UI enabled |
| SaaS B2B, standard security | Synced passkeys, attestation: none, userVerification: required, Conditional UI + explicit button |
| Banking/Financial services | Hybrid (synced for login, device-bound for transactions), attestation: direct, userVerification: required |
| Healthcare (HIPAA) | Device-bound passkeys (smart cards), attestation: direct, userVerification: required |
| Government (AAL3) | Device-bound passkeys (FIPS-certified keys), attestation: enterprise, userVerification: required |
| Internal admin tools | Device-bound hardware keys (YubiKey), attestation: direct, userVerification: required, no password fallback |
| IoT/Embedded devices | Cross-device authentication via hybrid transport, userVerification: required on phone |

| Migration Phase | Strategy |
|----------------|----------|
| Day 0 (Launch) | Offer passkey registration during signup, password remains primary |
| Month 1-3 | Passkey-first UI, upgrade prompts after password login |
| Month 3-6 | Conditional UI as default, password fields hidden behind "Other options" |
| Month 6-12 | Disable password for users with 2+ registered passkeys |
| Month 12+ | Full passwordless for all enrolled users, password only for recovery |

This specialist document provides the complete knowledge base required to design, implement, deploy, and maintain a production-grade passkey authentication system across any platform, compliance framework, or organizational scale.
## 31. Operational Runbook

### 31.1 Daily Operations Checklist

Monitor the passkey authentication success rate dashboard. Investigate any drop below 95% immediately. Review clone detection alerts and escalate any alerts on device-bound credentials with non-zero counters. Verify that the challenge cache (Redis) is healthy and TTL expiration is functioning correctly. Check certificate expiration dates for any attestation root certificates stored in the trust anchor configuration.

### 31.2 Incident Response: Mass Authentication Failure

If a sudden spike in authentication failures is detected, immediately check whether a browser or OS update has been released that may have changed WebAuthn behavior. Verify that the server's challenge generation endpoint is responding correctly and that the database containing stored credentials is accessible. If the issue is isolated to a specific platform (e.g., all iOS users failing), check Apple's system status page for iCloud Keychain outages. Communicate the issue to affected users via in-app messaging and temporarily increase the visibility of fallback authentication methods until the root cause is resolved and a fix is deployed.

### 31.3 Credential Rotation Policy

While passkeys do not expire in the traditional sense (unlike certificates or API keys), organizations should establish a credential hygiene policy. Credentials that have not been used within 12 months should be flagged for review. Users should be periodically prompted to verify their registered credentials are still accessible and to remove any that correspond to devices they no longer own.

## === FILE: 51-passkeys-troubleshooting.md ===
# Passkeys Troubleshooting Guide

## 1. Registration Failures

### 1.1 NotAllowedError: The operation either timed out or was not allowed

**Cause:** This is the most common error and has multiple root causes.

**Diagnosis Steps:**
1. Check if the WebAuthn call was triggered by a user gesture. Safari strictly requires a click/tap event to precede `navigator.credentials.create()`. Programmatic calls without user interaction will be rejected.
2. Verify the RP ID matches the current domain. If the page is served from `auth.example.com` but the RP ID is set to `other.com`, the browser will reject the operation.
3. Check if the user cancelled the biometric prompt. This is not an error condition but must be handled gracefully.
4. Verify the timeout has not expired. Default timeouts vary by browser (Chrome: 120s, Safari: 60s, Firefox: 120s).
5. Check if `excludeCredentials` contains a credential already present on the authenticator. The browser will throw this error to prevent duplicate registration.

**Resolution:**
- Ensure all WebAuthn calls are within a click event handler
- Verify RP ID configuration matches the serving domain
- Implement retry logic with a clear "Try Again" button
- Increase timeout for cross-device flows

### 1.2 SecurityError: The RP ID is not a registrable domain suffix of the current origin

**Cause:** The RP ID does not match the page's origin. The RP ID must be equal to or a registrable domain suffix of the page's effective domain.

**Examples:**
- Page at `https://login.example.com` with RP ID `example.com` → VALID (registrable domain suffix)
- Page at `https://example.com` with RP ID `example.com` → VALID (exact match)
- Page at `https://example.com` with RP ID `login.example.com` → INVALID (RP ID is more specific)
- Page at `https://example.com` with RP ID `other.com` → INVALID (different domain)
- Page at `http://example.com` (HTTP) → INVALID (WebAuthn requires HTTPS, except localhost)

**Resolution:** Correct the RP ID to match the registrable domain. Remember: you cannot change the RP ID after credentials are registered without invalidating all existing passkeys.

### 1.3 InvalidStateError: The authenticator was previously registered

**Cause:** The `excludeCredentials` list contains a credential ID that already exists on the authenticator being used. This is the intended behavior to prevent duplicate registration.

**Resolution:** Inform the user that they already have a passkey registered on this device. Offer to proceed to authentication instead, or allow them to manage existing credentials.

### 1.4 NotSupportedError: The algorithm is not supported

**Cause:** The `pubKeyCredParams` array contains only algorithms that the authenticator does not support.

**Resolution:** Always include ES256 (`alg: -7`) as it is universally supported by all FIDO2 authenticators. Include RS256 (`alg: -257`) as a fallback for older Windows Hello implementations.

## 2. Authentication Failures

### 2.1 No Passkey Available in Autofill (Conditional UI)

**Cause:** Conditional UI is not triggering, and no passkeys appear in the autofill dropdown.

**Diagnosis Steps:**
1. Verify `mediation: "conditional"` is set in the `navigator.credentials.get()` call.
2. Ensure the call is made on page load (not inside a click handler for conditional UI).
3. Check that the input field has `autocomplete="username webauthn"` attribute.
4. Verify the browser supports Conditional UI: `PublicKeyCredential.isConditionalMediationAvailable()`.
5. Confirm passkeys exist for this RP ID in the user's credential manager.
6. Check that no other `navigator.credentials.get()` call is already pending (only one can be active).

**Resolution:**
- Add the `webauthn` token to the input's `autocomplete` attribute
- Call `navigator.credentials.get()` immediately on page load
- Abort any pending requests before starting a new one using `AbortController`
- Provide an explicit "Sign in with Passkey" button as fallback

### 2.2 Signature Verification Failed

**Cause:** The server's cryptographic verification of the assertion signature fails.

**Diagnosis Steps:**
1. Verify the correct public key is being used (match credential ID to stored record).
2. Ensure the signed data is constructed correctly: `authenticatorData || SHA-256(clientDataJSON)`.
3. Check the algorithm matches what was used during registration (ES256 vs RS256).
4. Verify no data corruption occurred during base64url encoding/decoding.
5. Check for byte-order issues in the public key parsing.

**Resolution:**
- Log the raw authenticatorData and clientDataJSON for debugging
- Verify base64url decoding is correct (no padding, URL-safe alphabet)
- Ensure the public key was stored in the correct format (COSE vs PEM vs DER)
- Use a well-tested library rather than implementing verification manually

### 2.3 Sign Count Regression (Clone Detection)

**Cause:** The received `signCount` is less than or equal to the stored `signCount`, indicating a potential credential clone.

**Diagnosis Steps:**
1. Check if the credential is a synced passkey (backup_eligible = true). Synced passkeys often report signCount = 0 consistently.
2. If the credential is device-bound and the counter has regressed, this is a genuine security concern.

**Resolution:**
- For synced passkeys (signCount always 0): Disable clone detection for these credentials
- For device-bound passkeys with regression: Immediately revoke the credential, notify the user, and require re-registration via a high-assurance recovery flow

## 3. Cross-Device (Hybrid Transport) Issues

### 3.1 QR Code Not Appearing

**Cause:** The browser is not offering the cross-device option.

**Diagnosis Steps:**
1. Verify the device has Bluetooth hardware and it is enabled.
2. Check that the browser supports hybrid transport (Chrome 108+, Safari 16+, Edge 108+).
3. Ensure `allowCredentials` does not restrict to only `["internal"]` transports.

**Resolution:**
- Do not restrict transports in `allowCredentials` unless specifically required
- Inform users that Bluetooth must be enabled for cross-device authentication
- Provide alternative authentication methods for devices without Bluetooth

### 3.2 Cross-Device Connection Timeout

**Cause:** The BLE proximity check or cloud relay connection failed.

**Diagnosis Steps:**
1. Ensure the phone and computer are within Bluetooth range (typically 10 meters).
2. Check that both devices have internet connectivity.
3. Verify no firewall is blocking the WebSocket connection to the cloud relay.

**Resolution:**
- Increase the timeout to at least 120 seconds for cross-device flows
- Instruct users to keep devices close together
- Check corporate firewall rules for WebSocket blocking

## 4. Platform-Specific Issues

### 4.1 Safari: "This request has been cancelled by the user"

**Cause:** Safari is particularly strict about user gesture requirements and will cancel requests that are not directly triggered by user interaction.

**Resolution:** Ensure the WebAuthn call is the direct result of a click event. Do not use `setTimeout`, `Promise.then`, or `async/await` chains that break the user gesture context.

### 4.2 Android: Multiple Credential Provider Dialog

**Cause:** The user has multiple credential providers installed (Google Password Manager + 1Password + Bitwarden), and Android displays a selection dialog.

**Resolution:** This is expected behavior on Android and cannot be suppressed by the relying party. Ensure your documentation helps users understand which provider contains their passkey.

### 4.3 Windows: "Windows Hello is not set up"

**Cause:** The user's Windows device does not have Windows Hello configured (no PIN, fingerprint, or facial recognition set up).

**Resolution:** Guide the user to Settings > Accounts > Sign-in options to configure Windows Hello. Alternatively, offer cross-device authentication via their smartphone.

### 4.4 Firefox: Conditional UI Not Working

**Cause:** Firefox's Conditional UI support has historically lagged behind Chrome and Safari.

**Resolution:** Always implement both Conditional UI and an explicit "Sign in with Passkey" button. Check `isConditionalMediationAvailable()` and only activate conditional mediation if supported.

## 5. Server-Side Issues

### 5.1 Challenge Expired or Not Found

**Cause:** The challenge stored in the server's session/cache has expired (TTL exceeded) or was never stored.

**Resolution:**
- Increase challenge TTL to 120-300 seconds to accommodate slow users
- Verify Redis/session storage is healthy and accessible
- Ensure challenge is stored BEFORE returning options to the client
- Implement proper error handling that prompts the user to retry

### 5.2 Origin Mismatch

**Cause:** The `origin` in `clientDataJSON` does not match the server's expected origin.

**Common causes:**
- Server expects `https://example.com` but client sends `https://www.example.com`
- Reverse proxy stripping or modifying headers
- Development environment using `http://localhost` while production expects HTTPS

**Resolution:**
- Configure the server to accept all valid origins for your deployment
- For localhost development, accept `http://localhost:<port>` origins
- Ensure reverse proxy configuration preserves the original origin

### 5.3 Attestation Verification Failure

**Cause:** The server cannot verify the attestation certificate chain.

**Resolution:**
- If attestation is not required for your use case, set `attestation: "none"` and skip verification
- If attestation is required, ensure root certificates are up to date
- Download the latest FIDO MDS blob and update trust anchors
- Check certificate expiration dates in the attestation chain

## 6. Migration and Upgrade Issues

### 6.1 Cannot Change RP ID After Deployment

**Problem:** The RP ID was set incorrectly during initial deployment, and now all existing credentials are bound to the wrong domain.

**Impact:** All existing passkeys become permanently unusable if the RP ID is changed.

**Resolution:** There is no technical fix. The RP ID is cryptographically bound to the credential. Options:
1. Keep the incorrect RP ID and work around it (if possible)
2. Force all users to re-register new passkeys under the correct RP ID
3. Use WebAuthn Level 3 "related origins" if the incorrect RP ID is a related domain

### 6.2 Library Upgrade Breaking Changes

**Problem:** Upgrading the WebAuthn server library introduces breaking changes in the verification logic.

**Resolution:**
- Pin library versions in production
- Test upgrades thoroughly in staging with real authenticators
- Maintain backward compatibility for existing credential formats
- Never modify stored credential data during library upgrades

