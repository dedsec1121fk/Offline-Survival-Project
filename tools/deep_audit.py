#!/usr/bin/env python3
# MAINTENANCE: Audit active source/config/docs line-by-line and keep the source list synchronized with shipped files.
"""Deep static/content audit for Offline Survival Project.

This is intentionally standard-library only. It complements --self-test by
scanning active source/config/current-documentation files line-by-line and validating project-wide JSON and
Offline Library duplicate content.
"""
from __future__ import annotations

import ast
import hashlib
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE_FILES = [
    ROOT / "Offline Survival.py",
    ROOT / "Offline Survival Web.py",
    ROOT / "tools" / "self_test.py",
    ROOT / "tools" / "api_smoke_test.py",
    ROOT / "tools" / "content_quality.py",
    ROOT / "tools" / "translation_audit.py",
    ROOT / "tools" / "library_quality.py",
    ROOT / "tools" / "ui_logic_test.js",
    ROOT / "tools" / "phone_browser_assets_test.py",
    ROOT / "tools" / "standalone_reader_test.py",
    ROOT / "tools" / "build_standalone_reader.py",
    Path(__file__),
    ROOT / "web" / "index.html",
    ROOT / "web" / "styles.css",
    ROOT / "web" / "app.js",
    ROOT / "web" / "field-operations.js",
    ROOT / "web" / "continuity-operations.js",
    ROOT / "web" / "knowledge-atlas.js",
    ROOT / "web" / "phone-test.html",
    ROOT / "web" / "phone-test.js",
    ROOT / "web" / "sw.js",
    ROOT / "web" / "manifest.webmanifest",
    ROOT / "MAINTENANCE.json",
    ROOT / "README.md",
    ROOT / "COMMAND_CENTER.md",
    ROOT / "SECURITY.md",
    ROOT / "THIRD_PARTY_NOTICES.md",
    ROOT / "Offline Library" / "README.md",
]
MARKER_RE = re.compile(r"\b(?:TODO|FIXME|HACK|XXX)\b", re.I)
REMOTE_RE = re.compile(r"https?://[^\s'\"<>]+", re.I)
DANGEROUS = {
    "python-eval": re.compile(r"\beval\s*\("),
    "python-exec": re.compile(r"\bexec\s*\("),
    "shell-true": re.compile(r"shell\s*=\s*True"),
    "js-eval": re.compile(r"\beval\s*\("),
    "js-new-function": re.compile(r"\bnew\s+Function\s*\("),
}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    issues: list[str] = []
    stats: list[tuple[str, int, int]] = []

    for path in SOURCE_FILES:
        rel = path.relative_to(ROOT)
        if not path.is_file():
            issues.append(f"missing source: {rel}")
            continue
        raw = path.read_bytes()
        if b"\x00" in raw:
            issues.append(f"NUL byte: {rel}")
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError as error:
            issues.append(f"invalid UTF-8: {rel}: {error}")
            continue
        lines = text.splitlines()
        stats.append((str(rel), len(lines), len(raw)))
        for number, line in enumerate(lines, 1):
            if line.rstrip(" \t") != line:
                issues.append(f"trailing whitespace: {rel}:{number}")
            if MARKER_RE.search(line) and path.name != "deep_audit.py":
                issues.append(f"unfinished marker: {rel}:{number}: {line.strip()[:120]}")
        if path.suffix in {".py", ".js"}:
            for label, pattern in DANGEROUS.items():
                for match in pattern.finditer(text):
                    line = text.count("\n", 0, match.start()) + 1
                    # Python source may mention these strings inside the auditor/self-test itself.
                    if path.name in {"self_test.py", "deep_audit.py"}:
                        continue
                    issues.append(f"dangerous pattern {label}: {rel}:{line}")
            for match in REMOTE_RE.finditer(text):
                url = match.group(0).rstrip("),.;")
                if path.name == "api_smoke_test.py":
                    continue  # Intentional hostile-origin test fixture.
                if any(host in url for host in ("127.0.0.1", "localhost", "example.invalid")):
                    continue
                if path.name == "Offline Survival Web.py" and "{display_host}" in url:
                    continue  # Runtime URL built from the explicitly selected local bind host.
                line = text.count("\n", 0, match.start()) + 1
                issues.append(f"unexpected remote URL: {rel}:{line}: {url[:160]}")

    # Python parse validation plus duplicate functions/classes in a single scope.
    for path in [p for p in SOURCE_FILES if p.suffix == ".py" and p.is_file()]:
        rel = path.relative_to(ROOT)
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        except SyntaxError as error:
            issues.append(f"Python syntax: {rel}:{error.lineno}: {error.msg}")
            continue
        names: dict[tuple[str, str], list[int]] = defaultdict(list)
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                names[(type(node).__name__, node.name)].append(node.lineno)
            if isinstance(node, ast.ClassDef):
                for child in node.body:
                    if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        names[(f"method:{node.name}", child.name)].append(child.lineno)
        for (kind, name), lines in names.items():
            if len(lines) > 1:
                issues.append(f"duplicate Python {kind} {name}: {rel}:{','.join(map(str, lines))}")

    # Validate every JSON file in the source tree, including both databases.
    json_files = sorted(ROOT.rglob("*.json"))
    json_ok = 0
    for path in json_files:
        if any(part == "__pycache__" for part in path.parts):
            continue
        try:
            json.loads(path.read_text(encoding="utf-8"))
            json_ok += 1
        except Exception as error:
            issues.append(f"invalid JSON: {path.relative_to(ROOT)}: {error}")

    # Symlinks complicate the local-file trust boundary; none are expected in release payloads.
    symlinks = [p.relative_to(ROOT) for p in ROOT.rglob("*") if p.is_symlink()]
    for rel in symlinks:
        issues.append(f"unexpected symlink: {rel}")

    # Exact duplicate payload audit across the Offline Library.
    library = ROOT / "Offline Library"
    digest_groups: dict[tuple[int, str], list[str]] = defaultdict(list)
    library_files = []
    if library.is_dir():
        for path in sorted(p for p in library.rglob("*") if p.is_file()):
            library_files.append(path)
            digest_groups[(path.stat().st_size, sha256(path))].append(path.relative_to(library).as_posix())
    duplicates = [paths for paths in digest_groups.values() if len(paths) > 1]
    for paths in duplicates:
        issues.append("duplicate Library payload: " + " | ".join(paths))

    total_lines = sum(lines for _, lines, _ in stats)
    total_bytes = sum(size for _, _, size in stats)
    print("Offline Survival Project — deep audit")
    print("=" * 72)
    for rel, lines, size in stats:
        print(f"[SOURCE] {rel}: {lines} lines, {size} bytes")
    print("=" * 72)
    print(f"Active source/config/docs: {len(stats)} files, {total_lines} lines, {total_bytes} bytes")
    print(f"JSON parsed: {json_ok} files")
    print(f"Offline Library: {len(library_files)} files, {len(duplicates)} exact duplicate groups")
    print(f"Symlinks: {len(symlinks)}")
    if issues:
        print(f"[FAIL] {len(issues)} issue(s)")
        for issue in issues[:200]:
            print(" - " + issue)
        if len(issues) > 200:
            print(f" - ... {len(issues) - 200} more")
        return 2
    print("[PASS] No audit issues detected")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
