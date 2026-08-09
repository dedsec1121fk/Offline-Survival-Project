#!/usr/bin/env python3
"""Offline Survival Project v7 self-test.

Uses only Python's standard library. Node.js is optional; when available it
adds JavaScript syntax and runtime translation-object checks.
"""
from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WEB = ROOT / "web"
RESULTS: list[tuple[str, bool, str]] = []


def check(name: str, ok: bool, detail: str = "") -> None:
    RESULTS.append((name, bool(ok), detail))


def run(cmd: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=180)


def main() -> int:
    required = [
        ROOT / "Offline Survival.py",
        ROOT / "Offline Survival Web.py",
        WEB / "index.html",
        WEB / "styles.css",
        WEB / "app.js",
        WEB / "v5.js",
        WEB / "v6.js",
        WEB / "v7.js",
        WEB / "phone-test.html",
        WEB / "phone-test.js",
        WEB / "sw.js",
        WEB / "manifest.webmanifest",
        ROOT / "English",
        ROOT / "Ελληνικά",
        ROOT / "Offline Library",
        ROOT / "tools" / "api_smoke_test.py",
        ROOT / "tools" / "deep_audit.py",
        ROOT / "tools" / "content_quality.py",
        ROOT / "tools" / "translation_audit.py",
        ROOT / "tools" / "library_quality.py",
        ROOT / "tools" / "ui_logic_test.js",
        ROOT / "tools" / "phone_browser_assets_test.py",
        ROOT / "tools" / "standalone_reader_test.py",
        ROOT / "tools" / "build_standalone_reader.py",
        ROOT / "Offline Survival Reader.html",
    ]
    for path in required:
        check(f"required:{path.name}", path.exists(), str(path.relative_to(ROOT)))

    # Python compilation.
    py_files = [ROOT / "Offline Survival.py", ROOT / "Offline Survival Web.py", Path(__file__), ROOT / "tools" / "api_smoke_test.py", ROOT / "tools" / "deep_audit.py", ROOT / "tools" / "content_quality.py", ROOT / "tools" / "translation_audit.py", ROOT / "tools" / "library_quality.py", ROOT / "tools" / "phone_browser_assets_test.py", ROOT / "tools" / "standalone_reader_test.py", ROOT / "tools" / "build_standalone_reader.py"]
    compile_proc = run([sys.executable, "-m", "py_compile", *map(str, py_files)])
    check("python-syntax", compile_proc.returncode == 0, compile_proc.stderr.strip())

    phone_qa = run([sys.executable, str(ROOT / "tools" / "phone_browser_assets_test.py")])
    check("phone-browser-assets", phone_qa.returncode == 0, (phone_qa.stdout + phone_qa.stderr)[-600:].strip())

    reader_qa = run([sys.executable, str(ROOT / "tools" / "standalone_reader_test.py")])
    check("standalone-reader", reader_qa.returncode == 0, (reader_qa.stdout + reader_qa.stderr)[-600:].strip())

    # Full database validator from the actual application.
    db = run([sys.executable, str(ROOT / "Offline Survival.py"), "--check"])
    db_ok = db.returncode == 0
    detail = ""
    try:
        report = json.loads(db.stdout)
        en = report["languages"]["en"]
        el = report["languages"]["el"]
        detail = f"EN {en['records']} records/{en['files']} files; EL {el['records']} records/{el['files']} files"
        db_ok = db_ok and bool(report.get("ok"))
    except Exception:
        detail = (db.stderr or db.stdout)[-600:]
        db_ok = False
    check("database-integrity", db_ok, detail)

    quality = run([sys.executable, str(ROOT / "tools" / "content_quality.py")])
    check("content-quality", quality.returncode == 0, (quality.stderr or quality.stdout)[-700:] if quality.returncode else "no template filler / high-frequency repeated guidance")

    translations = run([sys.executable, str(ROOT / "tools" / "translation_audit.py")])
    check("translation-audit", translations.returncode == 0, (translations.stderr or translations.stdout)[-700:] if translations.returncode else "database + Library bilingual parity")

    library_quality = run([sys.executable, str(ROOT / "tools" / "library_quality.py")])
    check("library-quality", library_quality.returncode == 0, (library_quality.stderr or library_quality.stdout)[-700:] if library_quality.returncode else "no exact duplicates, repeated substantive paragraphs or template-like Library documents")

    html = (WEB / "index.html").read_text(encoding="utf-8")
    app_js = (WEB / "app.js").read_text(encoding="utf-8")
    v5_js = (WEB / "v5.js").read_text(encoding="utf-8")
    v6_js = (WEB / "v6.js").read_text(encoding="utf-8")
    v7_js = (WEB / "v7.js").read_text(encoding="utf-8")
    js = app_js + "\n" + v5_js + "\n" + v6_js + "\n" + v7_js
    css = (WEB / "styles.css").read_text(encoding="utf-8")
    server = (ROOT / "Offline Survival Web.py").read_text(encoding="utf-8")

    ids = re.findall(r'\bid="([^"]+)"', html)
    duplicate_ids = sorted({x for x in ids if ids.count(x) > 1})
    check("html-unique-ids", not duplicate_ids, ", ".join(duplicate_ids[:20]))

    sections = re.findall(r'<section[^>]*\bid="([^"]+)"', html)
    check("section-count", len(sections) >= 32, f"{len(sections)} sections")

    fn_names = re.findall(r'(?<![\w$])(?:async\s+)?function\s+([A-Za-z_$][\w$]*)\s*\(', js)
    dup_fns = sorted({x for x in fn_names if fn_names.count(x) > 1})
    check("js-unique-functions", not dup_fns, ", ".join(dup_fns[:20]))

    handlers = set(re.findall(r'\bonclick="\s*([A-Za-z_$][\w$]*)\s*\(', html))
    defined = set(fn_names)
    missing_handlers = sorted(handlers - defined)
    check("inline-handler-targets", not missing_handlers, ", ".join(missing_handlers))

    # Static references from the HTML shell.
    refs = re.findall(r'(?:href|src)="(/[^"?#]+)', html)
    static_map = {"/styles.css": WEB / "styles.css", "/app.js": WEB / "app.js", "/v5.js": WEB / "v5.js", "/v6.js": WEB / "v6.js", "/v7.js": WEB / "v7.js", "/manifest.webmanifest": WEB / "manifest.webmanifest"}
    missing_refs = [r for r in refs if r in static_map and not static_map[r].is_file()]
    check("static-assets", not missing_refs, ", ".join(missing_refs))

    try:
        manifest = json.loads((WEB / "manifest.webmanifest").read_text(encoding="utf-8"))
        check("web-manifest", manifest.get("start_url") == "/" and manifest.get("display") == "standalone", manifest.get("name", ""))
    except Exception as error:
        check("web-manifest", False, str(error))

    # Simple structural guards that catch accidental truncation.
    check("css-braces", css.count("{") == css.count("}"), f"{css.count('{')} open / {css.count('}')} close")
    check("html-shell", html.lstrip().startswith("<!doctype html>") and html.rstrip().endswith("</html>"), f"{len(html)} chars")

    security_bad = []
    for pattern in (r'\beval\s*\(', r'\bexec\s*\(', r'shell\s*=\s*True'):
        if re.search(pattern, (ROOT / "Offline Survival Web.py").read_text(encoding="utf-8")):
            security_bad.append(pattern)
    check("server-dangerous-exec-patterns", not security_bad, ", ".join(security_bad))

    version_match = re.search(r"COMMAND_CENTER_VERSION\s*=\s*(\d+)", server)
    server_version_match = re.search(r"server_version\s*=\s*\"OfflineSurvivalCommandCenter/(\d+)\.0\"", server)
    schema_match = re.search(r"SCHEMA_VERSION\s*=\s*(\d+)", server)
    version_ok = bool(version_match and server_version_match and schema_match and version_match.group(1) == server_version_match.group(1) == schema_match.group(1))
    check("version-consistency", version_ok, f"command={version_match.group(1) if version_match else '?'} server={server_version_match.group(1) if server_version_match else '?'} schema={schema_match.group(1) if schema_match else '?'}")

    # Release metadata must describe the actual payload, not a stale earlier build.
    try:
        release = json.loads((ROOT / "RELEASE_MANIFEST.json").read_text(encoding="utf-8"))
        library_count = sum(1 for p in (ROOT / "Offline Library").rglob("*") if p.is_file())
        release_ok = bool(
            release.get("command_center_version") == int(version_match.group(1))
            and release.get("state_schema") == int(schema_match.group(1))
            and release.get("database", {}).get("english_records") == report["languages"]["en"]["records"]
            and release.get("database", {}).get("greek_records") == report["languages"]["el"]["records"]
            and release.get("database", {}).get("json_files_per_language") == report["languages"]["en"]["files"]
            and release.get("offline_library", {}).get("files_total") == library_count
            and release.get("web_sections") == len(sections)
        )
        check("release-manifest-consistency", release_ok, f"db={report['languages']['en']['records']}/{report['languages']['en']['files']} library={library_count} sections={len(sections)}")
    except Exception as error:
        check("release-manifest-consistency", False, str(error))

    bad_download_order = re.findall(r"downloadBlob\(\s*['\"][^'\"]+\.(?:csv|geojson|json|txt)['\"]\s*,", js)
    check("download-export-argument-order", not bad_download_order, ", ".join(bad_download_order[:10]))
    check("redacted-export-blank-schema", "exportRedactedState(){const clean=structuredCloneSafe(DEFAULT_STATE)" in app_js)

    lib_hardened = "self.send_file(path, cache=False, untrusted=True)" in server and "Content-Disposition" in server and "default-src 'none'; sandbox" in server
    check("library-untrusted-content-hardening", lib_hardened)

    origin_hardened = "def same_origin_request" in server and "if not self.same_origin_request()" in server
    check("same-origin-write-protection", origin_hardened)
    host_hardened = "def host_header_allowed" in server and "server.allowed_hosts" in server and "HTTPStatus.MISDIRECTED_REQUEST" in server
    check("localhost-host-header-protection", host_hardened)

    # Browser backups must advertise the same schema as the server.
    export_schemas = re.findall(r"payload=\{app:'Offline Survival Project',schema:(\d+)", app_js)
    expected_schema = schema_match.group(1) if schema_match else None
    check("browser-backup-schema", bool(export_schemas) and all(x == expected_schema for x in export_schemas), f"exports={export_schemas} expected={expected_schema}")

    sw = (WEB / "sw.js").read_text(encoding="utf-8")
    sw_sensitive_ok = "/api/" in sw and "/library/" in sw and "SHELL_PATHS" in sw and ".put(" in sw and "startsWith" in sw
    check("service-worker-sensitive-exclusions", sw_sensitive_ok, "API/library excluded; shell allowlist present" if sw_sensitive_ok else "missing API/library exclusion or shell allowlist")

    node = shutil.which("node")
    if node:
        for asset in (WEB / "app.js", WEB / "v5.js", WEB / "v6.js", WEB / "v7.js", WEB / "phone-test.js", WEB / "sw.js", ROOT / "tools" / "ui_logic_test.js"):
            proc = run([node, "--check", str(asset)])
            check(f"js-syntax:{asset.name}", proc.returncode == 0, proc.stderr.strip())

        # Evaluate constant/translation setup but suppress init(), so DOM is not needed.
        probe = r'''
const fs=require('fs'),vm=require('vm');
let base=fs.readFileSync(process.argv[1],'utf8').replace(/\ninit\(\);\s*$/,'\nglobalThis.__T=T; globalThis.__NAV=NAV; globalThis.__MOBILE_NAV=MOBILE_NAV;');
let ext=fs.readFileSync(process.argv[2],'utf8').replace(/\napplyLang\(\);\s*$/,'');
let ext6=fs.readFileSync(process.argv[3],'utf8').replace(/\napplyLang\(\);\s*$/,'');
let ext7=fs.readFileSync(process.argv[4],'utf8').replace(/\napplyLang\(\);\s*$/,'');
const box={localStorage:{getItem:()=>null,setItem:()=>{}},console,structuredClone:global.structuredClone,URL,Blob,Date,Math,JSON,Number,String,Array,Object,Set,Map,Intl,decodeURIComponent,encodeURIComponent};
vm.createContext(box); vm.runInContext(base,box); vm.runInContext(ext,box); vm.runInContext(ext6,box); vm.runInContext(ext7,box);
vm.runInContext('globalThis.__T=T; globalThis.__NAV=NAV; globalThis.__MOBILE_NAV=MOBILE_NAV;',box);
process.stdout.write(JSON.stringify({T:box.__T,NAV:box.__NAV,MOBILE_NAV:box.__MOBILE_NAV}));
'''
        proc = run([node, "-e", probe, str(WEB / "app.js"), str(WEB / "v5.js"), str(WEB / "v6.js"), str(WEB / "v7.js")])
        if proc.returncode == 0:
            runtime = json.loads(proc.stdout)
            t = runtime["T"]
            data_keys = set(re.findall(r'data-(?:t|ph)="([^"]+)"', html))
            en, el = set(t["en"]), set(t["el"])
            missing_en, missing_el = sorted(data_keys - en), sorted(data_keys - el)
            check("translation-coverage-en", not missing_en, ", ".join(missing_en[:30]))
            check("translation-coverage-el", not missing_el, ", ".join(missing_el[:30]))
            parity = sorted(en ^ el)
            check("translation-key-parity", not parity, ", ".join(parity[:30]))
            nav = [x[0] for x in runtime["NAV"]]
            check("navigation-section-parity", set(nav) == set(sections), f"{len(nav)} nav / {len(sections)} sections")
        else:
            check("translation-runtime-probe", False, proc.stderr.strip())

        ui_proc = run([node, str(ROOT / "tools" / "ui_logic_test.js")])
        check("ui-logic-runtime", ui_proc.returncode == 0, (ui_proc.stderr or ui_proc.stdout)[-700:] if ui_proc.returncode else "v7 DOM/state logic exercised without network")
        if proc.returncode != 0:
            pass
    else:
        check("node-optional", True, "Node not installed; JavaScript syntax/runtime checks skipped")

    passed = sum(ok for _, ok, _ in RESULTS)
    print("Offline Survival Project — v7 self-test")
    print("=" * 64)
    for name, ok, detail in RESULTS:
        suffix = f" — {detail}" if detail else ""
        print(f"[{'PASS' if ok else 'FAIL'}] {name}{suffix}")
    print("=" * 64)
    print(f"{passed}/{len(RESULTS)} checks passed")
    return 0 if passed == len(RESULTS) else 2


if __name__ == "__main__":
    raise SystemExit(main())
