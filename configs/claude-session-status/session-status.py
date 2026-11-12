#!/usr/bin/env python3
"""Personal end-of-turn status block (replaces Ring's session-done.sh, which
settings.json turns off with RING_SESSION_DONE=0).

SessionStart and UserPromptSubmit announce the rule; Stop checks the closing
block and nudges once per turn when it is missing or malformed. Like Ring's
hook it keeps the "needs you" flag at $XDG_STATE_HOME/ring/needs-you/<sid>:
it holds the "With you" items while the last turn ended on something only the
user can do, and is removed on every other ending.
"""

import hashlib
import json
import os
import re
import sys
import tempfile

DONE_LINE = "# ✅ DONE — you can close this session"
HEADER_RE = re.compile(r"^## ⏳ NOT DONE YET — (\d+)/(\d+) done · (\d{1,3})%$")
BAR_RE = re.compile(r"^`([█░]{10})` (\d{1,3})%$")
ME = "**🤖 With me**"
YOU = "**🙋 With you**"
ITEM_RE = re.compile(r"^- \S")
NOTHING = "- nothing"

RULE = f"""End every turn with the status block, always in English (whatever language the conversation uses), so the user can tell from across their panes whether this session can be closed. This holds on turns started by a background notification or by another session's message too.

Done = everything the user asked for is delivered and verified, no lane, workflow, background job or PR of this session waits on anything, and no question to the user is open. Then the last line is exactly:
{DONE_LINE}

Not done: end with this block, nothing after it:

## ⏳ NOT DONE YET — <done>/<total> done · <pct>%
`<bar>` <pct>%

{ME}
- <emoji> <system> · <what this session still does or will remind the user of> — waiting on <what>

{YOU}
- <emoji> <system> · <what it unblocks>: <exactly what the user does now, with the command, path or link inline>

Rules for the block:
- <total> counts the deliverables of the user's requests still tracked in this session (finished ones included); <done> counts those delivered and verified; <pct> = round(done / total * 100). Never 100% in this block.
- <bar> is exactly 10 characters: one █ per full 10% (pct // 10), the rest ░. The pct after the bar repeats the header's.
- One bullet per item, one line each. Emojis: 🔄 in progress / waiting on CI, a merge or a lane; ⏸️ blocked; ✅ an action to take (approve, run, merge); ❓ a question or decision, with your recommendation.
- The user reads the block cold, hours later: every item starts with its system and the work it belongs to, and a "With you" item says what it unblocks and exactly how to do it, never "above".
- "With you" holds only actions the user can take this turn (approve, answer, run, decide). Anything that first waits on something else (CI, a merge, a lane, another person) stays under "With me", worded as what you will ask or remind the user once it lands.
- A side with no items is exactly the single bullet "{NOTHING}". Both sides "{NOTHING}" means done: use the done line instead."""

RULE_SUM = hashlib.sha256(RULE.encode()).hexdigest()[:16]
STATE = os.path.join(os.environ.get("XDG_STATE_HOME") or os.path.expanduser("~/.local/state"), "ring")
MARKER_DIR = os.path.join(STATE, "session-status")
FLAG_DIR = os.path.join(STATE, "needs-you")


def emit(event, context):
    print(json.dumps({"hookSpecificOutput": {"hookEventName": event, "additionalContext": context}}))


def mark(sid):
    if sid:
        try:
            os.makedirs(MARKER_DIR, exist_ok=True)
            with open(os.path.join(MARKER_DIR, sid), "w") as f:
                f.write(RULE_SUM + "\n")
        except OSError:
            pass


def unflag(sid):
    if sid:
        try:
            os.remove(os.path.join(FLAG_DIR, sid))
        except OSError:
            pass


def setflag(sid, you_items):
    if not sid:
        return
    text = " | ".join(i[2:].replace("**", "").strip() for i in you_items)
    try:
        os.makedirs(FLAG_DIR, exist_ok=True)
        fd, tmp = tempfile.mkstemp(dir=FLAG_DIR, prefix=f".{sid}.")
        with os.fdopen(fd, "w") as f:
            f.write(text + "\n")
        os.replace(tmp, os.path.join(FLAG_DIR, sid))
    except OSError:
        pass


def parse_block(message):
    """(ok, you_items, problem) for the closing not-done block of `message`."""
    lines = [l.rstrip() for l in message.split("\n") if l.strip()]
    starts = [i for i, l in enumerate(lines) if l.startswith("## ⏳ NOT DONE YET")]
    if not starts:
        return False, [], "no '## ⏳ NOT DONE YET' header and the last line is not the done line"
    block = lines[starts[-1]:]
    m = HEADER_RE.match(block[0])
    if not m:
        return False, [], f"header must read '## ⏳ NOT DONE YET — <done>/<total> done · <pct>%', got {block[0]!r}"
    done, total, pct = int(m[1]), int(m[2]), int(m[3])
    if total < 1 or done > total or done == total:
        return False, [], f"{done}/{total}: total must be ≥ 1 and done < total (all done means the done line)"
    if pct != round(done / total * 100):
        return False, [], f"{pct}% does not match {done}/{total} (expected {round(done / total * 100)}%)"
    if len(block) < 2 or not BAR_RE.match(block[1]):
        return False, [], "second line must be the 10-character bar in backticks followed by the percentage"
    bm = BAR_RE.match(block[1])
    if int(bm[2]) != pct or bm[1] != "█" * (pct // 10) + "░" * (10 - pct // 10):
        return False, [], f"bar must be `{'█' * (pct // 10) + '░' * (10 - pct // 10)}` {pct}%"
    rest = block[2:]
    if ME not in rest or YOU not in rest or rest.index(ME) != 0 or rest.index(YOU) < 2:
        return False, [], f"after the bar: '{ME}' with its bullets, then '{YOU}' with its bullets, nothing else"
    y = rest.index(YOU)
    me_items, you_items = rest[1:y], rest[y + 1:]
    for name, items in (("With me", me_items), ("With you", you_items)):
        if not items:
            return False, [], f"'{name}' needs at least one bullet (or exactly '{NOTHING}')"
        bad = [i for i in items if not ITEM_RE.match(i)]
        if bad:
            return False, [], f"'{name}' holds a line that is not a '- ' bullet, or text follows the block: {bad[0]!r}"
        if len(items) > 1 and any(i.lower().rstrip(".") == NOTHING for i in items):
            return False, [], f"'{name}': '{NOTHING}' must be the only bullet"
    nothing = lambda items: len(items) == 1 and items[0].lower().rstrip(".") == NOTHING
    if nothing(me_items) and nothing(you_items):
        return False, [], "both sides are 'nothing': end with the done line instead"
    return True, ([] if nothing(you_items) else you_items), None


def main():
    if os.environ.get("CLAUDE_CODE_SESSION_ATTENDED") != "1" or os.environ.get("SESSION_STATUS") == "0":
        return
    try:
        data = json.load(sys.stdin)
    except ValueError:
        return
    sid = data.get("session_id") or ""
    event = data.get("hook_event_name")
    if re.search(r"/lerianstudio/isengard/\.runs(/|$)", data.get("cwd") or ""):
        return

    if event == "SessionStart":
        mark(sid)
        emit("SessionStart", RULE)
        return
    if event == "UserPromptSubmit":
        unflag(sid)
        try:
            current = open(os.path.join(MARKER_DIR, sid)).read().strip() if sid else RULE_SUM
        except OSError:
            current = ""
        if current != RULE_SUM:
            mark(sid)
            emit("UserPromptSubmit", "This closing-block rule replaces any earlier one (including Ring's AINDA NÃO ACABEI / PRONTO, ACABEI):\n" + RULE)
        return
    if event != "Stop":
        return

    message = data.get("last_assistant_message") or ""
    nonempty = [l.rstrip() for l in message.split("\n") if l.strip()]
    if nonempty and nonempty[-1] == DONE_LINE:
        unflag(sid)
        return
    ok, you_items, problem = parse_block(message)
    if ok:
        if you_items:
            setflag(sid, you_items)
        else:
            unflag(sid)
        return
    unflag(sid)
    if data.get("stop_hook_active"):
        return
    mark(sid)
    tail = "\n".join(json.dumps(l, ensure_ascii=False) for l in nonempty[-4:])
    emit("Stop", f"{RULE}\n\nYour reply does not end with the done line or a valid status block: {problem}.\nLast lines:\n{tail}\nReply with the done line or the status block only. Do not rewrite the answer.")


if __name__ == "__main__":
    main()
