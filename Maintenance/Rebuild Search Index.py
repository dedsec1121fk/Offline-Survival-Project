#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rebuild the compact contentless SQLite search index atomically."""

import importlib.util
import os
import sqlite3
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP_FILE = os.path.join(ROOT, "Offline Survival.py")
INDEX_FILE = os.path.join(ROOT, "Offline Survival Search Index.sqlite3")
TEMP_FILE = INDEX_FILE + ".tmp"
MAX_REPOSITORY_FILE_BYTES = 40_000_000


def load_application_module():
    spec = importlib.util.spec_from_file_location("offline_survival_app", APP_FILE)
    if spec is None or spec.loader is None:
        raise RuntimeError("Could not load Offline Survival.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def rebuild_index():
    module = load_application_module()
    store = module.STORE
    if store.load_errors:
        raise RuntimeError("Database load errors: " + "; ".join(store.load_errors))

    if os.path.exists(TEMP_FILE):
        os.remove(TEMP_FILE)

    connection = sqlite3.connect(TEMP_FILE)
    try:
        connection.execute("PRAGMA page_size=4096")
        connection.execute("PRAGMA journal_mode=OFF")
        connection.execute("PRAGMA synchronous=OFF")
        connection.execute(
            "CREATE TABLE metadata(key TEXT PRIMARY KEY, value TEXT NOT NULL) WITHOUT ROWID"
        )
        connection.execute(
            "CREATE TABLE entry_map(rowid INTEGER PRIMARY KEY, entry_id TEXT NOT NULL UNIQUE)"
        )
        connection.execute(
            "CREATE VIRTUAL TABLE entries_fts USING fts5("
            "content, content='', columnsize=0, detail=none, tokenize='unicode61')"
        )
        connection.executemany(
            "INSERT INTO metadata(key, value) VALUES(?, ?)",
            [
                ("entry_count", str(len(store.entries))),
                ("database_signature", store.database_signature()),
                ("index_format", "contentless-v2"),
            ],
        )
        for rowid, entry in enumerate(store.entries, 1):
            connection.execute(
                "INSERT INTO entry_map(rowid, entry_id) VALUES(?, ?)",
                (rowid, entry["id"]),
            )
            connection.execute(
                "INSERT INTO entries_fts(rowid, content) VALUES(?, ?)",
                (rowid, store.build_full_search_blob(entry)),
            )
        connection.commit()
        connection.execute("INSERT INTO entries_fts(entries_fts) VALUES('optimize')")
        connection.commit()
        connection.execute("VACUUM")
    finally:
        connection.close()

    size = os.path.getsize(TEMP_FILE)
    if size >= MAX_REPOSITORY_FILE_BYTES:
        os.remove(TEMP_FILE)
        raise RuntimeError(
            f"Compact index is still too large: {size:,} bytes "
            f"(limit {MAX_REPOSITORY_FILE_BYTES:,})"
        )

    os.replace(TEMP_FILE, INDEX_FILE)
    print(f"Rebuilt {len(store.entries):,} entries")
    print(f"Index size: {size:,} bytes")
    print(f"Saved: {INDEX_FILE}")


if __name__ == "__main__":
    try:
        rebuild_index()
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        if os.path.exists(TEMP_FILE):
            os.remove(TEMP_FILE)
        raise SystemExit(1)
