#!/usr/bin/env python3
"""audio_bridge.py — Reference implementation of the real-time audio bridge.

Capture side : parec on `sindarian-meeting-source` -> 16kHz s16le mono PCM chunks
               -> async queue -> STT WebSocket client (provider-pluggable).
Playback side: TTS audio bytes -> paplay to `sindarian-out` with barge-in cancel.

This is a template: wire `stt_stream()` to ElevenLabs scribe_v2_realtime (primary)
with OpenAI whisper-1 / Groq whisper-large-v3-turbo fallbacks, and `speak()` to
ElevenLabs eleven_multilingual_v2 (primary) with OpenAI tts-1 fallback.
"""
import asyncio
import contextlib
import os
import signal

CAPTURE_DEVICE = os.environ.get("MEET_CAPTURE_DEVICE", "sindarian-meeting-source")
PLAYBACK_DEVICE = os.environ.get("MEET_PLAYBACK_DEVICE", "sindarian-out")
SAMPLE_RATE = int(os.environ.get("MEET_STT_SAMPLE_RATE", "16000"))
CHUNK_MS = int(os.environ.get("MEET_STT_CHUNK_MS", "100"))  # 100ms chunks
CHUNK_BYTES = SAMPLE_RATE * 2 * CHUNK_MS // 1000  # s16le mono


class AudioBridge:
    def __init__(self):
        self.capture_proc: asyncio.subprocess.Process | None = None
        self.playback_proc: asyncio.subprocess.Process | None = None
        self.audio_queue: asyncio.Queue[bytes] = asyncio.Queue(maxsize=100)
        self._speaking = asyncio.Event()

    # ---------------- Capture: meeting audio -> STT ----------------
    async def start_capture(self):
        """Spawn parec and push fixed-size PCM chunks onto the queue."""
        self.capture_proc = await asyncio.create_subprocess_exec(
            "parec",
            f"--device={CAPTURE_DEVICE}",
            "--format=s16le",
            f"--rate={SAMPLE_RATE}",
            "--channels=1",
            "--latency-msec=20",
            stdout=asyncio.subprocess.PIPE,
        )
        assert self.capture_proc.stdout
        try:
            while True:
                chunk = await self.capture_proc.stdout.readexactly(CHUNK_BYTES)
                # Drop oldest if STT is slower than realtime (never block capture).
                if self.audio_queue.full():
                    with contextlib.suppress(asyncio.QueueEmpty):
                        self.audio_queue.get_nowait()
                await self.audio_queue.put(chunk)
        except asyncio.IncompleteReadError:
            pass  # capture process exited

    async def stt_stream(self, on_partial, on_committed):
        """Consume PCM chunks and stream to the STT provider WebSocket.

        Implement: connect to wss endpoint for scribe_v2_realtime, send chunks
        from self.audio_queue, invoke on_partial(text) / on_committed(text, words).
        On connection error: fail over to whisper-1, then whisper-large-v3-turbo
        (buffer ~3s windows and POST as files for the non-streaming fallbacks).
        """
        raise NotImplementedError("Wire to your STT provider chain")

    # ---------------- Playback: TTS -> meeting ----------------
    async def speak(self, audio_bytes: bytes, codec: str = "mp3"):
        """Play TTS audio into the meeting via the TTS sink. Cancellable (barge-in)."""
        await self.cancel_speech()  # only one utterance at a time
        self._speaking.set()
        if codec == "mp3":
            # Decode mp3 -> wav on the fly; paplay only accepts PCM/WAV.
            cmd = ["bash", "-c",
                   f"ffmpeg -loglevel error -i pipe:0 -f wav pipe:1 | "
                   f"paplay --device={PLAYBACK_DEVICE}"]
        else:  # raw wav/pcm
            cmd = ["paplay", f"--device={PLAYBACK_DEVICE}", "--raw",
                   f"--rate={SAMPLE_RATE}", "--format=s16le", "--channels=1"]
        self.playback_proc = await asyncio.create_subprocess_exec(
            *cmd if isinstance(cmd[0], str) and cmd[0] != "bash" else cmd[0],
            *([] if cmd[0] != "bash" else cmd[1:]),
            stdin=asyncio.subprocess.PIPE,
        )
        try:
            self.playback_proc.stdin.write(audio_bytes)
            await self.playback_proc.stdin.drain()
            self.playback_proc.stdin.close()
            await self.playback_proc.wait()
        finally:
            self._speaking.clear()
            self.playback_proc = None

    async def cancel_speech(self):
        """Barge-in: kill any in-flight playback immediately."""
        if self.playback_proc and self.playback_proc.returncode is None:
            self.playback_proc.send_signal(signal.SIGKILL)
            with contextlib.suppress(ProcessLookupError):
                await self.playback_proc.wait()
        self._speaking.clear()

    @property
    def is_speaking(self) -> bool:
        return self._speaking.is_set()

    async def close(self):
        await self.cancel_speech()
        if self.capture_proc and self.capture_proc.returncode is None:
            self.capture_proc.terminate()
            await self.capture_proc.wait()


if __name__ == "__main__":
    # Smoke test: verify devices exist and capture produces audio frames.
    async def main():
        bridge = AudioBridge()
        task = asyncio.create_task(bridge.start_capture())
        chunk = await asyncio.wait_for(bridge.audio_queue.get(), timeout=10)
        print(f"OK: captured {len(chunk)} bytes from {CAPTURE_DEVICE}")
        task.cancel()
        await bridge.close()

    asyncio.run(main())
