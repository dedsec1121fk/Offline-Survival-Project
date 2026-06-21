#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run the complete offline release validation without external dependencies."""

import importlib.util
import json
import os
import py_compile
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
APP_FILE = ROOT / "Offline Survival.py"
EXPECTED_FIELDS = 48


def load_app():
    spec = importlib.util.spec_from_file_location("offline_survival_validation", APP_FILE)
    if spec is None or spec.loader is None:
        raise RuntimeError("Could not load Offline Survival.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    checks = {}
    py_compile.compile(str(APP_FILE), doraise=True)
    for path in (ROOT / "Maintenance").glob("*.py"):
        py_compile.compile(str(path), doraise=True)
    checks["python_compilation"] = True

    app = load_app()
    store = app.STORE
    checks["entries"] = len(store.entries)
    checks["database_files"] = len(store.by_file)
    checks["categories"] = len(store.by_category)
    checks["load_errors"] = list(store.load_errors)
    checks["search_index_ready"] = store.search_index_ready
    checks["search_index_format"] = store.search_index_format

    schemas = {
        tuple(sorted(key for key in entry if not key.startswith("_")))
        for entry in store.entries
    }
    checks["schema_variants"] = len(schemas)
    checks["fields_per_record"] = sorted({len(schema) for schema in schemas})

    report = store.integrity_report()
    checks["audit_counts"] = {key: len(value) for key, value in report.items()}

    en, mode_en = store.search_with_mode("earthquake aftershock", "en", 25)
    el, mode_el = store.search_with_mode("σεισμος", "el", 25)
    relaxed, mode_relaxed = store.search_with_mode("earthquake impossibleword", "en", 25)
    checks["search_tests"] = {
        "english_results": len(en),
        "english_mode": mode_en,
        "greek_without_accents_results": len(el),
        "greek_mode": mode_el,
        "relaxed_results": len(relaxed),
        "relaxed_mode": mode_relaxed,
    }

    largest, oversized = store.repository_size_report()
    checks["largest_file"] = {
        "bytes": largest[0][0] if largest else 0,
        "path": largest[0][1] if largest else None,
    }
    checks["oversized_files"] = oversized

    required_web_tokens = [
        "/api/favorites", "/api/recent", "priority", "offlineSurvivalLang",
        "Πρόσφατα", "No exact all-word match",
    ]
    checks["web_interface_tokens_missing"] = [
        token for token in required_web_tokens if token not in app.WEB_PAGE
    ]

    failures = []
    if checks["load_errors"]:
        failures.append("database load errors")
    if not checks["search_index_ready"]:
        failures.append("search index is missing or stale")
    if checks["schema_variants"] != 1 or checks["fields_per_record"] != [EXPECTED_FIELDS]:
        failures.append("record schema mismatch")
    if any(checks["audit_counts"].values()):
        failures.append("integrity audit defects")
    if not en or not el or not relaxed or mode_relaxed != "relaxed":
        failures.append("search behavior failure")
    if oversized:
        failures.append("one or more repository files reached 40 MB")
    if checks["web_interface_tokens_missing"]:
        failures.append("web interface integration markers missing")

    checks["status"] = "PASS" if not failures else "FAIL"
    checks["failures"] = failures
    print(json.dumps(checks, ensure_ascii=False, indent=2))
    raise SystemExit(0 if not failures else 1)


if __name__ == "__main__":
    main()
