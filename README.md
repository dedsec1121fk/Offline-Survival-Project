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

## Running in Termux

```bash
cd ~/Offline_Survival_Project_prompt_aligned_v65
python "Offline Survival.py"
```

If your device uses `python3`:

```bash
cd ~/Offline_Survival_Project_prompt_aligned_v65
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
Examples include:
- `anatomy_biology_medicine_and_field_care.json`
- `food_recipes_preservation_and_gathering.json`
- `water_fire_shelter_and_environmental_survival.json`
- `tools_repair_construction_energy_and_textiles.json`

## Notes

- Update logs are stored in `Offline Survival Updates/`
- The project is designed for continued expansion without deleting useful older content
- JSON files are kept under the size limit discussed in chat


## Current Database Layout

The database is now grouped into 3 larger domain JSON files, each kept under the per-file size ceiling while staying easier to browse in larger knowledge blocks.

- `water_fire_shelter_environment_and_records.json`
- `anatomy_biology_medicine_tools_repair_and_construction.json`
- `food_agriculture_psychology_planning_and_daily_operations.json`
