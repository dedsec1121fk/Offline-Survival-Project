#!/usr/bin/env python3
"""Strict bilingual narrative-quality gate and curation tool.

This tool rejects mass-generated prose rather than merely detecting byte-identical files.
It treats English/Greek records as one translation pair during cleanup: if a narrative
field/item is rejected in either language, the corresponding item is removed from both.
That prevents quality cleanup from creating translation drift.

Expected repetition such as source URLs, taxonomy values, record IDs and short material
names is intentionally outside the narrative gate. The gate focuses on user-facing prose.
"""
from __future__ import annotations

import argparse
import collections
import json
import math
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[1]
LANG_DIRS = ("English", "Ελληνικά")
NARRATIVE_FIELDS = (
    "summary", "content", "materials", "steps", "warnings", "common_mistakes",
    "alternatives", "failure_signs", "when_not_to_use", "short_term", "long_term",
    "if_method_fails", "environment_notes",
)
SCALAR_FIELDS = {"summary", "content", "short_term", "long_term", "if_method_fails", "environment_notes"}
LIST_FIELDS = set(NARRATIVE_FIELDS) - SCALAR_FIELDS
INTERNAL_TAG_RE = re.compile(r"(?:^|[-_ ])pass\d+(?:[-_ ][\w-]+)*$|^pass\d+", re.I)
QUOTED_RE = re.compile(r"[“\"«][^”\"»]{2,260}[”\"»]")
NUMBER_RE = re.compile(r"\b\d+(?:[.,]\d+)?\b")
URL_RE = re.compile(r"https?://\S+", re.I)
WORD_RE = re.compile(r"[\wΆ-ώ]+", re.UNICODE)

# User-facing generated-writing signatures discovered in earlier project passes.
# They remain as an explicit regression list in addition to the generic shingle detector.
KNOWN_MARKERS = {
    "English": (
        "apply this boundary to ", "practical guidance for ", "this is the opening check for ",
        "record-specific context:", "apply it specifically within ",
        "treat this as a specific boundary while managing ", "this note applies specifically to ",
        "while carrying out ", "complete one verified cycle for ",
        "recheck this point before closing ", "treat any uncertainty here as an unresolved item ",
        "include the outcome of ", "use a dated paper note and spoken read-back for ",
        "a second person should be able to verify this part of ",
        "is designed for conditions where normal services, internet, transport, or outside help may be delayed",
        "keep the routine visible, assign one calm recorder, protect vulnerable people first",
        "a complete offline workflow for ",
        "trying to solve {title} alone instead of using a small visible team",
        "for the first hours, use {title} to stabilize decisions",
        "for longer disruption, turn {title} into a daily checklist",
        "if {title} fails, stop the routine, isolate the hazard if safe",
        "adapt {title} to apartment blocks, villages, islands",
        "do not let {title} delay evacuation, medical care",
        "assign one calm person to lead {title}",
        "for a reduced version of ",
        "close the routine by marking what is safe, what is unsafe",
    ),
    "Ελληνικά": (
        "εφάρμοσε αυτό το όριο στο θέμα ", "συγκεκριμένο πλαίσιο εγγραφής:",
        "εφάρμοσέ το ειδικά στη διαδικασία ", "το συγκεκριμένο όριο ισχύει κατά τη διαχείριση ",
        "η σημείωση αυτή αφορά ειδικά το θέμα ",
        "ένα δεύτερο άτομο πρέπει να μπορεί να επαληθεύσει αυτό το μέρος του θέματος ",
        "αυτός είναι ο αρχικός έλεγχος για το θέμα ",
        "ολοκλήρωσε έναν επαληθευμένο κύκλο για το θέμα ",
        "ανασκόπησε το θέμα ",
        "προσάρμοσε την καθοδήγηση του θέματος ",
        "πλήρης offline ροή εργασίας για το θέμα ",
        "προσπάθεια να λυθεί το θέμα ",
        "τις πρώτες ώρες χρησιμοποίησε το θέμα ",
        "σε μεγαλύτερη διακοπή μετέτρεψε το θέμα ",
        "αν αποτύχει το θέμα ",
        "για περιορισμένη εκδοχή του θέματος ",
        "αυτή η προχωρημένη διαδικασία προσθέτει βαθύτερο λειτουργικό επίπεδο χωρίς να αντικαθιστά τη βασική κάρτα",
        "μην αφήσεις το θέμα ",
    ),
}

# Generic similarity detector. A long item is considered templated when most of its 4-word
# shingles recur in several other values in the same field. Four-word shingles keep normal
# domain vocabulary from being mistaken for a template while still detecting sentence frames.
SHINGLE_SIZE = 4
SHINGLE_MIN_DOCUMENTS = 5
SHINGLE_RATIO_THRESHOLD = 0.58
SHINGLE_MIN_COUNT = 7
NORMALIZED_DUP_MIN_CHARS = 45
SENTENCE_DUP_MIN_CHARS = 70
SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+")
EDITORIAL_PREFIXES = {
    "English": ("Continuing after this warning appears: ",),
    "Ελληνικά": ("Συνέχιση μετά την εμφάνιση αυτής της προειδοποίησης: ",),
}


@dataclass
class RecordRef:
    lang: str
    path: Path
    document: Any
    records: list[dict[str, Any]]
    index: int
    record: dict[str, Any]


@dataclass
class Unit:
    lang: str
    field: str
    rid: str
    title: str
    category: str
    subcategory: str
    index: int | None
    text: str
    normalized: str
    shingles: tuple[str, ...]


def record_lists(document: Any) -> list[dict[str, Any]]:
    if isinstance(document, list):
        return document if all(isinstance(r, dict) for r in document) else [r for r in document if isinstance(r, dict)]
    if isinstance(document, dict):
        for key in ("records", "items", "entries"):
            value = document.get(key)
            if isinstance(value, list):
                return value if all(isinstance(r, dict) for r in value) else [r for r in value if isinstance(r, dict)]
        for value in document.values():
            if isinstance(value, list) and value and isinstance(value[0], dict):
                return value
    return []


def load_refs(lang: str) -> list[RecordRef]:
    refs: list[RecordRef] = []
    for path in sorted((ROOT / lang).rglob("*.json")):
        try:
            doc = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError):
            continue
        records = record_lists(doc)
        for i, record in enumerate(records):
            refs.append(RecordRef(lang, path, doc, records, i, record))
    return refs


def normalize(text: str, record: dict[str, Any]) -> str:
    value = text.strip().casefold()
    # Replace record-specific labels before quotes so translated title/category insertions do
    # not disguise a shared sentence frame.
    for key in ("title", "category", "subcategory"):
        raw = str(record.get(key, "")).strip().casefold()
        if len(raw) >= 4:
            value = value.replace(raw, "{" + key + "}")
    value = QUOTED_RE.sub("{quoted}", value)
    value = URL_RE.sub("{url}", value)
    value = NUMBER_RE.sub("{n}", value)
    value = re.sub(r"\s+", " ", value).strip()
    return value


def shingle_tokens(normalized: str) -> tuple[str, ...]:
    words = WORD_RE.findall(normalized)
    if len(words) < SHINGLE_SIZE:
        return ()
    return tuple(" ".join(words[i:i + SHINGLE_SIZE]) for i in range(len(words) - SHINGLE_SIZE + 1))


def extract_units(refs: Iterable[RecordRef]) -> list[Unit]:
    units: list[Unit] = []
    for ref in refs:
        r = ref.record
        rid = str(r.get("id", "")).strip()
        title = str(r.get("title", "")).strip()
        for field in NARRATIVE_FIELDS:
            value = r.get(field)
            if isinstance(value, str) and value.strip():
                n = normalize(value, r)
                units.append(Unit(ref.lang, field, rid, title, str(r.get("category", "")), str(r.get("subcategory", "")), None, value.strip(), n, shingle_tokens(n)))
            elif isinstance(value, list):
                for idx, item in enumerate(value):
                    if isinstance(item, str) and item.strip():
                        n = normalize(item, r)
                        units.append(Unit(ref.lang, field, rid, title, str(r.get("category", "")), str(r.get("subcategory", "")), idx, item.strip(), n, shingle_tokens(n)))
    return units



def split_sentences(text: str) -> list[str]:
    return [part.strip() for part in SENTENCE_SPLIT_RE.split(text.strip()) if part.strip()]


def strip_editorial_prefixes(text: str, lang: str) -> str:
    value = text.strip()
    for prefix in EDITORIAL_PREFIXES.get(lang, ()):
        if value.startswith(prefix):
            value = value[len(prefix):].lstrip()
    return value


def sentence_duplicate_groups(refs: list[RecordRef]) -> list[tuple[int, str, str]]:
    counts: collections.Counter[str] = collections.Counter()
    examples: dict[str, str] = {}
    for ref in refs:
        for field in NARRATIVE_FIELDS:
            value = ref.record.get(field)
            vals = value if isinstance(value, list) else [value] if isinstance(value, str) else []
            for item in vals:
                if not isinstance(item, str):
                    continue
                item = strip_editorial_prefixes(item, ref.lang)
                for sentence in split_sentences(item):
                    normalized = normalize(sentence, ref.record)
                    if len(normalized) >= SENTENCE_DUP_MIN_CHARS:
                        counts[normalized] += 1
                        examples.setdefault(normalized, sentence)
    rows = [(count, normalized, examples[normalized]) for normalized, count in counts.items() if count > 1]
    rows.sort(key=lambda row: (-row[0], row[1]))
    return rows


def remove_repeated_sentences_paired(en: dict[str, RecordRef], el: dict[str, RecordRef], changed_paths: set[Path], stats: collections.Counter[str]) -> None:
    seen_en: set[str] = set()
    seen_el: set[str] = set()
    for rid in sorted(set(en) & set(el)):
        a, b = en[rid], el[rid]
        for field in NARRATIVE_FIELDS:
            va, vb = a.record.get(field), b.record.get(field)
            if isinstance(va, str) and isinstance(vb, str):
                left = split_sentences(strip_editorial_prefixes(va, "English"))
                right = split_sentences(strip_editorial_prefixes(vb, "Ελληνικά"))
                if len(left) != len(right):
                    # Rare translation punctuation mismatch: preserve the pair unless the full field
                    # is handled by the broader unit-level template detector.
                    continue
                out_l: list[str] = []
                out_r: list[str] = []
                for ls, rs in zip(left, right):
                    nl, nr = normalize(ls, a.record), normalize(rs, b.record)
                    duplicate = ((len(nl) >= SENTENCE_DUP_MIN_CHARS and nl in seen_en) or
                                 (len(nr) >= SENTENCE_DUP_MIN_CHARS and nr in seen_el))
                    if duplicate:
                        stats["paired_repeated_sentences_removed"] += 1
                        continue
                    out_l.append(ls); out_r.append(rs)
                    if len(nl) >= SENTENCE_DUP_MIN_CHARS: seen_en.add(nl)
                    if len(nr) >= SENTENCE_DUP_MIN_CHARS: seen_el.add(nr)
                new_l, new_r = " ".join(out_l).strip(), " ".join(out_r).strip()
                if new_l != va.strip() or new_r != vb.strip():
                    if new_l and new_r:
                        a.record[field] = new_l; b.record[field] = new_r
                    else:
                        a.record.pop(field, None); b.record.pop(field, None)
                    changed_paths.update((a.path, b.path))
            elif isinstance(va, list) and isinstance(vb, list):
                new_la: list[str] = []
                new_lb: list[str] = []
                for xa, xb in zip(va, vb):
                    if not isinstance(xa, str) or not isinstance(xb, str):
                        continue
                    left = split_sentences(strip_editorial_prefixes(xa, "English"))
                    right = split_sentences(strip_editorial_prefixes(xb, "Ελληνικά"))
                    if len(left) != len(right):
                        # If a mismatched item itself contains a known editorial prefix, keep its
                        # unique warning but remove only the prefix; otherwise leave it intact.
                        clean_a = strip_editorial_prefixes(xa, "English")
                        clean_b = strip_editorial_prefixes(xb, "Ελληνικά")
                        new_la.append(clean_a); new_lb.append(clean_b)
                        if clean_a != xa.strip() or clean_b != xb.strip():
                            stats["editorial_prefixes_removed"] += 1
                            changed_paths.update((a.path, b.path))
                        continue
                    out_l: list[str] = []
                    out_r: list[str] = []
                    for ls, rs in zip(left, right):
                        nl, nr = normalize(ls, a.record), normalize(rs, b.record)
                        duplicate = ((len(nl) >= SENTENCE_DUP_MIN_CHARS and nl in seen_en) or
                                     (len(nr) >= SENTENCE_DUP_MIN_CHARS and nr in seen_el))
                        if duplicate:
                            stats["paired_repeated_sentences_removed"] += 1
                            continue
                        out_l.append(ls); out_r.append(rs)
                        if len(nl) >= SENTENCE_DUP_MIN_CHARS: seen_en.add(nl)
                        if len(nr) >= SENTENCE_DUP_MIN_CHARS: seen_el.add(nr)
                    clean_a, clean_b = " ".join(out_l).strip(), " ".join(out_r).strip()
                    if clean_a and clean_b:
                        new_la.append(clean_a); new_lb.append(clean_b)
                    else:
                        stats["paired_empty_items_removed"] += 1
                if new_la != va or new_lb != vb:
                    if new_la and new_lb:
                        a.record[field] = new_la; b.record[field] = new_lb
                    else:
                        a.record.pop(field, None); b.record.pop(field, None)
                    changed_paths.update((a.path, b.path))


def build_flags(refs: list[RecordRef]) -> tuple[set[tuple[str, str, int | None]], dict[str, Any]]:
    units = extract_units(refs)
    normalized_counts: dict[str, collections.Counter[str]] = {f: collections.Counter() for f in NARRATIVE_FIELDS}
    shingle_df: dict[str, collections.Counter[str]] = {f: collections.Counter() for f in NARRATIVE_FIELDS}
    for u in units:
        if len(u.normalized) >= NORMALIZED_DUP_MIN_CHARS:
            normalized_counts[u.field][u.normalized] += 1
        shingle_df[u.field].update(set(u.shingles))

    flags: set[tuple[str, str, int | None]] = set()
    reasons = collections.Counter()
    examples: dict[str, list[dict[str, Any]]] = collections.defaultdict(list)
    markers = KNOWN_MARKERS[refs[0].lang] if refs else ()

    for u in units:
        key = (u.rid, u.field, u.index)
        reason = None
        if any(marker.casefold() in u.normalized for marker in markers):
            reason = "known_template_signature"
        elif len(u.normalized) >= NORMALIZED_DUP_MIN_CHARS and normalized_counts[u.field][u.normalized] > 1:
            reason = "normalized_duplicate"
        elif len(u.shingles) >= SHINGLE_MIN_COUNT:
            recurring = sum(1 for s in u.shingles if shingle_df[u.field][s] >= SHINGLE_MIN_DOCUMENTS)
            ratio = recurring / len(u.shingles)
            if recurring >= SHINGLE_MIN_COUNT and ratio >= SHINGLE_RATIO_THRESHOLD:
                reason = "shared_sentence_frame"
        if reason:
            flags.add(key)
            reasons[reason] += 1
            if len(examples[reason]) < 6:
                examples[reason].append({"id": u.rid, "field": u.field, "text": u.text[:220]})

    return flags, {
        "units": len(units),
        "flagged_units": len(flags),
        "reasons": dict(reasons),
        "examples": dict(examples),
    }


def narrative_stats(record: dict[str, Any]) -> tuple[int, int]:
    units = 0
    chars = 0
    for field in NARRATIVE_FIELDS:
        value = record.get(field)
        vals = value if isinstance(value, list) else [value] if isinstance(value, str) else []
        for text in vals:
            if isinstance(text, str) and text.strip():
                units += 1
                chars += len(text.strip())
    return units, chars


def pair_maps() -> tuple[dict[str, RecordRef], dict[str, RecordRef], dict[Path, tuple[Any, list[dict[str, Any]]]]]:
    en_refs = load_refs("English")
    el_refs = load_refs("Ελληνικά")
    en = {str(x.record.get("id", "")): x for x in en_refs if str(x.record.get("id", ""))}
    el = {str(x.record.get("id", "")): x for x in el_refs if str(x.record.get("id", ""))}
    docs: dict[Path, tuple[Any, list[dict[str, Any]]]] = {}
    for ref in en_refs + el_refs:
        docs[ref.path] = (ref.document, ref.records)
    return en, el, docs


def clean_pairs(apply: bool) -> dict[str, Any]:
    en_refs = load_refs("English")
    el_refs = load_refs("Ελληνικά")
    en = {str(x.record.get("id", "")): x for x in en_refs if str(x.record.get("id", ""))}
    el = {str(x.record.get("id", "")): x for x in el_refs if str(x.record.get("id", ""))}
    paired_ids = sorted(set(en) & set(el))
    stats = collections.Counter()
    changed_paths: set[Path] = set()
    remove_ids: set[str] = set()
    remove_repeated_sentences_paired(en, el, changed_paths, stats)
    en_flags, en_report = build_flags(en_refs)
    el_flags, el_report = build_flags(el_refs)

    for rid in paired_ids:
        a, b = en[rid], el[rid]
        ra, rb = a.record, b.record

        # Generation tags are internal implementation residue, not reader content.
        for record, ref in ((ra, a), (rb, b)):
            tags = record.get("tags")
            if isinstance(tags, list):
                new_tags = [t for t in tags if isinstance(t, str) and t.strip() and not INTERNAL_TAG_RE.search(t.strip()) and not re.search(r"\bpass\d+\b", t, re.I)]
                if new_tags != tags:
                    record["tags"] = new_tags
                    stats["internal_tags_removed"] += len(tags) - len(new_tags)
                    changed_paths.add(ref.path)

        # Keep user-facing enum metadata translated in Greek.
        translations = {
            "high": "υψηλή", "medium": "μεσαία", "low": "χαμηλή",
            "advanced": "προχωρημένο", "basic": "βασικό", "intermediate": "μεσαίο",
            "moderate_to_advanced": "μεσαίο έως προχωρημένο",
            "basic_to_intermediate": "βασικό έως μεσαίο",
            "preparedness_to_response": "προετοιμασία έως απόκριση",
            "preparedness_to_immediate": "προετοιμασία έως άμεση δράση",
        }
        for field in ("difficulty", "urgency", "priority"):
            cur = rb.get(field)
            if isinstance(cur, str) and cur in translations:
                rb[field] = translations[cur]
                stats["metadata_translated"] += 1
                changed_paths.add(b.path)

        for field in NARRATIVE_FIELDS:
            va, vb = ra.get(field), rb.get(field)
            if field in SCALAR_FIELDS:
                # Full translation parity: keep the field only when both translations have it
                # and neither side is classified as repeated/template-generated.
                keep = (
                    isinstance(va, str) and va.strip() and isinstance(vb, str) and vb.strip()
                    and (rid, field, None) not in en_flags
                    and (rid, field, None) not in el_flags
                )
                if not keep:
                    if field in ra:
                        ra.pop(field, None); changed_paths.add(a.path); stats["paired_scalar_fields_removed"] += 1
                    if field in rb:
                        rb.pop(field, None); changed_paths.add(b.path)
            else:
                la = va if isinstance(va, list) else []
                lb = vb if isinstance(vb, list) else []
                out_a: list[str] = []
                out_b: list[str] = []
                seen_a: set[str] = set()
                seen_b: set[str] = set()
                for idx in range(min(len(la), len(lb))):
                    xa, xb = la[idx], lb[idx]
                    if not isinstance(xa, str) or not xa.strip() or not isinstance(xb, str) or not xb.strip():
                        continue
                    if (rid, field, idx) in en_flags or (rid, field, idx) in el_flags:
                        stats["paired_list_items_removed"] += 1
                        continue
                    na, nb = normalize(xa, ra), normalize(xb, rb)
                    # Within-record repetition is removed symmetrically.
                    if na in seen_a or nb in seen_b:
                        stats["within_record_duplicates_removed"] += 1
                        continue
                    seen_a.add(na); seen_b.add(nb)
                    out_a.append(xa.strip()); out_b.append(xb.strip())
                if out_a and out_b:
                    if out_a != la:
                        ra[field] = out_a; changed_paths.add(a.path)
                    if out_b != lb:
                        rb[field] = out_b; changed_paths.add(b.path)
                else:
                    if field in ra:
                        ra.pop(field, None); changed_paths.add(a.path)
                    if field in rb:
                        rb.pop(field, None); changed_paths.add(b.path)

        # Avoid summary/content saying the same thing within a record.
        if isinstance(ra.get("summary"), str) and isinstance(ra.get("content"), str):
            if normalize(ra["summary"], ra) == normalize(ra["content"], ra):
                ra.pop("content", None); rb.pop("content", None)
                stats["within_record_summary_content_duplicates_removed"] += 1
                changed_paths.update((a.path, b.path))

        ua, ca = narrative_stats(ra)
        ub, cb = narrative_stats(rb)
        # A record must still contain meaningful, actionable bilingual material after curation.
        # Tiny title-only or one-line generated remnants are removed as a pair rather than kept
        # merely to inflate the record count.
        if ua == 0 or ub == 0 or ca < 90 or cb < 90:
            remove_ids.add(rid)

    if remove_ids:
        for ref in en_refs + el_refs:
            before = len(ref.records)
            # Each ref points at a shared per-file list; mutate it only once per file below.
        by_path: dict[Path, tuple[Any, list[dict[str, Any]]]] = {}
        for ref in en_refs + el_refs:
            by_path[ref.path] = (ref.document, ref.records)
        for path, (doc, records) in by_path.items():
            before = len(records)
            records[:] = [r for r in records if str(r.get("id", "")) not in remove_ids]
            if len(records) != before:
                changed_paths.add(path)
        stats["record_pairs_removed"] = len(remove_ids)

    if apply:
        # Write each changed document once. Empty lists are intentionally retained so bilingual
        # path/file parity remains stable and existing bookmarks do not break.
        by_path: dict[Path, Any] = {}
        for ref in en_refs + el_refs:
            by_path[ref.path] = ref.document
        for path in sorted(changed_paths):
            path.write_text(json.dumps(by_path[path], ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    return {
        "english_detection": en_report,
        "greek_detection": el_report,
        "paired_ids_before": len(paired_ids),
        "changed_files": len(changed_paths),
        **dict(stats),
    }


def audit_language(lang: str) -> dict[str, Any]:
    refs = load_refs(lang)
    flags, detector = build_flags(refs)
    exact_narrative = collections.Counter()
    internal_tags = 0
    zero_narrative: list[str] = []
    for ref in refs:
        r = ref.record
        rid = str(r.get("id", ""))
        for tag in r.get("tags", []) if isinstance(r.get("tags"), list) else []:
            if isinstance(tag, str) and (INTERNAL_TAG_RE.search(tag.strip()) or re.search(r"\bpass\d+\b", tag, re.I)):
                internal_tags += 1
        units, chars = narrative_stats(r)
        if units == 0 or chars < 90:
            zero_narrative.append(rid)
        for field in NARRATIVE_FIELDS:
            v = r.get(field)
            vals = v if isinstance(v, list) else [v] if isinstance(v, str) else []
            for text in vals:
                if isinstance(text, str) and len(text.strip()) >= NORMALIZED_DUP_MIN_CHARS:
                    exact_narrative[(field, re.sub(r"\s+", " ", text.strip().casefold()))] += 1
    dup_groups = [(field, count, text[:180]) for (field, text), count in exact_narrative.items() if count > 1]
    dup_groups.sort(key=lambda x: (-x[1], x[0], x[2]))
    sentence_dups = sentence_duplicate_groups(refs)
    return {
        "records": len(refs),
        "detected_template_or_repeated_units": len(flags),
        "detector_reasons": detector["reasons"],
        "exact_substantive_duplicate_groups": len(dup_groups),
        "repeated_substantive_sentence_groups": len(sentence_dups),
        "internal_generation_tags": internal_tags,
        "records_below_minimum_narrative": len(zero_narrative),
        "examples": {
            "detector": detector["examples"],
            "exact_duplicates": dup_groups[:8],
            "sentence_duplicates": [(count, text[:220]) for count, _normalized, text in sentence_dups[:8]],
            "low_content_ids": zero_narrative[:8],
        },
        "pass": not flags and not dup_groups and not sentence_dups and internal_tags == 0 and not zero_narrative,
    }


def audit() -> tuple[bool, dict[str, Any]]:
    en = audit_language("English")
    el = audit_language("Ελληνικά")
    en_ids = {str(x.record.get("id", "")) for x in load_refs("English")}
    el_ids = {str(x.record.get("id", "")) for x in load_refs("Ελληνικά")}
    pair_ok = en_ids == el_ids
    report = {
        "English": en,
        "Ελληνικά": el,
        "translation_id_pairing": {
            "english": len(en_ids), "greek": len(el_ids),
            "missing_in_greek": sorted(en_ids - el_ids)[:20],
            "missing_in_english": sorted(el_ids - en_ids)[:20],
            "pass": pair_ok,
        },
    }
    return bool(en["pass"] and el["pass"] and pair_ok), report


def main() -> int:
    parser = argparse.ArgumentParser(description="Strict bilingual anti-template database quality gate")
    parser.add_argument("--apply", action="store_true", help="Curate repeated/template prose symmetrically across EN/GR records.")
    args = parser.parse_args()
    if args.apply:
        stats = clean_pairs(True)
        print("Cleanup:")
        print(json.dumps(stats, ensure_ascii=False, indent=2))
    ok, report = audit()
    print(json.dumps(report, ensure_ascii=False, indent=2))
    print("[PASS] strict narrative quality" if ok else "[FAIL] strict narrative quality")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
