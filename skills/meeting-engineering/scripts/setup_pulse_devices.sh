#!/usr/bin/env bash
# setup_pulse_devices.sh — Create the virtual audio devices for a Google Meet bot.
# Idempotent: safe to re-run; existing modules with the same sink names are skipped.
#
# Devices created:
#   sindarian-out            null sink   -> bot TTS playback target (paplay --device=sindarian-out)
#   sindarian-out.monitor    monitor src -> Chromium's "microphone" (set as default source)
#   sindarian-meeting        null sink   -> Chromium's audio output (incoming Meet audio)
#   sindarian-meeting-source remap src   -> STT capture device (parec --device=sindarian-meeting-source)
set -euo pipefail

PULSE_SERVER="${PULSE_SERVER:-unix:/tmp/pulse-socket}"
export PULSE_SERVER

wait_for_pulse() {
  for i in $(seq 1 30); do
    if pactl info >/dev/null 2>&1; then return 0; fi
    sleep 0.5
  done
  echo "ERROR: PulseAudio not reachable at ${PULSE_SERVER}" >&2
  exit 1
}

sink_exists() { pactl list short sinks | awk '{print $2}' | grep -qx "$1"; }
source_exists() { pactl list short sources | awk '{print $2}' | grep -qx "$1"; }

wait_for_pulse

if ! sink_exists sindarian-out; then
  pactl load-module module-null-sink \
    sink_name=sindarian-out \
    sink_properties=device.description=TTS_Playback
fi

if ! sink_exists sindarian-meeting; then
  pactl load-module module-null-sink \
    sink_name=sindarian-meeting \
    sink_properties=device.description=Meeting_Audio
fi

if ! source_exists sindarian-meeting-source; then
  pactl load-module module-remap-source \
    master=sindarian-meeting.monitor \
    source_name=sindarian-meeting-source \
    source_properties=device.description=STT_Capture
fi

# Route defaults: Chromium plays Meet audio to sindarian-meeting,
# and captures its "mic" from the TTS sink monitor.
pactl set-default-sink sindarian-meeting
pactl set-default-source sindarian-out.monitor

echo "PulseAudio virtual devices ready:"
pactl list short sinks
pactl list short sources
