#!/usr/bin/env python3
"""Offline Survival Project terminal browser.

A dependency-free, bilingual terminal application for searching, finding,
browsing, validating, and reading the English and Greek JSON databases that
ship with this repository.
"""

from __future__ import annotations

import json
import random
import shutil
import sys
import textwrap
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Callable, Optional, Sequence

APP_NAME = "Offline Survival Project"
PROJECT_ROOT = Path(__file__).resolve().parent
SETTINGS_DIR = Path.home() / ".offline_survival_project"
SETTINGS_FILE = SETTINGS_DIR / "settings.json"

LANGUAGES = {
    "en": {"folder": "English", "name": "English"},
    "el": {"folder": "Ελληνικά", "name": "Ελληνικά"},
}

DEFAULT_SETTINGS: dict[str, Any] = {
    "language": "en",
    "page_size": 10,
    "clear_screen": True,
}

BACK_COMMANDS = {
    "0",
    "q",
    "quit",
    "exit",
    "b",
    "back",
    "πισω",
    "εξοδος",
}
NEXT_COMMANDS = {"", "n", "next", "ε", "επομενη"}
PREVIOUS_COMMANDS = {"p", "prev", "previous", "π", "προηγουμενη"}
YES_COMMANDS = {"y", "yes", "ν", "ναι"}
NO_COMMANDS = {"n", "no", "ο", "οχι", "0", "q"}

TEXT: dict[str, dict[str, str]] = {
    "en": {
        "header_language": "Language",
        "main_menu": "Main menu",
        "search": "Search the knowledge base",
        "browse": "Browse categories",
        "find_file": "Find and read a JSON file",
        "open_id": "Open a record by ID",
        "random": "Read a random topic",
        "settings": "Settings",
        "help": "Help and controls",
        "integrity": "Check database integrity",
        "exit": "Exit",
        "goodbye": "Goodbye.",
        "choice": "Choose an option",
        "invalid": "Invalid option. Please try again.",
        "press_enter": "Press Enter to continue",
        "search_prompt": "Search words (or 0 to go back)",
        "file_prompt": "File name/path words; Enter shows every file (or 0 to go back)",
        "id_prompt": "Complete or partial record ID (or 0 to go back)",
        "no_results": "No matching results were found.",
        "results": "results",
        "records": "records",
        "files": "files",
        "categories": "categories",
        "loading": "Loading the selected database...",
        "loaded": "Database loaded",
        "load_error": "The database could not be loaded",
        "missing_folder": "The selected language folder is missing",
        "select_item": "Choose a visible number | n/Enter: next | p: previous | 0/q: back",
        "reader_controls": "Enter/n: next page | p: previous page | 0/q: back",
        "reader_return": "Press Enter or 0/q to return",
        "back": "Back",
        "page": "Page",
        "of": "of",
        "category_filter": "Category words; Enter shows every category (or 0 to go back)",
        "records_in_category": "Records in category",
        "file_actions": "File options",
        "browse_file_records": "Browse records in this file",
        "view_raw_json": "Read the raw JSON",
        "file_path": "File path",
        "source_file": "Source file",
        "raw_json": "Raw JSON",
        "change_language": "Change language",
        "page_size": "Results per list page",
        "clear_screen": "Clear the screen between views",
        "enabled": "Enabled",
        "disabled": "Disabled",
        "reset_settings": "Reset all settings",
        "settings_saved": "Settings saved.",
        "settings_file": "Settings file",
        "settings_save_error": "Settings could not be saved. Check storage permissions.",
        "choose_language": "Choose interface and database language",
        "choose_page_size": "Choose results per list page",
        "settings_reset": "Settings reset to their defaults.",
        "confirm_reset": "Reset language, page size, and screen setting? (y/n)",
        "first_run": "First launch: choose a language",
        "about_title": "Help and controls",
        "about_text": (
            "The application works fully offline and uses only Python's standard library. "
            "Use numbers to open menu items. In lists, use n or Enter for the next page, p for "
            "the previous page, and 0 or q to go back. Record and raw-file views are paged so "
            "long information remains readable on small Termux screens. Search checks every "
            "record field, including materials, steps, warnings, tags, IDs, and file paths."
        ),
        "safety_title": "Safety",
        "safety_text": (
            "This is a preparation and reference aid, not a replacement for emergency services "
            "or qualified medical, engineering, electrical, utility, fire, police, coast guard, "
            "veterinary, agricultural, or civil-protection guidance."
        ),
        "search_results": "Search results",
        "empty_query": "Enter at least one search word.",
        "raw_read_error": "The raw file could not be read.",
        "unexpected_error": "An unexpected error occurred",
        "another_random": "Open another random topic? (y/n)",
        "integrity_running": "Checking every JSON file in both languages...",
        "integrity_title": "Database integrity report",
        "integrity_ok": "All integrity checks passed.",
        "integrity_failed": "One or more integrity checks failed.",
        "language_report": "Language database",
        "json_files": "JSON files",
        "category_folders": "category folders",
        "duplicate_ids": "duplicate IDs",
        "duplicate_titles": "duplicate titles",
        "invalid_files": "invalid files",
        "missing_fields": "missing required fields",
        "empty_fields": "empty required fields",
        "mirrored_paths": "Mirrored file paths",
        "mirrored_ids": "Mirrored record IDs",
        "mirrored_file_ids": "IDs inside corresponding files",
        "database_folder": "Database folder present",
        "matching": "matching",
        "not_matching": "not matching",
        "yes": "Yes",
        "no": "No",
        "untitled": "Untitled",
        "uncategorized": "Uncategorized",
    },
    "el": {
        "header_language": "Γλώσσα",
        "main_menu": "Κεντρικό μενού",
        "search": "Αναζήτηση στη βάση γνώσεων",
        "browse": "Περιήγηση στις κατηγορίες",
        "find_file": "Εύρεση και ανάγνωση αρχείου JSON",
        "open_id": "Άνοιγμα εγγραφής με ID",
        "random": "Ανάγνωση τυχαίου θέματος",
        "settings": "Ρυθμίσεις",
        "help": "Βοήθεια και χειρισμός",
        "integrity": "Έλεγχος ακεραιότητας βάσης",
        "exit": "Έξοδος",
        "goodbye": "Έξοδος από την εφαρμογή.",
        "choice": "Επίλεξε μία επιλογή",
        "invalid": "Μη έγκυρη επιλογή. Δοκίμασε ξανά.",
        "press_enter": "Πάτησε Enter για συνέχεια",
        "search_prompt": "Λέξεις αναζήτησης (ή 0 για επιστροφή)",
        "file_prompt": "Λέξεις ονόματος/διαδρομής· Enter για όλα τα αρχεία (ή 0 για επιστροφή)",
        "id_prompt": "Ολόκληρο ή μέρος του ID εγγραφής (ή 0 για επιστροφή)",
        "no_results": "Δεν βρέθηκαν αποτελέσματα.",
        "results": "αποτελέσματα",
        "records": "εγγραφές",
        "files": "αρχεία",
        "categories": "κατηγορίες",
        "loading": "Φόρτωση της επιλεγμένης βάσης...",
        "loaded": "Η βάση φορτώθηκε",
        "load_error": "Δεν ήταν δυνατή η φόρτωση της βάσης",
        "missing_folder": "Λείπει ο φάκελος της επιλεγμένης γλώσσας",
        "select_item": "Επίλεξε ορατό αριθμό | n/Enter: επόμενη | p: προηγούμενη | 0/q: επιστροφή",
        "reader_controls": "Enter/n: επόμενη σελίδα | p: προηγούμενη | 0/q: επιστροφή",
        "reader_return": "Πάτησε Enter ή 0/q για επιστροφή",
        "back": "Επιστροφή",
        "page": "Σελίδα",
        "of": "από",
        "category_filter": "Λέξεις κατηγορίας· Enter για όλες (ή 0 για επιστροφή)",
        "records_in_category": "Εγγραφές στην κατηγορία",
        "file_actions": "Επιλογές αρχείου",
        "browse_file_records": "Περιήγηση στις εγγραφές του αρχείου",
        "view_raw_json": "Ανάγνωση του αρχικού JSON",
        "file_path": "Διαδρομή αρχείου",
        "source_file": "Αρχείο προέλευσης",
        "raw_json": "Αρχικό JSON",
        "change_language": "Αλλαγή γλώσσας",
        "page_size": "Αποτελέσματα ανά σελίδα λίστας",
        "clear_screen": "Καθαρισμός οθόνης μεταξύ προβολών",
        "enabled": "Ενεργός",
        "disabled": "Ανενεργός",
        "reset_settings": "Επαναφορά όλων των ρυθμίσεων",
        "settings_saved": "Οι ρυθμίσεις αποθηκεύτηκαν.",
        "settings_file": "Αρχείο ρυθμίσεων",
        "settings_save_error": "Δεν αποθηκεύτηκαν οι ρυθμίσεις. Έλεγξε τα δικαιώματα αποθήκευσης.",
        "choose_language": "Επίλεξε γλώσσα περιβάλλοντος και βάσης",
        "choose_page_size": "Επίλεξε αποτελέσματα ανά σελίδα λίστας",
        "settings_reset": "Οι ρυθμίσεις επανήλθαν στις προεπιλογές.",
        "confirm_reset": "Επαναφορά γλώσσας, μεγέθους σελίδας και οθόνης; (ν/ο)",
        "first_run": "Πρώτη εκκίνηση: επίλεξε γλώσσα",
        "about_title": "Βοήθεια και χειρισμός",
        "about_text": (
            "Η εφαρμογή λειτουργεί πλήρως εκτός σύνδεσης και χρησιμοποιεί μόνο την τυπική "
            "βιβλιοθήκη της Python. Χρησιμοποίησε αριθμούς για να ανοίξεις επιλογές. Στις λίστες, "
            "χρησιμοποίησε n ή Enter για την επόμενη σελίδα, p για την προηγούμενη και 0 ή q για "
            "επιστροφή. Οι εγγραφές και τα αρχικά αρχεία εμφανίζονται σε σελίδες ώστε να "
            "διαβάζονται εύκολα σε μικρές οθόνες Termux. Η αναζήτηση ελέγχει όλα τα πεδία, "
            "μαζί με υλικά, βήματα, προειδοποιήσεις, ετικέτες, IDs και διαδρομές αρχείων."
        ),
        "safety_title": "Ασφάλεια",
        "safety_text": (
            "Το έργο είναι βοήθημα προετοιμασίας και αναφοράς και δεν αντικαθιστά τις υπηρεσίες "
            "έκτακτης ανάγκης ούτε την καθοδήγηση αρμόδιων επαγγελματιών υγείας, μηχανικών, "
            "ηλεκτρολόγων, τεχνικών δικτύων, πυροσβεστικής, αστυνομίας, λιμενικού, κτηνιάτρων, "
            "γεωπόνων ή πολιτικής προστασίας."
        ),
        "search_results": "Αποτελέσματα αναζήτησης",
        "empty_query": "Γράψε τουλάχιστον μία λέξη αναζήτησης.",
        "raw_read_error": "Δεν ήταν δυνατή η ανάγνωση του αρχείου.",
        "unexpected_error": "Παρουσιάστηκε απρόσμενο σφάλμα",
        "another_random": "Άνοιγμα άλλου τυχαίου θέματος; (ν/ο)",
        "integrity_running": "Έλεγχος όλων των αρχείων JSON και στις δύο γλώσσες...",
        "integrity_title": "Αναφορά ακεραιότητας βάσης",
        "integrity_ok": "Όλοι οι έλεγχοι ακεραιότητας ολοκληρώθηκαν επιτυχώς.",
        "integrity_failed": "Ένας ή περισσότεροι έλεγχοι ακεραιότητας απέτυχαν.",
        "language_report": "Βάση γλώσσας",
        "json_files": "αρχεία JSON",
        "category_folders": "φάκελοι κατηγοριών",
        "duplicate_ids": "διπλότυπα IDs",
        "duplicate_titles": "διπλότυποι τίτλοι",
        "invalid_files": "μη έγκυρα αρχεία",
        "missing_fields": "απόντα υποχρεωτικά πεδία",
        "empty_fields": "κενά υποχρεωτικά πεδία",
        "mirrored_paths": "Κατοπτρισμένες διαδρομές αρχείων",
        "mirrored_ids": "Κατοπτρισμένα IDs εγγραφών",
        "mirrored_file_ids": "IDs μέσα στα αντίστοιχα αρχεία",
        "database_folder": "Υπάρχει ο φάκελος βάσης",
        "matching": "ταιριάζουν",
        "not_matching": "δεν ταιριάζουν",
        "yes": "Ναι",
        "no": "Όχι",
        "untitled": "Χωρίς τίτλο",
        "uncategorized": "Χωρίς κατηγορία",
    },
}

FIELD_LABELS: dict[str, dict[str, str]] = {
    "en": {
        "id": "ID",
        "language": "Language",
        "title": "Title",
        "category": "Category",
        "subcategory": "Subcategory",
        "summary": "Summary",
        "content": "Full guidance",
        "difficulty": "Difficulty",
        "urgency": "Urgency",
        "priority": "Priority",
        "tags": "Tags",
        "materials": "Materials",
        "steps": "Steps",
        "warnings": "Warnings",
        "common_mistakes": "Common mistakes",
        "alternatives": "Alternatives",
        "failure_signs": "Failure signs",
        "when_not_to_use": "When not to use",
        "short_term": "Short-term actions",
        "long_term": "Long-term actions",
        "if_method_fails": "If the method fails",
        "environment_notes": "Environment notes",
        "related_topics": "Related topics",
        "sources": "Sources",
        "last_updated": "Last updated",
    },
    "el": {
        "id": "ID",
        "language": "Γλώσσα",
        "title": "Τίτλος",
        "category": "Κατηγορία",
        "subcategory": "Υποκατηγορία",
        "summary": "Σύνοψη",
        "content": "Πλήρεις οδηγίες",
        "difficulty": "Δυσκολία",
        "urgency": "Επείγον",
        "priority": "Προτεραιότητα",
        "tags": "Ετικέτες",
        "materials": "Υλικά",
        "steps": "Βήματα",
        "warnings": "Προειδοποιήσεις",
        "common_mistakes": "Συνηθισμένα λάθη",
        "alternatives": "Εναλλακτικές",
        "failure_signs": "Ενδείξεις αποτυχίας",
        "when_not_to_use": "Πότε να μη χρησιμοποιηθεί",
        "short_term": "Βραχυπρόθεσμες ενέργειες",
        "long_term": "Μακροπρόθεσμες ενέργειες",
        "if_method_fails": "Αν η μέθοδος αποτύχει",
        "environment_notes": "Σημειώσεις περιβάλλοντος",
        "related_topics": "Σχετικά θέματα",
        "sources": "Πηγές",
        "last_updated": "Τελευταία ενημέρωση",
    },
}

DISPLAY_ORDER = [
    "id",
    "language",
    "category",
    "subcategory",
    "summary",
    "content",
    "difficulty",
    "urgency",
    "priority",
    "materials",
    "steps",
    "warnings",
    "common_mistakes",
    "alternatives",
    "failure_signs",
    "when_not_to_use",
    "short_term",
    "long_term",
    "if_method_fails",
    "environment_notes",
    "related_topics",
    "tags",
    "sources",
    "last_updated",
]

REQUIRED_FIELDS = tuple(["title", *DISPLAY_ORDER])


def normalize(value: Any) -> str:
    """Return lowercase, accent-insensitive text for English and Greek matching."""
    text = unicodedata.normalize("NFKD", str(value))
    return "".join(character for character in text if not unicodedata.combining(character)).casefold()


def flatten(value: Any) -> str:
    """Convert nested JSON-compatible data to searchable text."""
    if isinstance(value, dict):
        return " ".join(f"{flatten(key)} {flatten(item)}" for key, item in value.items())
    if isinstance(value, (list, tuple, set)):
        return " ".join(flatten(item) for item in value)
    return str(value)


def terminal_size() -> tuple[int, int]:
    size = shutil.get_terminal_size((80, 24))
    return max(20, min(size.columns, 110)), max(12, size.lines)


def terminal_width() -> int:
    return terminal_size()[0]


def divider(character: str = "─") -> str:
    return character * terminal_width()


def wrap_lines(text: Any, initial: str = "", subsequent: str = "") -> list[str]:
    """Wrap text safely for narrow mobile terminals while preserving paragraphs."""
    width = terminal_width()
    paragraphs = str(text).splitlines() or [""]
    output: list[str] = []
    for paragraph in paragraphs:
        if not paragraph.strip():
            output.append("")
            continue
        output.extend(
            textwrap.wrap(
                paragraph.strip(),
                width=max(12, width),
                initial_indent=initial,
                subsequent_indent=subsequent,
                replace_whitespace=False,
                break_long_words=True,
                break_on_hyphens=False,
            )
            or [initial.rstrip()]
        )
    return output



def is_rule_line(line: str) -> bool:
    stripped = line.strip()
    return bool(stripped) and len(set(stripped)) == 1 and stripped[0] in {"·", "─", "═"}


def paginate_lines(lines: Sequence[str], page_height: int) -> list[list[str]]:
    """Split lines into pages without leaving a section heading above its value."""
    content = list(lines) or [""]
    pages: list[list[str]] = []
    start = 0
    while start < len(content):
        end = min(len(content), start + page_height)
        if end < len(content):
            while end > start + 1 and not content[end - 1].strip():
                end -= 1
            if end > start + 2 and is_rule_line(content[end - 1]):
                end -= 2
        if end <= start:
            end = min(len(content), start + page_height)
        pages.append(content[start:end])
        start = end
    return pages

def load_settings() -> tuple[dict[str, Any], bool]:
    settings = dict(DEFAULT_SETTINGS)
    existed = SETTINGS_FILE.is_file()
    if existed:
        try:
            saved = json.loads(SETTINGS_FILE.read_text(encoding="utf-8"))
            if isinstance(saved, dict):
                settings.update(saved)
            else:
                existed = False
        except (OSError, UnicodeError, json.JSONDecodeError):
            existed = False

    if settings.get("language") not in LANGUAGES:
        settings["language"] = DEFAULT_SETTINGS["language"]
    if settings.get("page_size") not in {5, 10, 15, 20}:
        settings["page_size"] = DEFAULT_SETTINGS["page_size"]
    if not isinstance(settings.get("clear_screen"), bool):
        settings["clear_screen"] = DEFAULT_SETTINGS["clear_screen"]
    return settings, existed


def save_settings(settings: dict[str, Any]) -> bool:
    """Atomically save local preferences outside the repository."""
    try:
        SETTINGS_DIR.mkdir(parents=True, exist_ok=True)
        temporary = SETTINGS_FILE.with_suffix(".tmp")
        temporary.write_text(
            json.dumps(settings, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        temporary.replace(SETTINGS_FILE)
        return True
    except OSError:
        return False


class OfflineDatabase:
    """Load, index, search, and validate the bundled JSON databases."""

    def __init__(self) -> None:
        self._records: dict[str, list[dict[str, Any]]] = {}
        self._files: dict[str, dict[str, list[dict[str, Any]]]] = {}

    def language_root(self, language: str) -> Path:
        return PROJECT_ROOT / LANGUAGES[language]["folder"]

    def load(self, language: str) -> list[dict[str, Any]]:
        if language in self._records:
            return self._records[language]

        base = self.language_root(language)
        if not base.is_dir():
            raise FileNotFoundError(base)

        records: list[dict[str, Any]] = []
        files: dict[str, list[dict[str, Any]]] = {}
        paths = sorted(base.rglob("*.json"), key=lambda path: normalize(path.relative_to(base)))

        for path in paths:
            try:
                payload = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, UnicodeError, json.JSONDecodeError) as error:
                raise RuntimeError(f"{path}: {error}") from error

            if not isinstance(payload, list):
                raise RuntimeError(f"{path}: top-level JSON value must be a list")

            relative_path = path.relative_to(base).as_posix()
            file_records: list[dict[str, Any]] = []
            for position, record in enumerate(payload, start=1):
                if not isinstance(record, dict):
                    raise RuntimeError(f"{path}: record {position} must be a JSON object")
                primary_fields = {
                    key: record.get(key, "")
                    for key in ("id", "title", "category", "subcategory", "summary", "tags")
                }
                item = {
                    "record": record,
                    "relative_path": relative_path,
                    "absolute_path": path,
                    "primary_search_text": normalize(f"{relative_path} {flatten(primary_fields)}"),
                    "search_text": normalize(f"{relative_path} {flatten(record)}"),
                }
                records.append(item)
                file_records.append(item)
            files[relative_path] = file_records

        records.sort(key=lambda item: normalize(item["record"].get("title", "")))
        self._records[language] = records
        self._files[language] = files
        return records

    def files(self, language: str) -> dict[str, list[dict[str, Any]]]:
        self.load(language)
        return self._files[language]

    def search(self, language: str, query: str) -> list[dict[str, Any]]:
        phrase = normalize(query).strip()
        tokens = list(dict.fromkeys(token for token in phrase.split() if token))
        if not tokens:
            return []

        primary_complete: list[tuple[int, str, dict[str, Any]]] = []
        full_complete: list[tuple[int, str, dict[str, Any]]] = []
        partial_matches: list[tuple[int, str, dict[str, Any]]] = []

        for item in self.load(language):
            primary_text = item["primary_search_text"]
            full_text = item["search_text"]
            primary_count = sum(1 for token in tokens if token in primary_text)
            full_count = sum(1 for token in tokens if token in full_text)
            if full_count == 0:
                continue

            record = item["record"]
            title = normalize(record.get("title", ""))
            category = normalize(record.get("category", ""))
            summary = normalize(record.get("summary", ""))
            record_id = normalize(record.get("id", ""))
            path = normalize(item["relative_path"])

            score = full_count * 12 + primary_count * 25
            if phrase == record_id:
                score += 500
            if phrase == title:
                score += 400
            elif title.startswith(phrase):
                score += 250
            elif phrase in title:
                score += 180
            if phrase in category:
                score += 90
            if phrase in summary:
                score += 60
            if phrase in path:
                score += 45

            row = (score, title, item)
            if primary_count == len(tokens):
                primary_complete.append(row)
            elif full_count == len(tokens):
                full_complete.append(row)
            else:
                partial_matches.append(row)

        selected = primary_complete or full_complete or partial_matches
        selected.sort(key=lambda row: (-row[0], row[1]))
        return [row[2] for row in selected]

    def find_files(self, language: str, query: str) -> list[tuple[str, list[dict[str, Any]]]]:
        phrase = normalize(query).strip()
        tokens = list(dict.fromkeys(token for token in phrase.split() if token))
        ranked: list[tuple[int, str, str, list[dict[str, Any]]]] = []

        for relative_path, records in self.files(language).items():
            path_text = normalize(relative_path)
            combined = " ".join([path_text, *(item["search_text"] for item in records)])
            if not tokens:
                score = 0
            else:
                matched = sum(1 for token in tokens if token in combined)
                if matched == 0:
                    continue
                score = matched * 15
                if matched == len(tokens):
                    score += 60
                if phrase in path_text:
                    score += 100
                if normalize(Path(relative_path).stem).startswith(phrase):
                    score += 60
            ranked.append((score, path_text, relative_path, records))

        ranked.sort(key=lambda row: (-row[0], row[1]))
        return [(relative_path, records) for _, _, relative_path, records in ranked]

    def find_by_id(self, language: str, query: str) -> list[dict[str, Any]]:
        phrase = normalize(query).strip()
        if not phrase:
            return []
        exact: list[dict[str, Any]] = []
        starts: list[dict[str, Any]] = []
        partial: list[dict[str, Any]] = []
        for item in self.load(language):
            record_id = normalize(item["record"].get("id", ""))
            if record_id == phrase:
                exact.append(item)
            elif record_id.startswith(phrase):
                starts.append(item)
            elif phrase in record_id:
                partial.append(item)
        return exact + starts + partial

    def categories(self, language: str, uncategorized: str) -> dict[str, list[dict[str, Any]]]:
        grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for item in self.load(language):
            category = str(item["record"].get("category") or uncategorized)
            grouped[category].append(item)
        return dict(sorted(grouped.items(), key=lambda pair: normalize(pair[0])))

    def integrity_report(self) -> dict[str, Any]:
        report: dict[str, Any] = {
            "languages": {},
            "paths_match": False,
            "ids_match": False,
            "file_ids_match": False,
        }
        paths_by_language: dict[str, set[str]] = {}
        ids_by_language: dict[str, set[str]] = {}
        file_ids_by_language: dict[str, dict[str, set[str]]] = {}

        for language in LANGUAGES:
            base = self.language_root(language)
            root_present = base.is_dir()
            files = sorted(base.rglob("*.json")) if root_present else []
            invalid_files = 0
            missing_fields = 0
            empty_fields = 0
            ids: list[str] = []
            titles: list[str] = []
            category_folders: set[Path] = set()
            record_count = 0
            ids_by_file: dict[str, set[str]] = {}

            for path in files:
                category_folders.add(path.parent)
                relative_path = path.relative_to(base).as_posix()
                current_file_ids: set[str] = set()
                try:
                    payload = json.loads(path.read_text(encoding="utf-8"))
                except (OSError, UnicodeError, json.JSONDecodeError):
                    invalid_files += 1
                    continue
                if not isinstance(payload, list):
                    invalid_files += 1
                    continue
                file_has_invalid_record = False
                for record in payload:
                    if not isinstance(record, dict):
                        file_has_invalid_record = True
                        continue
                    record_count += 1
                    record_id = str(record.get("id", ""))
                    ids.append(record_id)
                    current_file_ids.add(record_id)
                    titles.append(str(record.get("title", "")))
                    for field in REQUIRED_FIELDS:
                        if field not in record:
                            missing_fields += 1
                        elif record[field] in (None, "", []):
                            empty_fields += 1
                if file_has_invalid_record:
                    invalid_files += 1
                ids_by_file[relative_path] = current_file_ids

            relative_paths = {path.relative_to(base).as_posix() for path in files}
            id_set = set(ids)
            paths_by_language[language] = relative_paths
            ids_by_language[language] = id_set
            file_ids_by_language[language] = ids_by_file
            report["languages"][language] = {
                "root_present": root_present,
                "files": len(files),
                "records": record_count,
                "category_folders": len(category_folders),
                "invalid_files": invalid_files,
                "missing_fields": missing_fields,
                "empty_fields": empty_fields,
                "duplicate_ids": sum(count - 1 for count in Counter(ids).values() if count > 1),
                "duplicate_titles": sum(count - 1 for count in Counter(titles).values() if count > 1),
            }

        report["paths_match"] = paths_by_language.get("en", set()) == paths_by_language.get("el", set())
        report["ids_match"] = ids_by_language.get("en", set()) == ids_by_language.get("el", set())
        report["file_ids_match"] = (
            file_ids_by_language.get("en", {}) == file_ids_by_language.get("el", {})
        )
        report["ok"] = bool(
            report["paths_match"]
            and report["ids_match"]
            and report["file_ids_match"]
            and all(
                values["root_present"]
                and values["files"] > 0
                and values["invalid_files"] == 0
                and values["missing_fields"] == 0
                and values["empty_fields"] == 0
                and values["duplicate_ids"] == 0
                and values["duplicate_titles"] == 0
                for values in report["languages"].values()
            )
        )
        return report


class Application:
    """Interactive bilingual terminal interface."""

    def __init__(self) -> None:
        self.settings, settings_existed = load_settings()
        self.database = OfflineDatabase()
        self.exit_requested = False
        if not settings_existed:
            self.exit_requested = not self.first_run_language()

    @property
    def language(self) -> str:
        return str(self.settings["language"])

    def t(self, key: str) -> str:
        return TEXT[self.language][key]

    def clear(self) -> None:
        if self.settings.get("clear_screen", True) and sys.stdout.isatty():
            print("\033[2J\033[H", end="")

    def header(self, subtitle: Optional[str] = None) -> None:
        self.clear()
        width = terminal_width()
        print(divider("═"))
        for line in wrap_lines(APP_NAME):
            print(line.center(width))
        language_line = f"{self.t('header_language')}: {LANGUAGES[self.language]['name']}"
        for line in wrap_lines(language_line):
            print(line.center(width))
        if subtitle:
            for line in wrap_lines(subtitle):
                print(line.center(width))
        print(divider("═"))

    def ask(self, prompt: str) -> str:
        prompt_width = max(12, terminal_width() - 2)
        prompt_lines = textwrap.wrap(
            prompt,
            width=prompt_width,
            replace_whitespace=False,
            break_long_words=True,
            break_on_hyphens=False,
        ) or [prompt]
        for line in prompt_lines[:-1]:
            print(line)
        try:
            return input(f"{prompt_lines[-1]}: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return "q"

    def pause(self) -> None:
        print()
        try:
            self.ask(f"{self.t('press_enter')}...")
        except (EOFError, KeyboardInterrupt):
            print()

    def save_preferences(self) -> bool:
        if save_settings(self.settings):
            print(self.t("settings_saved"))
            return True
        print(self.t("settings_save_error"))
        return False

    def first_run_language(self) -> bool:
        while True:
            self.clear()
            print(divider("═"))
            print(APP_NAME.center(terminal_width()))
            print("First launch / Πρώτη εκκίνηση".center(terminal_width()))
            print(divider("═"))
            print("1. English")
            print("2. Ελληνικά")
            print("0. Exit / Έξοδος")
            answer = normalize(self.ask("Choose language / Επίλεξε γλώσσα"))
            if answer == "1":
                self.settings["language"] = "en"
            elif answer == "2":
                self.settings["language"] = "el"
            elif answer in BACK_COMMANDS:
                return False
            else:
                print("Invalid option / Μη έγκυρη επιλογή")
                try:
                    input("Press Enter / Πάτησε Enter...")
                except (EOFError, KeyboardInterrupt):
                    return False
                continue
            if not save_settings(self.settings):
                print("Settings could not be saved / Δεν αποθηκεύτηκαν οι ρυθμίσεις")
                self.pause()
            return True

    def ensure_loaded(self) -> bool:
        try:
            if self.language not in self.database._records:
                self.header(self.t("loading"))
            self.database.load(self.language)
            return True
        except FileNotFoundError as error:
            self.header(self.t("load_error"))
            print(f"{self.t('missing_folder')}: {error}")
        except RuntimeError as error:
            self.header(self.t("load_error"))
            print(error)
        self.pause()
        return False

    def print_list_entry(self, number: int, label: str) -> None:
        prefix = f"{number}. "
        continuation = " " * len(prefix)
        for line in wrap_lines(label, prefix, continuation):
            print(line)

    def browse_list(
        self,
        items: Sequence[Any],
        label: Callable[[Any], str],
        subtitle: str,
        on_select: Callable[[Any], None],
    ) -> None:
        if not items:
            self.header(subtitle)
            print(self.t("no_results"))
            self.pause()
            return

        page_size = int(self.settings["page_size"])
        page = 0
        pages = max(1, (len(items) + page_size - 1) // page_size)

        while True:
            page = max(0, min(page, pages - 1))
            start = page * page_size
            visible = items[start : start + page_size]
            self.header(subtitle)
            for local_number, item in enumerate(visible, start=1):
                self.print_list_entry(local_number, label(item))
            print(divider())
            footer = f"{self.t('page')} {page + 1} {self.t('of')} {pages} | {len(items)} {self.t('results')}"
            for line in wrap_lines(footer):
                print(line)
            for line in wrap_lines(self.t("select_item")):
                print(line)
            command = normalize(self.ask(self.t("choice")))

            if command in BACK_COMMANDS:
                return
            if command in NEXT_COMMANDS:
                if page + 1 < pages:
                    page += 1
                continue
            if command in PREVIOUS_COMMANDS:
                if page > 0:
                    page -= 1
                continue
            if command.isdigit():
                selected = int(command) - 1
                if 0 <= selected < len(visible):
                    on_select(visible[selected])
                    continue
            print(self.t("invalid"))
            self.pause()

    def record_label(self, item: dict[str, Any]) -> str:
        record = item["record"]
        title = str(record.get("title") or self.t("untitled"))
        category = str(record.get("category") or self.t("uncategorized"))
        return f"{title} [{category}]"

    def render_value_lines(self, value: Any) -> list[str]:
        if isinstance(value, list):
            output: list[str] = []
            for index, item in enumerate(value, start=1):
                if isinstance(item, (dict, list)):
                    rendered = json.dumps(item, ensure_ascii=False, indent=2)
                else:
                    rendered = str(item)
                output.extend(wrap_lines(rendered, f"{index}. ", "   "))
            return output
        if isinstance(value, dict):
            return wrap_lines(json.dumps(value, ensure_ascii=False, indent=2))
        return wrap_lines(value)

    def paged_reader(self, title: str, lines: Sequence[str]) -> None:
        content = list(lines) or [""]
        page = 0
        while True:
            _, height = terminal_size()
            page_height = max(8, height - 9)
            page_content = paginate_lines(content, page_height)
            pages = len(page_content)
            page = max(0, min(page, pages - 1))

            self.header(title)
            for line in page_content[page]:
                print(line)
            print(divider())
            print(f"{self.t('page')} {page + 1} {self.t('of')} {pages}")

            if pages == 1:
                for line in wrap_lines(self.t("reader_return")):
                    print(line)
                command = normalize(self.ask(self.t("choice")))
                if command in BACK_COMMANDS or command == "":
                    return
                print(self.t("invalid"))
                self.pause()
                continue

            for line in wrap_lines(self.t("reader_controls")):
                print(line)
            command = normalize(self.ask(self.t("choice")))
            if command in BACK_COMMANDS:
                return
            if command in PREVIOUS_COMMANDS:
                if page > 0:
                    page -= 1
                continue
            if command in NEXT_COMMANDS:
                if page + 1 < pages:
                    page += 1
                else:
                    return
                continue
            print(self.t("invalid"))
            self.pause()

    def record_lines(self, item: dict[str, Any]) -> list[str]:
        record = item["record"]
        labels = FIELD_LABELS[self.language]
        lines: list[str] = []
        lines.extend(wrap_lines(f"{self.t('source_file')}: {item['relative_path']}"))
        displayed: set[str] = {"title"}

        for field in DISPLAY_ORDER:
            if field not in record or record[field] in (None, "", []):
                continue
            displayed.add(field)
            lines.append("")
            lines.extend(wrap_lines(labels.get(field, field.replace("_", " ").title())))
            lines.append("·" * terminal_width())
            lines.extend(self.render_value_lines(record[field]))

        for field, value in record.items():
            if field in displayed or value in (None, "", []):
                continue
            lines.append("")
            lines.extend(wrap_lines(labels.get(field, field.replace("_", " ").title())))
            lines.append("·" * terminal_width())
            lines.extend(self.render_value_lines(value))
        return lines

    def read_record(self, item: dict[str, Any]) -> None:
        title = str(item["record"].get("title") or self.t("untitled"))
        self.paged_reader(title, self.record_lines(item))

    def search_menu(self) -> None:
        if not self.ensure_loaded():
            return
        self.header(self.t("search"))
        query = self.ask(self.t("search_prompt"))
        if normalize(query) in BACK_COMMANDS:
            return
        if not query.strip():
            print(self.t("empty_query"))
            self.pause()
            return
        results = self.database.search(self.language, query)
        self.browse_list(results, self.record_label, self.t("search_results"), self.read_record)

    def browse_categories(self) -> None:
        if not self.ensure_loaded():
            return
        categories = self.database.categories(self.language, self.t("uncategorized"))
        self.header(self.t("browse"))
        query = self.ask(self.t("category_filter"))
        if normalize(query) in BACK_COMMANDS:
            return
        tokens = normalize(query).split()
        names = [
            name
            for name in categories
            if not tokens or all(token in normalize(name) for token in tokens)
        ]

        def open_category(name: str) -> None:
            subtitle = f"{self.t('records_in_category')}: {name}"
            self.browse_list(categories[name], self.record_label, subtitle, self.read_record)

        self.browse_list(
            names,
            lambda name: f"{name} ({len(categories[name])} {self.t('records')})",
            self.t("categories"),
            open_category,
        )

    def file_actions(self, selected: tuple[str, list[dict[str, Any]]]) -> None:
        relative_path, records = selected
        while True:
            self.header(self.t("file_actions"))
            for line in wrap_lines(f"{self.t('file_path')}: {relative_path}"):
                print(line)
            print()
            self.print_list_entry(1, self.t("browse_file_records"))
            self.print_list_entry(2, self.t("view_raw_json"))
            self.print_list_entry(0, self.t("back"))
            command = normalize(self.ask(self.t("choice")))
            if command == "1":
                self.browse_list(records, self.record_label, relative_path, self.read_record)
            elif command == "2":
                path = self.database.language_root(self.language) / Path(relative_path)
                self.view_raw_file(path, relative_path)
            elif command in BACK_COMMANDS:
                return
            else:
                print(self.t("invalid"))
                self.pause()

    def file_menu(self) -> None:
        if not self.ensure_loaded():
            return
        self.header(self.t("find_file"))
        query = self.ask(self.t("file_prompt"))
        if normalize(query) in BACK_COMMANDS:
            return
        matches = self.database.find_files(self.language, query)
        self.browse_list(
            matches,
            lambda pair: f"{pair[0]} ({len(pair[1])} {self.t('records')})",
            self.t("files"),
            self.file_actions,
        )

    def view_raw_file(self, path: Path, relative_path: str) -> None:
        try:
            raw = path.read_text(encoding="utf-8")
            lines: list[str] = []
            lines.extend(wrap_lines(f"{self.t('file_path')}: {relative_path}"))
            lines.append("")
            for raw_line in raw.splitlines():
                lines.extend(wrap_lines(raw_line))
            self.paged_reader(self.t("raw_json"), lines)
        except (OSError, UnicodeError) as error:
            self.header(self.t("raw_json"))
            print(f"{self.t('raw_read_error')} {error}")
            self.pause()

    def open_by_id(self) -> None:
        if not self.ensure_loaded():
            return
        self.header(self.t("open_id"))
        query = self.ask(self.t("id_prompt"))
        if normalize(query) in BACK_COMMANDS:
            return
        if not query.strip():
            print(self.t("empty_query"))
            self.pause()
            return
        matches = self.database.find_by_id(self.language, query)
        self.browse_list(matches, self.record_label, self.t("records"), self.read_record)

    def random_record(self) -> None:
        if not self.ensure_loaded():
            return
        records = self.database.load(self.language)
        if not records:
            self.header(self.t("random"))
            print(self.t("no_results"))
            self.pause()
            return
        while True:
            self.read_record(random.choice(records))
            self.header(self.t("random"))
            answer = normalize(self.ask(self.t("another_random")))
            if answer in YES_COMMANDS:
                continue
            if answer in NO_COMMANDS or answer in BACK_COMMANDS or answer == "":
                return
            print(self.t("invalid"))
            self.pause()

    def change_language(self) -> None:
        while True:
            self.header(self.t("choose_language"))
            print("1. English")
            print("2. Ελληνικά")
            print(f"0. {self.t('back')}")
            command = normalize(self.ask(self.t("choice")))
            if command == "1":
                self.settings["language"] = "en"
            elif command == "2":
                self.settings["language"] = "el"
            elif command in BACK_COMMANDS:
                return
            else:
                print(self.t("invalid"))
                self.pause()
                continue
            self.header(self.t("settings"))
            self.save_preferences()
            self.pause()
            return

    def change_page_size(self) -> None:
        sizes = [5, 10, 15, 20]
        while True:
            self.header(self.t("choose_page_size"))
            for index, size in enumerate(sizes, start=1):
                print(f"{index}. {size}")
            print(f"0. {self.t('back')}")
            command = normalize(self.ask(self.t("choice")))
            if command in BACK_COMMANDS:
                return
            if command.isdigit() and 1 <= int(command) <= len(sizes):
                self.settings["page_size"] = sizes[int(command) - 1]
                self.header(self.t("settings"))
                self.save_preferences()
                self.pause()
                return
            print(self.t("invalid"))
            self.pause()

    def toggle_clear_screen(self) -> None:
        self.settings["clear_screen"] = not bool(self.settings.get("clear_screen", True))
        self.header(self.t("settings"))
        self.save_preferences()
        self.pause()

    def reset_settings(self) -> None:
        self.header(self.t("reset_settings"))
        answer = normalize(self.ask(self.t("confirm_reset")))
        if answer not in YES_COMMANDS:
            return
        self.settings = dict(DEFAULT_SETTINGS)
        self.header(TEXT["en"]["settings"])
        if save_settings(self.settings):
            print("Settings reset to defaults. / Οι ρυθμίσεις επανήλθαν στις προεπιλογές.")
        else:
            print("Settings could not be saved. / Δεν αποθηκεύτηκαν οι ρυθμίσεις.")
        self.pause()

    def settings_menu(self) -> None:
        while True:
            self.header(self.t("settings"))
            clear_state = self.t("enabled") if self.settings.get("clear_screen") else self.t("disabled")
            self.print_list_entry(1, f"{self.t('change_language')}: {LANGUAGES[self.language]['name']}")
            self.print_list_entry(2, f"{self.t('page_size')}: {self.settings['page_size']}")
            self.print_list_entry(3, f"{self.t('clear_screen')}: {clear_state}")
            self.print_list_entry(4, self.t("reset_settings"))
            self.print_list_entry(0, self.t("back"))
            command = normalize(self.ask(self.t("choice")))
            if command == "1":
                self.change_language()
            elif command == "2":
                self.change_page_size()
            elif command == "3":
                self.toggle_clear_screen()
            elif command == "4":
                self.reset_settings()
            elif command in BACK_COMMANDS:
                return
            else:
                print(self.t("invalid"))
                self.pause()

    def help_menu(self) -> None:
        lines: list[str] = []
        lines.extend(wrap_lines(self.t("about_text")))
        lines.append("")
        lines.extend(wrap_lines(self.t("safety_title")))
        lines.append("·" * terminal_width())
        lines.extend(wrap_lines(self.t("safety_text")))
        lines.append("")
        lines.extend(wrap_lines(f"{self.t('settings_file')}: {SETTINGS_FILE}"))
        self.paged_reader(self.t("about_title"), lines)

    def integrity_check(self) -> None:
        self.header(self.t("integrity"))
        print(self.t("integrity_running"))
        report = self.database.integrity_report()
        lines: list[str] = []
        lines.extend(wrap_lines(self.t("integrity_ok") if report["ok"] else self.t("integrity_failed")))

        for language, values in report["languages"].items():
            lines.append("")
            lines.extend(wrap_lines(f"{self.t('language_report')}: {LANGUAGES[language]['name']}"))
            lines.append("·" * terminal_width())
            root_state = self.t("yes") if values["root_present"] else self.t("no")
            lines.extend(wrap_lines(f"{self.t('database_folder')}: {root_state}"))
            lines.extend(wrap_lines(f"{values['files']} {self.t('json_files')}"))
            lines.extend(wrap_lines(f"{values['records']} {self.t('records')}"))
            lines.extend(wrap_lines(f"{values['category_folders']} {self.t('category_folders')}"))
            lines.extend(wrap_lines(f"{values['invalid_files']} {self.t('invalid_files')}"))
            lines.extend(wrap_lines(f"{values['missing_fields']} {self.t('missing_fields')}"))
            lines.extend(wrap_lines(f"{values['empty_fields']} {self.t('empty_fields')}"))
            lines.extend(wrap_lines(f"{values['duplicate_ids']} {self.t('duplicate_ids')}"))
            lines.extend(wrap_lines(f"{values['duplicate_titles']} {self.t('duplicate_titles')}"))

        lines.append("")
        path_state = self.t("matching") if report["paths_match"] else self.t("not_matching")
        id_state = self.t("matching") if report["ids_match"] else self.t("not_matching")
        file_id_state = self.t("matching") if report["file_ids_match"] else self.t("not_matching")
        lines.extend(wrap_lines(f"{self.t('mirrored_paths')}: {path_state}"))
        lines.extend(wrap_lines(f"{self.t('mirrored_ids')}: {id_state}"))
        lines.extend(wrap_lines(f"{self.t('mirrored_file_ids')}: {file_id_state}"))
        self.paged_reader(self.t("integrity_title"), lines)

    def run(self) -> None:
        if self.exit_requested:
            return
        while True:
            self.header(self.t("main_menu"))
            self.print_list_entry(1, self.t("search"))
            self.print_list_entry(2, self.t("browse"))
            self.print_list_entry(3, self.t("find_file"))
            self.print_list_entry(4, self.t("open_id"))
            self.print_list_entry(5, self.t("random"))
            self.print_list_entry(6, self.t("settings"))
            self.print_list_entry(7, self.t("help"))
            self.print_list_entry(8, self.t("integrity"))
            self.print_list_entry(0, self.t("exit"))
            command = normalize(self.ask(self.t("choice")))

            if command == "1":
                self.search_menu()
            elif command == "2":
                self.browse_categories()
            elif command == "3":
                self.file_menu()
            elif command == "4":
                self.open_by_id()
            elif command == "5":
                self.random_record()
            elif command == "6":
                self.settings_menu()
            elif command == "7":
                self.help_menu()
            elif command == "8":
                self.integrity_check()
            elif command in BACK_COMMANDS:
                self.header(self.t("exit"))
                print(self.t("goodbye"))
                return
            else:
                print(self.t("invalid"))
                self.pause()


def main() -> int:
    try:
        Application().run()
        return 0
    except KeyboardInterrupt:
        print("\nExit / Έξοδος")
        return 130
    except Exception as error:  # Last-resort terminal guard with a useful message.
        settings, _ = load_settings()
        language = str(settings.get("language", "en"))
        if language not in LANGUAGES:
            language = "en"
        print(f"\n{TEXT[language]['unexpected_error']}: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
