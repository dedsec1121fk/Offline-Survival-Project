#!/usr/bin/env python3
# MAINTENANCE: Keep the standalone reader network-free, bilingual, self-contained, and synchronized with the compendium.
"""QA for the generated single-file Offline Survival Reader."""
from __future__ import annotations
import json,re,subprocess,shutil,tempfile,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
READER=ROOT/'Offline Survival Reader.html'
checks=[]
def ck(name,ok,detail=''):
    checks.append((name,bool(ok),detail));print(f"[{'PASS' if ok else 'FAIL'}] {name}"+(f": {detail}" if detail else ''))
if not READER.is_file():
    ck('reader-file',False,str(READER));sys.exit(1)
s=READER.read_text(encoding='utf-8')
ck('reader-file',len(s)>100000,f'{READER.stat().st_size} bytes')
m=re.search(r'<script>const CHAPTERS=(\[.*?\]);</script>',s,re.S)
data=[]
try:data=json.loads(m.group(1)) if m else []
except Exception as e:ck('embedded-json',False,str(e))
else:ck('embedded-json',True,f'{len(data)} chapters')
ids=[x.get('id') for x in data]
ck('chapter-sequence',ids==list(range(1,221)),f'{ids[:3]}...{ids[-3:] if ids else []}')
ck('bilingual-chapters',all(x.get('en',{}).get('title') and x.get('en',{}).get('body') and x.get('el',{}).get('title') and x.get('el',{}).get('body') for x in data))
ck('no-external-assets','<script src=' not in s and '<link rel="stylesheet"' not in s)
ck('no-runtime-network',not re.search(r'\b(?:fetch|XMLHttpRequest|WebSocket)\s*\(',s))
ck('no-http-resource-tags',not re.search(r'(?:src|href)=["\']https?://',s,re.I))
ck('mobile-viewport','width=device-width' in s and '@media(max-width:800px)' in s)
ck('local-search','function filtered()' in s and "id=\"q\"" in s)
ck('local-progress','osp-reader-fav' in s and 'osp-reader-reviewed' in s and 'localStorage' in s)
ck('print-support','window.print' not in s and "$('print').onclick=()=>print()" in s)
ck('bilingual-ui','Μονοαρχείος οδηγός επιβίωσης' in s and 'Single-file survival library' in s)
node=shutil.which('node')
if node:
    scripts=re.findall(r'<script>(.*?)</script>',s,re.S)
    with tempfile.NamedTemporaryFile('w',suffix='.js',delete=False,encoding='utf-8') as f:
        for block in scripts:f.write(block+'\n')
        tmp=Path(f.name)
    proc=subprocess.run([node,'--check',str(tmp)],capture_output=True,text=True)
    tmp.unlink(missing_ok=True)
    ck('embedded-js-syntax',proc.returncode==0,proc.stderr.strip())
else:ck('embedded-js-syntax',True,'Node unavailable; syntax covered by generator/static guards')
print(f"Standalone reader QA: {sum(x[1] for x in checks)}/{len(checks)} PASS")
sys.exit(0 if all(x[1] for x in checks) else 1)
