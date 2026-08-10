#!/usr/bin/env python3
# MAINTENANCE: Keep the CLI standard-library only, preserve bilingual parity, and keep database reads tolerant of optional narrative fields.
"""Offline Survival Project terminal browser.

A dependency-free, bilingual terminal application for searching, finding,
browsing, validating, and reading the English and Greek JSON databases that
ship with this repository.
"""

from __future__ import annotations

import json
import random
import re
import shutil
import sys
import textwrap
import unicodedata
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path
from typing import Any, Callable, Optional, Sequence
from urllib.parse import urlparse

APP_NAME = "Offline Survival Project"
PROJECT_ROOT = Path(__file__).resolve().parent
SETTINGS_DIR = Path.home() / ".offline_survival_project"
SETTINGS_FILE = SETTINGS_DIR / "settings.json"

LANGUAGES = {
    "en": {"folder": "English", "name": "English", "record_language": "English"},
    "el": {"folder": "Ελληνικά", "name": "Ελληνικά", "record_language": "Ελληνικά"},
}
LEGACY_GREEK_FOLDER = "#U0395#U03bb#U03bb#U03b7#U03bd#U03b9#U03ba#U03ac"

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
        "verified_essentials": "Verified emergency essentials",
        "food_growing": "Food growing and safe preservation",
        "verified_food_guides": "verified food-growing and preservation guides",
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
        "field_type_errors": "field type errors",
        "invalid_source_urls": "invalid source URLs",
        "unapproved_source_domains": "unapproved source domains",
        "records_without_sources": "records without sources",
        "invalid_dates": "invalid or future update dates",
        "language_mismatches": "record language mismatches",
        "source_domains": "approved source domains used",
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
        "verified_essentials": "Επαληθευμένα βασικά έκτακτης ανάγκης",
        "food_growing": "Καλλιέργεια και ασφαλής διατήρηση τροφίμων",
        "verified_food_guides": "επαληθευμένοι οδηγοί καλλιέργειας και διατήρησης τροφίμων",
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
        "field_type_errors": "σφάλματα τύπου πεδίων",
        "invalid_source_urls": "μη έγκυρα URLs πηγών",
        "unapproved_source_domains": "μη εγκεκριμένοι τομείς πηγών",
        "records_without_sources": "εγγραφές χωρίς πηγές",
        "invalid_dates": "μη έγκυρες ή μελλοντικές ημερομηνίες",
        "language_mismatches": "ασυμφωνίες γλώσσας εγγραφών",
        "source_domains": "εγκεκριμένοι τομείς πηγών",
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
    "sources",
    "last_updated",
]

REQUIRED_FIELDS = ("title", "id", "language", "category", "sources", "last_updated")
# Optional display sections are validated when present, but are no longer mandatory.
# This prevents generic filler from being inserted merely to satisfy the schema.
FLEXIBLE_TEXT_FIELDS = {"short_term", "long_term", "if_method_fails", "environment_notes"}
LIST_FIELDS = {
    "tags",
    "materials",
    "steps",
    "warnings",
    "common_mistakes",
    "alternatives",
    "failure_signs",
    "when_not_to_use",
    "related_topics",
    "sources",
}
OFFICIAL_SOURCE_DOMAINS = {
    "civilprotection.gov.gr",
    "www.avma.org",
    "www.cdc.gov",
    "www.cisa.gov",
    "www.cpsc.gov",
    "www.epa.gov",
    "www.faa.gov",
    "www.fao.org",
    "www.fcc.gov",
    "www.ars.usda.gov",
    "www.minagric.gr",
    "www.nal.usda.gov",
    "www.nrcs.usda.gov",
    "www.usda.gov",
    "nchfp.uga.edu",
    "www.moh.gov.gr",
    "www.nhs.uk",
    "www.osha.gov",
    "www.ready.gov",
    "www.redcross.org",
    "www.sarsat.noaa.gov",
    "www.usgs.gov",
    "www.who.int",
    "cdn.who.int",
}
DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")


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
        preferred = PROJECT_ROOT / LANGUAGES[language]["folder"]
        if language == "el" and not preferred.is_dir():
            legacy = PROJECT_ROOT / LEGACY_GREEK_FOLDER
            if legacy.is_dir():
                return legacy
        return preferred

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
        """Validate structure, bilingual parity, dates, field types, and source provenance."""
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
            field_type_errors = 0
            invalid_source_urls = 0
            unapproved_source_domains = 0
            records_without_sources = 0
            invalid_dates = 0
            language_mismatches = 0
            verified_food_guides = 0
            source_domains: set[str] = set()
            ids: list[str] = []
            titles: list[str] = []
            category_folders: set[Path] = set()
            record_count = 0
            ids_by_file: dict[str, set[str]] = {}
            expected_record_language = LANGUAGES[language]["record_language"]

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
                    if record_id.startswith("verified-food-"):
                        verified_food_guides += 1
                    ids.append(record_id)
                    current_file_ids.add(record_id)
                    titles.append(str(record.get("title", "")))

                    for field in REQUIRED_FIELDS:
                        if field not in record:
                            missing_fields += 1
                            continue
                        value = record[field]
                        if value in (None, "", []):
                            empty_fields += 1
                        if field in FLEXIBLE_TEXT_FIELDS:
                            valid_type = isinstance(value, (str, list))
                        elif field in LIST_FIELDS:
                            valid_type = isinstance(value, list)
                        else:
                            valid_type = isinstance(value, str)
                        if not valid_type:
                            field_type_errors += 1

                    if record.get("language") != expected_record_language:
                        language_mismatches += 1

                    updated = record.get("last_updated")
                    try:
                        if not isinstance(updated, str) or not DATE_PATTERN.fullmatch(updated):
                            raise ValueError
                        parsed_date = date.fromisoformat(updated)
                        if parsed_date > date.today():
                            raise ValueError
                    except ValueError:
                        invalid_dates += 1

                    sources = record.get("sources")
                    if not isinstance(sources, list) or not sources:
                        records_without_sources += 1
                    elif isinstance(sources, list):
                        for source in sources:
                            if not isinstance(source, str):
                                invalid_source_urls += 1
                                continue
                            parsed = urlparse(source)
                            domain = parsed.netloc.casefold()
                            if parsed.scheme != "https" or not domain or not parsed.path:
                                invalid_source_urls += 1
                                continue
                            source_domains.add(domain)
                            if domain not in OFFICIAL_SOURCE_DOMAINS:
                                unapproved_source_domains += 1

                if file_has_invalid_record:
                    invalid_files += 1
                ids_by_file[relative_path] = current_file_ids

            relative_paths = {path.relative_to(base).as_posix() for path in files}
            paths_by_language[language] = relative_paths
            ids_by_language[language] = set(ids)
            file_ids_by_language[language] = ids_by_file
            report["languages"][language] = {
                "root_present": root_present,
                "files": len(files),
                "records": record_count,
                "category_folders": len(category_folders),
                "invalid_files": invalid_files,
                "missing_fields": missing_fields,
                "empty_fields": empty_fields,
                "field_type_errors": field_type_errors,
                "invalid_source_urls": invalid_source_urls,
                "unapproved_source_domains": unapproved_source_domains,
                "records_without_sources": records_without_sources,
                "invalid_dates": invalid_dates,
                "language_mismatches": language_mismatches,
                "verified_food_guides": verified_food_guides,
                "source_domains": sorted(source_domains),
                "duplicate_ids": sum(count - 1 for count in Counter(ids).values() if count > 1),
                "duplicate_titles": sum(count - 1 for count in Counter(titles).values() if count > 1),
            }

        report["paths_match"] = paths_by_language.get("en", set()) == paths_by_language.get("el", set())
        report["ids_match"] = ids_by_language.get("en", set()) == ids_by_language.get("el", set())
        report["file_ids_match"] = file_ids_by_language.get("en", {}) == file_ids_by_language.get("el", {})
        report["ok"] = bool(
            report["paths_match"]
            and report["ids_match"]
            and report["file_ids_match"]
            and all(
                values["root_present"]
                and values["files"] > 0
                and all(
                    values[key] == 0
                    for key in (
                        "invalid_files",
                        "missing_fields",
                        "empty_fields",
                        "field_type_errors",
                        "invalid_source_urls",
                        "unapproved_source_domains",
                        "records_without_sources",
                        "invalid_dates",
                        "language_mismatches",
                        "duplicate_ids",
                        "duplicate_titles",
                    )
                )
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

    def verified_essentials(self) -> None:
        if not self.ensure_loaded():
            return
        records = [
            item
            for item in self.database.load(self.language)
            if str(item["record"].get("id", "")).startswith("verified-essential-")
        ]
        self.browse_list(
            records,
            self.record_label,
            self.t("verified_essentials"),
            self.read_record,
        )

    def food_growing(self) -> None:
        if not self.ensure_loaded():
            return
        records = [
            item
            for item in self.database.load(self.language)
            if str(item["record"].get("id", "")).startswith("verified-food-")
        ]
        self.browse_list(
            records,
            self.record_label,
            self.t("food_growing"),
            self.read_record,
        )

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
            lines.extend(wrap_lines(f"{values['field_type_errors']} {self.t('field_type_errors')}"))
            lines.extend(wrap_lines(f"{values['invalid_source_urls']} {self.t('invalid_source_urls')}"))
            lines.extend(wrap_lines(f"{values['unapproved_source_domains']} {self.t('unapproved_source_domains')}"))
            lines.extend(wrap_lines(f"{values['records_without_sources']} {self.t('records_without_sources')}"))
            lines.extend(wrap_lines(f"{values['invalid_dates']} {self.t('invalid_dates')}"))
            lines.extend(wrap_lines(f"{values['language_mismatches']} {self.t('language_mismatches')}"))
            lines.extend(wrap_lines(f"{values['verified_food_guides']} {self.t('verified_food_guides')}"))
            lines.extend(wrap_lines(f"{len(values['source_domains'])} {self.t('source_domains')}"))
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
            self.print_list_entry(6, self.t("verified_essentials"))
            self.print_list_entry(7, self.t("food_growing"))
            self.print_list_entry(8, self.t("settings"))
            self.print_list_entry(9, self.t("help"))
            self.print_list_entry(10, self.t("integrity"))
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
                self.verified_essentials()
            elif command == "7":
                self.food_growing()
            elif command == "8":
                self.settings_menu()
            elif command == "9":
                self.help_menu()
            elif command == "10":
                self.integrity_check()
            elif command in BACK_COMMANDS:
                self.header(self.t("exit"))
                print(self.t("goodbye"))
                return
            else:
                print(self.t("invalid"))
                self.pause()


def print_cli_help() -> None:
    print(f"{APP_NAME}\n")
    print('Run the interactive application:')
    print('  python "Offline Survival.py"')
    print('\nValidate both databases and return exit code 0/2:')
    print('  python "Offline Survival.py" --check')
    print('\nShow database counts:')
    print('  python "Offline Survival.py" --stats')
    print('\nLaunch the local browser Command Center:')
    print('  python "Offline Survival.py" --web')
    print('\nRun the repeatable engineering self-test:')
    print('  python "Offline Survival.py" --self-test')
    print('\nRun the isolated localhost API/security smoke test:')
    print('  python "Offline Survival.py" --api-test')
    print('\nRun the line-by-line deep source/content audit:')
    print('  python "Offline Survival.py" --audit')
    print('\nRun the narrative/template quality gate:')
    print('  python "Offline Survival.py" --quality')
    print('\nAudit Offline Library duplicates, repeated paragraphs and template similarity:')
    print('  python "Offline Survival.py" --library-quality')
    print('\nAudit bilingual database, Library and user-visible translation coverage:')
    print('  python "Offline Survival.py" --translations')
    print('\nRun deterministic browser UI/state logic tests with Node.js:')
    print('  python "Offline Survival.py" --ui-test')
    print('\nOpen on-device diagnostics in the installed/default phone browser:')
    print('  python "Offline Survival.py" --phone-browser-test')
    print('\nOpen the standalone 220-chapter bilingual survival reader:')
    print('  python "Offline Survival.py" --reader')


def main() -> int:
    try:
        if len(sys.argv) > 1:
            command = sys.argv[1].casefold()
            if command in {"-h", "--help"}:
                print_cli_help()
                return 0
            if command in {"--check", "--validate"}:
                report = OfflineDatabase().integrity_report()
                print(json.dumps(report, ensure_ascii=False, indent=2))
                return 0 if report["ok"] else 2
            if command == "--stats":
                database = OfflineDatabase()
                report = database.integrity_report()
                for language, values in report["languages"].items():
                    print(
                        f"{LANGUAGES[language]['name']}: "
                        f"{values['records']} records, {values['files']} JSON files, "
                        f"{values['category_folders']} category folders"
                    )
                return 0 if report["ok"] else 2
            if command in {"--web", "--command-center"}:
                return run_local_command_center(sys.argv[2:])
            if command in {"--self-test", "--test"}:
                return integrated_self_test()
            if command in {"--api-test", "--api-smoke"}:
                return run_embedded_tool("api_smoke_test")
            if command in {"--audit", "--deep-audit"}:
                return integrated_deep_audit()
            if command in {"--quality", "--content-quality"}:
                return run_embedded_tool("content_quality")
            if command in {"--translations", "--translation-audit"}:
                return run_embedded_tool("translation_audit")
            if command in {"--library-quality", "--library-audit"}:
                return run_embedded_tool("library_quality")
            if command in {"--ui-test", "--ui-logic-test"}:
                import subprocess
                test_app = PROJECT_ROOT / "tools" / "ui_logic_test.js"
                if not test_app.is_file():
                    print(f"Missing UI logic test: {test_app}", file=sys.stderr)
                    return 2
                node = shutil.which("node")
                if not node:
                    print("Node.js is required for --ui-test", file=sys.stderr)
                    return 2
                return subprocess.call([node, str(test_app)])
            if command in {"--reader", "--standalone-reader"}:
                return run_local_command_center(["--reader", *sys.argv[2:]])
            if command in {"--phone-browser-test", "--browser-test", "--local-browser-test"}:
                return run_local_command_center(["--phone-test", *sys.argv[2:]])
            print(f"Unknown option: {sys.argv[1]}", file=sys.stderr)
            print_cli_help()
            return 2

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

# ---------------------------------------------------------------------------
# Integrated local web server and maintenance/audit helpers.
# MAINTENANCE: These helpers intentionally live in this file so the project
# ships exactly one Python script. Keep feature-specific browser code in /web
# and keep user knowledge in the bilingual JSON/Markdown data stores.
# ---------------------------------------------------------------------------

import os as _osp_os
import socket as _osp_socket
import subprocess as _osp_subprocess
import tempfile as _osp_tempfile
import time as _osp_time
from urllib import request as _osp_request, error as _osp_urlerror

_EMBEDDED_TOOL_SOURCES = {'content_quality': '# MAINTENANCE: Tighten quality rules when needed; do not weaken gates just to preserve record counts.\n"""Strict bilingual narrative-quality gate and curation tool.\n\nThis tool rejects mass-generated prose rather than merely detecting byte-identical files.\nIt treats English/Greek records as one translation pair during cleanup: if a narrative\nfield/item is rejected in either language, the corresponding item is removed from both.\nThat prevents quality cleanup from creating translation drift.\n\nExpected repetition such as source URLs, taxonomy values, record IDs and short material\nnames is intentionally outside the narrative gate. The gate focuses on user-facing prose.\n"""\n\nimport argparse\nimport collections\nimport json\nimport math\nimport re\nfrom dataclasses import dataclass\nfrom pathlib import Path\nfrom typing import Any, Iterable\n\nROOT = Path(__file__).resolve().parents[1]\nLANG_DIRS = ("English", "Ελληνικά")\nNARRATIVE_FIELDS = (\n    "summary", "content", "materials", "steps", "warnings", "common_mistakes",\n    "alternatives", "failure_signs", "when_not_to_use", "short_term", "long_term",\n    "if_method_fails", "environment_notes",\n)\nSCALAR_FIELDS = {"summary", "content", "short_term", "long_term", "if_method_fails", "environment_notes"}\nLIST_FIELDS = set(NARRATIVE_FIELDS) - SCALAR_FIELDS\nINTERNAL_TAG_RE = re.compile(r"(?:^|[-_ ])pass\\d+(?:[-_ ][\\w-]+)*$|^pass\\d+", re.I)\nQUOTED_RE = re.compile(r"[“\\"«][^”\\"»]{2,260}[”\\"»]")\nNUMBER_RE = re.compile(r"\\b\\d+(?:[.,]\\d+)?\\b")\nURL_RE = re.compile(r"https?://\\S+", re.I)\nWORD_RE = re.compile(r"[\\wΆ-ώ]+", re.UNICODE)\n\n# User-facing generated-writing signatures discovered in earlier project passes.\n# They remain as an explicit regression list in addition to the generic shingle detector.\nKNOWN_MARKERS = {\n    "English": (\n        "apply this boundary to ", "practical guidance for ", "this is the opening check for ",\n        "record-specific context:", "apply it specifically within ",\n        "treat this as a specific boundary while managing ", "this note applies specifically to ",\n        "while carrying out ", "complete one verified cycle for ",\n        "recheck this point before closing ", "treat any uncertainty here as an unresolved item ",\n        "include the outcome of ", "use a dated paper note and spoken read-back for ",\n        "a second person should be able to verify this part of ",\n        "is designed for conditions where normal services, internet, transport, or outside help may be delayed",\n        "keep the routine visible, assign one calm recorder, protect vulnerable people first",\n        "a complete offline workflow for ",\n        "trying to solve {title} alone instead of using a small visible team",\n        "for the first hours, use {title} to stabilize decisions",\n        "for longer disruption, turn {title} into a daily checklist",\n        "if {title} fails, stop the routine, isolate the hazard if safe",\n        "adapt {title} to apartment blocks, villages, islands",\n        "do not let {title} delay evacuation, medical care",\n        "assign one calm person to lead {title}",\n        "for a reduced version of ",\n        "close the routine by marking what is safe, what is unsafe",\n    ),\n    "Ελληνικά": (\n        "εφάρμοσε αυτό το όριο στο θέμα ", "συγκεκριμένο πλαίσιο εγγραφής:",\n        "εφάρμοσέ το ειδικά στη διαδικασία ", "το συγκεκριμένο όριο ισχύει κατά τη διαχείριση ",\n        "η σημείωση αυτή αφορά ειδικά το θέμα ",\n        "ένα δεύτερο άτομο πρέπει να μπορεί να επαληθεύσει αυτό το μέρος του θέματος ",\n        "αυτός είναι ο αρχικός έλεγχος για το θέμα ",\n        "ολοκλήρωσε έναν επαληθευμένο κύκλο για το θέμα ",\n        "ανασκόπησε το θέμα ",\n        "προσάρμοσε την καθοδήγηση του θέματος ",\n        "πλήρης offline ροή εργασίας για το θέμα ",\n        "προσπάθεια να λυθεί το θέμα ",\n        "τις πρώτες ώρες χρησιμοποίησε το θέμα ",\n        "σε μεγαλύτερη διακοπή μετέτρεψε το θέμα ",\n        "αν αποτύχει το θέμα ",\n        "για περιορισμένη εκδοχή του θέματος ",\n        "αυτή η προχωρημένη διαδικασία προσθέτει βαθύτερο λειτουργικό επίπεδο χωρίς να αντικαθιστά τη βασική κάρτα",\n        "μην αφήσεις το θέμα ",\n    ),\n}\n\n# Generic similarity detector. A long item is considered templated when most of its 4-word\n# shingles recur in several other values in the same field. Four-word shingles keep normal\n# domain vocabulary from being mistaken for a template while still detecting sentence frames.\nSHINGLE_SIZE = 4\nSHINGLE_MIN_DOCUMENTS = 5\nSHINGLE_RATIO_THRESHOLD = 0.58\nSHINGLE_MIN_COUNT = 7\nNORMALIZED_DUP_MIN_CHARS = 45\nSENTENCE_DUP_MIN_CHARS = 70\nSENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\\s+")\nEDITORIAL_PREFIXES = {\n    "English": ("Continuing after this warning appears: ",),\n    "Ελληνικά": ("Συνέχιση μετά την εμφάνιση αυτής της προειδοποίησης: ",),\n}\n\n\n@dataclass\nclass RecordRef:\n    lang: str\n    path: Path\n    document: Any\n    records: list[dict[str, Any]]\n    index: int\n    record: dict[str, Any]\n\n\n@dataclass\nclass Unit:\n    lang: str\n    field: str\n    rid: str\n    title: str\n    category: str\n    subcategory: str\n    index: int | None\n    text: str\n    normalized: str\n    shingles: tuple[str, ...]\n\n\ndef record_lists(document: Any) -> list[dict[str, Any]]:\n    if isinstance(document, list):\n        return document if all(isinstance(r, dict) for r in document) else [r for r in document if isinstance(r, dict)]\n    if isinstance(document, dict):\n        for key in ("records", "items", "entries"):\n            value = document.get(key)\n            if isinstance(value, list):\n                return value if all(isinstance(r, dict) for r in value) else [r for r in value if isinstance(r, dict)]\n        for value in document.values():\n            if isinstance(value, list) and value and isinstance(value[0], dict):\n                return value\n    return []\n\n\ndef load_refs(lang: str) -> list[RecordRef]:\n    refs: list[RecordRef] = []\n    for path in sorted((ROOT / lang).rglob("*.json")):\n        try:\n            doc = json.loads(path.read_text(encoding="utf-8"))\n        except (OSError, UnicodeError, json.JSONDecodeError):\n            continue\n        records = record_lists(doc)\n        for i, record in enumerate(records):\n            refs.append(RecordRef(lang, path, doc, records, i, record))\n    return refs\n\n\ndef normalize(text: str, record: dict[str, Any]) -> str:\n    value = text.strip().casefold()\n    # Replace record-specific labels before quotes so translated title/category insertions do\n    # not disguise a shared sentence frame.\n    for key in ("title", "category", "subcategory"):\n        raw = str(record.get(key, "")).strip().casefold()\n        if len(raw) >= 4:\n            value = value.replace(raw, "{" + key + "}")\n    value = QUOTED_RE.sub("{quoted}", value)\n    value = URL_RE.sub("{url}", value)\n    value = NUMBER_RE.sub("{n}", value)\n    value = re.sub(r"\\s+", " ", value).strip()\n    return value\n\n\ndef shingle_tokens(normalized: str) -> tuple[str, ...]:\n    words = WORD_RE.findall(normalized)\n    if len(words) < SHINGLE_SIZE:\n        return ()\n    return tuple(" ".join(words[i:i + SHINGLE_SIZE]) for i in range(len(words) - SHINGLE_SIZE + 1))\n\n\ndef extract_units(refs: Iterable[RecordRef]) -> list[Unit]:\n    units: list[Unit] = []\n    for ref in refs:\n        r = ref.record\n        rid = str(r.get("id", "")).strip()\n        title = str(r.get("title", "")).strip()\n        for field in NARRATIVE_FIELDS:\n            value = r.get(field)\n            if isinstance(value, str) and value.strip():\n                n = normalize(value, r)\n                units.append(Unit(ref.lang, field, rid, title, str(r.get("category", "")), str(r.get("subcategory", "")), None, value.strip(), n, shingle_tokens(n)))\n            elif isinstance(value, list):\n                for idx, item in enumerate(value):\n                    if isinstance(item, str) and item.strip():\n                        n = normalize(item, r)\n                        units.append(Unit(ref.lang, field, rid, title, str(r.get("category", "")), str(r.get("subcategory", "")), idx, item.strip(), n, shingle_tokens(n)))\n    return units\n\n\n\ndef split_sentences(text: str) -> list[str]:\n    return [part.strip() for part in SENTENCE_SPLIT_RE.split(text.strip()) if part.strip()]\n\n\ndef strip_editorial_prefixes(text: str, lang: str) -> str:\n    value = text.strip()\n    for prefix in EDITORIAL_PREFIXES.get(lang, ()):\n        if value.startswith(prefix):\n            value = value[len(prefix):].lstrip()\n    return value\n\n\ndef sentence_duplicate_groups(refs: list[RecordRef]) -> list[tuple[int, str, str]]:\n    counts: collections.Counter[str] = collections.Counter()\n    examples: dict[str, str] = {}\n    for ref in refs:\n        for field in NARRATIVE_FIELDS:\n            value = ref.record.get(field)\n            vals = value if isinstance(value, list) else [value] if isinstance(value, str) else []\n            for item in vals:\n                if not isinstance(item, str):\n                    continue\n                item = strip_editorial_prefixes(item, ref.lang)\n                for sentence in split_sentences(item):\n                    normalized = normalize(sentence, ref.record)\n                    if len(normalized) >= SENTENCE_DUP_MIN_CHARS:\n                        counts[normalized] += 1\n                        examples.setdefault(normalized, sentence)\n    rows = [(count, normalized, examples[normalized]) for normalized, count in counts.items() if count > 1]\n    rows.sort(key=lambda row: (-row[0], row[1]))\n    return rows\n\n\ndef remove_repeated_sentences_paired(en: dict[str, RecordRef], el: dict[str, RecordRef], changed_paths: set[Path], stats: collections.Counter[str]) -> None:\n    seen_en: set[str] = set()\n    seen_el: set[str] = set()\n    for rid in sorted(set(en) & set(el)):\n        a, b = en[rid], el[rid]\n        for field in NARRATIVE_FIELDS:\n            va, vb = a.record.get(field), b.record.get(field)\n            if isinstance(va, str) and isinstance(vb, str):\n                left = split_sentences(strip_editorial_prefixes(va, "English"))\n                right = split_sentences(strip_editorial_prefixes(vb, "Ελληνικά"))\n                if len(left) != len(right):\n                    # Rare translation punctuation mismatch: preserve the pair unless the full field\n                    # is handled by the broader unit-level template detector.\n                    continue\n                out_l: list[str] = []\n                out_r: list[str] = []\n                for ls, rs in zip(left, right):\n                    nl, nr = normalize(ls, a.record), normalize(rs, b.record)\n                    duplicate = ((len(nl) >= SENTENCE_DUP_MIN_CHARS and nl in seen_en) or\n                                 (len(nr) >= SENTENCE_DUP_MIN_CHARS and nr in seen_el))\n                    if duplicate:\n                        stats["paired_repeated_sentences_removed"] += 1\n                        continue\n                    out_l.append(ls); out_r.append(rs)\n                    if len(nl) >= SENTENCE_DUP_MIN_CHARS: seen_en.add(nl)\n                    if len(nr) >= SENTENCE_DUP_MIN_CHARS: seen_el.add(nr)\n                new_l, new_r = " ".join(out_l).strip(), " ".join(out_r).strip()\n                if new_l != va.strip() or new_r != vb.strip():\n                    if new_l and new_r:\n                        a.record[field] = new_l; b.record[field] = new_r\n                    else:\n                        a.record.pop(field, None); b.record.pop(field, None)\n                    changed_paths.update((a.path, b.path))\n            elif isinstance(va, list) and isinstance(vb, list):\n                new_la: list[str] = []\n                new_lb: list[str] = []\n                for xa, xb in zip(va, vb):\n                    if not isinstance(xa, str) or not isinstance(xb, str):\n                        continue\n                    left = split_sentences(strip_editorial_prefixes(xa, "English"))\n                    right = split_sentences(strip_editorial_prefixes(xb, "Ελληνικά"))\n                    if len(left) != len(right):\n                        # If a mismatched item itself contains a known editorial prefix, keep its\n                        # unique warning but remove only the prefix; otherwise leave it intact.\n                        clean_a = strip_editorial_prefixes(xa, "English")\n                        clean_b = strip_editorial_prefixes(xb, "Ελληνικά")\n                        new_la.append(clean_a); new_lb.append(clean_b)\n                        if clean_a != xa.strip() or clean_b != xb.strip():\n                            stats["editorial_prefixes_removed"] += 1\n                            changed_paths.update((a.path, b.path))\n                        continue\n                    out_l: list[str] = []\n                    out_r: list[str] = []\n                    for ls, rs in zip(left, right):\n                        nl, nr = normalize(ls, a.record), normalize(rs, b.record)\n                        duplicate = ((len(nl) >= SENTENCE_DUP_MIN_CHARS and nl in seen_en) or\n                                     (len(nr) >= SENTENCE_DUP_MIN_CHARS and nr in seen_el))\n                        if duplicate:\n                            stats["paired_repeated_sentences_removed"] += 1\n                            continue\n                        out_l.append(ls); out_r.append(rs)\n                        if len(nl) >= SENTENCE_DUP_MIN_CHARS: seen_en.add(nl)\n                        if len(nr) >= SENTENCE_DUP_MIN_CHARS: seen_el.add(nr)\n                    clean_a, clean_b = " ".join(out_l).strip(), " ".join(out_r).strip()\n                    if clean_a and clean_b:\n                        new_la.append(clean_a); new_lb.append(clean_b)\n                    else:\n                        stats["paired_empty_items_removed"] += 1\n                if new_la != va or new_lb != vb:\n                    if new_la and new_lb:\n                        a.record[field] = new_la; b.record[field] = new_lb\n                    else:\n                        a.record.pop(field, None); b.record.pop(field, None)\n                    changed_paths.update((a.path, b.path))\n\n\ndef build_flags(refs: list[RecordRef]) -> tuple[set[tuple[str, str, int | None]], dict[str, Any]]:\n    units = extract_units(refs)\n    normalized_counts: dict[str, collections.Counter[str]] = {f: collections.Counter() for f in NARRATIVE_FIELDS}\n    shingle_df: dict[str, collections.Counter[str]] = {f: collections.Counter() for f in NARRATIVE_FIELDS}\n    for u in units:\n        if len(u.normalized) >= NORMALIZED_DUP_MIN_CHARS:\n            normalized_counts[u.field][u.normalized] += 1\n        shingle_df[u.field].update(set(u.shingles))\n\n    flags: set[tuple[str, str, int | None]] = set()\n    reasons = collections.Counter()\n    examples: dict[str, list[dict[str, Any]]] = collections.defaultdict(list)\n    markers = KNOWN_MARKERS[refs[0].lang] if refs else ()\n\n    for u in units:\n        key = (u.rid, u.field, u.index)\n        reason = None\n        if any(marker.casefold() in u.normalized for marker in markers):\n            reason = "known_template_signature"\n        elif len(u.normalized) >= NORMALIZED_DUP_MIN_CHARS and normalized_counts[u.field][u.normalized] > 1:\n            reason = "normalized_duplicate"\n        elif len(u.shingles) >= SHINGLE_MIN_COUNT:\n            recurring = sum(1 for s in u.shingles if shingle_df[u.field][s] >= SHINGLE_MIN_DOCUMENTS)\n            ratio = recurring / len(u.shingles)\n            if recurring >= SHINGLE_MIN_COUNT and ratio >= SHINGLE_RATIO_THRESHOLD:\n                reason = "shared_sentence_frame"\n        if reason:\n            flags.add(key)\n            reasons[reason] += 1\n            if len(examples[reason]) < 6:\n                examples[reason].append({"id": u.rid, "field": u.field, "text": u.text[:220]})\n\n    return flags, {\n        "units": len(units),\n        "flagged_units": len(flags),\n        "reasons": dict(reasons),\n        "examples": dict(examples),\n    }\n\n\ndef narrative_stats(record: dict[str, Any]) -> tuple[int, int]:\n    units = 0\n    chars = 0\n    for field in NARRATIVE_FIELDS:\n        value = record.get(field)\n        vals = value if isinstance(value, list) else [value] if isinstance(value, str) else []\n        for text in vals:\n            if isinstance(text, str) and text.strip():\n                units += 1\n                chars += len(text.strip())\n    return units, chars\n\n\ndef pair_maps() -> tuple[dict[str, RecordRef], dict[str, RecordRef], dict[Path, tuple[Any, list[dict[str, Any]]]]]:\n    en_refs = load_refs("English")\n    el_refs = load_refs("Ελληνικά")\n    en = {str(x.record.get("id", "")): x for x in en_refs if str(x.record.get("id", ""))}\n    el = {str(x.record.get("id", "")): x for x in el_refs if str(x.record.get("id", ""))}\n    docs: dict[Path, tuple[Any, list[dict[str, Any]]]] = {}\n    for ref in en_refs + el_refs:\n        docs[ref.path] = (ref.document, ref.records)\n    return en, el, docs\n\n\ndef clean_pairs(apply: bool) -> dict[str, Any]:\n    en_refs = load_refs("English")\n    el_refs = load_refs("Ελληνικά")\n    en = {str(x.record.get("id", "")): x for x in en_refs if str(x.record.get("id", ""))}\n    el = {str(x.record.get("id", "")): x for x in el_refs if str(x.record.get("id", ""))}\n    paired_ids = sorted(set(en) & set(el))\n    stats = collections.Counter()\n    changed_paths: set[Path] = set()\n    remove_ids: set[str] = set()\n    remove_repeated_sentences_paired(en, el, changed_paths, stats)\n    en_flags, en_report = build_flags(en_refs)\n    el_flags, el_report = build_flags(el_refs)\n\n    for rid in paired_ids:\n        a, b = en[rid], el[rid]\n        ra, rb = a.record, b.record\n\n        # Generation tags are internal implementation residue, not reader content.\n        for record, ref in ((ra, a), (rb, b)):\n            tags = record.get("tags")\n            if isinstance(tags, list):\n                new_tags = [t for t in tags if isinstance(t, str) and t.strip() and not INTERNAL_TAG_RE.search(t.strip()) and not re.search(r"\\bpass\\d+\\b", t, re.I)]\n                if new_tags != tags:\n                    record["tags"] = new_tags\n                    stats["internal_tags_removed"] += len(tags) - len(new_tags)\n                    changed_paths.add(ref.path)\n\n        # Keep user-facing enum metadata translated in Greek.\n        translations = {\n            "high": "υψηλή", "medium": "μεσαία", "low": "χαμηλή",\n            "advanced": "προχωρημένο", "basic": "βασικό", "intermediate": "μεσαίο",\n            "moderate_to_advanced": "μεσαίο έως προχωρημένο",\n            "basic_to_intermediate": "βασικό έως μεσαίο",\n            "preparedness_to_response": "προετοιμασία έως απόκριση",\n            "preparedness_to_immediate": "προετοιμασία έως άμεση δράση",\n        }\n        for field in ("difficulty", "urgency", "priority"):\n            cur = rb.get(field)\n            if isinstance(cur, str) and cur in translations:\n                rb[field] = translations[cur]\n                stats["metadata_translated"] += 1\n                changed_paths.add(b.path)\n\n        for field in NARRATIVE_FIELDS:\n            va, vb = ra.get(field), rb.get(field)\n            if field in SCALAR_FIELDS:\n                # Full translation parity: keep the field only when both translations have it\n                # and neither side is classified as repeated/template-generated.\n                keep = (\n                    isinstance(va, str) and va.strip() and isinstance(vb, str) and vb.strip()\n                    and (rid, field, None) not in en_flags\n                    and (rid, field, None) not in el_flags\n                )\n                if not keep:\n                    if field in ra:\n                        ra.pop(field, None); changed_paths.add(a.path); stats["paired_scalar_fields_removed"] += 1\n                    if field in rb:\n                        rb.pop(field, None); changed_paths.add(b.path)\n            else:\n                la = va if isinstance(va, list) else []\n                lb = vb if isinstance(vb, list) else []\n                out_a: list[str] = []\n                out_b: list[str] = []\n                seen_a: set[str] = set()\n                seen_b: set[str] = set()\n                for idx in range(min(len(la), len(lb))):\n                    xa, xb = la[idx], lb[idx]\n                    if not isinstance(xa, str) or not xa.strip() or not isinstance(xb, str) or not xb.strip():\n                        continue\n                    if (rid, field, idx) in en_flags or (rid, field, idx) in el_flags:\n                        stats["paired_list_items_removed"] += 1\n                        continue\n                    na, nb = normalize(xa, ra), normalize(xb, rb)\n                    # Within-record repetition is removed symmetrically.\n                    if na in seen_a or nb in seen_b:\n                        stats["within_record_duplicates_removed"] += 1\n                        continue\n                    seen_a.add(na); seen_b.add(nb)\n                    out_a.append(xa.strip()); out_b.append(xb.strip())\n                if out_a and out_b:\n                    if out_a != la:\n                        ra[field] = out_a; changed_paths.add(a.path)\n                    if out_b != lb:\n                        rb[field] = out_b; changed_paths.add(b.path)\n                else:\n                    if field in ra:\n                        ra.pop(field, None); changed_paths.add(a.path)\n                    if field in rb:\n                        rb.pop(field, None); changed_paths.add(b.path)\n\n        # Avoid summary/content saying the same thing within a record.\n        if isinstance(ra.get("summary"), str) and isinstance(ra.get("content"), str):\n            if normalize(ra["summary"], ra) == normalize(ra["content"], ra):\n                ra.pop("content", None); rb.pop("content", None)\n                stats["within_record_summary_content_duplicates_removed"] += 1\n                changed_paths.update((a.path, b.path))\n\n        ua, ca = narrative_stats(ra)\n        ub, cb = narrative_stats(rb)\n        # A record must still contain meaningful, actionable bilingual material after curation.\n        # Tiny title-only or one-line generated remnants are removed as a pair rather than kept\n        # merely to inflate the record count.\n        if ua == 0 or ub == 0 or ca < 90 or cb < 90:\n            remove_ids.add(rid)\n\n    if remove_ids:\n        for ref in en_refs + el_refs:\n            before = len(ref.records)\n            # Each ref points at a shared per-file list; mutate it only once per file below.\n        by_path: dict[Path, tuple[Any, list[dict[str, Any]]]] = {}\n        for ref in en_refs + el_refs:\n            by_path[ref.path] = (ref.document, ref.records)\n        for path, (doc, records) in by_path.items():\n            before = len(records)\n            records[:] = [r for r in records if str(r.get("id", "")) not in remove_ids]\n            if len(records) != before:\n                changed_paths.add(path)\n        stats["record_pairs_removed"] = len(remove_ids)\n\n    if apply:\n        # Write each changed document once. Empty lists are intentionally retained so bilingual\n        # path/file parity remains stable and existing bookmarks do not break.\n        by_path: dict[Path, Any] = {}\n        for ref in en_refs + el_refs:\n            by_path[ref.path] = ref.document\n        for path in sorted(changed_paths):\n            path.write_text(json.dumps(by_path[path], ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")\n\n    return {\n        "english_detection": en_report,\n        "greek_detection": el_report,\n        "paired_ids_before": len(paired_ids),\n        "changed_files": len(changed_paths),\n        **dict(stats),\n    }\n\n\ndef audit_language(lang: str) -> dict[str, Any]:\n    refs = load_refs(lang)\n    flags, detector = build_flags(refs)\n    exact_narrative = collections.Counter()\n    internal_tags = 0\n    zero_narrative: list[str] = []\n    for ref in refs:\n        r = ref.record\n        rid = str(r.get("id", ""))\n        for tag in r.get("tags", []) if isinstance(r.get("tags"), list) else []:\n            if isinstance(tag, str) and (INTERNAL_TAG_RE.search(tag.strip()) or re.search(r"\\bpass\\d+\\b", tag, re.I)):\n                internal_tags += 1\n        units, chars = narrative_stats(r)\n        if units == 0 or chars < 90:\n            zero_narrative.append(rid)\n        for field in NARRATIVE_FIELDS:\n            v = r.get(field)\n            vals = v if isinstance(v, list) else [v] if isinstance(v, str) else []\n            for text in vals:\n                if isinstance(text, str) and len(text.strip()) >= NORMALIZED_DUP_MIN_CHARS:\n                    exact_narrative[(field, re.sub(r"\\s+", " ", text.strip().casefold()))] += 1\n    dup_groups = [(field, count, text[:180]) for (field, text), count in exact_narrative.items() if count > 1]\n    dup_groups.sort(key=lambda x: (-x[1], x[0], x[2]))\n    sentence_dups = sentence_duplicate_groups(refs)\n    return {\n        "records": len(refs),\n        "detected_template_or_repeated_units": len(flags),\n        "detector_reasons": detector["reasons"],\n        "exact_substantive_duplicate_groups": len(dup_groups),\n        "repeated_substantive_sentence_groups": len(sentence_dups),\n        "internal_generation_tags": internal_tags,\n        "records_below_minimum_narrative": len(zero_narrative),\n        "examples": {\n            "detector": detector["examples"],\n            "exact_duplicates": dup_groups[:8],\n            "sentence_duplicates": [(count, text[:220]) for count, _normalized, text in sentence_dups[:8]],\n            "low_content_ids": zero_narrative[:8],\n        },\n        "pass": not flags and not dup_groups and not sentence_dups and internal_tags == 0 and not zero_narrative,\n    }\n\n\ndef audit() -> tuple[bool, dict[str, Any]]:\n    en = audit_language("English")\n    el = audit_language("Ελληνικά")\n    en_ids = {str(x.record.get("id", "")) for x in load_refs("English")}\n    el_ids = {str(x.record.get("id", "")) for x in load_refs("Ελληνικά")}\n    pair_ok = en_ids == el_ids\n    report = {\n        "English": en,\n        "Ελληνικά": el,\n        "translation_id_pairing": {\n            "english": len(en_ids), "greek": len(el_ids),\n            "missing_in_greek": sorted(en_ids - el_ids)[:20],\n            "missing_in_english": sorted(el_ids - en_ids)[:20],\n            "pass": pair_ok,\n        },\n    }\n    return bool(en["pass"] and el["pass"] and pair_ok), report\n\n\ndef main() -> int:\n    parser = argparse.ArgumentParser(description="Strict bilingual anti-template database quality gate")\n    parser.add_argument("--apply", action="store_true", help="Curate repeated/template prose symmetrically across EN/GR records.")\n    args = parser.parse_args()\n    if args.apply:\n        stats = clean_pairs(True)\n        print("Cleanup:")\n        print(json.dumps(stats, ensure_ascii=False, indent=2))\n    ok, report = audit()\n    print(json.dumps(report, ensure_ascii=False, indent=2))\n    print("[PASS] strict narrative quality" if ok else "[FAIL] strict narrative quality")\n    return 0 if ok else 1\n\n\n', 'translation_audit': '# MAINTENANCE: Treat EN/GR parity as a release invariant for all user-visible content.\n"""Bilingual completeness audit for Offline Survival Project."""\n\nimport json\nimport re\nimport sys\nfrom pathlib import Path\n\nROOT = Path(__file__).resolve().parents[1]\nGREEK_RE = re.compile(r"[Α-ΩΆΈΉΊΌΎΏα-ωάέήίόύώϊΐϋΰ]")\nRAW_ENGLISH_ENUMS = {\n    "basic", "beginner", "intermediate", "moderate", "advanced",\n    "basic_to_moderate", "basic_to_intermediate", "moderate_to_advanced", "basic_to_advanced",\n    "low", "medium", "high", "critical", "urgent", "immediate", "non_immediate", "seasonal",\n    "planning", "context_dependent", "varies_by_context", "scenario_dependent",\n    "preparedness_to_response", "preparedness_to_immediate",\n}\n\n\ndef load_records(root: Path) -> dict[str, dict]:\n    out: dict[str, dict] = {}\n    for path in sorted(root.rglob("*.json")):\n        data = json.loads(path.read_text(encoding="utf-8"))\n        if not isinstance(data, list):\n            continue\n        for record in data:\n            if isinstance(record, dict) and record.get("id"):\n                out[str(record["id"])] = record\n    return out\n\n\ndef main() -> int:\n    issues: list[str] = []\n    en = load_records(ROOT / "English")\n    el = load_records(ROOT / "Ελληνικά")\n    if set(en) != set(el):\n        issues.append(f"database ID mismatch: EN={len(en)} EL={len(el)}")\n\n    enum_leaks = []\n    greek_text_fail = []\n    for record_id, record in el.items():\n        for field in ("difficulty", "urgency", "priority"):\n            value = record.get(field)\n            if isinstance(value, str) and value.casefold() in RAW_ENGLISH_ENUMS:\n                enum_leaks.append((record_id, field, value))\n        combined = " ".join(str(record.get(field, "")) for field in ("title", "summary", "content"))\n        if len(combined) > 80 and len(GREEK_RE.findall(combined)) < 20:\n            greek_text_fail.append(record_id)\n    if enum_leaks:\n        issues.append("untranslated Greek metadata: " + repr(enum_leaks[:20]))\n    if greek_text_fail:\n        issues.append("Greek records lacking Greek narrative: " + repr(greek_text_fail[:20]))\n\n    # Paired records must expose the same user-visible fields and list cardinalities.\n    # This does not pretend to prove literary equivalence, but it catches missing translation\n    # sections and asymmetric cleanup immediately.\n    paired_fields = (\n        "title", "category", "subcategory", "summary", "content", "difficulty", "urgency", "priority",\n        "materials", "steps", "warnings", "common_mistakes", "alternatives", "failure_signs",\n        "when_not_to_use", "short_term", "long_term", "if_method_fails", "environment_notes",\n        "related_topics", "sources", "last_updated",\n    )\n    field_presence_mismatches = []\n    list_length_mismatches = []\n    for record_id in sorted(set(en) & set(el)):\n        left, right = en[record_id], el[record_id]\n        for field in paired_fields:\n            lp = field in left and left.get(field) not in (None, "", [])\n            rp = field in right and right.get(field) not in (None, "", [])\n            if lp != rp:\n                field_presence_mismatches.append((record_id, field, lp, rp))\n                continue\n            if lp and isinstance(left.get(field), list) and isinstance(right.get(field), list):\n                if len(left[field]) != len(right[field]):\n                    list_length_mismatches.append((record_id, field, len(left[field]), len(right[field])))\n    if field_presence_mismatches:\n        issues.append("paired database field-presence mismatch: " + repr(field_presence_mismatches[:20]))\n    if list_length_mismatches:\n        issues.append("paired database list-length mismatch: " + repr(list_length_mismatches[:20]))\n\n    # Any Library collection that has EN/ and GR/ directories must be one-for-one by relative filename.\n    library = ROOT / "Offline Library"\n    paired_collections = 0\n    paired_files = 0\n    greek_title_failures: list[str] = []\n    untranslated_greek_lines: list[str] = []\n    for collection in sorted(p for p in library.iterdir() if p.is_dir()):\n        en_dir, gr_dir = collection / "EN", collection / "GR"\n        if not (en_dir.is_dir() or gr_dir.is_dir()):\n            continue\n        paired_collections += 1\n        en_files = {p.relative_to(en_dir).as_posix() for p in en_dir.rglob("*") if p.is_file()} if en_dir.is_dir() else set()\n        gr_files = {p.relative_to(gr_dir).as_posix() for p in gr_dir.rglob("*") if p.is_file()} if gr_dir.is_dir() else set()\n        if en_files != gr_files:\n            issues.append(f"Library pair mismatch in {collection.name}: EN-only={sorted(en_files-gr_files)[:10]} GR-only={sorted(gr_files-en_files)[:10]}")\n        paired_files += min(len(en_files), len(gr_files))\n        if gr_dir.is_dir():\n            for rel in sorted(gr_files):\n                path = gr_dir / rel\n                if path.suffix.casefold() not in {".md", ".txt", ".csv", ".json", ".log"}:\n                    continue\n                text = path.read_text(encoding="utf-8", errors="replace")\n                if len(text) > 100 and len(GREEK_RE.findall(text)) < 20:\n                    issues.append(f"Greek Library file lacks translated body: {path.relative_to(ROOT)}")\n                if path.suffix.casefold() == ".md":\n                    first = next((line.strip() for line in text.splitlines() if line.strip()), "")\n                    if first.startswith("#") and not GREEK_RE.search(first):\n                        greek_title_failures.append(str(path.relative_to(ROOT)))\n                    for line_no, line in enumerate(text.splitlines(), 1):\n                        stripped = re.sub(r"[`*_#>|:/()\\[\\]-]", " ", line)\n                        if GREEK_RE.search(stripped):\n                            continue\n                        english_words = re.findall(r"\\b[A-Za-z]{3,}\\b", stripped)\n                        if len(english_words) >= 3:\n                            untranslated_greek_lines.append(f"{path.relative_to(ROOT)}:{line_no}: {line.strip()[:100]}")\n\n    if greek_title_failures:\n        issues.append("Greek Library headings left untranslated: " + repr(greek_title_failures[:20]))\n    if untranslated_greek_lines:\n        issues.append("English-only lines in Greek Library documents: " + repr(untranslated_greek_lines[:20]))\n\n    # Scan Greek UI translation literals for accidental English prose. Product/file-format\n    # names and executable identifiers are allowed; ordinary UI wording is not.\n    ui_mixed_language: list[str] = []\n    allowed_ui_tokens = {\n        "json", "gpx", "geojson", "sha", "gps", "kiwix", "serve", "csv", "zim", "kcal",\n        "docker", "api", "pin", "termux", "linux", "windows", "android",\n    }\n    for js_name in ("app.js", "field-operations.js", "continuity-operations.js", "knowledge-atlas.js"):\n        js_text = (ROOT / "web" / js_name).read_text(encoding="utf-8")\n        for value in re.findall(r"\\b\\w+:\'([^\'\\\\]*(?:\\\\.[^\'\\\\]*)*)\'", js_text):\n            if not GREEK_RE.search(value):\n                continue\n            scrubbed = value.replace("Offline Survival Project", "").replace("Offline Survival", "").replace("Offline Library", "")\n            english_words = [w.casefold() for w in re.findall(r"\\b[A-Za-z]{3,}\\b", scrubbed)]\n            unexpected = [w for w in english_words if w not in allowed_ui_tokens]\n            if unexpected:\n                ui_mixed_language.append(f"{js_name}: {unexpected!r}: {value[:140]}")\n    if ui_mixed_language:\n        issues.append("mixed English prose in Greek UI translations: " + repr(ui_mixed_language[:20]))\n\n    # MAINTENANCE: Current user-facing documentation must itself be bilingual.\n    current_docs = (\n        "README.md", "COMMAND_CENTER.md", "SECURITY.md", "THIRD_PARTY_NOTICES.md", "Offline Library/README.md",\n    )\n    current_doc_translation_failures: list[str] = []\n    for rel in current_docs:\n        path = ROOT / rel\n        if not path.is_file():\n            current_doc_translation_failures.append(f"missing: {rel}")\n            continue\n        text = path.read_text(encoding="utf-8", errors="replace")\n        greek_count = len(GREEK_RE.findall(text))\n        if greek_count < 80:\n            current_doc_translation_failures.append(f"insufficient Greek coverage: {rel} ({greek_count} Greek chars)")\n    if current_doc_translation_failures:\n        issues.append("current release documentation translation failures: " + repr(current_doc_translation_failures[:20]))\n\n    # The browser should not expose internal English path/tags in the Greek record modal.\n    app = (ROOT / "web" / "app.js").read_text(encoding="utf-8")\n    if "[r.category,r._path]" in app:\n        issues.append("record modal still exposes internal filesystem path")\n    record_order_match = re.search(r"const order=\\[([^\\]]+)\\]", app)\n    if record_order_match and "\'tags\'" in record_order_match.group(1):\n        issues.append("record modal still exposes internal/untranslated tag taxonomy")\n\n    print("Offline Survival Project — translation audit")\n    print("=" * 72)\n    print(f"Database pair: EN {len(en)} / EL {len(el)} records")\n    print(f"Paired Library collections: {paired_collections}")\n    print(f"Paired Library documents: {paired_files} EN + {paired_files} GR")\n    print(f"Untranslated Greek metadata enums: {len(enum_leaks)}")\n    print(f"Greek narrative failures: {len(greek_text_fail)}")\n    print(f"Paired field-presence mismatches: {len(field_presence_mismatches)}")\n    print(f"Paired list-length mismatches: {len(list_length_mismatches)}")\n    print(f"Greek Library heading failures: {len(greek_title_failures)}")\n    print(f"English-only lines in Greek Library: {len(untranslated_greek_lines)}")\n    print(f"Current-document translation failures: {len(current_doc_translation_failures)}")\n    print(f"Mixed-language Greek UI values: {len(ui_mixed_language)}")\n    if issues:\n        print(f"[FAIL] {len(issues)} issue(s)")\n        for issue in issues[:100]:\n            print(" - " + issue)\n        return 2\n    print("[PASS] Bilingual structure and user-visible translation checks passed")\n    return 0\n\n\n', 'library_quality': '# MAINTENANCE: Keep duplicate/template detection strict across paired Library collections.\n"""Offline Library anti-duplication/template audit for Offline Survival Project.\n\nStandard-library only. The checks are deliberately stricter than exact-file hashing:\n- no exact duplicate payloads;\n- no repeated substantive paragraphs (80+ normalized characters) within one language;\n- no known legacy boilerplate/template phrases;\n- no highly similar same-collection Markdown documents (3-word shingle Jaccard >= 0.45).\n"""\n\nimport hashlib\nimport itertools\nimport re\nfrom collections import defaultdict\nfrom pathlib import Path\n\nROOT = Path(__file__).resolve().parents[1]\nLIB = ROOT / "Offline Library"\nTEXT_SUFFIXES = {".md", ".txt", ".csv", ".json", ".log"}\nLANGS = ("EN", "GR")\nBOILERPLATE = (\n    "assume the situation begins now and internet/cloud services may be unavailable",\n    "what is the first verified information you need",\n    "operational field card. adapt it to the incident",\n    "printable/offline worksheet. fill only the information",\n    "offline survival project field worksheet. fill only what is useful",\n    "name one primary owner and one backup owner",\n    "record the location of the relevant supplies and paper references",\n    "verify the situation before changing the plan",\n    "what if the primary person is unavailable",\n    "use concise facts. separate verified information from assumptions",\n    "επιχειρησιακή κάρτα πεδίου. προσαρμόζεται στο συμβάν",\n    "εκτυπώσιμο/offline φύλλο. συμπλήρωσε μόνο πληροφορίες",\n    "φύλλο πεδίου του offline survival project. συμπλήρωσε μόνο",\n    "τι είναι η πρώτη επιβεβαιωμένη πληροφορία που χρειάζεσαι",\n)\n\n\ndef digest(path: Path) -> str:\n    h = hashlib.sha256()\n    with path.open("rb") as f:\n        for chunk in iter(lambda: f.read(1024 * 1024), b""):\n            h.update(chunk)\n    return h.hexdigest()\n\n\ndef norm_para(block: str) -> str:\n    lines = []\n    for line in block.splitlines():\n        s = line.strip()\n        if not s or s.startswith("#"):\n            continue\n        lines.append(s)\n    text = " ".join(lines)\n    text = re.sub(r"[`*_>|]", " ", text)\n    text = re.sub(r"\\s+", " ", text).strip().casefold()\n    return text\n\n\ndef word_shingles(text: str, n: int = 3) -> set[tuple[str, ...]]:\n    words = re.findall(r"[^\\W_]+", text.casefold(), flags=re.UNICODE)\n    return {tuple(words[i:i+n]) for i in range(max(0, len(words)-n+1))}\n\n\ndef main() -> int:\n    issues: list[str] = []\n    files = [p for p in LIB.rglob("*") if p.is_file() and not p.is_symlink()]\n\n    # Exact payload duplicates across the whole Library.\n    groups: dict[tuple[int, str], list[str]] = defaultdict(list)\n    for p in files:\n        groups[(p.stat().st_size, digest(p))].append(p.relative_to(LIB).as_posix())\n    duplicate_payloads = [v for v in groups.values() if len(v) > 1]\n    for group in duplicate_payloads:\n        issues.append("exact duplicate Library payload: " + " | ".join(group))\n\n    repeated_paragraphs = 0\n    boilerplate_hits = 0\n    high_similarity = 0\n\n    for lang in LANGS:\n        paragraphs: dict[str, list[str]] = defaultdict(list)\n        for p in files:\n            rel = p.relative_to(LIB).as_posix()\n            if f"/{lang}/" not in f"/{rel}":\n                continue\n            if p.suffix.casefold() not in TEXT_SUFFIXES:\n                continue\n            text = p.read_text(encoding="utf-8", errors="replace")\n            folded = text.casefold()\n            for phrase in BOILERPLATE:\n                if phrase in folded:\n                    boilerplate_hits += 1\n                    issues.append(f"legacy boilerplate phrase: {rel}: {phrase[:70]}")\n            for block in re.split(r"\\n\\s*\\n", text):\n                para = norm_para(block)\n                if len(para) >= 80:\n                    paragraphs[para].append(rel)\n        for para, refs in paragraphs.items():\n            if len(refs) > 1:\n                repeated_paragraphs += 1\n                issues.append(f"repeated substantive paragraph ({len(refs)} docs): {para[:120]} :: {\' | \'.join(refs[:8])}")\n\n    # Similarity catches files that escaped paragraph checks but still share a generated skeleton.\n    for collection in sorted(p for p in LIB.iterdir() if p.is_dir()):\n        for lang in LANGS:\n            lang_dir = collection / lang\n            if not lang_dir.is_dir():\n                continue\n            docs: list[tuple[Path, set[tuple[str, ...]]]] = []\n            for p in sorted(lang_dir.rglob("*.md")):\n                sh = word_shingles(p.read_text(encoding="utf-8", errors="replace"))\n                if sh:\n                    docs.append((p, sh))\n            for (a, aa), (b, bb) in itertools.combinations(docs, 2):\n                union = aa | bb\n                score = len(aa & bb) / len(union) if union else 0.0\n                if score >= 0.45:\n                    high_similarity += 1\n                    issues.append(\n                        f"template-like document similarity {score:.3f}: "\n                        f"{a.relative_to(LIB)} | {b.relative_to(LIB)}"\n                    )\n\n    print("Offline Survival Project — Library quality audit")\n    print("=" * 72)\n    print(f"Library files checked: {len(files)}")\n    print(f"Exact duplicate payload groups: {len(duplicate_payloads)}")\n    print(f"Repeated substantive paragraph groups: {repeated_paragraphs}")\n    print(f"Legacy boilerplate hits: {boilerplate_hits}")\n    print(f"Template-like similarity pairs: {high_similarity}")\n    if issues:\n        print(f"[FAIL] {len(issues)} issue(s)")\n        for issue in issues[:150]:\n            print(" - " + issue)\n        return 2\n    print("[PASS] No duplicate, repeated-boilerplate, or template-like Library content detected")\n    return 0\n\n\n', 'standalone_reader_test': '# MAINTENANCE: Keep the standalone reader network-free, bilingual, self-contained, and synchronized with the compendium.\n"""QA for the generated single-file Offline Survival Reader."""\nimport json,re,subprocess,shutil,tempfile,sys\nfrom pathlib import Path\nROOT=Path(__file__).resolve().parents[1]\nREADER=ROOT/\'Offline Survival Reader.html\'\nchecks=[]\ndef ck(name,ok,detail=\'\'):\n    checks.append((name,bool(ok),detail));print(f"[{\'PASS\' if ok else \'FAIL\'}] {name}"+(f": {detail}" if detail else \'\'))\nif not READER.is_file():\n    ck(\'reader-file\',False,str(READER));sys.exit(1)\ns=READER.read_text(encoding=\'utf-8\')\nck(\'reader-file\',len(s)>100000,f\'{READER.stat().st_size} bytes\')\nm=re.search(r\'<script>const CHAPTERS=(\\[.*?\\]);</script>\',s,re.S)\ndata=[]\ntry:data=json.loads(m.group(1)) if m else []\nexcept Exception as e:ck(\'embedded-json\',False,str(e))\nelse:ck(\'embedded-json\',True,f\'{len(data)} chapters\')\nids=[x.get(\'id\') for x in data]\nck(\'chapter-sequence\',ids==list(range(1,221)),f\'{ids[:3]}...{ids[-3:] if ids else []}\')\nck(\'bilingual-chapters\',all(x.get(\'en\',{}).get(\'title\') and x.get(\'en\',{}).get(\'body\') and x.get(\'el\',{}).get(\'title\') and x.get(\'el\',{}).get(\'body\') for x in data))\nck(\'no-external-assets\',\'<script src=\' not in s and \'<link rel="stylesheet"\' not in s)\nck(\'no-runtime-network\',not re.search(r\'\\b(?:fetch|XMLHttpRequest|WebSocket)\\s*\\(\',s))\nck(\'no-http-resource-tags\',not re.search(r\'(?:src|href)=["\\\']https?://\',s,re.I))\nck(\'mobile-viewport\',\'width=device-width\' in s and \'@media(max-width:800px)\' in s)\nck(\'local-search\',\'function filtered()\' in s and "id=\\"q\\"" in s)\nck(\'local-progress\',\'osp-reader-fav\' in s and \'osp-reader-reviewed\' in s and \'localStorage\' in s)\nck(\'print-support\',\'window.print\' not in s and "$(\'print\').onclick=()=>print()" in s)\nck(\'bilingual-ui\',\'Μονοαρχείος οδηγός επιβίωσης\' in s and \'Single-file survival library\' in s)\nnode=shutil.which(\'node\')\nif node:\n    scripts=re.findall(r\'<script>(.*?)</script>\',s,re.S)\n    with tempfile.NamedTemporaryFile(\'w\',suffix=\'.js\',delete=False,encoding=\'utf-8\') as f:\n        for block in scripts:f.write(block+\'\\n\')\n        tmp=Path(f.name)\n    proc=subprocess.run([node,\'--check\',str(tmp)],capture_output=True,text=True)\n    tmp.unlink(missing_ok=True)\n    ck(\'embedded-js-syntax\',proc.returncode==0,proc.stderr.strip())\nelse:ck(\'embedded-js-syntax\',True,\'Node unavailable; syntax covered by generator/static guards\')\nprint(f"Standalone reader QA: {sum(x[1] for x in checks)}/{len(checks)} PASS")\nsys.exit(0 if all(x[1] for x in checks) else 1)\n', 'build_standalone_reader': '# MAINTENANCE: Rebuild the reader only from audited bilingual Knowledge Compendium pairs; keep it self-contained.\n"""Build a single-file bilingual offline reader from the Knowledge Compendium."""\nimport json, re\nfrom pathlib import Path\nROOT=Path(__file__).resolve().parents[1]\nBASE=ROOT/\'Offline Library\'/\'Knowledge Compendium\'\nOUT=ROOT/\'Offline Survival Reader.html\'\nNUM=re.compile(r\'^(\\d+)-\')\n\ndef parse_file(path:Path):\n    text=path.read_text(encoding=\'utf-8\').strip()\n    lines=text.splitlines()\n    title=lines[0].lstrip(\'#\').strip() if lines else path.stem\n    body=\'\\n\'.join(lines[1:]).strip()\n    return title,body\n\ndef main():\n    en={int(NUM.match(p.name).group(1)):p for p in (BASE/\'EN\').glob(\'*.md\') if NUM.match(p.name) and int(NUM.match(p.name).group(1))>0}\n    gr={int(NUM.match(p.name).group(1)):p for p in (BASE/\'GR\').glob(\'*.md\') if NUM.match(p.name) and int(NUM.match(p.name).group(1))>0}\n    if set(en)!=set(gr): raise SystemExit(f\'Knowledge pairing mismatch: EN-only {sorted(set(en)-set(gr))}, GR-only {sorted(set(gr)-set(en))}\')\n    data=[]\n    for n in sorted(en):\n        et,eb=parse_file(en[n]); gt,gb=parse_file(gr[n])\n        data.append({\'id\':n,\'en\':{\'title\':et,\'body\':eb},\'el\':{\'title\':gt,\'body\':gb}})\n    payload=json.dumps(data,ensure_ascii=False,separators=(\',\',\':\')).replace(\'</\',\'<\\\\/\')\n    html=TEMPLATE.replace(\'__CHAPTER_COUNT__\',str(len(data))).replace(\'__DATA__\',payload)\n    OUT.write_text(html,encoding=\'utf-8\')\n    print(json.dumps({\'output\':str(OUT),\'chapters\':len(data),\'bytes\':OUT.stat().st_size},ensure_ascii=False))\nTEMPLATE=r\'\'\'<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><meta name="color-scheme" content="dark light"><title>Offline Survival Reader</title>\n<style>\n:root{--bg:#0b0e0c;--panel:#121713;--panel2:#19201b;--text:#edf6ef;--muted:#a8b8ab;--line:#304238;--accent:#86e29b;--warn:#ffd377}*{box-sizing:border-box}html,body{margin:0;min-height:100%;background:var(--bg);color:var(--text);font:15px/1.55 system-ui,-apple-system,Segoe UI,Roboto,sans-serif}button,input,select{font:inherit}button,select,input{background:var(--panel2);color:var(--text);border:1px solid var(--line);border-radius:10px;padding:10px}button{cursor:pointer}button:hover{border-color:var(--accent)}a{color:var(--accent)}.app{min-height:100vh;display:grid;grid-template-columns:320px minmax(0,1fr)}aside{border-right:1px solid var(--line);padding:14px;position:sticky;top:0;height:100vh;overflow:auto;background:var(--panel)}main{padding:20px 24px;max-width:1050px;width:100%;margin:0 auto}.brand{font-weight:800;font-size:18px}.sub{color:var(--muted);font-size:12px}.controls{display:grid;gap:8px;margin:14px 0}.row{display:flex;gap:8px;flex-wrap:wrap}.row>*{flex:1}.list{display:grid;gap:6px}.chapterBtn{text-align:left;width:100%;padding:10px}.chapterBtn.active{border-color:var(--accent);background:#1c2b20}.chapterBtn small{display:block;color:var(--muted)}.top{display:flex;justify-content:space-between;gap:12px;align-items:flex-start;flex-wrap:wrap;border-bottom:1px solid var(--line);padding-bottom:14px}.badge{display:inline-block;border:1px solid var(--line);border-radius:999px;padding:4px 8px;font-size:12px;color:var(--accent)}article{padding-bottom:50px}article h1{font-size:clamp(26px,5vw,44px);line-height:1.08;margin:18px 0}article h2{font-size:22px;margin-top:30px}article h3{font-size:18px;margin-top:26px}article p{max-width:80ch}article li{margin:6px 0}.sourceNote{border-left:3px solid var(--warn);padding:8px 12px;background:var(--panel);color:var(--muted)}mark{background:#665714;color:white}.empty{color:var(--muted);padding:20px 0}.mobileTop{display:none;position:sticky;top:0;z-index:20;background:var(--bg);padding:8px 0;border-bottom:1px solid var(--line)}@media(max-width:800px){.app{display:block}aside{position:fixed;inset:0 8% 0 0;z-index:40;transform:translateX(-110%);transition:.2s;height:100vh;box-shadow:0 0 40px #000}.menuOpen aside{transform:none}.mobileTop{display:flex;gap:8px;align-items:center}main{padding:0 14px 24px}.mobileTop button{flex:0 0 auto}.mobileTop span{white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.top{margin-top:8px}}@media print{aside,.mobileTop,.top .actions{display:none!important}.app{display:block}main{max-width:none;padding:0;background:white;color:black}body{background:white;color:black}.sourceNote{color:#333;background:#fff}}\n</style></head><body><div class="app" id="app"><aside><div class="brand">Offline Survival Reader</div><div class="sub" id="offlineLabel">Single-file survival library · __CHAPTER_COUNT__ chapters · no internet required</div><div class="controls"><input id="q" type="search" placeholder="Search all chapters"><select id="domain"></select><div class="row"><button id="lang">Ελληνικά</button><button id="favOnly">★ Favorites</button></div><div class="row"><button id="clear">Clear</button><button id="closeMenu">Close menu</button></div></div><div class="sub" id="count"></div><div class="list" id="list"></div></aside><main><div class="mobileTop"><button id="menu">☰</button><span id="mobileTitle">Offline Survival Reader</span></div><div class="top"><div><span class="badge" id="status">OFFLINE · LOCAL FILE</span><div class="sub" id="privacy">All knowledge is embedded in this HTML file. Searches and favorites stay in this browser.</div></div><div class="actions row"><button id="favorite">☆ Favorite</button><button id="reviewed">✓ Reviewed</button><button id="print">Print chapter</button></div></div><article id="article"></article></main></div>\n<script>const CHAPTERS=__DATA__;</script><script>\n\'use strict\';(()=>{const $=id=>document.getElementById(id),app=$(\'app\');let lang=(localStorage.getItem(\'osp-reader-lang\')||((navigator.language||\'\').toLowerCase().startsWith(\'el\')?\'el\':\'en\'));let current=Number(localStorage.getItem(\'osp-reader-current\')||1);let fav=new Set(JSON.parse(localStorage.getItem(\'osp-reader-fav\')||\'[]\'));let reviewed=new Set(JSON.parse(localStorage.getItem(\'osp-reader-reviewed\')||\'[]\'));let onlyFav=false;\nconst T={en:{offline:`Single-file survival library · ${CHAPTERS.length} chapters · no internet required`,search:\'Search all chapters\',fav:\'★ Favorites\',all:\'All knowledge\',water:\'Water / food / sanitation\',medical:\'Medical continuity / first aid\',hazards:\'Fire / earthquake / weather\',nav:\'Navigation / communications / recovery\',greece:\'Greece-specific\',resilience:\'Household resilience\',infra:\'Infrastructure / long outage\',advanced:\'Advanced operational safety\',urgent:\'Recognition / rescue / fire\',systems:\'Power / water / food / shelter\',global:\'Global hazard supplement\',clear:\'Clear\',close:\'Close menu\',privacy:\'All knowledge is embedded in this HTML file. Searches and favorites stay in this browser.\',favorite:\'☆ Favorite\',favorited:\'★ Favorited\',reviewed:\'✓ Reviewed\',markReview:\'✓ Mark reviewed\',print:\'Print chapter\',no:\'No chapters match this filter.\',count:n=>`${n} chapter${n===1?\'\':\'s\'}`,source:\'Source URLs are stored for verification when connectivity is available; the survival guidance itself is contained offline.\'},el:{offline:`Μονοαρχείος οδηγός επιβίωσης · ${CHAPTERS.length} κεφάλαια · χωρίς ανάγκη διαδικτύου`,search:\'Αναζήτηση σε όλα τα κεφάλαια\',fav:\'★ Αγαπημένα\',all:\'Όλη η γνώση\',water:\'Νερό / τρόφιμα / υγιεινή\',medical:\'Ιατρική συνέχεια / πρώτες βοήθειες\',hazards:\'Φωτιά / σεισμός / καιρός\',nav:\'Πλοήγηση / επικοινωνίες / αποκατάσταση\',greece:\'Ειδικά για Ελλάδα\',resilience:\'Ανθεκτικότητα νοικοκυριού\',infra:\'Υποδομές / μεγάλη διακοπή\',advanced:\'Προχωρημένη επιχειρησιακή ασφάλεια\',urgent:\'Αναγνώριση / διάσωση / φωτιά\',systems:\'Ρεύμα / νερό / τρόφιμα / καταφύγιο\',global:\'Παγκόσμιο συμπλήρωμα κινδύνων\',clear:\'Καθαρισμός\',close:\'Κλείσιμο μενού\',privacy:\'Όλη η γνώση βρίσκεται μέσα σε αυτό το HTML. Οι αναζητήσεις και τα αγαπημένα μένουν σε αυτόν τον browser.\',favorite:\'☆ Αγαπημένο\',favorited:\'★ Αγαπημένο\',reviewed:\'✓ Διαβασμένο\',markReview:\'✓ Σήμανση ως διαβασμένο\',print:\'Εκτύπωση κεφαλαίου\',no:\'Δεν υπάρχει κεφάλαιο με αυτά τα φίλτρα.\',count:n=>`${n} κεφάλαια`,source:\'Οι διευθύνσεις πηγών αποθηκεύονται για μελλοντική επαλήθευση όταν υπάρχει σύνδεση· η ίδια η καθοδήγηση επιβίωσης βρίσκεται αποθηκευμένη τοπικά.\'}};\nconst ranges=[[\'all\',1,999],[\'water\',1,14],[\'medical\',15,21],[\'hazards\',22,32],[\'nav\',33,40],[\'greece\',41,48],[\'resilience\',49,80],[\'infra\',81,127],[\'advanced\',128,160],[\'urgent\',161,180],[\'systems\',181,200],[\'global\',201,220]];\nfunction esc(v){return String(v).replace(/[&<>"\']/g,c=>({\'&\':\'&amp;\',\'<\':\'&lt;\',\'>\':\'&gt;\',\'"\':\'&quot;\',"\'":\'&#39;\'}[c]));}function save(){localStorage.setItem(\'osp-reader-lang\',lang);localStorage.setItem(\'osp-reader-current\',String(current));localStorage.setItem(\'osp-reader-fav\',JSON.stringify([...fav]));localStorage.setItem(\'osp-reader-reviewed\',JSON.stringify([...reviewed]));}\nfunction md(text){const out=[];let inList=false;for(const raw of text.split(/\\r?\\n/)){const line=raw.trim();if(!line){if(inList){out.push(\'</ul>\');inList=false}continue}if(line.startsWith(\'## \')){if(inList){out.push(\'</ul>\');inList=false}out.push(`<h2>${esc(line.slice(3))}</h2>`)}else if(line.startsWith(\'### \')){if(inList){out.push(\'</ul>\');inList=false}out.push(`<h3>${esc(line.slice(4))}</h3>`)}else if(/^[-*] /.test(line)){if(!inList){out.push(\'<ul>\');inList=true}out.push(`<li>${esc(line.slice(2))}</li>`)}else{if(inList){out.push(\'</ul>\');inList=false}out.push(`<p>${esc(line)}</p>`)}}if(inList)out.push(\'</ul>\');return out.join(\'\')}\nfunction setupDomains(){const d=$(\'domain\'),old=d.value||\'all\';d.innerHTML=ranges.map(([k])=>`<option value="${k}">${esc(T[lang][k])}</option>`).join(\'\');d.value=old}\nfunction filtered(){const q=$(\'q\').value.trim().toLocaleLowerCase(lang===\'el\'?\'el\':\'en\'),r=ranges.find(x=>x[0]===$(\'domain\').value)||ranges[0];return CHAPTERS.filter(c=>{if(c.id<r[1]||c.id>r[2]||onlyFav&&!fav.has(c.id))return false;if(!q)return true;const x=c[lang];return `${x.title}\\n${x.body}`.toLocaleLowerCase(lang===\'el\'?\'el\':\'en\').includes(q)})}\nfunction renderList(){const a=filtered();$(\'count\').textContent=T[lang].count(a.length);$(\'list\').innerHTML=a.map(c=>`<button class="chapterBtn ${c.id===current?\'active\':\'\'}" data-id="${c.id}"><small>${String(c.id).padStart(3,\'0\')} ${reviewed.has(c.id)?\'✓\':\'\'}${fav.has(c.id)?\' ★\':\'\'}</small>${esc(c[lang].title)}</button>`).join(\'\')||`<div class="empty">${esc(T[lang].no)}</div>`;document.querySelectorAll(\'.chapterBtn\').forEach(b=>b.onclick=()=>{current=Number(b.dataset.id);save();render();app.classList.remove(\'menuOpen\')})}\nfunction renderArticle(){let c=CHAPTERS.find(x=>x.id===current)||CHAPTERS[0];current=c.id;const x=c[lang];$(\'article\').innerHTML=`<h1><span class="badge">${String(c.id).padStart(3,\'0\')}</span><br>${esc(x.title)}</h1><div class="sourceNote">${esc(T[lang].source)}</div>${md(x.body)}`;$(\'mobileTitle\').textContent=`${c.id}. ${x.title}`;$(\'favorite\').textContent=fav.has(c.id)?T[lang].favorited:T[lang].favorite;$(\'reviewed\').textContent=reviewed.has(c.id)?T[lang].reviewed:T[lang].markReview;document.title=`${c.id}. ${x.title} — Offline Survival Reader`;save()}\nfunction labels(){$(\'offlineLabel\').textContent=T[lang].offline;$(\'q\').placeholder=T[lang].search;$(\'favOnly\').textContent=T[lang].fav;$(\'clear\').textContent=T[lang].clear;$(\'closeMenu\').textContent=T[lang].close;$(\'privacy\').textContent=T[lang].privacy;$(\'print\').textContent=T[lang].print;$(\'lang\').textContent=lang===\'en\'?\'Ελληνικά\':\'English\';setupDomains()}\nfunction render(){labels();renderList();renderArticle()}\n$(\'q\').oninput=renderList;$(\'domain\').onchange=renderList;$(\'lang\').onclick=()=>{lang=lang===\'en\'?\'el\':\'en\';save();render()};$(\'favOnly\').onclick=()=>{onlyFav=!onlyFav;$(\'favOnly\').style.borderColor=onlyFav?\'var(--accent)\':\'\';renderList()};$(\'favorite\').onclick=()=>{fav.has(current)?fav.delete(current):fav.add(current);save();render()};$(\'reviewed\').onclick=()=>{reviewed.has(current)?reviewed.delete(current):reviewed.add(current);save();render()};$(\'print\').onclick=()=>print();$(\'clear\').onclick=()=>{$(\'q\').value=\'\';$(\'domain\').value=\'all\';onlyFav=false;renderList()};$(\'menu\').onclick=()=>app.classList.add(\'menuOpen\');$(\'closeMenu\').onclick=()=>app.classList.remove(\'menuOpen\');addEventListener(\'keydown\',e=>{if(e.key===\'Escape\')app.classList.remove(\'menuOpen\')});render();})();\n</script></body></html>\'\'\'\nif __name__==\'__main__\': main()\n', 'api_smoke_test': '# MAINTENANCE: Exercise real loopback API/security behavior without touching the user\'s persistent state.\n"""Repeatable localhost API/security smoke test for Offline Survival Project.\n\nUses only the Python standard library. A temporary HOME keeps the user\'s real\nCommand Center state untouched.\n"""\n\nimport json\nimport os\nimport socket\nimport subprocess\nimport sys\nimport tempfile\nimport time\nfrom pathlib import Path\nfrom typing import Any\nfrom urllib import error, parse, request\n\nROOT = Path(__file__).resolve().parents[1]\nWEB_APP = ROOT / "Offline Survival.py"\nMIN_LIBRARY_FILES = 420\n\n\ndef free_port() -> int:\n    with socket.socket() as sock:\n        sock.bind(("127.0.0.1", 0))\n        return int(sock.getsockname()[1])\n\n\ndef main() -> int:\n    port = free_port()\n    base = f"http://127.0.0.1:{port}"\n    temp_home = tempfile.mkdtemp(prefix="offline-survival-qa-")\n    env = os.environ.copy()\n    env["HOME"] = temp_home\n    proc = subprocess.Popen(\n        [sys.executable, str(WEB_APP), "--web", "--host", "127.0.0.1", "--port", str(port), "--no-browser", "--quiet"],\n        cwd=ROOT,\n        env=env,\n        stdout=subprocess.DEVNULL,\n        stderr=subprocess.PIPE,\n        text=True,\n    )\n    checks: list[tuple[str, bool, str]] = []\n\n    def check(name: str, condition: bool, detail: str = "") -> None:\n        checks.append((name, bool(condition), detail))\n        print(f"[{\'PASS\' if condition else \'FAIL\'}] {name}" + (f" — {detail}" if detail else ""))\n\n    def call(path: str, method: str = "GET", payload: Any = None, headers: dict[str, str] | None = None):\n        body = None if payload is None else json.dumps(payload).encode("utf-8")\n        req_headers = {"Content-Type": "application/json"} if body is not None else {}\n        req_headers.update(headers or {})\n        req = request.Request(base + path, data=body, headers=req_headers, method=method)\n        try:\n            with request.urlopen(req, timeout=10) as response:\n                return response.status, dict(response.headers), response.read()\n        except error.HTTPError as exc:\n            return exc.code, dict(exc.headers), exc.read()\n\n    try:\n        for _ in range(80):\n            try:\n                if call("/api/meta")[0] == 200:\n                    break\n            except Exception:\n                pass\n            time.sleep(0.1)\n        else:\n            check("server-start", False, "Command Center did not start")\n            return 1\n\n        status, headers, raw = call("/api/meta")\n        meta = json.loads(raw)\n        check("meta-state-schema", status == 200 and isinstance(meta.get("state_schema_version"), int))\n        check("library-discovery", meta.get("system", {}).get("library_files", 0) >= MIN_LIBRARY_FILES, str(meta.get("system", {}).get("library_files")))\n        status, _, raw = call("/api/library")\n        library = json.loads(raw) if status == 200 else {}\n        knowledge_files = [x for x in library.get("files", []) if str(x.get("path", "")).startswith("Knowledge Compendium/")] if status == 200 else []\n        expected_knowledge = sum(1 for f in (ROOT / "Offline Library" / "Knowledge Compendium").rglob("*.md") if f.is_file())\n        check("knowledge-compendium-discovery", status == 200 and len(knowledge_files) == expected_knowledge, f"{len(knowledge_files)}/{expected_knowledge}")\n        prefix = parse.quote("Knowledge Compendium/EN", safe="")\n        query = parse.quote("water", safe="")\n        status, _, raw = call(f"/api/library/search?q={query}&limit=250&prefix={prefix}")\n        scoped = json.loads(raw) if status == 200 else {}\n        scoped_rows = scoped.get("results", [])\n        check("library-prefix-search", status == 200 and bool(scoped_rows) and all(str(x.get("path", "")).startswith("Knowledge Compendium/EN/") for x in scoped_rows), str(len(scoped_rows)))\n        bad_prefix = parse.quote("../", safe="")\n        status, _, _ = call(f"/api/library/search?q={query}&prefix={bad_prefix}")\n        check("library-prefix-traversal-rejected", status == 400, str(status))\n        check("security-headers", headers.get("X-Frame-Options") == "DENY" and "frame-ancestors" in headers.get("Content-Security-Policy", ""))\n\n        status, _, raw = call("/api/diagnostics")\n        diagnostics = json.loads(raw)\n        check("diagnostics", status == 200 and diagnostics.get("ok") is True)\n\n        state_a = {"profile": {"adults": 2}, "resource_plans": [{"name": "Water", "stock": 20, "unit": "L", "daily_use": 4, "reserve": 4}], "shelter_zones": [{"name": "Room A", "status": "safe", "occupants": 2}], "water_batches": [{"source": "Stored container", "volume_l": 12, "status": "ready"}], "skill_matrix": [{"person": "A", "skill": "Radio check", "level": "practiced"}], "decision_board": [{"issue": "Route", "decision": "Use alternate", "status": "active"}], "food_lots": [{"name": "Rice bin", "qty": 4, "unit": "kg", "kcal_total": 14000, "status": "sealed"}], "sanitation_points": [{"name": "Wash station", "kind": "handwash", "status": "ready"}], "power_loads": [{"name": "Radio", "watts": 8, "hours_per_day": 2, "priority": "critical", "enabled": True}], "comms_windows": [{"name": "Evening check", "method": "radio", "status": "active"}], "dependents": [{"name": "Pet A", "kind": "pet", "backup": "Neighbour"}], "expense_log": [{"category": "transport", "description": "Fuel", "amount": 20, "currency": "EUR", "status": "recorded"}], "knowledge_progress": [{"path": "01-emergency-water-reserve.md", "status": "reviewed", "last_review": "2026-08-09", "notes": "checked"}]}\n        state_b = {"profile": {"adults": 3}, "routes": [{"name": "Route", "points": [[999, 999], [40.3, 23.1], [40.4, 23.2]]}]}\n        status, _, raw = call("/api/state", "POST", state_a)\n        saved_a = json.loads(raw)\n        check("state-save", status == 200 and saved_a.get("profile", {}).get("adults") == 2 and saved_a.get("schema_version") == 7 and len(saved_a.get("shelter_zones", [])) == 1 and len(saved_a.get("water_batches", [])) == 1 and len(saved_a.get("skill_matrix", [])) == 1 and len(saved_a.get("decision_board", [])) == 1 and len(saved_a.get("food_lots", [])) == 1 and len(saved_a.get("sanitation_points", [])) == 1 and len(saved_a.get("power_loads", [])) == 1 and len(saved_a.get("comms_windows", [])) == 1 and len(saved_a.get("dependents", [])) == 1 and len(saved_a.get("expense_log", [])) == 1 and len(saved_a.get("knowledge_progress", [])) == 1)\n        status, _, raw = call("/api/state", "POST", state_b)\n        saved_b = json.loads(raw)\n        check("coordinate-sanitization", status == 200 and len(saved_b.get("routes", [{}])[0].get("points", [])) == 2)\n        status, _, raw = call("/api/state/previous")\n        check("previous-state-created", status == 200 and json.loads(raw).get("available") is True)\n        status, _, raw = call("/api/state/restore-previous", "POST", {})\n        restored = json.loads(raw)\n        check("previous-state-restore", status == 200 and restored.get("profile", {}).get("adults") == 2)\n        check("knowledge-progress-restore", status == 200 and len(restored.get("knowledge_progress", [])) == 1 and restored.get("knowledge_progress", [{}])[0].get("status") == "reviewed")\n\n        status, _, _ = call("/api/state", "POST", state_a, {"Origin": "https://example.invalid"})\n        check("cross-origin-write-rejected", status == 403, str(status))\n        status, _, _ = call("/api/state", "POST", state_a, {"Origin": base})\n        check("same-origin-write-accepted", status == 200, str(status))\n        status, _, _ = call("/api/state", "POST", state_a, {"Host": f"evil.example:{port}", "Origin": f"http://evil.example:{port}"})\n        check("localhost-host-header-rejected", status == 421, str(status))\n\n        status, _, raw = call("/api/library")\n        files = json.loads(raw).get("files", [])\n        readable = next((item for item in files if item.get("readable")), None)\n        check("library-list", status == 200 and readable is not None, str(len(files)))\n        if readable:\n            quoted = parse.quote(readable["path"], safe="")\n            status, _, raw = call("/api/library/hash?path=" + quoted)\n            digest = json.loads(raw).get("sha256", "")\n            check("library-sha256", status == 200 and len(digest) == 64)\n            status, _, raw = call("/api/library/text?path=" + quoted)\n            check("library-text-reader", status == 200 and bool(json.loads(raw).get("text")))\n            status, _, raw = call("/api/library/search?q=" + parse.quote("water"))\n            search_data = json.loads(raw)\n            check("library-full-text-search", status == 200 and search_data.get("count", 0) > 0 and bool(search_data.get("results", [{}])[0].get("snippet")), str(search_data.get("count", 0)))\n            status, direct_headers, _ = call("/library/" + parse.quote(readable["path"]))\n            check("untrusted-library-download", status == 200 and direct_headers.get("Content-Disposition", "").startswith("attachment;") and "default-src \'none\'" in direct_headers.get("Content-Security-Policy", ""))\n\n        status, _, _ = call("/api/library/text?path=../../Offline%20Survival.py")\n        check("library-path-traversal-rejected", status == 400, str(status))\n\n        status, _, raw = call("/api/library/search?q=water&limit=100")\n        v7_search = json.loads(raw) if status == 200 else {}\n        knowledge_search_rows = [x for x in v7_search.get("results", []) if str(x.get("path", "")).startswith("Knowledge Compendium/EN/")] if status == 200 else []\n        check("knowledge-full-text-search", status == 200 and len(knowledge_search_rows) > 0, str(len(knowledge_search_rows)))\n\n        assets = {"/": "text/html", "/styles.css": "text/css", "/app.js": "javascript", "/field-operations.js": "javascript", "/continuity-operations.js": "javascript", "/knowledge-atlas.js": "javascript", "/phone-test.html": "text/html", "/phone-test.js": "javascript", "/reader.html": "text/html", "/manifest.webmanifest": "manifest", "/sw.js": "javascript"}\n        for path, expected in assets.items():\n            status, asset_headers, raw = call(path)\n            check(f"asset:{path}", status == 200 and len(raw) > 100 and expected in asset_headers.get("Content-Type", ""))\n\n        passed = sum(ok for _, ok, _ in checks)\n        print("=" * 64)\n        print(f"{passed}/{len(checks)} API/security smoke checks passed")\n        return 0 if passed == len(checks) else 1\n    finally:\n        proc.terminate()\n        try:\n            proc.wait(timeout=3)\n        except subprocess.TimeoutExpired:\n            proc.kill()\n        if proc.returncode not in (None, 0, -15) and proc.stderr:\n            tail = proc.stderr.read()[-1000:]\n            if tail.strip():\n                print(tail, file=sys.stderr)\n\n\n'}
_EMBEDDED_WEB_SOURCE = '# MAINTENANCE: Keep the local server bound to loopback by default; preserve state-schema backward compatibility and same-origin protections.\n"""Offline Survival Project local Command Center.\n\nA zero-third-party-dependency local web interface for the bundled bilingual\nsurvival database. It binds to localhost by default, performs no telemetry,\nand stores user-created operational planning data locally under\n~/.offline_survival_project/.\n"""\n\n\nimport argparse\nimport hashlib\nimport importlib.util\nimport json\nimport math\nimport mimetypes\nimport os\nimport platform\nimport random\nimport shutil\nimport subprocess\nimport sys\nimport threading\nimport time\nfrom datetime import datetime, timezone\nfrom http import HTTPStatus\nfrom http.server import BaseHTTPRequestHandler, ThreadingHTTPServer\nfrom pathlib import Path\nfrom typing import Any\nfrom urllib.parse import parse_qs, quote, unquote, urlparse\n\nPROJECT_ROOT = Path(__file__).resolve().parent\nWEB_ROOT = PROJECT_ROOT / "web"\nINDEX_FILE = WEB_ROOT / "index.html"\nLIBRARY_ROOT = PROJECT_ROOT / "Offline Library"\nSTATE_DIR = Path.home() / ".offline_survival_project"\nSTATE_FILE = STATE_DIR / "user_state.json"\nSTATE_PREVIOUS_FILE = STATE_DIR / "user_state.previous.json"\nSCHEMA_VERSION = 7\nMAX_POST_BYTES = 4_000_000\nDEFAULT_PORT = 8765\nKIWIX_PORT = 8766\nLIBRARY_TEXT_SUFFIXES = frozenset({".txt", ".md", ".json", ".csv", ".log"})\nLIBRARY_SEARCH_MAX_BYTES = 1_000_000\n\nSCENARIOS: dict[str, dict[str, str]] = {\n    "water": {"en": "safe drinking water boil water emergency", "el": "ασφαλές πόσιμο νερό βράσιμο νερού έκτακτη ανάγκη"},\n    "power": {"en": "power outage electricity generator carbon monoxide food refrigerator", "el": "διακοπή ρεύματος γεννήτρια μονοξείδιο άνθρακα ψυγείο τρόφιμα"},\n    "wildfire": {"en": "wildfire smoke evacuation fire", "el": "δασική πυρκαγιά καπνός εκκένωση φωτιά"},\n    "flood": {"en": "flood flooded road water electricity evacuation", "el": "πλημμύρα πλημμυρισμένος δρόμος νερό ρεύμα εκκένωση"},\n    "heat": {"en": "heat stroke extreme heat cooling dehydration", "el": "θερμοπληξία καύσωνας ψύξη αφυδάτωση"},\n    "cold": {"en": "hypothermia cold exposure warming", "el": "υποθερμία έκθεση κρύο θέρμανση"},\n    "injury": {"en": "bleeding wound injury first aid trauma", "el": "αιμορραγία τραύμα τραυματισμός πρώτες βοήθειες"},\n    "food": {"en": "food safety power outage refrigerator freezer preservation", "el": "ασφάλεια τροφίμων διακοπή ρεύματος ψυγείο κατάψυξη διατήρηση"},\n    "evacuation": {"en": "evacuation go bag documents route family reunification", "el": "εκκένωση σακίδιο ανάγκης έγγραφα διαδρομή οικογένεια επανένωση"},\n    "communications": {"en": "emergency communications radio phone battery information", "el": "επικοινωνίες έκτακτης ανάγκης ραδιόφωνο τηλέφωνο μπαταρία πληροφορίες"},\n    "shelter": {"en": "shelter emergency home safety sanitation", "el": "καταφύγιο έκτακτη ανάγκη σπίτι ασφάλεια υγιεινή"},\n    "medicine": {"en": "medication continuity medicines storage chronic care", "el": "συνέχεια φαρμάκων αποθήκευση φαρμάκων χρόνια πάθηση"},\n}\n\nDEFAULT_STATE: dict[str, Any] = {\n    "favorites": [],\n    "notes": {},\n    "checklist": {},\n    "custom_checklist": [],\n    "profile": {\n        "adults": 1,\n        "children": 0,\n        "pets": 0,\n        "days": 3,\n        "water_liters": 0,\n        "food_kcal": 0,\n        "battery_wh": 0,\n    },\n    "inventory": [],\n    "contacts": [],\n    "incident_log": [],\n    "risk_flags": [],\n    "communications": {},\n    "evacuation": {},\n    "medical_card": {},\n    "medications": [],\n    "waypoints": [],\n    "navigation": {},\n    "documents": [],\n    "maintenance": [],\n    "roles": [],\n    "drill_history": [],\n    "continuity": {},\n    "resource_plans": [],\n    "checkins": [],\n    "vehicles": [],\n    "kits": [],\n    "field_logs": [],\n    "routes": [],\n    "shelter_zones": [],\n    "water_batches": [],\n    "recovery_items": [],\n    "skill_matrix": [],\n    "decision_board": [],\n    "food_lots": [],\n    "sanitation_points": [],\n    "power_loads": [],\n    "comms_windows": [],\n    "dependents": [],\n    "expense_log": [],\n    "knowledge_progress": [],\n    "settings": {"low_power": False},\n    "schema_version": SCHEMA_VERSION,\n    "updated_at": "",\n}\n\n_KIWIX_PROCESS: subprocess.Popen[Any] | None = None\n_KIWIX_LOCK = threading.Lock()\n_INTEGRITY_LOCK = threading.Lock()\n_INTEGRITY_CACHE: dict[str, Any] | None = None\n\n\ndef load_core() -> Any:\n    path = PROJECT_ROOT / "Offline Survival.py"\n    spec = importlib.util.spec_from_file_location("offline_survival_core", path)\n    if spec is None or spec.loader is None:\n        raise RuntimeError("Could not load the Offline Survival core")\n    module = importlib.util.module_from_spec(spec)\n    spec.loader.exec_module(module)\n    return module\n\n\nCORE = load_core()\nDATABASE = CORE.OfflineDatabase()\n\n\n\n\ndef integrity_report_cached() -> dict[str, Any]:\n    global _INTEGRITY_CACHE\n    with _INTEGRITY_LOCK:\n        if _INTEGRITY_CACHE is None:\n            _INTEGRITY_CACHE = DATABASE.integrity_report()\n        return _INTEGRITY_CACHE\n\ndef safe_json_read(path: Path, default: Any) -> Any:\n    try:\n        return json.loads(path.read_text(encoding="utf-8"))\n    except (OSError, UnicodeError, json.JSONDecodeError):\n        return default\n\n\ndef _clean_text(value: Any, limit: int) -> str:\n    return str(value or "").strip()[:limit]\n\n\ndef _bounded_int(value: Any, default: int, minimum: int, maximum: int) -> int:\n    try:\n        return max(minimum, min(maximum, int(value)))\n    except (TypeError, ValueError):\n        return default\n\n\ndef _bounded_float(value: Any, default: float, minimum: float, maximum: float) -> float:\n    try:\n        number = float(value)\n        if not math.isfinite(number):\n            return default\n        return max(minimum, min(maximum, number))\n    except (TypeError, ValueError):\n        return default\n\n\ndef _clean_date(value: Any) -> str:\n    text = _clean_text(value, 10)\n    if not text:\n        return ""\n    try:\n        datetime.strptime(text, "%Y-%m-%d")\n    except ValueError:\n        return ""\n    return text\n\n\ndef _clean_datetime(value: Any) -> str:\n    text = _clean_text(value, 40)\n    if not text:\n        return ""\n    try:\n        datetime.fromisoformat(text.replace("Z", "+00:00"))\n    except ValueError:\n        return ""\n    return text\n\n\ndef load_state() -> dict[str, Any]:\n    saved = safe_json_read(STATE_FILE, {})\n    if not isinstance(saved, dict):\n        saved = {}\n    # Run old and new state through one sanitizer so schema upgrades stay safe.\n    try:\n        return sanitize_state(saved)\n    except ValueError:\n        return sanitize_state({})\n\n\ndef sanitize_state(candidate: Any) -> dict[str, Any]:\n    if not isinstance(candidate, dict):\n        raise ValueError("State must be a JSON object")\n\n    favorites = candidate.get("favorites", [])\n    notes = candidate.get("notes", {})\n    checklist = candidate.get("checklist", {})\n    custom = candidate.get("custom_checklist", [])\n    profile = candidate.get("profile", {})\n    inventory = candidate.get("inventory", [])\n    contacts = candidate.get("contacts", [])\n    incident_log = candidate.get("incident_log", [])\n    risk_flags = candidate.get("risk_flags", [])\n    communications = candidate.get("communications", {})\n    evacuation = candidate.get("evacuation", {})\n    medical_card = candidate.get("medical_card", {})\n    medications = candidate.get("medications", [])\n    waypoints = candidate.get("waypoints", [])\n    navigation = candidate.get("navigation", {})\n    documents = candidate.get("documents", [])\n    maintenance = candidate.get("maintenance", [])\n    roles = candidate.get("roles", [])\n    drill_history = candidate.get("drill_history", [])\n    continuity = candidate.get("continuity", {})\n    resource_plans = candidate.get("resource_plans", [])\n    checkins = candidate.get("checkins", [])\n    vehicles = candidate.get("vehicles", [])\n    kits = candidate.get("kits", [])\n    field_logs = candidate.get("field_logs", [])\n    routes = candidate.get("routes", [])\n    shelter_zones = candidate.get("shelter_zones", [])\n    water_batches = candidate.get("water_batches", [])\n    recovery_items = candidate.get("recovery_items", [])\n    skill_matrix = candidate.get("skill_matrix", [])\n    decision_board = candidate.get("decision_board", [])\n    food_lots = candidate.get("food_lots", [])\n    sanitation_points = candidate.get("sanitation_points", [])\n    power_loads = candidate.get("power_loads", [])\n    comms_windows = candidate.get("comms_windows", [])\n    dependents = candidate.get("dependents", [])\n    expense_log = candidate.get("expense_log", [])\n    knowledge_progress = candidate.get("knowledge_progress", [])\n    settings = candidate.get("settings", {})\n\n    if not isinstance(favorites, list) or len(favorites) > 5000:\n        raise ValueError("Invalid favorites")\n    clean_favorites = [_clean_text(item, 180) for item in favorites if _clean_text(item, 180)]\n    clean_favorites = list(dict.fromkeys(clean_favorites))\n\n    if not isinstance(notes, dict) or len(notes) > 5000:\n        raise ValueError("Invalid notes")\n    clean_notes = {_clean_text(key, 180): str(value)[:12000] for key, value in notes.items() if _clean_text(key, 180) and str(value).strip()}\n\n    if not isinstance(checklist, dict) or len(checklist) > 1000:\n        raise ValueError("Invalid checklist")\n    clean_checklist = {_clean_text(key, 180): bool(value) for key, value in checklist.items() if _clean_text(key, 180)}\n\n    if not isinstance(custom, list) or len(custom) > 500:\n        raise ValueError("Invalid custom checklist")\n    clean_custom: list[dict[str, Any]] = []\n    for item in custom:\n        if not isinstance(item, dict):\n            continue\n        text = _clean_text(item.get("text"), 300)\n        if text:\n            clean_custom.append({"id": _clean_text(item.get("id"), 80) or f"custom-{len(clean_custom)+1}", "text": text, "done": bool(item.get("done", False))})\n\n    if not isinstance(profile, dict):\n        profile = {}\n    clean_profile = {\n        "adults": _bounded_int(profile.get("adults"), 1, 0, 50),\n        "children": _bounded_int(profile.get("children"), 0, 0, 50),\n        "pets": _bounded_int(profile.get("pets"), 0, 0, 50),\n        "days": _bounded_int(profile.get("days"), 3, 1, 365),\n        "water_liters": _bounded_float(profile.get("water_liters"), 0, 0, 1_000_000),\n        "food_kcal": _bounded_float(profile.get("food_kcal"), 0, 0, 100_000_000),\n        "battery_wh": _bounded_float(profile.get("battery_wh"), 0, 0, 10_000_000),\n    }\n\n    if not isinstance(inventory, list) or len(inventory) > 2000:\n        raise ValueError("Invalid inventory")\n    clean_inventory: list[dict[str, Any]] = []\n    for item in inventory:\n        if not isinstance(item, dict):\n            continue\n        name = _clean_text(item.get("name"), 160)\n        if not name:\n            continue\n        clean_inventory.append({\n            "id": _clean_text(item.get("id"), 80) or f"inventory-{len(clean_inventory)+1}",\n            "name": name,\n            "category": _clean_text(item.get("category"), 80),\n            "qty": _bounded_float(item.get("qty"), 0, 0, 1_000_000_000),\n            "unit": _clean_text(item.get("unit"), 40),\n            "expiry": _clean_date(item.get("expiry")),\n            "notes": _clean_text(item.get("notes"), 500),\n        })\n\n    if not isinstance(contacts, list) or len(contacts) > 250:\n        raise ValueError("Invalid contacts")\n    clean_contacts: list[dict[str, Any]] = []\n    for item in contacts:\n        if not isinstance(item, dict):\n            continue\n        name = _clean_text(item.get("name"), 120)\n        if not name:\n            continue\n        clean_contacts.append({\n            "id": _clean_text(item.get("id"), 80) or f"contact-{len(clean_contacts)+1}",\n            "name": name,\n            "role": _clean_text(item.get("role"), 100),\n            "phone": _clean_text(item.get("phone"), 80),\n            "meeting": _clean_text(item.get("meeting"), 240),\n            "notes": _clean_text(item.get("notes"), 500),\n        })\n\n    if not isinstance(incident_log, list) or len(incident_log) > 2000:\n        raise ValueError("Invalid incident log")\n    clean_log: list[dict[str, Any]] = []\n    for item in incident_log:\n        if not isinstance(item, dict):\n            continue\n        event = _clean_text(item.get("event"), 500)\n        action = _clean_text(item.get("action"), 1000)\n        if not event and not action:\n            continue\n        clean_log.append({\n            "id": _clean_text(item.get("id"), 80) or f"log-{len(clean_log)+1}",\n            "time": _clean_datetime(item.get("time")),\n            "event": event,\n            "action": action,\n            "status": _clean_text(item.get("status"), 80),\n        })\n\n    if not isinstance(risk_flags, list) or len(risk_flags) > 100:\n        raise ValueError("Invalid risk flags")\n    known_risks = {"wildfire", "flood", "earthquake", "outage", "heat", "cold", "evacuation", "isolation"}\n    clean_risks = list(dict.fromkeys(x for x in (_clean_text(v, 80) for v in risk_flags) if x in known_risks))\n\n    def clean_small_dict(value: Any, limit: int = 40) -> dict[str, str]:\n        if not isinstance(value, dict) or len(value) > limit:\n            return {}\n        return {_clean_text(k, 80): _clean_text(v, 1000) for k, v in value.items() if _clean_text(k, 80) and _clean_text(v, 1000)}\n\n    clean_medical = clean_small_dict(medical_card, 40)\n\n    if not isinstance(medications, list) or len(medications) > 500:\n        raise ValueError("Invalid medications")\n    clean_medications: list[dict[str, Any]] = []\n    for item in medications:\n        if not isinstance(item, dict):\n            continue\n        name = _clean_text(item.get("name"), 160)\n        if not name:\n            continue\n        clean_medications.append({\n            "id": _clean_text(item.get("id"), 80) or f"med-{len(clean_medications)+1}",\n            "name": name,\n            "purpose": _clean_text(item.get("purpose"), 240),\n            "instructions": _clean_text(item.get("instructions"), 500),\n            "on_hand": _bounded_float(item.get("on_hand"), 0, 0, 10_000_000),\n            "unit": _clean_text(item.get("unit"), 40),\n            "refill": _clean_date(item.get("refill")),\n            "notes": _clean_text(item.get("notes"), 500),\n        })\n\n    if not isinstance(waypoints, list) or len(waypoints) > 1000:\n        raise ValueError("Invalid waypoints")\n    clean_waypoints: list[dict[str, Any]] = []\n    for item in waypoints:\n        if not isinstance(item, dict):\n            continue\n        name = _clean_text(item.get("name"), 160)\n        if not name:\n            continue\n        lat = _bounded_float(item.get("lat"), 0, -90, 90)\n        lon = _bounded_float(item.get("lon"), 0, -180, 180)\n        clean_waypoints.append({\n            "id": _clean_text(item.get("id"), 80) or f"waypoint-{len(clean_waypoints)+1}",\n            "name": name,\n            "type": _clean_text(item.get("type"), 80),\n            "lat": lat,\n            "lon": lon,\n            "notes": _clean_text(item.get("notes"), 800),\n        })\n    clean_navigation: dict[str, Any] = {}\n    if isinstance(navigation, dict) and "origin_lat" in navigation and "origin_lon" in navigation:\n        try:\n            nav_lat = float(navigation.get("origin_lat"))\n            nav_lon = float(navigation.get("origin_lon"))\n        except (TypeError, ValueError):\n            nav_lat = nav_lon = math.nan\n        if math.isfinite(nav_lat) and math.isfinite(nav_lon) and -90 <= nav_lat <= 90 and -180 <= nav_lon <= 180:\n            clean_navigation = {"origin_lat": round(nav_lat, 7), "origin_lon": round(nav_lon, 7)}\n\n    if not isinstance(documents, list) or len(documents) > 1000:\n        raise ValueError("Invalid document register")\n    clean_documents: list[dict[str, Any]] = []\n    for item in documents:\n        if not isinstance(item, dict):\n            continue\n        name = _clean_text(item.get("name"), 180)\n        if not name:\n            continue\n        clean_documents.append({\n            "id": _clean_text(item.get("id"), 80) or f"doc-{len(clean_documents)+1}",\n            "name": name,\n            "copy_type": _clean_text(item.get("copy_type"), 100),\n            "location": _clean_text(item.get("location"), 300),\n            "review": _clean_date(item.get("review")),\n            "notes": _clean_text(item.get("notes"), 600),\n        })\n\n    if not isinstance(maintenance, list) or len(maintenance) > 1000:\n        raise ValueError("Invalid maintenance schedule")\n    clean_maintenance: list[dict[str, Any]] = []\n    for item in maintenance:\n        if not isinstance(item, dict):\n            continue\n        task = _clean_text(item.get("task"), 220)\n        if not task:\n            continue\n        clean_maintenance.append({\n            "id": _clean_text(item.get("id"), 80) or f"maint-{len(clean_maintenance)+1}",\n            "task": task,\n            "interval_days": _bounded_int(item.get("interval_days"), 30, 1, 3650),\n            "last_done": _clean_date(item.get("last_done")),\n            "notes": _clean_text(item.get("notes"), 600),\n        })\n\n    if not isinstance(roles, list) or len(roles) > 250:\n        raise ValueError("Invalid household roles")\n    clean_roles: list[dict[str, Any]] = []\n    for item in roles:\n        if not isinstance(item, dict):\n            continue\n        name = _clean_text(item.get("name"), 140)\n        if not name:\n            continue\n        clean_roles.append({\n            "id": _clean_text(item.get("id"), 80) or f"role-{len(clean_roles)+1}",\n            "name": name,\n            "primary": _clean_text(item.get("primary"), 180),\n            "backup": _clean_text(item.get("backup"), 180),\n            "skills": _clean_text(item.get("skills"), 500),\n        })\n\n    if not isinstance(drill_history, list) or len(drill_history) > 500:\n        raise ValueError("Invalid drill history")\n    clean_drills: list[dict[str, Any]] = []\n    for item in drill_history:\n        if not isinstance(item, dict):\n            continue\n        scenario = _clean_text(item.get("scenario"), 100)\n        if not scenario:\n            continue\n        clean_drills.append({\n            "id": _clean_text(item.get("id"), 80) or f"drill-{len(clean_drills)+1}",\n            "scenario": scenario,\n            "time": _clean_datetime(item.get("time")),\n            "completed": _bounded_int(item.get("completed"), 0, 0, 50),\n            "total": _bounded_int(item.get("total"), 0, 0, 50),\n            "score": _bounded_int(item.get("score"), 0, 0, 100),\n            "debrief": _clean_text(item.get("debrief"), 2000),\n        })\n\n    clean_continuity = clean_small_dict(continuity, 50)\n\n    if not isinstance(resource_plans, list) or len(resource_plans) > 500:\n        raise ValueError("Invalid resource plans")\n    clean_resource_plans: list[dict[str, Any]] = []\n    for item in resource_plans:\n        if not isinstance(item, dict):\n            continue\n        name = _clean_text(item.get("name"), 160)\n        if not name:\n            continue\n        clean_resource_plans.append({\n            "id": _clean_text(item.get("id"), 80) or f"resource-{len(clean_resource_plans)+1}",\n            "name": name,\n            "stock": _bounded_float(item.get("stock"), 0, 0, 1_000_000_000),\n            "unit": _clean_text(item.get("unit"), 40),\n            "daily_use": _bounded_float(item.get("daily_use"), 0, 0, 1_000_000_000),\n            "reserve": _bounded_float(item.get("reserve"), 0, 0, 1_000_000_000),\n            "notes": _clean_text(item.get("notes"), 700),\n        })\n\n    if not isinstance(checkins, list) or len(checkins) > 500:\n        raise ValueError("Invalid check-ins")\n    clean_checkins: list[dict[str, Any]] = []\n    for item in checkins:\n        if not isinstance(item, dict):\n            continue\n        name = _clean_text(item.get("name"), 140)\n        if not name:\n            continue\n        clean_checkins.append({\n            "id": _clean_text(item.get("id"), 80) or f"checkin-{len(clean_checkins)+1}",\n            "name": name,\n            "status": _clean_text(item.get("status"), 80) if _clean_text(item.get("status"), 80) in {"ok", "away", "unknown", "needs-help"} else "unknown",\n            "location": _clean_text(item.get("location"), 240),\n            "time": _clean_datetime(item.get("time")),\n            "next": _clean_datetime(item.get("next")),\n            "notes": _clean_text(item.get("notes"), 700),\n        })\n\n    if not isinstance(vehicles, list) or len(vehicles) > 100:\n        raise ValueError("Invalid vehicles")\n    clean_vehicles: list[dict[str, Any]] = []\n    for item in vehicles:\n        if not isinstance(item, dict):\n            continue\n        name = _clean_text(item.get("name"), 160)\n        if not name:\n            continue\n        clean_vehicles.append({\n            "id": _clean_text(item.get("id"), 80) or f"vehicle-{len(clean_vehicles)+1}",\n            "name": name,\n            "fuel_l": _bounded_float(item.get("fuel_l"), 0, 0, 10_000),\n            "consumption_l100km": _bounded_float(item.get("consumption_l100km"), 0, 0, 1000),\n            "battery_pct": _bounded_float(item.get("battery_pct"), 0, 0, 100),\n            "odometer_km": _bounded_float(item.get("odometer_km"), 0, 0, 100_000_000),\n            "last_check": _clean_date(item.get("last_check")),\n            "notes": _clean_text(item.get("notes"), 700),\n        })\n\n    if not isinstance(kits, list) or len(kits) > 100:\n        raise ValueError("Invalid kits")\n    clean_kits: list[dict[str, Any]] = []\n    for item in kits:\n        if not isinstance(item, dict):\n            continue\n        name = _clean_text(item.get("name"), 160)\n        if not name:\n            continue\n        raw_items = item.get("items", [])\n        if not isinstance(raw_items, list) or len(raw_items) > 250:\n            raw_items = []\n        clean_items: list[dict[str, Any]] = []\n        for kit_item in raw_items:\n            if not isinstance(kit_item, dict):\n                continue\n            item_name = _clean_text(kit_item.get("name"), 160)\n            if not item_name:\n                continue\n            clean_items.append({\n                "id": _clean_text(kit_item.get("id"), 80) or f"kit-item-{len(clean_items)+1}",\n                "name": item_name,\n                "qty": _bounded_float(kit_item.get("qty"), 1, 0, 1_000_000),\n                "weight_g": _bounded_float(kit_item.get("weight_g"), 0, 0, 10_000_000),\n                "packed": bool(kit_item.get("packed", False)),\n                "critical": bool(kit_item.get("critical", False)),\n                "notes": _clean_text(kit_item.get("notes"), 400),\n            })\n        clean_kits.append({\n            "id": _clean_text(item.get("id"), 80) or f"kit-{len(clean_kits)+1}",\n            "name": name,\n            "owner": _clean_text(item.get("owner"), 140),\n            "max_weight_kg": _bounded_float(item.get("max_weight_kg"), 0, 0, 1000),\n            "notes": _clean_text(item.get("notes"), 700),\n            "items": clean_items,\n        })\n\n    if not isinstance(field_logs, list) or len(field_logs) > 2000:\n        raise ValueError("Invalid field logs")\n    clean_field_logs: list[dict[str, Any]] = []\n    for item in field_logs:\n        if not isinstance(item, dict):\n            continue\n        label = _clean_text(item.get("label"), 160)\n        notes_text = _clean_text(item.get("notes"), 1200)\n        if not label and not notes_text:\n            continue\n        clean_field_logs.append({\n            "id": _clean_text(item.get("id"), 80) or f"field-{len(clean_field_logs)+1}",\n            "time": _clean_datetime(item.get("time")),\n            "label": label,\n            "value": _clean_text(item.get("value"), 160),\n            "unit": _clean_text(item.get("unit"), 40),\n            "notes": notes_text,\n        })\n\n    if not isinstance(routes, list) or len(routes) > 20:\n        raise ValueError("Invalid routes")\n    clean_routes: list[dict[str, Any]] = []\n    route_point_budget = 25_000\n    for item in routes:\n        if route_point_budget <= 0:\n            break\n        if not isinstance(item, dict):\n            continue\n        name = _clean_text(item.get("name"), 160)\n        points = item.get("points", [])\n        if not name or not isinstance(points, list):\n            continue\n        points = points[: min(5000, route_point_budget)]\n        clean_points: list[list[float]] = []\n        for point in points:\n            if not isinstance(point, (list, tuple)) or len(point) < 2:\n                continue\n            try:\n                lat = float(point[0]); lon = float(point[1])\n            except (TypeError, ValueError):\n                continue\n            if -90 <= lat <= 90 and -180 <= lon <= 180:\n                clean_points.append([round(lat, 7), round(lon, 7)])\n        if len(clean_points) < 2:\n            continue\n        route_point_budget -= len(clean_points)\n        clean_routes.append({\n            "id": _clean_text(item.get("id"), 80) or f"route-{len(clean_routes)+1}",\n            "name": name,\n            "source": _clean_text(item.get("source"), 120),\n            "notes": _clean_text(item.get("notes"), 700),\n            "points": clean_points,\n        })\n\n    if not isinstance(shelter_zones, list) or len(shelter_zones) > 200:\n        raise ValueError("Invalid shelter zones")\n    clean_shelter_zones: list[dict[str, Any]] = []\n    for item in shelter_zones:\n        if not isinstance(item, dict):\n            continue\n        name = _clean_text(item.get("name"), 160)\n        if not name:\n            continue\n        status = _clean_text(item.get("status"), 40)\n        if status not in {"safe", "check", "avoid", "unknown"}:\n            status = "unknown"\n        clean_shelter_zones.append({\n            "id": _clean_text(item.get("id"), 80) or f"zone-{len(clean_shelter_zones)+1}",\n            "name": name,\n            "status": status,\n            "occupants": _bounded_int(item.get("occupants"), 0, 0, 10000),\n            "utilities": _clean_text(item.get("utilities"), 240),\n            "last_check": _clean_datetime(item.get("last_check")),\n            "notes": _clean_text(item.get("notes"), 1200),\n        })\n\n    if not isinstance(water_batches, list) or len(water_batches) > 1000:\n        raise ValueError("Invalid water batches")\n    clean_water_batches: list[dict[str, Any]] = []\n    for item in water_batches:\n        if not isinstance(item, dict):\n            continue\n        source = _clean_text(item.get("source"), 180)\n        if not source:\n            continue\n        status = _clean_text(item.get("status"), 40)\n        if status not in {"untreated", "processing", "ready", "discarded"}:\n            status = "untreated"\n        clean_water_batches.append({\n            "id": _clean_text(item.get("id"), 80) or f"water-{len(clean_water_batches)+1}",\n            "time": _clean_datetime(item.get("time")),\n            "source": source,\n            "volume_l": _bounded_float(item.get("volume_l"), 0, 0, 1_000_000),\n            "method": _clean_text(item.get("method"), 180),\n            "status": status,\n            "container": _clean_text(item.get("container"), 160),\n            "notes": _clean_text(item.get("notes"), 1200),\n        })\n\n    if not isinstance(recovery_items, list) or len(recovery_items) > 2000:\n        raise ValueError("Invalid recovery items")\n    clean_recovery_items: list[dict[str, Any]] = []\n    for item in recovery_items:\n        if not isinstance(item, dict):\n            continue\n        area = _clean_text(item.get("area"), 180)\n        if not area:\n            continue\n        severity = _clean_text(item.get("severity"), 40)\n        if severity not in {"minor", "moderate", "major", "critical", "unknown"}:\n            severity = "unknown"\n        status = _clean_text(item.get("status"), 40)\n        if status not in {"open", "isolated", "assigned", "resolved", "deferred"}:\n            status = "open"\n        clean_recovery_items.append({\n            "id": _clean_text(item.get("id"), 80) or f"recovery-{len(clean_recovery_items)+1}",\n            "time": _clean_datetime(item.get("time")),\n            "area": area,\n            "severity": severity,\n            "status": status,\n            "owner": _clean_text(item.get("owner"), 140),\n            "action": _clean_text(item.get("action"), 700),\n            "notes": _clean_text(item.get("notes"), 1600),\n        })\n\n    if not isinstance(skill_matrix, list) or len(skill_matrix) > 1000:\n        raise ValueError("Invalid skill matrix")\n    clean_skill_matrix: list[dict[str, Any]] = []\n    for item in skill_matrix:\n        if not isinstance(item, dict):\n            continue\n        person = _clean_text(item.get("person"), 140)\n        skill = _clean_text(item.get("skill"), 180)\n        if not person or not skill:\n            continue\n        level = _clean_text(item.get("level"), 40)\n        if level not in {"new", "practiced", "confident", "trainer"}:\n            level = "new"\n        clean_skill_matrix.append({\n            "id": _clean_text(item.get("id"), 80) or f"skill-{len(clean_skill_matrix)+1}",\n            "person": person,\n            "skill": skill,\n            "level": level,\n            "last_practiced": _clean_date(item.get("last_practiced")),\n            "next_practice": _clean_date(item.get("next_practice")),\n            "notes": _clean_text(item.get("notes"), 1000),\n        })\n\n    if not isinstance(decision_board, list) or len(decision_board) > 1500:\n        raise ValueError("Invalid decision board")\n    clean_decision_board: list[dict[str, Any]] = []\n    for item in decision_board:\n        if not isinstance(item, dict):\n            continue\n        issue = _clean_text(item.get("issue"), 240)\n        decision = _clean_text(item.get("decision"), 700)\n        if not issue or not decision:\n            continue\n        status = _clean_text(item.get("status"), 40)\n        if status not in {"active", "review", "closed", "superseded"}:\n            status = "active"\n        clean_decision_board.append({\n            "id": _clean_text(item.get("id"), 80) or f"decision-{len(clean_decision_board)+1}",\n            "time": _clean_datetime(item.get("time")),\n            "issue": issue,\n            "decision": decision,\n            "reason": _clean_text(item.get("reason"), 1200),\n            "owner": _clean_text(item.get("owner"), 140),\n            "next_review": _clean_datetime(item.get("next_review")),\n            "status": status,\n        })\n\n    if not isinstance(food_lots, list) or len(food_lots) > 2000:\n        raise ValueError("Invalid food lots")\n    clean_food_lots: list[dict[str, Any]] = []\n    for item in food_lots:\n        if not isinstance(item, dict):\n            continue\n        name = _clean_text(item.get("name"), 180)\n        if not name:\n            continue\n        status = _clean_text(item.get("status"), 40)\n        if status not in {"sealed", "open", "use-first", "isolated", "discarded"}:\n            status = "sealed"\n        clean_food_lots.append({\n            "id": _clean_text(item.get("id"), 80) or f"food-{len(clean_food_lots)+1}",\n            "name": name,\n            "category": _clean_text(item.get("category"), 120),\n            "qty": _bounded_float(item.get("qty"), 0, 0, 100_000_000),\n            "unit": _clean_text(item.get("unit"), 40),\n            "kcal_total": _bounded_float(item.get("kcal_total"), 0, 0, 10_000_000_000),\n            "opened_date": _clean_date(item.get("opened_date")),\n            "best_before": _clean_date(item.get("best_before")),\n            "location": _clean_text(item.get("location"), 180),\n            "status": status,\n            "notes": _clean_text(item.get("notes"), 1200),\n        })\n\n    if not isinstance(sanitation_points, list) or len(sanitation_points) > 1000:\n        raise ValueError("Invalid sanitation points")\n    clean_sanitation_points: list[dict[str, Any]] = []\n    for item in sanitation_points:\n        if not isinstance(item, dict):\n            continue\n        name = _clean_text(item.get("name"), 180)\n        if not name:\n            continue\n        kind = _clean_text(item.get("kind"), 40)\n        if kind not in {"toilet", "handwash", "waste", "laundry", "bathing", "other"}:\n            kind = "other"\n        status = _clean_text(item.get("status"), 40)\n        if status not in {"ready", "limited", "service", "unusable"}:\n            status = "ready"\n        clean_sanitation_points.append({\n            "id": _clean_text(item.get("id"), 80) or f"sanitation-{len(clean_sanitation_points)+1}",\n            "name": name,\n            "kind": kind,\n            "status": status,\n            "capacity": _bounded_float(item.get("capacity"), 0, 0, 100_000_000),\n            "unit": _clean_text(item.get("unit"), 40),\n            "owner": _clean_text(item.get("owner"), 140),\n            "last_service": _clean_datetime(item.get("last_service")),\n            "next_service": _clean_datetime(item.get("next_service")),\n            "notes": _clean_text(item.get("notes"), 1200),\n        })\n\n    if not isinstance(power_loads, list) or len(power_loads) > 1000:\n        raise ValueError("Invalid power loads")\n    clean_power_loads: list[dict[str, Any]] = []\n    for item in power_loads:\n        if not isinstance(item, dict):\n            continue\n        name = _clean_text(item.get("name"), 180)\n        if not name:\n            continue\n        priority = _clean_text(item.get("priority"), 40)\n        if priority not in {"critical", "important", "optional"}:\n            priority = "important"\n        clean_power_loads.append({\n            "id": _clean_text(item.get("id"), 80) or f"load-{len(clean_power_loads)+1}",\n            "name": name,\n            "watts": _bounded_float(item.get("watts"), 0, 0, 10_000_000),\n            "hours_per_day": _bounded_float(item.get("hours_per_day"), 0, 0, 24),\n            "priority": priority,\n            "source": _clean_text(item.get("source"), 120),\n            "enabled": bool(item.get("enabled", True)),\n            "notes": _clean_text(item.get("notes"), 1000),\n        })\n\n    if not isinstance(comms_windows, list) or len(comms_windows) > 1000:\n        raise ValueError("Invalid communications windows")\n    clean_comms_windows: list[dict[str, Any]] = []\n    for item in comms_windows:\n        if not isinstance(item, dict):\n            continue\n        name = _clean_text(item.get("name"), 180)\n        if not name:\n            continue\n        status = _clean_text(item.get("status"), 40)\n        if status not in {"active", "paused", "missed"}:\n            status = "active"\n        clean_comms_windows.append({\n            "id": _clean_text(item.get("id"), 80) or f"comms-{len(clean_comms_windows)+1}",\n            "name": name,\n            "method": _clean_text(item.get("method"), 120),\n            "channel": _clean_text(item.get("channel"), 120),\n            "participants": _clean_text(item.get("participants"), 300),\n            "time_local": _clean_text(item.get("time_local"), 80),\n            "frequency": _clean_text(item.get("frequency"), 120),\n            "backup": _clean_text(item.get("backup"), 240),\n            "status": status,\n            "notes": _clean_text(item.get("notes"), 1000),\n        })\n\n    if not isinstance(dependents, list) or len(dependents) > 500:\n        raise ValueError("Invalid dependents")\n    clean_dependents: list[dict[str, Any]] = []\n    for item in dependents:\n        if not isinstance(item, dict):\n            continue\n        name = _clean_text(item.get("name"), 180)\n        if not name:\n            continue\n        kind = _clean_text(item.get("kind"), 40)\n        if kind not in {"child", "older-adult", "disability", "pet", "service-animal", "other"}:\n            kind = "other"\n        clean_dependents.append({\n            "id": _clean_text(item.get("id"), 80) or f"dependent-{len(clean_dependents)+1}",\n            "name": name,\n            "kind": kind,\n            "needs": _clean_text(item.get("needs"), 1600),\n            "mobility": _clean_text(item.get("mobility"), 700),\n            "communication": _clean_text(item.get("communication"), 700),\n            "caregiver": _clean_text(item.get("caregiver"), 140),\n            "backup": _clean_text(item.get("backup"), 140),\n            "supplies": _clean_text(item.get("supplies"), 1200),\n            "notes": _clean_text(item.get("notes"), 1200),\n        })\n\n    if not isinstance(expense_log, list) or len(expense_log) > 5000:\n        raise ValueError("Invalid expense log")\n    clean_expense_log: list[dict[str, Any]] = []\n    for item in expense_log:\n        if not isinstance(item, dict):\n            continue\n        description = _clean_text(item.get("description"), 240)\n        if not description:\n            continue\n        status = _clean_text(item.get("status"), 40)\n        if status not in {"recorded", "claim-ready", "submitted", "reimbursed", "not-covered"}:\n            status = "recorded"\n        clean_expense_log.append({\n            "id": _clean_text(item.get("id"), 80) or f"expense-{len(clean_expense_log)+1}",\n            "time": _clean_datetime(item.get("time")),\n            "category": _clean_text(item.get("category"), 120),\n            "description": description,\n            "amount": _bounded_float(item.get("amount"), 0, 0, 1_000_000_000),\n            "currency": _clean_text(item.get("currency"), 12),\n            "payment": _clean_text(item.get("payment"), 80),\n            "claim_ref": _clean_text(item.get("claim_ref"), 160),\n            "status": status,\n            "notes": _clean_text(item.get("notes"), 1600),\n        })\n\n    if not isinstance(knowledge_progress, list) or len(knowledge_progress) > 1000:\n        raise ValueError("Invalid knowledge progress")\n    clean_knowledge_progress: list[dict[str, Any]] = []\n    seen_knowledge: set[str] = set()\n    for item in knowledge_progress:\n        if not isinstance(item, dict):\n            continue\n        path = _clean_text(item.get("path"), 500)\n        if not path or path in seen_knowledge:\n            continue\n        status = _clean_text(item.get("status"), 24)\n        if status not in {"reviewed", "review-later"}:\n            status = "reviewed"\n        seen_knowledge.add(path)\n        clean_knowledge_progress.append({\n            "path": path,\n            "status": status,\n            "last_review": _clean_date(item.get("last_review")),\n            "notes": _clean_text(item.get("notes"), 800),\n        })\n\n    clean_settings = {"low_power": bool(settings.get("low_power", False))} if isinstance(settings, dict) else {"low_power": False}\n    updated_at = _clean_datetime(candidate.get("updated_at"))\n\n    return {\n        "favorites": clean_favorites,\n        "notes": clean_notes,\n        "checklist": clean_checklist,\n        "custom_checklist": clean_custom,\n        "profile": clean_profile,\n        "inventory": clean_inventory,\n        "contacts": clean_contacts,\n        "incident_log": clean_log,\n        "risk_flags": clean_risks,\n        "communications": clean_small_dict(communications),\n        "evacuation": clean_small_dict(evacuation),\n        "medical_card": clean_medical,\n        "medications": clean_medications,\n        "waypoints": clean_waypoints,\n        "navigation": clean_navigation,\n        "documents": clean_documents,\n        "maintenance": clean_maintenance,\n        "roles": clean_roles,\n        "drill_history": clean_drills,\n        "continuity": clean_continuity,\n        "resource_plans": clean_resource_plans,\n        "checkins": clean_checkins,\n        "vehicles": clean_vehicles,\n        "kits": clean_kits,\n        "field_logs": clean_field_logs,\n        "routes": clean_routes,\n        "shelter_zones": clean_shelter_zones,\n        "water_batches": clean_water_batches,\n        "recovery_items": clean_recovery_items,\n        "skill_matrix": clean_skill_matrix,\n        "decision_board": clean_decision_board,\n        "food_lots": clean_food_lots,\n        "sanitation_points": clean_sanitation_points,\n        "power_loads": clean_power_loads,\n        "comms_windows": clean_comms_windows,\n        "dependents": clean_dependents,\n        "expense_log": clean_expense_log,\n        "knowledge_progress": clean_knowledge_progress,\n        "settings": clean_settings,\n        "schema_version": SCHEMA_VERSION,\n        "updated_at": updated_at,\n    }\n\n\ndef save_state(candidate: Any) -> dict[str, Any]:\n    state = sanitize_state(candidate)\n    state["schema_version"] = SCHEMA_VERSION\n    state["updated_at"] = datetime.now(timezone.utc).isoformat(timespec="seconds")\n    STATE_DIR.mkdir(parents=True, exist_ok=True)\n    temp = STATE_FILE.with_suffix(".tmp")\n    temp.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")\n    if STATE_FILE.is_file():\n        try:\n            shutil.copy2(STATE_FILE, STATE_PREVIOUS_FILE)\n        except OSError:\n            pass\n    temp.replace(STATE_FILE)\n    return state\n\n\ndef restore_previous_state() -> dict[str, Any]:\n    if not STATE_PREVIOUS_FILE.is_file():\n        raise ValueError("No previous state backup is available")\n    return save_state(safe_json_read(STATE_PREVIOUS_FILE, {}))\n\n\ndef sha256_file(path: Path) -> str:\n    digest = hashlib.sha256()\n    with path.open("rb") as stream:\n        for chunk in iter(lambda: stream.read(1024 * 1024), b""):\n            digest.update(chunk)\n    return digest.hexdigest()\n\n\ndef directory_size(path: Path) -> int:\n    total = 0\n    if not path.exists():\n        return 0\n    for item in path.rglob("*"):\n        try:\n            if item.is_file():\n                total += item.stat().st_size\n        except OSError:\n            pass\n    return total\n\n\ndef human_size(value: int) -> str:\n    size = float(value)\n    for unit in ("B", "KB", "MB", "GB", "TB"):\n        if size < 1024 or unit == "TB":\n            return f"{size:.1f} {unit}" if unit != "B" else f"{int(size)} B"\n        size /= 1024\n    return f"{size:.1f} TB"\n\n\ndef compact_item(item: dict[str, Any]) -> dict[str, Any]:\n    record = item["record"]\n    return {\n        "id": record.get("id", ""),\n        "title": record.get("title", ""),\n        "category": record.get("category", ""),\n        "subcategory": record.get("subcategory", ""),\n        "summary": record.get("summary", ""),\n        "urgency": record.get("urgency", ""),\n        "priority": record.get("priority", ""),\n        "tags": record.get("tags", []),\n        "path": item.get("relative_path", ""),\n    }\n\n\ndef full_item(item: dict[str, Any]) -> dict[str, Any]:\n    output = dict(item["record"])\n    output["_path"] = item.get("relative_path", "")\n    return output\n\n\ndef get_language(query: dict[str, list[str]]) -> str:\n    language = query.get("lang", ["en"])[0]\n    return language if language in CORE.LANGUAGES else "en"\n\n\ndef load_language(language: str) -> list[dict[str, Any]]:\n    return DATABASE.load(language)\n\n\ndef find_exact_record(language: str, record_id: str) -> dict[str, Any] | None:\n    matches = DATABASE.find_by_id(language, record_id)\n    for item in matches:\n        if str(item["record"].get("id", "")) == record_id:\n            return item\n    return None\n\n\ndef library_files() -> list[dict[str, Any]]:\n    if not LIBRARY_ROOT.is_dir():\n        return []\n    result: list[dict[str, Any]] = []\n    for path in sorted(LIBRARY_ROOT.rglob("*"), key=lambda p: str(p).casefold()):\n        if path.is_symlink() or not path.is_file():\n            continue\n        try:\n            stat = path.stat()\n        except OSError:\n            continue\n        rel = path.relative_to(LIBRARY_ROOT).as_posix()\n        suffix = path.suffix.casefold()\n        result.append({\n            "path": rel,\n            "name": path.name,\n            "extension": suffix,\n            "size": stat.st_size,\n            "size_human": human_size(stat.st_size),\n            "kind": "Kiwix ZIM" if suffix == ".zim" else "Offline map" if suffix == ".pmtiles" else "Document",\n            "readable": suffix in LIBRARY_TEXT_SUFFIXES,\n            "kiwix": suffix == ".zim",\n        })\n    return result\n\n\ndef safe_library_path(raw: str) -> Path:\n    candidate = (LIBRARY_ROOT / unquote(raw)).resolve()\n    root = LIBRARY_ROOT.resolve()\n    if candidate != root and root not in candidate.parents:\n        raise ValueError("Invalid library path")\n    return candidate\n\n\ndef read_text_prefix(path: Path, max_bytes: int) -> tuple[str, bool]:\n    """Read a bounded UTF-8 prefix for the built-in viewer/search index."""\n    with path.open("rb") as stream:\n        raw = stream.read(max_bytes + 1)\n    truncated = len(raw) > max_bytes\n    if truncated:\n        raw = raw[:max_bytes]\n    return raw.decode("utf-8", errors="replace"), truncated\n\n\ndef search_library_text(phrase: str, limit: int = 60, prefix: str = "") -> list[dict[str, Any]]:\n    """Search safe text-readable Library files without indexing or network access."""\n    query = " ".join(str(phrase).split())[:160]\n    if len(query) < 2:\n        return []\n    q_lower = query.lower()\n    terms = [part for part in q_lower.split() if len(part) >= 2][:12]\n    safe_prefix = str(prefix or "").replace("\\\\", "/").strip("/")[:220]\n    if ".." in safe_prefix.split("/"):\n        return []\n    results: list[dict[str, Any]] = []\n    for item in library_files():\n        if safe_prefix and not str(item.get("path", "")).startswith(safe_prefix + "/"):\n            continue\n        if not item.get("readable"):\n            continue\n        try:\n            path = safe_library_path(str(item["path"]))\n            text, truncated = read_text_prefix(path, LIBRARY_SEARCH_MAX_BYTES)\n        except (OSError, ValueError):\n            continue\n        normalized = " ".join(text.split())\n        hay = normalized.lower()\n        pos = hay.find(q_lower)\n        exact = pos >= 0\n        if not exact:\n            if not terms or not all(term in hay for term in terms):\n                continue\n            positions = [hay.find(term) for term in terms if hay.find(term) >= 0]\n            pos = min(positions) if positions else 0\n        start = max(0, pos - 110)\n        end = min(len(normalized), pos + max(len(query), 1) + 220)\n        snippet = normalized[start:end]\n        if start:\n            snippet = "…" + snippet\n        if end < len(normalized) or truncated:\n            snippet += "…"\n        results.append({\n            "path": item["path"],\n            "name": item["name"],\n            "kind": item["kind"],\n            "size_human": item["size_human"],\n            "snippet": snippet,\n            "exact_phrase": exact,\n            "search_truncated": truncated,\n        })\n    results.sort(key=lambda row: (not row["exact_phrase"], str(row["name"]).casefold()))\n    return results[:max(1, min(250, limit))]\n\n\ndef kiwix_executable() -> str | None:\n    return shutil.which("kiwix-serve")\n\n\ndef start_kiwix(path: Path) -> dict[str, Any]:\n    global _KIWIX_PROCESS\n    executable = kiwix_executable()\n    if not executable:\n        return {\n            "ok": False,\n            "error": "kiwix-serve is not installed. Open the ZIM with the Kiwix app, or install Kiwix tools on this device.",\n        }\n    if path.suffix.casefold() != ".zim" or not path.is_file():\n        return {"ok": False, "error": "The selected file is not a valid local ZIM file."}\n\n    with _KIWIX_LOCK:\n        if _KIWIX_PROCESS is not None and _KIWIX_PROCESS.poll() is None:\n            return {"ok": True, "url": f"http://127.0.0.1:{KIWIX_PORT}", "already_running": True}\n        try:\n            _KIWIX_PROCESS = subprocess.Popen(\n                [executable, "--port", str(KIWIX_PORT), str(path)],\n                stdout=subprocess.DEVNULL,\n                stderr=subprocess.DEVNULL,\n            )\n        except OSError as error:\n            return {"ok": False, "error": str(error)}\n    return {"ok": True, "url": f"http://127.0.0.1:{KIWIX_PORT}", "already_running": False}\n\n\nclass Handler(BaseHTTPRequestHandler):\n    server_version = "OfflineSurvivalCommandCenter"\n    sys_version = ""\n\n    def log_message(self, format: str, *args: Any) -> None:\n        # Local request log only; nothing leaves the device.\n        if getattr(self.server, "quiet", False):\n            return\n        super().log_message(format, *args)\n\n    def send_json(self, payload: Any, status: int = 200) -> None:\n        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")\n        self.send_response(status)\n        self.send_header("Content-Type", "application/json; charset=utf-8")\n        self.send_header("Content-Length", str(len(data)))\n        self.send_header("Cache-Control", "no-store")\n        self.send_header("X-Content-Type-Options", "nosniff")\n        self.send_header("X-Frame-Options", "DENY")\n        self.send_header("Referrer-Policy", "no-referrer")\n        self.send_header("Permissions-Policy", "geolocation=(self), camera=(), microphone=(), payment=(), usb=()")\n        self.send_header("Content-Security-Policy", "default-src \'self\'; style-src \'self\' \'unsafe-inline\'; script-src \'self\' \'unsafe-inline\'; img-src \'self\' data:; connect-src \'self\'; object-src \'none\'; base-uri \'none\'; frame-ancestors \'none\'")\n        self.end_headers()\n        self.wfile.write(data)\n\n    def send_file(self, path: Path, cache: bool = False, untrusted: bool = False) -> None:\n        if not path.is_file():\n            self.send_error(HTTPStatus.NOT_FOUND)\n            return\n        try:\n            size = path.stat().st_size\n            stream = path.open("rb")\n        except OSError:\n            self.send_error(HTTPStatus.INTERNAL_SERVER_ERROR)\n            return\n        content_type = mimetypes.guess_type(str(path))[0] or "application/octet-stream"\n        self.send_response(HTTPStatus.OK)\n        self.send_header("Content-Type", content_type)\n        self.send_header("Content-Length", str(size))\n        self.send_header("Cache-Control", "public, max-age=3600" if cache else "no-store")\n        self.send_header("X-Content-Type-Options", "nosniff")\n        self.send_header("X-Frame-Options", "DENY")\n        self.send_header("Referrer-Policy", "no-referrer")\n        self.send_header("Permissions-Policy", "geolocation=(self), camera=(), microphone=(), payment=(), usb=()")\n        if untrusted:\n            self.send_header("Content-Disposition", f"attachment; filename*=UTF-8\'\'{quote(path.name)}")\n            self.send_header("Content-Security-Policy", "default-src \'none\'; sandbox; frame-ancestors \'none\'")\n        else:\n            self.send_header("Content-Security-Policy", "default-src \'self\'; style-src \'self\' \'unsafe-inline\'; script-src \'self\' \'unsafe-inline\'; img-src \'self\' data:; connect-src \'self\'; object-src \'none\'; base-uri \'none\'; frame-ancestors \'none\'")\n        self.end_headers()\n        with stream:\n            while True:\n                chunk = stream.read(1024 * 1024)\n                if not chunk:\n                    break\n                try:\n                    self.wfile.write(chunk)\n                except (BrokenPipeError, ConnectionResetError):\n                    return\n\n    def read_json_body(self) -> Any:\n        raw_length = self.headers.get("Content-Length", "0")\n        try:\n            length = int(raw_length)\n        except ValueError as error:\n            raise ValueError("Invalid Content-Length") from error\n        if length < 0 or length > MAX_POST_BYTES:\n            raise ValueError("Request body too large")\n        raw = self.rfile.read(length)\n        if not raw:\n            return {}\n        try:\n            return json.loads(raw.decode("utf-8"))\n        except (UnicodeError, json.JSONDecodeError) as error:\n            raise ValueError("Invalid JSON body") from error\n\n    def do_GET(self) -> None:  # noqa: N802\n        parsed = urlparse(self.path)\n        path = parsed.path\n        query = parse_qs(parsed.query)\n        try:\n            if not self.host_header_allowed():\n                self.send_json({"error": "Host header rejected"}, HTTPStatus.MISDIRECTED_REQUEST)\n                return\n            if path == "/":\n                self.send_file(INDEX_FILE)\n                return\n            if path == "/reader.html":\n                self.send_file(PROJECT_ROOT / "Offline Survival Reader.html")\n                return\n            static_assets = {\n                "/styles.css": WEB_ROOT / "styles.css",\n                "/app.js": WEB_ROOT / "app.js",\n                "/field-operations.js": WEB_ROOT / "field-operations.js",\n                "/continuity-operations.js": WEB_ROOT / "continuity-operations.js",\n                "/knowledge-atlas.js": WEB_ROOT / "knowledge-atlas.js",\n                "/phone-test.html": WEB_ROOT / "phone-test.html",\n                "/phone-test.js": WEB_ROOT / "phone-test.js",\n                "/manifest.webmanifest": WEB_ROOT / "manifest.webmanifest",\n                "/sw.js": WEB_ROOT / "sw.js",\n            }\n            if path in static_assets:\n                self.send_file(static_assets[path], cache=path != "/sw.js")\n                return\n            if path == "/api/meta":\n                self.api_meta()\n                return\n            if path == "/api/search":\n                self.api_search(query)\n                return\n            if path == "/api/categories":\n                self.api_categories(query)\n                return\n            if path == "/api/category":\n                self.api_category(query)\n                return\n            if path == "/api/record":\n                self.api_record(query)\n                return\n            if path == "/api/essentials":\n                self.api_essentials(query)\n                return\n            if path == "/api/food":\n                self.api_food(query)\n                return\n            if path == "/api/random":\n                self.api_random(query)\n                return\n            if path == "/api/scenario":\n                self.api_scenario(query)\n                return\n            if path == "/api/state":\n                self.send_json(load_state())\n                return\n            if path == "/api/library":\n                self.send_json({"files": library_files(), "root": str(LIBRARY_ROOT), "kiwix_available": bool(kiwix_executable())})\n                return\n            if path == "/api/library/search":\n                self.api_library_search(query)\n                return\n            if path == "/api/library/text":\n                self.api_library_text(query)\n                return\n            if path == "/api/library/hash":\n                self.api_library_hash(query)\n                return\n            if path == "/api/diagnostics":\n                self.api_diagnostics()\n                return\n            if path == "/api/state/previous":\n                self.send_json({"available": STATE_PREVIOUS_FILE.is_file()})\n                return\n            if path.startswith("/library/"):\n                self.api_library_file(path[len("/library/"):])\n                return\n            self.send_error(HTTPStatus.NOT_FOUND)\n        except FileNotFoundError as error:\n            self.send_json({"error": f"Database folder missing: {error}"}, 500)\n        except (RuntimeError, ValueError, OSError) as error:\n            self.send_json({"error": str(error)}, 400)\n        except Exception as error:\n            self.send_json({"error": f"Unexpected local server error: {error}"}, 500)\n\n\n    def host_header_allowed(self) -> bool:\n        allowed = getattr(self.server, "allowed_hosts", None)\n        if allowed is None:\n            return True\n        host = self.headers.get("Host", "").strip().casefold()\n        return host in allowed\n\n    def same_origin_request(self) -> bool:\n        """Reject cross-origin browser writes while allowing non-browser local clients."""\n        origin = self.headers.get("Origin")\n        if not origin:\n            return True\n        try:\n            parsed = urlparse(origin)\n        except ValueError:\n            return False\n        if parsed.scheme not in {"http", "https"} or not parsed.netloc:\n            return False\n        host = self.headers.get("Host", "").strip().casefold()\n        return bool(host) and parsed.netloc.casefold() == host\n\n    def do_POST(self) -> None:  # noqa: N802\n        parsed = urlparse(self.path)\n        try:\n            if not self.host_header_allowed():\n                self.send_json({"error": "Host header rejected"}, HTTPStatus.MISDIRECTED_REQUEST)\n                return\n            if not self.same_origin_request():\n                self.send_json({"error": "Cross-origin state-changing request rejected"}, HTTPStatus.FORBIDDEN)\n                return\n            if parsed.path == "/api/state":\n                body = self.read_json_body()\n                self.send_json(save_state(body))\n                return\n            if parsed.path == "/api/state/restore-previous":\n                self.send_json(restore_previous_state())\n                return\n            if parsed.path == "/api/kiwix/start":\n                body = self.read_json_body()\n                raw_path = str(body.get("path", "")) if isinstance(body, dict) else ""\n                path = safe_library_path(raw_path)\n                self.send_json(start_kiwix(path))\n                return\n            self.send_error(HTTPStatus.NOT_FOUND)\n        except (ValueError, OSError) as error:\n            self.send_json({"error": str(error)}, 400)\n        except Exception as error:\n            self.send_json({"error": f"Unexpected local server error: {error}"}, 500)\n\n    def api_meta(self) -> None:\n        report = integrity_report_cached()\n        usage = shutil.disk_usage(PROJECT_ROOT)\n        files = library_files()\n        project_size = directory_size(PROJECT_ROOT)\n        library_size = sum(item["size"] for item in files)\n        essentials_count = sum(1 for item in load_language("en") if str(item["record"].get("id", "")).startswith("verified-essential-"))\n        food_count = sum(1 for item in load_language("en") if str(item["record"].get("id", "")).startswith("verified-food-"))\n        self.send_json({\n            "app": "Offline Survival Project",\n            "mode": "Ultimate Operations Command Center",\n            "state_schema_version": SCHEMA_VERSION,\n            "report": report,\n            "verified_essentials": essentials_count,\n            "verified_food_guides": food_count,\n            "state": load_state(),\n            "system": {\n                "platform": platform.platform(),\n                "python": platform.python_version(),\n                "project_size": project_size,\n                "project_size_human": human_size(project_size),\n                "disk_free": usage.free,\n                "disk_free_human": human_size(usage.free),\n                "library_files": len(files),\n                "library_size": library_size,\n                "library_size_human": human_size(library_size),\n                "kiwix_available": bool(kiwix_executable()),\n            },\n            "scenarios": list(SCENARIOS),\n        })\n\n    def api_search(self, query: dict[str, list[str]]) -> None:\n        language = get_language(query)\n        phrase = query.get("q", [""])[0].strip()\n        try:\n            limit = max(1, min(200, int(query.get("limit", ["80"])[0])))\n        except ValueError:\n            limit = 80\n        results = DATABASE.search(language, phrase) if phrase else []\n        self.send_json({"query": phrase, "count": len(results), "results": [compact_item(item) for item in results[:limit]]})\n\n    def api_categories(self, query: dict[str, list[str]]) -> None:\n        language = get_language(query)\n        uncategorized = "Uncategorized" if language == "en" else "Χωρίς κατηγορία"\n        categories = DATABASE.categories(language, uncategorized)\n        rows = [{"name": name, "count": len(items)} for name, items in categories.items()]\n        self.send_json({"count": len(rows), "categories": rows})\n\n    def api_category(self, query: dict[str, list[str]]) -> None:\n        language = get_language(query)\n        name = query.get("name", [""])[0]\n        uncategorized = "Uncategorized" if language == "en" else "Χωρίς κατηγορία"\n        categories = DATABASE.categories(language, uncategorized)\n        items = categories.get(name, [])\n        self.send_json({"name": name, "count": len(items), "results": [compact_item(item) for item in items]})\n\n    def api_record(self, query: dict[str, list[str]]) -> None:\n        language = get_language(query)\n        record_id = query.get("id", [""])[0].strip()\n        item = find_exact_record(language, record_id)\n        if item is None:\n            self.send_json({"error": "Record not found"}, 404)\n            return\n        self.send_json(full_item(item))\n\n    def api_essentials(self, query: dict[str, list[str]]) -> None:\n        language = get_language(query)\n        rows = [item for item in load_language(language) if str(item["record"].get("id", "")).startswith("verified-essential-")]\n        self.send_json({"count": len(rows), "results": [compact_item(item) for item in rows]})\n\n    def api_food(self, query: dict[str, list[str]]) -> None:\n        language = get_language(query)\n        rows = [item for item in load_language(language) if str(item["record"].get("id", "")).startswith("verified-food-")]\n        self.send_json({"count": len(rows), "results": [compact_item(item) for item in rows]})\n\n    def api_random(self, query: dict[str, list[str]]) -> None:\n        language = get_language(query)\n        rows = load_language(language)\n        if not rows:\n            self.send_json({"error": "Database is empty"}, 404)\n            return\n        self.send_json(full_item(random.choice(rows)))\n\n    def api_scenario(self, query: dict[str, list[str]]) -> None:\n        language = get_language(query)\n        key = query.get("key", [""])[0]\n        scenario = SCENARIOS.get(key)\n        if scenario is None:\n            self.send_json({"error": "Unknown scenario"}, 404)\n            return\n        phrase = scenario[language]\n        results = DATABASE.search(language, phrase)\n        # Search terms may be broad; reward curated emergency essentials.\n        results.sort(key=lambda item: (not str(item["record"].get("id", "")).startswith("verified-essential-"), CORE.normalize(item["record"].get("title", ""))))\n        self.send_json({"key": key, "query": phrase, "count": len(results), "results": [compact_item(item) for item in results[:60]]})\n\n    def api_library_search(self, query: dict[str, list[str]]) -> None:\n        phrase = query.get("q", [""])[0].strip()\n        try:\n            limit = max(1, min(250, int(query.get("limit", ["60"])[0])))\n        except ValueError:\n            limit = 60\n        prefix = query.get("prefix", [""])[0].strip().replace("\\\\", "/")[:220]\n        if ".." in prefix.split("/"):\n            raise ValueError("Invalid Library search prefix")\n        rows = search_library_text(phrase, limit=limit, prefix=prefix)\n        self.send_json({"query": phrase[:160], "prefix": prefix, "count": len(rows), "results": rows})\n\n    def api_library_text(self, query: dict[str, list[str]]) -> None:\n        raw = query.get("path", [""])[0]\n        path = safe_library_path(raw)\n        if path.suffix.casefold() not in LIBRARY_TEXT_SUFFIXES:\n            raise ValueError("This library file is not text-readable in the built-in viewer")\n        if not path.is_file():\n            self.send_json({"error": "Library file not found"}, 404)\n            return\n        text = path.read_text(encoding="utf-8", errors="replace")\n        if len(text) > 2_000_000:\n            text = text[:2_000_000] + "\\n\\n[Viewer truncated this file at 2 MB.]"\n        self.send_json({"path": raw, "text": text})\n\n    def api_library_hash(self, query: dict[str, list[str]]) -> None:\n        raw = query.get("path", [""])[0]\n        path = safe_library_path(raw)\n        if not path.is_file():\n            self.send_json({"error": "Library file not found"}, 404)\n            return\n        self.send_json({"path": raw, "sha256": sha256_file(path), "size": path.stat().st_size})\n\n    def api_diagnostics(self) -> None:\n        checks: list[dict[str, Any]] = []\n        def add(name: str, ok: bool, detail: str = "") -> None:\n            checks.append({"name": name, "ok": bool(ok), "detail": detail})\n        add("web_index", INDEX_FILE.is_file(), str(INDEX_FILE))\n        add("web_styles", (WEB_ROOT / "styles.css").is_file(), str(WEB_ROOT / "styles.css"))\n        add("web_script", (WEB_ROOT / "app.js").is_file(), str(WEB_ROOT / "app.js"))\n        add("web_field_operations_script", (WEB_ROOT / "field-operations.js").is_file(), str(WEB_ROOT / "field-operations.js"))\n        add("web_continuity_operations_script", (WEB_ROOT / "continuity-operations.js").is_file(), str(WEB_ROOT / "continuity-operations.js"))\n        add("web_knowledge_atlas_script", (WEB_ROOT / "knowledge-atlas.js").is_file(), str(WEB_ROOT / "knowledge-atlas.js"))\n        add("phone_browser_diagnostics", (WEB_ROOT / "phone-test.html").is_file() and (WEB_ROOT / "phone-test.js").is_file(), str(WEB_ROOT / "phone-test.html"))\n        add("standalone_reader", (PROJECT_ROOT / "Offline Survival Reader.html").is_file(), str(PROJECT_ROOT / "Offline Survival Reader.html"))\n        for code in ("en", "el"):\n            root = DATABASE.language_root(code)\n            add(f"database_{code}", root.is_dir(), str(root))\n        try:\n            STATE_DIR.mkdir(parents=True, exist_ok=True)\n            probe = STATE_DIR / ".write-test"\n            probe.write_text("ok", encoding="utf-8")\n            probe.unlink(missing_ok=True)\n            add("state_writable", True, str(STATE_DIR))\n        except OSError as error:\n            add("state_writable", False, str(error))\n        add("library_root", LIBRARY_ROOT.is_dir(), str(LIBRARY_ROOT))\n        try:\n            report = integrity_report_cached()\n            add("database_integrity", bool(report.get("ok")), "validator report")\n        except Exception as error:\n            add("database_integrity", False, str(error))\n        self.send_json({"ok": all(x["ok"] for x in checks), "checks": checks})\n\n    def api_library_file(self, raw: str) -> None:\n        path = safe_library_path(raw)\n        self.send_file(path, cache=False, untrusted=True)\n\n\ndef open_browser_later(url: str) -> None:\n    """Delegate URL opening to the OS-installed/default browser.\n\n    On Android/Termux this intentionally uses Android URL intents rather than\n    selecting, embedding, or automating any browser engine. Desktop fallbacks\n    also use the operating system\'s default URL opener.\n    """\n    time.sleep(0.6)\n    candidates: list[list[str]] = []\n    opener = shutil.which("termux-open-url")\n    if opener:\n        candidates.append([opener, url])\n    am = shutil.which("am")\n    if not am and Path("/system/bin/am").is_file():\n        am = "/system/bin/am"\n    if am:\n        candidates.append([am, "start", "-a", "android.intent.action.VIEW", "-d", url])\n    xdg = shutil.which("xdg-open")\n    if xdg:\n        candidates.append([xdg, url])\n    mac_open = shutil.which("open")\n    if mac_open:\n        candidates.append([mac_open, url])\n\n    for command in candidates:\n        try:\n            subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)\n            return\n        except OSError:\n            continue\n    print(f"Could not invoke the system browser automatically. Open this URL in the installed browser: {url}")\n\n\ndef main(argv=None) -> int:\n    parser = argparse.ArgumentParser(description="Run the Offline Survival local Command Center.")\n    parser.add_argument("--host", default="127.0.0.1", help="Bind address. Default is localhost only.")\n    parser.add_argument("--port", type=int, default=DEFAULT_PORT, help=f"HTTP port. Default: {DEFAULT_PORT}")\n    parser.add_argument("--no-browser", action="store_true", help="Do not ask the operating system to open its installed/default browser.")\n    parser.add_argument("--phone-test", action="store_true", help="Open on-device diagnostics in the installed/default phone browser.")\n    parser.add_argument("--reader", action="store_true", help="Open the standalone bilingual Knowledge Reader in the installed/default browser.")\n    parser.add_argument("--quiet", action="store_true", help="Suppress local request logging.")\n    args = parser.parse_args(argv)\n\n    if not INDEX_FILE.is_file():\n        print(f"Missing web interface: {INDEX_FILE}", file=sys.stderr)\n        return 2\n    if not (1 <= args.port <= 65535):\n        print("Port must be between 1 and 65535.", file=sys.stderr)\n        return 2\n\n    try:\n        server = ThreadingHTTPServer((args.host, args.port), Handler)\n    except OSError as error:\n        print(f"Could not start local Command Center: {error}", file=sys.stderr)\n        return 2\n    server.quiet = bool(args.quiet)  # type: ignore[attr-defined]\n    if args.host in {"127.0.0.1", "localhost", "::1"}:\n        port_text = str(args.port)\n        server.allowed_hosts = {  # type: ignore[attr-defined]\n            "127.0.0.1", f"127.0.0.1:{port_text}",\n            "localhost", f"localhost:{port_text}",\n            "[::1]", f"[::1]:{port_text}",\n        }\n    elif args.host not in {"0.0.0.0", "::"}:\n        port_text = str(args.port)\n        server.allowed_hosts = {args.host.casefold(), f"{args.host.casefold()}:{port_text}"}  # type: ignore[attr-defined]\n    else:\n        # Wildcard/LAN mode is an explicit advanced choice; hostname policy is left to the surrounding network/host.\n        server.allowed_hosts = None  # type: ignore[attr-defined]\n\n    display_host = "127.0.0.1" if args.host in {"0.0.0.0", "::"} else args.host\n    base_url = f"http://{display_host}:{args.port}/"\n    suffix = "phone-test.html" if args.phone_test else ("reader.html" if args.reader else "")\n    url = base_url + suffix\n    print("=" * 72)\n    print("Offline Survival Project — Local Command Center")\n    print("=" * 72)\n    print(f"Open: {url}")\n    if args.phone_test:\n        print("Phone diagnostics: run inside the browser Android actually opens. No browser engine is selected or automated by this project.")\n    print("Offline by design. No cloud account, telemetry, Docker, or database server required.")\n    if args.host not in {"127.0.0.1", "localhost", "::1"}:\n        print("WARNING: You chose a non-localhost bind address. Other devices on the network may be able to connect.")\n    print("Press Ctrl+C to stop.")\n\n    if not args.no_browser:\n        threading.Thread(target=open_browser_later, args=(url,), daemon=True).start()\n\n    try:\n        server.serve_forever(poll_interval=0.3)\n    except KeyboardInterrupt:\n        print("\\nStopping Command Center...")\n    finally:\n        server.server_close()\n        global _KIWIX_PROCESS\n        with _KIWIX_LOCK:\n            if _KIWIX_PROCESS is not None and _KIWIX_PROCESS.poll() is None:\n                _KIWIX_PROCESS.terminate()\n    return 0\n\n\n'


def _exec_embedded(source: str, label: str, fake_path: Path) -> dict[str, Any]:
    """Execute a bundled maintenance component in an isolated module namespace."""
    import types
    module_name = f"_offline_survival_{label}"
    module = types.ModuleType(module_name)
    module.__file__ = str(fake_path)
    module.__package__ = None
    sys.modules[module_name] = module
    exec(compile(source, f"<embedded:{label}>", "exec"), module.__dict__, module.__dict__)
    return module.__dict__


def run_embedded_tool(name: str) -> int:
    source = _EMBEDDED_TOOL_SOURCES.get(name)
    if source is None:
        print(f"Unknown integrated tool: {name}", file=sys.stderr)
        return 2
    namespace = _exec_embedded(source, name, PROJECT_ROOT / "tools" / f"{name}.embedded")
    entry = namespace.get("main")
    if not callable(entry):
        print(f"Integrated tool has no entry point: {name}", file=sys.stderr)
        return 2
    previous_argv = sys.argv[:]
    try:
        sys.argv = [str(PROJECT_ROOT / "Offline Survival.py")]
        try:
            result = entry()
        except SystemExit as exc:
            result = exc.code
    finally:
        sys.argv = previous_argv
    return int(result or 0)


def run_local_command_center(argv: list[str] | None = None) -> int:
    """Run the bundled localhost server from this single Python file."""
    namespace = _exec_embedded(_EMBEDDED_WEB_SOURCE, "local_web", PROJECT_ROOT / "Offline Survival.py")
    entry = namespace.get("main")
    if not callable(entry):
        print("The integrated local Command Center could not start.", file=sys.stderr)
        return 2
    return int(entry(list(argv or [])) or 0)


def _phone_assets_test() -> tuple[bool, str]:
    """Static checks for the Android/default-browser launcher and diagnostics assets."""
    required = [
        PROJECT_ROOT / "web" / "phone-test.html",
        PROJECT_ROOT / "web" / "phone-test.js",
        PROJECT_ROOT / "start-phone-browser.sh",
        PROJECT_ROOT / "phone-browser-diagnostics.sh",
    ]
    missing = [str(p.relative_to(PROJECT_ROOT)) for p in required if not p.is_file()]
    shell = "\n".join(p.read_text(encoding="utf-8", errors="replace") for p in required if p.suffix == ".sh" and p.is_file())
    engine_neutral = "termux-open-url" in _EMBEDDED_WEB_SOURCE and "android.intent.action.VIEW" in _EMBEDDED_WEB_SOURCE
    ok = not missing and engine_neutral and "Offline Survival.py" in shell
    detail = "installed/default-browser path present" if ok else f"missing={missing}, engine_neutral={engine_neutral}"
    return ok, detail


def _standalone_reader_test() -> int:
    """Validate the self-contained reader without a separate Python helper."""
    import tempfile
    reader = PROJECT_ROOT / "Offline Survival Reader.html"
    checks: list[tuple[str, bool, str]] = []
    def ck(name: str, ok: bool, detail: str = "") -> None:
        checks.append((name, bool(ok), detail))
        print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f": {detail}" if detail else ""))
    if not reader.is_file():
        ck("reader-file", False, str(reader))
        return 1
    text = reader.read_text(encoding="utf-8")
    ck("reader-file", len(text) > 100000, f"{reader.stat().st_size} bytes")
    match = re.search(r'<script>const CHAPTERS=(\[.*?\]);</script>', text, re.S)
    data: list[dict[str, Any]] = []
    try:
        data = json.loads(match.group(1)) if match else []
        ck("embedded-json", bool(match), f"{len(data)} chapters")
    except Exception as exc:
        ck("embedded-json", False, str(exc))
    ids = [item.get("id") for item in data]
    ck("chapter-sequence", ids == list(range(1, 221)), f"{ids[:3]}...{ids[-3:] if ids else []}")
    ck("bilingual-chapters", all(item.get("en", {}).get("title") and item.get("en", {}).get("body") and item.get("el", {}).get("title") and item.get("el", {}).get("body") for item in data))
    ck("no-external-assets", '<script src=' not in text and '<link rel="stylesheet"' not in text)
    ck("no-runtime-network", not re.search(r'\b(?:fetch|XMLHttpRequest|WebSocket)\s*\(', text))
    ck("mobile-viewport", "width=device-width" in text and "@media(max-width:800px)" in text)
    ck("local-search", "function filtered()" in text and 'id="q"' in text)
    ck("local-progress", "osp-reader-fav" in text and "osp-reader-reviewed" in text and "localStorage" in text)
    ck("print-support", "$('print').onclick=()=>print()" in text)
    ck("bilingual-ui", "Μονοαρχείος οδηγός επιβίωσης" in text and "Single-file survival library" in text)
    node = shutil.which("node")
    if node:
        scripts = re.findall(r'<script>(.*?)</script>', text, re.S)
        with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False, encoding="utf-8") as handle:
            for block in scripts:
                handle.write(block + "\n")
            temp_path = Path(handle.name)
        proc = _osp_subprocess.run([node, "--check", str(temp_path)], capture_output=True, text=True)
        temp_path.unlink(missing_ok=True)
        ck("embedded-js-syntax", proc.returncode == 0, proc.stderr.strip())
    else:
        ck("embedded-js-syntax", True, "Node unavailable; static checks only")
    passed = sum(1 for _, ok, _ in checks if ok)
    print(f"Standalone reader QA: {passed}/{len(checks)} PASS")
    return 0 if passed == len(checks) else 1


def integrated_self_test() -> int:
    """Structural release gate for the single-script distribution."""
    import py_compile
    results: list[tuple[str, bool, str]] = []
    def check(name: str, ok: bool, detail: str = "") -> None:
        results.append((name, bool(ok), detail))
        print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f" — {detail}" if detail else ""))

    required = [
        PROJECT_ROOT / "Offline Survival.py",
        PROJECT_ROOT / "README.md",
        PROJECT_ROOT / "MAINTENANCE.json",
        PROJECT_ROOT / "Offline Survival Reader.html",
        PROJECT_ROOT / "web" / "index.html",
        PROJECT_ROOT / "web" / "styles.css",
        PROJECT_ROOT / "web" / "app.js",
        PROJECT_ROOT / "web" / "field-operations.js",
        PROJECT_ROOT / "web" / "continuity-operations.js",
        PROJECT_ROOT / "web" / "knowledge-atlas.js",
        PROJECT_ROOT / "web" / "phone-test.html",
        PROJECT_ROOT / "web" / "phone-test.js",
        PROJECT_ROOT / "web" / "sw.js",
        PROJECT_ROOT / "web" / "manifest.webmanifest",
        PROJECT_ROOT / "English",
        PROJECT_ROOT / "Ελληνικά",
        PROJECT_ROOT / "Offline Library",
    ]
    for path in required:
        check(f"required:{path.name}", path.exists(), str(path.relative_to(PROJECT_ROOT)))

    py_files = sorted(PROJECT_ROOT.rglob("*.py"))
    check("single-python-script", py_files == [PROJECT_ROOT / "Offline Survival.py"], ", ".join(str(p.relative_to(PROJECT_ROOT)) for p in py_files))
    try:
        py_compile.compile(str(PROJECT_ROOT / "Offline Survival.py"), doraise=True)
        check("python-syntax", True)
    except Exception as exc:
        check("python-syntax", False, str(exc))

    report = OfflineDatabase().integrity_report()
    check("database-integrity", bool(report.get("ok")), f"EN {report['languages']['en']['records']} / EL {report['languages']['el']['records']}")

    for label, tool in (("content-quality", "content_quality"), ("translation-audit", "translation_audit"), ("library-quality", "library_quality")):
        try:
            code = run_embedded_tool(tool)
            check(label, code == 0, "integrated")
        except Exception as exc:
            check(label, False, str(exc))

    ok, detail = _phone_assets_test()
    check("phone-browser-assets", ok, detail)
    try:
        check("standalone-reader", _standalone_reader_test() == 0, "integrated")
    except Exception as exc:
        check("standalone-reader", False, str(exc))

    html = (PROJECT_ROOT / "web" / "index.html").read_text(encoding="utf-8")
    scripts = "\n".join((PROJECT_ROOT / "web" / name).read_text(encoding="utf-8") for name in ("app.js","field-operations.js","continuity-operations.js","knowledge-atlas.js"))
    ids = re.findall(r'\bid="([^"]+)"', html)
    duplicates = sorted({x for x in ids if ids.count(x) > 1})
    check("html-unique-ids", not duplicates, ", ".join(duplicates[:10]))
    sections = re.findall(r'<section[^>]*\bid="([^"]+)"', html)
    check("command-center-sections", len(sections) >= 32, str(len(sections)))
    handlers = set(re.findall(r'\bonclick="\s*([A-Za-z_$][\w$]*)\s*\(', html))
    functions = set(re.findall(r'(?<![\w$])(?:async\s+)?function\s+([A-Za-z_$][\w$]*)\s*\(', scripts))
    check("inline-handler-targets", not (handlers-functions), ", ".join(sorted(handlers-functions)))

    node = shutil.which("node")
    if node:
        js_files = [PROJECT_ROOT / "web" / x for x in ("app.js","field-operations.js","continuity-operations.js","knowledge-atlas.js","phone-test.js","sw.js")]
        ok = True; detail_parts=[]
        for js in js_files:
            proc=_osp_subprocess.run([node,"--check",str(js)],capture_output=True,text=True)
            if proc.returncode:
                ok=False; detail_parts.append(f"{js.name}: {proc.stderr.strip()}")
        check("javascript-syntax", ok, " | ".join(detail_parts))
    else:
        check("javascript-syntax", True, "Node.js unavailable; static JS checks only")

    passed=sum(1 for _,ok,_ in results if ok)
    print("="*64)
    print(f"{passed}/{len(results)} self-tests passed")
    return 0 if passed==len(results) else 1


def integrated_deep_audit() -> int:
    """Line-by-line source/config audit with a hard one-Python-file rule."""
    findings: list[str] = []
    active_suffixes={".py",".js",".css",".html",".sh",".bat",".json",".webmanifest",".md"}
    files=[]
    for path in PROJECT_ROOT.rglob("*"):
        if not path.is_file() or path.name == "Offline Survival Reader.html":
            continue
        if "Offline Library" in path.parts and path.suffix.lower() not in {".json"}:
            continue
        if path.suffix.lower() in active_suffixes or path.name in {"manifest.webmanifest"}:
            files.append(path)
    line_count=0; json_count=0
    for path in files:
        try:
            raw=path.read_bytes()
            if bytes([0]) in raw:
                findings.append(f"NUL byte: {path.relative_to(PROJECT_ROOT)}")
                continue
            text=raw.decode("utf-8")
        except Exception as exc:
            findings.append(f"Unreadable UTF-8: {path.relative_to(PROJECT_ROOT)}: {exc}")
            continue
        line_count += text.count("\\n") + 1
        for no,line in enumerate(text.splitlines(),1):
            if line.rstrip()!=line:
                findings.append(f"Trailing whitespace: {path.relative_to(PROJECT_ROOT)}:{no}")
        if path.suffix.lower() in {".json", ".webmanifest"} or path.name.endswith(".webmanifest"):
            try:
                json.loads(text); json_count+=1
            except Exception as exc:
                findings.append(f"Invalid JSON: {path.relative_to(PROJECT_ROOT)}: {exc}")
    py_files=sorted(PROJECT_ROOT.rglob("*.py"))
    if py_files != [PROJECT_ROOT / "Offline Survival.py"]:
        findings.append("Expected exactly one Python script: Offline Survival.py")
    stale_docs=[p for p in PROJECT_ROOT.glob("*.md") if p.name.upper().startswith(("VALIDATION","UPGRADE","V3_","V4_","V5_","V6_","V7_","AUDIT"))]
    if stale_docs:
        findings.append("Release/validation documents should not ship: "+", ".join(p.name for p in stale_docs))
    symlinks=[p for p in PROJECT_ROOT.rglob("*") if p.is_symlink()]
    if symlinks:
        findings.append("Unexpected symlinks: "+", ".join(str(p.relative_to(PROJECT_ROOT)) for p in symlinks[:10]))
    print("Offline Survival Project Deep Audit")
    print(f"Files inspected: {len(files)}")
    print(f"Lines inspected: {line_count}")
    print(f"JSON/config files parsed: {json_count}")
    print(f"Python scripts: {len(py_files)}")
    if findings:
        for item in findings[:100]: print(f"[FAIL] {item}")
        print(f"FAIL — {len(findings)} finding(s)")
        return 1
    print("PASS — no deep-audit findings")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
