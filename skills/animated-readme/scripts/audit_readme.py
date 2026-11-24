#!/usr/bin/env python3
"""Audit a README against the animated-readme writing guide. Stdlib only, reads files, no network.

Usage:
    python3 audit_readme.py README.md [--json]

Rules (ERROR fails the run with exit 1, WARN does not):
    em-dash        ERROR  an em-dash outside a code block
    hype-word      ERROR  a word from the writing guide's cut list outside a code block
    alt-missing    ERROR  an image with no alt text
    alt-weak       ERROR  alt text that is generic ("demo", "screenshot") or under 25 characters
    image-missing  ERROR  a local image path that does not exist
    install-first  ERROR  the first section is install or setup, before the project is explained
    no-hero        ERROR  no picture before the first section (badges do not count)
    image-heavy    WARN   a local image over 4 MB
    no-audience    WARN   no "who it is for" or "not for you" statement
"""
import argparse
import json
import re
import sys
from pathlib import Path

HYPE = ('seamless', 'seamlessly', 'effortless', 'effortlessly', 'unlock', 'supercharge', 'revolutionize',
        'leverage', 'empower', 'robust', 'powerful', 'cutting-edge', 'next-generation', 'game-changer',
        'delve', 'elevate', 'streamline')
PHRASES = ("in today's fast-paced world", 'look no further', "it's worth noting")
GENERIC_ALT = {'demo', 'screenshot', 'image', 'gif', 'animation', 'demo gif', 'banner', 'logo', 'preview'}
MIN_ALT = 25
BUDGET_BYTES = 4 * 1024 * 1024
IMG_MD = re.compile(r'!\[([^\]]*)\]\(([^)\s]+)')
IMG_HTML = re.compile(r'<img\b[^>]*>', re.I)
ATTR = re.compile(r'(\w+)\s*=\s*"([^"]*)"')
H2 = re.compile(r'^##\s+(.*)')
INSTALL_HEAD = re.compile(r'install|getting started|setup|set up', re.I)
AUDIENCE = re.compile(r'who (it|this) is for|who is (it|this) for|not for you|not for\b', re.I)


def prose_lines(text):
    """Yield (line number, line) for lines outside fenced code blocks."""
    fenced = False
    for n, line in enumerate(text.splitlines(), 1):
        if line.lstrip().startswith('```'):
            fenced = not fenced
            continue
        if not fenced:
            yield n, line


def images(lines):
    """Yield (line number, alt, src) for markdown and HTML images in prose."""
    for n, line in lines:
        for m in IMG_MD.finditer(line):
            yield n, m.group(1).strip(), m.group(2)
        for tag in IMG_HTML.findall(line):
            attrs = dict(ATTR.findall(tag))
            yield n, attrs.get('alt', '').strip(), attrs.get('src', '')


def is_badge(src):
    return 'shields.io' in src or 'badge' in src.lower()


def find(rule, severity, line, message):
    return {'rule': rule, 'severity': severity, 'line': line, 'message': message}


def style_findings(lines):
    out = []
    for n, line in lines:
        if '—' in line:
            out.append(find('em-dash', 'ERROR', n, 'em-dash: use a comma, a colon or a full stop'))
        low = line.lower()
        for word in HYPE:
            if re.search(r'\b' + re.escape(word) + r'\b', low):
                out.append(find('hype-word', 'ERROR', n, f'cut the word "{word}"'))
        for phrase in PHRASES:
            if phrase in low:
                out.append(find('hype-word', 'ERROR', n, f'cut the phrase "{phrase}"'))
    return out


def image_findings(lines, base):
    out = []
    for n, alt, src in images(lines):
        if is_badge(src):
            continue
        if not alt:
            out.append(find('alt-missing', 'ERROR', n, f'{src} has no alt text'))
        elif alt.lower() in GENERIC_ALT or len(alt) < MIN_ALT:
            out.append(find('alt-weak', 'ERROR', n, f'alt text "{alt}" does not say what the image shows'))
        if src.startswith(('http://', 'https://', 'data:')):
            continue
        path = base / src.split('#')[0].split('?')[0]
        if not path.is_file():
            out.append(find('image-missing', 'ERROR', n, f'{src} does not exist'))
        elif path.stat().st_size > BUDGET_BYTES:
            out.append(find('image-heavy', 'WARN', n, f'{src} is over 4 MB'))
    return out


def first_section(lines):
    """Return (line number, heading text) of the first H2, or (None, '')."""
    for n, line in lines:
        m = H2.match(line)
        if m:
            return n, m.group(1)
    return None, ''


def structure_findings(lines):
    out = []
    first_h2, heading = first_section(lines)
    if first_h2 is not None and INSTALL_HEAD.search(heading):
        out.append(find('install-first', 'ERROR', first_h2, 'the first section is install: explain the project first'))
    if not any(not is_badge(src) and (first_h2 is None or n < first_h2) for n, _, src in images(lines)):
        out.append(find('no-hero', 'ERROR', first_h2 or 1, 'no picture before the first section'))
    if not any(AUDIENCE.search(line) for _, line in lines):
        out.append(find('no-audience', 'WARN', 1, 'say who it is for and who it is not for'))
    return out


def audit(text, base):
    lines = list(prose_lines(text))
    found = style_findings(lines) + image_findings(lines, base) + structure_findings(lines)
    return sorted(found, key=lambda f: (f['line'], f['rule']))


def main(argv=None):
    ap = argparse.ArgumentParser(description='Audit a README against the animated-readme writing guide.')
    ap.add_argument('readme', help='path to the README to audit')
    ap.add_argument('--json', action='store_true', help='print the findings as JSON')
    args = ap.parse_args(argv)
    path = Path(args.readme)
    findings = audit(path.read_text(encoding='utf-8'), path.resolve().parent)
    errors = sum(f['severity'] == 'ERROR' for f in findings)
    if args.json:
        print(json.dumps({'file': str(path), 'errors': errors, 'findings': findings}, indent=2))
    else:
        for f in findings:
            print(f"{path}:{f['line']}: {f['severity']} {f['rule']}: {f['message']}")
        print(f'{errors} error(s), {len(findings) - errors} warning(s)')
    return 1 if errors else 0


if __name__ == '__main__':
    sys.exit(main())
