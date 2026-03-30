#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import textwrap
import difflib
from collections import Counter
from datetime import datetime

APP_NAME = "Offline Survival"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.join(SCRIPT_DIR, "Offline Survival Database")
UPDATES_DIR = os.path.join(SCRIPT_DIR, "Offline Survival Updates")
APP_HOME = os.path.join(os.path.expanduser("~"), "Offline Survival")
EXPORT_DIR = os.path.join(APP_HOME, "Exports")
BOOKMARKS_FILE = os.path.join(APP_HOME, "bookmarks.json")
WRAP_WIDTH = 96
PAGE_BREAK = "=" * WRAP_WIDTH

REQUIRED_FIELDS = [
    "id", "topic", "category", "subcategory", "tags",
    "summary_en", "summary_el", "content_en", "content_el",
    "steps_en", "steps_el", "warnings_en", "warnings_el",
    "mistakes_en", "mistakes_el", "related_topics",
    "difficulty", "urgency", "priority", "last_updated", "update_note"
]

UI = {
    "en": {
        "choose_language": "Choose language / Επιλογή γλώσσας",
        "welcome": "Offline Survival - smarter offline search, reading, and bookmarks",
        "main_menu": "Main menu",
        "menu_items": [
            "1. Search by keyword or phrase",
            "2. Search by tag",
            "3. Search by category",
            "4. Search by topic",
            "5. Browse categories",
            "6. Browse topics",
            "7. Bookmarks",
            "8. Database statistics",
            "9. Read update logs",
            "10. Integrity check",
            "11. Help",
            "0. Exit"
        ],
        "prompt": "Choose an option",
        "invalid": "Invalid choice.",
        "press_enter": "Press Enter to continue...",
        "search": "Enter search text",
        "tag": "Enter tag",
        "category": "Enter category",
        "topic": "Enter topic",
        "no_results": "No matching entries found.",
        "results": "results",
        "pick_result": "Open result number, or press Enter to go back",
        "categories": "Categories",
        "topics": "Topics",
        "bookmarks": "Bookmarks",
        "choose_category": "Choose category number, or Enter to go back",
        "choose_topic": "Choose topic number, or Enter to go back",
        "choose_log": "Choose log number, or Enter to go back",
        "choose_bookmark": "Choose bookmark number, or Enter to go back",
        "update_logs": "Update logs",
        "stats": "Database statistics",
        "integrity": "Integrity check",
        "help": "Help",
        "summary": "Summary",
        "actions": "Actions",
        "warnings": "Warnings",
        "mistakes": "Common mistakes",
        "full": "Full detail",
        "related": "Related topics",
        "snippet": "Search preview",
        "priority": "Priority",
        "urgency": "Urgency",
        "difficulty": "Difficulty",
        "last_updated": "Last updated",
        "update_note": "Update note",
        "tags": "Tags",
        "bookmarked": "Bookmarked",
        "not_bookmarked": "Not bookmarked",
        "bookmark_added": "Bookmark added.",
        "bookmark_removed": "Bookmark removed.",
        "bookmark_empty": "No bookmarks saved yet.",
        "reader_help": "Commands: [n] next result  [p] previous result  [1] overview  [2] full detail  [3] mistakes  [r] related  [m] bookmark toggle  [e] export  [b] back",
        "export_done": "Export created:",
        "export_failed": "Export failed:",
        "group_export": "Export [1] this entry, [2] current results, [3] same category, [Enter] cancel",
        "integrity_ok": "No duplicate IDs or major missing-field issues were found.",
        "empty_db": "Database is missing or empty.",
        "reload_msg": "Database reloaded.",
        "suggestions": "Closest suggestions",
        "help_body": "This improved script keeps the project standard-library only while making search and reading more practical. Search now combines exact phrase ranking, multi-token matching across many fields, tag/category/topic weighting, fuzzy similarity, and preview snippets. Reader mode defaults to a cleaner overview and lets you jump between overview, full detail, mistakes, related topics, export, and bookmarks. Any file the script needs for its own operation is stored in ~/Offline Survival.",
        "exit": "Stay safe. Protect function first, then comfort."
    },
    "el": {
        "choose_language": "Επιλογή γλώσσας / Choose language",
        "welcome": "Offline Survival - πιο έξυπνη offline αναζήτηση, ανάγνωση και σελιδοδείκτες",
        "main_menu": "Κεντρικό μενού",
        "menu_items": [
            "1. Αναζήτηση με λέξη ή φράση",
            "2. Αναζήτηση με ετικέτα",
            "3. Αναζήτηση με κατηγορία",
            "4. Αναζήτηση με θέμα",
            "5. Περιήγηση κατηγοριών",
            "6. Περιήγηση θεμάτων",
            "7. Σελιδοδείκτες",
            "8. Στατιστικά βάσης",
            "9. Ανάγνωση αρχείων ενημέρωσης",
            "10. Έλεγχος ακεραιότητας",
            "11. Βοήθεια",
            "0. Έξοδος"
        ],
        "prompt": "Διάλεξε επιλογή",
        "invalid": "Μη έγκυρη επιλογή.",
        "press_enter": "Πάτησε Enter για συνέχεια...",
        "search": "Δώσε λέξη ή φράση αναζήτησης",
        "tag": "Δώσε ετικέτα",
        "category": "Δώσε κατηγορία",
        "topic": "Δώσε θέμα",
        "no_results": "Δεν βρέθηκαν αποτελέσματα.",
        "results": "αποτελέσματα",
        "pick_result": "Άνοιξε αριθμό αποτελέσματος ή πάτησε Enter για επιστροφή",
        "categories": "Κατηγορίες",
        "topics": "Θέματα",
        "bookmarks": "Σελιδοδείκτες",
        "choose_category": "Διάλεξε αριθμό κατηγορίας ή Enter για επιστροφή",
        "choose_topic": "Διάλεξε αριθμό θέματος ή Enter για επιστροφή",
        "choose_log": "Διάλεξε αριθμό αρχείου ή Enter για επιστροφή",
        "choose_bookmark": "Διάλεξε αριθμό σελιδοδείκτη ή Enter για επιστροφή",
        "update_logs": "Αρχεία ενημερώσεων",
        "stats": "Στατιστικά βάσης",
        "integrity": "Έλεγχος ακεραιότητας",
        "help": "Βοήθεια",
        "summary": "Περίληψη",
        "actions": "Ενέργειες",
        "warnings": "Προειδοποιήσεις",
        "mistakes": "Συχνά λάθη",
        "full": "Πλήρης ανάλυση",
        "related": "Σχετικά θέματα",
        "snippet": "Προεπισκόπηση αναζήτησης",
        "priority": "Προτεραιότητα",
        "urgency": "Επείγον",
        "difficulty": "Δυσκολία",
        "last_updated": "Τελευταία ενημέρωση",
        "update_note": "Σημείωση ενημέρωσης",
        "tags": "Ετικέτες",
        "bookmarked": "Αποθηκευμένο",
        "not_bookmarked": "Χωρίς σελιδοδείκτη",
        "bookmark_added": "Ο σελιδοδείκτης προστέθηκε.",
        "bookmark_removed": "Ο σελιδοδείκτης αφαιρέθηκε.",
        "bookmark_empty": "Δεν υπάρχουν ακόμη αποθηκευμένοι σελιδοδείκτες.",
        "reader_help": "Εντολές: [n] επόμενο αποτέλεσμα  [p] προηγούμενο αποτέλεσμα  [1] overview  [2] πλήρης ανάλυση  [3] λάθη  [r] σχετικά  [m] εναλλαγή σελιδοδείκτη  [e] εξαγωγή  [b] πίσω",
        "export_done": "Η εξαγωγή δημιουργήθηκε:",
        "export_failed": "Η εξαγωγή απέτυχε:",
        "group_export": "Εξαγωγή [1] αυτής της καταχώρησης, [2] τρεχόντων αποτελεσμάτων, [3] ίδιας κατηγορίας, [Enter] ακύρωση",
        "integrity_ok": "Δεν βρέθηκαν διπλά IDs ή σοβαρά προβλήματα ελλιπών πεδίων.",
        "empty_db": "Η βάση λείπει ή είναι άδεια.",
        "reload_msg": "Η βάση επαναφορτώθηκε.",
        "suggestions": "Κοντινές προτάσεις",
        "help_body": "Αυτό το βελτιωμένο script παραμένει μόνο με standard library αλλά κάνει την αναζήτηση και την ανάγνωση πιο πρακτικές. Η αναζήτηση συνδυάζει ακριβή αντιστοίχιση φράσης, πολλαπλά token σε πολλά πεδία, βαρύτητα για ετικέτες/κατηγορίες/θέματα, fuzzy similarity και snippets προεπισκόπησης. Το reader mode ξεκινά με πιο καθαρό overview και σε αφήνει να πηδάς σε πλήρη ανάλυση, λάθη, σχετικά θέματα, εξαγωγή και σελιδοδείκτες. Κάθε αρχείο που χρειάζεται το script για τη λειτουργία του αποθηκεύεται στο ~/Offline Survival.",
        "exit": "Μείνε ασφαλής. Προστάτεψε πρώτα τη λειτουργία και μετά την άνεση."
    }
}


def clear():
    os.system("clear")


def safe_mkdir(path):
    os.makedirs(path, exist_ok=True)


def ensure_runtime_dirs():
    safe_mkdir(APP_HOME)
    safe_mkdir(EXPORT_DIR)
    safe_mkdir(DB_DIR)
    safe_mkdir(UPDATES_DIR)


def normalize(text):
    return " ".join(str(text).lower().split())


def tokenize(text):
    cleaned = []
    for ch in str(text).lower():
        cleaned.append(ch if ch.isalnum() or ch in "-_ " else " ")
    return [tok for tok in "".join(cleaned).split() if tok]


def wrap(text, width=WRAP_WIDTH):
    out = []
    for paragraph in str(text).splitlines():
        if not paragraph.strip():
            out.append("")
        else:
            out.extend(textwrap.fill(paragraph, width=width).splitlines())
    return "\n".join(out)


def pause(lang):
    input("\n" + UI[lang]["press_enter"])


def choose_language():
    while True:
        clear()
        print(PAGE_BREAK)
        print(APP_NAME)
        print(PAGE_BREAK)
        print(UI["en"]["choose_language"])
        print("1. English")
        print("2. Ελληνικά")
        choice = input("> ").strip()
        if choice == "1":
            return "en"
        if choice == "2":
            return "el"


def load_bookmarks():
    ensure_runtime_dirs()
    if not os.path.isfile(BOOKMARKS_FILE):
        return []
    try:
        with open(BOOKMARKS_FILE, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        return data if isinstance(data, list) else []
    except Exception:
        return []


def save_bookmarks(bookmarks):
    ensure_runtime_dirs()
    with open(BOOKMARKS_FILE, "w", encoding="utf-8") as fh:
        json.dump(sorted(set(bookmarks)), fh, ensure_ascii=False, indent=2)


def build_aliases(item):
    aliases = set()
    aliases.update(tokenize(item.get("topic", "")))
    aliases.update(tokenize(item.get("category", "")))
    aliases.update(tokenize(item.get("subcategory", "")))
    for tag in item.get("tags", []) or []:
        aliases.update(tokenize(tag))
    return sorted(aliases)


def load_database():
    entries = []
    if not os.path.isdir(DB_DIR):
        return entries
    for filename in sorted(os.listdir(DB_DIR)):
        if not filename.endswith(".json"):
            continue
        path = os.path.join(DB_DIR, filename)
        try:
            with open(path, "r", encoding="utf-8") as fh:
                data = json.load(fh)
            if isinstance(data, dict):
                data = [data]
            if not isinstance(data, list):
                continue
            for item in data:
                if not isinstance(item, dict):
                    continue
                item["_source_file"] = filename
                item["_aliases"] = build_aliases(item)
                entries.append(item)
        except Exception as exc:
            entries.append({
                "id": f"broken::{filename}",
                "topic": filename,
                "category": "system",
                "subcategory": "load_error",
                "tags": ["load_error"],
                "summary_en": f"Failed to load {filename}: {exc}",
                "summary_el": f"Αποτυχία φόρτωσης του {filename}: {exc}",
                "content_en": "Fix or replace the broken JSON file.",
                "content_el": "Διόρθωσε ή αντικατέστησε το κατεστραμμένο αρχείο JSON.",
                "steps_en": [], "steps_el": [],
                "warnings_en": ["Broken data file."], "warnings_el": ["Κατεστραμμένο αρχείο δεδομένων."],
                "mistakes_en": [], "mistakes_el": [],
                "related_topics": [],
                "difficulty": "low", "urgency": "medium", "priority": "high", "last_updated": "", "update_note": "Auto-generated load error.",
                "_source_file": filename,
                "_aliases": ["load_error"]
            })
    return entries


def list_update_logs():
    if not os.path.isdir(UPDATES_DIR):
        return []
    return sorted([name for name in os.listdir(UPDATES_DIR) if name.lower().endswith(".txt")])


def get_text(item, lang, base):
    val = item.get(f"{base}_{lang}", "")
    return val if not isinstance(val, list) else val


def get_list(item, lang, base):
    val = item.get(f"{base}_{lang}", [])
    return val if isinstance(val, list) else ([val] if val else [])


def search_blob(item):
    parts = [
        item.get("topic", ""), item.get("category", ""), item.get("subcategory", ""),
        " ".join(item.get("tags", []) or []),
        item.get("summary_en", ""), item.get("summary_el", ""),
        item.get("content_en", ""), item.get("content_el", ""),
        " ".join(get_list(item, "en", "steps")), " ".join(get_list(item, "el", "steps")),
        " ".join(get_list(item, "en", "warnings")), " ".join(get_list(item, "el", "warnings")),
        " ".join(get_list(item, "en", "mistakes")), " ".join(get_list(item, "el", "mistakes")),
        " ".join(item.get("_aliases", []))
    ]
    return normalize(" ".join(parts))


def match_snippet(item, query, lang):
    fields = [
        get_text(item, lang, "summary"),
        get_text(item, lang, "content"),
        " ".join(get_list(item, lang, "steps")),
        " ".join(get_list(item, lang, "warnings")),
        " ".join(get_list(item, lang, "mistakes"))
    ]
    q = normalize(query)
    for field in fields:
        lower = normalize(field)
        idx = lower.find(q)
        if idx != -1:
            raw = str(field)
            start = max(0, idx - 70)
            end = min(len(raw), idx + len(query) + 100)
            return raw[start:end].replace("\n", " ").strip()
    return (get_text(item, lang, "summary") or get_text(item, "en", "summary"))[:180]


def find_suggestions(entries, query):
    pool = set()
    for item in entries:
        pool.add(item.get("topic", ""))
        pool.add(item.get("category", ""))
        pool.update(item.get("tags", []) or [])
        pool.update(item.get("_aliases", []) or [])
    pool = [x for x in pool if x]
    return difflib.get_close_matches(query, pool, n=8, cutoff=0.55)


def score_entry(item, query, mode):
    q = normalize(query)
    if not q:
        return 0.0
    topic = normalize(item.get("topic", ""))
    category = normalize(item.get("category", ""))
    subcategory = normalize(item.get("subcategory", ""))
    tags = [normalize(tag) for tag in item.get("tags", []) or []]
    aliases = [normalize(alias) for alias in item.get("_aliases", [])]
    blob = search_blob(item)
    tokens = tokenize(q)
    score = 0.0

    if mode == "topic":
        if q == topic:
            score += 280
        if q in topic:
            score += 170
        for token in tokens:
            if token in topic:
                score += 25
        score += difflib.SequenceMatcher(None, q, topic).ratio() * 80
        return score

    if mode == "category":
        if q == category:
            score += 260
        if q in category or q in subcategory:
            score += 150
        for token in tokens:
            if token in category or token in subcategory:
                score += 20
        score += difflib.SequenceMatcher(None, q, category).ratio() * 65
        return score

    if mode == "tag":
        if q in tags or q in aliases:
            score += 250
        for tag in tags + aliases:
            if q in tag:
                score += 80
            score += difflib.SequenceMatcher(None, q, tag).ratio() * 30
        return score

    # smarter keyword search
    if q == topic:
        score += 320
    if q in topic:
        score += 210
    if q in (normalize(get_text(item, "en", "summary")), normalize(get_text(item, "el", "summary"))):
        score += 120
    if q in blob:
        score += 90
    if q == category or q == subcategory:
        score += 110
    if q in category or q in subcategory:
        score += 70
    if q in tags or q in aliases:
        score += 90

    if tokens:
        token_hits = 0
        for token in tokens:
            if token in topic:
                score += 30
                token_hits += 1
            elif token in category or token in subcategory:
                score += 18
                token_hits += 1
            elif token in tags or token in aliases:
                score += 22
                token_hits += 1
            elif token in blob:
                score += 10
                token_hits += 1
        if token_hits == len(tokens):
            score += 55 + len(tokens) * 6

    score += difflib.SequenceMatcher(None, q, topic).ratio() * 50
    score += difflib.SequenceMatcher(None, q, blob[:1600]).ratio() * 22

    if normalize(item.get("priority", "")) == "high":
        score += 5
    if normalize(item.get("urgency", "")) in {"high", "critical"}:
        score += 5
    return score


def search_entries(entries, query, mode="keyword"):
    ranked = []
    for item in entries:
        score = score_entry(item, query, mode)
        if score >= 25:
            ranked.append((score, item))
    ranked.sort(key=lambda pair: (-pair[0], pair[1].get("topic", "")))
    return ranked


def related_entries(entries, item):
    rel_names = {normalize(name) for name in item.get("related_topics", []) or []}
    return [other for other in entries if other.get("id") != item.get("id") and normalize(other.get("topic", "")) in rel_names]


def detect_latest(entries):
    dates = [str(item.get("last_updated", "")).strip() for item in entries if str(item.get("last_updated", "")).strip()]
    return max(dates) if dates else "n/a"


def stats(entries):
    categories = {item.get("category", "") for item in entries if item.get("category")}
    topics = {item.get("topic", "") for item in entries if item.get("topic")}
    tags = set()
    missing = 0
    urgent = 0
    high_priority = 0
    for item in entries:
        tags.update(item.get("tags", []) or [])
        if any(field not in item or item.get(field) in ("", None) for field in REQUIRED_FIELDS):
            missing += 1
        if normalize(item.get("priority", "")) == "high":
            high_priority += 1
        if normalize(item.get("urgency", "")) in {"high", "critical"}:
            urgent += 1
    file_count = len([x for x in os.listdir(DB_DIR) if x.endswith(".json")]) if os.path.isdir(DB_DIR) else 0
    return file_count, len(entries), len(categories), len(topics), len(tags), len(list_update_logs()), detect_latest(entries), high_priority, urgent, missing


def integrity(entries):
    missing = []
    ids = Counter()
    pairs = Counter()
    for item in entries:
        missing_fields = [f for f in REQUIRED_FIELDS if f not in item or item.get(f) in ("", None)]
        if missing_fields:
            missing.append((item.get("id", "unknown"), missing_fields))
        ids[item.get("id", "")] += 1
        pairs[(normalize(item.get("topic", "")), normalize(item.get("subcategory", "")))] += 1
    dupe_ids = [k for k, v in ids.items() if k and v > 1]
    dupe_pairs = [k for k, v in pairs.items() if k[0] and v > 1]
    return missing, dupe_ids, dupe_pairs


def print_header(title):
    print(PAGE_BREAK)
    print(title)
    print(PAGE_BREAK)


def print_meta(item, lang, bookmarks):
    status = UI[lang]["bookmarked"] if item.get("id") in bookmarks else UI[lang]["not_bookmarked"]
    print(f"Category: {item.get('category', '')}")
    print(f"Subcategory: {item.get('subcategory', '')}")
    print(f"{UI[lang]['tags']}: {', '.join(item.get('tags', []) or [])}")
    print(f"{UI[lang]['priority']}: {item.get('priority', '')} | {UI[lang]['urgency']}: {item.get('urgency', '')} | {UI[lang]['difficulty']}: {item.get('difficulty', '')}")
    print(f"{UI[lang]['last_updated']}: {item.get('last_updated', '')}")
    print(f"{UI[lang]['update_note']}: {item.get('update_note', '')}")
    print(f"{status}")


def render_entry(item, lang, section, bookmarks):
    clear()
    print_header(item.get("topic", ""))
    print_meta(item, lang, bookmarks)
    print()
    if section == "1":
        print(f"[{UI[lang]['summary']}]\n")
        print(wrap(get_text(item, lang, "summary") or get_text(item, "en", "summary")))
        print()
        print(f"[{UI[lang]['actions']}]\n")
        for line in get_list(item, lang, "steps") or get_list(item, "en", "steps"):
            print("- " + wrap(line))
        print()
        print(f"[{UI[lang]['warnings']}]\n")
        for line in get_list(item, lang, "warnings") or get_list(item, "en", "warnings"):
            print("- " + wrap(line))
    elif section == "2":
        print(f"[{UI[lang]['full']}]\n")
        print(wrap(get_text(item, lang, "content") or get_text(item, "en", "content")))
    else:
        print(f"[{UI[lang]['mistakes']}]\n")
        for line in get_list(item, lang, "mistakes") or get_list(item, "en", "mistakes"):
            print("- " + wrap(line))
    print()
    print(f"{UI[lang]['related']}: {', '.join(item.get('related_topics', []) or []) or '-'}")


def export_entries(entries_to_export, lang, label):
    ensure_runtime_dirs()
    safe_name = "".join(ch if ch.isalnum() or ch in ("_", "-", " ") else "_" for ch in label).strip() or "export"
    path = os.path.join(EXPORT_DIR, f"{safe_name}.txt")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(f"{APP_NAME} Export\n")
        fh.write(f"Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        fh.write(f"Language: {'English' if lang == 'en' else 'Greek'}\n")
        fh.write(PAGE_BREAK + "\n\n")
        for num, item in enumerate(entries_to_export, 1):
            fh.write(f"{num}. {item.get('topic', '')}\n")
            fh.write(f"Category: {item.get('category', '')}\n")
            fh.write(f"Tags: {', '.join(item.get('tags', []) or [])}\n")
            fh.write(f"Summary:\n{get_text(item, lang, 'summary') or get_text(item, 'en', 'summary')}\n\n")
            fh.write(f"Actions:\n")
            for line in get_list(item, lang, 'steps') or get_list(item, 'en', 'steps'):
                fh.write(f"- {line}\n")
            fh.write(f"\nWarnings:\n")
            for line in get_list(item, lang, 'warnings') or get_list(item, 'en', 'warnings'):
                fh.write(f"- {line}\n")
            fh.write(f"\nCommon mistakes:\n")
            for line in get_list(item, lang, 'mistakes') or get_list(item, 'en', 'mistakes'):
                fh.write(f"- {line}\n")
            fh.write(f"\nFull detail:\n{get_text(item, lang, 'content') or get_text(item, 'en', 'content')}\n\n")
            fh.write(PAGE_BREAK + "\n\n")
    return path


def toggle_bookmark(item_id, bookmarks, lang):
    if item_id in bookmarks:
        bookmarks.remove(item_id)
        save_bookmarks(bookmarks)
        return UI[lang]["bookmark_removed"]
    bookmarks.append(item_id)
    save_bookmarks(bookmarks)
    return UI[lang]["bookmark_added"]


def reader(entries, result_items, start_index, lang, bookmarks):
    idx = start_index
    section = "1"
    while 0 <= idx < len(result_items):
        current = result_items[idx]
        render_entry(current, lang, section, bookmarks)
        print()
        print(UI[lang]["reader_help"])
        cmd = input("> ").strip().lower()
        if cmd == "n" and idx < len(result_items) - 1:
            idx += 1
        elif cmd == "p" and idx > 0:
            idx -= 1
        elif cmd in {"1", "2", "3"}:
            section = cmd
        elif cmd == "r":
            rel = related_entries(entries, current)
            if rel:
                print()
                for num, item in enumerate(rel, 1):
                    print(f"{num}. {item.get('topic', '')} [{item.get('category', '')}]")
                pick = input("Choose related number or Enter: ").strip()
                if pick.isdigit():
                    n = int(pick)
                    if 1 <= n <= len(rel):
                        chosen = rel[n - 1]
                        if chosen in result_items:
                            idx = result_items.index(chosen)
                        else:
                            result_items.append(chosen)
                            idx = len(result_items) - 1
        elif cmd == "m":
            print(toggle_bookmark(current.get("id"), bookmarks, lang))
            pause(lang)
        elif cmd == "e":
            choice = input(UI[lang]["group_export"] + ": ").strip()
            try:
                path = None
                if choice == "1":
                    path = export_entries([current], lang, current.get("topic", "entry"))
                elif choice == "2":
                    path = export_entries(result_items, lang, "current_results")
                elif choice == "3":
                    same = [x for x in entries if normalize(x.get("category", "")) == normalize(current.get("category", ""))]
                    path = export_entries(same, lang, f"category_{current.get('category', '')}")
                if path:
                    print(f"\n{UI[lang]['export_done']} {path}")
            except Exception as exc:
                print(f"\n{UI[lang]['export_failed']} {exc}")
            pause(lang)
        elif cmd in {"b", ""}:
            return


def show_results(entries, ranked, lang, query, bookmarks):
    clear()
    print_header(f"{len(ranked)} {UI[lang]['results']} - {query}")
    for num, (score, item) in enumerate(ranked, 1):
        preview = match_snippet(item, query, lang)
        mark = "*" if item.get("id") in bookmarks else " "
        print(f"{mark}{num}. {item.get('topic', '')} [{item.get('category', '')}] score={score:.1f}")
        print(f"   {UI[lang]['snippet']}: {preview[:240]}{'...' if len(preview) > 240 else ''}")
    print()
    choice = input(UI[lang]["pick_result"] + ": ").strip()
    if choice.isdigit():
        n = int(choice)
        if 1 <= n <= len(ranked):
            reader(entries, [item for _, item in ranked], n - 1, lang, bookmarks)


def search_mode(entries, lang, mode, bookmarks):
    labels = {"keyword": UI[lang]["search"], "tag": UI[lang]["tag"], "category": UI[lang]["category"], "topic": UI[lang]["topic"]}
    query = input(labels[mode] + ": ").strip()
    if not query:
        return
    ranked = search_entries(entries, query, mode)
    if not ranked:
        print(UI[lang]["no_results"])
        suggestions = find_suggestions(entries, query)
        if suggestions:
            print(f"\n{UI[lang]['suggestions']}: {', '.join(suggestions)}")
        pause(lang)
        return
    show_results(entries, ranked, lang, query, bookmarks)


def browse_categories(entries, lang, bookmarks):
    cats = sorted({item.get("category", "") for item in entries if item.get("category")})
    clear()
    print_header(UI[lang]["categories"])
    for i, cat in enumerate(cats, 1):
        count = sum(1 for item in entries if item.get("category", "") == cat)
        print(f"{i}. {cat} ({count})")
    choice = input("\n" + UI[lang]["choose_category"] + ": ").strip()
    if choice.isdigit():
        n = int(choice)
        if 1 <= n <= len(cats):
            selected = cats[n - 1]
            ranked = [(100.0, item) for item in entries if item.get("category", "") == selected]
            show_results(entries, ranked, lang, selected, bookmarks)


def browse_topics(entries, lang, bookmarks):
    topics = sorted({item.get("topic", "") for item in entries if item.get("topic")})
    clear()
    print_header(UI[lang]["topics"])
    for i, topic in enumerate(topics, 1):
        count = sum(1 for item in entries if item.get("topic", "") == topic)
        print(f"{i}. {topic} ({count})")
    choice = input("\n" + UI[lang]["choose_topic"] + ": ").strip()
    if choice.isdigit():
        n = int(choice)
        if 1 <= n <= len(topics):
            selected = topics[n - 1]
            ranked = [(100.0, item) for item in entries if item.get("topic", "") == selected]
            show_results(entries, ranked, lang, selected, bookmarks)


def browse_bookmarks(entries, lang, bookmarks):
    clear()
    print_header(UI[lang]["bookmarks"])
    saved = [item for item in entries if item.get("id") in bookmarks]
    if not saved:
        print(UI[lang]["bookmark_empty"])
        pause(lang)
        return
    for i, item in enumerate(saved, 1):
        print(f"{i}. {item.get('topic', '')} [{item.get('category', '')}]")
    choice = input("\n" + UI[lang]["choose_bookmark"] + ": ").strip()
    if choice.isdigit():
        n = int(choice)
        if 1 <= n <= len(saved):
            reader(entries, saved, n - 1, lang, bookmarks)


def show_update_logs(lang):
    logs = list_update_logs()
    clear()
    print_header(UI[lang]["update_logs"])
    for i, log in enumerate(logs, 1):
        print(f"{i}. {log}")
    choice = input("\n" + UI[lang]["choose_log"] + ": ").strip()
    if choice.isdigit():
        n = int(choice)
        if 1 <= n <= len(logs):
            clear()
            print_header(logs[n - 1])
            with open(os.path.join(UPDATES_DIR, logs[n - 1]), "r", encoding="utf-8") as fh:
                print(fh.read())
            pause(lang)


def show_stats(entries, lang):
    clear()
    print_header(UI[lang]["stats"])
    file_count, entry_count, cat_count, topic_count, tag_count, log_count, latest, high_priority, urgent, missing = stats(entries)
    print(f"JSON files: {file_count}")
    print(f"Entries: {entry_count}")
    print(f"Categories: {cat_count}")
    print(f"Topics: {topic_count}")
    print(f"Tags: {tag_count}")
    print(f"Update logs: {log_count}")
    print(f"Latest date: {latest}")
    print(f"High priority entries: {high_priority}")
    print(f"Urgent entries: {urgent}")
    print(f"Entries with missing required fields: {missing}")
    print(f"Runtime home: {APP_HOME}")
    pause(lang)


def run_integrity(entries, lang):
    clear()
    print_header(UI[lang]["integrity"])
    missing, dupe_ids, dupe_pairs = integrity(entries)
    if not missing and not dupe_ids and not dupe_pairs:
        print(UI[lang]["integrity_ok"])
        pause(lang)
        return
    if missing:
        print("Missing fields:")
        for entry_id, fields in missing[:40]:
            print(f"- {entry_id}: {', '.join(fields)}")
        print()
    if dupe_ids:
        print("Duplicate IDs:")
        for val in dupe_ids:
            print(f"- {val}")
        print()
    if dupe_pairs:
        print("Duplicate topic/subcategory pairs:")
        for pair in dupe_pairs[:40]:
            print(f"- {pair[0]} / {pair[1]}")
    pause(lang)


def print_help(lang):
    clear()
    print_header(UI[lang]["help"])
    print(wrap(UI[lang]["help_body"]))
    print()
    print("Hidden commands: reload | lang")
    pause(lang)


def main():
    ensure_runtime_dirs()
    lang = choose_language()
    entries = load_database()
    bookmarks = load_bookmarks()
    while True:
        clear()
        print_header(UI[lang]["welcome"])
        if not entries:
            print(UI[lang]["empty_db"])
            print()
        print(UI[lang]["main_menu"])
        for line in UI[lang]["menu_items"]:
            print(line)
        choice = input("\n" + UI[lang]["prompt"] + ": ").strip().lower()
        if choice == "1":
            search_mode(entries, lang, "keyword", bookmarks)
        elif choice == "2":
            search_mode(entries, lang, "tag", bookmarks)
        elif choice == "3":
            search_mode(entries, lang, "category", bookmarks)
        elif choice == "4":
            search_mode(entries, lang, "topic", bookmarks)
        elif choice == "5":
            browse_categories(entries, lang, bookmarks)
        elif choice == "6":
            browse_topics(entries, lang, bookmarks)
        elif choice == "7":
            browse_bookmarks(entries, lang, bookmarks)
        elif choice == "8":
            show_stats(entries, lang)
        elif choice == "9":
            show_update_logs(lang)
        elif choice == "10":
            run_integrity(entries, lang)
        elif choice == "11":
            print_help(lang)
        elif choice == "reload":
            entries = load_database()
            bookmarks = load_bookmarks()
            print(UI[lang]["reload_msg"])
            pause(lang)
        elif choice == "lang":
            lang = "el" if lang == "en" else "en"
        elif choice == "0":
            clear()
            print(UI[lang]["exit"])
            break
        else:
            print(UI[lang]["invalid"])
            pause(lang)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExit requested.")
