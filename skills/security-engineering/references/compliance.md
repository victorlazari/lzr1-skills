# Compliance and Governance

## Table of Contents
1. Compliance Frameworks
2. Audits and Assessments
3. Governance Principles

---

## 1. Compliance Frameworks

Compliance frameworks provide structured guidelines for managing security risks and protecting sensitive data. Do not rely on hardcoded framework versions or specific control requirements, as they are updated periodically. Always verify the current requirements from the authoritative sources.

### Common Frameworks

- **SOC 2 (Service Organization Control 2):** Focuses on security, availability, processing integrity, confidentiality, and privacy of customer data.
  - **Canonical Source:** [AICPA SOC 2](https://us.aicpa.org/interestareas/frc/assuranceadvisoryservices/aicpasoc2report)
- **ISO/IEC 27001:** International standard for Information Security Management Systems (ISMS).
  - **Canonical Source:** [ISO 27001](https://www.iso.org/isoiec-27001-information-security.html)
- **PCI DSS (Payment Card Industry Data Security Standard):** Requirements for organizations that handle branded credit cards.
  - **Canonical Source:** [PCI Security Standards Council](https://www.pcisecuritystandards.org/)
- **HIPAA (Health Insurance Portability and Accountability Act):** US legislation that provides data privacy and security provisions for safeguarding medical information.
  - **Canonical Source:** [HHS HIPAA](https://www.hhs.gov/hipaa/index.html)
- **GDPR (General Data Protection Regulation):** EU regulation on data protection and privacy.
  - **Canonical Source:** [GDPR.eu](https://gdpr.eu/)
- **NIST Cybersecurity Framework (CSF):** Voluntary framework consisting of standards, guidelines, and best practices to manage cybersecurity risk.
  - **Canonical Source:** [NIST CSF](https://www.nist.gov/cyberframework)

### Mapping Requirements to Controls

When working with compliance, the primary task is mapping framework requirements to architectural and operational controls.

1. **Identify Requirements:** Determine which frameworks apply to the organization or system.
2. **Select Controls:** Choose appropriate security controls (e.g., encryption, access control, logging) to meet the requirements.
3. **Implement Controls:** Integrate the controls into the system architecture and DevSecOps pipeline.
4. **Gather Evidence:** Continuously collect evidence (e.g., logs, configurations, scan results) to demonstrate that controls are operating effectively.

---

## 2. Audits and Assessments

Audits verify that an organization is adhering to its stated security policies and compliance requirements.

- **Internal Audits:** Conducted by the organization itself to assess readiness and identify gaps.
- **External Audits:** Conducted by independent third parties to provide formal certification or attestation (e.g., SOC 2 Type II report).
- **Continuous Compliance:** Moving away from point-in-time audits to continuous monitoring of controls using automated tools (CSPM, IaC scanning).

---

## 3. Governance Principles

Governance ensures that security strategies align with business objectives and risk tolerance.

- **Risk Management:** Identify, assess, and prioritize risks. Implement controls to mitigate risks to an acceptable level.
- **Policies and Procedures:** Develop and maintain clear security policies, standards, and procedures.
- **Security Awareness Training:** Educate employees on security best practices and their responsibilities.
- **Vendor Risk Management:** Assess and monitor the security posture of third-party vendors and service providers.
