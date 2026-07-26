<div align="center">

# Offline Survival Project

**Bilingual offline emergency-preparedness reference and terminal reader for English and Greek.**

**Δίγλωσση βάση αναφοράς έκτακτης ανάγκης και εφαρμογή τερματικού, πλήρως εκτός σύνδεσης.**

[English](#english) • [Ελληνικά](#ελληνικά)

</div>

---

# English

## What it is

Offline Survival Project is a dependency-free Python application with mirrored English and Greek JSON knowledge bases. It is designed for Termux on Android, Linux, Windows, macOS, offline storage, and devices kept as emergency references.

After download, the application does not require an account, API key, server, analytics service, or internet connection.

## Important correction

The project now has **one Python script only**:

```text
Offline Survival.py
```

The former `main.py` and compatibility launcher were merged. The Greek database folder was also corrected from an encoded folder name to the real `Ελληνικά` name.

## Current database

Each language contains:

- **2,378 records**
- **703 JSON files**
- **260 category folders**
- **10 mirrored, manually reviewed emergency-essential cards**
- **60 mirrored food-growing and safe-preservation guides**

The complete project therefore contains **4,756 language-specific records** across the mirrored English and Greek databases.

## Main features

- Fully offline operation
- Complete English and Greek interface
- Mirrored English and Greek database paths and record IDs
- Accent-insensitive Greek search
- Search across titles, summaries, categories, IDs, tags, paths, steps, warnings, sources, and all other fields
- Category and file browser
- Direct record-ID lookup
- Random topic reader
- Small-terminal pagination
- Local settings with no activity logging
- Dedicated **Verified emergency essentials** menu
- Dedicated **Food growing and safe preservation** menu
- Strong database and source validator
- No third-party Python packages

## Verified emergency essentials

The dedicated menu contains concise cards for:

1. Greece emergency calls and 112 alerts
2. Household emergency planning and supply kits
3. Earthquake immediate actions
4. Flood-route and electrical safety
5. Wildfire warning and evacuation readiness
6. Emergency drinking-water safety
7. Food safety during power outages
8. Generator and carbon-monoxide safety
9. Heat-illness recognition and escalation
10. Poisoning response and the Greek Poison Centre

These cards were cross-checked against current official guidance from Greek Civil Protection, the Greek Ministry of Health, CDC/NIOSH, and Ready.gov on **July 26, 2026**.

## Food growing and safe preservation

Menu option **7** opens 60 detailed, mirrored guides designed for household, balcony, container, raised-bed, and small-garden use. They are grouped into:

- 7 planning and season-management guides
- 7 soil, compost, mulch, salinity, and raised-bed guides
- 9 container, irrigation, rainwater, wastewater, heat, balcony, and drought guides
- 7 seed inventory, germination, propagation, seed-saving, and storage guides
- 11 crop and pollination guides
- 6 integrated pest and disease-management guides
- 13 harvesting, cooling, freezing, drying, pickling, fermenting, canning, sprout-safety, and botulism guides

The material emphasizes conservative small trials, reliable water, correct plant identity, clean tools, product-label compliance, and current tested food-preservation recipes. It does not present exact planting dates as universal: Mediterranean heat, altitude, frost, wind, shade, local restrictions, and the actual microclimate must be considered.

The new collection was reviewed against official material from FAO, USDA/NAL/NRCS/ARS, EPA, WHO, CDC, Greece's Ministry of Rural Development and Food, and the National Center for Home Food Preservation. Important safety boundaries include:

- Roof-collected rainwater is not automatically suitable for edible crops; verified safe water is preferred and local health guidance takes priority.
- Untreated sewage, floodwater, and chemically contaminated water must not be improvised as irrigation water.
- Raw sprouts carry a foodborne-illness risk; higher-risk people should choose thoroughly cooked sprouts or another cooked crop.
- Low-acid vegetables require a current tested pressure-canning process, not boiling-water canning.
- Pickling, fermenting, drying, freezing, and canning instructions must come from a current tested recipe for the exact product and method.

## Repository structure

```text
Offline-Survival-Project-main/
├── Offline Survival.py
├── README.md
├── VALIDATION.md
├── English/
│   └── Category folder/
│       └── JSON knowledge files
└── Ελληνικά/
    └── Matching category folder/
        └── Matching Greek JSON knowledge files
```

## Quick start

### Termux

```bash
pkg update -y && pkg install python -y
cd ~/Offline-Survival-Project-main
python "Offline Survival.py"
```

### Linux or macOS

```bash
python3 "Offline Survival.py"
```

### Windows

```powershell
python "Offline Survival.py"
```

Python 3.9 or newer is recommended.

## Command-line validation

Run the complete non-interactive validation:

```bash
python "Offline Survival.py" --check
```

The command prints a JSON report and returns:

- Exit code `0` when every check passes
- Exit code `2` when any database, parity, date, source, language, or type check fails

Show only database totals:

```bash
python "Offline Survival.py" --stats
```

Show command help:

```bash
python "Offline Survival.py" --help
```

## Main menu

1. Search the knowledge base
2. Browse categories
3. Find and read a JSON file
4. Open a record by ID
5. Read a random topic
6. Verified emergency essentials
7. Food growing and safe preservation
8. Settings
9. Help and controls
10. Check database integrity
0. Exit

## Controls

- Enter a visible number to open an item.
- Use `n` or Enter for the next page.
- Use `p` for the previous page.
- Use `0` or `q` to return.
- `Ctrl+C` exits safely.

## What the validator checks

Every record in both languages is checked for:

- Valid JSON syntax and list structure
- Required fields and non-empty required values
- Correct field data types
- Unique record IDs and titles
- Correct English or Greek language value
- Valid ISO update dates that are not in the future
- Non-empty source lists
- Plain HTTPS source URLs
- Sources restricted to approved official domains
- Matching English and Greek file paths
- Matching bilingual record IDs
- Matching record IDs inside corresponding files

The latest packaged version passes all checks with zero reported errors. Details and validation limits are documented in `VALIDATION.md`.

## Settings and privacy

Only these local preferences are stored:

```text
~/.offline_survival_project/settings.json
```

The file contains the selected language, results-per-page value, and screen-clearing preference. Searches, viewed records, personal details, and usage history are not collected or transmitted.

## Safety notice

This project is a preparation and reference aid. It does not replace emergency services, official alerts, or qualified medical, engineering, electrical, utility, fire, police, coast-guard, veterinary, agricultural, or civil-protection guidance.

For an immediate emergency in Greece or elsewhere in the European Union, call **112**. For suspected poisoning in Greece, the Ministry of Health lists the Poison Centre at **210 7793777**, operating 24 hours a day, 7 days a week.

Follow live official instructions whenever they differ from stored offline material.

---

# Ελληνικά

## Τι είναι

Το Offline Survival Project είναι μια αυτόνομη εφαρμογή Python με κατοπτρισμένες βάσεις γνώσεων JSON στα Αγγλικά και στα Ελληνικά. Έχει σχεδιαστεί για Termux σε Android, Linux, Windows, macOS, αποθήκευση χωρίς σύνδεση και συσκευές που διατηρούνται ως πηγές αναφοράς έκτακτης ανάγκης.

Μετά τη λήψη δεν χρειάζεται λογαριασμό, κλειδί API, διακομιστή, analytics ή σύνδεση στο διαδίκτυο.

## Σημαντική διόρθωση

Το έργο έχει πλέον **μόνο ένα Python script**:

```text
Offline Survival.py
```

Το παλιό `main.py` και ο compatibility launcher ενώθηκαν. Διορθώθηκε επίσης ο κωδικοποιημένος φάκελος της ελληνικής βάσης στο πραγματικό όνομα `Ελληνικά`.

## Τρέχουσα βάση

Κάθε γλώσσα περιέχει:

- **2.378 εγγραφές**
- **703 αρχεία JSON**
- **260 φακέλους κατηγοριών**
- **10 κατοπτρισμένες και χειροκίνητα ελεγμένες κάρτες βασικών ενεργειών**
- **60 κατοπτρισμένους οδηγούς καλλιέργειας και ασφαλούς διατήρησης τροφίμων**

Συνολικά το έργο περιέχει **4.756 γλωσσικές εγγραφές** στις κατοπτρισμένες αγγλικές και ελληνικές βάσεις.

## Κύριες δυνατότητες

- Πλήρης λειτουργία εκτός σύνδεσης
- Πλήρες αγγλικό και ελληνικό περιβάλλον
- Κατοπτρισμένες διαδρομές και IDs
- Ελληνική αναζήτηση με ή χωρίς τόνους
- Αναζήτηση σε τίτλους, συνόψεις, κατηγορίες, IDs, ετικέτες, διαδρομές, βήματα, προειδοποιήσεις, πηγές και όλα τα υπόλοιπα πεδία
- Περιήγηση κατηγοριών και αρχείων
- Άμεση αναζήτηση με ID
- Τυχαίο θέμα
- Σελιδοποίηση για μικρές οθόνες τερματικού
- Τοπικές ρυθμίσεις χωρίς καταγραφή δραστηριότητας
- Ξεχωριστό μενού **Επαληθευμένα βασικά έκτακτης ανάγκης**
- Ξεχωριστό μενού **Καλλιέργεια και ασφαλής διατήρηση τροφίμων**
- Ενισχυμένος έλεγχος βάσης και πηγών
- Χωρίς πακέτα τρίτων

## Επαληθευμένα βασικά έκτακτης ανάγκης

Το ειδικό μενού περιλαμβάνει κάρτες για:

1. Κλήσεις έκτακτης ανάγκης και ειδοποιήσεις 112
2. Οικιακό σχέδιο και κιτ προετοιμασίας
3. Άμεσες ενέργειες σε σεισμό
4. Ασφάλεια διαδρομής και ηλεκτρισμού σε πλημμύρα
5. Ετοιμότητα για δασική πυρκαγιά και εκκένωση
6. Ασφάλεια πόσιμου νερού
7. Ασφάλεια τροφίμων σε διακοπή ρεύματος
8. Γεννήτριες και μονοξείδιο του άνθρακα
9. Αναγνώριση θερμικής νόσου
10. Δηλητηρίαση και Κέντρο Δηλητηριάσεων

Οι κάρτες διασταυρώθηκαν με τρέχουσες επίσημες οδηγίες της Ελληνικής Πολιτικής Προστασίας, του Υπουργείου Υγείας, του CDC/NIOSH και του Ready.gov στις **26 Ιουλίου 2026**.

## Καλλιέργεια και ασφαλής διατήρηση τροφίμων

Η επιλογή **7** ανοίγει 60 αναλυτικούς και κατοπτρισμένους οδηγούς για οικιακή καλλιέργεια, μπαλκόνια, δοχεία, υπερυψωμένα παρτέρια και μικρούς κήπους. Περιλαμβάνονται:

- 7 οδηγοί σχεδιασμού και εποχών
- 7 οδηγοί εδάφους, κομπόστ, εδαφοκάλυψης, αλατότητας και υπερυψωμένων παρτεριών
- 9 οδηγοί δοχείων, άρδευσης, βρόχινου νερού, λυμάτων, ζέστης, μπαλκονιού και ξηρασίας
- 7 οδηγοί αποθέματος σπόρων, βλάστησης, πολλαπλασιασμού, διατήρησης και αποθήκευσης σπόρων
- 11 οδηγοί καλλιεργειών και επικονίασης
- 6 οδηγοί ολοκληρωμένης φυτοπροστασίας
- 13 οδηγοί συγκομιδής, ψύξης, κατάψυξης, ξήρανσης, τουρσιών, ζύμωσης, κονσερβοποίησης, ασφάλειας φύτρων και αλλαντίασης

Το υλικό δίνει έμφαση σε μικρές ελεγχόμενες δοκιμές, αξιόπιστο νερό, σωστή αναγνώριση φυτών, καθαρά εργαλεία, τήρηση ετικετών και σύγχρονες δοκιμασμένες συνταγές διατήρησης. Δεν παρουσιάζει ακριβείς ημερομηνίες φύτευσης ως καθολικές: πρέπει να λαμβάνονται υπόψη μεσογειακή ζέστη, υψόμετρο, παγετός, άνεμος, σκιά, τοπικοί περιορισμοί και πραγματικό μικροκλίμα.

Η νέα συλλογή ελέγχθηκε με επίσημο υλικό από FAO, USDA/NAL/NRCS/ARS, EPA, WHO, CDC, το ελληνικό Υπουργείο Αγροτικής Ανάπτυξης και Τροφίμων και το National Center for Home Food Preservation. Βασικά όρια ασφάλειας:

- Το βρόχινο νερό στέγης δεν είναι αυτόματα κατάλληλο για βρώσιμες καλλιέργειες· προτιμάται επαληθευμένα ασφαλές νερό και υπερισχύουν οι τοπικές υγειονομικές οδηγίες.
- Ανεπεξέργαστα λύματα, νερά πλημμύρας και χημικά μολυσμένο νερό δεν χρησιμοποιούνται αυτοσχέδια για άρδευση.
- Τα ωμά φύτρα έχουν κίνδυνο τροφιμογενούς νόσου· άτομα υψηλότερου κινδύνου πρέπει να προτιμούν καλά μαγειρεμένα φύτρα ή άλλη μαγειρεμένη καλλιέργεια.
- Τα λαχανικά χαμηλής οξύτητας απαιτούν σύγχρονη δοκιμασμένη κονσερβοποίηση υπό πίεση, όχι επεξεργασία μόνο σε βραστό νερό.
- Τουρσιά, ζύμωση, ξήρανση, κατάψυξη και κονσερβοποίηση πρέπει να βασίζονται σε σύγχρονη δοκιμασμένη συνταγή για το ακριβές προϊόν και τη συγκεκριμένη μέθοδο.

## Δομή

```text
Offline-Survival-Project-main/
├── Offline Survival.py
├── README.md
├── VALIDATION.md
├── English/
│   └── Φάκελος κατηγορίας/
│       └── Αρχεία γνώσεων JSON
└── Ελληνικά/
    └── Αντίστοιχος φάκελος κατηγορίας/
        └── Αντίστοιχα ελληνικά JSON
```

## Γρήγορη εκκίνηση στο Termux

```bash
pkg update -y && pkg install python -y
cd ~/Offline-Survival-Project-main
python "Offline Survival.py"
```

## Έλεγχος από τη γραμμή εντολών

Πλήρης μη διαδραστικός έλεγχος:

```bash
python "Offline Survival.py" --check
```

Σύνολα βάσης:

```bash
python "Offline Survival.py" --stats
```

Βοήθεια:

```bash
python "Offline Survival.py" --help
```

## Κεντρικό μενού

1. Αναζήτηση στη βάση γνώσεων
2. Περιήγηση κατηγοριών
3. Εύρεση και ανάγνωση JSON
4. Άνοιγμα εγγραφής με ID
5. Τυχαίο θέμα
6. Επαληθευμένα βασικά έκτακτης ανάγκης
7. Καλλιέργεια και ασφαλής διατήρηση τροφίμων
8. Ρυθμίσεις
9. Βοήθεια και χειρισμός
10. Έλεγχος ακεραιότητας
0. Έξοδος

## Τι ελέγχει ο validator

Κάθε εγγραφή και στις δύο γλώσσες ελέγχεται για:

- Έγκυρη σύνταξη JSON
- Υποχρεωτικά και μη κενά πεδία
- Σωστούς τύπους δεδομένων
- Μοναδικά IDs και τίτλους
- Σωστή τιμή γλώσσας
- Έγκυρες ημερομηνίες ISO που δεν βρίσκονται στο μέλλον
- Μη κενές λίστες πηγών
- Καθαρά HTTPS URLs
- Πηγές μόνο από εγκεκριμένους επίσημους τομείς
- Ίδιες αγγλικές και ελληνικές διαδρομές
- Ίδια IDs στις δύο γλώσσες
- Ίδια IDs μέσα στα αντίστοιχα αρχεία

Η τελευταία συσκευασμένη έκδοση περνά όλους τους ελέγχους χωρίς αναφερόμενο σφάλμα. Οι λεπτομέρειες και τα όρια του ελέγχου βρίσκονται στο `VALIDATION.md`.

## Ρυθμίσεις και ιδιωτικότητα

Αποθηκεύονται μόνο τοπικές προτιμήσεις στο:

```text
~/.offline_survival_project/settings.json
```

Δεν καταγράφονται ή μεταδίδονται αναζητήσεις, αναγνωσμένες εγγραφές, προσωπικά στοιχεία ή ιστορικό χρήσης.

## Σημείωση ασφάλειας

Το έργο είναι βοήθημα προετοιμασίας και αναφοράς. Δεν αντικαθιστά υπηρεσίες έκτακτης ανάγκης, ζωντανές επίσημες ειδοποιήσεις ή εξειδικευμένη ιατρική, τεχνική και επιχειρησιακή καθοδήγηση.

Για άμεση έκτακτη ανάγκη στην Ελλάδα ή στην Ευρωπαϊκή Ένωση κάλεσε **112**. Για πιθανή δηλητηρίαση στην Ελλάδα, το Υπουργείο Υγείας αναφέρει το Κέντρο Δηλητηριάσεων στο **210 7793777**, με λειτουργία 24 ώρες το 24ωρο, 7 ημέρες την εβδομάδα.

Όταν οι ζωντανές επίσημες οδηγίες διαφέρουν από το αποθηκευμένο υλικό, ακολούθησε τις επίσημες οδηγίες.
