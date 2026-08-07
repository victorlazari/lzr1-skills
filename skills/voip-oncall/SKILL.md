---
name: voip-oncall
description: Comprehensive mastery of VoIP On-Call Services, including advanced IVR, WebRTC integration, telecom regulations, programmable voice APIs, and cost optimization.
---

# VoIP On-Call Services Specialist

## When to Use

Use this skill when tasks involve designing, configuring, troubleshooting, or optimizing VoIP-based on-call communication systems. This includes:
- Implementing advanced Interactive Voice Response (IVR) systems for incident acknowledgment.
- Integrating WebRTC for browser-based war rooms and real-time collaboration.
- Navigating global telecom regulations such as A2P 10DLC, GDPR, and STIR/SHAKEN.
- Utilizing programmable voice APIs (e.g., Twilio, Vonage) for custom call flows.
- Handling carrier outages, latency issues, and multi-carrier redundancy strategies.
- Optimizing costs for high-volume alerting and messaging.
- Managing VoIP-OnCall CLI commands and configuration schemas (e.g., SIP trunks, schedules, escalations).

## Preconditions and Safety

- **Read-only Discovery:** Always perform read-only discovery of current configurations before making changes.
- **Confirmation Required:** Require explicit user confirmation before applying destructive, external, privileged, financial, legal, or production-impacting actions (e.g., deploying SIP configurations, modifying escalation policies).
- **Compliance Checks:** Explicitly require compliance checks for A2P 10DLC, GDPR, and STIR/SHAKEN before deployment.
- **Source Freshness:** Verify volatile facts (e.g., API versions, compliance rules) against official current documentation or bundled verified references.

## Workflow

1. **Requirement Analysis**: Analyze VoIP on-call requirements and architecture design.
2. **Compliance Check**: Check compliance against A2P 10DLC, GDPR, and STIR/SHAKEN guidelines.
3. **Configuration Management**: Configure SIP trunks using `templates/sip-config.yaml`.
4. **Testing and Validation**: Validate configuration and run `scripts/test-ivr.sh` to verify call flows (use dry-run where possible).
5. **Deployment**: Deploy configuration after confirmation and successful validation.
6. **Stop/Rollback**: Stop when deployment is successful and verified, or rollback if validation fails.

## Resources

- [Complete Reference](references/complete-reference.md): Detailed technical and operational exploration of VoIP on-call services.
- [Test IVR Script](scripts/test-ivr.sh): Automate IVR testing with dry-run support.
- [SIP Config Template](templates/sip-config.yaml): Standardize SIP trunk configuration.

## Output Contract

The final output must include:
- A structured summary of the configuration changes made.
- Evidence of successful validation (e.g., dry-run output).
- A clear statement of compliance with relevant regulations.
- Actionable next steps or rollback instructions if applicable.

## Authoritative sources

- [Authoritative source map](references/source-map.md) — consult this before relying on volatile upstream behavior.

## Package resource index

| Resource | Purpose |
|---|---|
| [references/source-map.md](references/source-map.md) | Supporting package resource; inspect before use and apply the workflow’s safety and validation gates. |
