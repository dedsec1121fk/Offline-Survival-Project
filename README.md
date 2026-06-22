# Offline Survival Project

A clean offline survival reference organized as mirrored JSON databases in English and Greek.

This repository is made for GitHub browsing and offline reuse. It contains only categorized knowledge databases and simple documentation. There are no app files, generated indexes, caches, exports, validation folders, or user-state files.

## Repository structure

```text
English/
  Category name/
    JSON database files
Ελληνικά/
  Same category name/
    Matching Greek JSON database files
README.md
UPDATE_LOG.md
```

## Current database

- Entries per language: 2308
- English JSON database files: 642
- Greek JSON database files: 642
- Mirrored category folders per language: 258
- New total-systems entries added in the latest expansion: 132
- Largest repository file: 397,010 bytes
- Maximum repository file target: below 40 MB

## What the guide covers

The guide covers immediate emergency response, earthquakes, wildfires, floods, storms, extreme heat and cold, water, food, medicine continuity, hygiene, shelter, power, communications, evacuation, animals, community coordination, documents, digital continuity, Greece-specific emergencies, long-term disruption, recovery, cleanup, rebuilding skills, and worst-case continuity.

The latest expansion adds larger full-system manuals for water, food, health, sanitation, shelter, energy, evacuation, community coordination, Greece-local survival, rebuilding, and hazard recovery. These records focus on full workflows: materials, sequence, warnings, mistakes, alternatives, failure signs, stop points, short-term use, long-term use, and recovery.

## JSON record format

Each JSON file contains a list of records. A record includes:

- `id`
- `language`
- `title`
- `category`
- `subcategory`
- `summary`
- `content`
- `difficulty`
- `urgency`
- `priority`
- `tags`
- `materials`
- `steps`
- `warnings`
- `common_mistakes`
- `alternatives`
- `failure_signs`
- `when_not_to_use`
- `short_term`
- `long_term`
- `if_method_fails`
- `environment_notes`
- `related_topics`
- `sources`
- `last_updated`

## Use

Open the language folder you want, choose a category, and read the JSON records. The English and Greek folders are mirrored by path and record ID so the same subject can be compared between languages.

## Safety note

This guide is an offline reference for preparation, organization, and safer decision-making. It does not replace emergency services, medical professionals, engineers, electricians, utility workers, fire services, police, coast guard, or official civil-protection instructions.
