# Offline Survival Project

A clean offline survival reference organized as JSON databases in English and Greek.

## Repository structure

```text
English/
  Category name/
    Subcategory name.json
Ελληνικά/
  Category name/
    Subcategory name.json
README.md
UPDATE_LOG.md
```

Both language folders use the same category and file layout so the Greek database can be compared directly with the English one.

## Current database

- Entries per language: 1752
- Source database files reorganized: 75
- Category folders: 182
- JSON database files per language: 566

## JSON format

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

## Notes

This repository is meant to stay simple: no app files, no generated cache, no search index, no exports, and no validation folders. It is only the organized knowledge database plus this README and the update log.

Emergency guidance can become outdated or differ by country. For real emergencies, follow local authorities and emergency services first.
