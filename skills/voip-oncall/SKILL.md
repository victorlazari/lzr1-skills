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

## Sub-Agent Spawning

This skill supports spawning sub-agents for parallel execution when tasks can be decomposed:

| Trigger Condition | Sub-Agent Type | Purpose |
|---|---|---|
| Multiple SIP trunks to configure | SIP Configurator | Parallel configuration and validation of SIP trunks |
| Multiple escalation policies to test | Policy Tester | Parallel testing of escalation rules and delays |
| Multiple telecom regulations to audit | Compliance Auditor | Parallel compliance checks for A2P 10DLC, GDPR, STIR/SHAKEN |
| Bulk latency monitoring across regions | Network Monitor | Parallel monitoring of RTT, jitter, and packet loss |
| Multiple carrier failover scenarios | Failover Tester | Parallel simulation of carrier outages and routing |

### Spawning Rules
- Spawn when 3+ independent items need the same operation.
- Each sub-agent receives: context, specific target (e.g., specific SIP trunk or region), success criteria.
- Results are aggregated and cross-referenced for conflicts.
- Maximum concurrent sub-agents: 10.

## Workflow

1. **Requirement Analysis**: Understand the specific VoIP on-call requirements, whether it's setting up a new IVR, configuring SIP trunks, or auditing compliance.
2. **Architecture Design**: Design the call flow, redundancy strategies, and integration points (e.g., WebRTC, programmable APIs).
3. **Configuration Management**: Use the VoIP-OnCall CLI and configuration schemas (`global.yaml`, `sip_trunks.json`, `schedules.yaml`, `escalations.json`) to implement the design.
4. **Compliance Check**: Ensure all configurations adhere to relevant telecom regulations (A2P 10DLC, GDPR, STIR/SHAKEN).
5. **Testing and Validation**: Simulate incidents to test IVR acknowledgment, escalation policies, and failover mechanisms.
6. **Optimization**: Analyze logs and metrics to optimize latency, call quality, and costs.

## Core Principles

- **High Availability**: Always implement multi-carrier redundancy and failover mechanisms to ensure critical alerts are delivered.
- **Security First**: Use TLS for SIP signaling, SRTP for media encryption, and secure secrets management for API keys and passwords.
- **Compliance**: Strictly adhere to global telecom regulations to avoid message blocking and legal penalties.
- **Cost Efficiency**: Optimize call flows, leverage least-cost routing, and use AI/automation to reduce unnecessary telecom expenses.
- **User Experience**: Design intuitive IVR prompts with NLP and ensure low-latency, high-quality audio for WebRTC war rooms.

## Key References

- [RFC 3261: SIP: Session Initiation Protocol](https://tools.ietf.org/html/rfc3261)
- [WebRTC Official Site](https://webrtc.org/)
- [Twilio Programmable Voice API Documentation](https://www.twilio.com/docs/voice)
- [GSMA A2P 10DLC Guidelines](https://www.gsma.com/newsroom/press-release/a2p-10dlc-messaging/)
- [European Commission GDPR](https://gdpr-info.eu/)
- [FCC STIR/SHAKEN](https://www.fcc.gov/call-authentication-stir-shaken)
- [ITU-T Y.1541: Network Performance Objectives for IP-based Services](https://www.itu.int/rec/T-REC-Y.1541/en)
- [Vonage Voice APIs and SDKs](https://developer.vonage.com/voice/voice-api/overview)

---

## Adversarial Verification Panel

For each significant VoIP on-call configuration finding or compliance issue produced by the parallel sub-agents:

1. Spawn **3 independent Refuter Agents** per finding, each with:
   - The finding in full
   - Instruction: *"Assume this finding is wrong. Find the strongest argument against it."*
   - Default stance: `refuted=true` if evidence is insufficient or ambiguous
2. A finding is **confirmed** only if ≥2 refuters fail to refute it
3. A finding is **discarded** if ≥2 refuters succeed
4. When a confirmed finding had 1 successful refuter, include the dissenting argument in the output with a `CONTESTED` label

> This prevents plausible-but-wrong VoIP on-call configuration findings from reaching the final output. The 3-vote panel eliminates single-point hallucination without requiring unanimity.

## Cross-System Consistency Validator

After all parallel agents (SIP Configurator, Policy Tester, Compliance Auditor, Network Monitor, Failover Tester) complete, but **before** synthesis:

Run one **Consistency Validator Agent** with all parallel outputs that:
- Flags any pair of recommendations that logically contradict each other
  *(example: the Network Monitor recommends adding a low-latency carrier in a region where the Failover Tester flagged that same carrier as unreliable and recommends removing it from the routing pool)*
- Notes where one agent's output is a prerequisite for another agent's recommendation
- Passes contradictions to the Synthesis Agent as `MUST_RESOLVE` items
- Passes missing prerequisites as `SEQUENCING_REQUIRED` items

## Synthesis Agent (Upgraded)

The synthesis step actively resolves rather than aggregates:

1. **`MUST_RESOLVE` contradictions**: Pick the better recommendation, annotate the reasoning, preserve the dissenting view as a footnote
2. **`SEQUENCING_REQUIRED` items**: Re-order the unified on-call readiness report so prerequisites appear before the steps that depend on them
3. **Confidence calibration**: Label each finding `HIGH` / `MEDIUM` / `LOW` confidence based on refuter panel outcomes
4. **Gap analysis**: Note any analysis dimension not covered by any of the parallel agents — these are blind spots, not confirmed negatives
