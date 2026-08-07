# Security Review Authoritative Source Matrix

**Verified against upstream: 2026-08-07**

## Purpose and Boundaries
This reference provides the master source-to-control map for the `security-review` super-agent. It governs the execution of the line-by-line code audit across more than 50 verified primary source families from major standards bodies, government agencies, foundations, and platform publishers. This is defensive code-review guidance, not an exploitation manual. The review must record target scope, environment, jurisdiction, contractual obligations, and evidence before asserting compliance. Never claim certification or guaranteed absence of vulnerabilities. Never instruct the agent to execute target code, upload proprietary material, expose secrets, or actively test production without explicit authorization.

## Table of Contents
- [Threat Assumptions and Review Procedure](#threat-assumptions-and-review-procedure)
- [Application and API Security](#application-and-api-security)
- [Identity and Authorization](#identity-and-authorization)
- [Vulnerability Intelligence and Scoring](#vulnerability-intelligence-and-scoring)
- [Supply Chain and Build](#supply-chain-and-build)
- [Cloud, Container, and IaC](#cloud-container-and-iac)
- [Mobile and Client](#mobile-and-client)
- [Privacy and Logging](#privacy-and-logging)
- [AI and LLM Security](#ai-and-llm-security)
- [Cryptography and Governance](#cryptography-and-governance)
- [Official References](#official-references)

## Threat Assumptions and Review Procedure
**Threat Assumptions:** Assume a zero-trust environment where all inputs are malicious, networks are compromised, and internal actors may be hostile.
**Review Procedure:**
1. **Discovery:** Perform read-only discovery of the target application architecture and data flows.
2. **Mapping:** Map identified components to the relevant authoritative sources in this matrix.
3. **Audit:** Execute line-by-line code review using the concrete checks defined for each source.
4. **Validation:** Validate findings against false-positive controls (e.g., verifying if a "secret" is a test fixture or a real credential).
5. **Reporting:** Generate structured findings with file/line evidence, CVSS scoring, and remediation steps.
**Stop/Escalation Rules:** Stop and escalate if the review encounters obfuscated malware, active exploitation indicators, or requires executing untrusted code.

## Application and API Security
| Source | Edition/Status | Governs | Volatile Refresh Points | Review Agent |
|---|---|---|---|---|
| OWASP Top 10:2025 | v2025; final | access control; security configuration; injection prevention | none identified | Security Review Agent |
| OWASP ASVS | v5.0.0; final | Validation and Business Logic; Injection Prevention | none identified | Security Review Agent |
| OWASP API Security Top 10 | 2023 Edition; final | authentication; authorization; resource management | API endpoint inventory; Rate limiting | API Security Agent |
| OWASP Cheat Sheet Series | runtime-current; living | authentication; input validation; cryptography | Specific library versions | Security Review Agent |
| SEI CERT Coding Standards | runtime-current; living | memory management; input/output; concurrency | none identified | Code Review Agent |
| RFC 9110 HTTP Semantics | RFC 9110; final | methods; fields; status semantics; intermediaries; request routing | none identified | Application and API Security Agent |

## Identity and Authorization
| Source | Edition/Status | Governs | Volatile Refresh Points | Review Agent |
|---|---|---|---|---|
| NIST SP 800-63-4 | v4; final | identity proofing; authentication; federation | none identified | Identity Proofing Agent |
| RFC 9700 OAuth 2.0 Security | RFC 9700; final | authentication; authorization; token management | none identified | Authorization Agent |
| RFC 8725 JWT Best Practices | RFC 8725; final | authentication; cryptography; data integrity | none identified | Authentication Agent |

## Vulnerability Intelligence and Scoring
| Source | Edition/Status | Governs | Volatile Refresh Points | Review Agent |
|---|---|---|---|---|
| MITRE CWE Top 25 | 2025 CWE Top 25; living | input validation; memory safety; authorization | none identified | Vulnerability Scanner Agent |
| Common Weakness Enumeration | v4.20; living | input validation; authorization; memory safety | none identified | Vulnerability Scanner Agent |
| MITRE ATT&CK | v19.0; living | tactics; techniques; mitigations | none identified | Threat Intelligence Agent |
| CAPEC | v3.9; living | attack patterns; threat modeling | none identified | Threat Modeling Agent |
| CISA KEV Catalog | runtime-current; living | vulnerability management; patch management | KEV catalog updates | Vulnerability Management Agent |
| CVSS v4.0 Specification | v1.2; final | vulnerability severity scoring; impact assessment | none identified | Vulnerability Management Agent |
| EPSS | runtime-current; living | vulnerability management; patch prioritization | EPSS score updates | Vulnerability Management Agent |
| CVE Program | runtime-current; living | vulnerability identification; cataloging | none identified | Vulnerability Management Agent |
| National Vulnerability Database | runtime-current; living | vulnerability management; compliance | none identified | Vulnerability Management Agent |
| SPDX Specification | v3.0.1; final | vulnerability management; assessment | none identified | Vulnerability Management Agent |
| OSV Schema | v1.9.0; living | vulnerability management; dependency management | none identified | Dependency Scanner Agent |

## Supply Chain and Build
| Source | Edition/Status | Governs | Volatile Refresh Points | Review Agent |
|---|---|---|---|---|
| CISA SBOM Guidance | runtime-current; living | software supply chain security; component transparency | none identified | Supply Chain Security Agent |
| Securing the Software Supply Chain | August 2022; final | Secure product criteria; Third-party component verification | none identified | Supply Chain Security Agent |
| OpenSSF Scorecard | v5.5.0; living | code vulnerabilities; source risk assessment | none identified | Source Code Management Agent |
| SLSA | v1.2; final | source integrity; build integrity; provenance | none identified | Build Platform Agent |
| Sigstore | runtime-current; living | authentication; integrity; supply chain security | none identified | Supply Chain Security Agent |
| in-toto Attestation Framework | v1.2; final | supply chain integrity; artifact provenance | none identified | Supply Chain Security Agent |
| CycloneDX Specification | v1.7; final | supply chain transparency; vulnerability management | none identified | Supply Chain Security Agent |

## Cloud, Container, and IaC
| Source | Edition/Status | Governs | Volatile Refresh Points | Review Agent |
|---|---|---|---|---|
| NIST SP 800-190 | Final; final | image vulnerabilities; container runtime configuration | none identified | Container Security Agent |
| NIST SP 800-204 | Final; final | authentication; secure communication; microservices | none identified | Microservices Security Agent |
| NIST SP 800-207 | vFinal; final | authentication; authorization; zero trust | none identified | Zero Trust Architecture Agent |
| Cloud Security Alliance CCM | v4.1; final | application & interface security; datacenter security | none identified | Cloud Security Assessment Agent |
| Kubernetes Pod Security Standards | runtime-current; living | container isolation; privilege escalation | none identified | Kubernetes Security Agent |
| Kubernetes Hardening Guide | Version 1.2; final | Pod security; Network separation and hardening | none identified | Kubernetes Security Agent |

## Mobile and Client
| Source | Edition/Status | Governs | Volatile Refresh Points | Review Agent |
|---|---|---|---|---|
| OWASP MASVS | v2.1.0; final | storage; cryptography; authentication and authorization | MASVS releases | Mobile Security Agent |
| OWASP MASTG | runtime-current; living | mobile test cases; platform-specific verification | test catalog and platform guidance | Mobile Security Agent |
| Android Security Best Practices | runtime-current; living | Android storage; IPC; network; permissions; WebView | Android and SDK releases | Mobile Security Agent |
| Apple Platform Security | runtime-current; living | iOS and Apple platform data protection; keychain; signing; transport | OS and platform releases | Mobile Security Agent |

## Privacy and Logging
| Source | Edition/Status | Governs | Volatile Refresh Points | Review Agent |
|---|---|---|---|---|
| GDPR | v2016-05-04; final | data protection; privacy; consent management | none identified | Privacy Agent |
| NIST Privacy Framework | v1.1 IPD; draft | privacy risk management; data processing | framework revisions | Privacy Agent |
| OWASP Logging Cheat Sheet | runtime-current; living | event selection; sanitization; access control; retention | guidance revisions | Privacy and Logging Agent |
| OWASP MASWE-0005 | runtime-current; living | sensitive data in logs | weakness catalog revisions | Mobile and Privacy Agent |
| OWASP MASTG-TEST-0296 | runtime-current; living | Android sensitive-data logging verification | test catalog revisions | Mobile and Privacy Agent |
| OWASP Log Injection Guidance | runtime-current; living | log neutralization; forged entries | guidance revisions | Privacy and Logging Agent |
| CWE-117 | CWE 4.20; living | improper output neutralization for logs | CWE revisions | Privacy and Logging Agent |
| CWE-209 | CWE 4.20; living | sensitive information in error messages | CWE revisions | Privacy and Logging Agent |

## AI and LLM Security
| Source | Edition/Status | Governs | Volatile Refresh Points | Review Agent |
|---|---|---|---|---|
| OWASP Top 10 for LLM | v2025; final | prompt injection; sensitive information disclosure | none identified | LLM Security Agent |
| OWASP GenAI Security Project | v2.01; living | Autonomy/Tool Use; Multi-Agent Coordination | none identified | Agentic Security Initiative |
| MITRE ATLAS | v2026.07; living | adversarial machine learning; AI system security | none identified | AI Security Agent |
| NIST SP 800-218A | Final; final | data provenance; model and weight protection | none identified | AI Security Agent |
| NIST AI Risk Management Framework | v1.0; living | AI risk management; trustworthiness | none identified | AI Risk Management Agent |
| NIST AI 600-1 | v1.0; final | CBRN Information; Data Privacy; Harmful Bias | none identified | AI Risk Management Agent |

## Cryptography and Governance
| Source | Edition/Status | Governs | Volatile Refresh Points | Review Agent |
|---|---|---|---|---|
| OWASP SAMM | v2.0; final | Governance; Design; Implementation; Verification | none identified | Security Review Agent |
| Secure by Design | runtime-current; living | authentication; logging; memory safety | none identified | Coordinator plus application/API, identity, and privacy/logging specialists |
| NIST SP 800-218 SSDF | Version 1.1; final | software development life cycle security | none identified | Software Development Agent |
| NIST SP 800-53 | Release 5.2.0; final | access control; audit and accountability | none identified | Compliance Agent |
| NIST CSF 2.0 | v2.0; final | governance; identify; protect; detect; respond | none identified | Enterprise Risk Management Agent |
| NIST SP 800-61 Rev 3 | v3.0.0; final | incident response; cybersecurity risk management | none identified | Incident Response Agent |
| CIS Critical Security Controls | v8.1; final | asset management; configuration management | none identified | Security Review Agent |
| CIS Benchmarks | runtime-current; living | configuration management; access control | none identified | Configuration Review Agent |
| PCI DSS | v4.0.1; final | network security; secure configuration; data protection | none identified | Coordinator plus cloud/IaC, application/API, and privacy/logging specialists |
| ISO/IEC 27001 | Edition 3; partly-paywalled | information security management; risk management | none identified | Information Security Management Agent |
| FIPS 140-3 | Final; final | cryptographic module specification; physical security | none identified | Cryptography Agent |
| NIST Cryptographic Standards and Guidelines | runtime-current; living | algorithms; key management; transitions; validated modules | standards and transition updates | Cryptography Agent |
| OWASP Cryptographic Storage Cheat Sheet | runtime-current; living | data-at-rest design; algorithms; key lifecycle | guidance revisions | Cryptography Agent |
| OWASP Secrets Management Cheat Sheet | runtime-current; living | secret lifecycle; rotation; access; logging | guidance revisions | Secrets Agent |

## Official References
- [OWASP Top 10:2025](https://owasp.org/Top10/2025/en/)
- [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/)
- [OWASP API Security Top 10 2023](https://owasp.org/API-Security/editions/2023/en/0x11-t10/)
- [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/)
- [OWASP MASVS](https://mas.owasp.org/MASVS/)
- [OWASP SAMM](https://owaspsamm.org/)
- [OWASP Top 10 for LLM](https://genai.owasp.org/llm-top-10/)
- [OWASP GenAI Security Project](https://genai.owasp.org/)
- [MITRE CWE Top 25](https://cwe.mitre.org/top25/)
- [Common Weakness Enumeration](https://cwe.mitre.org/)
- [MITRE ATT&CK](https://attack.mitre.org/)
- [CAPEC](https://capec.mitre.org/)
- [MITRE ATLAS](https://atlas.mitre.org/)
- [CISA KEV Catalog](https://www.cisa.gov/known-exploited-vulnerabilities-catalog)
- [Secure by Design](https://www.cisa.gov/securebydesign)
- [CISA SBOM Guidance](https://www.cisa.gov/sbom)
- [Securing the Software Supply Chain](https://www.cisa.gov/sites/default/files/publications/ESF_SECURING_THE_SOFTWARE_SUPPLY_CHAIN_DEVELOPERS.PDF)
- [NIST SP 800-218 SSDF](https://csrc.nist.gov/pubs/sp/800/218/final)
- [NIST SP 800-218A](https://csrc.nist.gov/pubs/sp/800/218/a/final)
- [NIST SP 800-53](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final)
- [NIST CSF 2.0](https://www.nist.gov/cyberframework)
- [NIST SP 800-61 Rev 3](https://csrc.nist.gov/pubs/sp/800/61/r3/final)
- [NIST SP 800-63-4](https://pages.nist.gov/800-63-4/)
- [NIST SP 800-190](https://csrc.nist.gov/pubs/sp/800/190/final)
- [NIST SP 800-204](https://csrc.nist.gov/pubs/sp/800/204/final)
- [NIST SP 800-207](https://csrc.nist.gov/pubs/sp/800/207/final)
- [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework)
- [NIST AI 600-1](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf)
- [CVSS v4.0 Specification](https://www.first.org/cvss/v4-0/specification-document)
- [EPSS](https://www.first.org/epss/)
- [CVE Program](https://www.cve.org/)
- [National Vulnerability Database](https://nvd.nist.gov/)
- [OpenSSF Scorecard](https://scorecard.dev/)
- [SLSA](https://slsa.dev/spec/)
- [Sigstore](https://docs.sigstore.dev/)
- [in-toto Attestation Framework](https://github.com/in-toto/attestation)
- [SPDX Specification](https://spdx.dev/specifications/)
- [CycloneDX Specification](https://cyclonedx.org/specification/overview/)
- [OSV Schema](https://ossf.github.io/osv-schema/)
- [CIS Critical Security Controls](https://www.cisecurity.org/controls)
- [CIS Benchmarks](https://www.cisecurity.org/cis-benchmarks)
- [Cloud Security Alliance CCM](https://cloudsecurityalliance.org/research/cloud-controls-matrix)
- [Kubernetes Pod Security Standards](https://kubernetes.io/docs/concepts/security/pod-security-standards/)
- [Kubernetes Hardening Guide](https://media.defense.gov/2022/Aug/29/2003066362/-1/-1/0/CTR_KUBERNETES_HARDENING_GUIDANCE_1.2_20220829.PDF)
- [PCI DSS](https://www.pcisecuritystandards.org/standards/pci-dss/)
- [ISO/IEC 27001](https://www.iso.org/standard/82875.html)
- [GDPR](https://eur-lex.europa.eu/eli/reg/2016/679/oj)
- [NIST Privacy Framework](https://www.nist.gov/privacy-framework)
- [RFC 9700 OAuth 2.0 Security](https://www.rfc-editor.org/rfc/rfc9700.html)
- [RFC 8725 JWT Best Practices](https://www.rfc-editor.org/rfc/rfc8725.html)
- [FIPS 140-3](https://csrc.nist.gov/pubs/fips/140-3/final)
- [SEI CERT Coding Standards](https://cmu-sei.github.io/secure-coding-standards/)
- [RFC 9110 HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110.html)
- [OWASP MASTG](https://mas.owasp.org/MASTG/)
- [Android Security Best Practices](https://developer.android.com/privacy-and-security/security-best-practices)
- [Apple Platform Security](https://support.apple.com/guide/security/welcome/web)
- [OWASP Logging Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html)
- [OWASP MASWE-0005](https://mas.owasp.org/MASWE/MASVS-STORAGE/MASWE-0005/)
- [OWASP MASTG-TEST-0296](https://mas.owasp.org/MASTG/tests/ios/MASVS-STORAGE/MASTG-TEST-0296/)
- [OWASP Log Injection Guidance](https://owasp.org/www-community/attacks/Log_Injection)
- [CWE-117](https://cwe.mitre.org/data/definitions/117.html)
- [CWE-209](https://cwe.mitre.org/data/definitions/209.html)
- [NIST Cryptographic Standards and Guidelines](https://csrc.nist.gov/projects/cryptographic-standards-and-guidelines)
- [OWASP Cryptographic Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html)
- [OWASP Secrets Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html)
