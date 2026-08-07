# Security Architecture

## Table of Contents
1. Threat Modeling
2. Zero Trust Architecture
3. Cryptography and Data Protection
4. AI/Agentic Threat Modeling

---

## 1. Threat Modeling

Threat modeling is a structured approach to identifying and mitigating security risks in system design.

### Methodologies

- **STRIDE:** Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege. Useful for identifying threats in software design.
- **PASTA:** Process for Attack Simulation and Threat Analysis. A risk-centric approach.
- **LINDDUN:** Focuses on privacy threats (Linkability, Identifiability, Non-repudiation, Detectability, Disclosure of information, Unawareness, Non-compliance).

### Process

1. **Decompose the Application:** Create data flow diagrams (DFDs) to understand how data moves through the system. Identify trust boundaries.
2. **Identify Threats:** Use a methodology like STRIDE to identify potential threats at each trust boundary and component.
3. **Determine Mitigations:** Design security controls to mitigate the identified threats.
4. **Validate:** Review the threat model to ensure all threats are addressed and mitigations are effective.

---

## 2. Zero Trust Architecture

Zero Trust is a security model based on the principle of "never trust, always verify." It assumes that threats exist both inside and outside the network perimeter.

**Canonical Source:** [NIST SP 800-207 Zero Trust Architecture](https://csrc.nist.gov/publications/detail/sp/800-207/final)
**Verification:** Verify current Zero Trust principles from the canonical source.

### Core Principles

- All data sources and computing services are considered resources.
- All communication is secured regardless of network location.
- Access to individual enterprise resources is granted on a per-session basis.
- Access to resources is determined by dynamic policy.
- The enterprise monitors and measures the integrity and security posture of all owned and associated assets.
- All resource authentication and authorization are dynamic and strictly enforced before access is allowed.
- The enterprise collects as much information as possible about the current state of assets, network infrastructure and communications and uses it to improve its security posture.

---

## 3. Cryptography and Data Protection

Do not rely on hardcoded cryptographic algorithm recommendations, as they become obsolete. Always verify current recommendations from authoritative sources.

**Canonical Source:** [NIST Cryptographic Standards and Guidelines](https://csrc.nist.gov/projects/cryptographic-standards-and-guidelines)
**Verification:** Verify current approved cryptographic algorithms and key lengths from the canonical source at runtime.

### Principles

- **Use Standard Algorithms:** Never invent custom cryptographic algorithms. Use well-established, peer-reviewed algorithms.
- **Key Management:** The security of cryptography relies on the secrecy of the keys. Implement robust key generation, storage, rotation, and destruction processes. Use dedicated Key Management Systems (KMS) or Hardware Security Modules (HSM).
- **Encryption at Rest:** Protect data stored on disk.
- **Encryption in Transit:** Protect data moving across networks using TLS.
- **Hashing:** Use strong, salted hash functions for passwords (e.g., Argon2id, bcrypt).

---

## 4. AI/Agentic Threat Modeling

When designing systems that incorporate AI models or autonomous agents, specific threat modeling is required.

**Canonical Source:** [MITRE ATLAS (Adversarial Threat Landscape for AI Systems)](https://atlas.mitre.org/)
**Verification:** Verify current AI threat tactics and techniques from the canonical source.

### Key Considerations

- **Data Poisoning:** Attackers manipulating training data to influence model behavior.
- **Prompt Injection:** Attackers crafting inputs to bypass safety filters or alter the intended behavior of an LLM.
- **Model Inversion/Extraction:** Attackers extracting sensitive information from the model or stealing the model itself.
- **Agent Autonomy:** Limit the blast radius of autonomous agents by enforcing least privilege and requiring human-in-the-loop confirmation for critical actions.
- **Supply Chain:** Verify the provenance and integrity of pre-trained models and datasets.
