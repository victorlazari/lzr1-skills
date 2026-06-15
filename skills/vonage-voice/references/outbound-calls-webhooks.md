# Outbound Calls and Webhooks

This document details the mechanics of initiating outbound calls using the Vonage Voice API and handling the webhooks that drive the call flow.

## 1. Authentication

The Voice API uses JSON Web Tokens (JWT) for authentication. The JWT must be signed using the private key generated when creating the Vonage Application.

To generate a JWT using the Vonage CLI or a server SDK, you need:
- `application_id`: The UUID of your Vonage Application.
- `private_key`: The contents of the `private.key` file.

When making REST API requests, include the JWT in the Authorization header:
`Authorization: Bearer <JWT>`

## 2. Initiating an Outbound Call

To start a voice call from your backend application, make an HTTP `POST` request to `/v1/calls`.

**Endpoint:** `POST https://api.nexmo.com/v1/calls`

### Required Payload Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `to` | Array | An array containing a single endpoint object representing the destination. For a phone call, use `{"type": "phone", "number": "DESTINATION_NUMBER"}`. |
| `from` | Object | An endpoint object representing the caller ID. This MUST be one of your linked Vonage virtual numbers. Example: `{"type": "phone", "number": "YOUR_VONAGE_NUMBER"}`. |
| `answer_url` | Array | An array containing a single URL pointing to your server. Vonage will make a request to this URL when the call is answered to retrieve the NCCO instructions. |

### Example Request

```bash
curl -X POST https://api.nexmo.com/v1/calls \
  -H "Authorization: Bearer $JWT" \
  -H "Content-Type: application/json" \
  -d '{
    "to": [{"type": "phone", "number": "447700900001"}],
    "from": {"type": "phone", "number": "447700900000"},
    "answer_url": ["https://api.example.com/answer"]
  }'
```

## 3. Webhooks Overview

Vonage uses webhooks to interact with your application. There are two primary webhook endpoints you must configure:

1. **Answer Webhook:** Sent when a call is answered. Your server must respond with an NCCO array.
2. **Event Webhook:** Sent when there is a status change in the call (e.g., ringing, answered, completed, or user input received).

### Answer Webhook

When the outbound call connects, Vonage sends an HTTP request to the `answer_url` provided in the `POST /v1/calls` request. 

- **Method:** `GET` (by default, can be overridden to `POST`).
- **Response Required:** Your server MUST return a valid JSON array representing the NCCO.

**Key Data Fields Received:**
- `to`: The number that answered.
- `from`: The number that called.
- `uuid`: A unique identifier for this call leg.
- `conversation_uuid`: A unique identifier for the entire conversation.

### Event Webhook

Event webhooks notify your application of call progression and user interactions.

- **URL Configuration:** Set at the Application level in the Vonage Dashboard, or overridden per-call or per-action (e.g., inside an `input` action).
- **Method:** `POST` with a JSON body (by default).
- **Response Required:** HTTP `200 OK`. If your system responds with a 429, 502, or 504, Vonage will attempt a retry.

**Common Call States:**
- `started`
- `ringing`
- `answered`
- `completed`
- `machine` / `human` (if Answering Machine Detection is enabled)

## 4. In-Call Control (REST API)

Once a call is active, you can modify it dynamically using the REST API `PUT /v1/calls/{uuid}` endpoint.

### Transferring a Call via REST
You can transfer an active call to a new NCCO URL. This is useful for interrupting a long audio stream or moving a user out of a queue.

```bash
curl -X PUT https://api.nexmo.com/v1/calls/$VOICE_CALL_ID \
  -H "Authorization: Bearer $JWT" \
  -H "Content-Type: application/json" \
  -d '{
    "action": "transfer",
    "destination": {
      "type": "ncco", 
      "url": ["https://api.example.com/new-ncco"]
    }
  }'
```

### Other In-Call Actions
- **Hangup:** Send `{"action": "hangup"}` to terminate the call.
- **Mute:** Send `{"action": "mute"}` to mute the call leg.
- **Earmuff:** Send `{"action": "earmuff"}` to prevent the caller from hearing audio.
