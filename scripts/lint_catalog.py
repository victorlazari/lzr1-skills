#!/usr/bin/env python3
"""Catalog linter for the skills repository (stdlib only; run with python3 -I).

Rules: fm-missing fm-name fm-desc fm-syntax link-broken ref-orphan exec-bit
       manifest-sync count-sync symlink stale-ref desc-trigger skill-ref script-untested (ERROR); link-broken-prose (WARN).

stale-ref model ids: any token claude-(fable|opus|sonnet|haiku|mythos)-<digit>... must be
exactly one of VALID_MODELS, optionally followed by -YYYYMMDD; claude_<digit> and the spaced
prose "claude mythos" are always flagged. A line containing "(historical)" is exempt.

skill-ref heuristic (deliberately conservative). A single-backtick token is a skill pointer
ONLY in these places, and must then be a name listed in skills-list.txt:
  (a) frontmatter description: the token right after the word "use" or "see", or after
      "not for ...:" (e.g. "Not for X: use `foo-bar`");
  (b) a line starting with "**Related skills:**": every backticked token on it;
  (c) a body line containing "route to", "defer to", "hand off to" or "instead": backticked
      tokens matching ^[a-z][a-z0-9]*(-[a-z0-9]+)+$ (hyphenated; so no "/", ".", leading
      "-", spaces). Names in SKILL_REF_ALLOW (hyphenated commands) are skipped.
Fenced code blocks are ignored for (b) and (c).

script-untested: every file under skills/*/scripts/ (recursive; __pycache__, *.pyc and
.DS_Store ignored; skill tests/ dirs are not scripts) needs a row in tests/script-coverage.tsv
(header path<TAB>level<TAB>reason<TAB>test, rows bytewise sorted by path, no duplicates). Level is
static (reason required), help (--help is safe) or behavior (test = existing file under the repo
that mentions the script basename). Rows must point at existing files.
"""
import argparse
import os
import re
import sys

_STOP = r"[^\s)`\"'\]>]"
PATH_RE = re.compile(
    r"(?:\.\./)+" + _STOP + r"+"
    r"|skills/[A-Za-z0-9_.-]+/" + _STOP + r"+"
    r"|(?:references|scripts|templates|assets)/" + _STOP + r"+"
)
MDLINK_RE = re.compile(r"\]\(\s*<?([^)\s>]+)")
BARE_RE = re.compile(
    r"(?<![A-Za-z0-9_./~-])(?:references|scripts|templates|assets)/" + _STOP + r"+"
)
SPAN_RE = re.compile(r"`([^`\n]+)`")
BLOCK_RE = re.compile(r"^[>|][+-]?$")
SKIP_CHARS = ("*", "<", "{", "$")
TRIGGER_RE = re.compile(r"use when|use for|triggers", re.I)
# Scope: files under skills/ only; README.md and root docs are deliberately not scanned.
_G = r"(?<![A-Za-z0-9])"
VALID_MODELS = ("claude-fable-5-1", "claude-opus-5-5", "claude-sonnet-5-5", "claude-haiku-5-5")
# Id = family + dash-separated digits, optional -suffix (only -vN is accepted, checked below); then a hard boundary so a trailing
# ".md", sentence "." or ")" is fine but "-beta", "_x", ".5" (claude-opus-5.5) are not.
MODEL_RE = re.compile(r"(?<![A-Za-z0-9])claude-(?:fable|opus|sonnet|haiku|mythos)-[0-9]+(?:-[0-9]+)*(?:\.[0-9]+)*"
                      r"(?:-[A-Za-z][A-Za-z0-9_-]*)?(?![A-Za-z0-9_])", re.I)
DATE_RE = re.compile(r"-20(?:2[4-9]|[3-9][0-9])(?:0[1-9]|1[0-2])(?:0[1-9]|[12][0-9]|3[01])$")
DESC_PTR_RE = re.compile(r"(?:\b(?:use|see)\b|\bnot for\b[^`]*?:)\s*`([^`\n]+)`", re.I)
# Body trigger: route/defer/hand off to, or "use `tok` instead". Bare "instead" is not a trigger.
ROUTE_TOK_RE = re.compile(r"(?:route to|defer to|hand off to)|\buse\s+`[^`\n]+`\s*(?:\w+\s+){0,3}?instead", re.I)
HYPHEN_RE = re.compile(r"^[a-z][a-z0-9]*(-[a-z0-9]+)+$")
SKILL_REF_ALLOW = frozenset(("docker-compose",))
STALE_PATTERNS = [
    _G + r"claude[- ]?3(?![A-Za-z])", _G + r"claude[- ]2(?!\d)", _G + r"claude-instant",
    _G + r"claude[- ]instant", _G + r"gpt-4o", _G + r"gpt-4-turbo", _G + r"gpt-3\.5",
    _G + r"text-davinci", _G + r"gemini[- ]?1\.5",
    _G + r"claude_[0-9]", _G + r"claude mythos",
    r"Next\.js 1[0-2](?!\d)", r"Next\.js 13(?!\d)(?!\.[4-9](?!\d))",
]
STALE_RE = re.compile("|".join("(?:%s)" % p for p in STALE_PATTERNS), re.I)
STALE_EXEMPT = "(historical)"
STALE_EXTS = (".md", ".yaml", ".yml", ".json", ".sh", ".py", ".txt", ".toml", ".ts",
              ".tsx", ".js", ".mjs", ".html", ".jinja", ".j2")


REGISTRY = "tests/script-coverage.tsv"
LEVELS = ("static", "help", "behavior")
SCRIPT_SKIP_DIRS = ("__pycache__",)
SCRIPT_SKIP_FILES = (".DS_Store",)


def skill_scripts(root, name):
    """Repo-relative posix paths of every script file of one skill."""
    base = os.path.join(root, "skills", name, "scripts")
    found = []
    for dp, dns, fns in os.walk(base):
        dns[:] = sorted(d for d in dns if d not in SCRIPT_SKIP_DIRS)
        for fn in fns:
            if fn in SCRIPT_SKIP_FILES or fn.endswith(".pyc"):
                continue
            found.append(os.path.relpath(os.path.join(dp, fn), root).replace(os.sep, "/"))
    return sorted(found)


def load_registry(root):
    """Return (rows, problems). rows: list of (lineno, path, level, reason, test)."""
    path = os.path.join(root, REGISTRY)
    if not os.path.isfile(path):
        return None, ["%s missing" % REGISTRY]
    lines = read(path).replace("\r\n", "\n").split("\n")
    while lines and lines[-1] == "":
        lines.pop()
    problems, rows = [], []
    if not lines or lines[0].split("\t") != ["path", "level", "reason", "test"]:
        problems.append("%s: header must be path<TAB>level<TAB>reason<TAB>test" % REGISTRY)
        return rows, problems
    for i, ln in enumerate(lines[1:], 2):
        cols = ln.split("\t")
        if len(cols) != 4:
            problems.append("%s:%d expected 4 tab-separated columns, got %d" % (REGISTRY, i, len(cols)))
            continue
        rows.append((i,) + tuple(c.strip() for c in cols))
    return rows, problems


def mentions_basename(path, base):
    rx = re.compile(r"(?<![A-Za-z0-9_.-])" + re.escape(base) + r"(?![A-Za-z0-9_-])")
    return bool(rx.search(read(path)))


def parse_frontmatter(text):
    lines = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    if not lines or lines[0].strip() != "---":
        return None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            fm = {}
            bad = []
            last = None
            for ln in lines[1:i]:
                if not ln.strip() or ln.lstrip().startswith("#"):
                    continue
                if ln[0] in " \t" and last == "description":
                    fm["__multi_description"] = True
                    continue
                m = re.match(r"^([A-Za-z0-9_-]+)\s*:\s*(.*)$", ln)
                if not m:
                    bad.append(ln.strip()[:60])
                    last = None
                    continue
                last = m.group(1)
                v = m.group(2).strip()
                if BLOCK_RE.match(v) and last == "description":
                    fm["__multi_description"] = True
                    continue
                if BLOCK_RE.match(v):
                    bad.append("%s: %s (block scalar)" % (m.group(1), v))
                    fm["__block_" + m.group(1)] = v
                    continue
                if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
                    v = v[1:-1]
                fm[m.group(1)] = v
            fm["__bad"] = bad
            return fm
    return None


def read(path):
    with open(path, encoding="utf-8-sig", errors="replace") as f:
        return f.read()


def first_int(path, pattern):
    try:
        m = re.search(pattern, read(path), re.M)
    except OSError:
        return None
    return int(m.group(1)) if m else None


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    default_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ap.add_argument("--root", default=default_root, help="repo root")
    ap.add_argument("--skill", help="only lint this skill (skips repo-level rules)")
    args = ap.parse_args()
    root = os.path.abspath(args.root)
    sdir = os.path.join(root, "skills")
    out = []  # (level, skill, rule, detail)

    def add(level, skill, rule, detail=""):
        out.append((level, skill, rule, detail))

    names = sorted(
        d for d in os.listdir(sdir)
        if os.path.islink(os.path.join(sdir, d)) or os.path.isdir(os.path.join(sdir, d))
    ) if os.path.isdir(sdir) else []
    targets = [args.skill] if args.skill else names
    if args.skill and args.skill not in names:
        print("ERROR %s: fm-missing skill directory not found" % args.skill)
        return 1

    reg_rows, reg_problems = load_registry(root)
    registered = set(r[1] for r in reg_rows or [])
    known = set(names)
    mp = os.path.join(root, "skills-list.txt")
    if os.path.isfile(mp):
        known = set(l.strip() for l in read(mp).splitlines()
                    if l.strip() and not l.strip().startswith("#"))
    for name in targets:
        base = os.path.join(sdir, name)
        if os.path.islink(base):
            add("ERROR", name, "symlink", os.path.relpath(base, root))
            continue
        # symlinks anywhere inside the skill
        for dp, dns, fns in os.walk(base):
            for n in dns + fns:
                p = os.path.join(dp, n)
                if os.path.islink(p):
                    add("ERROR", name, "symlink", os.path.relpath(p, root))
        for dp, _, fns in os.walk(base):
            for fn in sorted(fns):
                p = os.path.join(dp, fn)
                if not fn.lower().endswith(STALE_EXTS) or os.path.islink(p):
                    continue
                for i, ln in enumerate(read(p).splitlines(), 1):
                    if STALE_EXEMPT in ln.lower():
                        continue
                    for m in STALE_RE.finditer(ln):
                        add("ERROR", name, "stale-ref", "%s:%d %s"
                            % (os.path.relpath(p, root), i, m.group(0)))
                    for m in MODEL_RE.finditer(ln):
                        tok = re.sub(r"-v[0-9]+$", "", m.group(0).lower())
                        if not any(tok == v or (tok.startswith(v) and DATE_RE.fullmatch(tok[len(v):]))
                                   for v in VALID_MODELS):
                            add("ERROR", name, "stale-ref", "%s:%d %s"
                                % (os.path.relpath(p, root), i, m.group(0)))
        skill_md = os.path.join(base, "SKILL.md")
        if not os.path.isfile(skill_md):
            add("ERROR", name, "fm-missing", "SKILL.md not found")
            continue
        text = read(skill_md)
        fm = parse_frontmatter(text)
        if fm is None:
            add("ERROR", name, "fm-missing", "no frontmatter block")
            continue
        if fm.get("name") != name:
            add("ERROR", name, "fm-name",
                "name %r != directory %r" % (fm.get("name"), name))
        for b in fm.get("__bad", []):
            add("ERROR", name, "fm-syntax",
                "frontmatter must be single-line 'key: value': " + b)
        desc = fm.get("description", "")
        if fm.get("__multi_description"):
            add("ERROR", name, "fm-desc",
                "multi-line/block description not supported")
        elif not desc:
            add("ERROR", name, "fm-desc", "description absent or empty")
        elif len(desc) > 1024:
            add("ERROR", name, "fm-desc", "description is %d chars (max 1024)" % len(desc))
        if desc and not TRIGGER_RE.search(desc):
            add("ERROR", name, "desc-trigger",
                "description has no 'use when'/'use for'/'triggers'")
        # skill pointers
        ptrs = [m.group(1) for m in DESC_PTR_RE.finditer(desc)
                if HYPHEN_RE.match(m.group(1)) and m.group(1) not in SKILL_REF_ALLOW]
        infence = False
        for ln in text.splitlines():
            if ln.lstrip().startswith(("```", "~~~")):
                infence = not infence
                continue
            if infence:
                continue
            toks = SPAN_RE.findall(ln)
            if ln.lstrip().startswith("**Related skills:**"):
                ptrs.extend(toks)
            elif ROUTE_TOK_RE.search(ln):
                ptrs.extend(t for t in toks if HYPHEN_RE.match(t)
                            and t not in SKILL_REF_ALLOW)
        for t in dict.fromkeys(ptrs):
            if t not in known:
                add("ERROR", name, "skill-ref", "`%s` not in skills-list.txt" % t)
        # links
        seen = set()
        fences = []
        prose = []
        in_fence = False
        for ln in text.splitlines():
            if ln.lstrip().startswith(("```", "~~~")):
                in_fence = not in_fence
                continue
            (fences if in_fence else prose).append(ln)
        strong = [(m.group(1), "link-broken") for m in MDLINK_RE.finditer(text)]
        for sm in SPAN_RE.finditer(text):
            strong.extend((c, "link-broken") for c in PATH_RE.findall(sm.group(1)))
        weak = [(c, "link-broken-prose")
                for c in BARE_RE.findall("\n".join(prose + fences))]
        for raw, rule in strong + weak:
            if "://" in raw:
                continue
            if raw.startswith("./"):
                raw = raw[2:]
            pm = PATH_RE.match(raw)
            if not pm:
                continue
            tok = pm.group(0).split("#", 1)[0].rstrip("!?,.;:")
            if not tok or any(c in tok for c in SKIP_CHARS) or tok in seen:
                continue
            origin = root if tok.startswith("skills/") else base
            if os.path.exists(os.path.join(origin, tok)):
                seen.add(tok)
            elif rule == "link-broken":
                seen.add(tok)
                add("ERROR", name, rule, tok)
            elif (tok, "w") not in seen:
                seen.add((tok, "w"))
                add("WARN", name, rule, tok)
        # orphan refs
        refdir = os.path.join(base, "references")
        if os.path.isdir(refdir):
            for dp, _, fns in os.walk(refdir):
                for fn in sorted(fns):
                    if not re.search(r"(?<![A-Za-z0-9_.-])" + re.escape(fn)
                                     + r"(?![A-Za-z0-9_-])", text):
                        add("ERROR", name, "ref-orphan",
                            os.path.relpath(os.path.join(dp, fn), base))
        # script registry: every script needs a row
        for rel in skill_scripts(root, name):
            if rel not in registered:
                add("ERROR", name, "script-untested", "%s has no row in %s" % (rel, REGISTRY))
        # exec bits
        scdir = os.path.join(base, "scripts")
        if os.path.isdir(scdir):
            for dp, _, fns in os.walk(scdir):
                for fn in sorted(fns):
                    p = os.path.join(dp, fn)
                    if fn.endswith((".sh", ".py")) and not os.path.islink(p) \
                            and not os.access(p, os.X_OK):
                        add("ERROR", name, "exec-bit",
                            os.path.relpath(p, base) + " is not executable")

    if not args.skill:
        count = len(names)
        mpath = os.path.join(root, "skills-list.txt")
        if os.path.isfile(mpath):
            listed = [l.strip() for l in read(mpath).splitlines()
                      if l.strip() and not l.strip().startswith("#")]
            if len(listed) != len(set(listed)):
                add("ERROR", "-", "manifest-sync", "skills-list.txt contains duplicate lines")
            if listed != sorted(listed):
                add("ERROR", "-", "manifest-sync", "skills-list.txt must be bytewise sorted")
            a, b = set(names), set(listed)
            if a != b:
                add("ERROR", "-", "manifest-sync",
                    "on disk not in manifest: %s; in manifest not on disk: %s"
                    % (sorted(a - b), sorted(b - a)))
        else:
            add("ERROR", "-", "manifest-sync", "skills-list.txt missing")
        checks = [
            ("install.sh", r"^\s*EXPECTED_SKILL_COUNT=(\d+)", "EXPECTED_SKILL_COUNT"),
            ("tests/test-installer.sh", r"^\s*EXPECTED=(\d+)", "EXPECTED"),
            ("README.md", r"skills-(\d+)-", "badge skills-N-"),
            ("README.md", r"(\d+) curated AI skills", "'N curated AI skills'"),
        ]
        derived_pat = re.compile(r'^\s*EXPECTED=\$\(\s*wc\s+-l\s*<\s*"\$ROOT/skills-list\.txt"')
        for rel, pat, label in checks:
            if rel == "tests/test-installer.sh":
                tp = os.path.join(root, rel)
                if os.path.isfile(tp) and any(derived_pat.match(l) for l in read(tp).splitlines()):
                    continue  # derived from skills-list.txt, nothing to compare
            v = first_int(os.path.join(root, rel), pat)
            if v is None:
                add("ERROR", "-", "count-sync", "%s: pattern for %s not found" % (rel, label))
            elif v != count:
                add("ERROR", "-", "count-sync",
                    "%s %s=%d but %d skill directories" % (rel, label, v, count))

    if not args.skill:
        for pr in reg_problems:
            add("ERROR", "-", "script-untested", pr)
        prev = None
        seen_paths = set()
        for lineno, path, level, reason, test in reg_rows or []:
            where = "%s:%d %s" % (REGISTRY, lineno, path)
            if path in seen_paths:
                add("ERROR", "-", "script-untested", where + " duplicate row")
            seen_paths.add(path)
            if prev is not None and path < prev:
                add("ERROR", "-", "script-untested", where + " rows must be sorted by path")
            prev = path
            if not re.match(r"^skills/[^/]+/scripts/.+", path) or not os.path.isfile(os.path.join(root, path)):
                add("ERROR", "-", "script-untested", where + " stale row: no such script file")
            if level not in LEVELS:
                add("ERROR", "-", "script-untested", where + " level %r not in static|help|behavior" % level)
            elif level == "static" and not reason:
                add("ERROR", "-", "script-untested", where + " static row needs a reason")
            elif level == "behavior":
                tp = os.path.join(root, test) if test else ""
                if not test:
                    add("ERROR", "-", "script-untested", where + " behavior row needs a test file")
                elif not os.path.isfile(tp):
                    add("ERROR", "-", "script-untested", where + " test file %s not found" % test)
                elif not mentions_basename(tp, os.path.basename(path)):
                    add("ERROR", "-", "script-untested", where + " test %s does not mention %s"
                        % (test, os.path.basename(path)))

    for level, skill, rule, detail in out:
        print(("%s %s: %s %s" % (level, skill, rule, detail)).rstrip())
    errs = sum(1 for o in out if o[0] == "ERROR")
    warns = len(out) - errs
    print("Summary: %d skill(s) checked, %d error(s), %d warning(s)" % (len(targets), errs, warns))
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
