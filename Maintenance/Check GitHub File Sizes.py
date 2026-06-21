#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fail when a repository file reaches the project's 40 MB safety limit."""

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIMIT_BYTES = 40_000_000
SKIP_DIRS = {".git", "__pycache__"}

oversized = []
largest = []
for current, dirs, files in os.walk(ROOT):
    dirs[:] = [name for name in dirs if name not in SKIP_DIRS]
    for name in files:
        path = os.path.join(current, name)
        size = os.path.getsize(path)
        rel = os.path.relpath(path, ROOT)
        largest.append((size, rel))
        if size >= LIMIT_BYTES:
            oversized.append((size, rel))

largest.sort(reverse=True)
print("Largest project files:")
for size, rel in largest[:10]:
    print(f"  {size:>12,} bytes  {rel}")

if oversized:
    print("\nFiles at or above the 40,000,000-byte limit:")
    for size, rel in sorted(oversized, reverse=True):
        print(f"  {size:>12,} bytes  {rel}")
    raise SystemExit(1)

print("\nPASS: every project file is below 40,000,000 bytes.")
