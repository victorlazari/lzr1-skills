# Claude Code: English end-of-turn status block

Replaces the Ring plugin's Portuguese closing block (`AINDA NÃO ACABEI` / `PRONTO, ACABEI`)
with an English one that has a progress bar and percentage, on this machine only.

```
## ⏳ NOT DONE YET — 3/6 done · 50%
`█████░░░░░` 50%

**🤖 With me**
- 🔄 <system> · <what Claude still does> — waiting on <what>

**🙋 With you**
- ✅ <system> · <what it unblocks>: <exactly what you do, with link or command>
```

When everything is finished, the last line is `# ✅ DONE — you can close this session`.

## Files

- `session-status.py`: the hook. On SessionStart and UserPromptSubmit it gives Claude the rule. On Stop it checks the block (header counts, percentage, 10-character bar, both lists) and asks Claude once to fix a missing or malformed block. It keeps Ring's dashboard flag at `~/.local/state/ring/needs-you/<session_id>`, which holds the "With you" items.
- `install.sh`: copies the hook to `~/.claude/hooks/` and backs up `~/.claude/settings.json`. In settings it adds the three hook entries and `env.RING_SESSION_DONE=0`, which turns Ring's own closing-block hook off. You can run it more than once, and it ends with a self-test.

## Install

On the other machine, copy this folder anywhere, then either run it yourself:

```bash
bash /path/to/claude-session-status/install.sh
```

or tell Claude Code there: "read /path/to/claude-session-status/README.md and install it". Then restart open Claude Code sessions.

Needs `python3` and `jq`.

## Uninstall

Restore the newest `~/.claude/settings.json.bak-session-status-*`, or remove the three `session-status.py` hook entries and `RING_SESSION_DONE` from `~/.claude/settings.json`.
