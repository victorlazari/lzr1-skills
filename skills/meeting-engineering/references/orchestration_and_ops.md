# Orchestration, Scheduling, and Operations

This reference covers the operational backbone of the meeting assistant fleet: calendar-driven scheduling, task dispatch, persistence, deduplication, notifications, and containerized deployment.

## Calendar-Driven Scheduling (Google Calendar API)

The bot should join meetings automatically based on the calendar, not manual URL submission.

*   **Watcher Process (`meet_calendar_watcher.py`)**: A long-running worker polls the Google Calendar API (`events.list` with `timeMin`/`timeMax` windows and `singleEvents=true`) every 30–60 seconds for upcoming events containing a `hangoutLink` or `conferenceData.entryPoints` of type `video`.
*   **OAuth2**: Use an OAuth2 refresh token persisted on disk (e.g., `workspace/config/meet-auth-state.json`). Refresh access tokens proactively before expiry; on `invalid_grant`, alert immediately via Slack — the bot is dead until re-authorized.
*   **Join Timing**: Dispatch the join task ~1–2 minutes before the event start so the bot is in the waiting room when the host arrives. Respect event updates (cancellations, time changes) by re-checking the event `updated` timestamp before dispatch.

## Task Dispatch (RabbitMQ + Pika)

Decouple the watcher from the bot workers with a message broker.

*   **Topology**: Publish to a topic exchange (e.g., `sindarian.tasks`) with routing key `tasks.meet`; workers consume from a durable queue (`tasks.meet`) bound to it.
*   **Dead-Letter Exchange (DLX)**: Configure the queue with `x-dead-letter-exchange` so failed/rejected joins land in a DLQ for inspection and retry, instead of being lost or hot-looping.
*   **Pika Patterns**: Use `basic_qos(prefetch_count=1)` so one worker handles one meeting at a time (a meeting bot is a heavyweight, stateful task). Ack only after the bot has successfully joined or definitively failed; use `basic_nack(requeue=False)` to dead-letter poisoned messages.
*   **Message Schema**: Include `event_id`, `meet_url`, `start_time`, `title`, `organizer`, and a `dispatch_id` for tracing across services.

## Persistence and Deduplication

*   **PostgreSQL**: The system of record. Store the task registry (event → dispatch status), session state (join time, leave time, exit reason), transcripts/segments, summaries, and action items. Use `meeting_id`/`event_id` as the partition key for segregated per-meeting memory.
*   **Valkey (Redis)**: Fast deduplication and ephemeral state. Before dispatching a join task, perform `SET dedup:{event_id} 1 NX EX {MEET_DEDUP_TTL}`; if the key already exists, the event was already dispatched — skip it. This prevents double-joins when the watcher restarts or polls overlap. Also useful for the KB hot cache and live presence flags (`meeting:{id}:active`).

## Notifications (Slack)

Operational visibility keeps humans in the loop.

*   Announce joins and leaves to a configured channel (`MEET_SLACK_CHANNEL`): "Joined *Weekly Sync* (5 participants)" / "Left *Weekly Sync* — transcript saved, 12 action items".
*   Alert on failures: denied entry, removed by host, auth expiry, STT/TTS provider errors after fallback exhaustion.
*   Optionally post the meeting summary thread after the meeting ends.

## Provider Fallback Chains

Never depend on a single external provider in a live conversation. Implement ordered fallbacks with fast failure detection (tight connect/read timeouts, ~2s):

| Stage | Primary | Fallbacks |
| --- | --- | --- |
| STT | ElevenLabs `scribe_v2_realtime` | OpenAI `whisper-1`, Groq `whisper-large-v3-turbo` |
| TTS | ElevenLabs `eleven_multilingual_v2` (language-aware voice IDs) | OpenAI `tts-1` |
| LLM | Gateway → `gpt-5-mini` (Groq fast path) | Direct OpenAI API |

For TTS, keep a mapping of language code → voice ID so the bot replies in the language of the conversation. Detect language from the STT output metadata.

## Container Topology (Docker Compose)

Run the meeting stack under a dedicated compose file and profile (e.g., `docker-compose.meet.yml`, profile `meet`).

*   **Process Supervision**: Use `tini` as PID 1 (`init: true` or explicit entrypoint) so signals propagate and zombie Chromium processes are reaped.
*   **Entrypoint (`meet-entrypoint.sh`)** ordering matters: start Xvfb, wait for the display socket; start PulseAudio with the unix socket (`/tmp/pulse-socket`), wait until `pactl info` succeeds; load the null-sink/remap modules; then exec the worker. See `scripts/meet-entrypoint.sh` in this skill for a working template.
*   **Resources**: A Chromium + Meet tab consumes ~1–2 GB RAM and 1–2 vCPUs. Set explicit memory limits and `shm_size: 2gb` (Chromium crashes with the default 64MB `/dev/shm`).
*   **Health**: Expose a health endpoint per worker reporting browser liveness, PulseAudio status, and pipeline latency percentiles. Restart policy `unless-stopped` with the DLX absorbing in-flight task loss.

## Graceful Shutdown and Cleanup

On SIGTERM: leave the meeting via the UI (click leave button) if possible, flush pending transcript segments to PostgreSQL, publish a leave notification, close the Playwright context, terminate Chromium, and let `tini` reap remaining children. Always release the Valkey dedup key only after the TTL expires (do not delete it on exit, or a restart will re-join the same meeting).
