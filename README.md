# Offline Survival

Offline Survival is a bilingual offline-first survival knowledge system for Termux on Android.

It is designed to keep practical knowledge available when internet access is weak or absent, infrastructure is failing, hospitals are difficult to reach, or daily life is unstable for long periods.

## Project structure

- `Offline Survival.py`
- `Offline Survival Database/`
- `Offline Survival Updates/`

## Core goals

This project is built to support:

- immediate emergency response
- long blackouts and infrastructure failure
- apartment and urban hardship
- sanitation and disease prevention
- water collection, storage, and treatment
- shelter and repair discipline
- food scarcity and preservation
- first aid and medical continuity
- psychology, morale, and group stability
- communications under weak or failed networks
- high-surveillance and digital-dependency resilience
- wartime civilian continuity
- rebuilding household and small-group function over time

## Languages

The project is combined bilingual:

- English
- Greek

The main script includes language selection at startup and the knowledge database contains paired English and Greek fields.

## Main script features

`Offline Survival.py` is the main Termux interface.

Current core functions include:

- language choice at startup
- search by keyword
- search by tag
- search by category
- search by topic
- browse categories
- browse topics
- terminal reading mode
- related-topic suggestions
- export to text files in Android Downloads
- update log reading
- database statistics
- integrity checks for missing fields and duplicate IDs

## Database design

The database is split into topic-based JSON files with a stable schema built for expansion.

Common fields include:

- `id`
- `topic`
- `category`
- `subcategory`
- `tags`
- `summary_en`
- `summary_el`
- `content_en`
- `content_el`
- `steps_en`
- `steps_el`
- `warnings_en`
- `warnings_el`
- `mistakes_en`
- `mistakes_el`
- `related_topics`
- `difficulty`
- `urgency`
- `priority`
- `last_updated`
- `update_note`

## Design principles

The project is being expanded with these rules:

- practical over dramatic
- offline-friendly over dependency-heavy
- clear over bloated
- field-useful over theoretical
- bilingual parity over partial translation
- depth over duplication

The goal is not to create a toy database or a collection of filler tips.
The goal is to create a serious reference system that remains readable under stress.

## Termux notes

The project is intended for Termux on Android.

Key design choices:

- no root required
- avoids pip upgrade behavior
- dependency-light design
- UTF-8 safe for English and Greek
- readable on budget devices

## Exports

The script exports text output to:

`/storage/emulated/0/Download/Offline Survival`

## Update logs

The `Offline Survival Updates/` folder exists so future work can continue cleanly.
It tracks:

- what was added
- what was expanded
- what still needs more depth
- how duplicates were avoided

## Current development state

The repository has been receiving direct incremental pushes on `main`.
Recent work has focused on:

- broad category coverage
- deeper operational detail
- additional standalone reference files
- continuation logs for future expansion

## Ongoing priorities

The strongest next directions remain:

- improving search and reading usability further
- deepening medical quick-reference content
- expanding local ecology and food gathering safety
- adding more building-level and community-level continuity guidance
- creating denser rapid-reference material for real stress use

## Usage idea

Run the main script inside Termux from the project directory and use the menu to search, browse, read, and export content.

This project is meant to become a durable offline library for crisis, collapse, and long-term survival continuity.
