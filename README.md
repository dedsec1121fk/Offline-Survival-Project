# Offline Survival

Serious bilingual offline survival guide for Termux on Android.

## Project structure

- `Offline Survival.py`
- `Offline Survival Database/`
- `Offline Survival Updates/`
- `OFFICIAL_SAFETY_SOURCES.md`

## Current state

This build includes:
- English and Greek survival knowledge
- terminal menu and local browser UI
- search by keyword, category, and file
- database statistics and integrity check
- update-log viewing
- TXT export from inside the main script
- cleaned duplicate/repeated generated text and verified bilingual fields

## Running in Termux

```bash
cd ~/Offline-Survival-Project
python "Offline Survival.py"
```

If your device uses `python3`:

```bash
cd ~/Offline-Survival-Project
python3 "Offline Survival.py"
```

## Browser UI

From the terminal menu, choose the local browser UI option.
The app serves a local page on:

```text
http://127.0.0.1:8765/
```

## Notes

- The project is offline-first.
- The database is split into JSON files inside `Offline Survival Database/`.
- Keep English and Greek fields together when adding new entries.
- Keep advice cautious and practical. Do not replace emergency services, doctors, pharmacists, electricians, gas technicians, structural engineers, or local authorities.
