#!/usr/bin/env python3
"""Behavior test for scripts/audit_readme.py: run it on READMEs the way a user would.

Usage: python3 tests/test_audit.py   (stdlib only, no browser needed)
"""
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
AUDIT = ROOT / 'scripts' / 'audit_readme.py'

BAD = """# proj

A seamless, powerful framework — built for everyone.

## Installation

```bash
pip install proj
```

![demo](demo.gif)
![](x.png)
"""

GOOD = """# proj

Stop copying numbers between three spreadsheets.

![Animated. A terminal runs proj sync and three spreadsheets collapse into one table.](docs/hero.gif)

## Sound familiar?

- The Monday report takes two hours.

## Who it is for

A good fit if you keep numbers in spreadsheets. Not for you if you need a database.

## Quick start

```bash
pip install proj
```
"""


def audit(text, *extra):
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / 'README.md'
        p.write_text(text, encoding='utf-8')
        (Path(d) / 'docs').mkdir()
        (Path(d) / 'docs' / 'hero.gif').write_bytes(b'GIF89a')
        r = subprocess.run([sys.executable, '-I', str(AUDIT), str(p), *extra],
                           capture_output=True, text=True)
        return r.returncode, r.stdout


def main():
    code, out = audit(BAD)
    assert code == 1, (code, out)
    for rule in ('em-dash', 'hype-word', 'alt-weak', 'alt-missing', 'install-first', 'no-hero', 'no-audience'):
        assert rule in out, (rule, out)
    assert 'seamless' in out and 'powerful' in out, out

    code, out = audit(GOOD)
    assert code == 0, (code, out)
    assert 'ERROR' not in out, out

    code, out = audit(GOOD, '--json')
    assert code == 0 and out.lstrip().startswith('{'), out

    code, out = audit(GOOD.replace('docs/hero.gif', 'docs/gone.gif'))
    assert code == 1 and 'image-missing' in out, (code, out)

    r = subprocess.run([sys.executable, '-I', str(AUDIT), '--help'], capture_output=True, text=True)
    assert r.returncode == 0 and 'usage' in r.stdout.lower(), r
    print('test_audit ok')


if __name__ == '__main__':
    main()
