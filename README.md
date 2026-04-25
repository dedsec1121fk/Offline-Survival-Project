# Offline Survival

Serious bilingual offline survival guide for Termux on Android.

## Project structure

- `Offline Survival.py`
- `Offline Survival Database/`
- `Offline Survival Updates/`

## Current state

This build includes:
- split domain JSON files instead of one oversized master file
- English and Greek content across the database
- terminal interface and local browser UI
- search by keyword, category, and file
- update-log viewing inside the project
- repaired core database files from the 2026-04-25 audit pass
- additional bilingual community operations knowledge added as pass 79

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

That UI is intended to make searching and reading easier on mobile browsers.

## Database layout

The database is kept in descriptive split files so no single JSON approaches the agreed size ceiling.
Current visible layout:

- `water_fire_shelter_environment_and_records.json`
- `anatomy_biology_medicine_tools_repair_and_construction.json`
- `food_agriculture_psychology_planning_and_daily_operations.json`
- `deep_resilience_community_operations_pass79.json`

## 2026-04-25 audit and repair pass

This pass checked the exposed repository files and the loader behavior. The main Python app loads every `.json` file inside `Offline Survival Database/`, so new database files can be added without changing the loader.

The three core database files were repaired from empty content into valid bilingual JSON entries:

- water, fire, shelter, environment, and records
- anatomy, biology, medicine, tools, repair, and construction
- food, agriculture, psychology, planning, and daily operations

A supplemental pass 79 database file was also added for household, neighborhood, sanitation, medicine recordkeeping, food safety, and low-power communication operations.

## Notes

- Update logs are stored in `Offline Survival Updates/`
- The project is designed for continued expansion without deleting useful older content
- JSON files should remain valid UTF-8 JSON arrays
- Each entry should keep English and Greek fields together for parity
- The project should remain offline-first and Termux-friendly
