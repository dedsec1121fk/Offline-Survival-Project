#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import difflib
import textwrap
from collections import Counter
from datetime import datetime

APP_NAME = "Offline Survival"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.join(SCRIPT_DIR, "Offline Survival Database")
UPDATES_DIR = os.path.join(SCRIPT_DIR, "Offline Survival Updates")
APP_HOME = os.path.join(os.path.expanduser("~"), "Offline Survival")
EXPORT_DIR = os.path.join(APP_HOME, "Exports")
TXT_LIBRARY_DIR = "/storage/emulated/0/Download/Offline Survival TXT's"
BOOKMARKS_FILE = os.path.join(APP_HOME, "bookmarks.json")
SEARCH_HISTORY_FILE = os.path.join(APP_HOME, "search_history.json")
WRAP_WIDTH = 96
RECENT_LIMIT = 40
PAGE_BREAK = "=" * WRAP_WIDTH

REQUIRED_FIELDS = [
    "id", "topic", "category", "subcategory", "tags",
    "summary_en", "summary_el", "content_en", "content_el",
    "steps_en", "steps_el", "warnings_en", "warnings_el",
    "mistakes_en", "mistakes_el", "related_topics",
    "difficulty", "urgency", "priority", "last_updated", "update_note"
]

SEARCH_SYNONYMS = {
    "water": ["hydration", "dehydration", "purification", "storage", "ors"],
    "hydration": ["water", "dehydration", "fluids"],
    "food": ["nutrition", "calories", "preservation", "scarcity"],
    "medicine": ["medical", "injury", "treatment", "triage", "firstaid", "first-aid"],
    "shelter": ["insulation", "storm", "cold", "sleep"],
    "psychology": ["stress", "panic", "morale", "mental"],
    "movement": ["route", "terrain", "evacuation", "travel"],
    "mountain": ["elevation", "slope", "terrain", "cold"],
    "garden": ["seed", "soil", "crop", "agriculture"],
    "wild": ["wilderness", "forest", "camp", "route", "rain"],
    "wilderness": ["wild", "forest", "camp", "route", "water"],
    "urban": ["town", "apartment", "blackout", "stairs", "sanitation"],
    "town": ["urban", "apartment", "neighbors", "barter", "water"],
    "blackout": ["power", "urban", "apartment", "light", "stairs"],
    "ai": ["automation", "lockout", "manual", "records", "offline"],
    "biology": ["anatomy", "sleep", "infection", "healing", "digestion"],
    "recipes": ["food", "rice", "bread", "beans", "broth"],
    "animals": ["livestock", "feed", "pen", "fodder"],
    "νερο": ["ενυδατωση", "αφυδατωση", "καθαρισμος", "αποθηκευση"],
    "τροφη": ["διατροφη", "θερμιδες", "συντηρηση", "πεινα"],
    "ιατρικη": ["φαρμακα", "τραυμα", "θεραπεια", "τριαζ"],
    "ψυχολογια": ["στρες", "πανικος", "ηθικο", "νοητικο"],
    "κινηση": ["διαδρομη", "εδάφος", "εκκενωση", "ταξιδι"],
    "βουνο": ["υψομετρο", "κλιση", "εδάφος", "κρυο"],
    "αγρια": ["υπαιθρος", "κατασκηνωση", "διαδρομη", "βροχη", "νερο"],
    "πολη": ["αστικο", "διαμερισμα", "blackout", "σκαλες", "υγιεινη"],
    "τεχνητη": ["ai", "αυτοματισμος", "κλειδωμα", "offline"],
    "βιολογια": ["ανατομια", "υπνος", "λοιμωξη", "επουλωση", "πεψη"],
    "συνταγες": ["τροφη", "ρυζι", "ψωμι", "οσπρια", "ζωμος"]
}

UI = {
    "en": {
        "welcome": "Offline Survival - stronger search, easier reading, deeper offline library",
        "choose_language": "Choose language / Επιλογή γλώσσας",
        "menu_items": [
            "1. Smart search",
            "2. Search by tag",
            "3. Search by category",
            "4. Search by topic",
            "5. Browse categories",
            "6. Browse topics",
            "7. Bookmarks",
            "8. Database statistics",
            "9. Update logs",
            "10. Integrity check",
            "11. Help",
            "12. Extract whole knowledge to TXT library",
            "0. Exit"
        ],
        "prompt": "Choose an option",
        "invalid": "Invalid choice.",
        "search": "Enter keyword or phrase",
        "tag": "Enter tag",
        "category": "Enter category",
        "topic": "Enter topic",
        "results": "results",
        "no_results": "No matching entries found.",
        "suggestions": "Closest suggestions",
        "pick": "Open result number, or press Enter to go back",
        "categories": "Categories",
        "topics": "Topics",
        "bookmarks": "Bookmarks",
        "recent": "Recent searches",
        "recent_empty": "No recent searches saved yet.",
        "logs": "Update logs",
        "stats": "Database statistics",
        "integrity": "Integrity check",
        "help": "Help",
        "press": "Press Enter to continue...",
        "summary": "Summary",
        "actions": "Actions",
        "warnings": "Warnings",
        "mistakes": "Common mistakes",
        "full": "Full detail",
        "easy": "Easy read",
        "reasons": "Why this matched",
        "snippet": "Preview",
        "bookmarked": "Bookmarked",
        "not_bookmarked": "Not bookmarked",
        "bookmark_added": "Bookmark added.",
        "bookmark_removed": "Bookmark removed.",
        "bookmark_empty": "No bookmarks saved yet.",
        "reader_help": "Commands: [n] next  [p] previous  [1] overview  [2] full  [3] mistakes  [4] easy read  [r] related  [m] bookmark  [e] export  [b] back",
        "export_prompt": "Export [1] this entry, [2] current results, [3] same category, [Enter] cancel",
        "export_done": "Export created:",
        "export_failed": "Export failed:",
        "library_done": "TXT library created:",
        "library_failed": "TXT library extraction failed:",
        "integrity_ok": "No duplicate IDs or major missing-field issues were found.",
        "reload_msg": "Database reloaded.",
        "help_text": "Search now expands queries with survival synonyms in English and Greek, ranks fields more intelligently, shows why results matched, stores recent searches in ~/Offline Survival, and can extract the entire knowledge base to /storage/emulated/0/Download/Offline Survival TXT's. The reader now starts in easy read mode. Hidden main-menu commands: reload | lang | recent.",
        "no_logs": "No update logs found yet.",
        "meta_category": "Category",
        "meta_subcategory": "Subcategory",
        "meta_tags": "Tags",
        "meta_priority": "Priority",
        "meta_urgency": "Urgency",
        "meta_difficulty": "Difficulty",
        "meta_updated": "Last updated",
        "meta_note": "Update note",
        "meta_source": "Source file",
        "related_topics_label": "Related topics",
        "choose_related": "Choose related number or Enter:"
    },
    "el": {
        "welcome": "Offline Survival - ισχυρότερη αναζήτηση, ευκολότερη ανάγνωση, βαθύτερη offline βιβλιοθήκη",
        "choose_language": "Επιλογή γλώσσας / Choose language",
        "menu_items": [
            "1. Έξυπνη αναζήτηση",
            "2. Αναζήτηση με ετικέτα",
            "3. Αναζήτηση με κατηγορία",
            "4. Αναζήτηση με θέμα",
            "5. Περιήγηση κατηγοριών",
            "6. Περιήγηση θεμάτων",
            "7. Σελιδοδείκτες",
            "8. Στατιστικά βάσης",
            "9. Αρχεία ενημέρωσης",
            "10. Έλεγχος ακεραιότητας",
            "11. Βοήθεια",
            "12. Εξαγωγή όλης της γνώσης σε βιβλιοθήκη TXT",
            "0. Έξοδος"
        ],
        "prompt": "Διάλεξε επιλογή",
        "invalid": "Μη έγκυρη επιλογή.",
        "search": "Δώσε λέξη ή φράση",
        "tag": "Δώσε ετικέτα",
        "category": "Δώσε κατηγορία",
        "topic": "Δώσε θέμα",
        "results": "αποτελέσματα",
        "no_results": "Δεν βρέθηκαν αποτελέσματα.",
        "suggestions": "Κοντινές προτάσεις",
        "pick": "Άνοιξε αριθμό αποτελέσματος ή πάτησε Enter για επιστροφή",
        "categories": "Κατηγορίες",
        "topics": "Θέματα",
        "bookmarks": "Σελιδοδείκτες",
        "recent": "Πρόσφατες αναζητήσεις",
        "recent_empty": "Δεν υπάρχουν ακόμη πρόσφατες αναζητήσεις.",
        "logs": "Αρχεία ενημερώσεων",
        "stats": "Στατιστικά βάσης",
        "integrity": "Έλεγχος ακεραιότητας",
        "help": "Βοήθεια",
        "press": "Πάτησε Enter για συνέχεια...",
        "summary": "Περίληψη",
        "actions": "Ενέργειες",
        "warnings": "Προειδοποιήσεις",
        "mistakes": "Συχνά λάθη",
        "full": "Πλήρης ανάλυση",
        "easy": "Εύκολη ανάγνωση",
        "reasons": "Γιατί ταίριαξε",
        "snippet": "Προεπισκόπηση",
        "bookmarked": "Αποθηκευμένο",
        "not_bookmarked": "Χωρίς σελιδοδείκτη",
        "bookmark_added": "Ο σελιδοδείκτης προστέθηκε.",
        "bookmark_removed": "Ο σελιδοδείκτης αφαιρέθηκε.",
        "bookmark_empty": "Δεν υπάρχουν ακόμη αποθηκευμένοι σελιδοδείκτες.",
        "reader_help": "Εντολές: [n] επόμενο  [p] προηγούμενο  [1] overview  [2] πλήρης  [3] λάθη  [4] εύκολη ανάγνωση  [r] σχετικά  [m] σελιδοδείκτης  [e] εξαγωγή  [b] πίσω",
        "export_prompt": "Εξαγωγή [1] αυτής της καταχώρησης, [2] τρεχόντων αποτελεσμάτων, [3] ίδιας κατηγορίας, [Enter] ακύρωση",
        "export_done": "Η εξαγωγή δημιουργήθηκε:",
        "export_failed": "Η εξαγωγή απέτυχε:",
        "library_done": "Η βιβλιοθήκη TXT δημιουργήθηκε:",
        "library_failed": "Η εξαγωγή βιβλιοθήκης TXT απέτυχε:",
        "integrity_ok": "Δεν βρέθηκαν διπλά IDs ή σοβαρά προβλήματα ελλιπών πεδίων.",
        "reload_msg": "Η βάση επαναφορτώθηκε.",
        "help_text": "Η αναζήτηση τώρα επεκτείνει ερωτήματα με συνώνυμα επιβίωσης σε Ελληνικά και Αγγλικά, δίνει πιο έξυπνη βαρύτητα στα πεδία, δείχνει γιατί ταίριαξαν τα αποτελέσματα, αποθηκεύει πρόσφατες αναζητήσεις στο ~/Offline Survival και μπορεί να εξάγει όλη τη γνώση στο /storage/emulated/0/Download/Offline Survival TXT's. Ο αναγνώστης ξεκινά τώρα σε εύκολη λειτουργία ανάγνωσης. Κρυφές εντολές κεντρικού μενού: reload | lang | recent.",
        "no_logs": "Δεν βρέθηκαν ακόμη αρχεία ενημερώσεων.",
        "meta_category": "Κατηγορία",
        "meta_subcategory": "Υποκατηγορία",
        "meta_tags": "Ετικέτες",
        "meta_priority": "Προτεραιότητα",
        "meta_urgency": "Επείγον",
        "meta_difficulty": "Δυσκολία",
        "meta_updated": "Τελευταία ενημέρωση",
        "meta_note": "Σημείωση ενημέρωσης",
        "meta_source": "Αρχείο πηγής",
        "related_topics_label": "Σχετικά θέματα",
        "choose_related": "Διάλεξε σχετικό αριθμό ή Enter:"
    }
}


def clear():
    os.system("clear")


def safe_mkdir(path):
    os.makedirs(path, exist_ok=True)


def ensure_dirs():
    safe_mkdir(APP_HOME)
    safe_mkdir(EXPORT_DIR)
    safe_mkdir(TXT_LIBRARY_DIR)
    safe_mkdir(DB_DIR)
    safe_mkdir(UPDATES_DIR)


def normalize(text):
    return " ".join(str(text).lower().split())


def tokenize(text):
    cleaned = []
    for ch in str(text).lower():
        cleaned.append(ch if ch.isalnum() or ch in "-_ '" else " ")
    return [tok for tok in "".join(cleaned).split() if tok]


def wrap(text):
    return "\n".join(textwrap.fill(line, width=WRAP_WIDTH) if line.strip() else "" for line in str(text).splitlines())


def pause(lang):
    input("\n" + UI[lang]["press"])


def safe_filename(name):
    out = []
    for ch in str(name):
        out.append(ch if ch.isalnum() or ch in (" ", "-", "_", "'", ".") else "_")
    return "".join(out).strip() or "untitled"


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


def load_json_list(path, fallback):
    if not os.path.isfile(path):
        return fallback
    try:
        with open(path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        return data if isinstance(data, list) else fallback
    except Exception:
        return fallback


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)


def load_bookmarks():
    ensure_dirs()
    return load_json_list(BOOKMARKS_FILE, [])


def save_bookmarks(bookmarks):
    ensure_dirs()
    save_json(BOOKMARKS_FILE, sorted(set(bookmarks)))


def load_history():
    ensure_dirs()
    return load_json_list(SEARCH_HISTORY_FILE, [])


def save_history(history):
    ensure_dirs()
    save_json(SEARCH_HISTORY_FILE, history[:RECENT_LIMIT])


def add_history(query, mode):
    hist = [h for h in load_history() if not (h.get("query") == query and h.get("mode") == mode)]
    hist.insert(0, {"query": query, "mode": mode, "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
    save_history(hist)


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
                "id": f"broken::{filename}", "topic": filename, "category": "system", "subcategory": "load_error", "tags": ["load_error"],
                "summary_en": f"Failed to load {filename}: {exc}", "summary_el": f"Αποτυχία φόρτωσης {filename}: {exc}",
                "content_en": "Fix or replace the broken JSON file.", "content_el": "Διόρθωσε ή αντικατέστησε το κατεστραμμένο JSON.",
                "steps_en": [], "steps_el": [], "warnings_en": ["Broken file."], "warnings_el": ["Κατεστραμμένο αρχείο."],
                "mistakes_en": [], "mistakes_el": [], "related_topics": [],
                "difficulty": "low", "urgency": "medium", "priority": "high", "last_updated": "", "update_note": "Auto-generated load error.",
                "_source_file": filename, "_aliases": ["load_error"]
            })
    return entries


def list_logs():
    if not os.path.isdir(UPDATES_DIR):
        return []
    return sorted([x for x in os.listdir(UPDATES_DIR) if x.lower().endswith(".txt")])


def get_text(item, lang, base):
    value = item.get(f"{base}_{lang}", "")
    return value if not isinstance(value, list) else " ".join(map(str, value))


def get_list(item, lang, base):
    value = item.get(f"{base}_{lang}", [])
    return value if isinstance(value, list) else ([value] if value else [])


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
    return {"raw": query, "q": q, "tokens": tokens, "expanded": expanded}


def search_blob(item):
    parts = [
        item.get("topic", ""), item.get("category", ""), item.get("subcategory", ""),
        " ".join(item.get("tags", []) or []), " ".join(item.get("_aliases", []) or []), item.get("_source_file", ""),
        item.get("summary_en", ""), item.get("summary_el", ""), item.get("content_en", ""), item.get("content_el", ""),
        " ".join(get_list(item, "en", "steps")), " ".join(get_list(item, "el", "steps")),
        " ".join(get_list(item, "en", "warnings")), " ".join(get_list(item, "el", "warnings")),
        " ".join(get_list(item, "en", "mistakes")), " ".join(get_list(item, "el", "mistakes")),
        " ".join(item.get("related_topics", []) or [])
    ]
    return normalize(" ".join(parts))


def score_entry(item, profile, mode):
    q = profile["q"]
    tokens = profile["tokens"]
    expanded = profile["expanded"]
    topic = normalize(item.get("topic", ""))
    category = normalize(item.get("category", ""))
    subcategory = normalize(item.get("subcategory", ""))
    tags = [normalize(x) for x in item.get("tags", []) or []]
    aliases = [normalize(x) for x in item.get("_aliases", []) or []]
    summary = normalize(get_text(item, "en", "summary") + " " + get_text(item, "el", "summary"))
    content = normalize(get_text(item, "en", "content") + " " + get_text(item, "el", "content"))
    steps = normalize(" ".join(get_list(item, "en", "steps") + get_list(item, "el", "steps")))
    warnings = normalize(" ".join(get_list(item, "en", "warnings") + get_list(item, "el", "warnings")))
    mistakes = normalize(" ".join(get_list(item, "en", "mistakes") + get_list(item, "el", "mistakes")))
    related = normalize(" ".join(item.get("related_topics", []) or []))
    source = normalize(item.get("_source_file", ""))
    blob = search_blob(item)

    score = 0.0
    reasons = []

    def add(points, reason):
        nonlocal score
        score += points
        if reason not in reasons:
            reasons.append(reason)

    if mode == "topic":
        if q == topic:
            add(320, "exact topic")
        if q in topic:
            add(160, "topic phrase")
        add(difflib.SequenceMatcher(None, q, topic).ratio() * 80, "topic similarity")
        return score, reasons[:4]

    if mode == "category":
        if q == category:
            add(300, "exact category")
        if q in category or q in subcategory:
            add(160, "category phrase")
        add(difflib.SequenceMatcher(None, q, category).ratio() * 70, "category similarity")
        return score, reasons[:4]

    if mode == "tag":
        if q in tags or q in aliases:
            add(280, "exact tag/alias")
        for t in tags + aliases:
            if q in t:
                add(80, "tag phrase")
            add(difflib.SequenceMatcher(None, q, t).ratio() * 28, "tag similarity")
        return score, reasons[:4]

    if q == topic:
        add(360, "exact topic")
    if q in topic:
        add(220, "topic phrase")
    if q == category or q == subcategory:
        add(180, "exact category/subcategory")
    if q in category or q in subcategory:
        add(95, "category phrase")
    if q in tags or q in aliases:
        add(130, "exact tag/alias")
    if q in summary:
        add(150, "summary phrase")
    if q in content:
        add(95, "content phrase")
    if q in steps:
        add(70, "action phrase")
    if q in warnings:
        add(65, "warning phrase")
    if q in mistakes:
        add(60, "mistake phrase")
    if q in related:
        add(50, "related phrase")
    if q in source:
        add(35, "source file phrase")

    token_hits = 0
    exp_hits = 0
    for token in tokens:
        if token in topic:
            add(34, "topic term")
            token_hits += 1
        elif token in tags or token in aliases:
            add(26, "tag term")
            token_hits += 1
        elif token in category or token in subcategory:
            add(20, "category term")
            token_hits += 1
        elif token in blob:
            add(10, "content term")
            token_hits += 1
    for token in expanded:
        if token in blob:
            exp_hits += 1
            add(2.5, "expanded synonym")
    if tokens and token_hits == len(tokens):
        add(65 + 5 * len(tokens), "all query terms found")
    if len(expanded) > 2 and exp_hits >= min(3, len(expanded)):
        add(18, "multiple related concepts found")

    add(difflib.SequenceMatcher(None, q, topic).ratio() * 55, "topic similarity")
    add(difflib.SequenceMatcher(None, q, summary[:500]).ratio() * 25, "summary similarity")
    if normalize(item.get("priority", "")) == "high":
        add(5, "high priority")
    if normalize(item.get("urgency", "")) in {"high", "critical"}:
        add(5, "high urgency")
    return score, reasons[:5]


def search_entries(entries, query, mode="keyword"):
    profile = build_profile(query)
    ranked = []
    for item in entries:
        score, reasons = score_entry(item, profile, mode)
        if score >= 25:
            ranked.append((score, reasons, item))
    ranked.sort(key=lambda x: (-x[0], x[2].get("topic", "")))
    return ranked, profile


def best_snippet(item, profile, lang):
    candidates = [
        get_text(item, lang, "summary"), get_text(item, lang, "content"),
        " ".join(get_list(item, lang, "steps")), " ".join(get_list(item, lang, "warnings")),
        " ".join(get_list(item, lang, "mistakes"))
    ]
    terms = [profile["q"]] + profile["expanded"]
    for text in candidates:
        low = normalize(text)
        for term in terms:
            idx = low.find(term)
            if idx != -1:
                start = max(0, idx - 75)
                end = min(len(text), idx + len(term) + 120)
                return text[start:end].replace("\n", " ").strip()
    return (get_text(item, lang, "summary") or get_text(item, "en", "summary"))[:220]


def suggestions(entries, query):
    pool = set()
    for item in entries:
        pool.add(item.get("topic", ""))
        pool.add(item.get("category", ""))
        pool.add(item.get("subcategory", ""))
        pool.update(item.get("tags", []) or [])
        pool.update(item.get("_aliases", []) or [])
    return difflib.get_close_matches(query, [x for x in pool if x], n=8, cutoff=0.55)


def related_entries(entries, item):
    rel = {normalize(x) for x in item.get("related_topics", []) or []}
    return [e for e in entries if e.get("id") != item.get("id") and normalize(e.get("topic", "")) in rel]


def print_header(title):
    print(PAGE_BREAK)
    print(title)
    print(PAGE_BREAK)


def print_meta(item, lang, bookmarks):
    print(f"{UI[lang]['meta_category']}: {item.get('category', '')}")
    print(f"{UI[lang]['meta_subcategory']}: {item.get('subcategory', '')}")
    print(f"{UI[lang]['meta_tags']}: {', '.join(item.get('tags', []) or [])}")
    print(f"{UI[lang]['meta_priority']}: {item.get('priority', '')} | {UI[lang]['meta_urgency']}: {item.get('urgency', '')} | {UI[lang]['meta_difficulty']}: {item.get('difficulty', '')}")
    print(f"{UI[lang]['meta_updated']}: {item.get('last_updated', '')}")
    print(f"{UI[lang]['meta_note']}: {item.get('update_note', '')}")
    print(f"{UI[lang]['meta_source']}: {item.get('_source_file', '')}")
    print(UI[lang]["bookmarked"] if item.get("id") in bookmarks else UI[lang]["not_bookmarked"])


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
    elif section == "3":
        print(f"[{UI[lang]['mistakes']}]\n")
        for line in get_list(item, lang, "mistakes") or get_list(item, "en", "mistakes"):
            print("- " + wrap(line))
    else:
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
        print()
        print(f"[{UI[lang]['mistakes']}]\n")
        for line in get_list(item, lang, "mistakes") or get_list(item, "en", "mistakes"):
            print("- " + wrap(line))
        print()
        print(f"[{UI[lang]['full']}]\n")
        print(wrap(get_text(item, lang, "content") or get_text(item, "en", "content")))
    print()
    print(f"Related topics: {', '.join(item.get('related_topics', []) or []) or '-'}")


def export_entries(entries_to_export, lang, label):
    ensure_dirs()
    path = os.path.join(EXPORT_DIR, f"{safe_filename(label)}.txt")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(f"{APP_NAME} Export\n")
        fh.write(f"Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        fh.write(PAGE_BREAK + "\n\n")
        for i, item in enumerate(entries_to_export, 1):
            fh.write(f"{i}. {item.get('topic', '')}\n")
            fh.write(f"Category: {item.get('category', '')}\n")
            fh.write(f"Subcategory: {item.get('subcategory', '')}\n")
            fh.write(f"Tags: {', '.join(item.get('tags', []) or [])}\n")
            fh.write(f"\nSummary\n{get_text(item, lang, 'summary') or get_text(item, 'en', 'summary')}\n\n")
            fh.write("Actions\n")
            for line in get_list(item, lang, 'steps') or get_list(item, 'en', 'steps'):
                fh.write(f"- {line}\n")
            fh.write("\nWarnings\n")
            for line in get_list(item, lang, 'warnings') or get_list(item, 'en', 'warnings'):
                fh.write(f"- {line}\n")
            fh.write("\nCommon mistakes\n")
            for line in get_list(item, lang, 'mistakes') or get_list(item, 'en', 'mistakes'):
                fh.write(f"- {line}\n")
            fh.write(f"\nFull detail\n{get_text(item, lang, 'content') or get_text(item, 'en', 'content')}\n\n")
            fh.write(PAGE_BREAK + "\n\n")
    return path


def extract_txt_library(entries, lang):
    ensure_dirs()
    count = 0
    for item in entries:
        cat = safe_filename(item.get("category", "uncategorized") or "uncategorized")
        topic = safe_filename(item.get("topic", "entry") or "entry")
        cat_dir = os.path.join(TXT_LIBRARY_DIR, cat)
        safe_mkdir(cat_dir)
        path = os.path.join(cat_dir, f"{topic}.txt")
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(f"Topic: {item.get('topic', '')}\n")
            fh.write(f"Category: {item.get('category', '')}\n")
            fh.write(f"Subcategory: {item.get('subcategory', '')}\n")
            fh.write(f"Tags: {', '.join(item.get('tags', []) or [])}\n")
            fh.write(f"Priority: {item.get('priority', '')}\n")
            fh.write(f"Urgency: {item.get('urgency', '')}\n")
            fh.write(f"Difficulty: {item.get('difficulty', '')}\n")
            fh.write(f"Last updated: {item.get('last_updated', '')}\n")
            fh.write(f"Update note: {item.get('update_note', '')}\n")
            fh.write(f"Source file: {item.get('_source_file', '')}\n")
            fh.write(PAGE_BREAK + "\n\n")
            fh.write("Summary\n\n")
            fh.write((get_text(item, lang, 'summary') or get_text(item, 'en', 'summary')) + "\n\n")
            fh.write("Actions\n")
            for line in get_list(item, lang, 'steps') or get_list(item, 'en', 'steps'):
                fh.write(f"- {line}\n")
            fh.write("\nWarnings\n")
            for line in get_list(item, lang, 'warnings') or get_list(item, 'en', 'warnings'):
                fh.write(f"- {line}\n")
            fh.write("\nCommon mistakes\n")
            for line in get_list(item, lang, 'mistakes') or get_list(item, 'en', 'mistakes'):
                fh.write(f"- {line}\n")
            fh.write("\nFull detail\n\n")
            fh.write((get_text(item, lang, 'content') or get_text(item, 'en', 'content')) + "\n\n")
            fh.write("Related topics\n")
            for rel in item.get('related_topics', []) or []:
                fh.write(f"- {rel}\n")
        count += 1
    return count, TXT_LIBRARY_DIR


def toggle_bookmark(item_id, bookmarks, lang):
    if item_id in bookmarks:
        bookmarks.remove(item_id)
        save_bookmarks(bookmarks)
        return UI[lang]["bookmark_removed"]
    bookmarks.append(item_id)
    save_bookmarks(bookmarks)
    return UI[lang]["bookmark_added"]


def reader(entries, items, start_index, lang, bookmarks):
    idx = start_index
    section = "4"
    while 0 <= idx < len(items):
        current = items[idx]
        render_entry(current, lang, section, bookmarks)
        print()
        print(UI[lang]["reader_help"])
        cmd = input("> ").strip().lower()
        if cmd == "n" and idx < len(items) - 1:
            idx += 1
        elif cmd == "p" and idx > 0:
            idx -= 1
        elif cmd in {"1", "2", "3", "4"}:
            section = cmd
        elif cmd == "r":
            rel = related_entries(entries, current)
            if rel:
                print()
                for i, item in enumerate(rel, 1):
                    print(f"{i}. {item.get('topic', '')} [{item.get('category', '')}]")
                pick = input(UI[lang]["choose_related"] + " ").strip()
                if pick.isdigit() and 1 <= int(pick) <= len(rel):
                    chosen = rel[int(pick) - 1]
                    if chosen in items:
                        idx = items.index(chosen)
                    else:
                        items.append(chosen)
                        idx = len(items) - 1
        elif cmd == "m":
            print(toggle_bookmark(current.get("id"), bookmarks, lang))
            pause(lang)
        elif cmd == "e":
            choice = input(UI[lang]["export_prompt"] + ": ").strip()
            try:
                path = None
                if choice == "1":
                    path = export_entries([current], lang, current.get("topic", "entry"))
                elif choice == "2":
                    path = export_entries(items, lang, "current_results")
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


def show_results(entries, ranked, profile, lang, bookmarks):
    clear()
    print_header(f"{len(ranked)} {UI[lang]['results']} - {profile['raw']}")
    for i, (score, reasons, item) in enumerate(ranked, 1):
        mark = "*" if item.get("id") in bookmarks else " "
        print(f"{mark}{i}. {item.get('topic', '')} [{item.get('category', '')}] score={score:.1f}")
        print(f"   {UI[lang]['reasons']}: {', '.join(reasons)}")
        preview = best_snippet(item, profile, lang)
        print(f"   {UI[lang]['snippet']}: {preview[:240]}{'...' if len(preview) > 240 else ''}")
    print()
    choice = input(UI[lang]["pick"] + ": ").strip()
    if choice.isdigit() and 1 <= int(choice) <= len(ranked):
        items = [item for _, _, item in ranked]
        reader(entries, items, int(choice) - 1, lang, bookmarks)


def search_mode(entries, lang, mode, bookmarks):
    label = {"keyword": UI[lang]["search"], "tag": UI[lang]["tag"], "category": UI[lang]["category"], "topic": UI[lang]["topic"]}[mode]
    query = input(label + ": ").strip()
    if not query:
        return
    add_history(query, mode)
    ranked, profile = search_entries(entries, query, mode)
    if not ranked:
        print(UI[lang]["no_results"])
        close = suggestions(entries, query)
        if close:
            print(f"\n{UI[lang]['suggestions']}: {', '.join(close)}")
        pause(lang)
        return
    show_results(entries, ranked, profile, lang, bookmarks)


def browse_group(entries, key, title, lang, bookmarks):
    values = sorted({item.get(key, "") for item in entries if item.get(key)})
    clear()
    print_header(title)
    for i, value in enumerate(values, 1):
        count = sum(1 for item in entries if item.get(key, "") == value)
        print(f"{i}. {value} ({count})")
    choice = input("\n" + (UI[lang]["pick"]) + ": ").strip()
    if choice.isdigit() and 1 <= int(choice) <= len(values):
        selected = values[int(choice) - 1]
        ranked = [(100.0, [f"{key} browse"], item) for item in entries if item.get(key, "") == selected]
        show_results(entries, ranked, {"raw": selected, "q": selected, "tokens": [], "expanded": []}, lang, bookmarks)


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
    choice = input("\n" + UI[lang]["pick"] + ": ").strip()
    if choice.isdigit() and 1 <= int(choice) <= len(saved):
        reader(entries, saved, int(choice) - 1, lang, bookmarks)


def browse_recent(entries, lang, bookmarks):
    history = load_history()
    clear()
    print_header(UI[lang]["recent"])
    if not history:
        print(UI[lang]["recent_empty"])
        pause(lang)
        return
    for i, h in enumerate(history, 1):
        print(f"{i}. [{h.get('mode')}] {h.get('query')} ({h.get('time')})")
    choice = input("\n" + UI[lang]["pick"] + ": ").strip()
    if choice.isdigit() and 1 <= int(choice) <= len(history):
        h = history[int(choice) - 1]
        ranked, profile = search_entries(entries, h.get("query", ""), h.get("mode", "keyword"))
        if ranked:
            show_results(entries, ranked, profile, lang, bookmarks)


def show_logs(lang):
    logs = list_logs()
    clear()
    print_header(UI[lang]["logs"])
    if not logs:
        print(UI[lang]["no_logs"])
        pause(lang)
        return
    for i, log in enumerate(logs, 1):
        print(f"{i}. {log}")
    choice = input("\n" + UI[lang]["pick"] + ": ").strip()
    if choice.isdigit() and 1 <= int(choice) <= len(logs):
        clear()
        print_header(logs[int(choice) - 1])
        with open(os.path.join(UPDATES_DIR, logs[int(choice) - 1]), "r", encoding="utf-8") as fh:
            print(fh.read())
        pause(lang)


def show_stats(entries, lang):
    clear()
    print_header(UI[lang]["stats"])
    file_count = len([x for x in os.listdir(DB_DIR) if x.endswith(".json")]) if os.path.isdir(DB_DIR) else 0
    categories = len({item.get("category", "") for item in entries if item.get("category")})
    topics = len({item.get("topic", "") for item in entries if item.get("topic")})
    tags = len({tag for item in entries for tag in (item.get("tags", []) or [])})
    missing = sum(1 for item in entries if any(f not in item or item.get(f) in ("", None) for f in REQUIRED_FIELDS))
    print(f"JSON files: {file_count}")
    print(f"Entries: {len(entries)}")
    print(f"Categories: {categories}")
    print(f"Topics: {topics}")
    print(f"Tags: {tags}")
    print(f"Update logs: {len(list_logs())}")
    print(f"Recent searches: {len(load_history())}")
    print(f"Runtime home: {APP_HOME}")
    print(f"TXT library: {TXT_LIBRARY_DIR}")
    print(f"Entries with missing required fields: {missing}")
    pause(lang)


def run_integrity(entries, lang):
    clear()
    print_header(UI[lang]["integrity"])
    ids = Counter(item.get("id", "") for item in entries)
    pairs = Counter((normalize(item.get("topic", "")), normalize(item.get("subcategory", ""))) for item in entries)
    dup_ids = [k for k, v in ids.items() if k and v > 1]
    dup_pairs = [k for k, v in pairs.items() if k[0] and v > 1]
    missing = [(item.get("id", "unknown"), [f for f in REQUIRED_FIELDS if f not in item or item.get(f) in ("", None)]) for item in entries]
    missing = [(a, b) for a, b in missing if b]
    if not dup_ids and not dup_pairs and not missing:
        print(UI[lang]["integrity_ok"])
    else:
        if dup_ids:
            print("Duplicate IDs:")
            for x in dup_ids[:50]:
                print("-", x)
            print()
        if dup_pairs:
            print("Duplicate topic/subcategory pairs:")
            for x in dup_pairs[:50]:
                print("-", x[0], "/", x[1])
            print()
        if missing:
            print("Missing fields:")
            for entry_id, fields in missing[:50]:
                print(f"- {entry_id}: {', '.join(fields)}")
    pause(lang)


def show_help(lang):
    clear()
    print_header(UI[lang]["help"])
    print(wrap(UI[lang]["help_text"]))
    pause(lang)


def main():
    ensure_dirs()
    lang = choose_language()
    entries = load_database()
    bookmarks = load_bookmarks()

    while True:
        clear()
        print_header(UI[lang]["welcome"])
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
            browse_group(entries, "category", UI[lang]["categories"], lang, bookmarks)
        elif choice == "6":
            browse_group(entries, "topic", UI[lang]["topics"], lang, bookmarks)
        elif choice == "7":
            browse_bookmarks(entries, lang, bookmarks)
        elif choice == "8":
            show_stats(entries, lang)
        elif choice == "9":
            show_logs(lang)
        elif choice == "10":
            run_integrity(entries, lang)
        elif choice == "11":
            show_help(lang)
        elif choice == "12":
            try:
                count, path = extract_txt_library(entries, lang)
                print(f"\n{UI[lang]['library_done']} {path} ({count} files)")
            except Exception as exc:
                print(f"\n{UI[lang]['library_failed']} {exc}")
            pause(lang)
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
