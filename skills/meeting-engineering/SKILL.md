---
name: meeting-engineering
description: "Build and deploy live Google Meet virtual assistants using Playwright, PulseAudio, and low-latency STT/LLM/TTS pipelines."
license: Complete terms in LICENSE.txt
---

# Meeting Engineering

Build high-performance virtual assistants that join Google Meet as live participants: hearing the room, retrieving knowledge-base context in real time, and speaking grounded responses with sub-second latency.

## Scope and Triggers
Use this skill when building, debugging, or deploying a Google Meet virtual assistant that requires real-time voice participation, Playwright automation, PulseAudio routing, or low-latency STT/LLM/TTS pipelines.
Do not use for general Playwright automation outside of Google Meet (route to `playwright-automation`) or general calendar/task scheduling (route to `automation-and-scheduling`).

## Preconditions
- Target environment must support Xvfb and PulseAudio.
- Valid Google account credentials (not a service account) must be available.
- Docker and Docker Compose must be installed for infrastructure provisioning.

## Source Freshness
Google Meet UI selectors and external API endpoints (ElevenLabs, Groq, OpenAI) are volatile. Always verify current documentation and test selectors locally before production deployment. See referenced files for canonical URLs and verification dates.

## Workflow
1. **Infrastructure**: Provision the containerized environment using `templates/docker-compose.meet.yml` and `templates/Dockerfile.meet`.
2. **Audio Setup**: Execute `scripts/setup_pulse_devices.sh` to create virtual PulseAudio devices. Verify with `pactl list short sources`.
3. **Join Automation**: Run a dry-run of the meeting join process using `scripts/meet_joiner.py` to verify Playwright selectors against the current Google Meet UI.
4. **Voice Pipeline**: Verify the STT/TTS pipeline using `scripts/audio_bridge.py` with test audio and text.
5. **Deployment**: Deploy the calendar watcher and worker containers. Monitor system logs for errors and latency bottlenecks.

## Safety and Validation
- **Read-only discovery**: Always run a dry-run of the meeting join process before deploying to production meetings.
- **Confirmation**: Require user confirmation before deploying the bot to production meetings or executing destructive actions.
- **Validation**: Verify PulseAudio routing with test commands (`parec`, `paplay`) before full execution. Monitor memory usage to prevent Chromium crashes.
- **Syntax Checks**: Run `bash -n` on shell scripts and `python3 -m py_compile` on Python scripts before execution.

## Failure Handling
- **STT/TTS Failures**: Ensure graceful fallback mechanisms are in place (e.g., ElevenLabs -> OpenAI TTS).
- **UI Changes**: If Playwright selectors fail, re-derive them using the current Google Meet DOM and update `scripts/meet_joiner.py`.
- **Audio Issues**: If audio routing fails, restart PulseAudio and re-run `scripts/setup_pulse_devices.sh`.

## Output Contract
The skill must produce a functional, containerized Google Meet bot capable of joining meetings, capturing audio, and responding with low latency. The output must include logs of the dry-run execution and validation checks.

## Resources
- [Architecture and Audio](references/architecture_and_audio.md): PulseAudio configuration and Chromium launch flags.
- [Playwright Automation](references/playwright_automation.md): Google Meet UI selectors and anti-bot mitigation.
- [Low Latency Pipelines](references/low_latency_pipelines.md): STT/TTS provider details and latency budgets.
- [Knowledge Grounding](references/knowledge_grounding.md): RAG architecture and prompt assembly.
- [Orchestration and Ops](references/orchestration_and_ops.md): RabbitMQ, PostgreSQL, and Valkey integration.
- [Audio Bridge Script](scripts/audio_bridge.py): STT/TTS pipeline implementation.
- [Meet Joiner Script](scripts/meet_joiner.py): Playwright automation script.
- [Setup Pulse Devices Script](scripts/setup_pulse_devices.sh): PulseAudio configuration script.
- [Meet Entrypoint Script](scripts/meet-entrypoint.sh): Container entrypoint script.
- [Dockerfile](templates/Dockerfile.meet): Container image definition.
- [Docker Compose](templates/docker-compose.meet.yml): Infrastructure provisioning template.
