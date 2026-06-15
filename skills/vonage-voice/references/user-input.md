# Handling User Input (DTMF & ASR)

The `input` NCCO action allows you to collect digits pressed on a keypad (DTMF) or capture spoken words (Automatic Speech Recognition - ASR). 

When the input is captured, Vonage sends an HTTP request to the specified `eventUrl`. Your server MUST process this request and return a **new NCCO array** to replace the current one and continue the call flow.

## 1. The `input` Action Structure

```json
{
  "action": "input",
  "type": ["dtmf", "speech"],
  "eventUrl": ["https://api.example.com/handle-input"],
  "dtmf": {
    "maxDigits": 1,
    "timeOut": 5,
    "submitOnHash": true
  },
  "speech": {
    "language": "en-US",
    "endOnSilence": 2.0,
    "context": ["sales", "support", "billing"]
  }
}
```

### General Parameters
- `type` (Required): Array specifying accepted inputs. Options: `["dtmf"]`, `["speech"]`, or `["dtmf", "speech"]`.
- `eventUrl`: Array containing a single URL. Vonage sends the input payload here. If omitted, input is ignored.

### DTMF Settings
Configured inside the `dtmf` object:
- `maxDigits`: Maximum number of digits the user can press (default: 4, max: 20).
- `timeOut`: Seconds of inactivity before submitting the input (default: 3).
- `submitOnHash`: If `true`, the input is submitted immediately when the user presses `#`.

### Speech Settings (ASR)
Configured inside the `speech` object:
- `language`: BCP-47 language code (e.g., `en-US`).
- `context`: Array of expected words or phrases to improve recognition accuracy (e.g., `["yes", "no", "operator"]`).
- `endOnSilence`: Seconds of silence to wait after the user stops speaking before submitting (default: 2.0).

---

## 2. Using `bargeIn` with Prompts

Typically, an `input` action is preceded by a `talk` or `stream` action that prompts the user. To allow the user to interrupt the prompt by pressing a key or speaking, set `"bargeIn": true` on the prompt action.

**CRITICAL RULE:** If `bargeIn` is `true`, the very next action in the NCCO array **MUST** be the `input` action.

```json
[
  {
    "action": "talk",
    "text": "Please enter your 4-digit PIN.",
    "bargeIn": true
  },
  {
    "action": "input",
    "type": ["dtmf"],
    "dtmf": {
      "maxDigits": 4
    },
    "eventUrl": ["https://api.example.com/verify-pin"]
  }
]
```

---

## 3. Handling the Webhook Payload

When the input is captured (or times out), Vonage sends a POST request to your `eventUrl`.

### Example DTMF Payload Received by Your Server:
```json
{
  "dtmf": {
    "digits": "1234",
    "timed_out": false
  },
  "speech": {
    "results": []
  },
  "from": "14155550100",
  "to": "14155550200",
  "uuid": "aaaaaaaa-bbbb-cccc-dddd-0123456789ab"
}
```

### Example ASR Payload Received by Your Server:
```json
{
  "speech": {
    "results": [
      {
        "text": "sales",
        "confidence": "0.9405097"
      }
    ],
    "timeout_reason": "end_on_silence_timeout"
  },
  "dtmf": {
    "digits": null,
    "timed_out": false
  },
  "from": "14155550100",
  "to": "14155550200",
  "uuid": "aaaaaaaa-bbbb-cccc-dddd-0123456789ab"
}
```

---

## 4. Server-Side Execution Logic

Your application should parse the incoming payload, determine the appropriate response, and reply to the HTTP request with a new NCCO.

### Node.js / Express Example

```javascript
app.post('/handle-input', (req, res) => {
  const dtmfInput = req.body.dtmf?.digits;
  const speechInput = req.body.speech?.results?.[0]?.text?.toLowerCase();

  let ncco = [];

  if (dtmfInput === "1" || speechInput === "sales") {
    // Execute server-side logic: Log metric, look up available agent, etc.
    console.log("Routing to sales...");
    
    ncco = [
      { "action": "talk", "text": "Connecting to sales." },
      { 
        "action": "connect", 
        "from": "YOUR_VONAGE_NUMBER",
        "endpoint": [{ "type": "phone", "number": "SALES_TEAM_NUMBER" }]
      }
    ];
  } else {
    // Fallback logic
    ncco = [
      { "action": "talk", "text": "Input not recognized. Goodbye." }
    ];
  }

  // Respond to the webhook with the new NCCO
  res.json(ncco);
});
```
