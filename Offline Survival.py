#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import re
import sys
import textwrap
from collections import Counter, defaultdict
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DB_DIR = BASE_DIR / "Offline Survival Database"
UPDATES_DIR = BASE_DIR / "Offline Survival Updates"

LANGS = {
    "en": {
        "app_title": "Offline Survival",
        "choose_language": "Choose language: [1] English  [2] Ελληνικά",
        "invalid": "Invalid choice.",
        "main_menu": "Main Menu",
        "search": "Search all topics",
        "browse_topics": "Browse by topic",
        "browse_files": "Browse by file",
        "browse_categories": "Browse by category",
        "stats": "Statistics",
        "integrity": "Integrity check",
        "updates": "Read update logs",
        "switch_lang": "Switch language",
        "reload": "Reload database",
        "exit": "Exit",
        "back": "Back",
        "prompt": "Select an option: ",
        "search_prompt": "Enter search text: ",
        "no_results": "No results found.",
        "results": "Results",
        "open_entry": "Enter result number to open, or press Enter to go back: ",
        "file_label": "File",
        "topic_label": "Topic",
        "category_label": "Category",
        "subcategory_label": "Subcategory",
        "tags_label": "Tags",
        "summary_label": "Summary",
        "content_label": "Content",
        "steps_label": "Steps",
        "warnings_label": "Warnings",
        "mistakes_label": "Common mistakes",
        "related_label": "Related topics",
        "difficulty_label": "Difficulty",
        "urgency_label": "Urgency",
        "priority_label": "Priority",
        "updated_label": "Last updated",
        "note_label": "Update note",
        "materials_label": "Materials / resources",
        "alternatives_label": "Alternatives / low-resource options",
        "failure_label": "Signs of failure or drift",
        "when_not_label": "When not to use / when to stop",
        "entries_loaded": "Entries loaded",
        "json_files": "JSON files",
        "malformed_files": "Malformed files",
        "duplicate_ids": "Duplicate IDs",
        "duplicate_topics": "Duplicate topic titles",
        "integrity_ok": "No duplicate IDs or duplicate topic titles were found.",
        "updates_empty": "No update logs found.",
        "press_enter": "Press Enter to continue...",
        "choose_topic": "Enter number to open, or press Enter to go back: ",
        "language_switched": "Language switched.",
        "reload_done": "Database reloaded.",
        "db_missing": "Database folder not found.",
        "loading_error": "A database error occurred while loading files.",
        "searching": "Searching",
        "preview_label": "Preview",
        "source_label": "Source",
        "category_menu": "Categories",
        "file_menu": "Files",
        "topic_menu": "Topics",
        "update_menu": "Update logs",
        "errors_label": "File load errors",
    },
    "el": {
        "app_title": "Offline Survival",
        "choose_language": "Επίλεξε γλώσσα: [1] English  [2] Ελληνικά",
        "invalid": "Μη έγκυρη επιλογή.",
        "main_menu": "Κύριο Μενού",
        "search": "Αναζήτηση σε όλα τα θέματα",
        "browse_topics": "Περιήγηση ανά θέμα",
        "browse_files": "Περιήγηση ανά αρχείο",
        "browse_categories": "Περιήγηση ανά κατηγορία",
        "stats": "Στατιστικά",
        "integrity": "Έλεγχος ακεραιότητας",
        "updates": "Ανάγνωση αρχείων ενημέρωσης",
        "switch_lang": "Αλλαγή γλώσσας",
        "reload": "Επαναφόρτωση βάσης",
        "exit": "Έξοδος",
        "back": "Πίσω",
        "prompt": "Διάλεξε επιλογή: ",
        "search_prompt": "Δώσε κείμενο αναζήτησης: ",
        "no_results": "Δεν βρέθηκαν αποτελέσματα.",
        "results": "Αποτελέσματα",
        "open_entry": "Δώσε αριθμό για άνοιγμα ή πάτησε Enter για επιστροφή: ",
        "file_label": "Αρχείο",
        "topic_label": "Θέμα",
        "category_label": "Κατηγορία",
        "subcategory_label": "Υποκατηγορία",
        "tags_label": "Ετικέτες",
        "summary_label": "Σύνοψη",
        "content_label": "Περιεχόμενο",
        "steps_label": "Βήματα",
        "warnings_label": "Προειδοποιήσεις",
        "mistakes_label": "Συχνά λάθη",
        "related_label": "Σχετικά θέματα",
        "difficulty_label": "Δυσκολία",
        "urgency_label": "Επείγον",
        "priority_label": "Προτεραιότητα",
        "updated_label": "Τελευταία ενημέρωση",
        "note_label": "Σημείωση ενημέρωσης",
        "materials_label": "Υλικά / πόροι",
        "alternatives_label": "Εναλλακτικές / λύσεις λίγων πόρων",
        "failure_label": "Σημάδια αποτυχίας ή εκτροπής",
        "when_not_label": "Πότε να μη χρησιμοποιηθεί / πότε να σταματήσεις",
        "entries_loaded": "Φορτωμένες εγγραφές",
        "json_files": "Αρχεία JSON",
        "malformed_files": "Προβληματικά αρχεία",
        "duplicate_ids": "Διπλά IDs",
        "duplicate_topics": "Διπλοί τίτλοι θεμάτων",
        "integrity_ok": "Δεν βρέθηκαν διπλά IDs ή διπλοί τίτλοι θεμάτων.",
        "updates_empty": "Δεν βρέθηκαν αρχεία ενημέρωσης.",
        "press_enter": "Πάτησε Enter για συνέχεια...",
        "choose_topic": "Δώσε αριθμό για άνοιγμα ή πάτησε Enter για επιστροφή: ",
        "language_switched": "Η γλώσσα άλλαξε.",
        "reload_done": "Η βάση επαναφορτώθηκε.",
        "db_missing": "Ο φάκελος της βάσης δεν βρέθηκε.",
        "loading_error": "Παρουσιάστηκε σφάλμα κατά τη φόρτωση της βάσης.",
        "searching": "Αναζήτηση",
        "preview_label": "Προεπισκόπηση",
        "source_label": "Πηγή",
        "category_menu": "Κατηγορίες",
        "file_menu": "Αρχεία",
        "topic_menu": "Θέματα",
        "update_menu": "Αρχεία ενημέρωσης",
        "errors_label": "Σφάλματα φόρτωσης αρχείων",
    },
}


def clear_screen():
    if os.environ.get("TERM"):
        os.system("clear")
    else:
        print("\n" * 4)


def pause(lang):
    input(LANGS[lang]["press_enter"])


def wrap(text, width=94):
    lines = []
    for block in str(text).split("\n"):
        if not block.strip():
            lines.append("")
        else:
            lines.extend(textwrap.wrap(block, width=width, replace_whitespace=False, drop_whitespace=True) or [""])
    return "\n".join(lines)


def safe_lower(value):
    try:
        return str(value).casefold()
    except Exception:
        return ""


def as_list(value):
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def pretty_name(path):
    return path.name


class OfflineSurvivalApp:
    def __init__(self):
        self.lang = "en"
        self.entries = []
        self.file_errors = []
        self.update_logs = []
        self.indexed = []
        self.load_all()

    def load_all(self):
        self.entries = []
        self.file_errors = []
        self.indexed = []
        self.update_logs = []

        if not DB_DIR.exists():
            return

        for path in sorted(DB_DIR.glob("*.json")):
            try:
                raw = json.loads(path.read_text(encoding="utf-8"))
                if isinstance(raw, dict):
                    raw = [raw]
                if not isinstance(raw, list):
                    raise ValueError("JSON root is not a list/object")
                for entry in raw:
                    if not isinstance(entry, dict):
                        continue
                    item = dict(entry)
                    item["_source_file"] = pretty_name(path)
                    self.entries.append(item)
            except Exception as exc:
                self.file_errors.append((pretty_name(path), str(exc)))

        self.entries.sort(key=lambda e: safe_lower(e.get("topic", "")))
        for entry in self.entries:
            parts = [
                entry.get("topic", ""),
                entry.get("topic_en", ""),
                entry.get("topic_el", ""),
                entry.get("category", ""),
                entry.get("subcategory", ""),
                " ".join(as_list(entry.get("tags"))),
                entry.get("summary_en", ""),
                entry.get("summary_el", ""),
                entry.get("content_en", ""),
                entry.get("content_el", ""),
                " ".join(as_list(entry.get("steps_en"))),
                " ".join(as_list(entry.get("steps_el"))),
                " ".join(as_list(entry.get("warnings_en"))),
                " ".join(as_list(entry.get("warnings_el"))),
                " ".join(as_list(entry.get("mistakes_en"))),
                " ".join(as_list(entry.get("mistakes_el"))),
                " ".join(as_list(entry.get("related_topics"))),
                " ".join(as_list(entry.get("materials_en"))),
                " ".join(as_list(entry.get("materials_el"))),
                " ".join(as_list(entry.get("alternatives_en"))),
                " ".join(as_list(entry.get("alternatives_el"))),
                " ".join(as_list(entry.get("failure_signs_en"))),
                " ".join(as_list(entry.get("failure_signs_el"))),
                " ".join(as_list(entry.get("when_not_to_use_en"))),
                " ".join(as_list(entry.get("when_not_to_use_el"))),
                entry.get("_source_file", ""),
            ]
            self.indexed.append((entry, safe_lower(" ".join(parts))))

        if UPDATES_DIR.exists():
            for path in sorted(UPDATES_DIR.glob("*.txt")):
                try:
                    self.update_logs.append((pretty_name(path), path.read_text(encoding="utf-8")))
                except Exception as exc:
                    self.update_logs.append((pretty_name(path), f"[read error] {exc}"))

    def choose_language(self):
        while True:
            clear_screen()
            print(LANGS["en"]["app_title"])
            print("=" * 40)
            choice = input(LANGS["en"]["choose_language"] + "\n> ").strip()
            if choice == "1":
                self.lang = "en"
                return
            if choice == "2":
                self.lang = "el"
                return
            print(LANGS["en"]["invalid"])
            pause("en")

    def t(self, key):
        return LANGS[self.lang][key]

    def field(self, entry, base):
        if self.lang == "el":
            return entry.get(base + "_el") or entry.get(base + "_en") or ""
        return entry.get(base + "_en") or entry.get(base + "_el") or ""

    def list_field(self, entry, base):
        val = self.field(entry, base)
        return as_list(val)

    def preview(self, entry, max_len=150):
        text = self.field(entry, "summary") or self.field(entry, "content")
        text = re.sub(r"\s+", " ", str(text)).strip()
        if len(text) > max_len:
            return text[: max_len - 1].rstrip() + "…"
        return text

    def print_entry(self, entry):
        clear_screen()
        title = entry.get("topic_el") if self.lang == "el" and entry.get("topic_el") else entry.get("topic", "Untitled")
        print(title)
        print("=" * 94)
        meta = [
            (self.t("source_label"), entry.get("_source_file", "")),
            (self.t("category_label"), entry.get("category", "")),
            (self.t("subcategory_label"), entry.get("subcategory", "")),
            (self.t("difficulty_label"), entry.get("difficulty", "")),
            (self.t("urgency_label"), entry.get("urgency", "")),
            (self.t("priority_label"), entry.get("priority", "")),
            (self.t("updated_label"), entry.get("last_updated", "")),
        ]
        for label, value in meta:
            if value:
                print(f"{label}: {value}")
        tags = ", ".join(as_list(entry.get("tags")))
        if tags:
            print(f"{self.t('tags_label')}: {tags}")

        sections = [
            (self.t("summary_label"), self.field(entry, "summary")),
            (self.t("content_label"), self.field(entry, "content")),
            (self.t("materials_label"), self.list_field(entry, "materials")),
            (self.t("steps_label"), self.list_field(entry, "steps")),
            (self.t("alternatives_label"), self.list_field(entry, "alternatives")),
            (self.t("warnings_label"), self.list_field(entry, "warnings")),
            (self.t("failure_label"), self.list_field(entry, "failure_signs")),
            (self.t("mistakes_label"), self.list_field(entry, "mistakes")),
            (self.t("when_not_label"), self.list_field(entry, "when_not_to_use")),
            (self.t("related_label"), as_list(entry.get("related_topics"))),
            (self.t("note_label"), entry.get("update_note", "")),
        ]

        for heading, value in sections:
            if not value:
                continue
            print("\n" + heading)
            print("-" * len(heading))
            if isinstance(value, list):
                for item in value:
                    print("• " + wrap(item, 90).replace("\n", "\n  "))
            else:
                print(wrap(value, 94))
        pause(self.lang)

    def pick_from_entries(self, items, title):
        if not items:
            clear_screen()
            print(self.t("no_results"))
            pause(self.lang)
            return
        page_size = 15
        page = 0
        while True:
            clear_screen()
            print(title)
            print("=" * 94)
            total_pages = max(1, (len(items) + page_size - 1) // page_size)
            start = page * page_size
            chunk = items[start : start + page_size]
            for i, entry in enumerate(chunk, start=1):
                absolute = start + i
                preview = self.preview(entry)
                print(f"{absolute:>3}. {entry.get('topic','')}")
                print(f"     {self.t('source_label')}: {entry.get('_source_file','')} | {self.t('category_label')}: {entry.get('category','')}")
                print(f"     {self.t('preview_label')}: {preview}")
            print(f"\n[{page + 1}/{total_pages}] n=next  p=prev")
            choice = input(self.t("choose_topic")).strip().lower()
            if not choice:
                return
            if choice == "n" and page < total_pages - 1:
                page += 1
                continue
            if choice == "p" and page > 0:
                page -= 1
                continue
            if choice.isdigit():
                idx = int(choice)
                if 1 <= idx <= len(items):
                    self.print_entry(items[idx - 1])

    def search_entries(self):
        clear_screen()
        query = input(self.t("search_prompt")).strip()
        if not query:
            return
        q = safe_lower(query)
        results = [entry for entry, hay in self.indexed if q in hay]
        self.pick_from_entries(results, f"{self.t('results')}: {query}")

    def browse_topics(self):
        self.pick_from_entries(self.entries, self.t("topic_menu"))

    def browse_files(self):
        grouped = defaultdict(list)
        for e in self.entries:
            grouped[e.get("_source_file", "")].append(e)
        files = sorted(grouped.items(), key=lambda kv: safe_lower(kv[0]))
        while True:
            clear_screen()
            print(self.t("file_menu"))
            print("=" * 94)
            for i, (fname, items) in enumerate(files, start=1):
                print(f"{i:>3}. {fname} ({len(items)})")
            choice = input(self.t("choose_topic")).strip()
            if not choice:
                return
            if choice.isdigit():
                idx = int(choice)
                if 1 <= idx <= len(files):
                    fname, items = files[idx - 1]
                    self.pick_from_entries(items, f"{self.t('file_label')}: {fname}")

    def browse_categories(self):
        grouped = defaultdict(list)
        for e in self.entries:
            grouped[e.get("category", "uncategorized")].append(e)
        cats = sorted(grouped.items(), key=lambda kv: safe_lower(kv[0]))
        while True:
            clear_screen()
            print(self.t("category_menu"))
            print("=" * 94)
            for i, (cat, items) in enumerate(cats, start=1):
                print(f"{i:>3}. {cat} ({len(items)})")
            choice = input(self.t("choose_topic")).strip()
            if not choice:
                return
            if choice.isdigit():
                idx = int(choice)
                if 1 <= idx <= len(cats):
                    cat, items = cats[idx - 1]
                    self.pick_from_entries(items, f"{self.t('category_label')}: {cat}")

    def show_stats(self):
        clear_screen()
        print(self.t("stats"))
        print("=" * 94)
        print(f"{self.t('entries_loaded')}: {len(self.entries)}")
        print(f"{self.t('json_files')}: {len(list(DB_DIR.glob('*.json')))}")
        print(f"{self.t('malformed_files')}: {len(self.file_errors)}")
        categories = Counter(e.get("category", "uncategorized") for e in self.entries)
        print("\nTop categories:")
        for cat, count in categories.most_common(15):
            print(f"• {cat}: {count}")
        if self.file_errors:
            print(f"\n{self.t('errors_label')}:")
            for fname, err in self.file_errors[:20]:
                print(f"• {fname}: {err}")
        pause(self.lang)

    def integrity_check(self):
        clear_screen()
        print(self.t("integrity"))
        print("=" * 94)
        ids = [e.get("id", "") for e in self.entries if e.get("id")]
        topics = [e.get("topic", "") for e in self.entries if e.get("topic")]
        dup_ids = [k for k, v in Counter(ids).items() if v > 1]
        dup_topics = [k for k, v in Counter(topics).items() if v > 1]
        print(f"{self.t('duplicate_ids')}: {len(dup_ids)}")
        print(f"{self.t('duplicate_topics')}: {len(dup_topics)}")
        if not dup_ids and not dup_topics:
            print(self.t("integrity_ok"))
        if dup_ids[:20]:
            print("\nDuplicate IDs:")
            for item in dup_ids[:20]:
                print("•", item)
        if dup_topics[:20]:
            print("\nDuplicate topics:")
            for item in dup_topics[:20]:
                print("•", item)
        if self.file_errors:
            print(f"\n{self.t('errors_label')}:")
            for fname, err in self.file_errors[:20]:
                print(f"• {fname}: {err}")
        pause(self.lang)

    def read_update_logs(self):
        if not self.update_logs:
            clear_screen()
            print(self.t("updates_empty"))
            pause(self.lang)
            return
        while True:
            clear_screen()
            print(self.t("update_menu"))
            print("=" * 94)
            for i, (name, _) in enumerate(self.update_logs, start=1):
                print(f"{i:>3}. {name}")
            choice = input(self.t("choose_topic")).strip()
            if not choice:
                return
            if choice.isdigit():
                idx = int(choice)
                if 1 <= idx <= len(self.update_logs):
                    name, content = self.update_logs[idx - 1]
                    clear_screen()
                    print(name)
                    print("=" * 94)
                    print(wrap(content, 94))
                    pause(self.lang)

    def run(self):
        self.choose_language()
        while True:
            clear_screen()
            print(self.t("app_title"))
            print("=" * 94)
            print(f"1. {self.t('search')}")
            print(f"2. {self.t('browse_topics')}")
            print(f"3. {self.t('browse_files')}")
            print(f"4. {self.t('browse_categories')}")
            print(f"5. {self.t('stats')}")
            print(f"6. {self.t('integrity')}")
            print(f"7. {self.t('updates')}")
            print(f"8. {self.t('switch_lang')}")
            print(f"9. {self.t('reload')}")
            print(f"0. {self.t('exit')}")
            choice = input("\n" + self.t("prompt")).strip()
            if choice == "1":
                self.search_entries()
            elif choice == "2":
                self.browse_topics()
            elif choice == "3":
                self.browse_files()
            elif choice == "4":
                self.browse_categories()
            elif choice == "5":
                self.show_stats()
            elif choice == "6":
                self.integrity_check()
            elif choice == "7":
                self.read_update_logs()
            elif choice == "8":
                self.lang = "el" if self.lang == "en" else "en"
                clear_screen()
                print(self.t("language_switched"))
                pause(self.lang)
            elif choice == "9":
                self.load_all()
                clear_screen()
                print(self.t("reload_done"))
                pause(self.lang)
            elif choice == "0":
                return
            else:
                clear_screen()
                print(self.t("invalid"))
                pause(self.lang)


def main():
    try:
        app = OfflineSurvivalApp()
        if not DB_DIR.exists():
            print(LANGS["en"]["db_missing"])
            sys.exit(1)
        app.run()
    except KeyboardInterrupt:
        print("\nExiting.")
    except Exception as exc:
        print("\nFatal error:", exc)
        sys.exit(1)


if __name__ == "__main__":
    main()
