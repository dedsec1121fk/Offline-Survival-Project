# Offline Survival Project — Pass 104

**Pass 104 — complete export restore, GitHub-safe file sizes, and Pass 103 content preserved**

This release keeps the full Pass 103 knowledge base and fixes the problem that made the package look too small: the complete English and Greek field-manual exports are now included again. The project is still safe for GitHub because every individual repository file remains below 40 MB.

## Current status

| Item | Status |
|---|---:|
| Bilingual entries | **1752** |
| JSON database files | **75** |
| Categories | **182** |
| Fields per record | **48** |
| Complete English export | **13.8 MB** |
| Complete Greek export | **28.2 MB** |
| Largest repository file | **28,174,037 bytes** |
| Files over 40 MB | **0** |

## What changed in Pass 104

- Restored `Offline Survival Exports/COMPLETE_ENGLISH_FIELD_MANUAL_EXPORT.txt`.
- Restored `Offline Survival Exports/COMPLETE_GREEK_FIELD_MANUAL_EXPORT.txt`.
- Kept all Pass 103 database records, translations, sources, urgent-helper improvements and compact offline search.
- Updated the application version to **104.0 / Pass 104**.
- Added a fresh Pass 104 release validation file and SHA-256 manifest.
- Verified that no file inside the repository is bigger than 40 MB.

The ZIP may still compress smaller than expected because plain text and JSON compress very strongly. After extraction, the repository folder is much larger and includes the full export TXT files.

## Termux run command

```bash
python "Offline Survival.py"
```

## Useful direct commands

```bash
python "Offline Survival.py" --version
python "Offline Survival.py" --search "water" --lang en
python "Offline Survival.py" --search "νερο" --lang el
python "Maintenance/Check GitHub File Sizes.py"
python "Maintenance/Run Full Validation.py"
```

## GitHub-safe update note

Do **not** upload the ZIP itself as a repository file. Use the update command that unzips it and pushes the extracted project. All extracted files are below the 40 MB limit.

## Ελληνικά

Το Pass 104 κρατά όλο το περιεχόμενο του Pass 103 και επαναφέρει τις πλήρεις εξαγωγές σε TXT. Το αρχείο ZIP μπορεί να φαίνεται μικρό επειδή τα κείμενα συμπιέζονται πολύ, αλλά μετά την αποσυμπίεση υπάρχουν ξανά τα μεγάλα αρχεία εξαγωγής:

- `COMPLETE_ENGLISH_FIELD_MANUAL_EXPORT.txt`
- `COMPLETE_GREEK_FIELD_MANUAL_EXPORT.txt`

Κανένα αρχείο του repository δεν ξεπερνά τα 40 MB.
