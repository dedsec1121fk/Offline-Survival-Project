#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import re
from collections import Counter, defaultdict
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.join(BASE_DIR, "Offline Survival Database")
OUT_DIR = os.path.join(BASE_DIR, "Offline Survival Exports")

REQUIRED = [
    "id", "topic_en", "topic_el", "category",
    "summary_en", "summary_el", "content_en", "content_el"
]

IMPORTANT_LIST_FIELDS = [
    "steps_en", "steps_el", "warnings_en", "warnings_el",
    "mistakes_en", "mistakes_el", "materials_en", "materials_el",
    "related_topics", "tags"
]

OPTIONAL_TEXT_FIELDS = [
    "short_term_en", "short_term_el", "long_term_en", "long_term_el",
    "if_method_fails_en", "if_method_fails_el", "environment_notes_en", "environment_notes_el"
]

GREEK_RE = re.compile(r"[Α-Ωα-ωΆ-Ώά-ώ]")


def is_blank(value):
    if value is None:
        return True
    if isinstance(value, str):
        return not value.strip()
    if isinstance(value, list):
        return len(value) == 0
    return False


def norm(value):
    return re.sub(r"\s+", " ", str(value or "").strip().lower())


def word_count(value):
    return len(re.findall(r"\w+", str(value or ""), flags=re.UNICODE))


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    report = []
    all_entries = []
    load_errors = []
    file_counts = {}
    file_sizes = {}
    empty_files = []
    oversized_files = []
    non_json_files = []

    if not os.path.isdir(DB_DIR):
        print("Database folder not found:", DB_DIR)
        return

    for name in sorted(os.listdir(DB_DIR)):
        path = os.path.join(DB_DIR, name)
        if not name.endswith(".json"):
            non_json_files.append(name)
            continue
        size = os.path.getsize(path)
        file_sizes[name] = size
        if size == 0:
            empty_files.append(name)
        if size > 1000000:
            oversized_files.append((name, size))
        try:
            with open(path, "r", encoding="utf-8") as fh:
                data = json.load(fh)
            if isinstance(data, dict):
                data = [data]
            if not isinstance(data, list):
                raise ValueError("Top level must be a list or object.")
            file_counts[name] = len(data)
            for entry in data:
                if isinstance(entry, dict):
                    all_entries.append((name, entry))
                else:
                    load_errors.append(f"{name}: non-object entry found")
        except Exception as exc:
            load_errors.append(f"{name}: {exc}")

    ids = [entry.get("id", "") for _, entry in all_entries]
    topics_en = [norm(entry.get("topic_en", "")) for _, entry in all_entries]
    topics_el = [norm(entry.get("topic_el", "")) for _, entry in all_entries]
    dup_ids = [k for k, v in Counter(ids).items() if k and v > 1]
    dup_topics_en = [k for k, v in Counter(topics_en).items() if k and v > 1]
    dup_topics_el = [k for k, v in Counter(topics_el).items() if k and v > 1]

    missing = []
    weak_lists = []
    weak_content = []
    greek_missing = []
    english_suspect = []
    categories = Counter()
    subcategories = Counter()
    by_file_category = defaultdict(Counter)

    for source, entry in all_entries:
        category = entry.get("category", "uncategorized")
        categories[category] += 1
        subcategories[entry.get("subcategory", "none")] += 1
        by_file_category[source][category] += 1
        eid = entry.get("id", "missing-id")
        for key in REQUIRED:
            if is_blank(entry.get(key)):
                missing.append(f"{source} :: {eid} :: missing {key}")
        for key in IMPORTANT_LIST_FIELDS:
            value = entry.get(key)
            if value is not None and not isinstance(value, list):
                weak_lists.append(f"{source} :: {eid} :: {key} is not a list")
            if isinstance(value, list) and key in ("steps_en", "steps_el", "warnings_en", "warnings_el") and len(value) < 2:
                weak_lists.append(f"{source} :: {eid} :: {key} has fewer than 2 items")
        for key in ("summary_en", "content_en"):
            if word_count(entry.get(key)) < (8 if key.startswith("summary") else 40):
                weak_content.append(f"{source} :: {eid} :: weak {key}")
        for key in ("summary_el", "content_el", "topic_el"):
            val = str(entry.get(key, ""))
            if val and not GREEK_RE.search(val):
                greek_missing.append(f"{source} :: {eid} :: {key} has no Greek characters")
        for key in ("summary_en", "content_en", "topic_en"):
            val = str(entry.get(key, ""))
            if val and GREEK_RE.search(val):
                english_suspect.append(f"{source} :: {eid} :: {key} may contain Greek text")

    report.append("Offline Survival Local Audit")
    report.append("=" * 70)
    report.append(f"Generated: {datetime.now().isoformat(timespec='seconds')}")
    report.append(f"Database folder: {DB_DIR}")
    report.append("")
    report.append(f"JSON files: {len(file_counts)}")
    report.append(f"Entries: {len(all_entries)}")
    report.append(f"Categories: {len(categories)}")
    report.append(f"Subcategories: {len(subcategories)}")
    report.append(f"Load errors: {len(load_errors)}")
    report.append(f"Empty files: {len(empty_files)}")
    report.append(f"Oversized files > 1 MB: {len(oversized_files)}")
    report.append(f"Duplicate IDs: {len(dup_ids)}")
    report.append(f"Duplicate English topics: {len(dup_topics_en)}")
    report.append(f"Duplicate Greek topics: {len(dup_topics_el)}")
    report.append(f"Missing required fields: {len(missing)}")
    report.append(f"Wrong or weak list fields: {len(weak_lists)}")
    report.append(f"Weak content fields: {len(weak_content)}")
    report.append(f"Greek fields without Greek characters: {len(greek_missing)}")
    report.append(f"English fields containing Greek characters: {len(english_suspect)}")
    report.append("")
    report.append("Files")
    report.append("-" * 70)
    for name, count in sorted(file_counts.items()):
        report.append(f"{name}: {count} entries, {file_sizes.get(name, 0)} bytes")
    report.append("")
    report.append("Categories")
    report.append("-" * 70)
    for name, count in categories.most_common():
        report.append(f"{name}: {count}")
    report.append("")
    report.append("File category spread")
    report.append("-" * 70)
    for file_name in sorted(by_file_category):
        parts = [f"{cat}={count}" for cat, count in by_file_category[file_name].most_common()]
        report.append(f"{file_name}: " + ", ".join(parts))

    sections = [
        ("Load errors", load_errors),
        ("Non JSON files in database folder", non_json_files),
        ("Empty files", empty_files),
        ("Oversized files", [f"{n}: {s} bytes" for n, s in oversized_files]),
        ("Duplicate IDs", dup_ids),
        ("Duplicate English topics", dup_topics_en[:200]),
        ("Duplicate Greek topics", dup_topics_el[:200]),
        ("Missing required fields", missing[:300]),
        ("Wrong or weak list fields", weak_lists[:300]),
        ("Weak content fields", weak_content[:300]),
        ("Greek fields without Greek characters", greek_missing[:300]),
        ("English fields containing Greek characters", english_suspect[:300]),
    ]

    for title, items in sections:
        report.append("")
        report.append(title)
        report.append("-" * 70)
        if items:
            report.extend(str(x) for x in items)
        else:
            report.append("None")

    out_path = os.path.join(OUT_DIR, "offline_survival_audit_report.txt")
    text = "\n".join(report) + "\n"
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write(text)

    pass85_path = os.path.join(OUT_DIR, "offline_survival_audit_report_pass85.txt")
    with open(pass85_path, "w", encoding="utf-8") as fh:
        fh.write(text)

    latest_summary = {
        "generated": datetime.now().isoformat(timespec="seconds"),
        "json_files": len(file_counts),
        "entries": len(all_entries),
        "categories": len(categories),
        "load_errors": len(load_errors),
        "empty_files": len(empty_files),
        "duplicate_ids": len(dup_ids),
        "duplicate_topics_en": len(dup_topics_en),
        "duplicate_topics_el": len(dup_topics_el),
        "missing_required": len(missing),
        "weak_content_fields": len(weak_content)
    }
    with open(os.path.join(OUT_DIR, "offline_survival_latest_audit_summary.json"), "w", encoding="utf-8") as fh:
        json.dump(latest_summary, fh, ensure_ascii=False, indent=2)

    print(text)
    print("Saved audit reports:")
    print(out_path)
    print(pass85_path)


if __name__ == "__main__":
    main()
