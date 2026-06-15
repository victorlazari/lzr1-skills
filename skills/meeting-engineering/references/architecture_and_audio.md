# Architecture and Virtual Audio Routing

This reference provides a deep dive into the infrastructure and audio routing required to build a high-performance, low-latency Google Meet virtual assistant. The core challenge is bridging a headless Chromium browser (running via Playwright) with real-time audio processing pipelines without physical audio hardware.

## System Architecture Overview

The system is designed as a cascaded voice agent architecture optimized for low latency.

1.  **Capture & Join Layer**: A headless Chromium instance controlled by Playwright joins the Google Meet.
2.  **Virtual Audio Layer**: PulseAudio creates virtual sinks and sources to route audio into and out of the headless browser.
3.  **STT Layer**: Audio from the meeting is captured and streamed via WebSocket to a low-latency Speech-to-Text provider (e.g., ElevenLabs Scribe v2 Realtime).
4.  **Turn Detection Layer**: Voice Activity Detection (VAD) and endpointing determine when the user has finished speaking.
5.  **LLM Layer**: A fast LLM (e.g., GPT-4o-mini or GPT-5-mini via Groq) generates the response.
6.  **TTS Layer**: Text is streamed to a low-latency Text-to-Speech provider (e.g., ElevenLabs Flash v2.5 or Multilingual v2) and played back into the meeting.

## Infrastructure and Containerization

To run headless Chromium with full media capabilities, a virtual display and a virtual audio server are required. This is typically orchestrated using Docker Compose.

*   **Xvfb (X Virtual Framebuffer)**: Provides a virtual display (`:99`) so Chromium can render the DOM and execute without a physical monitor.
*   **PulseAudio**: Runs as a daemon to handle audio routing via a unix socket (`/tmp/pulse-socket`).
*   **tini**: Used as PID 1 in the Docker container to handle signal forwarding and zombie process reaping.
*   **Entrypoint Script (`meet-entrypoint.sh`)**: Orchestrates the startup of Xvfb, PulseAudio, and the worker processes.

## PulseAudio Virtual Routing Setup

PulseAudio must be configured to create specific virtual devices using the `module-null-sink` and `module-remap-source` modules. This allows us to separate the audio *coming from* the meeting (to be transcribed) from the audio *going to* the meeting (the bot speaking).

### Required Virtual Devices

1.  **`sindarian-out` (Null Sink)**: Where the TTS engine plays audio.
2.  **`sindarian-out.monitor` (Monitor Source)**: The monitor of the TTS sink. Chromium captures this as its microphone input.
3.  **`sindarian-meeting` (Null Sink)**: Where Chromium routes incoming audio from other participants in the meeting.
4.  **`sindarian-meeting-source` (Virtual Source)**: A remapped source from `sindarian-meeting.monitor`. The STT engine captures from this source.

### Setup Commands (via `pactl`)

To initialize these virtual devices, execute the following commands within the container environment (typically in the entrypoint script or via a setup script before launching the bot):

```bash
# 1. Create the sink for TTS playback (Bot speaking)
pactl load-module module-null-sink sink_name=sindarian-out sink_properties=device.description="TTS_Playback"

# 2. Create the sink for Meeting audio (Bot listening)
pactl load-module module-null-sink sink_name=sindarian-meeting sink_properties=device.description="Meeting_Audio"

# 3. Remap the meeting monitor to a dedicated source for STT capture
pactl load-module module-remap-source master=sindarian-meeting.monitor source_name=sindarian-meeting-source source_properties=device.description="STT_Capture"
```

### Audio I/O Tools

Once the PulseAudio routing is established, standard Linux audio tools can interface with the streams:

*   **Playing Audio (TTS -> Meeting)**: Use `paplay` (or similar audio playback libraries in Python/Node) to play the generated TTS audio file to the `sindarian-out` sink.
    ```bash
    paplay --device=sindarian-out response.wav
    ```
*   **Capturing Audio (Meeting -> STT)**: Use `parec` (or `pacat --record`) to capture the raw PCM audio stream from the `sindarian-meeting-source` and pipe it to the STT WebSocket client.
    ```bash
    parec --device=sindarian-meeting-source --format=s16le --rate=16000 --channels=1 | python stt_streamer.py
    ```

## Chromium Launch Flags

To force Chromium to use the PulseAudio virtual devices and bypass standard media restrictions, specific flags must be passed when launching the browser via Playwright:

```javascript
const browser = await chromium.launch({
  headless: false, // Often required to be false when using Xvfb for full media support
  args: [
    '--no-sandbox',
    '--disable-setuid-sandbox',
    '--use-fake-ui-for-media-stream', // Auto-accepts camera/mic permission prompts
    '--autoplay-policy=no-user-gesture-required', // Allows audio to play immediately without user interaction
    // The following flags can sometimes interfere with PulseAudio routing if not careful.
    // Only use if specifically providing fake file streams, otherwise rely on PulseAudio default sinks.
    // '--use-fake-device-for-media-stream', 
  ],
  env: {
    ...process.env,
    DISPLAY: ':99', // Point to Xvfb
    PULSE_SERVER: 'unix:/tmp/pulse-socket' // Point to PulseAudio
  }
});
```

*Note on Headless Mode*: While `headless: true` is desirable, some media APIs and complex DOM interactions (like Google Meet's join flow) behave more reliably with `headless: false` running inside an Xvfb virtual display.

## High-Scale Considerations

For high-scale bot architectures:

*   **Segregated Memory**: Ensure each bot instance operates in complete isolation. Use isolated BrowserContexts in Playwright and unique PulseAudio daemon instances per container.
*   **Task Dispatch**: Use a message broker like RabbitMQ (e.g., `sindarian.tasks` exchange) to distribute join requests across a fleet of worker containers.
*   **State Management**: Use PostgreSQL for persistent task registry and session state, and Valkey/Redis for fast deduplication of events and short-lived state caching.
