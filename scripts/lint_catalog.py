#!/usr/bin/env python3
"""Catalog linter for the skills repository (stdlib only; run with python3 -I).

Rules: fm-missing fm-name fm-desc fm-syntax link-broken ref-orphan exec-bit
       manifest-sync count-sync symlink stale-ref (ERROR); desc-trigger, link-broken-prose (WARN).
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
STALE_PATTERNS = [
    r"claude[- ]?3", r"claude-(instant|2)", r"gpt-4o", r"gpt-4-turbo",
    r"gpt-3\.5", r"text-davinci", r"gemini[- ]?1\.5", r"Next\.js 1[0-3]\b(?!\.\d)",
]
STALE_RE = re.compile("|".join("(?:%s)" % p for p in STALE_PATTERNS), re.I)
STALE_EXEMPT = "(historical)"
STALE_EXTS = (".md", ".yaml", ".yml", ".json", ".sh", ".py")


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
                    m = STALE_RE.search(ln)
                    if m and STALE_EXEMPT not in ln:
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
            add("WARN", name, "desc-trigger",
                "description has no 'use when'/'use for'/'triggers'")
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

    for level, skill, rule, detail in out:
        print(("%s %s: %s %s" % (level, skill, rule, detail)).rstrip())
    errs = sum(1 for o in out if o[0] == "ERROR")
    warns = len(out) - errs
    print("Summary: %d skill(s) checked, %d error(s), %d warning(s)" % (len(targets), errs, warns))
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
