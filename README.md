<div align="center">

# Offline Survival Project

**Bilingual, fully offline emergency-preparedness knowledge base and terminal reader.**

**Δίγλωσση, πλήρως εκτός σύνδεσης βάση γνώσεων προετοιμασίας και εφαρμογή ανάγνωσης τερματικού.**

[English](#english) • [Ελληνικά](#ελληνικά)

</div>

---

# English

## Overview

Offline Survival Project is a structured English and Greek reference for emergency preparation, immediate response, continuity, recovery, and long-term disruption. The repository includes two mirrored JSON databases and a dependency-free Python application that can search, find, browse, validate, and read the information entirely offline.

It is designed for Termux on Android, Linux, Windows, macOS, GitHub browsing, offline storage, and devices kept as emergency references. After the project is downloaded, the knowledge base does not need an account, API key, server, or internet connection.

## Main features

- **Fully offline:** no sign-in, API key, server, tracking, or network connection.
- **Bilingual database:** complete English and Greek record sets with matching IDs and mirrored file paths.
- **Bilingual interface:** Settings switches both the application language and active database.
- **Relevant search:** checks titles, categories, summaries, tags, IDs, and paths first, then searches every field when needed.
- **Accent-insensitive matching:** Greek searches work with or without written accent marks.
- **Category browser:** lists or filters all categories and keeps the current list open after reading a record.
- **File finder:** searches JSON names, paths, titles, and all content stored in each file. Pressing Enter lists every file.
- **Paged reader:** long records and raw JSON are split into readable pages instead of flooding a small terminal.
- **Record-ID lookup:** accepts a complete or partial record ID.
- **Random topic:** useful for study, practice, and discovering unfamiliar material.
- **Built-in integrity check:** validates both databases and confirms that files and record IDs remain mirrored.
- **No third-party packages:** only the Python standard library is used.
- **Persistent local settings:** language, list size, and screen-clearing preference are saved outside the repository.

## Repository structure

```text
Offline-Survival-Project-main/
├── main.py                 # Recommended application launcher
├── Offline Survival.py     # Compatibility launcher for the original name
├── README.md
├── English/
│   └── Category folder/
│       └── JSON knowledge files
└── Ελληνικά/
    └── Matching category folder/
        └── Matching Greek JSON knowledge files
```

`main.py` is the primary launcher. `Offline Survival.py` remains available so older commands and shortcuts continue to work.

## Database size and integrity

Each language currently contains:

- **2,308 records**
- **642 JSON files**
- **258 category folders**

The English and Greek trees have matching relative paths, matching record counts, matching record IDs, and matching IDs inside each corresponding file. Every JSON file has been checked for valid syntax, required fields, empty required values, duplicate IDs, and duplicate titles.

## Quick start

### Termux

```bash
pkg update -y && pkg install python -y
cd ~/Offline-Survival-Project-main
python main.py
```

If the folder is stored elsewhere, replace the `cd` path with its actual location.

### Linux or macOS

Install Python 3.9 or newer, open a terminal in the extracted project folder, and run:

```bash
python3 main.py
```

### Windows

Install Python 3.9 or newer, open Command Prompt or PowerShell in the extracted project folder, and run:

```powershell
python main.py
```

The compatibility command also remains available:

```bash
python "Offline Survival.py"
```

## Controls

- Enter a **number** to open a visible menu or list item.
- Press **n** or **Enter** for the next page.
- Press **p** for the previous page.
- Enter **0** or **q** to go back or exit.
- `next`, `previous`, `back`, and their supported Greek equivalents also work.
- `Ctrl+C` exits safely from any input prompt.

List numbers always refer to the items currently visible on the screen. After a record is closed, the application returns to the same results page instead of discarding the search.

## Main menu

1. **Search the knowledge base** — searches the active language database.
2. **Browse categories** — shows all categories or filters them using one or more words.
3. **Find and read a JSON file** — locates files, browses their records, or reads raw JSON.
4. **Open a record by ID** — finds complete, beginning, or partial ID matches.
5. **Read a random topic** — opens a random record and optionally another one.
6. **Settings** — changes language, results per page, or screen clearing.
7. **Help and controls** — shows usage and safety information inside the application.
8. **Check database integrity** — validates every JSON file in both languages.
0. **Exit** — closes the application.

## Search behavior

Search is case-insensitive and accent-insensitive. It first prioritizes matches in:

- title
- category and subcategory
- summary
- tags
- record ID
- file name and path

When the complete search phrase is not found in those high-relevance fields, the application searches all remaining fields, including full guidance, materials, steps, warnings, alternatives, failure signs, related topics, and sources.

## Settings and privacy

The application stores only local preferences in:

```text
~/.offline_survival_project/settings.json
```

The file is outside the repository. It contains only the selected language, results-per-page value, and screen-clearing preference. Searches, viewed records, and personal information are not logged, transmitted, or collected.

To show the first-launch language screen again, delete that settings file and restart the application.

## Knowledge coverage

The databases include material related to:

- immediate response and the first minutes of an emergency
- earthquakes and structural safety
- wildfire, fire, smoke, flood, storm, heat, cold, and air hazards
- water collection, storage, treatment, quality, and distribution
- food safety, cooking, preservation, rationing, and production
- health continuity, medicine storage, first aid support, hygiene, and sanitation
- shelter, ventilation, power, lighting, utilities, and outage planning
- communication, radio routines, records, maps, and navigation
- evacuation, transport, accessibility, children, and older adults
- pets, livestock, agriculture, soil, seeds, and animal care
- community coordination, welfare checks, fairness, morale, and conflict reduction
- financial, document, and digital continuity
- Greece-specific conditions, apartments, islands, ferries, and local emergencies
- repair, cleanup, recovery, rebuilding, and long-term continuity

## JSON record format

A record contains structured fields such as:

```text
id
language
title
category
subcategory
summary
content
difficulty
urgency
priority
tags
materials
steps
warnings
common_mistakes
alternatives
failure_signs
when_not_to_use
short_term
long_term
if_method_fails
environment_notes
related_topics
sources
last_updated
```

The reader automatically handles text, lists, and structured JSON values.

## Troubleshooting

- **`python: command not found`** — install Python, or try `python3 main.py`.
- **Language folder missing** — keep `main.py`, `English`, and `Ελληνικά` in the same project folder.
- **Unreadable or crowded terminal** — reduce Results per list page or disable/enable screen clearing in Settings.
- **Settings do not save** — confirm that the current user can write to their home directory.
- **Damaged data suspected** — run option **8. Check database integrity** from the main menu.

## Safety notice

This project is an offline preparation and reference aid. It does not replace emergency services or qualified medical, engineering, electrical, utility, fire, police, coast guard, veterinary, agricultural, or civil-protection guidance.

During a real emergency, follow official instructions and use qualified assistance whenever it is available. Do not attempt a method when the situation, equipment, materials, environment, or your training makes it unsafe.

---

# Ελληνικά

## Επισκόπηση

Το Offline Survival Project είναι μια οργανωμένη πηγή αναφοράς στα Αγγλικά και στα Ελληνικά για προετοιμασία έκτακτης ανάγκης, άμεση αντίδραση, συνέχεια βασικών λειτουργιών, αποκατάσταση και μακροχρόνιες διακοπές. Το αποθετήριο περιλαμβάνει δύο κατοπτρισμένες βάσεις JSON και μια αυτόνομη εφαρμογή Python που αναζητά, εντοπίζει, περιηγείται, ελέγχει και διαβάζει τις πληροφορίες πλήρως εκτός σύνδεσης.

Έχει σχεδιαστεί για Termux σε Android, Linux, Windows, macOS, περιήγηση μέσω GitHub, αποθήκευση χωρίς σύνδεση και συσκευές που διατηρούνται ως πηγές αναφοράς έκτακτης ανάγκης. Μετά τη λήψη του έργου, η βάση γνώσεων δεν χρειάζεται λογαριασμό, κλειδί API, διακομιστή ή σύνδεση στο διαδίκτυο.

## Κύριες δυνατότητες

- **Πλήρης λειτουργία εκτός σύνδεσης:** χωρίς σύνδεση χρήστη, κλειδί API, διακομιστή, παρακολούθηση ή δίκτυο.
- **Δίγλωσση βάση δεδομένων:** πλήρη σύνολα εγγραφών στα Αγγλικά και στα Ελληνικά, με ίδια IDs και κατοπτρισμένες διαδρομές.
- **Δίγλωσσο περιβάλλον:** οι Ρυθμίσεις αλλάζουν ταυτόχρονα τη γλώσσα της εφαρμογής και την ενεργή βάση.
- **Σχετική αναζήτηση:** ελέγχει πρώτα τίτλους, κατηγορίες, συνόψεις, ετικέτες, IDs και διαδρομές και, όταν χρειάζεται, όλα τα πεδία.
- **Αναζήτηση χωρίς εξάρτηση από τόνους:** οι ελληνικές αναζητήσεις λειτουργούν με ή χωρίς γραμμένους τόνους.
- **Περιήγηση κατηγοριών:** εμφανίζει ή φιλτράρει όλες τις κατηγορίες και διατηρεί ανοιχτή την τρέχουσα λίστα μετά την ανάγνωση.
- **Εύρεση αρχείων:** αναζητά ονόματα JSON, διαδρομές, τίτλους και όλο το περιεχόμενο κάθε αρχείου. Με Enter εμφανίζονται όλα τα αρχεία.
- **Ανάγνωση σε σελίδες:** οι μεγάλες εγγραφές και το αρχικό JSON χωρίζονται σε αναγνώσιμες σελίδες αντί να γεμίζουν το τερματικό.
- **Εύρεση με ID:** δέχεται ολόκληρο ή μέρος του ID μιας εγγραφής.
- **Τυχαίο θέμα:** χρήσιμο για μελέτη, εξάσκηση και ανακάλυψη άγνωστου υλικού.
- **Ενσωματωμένος έλεγχος ακεραιότητας:** ελέγχει και τις δύο βάσεις και επιβεβαιώνει ότι αρχεία και IDs παραμένουν κατοπτρισμένα.
- **Χωρίς εξωτερικά πακέτα:** χρησιμοποιείται μόνο η τυπική βιβλιοθήκη της Python.
- **Μόνιμες τοπικές ρυθμίσεις:** η γλώσσα, το μέγεθος λίστας και ο καθαρισμός οθόνης αποθηκεύονται έξω από το αποθετήριο.

## Δομή αποθετηρίου

```text
Offline-Survival-Project-main/
├── main.py                 # Προτεινόμενο κύριο αρχείο εκκίνησης
├── Offline Survival.py     # Συμβατότητα με το αρχικό όνομα
├── README.md
├── English/
│   └── Φάκελος κατηγορίας/
│       └── Αρχεία γνώσεων JSON
└── Ελληνικά/
    └── Αντίστοιχος φάκελος κατηγορίας/
        └── Αντίστοιχα ελληνικά αρχεία JSON
```

Το `main.py` είναι το κύριο αρχείο εκκίνησης. Το `Offline Survival.py` παραμένει διαθέσιμο ώστε παλιότερες εντολές και συντομεύσεις να συνεχίσουν να λειτουργούν.

## Μέγεθος και ακεραιότητα βάσης

Κάθε γλώσσα περιλαμβάνει αυτή τη στιγμή:

- **2.308 εγγραφές**
- **642 αρχεία JSON**
- **258 φακέλους κατηγοριών**

Οι αγγλικές και ελληνικές δομές έχουν ίδιες σχετικές διαδρομές, ίδιο αριθμό εγγραφών, ίδια IDs και ίδια IDs μέσα σε κάθε αντίστοιχο αρχείο. Όλα τα JSON έχουν ελεγχθεί για έγκυρη σύνταξη, υποχρεωτικά πεδία, κενές υποχρεωτικές τιμές, διπλότυπα IDs και διπλότυπους τίτλους.

## Γρήγορη εκκίνηση

### Termux

```bash
pkg update -y && pkg install python -y
cd ~/Offline-Survival-Project-main
python main.py
```

Αν ο φάκελος βρίσκεται αλλού, αντικατάστησε τη διαδρομή της εντολής `cd` με την πραγματική του θέση.

### Linux ή macOS

Εγκατέστησε Python 3.9 ή νεότερη, άνοιξε τερματικό μέσα στον αποσυμπιεσμένο φάκελο του έργου και εκτέλεσε:

```bash
python3 main.py
```

### Windows

Εγκατέστησε Python 3.9 ή νεότερη, άνοιξε Command Prompt ή PowerShell μέσα στον αποσυμπιεσμένο φάκελο και εκτέλεσε:

```powershell
python main.py
```

Παραμένει διαθέσιμη και η εντολή συμβατότητας:

```bash
python "Offline Survival.py"
```

## Χειρισμός

- Γράψε έναν **αριθμό** για να ανοίξεις μια ορατή επιλογή μενού ή λίστας.
- Πάτησε **n** ή **Enter** για την επόμενη σελίδα.
- Πάτησε **p** για την προηγούμενη σελίδα.
- Γράψε **0** ή **q** για επιστροφή ή έξοδο.
- Λειτουργούν επίσης τα `next`, `previous`, `back` και οι υποστηριζόμενες ελληνικές ισοδύναμες εντολές.
- Το `Ctrl+C` κλείνει με ασφάλεια από οποιοδήποτε πεδίο εισαγωγής.

Οι αριθμοί λίστας αντιστοιχούν πάντα στα στοιχεία που φαίνονται εκείνη τη στιγμή στην οθόνη. Μετά το κλείσιμο μιας εγγραφής, η εφαρμογή επιστρέφει στην ίδια σελίδα αποτελεσμάτων αντί να διαγράφει την αναζήτηση.

## Κεντρικό μενού

1. **Αναζήτηση στη βάση γνώσεων** — αναζητά στην ενεργή γλωσσική βάση.
2. **Περιήγηση στις κατηγορίες** — εμφανίζει όλες τις κατηγορίες ή τις φιλτράρει με λέξεις.
3. **Εύρεση και ανάγνωση αρχείου JSON** — εντοπίζει αρχεία, εμφανίζει εγγραφές ή διαβάζει το αρχικό JSON.
4. **Άνοιγμα εγγραφής με ID** — βρίσκει πλήρεις, αρχικές ή μερικές αντιστοιχίες ID.
5. **Ανάγνωση τυχαίου θέματος** — ανοίγει τυχαία εγγραφή και προαιρετικά άλλη μία.
6. **Ρυθμίσεις** — αλλάζει γλώσσα, αποτελέσματα ανά σελίδα ή καθαρισμό οθόνης.
7. **Βοήθεια και χειρισμός** — εμφανίζει πληροφορίες χρήσης και ασφάλειας.
8. **Έλεγχος ακεραιότητας βάσης** — ελέγχει κάθε αρχείο JSON και στις δύο γλώσσες.
0. **Έξοδος** — κλείνει την εφαρμογή.

## Λειτουργία αναζήτησης

Η αναζήτηση δεν επηρεάζεται από πεζά ή κεφαλαία και δεν απαιτεί τόνους. Δίνει πρώτα προτεραιότητα σε αντιστοιχίες στα εξής:

- τίτλος
- κατηγορία και υποκατηγορία
- σύνοψη
- ετικέτες
- ID εγγραφής
- όνομα και διαδρομή αρχείου

Όταν η πλήρης φράση δεν υπάρχει σε αυτά τα πεδία υψηλής σχετικότητας, η εφαρμογή ελέγχει όλα τα υπόλοιπα πεδία, όπως πλήρεις οδηγίες, υλικά, βήματα, προειδοποιήσεις, εναλλακτικές, ενδείξεις αποτυχίας, σχετικά θέματα και πηγές.

## Ρυθμίσεις και ιδιωτικότητα

Η εφαρμογή αποθηκεύει μόνο τοπικές προτιμήσεις στη διαδρομή:

```text
~/.offline_survival_project/settings.json
```

Το αρχείο βρίσκεται έξω από το αποθετήριο. Περιέχει μόνο την επιλεγμένη γλώσσα, τον αριθμό αποτελεσμάτων ανά σελίδα και την προτίμηση καθαρισμού οθόνης. Οι αναζητήσεις, οι εγγραφές που διαβάζονται και τα προσωπικά δεδομένα δεν καταγράφονται, δεν αποστέλλονται και δεν συλλέγονται.

Για να εμφανιστεί ξανά η επιλογή γλώσσας πρώτης εκκίνησης, διέγραψε αυτό το αρχείο ρυθμίσεων και επανεκκίνησε την εφαρμογή.

## Θεματολογία γνώσεων

Οι βάσεις περιλαμβάνουν υλικό σχετικό με:

- άμεση αντίδραση και τα πρώτα λεπτά μιας έκτακτης ανάγκης
- σεισμούς και δομική ασφάλεια
- δασικές πυρκαγιές, φωτιά, καπνό, πλημμύρες, καταιγίδες, ζέστη, κρύο και κινδύνους αέρα
- συλλογή, αποθήκευση, επεξεργασία, ποιότητα και διανομή νερού
- ασφάλεια τροφίμων, μαγείρεμα, συντήρηση, δελτίο και παραγωγή
- συνέχεια υγειονομικής φροντίδας, αποθήκευση φαρμάκων, υποστήριξη πρώτων βοηθειών, υγιεινή και αποχέτευση
- καταφύγιο, αερισμό, ενέργεια, φωτισμό, βασικά δίκτυα και σχεδιασμό διακοπών
- επικοινωνία, ραδιοφωνικές ρουτίνες, αρχεία, χάρτες και πλοήγηση
- εκκένωση, μεταφορά, προσβασιμότητα, παιδιά και ηλικιωμένους
- κατοικίδια, κτηνοτροφία, γεωργία, χώμα, σπόρους και φροντίδα ζώων
- συντονισμό κοινότητας, ελέγχους ευημερίας, δικαιοσύνη, ηθικό και μείωση συγκρούσεων
- οικονομική, εγγράφων και ψηφιακή συνέχεια
- ειδικές συνθήκες της Ελλάδας, πολυκατοικίες, νησιά, πλοία και τοπικές έκτακτες ανάγκες
- επισκευή, καθαρισμό, αποκατάσταση, ανασυγκρότηση και μακροχρόνια συνέχεια

## Μορφή εγγραφής JSON

Μια εγγραφή περιλαμβάνει οργανωμένα πεδία όπως:

```text
id
language
title
category
subcategory
summary
content
difficulty
urgency
priority
tags
materials
steps
warnings
common_mistakes
alternatives
failure_signs
when_not_to_use
short_term
long_term
if_method_fails
environment_notes
related_topics
sources
last_updated
```

Η εφαρμογή ανάγνωσης διαχειρίζεται αυτόματα κείμενο, λίστες και οργανωμένες τιμές JSON.

## Αντιμετώπιση προβλημάτων

- **`python: command not found`** — εγκατέστησε Python ή δοκίμασε `python3 main.py`.
- **Λείπει φάκελος γλώσσας** — κράτησε τα `main.py`, `English` και `Ελληνικά` στον ίδιο φάκελο έργου.
- **Δυσανάγνωστο ή γεμάτο τερματικό** — μείωσε τα αποτελέσματα ανά σελίδα ή άλλαξε τον καθαρισμό οθόνης στις Ρυθμίσεις.
- **Οι ρυθμίσεις δεν αποθηκεύονται** — επιβεβαίωσε ότι ο τρέχων χρήστης μπορεί να γράψει στον προσωπικό του φάκελο.
- **Υποψία κατεστραμμένων δεδομένων** — εκτέλεσε την επιλογή **8. Έλεγχος ακεραιότητας βάσης**.

## Σημείωση ασφάλειας

Το έργο αποτελεί βοήθημα προετοιμασίας και αναφοράς εκτός σύνδεσης. Δεν αντικαθιστά τις υπηρεσίες έκτακτης ανάγκης ούτε την καθοδήγηση αρμόδιων επαγγελματιών υγείας, μηχανικών, ηλεκτρολόγων, τεχνικών δικτύων, πυροσβεστικής, αστυνομίας, λιμενικού, κτηνιάτρων, γεωπόνων ή πολιτικής προστασίας.

Σε πραγματική κατάσταση έκτακτης ανάγκης, ακολούθησε τις επίσημες οδηγίες και χρησιμοποίησε ειδικευμένη βοήθεια όταν είναι διαθέσιμη. Μην επιχειρείς μια μέθοδο όταν η κατάσταση, ο εξοπλισμός, τα υλικά, το περιβάλλον ή η εκπαίδευσή σου δεν την καθιστούν ασφαλή.
