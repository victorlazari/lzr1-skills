# AI Security and Compliance Reference

## 1. AI Security Audit and Hardening

AI systems introduce unique security challenges. A comprehensive security audit covers the entire AI lifecycle, from data ingestion to deployment.

Threat modeling frameworks like STRIDE for AI and MITRE ATLAS help identify vulnerabilities. Training data security involves verifying data provenance, preventing data poisoning, enforcing access controls, and encrypting data. Privacy considerations include PII/PHI sanitization and differential privacy.

AI models are susceptible to adversarial attacks, such as evasion attacks, model inversion, membership inference, and prompt injection. Model integrity and supply chain security involve auditing the training process for neural trojans and verifying third-party models.

Infrastructure and deployment security require rigorous cloud-native best practices, including container image scanning, Kubernetes security posture, secret management, and API security. A robust Identity Access Management (IAM) strategy is critical, enforcing Role-Based Access Control (RBAC) and the Principle of Least Privilege (PoLP).

Hardening strategies include adversarial training, ensemble methods, output sanitization, network segmentation, immutable infrastructure, and runtime protection.

## 2. Compliance and Frameworks

- **MITRE ATLAS**: Adversarial Threat Landscape for AI Systems. Use for threat modeling and understanding adversarial tactics.
- **NIST AI RMF**: AI Risk Management Framework. Use for comprehensive risk assessment and governance.

Verified against upstream: 2026-08-07
