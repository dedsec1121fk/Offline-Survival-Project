#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Offline Survival — Pass 100 expanded, audited bilingual Termux knowledge reader."""

import hashlib
import json
import os
import random
import re
import socket
import sqlite3
import subprocess
import sys
import textwrap
import unicodedata
import webbrowser
from collections import Counter, defaultdict
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from threading import Thread
from urllib.parse import parse_qs, urlparse

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.join(BASE_DIR, "Offline Survival Database")
UPDATES_DIR = os.path.join(BASE_DIR, "Offline Survival Updates")
EXPORT_DIR_NAME = "Offline Survival Exports"
STATE_FILE = os.path.join(BASE_DIR, ".offline_survival_user_state.json")
SEARCH_INDEX_FILE = os.path.join(BASE_DIR, "Offline Survival Search Index.sqlite3")
WEB_HOST = "127.0.0.1"
WEB_PORT_START = 8765
WEB_PORT_END = 8775

TEXT_KEYS = [
    "id", "topic", "topic_en", "topic_el", "category", "subcategory",
    "category_en", "category_el", "subcategory_en", "subcategory_el",
    "summary_en", "summary_el", "content_en", "content_el", "difficulty",
    "urgency", "priority", "last_updated", "update_note", "update_note_en",
    "update_note_el", "short_term_en", "short_term_el", "long_term_en",
    "long_term_el", "if_method_fails_en", "if_method_fails_el",
    "environment_notes_en", "environment_notes_el",
]
LIST_KEYS = [
    "tags", "steps_en", "steps_el", "warnings_en", "warnings_el",
    "mistakes_en", "mistakes_el", "related_topics", "related_topics_en",
    "related_topics_el", "materials_en",
    "materials_el", "alternatives_en", "alternatives_el", "failure_signs_en",
    "failure_signs_el", "when_not_to_use_en", "when_not_to_use_el", "sources",
]
PAIR_REQUIRED = [
    ("topic_en", "topic_el"), ("summary_en", "summary_el"),
    ("content_en", "content_el"), ("steps_en", "steps_el"),
    ("warnings_en", "warnings_el"), ("mistakes_en", "mistakes_el"),
    ("materials_en", "materials_el"), ("alternatives_en", "alternatives_el"),
    ("failure_signs_en", "failure_signs_el"),
    ("when_not_to_use_en", "when_not_to_use_el"),
    ("short_term_en", "short_term_el"), ("long_term_en", "long_term_el"),
    ("if_method_fails_en", "if_method_fails_el"),
    ("environment_notes_en", "environment_notes_el"),
    ("category_en", "category_el"), ("subcategory_en", "subcategory_el"),
    ("related_topics_en", "related_topics_el"),
]

I18N = {
    "en": {
        "app": "Offline Survival",
        "language": "Language",
        "entries_loaded": "Entries loaded",
        "search": "Search",
        "browse_topics": "Browse topics",
        "browse_files": "Browse database files",
        "browse_categories": "Browse categories",
        "quick_emergency": "Quick emergency cards",
        "scenario_packs": "Guided emergency packs",
        "emergency_helper": "What is happening now?",
        "recent": "Recently viewed",
        "emergency_numbers": "Greece: 112 emergency • Poison Centre: 210 7793777",
        "favorites": "Favorites",
        "readiness": "Preparedness self-check",
        "plan_builder": "Build a one-page emergency plan",
        "browser": "Launch local browser interface",
        "statistics": "Database statistics",
        "integrity": "Integrity and translation audit",
        "updates": "Update logs",
        "official_sources": "Official safety-source guide",
        "sources_missing": "Entries without reference sources",
        "placeholder_topics": "Numbered placeholder topics",
        "switch_language": "Switch language",
        "reload": "Reload database",
        "export": "Export knowledge",
        "exit": "Exit",
        "return": "Return",
        "query": "Search query",
        "no_entries": "No entries found.",
        "entries": "Entries",
        "showing": "Showing",
        "of": "of",
        "read_prompt": "Enter a number to read, N for next, P for previous, F to favorite, or Enter to return.",
        "invalid": "Invalid choice.",
        "press_enter": "Press Enter to continue...",
        "category": "Category",
        "subcategory": "Subcategory",
        "source_file": "Source file",
        "difficulty": "Difficulty",
        "urgency": "Urgency",
        "priority": "Priority",
        "last_updated": "Last updated",
        "summary": "Summary",
        "core_reading": "Core reading",
        "materials": "Materials",
        "steps": "Steps",
        "alternatives": "Alternatives",
        "warnings": "Warnings",
        "failure_signs": "Failure signs",
        "when_not_to_use": "When not to use",
        "mistakes": "Common mistakes",
        "short_term": "Short-term considerations",
        "long_term": "Long-term considerations",
        "if_method_fails": "If the method fails",
        "environment_notes": "Environment notes",
        "related_topics": "Related topics",
        "sources": "Official/reference sources",
        "update_note": "Update note",
        "add_favorite": "Added to favorites",
        "remove_favorite": "Removed from favorites",
        "empty_favorites": "No favorites saved yet.",
        "files": "Database files",
        "categories": "Categories",
        "choose_number": "Enter a number to inspect, or press Enter to return.",
        "stats_title": "Database statistics",
        "top_categories": "Top categories",
        "integrity_title": "Integrity and translation audit",
        "duplicate_ids": "Duplicate IDs",
        "duplicate_topics": "Duplicate English topics",
        "duplicate_topics_el": "Duplicate Greek topics",
        "duplicate_blocks": "Exact duplicate long bilingual blocks",
        "repeated_core_text": "Exact repeated core text across different entries",
        "missing_pairs": "Missing bilingual pairs",
        "load_errors": "Load errors",
        "ascii_leaks": "Reviewable English leakage in Greek fields",
        "legacy_template_flags": "Legacy generic-template signatures",
        "semantic_mismatches": "Domain and guidance mismatches",
        "shallow_entries": "Entries below minimum practical depth",
        "clean_audit": "No integrity defects detected by the current audit.",
        "update_logs": "Update logs",
        "no_logs": "No update logs found.",
        "web_started": "Local browser interface started at",
        "web_stop": "Press Enter here to stop the local server and return to the menu.",
        "web_failed": "Could not start the local web interface on the available ports.",
        "database_reloaded": "Database reloaded.",
        "export_title": "Export knowledge",
        "export_all": "Export the entire database",
        "export_search": "Export search results",
        "export_category": "Export one category",
        "export_file": "Export one database file",
        "export_favorites": "Export favorites",
        "export_quick": "Export quick emergency pack",
        "export_both": "Export current selection in both languages",
        "exported": "Exported",
        "to": "to",
        "nothing_export": "There are no entries to export.",
        "quick_note": "High-priority and urgent entries are shown first. Official instructions and emergency services override this guide.",
        "readiness_title": "Preparedness self-check",
        "yes_no": "Answer y/n",
        "score": "Score",
        "recommendations": "Priority improvements",
        "saved_report": "Saved report",
        "plan_title": "One-page emergency plan",
        "household": "Household or group name",
        "primary_meeting": "Primary meeting point",
        "backup_meeting": "Backup meeting point",
        "outside_contact": "Out-of-area contact",
        "emergency_contacts": "Local emergency contacts",
        "medical_needs": "Medicines, allergies, disabilities, or medical-device needs",
        "pets": "Pets or livestock",
        "evacuation": "Primary and backup evacuation routes",
        "utilities": "Utility shutoff boundaries and qualified contacts",
        "supplies_location": "Location of water, kits, documents, and keys",
        "notes": "Other critical notes",
        "plan_saved": "Emergency plan saved",
        "choose_language": "Choose language / Επιλογή γλώσσας",
    },
    "el": {
        "app": "Offline Survival / Επιβίωση Χωρίς Σύνδεση",
        "language": "Γλώσσα",
        "entries_loaded": "Φορτωμένες εγγραφές",
        "search": "Αναζήτηση",
        "browse_topics": "Περιήγηση θεμάτων",
        "browse_files": "Περιήγηση αρχείων βάσης",
        "browse_categories": "Περιήγηση κατηγοριών",
        "quick_emergency": "Γρήγορες κάρτες έκτακτης ανάγκης",
        "scenario_packs": "Καθοδηγούμενα πακέτα έκτακτης ανάγκης",
        "emergency_helper": "Τι συμβαίνει τώρα;",
        "recent": "Πρόσφατα θέματα",
        "emergency_numbers": "Ελλάδα: 112 έκτακτη ανάγκη • Κέντρο Δηλητηριάσεων: 210 7793777",
        "favorites": "Αγαπημένα",
        "readiness": "Αυτοέλεγχος ετοιμότητας",
        "plan_builder": "Δημιουργία μονοσέλιδου σχεδίου ανάγκης",
        "browser": "Άνοιγμα τοπικού περιβάλλοντος περιήγησης",
        "statistics": "Στατιστικά βάσης",
        "integrity": "Έλεγχος ακεραιότητας και μετάφρασης",
        "updates": "Αρχεία ενημερώσεων",
        "official_sources": "Οδηγός επίσημων πηγών ασφάλειας",
        "sources_missing": "Εγγραφές χωρίς πηγές αναφοράς",
        "placeholder_topics": "Αριθμημένα προσωρινά θέματα",
        "switch_language": "Αλλαγή γλώσσας",
        "reload": "Επαναφόρτωση βάσης",
        "export": "Εξαγωγή γνώσης",
        "exit": "Έξοδος",
        "return": "Επιστροφή",
        "query": "Όρος αναζήτησης",
        "no_entries": "Δεν βρέθηκαν εγγραφές.",
        "entries": "Εγγραφές",
        "showing": "Εμφάνιση",
        "of": "από",
        "read_prompt": "Γράψε αριθμό για ανάγνωση, N για επόμενα, P για προηγούμενα, F για αγαπημένο ή Enter για επιστροφή.",
        "invalid": "Μη έγκυρη επιλογή.",
        "press_enter": "Πάτησε Enter για συνέχεια...",
        "category": "Κατηγορία",
        "subcategory": "Υποκατηγορία",
        "source_file": "Αρχείο προέλευσης",
        "difficulty": "Δυσκολία",
        "urgency": "Επείγον",
        "priority": "Προτεραιότητα",
        "last_updated": "Τελευταία ενημέρωση",
        "summary": "Σύνοψη",
        "core_reading": "Κύριο κείμενο",
        "materials": "Υλικά",
        "steps": "Βήματα",
        "alternatives": "Εναλλακτικές",
        "warnings": "Προειδοποιήσεις",
        "failure_signs": "Σημάδια αποτυχίας",
        "when_not_to_use": "Πότε να μη χρησιμοποιηθεί",
        "mistakes": "Συχνά λάθη",
        "short_term": "Βραχυπρόθεσμες παρατηρήσεις",
        "long_term": "Μακροπρόθεσμες παρατηρήσεις",
        "if_method_fails": "Αν αποτύχει η μέθοδος",
        "environment_notes": "Σημειώσεις περιβάλλοντος",
        "related_topics": "Σχετικά θέματα",
        "sources": "Επίσημες/βοηθητικές πηγές",
        "update_note": "Σημείωση ενημέρωσης",
        "add_favorite": "Προστέθηκε στα αγαπημένα",
        "remove_favorite": "Αφαιρέθηκε από τα αγαπημένα",
        "empty_favorites": "Δεν υπάρχουν αποθηκευμένα αγαπημένα.",
        "files": "Αρχεία βάσης",
        "categories": "Κατηγορίες",
        "choose_number": "Γράψε αριθμό για προβολή ή Enter για επιστροφή.",
        "stats_title": "Στατιστικά βάσης",
        "top_categories": "Μεγαλύτερες κατηγορίες",
        "integrity_title": "Έλεγχος ακεραιότητας και μετάφρασης",
        "duplicate_ids": "Διπλότυπα ID",
        "duplicate_topics": "Διπλότυποι αγγλικοί τίτλοι",
        "duplicate_topics_el": "Διπλότυποι ελληνικοί τίτλοι",
        "duplicate_blocks": "Ακριβώς διπλότυπα μεγάλα δίγλωσσα κείμενα",
        "repeated_core_text": "Ακριβώς επαναλαμβανόμενο κύριο κείμενο μεταξύ διαφορετικών εγγραφών",
        "missing_pairs": "Ελλιπή δίγλωσσα ζεύγη",
        "load_errors": "Σφάλματα φόρτωσης",
        "ascii_leaks": "Αγγλικό κείμενο προς έλεγχο σε ελληνικά πεδία",
        "legacy_template_flags": "Υπογραφές παλιού γενικού προτύπου",
        "semantic_mismatches": "Αναντιστοιχίες τομέα και οδηγιών",
        "shallow_entries": "Εγγραφές κάτω από το ελάχιστο πρακτικό βάθος",
        "clean_audit": "Δεν εντοπίστηκαν προβλήματα ακεραιότητας από τον τρέχοντα έλεγχο.",
        "update_logs": "Αρχεία ενημερώσεων",
        "no_logs": "Δεν βρέθηκαν αρχεία ενημερώσεων.",
        "web_started": "Το τοπικό περιβάλλον ξεκίνησε στη διεύθυνση",
        "web_stop": "Πάτησε Enter εδώ για διακοπή του διακομιστή και επιστροφή στο μενού.",
        "web_failed": "Δεν ήταν δυνατή η εκκίνηση του τοπικού περιβάλλοντος στις διαθέσιμες θύρες.",
        "database_reloaded": "Η βάση επαναφορτώθηκε.",
        "export_title": "Εξαγωγή γνώσης",
        "export_all": "Εξαγωγή ολόκληρης βάσης",
        "export_search": "Εξαγωγή αποτελεσμάτων αναζήτησης",
        "export_category": "Εξαγωγή μιας κατηγορίας",
        "export_file": "Εξαγωγή ενός αρχείου βάσης",
        "export_favorites": "Εξαγωγή αγαπημένων",
        "export_quick": "Εξαγωγή γρήγορου πακέτου ανάγκης",
        "export_both": "Εξαγωγή τρέχουσας επιλογής και στις δύο γλώσσες",
        "exported": "Έγινε εξαγωγή",
        "to": "στο",
        "nothing_export": "Δεν υπάρχουν εγγραφές για εξαγωγή.",
        "quick_note": "Οι εγγραφές υψηλής προτεραιότητας εμφανίζονται πρώτες. Οι επίσημες οδηγίες και οι υπηρεσίες ανάγκης υπερισχύουν του οδηγού.",
        "readiness_title": "Αυτοέλεγχος ετοιμότητας",
        "yes_no": "Απάντησε y/n",
        "score": "Βαθμολογία",
        "recommendations": "Βελτιώσεις προτεραιότητας",
        "saved_report": "Αποθηκευμένη αναφορά",
        "plan_title": "Μονοσέλιδο σχέδιο έκτακτης ανάγκης",
        "household": "Όνομα νοικοκυριού ή ομάδας",
        "primary_meeting": "Κύριο σημείο συνάντησης",
        "backup_meeting": "Εφεδρικό σημείο συνάντησης",
        "outside_contact": "Επαφή εκτός περιοχής",
        "emergency_contacts": "Τοπικές επαφές έκτακτης ανάγκης",
        "medical_needs": "Φάρμακα, αλλεργίες, αναπηρίες ή ανάγκες ιατρικών συσκευών",
        "pets": "Κατοικίδια ή ζώα εκτροφής",
        "evacuation": "Κύρια και εφεδρική διαδρομή εκκένωσης",
        "utilities": "Όρια διακοπής παροχών και ειδικευμένες επαφές",
        "supplies_location": "Θέση νερού, κιτ, εγγράφων και κλειδιών",
        "notes": "Άλλες κρίσιμες σημειώσεις",
        "plan_saved": "Το σχέδιο ανάγκης αποθηκεύτηκε",
        "choose_language": "Choose language / Επιλογή γλώσσας",
    },
}


def tr(lang, key):
    return I18N.get(lang, I18N["en"]).get(key, I18N["en"].get(key, key))


def clear():
    os.system("clear" if os.name != "nt" else "cls")


def safe_text(value):
    return "" if value is None else str(value).strip()


def safe_list(value):
    values = value if isinstance(value, list) else ([] if value is None else [value])
    out, seen = [], set()
    for item in values:
        text = safe_text(item)
        key = unicodedata.normalize("NFKC", text).casefold()
        if text and key not in seen:
            seen.add(key)
            out.append(text)
    return out


def normalize_search(value):
    text = unicodedata.normalize("NFKD", safe_text(value).casefold())
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    text = re.sub(r"[^\w]+", " ", text, flags=re.UNICODE)
    return re.sub(r"\s+", " ", text).strip()


def pause(lang="en", message=None):
    try:
        input(message or "\n" + tr(lang, "press_enter"))
    except EOFError:
        pass


def load_state():
    try:
        with open(STATE_FILE, "r", encoding="utf-8") as fh:
            state = json.load(fh)
        if not isinstance(state, dict):
            raise ValueError("state is not an object")
    except Exception:
        state = {}
    state.setdefault("favorites", [])
    state.setdefault("recent", [])
    state.setdefault("language", "en")
    return state


def save_state(state):
    try:
        with open(STATE_FILE, "w", encoding="utf-8") as fh:
            json.dump(state, fh, ensure_ascii=False, indent=2)
    except OSError:
        pass


STATE = load_state()


class OfflineSurvivalStore:
    def __init__(self):
        self.entries = []
        self.by_id = {}
        self.by_file = defaultdict(list)
        self.by_category = defaultdict(list)
        self.load_errors = []
        self.last_loaded_files = []
        self.search_index_ready = False

    def normalize_entry(self, raw, source_file):
        e = dict(raw) if isinstance(raw, dict) else {}
        for key in TEXT_KEYS:
            e[key] = safe_text(e.get(key))
        for key in LIST_KEYS:
            e[key] = safe_list(e.get(key))
        e["id"] = e["id"] or f"missing::{len(self.entries) + 1}"
        e["topic_en"] = e["topic_en"] or e["topic"] or e["id"]
        e["topic"] = e["topic_en"]
        e["topic_el"] = e["topic_el"] or e["topic_en"]
        e["category"] = e["category"] or "uncategorized"
        e["category_en"] = e["category_en"] or e["category"].replace("_", " ")
        e["category_el"] = e["category_el"] or e["category_en"]
        e["subcategory_en"] = e["subcategory_en"] or e["subcategory"].replace("_", " ")
        e["subcategory_el"] = e["subcategory_el"] or e["subcategory_en"]
        e["related_topics_en"] = e["related_topics_en"] or e["related_topics"]
        e["related_topics_el"] = e["related_topics_el"] or e["related_topics_en"]
        e["update_note_en"] = e["update_note_en"] or e["update_note"]
        e["update_note_el"] = e["update_note_el"] or e["update_note_en"]
        e["_source_file"] = source_file
        e["_search_primary"] = self.build_primary_search_blob(e)
        return e

    def build_primary_search_blob(self, e):
        parts = [
            e.get("id", ""), e.get("topic_en", ""), e.get("topic_el", ""),
            e.get("summary_en", ""), e.get("summary_el", ""),
            e.get("category", ""), e.get("subcategory", ""),
            e.get("category_en", ""), e.get("category_el", ""),
            e.get("subcategory_en", ""), e.get("subcategory_el", ""),
            e.get("_source_file", ""),
        ]
        parts.extend(e.get("tags", []))
        parts.extend(e.get("related_topics_en", []))
        parts.extend(e.get("related_topics_el", []))
        return normalize_search("\n".join(parts))

    def build_full_search_blob(self, e):
        parts = [e.get(key, "") for key in TEXT_KEYS]
        for key in LIST_KEYS:
            parts.extend(e.get(key, []))
        parts.append(e.get("_source_file", ""))
        return normalize_search("\n".join(parts))

    def database_signature(self):
        digest = hashlib.sha256()
        for name in sorted(self.last_loaded_files):
            path = os.path.join(DB_DIR, name)
            digest.update(name.encode("utf-8"))
            digest.update(b"\0")
            try:
                with open(path, "rb") as fh:
                    for chunk in iter(lambda: fh.read(1024 * 1024), b""):
                        digest.update(chunk)
            except OSError:
                return ""
            digest.update(b"\0")
        return digest.hexdigest()

    def validate_search_index(self):
        self.search_index_ready = False
        if not os.path.isfile(SEARCH_INDEX_FILE):
            return
        try:
            with sqlite3.connect(f"file:{SEARCH_INDEX_FILE}?mode=ro", uri=True) as con:
                metadata = dict(con.execute("SELECT key, value FROM metadata"))
                if metadata.get("entry_count") != str(len(self.entries)):
                    return
                if metadata.get("database_signature") != self.database_signature():
                    return
                con.execute("SELECT entry_id FROM entries_fts LIMIT 1").fetchone()
            self.search_index_ready = True
        except (sqlite3.Error, OSError):
            self.search_index_ready = False

    def indexed_candidates(self, tokens, limit=1200):
        if not self.search_index_ready or not tokens:
            return None
        safe_tokens = [re.sub(r"[^\w]+", "", token, flags=re.UNICODE) for token in tokens]
        safe_tokens = [token for token in safe_tokens if token]
        if not safe_tokens:
            return None
        expression = " AND ".join('"' + token.replace('"', '""') + '"' for token in safe_tokens)
        try:
            with sqlite3.connect(f"file:{SEARCH_INDEX_FILE}?mode=ro", uri=True) as con:
                rows = con.execute(
                    "SELECT entry_id FROM entries_fts WHERE entries_fts MATCH ? LIMIT ?",
                    (expression, int(limit)),
                ).fetchall()
            return [self.by_id[row[0]] for row in rows if row[0] in self.by_id]
        except sqlite3.Error:
            return None

    def load(self):
        self.entries = []
        self.by_id = {}
        self.by_file = defaultdict(list)
        self.by_category = defaultdict(list)
        self.load_errors = []
        self.last_loaded_files = []
        self.search_index_ready = False
        if not os.path.isdir(DB_DIR):
            self.load_errors.append(f"Database folder not found: {DB_DIR}")
            return
        for name in sorted(os.listdir(DB_DIR)):
            if not name.endswith(".json"):
                continue
            path = os.path.join(DB_DIR, name)
            try:
                with open(path, "r", encoding="utf-8") as fh:
                    data = json.load(fh)
                if isinstance(data, dict):
                    data = [data]
                if not isinstance(data, list):
                    raise ValueError("Top-level JSON must be a list or object")
                self.last_loaded_files.append(name)
                for raw in data:
                    e = self.normalize_entry(raw, name)
                    self.entries.append(e)
                    if e["id"] not in self.by_id:
                        self.by_id[e["id"]] = e
                    self.by_file[name].append(e)
                    self.by_category[e["category"]].append(e)
            except Exception as exc:
                self.load_errors.append(f"{name}: {exc}")
        self.entries.sort(key=lambda x: (x.get("category", ""), x.get("topic_en", "").casefold()))
        self.validate_search_index()

    def stats(self):
        return {
            "entries": len(self.entries),
            "files": len(self.by_file),
            "categories": len(self.by_category),
            "load_errors": len(self.load_errors),
            "favorites": len([x for x in STATE.get("favorites", []) if x in self.by_id]),
            "search_index": "ready" if self.search_index_ready else "fallback",
        }

    def search(self, query, lang="en", limit=500):
        q = normalize_search(query)
        tokens = [t for t in q.split() if t]
        if not tokens:
            return list(self.entries[:limit])
        scored = []
        indexed = self.indexed_candidates(tokens, max(limit * 8, 1200))
        candidates = indexed if indexed is not None else self.entries
        for e in candidates:
            primary = e["_search_primary"]
            if indexed is None and not all(token in primary for token in tokens):
                blob = self.build_full_search_blob(e)
                if not all(token in blob for token in tokens):
                    continue
            topic = normalize_search(" ".join([e.get("topic_en", ""), e.get("topic_el", "")]))
            summary = normalize_search(" ".join([e.get("summary_en", ""), e.get("summary_el", "")]))
            category = normalize_search(" ".join([
                e.get("category", ""), e.get("subcategory", ""),
                e.get("category_en", ""), e.get("category_el", ""),
                e.get("subcategory_en", ""), e.get("subcategory_el", ""),
            ]))
            score = 0
            if q == topic:
                score += 250
            elif q in topic:
                score += 120
            if all(t in topic for t in tokens):
                score += 75
            if q in summary:
                score += 45
            if q in category:
                score += 30
            score += sum(8 for t in tokens if t in topic)
            score += sum(3 for t in tokens if t in summary)
            priority = normalize_search(e.get("priority", ""))
            urgency = normalize_search(e.get("urgency", ""))
            if priority in {"critical", "high"}:
                score += 4
            if urgency in {"critical", "urgent", "immediate"}:
                score += 5
            scored.append((score, e))
        scored.sort(key=lambda x: (-x[0], display_topic(x[1], lang).casefold()))
        return [e for _, e in scored[:limit]]

    def quick_entries(self):
        def rank(e):
            text = normalize_search(" ".join([e.get("priority", ""), e.get("urgency", ""), e.get("category", ""), e.get("subcategory", "")]))
            score = 0
            for term, weight in [("critical", 50), ("urgent", 45), ("immediate", 40), ("high", 30), ("emergency", 20), ("pass100", 24), ("pass98", 18), ("pass97", 14), ("pass96", 10), ("greece", 8)]:
                if term in text:
                    score += weight
            return score
        rows = [(rank(e), e) for e in self.entries]
        rows = [x for x in rows if x[0] > 0]
        rows.sort(key=lambda x: (-x[0], x[1].get("topic_en", "").casefold()))
        return [e for _, e in rows[:250]]

    def integrity_report(self):
        ids = Counter(e["id"].casefold() for e in self.entries)
        topics_en = Counter(normalize_search(e["topic_en"]) for e in self.entries)
        topics_el = Counter(normalize_search(e["topic_el"]) for e in self.entries)
        duplicate_ids = [k for k, v in ids.items() if v > 1]
        duplicate_topics = [k for k, v in topics_en.items() if k and v > 1]
        duplicate_topics_el = [k for k, v in topics_el.items() if k and v > 1]
        missing_pairs = []
        for e in self.entries:
            for en, el in PAIR_REQUIRED:
                a, b = e.get(en), e.get(el)
                if isinstance(a, list):
                    if not a or not isinstance(b, list) or not b or len(a) != len(b):
                        missing_pairs.append((e["id"], en, el))
                elif not safe_text(a) or not safe_text(b):
                    missing_pairs.append((e["id"], en, el))

        exact_seen = {}
        duplicate_blocks = []
        repeated_core_text = []
        core_fields = [base + "_" + language for base in (
            "summary", "content", "steps", "materials", "warnings", "mistakes",
            "alternatives", "failure_signs", "when_not_to_use", "short_term",
            "long_term", "if_method_fails", "environment_notes"
        ) for language in ("en", "el")]
        for e in self.entries:
            for key in core_fields:
                value = e.get(key, [])
                values = value if isinstance(value, list) else [value]
                for item in values:
                    text = " ".join(str(item).split()).strip()
                    if len(text) < 25:
                        continue
                    digest = hashlib.sha256(text.casefold().encode("utf-8")).digest()
                    previous = exact_seen.get(digest)
                    if previous and previous[0] != e["id"]:
                        repeated_core_text.append((key, e["id"], previous[0]))
                    else:
                        exact_seen[digest] = (e["id"], key)
                if isinstance(value, list) and value:
                    joined = "\n".join(" ".join(str(x).split()).casefold() for x in value)
                    digest = hashlib.sha256((key + "\0" + joined).encode("utf-8")).digest()
                    previous = exact_seen.get(digest)
                    if previous and previous[0] != e["id"]:
                        duplicate_blocks.append((key, e["id"], previous[0]))
                    else:
                        exact_seen[digest] = (e["id"], key)

        accepted = {"sms", "usb", "json", "termux", "cpr", "aed", "hvac", "url", "wifi", "gps", "pdf", "txt", "api", "fda", "cdc", "who", "bluetooth", "cabcde", "fast", "cpap", "sbar"}
        leaks = []
        for e in self.entries:
            for key, value in e.items():
                if not key.endswith("_el"):
                    continue
                values = value if isinstance(value, list) else [value]
                for item in values:
                    bad = [word for word in re.findall(r"\b[A-Za-z][A-Za-z-]{2,}\b", str(item)) if word.casefold() not in accepted and not word.casefold().startswith("http")]
                    if bad:
                        leaks.append((e["id"], key, sorted(set(bad))[:10]))

        legacy_signatures = [
            "pass96 replaced generic boilerplate", "after real use of",
            "use the smallest reversible and directly observable version",
            "without identifying the domain specific hazard and stop rule",
            "stop depending on the result", "adapt " + "the to",
        ]
        legacy_template_flags = []
        semantic_mismatches = []
        shallow_entries = []
        sources_missing = []
        placeholder_topics = []
        for e in self.entries:
            joined_en = normalize_search(" ".join(str(e.get(k, "")) for k in ["summary_en", "content_en", "short_term_en", "long_term_en", "if_method_fails_en"]))
            for signature in legacy_signatures:
                if signature in joined_en or signature in normalize_search(e.get("update_note", "")):
                    legacy_template_flags.append((e["id"], signature))
            domain_text = normalize_search(" ".join([e.get("category", ""), e.get("subcategory", ""), e.get("topic_en", "")]))
            human_care = any(x in domain_text for x in ["medical", "medicine", "health", "first aid", "patient", "care", "body", "anatomy", "children", "elderly", "vulnerable", "clinic"])
            animal_care = any(x in domain_text for x in ["animal", "livestock", "pet", "veterinary"])
            strongly_nonmedical = any(x in domain_text for x in ["water", "food", "shelter", "power", "route", "agriculture"]) and not human_care
            if strongly_nonmedical and "medicines already taken" in joined_en:
                semantic_mismatches.append((e["id"], "human-care procedure used outside human-care domain"))
            if not animal_care and "species-appropriate restraint" in joined_en:
                semantic_mismatches.append((e["id"], "animal-care procedure used outside animal domain"))
            if len(safe_text(e.get("content_en"))) < 180 or len(safe_text(e.get("content_el"))) < 180 or len(e.get("steps_en", [])) < 3 or len(e.get("warnings_en", [])) < 2:
                shallow_entries.append(e["id"])
            if not e.get("sources"):
                sources_missing.append(e["id"])
            if re.search(r"(?:page|note|checkpoint|entry)\s+\d+$", e.get("topic_en", ""), re.I):
                placeholder_topics.append(e["id"])
        return {
            "duplicate_ids": duplicate_ids,
            "duplicate_topics": duplicate_topics,
            "duplicate_topics_el": duplicate_topics_el,
            "duplicate_blocks": duplicate_blocks,
            "repeated_core_text": repeated_core_text,
            "missing_pairs": missing_pairs,
            "ascii_leaks": leaks,
            "legacy_template_flags": legacy_template_flags,
            "semantic_mismatches": semantic_mismatches,
            "shallow_entries": shallow_entries,
            "sources_missing": sources_missing,
            "placeholder_topics": placeholder_topics,
            "load_errors": list(self.load_errors),
        }


STORE = OfflineSurvivalStore()
STORE.load()


def display_topic(e, lang):
    return e.get("topic_el") if lang == "el" else e.get("topic_en")


def display_summary(e, lang):
    return e.get("summary_el") if lang == "el" else e.get("summary_en")


def display_category(e, lang):
    return e.get("category_el") if lang == "el" else e.get("category_en")


def display_subcategory(e, lang):
    return e.get("subcategory_el") if lang == "el" else e.get("subcategory_en")


def display_related(e, lang):
    return e.get("related_topics_el", []) if lang == "el" else e.get("related_topics_en", [])


def local_value(value, lang):
    values = {
        "basic": ("Basic", "Βασικό"), "basic_to_intermediate": ("Basic to intermediate", "Βασικό έως μέτριο"),
        "intermediate": ("Intermediate", "Μέτριο"), "advanced": ("Advanced", "Προχωρημένο"),
        "low": ("Low", "Χαμηλό"), "medium": ("Medium", "Μέτριο"), "high": ("High", "Υψηλό"),
        "critical": ("Critical", "Κρίσιμο"), "urgent": ("Urgent", "Επείγον"),
        "scenario_dependent": ("Depends on scenario", "Εξαρτάται από το σενάριο"),
        "context_dependent": ("Depends on context", "Εξαρτάται από το πλαίσιο"),
        "varies_by_context": ("Varies by context", "Μεταβάλλεται ανάλογα με το πλαίσιο"),
        "basic_to_moderate": ("Basic to moderate", "Βασικό έως μέτριο"),
        "moderate": ("Moderate", "Μέτριο"), "beginner": ("Beginner", "Αρχάριο"),
        "non_immediate": ("Not immediate", "Μη άμεσο"), "seasonal": ("Seasonal", "Εποχικό"),
        "immediate": ("Immediate", "Άμεσο"),
    }
    key = normalize_search(value).replace(" ", "_")
    if key in values:
        return values[key][1 if lang == "el" else 0]
    return safe_text(value).replace("_", " ")


def section(lines, title, content, numbered=False):
    if not content:
        return
    lines.extend([title, "-" * max(5, len(title))])
    if isinstance(content, list):
        for i, item in enumerate(content, 1):
            lines.append(f"{i}. {item}" if numbered else f"- {item}")
    else:
        for paragraph in safe_text(content).split("\n"):
            if paragraph.strip():
                lines.append(textwrap.fill(paragraph.strip(), width=98))
                lines.append("")
        if lines and lines[-1] == "":
            lines.pop()
    lines.append("")


def format_entry_text(e, lang="en"):
    title = display_topic(e, lang) or e.get("id", "Untitled")
    lines = [title, "=" * max(10, len(title)), f"ID: {e.get('id', '')}"]
    lines.append(f"{tr(lang, 'category')}: {display_category(e, lang)}")
    if display_subcategory(e, lang):
        lines.append(f"{tr(lang, 'subcategory')}: {display_subcategory(e, lang)}")
    lines.append(f"{tr(lang, 'source_file')}: {e.get('_source_file', '')}")
    metadata = []
    for key in ["difficulty", "urgency", "priority"]:
        if e.get(key):
            metadata.append(f"{tr(lang, key)}: {local_value(e.get(key), lang)}")
    if metadata:
        lines.append(" | ".join(metadata))
    if e.get("last_updated"):
        lines.append(f"{tr(lang, 'last_updated')}: {e.get('last_updated')}")
    lines.append("")
    suffix = "el" if lang == "el" else "en"
    section(lines, tr(lang, "summary"), e.get(f"summary_{suffix}"))
    section(lines, tr(lang, "core_reading"), e.get(f"content_{suffix}"))
    for label, field in [
        ("materials", f"materials_{suffix}"), ("steps", f"steps_{suffix}"),
        ("alternatives", f"alternatives_{suffix}"), ("warnings", f"warnings_{suffix}"),
        ("failure_signs", f"failure_signs_{suffix}"),
        ("when_not_to_use", f"when_not_to_use_{suffix}"),
        ("mistakes", f"mistakes_{suffix}"),
    ]:
        section(lines, tr(lang, label), e.get(field, []), numbered=label in {"steps", "materials"})
    for label, field in [
        ("short_term", f"short_term_{suffix}"), ("long_term", f"long_term_{suffix}"),
        ("if_method_fails", f"if_method_fails_{suffix}"),
        ("environment_notes", f"environment_notes_{suffix}"),
    ]:
        section(lines, tr(lang, label), e.get(field))
    section(lines, tr(lang, "related_topics"), display_related(e, lang))
    section(lines, tr(lang, "sources"), e.get("sources", []))
    update = e.get("update_note_el") if lang == "el" else e.get("update_note_en")
    section(lines, tr(lang, "update_note"), update)
    return "\n".join(lines).strip()


def remember_recent(entry_id):
    recent = [x for x in STATE.get("recent", []) if x != entry_id]
    STATE["recent"] = ([entry_id] + recent)[:30]
    save_state(STATE)


def toggle_favorite(entry_id, lang):
    fav = [x for x in STATE.get("favorites", []) if x in STORE.by_id]
    if entry_id in fav:
        fav.remove(entry_id)
        message = tr(lang, "remove_favorite")
    else:
        fav.append(entry_id)
        message = tr(lang, "add_favorite")
    STATE["favorites"] = fav
    save_state(STATE)
    return message


def pick_from_entries(entries, lang, page_size=25):
    if not entries:
        print(tr(lang, "no_entries"))
        pause(lang)
        return
    page_index = 0
    while True:
        clear()
        start = page_index * page_size
        page = entries[start:start + page_size]
        if not page:
            page_index = 0
            continue
        print(f"{tr(lang, 'entries')}: {len(entries)}")
        print("-" * 72)
        favorites = set(STATE.get("favorites", []))
        for index, e in enumerate(page, start + 1):
            star = "★ " if e["id"] in favorites else ""
            print(f"{index}. {star}{display_topic(e, lang)}  [{display_category(e, lang)}]")
        print(f"\n{tr(lang, 'showing')} {start + 1}-{start + len(page)} {tr(lang, 'of')} {len(entries)}")
        print(tr(lang, "read_prompt"))
        choice = input("> ").strip()
        if not choice:
            return
        if choice.casefold() == "n" and start + page_size < len(entries):
            page_index += 1
            continue
        if choice.casefold() == "p" and page_index > 0:
            page_index -= 1
            continue
        if choice.casefold().startswith("f"):
            number = choice[1:].strip()
            if not number:
                number = input("ID/number: ").strip()
            if number.isdigit() and 1 <= int(number) <= len(entries):
                message = toggle_favorite(entries[int(number) - 1]["id"], lang)
                pause(lang, f"\n{message}.\n\n{tr(lang, 'press_enter')}")
            continue
        if choice.isdigit() and 1 <= int(choice) <= len(entries):
            e = entries[int(choice) - 1]
            remember_recent(e["id"])
            clear()
            print(format_entry_text(e, lang))
            action = input("\n[F] ★  |  Enter: " + tr(lang, "return") + "\n> ").strip().casefold()
            if action == "f":
                message = toggle_favorite(e["id"], lang)
                pause(lang, f"\n{message}.\n\n{tr(lang, 'press_enter')}")


WEB_PAGE = r'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Offline Survival</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
:root{--bg:#0c0f14;--card:#151a22;--card2:#1b2330;--line:#2c3545;--text:#eef2f8;--muted:#aeb8ca;--accent:#89b4ff;--accent2:#7bdcb5;--danger:#ffb4a8;--font:16px}
*{box-sizing:border-box}html{font-size:var(--font)}body{margin:0;font-family:system-ui,-apple-system,Segoe UI,Roboto,sans-serif;background:var(--bg);color:var(--text)}
header{position:sticky;top:0;z-index:10;background:rgba(12,15,20,.97);border-bottom:1px solid var(--line);padding:12px}.header-row{display:flex;justify-content:space-between;gap:12px;align-items:center}.title{font-size:1.08rem;font-weight:800}.sub,.meta{color:var(--muted);font-size:.86rem}.controls{display:grid;grid-template-columns:minmax(190px,1fr) 120px minmax(150px,.55fr) minmax(150px,.55fr) repeat(7,auto);gap:8px;margin-top:10px;align-items:center}
input,select,button{font:inherit;padding:10px 11px;border:1px solid var(--line);border-radius:10px;background:var(--card);color:var(--text)}button{cursor:pointer}button.primary{background:var(--accent);color:#07111f;border-color:transparent;font-weight:800}button:hover{background:var(--card2)}button.primary:hover{filter:brightness(1.06)}
main{display:grid;grid-template-columns:minmax(300px,35%) 1fr;min-height:calc(100vh - 190px)}aside{border-right:1px solid var(--line);overflow:auto;max-height:calc(100vh - 190px);position:sticky;top:190px}.panel{padding:12px}.card,.result{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:14px;margin-bottom:12px}.result{cursor:pointer}.result:hover,.result.active{border-color:var(--accent);background:var(--card2)}.result p{margin-bottom:0}.entry-title{margin:.1rem 0 .6rem;font-size:1.5rem}.entry-block{line-height:1.62;white-space:normal}.meta-line{display:flex;flex-wrap:wrap;gap:6px;margin:8px 0}.pill{padding:4px 8px;border:1px solid var(--line);border-radius:999px;color:var(--muted);font-size:.8rem}.grid2{display:grid;grid-template-columns:1fr 1fr;gap:12px}.count{font-weight:800;color:var(--accent2)}.empty{color:var(--muted)}ul{padding-left:21px;line-height:1.55}.chips{display:flex;flex-wrap:wrap;gap:7px}.chip{padding:7px 9px;border-radius:999px}.source a{color:var(--accent);word-break:break-word}.toolbar{display:flex;flex-wrap:wrap;gap:7px;margin-top:10px}.warning{border-color:#6e4f4a;color:var(--danger)}.emergency-strip{margin-top:9px;padding:8px 10px;border:1px solid #6e4f4a;border-radius:10px;background:#241b1b;color:#ffd4cd;font-weight:700}.quickbar{display:flex;gap:7px;overflow:auto;margin-top:8px}.quickbar button{white-space:nowrap;padding:8px 10px}
@media(max-width:1250px){.controls{grid-template-columns:1fr 110px 1fr 1fr repeat(4,auto)}.controls .secondary{display:none}}
@media(max-width:900px){header{position:relative}.controls{grid-template-columns:1fr 1fr}.controls input{grid-column:1/-1}main{grid-template-columns:1fr}aside{position:relative;top:0;max-height:45vh;border-right:0;border-bottom:1px solid var(--line)}.grid2{grid-template-columns:1fr}.header-row{align-items:flex-start}}
@media print{header,aside,.toolbar{display:none!important}main{display:block}.card{border:0;box-shadow:none}.panel{padding:0}body{background:white;color:black}}
</style>
</head>
<body>
<header>
 <div class="header-row"><div><div class="title" id="appTitle">Offline Survival</div><div class="sub" id="appSub"></div></div><div class="meta" id="stats"></div></div>
 <div class="controls">
  <input id="q"><select id="lang"><option value="en">English</option><option value="el">Ελληνικά</option></select>
  <select id="cat"></select><select id="file"></select>
  <button class="primary" id="searchBtn" onclick="runSearch()"></button>
  <button id="randomBtn" onclick="randomEntry()"></button><button id="favBtn" onclick="showFavorites()">★</button>
  <button id="updatesBtn" onclick="loadUpdates()"></button><button class="secondary" onclick="fontSize(-1)">A−</button><button class="secondary" onclick="fontSize(1)">A+</button><button class="secondary" id="clearBtn" onclick="resetView()"></button>
 </div>
 <div class="emergency-strip" id="emergencyStrip"></div>
 <div class="quickbar" id="quickbar"></div>
</header>
<main><aside><div class="panel"><div class="card"><div class="count" id="count"></div><div class="empty" id="hint"></div></div><div id="results"></div></div></aside><section><div class="panel" id="viewer"></div></section></main>
<script>
const UI={en:{sub:'Private local reader for the bilingual survival database. No internet is required.',search:'Search',random:'Random',updates:'Updates',clear:'Clear',allcat:'All categories',allfiles:'All files',placeholder:'Search topic, symptom, tool, method, food, terrain…',results:'results',hint:'Search or use a filter. Tap a result to read the full entry.',none:'No matching entries.',ready:'Ready',readytext:'Search, open a random entry, or use favorites. Official instructions and emergency services override this guide.',materials:'Materials',steps:'Steps',alternatives:'Alternatives',warnings:'Warnings',failure:'Failure signs',notuse:'When not to use',mistakes:'Common mistakes',short:'Short-term',long:'Long-term',fallback:'If the method fails',environment:'Environment notes',related:'Related topics',sources:'Official/reference sources',update:'Update note',copy:'Copy entry',print:'Print',favorite:'Favorite',unfavorite:'Remove favorite',favorites:'Favorites',nofav:'No saved favorites.',loading:'Loading…',entrymissing:'Entry not found.',source:'Source',copied:'Copied to clipboard',emergency:'Greece: 112 emergency • Poison Centre: 210 7793777',files:'files',categories:'categories',quick:['First 30 min','Earthquake','Wildfire','Flood','Power','Heat','Water','Medicine','Accessibility','Collapse','Digital','Recovery']},el:{sub:'Ιδιωτικός τοπικός αναγνώστης της δίγλωσσης βάσης επιβίωσης. Δεν απαιτείται διαδίκτυο.',search:'Αναζήτηση',random:'Τυχαίο',updates:'Ενημερώσεις',clear:'Καθαρισμός',allcat:'Όλες οι κατηγορίες',allfiles:'Όλα τα αρχεία',placeholder:'Αναζήτηση θέματος, συμπτώματος, εργαλείου, μεθόδου, τροφής, εδάφους…',results:'αποτελέσματα',hint:'Κάνε αναζήτηση ή χρησιμοποίησε φίλτρο. Πάτησε αποτέλεσμα για πλήρη ανάγνωση.',none:'Δεν βρέθηκαν αποτελέσματα.',ready:'Έτοιμο',readytext:'Κάνε αναζήτηση, άνοιξε τυχαία εγγραφή ή χρησιμοποίησε αγαπημένα. Οι επίσημες οδηγίες και οι υπηρεσίες ανάγκης υπερισχύουν του οδηγού.',materials:'Υλικά',steps:'Βήματα',alternatives:'Εναλλακτικές',warnings:'Προειδοποιήσεις',failure:'Σημάδια αποτυχίας',notuse:'Πότε να μη χρησιμοποιηθεί',mistakes:'Συχνά λάθη',short:'Βραχυπρόθεσμα',long:'Μακροπρόθεσμα',fallback:'Αν αποτύχει η μέθοδος',environment:'Σημειώσεις περιβάλλοντος',related:'Σχετικά θέματα',sources:'Επίσημες/βοηθητικές πηγές',update:'Σημείωση ενημέρωσης',copy:'Αντιγραφή εγγραφής',print:'Εκτύπωση',favorite:'Αγαπημένο',unfavorite:'Αφαίρεση αγαπημένου',favorites:'Αγαπημένα',nofav:'Δεν υπάρχουν αγαπημένα.',loading:'Φόρτωση…',entrymissing:'Η εγγραφή δεν βρέθηκε.',source:'Πηγή',copied:'Αντιγράφηκε',emergency:'Ελλάδα: 112 έκτακτη ανάγκη • Κέντρο Δηλητηριάσεων: 210 7793777',files:'αρχεία',categories:'κατηγορίες',quick:['Πρώτα 30 λεπτά','Σεισμός','Πυρκαγιά','Πλημμύρα','Ρεύμα','Καύσωνας','Νερό','Φάρμακα','Προσβασιμότητα','Κατάρρευση','Ψηφιακά','Αποκατάσταση']}};
let lastResults=[],activeId=null,meta=null,currentText='';
const $=id=>document.getElementById(id);const esc=s=>String(s||'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const lang=()=>$('lang').value;const t=k=>UI[lang()][k]||k;
function favs(){try{return JSON.parse(localStorage.getItem('offlineSurvivalFavorites')||'[]')}catch(e){return[]}}function saveFavs(v){localStorage.setItem('offlineSurvivalFavorites',JSON.stringify([...new Set(v)]))}function isFav(id){return favs().includes(id)}
function applyUI(){document.documentElement.lang=lang();$('appSub').textContent=t('sub');$('searchBtn').textContent=t('search');$('randomBtn').textContent=t('random');$('updatesBtn').textContent=t('updates');$('clearBtn').textContent=t('clear');$('q').placeholder=t('placeholder');$('cat').options[0].text=t('allcat');$('file').options[0].text=t('allfiles');$('emergencyStrip').textContent=t('emergency');const queries=['first 30 minutes','earthquake','wildfire','flood','power outage','heatwave','unsafe water','medicine','accessibility','collapse trapped debris','ransomware phone cash documents','recovery cleanup'];$('quickbar').innerHTML=t('quick').map((x,i)=>`<button onclick="quickSearch('${queries[i]}')">${esc(x)}</button>`).join('');if(!activeId) resetView(false);}
function textCard(title,text,cls=''){if(!text)return'';return `<div class="card ${cls}"><h3>${esc(title)}</h3><div class="entry-block">${esc(text).replace(/\n/g,'<br><br>')}</div></div>`}
function listCard(title,items,cls=''){if(!items||!items.length)return'';return `<div class="card ${cls}"><h3>${esc(title)}</h3><ul>${items.map(x=>`<li>${esc(x)}</li>`).join('')}</ul></div>`}
function sourceCard(items){if(!items||!items.length)return'';return `<div class="card source"><h3>${esc(t('sources'))}</h3><ul>${items.map(x=>{const m=String(x).match(/(https?:\/\/\S+)/);return m?`<li>${esc(x.slice(0,m.index))}<a href="${esc(m[1])}" target="_blank" rel="noreferrer">${esc(m[1])}</a></li>`:`<li>${esc(x)}</li>`}).join('')}</ul></div>`}
function chipCard(title,items){if(!items||!items.length)return'';return `<div class="card"><h3>${esc(title)}</h3><div class="chips">${items.map(x=>`<button class="chip" onclick="searchRelated('${String(x).replace(/'/g,"\\'")}')">${esc(x)}</button>`).join('')}</div></div>`}
async function loadMeta(){const oldCat=$('cat').value,oldFile=$('file').value;const r=await fetch('/api/meta?lang='+lang());meta=await r.json();$('stats').textContent=`${meta.stats.entries} • ${meta.stats.files} ${t('files')} • ${meta.stats.categories} ${t('categories')}`;for(const [id,items] of [['cat',meta.categories],['file',meta.files]]){const s=$(id);s.innerHTML='<option value=""></option>';items.forEach(x=>{const o=document.createElement('option');o.value=(typeof x==='object'?x.value:x);o.textContent=(typeof x==='object'?x.label:x);s.appendChild(o)})}if([...$('cat').options].some(o=>o.value===oldCat))$('cat').value=oldCat;if([...$('file').options].some(o=>o.value===oldFile))$('file').value=oldFile;applyUI()}
function updateCount(n,msg){$('count').textContent=`${n} ${t('results')}`;$('hint').textContent=msg||t('hint')}
async function runSearch(){const qs=new URLSearchParams({q:$('q').value.trim(),lang:lang(),category:$('cat').value,file:$('file').value});$('results').innerHTML=`<div class="card empty">${t('loading')}</div>`;const r=await fetch('/api/search?'+qs);const d=await r.json();lastResults=d.results||[];renderResults(lastResults);if(lastResults.length)loadEntry(lastResults[0].id);else $('viewer').innerHTML=textCard(t('none'),t('hint'))}
function renderResults(rows){updateCount(rows.length,rows.length?t('hint'):t('none'));$('results').innerHTML=rows.map(r=>`<div class="result ${activeId===r.id?'active':''}" onclick="loadEntry('${esc(r.id)}')"><strong>${isFav(r.id)?'★ ':''}${esc(r.topic)}</strong><div class="meta">${esc(r.category)} • ${esc(r.file)}</div><p>${esc((r.summary||'').slice(0,280))}</p></div>`).join('')||`<div class="card empty">${t('none')}</div>`}
async function loadEntry(id){activeId=id;$('viewer').innerHTML=`<div class="card empty">${t('loading')}</div>`;const r=await fetch(`/api/entry?id=${encodeURIComponent(id)}&lang=${lang()}`);const d=await r.json();if(!d.entry){$('viewer').innerHTML=textCard(t('entrymissing'),'');return}const e=d.entry;currentText=e.text||'';const pills=[e.category,e.subcategory,e.file,e.priority,e.urgency].filter(Boolean).map(x=>`<span class="pill">${esc(x)}</span>`).join('');$('viewer').innerHTML=`<div class="card"><h1 class="entry-title">${esc(e.topic)}</h1><div class="meta-line">${pills}<span class="pill">${esc(e.id)}</span></div><div class="entry-block"><strong>${esc(e.summary)}</strong><br><br>${esc(e.content).replace(/\n/g,'<br><br>')}</div><div class="toolbar"><button onclick="toggleFav('${esc(e.id)}')">${isFav(e.id)?'★ '+t('unfavorite'):'☆ '+t('favorite')}</button><button onclick="copyEntry()">${t('copy')}</button><button onclick="window.print()">${t('print')}</button></div></div><div class="grid2"><div>${listCard(t('materials'),e.materials)}${listCard(t('steps'),e.steps)}${listCard(t('alternatives'),e.alternatives)}${listCard(t('warnings'),e.warnings,'warning')}${listCard(t('failure'),e.failure_signs,'warning')}</div><div>${listCard(t('notuse'),e.when_not_to_use,'warning')}${listCard(t('mistakes'),e.mistakes)}${textCard(t('short'),e.short_term)}${textCard(t('long'),e.long_term)}${textCard(t('fallback'),e.if_method_fails)}${textCard(t('environment'),e.environment_notes)}</div></div>${chipCard(t('related'),e.related_topics)}${sourceCard(e.sources)}${textCard(t('update'),e.update_note)}`;document.querySelectorAll('.result').forEach(x=>x.classList.remove('active'));renderResults(lastResults)}
function toggleFav(id){let f=favs();f=f.includes(id)?f.filter(x=>x!==id):[...f,id];saveFavs(f);loadEntry(id)}
async function showFavorites(){const ids=favs();if(!ids.length){lastResults=[];renderResults([]);$('viewer').innerHTML=textCard(t('favorites'),t('nofav'));return}const r=await fetch('/api/favorites?ids='+encodeURIComponent(ids.join(','))+'&lang='+lang());const d=await r.json();lastResults=d.results||[];renderResults(lastResults);if(lastResults.length)loadEntry(lastResults[0].id)}
async function randomEntry(){const r=await fetch('/api/random?lang='+lang());const d=await r.json();if(d.id)loadEntry(d.id)}
async function loadUpdates(){const r=await fetch('/api/updates');const d=await r.json();lastResults=[];$('results').innerHTML=(d.logs||[]).slice().reverse().map(x=>`<div class="result" onclick="loadUpdate('${String(x).replace(/'/g,"\\'")}')"><strong>${esc(x)}</strong></div>`).join('');updateCount((d.logs||[]).length,t('updates'))}
async function loadUpdate(name){const r=await fetch('/api/update?name='+encodeURIComponent(name));const d=await r.json();$('viewer').innerHTML=textCard(d.name||t('updates'),d.content||'')}
function searchRelated(x){$('q').value=x;runSearch()}function quickSearch(x){$('q').value=x;$('cat').value='';$('file').value='';runSearch()}function resetView(reset=true){if(reset){$('q').value='';$('cat').value='';$('file').value='';$('results').innerHTML=''}activeId=null;updateCount(0,t('hint'));$('viewer').innerHTML=textCard(t('ready'),t('readytext'))}
function fontSize(delta){const cur=parseInt(getComputedStyle(document.documentElement).fontSize)||16;document.documentElement.style.setProperty('--font',Math.max(13,Math.min(22,cur+delta))+'px')}async function copyEntry(){try{await navigator.clipboard.writeText(currentText);alert(t('copied'))}catch(e){}}
$('q').addEventListener('keydown',e=>{if(e.key==='Enter')runSearch()});$('lang').addEventListener('change',async()=>{await loadMeta();if(activeId)await loadEntry(activeId);else if(lastResults.length)await runSearch();});$('cat').addEventListener('change',runSearch);$('file').addEventListener('change',runSearch);loadMeta();
</script>
</body></html>'''


def browser_labels(lang):
    return {key: tr(lang, key) for key in ["materials", "steps", "alternatives", "warnings", "failure_signs", "when_not_to_use", "mistakes", "short_term", "long_term", "if_method_fails", "environment_notes", "related_topics", "sources", "update_note"]}


class OfflineWebHandler(BaseHTTPRequestHandler):
    def send_json(self, payload, status=200):
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def send_html(self, text, status=200):
        data = text.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Security-Policy", "default-src 'self' 'unsafe-inline'; img-src 'self' data:; connect-src 'self';")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        parsed = urlparse(self.path)
        qs = parse_qs(parsed.query)
        if parsed.path == "/":
            self.send_html(WEB_PAGE)
            return
        if parsed.path == "/api/meta":
            lang = qs.get("lang", ["en"])[0]
            categories = []
            for value in sorted(STORE.by_category):
                rows = STORE.by_category[value]
                categories.append({"value": value, "label": display_category(rows[0], lang) if rows else value})
            self.send_json({"categories": categories, "files": sorted(STORE.by_file), "stats": STORE.stats()})
            return
        if parsed.path == "/api/random":
            if not STORE.entries:
                self.send_json({"id": None}, 404)
            else:
                e = random.choice(STORE.entries)
                self.send_json({"id": e["id"]})
            return
        if parsed.path == "/api/search":
            query = qs.get("q", [""])[0]
            lang = qs.get("lang", ["en"])[0]
            category = qs.get("category", [""])[0]
            file_name = qs.get("file", [""])[0]
            rows = STORE.search(query, lang, 1000) if query else list(STORE.entries)
            if category:
                rows = [e for e in rows if e["category"] == category]
            if file_name:
                rows = [e for e in rows if e["_source_file"] == file_name]
            self.send_json({"results": [result_payload(e, lang) for e in rows[:250]]})
            return
        if parsed.path == "/api/favorites":
            lang = qs.get("lang", ["en"])[0]
            ids = [x for x in qs.get("ids", [""])[0].split(",") if x]
            self.send_json({"results": [result_payload(STORE.by_id[x], lang) for x in ids if x in STORE.by_id]})
            return
        if parsed.path == "/api/entry":
            entry_id = qs.get("id", [""])[0]
            lang = qs.get("lang", ["en"])[0]
            e = STORE.by_id.get(entry_id)
            if not e:
                self.send_json({"entry": None}, 404)
                return
            suffix = "el" if lang == "el" else "en"
            payload = {
                "id": e["id"], "topic": display_topic(e, lang), "summary": e.get(f"summary_{suffix}", ""),
                "content": e.get(f"content_{suffix}", ""), "category": display_category(e, lang), "subcategory": display_subcategory(e, lang),
                "file": e["_source_file"], "difficulty": local_value(e.get("difficulty"), lang),
                "urgency": local_value(e.get("urgency"), lang), "priority": local_value(e.get("priority"), lang),
                "materials": e.get(f"materials_{suffix}", []), "steps": e.get(f"steps_{suffix}", []),
                "alternatives": e.get(f"alternatives_{suffix}", []), "warnings": e.get(f"warnings_{suffix}", []),
                "failure_signs": e.get(f"failure_signs_{suffix}", []), "when_not_to_use": e.get(f"when_not_to_use_{suffix}", []),
                "mistakes": e.get(f"mistakes_{suffix}", []), "short_term": e.get(f"short_term_{suffix}", ""),
                "long_term": e.get(f"long_term_{suffix}", ""), "if_method_fails": e.get(f"if_method_fails_{suffix}", ""),
                "environment_notes": e.get(f"environment_notes_{suffix}", ""), "related_topics": display_related(e, lang),
                "sources": e.get("sources", []), "update_note": e.get(f"update_note_{suffix}", ""),
                "text": format_entry_text(e, lang),
            }
            self.send_json({"entry": payload, "labels": browser_labels(lang)})
            return
        if parsed.path == "/api/updates":
            logs = [x for x in sorted(os.listdir(UPDATES_DIR)) if x.endswith(".txt")] if os.path.isdir(UPDATES_DIR) else []
            self.send_json({"logs": logs})
            return
        if parsed.path == "/api/update":
            name = os.path.basename(qs.get("name", [""])[0])
            path = os.path.join(UPDATES_DIR, name)
            if not name or not os.path.isfile(path):
                self.send_json({"name": None}, 404)
            else:
                with open(path, "r", encoding="utf-8") as fh:
                    self.send_json({"name": name, "content": fh.read()})
            return
        self.send_json({"error": "Not found"}, 404)

    def log_message(self, _format, *_args):
        return


def result_payload(e, lang):
    return {"id": e["id"], "topic": display_topic(e, lang), "summary": display_summary(e, lang), "category": display_category(e, lang), "file": e["_source_file"]}


def slugify(value, fallback="entry"):
    text = normalize_search(value).replace(" ", "_")
    return text[:90] or fallback


def export_root():
    candidates = [
        os.path.join("/storage/emulated/0/Download", EXPORT_DIR_NAME),
        os.path.join(os.path.expanduser("~"), "storage", "downloads", EXPORT_DIR_NAME),
        os.path.join(BASE_DIR, EXPORT_DIR_NAME),
    ]
    for folder in candidates:
        try:
            os.makedirs(folder, exist_ok=True)
            test = os.path.join(folder, ".write_test")
            with open(test, "w", encoding="utf-8") as fh:
                fh.write("ok")
            os.remove(test)
            return folder
        except OSError:
            continue
    return os.path.join(BASE_DIR, EXPORT_DIR_NAME)


def export_entries(entries, lang="en", name="export"):
    root = export_root()
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    folder = os.path.join(root, f"{slugify(name, 'export')}_{stamp}")
    os.makedirs(folder, exist_ok=True)
    index = [tr(lang, "app"), "=" * 40, f"{tr(lang, 'language')}: {lang}", f"{tr(lang, 'entries')}: {len(entries)}", f"Created: {stamp}", ""]
    for number, e in enumerate(entries, 1):
        title = display_topic(e, lang)
        filename = f"{number:04d}_{slugify(title, 'topic')}.txt"
        with open(os.path.join(folder, filename), "w", encoding="utf-8") as fh:
            fh.write(format_entry_text(e, lang) + "\n")
        index.append(f"{number:04d}. {title} -> {filename}")
    with open(os.path.join(folder, "INDEX.txt"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(index) + "\n")
    return folder, len(entries)


def export_menu(lang):
    while True:
        clear()
        print(tr(lang, "export_title"))
        print("-" * 60)
        options = ["export_all", "export_search", "export_category", "export_file", "export_favorites", "export_quick", "export_both"]
        for i, key in enumerate(options, 1):
            print(f"{i}. {tr(lang, key)}")
        print(f"0. {tr(lang, 'return')}")
        try:
            choice = input("\n> ").strip()
        except EOFError:
            break
        if not choice or choice == "0":
            return
        entries, label = [], "export"
        if choice == "1":
            entries, label = list(STORE.entries), "entire_database"
        elif choice == "2":
            query = input(f"{tr(lang, 'query')}: ").strip()
            entries, label = STORE.search(query, lang, len(STORE.entries)), f"search_{query}"
        elif choice == "3":
            items = sorted(STORE.by_category.items())
            for i, (name, data) in enumerate(items, 1):
                print(f"{i}. {name} ({len(data)})")
            pick = input("> ").strip()
            if pick.isdigit() and 1 <= int(pick) <= len(items):
                label, entries = items[int(pick) - 1]
        elif choice == "4":
            items = sorted(STORE.by_file.items())
            for i, (name, data) in enumerate(items, 1):
                print(f"{i}. {name} ({len(data)})")
            pick = input("> ").strip()
            if pick.isdigit() and 1 <= int(pick) <= len(items):
                label, entries = items[int(pick) - 1]
        elif choice == "5":
            entries = [STORE.by_id[x] for x in STATE.get("favorites", []) if x in STORE.by_id]
            label = "favorites"
        elif choice == "6":
            entries, label = STORE.quick_entries(), "quick_emergency_pack"
        elif choice == "7":
            entries, label = list(STORE.entries), "bilingual_database"
            if entries:
                folder_en, n = export_entries(entries, "en", label + "_english")
                folder_el, _ = export_entries(entries, "el", label + "_greek")
                pause(lang, f"\n{tr(lang, 'exported')} {n} + {n}\n{folder_en}\n{folder_el}\n\n{tr(lang, 'press_enter')}")
            continue
        if not entries:
            pause(lang, f"\n{tr(lang, 'nothing_export')}\n\n{tr(lang, 'press_enter')}")
            continue
        folder, written = export_entries(entries, lang, label)
        pause(lang, f"\n{tr(lang, 'exported')} {written} {tr(lang, 'to')}:\n{folder}\n\n{tr(lang, 'press_enter')}")


def browse_mapping(mapping, lang, title_key):
    items = sorted(mapping.items())
    while True:
        clear()
        print(tr(lang, title_key))
        print("-" * 72)
        for i, (name, data) in enumerate(items, 1):
            label = display_category(data[0], lang) if title_key == "categories" and data else name
            print(f"{i}. {label} ({len(data)})")
        print("\n" + tr(lang, "choose_number"))
        choice = input("> ").strip()
        if not choice:
            return
        if choice.isdigit() and 1 <= int(choice) <= len(items):
            pick_from_entries(items[int(choice) - 1][1], lang)


def show_stats(lang):
    clear()
    print(tr(lang, "stats_title"))
    print("-" * 60)
    for key, value in STORE.stats().items():
        print(f"{key}: {value}")
    print("\n" + tr(lang, "top_categories"))
    print("-" * 60)
    for name, count in Counter(e["category"] for e in STORE.entries).most_common(30):
        sample = STORE.by_category[name][0]
        print(f"{count:4d}  {display_category(sample, lang)}")
    pause(lang)


def show_integrity(lang):
    clear()
    report = STORE.integrity_report()
    print(tr(lang, "integrity_title"))
    print("-" * 72)
    pairs = [
        ("duplicate_ids", len(report["duplicate_ids"])),
        ("duplicate_topics", len(report["duplicate_topics"])),
        ("duplicate_topics_el", len(report["duplicate_topics_el"])),
        ("duplicate_blocks", len(report["duplicate_blocks"])),
        ("repeated_core_text", len(report["repeated_core_text"])),
        ("missing_pairs", len(report["missing_pairs"])),
        ("ascii_leaks", len(report["ascii_leaks"])),
        ("legacy_template_flags", len(report["legacy_template_flags"])),
        ("semantic_mismatches", len(report["semantic_mismatches"])),
        ("shallow_entries", len(report["shallow_entries"])),
        ("sources_missing", len(report["sources_missing"])),
        ("placeholder_topics", len(report["placeholder_topics"])),
        ("load_errors", len(report["load_errors"])),
    ]
    for key, value in pairs:
        print(f"{tr(lang, key)}: {value}")
    if all(value == 0 for _, value in pairs):
        print("\n✓ " + tr(lang, "clean_audit"))
    else:
        for key in ["duplicate_ids", "duplicate_topics", "duplicate_topics_el", "duplicate_blocks", "repeated_core_text", "missing_pairs", "ascii_leaks", "legacy_template_flags", "semantic_mismatches", "shallow_entries", "sources_missing", "placeholder_topics", "load_errors"]:
            if report[key]:
                print(f"\n{tr(lang, key)}:")
                for item in report[key][:40]:
                    print("-", item)
    pause(lang)


def show_source_guide(lang):
    path = os.path.join(BASE_DIR, "OFFICIAL_SAFETY_SOURCES.md")
    clear()
    print(tr(lang, "official_sources"))
    print("-" * 72)
    if not os.path.isfile(path):
        print(tr(lang, "no_entries"))
    else:
        with open(path, "r", encoding="utf-8") as fh:
            print(fh.read())
    pause(lang)


def show_updates(lang):
    clear()
    print(tr(lang, "update_logs"))
    print("-" * 72)
    logs = [x for x in sorted(os.listdir(UPDATES_DIR)) if x.endswith(".txt")] if os.path.isdir(UPDATES_DIR) else []
    if not logs:
        print(tr(lang, "no_logs"))
        pause(lang)
        return
    logs.reverse()
    for i, name in enumerate(logs, 1):
        print(f"{i}. {name}")
    choice = input("\n> ").strip()
    if choice.isdigit() and 1 <= int(choice) <= len(logs):
        path = os.path.join(UPDATES_DIR, logs[int(choice) - 1])
        clear()
        with open(path, "r", encoding="utf-8") as fh:
            print(fh.read())
        pause(lang)


def find_free_port():
    for port in range(WEB_PORT_START, WEB_PORT_END + 1):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            try:
                sock.bind((WEB_HOST, port))
            except OSError:
                continue
            return port
    return None


def launch_web_ui(lang):
    port = find_free_port()
    if port is None:
        pause(lang, f"\n{tr(lang, 'web_failed')}\n\n{tr(lang, 'press_enter')}")
        return
    server = ThreadingHTTPServer((WEB_HOST, port), OfflineWebHandler)
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    url = f"http://{WEB_HOST}:{port}/"
    print(f"\n{tr(lang, 'web_started')}: {url}")
    opened = False
    try:
        result = subprocess.run(["termux-open-url", url], check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        opened = result.returncode == 0
    except Exception:
        pass
    if not opened:
        try:
            opened = bool(webbrowser.open(url))
        except Exception:
            pass
    print(tr(lang, "web_stop"))
    pause(lang, "")
    server.shutdown()
    server.server_close()


READINESS_ITEMS = {
    "en": [
        "A written meeting and communication plan exists.", "At least two safe exits or routes are known.",
        "Emergency water is stored and rotated.", "Shelf-stable food covers the household's needs.",
        "Medicines, allergies, prescriptions, and pharmacy details are written down.", "A light, radio or information method works without mains power.",
        "Phones and critical devices have a charging reserve.", "Smoke and carbon-monoxide alarms are present where applicable and tested.",
        "A first-aid kit is present and someone has current training.", "Copies of key documents and emergency cash are protected.",
        "Pets, livestock, children, older adults, and disability needs are included.", "The household knows when to call 112 and what information to give.",
        "The evacuation kit can actually be carried through the exit route.", "Food, water, batteries, and medicines have been checked recently.",
        "One trusted out-of-area contact is known to everyone.", "The plan has been practised within the last six months.",
    ],
    "el": [
        "Υπάρχει γραπτό σχέδιο συνάντησης και επικοινωνίας.", "Είναι γνωστές τουλάχιστον δύο ασφαλείς έξοδοι ή διαδρομές.",
        "Υπάρχει αποθηκευμένο και ανανεωμένο νερό ανάγκης.", "Υπάρχουν τρόφιμα ραφιού για τις ανάγκες του νοικοκυριού.",
        "Φάρμακα, αλλεργίες, συνταγές και στοιχεία φαρμακείου είναι γραμμένα.", "Υπάρχει φωτισμός, ραδιόφωνο ή τρόπος ενημέρωσης χωρίς ρεύμα δικτύου.",
        "Υπάρχει εφεδρική φόρτιση για κινητά και κρίσιμες συσκευές.", "Υπάρχουν και έχουν ελεγχθεί ανιχνευτές καπνού και μονοξειδίου όπου απαιτούνται.",
        "Υπάρχει κιτ πρώτων βοηθειών και άτομο με πρόσφατη εκπαίδευση.", "Αντίγραφα βασικών εγγράφων και μετρητά ανάγκης προστατεύονται.",
        "Το σχέδιο περιλαμβάνει κατοικίδια, ζώα, παιδιά, ηλικιωμένους και ανάγκες αναπηρίας.", "Το νοικοκυριό ξέρει πότε καλεί 112 και ποιες πληροφορίες δίνει.",
        "Το κιτ εκκένωσης μπορεί πραγματικά να μεταφερθεί από την έξοδο.", "Τρόφιμα, νερό, μπαταρίες και φάρμακα ελέγχθηκαν πρόσφατα.",
        "Όλοι γνωρίζουν μία έμπιστη επαφή εκτός περιοχής.", "Το σχέδιο εξασκήθηκε τους τελευταίους έξι μήνες.",
    ],
}


def readiness_check(lang):
    clear()
    print(tr(lang, "readiness_title"))
    print(tr(lang, "yes_no"))
    print("-" * 72)
    no_items = []
    for i, item in enumerate(READINESS_ITEMS[lang], 1):
        answer = input(f"{i}. {item} [y/n] ").strip().casefold()
        if answer not in {"y", "yes", "ν", "ναι"}:
            no_items.append(item)
    score = len(READINESS_ITEMS[lang]) - len(no_items)
    percent = round(score / len(READINESS_ITEMS[lang]) * 100)
    lines = [tr(lang, "readiness_title"), "=" * 40, f"{tr(lang, 'score')}: {score}/{len(READINESS_ITEMS[lang])} ({percent}%)", "", tr(lang, "recommendations") + ":"]
    lines.extend(f"- {x}" for x in no_items[:10])
    folder = export_root()
    path = os.path.join(folder, f"readiness_check_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{lang}.txt")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    clear()
    print("\n".join(lines))
    print(f"\n{tr(lang, 'saved_report')}: {path}")
    pause(lang)


def build_plan(lang):
    clear()
    print(tr(lang, "plan_title"))
    print("-" * 72)
    keys = ["household", "primary_meeting", "backup_meeting", "outside_contact", "emergency_contacts", "medical_needs", "pets", "evacuation", "utilities", "supplies_location", "notes"]
    values = {}
    for key in keys:
        values[key] = input(f"{tr(lang, key)}: ").strip()
    title = values["household"] or tr(lang, "plan_title")
    lines = [title, "=" * max(30, len(title)), f"{tr(lang, 'last_updated')}: {datetime.now().strftime('%Y-%m-%d %H:%M')}", ""]
    for key in keys[1:]:
        lines.append(f"{tr(lang, key)}: {values[key] or '-'}")
    lines.extend(["", "112: " + ("European emergency number; free in Greece and the EU." if lang == "en" else "Ευρωπαϊκός αριθμός έκτακτης ανάγκης· δωρεάν στην Ελλάδα και την ΕΕ."), "", tr(lang, "quick_note")])
    path = os.path.join(export_root(), f"emergency_plan_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{lang}.txt")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    clear()
    print("\n".join(lines))
    print(f"\n{tr(lang, 'plan_saved')}: {path}")
    pause(lang)


def choose_language(current="en"):
    clear()
    print(tr(current, "choose_language"))
    print("1. English\n2. Ελληνικά")
    choice = input("> ").strip()
    return "el" if choice == "2" else "en"


def print_menu(lang):
    print(tr(lang, "app"))
    print("=" * 72)
    print(f"{tr(lang, 'language')}: {'Ελληνικά' if lang == 'el' else 'English'}")
    print(f"{tr(lang, 'entries_loaded')}: {len(STORE.entries)}")
    print(tr(lang, "emergency_numbers"))
    print("")
    menu = [
        ("1", "emergency_helper"), ("2", "search"), ("3", "scenario_packs"),
        ("4", "quick_emergency"), ("5", "recent"), ("6", "favorites"),
        ("7", "browse_topics"), ("8", "browse_categories"), ("9", "browse_files"),
        ("10", "readiness"), ("11", "plan_builder"), ("12", "browser"),
        ("13", "export"), ("14", "statistics"), ("15", "integrity"),
        ("16", "updates"), ("17", "official_sources"),
        ("18", "switch_language"), ("19", "reload"), ("0", "exit"),
    ]
    for number, key in menu:
        print(f"{number}. {tr(lang, key)}")





EMERGENCY_CHOICES = {
    "en": [
        ("Immediate danger or someone seriously unwell", "first 30 minutes 112"),
        ("Earthquake or aftershocks", "earthquake aftershock"),
        ("Wildfire, smoke, or evacuation", "wildfire smoke evacuation"),
        ("Flood or rising water", "flood rising water"),
        ("Power outage, generator, or carbon monoxide", "power outage carbon monoxide"),
        ("Heatwave or dangerous indoor heat", "heatwave cooling"),
        ("Water may be unsafe or supply stopped", "water unsafe supply interruption"),
        ("Food, refrigerator, or freezer safety", "refrigerator freezer food outage"),
        ("Medicine, poisoning, or medical-device continuity", "medicine poisoning medical device"),
        ("A household member is missing or contact is lost", "missing household member reunification"),
        ("Vehicle or travel problem", "vehicle stranded evacuation"),
        ("Disability, mobility, sensory, or communication support", "accessibility mobility communication"),
        ("Returning, cleaning, mould, or recovery", "re-entry cleanup mould recovery"),
        ("Collapse, entrapment, or damaged building", "collapse trapped debris damaged building"),
        ("Landslide or destructive weather", "landslide debris flow hail whiteout wind"),
        ("Unsafe water or infant feeding disruption", "water advisory infant formula feeding"),
        ("Cash, documents, phone, or cyber outage", "cash documents phone ransomware recovery"),
    ],
    "el": [
        ("Άμεσος κίνδυνος ή σοβαρή αδιαθεσία", "πρώτα 30 λεπτά 112"),
        ("Σεισμός ή μετασεισμοί", "σεισμός μετασεισμός"),
        ("Δασική πυρκαγιά, καπνός ή εκκένωση", "πυρκαγιά καπνός εκκένωση"),
        ("Πλημμύρα ή ανερχόμενο νερό", "πλημμύρα ανερχόμενο νερό"),
        ("Διακοπή ρεύματος, γεννήτρια ή μονοξείδιο", "διακοπή ρεύματος μονοξείδιο"),
        ("Καύσωνας ή επικίνδυνη ζέστη μέσα", "καύσωνας δροσιά"),
        ("Ύποπτο νερό ή διακοπή παροχής", "νερό μη ασφαλές διακοπή"),
        ("Ασφάλεια τροφίμων, ψυγείου ή καταψύκτη", "ψυγείο καταψύκτης τρόφιμα"),
        ("Φάρμακα, δηλητηρίαση ή ιατρική συσκευή", "φάρμακα δηλητηρίαση ιατρική συσκευή"),
        ("Αγνοείται μέλος ή χάθηκε επικοινωνία", "αγνοούμενο μέλος επανένωση"),
        ("Πρόβλημα οχήματος ή μετακίνησης", "όχημα ακινητοποιημένο εκκένωση"),
        ("Αναπηρία, κινητικότητα, αισθητηριακή ή επικοινωνιακή υποστήριξη", "προσβασιμότητα κινητικότητα επικοινωνία"),
        ("Επιστροφή, καθαρισμός, μούχλα ή αποκατάσταση", "επανείσοδος καθαρισμός μούχλα αποκατάσταση"),
        ("Κατάρρευση, παγίδευση ή κατεστραμμένο κτίριο", "κατάρρευση παγίδευση συντρίμμια κτίριο"),
        ("Κατολίσθηση ή καταστροφικός καιρός", "κατολίσθηση φερτά υλικά χαλάζι χιονοθύελλα άνεμος"),
        ("Μη ασφαλές νερό ή διακοπή βρεφικής σίτισης", "οδηγία νερού βρεφικό γάλα σίτιση"),
        ("Μετρητά, έγγραφα, τηλέφωνο ή ψηφιακή διακοπή", "μετρητά έγγραφα τηλέφωνο επίθεση λύτρα ανάκτηση"),
    ],
}


def emergency_helper(lang):
    while True:
        clear()
        print(tr(lang, "emergency_helper"))
        print(tr(lang, "emergency_numbers"))
        print("-" * 72)
        rows = EMERGENCY_CHOICES[lang]
        for i, (label, _query) in enumerate(rows, 1):
            print(f"{i}. {label}")
        print()
        print(tr(lang, "choose_number"))
        choice = input("> ").strip()
        if not choice:
            return
        if choice.isdigit() and 1 <= int(choice) <= len(rows):
            query = rows[int(choice)-1][1]
            results = STORE.search(query, lang, 120)
            # Broad fallback: OR-like search if strict token matching is too narrow.
            if not results:
                terms = query.split()
                merged, seen = [], set()
                for term in terms:
                    for e in STORE.search(term, lang, 60):
                        if e["id"] not in seen:
                            seen.add(e["id"]); merged.append(e)
                results = merged[:120]
            pick_from_entries(results, lang)


def show_recent(lang):
    rows = [STORE.by_id[x] for x in STATE.get("recent", []) if x in STORE.by_id]
    if rows:
        pick_from_entries(rows, lang)
    else:
        print(tr(lang, "no_entries"))
        pause(lang)


def scenario_pack_menu(lang):
    packs = defaultdict(list)
    for entry in STORE.entries:
        for tag in entry.get("tags", []):
            if str(tag).startswith("pack:"):
                packs[str(tag).split(":", 1)[1]].append(entry)
    if not packs:
        pause(lang, tr(lang, "no_entries"))
        return
    labels = {
        "first30": ("First 30 minutes", "Τα πρώτα 30 λεπτά"),
        "earthquake": ("Earthquake", "Σεισμός"), "wildfire": ("Wildfire", "Δασική πυρκαγιά"),
        "flood": ("Flood", "Πλημμύρα"), "storm": ("Severe weather", "Έντονα καιρικά φαινόμενα"),
        "outage": ("Power outage", "Διακοπή ρεύματος"), "utilities": ("Home utilities", "Παροχές κατοικίας"),
        "water": ("Emergency water", "Νερό ανάγκης"), "food": ("Emergency food", "Τρόφιμα ανάγκης"),
        "accessibility": ("Accessibility and support needs", "Προσβασιμότητα και ανάγκες υποστήριξης"),
        "medicine": ("Medicine continuity", "Συνέχεια φαρμάκων"), "travel": ("Travel and vehicle", "Μετακίνηση και όχημα"),
        "recovery": ("Cleanup and recovery", "Καθαρισμός και αποκατάσταση"),
        "coordination": ("Family and information coordination", "Συντονισμός οικογένειας και πληροφοριών"),
        "greece": ("Greece, islands, villages and coast", "Ελλάδα, νησιά, χωριά και ακτές"),
        "structural": ("Collapse, entrapment and missing people", "Κατάρρευση, παγίδευση και αγνοούμενοι"),
        "continuity": ("Financial and digital continuity", "Οικονομική και ψηφιακή συνέχεια"),
    }
    preferred = ["first30","earthquake","wildfire","flood","storm","outage","utilities","water","food","medicine","accessibility","travel","recovery","coordination","structural","continuity","greece"]
    keys = [k for k in preferred if k in packs] + sorted(k for k in packs if k not in preferred)
    while True:
        clear(); print(tr(lang, "scenario_packs")); print("-" * 72)
        for i, key in enumerate(keys, 1):
            label = labels.get(key, (key.replace("_", " ").title(), key))[1 if lang == "el" else 0]
            print(f"{i}. {label} ({len(packs[key])})")
        print("\n" + tr(lang, "choose_number")); choice = input("> ").strip()
        if not choice: return
        if choice.isdigit() and 1 <= int(choice) <= len(keys):
            pick_from_entries(packs[keys[int(choice)-1]], lang)

def main():
    lang = STATE.get("language", "en")
    explicit_language = False
    if lang not in {"en", "el"}:
        lang = "en"
    if "--lang" in sys.argv:
        try:
            requested = sys.argv[sys.argv.index("--lang") + 1]
            if requested in {"en", "el"}:
                lang = requested
                explicit_language = True
        except (ValueError, IndexError):
            pass
    if "--audit" in sys.argv:
        report = STORE.integrity_report()
        print(json.dumps({k: len(v) for k, v in report.items()}, ensure_ascii=False, indent=2))
        return
    if "--stats" in sys.argv:
        print(json.dumps(STORE.stats(), ensure_ascii=False, indent=2))
        return
    if not os.path.exists(STATE_FILE) and not explicit_language:
        lang = choose_language(lang)
    STATE["language"] = lang
    save_state(STATE)
    while True:
        clear()
        print_menu(lang)
        try:
            choice = input("\n> ").strip()
        except EOFError:
            break
        if choice == "1":
            emergency_helper(lang)
        elif choice == "2":
            query = input(f"{tr(lang, 'query')}: ").strip()
            pick_from_entries(STORE.search(query, lang), lang)
        elif choice == "3":
            scenario_pack_menu(lang)
        elif choice == "4":
            clear()
            print(tr(lang, "quick_note"))
            print()
            pick_from_entries(STORE.quick_entries(), lang)
        elif choice == "5":
            show_recent(lang)
        elif choice == "6":
            favorites = [STORE.by_id[x] for x in STATE.get("favorites", []) if x in STORE.by_id]
            if favorites:
                pick_from_entries(favorites, lang)
            else:
                print(tr(lang, "empty_favorites"))
                pause(lang)
        elif choice == "7":
            pick_from_entries(STORE.entries, lang)
        elif choice == "8":
            browse_mapping(STORE.by_category, lang, "categories")
        elif choice == "9":
            browse_mapping(STORE.by_file, lang, "files")
        elif choice == "10":
            readiness_check(lang)
        elif choice == "11":
            build_plan(lang)
        elif choice == "12":
            launch_web_ui(lang)
        elif choice == "13":
            export_menu(lang)
        elif choice == "14":
            show_stats(lang)
        elif choice == "15":
            show_integrity(lang)
        elif choice == "16":
            show_updates(lang)
        elif choice == "17":
            show_source_guide(lang)
        elif choice == "18":
            lang = choose_language(lang)
            STATE["language"] = lang
            save_state(STATE)
        elif choice == "19":
            STORE.load()
            print(tr(lang, "database_reloaded"))
            pause(lang)
        elif choice == "0":
            break


if __name__ == "__main__":
    main()
