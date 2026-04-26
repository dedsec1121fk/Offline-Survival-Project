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
- pass 79 through pass84 bilingual expansion content

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

- `agriculture_soil_plants_animals_pass84.json`
- `anatomy_biology_medicine_tools_repair_and_construction.json`
- `care_navigation_community_expansion_pass81.json`
- `community_governance_conflict_records_pass84.json`
- `community_governance_learning_pass83.json`
- `community_psychology_records_expansion_pass82.json`
- `deep_resilience_community_operations_pass79.json`
- `documentation_maintenance_training_pass83.json`
- `environment_animals_farming_pass83.json`
- `environment_recovery_hazards_pass84.json`
- `food_agriculture_preservation_expansion_pass82.json`
- `food_agriculture_psychology_planning_and_daily_operations.json`
- `food_cooking_storage_pass83.json`
- `food_preservation_kitchen_planning_pass84.json`
- `long_term_rebuilding_civilization_pass83.json`
- `longterm_rebuilding_education_pass84.json`
- `medicine_care_body_systems_pass83.json`
- `navigation_communication_records_pass83.json`
- `navigation_mobility_communication_pass84.json`
- `power_energy_lighting_tools_pass84.json`
- `power_tools_lowtech_repair_pass83.json`
- `rebuilding_agriculture_environment_recovery_pass81.json`
- `rebuilding_longterm_resilience_expansion_pass82.json`
- `safe_care_medicine_records_pass84.json`
- `shelter_clothing_weather_pass83.json`
- `shelter_power_navigation_expansion_pass82.json`
- `shelter_weather_clothing_microclimate_pass84.json`
- `training_drills_offline_maintenance_pass84.json`
- `urban_greece_mediterranean_scenarios_pass84.json`
- `urban_rural_specific_scenarios_pass83.json`
- `water_fire_shelter_environment_and_records.json`
- `water_hygiene_public_health_pass83.json`
- `water_sanitation_food_energy_expansion_pass81.json`
- `water_sanitation_health_expansion_pass82.json`
- `water_sanitation_public_health_pass84.json`
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


## 2026-04-25 pass82 large expansion

This pass used the full uploaded repository zip and expanded the project far beyond pass81.

Added:

- `Offline Survival Audit.py`
- `water_sanitation_health_expansion_pass82.json`
- `food_agriculture_preservation_expansion_pass82.json`
- `shelter_power_navigation_expansion_pass82.json`
- `community_psychology_records_expansion_pass82.json`
- `rebuilding_longterm_resilience_expansion_pass82.json`

Pass82 adds 120 new bilingual English/Greek entries across water, sanitation, food, agriculture, shelter, power outage routines, navigation, community psychology, records, repair, and long-term rebuilding.

## Local audit tool

Run this in Termux from the project folder:

```bash
python "Offline Survival Audit.py"
```

If your device uses `python3`:

```bash
python3 "Offline Survival Audit.py"
```

The audit tool checks JSON loading, empty files, duplicate IDs, duplicate topics, missing English/Greek fields, wrong list field types, category counts, file counts, and writes:

```text
Offline Survival Exports/offline_survival_audit_report.txt
```

## Notes

- Update logs are stored in `Offline Survival Updates/`
- The project is designed for continued expansion without deleting useful older content
- JSON files should remain valid UTF-8 JSON arrays
- Each entry should keep English and Greek fields together for parity
- Medical content should stay non-diagnostic and should direct users toward qualified help for serious, worsening, or uncertain conditions
- The project should remain offline-first and Termux-friendly


## 2026-04-25 expanded pass83

Pass83 continues the large database expansion from pass82.

Added eight new bilingual database files:

- `water_hygiene_public_health_pass83.json`
- `food_cooking_storage_pass83.json`
- `medicine_care_body_systems_pass83.json`
- `shelter_clothing_weather_pass83.json`
- `power_tools_lowtech_repair_pass83.json`
- `navigation_communication_records_pass83.json`
- `community_governance_learning_pass83.json`
- `long_term_rebuilding_civilization_pass83.json`
- `environment_animals_farming_pass83.json`
- `urban_rural_specific_scenarios_pass83.json`
- `documentation_maintenance_training_pass83.json`

Pass83 also improves `Offline Survival Audit.py` and adds a menu option in `Offline Survival.py` to run the local audit directly.

Maintenance goals:

- keep every JSON file valid UTF-8
- keep every database file as a list of entries
- keep English and Greek fields paired
- avoid duplicate IDs and duplicate topics
- keep medical content observational and non-diagnostic
- keep tool/rebuilding content focused on repair, safety, water, shelter, food, and community resilience

## 2026-04-25 pass84 continuation expansion

Pass84 continues from pass83 and adds another large bilingual database growth pass.

Added **240 new English/Greek entries** across **12 new JSON database files**:

- `water_sanitation_public_health_pass84.json`
- `food_preservation_kitchen_planning_pass84.json`
- `safe_care_medicine_records_pass84.json`
- `shelter_weather_clothing_microclimate_pass84.json`
- `power_energy_lighting_tools_pass84.json`
- `navigation_mobility_communication_pass84.json`
- `community_governance_conflict_records_pass84.json`
- `agriculture_soil_plants_animals_pass84.json`
- `longterm_rebuilding_education_pass84.json`
- `urban_greece_mediterranean_scenarios_pass84.json`
- `environment_recovery_hazards_pass84.json`
- `training_drills_offline_maintenance_pass84.json`

Pass84 totals after validation:

- Database entries: **633**
- Database JSON files: **35**
- Categories: **40**
- Duplicate IDs: **0**
- Duplicate English topics: **0**
- Duplicate Greek topics: **0**
- Missing required fields: **0**
- Weak content fields: **0**

Pass84 also adds:

- `DATABASE_INDEX_PASS84.md`
- `Offline Survival Exports/offline_survival_audit_report_pass84.txt`
- `Offline Survival Exports/offline_survival_pass84_validation_summary.json`



## 2026-04-25 pass85 continuation

Pass85 adds another huge bilingual offline-first expansion.

- New entries added in pass85: 560
- New database files added in pass85: 28
- Total database entries after pass85: 1193
- Total database files after pass85: 63
- Total categories after pass85: 68

Pass85 focuses on water, sanitation, food, medicine/care records, shelter, energy, routes, community rules, children/elder support, agriculture, rebuilding skills, Greek apartment scenarios, rural/coastal/mountain cases, repairs, cleanup, documentation, resources, communications, household boundaries, pets, clothing, morale, and project maintenance.

Added files include `DATABASE_INDEX_PASS85.md`, `Offline Survival Exports/offline_survival_pass85_validation_summary.json`, and `Offline Survival Updates/2026-04-25_continue_huge_expansion_pass85.txt`.
