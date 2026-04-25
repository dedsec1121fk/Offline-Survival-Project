# Offline Survival

Serious bilingual offline survival guide for Termux on Android.

## Project structure

- `Offline Survival.py`
- `Offline Survival Database/`
- `Offline Survival Updates/`
- `.github/FUNDING.yml`
- `OFFICIAL_SAFETY_SOURCES.md`

## Current state

This build includes:
- split domain JSON files instead of one oversized master file
- English and Greek content across the database
- terminal interface and local browser UI
- search by keyword, category, and file
- update-log viewing inside the project
- database statistics and integrity check
- TXT export for the entire database, search results, one category, or one database file
- repaired browser UI JavaScript newline handling
- repaired core database files from the 2026-04-25 audit pass
- pass 79, pass 80, and pass 81 bilingual expansion content

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

The browser UI is intended to make searching and reading easier on mobile browsers. It is local-only and does not require a remote server.

## Exporting to TXT

From the terminal menu, choose:

```text
11. Export to TXT
```

You can export:
- the whole database
- search results
- one category
- one database file

On Android/Termux the app first tries to save exports under:

```text
/storage/emulated/0/Download/Offline Survival Exports/
```

If that path is not available, it falls back to a local project export folder.

## Database layout

Current database files:

- `water_fire_shelter_environment_and_records.json`
- `anatomy_biology_medicine_tools_repair_and_construction.json`
- `food_agriculture_psychology_planning_and_daily_operations.json`
- `deep_resilience_community_operations_pass79.json`
- `water_sanitation_food_energy_expansion_pass81.json`
- `care_navigation_community_expansion_pass81.json`
- `rebuilding_agriculture_environment_recovery_pass81.json`

## 2026-04-25 full zip expansion pass

This pass worked from the full uploaded repository zip and checked every folder/file visible in the archive:

- `.github/FUNDING.yml`
- `README.md`
- `Offline Survival.py`
- all JSON database files
- all visible TXT update logs

Main improvements:
- fixed the local browser UI JavaScript newline rendering issue
- added export-to-TXT functionality
- added 36 new bilingual knowledge entries across water, hygiene, food, energy, care, navigation, community operations, rebuilding, agriculture, environment, and long-term recovery
- added `OFFICIAL_SAFETY_SOURCES.md` for source-tracking and future verification
- added a new update log documenting this pass

## Notes

- Update logs are stored in `Offline Survival Updates/`
- The project is designed for continued expansion without deleting useful older content
- JSON files should remain valid UTF-8 JSON arrays
- Each entry should keep English and Greek fields together for parity
- Medical content should stay non-diagnostic and should direct users toward qualified help for serious, worsening, or uncertain conditions
- The project should remain offline-first and Termux-friendly
