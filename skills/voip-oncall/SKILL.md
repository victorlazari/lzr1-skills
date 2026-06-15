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
