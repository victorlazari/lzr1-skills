# Mobile Client Security Review Reference

**Verified against upstream:** 2026-08-07

## Purpose and Boundaries
This reference provides deterministic, line-by-line code review guidance for mobile client applications (iOS, Android, and cross-platform frameworks). It is designed for defensive code review and is not an exploitation manual. The review assumes the device environment is fundamentally untrusted and that the client application operates outside the organization's security perimeter.

**Scope:** Mobile application code, configuration files, manifests, and local storage mechanisms.
**Out of Scope:** Server-side API implementation (see API Security reference), active exploitation, or dynamic testing of production systems without explicit authorization.
**Safety Limits:** Never instruct the agent to execute target code, upload proprietary material, expose secrets, or actively test production without explicit authorization.

## Table of Contents
1. [Threat Assumptions](#threat-assumptions)
2. [Review Inputs](#review-inputs)
3. [Deterministic Review Procedure](#deterministic-review-procedure)
4. [OWASP MASVS Dimensions](#owasp-masvs-dimensions)
5. [Validation and Regression Checks](#validation-and-regression-checks)
6. [Finding Evidence Requirements](#finding-evidence-requirements)
7. [Stop and Escalation Rules](#stop-and-escalation-rules)
8. [Official References](#official-references)

## Threat Assumptions
- **Untrusted Environment:** The device may be rooted, jailbroken, or compromised by malware.
- **Client-Side Trust Limitations:** Any security control implemented solely on the client can be bypassed. The client cannot be trusted to enforce business logic or authorization.
- **Network Interception:** Network traffic may be intercepted or manipulated by a local proxy or malicious network.
- **Physical Access:** An attacker may have physical access to the device and its file system.

## Review Inputs
- Application source code (Swift, Objective-C, Kotlin, Java, Dart, JavaScript/TypeScript, C#).
- Configuration files (e.g., `Info.plist`, `AndroidManifest.xml`).
- Build scripts and dependency manifests (e.g., `Podfile`, `build.gradle`, `pubspec.yaml`, `package.json`).
- Current live catalogs (CISA KEV, EPSS, NVD, CVE) for runtime-refreshed context.

## Deterministic Review Procedure
1. **Inventory:** Identify all exported components, deep links, WebViews, and local storage mechanisms.
2. **Static Analysis:** Scan code and configuration files against the OWASP MASVS dimensions.
3. **Data Flow Tracing:** Trace sensitive data from input (user, API) to sink (storage, network, UI).
4. **False-Positive Controls:** Verify that identified vulnerabilities are not mitigated by other controls (e.g., OS-level protections, server-side validation).
5. **Documentation:** Record findings with exact file/line evidence, source-to-sink reasoning, and impact.

## OWASP MASVS Dimensions

### 1. Storage and Privacy
**Normative Requirement:** Sensitive data must not be stored in plaintext on the device.
- **Check:** Audit usage of `UserDefaults`, `SharedPreferences`, SQLite databases, and local files.
- **Anti-pattern:** Storing authentication tokens or PII in `SharedPreferences` without encryption.
- **Pattern:** Use platform-provided secure storage (iOS Keychain, Android Keystore/EncryptedSharedPreferences).
- **Privacy:** Verify that screenshots, clipboard, and notifications do not expose sensitive data. Ensure backups exclude sensitive directories.

### 2. Cryptography
**Normative Requirement:** Use strong, up-to-date cryptographic algorithms and platform-provided key management.
- **Check:** Audit cryptographic implementations for hardcoded keys, weak algorithms (e.g., MD5, DES), and improper IV usage.
- **Anti-pattern:** Hardcoding symmetric encryption keys in the source code.
- **Pattern:** Generate and store keys in the hardware-backed Keystore/Keychain.

### 3. Authentication and Authorization
**Normative Requirement:** The client must securely manage authentication state and rely on the server for authorization.
- **Check:** Verify secure handling of session tokens (e.g., JWTs). Audit local biometric authentication implementations.
- **Anti-pattern:** Using local biometric authentication as a substitute for server-side authorization.
- **Pattern:** Use biometrics to unlock a securely stored token, which is then used for API requests.

### 4. Network Communication
**Normative Requirement:** All network traffic must be encrypted using TLS.
- **Check:** Audit network configurations (e.g., App Transport Security, Network Security Configuration) to ensure cleartext traffic is disabled.
- **Tradeoffs:** Evaluate certificate validation and pinning. Pinning increases security but requires careful operational management to avoid app bricking during certificate rotation.

### 5. Platform Interaction
**Normative Requirement:** The app must securely interact with the underlying OS and other apps.
- **Check:** Audit exported components (Activities, Services, Receivers), intents, and IPC mechanisms.
- **Anti-pattern:** Exporting a component that handles sensitive actions without requiring permissions.
- **Pattern:** Use explicit intents and validate incoming data from other apps.

### 6. Code Quality and Build Settings
**Normative Requirement:** The app must be built with security features enabled and free of common coding errors.
- **Check:** Verify that debugging is disabled in release builds. Audit for embedded secrets (API keys, credentials).
- **Anti-pattern:** Leaving `android:debuggable="true"` in the release manifest.

### 7. Resilience
**Normative Requirement:** The app should implement defense-in-depth measures against reverse engineering and tampering.
- **Check:** Evaluate the use of obfuscation, anti-debugging, and anti-tampering controls.
- **Note:** These controls increase the effort required by an attacker but do not guarantee security.

### 8. Mobile API Trust Boundaries
**Normative Requirement:** Treat all data received from the client as untrusted on the server.
- **Check:** Ensure the client does not perform critical business logic or authorization checks that are not replicated on the server.

### 9. Deep Links and WebViews
**Normative Requirement:** Deep links and WebViews must be securely configured to prevent injection and hijacking.
- **Check:** Audit deep link handlers for input validation. Verify WebViews disable JavaScript if not needed and restrict file access.
- **Anti-pattern:** Enabling `setJavaScriptEnabled(true)` and `setAllowFileAccess(true)` on a WebView that loads untrusted content.
- **Pattern:** Use Universal Links (iOS) or App Links (Android) instead of custom URL schemes to prevent hijacking.

## Validation and Regression Checks
- **Syntax Checks:** Ensure all configuration files (XML, Plist, JSON) are well-formed.
- **Safe capability check:** Use a non-executing synthetic fixture included with the package, or review the source of a deliberately vulnerable training application only when its license and provenance are known. Installing, building, launching, instrumenting, or interacting with any mobile application requires explicit authorization and an isolated environment.
- **Postcondition Verification:** Confirm that all identified vulnerabilities have corresponding remediation guidance.

## Canonical finding evidence requirements

Every report must conform to `../templates/finding.schema.json`. The report root must contain `schema_version`, `review`, `findings`, `conflicts`, and `unknowns`. Every finding must contain `id`, `title`, `status`, `asset`, `locations`, `evidence`, `reasoning`, `preconditions`, `impact`, `taxonomy`, `confidence`, `remediation`, `validation`, `residual_risk`, and `conflicts`. Add optional `cvss_v4` or `live_context` only when supported by the finding; omission is valid. The `conflicts` array contains only top-level conflict IDs. `accepted_risk` is required when `status` is `accepted-risk` and forbidden for every other status; it contains `owner`, `rationale`, non-empty `compensating_controls`, `review_by`, and `expires_at`. For binary-only evidence, identify the artifact and immutable digest rather than implying source-line precision.

Distinguish static configuration, source intent, built artifact behavior, device policy, operating-system version, and backend enforcement. Missing entitlements, signing configuration, minification output, runtime policy, or server behavior must be recorded as unknowns. Do not copy production tokens, signing material, personal records, complete decompiled applications, or proprietary binary payloads into a report.

## Stop and escalation rules

- **Architecture boundary:** If critical authorization or business invariants exist only in the client, record a high-impact server-boundary finding and notify the coordinator; do not halt unrelated authorized review dimensions.
- **Sensitive material:** If actual production credentials, signing keys, personal data, or suspicious binaries appear, stop the affected action, minimize and redact evidence, and notify the coordinator or user-designated Phase 0 contact. Do not validate, rotate, revoke, upload, or disclose them without authorization.
- **Conflict:** Represent contradictory evidence as a top-level conflict object and place its conflict ID in each affected finding’s `conflicts` array. Use `disputed` when the finding status itself remains unresolved; the coordinator owns resolution and final synthesis.

## Authoritative references

Use the complete source-to-check and freshness matrix in `sources.md`; refresh living MASVS/MASTG and platform guidance for the exact OS and SDK versions under review.

### Primary sources
1. [OWASP Mobile Application Security Verification Standard (MASVS)](https://mas.owasp.org/MASVS/)
2. [OWASP Top 10:2025](https://owasp.org/Top10/2025/en/)
3. [OWASP API Security Top 10 2023](https://owasp.org/API-Security/editions/2023/en/0x11-t10/)
4. [NIST SP 800-63-4 Digital Identity Guidelines](https://pages.nist.gov/800-63-4/)
5. [RFC 9700 Best Current Practice for OAuth 2.0 Security](https://www.rfc-editor.org/rfc/rfc9700.html)
6. [RFC 8725 JSON Web Token Best Current Practices](https://www.rfc-editor.org/rfc/rfc8725.html)
7. [FIPS 140-3 Security Requirements for Cryptographic Modules](https://csrc.nist.gov/pubs/fips/140-3/final)
8. [NIST Privacy Framework](https://www.nist.gov/privacy-framework)

## Extended Guidance for Specific Platforms

### iOS Specific Checks
- **Keychain:** Verify that `kSecAttrAccessible` is set appropriately (e.g., `kSecAttrAccessibleWhenUnlockedThisDeviceOnly`) to prevent data extraction from locked devices or backups.
- **App Transport Security (ATS):** Ensure `NSAllowsArbitraryLoads` is not set to `YES` in `Info.plist` without a valid, documented exception.
- **Data Protection API:** Verify that files containing sensitive data are created with `NSFileProtectionComplete` or `NSFileProtectionCompleteUnlessOpen`.
- **Background Snapshots:** Ensure the app obscures sensitive information (e.g., by overlaying a view or blurring) in `applicationDidEnterBackground` to prevent data leakage in the app switcher snapshot.

### Android Specific Checks
- **Network Security Configuration:** Verify that cleartext traffic is explicitly disabled (`cleartextTrafficPermitted="false"`) and that custom trust anchors are not permitted in release builds.
- **Intents and IPC:** Ensure that sensitive BroadcastReceivers, Services, and Activities are not exported (`android:exported="false"`) unless necessary, and if exported, are protected by strong signature-level permissions.
- **Tapjacking:** Verify that `filterTouchesWhenObscured="true"` is set on sensitive UI elements to prevent overlay attacks.
- **Keystore:** Ensure cryptographic keys are generated within the Android Keystore system and require user authentication (biometrics or device credentials) for use.

### Cross-Platform Frameworks (React Native, Flutter)
- **JavaScript/Dart Obfuscation:** Verify that code obfuscation (e.g., ProGuard/R8 for Android, Hermes for React Native, Dart obfuscation for Flutter) is enabled for release builds.
- **Secure Storage Plugins:** Ensure that cross-platform secure storage plugins (e.g., `react-native-keychain`, `flutter_secure_storage`) correctly utilize the underlying native secure storage mechanisms (Keychain/Keystore).
- **Bridge Security:** Audit the communication bridge between the JavaScript/Dart context and native code for injection vulnerabilities and insecure data passing.

## False-Positive Controls and Validation
- **OS-Level Protections:** A finding regarding insecure file storage may be a false positive if the device's full-disk encryption provides sufficient protection for the specific data type, based on the threat model.
- **Server-Side Validation:** A client-side input validation bypass is a lower severity finding (or false positive) if the server strictly validates the same input and rejects malicious payloads.
- **Development vs. Release:** Findings related to debugging flags, cleartext traffic, or verbose logging are often false positives if they are strictly confined to development or staging build variants.

## Remediation Roadmap Integration
When generating the final Security Audit Report, ensure that mobile-specific findings are integrated into the Remediation Roadmap with clear, platform-specific code examples. For instance, if insecure storage is found on Android, provide the exact Kotlin code to implement `EncryptedSharedPreferences`. If found on iOS, provide the Swift code for Keychain integration.

## Advanced Threat Modeling for Mobile Clients

Mobile applications operate in a unique threat landscape where the device itself cannot be trusted. The review must consider scenarios where an attacker has full control over the device, including the ability to inspect memory, modify the file system, and intercept network traffic.

When evaluating the application's architecture, consider the implications of a compromised device. If the application relies on client-side logic to enforce security policies, an attacker can easily bypass these controls by modifying the application binary or hooking into the runtime environment using tools like Frida or Xposed. Therefore, the review must ensure that all critical security decisions are made on the server, and the client is treated merely as a presentation layer.

Furthermore, the review must assess the application's resilience against reverse engineering. While obfuscation and anti-tampering techniques cannot prevent a determined attacker, they can significantly increase the effort required to understand and modify the application. The review should verify that these techniques are applied appropriately, balancing security with performance and maintainability.

## Summary of Key Review Areas

| Review Area | Primary Focus | Expected Outcome |
| :--- | :--- | :--- |
| **Data Storage** | Keychain, Keystore, SQLite, SharedPreferences | Sensitive data is encrypted at rest using platform-provided secure storage. |
| **Network Security** | TLS configuration, Certificate Pinning | All communication is encrypted; pinning is used for high-security apps. |
| **Platform Integration** | IPC, Intents, Exported Components | Components are protected by permissions; input is validated. |
| **Authentication** | Session management, Biometrics | Tokens are stored securely; biometrics unlock tokens, not bypass auth. |
| **Code Quality** | Obfuscation, Debug flags, Hardcoded secrets | Release builds are optimized, obfuscated, and free of embedded secrets. |

This reference file serves as the definitive guide for the mobile-client dimension of the security review process. By adhering to these guidelines, the review agent can systematically identify and document vulnerabilities, providing actionable remediation advice to improve the application's security posture.
