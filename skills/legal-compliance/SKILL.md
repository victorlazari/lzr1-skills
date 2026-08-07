---
name: legal-compliance
description: Comprehensive legal and compliance skill covering corporate law, contracts, intellectual property, data privacy (GDPR/CCPA), regulatory compliance, and risk management for technology companies. Use when drafting contracts, reviewing legal risks, building compliance programs, managing IP, or navigating regulatory requirements.
---

# Legal & Compliance

Expert-level legal and compliance covering corporate law, contracts, IP, data privacy, regulatory compliance, and risk management for technology companies.

## Scope and Triggers

- **Scope**: Drafting or reviewing contracts, building compliance programs (SOC2, GDPR, HIPAA, PCI DSS), managing intellectual property, data privacy, corporate governance, risk assessment, and employment law.
- **Triggers**: Activates when tasks involve legal agreements, compliance audits, privacy regulations, or corporate structuring.
- **Non-goals**: Does not provide formal legal counsel or represent clients in litigation. All outputs must include a disclaimer.

## Preconditions

- Detect the jurisdiction, business model, and specific legal/compliance domain involved.
- Identify the target regulatory framework (e.g., GDPR, CCPA, PCI DSS) and verify its current version.

## Source Freshness

- Verify the current status of regulations via their canonical URLs before providing definitive compliance advice.
- See domain references for specific canonical URLs and verification dates.

## Workflow

1. **Detect Domain**: Identify the legal/compliance domain(s) involved in the task.
2. **Spawn Specialists**: If multiple domains are detected, spawn specialists concurrently with their respective reference files (max 4).
   - Contract Law → `references/contracts.md`
   - Regulatory Compliance → `references/compliance-programs.md`
   - Intellectual Property → `references/corporate-ip.md`
   - Data Privacy → `references/privacy.md`
3. **Verify Freshness**: Verify the freshness of the relevant regulations using the embedded canonical URLs.
4. **Generate Artifact**: Generate the required legal or compliance artifact.
5. **Synthesize**: If multiple specialists were spawned, run the Legal Risk Synthesizer to resolve contradictions and identify gaps.
6. **Validate**: Run `scripts/validate-compliance-checklist.py` to ensure the artifact meets structural requirements.
7. **Present**: Present the final artifact to the user with appropriate legal disclaimers.

## Safety

- **Read-only**: Discovery of legal requirements and gap analysis.
- **Confirmation Required**: Require explicit user confirmation before generating final legal documents or compliance reports.
- **Disclaimer**: Ensure all generated advice includes a disclaimer that it does not constitute formal legal counsel.

## Validation

- Use `scripts/validate-compliance-checklist.py` to validate that generated compliance artifacts meet minimum structural requirements based on the selected framework.
- Implement dry-run mode for the validation script.
- Validate that all referenced regulatory frameworks are explicitly versioned in the output.

## Failure Handling

- If a regulatory source is unreachable, fall back to the bundled verified references and note the inability to verify freshness.
- If the validation script fails, review the output against the specific framework requirements and adjust the artifact.

## Output Contract

- **Structure**: Clear, structured legal or compliance documents with explicit versioning of referenced frameworks.
- **Evidence**: Citations to canonical regulatory sources.
- **Actionable Steps**: Clear recommendations with risk/benefit tradeoffs.

## Resources

- `references/contracts.md`: Contracts and commercial law.
- `references/compliance-programs.md`: Compliance programs (SOC 2, ISO 27001, HIPAA, PCI DSS).
- `references/corporate-ip.md`: Corporate governance and intellectual property.
- `references/privacy.md`: Data privacy and protection (GDPR, CCPA).
- `scripts/validate-compliance-checklist.py`: Deterministic script to validate compliance artifacts.

## Orchestration

- **Multi-Specialist Protocol**: When multiple domains are detected, spawn all relevant specialists simultaneously.
- **Legal Risk Synthesizer**: After all specialists complete, run one synthesizer to identify contradictions, gaps, and dependencies, producing a unified recommendation with explicit trade-off annotations.
