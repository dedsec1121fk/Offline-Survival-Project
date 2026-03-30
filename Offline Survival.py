
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import json
import textwrap
import difflib
from collections import defaultdict, Counter
from datetime import datetime

APP_NAME = "Offline Survival"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.join(SCRIPT_DIR, "Offline Survival Database")
UPDATES_DIR = os.path.join(SCRIPT_DIR, "Offline Survival Updates")
EXPORT_DIR = "/storage/emulated/0/Download/Offline Survival"
WRAP_WIDTH = 92

REQUIRED_FIELDS = [
    "id", "topic", "category", "subcategory", "tags",
    "summary_en", "summary_el", "content_en", "content_el",
    "steps_en", "steps_el", "warnings_en", "warnings_el",
    "mistakes_en", "mistakes_el", "related_topics",
    "difficulty", "urgency", "priority", "last_updated", "update_note"
]

UI = {
    "en": {
        "welcome": "Offline Survival - bilingual offline knowledge system",
        "choose_language": "Choose language / Επιλογή γλώσσας",
        "language_options": ["1. English", "2. Ελληνικά"],
        "invalid": "Invalid choice. Please try again.",
        "press_enter": "Press Enter to continue...",
        "main_menu": "Main menu",
        "menu_items": [
            "1. Search by keyword",
            "2. Search by tag",
            "3. Search by category",
            "4. Search by topic",
            "5. Browse all categories",
            "6. Browse all topics",
            "7. Database statistics",
            "8. Update logs",
            "9. Integrity check",
            "10. Help",
            "0. Exit"
        ],
        "prompt": "Choose an option",
        "search_term": "Enter search text",
        "tag_term": "Enter a tag",
        "category_term": "Enter a category",
        "topic_term": "Enter a topic",
        "no_results": "No matching entries were found.",
        "results_found": "results found",
        "select_result": "Open result number, or press Enter to go back",
        "reader_actions": "Commands: [n]ext  [p]revious  [r]elated  [e]xport this  [g]roup export  [b]ack",
        "select_related": "Choose a related entry number, or press Enter to stay here",
        "export_done": "Export created:",
        "export_fail": "Export failed:",
        "categories": "Categories",
        "topics": "Topics",
        "choose_category": "Choose category number, or press Enter to go back",
        "choose_topic": "Choose topic number, or press Enter to go back",
        "update_logs": "Update logs",
        "choose_log": "Choose log number, or press Enter to go back",
        "stats_title": "Database statistics",
        "integrity_title": "Integrity check",
        "help_title": "Help",
        "exit_text": "Stay safe. Preserve knowledge, discipline, and calm judgment.",
        "priority": "Priority",
        "urgency": "Urgency",
        "difficulty": "Difficulty",
        "related": "Related topics",
        "summary": "Summary",
        "steps": "Actions",
        "warnings": "Warnings",
        "mistakes": "Common mistakes",
        "update_note": "Update note",
        "last_updated": "Last updated",
        "category": "Category",
        "subcategory": "Subcategory",
        "tags": "Tags",
        "topic": "Topic",
        "help_body": (
            "This tool is designed for offline use after setup. It loads topic-based JSON files from the local "
            "'Offline Survival Database' folder and lets you search, browse, read, and export entries in English "
            "or Greek. The search system ranks exact matches first, then partial matches, then fuzzy matches. "
            "Use export when you want a plain-text copy in /storage/emulated/0/Download/Offline Survival. "
            "Medical content is practical first-aid guidance, not a substitute for a clinician when one is available. "
            "For safety, verify identity, dosage, and contamination risks before acting under stress."
        ),
        "integrity_ok": "No critical missing fields or duplicate IDs were found.",
        "integrity_missing": "Entries with missing fields",
        "integrity_dupe_ids": "Duplicate IDs",
        "integrity_dupe_topics": "Possible duplicate topic/subcategory pairs",
        "group_export_prompt": "Export [1] current result set, [2] category, [3] topic, [Enter] cancel",
        "group_export_done": "Group export created:",
        "read_entry_header": "Reading entry",
        "result_rank": "Rank",
        "integrity_entries_checked": "Entries checked",
        "stats_files": "JSON files",
        "stats_entries": "Entries",
        "stats_categories": "Unique categories",
        "stats_topics": "Unique topic names",
        "stats_tags": "Unique tags",
        "stats_updates": "Update logs",
        "stats_latest": "Latest update date",
        "stats_high_priority": "High-priority entries",
        "stats_urgent": "Urgent entries",
        "stats_missing_summary": "Entries with missing required fields",
        "empty_db": "Database folder is missing or empty.",
        "reloading": "Reloading database...",
        "dependency_msg": "Using Python standard library only. No extra packages are required."
    },
    "el": {
        "welcome": "Offline Survival - δίγλωσσο σύστημα γνώσης εκτός σύνδεσης",
        "choose_language": "Επιλογή γλώσσας / Choose language",
        "language_options": ["1. English", "2. Ελληνικά"],
        "invalid": "Μη έγκυρη επιλογή. Προσπάθησε ξανά.",
        "press_enter": "Πάτησε Enter για συνέχεια...",
        "main_menu": "Κεντρικό μενού",
        "menu_items": [
            "1. Αναζήτηση με λέξη-κλειδί",
            "2. Αναζήτηση με ετικέτα",
            "3. Αναζήτηση με κατηγορία",
            "4. Αναζήτηση με θέμα",
            "5. Περιήγηση σε όλες τις κατηγορίες",
            "6. Περιήγηση σε όλα τα θέματα",
            "7. Στατιστικά βάσης",
            "8. Αρχεία ενημερώσεων",
            "9. Έλεγχος ακεραιότητας",
            "10. Βοήθεια",
            "0. Έξοδος"
        ],
        "prompt": "Διάλεξε επιλογή",
        "search_term": "Δώσε κείμενο αναζήτησης",
        "tag_term": "Δώσε ετικέτα",
        "category_term": "Δώσε κατηγορία",
        "topic_term": "Δώσε θέμα",
        "no_results": "Δεν βρέθηκαν καταχωρήσεις που να ταιριάζουν.",
        "results_found": "αποτελέσματα βρέθηκαν",
        "select_result": "Άνοιξε αριθμό αποτελέσματος ή πάτησε Enter για επιστροφή",
        "reader_actions": "Εντολές: [n]ext επόμενο  [p]revious προηγούμενο  [r]elated σχετικά  [e]xport εξαγωγή  [g]roup ομαδική εξαγωγή  [b]ack πίσω",
        "select_related": "Διάλεξε αριθμό σχετικού θέματος ή πάτησε Enter για παραμονή εδώ",
        "export_done": "Η εξαγωγή δημιουργήθηκε:",
        "export_fail": "Η εξαγωγή απέτυχε:",
        "categories": "Κατηγορίες",
        "topics": "Θέματα",
        "choose_category": "Διάλεξε αριθμό κατηγορίας ή πάτησε Enter για επιστροφή",
        "choose_topic": "Διάλεξε αριθμό θέματος ή πάτησε Enter για επιστροφή",
        "update_logs": "Αρχεία ενημερώσεων",
        "choose_log": "Διάλεξε αριθμό αρχείου ή πάτησε Enter για επιστροφή",
        "stats_title": "Στατιστικά βάσης",
        "integrity_title": "Έλεγχος ακεραιότητας",
        "help_title": "Βοήθεια",
        "exit_text": "Μείνε ασφαλής. Διατήρησε γνώση, πειθαρχία και καθαρή κρίση.",
        "priority": "Προτεραιότητα",
        "urgency": "Επείγον",
        "difficulty": "Δυσκολία",
        "related": "Σχετικά θέματα",
        "summary": "Περίληψη",
        "steps": "Ενέργειες",
        "warnings": "Προειδοποιήσεις",
        "mistakes": "Συχνά λάθη",
        "update_note": "Σημείωση ενημέρωσης",
        "last_updated": "Τελευταία ενημέρωση",
        "category": "Κατηγορία",
        "subcategory": "Υποκατηγορία",
        "tags": "Ετικέτες",
        "topic": "Θέμα",
        "help_body": (
            "Αυτό το εργαλείο έχει σχεδιαστεί για χρήση εκτός σύνδεσης μετά την αρχική εγκατάσταση. "
            "Φορτώνει αρχεία JSON ανά θέμα από τον τοπικό φάκελο 'Offline Survival Database' και επιτρέπει "
            "αναζήτηση, περιήγηση, ανάγνωση και εξαγωγή καταχωρήσεων στα Αγγλικά ή στα Ελληνικά. "
            "Το σύστημα αναζήτησης δίνει προτεραιότητα στις ακριβείς αντιστοιχίες, μετά στις μερικές και μετά στις ασαφείς. "
            "Χρησιμοποίησε την εξαγωγή όταν θέλεις απλό αρχείο κειμένου στο /storage/emulated/0/Download/Offline Survival. "
            "Το ιατρικό περιεχόμενο παρέχει πρακτική καθοδήγηση πρώτων βοηθειών και δεν αντικαθιστά γιατρό όταν υπάρχει πρόσβαση. "
            "Για ασφάλεια, επιβεβαίωσε ταυτότητα, δοσολογία και κινδύνους μόλυνσης πριν ενεργήσεις υπό πίεση."
        ),
        "integrity_ok": "Δεν βρέθηκαν κρίσιμα ελλείποντα πεδία ή διπλά IDs.",
        "integrity_missing": "Καταχωρήσεις με ελλείποντα πεδία",
        "integrity_dupe_ids": "Διπλά IDs",
        "integrity_dupe_topics": "Πιθανές διπλές δυάδες θέματος/υποκατηγορίας",
        "group_export_prompt": "Εξαγωγή [1] τρέχοντος συνόλου, [2] κατηγορίας, [3] θέματος, [Enter] ακύρωση",
        "group_export_done": "Η ομαδική εξαγωγή δημιουργήθηκε:",
        "read_entry_header": "Ανάγνωση καταχώρησης",
        "result_rank": "Κατάταξη",
        "integrity_entries_checked": "Καταχωρήσεις που ελέγχθηκαν",
        "stats_files": "Αρχεία JSON",
        "stats_entries": "Καταχωρήσεις",
        "stats_categories": "Μοναδικές κατηγορίες",
        "stats_topics": "Μοναδικά ονόματα θεμάτων",
        "stats_tags": "Μοναδικές ετικέτες",
        "stats_updates": "Αρχεία ενημερώσεων",
        "stats_latest": "Νεότερη ημερομηνία ενημέρωσης",
        "stats_high_priority": "Καταχωρήσεις υψηλής προτεραιότητας",
        "stats_urgent": "Επείγουσες καταχωρήσεις",
        "stats_missing_summary": "Καταχωρήσεις με ελλείποντα απαιτούμενα πεδία",
        "empty_db": "Ο φάκελος της βάσης λείπει ή είναι κενός.",
        "reloading": "Επαναφόρτωση βάσης...",
        "dependency_msg": "Χρησιμοποιείται μόνο η βασική βιβλιοθήκη της Python. Δεν απαιτούνται επιπλέον πακέτα."
    }
}

def clear():
    os.system("clear")

def wrap(text, width=WRAP_WIDTH):
    lines = []
    for paragraph in str(text).splitlines():
        if not paragraph.strip():
            lines.append("")
            continue
        lines.extend(textwrap.fill(paragraph, width=width).splitlines())
    return "\n".join(lines)

def pause(lang):
    input("\n" + UI[lang]["press_enter"])

def choose_language():
    while True:
        clear()
        print("=" * WRAP_WIDTH)
        print("Offline Survival")
        print("=" * WRAP_WIDTH)
        print(UI["en"]["choose_language"])
        for line in UI["en"]["language_options"]:
            print(line)
        choice = input("> ").strip()
        if choice == "1":
            return "en"
        if choice == "2":
            return "el"

def safe_mkdir(path):
    os.makedirs(path, exist_ok=True)

def normalize(text):
    return " ".join(str(text).lower().strip().split())

def load_database():
    entries = []
    if not os.path.isdir(DB_DIR):
        return entries
    for filename in sorted(os.listdir(DB_DIR)):
        if not filename.lower().endswith(".json"):
            continue
        path = os.path.join(DB_DIR, filename)
        try:
            with open(path, "r", encoding="utf-8") as handle:
                data = json.load(handle)
            if isinstance(data, dict):
                data = [data]
            if not isinstance(data, list):
                continue
            for item in data:
                if isinstance(item, dict):
                    item["_source_file"] = filename
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
                "steps_en": [],
                "steps_el": [],
                "warnings_en": ["Broken data file."],
                "warnings_el": ["Κατεστραμμένο αρχείο δεδομένων."],
                "mistakes_en": [],
                "mistakes_el": [],
                "related_topics": [],
                "difficulty": "low",
                "urgency": "medium",
                "priority": "high",
                "last_updated": "",
                "update_note": "Auto-generated error placeholder.",
                "_source_file": filename
            })
    return entries

def list_update_logs():
    if not os.path.isdir(UPDATES_DIR):
        return []
    return sorted([name for name in os.listdir(UPDATES_DIR) if name.lower().endswith(".txt")])

def detect_latest_date(entries):
    dates = []
    for item in entries:
        date = str(item.get("last_updated", "")).strip()
        if date:
            dates.append(date)
    return max(dates) if dates else "n/a"

def database_stats(entries):
    categories = set(); topics = set(); tags = set(); missing = 0; high_priority = 0; urgent = 0
    for item in entries:
        categories.add(item.get("category", "")); topics.add(item.get("topic", ""))
        for tag in item.get("tags", []) or []: tags.add(str(tag))
        if any(field not in item or item.get(field) in ("", None) for field in REQUIRED_FIELDS): missing += 1
        if normalize(item.get("priority", "")) == "high": high_priority += 1
        if normalize(item.get("urgency", "")) in {"high", "critical"}: urgent += 1
    return {"files": len([name for name in os.listdir(DB_DIR) if name.endswith(".json")]) if os.path.isdir(DB_DIR) else 0, "entries": len(entries), "categories": len([x for x in categories if x]), "topics": len([x for x in topics if x]), "tags": len([x for x in tags if x]), "updates": len(list_update_logs()), "latest": detect_latest_date(entries), "high_priority": high_priority, "urgent": urgent, "missing": missing}

def integrity_check(entries):
    missing = []; id_counter = Counter(); topic_pairs = Counter()
    for item in entries:
        missing_fields = [field for field in REQUIRED_FIELDS if field not in item or item.get(field) in ("", None)]
        if missing_fields: missing.append((item.get("id", "unknown"), missing_fields))
        id_counter[item.get("id", "")] += 1
        pair = (normalize(item.get("topic", "")), normalize(item.get("subcategory", "")))
        topic_pairs[pair] += 1
    dupe_ids = [key for key, count in id_counter.items() if key and count > 1]
    dupe_topics = [pair for pair, count in topic_pairs.items() if pair[0] and count > 1]
    return missing, dupe_ids, dupe_topics

def get_text(item, lang, field_base):
    field = f"{field_base}_{lang}"; value = item.get(field, "")
    if isinstance(value, list): return value
    return value

def entry_blob_for_search(item):
    pieces = [item.get("topic", ""), item.get("category", ""), item.get("subcategory", ""), " ".join(item.get("tags", []) or []), item.get("summary_en", ""), item.get("summary_el", ""), item.get("content_en", ""), item.get("content_el", ""), " ".join(item.get("steps_en", []) or []), " ".join(item.get("steps_el", []) or [])]
    return normalize(" ".join(pieces))

def score_entry(item, query, mode):
    q = normalize(query)
    if not q: return 0.0
    score = 0.0
    topic = normalize(item.get("topic", "")); category = normalize(item.get("category", "")); subcategory = normalize(item.get("subcategory", "")); tags = [normalize(tag) for tag in item.get("tags", []) or []]; blob = entry_blob_for_search(item)
    if mode == "tag":
        if q in tags: score += 150
        for tag in tags:
            if q in tag: score += 90
            score += difflib.SequenceMatcher(None, q, tag).ratio() * 40
    elif mode == "category":
        if q == category: score += 150
        if q in category: score += 90
        score += difflib.SequenceMatcher(None, q, category).ratio() * 40
    elif mode == "topic":
        if q == topic: score += 170
        if q in topic: score += 100
        score += difflib.SequenceMatcher(None, q, topic).ratio() * 50
    else:
        if q == topic: score += 200
        if q in topic: score += 120
        if q == category or q == subcategory: score += 100
        if q in category or q in subcategory: score += 70
        if q in tags: score += 80
        if q in blob: score += 60
        score += difflib.SequenceMatcher(None, q, topic).ratio() * 35
        score += difflib.SequenceMatcher(None, q, blob[:500]).ratio() * 20
    if normalize(item.get("priority", "")) == "high": score += 5
    if normalize(item.get("urgency", "")) in {"high", "critical"}: score += 5
    return score

def search_entries(entries, query, mode="keyword"):
    ranked = []
    for item in entries:
        score = score_entry(item, query, mode)
        if score >= 30: ranked.append((score, item))
    ranked.sort(key=lambda pair: (-pair[0], pair[1].get("topic", "")))
    return ranked

def related_entries(entries, item):
    related_names = {normalize(name) for name in item.get("related_topics", []) or []}; results = []
    for other in entries:
        if other.get("id") == item.get("id"): continue
        topic = normalize(other.get("topic", ""))
        if topic in related_names: results.append(other)
    return results

def print_header(title):
    print("=" * WRAP_WIDTH); print(title); print("=" * WRAP_WIDTH)

def print_entry(item, lang, index_label=None):
    title = item.get("topic", "")
    if index_label: title = f"{index_label} - {title}"
    print_header(title)
    print(f"{UI[lang]['category']}: {item.get('category', '')}")
    print(f"{UI[lang]['subcategory']}: {item.get('subcategory', '')}")
    print(f"{UI[lang]['tags']}: {', '.join(item.get('tags', []) or [])}")
    print(f"{UI[lang]['priority']}: {item.get('priority', '')} | {UI[lang]['urgency']}: {item.get('urgency', '')} | {UI[lang]['difficulty']}: {item.get('difficulty', '')}")
    print(f"{UI[lang]['last_updated']}: {item.get('last_updated', '')}")
    print(f"{UI[lang]['update_note']}: {item.get('update_note', '')}")
    print(); print(f"[{UI[lang]['summary']}]" ); print(wrap(get_text(item, lang, "summary"))); print(); print(f"[{UI[lang]['steps']}]" )
    for step in get_text(item, lang, "steps") or []: print("- " + wrap(step))
    print(); print(f"[{UI[lang]['warnings']}]" )
    for line in get_text(item, lang, "warnings") or []: print("- " + wrap(line))
    print(); print(f"[{UI[lang]['mistakes']}]" )
    for line in get_text(item, lang, "mistakes") or []: print("- " + wrap(line))
    print(); print(f"[{UI[lang]['topic']}]" ); print(wrap(get_text(item, lang, "content"))); print(); rel = item.get("related_topics", []) or []; print(f"{UI[lang]['related']}: {', '.join(rel) if rel else '-'}")

def export_entries(entries_to_export, lang, file_label):
    safe_mkdir(EXPORT_DIR)
    safe_name = "".join(c if c.isalnum() or c in ("_", "-", " ") else "_" for c in file_label).strip() or "export"
    path = os.path.join(EXPORT_DIR, f"{safe_name}.txt")
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(f"{APP_NAME} Export\n"); handle.write(f"Language: {'English' if lang == 'en' else 'Greek'}\n"); handle.write(f"Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"); handle.write("=" * WRAP_WIDTH + "\n\n")
        for idx, item in enumerate(entries_to_export, 1):
            handle.write(f"{idx}. {item.get('topic', '')}\n"); handle.write(f"{UI[lang]['category']}: {item.get('category', '')}\n"); handle.write(f"{UI[lang]['subcategory']}: {item.get('subcategory', '')}\n"); handle.write(f"{UI[lang]['tags']}: {', '.join(item.get('tags', []) or [])}\n"); handle.write(f"{UI[lang]['priority']}: {item.get('priority', '')} | {UI[lang]['urgency']}: {item.get('urgency', '')} | {UI[lang]['difficulty']}: {item.get('difficulty', '')}\n"); handle.write(f"{UI[lang]['summary']}:\n{get_text(item, lang, 'summary')}\n\n"); handle.write(f"{UI[lang]['topic']}:\n{get_text(item, lang, 'content')}\n\n"); handle.write(f"{UI[lang]['steps']}:\n")
            for step in get_text(item, lang, "steps") or []: handle.write(f"- {step}\n")
            handle.write(f"\n{UI[lang]['warnings']}:\n")
            for line in get_text(item, lang, "warnings") or []: handle.write(f"- {line}\n")
            handle.write(f"\n{UI[lang]['mistakes']}:\n")
            for line in get_text(item, lang, "mistakes") or []: handle.write(f"- {line}\n")
            handle.write("\n" + "=" * WRAP_WIDTH + "\n\n")
    return path

def show_ranked_results(entries, ranked, lang):
    clear(); print_header(f"{len(ranked)} {UI[lang]['results_found']}")
    for idx, (score, item) in enumerate(ranked, 1):
        summary = get_text(item, lang, "summary") or get_text(item, "en", "summary")
        summary = summary[:140] + ("..." if len(summary) > 140 else "")
        print(f"{idx}. {item.get('topic', '')}  [{item.get('category', '')}]  ({UI[lang]['result_rank']}: {score:.1f})"); print("   " + summary)
    print(); choice = input(UI[lang]["select_result"] + ": ").strip()
    if not choice: return
    if choice.isdigit():
        num = int(choice)
        if 1 <= num <= len(ranked): navigate_entries(entries, [item for _, item in ranked], num - 1, lang)

def navigate_entries(all_entries, result_items, start_index, lang):
    index = start_index
    while 0 <= index < len(result_items):
        clear(); current = result_items[index]; print_entry(current, lang, index_label=f"{UI[lang]['read_entry_header']} {index + 1}/{len(result_items)}"); print(); print(UI[lang]["reader_actions"]); command = input("> ").strip().lower()
        if command == "n":
            if index < len(result_items) - 1: index += 1
        elif command == "p":
            if index > 0: index -= 1
        elif command == "r":
            rel = related_entries(all_entries, current)
            if not rel: continue
            print()
            for num, item in enumerate(rel, 1): print(f"{num}. {item.get('topic', '')} [{item.get('category', '')}]")
            pick = input(UI[lang]["select_related"] + ": ").strip()
            if pick.isdigit():
                rel_num = int(pick)
                if 1 <= rel_num <= len(rel):
                    target = rel[rel_num - 1]
                    if target in result_items: index = result_items.index(target)
                    else:
                        result_items.append(target); index = len(result_items) - 1
        elif command == "e":
            try:
                path = export_entries([current], lang, current.get("topic", "entry")); print(f"\n{UI[lang]['export_done']} {path}")
            except Exception as exc:
                print(f"\n{UI[lang]['export_fail']} {exc}")
            pause(lang)
        elif command == "g": do_group_export(all_entries, result_items, current, lang)
        elif command == "b" or command == "": return

def do_group_export(all_entries, current_results, current_item, lang):
    print(); choice = input(UI[lang]["group_export_prompt"] + ": ").strip()
    if choice == "1": items = current_results; label = "current_results"
    elif choice == "2": items = [x for x in all_entries if normalize(x.get("category", "")) == normalize(current_item.get("category", ""))]; label = f"category_{current_item.get('category', '')}"
    elif choice == "3": items = [x for x in all_entries if normalize(x.get("topic", "")) == normalize(current_item.get("topic", ""))]; label = f"topic_{current_item.get('topic', '')}"
    else: return
    try:
        path = export_entries(items, lang, label); print(f"\n{UI[lang]['group_export_done']} {path}")
    except Exception as exc:
        print(f"\n{UI[lang]['export_fail']} {exc}")
    pause(lang)

def browse_categories(entries, lang):
    categories = sorted({item.get("category", "") for item in entries if item.get("category")}); clear(); print_header(UI[lang]["categories"])
    for idx, category in enumerate(categories, 1):
        count = sum(1 for item in entries if item.get("category", "") == category); print(f"{idx}. {category} ({count})")
    choice = input("\n" + UI[lang]["choose_category"] + ": ").strip()
    if choice.isdigit():
        num = int(choice)
        if 1 <= num <= len(categories):
            category = categories[num - 1]; ranked = [(100.0, item) for item in entries if item.get("category", "") == category]; show_ranked_results(entries, ranked, lang)

def browse_topics(entries, lang):
    topic_map = {}
    for item in entries: topic_map.setdefault(item.get("topic", ""), []).append(item)
    topics = sorted(topic_map.keys()); clear(); print_header(UI[lang]["topics"])
    for idx, topic in enumerate(topics, 1): print(f"{idx}. {topic} ({len(topic_map[topic])})")
    choice = input("\n" + UI[lang]["choose_topic"] + ": ").strip()
    if choice.isdigit():
        num = int(choice)
        if 1 <= num <= len(topics):
            topic = topics[num - 1]; ranked = [(100.0, item) for item in topic_map[topic]]; show_ranked_results(entries, ranked, lang)

def show_stats(entries, lang):
    stats = database_stats(entries); clear(); print_header(UI[lang]["stats_title"])
    print(f"{UI[lang]['stats_files']}: {stats['files']}"); print(f"{UI[lang]['stats_entries']}: {stats['entries']}"); print(f"{UI[lang]['stats_categories']}: {stats['categories']}"); print(f"{UI[lang]['stats_topics']}: {stats['topics']}"); print(f"{UI[lang]['stats_tags']}: {stats['tags']}"); print(f"{UI[lang]['stats_updates']}: {stats['updates']}"); print(f"{UI[lang]['stats_latest']}: {stats['latest']}"); print(f"{UI[lang]['stats_high_priority']}: {stats['high_priority']}"); print(f"{UI[lang]['stats_urgent']}: {stats['urgent']}"); print(f"{UI[lang]['stats_missing_summary']}: {stats['missing']}"); pause(lang)

def show_update_logs(lang):
    logs = list_update_logs(); clear(); print_header(UI[lang]["update_logs"])
    for idx, name in enumerate(logs, 1): print(f"{idx}. {name}")
    choice = input("\n" + UI[lang]["choose_log"] + ": ").strip()
    if not choice: return
    if choice.isdigit():
        num = int(choice)
        if 1 <= num <= len(logs):
            path = os.path.join(UPDATES_DIR, logs[num - 1]); clear(); print_header(logs[num - 1])
            with open(path, "r", encoding="utf-8") as handle: print(handle.read())
            pause(lang)

def run_integrity(entries, lang):
    missing, dupe_ids, dupe_topics = integrity_check(entries); clear(); print_header(UI[lang]["integrity_title"]); print(f"{UI[lang]['integrity_entries_checked']}: {len(entries)}\n")
    if not missing and not dupe_ids and not dupe_topics:
        print(UI[lang]["integrity_ok"]); pause(lang); return
    if missing:
        print(UI[lang]["integrity_missing"] + ":")
        for item_id, fields in missing[:25]: print(f"- {item_id}: {', '.join(fields)}")
        if len(missing) > 25: print(f"... +{len(missing) - 25} more")
        print()
    if dupe_ids:
        print(UI[lang]["integrity_dupe_ids"] + ":")
        for value in dupe_ids[:25]: print(f"- {value}")
        if len(dupe_ids) > 25: print(f"... +{len(dupe_ids) - 25} more")
        print()
    if dupe_topics:
        print(UI[lang]["integrity_dupe_topics"] + ":")
        for topic, subcategory in dupe_topics[:25]: print(f"- {topic} / {subcategory}")
        if len(dupe_topics) > 25: print(f"... +{len(dupe_topics) - 25} more")
    pause(lang)

def run_search(entries, lang, mode):
    label_map = {"keyword": UI[lang]["search_term"], "tag": UI[lang]["tag_term"], "category": UI[lang]["category_term"], "topic": UI[lang]["topic_term"]}
    query = input(label_map[mode] + ": ").strip()
    if not query: return
    ranked = search_entries(entries, query, mode=mode)
    if not ranked:
        print(UI[lang]["no_results"]); pause(lang); return
    show_ranked_results(entries, ranked, lang)

def print_help(lang):
    clear(); print_header(UI[lang]["help_title"]); print(wrap(UI[lang]["help_body"])); print(); print(wrap(UI[lang]["dependency_msg"])); pause(lang)

def main():
    lang = choose_language(); safe_mkdir(DB_DIR); safe_mkdir(UPDATES_DIR); entries = load_database()
    while True:
        clear(); print_header(UI[lang]["welcome"]); print(UI[lang]["dependency_msg"]); print()
        if not entries:
            print(UI[lang]["empty_db"]); print()
        print(UI[lang]["main_menu"])
        for line in UI[lang]["menu_items"]: print(line)
        choice = input("\n" + UI[lang]["prompt"] + ": ").strip().lower()
        if choice == "1": run_search(entries, lang, "keyword")
        elif choice == "2": run_search(entries, lang, "tag")
        elif choice == "3": run_search(entries, lang, "category")
        elif choice == "4": run_search(entries, lang, "topic")
        elif choice == "5": browse_categories(entries, lang)
        elif choice == "6": browse_topics(entries, lang)
        elif choice == "7": show_stats(entries, lang)
        elif choice == "8": show_update_logs(lang)
        elif choice == "9": run_integrity(entries, lang)
        elif choice == "10": print_help(lang)
        elif choice == "reload":
            print(UI[lang]["reloading"]); entries = load_database(); pause(lang)
        elif choice == "lang": lang = "el" if lang == "en" else "en"
        elif choice == "0":
            clear(); print(UI[lang]["exit_text"]); break
        else:
            print(UI[lang]["invalid"]); pause(lang)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExit requested.")
