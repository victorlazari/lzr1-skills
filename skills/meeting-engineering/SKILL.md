---
name: meeting-engineering
description: "Extreme expertise for building live Google Meet virtual assistants that participate in real time with voice. Use for: Playwright/Chromium Meet automation, Xvfb virtual display, PulseAudio virtual audio routing (null sinks, monitor sources, parec/paplay), low-latency STT/LLM/TTS pipelines with VAD/barge-in, real-time knowledge-base grounding (RAG), calendar-driven scheduling, RabbitMQ task dispatch, and Docker Compose meeting-bot deployment."
license: Complete terms in LICENSE.txt
---

# Meeting Engineering

Build high-performance virtual assistants that join Google Meet as live participants: hearing the room, retrieving knowledge-base context in real time, and speaking grounded responses with sub-second latency.

The architecture is a cascaded real-time pipeline inside a container:

```
Calendar watcher ─→ RabbitMQ (tasks.meet) ─→ Worker container
                                              ├─ tini (PID 1)
                                              ├─ Xvfb :99 (virtual display)
                                              ├─ PulseAudio (unix:/tmp/pulse-socket)
                                              │   ├─ sindarian-out (TTS sink) ─ monitor → Chrome "mic"
                                              │   └─ sindarian-meeting (Chrome output) → sindarian-meeting-source → STT
                                              └─ Playwright → Chromium (non-headless on Xvfb) → Google Meet
Meeting audio → parec → STT (scribe_v2_realtime → whisper fallbacks)
             → VAD/endpointing → relevance gate → RAG retrieval → LLM (gpt-5-mini, Groq fast path)
             → TTS (eleven_multilingual_v2 → tts-1 fallback) → paplay → sindarian-out → Meet
State: PostgreSQL (registry, sessions) · Valkey (dedup, hot cache) · Slack (join/leave alerts)
```

## Non-Negotiable Rules

1. **Real account, never a service account** — Google Meet blocks service accounts. Persist auth state (cookies + OAuth refresh token) to `workspace/config/meet-auth-state.json` and inject via Playwright `storage_state`.
2. **Non-headless Chromium on Xvfb** — full WebRTC media only works reliably with `headless=False` on a virtual display. Never pass `--use-fake-device-for-media-stream` when PulseAudio devices must back `getUserMedia`.
3. **Stream everything** — audio to STT, tokens from LLM, audio from TTS. Any stage that buffers a full payload destroys the latency budget (<1s mouth-to-ear).
4. **Stay silent by default** — respond only on direct address, detected questions matching the KB, or configured triggers. A chatty bot gets removed.
5. **Isolate per meeting** — one worker = one meeting (prefetch_count=1), segregated memory keyed by `meeting_id`, dedup via Valkey `SET NX EX MEET_DEDUP_TTL` before dispatch.

## Workflow

When building or debugging a Meet assistant, work through these layers in order:

1. **Infrastructure** — Container with tini, Xvfb, PulseAudio, and virtual devices. Start from `templates/Dockerfile.meet` and `templates/docker-compose.meet.yml`; the startup ordering lives in `scripts/meet-entrypoint.sh` and device creation in `scripts/setup_pulse_devices.sh`. Read [references/architecture_and_audio.md](references/architecture_and_audio.md) for the full routing model, pactl commands, and Chromium launch flags.
2. **Join automation** — Playwright (Python) drives auth injection, CDP/context permission grants, the green-room flow (camera off, name fill, "Join now"/"Ask to join"), admission waiting, popup dismissal, participant monitoring, and graceful leave. `scripts/meet_joiner.py` is a working template. Read [references/playwright_automation.md](references/playwright_automation.md) for selectors, anti-bot mitigation, and caption-scraping fallback.
3. **Real-time voice pipeline** — `parec` captures meeting audio from `sindarian-meeting-source`; chunks stream to STT; turn detection (Silero VAD + semantic endpointing) fires the LLM; streamed TTS plays via `paplay` to `sindarian-out` with instant barge-in cancellation. `scripts/audio_bridge.py` provides the capture/playback skeleton. Read [references/low_latency_pipelines.md](references/low_latency_pipelines.md) for the latency budget table, provider settings, and chunking strategy.
4. **Knowledge grounding** — Run an ambient comprehension loop that pre-fetches KB chunks as the conversation evolves, so response-time retrieval is a cache hit. Hybrid (vector + keyword) search over a chunked KB repo, layered prompt assembly, relevance gating, rolling summarization. Read [references/knowledge_grounding.md](references/knowledge_grounding.md).
5. **Orchestration & ops** — Calendar watcher polls Google Calendar (OAuth2) and publishes to `sindarian.tasks`/`tasks.meet` (with DLX); PostgreSQL is the system of record; Valkey handles dedup; Slack announces joins/leaves and failures; provider fallback chains keep the conversation alive. Read [references/orchestration_and_ops.md](references/orchestration_and_ops.md).

## Default Provider Stack

| Stage | Primary | Fallbacks | Notes |
| --- | --- | --- | --- |
| STT | ElevenLabs `scribe_v2_realtime` (WebSocket, ~150ms) | OpenAI `whisper-1`, Groq `whisper-large-v3-turbo` | Fallbacks are non-streaming: buffer ~3s windows |
| LLM | Gateway → `gpt-5-mini` via Groq fast path (~1s) | Direct OpenAI | Always stream tokens; keep prompts <4k tokens |
| TTS | ElevenLabs `eleven_multilingual_v2`, language-aware voice IDs | OpenAI `tts-1` | Use `eleven_flash_v2_5` when latency beats quality; LLM normalizes numbers/dates |

## Debugging Quick Reference

| Symptom | First checks |
| --- | --- |
| Bot joins but hears nothing | `pactl list short sources` — does `sindarian-meeting-source` exist? Is Chrome's output routed to `sindarian-meeting` (default sink)? Run `scripts/audio_bridge.py` smoke test. |
| Bot speaks but Meet participants hear nothing | Is Chrome's input the `sindarian-out.monitor` (default source)? Is the bot's Meet mic muted in the UI? Did `--use-fake-device-for-media-stream` sneak into the flags? |
| Join button never found | Google rotated the DOM. Re-derive role/aria-label locators; check for blocking dialogs; verify auth state hasn't expired (login redirect). |
| "You can't join" / denied | Anti-bot heuristics or waiting-room denial. Use trusted-domain account, human-like delays, verify host admitted the bot. |
| Chromium crashes in container | `shm_size: 2gb`, `--disable-dev-shm-usage`, memory limit ≥3GB. |
| Latency feels slow | Measure per stage. Usual culprits: silence threshold too high (>800ms), non-streamed LLM/TTS, TTS text normalization enabled, oversized prompt. |
| Double-joins after restart | Valkey dedup key must use TTL and never be deleted on shutdown. |
