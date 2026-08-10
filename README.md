# Offline Survival Project

> Για να μεταβείτε στην πλήρη Ελληνική ενότητα, συνεχίστε [πατώντας εδώ](#ελληνικά).

Offline Survival Project is a bilingual, offline-first survival knowledge and household-operations toolkit designed to stay useful when internet access is unavailable.

It combines a curated survival database, a local Command Center, a searchable Offline Library, a large bilingual Knowledge Compendium, operational planning tools, and a standalone single-file survival reader.

## Table of Contents

- [What The Project Includes](#what-the-project-includes)
- [Requirements](#requirements)
- [First-Time Use](#first-time-use)
- [Main Commands](#main-commands)
- [Survival Knowledge](#survival-knowledge)
- [Command Center](#command-center)
- [Offline Library](#offline-library)
- [Standalone Survival Reader](#standalone-survival-reader)
- [Phone Browser Support](#phone-browser-support)
- [Privacy & Local Storage](#privacy--local-storage)
- [Maintenance](#maintenance)
- [Safety Boundary](#safety-boundary)
- [Ελληνικά](#ελληνικά)

## What The Project Includes

- **English + Greek support** across the main database, interface, Library collections, and Knowledge Compendium.
- **220 detailed Knowledge Compendium subjects per language** covering emergency response, water, food, sanitation, first aid boundaries, evacuation, shelter, fire, power, communications, severe weather, navigation, recovery, accessibility, animals, and long-duration continuity.
- **871 curated database records per language** after removing low-value, templated, duplicated, and repetitive material.
- **732 Offline Library files** with paired bilingual collections and local full-text search.
- **32 Command Center sections** for practical household emergency operations.
- **Standalone Survival Reader** containing the complete bilingual Knowledge Compendium in one local HTML file.
- **No account required.**
- **No cloud required.**
- **No telemetry.**
- **No Docker or database server required.**
- **Python standard library only for the core.**
- **Localhost-first browser interface** for Android, Termux, Linux, and Windows-style local use.

## Requirements

| Component | Requirement |
| --- | --- |
| Python | Python 3 |
| Internet | Not required for normal offline use |
| Browser | Any modern installed/default phone or desktop browser for the Command Center |
| Storage | Enough space for the repository and any extra offline Library packs you add |
| Android | Termux is recommended for the Python launcher and local Command Center |

## First-Time Use

- Download or clone the repository.
- Open a terminal in the project folder.
- Run the terminal application if you want the lightweight text interface.
- Run the local Command Center if you want the full phone-friendly interface.
- Run the built-in checks after modifying files.
- Keep an additional copy of the project on separate local storage if you depend on it during outages.

### Terminal Interface

```bash
python "Offline Survival.py"
```

### Full Local Command Center

```bash
python "Offline Survival.py" --web
```

### Standalone Reader

```bash
python "Offline Survival.py" --reader
```

### Phone Browser Diagnostics

```bash
python "Offline Survival.py" --phone-browser-test
```

## Main Commands

- `--web` — start the complete local Command Center and hand it to the installed/default browser.
- `--reader` — open the self-contained bilingual survival reader.
- `--phone-browser-test` — run diagnostics inside the browser actually installed on the phone.
- `--check` — validate both language databases and mirrored IDs/paths.
- `--quality` — detect template filler and repeated narrative patterns.
- `--translations` — verify English/Greek parity.
- `--library-quality` — inspect Offline Library duplication and repeated-content quality.
- `--self-test` — run structural project checks.
- `--api-test` — test the localhost API and security boundaries.
- `--ui-test` — run deterministic UI/state/export logic tests.
- `--audit` — run the deep source/content audit.

## Survival Knowledge

The Knowledge Compendium is intended to be useful when the network is unavailable and normal search engines cannot be reached.

It includes detailed material for:

- immediate emergency priorities;
- household emergency command and accountability;
- drinking-water storage, collection, treatment boundaries, wells, rainwater, and contamination decisions;
- food storage, outage cooking, refrigeration loss, rationing, preservation boundaries, and hygiene;
- sanitation, emergency toilets, waste control, laundry, bathing, sewage problems, and public-health continuity;
- first-aid boundaries, CPR/AED readiness, bleeding, burns, choking, fractures, wounds, dehydration, heat/cold illness, and recognition of conditions that require professional care;
- medication continuity and refrigeration-dependent medical needs;
- infants, children, older adults, disabilities, accessibility requirements, service animals, and pets;
- earthquakes, aftershocks, tsunami, wildfire, smoke, flood, flash flood, severe storms, tornadoes, hurricanes, storm surge, dust storms, extreme heat, snow, ice, and cold;
- fire escape, cooking fire, LPG, generator, carbon-monoxide, electrical, battery, inverter, extension-cord, and solar-power safety;
- evacuation, go-bags, route planning, walking loads, vehicles, fuel, map use, bearings, waypoints, GPX/GeoJSON routes, and rescue signaling;
- shelter zoning, ventilation, temporary shelter, apartment/high-rise continuity, rural/coastal/mountain/island scenarios, and damaged-building boundaries;
- communications schedules, low-power communications, reunification, check-ins, information verification, and rumor control;
- recovery documentation, expenses, evidence, insurance/claim preparation, maintenance, decisions, shift handovers, and post-incident learning.

Safety-sensitive chapters include source anchors so the material can be re-checked when internet access is available again.

## Command Center

The local Command Center turns the guide into an operational workspace.

Major areas include:

- emergency search and verified essentials;
- household profile and readiness picture;
- inventory and supply tracking;
- water-batch traceability;
- food-lot and cold-chain tracking;
- sanitation capability tracking;
- power-load and stored-energy planning;
- communications windows and fallback methods;
- emergency contacts and meeting points;
- evacuation routes and grab-first planning;
- medical continuity records;
- dependents and accessibility planning;
- shelter zoning;
- damage and recovery tracking;
- vehicle readiness;
- kits and bag-weight tracking;
- household skill coverage;
- decision review board;
- incident and field logs;
- numeric observation trends;
- training drills and debrief history;
- recovery-cost ledger;
- Situation Brief and shift-handover outputs;
- searchable Knowledge Atlas and Offline Library;
- local diagnostics and backup/restore tools.

## Offline Library

- Library files remain on the local device.
- Readable documents can be searched by content from the Command Center.
- Binary reference packs are not scanned as ordinary text.
- User-added Library content is treated as untrusted when served through the local web interface.
- Exact duplicates, repeated substantive paragraphs, inherited boilerplate, and suspicious template similarity are checked by the Library-quality tool.

## Standalone Survival Reader

`Offline Survival Reader.html` is designed as a fallback when you want the knowledge without the complete operational interface.

It provides:

- all 220 English chapters;
- all 220 Greek chapters;
- local full-text search;
- domain/subject filtering;
- favorites;
- reviewed-state tracking;
- phone-friendly navigation;
- print support;
- no CDN;
- no external JavaScript;
- no external stylesheet;
- no runtime network requirement.

## Phone Browser Support

The launcher does not force a particular browser engine.

On Android/Termux it:

- prefers `termux-open-url`;
- falls back to Android's VIEW intent when available;
- hands the localhost URL to the phone's installed/default browser;
- keeps the local server bound to loopback by default.

## Privacy & Local Storage

- Operational state is stored locally.
- The project does not include telemetry.
- Full exported backups may contain sensitive household information.
- Redacted/template exports intentionally omit personal operational state.
- Local backups are plaintext unless the device/filesystem protects them with encryption.
- Do not expose the local Command Center to untrusted networks unless you understand the trust implications.

## Maintenance

- Main source files contain `MAINTENANCE` comments around important trust boundaries and extension points.
- Standard JSON does not support comments; technical JSON files use reserved maintenance-note fields instead of invalid `//` or `#` comments.
- `MAINTENANCE.json` records project-wide maintenance rules in valid JSON.
- Keep user-visible project release numbers out of titles, menus, diagnostics, filenames, and public documentation.
- Keep English and Greek content synchronized.
- Do not increase content counts with duplicated, templated, or lightly reworded filler.
- Run the built-in QA commands after meaningful changes.

## Safety Boundary

- This project is a preparedness and reference aid.
- It does not replace emergency services or official warnings.
- It does not replace qualified medical, structural, electrical, fire, utility, rescue, veterinary, or civil-protection professionals.
- Live official instructions take priority over cached/offline material when they are available.
- Do not enter unsafe structures, contaminated areas, floodwater, fire zones, electrical hazards, or other dangerous environments merely to follow or complete a checklist.

---

<a id="ελληνικά"></a>
# Offline Survival Project — Ελληνικά

Το Offline Survival Project είναι ένα δίγλωσσο σύστημα γνώσης επιβίωσης και οργάνωσης νοικοκυριού που έχει σχεδιαστεί για να παραμένει χρήσιμο χωρίς σύνδεση στο διαδίκτυο.

## Περιεχόμενα

- [Τι Περιλαμβάνει Το Project](#τι-περιλαμβάνει-το-project)
- [Απαιτήσεις](#απαιτήσεις)
- [Πρώτη Χρήση](#πρώτη-χρήση)
- [Βασικές Εντολές](#βασικές-εντολές)
- [Γνώση Επιβίωσης](#γνώση-επιβίωσης)
- [Command Center](#command-center-1)
- [Offline Library](#offline-library-1)
- [Αυτόνομος Αναγνώστης](#αυτόνομος-αναγνώστης)
- [Browser Τηλεφώνου](#browser-τηλεφώνου)
- [Ιδιωτικότητα](#ιδιωτικότητα)
- [Συντήρηση](#συντήρηση)
- [Όρια Ασφάλειας](#όρια-ασφάλειας)

## Τι Περιλαμβάνει Το Project

- **Αγγλικά + Ελληνικά** στη βάση, στο περιβάλλον, στις συλλογές της Library και στη Συλλογή Γνώσης.
- **220 αναλυτικά θέματα γνώσης ανά γλώσσα** για νερό, τρόφιμα, υγιεινή, πρώτες βοήθειες, εκκένωση, καταφύγιο, φωτιά, ενέργεια, επικοινωνίες, ακραία φαινόμενα, πλοήγηση, αποκατάσταση, προσβασιμότητα και μακροχρόνια συνέχεια.
- **871 επιμελημένες εγγραφές βάσης ανά γλώσσα** μετά την αφαίρεση επαναλαμβανόμενου και χαμηλής αξίας υλικού.
- **732 αρχεία Offline Library** με δίγλωσσες αντιστοιχίες και τοπική αναζήτηση πλήρους κειμένου.
- **32 ενότητες Command Center** για πρακτική διαχείριση έκτακτης ανάγκης.
- **Αυτόνομος Αναγνώστης Επιβίωσης** σε ένα τοπικό αρχείο HTML.
- **Χωρίς υποχρεωτικό λογαριασμό.**
- **Χωρίς cloud.**
- **Χωρίς τηλεμετρία.**
- **Χωρίς Docker ή ξεχωριστό database server.**
- **Μόνο standard library της Python για τον βασικό πυρήνα.**

## Απαιτήσεις

| Στοιχείο | Απαίτηση |
| --- | --- |
| Python | Python 3 |
| Internet | Δεν απαιτείται για τη συνηθισμένη offline χρήση |
| Browser | Σύγχρονος εγκατεστημένος/default browser κινητού ή υπολογιστή για το Command Center |
| Αποθήκευση | Αρκετός χώρος για το repository και πρόσθετα offline πακέτα που θα προσθέσεις |
| Android | Το Termux προτείνεται για τον Python launcher και το τοπικό Command Center |

## Πρώτη Χρήση

- Κατέβασε ή κάνε clone το repository.
- Άνοιξε terminal μέσα στον φάκελο του project.
- Χρησιμοποίησε το terminal interface για ελαφριά χρήση.
- Άνοιξε το Command Center για πλήρη χρήση από browser.
- Εκτέλεσε τους ελέγχους μετά από αλλαγές στα αρχεία.
- Κράτα δεύτερο τοπικό αντίγραφο αν σκοπεύεις να βασιστείς στο project κατά τη διάρκεια διακοπών ή καταστροφών.

### Terminal Interface

```bash
python "Offline Survival.py"
```

### Πλήρες Command Center

```bash
python "Offline Survival.py" --web
```

### Αυτόνομος Αναγνώστης

```bash
python "Offline Survival.py" --reader
```

### Διαγνωστικός Έλεγχος Browser Τηλεφώνου

```bash
python "Offline Survival.py" --phone-browser-test
```

## Βασικές Εντολές

- `--web` — ανοίγει το τοπικό Command Center στον εγκατεστημένο/default browser.
- `--reader` — ανοίγει τον αυτοτελή δίγλωσσο αναγνώστη.
- `--phone-browser-test` — εκτελεί διαγνωστικό έλεγχο μέσα στον browser του τηλεφώνου.
- `--check` — ελέγχει ακεραιότητα, αντιστοίχιση IDs και paths.
- `--quality` — ελέγχει templates και επαναλαμβανόμενη αφήγηση.
- `--translations` — ελέγχει αντιστοίχιση Αγγλικών/Ελληνικών.
- `--library-quality` — ελέγχει διπλότυπα και επαναλήψεις στην Offline Library.
- `--self-test` — εκτελεί δομικούς ελέγχους.
- `--api-test` — ελέγχει το localhost API και τα όρια ασφαλείας.
- `--ui-test` — ελέγχει λογική UI/state/export.
- `--audit` — εκτελεί βαθύ έλεγχο source/content.

## Γνώση Επιβίωσης

Η Συλλογή Γνώσης έχει σχεδιαστεί ώστε οι βασικές πληροφορίες να είναι διαθέσιμες ακόμη και όταν δεν λειτουργεί το διαδίκτυο.

Περιλαμβάνει αναλυτικό υλικό για:

- άμεσες προτεραιότητες έκτακτης ανάγκης,
- νερό και μόλυνση,
- τρόφιμα και ψύξη,
- υγιεινή και λύματα,
- πρώτες βοήθειες και όρια ιατρικής αυτοβοήθειας,
- φάρμακα και ιατρική συνέχεια,
- παιδιά, ηλικιωμένους, αναπηρίες και προσβασιμότητα,
- κατοικίδια και ζώα υπηρεσίας,
- σεισμούς, τσουνάμι, πυρκαγιές, καπνό και πλημμύρες,
- καύσωνες, κρύο, χιόνι, ανεμοθύελλες, τροπικούς κυκλώνες και άλλα ακραία φαινόμενα,
- ηλεκτρική ασφάλεια, μπαταρίες, γεννήτριες, inverter και ηλιακή ενέργεια,
- εκκένωση, οχήματα, καύσιμα, χάρτες, συντεταγμένες και διαδρομές,
- καταφύγιο και ζώνες χρήσης/αποφυγής,
- επικοινωνίες, check-ins και οικογενειακή επανένωση,
- αποκατάσταση, έξοδα, αποδεικτικά στοιχεία, αποφάσεις και παράδοση βάρδιας.

## Command Center

Το Command Center μετατρέπει τη γνώση σε τοπικό επιχειρησιακό χώρο εργασίας.

Περιλαμβάνει:

- αναζήτηση έκτακτης ανάγκης,
- προφίλ νοικοκυριού,
- αποθέματα και inventory,
- παρτίδες νερού,
- παρτίδες τροφίμων,
- υγιεινή,
- φορτία και διαθέσιμη ενέργεια,
- επικοινωνίες,
- επαφές και σημεία συνάντησης,
- εκκένωση,
- ιατρική συνέχεια,
- εξαρτώμενα άτομα και προσβασιμότητα,
- ζώνες καταφυγίου,
- ζημιές και αποκατάσταση,
- οχήματα,
- κιτ και βάρος σακιδίων,
- δεξιότητες,
- πίνακα αποφάσεων,
- incident/field logs,
- γραφήματα αριθμητικών μετρήσεων,
- ασκήσεις και debrief,
- έξοδα αποκατάστασης,
- Situation Brief και shift handover,
- Knowledge Atlas,
- Offline Library,
- backup/restore και τοπικά diagnostics.

## Offline Library

- Τα αρχεία παραμένουν στη συσκευή.
- Τα αναγνώσιμα έγγραφα αναζητούνται τοπικά.
- Τα δυαδικά reference packs δεν σαρώνονται σαν απλό κείμενο.
- Πρόσθετο περιεχόμενο χρήστη αντιμετωπίζεται ως μη έμπιστο από το web interface.
- Ο έλεγχος ποιότητας απορρίπτει ακριβή διπλότυπα, επαναλαμβανόμενες ουσιαστικές παραγράφους και ύποπτα templates.

## Αυτόνομος Αναγνώστης

Το `Offline Survival Reader.html` περιλαμβάνει ολόκληρη τη δίγλωσση Συλλογή Γνώσης σε ένα αρχείο.

Προσφέρει:

- 220 αγγλικά κεφάλαια,
- 220 ελληνικά κεφάλαια,
- τοπική αναζήτηση,
- φίλτρα,
- αγαπημένα,
- κατάσταση μελέτης,
- πλοήγηση για κινητό,
- εκτύπωση,
- χωρίς CDN,
- χωρίς εξωτερικό JavaScript,
- χωρίς εξωτερικό stylesheet,
- χωρίς απαίτηση δικτύου κατά την εκτέλεση.

## Browser Τηλεφώνου

Ο launcher δεν επιβάλλει συγκεκριμένο browser engine.

Σε Android/Termux:

- προτιμά `termux-open-url`,
- χρησιμοποιεί Android VIEW intent ως εναλλακτική,
- παραδίδει το localhost URL στον εγκατεστημένο/default browser,
- κρατά τον server σε loopback από προεπιλογή.

## Ιδιωτικότητα

- Τα επιχειρησιακά δεδομένα παραμένουν τοπικά.
- Δεν υπάρχει τηλεμετρία.
- Τα πλήρη backups μπορεί να περιέχουν ευαίσθητα δεδομένα νοικοκυριού.
- Τα redacted/template exports δεν περιλαμβάνουν προσωπική επιχειρησιακή κατάσταση.
- Τα τοπικά backups είναι plaintext αν δεν προστατεύονται από κρυπτογράφηση συσκευής/filesystem.

## Συντήρηση

- Τα βασικά scripts περιέχουν σχόλια `MAINTENANCE` στα κρίσιμα σημεία.
- Το standard JSON δεν υποστηρίζει πραγματικά σχόλια· γι' αυτό τα τεχνικά JSON χρησιμοποιούν ειδικά maintenance-note fields χωρίς να παραβιάζεται το format.
- Το `MAINTENANCE.json` περιγράφει τους κανόνες συντήρησης σε έγκυρο JSON.
- Δεν εμφανίζονται αριθμοί release σε τίτλους, μενού, diagnostics, filenames ή δημόσια documentation.
- Τα Αγγλικά και Ελληνικά πρέπει να παραμένουν συγχρονισμένα.
- Δεν προστίθεται περιεχόμενο μόνο για αύξηση αριθμών μέσω templates ή επαναλήψεων.

## Όρια Ασφάλειας

- Το project είναι βοήθημα προετοιμασίας και αναφοράς.
- Δεν αντικαθιστά υπηρεσίες έκτακτης ανάγκης ή επίσημες προειδοποιήσεις.
- Δεν αντικαθιστά επαγγελματίες υγείας, μηχανικούς, ηλεκτρολόγους, πυροσβέστες, διασώστες, υπηρεσίες κοινής ωφέλειας ή πολιτική προστασία.
- Οι ζωντανές επίσημες οδηγίες υπερισχύουν του αποθηκευμένου offline υλικού όταν είναι διαθέσιμες.

