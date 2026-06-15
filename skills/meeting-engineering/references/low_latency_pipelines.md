# Low-Latency Pipelines and Turn Detection

Achieving a natural, conversational feel in a voice agent requires minimizing "core latency"—the mouth-to-ear turn gap. This reference covers the best practices for configuring the Speech-to-Text (STT), Turn Detection, Large Language Model (LLM), and Text-to-Speech (TTS) pipeline.

## The Latency Budget

For a conversation to feel natural, the target end-to-end latency (from the user stopping speech to the bot starting audio playback) should be **under 1000ms (1 second)**, with a stretch goal of sub-500ms for highly responsive agents.

Every component in the cascaded architecture consumes part of this budget:
*   **Turn Detection / Endpointing**: ~300ms - 800ms (Waiting to ensure the user is actually done speaking).
*   **STT Finalization**: ~50ms - 150ms.
*   **LLM Time-to-First-Token (TTFT)**: ~200ms - 500ms.
*   **TTS Time-to-First-Byte (TTFB)**: ~100ms - 300ms.
*   **Network & Audio Buffer Overhead**: ~50ms - 100ms.

## Turn Detection Strategies

Turn detection is the process of identifying the boundary between a user's spoken utterance and the silence that follows. It is the trigger for the entire response pipeline.

1.  **Voice Activity Detection (VAD) Only**:
    *   *How it works*: Classifies incoming audio frames as speech or silence in real-time. Triggers when silence exceeds a threshold (e.g., 500ms).
    *   *Tools*: **Silero VAD** (open-source, highly accurate, <1ms processing time per 30ms chunk), WebRTC VAD.
    *   *Pros*: Fast processing, runs locally.
    *   *Cons*: Adds fixed latency proportional to the silence threshold. Prone to false positives on mid-sentence pauses.
2.  **STT Endpointing**:
    *   *How it works*: Relies on the STT provider's model to emit an explicit end-of-utterance event based on acoustic and linguistic features.
    *   *Pros*: Often more accurate than pure silence detection.
    *   *Cons*: Dependent on the provider's latency.
3.  **Model-Based / Semantic Endpointing**:
    *   *How it works*: A lightweight classification model reads the partial transcript stream and predicts turn completion based on semantic meaning and punctuation, often triggering before the trailing silence finishes.
    *   *Pros*: Lowest possible latency.
    *   *Cons*: Complex to tune; risk of cutting users off if they hesitate mid-thought.

**Best Practice**: Use a hybrid approach. Implement Silero VAD to filter out background noise and handle hard silence timeouts, combined with semantic endpointing from the STT stream to trigger responses quickly on complete sentences.

## Barge-in and Interruptions

Barge-in allows the user to interrupt the agent while it is speaking.
*   **Implementation**: The turn detection layer (VAD/STT) must remain active while the TTS is playing.
*   **Action**: When user speech is detected during agent playback, immediately cancel the current TTS stream, halt LLM generation, and hand control back to the STT pipeline.
*   **Challenge**: Echo cancellation. In a Google Meet environment via PulseAudio, ensure the bot's own TTS output (`sindarian-out`) does not leak into the STT capture (`sindarian-meeting-source`). Google Meet's built-in echo cancellation helps, but careful routing is essential.

## Low-Latency STT: ElevenLabs Scribe v2 Realtime

For the STT layer, ElevenLabs Scribe v2 Realtime is recommended for its ultra-low latency (~150ms) and high multilingual accuracy.

*   **Connection**: Use WebSocket for client-side or server-side streaming.
*   **Streaming**: Pipe the raw audio captured from `sindarian-meeting-source` directly into the WebSocket.
*   **Events**: Listen for `partial_transcript` for semantic endpointing hints, and `committed_transcript` for the final finalized text to send to the LLM.

## Fast LLM Generation

The LLM is the brain of the agent. To minimize TTFT:
*   **Model Choice**: Use fast, smaller models like `gpt-4o-mini` or `gpt-5-mini`.
*   **Gateway/Provider**: Route requests through low-latency inference providers like Groq to achieve extremely fast token generation rates (~1s total response generation time).
*   **Streaming**: **Crucially, stream the LLM output.** Do not wait for the entire response to generate.

## Low-Latency TTS: ElevenLabs Flash v2.5

For the TTS layer, ElevenLabs Flash v2.5 provides ultra-low latency (~75ms TTFB) and supports 32 languages.

*   **Streaming Input**: Pipe the streamed text chunks from the LLM directly into the TTS API.
*   **Streaming Output**: The TTS API will return an audio stream. Play this stream immediately to the `sindarian-out` PulseAudio sink.
*   **Chunking Strategy**: Send text to the TTS engine at sentence or clause boundaries. Sending text token-by-token reduces latency but can degrade speech prosody (intonation and rhythm). Buffering until a punctuation mark (.,!?) offers the best balance of speed and natural delivery.

### TTS API Optimization Flags (ElevenLabs)
When calling the ElevenLabs streaming endpoint (`/v1/text-to-speech/{voice_id}/stream`):
*   Set `output_format` to a low-latency PCM format if supported by your playback pipeline, or standard `mp3_44100_128`.
*   Avoid `apply_language_text_normalization=true` unless absolutely necessary, as it heavily increases latency. Ensure the LLM normalizes numbers and dates in its text output instead.
