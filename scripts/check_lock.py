#!/usr/bin/env python3
"""Fail when uv.lock drops distribution hashes or the 7-day cooldown."""

import sys
from pathlib import Path

text = Path("uv.lock").read_text()
errors = []
if 'exclude-newer-span = "P7D"' not in text:
    errors.append('uv.lock is missing the 7-day cooldown (exclude-newer-span = "P7D")')

missing = []
for number, line in enumerate(text.splitlines(), 1):
    stripped = line.strip()
    if "url = " in stripped and "hash = " not in stripped:
        missing.append(str(number))
if missing:
    errors.append("uv.lock distributions missing hashes at lines " + ", ".join(missing))

if errors:
    print("\n".join(errors), file=sys.stderr)
    sys.exit(1)
