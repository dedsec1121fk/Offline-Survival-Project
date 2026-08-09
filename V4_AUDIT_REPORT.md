# v4 Engineering Audit Report — August 8, 2026

## Scope

This audit reviewed the v3 codebase used as the exact v4 baseline, then re-ran checks after each material v4 change. The review covered executable Python, browser HTML/CSS/JavaScript, state sanitization, HTTP routes, Library trust boundaries, bilingual UI keys, database integrity and newly generated Library content.

“Line-by-line” here means executable-source/static-path review plus automated checks over every relevant source file and every structured database file. It does not claim that every sentence of emergency guidance was newly fact-checked against the web on August 8; the database's existing source-validation date remains separately documented in `VALIDATION.md`.

## Defects found and corrected

### Version reporting mismatch

v3's HTTP server identified itself as 3.0 while `/api/meta` still reported Command Center version 2 in part of the inherited code path.

**Fix:** one `COMMAND_CENTER_VERSION = 4`, `SCHEMA_VERSION = 4`, and HTTP `server_version = 4.0`, with a permanent self-test for consistency.

### Monolithic browser source

The inherited UI stored roughly 147 KB of HTML/CSS/JavaScript in one page, increasing review and regression risk.

**Fix:** split HTML, CSS and JS into separate assets and added a minimal manifest/service worker.

### Mobile navigation regression

The v3 documentation said mobile navigation was horizontally scrollable, but the CSS still used a 5-column multi-row grid.

**Fix:** true one-row `flex`/`nowrap` horizontal navigation. Browser QA verifies horizontal overflow at 390 px width.

### Translation drift

Several dynamically generated labels remained hard-coded in English, including drill-history labels, coordinates, integrity labels and loading/result strings.

**Fix:** moved those strings into the EN/EL translation maps. Runtime self-test confirms translation-key parity and all `data-t` / `data-ph` references resolve in both languages.

### Weak navigation-origin sanitization

Waypoint and route coordinates were bounded, but persisted origin coordinates passed through a generic text dictionary.

**Fix:** origin latitude/longitude now require finite numeric values inside legal coordinate ranges.

### Loose date/time fields

Several dates/timestamps were previously length-limited strings only.

**Fix:** date fields now require `YYYY-MM-DD`; operational timestamps require Python ISO-compatible date-time strings. Invalid values normalize to empty strings.

### Non-finite numeric input

Generic bounded floats could receive non-finite values.

**Fix:** `NaN` and infinity are explicitly rejected to safe defaults.

### Untrusted Library content on trusted origin

User-added Library files could be served from the same origin as the Command Center.

**Fix:** direct arbitrary Library file delivery is attachment-only with a strict sandbox/no-source CSP. Text-readable files continue through the escaped JSON/text viewer. Path containment remains enforced.

### Browser backup schema drift

The v4 server/state sanitizer had already moved to schema 4, but both browser JSON export functions still stamped backups as schema 3.

**Fix:** normal and redacted exports now stamp schema 4, with a permanent self-test that compares browser-export schema markers against the server schema.

### Cross-origin state writes

The local API had no explicit browser-origin check for state-changing POSTs.

**Fix:** when `Origin` is present, it must match the request `Host`; mismatched browser writes receive HTTP 403. Default localhost mode also validates Host headers and returns HTTP 421 for unexpected authorities, reducing DNS-rebinding/Host-spoofing exposure.

### Stream disconnect handling

A client disconnect during a large file transfer could raise a write exception.

**Fix:** broken-pipe/connection-reset during streaming exits cleanly.

### Repeated integrity scans

Metadata/diagnostics could trigger repeated full database integrity work.

**Fix:** integrity result is cached per running server process.

## New v4 capability reviewed

- Resources/endurance board.
- Multi-kit builder.
- Accountability/check-in board.
- Field observation log and numeric trend chart.
- Vehicle readiness and trip-range estimate.
- GPX/GeoJSON route workspace.
- SHA-256 Library hashing.
- Bounded full-text search across readable Offline Library documents with local snippets.
- Permanent `--audit` source/content scanner.
- Previous-state rollback.
- Local diagnostics.
- 72 new Library files (48 operational cards + 24 printable forms).

## Automated QA results

At release-candidate stage:

- Full database validator: PASS.
- 2,378 EN + 2,378 GR records: PASS.
- 703 JSON files per language: PASS.
- 260 category folders per language: PASS.
- EN/GR paths, record IDs and file IDs match: PASS.
- Exact Offline Library duplicate-content groups: 0.
- Structural/self-test: 35/35 PASS.
- Isolated live API/security smoke test: 22/22 PASS.
- Browser interaction suite: 34/34 PASS.
- Deep line-by-line/content audit: PASS across 3,855 executable/config lines, 1,407 JSON files and all 210 Library files.
- Unexpected symlinks: 0.
- Unexpected external URLs in executable source: 0.
- Phone viewport tested: 390 × 844.
- Desktop viewport tested: 1440 × 900.
- Browser page errors: 0.
- Browser console errors: 0.
- Unhandled browser runtime errors: 0.

The browser interaction suite used an in-page mocked local API because the sandbox Chromium policy blocks HTTP navigation. The real localhost HTTP server was tested independently with the standard-library API smoke suite.

## Residual limitations / future hardening targets

1. The application-shell CSP still permits `'unsafe-inline'` because legacy HTML uses inline event handlers/styles. Splitting the assets in v4 is the prerequisite for removing that later.
2. State and exported backups are plaintext unless protected by the host/filesystem/storage layer.
3. There is no built-in multi-user authentication; localhost is the intended default trust boundary.
4. The service worker provides an app-shell cache, not guaranteed browser-wide offline installation behavior on every Android/browser combination.
5. Schematic route/waypoint plots are not authoritative maps.
6. Calculators and trend charts do not know real-world safety thresholds unless the user has sourced appropriate assumptions externally.
7. Emergency/reference content can age; official current guidance always takes priority.

## Repeat the audit-critical checks

```bash
python "Offline Survival.py" --check
python "Offline Survival.py" --self-test
python "Offline Survival.py" --api-test
python "Offline Survival.py" --audit
```
