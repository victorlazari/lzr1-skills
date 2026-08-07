# Passkeys Implementation Patterns

## Node.js

Use the `@simplewebauthn/server` library for server-side validation.

```javascript
const { generateRegistrationOptions, verifyRegistrationResponse } = require('@simplewebauthn/server');

// Generate options
const options = await generateRegistrationOptions({
  rpName: 'Example Corp',
  rpID: 'example.com',
  userID: 'user123',
  userName: 'lee@example.com',
  attestationType: 'none',
});

// Verify response
const verification = await verifyRegistrationResponse({
  response: credential,
  expectedChallenge: expectedChallenge,
  expectedOrigin: 'https://example.com',
  expectedRPID: 'example.com',
});
```

## Python

Use the `webauthn` library for server-side validation.

```python
from webauthn import generate_registration_options, verify_registration_response

# Generate options
options = generate_registration_options(
    rp_id="example.com",
    rp_name="Example Corp",
    user_id=b"user123",
    user_name="lee@example.com",
)

# Verify response
verification = verify_registration_response(
    credential=credential,
    expected_challenge=expected_challenge,
    expected_origin="https://example.com",
    expected_rp_id="example.com",
)
```

## Go

Use the `github.com/go-webauthn/webauthn` library for server-side validation.

```go
import "github.com/go-webauthn/webauthn/webauthn"

// Initialize WebAuthn
w, err := webauthn.New(&webauthn.Config{
    RPDisplayName: "Example Corp",
    RPID:          "example.com",
    RPOrigins:     []string{"https://example.com"},
})

// Generate options
options, sessionData, err := w.BeginRegistration(user)

// Verify response
credential, err := w.FinishRegistration(user, sessionData, response)
```

## Well-Known Files Configuration

To support related origins (WebAuthn Level 3), host a `.well-known/webauthn` file at the root of your domain.

```json
{
  "origins": [
    "https://app.example.com",
    "https://login.example.com"
  ]
}
```

*Verified against upstream: 2026-08-07*
