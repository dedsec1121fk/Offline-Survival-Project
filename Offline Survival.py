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
SEARCH_HISTORY_FILE = os.path.join(APP_HOME, "search_history.json")
WRAP_WIDTH = 96
PAGE_BREAK = "=" * WRAP_WIDTH
RECENT_SEARCH_LIMIT = 40

REQUIRED_FIELDS = [
    "id", "topic", "category", "subcategory", "tags",
    "summary_en", "summary_el", "content_en", "content_el",
    "steps_en", "steps_el", "warnings_en", "warnings_el",
    "mistakes_en", "mistakes_el", "related_topics",
    "difficulty", "urgency", "priority", "last_updated", "update_note"
]

SEARCH_SYNONYMS = {
    "water": ["hydration", "drink", "purification", "storage", "dehydration"],
    "hydration": ["water", "dehydration", "fluids", "ors"],
    "fire": ["heat", "cooking", "burn", "fuel"],
    "food": ["nutrition", "calories", "scarcity", "preservation"],
    "medicine": ["medical", "firstaid", "first-aid", "treatment", "injury"],
    "medical": ["medicine", "treatment", "triage", "injury"],
    "injury": ["wound", "bleeding", "fracture", "pain"],
    "shelter": ["insulation", "storm", "cold", "sleep"],
    "psychology": ["panic", "morale", "stress", "mental"],
    "stress": ["panic", "adrenaline", "psychology", "fatigue"],
    "movement": ["route", "travel", "evacuation", "terrain"],
    "route": ["movement", "terrain", "travel", "evacuation"],
    "cold": ["winter", "layering", "wet", "temperature"],
    "mountain": ["elevation", "slope", "terrain", "cold"],
    "garden": ["soil", "seed", "crop", "agriculture"],
    "animals": ["livestock", "feed", "pen", "fodder"],
    "books": ["knowledge", "maps", "writing", "archive"],
    "εργαλεια": ["επισκευη", "σχοινι", "φορτιο"],
    "νερο": ["ενυδατωση", "αποθηκευση", "καθαρισμος", "αφυδατωση"],
    "τροφη": ["διατροφη", "θερμιδες", "συντηρηση", "πεινα"],
    "ιατρικη": ["φαρμακα", "τραυμα", "τριαζ", "θεραπεια"],
    "ψυχολογια": ["πανικος", "ηθικο", "στρες", "νοητικο"],
    "κινηση": ["διαδρομη", "μετακινηση", "εκκενωση", "εδάφος"],
    "κρυο": ["χειμωνας", "στρωσεις", "βρεγμενα", "θερμοκρασια"],
    "βουνο": ["υψομετρο", "κλιση", "εδάφος", "κρυο"]
}

UI = {
    "en": {
        "choose_language": "Choose language / Επιλογή γλώσσας",
        "welcome": "Offline Survival - deeper search, clearer reading, stronger recall",
        "main_menu": "Main menu",
        "menu_items": [
            "1. Smart search by keyword or phrase",
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
        "search": "Enter keyword or phrase",
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
        "choose_recent": "Choose recent search number, or Enter to go back",
        "update_logs": "Update logs",
        "recent": "Recent searches",
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
        "reasons": "Why this matched",
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
        "reader_help": "Commands: [n] next  [p] previous  [1] overview  [2] full  [3] mistakes  [r] related  [m] bookmark  [e] export  [b] back",
        "export_done": "Export created:",
        "export_failed": "Export failed:",
        "group_export": "Export [1] this entry, [2] current results, [3] same category, [Enter] cancel",
        "integrity_ok": "No duplicate IDs or major missing-field issues were found.",
        "empty_db": "Database is missing or empty.",
        "reload_msg": "Database reloaded.",
        "suggestions": "Closest suggestions",
        "recent_empty": "No recent searches saved yet.",
        "help_body": "Search now expands queries through a built-in survival synonym map, ranks fields with stronger weighting, shows why results matched, stores recent searches in ~/Offline Survival, and uses better snippets. Hidden commands at the main menu: reload | lang | recent."
    },
    "el": {
        "choose_language": "Επιλογή γλώσσας / Choose language",
        "welcome": "Offline Survival - βαθύτερη αναζήτηση, καθαρότερη ανάγνωση, ισχυρότερη μνήμη",
        "main_menu": "Κεντρικό μενού",
        "menu_items": [
            "1. Έξυπνη αναζήτηση με λέξη ή φράση",
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
        "search": "Δώσε λέξη ή φράση",
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
        "choose_recent": "Διάλεξε αριθμό πρόσφατης αναζήτησης ή Enter για επιστροφή",
        "update_logs": "Αρχεία ενημερώσεων",
        "recent": "Πρόσφατες αναζητήσεις",
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
        "reasons": "Γιατί ταίριαξε",
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
        "reader_help": "Εντολές: [n] επόμενο  [p] προηγούμενο  [1] overview  [2] πλήρης  [3] λάθη  [r] σχετικά  [m] σελιδοδείκτης  [e] εξαγωγή  [b] πίσω",
        "export_done": "Η εξαγωγή δημιουργήθηκε:",
        "export_failed": "Η εξαγωγή απέτυχε:",
        "group_export": "Εξαγωγή [1] αυτής της καταχώρησης, [2] τρεχόντων αποτελεσμάτων, [3] ίδιας κατηγορίας, [Enter] ακύρωση",
        "integrity_ok": "Δεν βρέθηκαν διπλά IDs ή σοβαρά προβλήματα ελλιπών πεδίων.",
        "empty_db": "Η βάση λείπει ή είναι άδεια.",
        "reload_msg": "Η βάση επαναφορτώθηκε.",
        "suggestions": "Κοντινές προτάσεις",
        "recent_empty": "Δεν υπάρχουν ακόμη πρόσφατες αναζητήσεις.",
        "help_body": "Η αναζήτηση τώρα επεκτείνει ερωτήματα με εσωτερικό χάρτη συνωνύμων επιβίωσης, δίνει ισχυρότερη βαρύτητα στα πεδία, δείχνει γιατί ταίριαξαν τα αποτελέσματα, αποθηκεύει πρόσφατες αναζητήσεις στο ~/Offline Survival και χρησιμοποιεί καλύτερα snippets. Κρυφές εντολές στο κεντρικό μενού: reload | lang | recent."
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


def load_search_history():
    ensure_runtime_dirs()
    if not os.path.isfile(SEARCH_HISTORY_FILE):
        return []
    try:
        with open(SEARCH_HISTORY_FILE, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        return data if isinstance(data, list) else []
    except Exception:
        return []


def save_search_history(history):
    ensure_runtime_dirs()
    with open(SEARCH_HISTORY_FILE, "w", encoding="utf-8") as fh:
        json.dump(history[:RECENT_SEARCH_LIMIT], fh, ensure_ascii=False, indent=2)


def add_search_history(query, mode):
    history = load_search_history()
    record = {
        "query": query,
        "mode": mode,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    history = [x for x in history if not (x.get("query") == query and x.get("mode") == mode)]
    history.insert(0, record)
    save_search_history(history)


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
    return val if not isinstance(val, list) else " ".join(map(str, val))


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
        " ".join(item.get("related_topics", []) or []), item.get("_source_file", ""),
        " ".join(item.get("_aliases", []))
    ]
    return normalize(" ".join(parts))


def expand_terms(query):
    tokens = tokenize(query)
    expanded = set(tokens)
    for token in list(tokens):
        if token in SEARCH_SYNONYMS:
            expanded.update(SEARCH_SYNONYMS[token])
        for key, vals in SEARCH_SYNONYMS.items():
            if token in vals:
                expanded.add(key)
                expanded.update(vals)
    return tokens, sorted(expanded)


def build_profile(query):
    q = normalize(query)
    tokens, expanded = expand_terms(q)
    return {
        "raw": query,
        "q": q,
        "tokens": tokens,
        "expanded": expanded
    }


def best_snippet(item, profile, lang):
    candidates = [
        get_text(item, lang, "summary"),
        get_text(item, lang, "content"),
        " ".join(get_list(item, lang, "steps")),
        " ".join(get_list(item, lang, "warnings")),
        " ".join(get_list(item, lang, "mistakes"))
    ]
    q = profile["q"]
    terms = [q] + profile["expanded"]
    for field in candidates:
        low = normalize(field)
        for term in terms:
            idx = low.find(term)
            if idx != -1:
                start = max(0, idx - 75)
                end = min(len(field), idx + len(term) + 110)
                return field[start:end].replace("\n", " ").strip()
    return (get_text(item, lang, "summary") or get_text(item, "en", "summary"))[:220]


def closest_suggestions(entries, query):
    pool = set()
    for item in entries:
        pool.add(item.get("topic", ""))
        pool.add(item.get("category", ""))
        pool.add(item.get("subcategory", ""))
        pool.update(item.get("tags", []) or [])
        pool.update(item.get("_aliases", []) or [])
    pool = [x for x in pool if x]
    return difflib.get_close_matches(query, pool, n=10, cutoff=0.55)


def field_scores(item):
    return {
        "topic": normalize(item.get("topic", "")),
        "category": normalize(item.get("category", "")),
        "subcategory": normalize(item.get("subcategory", "")),
        "tags": [normalize(x) for x in item.get("tags", []) or []],
        "aliases": [normalize(x) for x in item.get("_aliases", []) or []],
        "summary_en": normalize(get_text(item, "en", "summary")),
        "summary_el": normalize(get_text(item, "el", "summary")),
        "content_en": normalize(get_text(item, "en", "content")),
        "content_el": normalize(get_text(item, "el", "content")),
        "steps_en": normalize(" ".join(get_list(item, "en", "steps"))),
        "steps_el": normalize(" ".join(get_list(item, "el", "steps"))),
        "warnings_en": normalize(" ".join(get_list(item, "en", "warnings"))),
        "warnings_el": normalize(" ".join(get_list(item, "el", "warnings"))),
        "mistakes_en": normalize(" ".join(get_list(item, "en", "mistakes"))),
        "mistakes_el": normalize(" ".join(get_list(item, "el", "mistakes"))),
        "related": normalize(" ".join(item.get("related_topics", []) or [])),
        "source": normalize(item.get("_source_file", ""))
    }


def compute_score(item, profile, mode="keyword"):
    fs = field_scores(item)
    q = profile["q"]
    tokens = profile["tokens"]
    expanded = profile["expanded"]
    score = 0.0
    reasons = []

    def add(points, reason):
        nonlocal score
        score += points
        if reason and reason not in reasons:
            reasons.append(reason)

    if mode == "topic":
        if q == fs["topic"]:
            add(320, "exact topic")
        if q in fs["topic"]:
            add(160, "topic phrase")
        for token in tokens:
            if token in fs["topic"]:
                add(26, "topic term")
        add(difflib.SequenceMatcher(None, q, fs["topic"]).ratio() * 80, "topic similarity")
        return score, reasons

    if mode == "category":
        if q == fs["category"]:
            add(300, "exact category")
        if q in fs["category"] or q in fs["subcategory"]:
            add(160, "category phrase")
        for token in tokens:
            if token in fs["category"] or token in fs["subcategory"]:
                add(22, "category term")
        add(difflib.SequenceMatcher(None, q, fs["category"]).ratio() * 70, "category similarity")
        return score, reasons

    if mode == "tag":
        if q in fs["tags"] or q in fs["aliases"]:
            add(280, "exact tag/alias")
        for tag in fs["tags"] + fs["aliases"]:
            if q in tag:
                add(80, "tag phrase")
            add(difflib.SequenceMatcher(None, q, tag).ratio() * 28, "tag similarity")
        return score, reasons

    # keyword mode with stronger ranking
    if q == fs["topic"]:
        add(360, "exact topic")
    if q in fs["topic"]:
        add(220, "topic phrase")
    if q == fs["category"] or q == fs["subcategory"]:
        add(180, "exact category/subcategory")
    if q in fs["category"] or q in fs["subcategory"]:
        add(95, "category phrase")
    if q in fs["summary_en"] or q in fs["summary_el"]:
        add(150, "summary phrase")
    if q in fs["content_en"] or q in fs["content_el"]:
        add(95, "content phrase")
    if q in fs["steps_en"] or q in fs["steps_el"]:
        add(70, "action phrase")
    if q in fs["warnings_en"] or q in fs["warnings_el"]:
        add(65, "warning phrase")
    if q in fs["mistakes_en"] or q in fs["mistakes_el"]:
        add(60, "mistake phrase")
    if q in fs["related"]:
        add(50, "related topic phrase")
    if q in fs["source"]:
        add(35, "source file phrase")
    if q in fs["tags"] or q in fs["aliases"]:
        add(130, "exact tag/alias")

    all_text = search_blob(item)
    token_hits = 0
    expanded_hits = 0
    for token in tokens:
        if token in fs["topic"]:
            add(34, f"topic term")
            token_hits += 1
        elif token in fs["tags"] or token in fs["aliases"]:
            add(26, "tag term")
            token_hits += 1
        elif token in fs["category"] or token in fs["subcategory"]:
            add(20, "category term")
            token_hits += 1
        elif token in all_text:
            add(10, "content term")
            token_hits += 1
    for token in expanded:
        if token in all_text:
            expanded_hits += 1
            add(2.5, "expanded synonym")

    if tokens and token_hits == len(tokens):
        add(65 + 5 * len(tokens), "all query terms found")
    if len(expanded) > 2 and expanded_hits >= min(3, len(expanded)):
        add(18, "multiple related concepts found")

    add(difflib.SequenceMatcher(None, q, fs["topic"]).ratio() * 55, "topic similarity")
    add(difflib.SequenceMatcher(None, q, fs["summary_en"][:500] + " " + fs["summary_el"][:500]).ratio() * 25, "summary similarity")

    if normalize(item.get("priority", "")) == "high":
        add(5, "high priority")
    if normalize(item.get("urgency", "")) in {"high", "critical"}:
        add(5, "high urgency")

    return score, reasons[:5]


def search_entries(entries, query, mode="keyword"):
    profile = build_profile(query)
    ranked = []
    for item in entries:
        score, reasons = compute_score(item, profile, mode)
        if score >= 25:
            ranked.append((score, reasons, item))
    ranked.sort(key=lambda pair: (-pair[0], pair[2].get("topic", "")))
    return ranked, profile


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
    print(f"Source file: {item.get('_source_file', '')}")
    print(status)


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


def show_results(entries, ranked, lang, profile, bookmarks):
    clear()
    print_header(f"{len(ranked)} {UI[lang]['results']} - {profile['raw']}")
    for num, (score, reasons, item) in enumerate(ranked, 1):
        preview = best_snippet(item, profile, lang)
        mark = "*" if item.get("id") in bookmarks else " "
        print(f"{mark}{num}. {item.get('topic', '')} [{item.get('category', '')}] score={score:.1f}")
        if reasons:
            print(f"   {UI[lang]['reasons']}: {', '.join(reasons)}")
        print(f"   {UI[lang]['snippet']}: {preview[:240]}{'...' if len(preview) > 240 else ''}")
    print()
    choice = input(UI[lang]["pick_result"] + ": ").strip()
    if choice.isdigit():
        n = int(choice)
        if 1 <= n <= len(ranked):
            reader(entries, [item for _, _, item in ranked], n - 1, lang, bookmarks)


def search_mode(entries, lang, mode, bookmarks):
    labels = {"keyword": UI[lang]["search"], "tag": UI[lang]["tag"], "category": UI[lang]["category"], "topic": UI[lang]["topic"]}
    query = input(labels[mode] + ": ").strip()
    if not query:
        return
    add_search_history(query, mode)
    ranked, profile = search_entries(entries, query, mode)
    if not ranked:
        print(UI[lang]["no_results"])
        suggestions = closest_suggestions(entries, query)
        if suggestions:
            print(f"\n{UI[lang]['suggestions']}: {', '.join(suggestions)}")
        pause(lang)
        return
    show_results(entries, ranked, lang, profile, bookmarks)


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
            ranked = [(100.0, ["category browse"], item) for item in entries if item.get("category", "") == selected]
            show_results(entries, ranked, lang, {"raw": selected, "q": selected, "expanded": [], "tokens": []}, bookmarks)


def browse_topics(entries, lang, bookmarks):
    topics = sorted({item.get("topic", "") for item in entries if item.get("topic")})
    clear()
    print_header(UI[lang]["topics"])
    for i, topic in enumerate(topics, 1):
        print(f"{i}. {topic}")
    choice = input("\n" + UI[lang]["choose_topic"] + ": ").strip()
    if choice.isdigit():
        n = int(choice)
        if 1 <= n <= len(topics):
            selected = topics[n - 1]
            ranked = [(100.0, ["topic browse"], item) for item in entries if item.get("topic", "") == selected]
            show_results(entries, ranked, lang, {"raw": selected, "q": selected, "expanded": [], "tokens": []}, bookmarks)


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


def browse_recent(entries, lang, bookmarks):
    history = load_search_history()
    clear()
    print_header(UI[lang]["recent"])
    if not history:
        print(UI[lang]["recent_empty"])
        pause(lang)
        return
    for i, rec in enumerate(history[:RECENT_SEARCH_LIMIT], 1):
        print(f"{i}. [{rec.get('mode')}] {rec.get('query')} ({rec.get('time')})")
    choice = input("\n" + UI[lang]["choose_recent"] + ": ").strip()
    if choice.isdigit():
        n = int(choice)
        if 1 <= n <= len(history[:RECENT_SEARCH_LIMIT]):
            rec = history[n - 1]
            ranked, profile = search_entries(entries, rec.get("query", ""), rec.get("mode", "keyword"))
            if ranked:
                show_results(entries, ranked, lang, profile, bookmarks)


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
    print(f"Recent searches stored: {len(load_search_history())}")
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
        for entry_id, fields in missing[:50]:
            print(f"- {entry_id}: {', '.join(fields)}")
        print()
    if dupe_ids:
        print("Duplicate IDs:")
        for val in dupe_ids:
            print(f"- {val}")
        print()
    if dupe_pairs:
        print("Duplicate topic/subcategory pairs:")
        for pair in dupe_pairs[:50]:
            print(f"- {pair[0]} / {pair[1]}")
    pause(lang)


def print_help(lang):
    clear()
    print_header(UI[lang]["help"])
    print(wrap(UI[lang]["help_body"]))
    print()
    print("Hidden commands: reload | lang | recent")
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
        elif choice == "recent":
            browse_recent(entries, lang, bookmarks)
        elif choice == "0":
            clear()
            print("Stay safe." if lang == "en" else "Μείνε ασφαλής.")
            break
        else:
            print(UI[lang]["invalid"])
            pause(lang)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExit requested.")
