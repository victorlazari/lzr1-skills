# Security Architecture

## Table of Contents
1. Threat Modeling
2. Zero Trust Architecture
3. Cryptography
4. Security Patterns
5. Supply Chain Security

---

## 1. Threat Modeling

### STRIDE Framework

| Threat | Description | Property Violated | Mitigation |
|---|---|---|---|
| Spoofing | Impersonating a user/system | Authentication | Strong auth, MFA |
| Tampering | Modifying data/code | Integrity | Signing, checksums, HMAC |
| Repudiation | Denying actions | Non-repudiation | Audit logs, digital signatures |
| Information Disclosure | Exposing data | Confidentiality | Encryption, access control |
| Denial of Service | Disrupting availability | Availability | Rate limiting, redundancy |
| Elevation of Privilege | Gaining unauthorized access | Authorization | Least privilege, sandboxing |

### Threat Modeling Process

1. **Decompose the system**: Identify components, data flows, trust boundaries
2. **Identify threats**: Apply STRIDE to each component/flow
3. **Rate threats**: Use DREAD or risk matrix (likelihood × impact)
4. **Mitigate**: Design controls for high-risk threats
5. **Validate**: Verify mitigations are effective

### Data Flow Diagram Elements

| Element | Symbol | Example |
|---|---|---|
| External entity | Rectangle | User, third-party API |
| Process | Circle | Web server, API service |
| Data store | Parallel lines | Database, file system |
| Data flow | Arrow | HTTP request, DB query |
| Trust boundary | Dashed line | Network perimeter, service mesh |

---

## 2. Zero Trust Architecture

### Zero Trust Principles (NIST SP 800-207)

1. All data sources and computing services are considered resources
2. All communication is secured regardless of network location
3. Access to individual resources is granted on a per-session basis
4. Access is determined by dynamic policy (identity, device, behavior, context)
5. Enterprise monitors and measures integrity/security of all assets
6. Authentication and authorization are dynamic and strictly enforced
7. Enterprise collects information about assets and uses it to improve security

### Zero Trust Implementation Layers

| Layer | Control | Implementation |
|---|---|---|
| Identity | Strong authentication | OIDC, MFA, passwordless |
| Device | Device trust and health | MDM, device certificates |
| Network | Micro-segmentation | Service mesh, network policies |
| Application | Per-request authorization | Policy engine (OPA, Cedar) |
| Data | Classification and protection | DLP, encryption, tokenization |
| Visibility | Continuous monitoring | SIEM, UEBA, NDR |

---

## 3. Cryptography

### Algorithm Selection Guide

| Purpose | Recommended | Avoid |
|---|---|---|
| Symmetric encryption | AES-256-GCM | DES, 3DES, RC4, ECB mode |
| Asymmetric encryption | RSA-2048+, ECDSA P-256 | RSA-1024, DSA |
| Hashing | SHA-256, SHA-3, BLAKE3 | MD5, SHA-1 |
| Password hashing | Argon2id, bcrypt (cost≥12) | MD5, SHA-256 (unsalted) |
| Key derivation | HKDF, PBKDF2 | Custom derivation |
| Digital signatures | Ed25519, ECDSA P-256 | RSA-1024 |
| TLS | TLS 1.3 | TLS 1.0, 1.1, SSL |
| Key exchange | X25519, ECDH P-256 | Static DH, RSA key exchange |

### Key Management Principles

- Never hardcode keys in source code
- Use hardware security modules (HSM) for root keys
- Implement key rotation (automated where possible)
- Use envelope encryption (DEK encrypted by KEK)
- Separate key management from data access
- Implement proper key destruction procedures
- Use cloud KMS for managed key lifecycle

### Certificate Management

| Aspect | Best Practice |
|---|---|
| Issuance | Automated (ACME/Let's Encrypt, ACM) |
| Rotation | Auto-renew 30 days before expiry |
| Storage | Never in code; use secrets manager |
| Monitoring | Alert on expiry (30, 14, 7 days) |
| Revocation | CRL or OCSP stapling |
| Chain | Verify full chain including intermediates |

---

## 4. Security Patterns

### Defense in Depth

```
Internet → DDoS Protection → WAF → Load Balancer → API Gateway → Application → Database
              ↓                 ↓         ↓              ↓            ↓           ↓
          Rate limiting    OWASP rules  TLS termination  Auth/AuthZ  Input validation  Encryption at rest
```

### Secure Architecture Patterns

| Pattern | Description | Use Case |
|---|---|---|
| API Gateway | Centralized auth, rate limiting, logging | Microservices |
| Service Mesh | mTLS, policy enforcement between services | Zero trust internal |
| Sidecar proxy | Security controls without app changes | Legacy modernization |
| Vault pattern | Centralized secrets with dynamic credentials | Secret management |
| Circuit breaker | Prevent cascade failures | Resilient services |
| Bulkhead | Isolate failures to prevent spread | Multi-tenant systems |

### Secure Development Lifecycle (SDL)

| Phase | Security Activity | Output |
|---|---|---|
| Requirements | Security requirements, abuse cases | Security user stories |
| Design | Threat modeling, security architecture | Threat model, ADRs |
| Implementation | Secure coding, SAST | Clean code, findings |
| Testing | DAST, penetration testing | Vulnerability report |
| Deployment | Security config review, hardening | Hardened deployment |
| Operations | Monitoring, incident response | Security alerts, runbooks |

---

## 5. Supply Chain Security

### Software Supply Chain Threats

| Threat | Example | Mitigation |
|---|---|---|
| Compromised dependency | event-stream, ua-parser-js | SCA scanning, lockfiles |
| Typosquatting | Malicious packages with similar names | Verify package names, use allowlists |
| Build system compromise | SolarWinds, Codecov | Hermetic builds, SLSA |
| Stolen credentials | npm token theft | Short-lived tokens, 2FA |
| Dependency confusion | Private package name collision | Scoped packages, registry config |

### SLSA Framework (Supply-chain Levels for Software Artifacts)

| Level | Requirements | Protection |
|---|---|---|
| SLSA 1 | Build process documented | Basic provenance |
| SLSA 2 | Hosted build, signed provenance | Tampering after build |
| SLSA 3 | Hardened build platform | Tampering during build |
| SLSA 4 | Two-person review, hermetic build | Insider threats |

### Dependency Management

- Pin all dependency versions (lockfiles)
- Scan dependencies for known CVEs (Snyk, Dependabot, Trivy)
- Review dependency updates before merging
- Use private registries for internal packages
- Implement Software Bill of Materials (SBOM)
- Sign and verify all artifacts (Sigstore, cosign)
- Minimize dependency count (fewer dependencies = smaller attack surface)
