#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import json
import html
import textwrap
import subprocess
import webbrowser
from collections import Counter, defaultdict
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from threading import Thread
from urllib.parse import parse_qs, urlparse

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.join(BASE_DIR, "Offline Survival Database")
UPDATES_DIR = os.path.join(BASE_DIR, "Offline Survival Updates")
WEB_HOST = "127.0.0.1"
WEB_PORT = 8765

def clear():
    os.system("clear" if os.name != "nt" else "cls")

def safe_text(value):
    if value is None:
        return ""
    return str(value).strip()

def safe_list(value):
    if isinstance(value, list):
        out = []
        seen = set()
        for item in value:
            text = safe_text(item)
            key = text.lower()
            if text and key not in seen:
                seen.add(key)
                out.append(text)
        return out
    if value is None:
        return []
    text = safe_text(value)
    return [text] if text else []

def pause(msg="\nPress Enter to continue..."):
    try:
        input(msg)
    except EOFError:
        pass

class OfflineSurvivalStore:
    def __init__(self):
        self.entries = []
        self.by_id = {}
        self.by_file = defaultdict(list)
        self.by_category = defaultdict(list)
        self.load_errors = []
        self.last_loaded_files = []

    def normalize_entry(self, entry, source_file):
        e = dict(entry) if isinstance(entry, dict) else {}
        e["id"] = safe_text(e.get("id")) or f"missing::{len(self.entries)+1}"
        e["topic"] = safe_text(e.get("topic"))
        e["topic_en"] = safe_text(e.get("topic_en")) or e["topic"]
        e["topic_el"] = safe_text(e.get("topic_el"))
        e["category"] = safe_text(e.get("category")) or "uncategorized"
        e["subcategory"] = safe_text(e.get("subcategory"))
        e["summary_en"] = safe_text(e.get("summary_en"))
        e["summary_el"] = safe_text(e.get("summary_el"))
        e["content_en"] = safe_text(e.get("content_en"))
        e["content_el"] = safe_text(e.get("content_el"))
        e["difficulty"] = safe_text(e.get("difficulty"))
        e["urgency"] = safe_text(e.get("urgency"))
        e["priority"] = safe_text(e.get("priority"))
        e["last_updated"] = safe_text(e.get("last_updated"))
        e["update_note"] = safe_text(e.get("update_note"))
        e["tags"] = safe_list(e.get("tags"))
        for key in [
            "steps_en","steps_el","warnings_en","warnings_el","mistakes_en","mistakes_el",
            "related_topics","materials_en","materials_el","alternatives_en","alternatives_el",
            "failure_signs_en","failure_signs_el","when_not_to_use_en","when_not_to_use_el"
        ]:
            e[key] = safe_list(e.get(key))
        for key in [
            "short_term_en","short_term_el","long_term_en","long_term_el",
            "if_method_fails_en","if_method_fails_el","environment_notes_en","environment_notes_el"
        ]:
            e[key] = safe_text(e.get(key))
        e["_source_file"] = source_file
        e["_search_blob"] = self.build_search_blob(e)
        return e

    def build_search_blob(self, entry):
        parts = [
            entry.get("id",""), entry.get("topic",""), entry.get("topic_en",""), entry.get("topic_el",""),
            entry.get("category",""), entry.get("subcategory",""),
            entry.get("summary_en",""), entry.get("summary_el",""),
            entry.get("content_en",""), entry.get("content_el",""),
            entry.get("short_term_en",""), entry.get("short_term_el",""),
            entry.get("long_term_en",""), entry.get("long_term_el",""),
            entry.get("if_method_fails_en",""), entry.get("if_method_fails_el",""),
            entry.get("environment_notes_en",""), entry.get("environment_notes_el",""),
            entry.get("difficulty",""), entry.get("urgency",""), entry.get("priority",""),
            entry.get("last_updated",""), entry.get("update_note",""), entry.get("_source_file","")
        ]
        for key in [
            "tags","steps_en","steps_el","warnings_en","warnings_el","mistakes_en","mistakes_el",
            "related_topics","materials_en","materials_el","alternatives_en","alternatives_el",
            "failure_signs_en","failure_signs_el","when_not_to_use_en","when_not_to_use_el"
        ]:
            parts.extend(entry.get(key, []))
        return " \n ".join(parts).lower()

    def load(self):
        self.entries = []
        self.by_id = {}
        self.by_file = defaultdict(list)
        self.by_category = defaultdict(list)
        self.load_errors = []
        self.last_loaded_files = []
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
                    raise ValueError("Top-level JSON must be a list or object.")
                self.last_loaded_files.append(name)
                for raw in data:
                    entry = self.normalize_entry(raw, name)
                    self.entries.append(entry)
                    self.by_id[entry["id"]] = entry
                    self.by_file[name].append(entry)
                    self.by_category[entry["category"]].append(entry)
            except Exception as exc:
                self.load_errors.append(f"{name}: {exc}")
        self.entries.sort(key=lambda x: (x.get("category",""), x.get("topic_en","").lower()))

    def stats(self):
        return {
            "entries": len(self.entries),
            "files": len(self.by_file),
            "categories": len(self.by_category),
            "load_errors": len(self.load_errors),
        }

    def search(self, query, lang="en", limit=80):
        q = safe_text(query).lower()
        if not q:
            return []
        tokens = [t for t in q.split() if t]
        results = []
        for entry in self.entries:
            blob = entry.get("_search_blob","")
            if all(token in blob for token in tokens):
                results.append(entry)
            elif q in blob:
                results.append(entry)
        results.sort(key=lambda e: (
            q not in (e.get("topic_en","").lower() + " " + e.get("topic","").lower() + " " + e.get("topic_el","").lower()),
            e.get("category",""),
            e.get("topic_en","").lower()
        ))
        return results[:limit]

    def integrity_report(self):
        ids = [e["id"] for e in self.entries]
        topics = [e.get("topic_en") or e.get("topic") for e in self.entries]
        dup_ids = [k for k,v in Counter(ids).items() if v > 1]
        dup_topics = [k for k,v in Counter(topics).items() if v > 1]
        missing = []
        for e in self.entries:
            for key in ["id","topic","summary_en","summary_el","content_en","content_el","category"]:
                if not safe_text(e.get(key)):
                    missing.append((e.get("id",""), key))
        return {
            "duplicate_ids": dup_ids,
            "duplicate_topics": dup_topics,
            "missing_required": missing,
            "load_errors": list(self.load_errors),
        }

STORE = OfflineSurvivalStore()
STORE.load()

def display_topic(entry, lang):
    if lang == "el":
        return entry.get("topic_el") or entry.get("topic") or entry.get("topic_en") or "Untitled"
    return entry.get("topic_en") or entry.get("topic") or "Untitled"

def display_summary(entry, lang):
    return entry.get("summary_el") if lang == "el" else entry.get("summary_en")

def format_entry_text(entry, lang="en"):
    lines = []
    lines.append(display_topic(entry, lang))
    lines.append("=" * max(10, len(lines[-1])))
    lines.append(f"ID: {entry.get('id','')}")
    lines.append(f"Category: {entry.get('category','')} / {entry.get('subcategory','')}")
    lines.append(f"Source file: {entry.get('_source_file','')}")
    if entry.get("difficulty") or entry.get("urgency") or entry.get("priority"):
        lines.append(f"Difficulty: {entry.get('difficulty','')} | Urgency: {entry.get('urgency','')} | Priority: {entry.get('priority','')}")
    if entry.get("last_updated"):
        lines.append(f"Last updated: {entry.get('last_updated','')}")
    lines.append("")
    summary = entry.get("summary_el") if lang == "el" else entry.get("summary_en")
    content = entry.get("content_el") if lang == "el" else entry.get("content_en")
    if summary:
        lines.append("Summary")
        lines.append("-" * 7)
        lines.append(textwrap.fill(summary, width=98))
        lines.append("")
    if content:
        lines.append("Core reading")
        lines.append("-" * 12)
        for para in content.split("\n"):
            para = para.strip()
            if para:
                lines.append(textwrap.fill(para, width=98))
                lines.append("")
    sections = [
        ("Materials", "materials_el" if lang == "el" else "materials_en"),
        ("Steps", "steps_el" if lang == "el" else "steps_en"),
        ("Alternatives", "alternatives_el" if lang == "el" else "alternatives_en"),
        ("Warnings", "warnings_el" if lang == "el" else "warnings_en"),
        ("Failure signs", "failure_signs_el" if lang == "el" else "failure_signs_en"),
        ("When not to use", "when_not_to_use_el" if lang == "el" else "when_not_to_use_en"),
        ("Common mistakes", "mistakes_el" if lang == "el" else "mistakes_en"),
    ]
    for title, key in sections:
        items = entry.get(key, [])
        if items:
            lines.append(title)
            lines.append("-" * len(title))
            for idx, item in enumerate(items, 1):
                lines.append(f"{idx}. {item}")
            lines.append("")
    extras = [
        ("Short-term considerations", "short_term_el" if lang == "el" else "short_term_en"),
        ("Long-term considerations", "long_term_el" if lang == "el" else "long_term_en"),
        ("If the method fails", "if_method_fails_el" if lang == "el" else "if_method_fails_en"),
        ("Environment notes", "environment_notes_el" if lang == "el" else "environment_notes_en"),
    ]
    for title, key in extras:
        val = safe_text(entry.get(key))
        if val:
            lines.append(title)
            lines.append("-" * len(title))
            for para in val.split("\n"):
                para = para.strip()
                if para:
                    lines.append(textwrap.fill(para, width=98))
            lines.append("")
    if entry.get("related_topics"):
        lines.append("Related topics")
        lines.append("-" * 14)
        for item in entry.get("related_topics", []):
            lines.append(f"- {item}")
        lines.append("")
    if entry.get("update_note"):
        lines.append("Update note")
        lines.append("-" * 11)
        lines.append(textwrap.fill(entry.get("update_note",""), width=98))
    return "\n".join(lines).strip()

def pick_from_entries(entries, lang):
    if not entries:
        print("No entries found.")
        pause()
        return
    while True:
        clear()
        print(f"Entries: {len(entries)}")
        print("-" * 60)
        page = entries[:200]
        for idx, entry in enumerate(page, 1):
            print(f"{idx}. {display_topic(entry, lang)}  [{entry.get('category','')}]")
        if len(entries) > len(page):
            print(f"\nShowing first {len(page)} of {len(entries)} results.")
        print("\nEnter number to read, or press Enter to return.")
        choice = input("> ").strip()
        if not choice:
            return
        if choice.isdigit():
            idx = int(choice)
            if 1 <= idx <= len(page):
                clear()
                print(format_entry_text(page[idx-1], lang))
                pause()

WEB_PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Offline Survival Local UI</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
:root{--bg:#0f1115;--card:#171a21;--card2:#1d2230;--line:#2d3444;--text:#edf1f7;--muted:#aab4c7;--accent:#89b4ff;--accent2:#74d2ae}
*{box-sizing:border-box} body{margin:0;font-family:system-ui,-apple-system,Segoe UI,Roboto,sans-serif;background:var(--bg);color:var(--text)}
header{position:sticky;top:0;z-index:10;background:rgba(15,17,21,.96);backdrop-filter:blur(10px);border-bottom:1px solid var(--line);padding:12px}
.header-grid{display:grid;grid-template-columns:1.2fr .8fr;gap:10px;align-items:center}.title{font-size:1.05rem;font-weight:700}.sub{font-size:.88rem;color:var(--muted)}
.controls{display:grid;grid-template-columns:1fr 140px 1fr 1fr auto auto;gap:8px;align-items:center;margin-top:10px}
input,select,button{font:inherit;padding:11px 12px;border-radius:12px;border:1px solid var(--line);background:var(--card);color:var(--text)} button{cursor:pointer} button.primary{background:var(--accent);color:#081221;border-color:transparent;font-weight:700} button.ghost{background:transparent}
main{display:grid;grid-template-columns:minmax(320px,36%) 1fr;min-height:calc(100vh - 98px)} aside{border-right:1px solid var(--line);overflow:auto} #viewer{overflow:auto}
.panel{padding:12px}.card{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:14px;margin-bottom:12px}.result{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:12px;margin-bottom:10px;cursor:pointer}.result:hover,.result.active{border-color:var(--accent);background:var(--card2)}
.meta{color:var(--muted);font-size:.85rem}.pill{display:inline-block;padding:4px 9px;border-radius:999px;background:#101722;border:1px solid var(--line);margin:3px 6px 0 0;color:var(--muted);font-size:.82rem}.entry-title{margin:0 0 8px 0;font-size:1.45rem}.entry-block p{line-height:1.58}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:12px} ul{padding-left:20px;line-height:1.5}.chips{display:flex;flex-wrap:wrap;gap:8px}.chip{padding:7px 10px;border-radius:999px;border:1px solid var(--line);background:#121722;color:var(--text);cursor:pointer}.count{font-weight:700;color:var(--accent2)} .empty{color:var(--muted)}
@media (max-width:1100px){.controls{grid-template-columns:1fr 120px 1fr 1fr auto auto}.header-grid{grid-template-columns:1fr}}
@media (max-width:900px){main{grid-template-columns:1fr}aside{border-right:none;border-bottom:1px solid var(--line);max-height:44vh}.controls{grid-template-columns:1fr 1fr}.controls input{grid-column:1/-1}.grid2{grid-template-columns:1fr}}
</style>
</head>
<body>
<header>
  <div class="header-grid">
    <div><div class="title">Offline Survival Local UI</div><div class="sub">Local browser search, cleaner mobile reading, filters, and related-topic browsing.</div></div>
    <div class="meta" id="stats">Loading database information…</div>
  </div>
  <div class="controls">
    <input id="q" placeholder="Search topic, symptom, tool, method, food, terrain, material…">
    <select id="lang"><option value="en">English</option><option value="el">Ελληνικά</option></select>
    <select id="cat"><option value="">All categories</option></select>
    <select id="file"><option value="">All files</option></select>
    <button class="primary" onclick="runSearch()">Search</button>
    <button class="ghost" onclick="resetView()">Clear</button>
  </div>
</header>
<main>
  <aside><div class="panel"><div class="card"><div class="count" id="count">0 results</div><div class="empty" id="hint">Use filters or search across the local database.</div></div><div id="results"></div></div></aside>
  <section id="viewer"><div class="panel" id="viewer-inner"><div class="card"><h2 class="entry-title">Ready</h2><p class="entry-block">Search, filter, or pick a result to read it in a cleaner browser layout. Related topics become clickable chips after an entry is loaded.</p></div></div></section>
</main>
<script>
let lastResults = []; let activeId = null;
function esc(s){return (s||"").replace(/[&<>"]/g, ch => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[ch]));}
function textCard(title, text){ if(!text) return ''; return `<div class="card"><h3>${esc(title)}</h3><div class="entry-block"><p>${esc(text).replace(/
/g,'<br><br>')}</p></div></div>`; }
function listCard(title, items){ if(!items || !items.length) return ''; return `<div class="card"><h3>${esc(title)}</h3><ul>${items.map(x=>`<li>${esc(x)}</li>`).join('')}</ul></div>`; }
function chipsCard(title, items){ if(!items || !items.length) return ''; return `<div class="card"><h3>${esc(title)}</h3><div class="chips">${items.map(x=>`<button class="chip" onclick="searchRelated('${String(x).replace(/'/g,'&#39;')}')">${esc(x)}</button>`).join('')}</div></div>`; }
async function loadMeta(){ const res = await fetch('/api/meta'); const data = await res.json(); document.getElementById('stats').textContent = `${data.stats.entries} entries • ${data.stats.files} files • ${data.stats.categories} categories`; const cat=document.getElementById('cat'); const file=document.getElementById('file'); (data.categories||[]).forEach(x=>{const o=document.createElement('option');o.value=x;o.textContent=x;cat.appendChild(o);}); (data.files||[]).forEach(x=>{const o=document.createElement('option');o.value=x;o.textContent=x;file.appendChild(o);}); }
function updateCount(n,msg=''){ document.getElementById('count').textContent = `${n} result${n===1?'':'s'}`; document.getElementById('hint').textContent = msg; }
function selectedFilters(){ return {q:document.getElementById('q').value.trim(), lang:document.getElementById('lang').value, category:document.getElementById('cat').value, file:document.getElementById('file').value}; }
async function runSearch(){ const {q,lang,category,file}=selectedFilters(); const resultsEl=document.getElementById('results'); const viewer=document.getElementById('viewer-inner'); resultsEl.innerHTML='<div class="card empty">Searching…</div>'; const qs=new URLSearchParams({q,lang,category,file}); const res=await fetch(`/api/search?${qs.toString()}`); const data=await res.json(); lastResults=data.results||[]; if(!lastResults.length){ updateCount(0,'Try broader keywords, a different category, or remove one filter.'); resultsEl.innerHTML='<div class="card empty">No matching entries found.</div>'; viewer.innerHTML='<div class="card"><h2 class="entry-title">No result</h2><p class="entry-block">Try fewer words, remove one filter, or switch language.</p></div>'; return; } updateCount(lastResults.length,'Tap a result to open the full entry.'); resultsEl.innerHTML=lastResults.map(r=>`<div class="result ${activeId===r.id?'active':''}" onclick="loadEntry('${r.id.replace(/'/g,'&#39;')}')"><strong>${esc(r.topic)}</strong><div class="meta">${esc(r.category)} • ${esc(r.file)}</div><p>${esc((r.summary||'').slice(0,260))}</p></div>`).join(''); loadEntry(lastResults[0].id); }
async function loadEntry(id){ activeId=id; const {lang}=selectedFilters(); const viewer=document.getElementById('viewer-inner'); viewer.innerHTML='<div class="card empty">Loading entry…</div>'; const res=await fetch(`/api/entry?id=${encodeURIComponent(id)}&lang=${encodeURIComponent(lang)}`); const data=await res.json(); if(!data.entry){ viewer.innerHTML='<div class="card">Entry not found.</div>'; return; } const e=data.entry; const kickers=[e.category,e.subcategory,e.file].filter(Boolean).map(x=>`<span class="pill">${esc(x)}</span>`).join(''); viewer.innerHTML=`<div class="card"><h1 class="entry-title">${esc(e.topic)}</h1><div>${kickers}<span class="pill">${esc(e.id)}</span></div><div class="entry-block"><p>${esc(e.summary).replace(/
/g,'<br>')}</p><p>${esc(e.content).replace(/
/g,'<br><br>')}</p></div></div><div class="grid2"><div>${listCard(data.labels.materials,e.materials)}${listCard(data.labels.steps,e.steps)}${listCard(data.labels.alternatives,e.alternatives)}${listCard(data.labels.warnings,e.warnings)}${listCard(data.labels.failure_signs,e.failure_signs)}</div><div>${listCard(data.labels.when_not_to_use,e.when_not_to_use)}${listCard(data.labels.mistakes,e.mistakes)}${textCard(data.labels.short_term,e.short_term)}${textCard(data.labels.long_term,e.long_term)}${textCard(data.labels.if_method_fails,e.if_method_fails)}${textCard(data.labels.environment_notes,e.environment_notes)}</div></div>${chipsCard(data.labels.related_topics,e.related_topics)}${textCard(data.labels.update_note,e.update_note)}`; document.querySelectorAll('.result').forEach(el=>el.classList.remove('active')); const chosen=[...document.querySelectorAll('.result')].find(el=>el.getAttribute('onclick')?.includes(id)); if(chosen) chosen.classList.add('active'); }
function searchRelated(term){ document.getElementById('q').value = term; runSearch(); }
function resetView(){ document.getElementById('q').value=''; document.getElementById('cat').value=''; document.getElementById('file').value=''; updateCount(0,'Use filters or search across the local database.'); document.getElementById('results').innerHTML=''; document.getElementById('viewer-inner').innerHTML='<div class="card"><h2 class="entry-title">Ready</h2><p class="entry-block">Search, filter, or pick a result to read it in a cleaner browser layout.</p></div>'; }
document.getElementById('q').addEventListener('keydown',ev=>{if(ev.key==='Enter') runSearch();}); document.getElementById('lang').addEventListener('change',()=>{ if(activeId){ loadEntry(activeId); } }); document.getElementById('cat').addEventListener('change',()=>runSearch()); document.getElementById('file').addEventListener('change',()=>runSearch()); loadMeta().then(()=>updateCount(0,'Use filters or search across the local database.'));
</script>
</body>
</html>
"""


def browser_labels(lang):
    if lang == "el":
        return {
            "materials":"Υλικά",
            "steps":"Βήματα",
            "alternatives":"Εναλλακτικές",
            "warnings":"Προειδοποιήσεις",
            "failure_signs":"Σημάδια αποτυχίας",
            "when_not_to_use":"Πότε να μην το χρησιμοποιήσεις",
            "mistakes":"Συχνά λάθη",
            "short_term":"Βραχυπρόθεσμα",
            "long_term":"Μακροπρόθεσμα",
            "if_method_fails":"Αν η μέθοδος αποτύχει",
            "environment_notes":"Σημειώσεις περιβάλλοντος",
            "related_topics":"Σχετικά θέματα",
            "update_note":"Σημείωση ενημέρωσης",
        }
    return {
        "materials":"Materials",
        "steps":"Steps",
        "alternatives":"Alternatives",
        "warnings":"Warnings",
        "failure_signs":"Failure signs",
        "when_not_to_use":"When not to use",
        "mistakes":"Common mistakes",
        "short_term":"Short-term considerations",
        "long_term":"Long-term considerations",
        "if_method_fails":"If the method fails",
        "environment_notes":"Environment notes",
        "related_topics":"Related topics",
        "update_note":"Update note",
    }

class OfflineWebHandler(BaseHTTPRequestHandler):
    def _send_json(self, payload, status=200):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_html(self, body, status=200):
        data = body.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/":
            self._send_html(WEB_PAGE)
            return
        if parsed.path == "/api/meta":
            self._send_json({
                "categories": sorted(STORE.by_category.keys()),
                "files": sorted(STORE.by_file.keys()),
                "stats": STORE.stats(),
            })
            return
        if parsed.path == "/api/search":
            qs = parse_qs(parsed.query)
            query = qs.get("q", [""])[0]
            lang = qs.get("lang", ["en"])[0]
            category = qs.get("category", [""])[0]
            file_name = qs.get("file", [""])[0]
            results = STORE.search(query, lang=lang) if query else list(STORE.entries)
            if category:
                results = [entry for entry in results if entry.get("category","") == category]
            if file_name:
                results = [entry for entry in results if entry.get("_source_file","") == file_name]
            results = results[:200]
            payload = []
            for entry in results:
                payload.append({
                    "id": entry.get("id",""),
                    "topic": display_topic(entry, lang),
                    "summary": display_summary(entry, lang),
                    "category": entry.get("category",""),
                    "file": entry.get("_source_file","")
                })
            self._send_json({"results": payload})
            return
        if parsed.path == "/api/entry":
            qs = parse_qs(parsed.query)
            entry_id = qs.get("id", [""])[0]
            lang = qs.get("lang", ["en"])[0]
            entry = STORE.by_id.get(entry_id)
            if not entry:
                self._send_json({"entry": None}, status=404)
                return
            payload = {
                "id": entry.get("id",""),
                "topic": display_topic(entry, lang),
                "summary": entry.get("summary_el") if lang == "el" else entry.get("summary_en"),
                "content": entry.get("content_el") if lang == "el" else entry.get("content_en"),
                "category": entry.get("category",""),
                "subcategory": entry.get("subcategory",""),
                "file": entry.get("_source_file",""),
                "materials": entry.get("materials_el") if lang == "el" else entry.get("materials_en"),
                "steps": entry.get("steps_el") if lang == "el" else entry.get("steps_en"),
                "alternatives": entry.get("alternatives_el") if lang == "el" else entry.get("alternatives_en"),
                "warnings": entry.get("warnings_el") if lang == "el" else entry.get("warnings_en"),
                "failure_signs": entry.get("failure_signs_el") if lang == "el" else entry.get("failure_signs_en"),
                "when_not_to_use": entry.get("when_not_to_use_el") if lang == "el" else entry.get("when_not_to_use_en"),
                "mistakes": entry.get("mistakes_el") if lang == "el" else entry.get("mistakes_en"),
                "short_term": entry.get("short_term_el") if lang == "el" else entry.get("short_term_en"),
                "long_term": entry.get("long_term_el") if lang == "el" else entry.get("long_term_en"),
                "if_method_fails": entry.get("if_method_fails_el") if lang == "el" else entry.get("if_method_fails_en"),
                "environment_notes": entry.get("environment_notes_el") if lang == "el" else entry.get("environment_notes_en"),
                "related_topics": entry.get("related_topics", []),
                "update_note": entry.get("update_note",""),
            }
            self._send_json({"entry": payload, "labels": browser_labels(lang)})
            return
        self._send_json({"error": "Not found"}, status=404)

    def log_message(self, format, *args):
        return

def browse_files(lang):
    items = sorted(STORE.by_file.items())
    while True:
        clear()
        print("Database files\n" + "-" * 60)
        for idx, (name, data) in enumerate(items, 1):
            print(f"{idx}. {name}  ({len(data)} entries)")
        print("\nEnter number to inspect, or press Enter to return.")
        choice = input("> ").strip()
        if not choice:
            return
        if choice.isdigit():
            idx = int(choice)
            if 1 <= idx <= len(items):
                pick_from_entries(items[idx-1][1], lang)

def browse_categories(lang):
    items = sorted(STORE.by_category.items())
    while True:
        clear()
        print("Categories\n" + "-" * 60)
        for idx, (name, data) in enumerate(items, 1):
            print(f"{idx}. {name}  ({len(data)} entries)")
        print("\nEnter number to inspect, or press Enter to return.")
        choice = input("> ").strip()
        if not choice:
            return
        if choice.isdigit():
            idx = int(choice)
            if 1 <= idx <= len(items):
                pick_from_entries(items[idx-1][1], lang)

def browse_topics(lang):
    pick_from_entries(STORE.entries, lang)

def show_stats():
    clear()
    stats = STORE.stats()
    print("Database statistics")
    print("-" * 60)
    for key, value in stats.items():
        print(f"{key}: {value}")
    print("\nTop categories")
    print("-" * 60)
    cat_counter = Counter(e.get("category","") for e in STORE.entries)
    for name, count in cat_counter.most_common(20):
        print(f"{count:4d}  {name}")
    print("\nDatabase files")
    print("-" * 60)
    for name in STORE.last_loaded_files:
        path = os.path.join(DB_DIR, name)
        size_mb = os.path.getsize(path) / 1024 / 1024
        print(f"{name}  ({size_mb:.2f} MB)")
    pause()

def show_integrity():
    clear()
    report = STORE.integrity_report()
    print("Integrity report")
    print("-" * 60)
    print(f"Duplicate IDs: {len(report['duplicate_ids'])}")
    print(f"Duplicate topics: {len(report['duplicate_topics'])}")
    print(f"Missing required fields: {len(report['missing_required'])}")
    print(f"Load errors: {len(report['load_errors'])}")
    if report["duplicate_ids"]:
        print("\nDuplicate IDs:")
        for item in report["duplicate_ids"][:50]:
            print("-", item)
    if report["duplicate_topics"]:
        print("\nDuplicate topics:")
        for item in report["duplicate_topics"][:50]:
            print("-", item)
    if report["missing_required"]:
        print("\nMissing required fields (first 50):")
        for entry_id, key in report["missing_required"][:50]:
            print(f"- {entry_id}: {key}")
    if report["load_errors"]:
        print("\nLoad errors:")
        for item in report["load_errors"]:
            print("-", item)
    pause()

def show_updates():
    clear()
    print("Update logs")
    print("-" * 60)
    if not os.path.isdir(UPDATES_DIR):
        print("No update log folder found.")
        pause()
        return
    logs = [name for name in sorted(os.listdir(UPDATES_DIR)) if name.endswith(".txt")]
    if not logs:
        print("No update logs found.")
        pause()
        return
    for idx, name in enumerate(logs, 1):
        print(f"{idx}. {name}")
    print("\nEnter number to read, or press Enter to return.")
    choice = input("> ").strip()
    if not choice:
        return
    if choice.isdigit():
        idx = int(choice)
        if 1 <= idx <= len(logs):
            path = os.path.join(UPDATES_DIR, logs[idx-1])
            clear()
            print(logs[idx-1])
            print("=" * len(logs[idx-1]))
            print(open(path, "r", encoding="utf-8").read())
            pause()

def launch_web_ui():
    server = ThreadingHTTPServer((WEB_HOST, WEB_PORT), OfflineWebHandler)
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    url = f"http://{WEB_HOST}:{WEB_PORT}/"
    print(f"\nLocal browser UI started at: {url}")
    opened = False
    try:
        subprocess.run(["termux-open-url", url], check=False)
        opened = True
    except Exception:
        pass
    if not opened:
        try:
            webbrowser.open(url)
        except Exception:
            pass
    print("Press Enter here to stop the local server and return to the menu.")
    pause("")
    server.shutdown()
    server.server_close()

def choose_language(current):
    clear()
    print("Choose language / Επιλογή γλώσσας")
    print("1. English")
    print("2. Ελληνικά")
    choice = input("> ").strip()
    if choice == "2":
        return "el"
    return "en"

def main():
    lang = "en"
    while True:
        clear()
        print("Offline Survival")
        print("=" * 60)
        print(f"Language: {'Ελληνικά' if lang == 'el' else 'English'}")
        print(f"Entries loaded: {len(STORE.entries)}")
        print("")
        print("1. Search")
        print("2. Browse topics")
        print("3. Browse files")
        print("4. Browse categories")
        print("5. Launch local browser UI")
        print("6. Database statistics")
        print("7. Integrity check")
        print("8. Update logs")
        print("9. Switch language")
        print("10. Reload database")
        print("0. Exit")
        choice = input("\n> ").strip()
        if choice == "1":
            query = input("Search query: ").strip()
            results = STORE.search(query, lang=lang)
            pick_from_entries(results, lang)
        elif choice == "2":
            browse_topics(lang)
        elif choice == "3":
            browse_files(lang)
        elif choice == "4":
            browse_categories(lang)
        elif choice == "5":
            launch_web_ui()
        elif choice == "6":
            show_stats()
        elif choice == "7":
            show_integrity()
        elif choice == "8":
            show_updates()
        elif choice == "9":
            lang = choose_language(lang)
        elif choice == "10":
            STORE.load()
            pause("\nDatabase reloaded. Press Enter to continue...")
        elif choice == "0":
            break

if __name__ == "__main__":
    main()
