---
name: sync-slack-session
description: Use when the user runs /sync-slack-session or a session already in progress never posted its main Slack message. Backfills the main message and thread without ever duplicating an existing one. Triggers on "sync slack session".
---

# Sync Slack Session

Backfills the Slack record for the current session using the `session-slack-status` skill (helper `H` = `~/.claude/skills/session-slack-status/scripts/session-hook.py`).

1. Channel: `python3 H config get`; if null, ask the user and `config set-channel <ID>`.
2. Session id: hook context, else the UUID in the scratchpad path.
3. Duplicate check, local: `python3 H state get <sid>`. `posted` -> do NOT post a main message; reply "already synced" with the message ts and, if useful, post only a catch-up thread reply.
4. Duplicate check, Slack (state may have been deleted): `slack_read_channel` on the configured channel (a few pages) or `slack_search_public_and_private` for the full session id. If a main message containing `Session: \`<sid>\`` exists: `state set <sid> <ts> "<title>"` and treat as posted.
5. Still none: `state claim <sid>`; on `exists:*` stop. Post the main message per `session-slack-status` section 2 (title from the work done so far; Started = first transcript event time if known, else now), then `state set`.
6. Post ONE thread reply `Sync <HH:MM>` summarizing everything discussed and done so far in the session, plus any html/csv/xml/json/curl already created (section 4 of `session-slack-status`, secrets masked).
7. Report to the user in one line: created or already synced, with the Slack link. From then on follow the normal per-interaction thread updates.
