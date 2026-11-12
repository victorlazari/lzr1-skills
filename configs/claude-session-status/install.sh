#!/usr/bin/env bash
# Installs the personal end-of-turn status hook for Claude Code.
# Safe to run more than once. Needs python3 and jq.
set -euo pipefail
here=$(cd "$(dirname "$0")" && pwd)
command -v jq >/dev/null || { echo "jq is required (brew install jq)"; exit 1; }
command -v python3 >/dev/null || { echo "python3 is required"; exit 1; }

mkdir -p ~/.claude/hooks
install -m 755 "$here/session-status.py" ~/.claude/hooks/session-status.py

s=~/.claude/settings.json
[ -f "$s" ] || echo '{}' > "$s"
cp "$s" "$s.bak-session-status-$(date +%Y%m%d%H%M%S)"
cmd='python3 ~/.claude/hooks/session-status.py'
tmp=$(mktemp)
jq --arg cmd "$cmd" '
  def add($ev): .hooks[$ev] = ((.hooks[$ev] // [])
    | if any(.[]?; any(.hooks[]?; .command == $cmd)) then . else . + [{hooks: [{type: "command", command: $cmd}]}] end);
  .env = ((.env // {}) + {RING_SESSION_DONE: "0"})
  | .hooks = (.hooks // {})
  | add("SessionStart") | add("UserPromptSubmit") | add("Stop")
' "$s" > "$tmp" && mv "$tmp" "$s"

# Self-test: a valid block passes, plain text is nudged.
export CLAUDE_CODE_SESSION_ATTENDED=1 XDG_STATE_HOME=$(mktemp -d)
ok=$(printf '%s' '{"session_id":"t","hook_event_name":"Stop","last_assistant_message":"x\n# ✅ DONE — you can close this session"}' | python3 ~/.claude/hooks/session-status.py)
bad=$(printf '%s' '{"session_id":"t","hook_event_name":"Stop","last_assistant_message":"plain text"}' | python3 ~/.claude/hooks/session-status.py)
[ -z "$ok" ] && [ -n "$bad" ] && echo "Installed and self-test passed. Restart open Claude Code sessions to pick it up." || { echo "Self-test FAILED"; exit 1; }
