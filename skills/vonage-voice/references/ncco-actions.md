# NCCO Actions Reference

A Nexmo Call Control Object (NCCO) is a JSON array containing instructions that control the flow of a Voice API call. Vonage executes the actions in the array sequentially.

## Execution Flow

- **Synchronous Actions:** The current action must complete before the next action in the array is executed. Examples: `talk` (unless bargeIn is true), `connect`, `input`, `wait`.
- **Asynchronous Actions:** The action starts and immediately allows the next action in the array to execute. Examples: `record`.

---

## 1. `talk`
Sends synthesized speech (Text-to-Speech) to the caller.

```json
{
  "action": "talk",
  "text": "Hello, please hold while we connect your call.",
  "language": "en-US",
  "bargeIn": false
}
```

**Key Parameters:**
- `text` (Required): The message to be synthesized (max 1,500 characters). Supports SSML if enclosed in a `<speak>` tag.
- `language`: The BCP-47 language code (e.g., `en-US`, `en-GB`, `es-ES`). Default is `en-US`.
- `bargeIn`: If `true`, the speech stops if the user interacts via DTMF or ASR. **Important:** If `bargeIn: true`, the very next action in the NCCO MUST be an `input` action.
- `loop`: Number of times to repeat the text. Set to `0` to loop infinitely.

---

## 2. `stream`
Plays an audio file to the caller.

```json
{
  "action": "stream",
  "streamUrl": ["https://example.com/hold-music.mp3"],
  "loop": 0
}
```

**Key Parameters:**
- `streamUrl` (Required): An array containing a single URL to an mp3 or wav (16-bit) audio file.
- `bargeIn`: Similar to `talk`, if `true`, the stream stops on user input, and the next action MUST be `input`.
- `loop`: Number of times to repeat. `0` means infinite loop.

---

## 3. `connect`
Connects the current call to another endpoint (e.g., a PSTN phone number, SIP endpoint, or WebSocket).

```json
{
  "action": "connect",
  "from": "14155550200",
  "timeout": 45,
  "endpoint": [
    {
      "type": "phone",
      "number": "14155550300"
    }
  ]
}
```

**Key Parameters:**
- `endpoint` (Required): An array containing a single endpoint object.
  - For PSTN: `{"type": "phone", "number": "E164_NUMBER"}`
  - For SIP: `{"type": "sip", "uri": "sip:user@domain.com"}`
  - For WebSocket: `{"type": "websocket", "uri": "wss://example.com/socket", "content-type": "audio/l16;rate=16000"}`
- `from`: The Caller ID to display to the destination. MUST be a linked Vonage virtual number when calling PSTN.
- `timeout`: Seconds to wait for the destination to answer before failing (default: 60).
- `machineDetection`: Set to `continue` or `hangup` to handle answering machines.

---

## 4. `record`
Records the call or part of the call. This action is asynchronous.

```json
{
  "action": "record",
  "eventUrl": ["https://example.com/recording-ready"],
  "format": "mp3",
  "endOnSilence": 3
}
```

**Key Parameters:**
- `eventUrl`: Webhook URL called when the recording is finished and ready for download.
- `format`: `mp3` (default), `wav`, or `ogg`.
- `split`: Set to `conversation` to record sent and received audio in separate stereo channels.
- `endOnSilence`: Stop recording after N seconds of silence.
- `timeOut`: Maximum length of the recording in seconds.

---

## 5. `wait`
Pauses execution of the NCCO for a specified number of seconds.

```json
{
  "action": "wait",
  "timeout": 5
}
```

**Key Parameters:**
- `timeout`: Duration to wait in seconds (0.1 to 7200). Default is 10.

---

## 6. `notify`
Sends a custom JSON payload to your server without interrupting the call flow.

```json
{
  "action": "notify",
  "payload": {"status": "user_reached_step_3"},
  "eventUrl": ["https://example.com/tracking"]
}
```

**Key Parameters:**
- `payload` (Required): The JSON object to send.
- `eventUrl` (Required): The URL that will receive the POST request containing the payload.

---

## 7. `transfer`
Moves the current call leg into an existing conversation. This action is terminal for the current NCCO.

```json
{
  "action": "transfer",
  "conversationId": "CON-f972836a-550f-45fa-956c-12a2ab5b7d22"
}
```

**Key Parameters:**
- `conversationId` (Required): The ID of the target conversation.
