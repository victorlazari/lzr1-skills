#!/usr/bin/env python3
"""Catalog linter for the skills repository (stdlib only; run with python3 -I).

Rules: fm-missing fm-name fm-desc link-broken ref-orphan exec-bit
       manifest-sync count-sync symlink (ERROR); desc-trigger (WARN).
"""
import argparse
import os
import re
import sys

LINK_RE = re.compile(r"(?:references|scripts|templates|assets)/[^\s)`\"'\]>,;]+")
SKIP_CHARS = ("*", "<", "{", "$")
TRIGGER_RE = re.compile(r"use when|use for|triggers", re.I)


def parse_frontmatter(text):
    lines = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    if not lines or lines[0].strip() != "---":
        return None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            fm = {}
            for ln in lines[1:i]:
                if not ln.strip() or ln.lstrip().startswith("#"):
                    continue
                m = re.match(r"^([A-Za-z0-9_-]+)\s*:\s*(.*)$", ln)
                if not m:
                    continue
                v = m.group(2).strip()
                if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
                    v = v[1:-1]
                fm[m.group(1)] = v
            return fm
    return None


def read(path):
    with open(path, encoding="utf-8", errors="replace") as f:
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
        d for d in os.listdir(sdir) if os.path.isdir(os.path.join(sdir, d))
    ) if os.path.isdir(sdir) else []
    targets = [args.skill] if args.skill else names
    if args.skill and args.skill not in names:
        print("ERROR %s: fm-missing skill directory not found" % args.skill)
        return 1

    for name in targets:
        base = os.path.join(sdir, name)
        # symlinks anywhere inside the skill
        for dp, dns, fns in os.walk(base):
            for n in dns + fns:
                p = os.path.join(dp, n)
                if os.path.islink(p):
                    add("ERROR", name, "symlink", os.path.relpath(p, root))
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
        desc = fm.get("description", "")
        if not desc:
            add("ERROR", name, "fm-desc", "description absent or empty")
        elif len(desc) > 1024:
            add("ERROR", name, "fm-desc", "description is %d chars (max 1024)" % len(desc))
        if desc and not TRIGGER_RE.search(desc):
            add("WARN", name, "desc-trigger",
                "description has no 'use when'/'use for'/'triggers'")
        # links
        seen = set()
        for m in LINK_RE.finditer(text):
            tok = m.group(0).rstrip(".:")
            if any(c in tok for c in SKIP_CHARS) or tok in seen:
                continue
            seen.add(tok)
            if not os.path.exists(os.path.join(base, tok)):
                add("ERROR", name, "link-broken", tok)
        # orphan refs
        refdir = os.path.join(base, "references")
        if os.path.isdir(refdir):
            for dp, _, fns in os.walk(refdir):
                for fn in sorted(fns):
                    if fn not in text:
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
