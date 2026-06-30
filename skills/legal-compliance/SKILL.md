---
name: legal-compliance
description: Comprehensive legal and compliance skill covering corporate law, contracts, intellectual property, data privacy (GDPR/CCPA), regulatory compliance, and risk management for technology companies. Use when drafting contracts, reviewing legal risks, building compliance programs, managing IP, or navigating regulatory requirements.
---

# Legal & Compliance

Expert-level legal and compliance covering corporate law, contracts, IP, data privacy, regulatory compliance, and risk management for technology companies.

## When to Use

- Drafting or reviewing contracts and agreements
- Building compliance programs (SOC2, GDPR, HIPAA)
- Managing intellectual property and patents
- Data privacy and protection requirements
- Corporate governance and entity management
- Risk assessment and mitigation
- Regulatory navigation and licensing
- Employment law and HR legal matters

## Workflow

1. **Understand the context** — What jurisdiction, business model, and legal question?
2. **Select reference** — Choose the appropriate domain:
   - Contracts and commercial law → `references/contracts.md`
   - Data privacy and protection → `references/privacy.md`
   - Compliance programs → `references/compliance-programs.md`
   - IP and corporate law → `references/corporate-ip.md`
3. **Research** — Applicable laws, regulations, precedents
4. **Analyze** — Risk assessment, gap analysis
5. **Advise** — Recommendations with risk/benefit tradeoffs
6. **Document** — Policies, contracts, or compliance artifacts

## Core Principles (All Legal Work)

- Risk-based: Prioritize by likelihood and impact
- Jurisdiction-aware: Laws vary by location; always specify
- Practical: Balance legal perfection with business needs
- Preventive: Proactive compliance beats reactive firefighting
- Documented: If it's not written down, it doesn't exist
- Proportionate: Controls should match the risk level
- Current: Laws change; stay updated on regulatory shifts
- Disclaimer: AI cannot replace qualified legal counsel for specific matters

## Role Capabilities

| Role | Expertise | Reference |
|---|---|---|
| General Counsel | Corporate, governance, strategy | `references/corporate-ip.md` |
| Contracts Attorney | Commercial agreements, negotiation | `references/contracts.md` |
| Privacy Counsel | GDPR, CCPA, data protection | `references/privacy.md` |
| Compliance Officer | Programs, audits, certifications | `references/compliance-programs.md` |
| IP Counsel | Patents, trademarks, trade secrets | `references/corporate-ip.md` |

## Key References

- **Contracts**: See `references/contracts.md` for agreements and commercial law.
- **Privacy**: See `references/privacy.md` for data protection and privacy.
- **Compliance programs**: See `references/compliance-programs.md` for certifications and audits.
- **Corporate and IP**: See `references/corporate-ip.md` for governance and intellectual property.
- **Recommended reading**: See `references/reading-list.md` for curated books and articles.

---

## Multi-Specialist Protocol

> **Replaces the single "Select reference" step.** When multiple domains are detected, spawn all relevant specialists simultaneously — do not serialize them.

### Domain Detection Table

Scan the task for signals that indicate which domains apply:

| Task Signal (examples) | Domain | Specialist Agent | Reference |
|---|---|---|---|
| `contract`, ... | **Contract Law** | Contract Specialist | `references/complete-reference.md` |
| `regulatory`, ... | **Regulatory Compliance** | Regulatory Specialist | `references/complete-reference.md` |
| `IP`, ... | **Intellectual Property** | IP Specialist | `references/complete-reference.md` |
| `data privacy`, ... | **Data Privacy** | Privacy Specialist | `references/complete-reference.md` |

### Spawning Logic

**Single domain detected** → Fall back to original single-reference behavior (no change).

**Multiple domains detected** → Launch all relevant specialists simultaneously:
- Each specialist receives: **full task context** + its dedicated reference file only
- No specialist waits for another — all start at the same time
- Maximum concurrent specialists: 4

### Cross-Domain Synthesizer

After all specialists complete, run one **Legal Risk Synthesizer** with all specialist outputs that:

1. **Identifies contradictions** between specialist recommendations for the same component
2. **Identifies gaps** — requirements addressed by no specialist
3. **Identifies dependencies** — where Domain A's output is a prerequisite for Domain B's recommendation
4. **Produces** a unified recommendation with explicit trade-off annotations for any resolved contradictions

> Synthesis focus for this skill: Flags where a data handling practice violates multiple regulatory frameworks simultaneously. Maps IP risks to contract clause gaps.
