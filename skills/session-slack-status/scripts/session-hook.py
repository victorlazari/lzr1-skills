#!/usr/bin/env python3
"""Session Slack status helper: config, per-session state, Claude Code hook, installer.

Subcommands:
  config get | config set-channel <ID>
  state get <sid> | state claim <sid> | state set <sid> <ts> <title> | state release <sid>
  hook            (reads a Claude Code hook event on stdin, prints additionalContext)
  install [--channel ID] | uninstall | status
Files live in ~/.claude/session-slack/ (override: SESSION_SLACK_DIR, CLAUDE_HOME).
"""
import json, os, re, sys, time, shutil

HOME = os.environ.get("CLAUDE_HOME") or os.path.expanduser("~/.claude")
DIR = os.environ.get("SESSION_SLACK_DIR") or os.path.join(HOME, "session-slack")
CONFIG = os.path.join(DIR, "config.json")
CH_RE = re.compile(r"^[CG][A-Z0-9]{8,}$")
SID_RE = re.compile(r"^[A-Za-z0-9-]{8,64}$")
TS_RE = re.compile(r"^\d{10}\.\d{6}$")
MARK = "session-slack-status/scripts/session-hook.py"
BEGIN, END = "<!-- session-slack-status:begin -->", "<!-- session-slack-status:end -->"

BLOCK = BEGIN + """
## Session Slack status
Configured channel lives in ~/.claude/session-slack/config.json (the skill asks for it if missing).
- Every new session (startup, /clear, /new): on the first real task, invoke the `session-slack-status` skill to post the main message. No post for bare greetings.
- After every interaction, invoke it again to post a thread reply with all details discussed. Send any html/csv/xml/json/curl created in the session to the thread too.
- `/sync-slack-session` backfills a session in progress; it never duplicates an existing main message.
""" + END + "\n"


def die(msg, code=2):
    print(msg, file=sys.stderr); sys.exit(code)


def read_json(path):
    try:
        with open(path) as f:
            return json.load(f)
    except (OSError, ValueError):
        return None


def write_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".tmp%d" % os.getpid()
    with open(tmp, "w") as f:
        json.dump(data, f, ensure_ascii=False)
    os.replace(tmp, path)


def channel():
    c = read_json(CONFIG) or {}
    v = c.get("channel", "")
    return v if CH_RE.match(v or "") else ""


def spath(sid):
    if not SID_RE.match(sid or ""):
        die("invalid session id")
    return os.path.join(DIR, sid + ".json")


def status(sid):
    """none | pending | posted | other-channel"""
    st = read_json(spath(sid))
    if not st:
        return "none", None
    if channel() and st.get("channel") != channel():
        return "other-channel", st
    if st.get("status") == "pending" or not st.get("ts"):
        if time.time() - st.get("claimed_at", 0) > 300:
            return "none", st  # stale claim
        return "pending", st
    return "posted", st


def cmd_state(a):
    if len(a) < 2:
        die(__doc__)
    op, sid = a[0], a[1]
    p = spath(sid)
    if op == "get":
        s, st = status(sid)
        print(json.dumps({"status": s, "state": st}, ensure_ascii=False))
    elif op == "claim":
        ch = channel()
        if not ch:
            die("no channel configured", 4)
        s, _ = status(sid)
        if s in ("posted", "pending"):
            print("exists:" + s); sys.exit(3)
        os.makedirs(DIR, exist_ok=True)
        if s == "none" and os.path.exists(p):
            os.remove(p)
        try:
            fd = os.open(p, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        except FileExistsError:
            if s == "other-channel":
                pass
            else:
                print("exists:pending"); sys.exit(3)
            fd = None
        if fd is not None:
            os.close(fd)
        write_json(p, {"channel": ch, "status": "pending", "claimed_at": time.time()})
        print("claimed")
    elif op == "set":
        if len(a) < 4 or not TS_RE.match(a[2]):
            die("usage: state set <sid> <ts 1234567890.123456> <title>")
        write_json(p, {"channel": channel(), "ts": a[2], "title": " ".join(a[3:]), "status": "posted"})
        print("saved")
    elif op == "release":
        st = read_json(p)
        if st and st.get("status") == "pending":
            os.remove(p)
        print("released")
    else:
        die(__doc__)


def cmd_config(a):
    if a[:1] == ["get"]:
        print(json.dumps({"channel": channel() or None}))
    elif a[:1] == ["set-channel"] and len(a) == 2 and CH_RE.match(a[1]):
        write_json(CONFIG, {"channel": a[1]})
        print("channel set")
    else:
        die("usage: config get | config set-channel <C...>")


def ctx_text(event, source, sid):
    ch = channel()
    if not ch:
        return ("Session Slack status is NOT configured: no channel. Before the first real task ask the user which Slack channel ID to use, "
                "then run `python3 ~/.claude/skills/session-slack-status/scripts/session-hook.py config set-channel <ID>`. Session id: %s." % sid)
    s, st = status(sid)
    base = "Session Slack status. Session id: %s. Channel: %s. " % (sid, ch)
    if s == "posted":
        base += "Main message exists (ts %s): post updates as thread replies only. " % st.get("ts")
    elif s == "pending":
        base += "A main message is being posted by this session; do not post another. "
    else:
        base += ("No main message yet: on the first real task invoke the `session-slack-status` skill to create it "
                 "(not for bare greetings); if this session already has work, `/sync-slack-session`. ")
    if event == "UserPromptSubmit":
        base += ("After this interaction invoke the skill to post a thread reply with all details discussed; "
                 "send any html/csv/xml/json/curl created (secrets masked).")
    return base


def cmd_hook():
    try:
        ev = json.load(sys.stdin)
    except ValueError:
        return
    sid = ev.get("session_id") or ""
    if not SID_RE.match(sid):
        return
    name = ev.get("hook_event_name") or "UserPromptSubmit"
    print(json.dumps({"hookSpecificOutput": {"hookEventName": name,
                      "additionalContext": ctx_text(name, ev.get("source"), sid)}}))


def load_settings(p):
    d = read_json(p)
    return d if isinstance(d, dict) else {}


def strip_hooks(d):
    h = d.get("hooks", {})
    for ev in list(h):
        keep = []
        for g in h[ev]:
            g["hooks"] = [x for x in g.get("hooks", []) if MARK not in x.get("command", "")]
            if g["hooks"]:
                keep.append(g)
        if keep:
            h[ev] = keep
        else:
            del h[ev]


def cmd_install(a):
    if "--channel" in a:
        ch = a[a.index("--channel") + 1]
        if not CH_RE.match(ch):
            die("invalid channel id")
        write_json(CONFIG, {"channel": ch})
    sp = os.path.join(HOME, "settings.json")
    if os.path.exists(sp):
        shutil.copy2(sp, sp + ".bak-session-slack")
    d = load_settings(sp)
    strip_hooks(d)
    cmd = 'python3 "$HOME/.claude/skills/%s" hook' % MARK
    h = d.setdefault("hooks", {})
    h.setdefault("SessionStart", []).append({"matcher": "startup|resume|clear|compact", "hooks": [{"type": "command", "command": cmd}]})
    h.setdefault("UserPromptSubmit", []).append({"hooks": [{"type": "command", "command": cmd}]})
    write_json(sp, d)
    cp = os.path.join(HOME, "CLAUDE.md")
    txt = open(cp).read() if os.path.exists(cp) else ""
    if BEGIN in txt and END in txt:
        txt = re.sub(re.escape(BEGIN) + r".*?" + re.escape(END) + r"\n?", lambda m: BLOCK, txt, flags=re.S)
    elif re.search(r"^## Session Slack status\n", txt, re.M):
        txt = re.sub(r"^## Session Slack status\n.*?(?=^## |\Z)", lambda m: BLOCK + "\n", txt, flags=re.S | re.M)
    else:
        txt = txt.rstrip("\n") + "\n\n" + BLOCK
    with open(cp, "w") as f:
        f.write(txt)
    print("installed; channel=%s" % (channel() or "NOT SET"))


def cmd_uninstall():
    sp = os.path.join(HOME, "settings.json")
    d = load_settings(sp)
    strip_hooks(d)
    if os.path.exists(sp):
        write_json(sp, d)
    cp = os.path.join(HOME, "CLAUDE.md")
    if os.path.exists(cp):
        t = open(cp).read()
        open(cp, "w").write(re.sub(re.escape(BEGIN) + r".*?" + re.escape(END) + r"\n?", "", t, flags=re.S))
    print("uninstalled")


def cmd_status():
    sp = os.path.join(HOME, "settings.json")
    h = load_settings(sp).get("hooks", {})
    ok = {ev: any(MARK in x.get("command", "") for g in h.get(ev, []) for x in g.get("hooks", [])) for ev in ("SessionStart", "UserPromptSubmit")}
    cp = os.path.join(HOME, "CLAUDE.md")
    print(json.dumps({"channel": channel() or None, "hooks": ok,
                      "claude_md_block": os.path.exists(cp) and BEGIN in open(cp).read()}))


def main():
    a = sys.argv[1:]
    if not a or a[0] in ("-h", "--help", "help"):
        print(__doc__); return
    c, rest = a[0], a[1:]
    {"config": lambda: cmd_config(rest), "state": lambda: cmd_state(rest), "hook": cmd_hook,
     "install": lambda: cmd_install(rest), "uninstall": cmd_uninstall, "status": cmd_status}.get(c, lambda: die(__doc__))()


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception as e:  # hooks must never break a session
        if len(sys.argv) > 1 and sys.argv[1] == "hook":
            sys.exit(0)
        die("error: %s" % e, 1)
