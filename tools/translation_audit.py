#!/usr/bin/env python3
"""Bilingual completeness audit for Offline Survival Project v7."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GREEK_RE = re.compile(r"[Α-ΩΆΈΉΊΌΎΏα-ωάέήίόύώϊΐϋΰ]")
RAW_ENGLISH_ENUMS = {
    "basic", "beginner", "intermediate", "moderate", "advanced",
    "basic_to_moderate", "basic_to_intermediate", "moderate_to_advanced", "basic_to_advanced",
    "low", "medium", "high", "critical", "urgent", "immediate", "non_immediate", "seasonal",
    "planning", "context_dependent", "varies_by_context", "scenario_dependent",
    "preparedness_to_response", "preparedness_to_immediate",
}


def load_records(root: Path) -> dict[str, dict]:
    out: dict[str, dict] = {}
    for path in sorted(root.rglob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(data, list):
            continue
        for record in data:
            if isinstance(record, dict) and record.get("id"):
                out[str(record["id"])] = record
    return out


def main() -> int:
    issues: list[str] = []
    en = load_records(ROOT / "English")
    el = load_records(ROOT / "Ελληνικά")
    if set(en) != set(el):
        issues.append(f"database ID mismatch: EN={len(en)} EL={len(el)}")

    enum_leaks = []
    greek_text_fail = []
    for record_id, record in el.items():
        for field in ("difficulty", "urgency", "priority"):
            value = record.get(field)
            if isinstance(value, str) and value.casefold() in RAW_ENGLISH_ENUMS:
                enum_leaks.append((record_id, field, value))
        combined = " ".join(str(record.get(field, "")) for field in ("title", "summary", "content"))
        if len(combined) > 80 and len(GREEK_RE.findall(combined)) < 20:
            greek_text_fail.append(record_id)
    if enum_leaks:
        issues.append("untranslated Greek metadata: " + repr(enum_leaks[:20]))
    if greek_text_fail:
        issues.append("Greek records lacking Greek narrative: " + repr(greek_text_fail[:20]))

    # Paired records must expose the same user-visible fields and list cardinalities.
    # This does not pretend to prove literary equivalence, but it catches missing translation
    # sections and asymmetric cleanup immediately.
    paired_fields = (
        "title", "category", "subcategory", "summary", "content", "difficulty", "urgency", "priority",
        "materials", "steps", "warnings", "common_mistakes", "alternatives", "failure_signs",
        "when_not_to_use", "short_term", "long_term", "if_method_fails", "environment_notes",
        "related_topics", "sources", "last_updated",
    )
    field_presence_mismatches = []
    list_length_mismatches = []
    for record_id in sorted(set(en) & set(el)):
        left, right = en[record_id], el[record_id]
        for field in paired_fields:
            lp = field in left and left.get(field) not in (None, "", [])
            rp = field in right and right.get(field) not in (None, "", [])
            if lp != rp:
                field_presence_mismatches.append((record_id, field, lp, rp))
                continue
            if lp and isinstance(left.get(field), list) and isinstance(right.get(field), list):
                if len(left[field]) != len(right[field]):
                    list_length_mismatches.append((record_id, field, len(left[field]), len(right[field])))
    if field_presence_mismatches:
        issues.append("paired database field-presence mismatch: " + repr(field_presence_mismatches[:20]))
    if list_length_mismatches:
        issues.append("paired database list-length mismatch: " + repr(list_length_mismatches[:20]))

    # Any Library collection that has EN/ and GR/ directories must be one-for-one by relative filename.
    library = ROOT / "Offline Library"
    paired_collections = 0
    paired_files = 0
    greek_title_failures: list[str] = []
    untranslated_greek_lines: list[str] = []
    for collection in sorted(p for p in library.iterdir() if p.is_dir()):
        en_dir, gr_dir = collection / "EN", collection / "GR"
        if not (en_dir.is_dir() or gr_dir.is_dir()):
            continue
        paired_collections += 1
        en_files = {p.relative_to(en_dir).as_posix() for p in en_dir.rglob("*") if p.is_file()} if en_dir.is_dir() else set()
        gr_files = {p.relative_to(gr_dir).as_posix() for p in gr_dir.rglob("*") if p.is_file()} if gr_dir.is_dir() else set()
        if en_files != gr_files:
            issues.append(f"Library pair mismatch in {collection.name}: EN-only={sorted(en_files-gr_files)[:10]} GR-only={sorted(gr_files-en_files)[:10]}")
        paired_files += min(len(en_files), len(gr_files))
        if gr_dir.is_dir():
            for rel in sorted(gr_files):
                path = gr_dir / rel
                if path.suffix.casefold() not in {".md", ".txt", ".csv", ".json", ".log"}:
                    continue
                text = path.read_text(encoding="utf-8", errors="replace")
                if len(text) > 100 and len(GREEK_RE.findall(text)) < 20:
                    issues.append(f"Greek Library file lacks translated body: {path.relative_to(ROOT)}")
                if path.suffix.casefold() == ".md":
                    first = next((line.strip() for line in text.splitlines() if line.strip()), "")
                    if first.startswith("#") and not GREEK_RE.search(first):
                        greek_title_failures.append(str(path.relative_to(ROOT)))
                    for line_no, line in enumerate(text.splitlines(), 1):
                        stripped = re.sub(r"[`*_#>|:/()\[\]-]", " ", line)
                        if GREEK_RE.search(stripped):
                            continue
                        english_words = re.findall(r"\b[A-Za-z]{3,}\b", stripped)
                        if len(english_words) >= 3:
                            untranslated_greek_lines.append(f"{path.relative_to(ROOT)}:{line_no}: {line.strip()[:100]}")

    if greek_title_failures:
        issues.append("Greek Library headings left untranslated: " + repr(greek_title_failures[:20]))
    if untranslated_greek_lines:
        issues.append("English-only lines in Greek Library documents: " + repr(untranslated_greek_lines[:20]))

    # Scan Greek UI translation literals for accidental English prose. Product/file-format
    # names and executable identifiers are allowed; ordinary UI wording is not.
    ui_mixed_language: list[str] = []
    allowed_ui_tokens = {
        "json", "gpx", "geojson", "sha", "gps", "kiwix", "serve", "csv", "zim", "kcal",
        "docker", "api", "pin", "termux", "linux", "windows", "android",
    }
    for js_name in ("app.js", "v5.js", "v6.js", "v7.js"):
        js_text = (ROOT / "web" / js_name).read_text(encoding="utf-8")
        for value in re.findall(r"\b\w+:'([^'\\]*(?:\\.[^'\\]*)*)'", js_text):
            if not GREEK_RE.search(value):
                continue
            scrubbed = value.replace("Offline Survival Project", "").replace("Offline Survival", "").replace("Offline Library", "")
            english_words = [w.casefold() for w in re.findall(r"\b[A-Za-z]{3,}\b", scrubbed)]
            unexpected = [w for w in english_words if w not in allowed_ui_tokens]
            if unexpected:
                ui_mixed_language.append(f"{js_name}: {unexpected!r}: {value[:140]}")
    if ui_mixed_language:
        issues.append("mixed English prose in Greek UI translations: " + repr(ui_mixed_language[:20]))

    # Current release documentation must itself be bilingual. Historical versioned files are
    # intentionally excluded because they are immutable release records.
    current_docs = (
        "README.md", "COMMAND_CENTER.md", "SECURITY.md", "UPGRADE_NOTES.md",
        "VALIDATION.md", "V7_OPERATIONS_GUIDE.md", "V7_AUDIT_REPORT.md",
        "Offline Library/README.md",
    )
    current_doc_translation_failures: list[str] = []
    for rel in current_docs:
        path = ROOT / rel
        if not path.is_file():
            current_doc_translation_failures.append(f"missing: {rel}")
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        greek_count = len(GREEK_RE.findall(text))
        if greek_count < 80:
            current_doc_translation_failures.append(f"insufficient Greek coverage: {rel} ({greek_count} Greek chars)")
    if current_doc_translation_failures:
        issues.append("current release documentation translation failures: " + repr(current_doc_translation_failures[:20]))

    # The browser should not expose internal English path/tags in the Greek record modal.
    app = (ROOT / "web" / "app.js").read_text(encoding="utf-8")
    if "[r.category,r._path]" in app:
        issues.append("record modal still exposes internal filesystem path")
    record_order_match = re.search(r"const order=\[([^\]]+)\]", app)
    if record_order_match and "'tags'" in record_order_match.group(1):
        issues.append("record modal still exposes internal/untranslated tag taxonomy")

    print("Offline Survival Project — v7 translation audit")
    print("=" * 72)
    print(f"Database pair: EN {len(en)} / EL {len(el)} records")
    print(f"Paired Library collections: {paired_collections}")
    print(f"Paired Library documents: {paired_files} EN + {paired_files} GR")
    print(f"Untranslated Greek metadata enums: {len(enum_leaks)}")
    print(f"Greek narrative failures: {len(greek_text_fail)}")
    print(f"Paired field-presence mismatches: {len(field_presence_mismatches)}")
    print(f"Paired list-length mismatches: {len(list_length_mismatches)}")
    print(f"Greek Library heading failures: {len(greek_title_failures)}")
    print(f"English-only lines in Greek Library: {len(untranslated_greek_lines)}")
    print(f"Current-document translation failures: {len(current_doc_translation_failures)}")
    print(f"Mixed-language Greek UI values: {len(ui_mixed_language)}")
    if issues:
        print(f"[FAIL] {len(issues)} issue(s)")
        for issue in issues[:100]:
            print(" - " + issue)
        return 2
    print("[PASS] Bilingual structure and user-visible translation checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
