---
name: session-slack-status
description: Use when real work starts in any Claude Code session (startup, /clear, /new) and after every interaction. Posts one main Slack message per session to a configured channel, then a thread reply after each interaction with all details discussed, plus any html/csv/xml/json/curl created.
---

# Session Slack Status

Helper: `scripts/session-hook.py` (installed at `~/.claude/skills/session-slack-status/scripts/session-hook.py`; call it as `H`). Slack tools: `mcp__claude_ai_Slack__slack_send_message`, `slack_read_channel`, `slack_create_canvas` (load with ToolSearch `select:` if missing).

## 0. Channel (required, never hardcoded)
Run `python3 H config get`. If `channel` is null: ask the user for the Slack channel ID (AskUserQuestion), check it with `slack_read_channel` (limit 1), then `python3 H config set-channel <ID>`. Never post to any other channel. Changing channels = `config set-channel`; old per-session state in another channel is ignored and a new main message is created.

## 1. Session id
Use the `session_id` from the hook context ("Session Slack status. Session id: ..."). Fallback: the UUID in the scratchpad path (`/private/tmp/claude-*/<project>/<SESSION_ID>/scratchpad`).

## 2. New session = new main message
Every new session (startup, `/clear`, `/new` all produce a new id) gets its own main message once real work starts. Not on a bare greeting.
1. `python3 H state claim <sid>`. `claimed` -> continue. `exists:posted` / `exists:pending` -> do NOT post a main message; go to section 3.
2. Post the main message (below) with `slack_send_message` to the configured channel.
3. `python3 H state set <sid> <ts> "<title>"`. `ts` from the result; if absent, derive from the link (`p1234567890123456` -> `1234567890.123456`).
4. If posting fails: `python3 H state release <sid>`, tell the user once, continue the work.

Main message template:
```
*[<session name>] - [<title>] - [<remote control name>]*

• Session: `<full session id>`
• Started: <local date time + timezone>
• Model: <model name> (`<model id>`)
• Effort: <level or default/unknown>
• Repository: <repo + branch, or "not a git repo", `<cwd>`>
```
Session name = `/rename` name else `session <first 8 chars>`; title <= 8 words; remote control name or `local`.

## 3. Thread update after every interaction
`state get <sid>` -> `ts`; `slack_send_message` with `thread_ts=<ts>`. After each user interaction (not only milestones) post:
- `Update <HH:MM>` then a complete account of what was discussed and done: the request, decisions, commands/changes made, results, links (PR, commit), open points.
- End of a task: prefix `FINAL STATUS`, delivered vs pending, what waits on the user.
- Split into several replies if long. No secrets, tokens, passwords or customer data (mask them).

## 4. Generated artifacts (html, csv, xml, json, curl)
Whenever the session creates one of these, post it in the thread right away (same or next reply):
- Label `<filename or "curl"> (<type>, <size>, <local path>)`.
- Content in a fenced code block with a language tag; chunk at ~4500 chars per reply (max 4 replies). Larger: create a canvas with `slack_create_canvas` holding the content and post its link; if still too large, post head + tail, size and sha256.
- The Slack connector has no file-upload tool; if one is ever available, upload instead.
- Mask `Authorization`, API keys, tokens, cookies, passwords in curls and JSON before posting.

## 5. Already running session
No hook context / no main message yet: use `/sync-slack-session` (never post a second main message).

## Install / status
`python3 H install [--channel <ID>]` wires the SessionStart (startup|resume|clear|compact) and UserPromptSubmit hooks in `~/.claude/settings.json` (backup `.bak-session-slack`) and the `~/.claude/CLAUDE.md` block; `status` verifies; `uninstall` removes. Hooks inject the session id and state as context; they cannot post by themselves.
