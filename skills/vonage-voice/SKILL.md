---
name: vonage-voice
description: Comprehensive mastery of the Vonage Voice API for building outbound calls, IVR systems, and programmable voice flows. Use when configuring outbound calls with NCCO actions, handling DTMF/ASR user input, implementing webhooks (answer and event), controlling active calls via REST API, or building any Vonage Voice integration including talk, stream, record, connect, notify, wait, and transfer actions.
---

# Vonage Voice API Specialist

## Overview
This skill provides comprehensive mastery of the Vonage Voice API, focusing on configuring outbound calls, defining NCCO (Nexmo Call Control Object) actions, handling user input (DTMF and ASR), and executing server-side logic via webhooks.

## Capabilities
- **Outbound Calls:** Making outbound calls via the REST API to connect to PSTN, SIP, or WebSockets.
- **Call Flow Control:** Designing and serving JSON-based NCCO arrays to direct call execution.
- **User Input:** Prompting users and capturing DTMF keypad presses and ASR (Automatic Speech Recognition).
- **Webhooks:** Handling Answer Webhooks to serve NCCOs and Event Webhooks to monitor call status and user inputs, including signed webhooks.
- **Advanced Actions:** Utilizing `talk`, `stream`, `record`, `connect`, `notify`, `wait`, and `transfer` actions.

## Prerequisites & Setup
Before implementing a Vonage Voice flow, ensure the following setup:
1. **Vonage Account:** Create an account and obtain the API Key and API Secret.
2. **Virtual Number:** Purchase a Vonage virtual number to use as the Caller ID (`from` number).
3. **Application Setup:** Create a Voice-enabled Vonage Application.
   - Configure the **Answer Webhook** (where Vonage requests the initial NCCO).
   - Configure the **Event Webhook** (where Vonage sends call status updates).
   - Generate a private key for JWT authentication.
4. **Link Number:** Link the purchased virtual number to the Application.

## Source Freshness
Verified against upstream: 2026-08-07
- Vonage Voice API Overview: https://developer.vonage.com/en/voice/voice-api/overview
- Vonage Voice API NCCO Reference: https://developer.vonage.com/en/voice/voice-api/ncco-reference
- Vonage Voice API Webhooks Reference: https://developer.vonage.com/en/voice/voice-api/webhook-reference
- Vonage Voice API Reference: https://developer.vonage.com/en/api/voice
- Vonage Voice API DTMF Concepts: https://developer.vonage.com/en/voice/voice-api/concepts/dtmf
- Vonage Voice API ASR Concepts: https://developer.vonage.com/en/voice/voice-api/concepts/asr

## Reference Materials
For detailed implementation instructions, refer to the specialized guides in the `references` directory:

- [Outbound Calls and Webhooks](references/outbound-calls-webhooks.md): Master the REST API for initiating calls, JWT authentication, and webhook handling (including signed webhooks and SIP headers).
- [NCCO Actions Reference](references/ncco-actions.md): Complete guide to all NCCO actions, including `talk`, `connect`, `record`, and `transfer`.
- [Handling User Input (DTMF & ASR)](references/user-input.md): Detailed patterns for building Interactive Voice Response (IVR) systems, including Google ASR configuration.

## Workflow
1. **Discover findings:** Identify current Vonage branding, API capabilities, and security practices.
2. **Classify findings:** Categorize findings into NCCO actions, outbound calls and webhooks, and user input.
3. **Fix one bounded set:** Update the corresponding reference file with the classified findings.
4. **Run targeted checks:** Verify that the updated reference file is accurate and complete.
5. **Run the reviewer again:** Review the updated reference file for consistency and clarity.
6. **Compare remaining findings:** Identify any remaining findings that need to be addressed.
7. **Stop** when no actionable findings remain, the iteration cap is reached, or progress stalls.

## Safety
- **Read-only discovery:** Always verify current API documentation and installed versions before making changes.
- **Mutations:** Require confirmation for destructive, external, privileged, financial, legal, or production-impacting actions.
- **Signed Webhooks:** Ensure webhook handlers can process signed webhooks for enhanced security.

## Validation
- Verify that all API endpoints use the correct base URL (`api.nexmo.com` for v1).
- Ensure that ASR configurations include the `provider` and `providerOptions` fields.
- Validate that webhook handlers can process signed webhooks.
- Check that outbound call requests include the `shaken` parameter when required for US destinations.

## Failure Handling
- If an API request fails, check the HTTP status code and response body for error details.
- Ensure JWT tokens are correctly signed and not expired.
- Verify that the `from` number is linked to the Vonage Application.
- Do not repeat a failed action unchanged; diagnose the issue and apply a fix.

## Output Contract
- **Structure:** Provide a clear, actionable summary of the implemented Voice API flow.
- **Evidence:** Include code snippets, NCCO JSON arrays, and API request/response examples.
- **Actionable Next Steps:** Specify any required configuration changes in the Vonage Dashboard or application code.
