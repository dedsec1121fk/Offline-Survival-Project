#!/usr/bin/env python3
# MAINTENANCE: Exercise real loopback API/security behavior without touching the user's persistent state.
"""Repeatable localhost API/security smoke test for Offline Survival Project.

Uses only the Python standard library. A temporary HOME keeps the user's real
Command Center state untouched.
"""
from __future__ import annotations

import json
import os
import socket
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Any
from urllib import error, parse, request

ROOT = Path(__file__).resolve().parents[1]
WEB_APP = ROOT / "Offline Survival Web.py"
MIN_LIBRARY_FILES = 420


def free_port() -> int:
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


def main() -> int:
    port = free_port()
    base = f"http://127.0.0.1:{port}"
    temp_home = tempfile.mkdtemp(prefix="offline-survival-qa-")
    env = os.environ.copy()
    env["HOME"] = temp_home
    proc = subprocess.Popen(
        [sys.executable, str(WEB_APP), "--host", "127.0.0.1", "--port", str(port), "--no-browser", "--quiet"],
        cwd=ROOT,
        env=env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
        text=True,
    )
    checks: list[tuple[str, bool, str]] = []

    def check(name: str, condition: bool, detail: str = "") -> None:
        checks.append((name, bool(condition), detail))
        print(f"[{'PASS' if condition else 'FAIL'}] {name}" + (f" — {detail}" if detail else ""))

    def call(path: str, method: str = "GET", payload: Any = None, headers: dict[str, str] | None = None):
        body = None if payload is None else json.dumps(payload).encode("utf-8")
        req_headers = {"Content-Type": "application/json"} if body is not None else {}
        req_headers.update(headers or {})
        req = request.Request(base + path, data=body, headers=req_headers, method=method)
        try:
            with request.urlopen(req, timeout=10) as response:
                return response.status, dict(response.headers), response.read()
        except error.HTTPError as exc:
            return exc.code, dict(exc.headers), exc.read()

    try:
        for _ in range(80):
            try:
                if call("/api/meta")[0] == 200:
                    break
            except Exception:
                pass
            time.sleep(0.1)
        else:
            check("server-start", False, "Command Center did not start")
            return 1

        status, headers, raw = call("/api/meta")
        meta = json.loads(raw)
        check("meta-state-schema", status == 200 and isinstance(meta.get("state_schema_version"), int))
        check("library-discovery", meta.get("system", {}).get("library_files", 0) >= MIN_LIBRARY_FILES, str(meta.get("system", {}).get("library_files")))
        status, _, raw = call("/api/library")
        library = json.loads(raw) if status == 200 else {}
        knowledge_files = [x for x in library.get("files", []) if str(x.get("path", "")).startswith("Knowledge Compendium/")] if status == 200 else []
        expected_knowledge = sum(1 for f in (ROOT / "Offline Library" / "Knowledge Compendium").rglob("*.md") if f.is_file())
        check("knowledge-compendium-discovery", status == 200 and len(knowledge_files) == expected_knowledge, f"{len(knowledge_files)}/{expected_knowledge}")
        prefix = parse.quote("Knowledge Compendium/EN", safe="")
        query = parse.quote("water", safe="")
        status, _, raw = call(f"/api/library/search?q={query}&limit=250&prefix={prefix}")
        scoped = json.loads(raw) if status == 200 else {}
        scoped_rows = scoped.get("results", [])
        check("library-prefix-search", status == 200 and bool(scoped_rows) and all(str(x.get("path", "")).startswith("Knowledge Compendium/EN/") for x in scoped_rows), str(len(scoped_rows)))
        bad_prefix = parse.quote("../", safe="")
        status, _, _ = call(f"/api/library/search?q={query}&prefix={bad_prefix}")
        check("library-prefix-traversal-rejected", status == 400, str(status))
        check("security-headers", headers.get("X-Frame-Options") == "DENY" and "frame-ancestors" in headers.get("Content-Security-Policy", ""))

        status, _, raw = call("/api/diagnostics")
        diagnostics = json.loads(raw)
        check("diagnostics", status == 200 and diagnostics.get("ok") is True)

        state_a = {"profile": {"adults": 2}, "resource_plans": [{"name": "Water", "stock": 20, "unit": "L", "daily_use": 4, "reserve": 4}], "shelter_zones": [{"name": "Room A", "status": "safe", "occupants": 2}], "water_batches": [{"source": "Stored container", "volume_l": 12, "status": "ready"}], "skill_matrix": [{"person": "A", "skill": "Radio check", "level": "practiced"}], "decision_board": [{"issue": "Route", "decision": "Use alternate", "status": "active"}], "food_lots": [{"name": "Rice bin", "qty": 4, "unit": "kg", "kcal_total": 14000, "status": "sealed"}], "sanitation_points": [{"name": "Wash station", "kind": "handwash", "status": "ready"}], "power_loads": [{"name": "Radio", "watts": 8, "hours_per_day": 2, "priority": "critical", "enabled": True}], "comms_windows": [{"name": "Evening check", "method": "radio", "status": "active"}], "dependents": [{"name": "Pet A", "kind": "pet", "backup": "Neighbour"}], "expense_log": [{"category": "transport", "description": "Fuel", "amount": 20, "currency": "EUR", "status": "recorded"}], "knowledge_progress": [{"path": "01-emergency-water-reserve.md", "status": "reviewed", "last_review": "2026-08-09", "notes": "checked"}]}
        state_b = {"profile": {"adults": 3}, "routes": [{"name": "Route", "points": [[999, 999], [40.3, 23.1], [40.4, 23.2]]}]}
        status, _, raw = call("/api/state", "POST", state_a)
        saved_a = json.loads(raw)
        check("state-save", status == 200 and saved_a.get("profile", {}).get("adults") == 2 and saved_a.get("schema_version") == 7 and len(saved_a.get("shelter_zones", [])) == 1 and len(saved_a.get("water_batches", [])) == 1 and len(saved_a.get("skill_matrix", [])) == 1 and len(saved_a.get("decision_board", [])) == 1 and len(saved_a.get("food_lots", [])) == 1 and len(saved_a.get("sanitation_points", [])) == 1 and len(saved_a.get("power_loads", [])) == 1 and len(saved_a.get("comms_windows", [])) == 1 and len(saved_a.get("dependents", [])) == 1 and len(saved_a.get("expense_log", [])) == 1 and len(saved_a.get("knowledge_progress", [])) == 1)
        status, _, raw = call("/api/state", "POST", state_b)
        saved_b = json.loads(raw)
        check("coordinate-sanitization", status == 200 and len(saved_b.get("routes", [{}])[0].get("points", [])) == 2)
        status, _, raw = call("/api/state/previous")
        check("previous-state-created", status == 200 and json.loads(raw).get("available") is True)
        status, _, raw = call("/api/state/restore-previous", "POST", {})
        restored = json.loads(raw)
        check("previous-state-restore", status == 200 and restored.get("profile", {}).get("adults") == 2)
        check("knowledge-progress-restore", status == 200 and len(restored.get("knowledge_progress", [])) == 1 and restored.get("knowledge_progress", [{}])[0].get("status") == "reviewed")

        status, _, _ = call("/api/state", "POST", state_a, {"Origin": "https://example.invalid"})
        check("cross-origin-write-rejected", status == 403, str(status))
        status, _, _ = call("/api/state", "POST", state_a, {"Origin": base})
        check("same-origin-write-accepted", status == 200, str(status))
        status, _, _ = call("/api/state", "POST", state_a, {"Host": f"evil.example:{port}", "Origin": f"http://evil.example:{port}"})
        check("localhost-host-header-rejected", status == 421, str(status))

        status, _, raw = call("/api/library")
        files = json.loads(raw).get("files", [])
        readable = next((item for item in files if item.get("readable")), None)
        check("library-list", status == 200 and readable is not None, str(len(files)))
        if readable:
            quoted = parse.quote(readable["path"], safe="")
            status, _, raw = call("/api/library/hash?path=" + quoted)
            digest = json.loads(raw).get("sha256", "")
            check("library-sha256", status == 200 and len(digest) == 64)
            status, _, raw = call("/api/library/text?path=" + quoted)
            check("library-text-reader", status == 200 and bool(json.loads(raw).get("text")))
            status, _, raw = call("/api/library/search?q=" + parse.quote("water"))
            search_data = json.loads(raw)
            check("library-full-text-search", status == 200 and search_data.get("count", 0) > 0 and bool(search_data.get("results", [{}])[0].get("snippet")), str(search_data.get("count", 0)))
            status, direct_headers, _ = call("/library/" + parse.quote(readable["path"]))
            check("untrusted-library-download", status == 200 and direct_headers.get("Content-Disposition", "").startswith("attachment;") and "default-src 'none'" in direct_headers.get("Content-Security-Policy", ""))

        status, _, _ = call("/api/library/text?path=../../Offline%20Survival.py")
        check("library-path-traversal-rejected", status == 400, str(status))

        status, _, raw = call("/api/library/search?q=water&limit=100")
        v7_search = json.loads(raw) if status == 200 else {}
        knowledge_search_rows = [x for x in v7_search.get("results", []) if str(x.get("path", "")).startswith("Knowledge Compendium/EN/")] if status == 200 else []
        check("knowledge-full-text-search", status == 200 and len(knowledge_search_rows) > 0, str(len(knowledge_search_rows)))

        assets = {"/": "text/html", "/styles.css": "text/css", "/app.js": "javascript", "/field-operations.js": "javascript", "/continuity-operations.js": "javascript", "/knowledge-atlas.js": "javascript", "/phone-test.html": "text/html", "/phone-test.js": "javascript", "/reader.html": "text/html", "/manifest.webmanifest": "manifest", "/sw.js": "javascript"}
        for path, expected in assets.items():
            status, asset_headers, raw = call(path)
            check(f"asset:{path}", status == 200 and len(raw) > 100 and expected in asset_headers.get("Content-Type", ""))

        passed = sum(ok for _, ok, _ in checks)
        print("=" * 64)
        print(f"{passed}/{len(checks)} API/security smoke checks passed")
        return 0 if passed == len(checks) else 1
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=3)
        except subprocess.TimeoutExpired:
            proc.kill()
        if proc.returncode not in (None, 0, -15) and proc.stderr:
            tail = proc.stderr.read()[-1000:]
            if tail.strip():
                print(tail, file=sys.stderr)


if __name__ == "__main__":
    raise SystemExit(main())
