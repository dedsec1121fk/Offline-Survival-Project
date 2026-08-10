#!/usr/bin/env python3
# MAINTENANCE: Validate the installed/default-browser route statically; never launch or require a specific browser engine.
"""Static QA for the on-device browser diagnostics.

This test deliberately does not launch or automate a browser engine. The actual
interactive diagnostics run in Android's installed/default browser when the
user executes ``Offline Survival.py --phone-browser-test``.
"""
from __future__ import annotations
import re, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
WEB=ROOT/'web'
checks=[]
def check(name,ok,detail=''):
    checks.append((name,bool(ok),detail)); print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f": {detail}" if detail else ''))
html=(WEB/'phone-test.html').read_text(encoding='utf-8')
js=(WEB/'phone-test.js').read_text(encoding='utf-8')
server=(ROOT/'Offline Survival Web.py').read_text(encoding='utf-8')
launcher=(ROOT/'Offline Survival.py').read_text(encoding='utf-8')
check('phone-test-assets', (WEB/'phone-test.html').is_file() and (WEB/'phone-test.js').is_file())
check('phone-test-bilingual', 'Phone Browser Diagnostics' in html and 'Διαγνωστικός έλεγχος browser τηλεφώνου' in js)
check('local-api-checks', '/api/meta' in js and '/api/diagnostics' in js)
check('local-storage-check', 'localStorage.setItem' in js and 'localStorage.removeItem' in js)
check('service-worker-check', "serviceWorker' in navigator" in js and "register('/sw.js')" in js)
check('viewport-check', 'horizontal overflow' in js and 'scrollWidth' in js)
check('privacy-copy', 'not uploaded' in html and 'δεν ανεβαίνουν πουθενά' in js)
check('android-default-browser', 'termux-open-url' in server and 'android.intent.action.VIEW' in server)
check('no-python-webbrowser', 'import webbrowser' not in server and 'webbrowser.open' not in server)
check('launcher-route', '--phone-browser-test' in launcher and '--phone-test' in launcher)
# Block explicit automated desktop browser engines in active phone-QA path.
forbidden=re.findall(r'\b(?:playwright|chromium|firefox|webkit)\b', (server+'\n'+launcher+'\n'+js).casefold())
check('no-browser-engine-automation', not forbidden, ', '.join(forbidden))
print(f"Phone browser asset QA: {sum(x[1] for x in checks)}/{len(checks)} PASS")
sys.exit(0 if all(x[1] for x in checks) else 1)
