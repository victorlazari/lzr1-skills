#!/usr/bin/env bash
# meet-entrypoint.sh — Container entrypoint template for a Google Meet bot worker.
# Run under tini (PID 1):  ENTRYPOINT ["/usr/bin/tini", "--", "/app/meet-entrypoint.sh"]
# Startup order: Xvfb -> PulseAudio -> virtual devices -> worker (exec'd, receives signals).
set -euo pipefail

export DISPLAY="${DISPLAY:-:99}"
export PULSE_SERVER="${PULSE_SERVER:-unix:/tmp/pulse-socket}"
SCREEN_GEOMETRY="${SCREEN_GEOMETRY:-1280x720x24}"

cleanup() {
  echo "[entrypoint] shutting down..."
  [[ -n "${PULSE_PID:-}" ]] && kill "${PULSE_PID}" 2>/dev/null || true
  [[ -n "${XVFB_PID:-}" ]] && kill "${XVFB_PID}" 2>/dev/null || true
}
trap cleanup EXIT

# --- 1. Virtual display -------------------------------------------------
Xvfb "${DISPLAY}" -screen 0 "${SCREEN_GEOMETRY}" -nolisten tcp -ac &
XVFB_PID=$!
for i in $(seq 1 30); do
  if xdpyinfo -display "${DISPLAY}" >/dev/null 2>&1; then break; fi
  sleep 0.5
done
echo "[entrypoint] Xvfb ready on ${DISPLAY}"

# --- 2. PulseAudio daemon ----------------------------------------------
# --exit-idle-time=-1 keeps the daemon alive with no clients connected.
pulseaudio --daemonize=no --exit-idle-time=-1 \
  --load="module-native-protocol-unix socket=/tmp/pulse-socket auth-anonymous=1" \
  --disallow-exit --log-target=stderr &
PULSE_PID=$!
for i in $(seq 1 30); do
  if pactl info >/dev/null 2>&1; then break; fi
  sleep 0.5
done
echo "[entrypoint] PulseAudio ready at ${PULSE_SERVER}"

# --- 3. Virtual audio devices -------------------------------------------
/app/setup_pulse_devices.sh

# --- 4. Worker -----------------------------------------------------------
# exec replaces the shell so the worker receives SIGTERM directly from tini.
echo "[entrypoint] starting worker: $*"
exec "$@"
