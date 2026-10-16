#!/usr/bin/env python3
"""Pattern census for the README (stdlib only; run with python3 -I).

Walks skills/*/SKILL.md and skills/*/references/*.md and, for each documented mechanism,
prints the count and the sorted list of skills whose files contain the criterion.
A skill matches a mechanism when ANY of its scanned files contains ANY of the mechanism's
phrases. Matching is a literal, case-sensitive substring test; no stemming, no regex.
Usage: pattern-census.py [--json] [--root DIR]
"""
import argparse
import glob
import json
import os
import sys

# Mechanism -> literal, case-sensitive phrase constants (one exact criterion each).
# parallel-execution-protocol (README Pattern B): the phrase below.
# multi-specialist-spawning (Pattern C): UNION rule, a skill counts when it contains at
#   least one of the three phrases (so legal-compliance and sales, which name their
#   synthesizer after the domain, count via "Spawn Specialists" / "Multi-Specialist").
# refuter-panel (Pattern A, 3x Refuter Panel): the phrase below.
# consistency-validator (Pattern A): the phrase below, anywhere in the skill's files; it
#   is a text criterion, so teaching skills that merely mention it also count.
# conflict-resolving-synthesis (Pattern A): the literal "actively resolves" in the
#   synthesis step; skills that word the same idea differently (for example
#   "Actively resolve", capital A, or "Resolve MUST_RESOLVE contradictions") do not count.
MECHANISMS = (
    ("parallel-execution-protocol", ("Parallel Execution Protocol",)),
    ("multi-specialist-spawning",
     ("Cross-Domain Synthesizer", "Spawn Specialists", "Multi-Specialist")),
    ("refuter-panel", ("3 independent Refuter Agents",)),
    ("consistency-validator", ("Consistency Validator",)),
    ("conflict-resolving-synthesis", ("actively resolves",)),
)


def census(root):
    """Return {mechanism: sorted skill names} for the repo at root."""
    files = []
    for pat in ("skills/*/SKILL.md", "skills/*/references/*.md"):
        files.extend(glob.glob(os.path.join(root, pat)))
    hits = dict((m, set()) for m, _ in MECHANISMS)
    for path in sorted(files):
        skill = os.path.relpath(path, os.path.join(root, "skills")).split(os.sep)[0]
        with open(path, encoding="utf-8", errors="replace") as fh:
            text = fh.read()
        for mech, phrases in MECHANISMS:
            if any(p in text for p in phrases):
                hits[mech].add(skill)
    return dict((m, sorted(hits[m])) for m, _ in MECHANISMS)


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    default_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ap.add_argument("--root", default=default_root, help="repo root")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    args = ap.parse_args()
    res = census(os.path.abspath(args.root))
    if args.json:
        print(json.dumps(dict((m, {"count": len(s), "skills": s}) for m, s in res.items()),
                         indent=2))
    else:
        for mech, _ in MECHANISMS:
            print("%s: %d" % (mech, len(res[mech])))
            print("  " + " ".join(res[mech]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
