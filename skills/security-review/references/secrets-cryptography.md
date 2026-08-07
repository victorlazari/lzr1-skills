# Secrets and Cryptography Security Review Reference

**Verified against upstream:** 2026-08-07

## Purpose and Boundaries
This reference provides deterministic, evidence-driven guidance for reviewing secrets management and cryptographic implementations in application code and configuration. It is designed to support a bounded specialist agent in a parallel review protocol or to be followed sequentially. This is defensive code-review guidance, not an exploitation manual. It does not claim certification or guarantee the absence of vulnerabilities. Never instruct the agent to execute target code, upload proprietary material, expose secrets, or actively test production without explicit authorization. The scope includes secret discovery, cryptographic purpose, password storage, randomness, key lifecycle, authenticated encryption, TLS, and FIPS boundary claims.

## Table of Contents
1. [Agent Contract](#agent-contract)
2. [Review Inputs and Threat Assumptions](#review-inputs-and-threat-assumptions)
3. [Deterministic Review Procedure](#deterministic-review-procedure)
4. [Code and Configuration Patterns](#code-and-configuration-patterns)
5. [False-Positive Controls and Validation](#false-positive-controls-and-validation)
6. [Finding Evidence Requirements and Escalation](#finding-evidence-requirements-and-escalation)
7. [References](#references)

## Agent Contract
The Cryptography Review Agent accepts source code, configuration files, and architecture diagrams as input, and outputs structured findings on secret exposure, cryptographic weaknesses, and key management flaws, supported by canonical citations and deterministic evidence.

## Review Inputs and Threat Assumptions
**Inputs:** Source code repositories, CI/CD pipeline configurations, infrastructure-as-code (IaC) templates, environment variable definitions, and cryptographic module configurations.
**Threat Assumptions:** Attackers have read access to source code, configuration files, and build artifacts. They can intercept network traffic, access compromised databases, and exploit weak randomness or outdated cryptographic algorithms. The threat model assumes that any hardcoded secret will eventually be discovered and that cryptographic implementations will be subjected to cryptanalysis.

## Deterministic Review Procedure

### 1. Secret Discovery
Identify hardcoded secrets, API keys, and credentials without relying solely on brittle provider-specific regexes. Analyze variable names, entropy, and context. Look for assignments to variables named `password`, `secret`, `api_key`, `token`, etc. Evaluate the entropy of string literals assigned to these variables. High entropy strings are often secrets.

### 2. History and Artifact Exposure
Verify that secrets are not exposed in version control history, build logs, or container image layers. Secrets committed to version control, even if later removed, remain in the history. Build logs and container image layers can also inadvertently expose secrets if not properly managed.

### 3. Rotation and Containment
Ensure mechanisms exist for secret rotation and that secrets are contained within secure vaults or environment variables, not hardcoded. Secrets should have a defined lifecycle and be rotated regularly. They should be injected into the application at runtime using secure mechanisms.

### 4. Cryptographic Purpose and Threat Model
Evaluate whether the chosen cryptographic algorithms align with the intended purpose (e.g., encryption, hashing, signing) and the defined threat model. Using a hashing algorithm for encryption or a weak algorithm for a high-security application is a vulnerability.

### 5. Password Storage
Verify the use of strong, salted, and iterated password hashing algorithms (e.g., Argon2, bcrypt, PBKDF2). Passwords must never be stored in plain text or using weak hashing algorithms like MD5 or SHA-1. A unique salt must be used for each password.

### 6. Randomness
Ensure the use of cryptographically secure pseudorandom number generators (CSPRNGs) for keys, nonces, and IVs. Standard PRNGs (like `Math.random()` or `rand()`) are predictable and must not be used for cryptographic purposes.

### 7. Key/Nonce/IV Lifecycle
Review the generation, storage, usage, and destruction of cryptographic keys, nonces, and initialization vectors. Keys must be generated securely, stored safely, used only for their intended purpose, and destroyed when no longer needed. Nonces and IVs must meet the specific requirements of the chosen algorithm (e.g., uniqueness, unpredictability).

### 8. Authenticated Encryption
Verify the use of authenticated encryption modes (e.g., AES-GCM, ChaCha20-Poly1305) to ensure both confidentiality and integrity. Unauthenticated encryption modes (like CBC) are vulnerable to padding oracle attacks and tampering.

### 9. Signatures and TLS
Check for proper implementation of digital signatures and the use of strong TLS configurations (TLS 1.2 or higher) with secure cipher suites. Digital signatures must use strong algorithms (e.g., RSA with SHA-256, ECDSA). TLS configurations must disable weak protocols and cipher suites.

### 10. Certificate Validation
Ensure proper validation of X.509 certificates, including hostname verification and chain of trust validation. Disabling certificate validation allows man-in-the-middle attacks.

### 11. Key Management and Crypto Agility
Evaluate key management practices and the system's ability to transition to new cryptographic algorithms (crypto agility). Systems should be designed to easily update cryptographic algorithms and keys in response to new vulnerabilities or advances in cryptanalysis.

### 12. FIPS Boundary Claims
Verify claims of FIPS 140-3 compliance and ensure cryptographic operations occur within the approved boundary. If an application claims FIPS compliance, it must use validated cryptographic modules and operate them in an approved mode.

## Code and Configuration Patterns

### Anti-Patterns
*   **Hardcoding secrets:** Storing passwords, API keys, or tokens directly in source code or configuration files.
*   **Weak algorithms:** Using deprecated algorithms like MD5, SHA-1, DES, or RC4 for security purposes.
*   **ECB mode:** Using Electronic Codebook (ECB) mode for block ciphers, which does not hide data patterns.
*   **Nonce/IV reuse:** Reusing nonces or IVs with stream ciphers or authenticated encryption modes, which can lead to key recovery or plaintext exposure.
*   **Weak password storage:** Storing passwords in plain text, using weak hashing algorithms, or not using a unique salt.
*   **Disabled certificate validation:** Disabling hostname verification or chain of trust validation in TLS connections.
*   **Insecure randomness:** Using non-cryptographic PRNGs for generating keys, nonces, or IVs.
*   **Custom cryptography:** Implementing custom cryptographic algorithms or protocols instead of using established, peer-reviewed standards.
*   **Hardcoded keys:** Embedding cryptographic keys directly in the application code or binary.
*   **Insufficient key length:** Using keys that are too short to provide adequate security against modern cryptanalysis.
*   **Missing integrity checks:** Failing to verify the integrity of encrypted data, leading to potential tampering.
*   **Improper key storage:** Storing keys in insecure locations, such as plain text files or easily accessible databases.
*   **Lack of rotation:** Failing to rotate cryptographic keys regularly, increasing the risk of compromise over time.
*   **Ignoring errors:** Failing to properly handle cryptographic errors, which can lead to information leakage or bypass of security controls.
*   **Using default credentials:** Relying on default passwords or keys provided by vendors or frameworks.
*   **Hardcoded salts:** Using a single, hardcoded salt for all passwords instead of generating a unique salt for each user.
*   **Insufficient iterations:** Using a low number of iterations for password hashing algorithms like PBKDF2, making them vulnerable to brute-force attacks.
*   **Storing keys with data:** Storing cryptographic keys in the same database or file system as the encrypted data they protect.
*   **Lack of key revocation:** Failing to implement a mechanism for revoking compromised keys.
*   **Using outdated TLS versions:** Supporting TLS 1.0 or 1.1, which have known vulnerabilities.
*   **Weak cipher suites:** Allowing the use of cipher suites that do not support forward secrecy or use weak encryption algorithms.
*   **Improper certificate handling:** Failing to securely store and manage X.509 certificates.
*   **Lack of crypto agility:** Hardcoding cryptographic algorithms and parameters, making it difficult to update them in the future.
*   **Ignoring FIPS requirements:** Claiming FIPS compliance without actually using validated modules or operating them in an approved mode.
*   **Insufficient logging:** Failing to log cryptographic operations and errors, making it difficult to detect and investigate security incidents.
*   **Over-reliance on encryption:** Assuming that encryption alone is sufficient for security, without implementing other necessary controls like access control and authentication.
*   **Improper use of APIs:** Misusing cryptographic APIs, leading to insecure implementations.
*   **Lack of testing:** Failing to adequately test cryptographic implementations for vulnerabilities.
*   **Ignoring threat models:** Implementing cryptography without considering the specific threats the system faces.
*   **Using unvetted libraries:** Relying on obscure or unmaintained cryptographic libraries.
*   **Failing to update:** Not keeping cryptographic libraries and dependencies up to date.
*   **Ignoring best practices:** Failing to follow established industry standards and best practices for cryptography.
*   **Lack of documentation:** Failing to document cryptographic implementations and key management procedures.
*   **Insufficient training:** Not providing adequate training to developers on secure cryptographic practices.
*   **Ignoring compliance requirements:** Failing to meet regulatory or compliance requirements related to cryptography.

### Recommended Patterns
*   **Secure secret management:** Using dedicated solutions like HashiCorp Vault, AWS Secrets Manager, or Azure Key Vault to store and manage secrets.
*   **Authenticated encryption:** Using modes like AES-GCM or ChaCha20-Poly1305 to provide both confidentiality and integrity.
*   **Strong password hashing:** Using algorithms like Argon2id, bcrypt, or PBKDF2 with appropriate work factors and unique salts.
*   **Strong TLS configuration:** Enforcing TLS 1.2 or higher and using secure cipher suites that support forward secrecy.
*   **Cryptographically secure randomness:** Using CSPRNGs provided by the operating system or a validated cryptographic library.
*   **Key derivation functions:** Using strong KDFs (e.g., HKDF) to derive keys from passwords or other secrets.
*   **Secure key storage:** Storing keys in hardware security modules (HSMs) or secure enclaves when possible.
*   **Regular key rotation:** Implementing automated key rotation policies to minimize the impact of a compromised key.
*   **Proper error handling:** Handling cryptographic errors securely without leaking sensitive information.
*   **Using established libraries:** Relying on well-vetted, widely used cryptographic libraries (e.g., OpenSSL, Bouncy Castle, libsodium) rather than custom implementations.
*   **Code reviews:** Conducting thorough security code reviews of all cryptographic implementations.
*   **Threat modeling:** Performing threat modeling to identify potential cryptographic vulnerabilities early in the development lifecycle.
*   **Security testing:** Incorporating automated security testing tools (e.g., SAST, DAST) to detect cryptographic flaws.
*   **Staying updated:** Keeping cryptographic libraries and dependencies up to date to patch known vulnerabilities.
*   **Following standards:** Adhering to industry standards and best practices (e.g., NIST, OWASP) for cryptographic implementations.
*   **Implementing crypto agility:** Designing systems to easily support new cryptographic algorithms and key sizes.
*   **Validating certificates:** Properly validating X.509 certificates, including hostname verification and chain of trust validation.
*   **Using appropriate key lengths:** Selecting key lengths that provide adequate security for the intended lifespan of the data.
*   **Protecting keys in memory:** Using techniques to protect cryptographic keys while they are in memory, such as secure enclaves or memory locking.
*   **Monitoring and logging:** Implementing comprehensive monitoring and logging of cryptographic operations to detect and respond to security incidents.
*   **Providing training:** Ensuring that developers have the necessary training and resources to implement cryptography securely.
*   **Conducting regular audits:** Performing regular security audits of cryptographic implementations and key management practices.
*   **Following compliance requirements:** Ensuring that cryptographic implementations meet all relevant regulatory and compliance requirements.
*   **Using hardware security modules (HSMs):** Utilizing HSMs for generating, storing, and managing highly sensitive cryptographic keys.
*   **Implementing secure boot:** Using secure boot mechanisms to ensure that only trusted code is executed on the system.
*   **Protecting against side-channel attacks:** Implementing countermeasures against side-channel attacks, such as timing attacks and power analysis.
*   **Using formal verification:** Employing formal verification techniques to mathematically prove the correctness and security of cryptographic implementations.
*   **Participating in bug bounties:** Encouraging security researchers to find and report vulnerabilities in cryptographic implementations through bug bounty programs.
*   **Staying informed:** Keeping up to date with the latest developments in cryptography and cryptanalysis.

## False-Positive Controls and Validation
*   **Contextual analysis:** Verify that identified "secrets" are not test credentials, placeholders, or public identifiers. Analyze the context in which the string is used.
*   **Algorithm purpose:** Confirm that flagged cryptographic algorithms are actually used for security purposes. For example, using MD5 for a non-security checksum is acceptable, but using it for password hashing is a vulnerability.
*   **Runtime validation:** Use runtime context only when the authorization record explicitly permits it and an isolated, safe environment exists. Otherwise, record the missing context as uncertainty and validate platform defaults against current official documentation.
*   **Scope verification:** Ensure that the identified vulnerability falls within the scope of the review and is relevant to the specific application or environment.
*   **Evidence corroboration:** Combine independent evidence where proportionate, but do not require active testing or a second source before recording a well-supported candidate. Preserve evidence quality, scope, and uncertainty explicitly.

## Finding evidence requirements and escalation

Emit reports through [`../templates/finding.schema.json`](../templates/finding.schema.json). The report root must contain `schema_version`, `review`, `findings`, `conflicts`, and `unknowns`. Every finding must contain `id`, `title`, `status`, `asset`, `locations`, `evidence`, `reasoning`, `preconditions`, `impact`, `taxonomy`, `confidence`, `remediation`, `validation`, `residual_risk`, and `conflicts`. Add optional `cvss_v4` or `live_context` only when supported by the finding; omission is valid. The `conflicts` array contains only top-level conflict IDs. `accepted_risk` is required when `status` is `accepted-risk` and forbidden for every other status; it contains `owner`, `rationale`, non-empty `compensating_controls`, `review_by`, and `expires_at`. Never store or reproduce a complete secret, private key, recovery code, token, credential-bearing request, or unnecessary personal data. Use a digest, length, non-authenticating fragment, or an access-controlled evidence reference.

Distinguish a placeholder, public identifier, encrypted value, password verifier, key handle, and live credential. Record missing provenance or runtime use as uncertainty. If specialists disagree about whether a value is sensitive or a cryptographic control is effective, preserve both evidence paths in a conflict object and use `disputed` while material conflict remains.

Stop the affected path when a likely live credential, private key, signing key, production trust anchor, or systemic cryptographic failure appears. Minimize exposure and notify the coordinator or Phase 0 user-designated contact. Do not test the value, contact its issuer, revoke or rotate it, modify a trust store, or run cryptographic probes without explicit authorization. Independent safe, read-only review may continue.

## Authoritative references

The complete source mapping is maintained in [`sources.md`](sources.md).

| Authority | Use |
| :--- | :--- |
| [NIST SP 800-63-4 Digital Identity Guidelines](https://pages.nist.gov/800-63-4/) | Current authenticator, verifier, federation, and lifecycle guidance. |
| [NIST Cryptographic Standards and Guidelines](https://csrc.nist.gov/projects/cryptographic-standards-and-guidelines) | Current algorithms, modes, transitions, and implementation guidance. |
| [FIPS 140-3](https://csrc.nist.gov/pubs/fips/140-3/final) | Security requirements for cryptographic modules where applicable. |
| [OWASP Cryptographic Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html) | Application cryptographic storage and key-management review. |
| [OWASP Secrets Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html) | Secret creation, storage, access, rotation, revocation, and logging controls. |
| [MITRE CWE-259](https://cwe.mitre.org/data/definitions/259.html) | Hard-coded password taxonomy. |
| [MITRE CWE-327](https://cwe.mitre.org/data/definitions/327.html) | Broken or risky cryptographic algorithm taxonomy. |
| [MITRE CWE-330](https://cwe.mitre.org/data/definitions/330.html) | Insufficient randomness taxonomy. |
| [MITRE CWE-295](https://cwe.mitre.org/data/definitions/295.html) | Certificate-validation weakness taxonomy. |
