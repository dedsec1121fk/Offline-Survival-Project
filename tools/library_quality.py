#!/usr/bin/env python3
"""Offline Library anti-duplication/template audit for Offline Survival Project v7.

Standard-library only. The checks are deliberately stricter than exact-file hashing:
- no exact duplicate payloads;
- no repeated substantive paragraphs (80+ normalized characters) within one language;
- no known legacy boilerplate/template phrases;
- no highly similar same-collection Markdown documents (3-word shingle Jaccard >= 0.45).
"""
from __future__ import annotations

import hashlib
import itertools
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LIB = ROOT / "Offline Library"
TEXT_SUFFIXES = {".md", ".txt", ".csv", ".json", ".log"}
LANGS = ("EN", "GR")
BOILERPLATE = (
    "assume the situation begins now and internet/cloud services may be unavailable",
    "what is the first verified information you need",
    "operational field card. adapt it to the incident",
    "printable/offline worksheet. fill only the information",
    "offline survival project field worksheet. fill only what is useful",
    "name one primary owner and one backup owner",
    "record the location of the relevant supplies and paper references",
    "verify the situation before changing the plan",
    "what if the primary person is unavailable",
    "use concise facts. separate verified information from assumptions",
    "επιχειρησιακή κάρτα πεδίου. προσαρμόζεται στο συμβάν",
    "εκτυπώσιμο/offline φύλλο. συμπλήρωσε μόνο πληροφορίες",
    "φύλλο πεδίου του offline survival project. συμπλήρωσε μόνο",
    "τι είναι η πρώτη επιβεβαιωμένη πληροφορία που χρειάζεσαι",
)


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def norm_para(block: str) -> str:
    lines = []
    for line in block.splitlines():
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        lines.append(s)
    text = " ".join(lines)
    text = re.sub(r"[`*_>|]", " ", text)
    text = re.sub(r"\s+", " ", text).strip().casefold()
    return text


def word_shingles(text: str, n: int = 3) -> set[tuple[str, ...]]:
    words = re.findall(r"[^\W_]+", text.casefold(), flags=re.UNICODE)
    return {tuple(words[i:i+n]) for i in range(max(0, len(words)-n+1))}


def main() -> int:
    issues: list[str] = []
    files = [p for p in LIB.rglob("*") if p.is_file() and not p.is_symlink()]

    # Exact payload duplicates across the whole Library.
    groups: dict[tuple[int, str], list[str]] = defaultdict(list)
    for p in files:
        groups[(p.stat().st_size, digest(p))].append(p.relative_to(LIB).as_posix())
    duplicate_payloads = [v for v in groups.values() if len(v) > 1]
    for group in duplicate_payloads:
        issues.append("exact duplicate Library payload: " + " | ".join(group))

    repeated_paragraphs = 0
    boilerplate_hits = 0
    high_similarity = 0

    for lang in LANGS:
        paragraphs: dict[str, list[str]] = defaultdict(list)
        for p in files:
            rel = p.relative_to(LIB).as_posix()
            if f"/{lang}/" not in f"/{rel}":
                continue
            if p.suffix.casefold() not in TEXT_SUFFIXES:
                continue
            text = p.read_text(encoding="utf-8", errors="replace")
            folded = text.casefold()
            for phrase in BOILERPLATE:
                if phrase in folded:
                    boilerplate_hits += 1
                    issues.append(f"legacy boilerplate phrase: {rel}: {phrase[:70]}")
            for block in re.split(r"\n\s*\n", text):
                para = norm_para(block)
                if len(para) >= 80:
                    paragraphs[para].append(rel)
        for para, refs in paragraphs.items():
            if len(refs) > 1:
                repeated_paragraphs += 1
                issues.append(f"repeated substantive paragraph ({len(refs)} docs): {para[:120]} :: {' | '.join(refs[:8])}")

    # Similarity catches files that escaped paragraph checks but still share a generated skeleton.
    for collection in sorted(p for p in LIB.iterdir() if p.is_dir()):
        for lang in LANGS:
            lang_dir = collection / lang
            if not lang_dir.is_dir():
                continue
            docs: list[tuple[Path, set[tuple[str, ...]]]] = []
            for p in sorted(lang_dir.rglob("*.md")):
                sh = word_shingles(p.read_text(encoding="utf-8", errors="replace"))
                if sh:
                    docs.append((p, sh))
            for (a, aa), (b, bb) in itertools.combinations(docs, 2):
                union = aa | bb
                score = len(aa & bb) / len(union) if union else 0.0
                if score >= 0.45:
                    high_similarity += 1
                    issues.append(
                        f"template-like document similarity {score:.3f}: "
                        f"{a.relative_to(LIB)} | {b.relative_to(LIB)}"
                    )

    print("Offline Survival Project — v7 Library quality audit")
    print("=" * 72)
    print(f"Library files checked: {len(files)}")
    print(f"Exact duplicate payload groups: {len(duplicate_payloads)}")
    print(f"Repeated substantive paragraph groups: {repeated_paragraphs}")
    print(f"Legacy boilerplate hits: {boilerplate_hits}")
    print(f"Template-like similarity pairs: {high_similarity}")
    if issues:
        print(f"[FAIL] {len(issues)} issue(s)")
        for issue in issues[:150]:
            print(" - " + issue)
        return 2
    print("[PASS] No duplicate, repeated-boilerplate, or template-like Library content detected")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
