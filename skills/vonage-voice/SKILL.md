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
- **User Input:** Prompting users and capturing DTMF keypad presses or Automatic Speech Recognition (ASR).
- **Webhooks:** Handling Answer Webhooks to serve NCCOs and Event Webhooks to monitor call status and user inputs.
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

## Reference Materials
For detailed implementation instructions, refer to the specialized guides in the `references` directory:

- [Outbound Calls and Webhooks](references/outbound-calls-webhooks.md): Master the REST API for initiating calls, JWT authentication, and webhook handling.
- [NCCO Actions Reference](references/ncco-actions.md): Complete guide to all NCCO actions, including `talk`, `connect`, `record`, and `transfer`.
- [Handling User Input (DTMF & ASR)](references/user-input.md): Detailed patterns for building Interactive Voice Response (IVR) systems.

## Core Implementation Pattern: Outbound IVR Flow

To build an outbound call that provides options and executes actions based on user input, follow this architecture:

1. **Initiate Call:** The backend server uses the Vonage REST API (`POST /v1/calls`) to dial the destination number. The request includes an `answer_url` pointing to your server.
2. **Serve Initial NCCO:** When the call connects, Vonage sends a GET/POST request to the `answer_url`. Your server responds with an NCCO containing a `talk` action (the prompt) and an `input` action (to capture the response).
3. **Capture Input:** The user hears the prompt and presses a keypad digit (DTMF) or speaks (ASR).
4. **Handle Event Webhook:** Vonage sends the captured input to the `eventUrl` defined in the `input` action.
5. **Execute Application Logic:** Your server receives the input, executes internal logic (e.g., updating a database, routing a ticket), and returns a *new* NCCO to replace the current one.
6. **Continue or End:** The new NCCO might `connect` the call to an agent, `talk` a confirmation message, or `transfer` the call.

### Example: Outbound Call to Webhook
```bash
# Initiating the call
curl -X POST https://api.nexmo.com/v1/calls \
  -H "Authorization: Bearer $JWT" \
  -H "Content-Type: application/json" \
  -d '{
    "to": [{"type": "phone", "number": "14155550100"}],
    "from": {"type": "phone", "number": "14155550200"},
    "answer_url": ["https://api.example.com/answer"]
  }'
```

### Example: Answer Webhook (Serving the IVR Menu)
When Vonage hits `https://api.example.com/answer`, return this NCCO:
```json
[
  {
    "action": "talk",
    "text": "Hello. Press 1 to speak with sales, or 2 for support.",
    "bargeIn": true
  },
  {
    "action": "input",
    "type": ["dtmf"],
    "dtmf": {
      "maxDigits": 1,
      "timeOut": 5
    },
    "eventUrl": ["https://api.example.com/ivr-input"]
  }
]
```

### Example: Handling the Input
When the user presses "1", Vonage sends a webhook to `https://api.example.com/ivr-input`.
Your server processes the JSON payload, checks `req.body.dtmf.digits === "1"`, executes internal logic, and returns a new NCCO to connect to sales:
```json
[
  {
    "action": "talk",
    "text": "Connecting you to sales."
  },
  {
    "action": "connect",
    "from": "14155550200",
    "endpoint": [
      {
        "type": "phone",
        "number": "14155550300"
      }
    ]
  }
]
```

---

## Adversarial Verification Panel

For each significant NCCO configuration issue and integration recommendation produced by the parallel sub-agents:

1. Spawn **3 independent Refuter Agents** per finding, each with:
   - The finding in full
   - Instruction: *"Assume this finding is wrong. Find the strongest argument against it."*
   - Default stance: `refuted=true` if evidence is insufficient or ambiguous
2. A finding is **confirmed** only if ≥2 refuters fail to refute it
3. A finding is **discarded** if ≥2 refuters succeed
4. When a confirmed finding had 1 successful refuter, include the dissenting argument in the output with a `CONTESTED` label

> This prevents plausible-but-wrong NCCO configuration issues and integration recommendations from reaching the final output. The 3-vote panel eliminates single-point hallucination without requiring unanimity.

## Cross-System Consistency Validator

After all parallel agents (Outbound Calls & Webhooks Agent, NCCO Actions Agent, User Input & IVR Agent) complete, but **before** synthesis:

Run one **Consistency Validator Agent** with all parallel outputs that:
- Flags any pair of recommendations that logically contradict each other
  *(example: the NCCO Actions Agent recommends setting `bargeIn: true` on all `talk` actions for a smoother IVR experience, while the User Input & IVR Agent recommends disabling `bargeIn` during compliance recording prompts to ensure the full legal disclosure is heard before input is accepted)*
- Notes where one agent's output is a prerequisite for another agent's recommendation
- Passes contradictions to the Synthesis Agent as `MUST_RESOLVE` items
- Passes missing prerequisites as `SEQUENCING_REQUIRED` items

## Synthesis Agent (Upgraded)

The synthesis step actively resolves rather than aggregates:

1. **`MUST_RESOLVE` contradictions**: Pick the better recommendation, annotate the reasoning, preserve the dissenting view as a footnote
2. **`SEQUENCING_REQUIRED` items**: Re-order the unified implementation plan so prerequisites appear before the steps that depend on them
3. **Confidence calibration**: Label each finding `HIGH` / `MEDIUM` / `LOW` confidence based on refuter panel outcomes
4. **Gap analysis**: Note any analysis dimension not covered by any of the parallel agents — these are blind spots, not confirmed negatives
