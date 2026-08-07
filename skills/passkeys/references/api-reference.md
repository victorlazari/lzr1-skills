# Passkeys API Reference

## WebAuthn JavaScript API

### Registration

```javascript
const publicKeyCredentialCreationOptions = {
  challenge: Uint8Array.from("randomStringFromServer", c => c.charCodeAt(0)),
  rp: {
    name: "Example Corp",
    id: "example.com",
  },
  user: {
    id: Uint8Array.from("UZSL85T9AFC", c => c.charCodeAt(0)),
    name: "lee@example.com",
    displayName: "Lee",
  },
  pubKeyCredParams: [{alg: -7, type: "public-key"}],
  authenticatorSelection: {
    authenticatorAttachment: "platform",
  },
  timeout: 60000,
  attestation: "direct"
};

const credential = await navigator.credentials.create({
  publicKey: publicKeyCredentialCreationOptions
});
```

### Authentication

```javascript
const publicKeyCredentialRequestOptions = {
  challenge: Uint8Array.from("randomStringFromServer", c => c.charCodeAt(0)),
  allowCredentials: [{
    id: Uint8Array.from("credentialId", c => c.charCodeAt(0)),
    type: "public-key",
    transports: ["internal"],
  }],
  timeout: 60000,
};

const assertion = await navigator.credentials.get({
  publicKey: publicKeyCredentialRequestOptions
});
```

## Server-Side Endpoints

- `POST /webauthn/register/generate-options`: Generate registration options.
- `POST /webauthn/register/verify`: Verify registration response.
- `POST /webauthn/authenticate/generate-options`: Generate authentication options.
- `POST /webauthn/authenticate/verify`: Verify authentication response.

## Database Schemas

```sql
CREATE TABLE users (
  id UUID PRIMARY KEY,
  username VARCHAR(255) UNIQUE NOT NULL,
  display_name VARCHAR(255)
);

CREATE TABLE credentials (
  id BYTEA PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  public_key BYTEA NOT NULL,
  sign_count INTEGER NOT NULL DEFAULT 0,
  transports VARCHAR(255)[]
);
```

*Verified against upstream: 2026-08-07*
