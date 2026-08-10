# Offline Survival Project

> Για να μεταβείτε στην πλήρη Ελληνική έκδοση, συνεχίστε [Πατώντας Εδώ](#offline-survival-project--ελληνικά).

Offline Survival Project is a bilingual, offline-first survival knowledge and household emergency-operations toolkit designed to stay useful when internet access is unavailable.

It combines a curated survival database, a phone-friendly local Command Center, a large bilingual Offline Library, a 250-subject Knowledge Compendium, planning and tracking tools, and a completely standalone survival reader.

---

## Table of Contents

* [What The Project Includes](#what-the-project-includes)
* [Requirements](#requirements)
* [Before You Start](#before-you-start)
* [Installation And First Use](#installation-and-first-use)
* [Main Commands](#main-commands)
* [One Python Script](#one-python-script)
* [One Consolidated JSON Database](#one-consolidated-json-database)
* [Survival Knowledge](#survival-knowledge)
* [Command Center](#command-center)
* [Knowledge Compendium](#knowledge-compendium)
* [Offline Library](#offline-library)
* [Standalone Survival Reader](#standalone-survival-reader)
* [Phone Browser Support](#phone-browser-support)
* [Operational Tools](#operational-tools)
* [Privacy And Local Storage](#privacy-and-local-storage)
* [Maintenance](#maintenance)
* [Important Safety Notes](#important-safety-notes)
* [Offline Survival Project — Ελληνικά](#offline-survival-project--ελληνικά)

## What The Project Includes

* **English + Greek support** across the main database, interface, Knowledge Compendium, paired Library collections, and current documentation.
* **250 detailed Knowledge Compendium subjects per language.**
* **871 curated database records per language.**
* **792 Offline Library files** with paired bilingual collections and local full-text search.
* **32+ Command Center sections** for practical household emergency operations.
* **Standalone Survival Reader** containing the complete bilingual Knowledge Compendium in one local HTML file.
* **One Python script only:** `Offline Survival.py`.
* **One repository JSON database only:** `Offline Survival Database.json`, containing both English and Greek records plus maintenance metadata.
* **No `.sh` launchers:** Command Center, Reader, and phone-browser diagnostics are launched directly through `Offline Survival.py`.
* **No account required.**
* **No cloud required.**
* **No telemetry.**
* **No Docker required.**
* **No database server required.**
* **No third-party Python package required for the core.**
* **Localhost-first browser interface** for Android, Termux, Linux, and compatible desktop environments.
* **Installed/default phone browser support** instead of forcing a specific browser engine.
* **Built-in database, translation, duplication, content-quality, API, UI, and deep-audit checks.**

## Requirements

Component | Requirement
--- | ---
Device | Android phone/tablet, Linux computer, or compatible computer with Python 3
Python | Python 3
Internet | Not required for normal offline use
Browser | Any modern installed/default browser for the local Command Center
Storage | Enough local storage for the project and any extra offline reference packs you add
Android | Termux is recommended for the Python launcher and local Command Center

## Before You Start

* Keep a copy of the project on the device you intend to use during an outage.
* Keep a second copy on another local storage device if the project is important to your preparedness plan.
* On Android, install Termux from a trusted source and allow storage access only if you need access to shared storage.
* Open the project once before an emergency so you know how the terminal interface, Command Center, Reader, and backup tools work.
* Use the Phone Browser Diagnostics command on the actual phone you plan to carry.
* Review critical chapters before you need them; do not rely on learning everything for the first time during an emergency.
* Keep live official instructions as the priority whenever official communications are available.

## Installation And First Use

### Option 1: Clone From GitHub

Run:

```bash
git clone https://github.com/dedsec1121fk/Offline-Survival-Project
cd Offline-Survival-Project
python "Offline Survival.py"
```

What this does:

* downloads the complete project;
* enters the project folder;
* launches the lightweight terminal interface;
* keeps all bundled survival knowledge available locally after the repository has been downloaded.

### Option 2: Use A Downloaded ZIP

* Download the repository ZIP.
* Extract it completely.
* Open a terminal inside the extracted `Offline-Survival-Project` folder.
* Run:

```bash
python "Offline Survival.py"
```

### Option 3: Open The Full Command Center

Run:

```bash
python "Offline Survival.py" --web
```

What this does:

* starts a local server on the device;
* binds to localhost by default;
* hands the local URL to the installed/default browser;
* opens the operational Command Center without requiring cloud services.

## Main Commands

* `python "Offline Survival.py"` — open the lightweight terminal knowledge browser.
* `python "Offline Survival.py" --web` — start the full local Command Center.
* `python "Offline Survival.py" --reader` — open the standalone bilingual survival reader.
* `python "Offline Survival.py" --phone-browser-test` — open diagnostics in the phone's installed/default browser.
* `python "Offline Survival.py" --check` — validate both languages inside the consolidated database and verify mirrored IDs/source groups.
* `python "Offline Survival.py" --stats` — show database counts.
* `python "Offline Survival.py" --quality` — detect template filler and repeated narrative patterns.
* `python "Offline Survival.py" --translations` — verify English/Greek parity.
* `python "Offline Survival.py" --library-quality` — inspect Library duplication, repeated content, and suspicious similarity.
* `python "Offline Survival.py" --self-test` — run structural project checks.
* `python "Offline Survival.py" --api-test` — run localhost API/security smoke tests.
* `python "Offline Survival.py" --ui-test` — run deterministic UI/state/export logic tests when Node.js is available.
* `python "Offline Survival.py" --audit` — run the deep source/config/content audit.

## One Python Script

The repository intentionally ships with only one Python script and no shell launchers:

* `Offline Survival.py`
* `Offline Survival Database.json` is the single physical JSON database file.
* The old hundreds of per-topic JSON files are represented as virtual source groups inside that database, preserving search/category organization without repository clutter.
* `--web`, `--reader`, and `--phone-browser-test` replace the old shell-launcher jobs directly.

That single Python script contains the Python-side functionality for:

* terminal browsing;
* database validation;
* local Command Center server;
* state sanitization and persistence;
* installed/default browser launching;
* content-quality checks;
* translation checks;
* Library-quality checks;
* API/security tests;
* deep audit checks;
* standalone-reader QA support.

Browser interface code remains in normal HTML, CSS, and JavaScript assets so it stays maintainable and can be inspected independently.

## One Consolidated JSON Database

All curated database records now live in one physical file:

* `Offline Survival Database.json`
* English and Greek records are stored together but remain separate language datasets.
* The previous topic/category file paths are preserved as **virtual source groups** inside the database.
* Search, category browsing, source-group browsing, raw grouped JSON viewing, integrity checks, translation parity, and the Command Center all read this same file.
* Maintenance guidance is stored in the top-level `_maintenance` metadata object.
* The repository therefore does not need hundreds of physical topic JSON files.

## Survival Knowledge

The project is designed to answer practical survival questions without relying on an internet search engine.

Major knowledge areas include:

* immediate emergency priorities;
* household command and accountability;
* drinking-water storage and reserve planning;
* water collection and treatment boundaries;
* private wells and post-flood well concerns;
* rainwater decisions;
* contamination and boil-water decisions;
* food storage and rotation;
* refrigerator/freezer outage decisions;
* outage cooking;
* rationing and calorie planning;
* food preservation boundaries;
* sanitation and emergency toilets;
* sewage and waste control;
* handwashing, bathing, and laundry continuity;
* first-aid boundaries;
* CPR/AED readiness;
* bleeding and wound monitoring;
* burns and choking;
* fractures, sprains, and trauma boundaries;
* dehydration, heat illness, and cold illness;
* stroke and heart-attack recognition;
* medication continuity;
* refrigeration-dependent medical needs;
* asthma and anaphylaxis continuity;
* infants and children;
* older adults;
* disability and accessibility planning;
* pets and service animals;
* earthquakes and aftershocks;
* tsunami;
* wildfire and smoke;
* flood and flash flood;
* tornadoes;
* hurricanes/cyclones;
* storm surge;
* severe thunderstorms and hail;
* dust storms;
* extreme heat;
* snow, ice, and extreme cold;
* avalanche terrain boundaries;
* rip currents and coastal hazards;
* fire escape and cooking-fire safety;
* LPG and fuel safety;
* generator and carbon-monoxide safety;
* electrical and extension-cord safety;
* lithium and lead-acid battery safety;
* inverter and DC load planning;
* solar and field-power planning;
* evacuation and go-bags;
* route planning and alternate routes;
* walking-load planning;
* vehicle readiness and fuel planning;
* map, bearing, waypoint, GPX, and GeoJSON workflows;
* rescue signaling;
* shelter zoning and ventilation;
* apartment/high-rise continuity;
* rural, coastal, mountain, and island scenarios;
* communications schedules;
* low-power communications;
* family reunification and check-ins;
* information verification and rumor control;
* recovery evidence and expense tracking;
* decision logs and review deadlines;
* shift handovers;
* training drills and post-incident learning.

## Command Center

The Command Center turns the guide into an operational workspace.

It can help you:

* search the curated bilingual database;
* search the Offline Library by file content;
* open the Knowledge Atlas;
* maintain a household profile;
* calculate readiness indicators;
* track supplies and expirations;
* track water batches and treatment status;
* manage food lots and cold-chain concerns;
* track sanitation points;
* plan electrical loads and energy endurance;
* schedule communications windows;
* store emergency contacts and meeting points;
* plan evacuation routes;
* maintain grab-first lists;
* record medical continuity information;
* record dependents and accessibility requirements;
* track shelter zones;
* record damage and recovery work;
* track vehicles and kits;
* maintain household skill coverage;
* maintain a decision board;
* create incident and field logs;
* view numeric field trends;
* run training drills and record debriefs;
* track recovery expenses;
* generate a Situation Brief;
* generate a shift-handover summary;
* export local operational data;
* back up and restore local state.

## Knowledge Compendium

The Knowledge Compendium contains **250 detailed subjects in English and 250 corresponding subjects in Greek**.

It is designed so that:

* each subject has a distinct operational purpose;
* paired English/Greek documents stay synchronized;
* repeated filler is rejected by quality checks;
* exact duplicate payloads are rejected;
* repeated substantive Library paragraphs are checked;
* source anchors can be used later to re-check safety-sensitive material when connectivity becomes available.

## Offline Library

The Offline Library is designed for material you want available without internet access.

It includes:

* paired English and Greek field guides;
* operational cards;
* worksheets;
* scenario drills;
* pocket references;
* long-form Knowledge Compendium chapters;
* local Library search;
* readable-document previews;
* SHA-256 hashing support for local files;
* optional Kiwix/ZIM-style reference material support where compatible tooling is available.

Important Library behavior:

* Library files remain on the local device.
* Binary reference packs are not treated as ordinary text.
* User-added Library content is treated as untrusted by the local web server.
* Direct delivery of untrusted files uses restrictive response handling.
* Path traversal outside the Library is rejected.

## Standalone Survival Reader

`Offline Survival Reader.html` provides the Knowledge Compendium without requiring the full Command Center.

It includes:

* 250 English chapters;
* 250 Greek chapters;
* one self-contained HTML file;
* local full-text search;
* subject/domain filters;
* favorites;
* reviewed-state tracking;
* mobile-friendly navigation;
* print support;
* no CDN;
* no external JavaScript;
* no external stylesheet;
* no runtime internet requirement.

Open it through the main script:

```bash
python "Offline Survival.py" --reader
```

## Phone Browser Support

The project does not force Chromium or another specific browser engine.

On Android/Termux the launcher:

* prefers `termux-open-url` when available;
* falls back to Android's normal VIEW intent when possible;
* hands the localhost URL to the installed/default browser;
* keeps the server on loopback by default;
* provides a dedicated on-phone diagnostics page.

Run:

```bash
python "Offline Survival.py" --phone-browser-test
```

The phone diagnostics check the browser that actually opens on the device.

## Operational Tools

The project includes practical offline tools for:

* water planning;
* food endurance;
* battery/power budgeting;
* unit conversion;
* distance and bearing calculations;
* waypoint records;
* field maps;
* GPX/GeoJSON route import and export;
* inventory management;
* expiration tracking;
* contact and meeting-point planning;
* evacuation planning;
* incident logs;
* numeric field observations;
* household roles;
* skill coverage;
* medical continuity;
* sanitation continuity;
* communications schedules;
* dependents/accessibility planning;
* damage/recovery tracking;
* decision tracking;
* recovery costs;
* drills and debriefs;
* Situation Brief generation;
* local backup/restore.

## Privacy And Local Storage

* Operational state is stored locally.
* The project does not include telemetry.
* The core does not require an account.
* The core does not require cloud storage.
* Full backups may contain sensitive household information.
* Redacted/template exports intentionally omit personal operational state.
* Local backups are plaintext unless the device/filesystem protects them with encryption.
* The local server binds to loopback by default.
* Do not deliberately expose the Command Center to untrusted networks unless you understand the consequences.

## Maintenance

* `Offline Survival.py` contains `MAINTENANCE` comments around important trust boundaries and extension points.
* The repository intentionally keeps **one Python script only** and **zero `.sh` files**.
* The repository intentionally keeps **one physical `.json` file only:** `Offline Survival Database.json`.
* Standard JSON does not support `//` or `#` comments, so project-wide maintenance notes are stored in the database's `_maintenance` metadata object.
* Do not split the consolidated database back into hundreds of physical topic JSON files; preserve its virtual source-group organization instead.
* Keep English and Greek content synchronized.
* Do not increase content counts using duplicated or lightly reworded filler.
* Do not add a second Python helper script; extend the single entry point instead.
* Keep phone-browser behavior engine-neutral.
* Keep localhost as the default server binding.
* Re-run the built-in checks after meaningful changes.

Recommended maintenance checks:

```bash
python "Offline Survival.py" --check
python "Offline Survival.py" --quality
python "Offline Survival.py" --translations
python "Offline Survival.py" --library-quality
python "Offline Survival.py" --self-test
python "Offline Survival.py" --api-test
python "Offline Survival.py" --audit
```

## Important Safety Notes

* This project is a preparedness and reference aid.
* It does not replace emergency services.
* It does not replace official emergency warnings.
* It does not replace qualified medical professionals.
* It does not replace structural, electrical, fire, utility, rescue, veterinary, agricultural, maritime, or civil-protection professionals.
* Live official instructions take priority over cached/offline information when they are available.
* Do not enter unsafe structures, floodwater, contaminated areas, fire zones, unstable terrain, energized areas, or other dangerous environments merely to complete a checklist.
* If a situation exceeds your training, equipment, or safe working conditions, prioritize withdrawal, isolation of the hazard when safe, and professional assistance.

---

<a id="offline-survival-project--ελληνικά"></a>
# Offline Survival Project — Ελληνικά

> Για να επιστρέψετε στην πλήρη Αγγλική έκδοση, συνεχίστε [Πατώντας Εδώ](#offline-survival-project).

Το Offline Survival Project είναι ένα δίγλωσσο, offline-first σύστημα γνώσης επιβίωσης και οργάνωσης έκτακτης ανάγκης για νοικοκυριά, σχεδιασμένο ώστε να παραμένει χρήσιμο όταν δεν υπάρχει πρόσβαση στο διαδίκτυο.

Συνδυάζει επιμελημένη βάση γνώσεων, τοπικό Command Center για κινητό, μεγάλη δίγλωσση Offline Library, Knowledge Compendium 250 θεμάτων, εργαλεία σχεδιασμού και καταγραφής και έναν πλήρως αυτόνομο οδηγό επιβίωσης.

---

## Περιεχόμενα

* [Τι Περιλαμβάνει Το Project](#τι-περιλαμβάνει-το-project)
* [Απαιτήσεις](#απαιτήσεις)
* [Πριν Ξεκινήσεις](#πριν-ξεκινήσεις)
* [Εγκατάσταση Και Πρώτη Χρήση](#εγκατάσταση-και-πρώτη-χρήση)
* [Βασικές Εντολές](#βασικές-εντολές)
* [Ένα Python Script](#ένα-python-script)
* [Γνώση Επιβίωσης](#γνώση-επιβίωσης)
* [Command Center](#command-center-1)
* [Knowledge Compendium](#knowledge-compendium-1)
* [Offline Library](#offline-library-1)
* [Αυτόνομος Survival Reader](#αυτόνομος-survival-reader)
* [Υποστήριξη Browser Κινητού](#υποστήριξη-browser-κινητού)
* [Επιχειρησιακά Εργαλεία](#επιχειρησιακά-εργαλεία)
* [Ιδιωτικότητα Και Τοπική Αποθήκευση](#ιδιωτικότητα-και-τοπική-αποθήκευση)
* [Συντήρηση](#συντήρηση)
* [Σημαντικές Σημειώσεις Ασφάλειας](#σημαντικές-σημειώσεις-ασφάλειας)

## Τι Περιλαμβάνει Το Project

* **Πλήρη υποστήριξη Αγγλικών + Ελληνικών** στη βασική βάση, στο interface, στο Knowledge Compendium, στις ζευγαρωμένες συλλογές της Library και στην τρέχουσα τεκμηρίωση.
* **250 αναλυτικά θέματα Knowledge Compendium ανά γλώσσα.**
* **871 επιμελημένες εγγραφές βάσης ανά γλώσσα.**
* **792 αρχεία Offline Library** με δίγλωσσα ζεύγη και τοπική αναζήτηση πλήρους κειμένου.
* **32+ ενότητες Command Center** για πραγματική οργάνωση έκτακτης ανάγκης.
* **Standalone Survival Reader** με ολόκληρο το δίγλωσσο Knowledge Compendium σε ένα τοπικό HTML αρχείο.
* **Μόνο ένα Python script:** `Offline Survival.py`.
* **Μόνο ένα repository JSON database:** `Offline Survival Database.json`, με Αγγλικά, Ελληνικά και maintenance metadata στο ίδιο αρχείο.
* **Χωρίς `.sh` launchers:** Command Center, Reader και phone-browser diagnostics ξεκινούν απευθείας από το `Offline Survival.py`.
* **Δεν χρειάζεται λογαριασμός.**
* **Δεν χρειάζεται cloud.**
* **Δεν υπάρχει telemetry.**
* **Δεν χρειάζεται Docker.**
* **Δεν χρειάζεται database server.**
* **Δεν απαιτείται τρίτο Python package για τον πυρήνα.**
* **Τοπικό browser interface** για Android, Termux, Linux και συμβατά desktop περιβάλλοντα.
* **Χρήση του εγκατεστημένου/default browser του κινητού** χωρίς εξαναγκασμό συγκεκριμένου browser engine.
* **Ενσωματωμένοι έλεγχοι** βάσης, μεταφράσεων, διπλοτύπων, ποιότητας κειμένου, API, UI και deep audit.

## Απαιτήσεις

Στοιχείο | Απαίτηση
--- | ---
Συσκευή | Android κινητό/tablet, Linux υπολογιστής ή συμβατός υπολογιστής με Python 3
Python | Python 3
Internet | Δεν απαιτείται για κανονική offline χρήση
Browser | Οποιοσδήποτε σύγχρονος εγκατεστημένος/default browser για το Command Center
Αποθήκευση | Αρκετός τοπικός χώρος για το project και επιπλέον offline πακέτα που προσθέτεις
Android | Προτείνεται Termux για τον Python launcher και το τοπικό Command Center

## Πριν Ξεκινήσεις

* Κράτησε ένα αντίγραφο του project στη συσκευή που σκοπεύεις να χρησιμοποιείς σε διακοπή υπηρεσιών.
* Κράτησε δεύτερο αντίγραφο σε διαφορετικό τοπικό αποθηκευτικό μέσο αν βασίζεσαι στο project για την ετοιμότητά σου.
* Σε Android, εγκατέστησε Termux από αξιόπιστη πηγή και δώσε πρόσβαση αποθήκευσης μόνο αν τη χρειάζεσαι.
* Άνοιξε το project πριν υπάρξει πραγματική ανάγκη ώστε να γνωρίζεις το terminal interface, το Command Center, τον Reader και τα backup εργαλεία.
* Τρέξε το Phone Browser Diagnostics στο πραγματικό κινητό που θα έχεις μαζί σου.
* Διάβασε εκ των προτέρων τα κρίσιμα κεφάλαια.
* Όταν υπάρχουν ζωντανές επίσημες οδηγίες, αυτές έχουν προτεραιότητα.

## Εγκατάσταση Και Πρώτη Χρήση

### Επιλογή 1: Clone Από GitHub

Τρέξε:

```bash
git clone https://github.com/dedsec1121fk/Offline-Survival-Project
cd Offline-Survival-Project
python "Offline Survival.py"
```

Τι κάνει:

* κατεβάζει ολόκληρο το project;
* μπαίνει στον φάκελο του project;
* ανοίγει το ελαφρύ terminal interface;
* αφήνει την ενσωματωμένη γνώση διαθέσιμη τοπικά μετά το download.

### Επιλογή 2: Χρήση ZIP

* Κατέβασε το ZIP του repository.
* Κάνε πλήρη αποσυμπίεση.
* Άνοιξε terminal μέσα στον φάκελο `Offline-Survival-Project`.
* Τρέξε:

```bash
python "Offline Survival.py"
```

### Επιλογή 3: Πλήρες Command Center

Τρέξε:

```bash
python "Offline Survival.py" --web
```

Τι κάνει:

* ξεκινά τοπικό server στη συσκευή;
* συνδέεται σε localhost από προεπιλογή;
* παραδίδει το τοπικό URL στον εγκατεστημένο/default browser;
* ανοίγει το επιχειρησιακό Command Center χωρίς cloud υπηρεσίες.

## Βασικές Εντολές

* `python "Offline Survival.py"` — άνοιγμα του ελαφρού terminal knowledge browser.
* `python "Offline Survival.py" --web` — εκκίνηση του πλήρους τοπικού Command Center.
* `python "Offline Survival.py" --reader` — άνοιγμα του αυτόνομου δίγλωσσου Survival Reader.
* `python "Offline Survival.py" --phone-browser-test` — diagnostics μέσα στον εγκατεστημένο/default browser του κινητού.
* `python "Offline Survival.py" --check` — έλεγχος και των δύο βάσεων και των mirrored IDs/paths.
* `python "Offline Survival.py" --stats` — εμφάνιση μετρήσεων βάσης.
* `python "Offline Survival.py" --quality` — εντοπισμός template filler και επαναλαμβανόμενων narrative patterns.
* `python "Offline Survival.py" --translations` — έλεγχος αντιστοιχίας Αγγλικών/Ελληνικών.
* `python "Offline Survival.py" --library-quality` — έλεγχος διπλοτύπων και επαναλαμβανόμενου περιεχομένου Library.
* `python "Offline Survival.py" --self-test` — structural checks του project.
* `python "Offline Survival.py" --api-test` — localhost API/security smoke tests.
* `python "Offline Survival.py" --ui-test` — deterministic UI/state/export tests όταν υπάρχει Node.js.
* `python "Offline Survival.py" --audit` — deep source/config/content audit.

## Ένα Python Script

Το repository περιέχει σκόπιμα μόνο ένα Python script και κανένα shell launcher:

* `Offline Survival.py`
* Το `Offline Survival Database.json` είναι το μοναδικό φυσικό JSON database file του repository.
* Τα παλιά εκατοντάδες topic JSON διατηρούνται ως virtual source groups μέσα στη μία βάση, ώστε να υπάρχει η ίδια οργάνωση χωρίς εκατοντάδες φυσικά αρχεία.
* Τα `--web`, `--reader` και `--phone-browser-test` καλύπτουν απευθείας τις λειτουργίες των παλιών `.sh` launchers.

Το ίδιο αρχείο χειρίζεται:

* terminal browsing;
* database validation;
* τοπικό Command Center server;
* sanitization και αποθήκευση state;
* άνοιγμα του εγκατεστημένου/default browser;
* content-quality checks;
* translation checks;
* Library-quality checks;
* API/security tests;
* deep audit checks;
* QA του standalone reader.

Ο browser κώδικας παραμένει σε κανονικά HTML, CSS και JavaScript assets ώστε να είναι πιο εύκολος στον έλεγχο και στη συντήρηση.

## Μία Ενοποιημένη JSON Βάση

Όλες οι επιμελημένες εγγραφές της βάσης βρίσκονται πλέον σε ένα φυσικό αρχείο:

* `Offline Survival Database.json`
* Οι αγγλικές και ελληνικές εγγραφές βρίσκονται μαζί στο αρχείο αλλά παραμένουν ξεχωριστά σύνολα γλώσσας.
* Οι παλιές διαδρομές θεμάτων/κατηγοριών διατηρούνται ως **virtual source groups** μέσα στη βάση.
* Αναζήτηση, κατηγορίες, source-group browsing, προβολή ομαδοποιημένου JSON, integrity checks, translation parity και Command Center διαβάζουν την ίδια ενιαία βάση.
* Οι οδηγίες συντήρησης αποθηκεύονται στο top-level `_maintenance` metadata object.
* Έτσι το repository δεν χρειάζεται εκατοντάδες φυσικά topic JSON αρχεία.

## Γνώση Επιβίωσης

Οι βασικοί τομείς περιλαμβάνουν:

* άμεσες προτεραιότητες έκτακτης ανάγκης;
* οργάνωση και λογοδοσία νοικοκυριού;
* αποθήκευση και απόθεμα πόσιμου νερού;
* συλλογή και επεξεργασία νερού;
* ιδιωτικά πηγάδια και προβλήματα μετά από πλημμύρα;
* βρόχινο νερό;
* μόλυνση και αποφάσεις βρασμού;
* αποθήκευση και rotation τροφίμων;
* ψυγείο/κατάψυξη σε διακοπή ρεύματος;
* μαγείρεμα χωρίς κανονικές υπηρεσίες;
* rationing και θερμιδικό σχεδιασμό;
* όρια ασφαλούς συντήρησης τροφίμων;
* αποχέτευση και αυτοσχέδιες τουαλέτες;
* έλεγχο απορριμμάτων;
* πλύσιμο χεριών, μπάνιο και πλύσιμο ρούχων;
* όρια πρώτων βοηθειών;
* ετοιμότητα CPR/AED;
* αιμορραγία και παρακολούθηση τραυμάτων;
* εγκαύματα και πνιγμονή;
* κατάγματα, διαστρέμματα και τραύμα;
* αφυδάτωση, θερμική και ψυχρή καταπόνηση;
* αναγνώριση εγκεφαλικού και καρδιακού επεισοδίου;
* συνέχεια φαρμάκων;
* φάρμακα που χρειάζονται ψύξη;
* άσθμα και αναφυλαξία;
* βρέφη και παιδιά;
* ηλικιωμένους;
* αναπηρία και προσβασιμότητα;
* κατοικίδια και ζώα υπηρεσίας;
* σεισμούς και μετασεισμούς;
* τσουνάμι;
* δασικές πυρκαγιές και καπνό;
* πλημμύρες και flash floods;
* ανεμοστρόβιλους;
* τυφώνες/κυκλώνες;
* storm surge;
* έντονες καταιγίδες και χαλάζι;
* dust storms;
* ακραία ζέστη;
* χιόνι, πάγο και ακραίο κρύο;
* avalanche terrain boundaries;
* rip currents και παράκτιους κινδύνους;
* διαφυγή από φωτιά;
* ασφάλεια LPG και καυσίμων;
* γεννήτριες και μονοξείδιο του άνθρακα;
* ηλεκτρική ασφάλεια;
* μπαταρίες λιθίου και μολύβδου;
* inverter και DC loads;
* ηλιακή και field power;
* εκκένωση και go-bags;
* κύριες και εναλλακτικές διαδρομές;
* βάρος εξοπλισμού για πεζή μετακίνηση;
* οχήματα και καύσιμα;
* χάρτες, bearings, waypoints, GPX και GeoJSON;
* σήματα διάσωσης;
* shelter zoning και αερισμό;
* πολυκατοικίες/high-rise continuity;
* αγροτικά, παράκτια, ορεινά και νησιωτικά σενάρια;
* προγράμματα επικοινωνίας;
* low-power communications;
* οικογενειακή επανένωση και check-ins;
* επαλήθευση πληροφοριών και έλεγχο φημών;
* τεκμηρίωση αποκατάστασης και έξοδα;
* decision logs;
* shift handovers;
* drills και post-incident learning.

## Command Center

Το Command Center μπορεί να χρησιμοποιηθεί για:

* αναζήτηση στην επιμελημένη δίγλωσση βάση;
* αναζήτηση μέσα στα αρχεία της Offline Library;
* Knowledge Atlas;
* household profile;
* readiness picture;
* inventory και λήξεις;
* water batch traceability;
* food lots και cold-chain concerns;
* sanitation points;
* power loads και energy endurance;
* communications windows;
* emergency contacts και meeting points;
* evacuation routes;
* grab-first planning;
* medical continuity;
* dependents και accessibility;
* shelter zones;
* damage/recovery;
* vehicles και kits;
* skill coverage;
* decision board;
* incident και field logs;
* numeric field trends;
* training drills και debriefs;
* recovery-cost ledger;
* Situation Brief;
* shift handover;
* τοπικά exports;
* backup/restore state.

## Knowledge Compendium

Το Knowledge Compendium περιέχει **250 αναλυτικά θέματα στα Αγγλικά και 250 αντίστοιχα θέματα στα Ελληνικά**.

Έχει σχεδιαστεί ώστε:

* κάθε θέμα να έχει ξεχωριστό επιχειρησιακό σκοπό;
* τα Αγγλικά και Ελληνικά ζεύγη να παραμένουν συγχρονισμένα;
* το επαναλαμβανόμενο filler να απορρίπτεται από τους quality checks;
* τα ακριβή duplicate payloads να απορρίπτονται;
* να ελέγχονται επαναλαμβανόμενες ουσιαστικές παράγραφοι;
* τα source anchors να επιτρέπουν επανέλεγχο safety-sensitive υλικού όταν επανέλθει η σύνδεση.

## Offline Library

Η Offline Library περιλαμβάνει:

* ζευγαρωμένους Αγγλικούς και Ελληνικούς field guides;
* operational cards;
* worksheets;
* scenario drills;
* pocket references;
* long-form κεφάλαια Knowledge Compendium;
* τοπική αναζήτηση Library;
* readable-document previews;
* SHA-256 hashing τοπικών αρχείων;
* προαιρετική υποστήριξη Kiwix/ZIM-style reference material όπου υπάρχει συμβατό tooling.

Σημαντική συμπεριφορά Library:

* τα αρχεία παραμένουν στη συσκευή;
* τα binary reference packs δεν σαρώνονται σαν απλό κείμενο;
* user-added Library content θεωρείται untrusted από τον τοπικό web server;
* απορρίπτεται path traversal έξω από τη Library.

## Αυτόνομος Survival Reader

Το `Offline Survival Reader.html` παρέχει το Knowledge Compendium χωρίς να χρειάζεται το πλήρες Command Center.

Περιλαμβάνει:

* 250 Αγγλικά κεφάλαια;
* 250 Ελληνικά κεφάλαια;
* ένα self-contained HTML αρχείο;
* local full-text search;
* φίλτρα θεμάτων;
* αγαπημένα;
* reviewed-state tracking;
* mobile-friendly navigation;
* print support;
* χωρίς CDN;
* χωρίς external JavaScript;
* χωρίς external stylesheet;
* χωρίς runtime internet requirement.

Άνοιξέ το με:

```bash
python "Offline Survival.py" --reader
```

## Υποστήριξη Browser Κινητού

Το project δεν επιβάλλει Chromium ή άλλο συγκεκριμένο browser engine.

Σε Android/Termux:

* προτιμά `termux-open-url` όταν υπάρχει;
* χρησιμοποιεί Android VIEW intent ως fallback όπου είναι δυνατό;
* δίνει το localhost URL στον εγκατεστημένο/default browser;
* κρατά τον server σε loopback από προεπιλογή;
* παρέχει ξεχωριστή σελίδα on-phone diagnostics.

Τρέξε:

```bash
python "Offline Survival.py" --phone-browser-test
```

## Επιχειρησιακά Εργαλεία

Το project έχει offline εργαλεία για:

* σχεδιασμό νερού;
* food endurance;
* battery/power budgeting;
* unit conversion;
* distance και bearing calculations;
* waypoints;
* field maps;
* GPX/GeoJSON import και export;
* inventory management;
* expiration tracking;
* contacts και meeting points;
* evacuation planning;
* incident logs;
* field observations;
* household roles;
* skill coverage;
* medical continuity;
* sanitation continuity;
* communications schedules;
* dependents/accessibility;
* damage/recovery;
* decision tracking;
* recovery costs;
* drills και debriefs;
* Situation Brief;
* local backup/restore.

## Ιδιωτικότητα Και Τοπική Αποθήκευση

* Το operational state αποθηκεύεται τοπικά.
* Δεν υπάρχει telemetry.
* Δεν απαιτείται λογαριασμός.
* Δεν απαιτείται cloud storage.
* Τα πλήρη backups μπορεί να περιέχουν ευαίσθητες πληροφορίες νοικοκυριού.
* Τα redacted/template exports δεν περιλαμβάνουν προσωπικό operational state.
* Τα τοπικά backups είναι plaintext εκτός αν προστατεύονται από encryption της συσκευής/filesystem.
* Ο τοπικός server χρησιμοποιεί loopback από προεπιλογή.
* Μην εκθέτεις σκόπιμα το Command Center σε μη αξιόπιστα δίκτυα χωρίς να κατανοείς τις συνέπειες.

## Συντήρηση

* Το `Offline Survival.py` έχει `MAINTENANCE` comments γύρω από σημαντικά trust boundaries και extension points.
* Το repository κρατά σκόπιμα **μόνο ένα Python script** και **κανένα `.sh` αρχείο**.
* Το repository κρατά σκόπιμα **μόνο ένα φυσικό `.json` αρχείο:** `Offline Survival Database.json`.
* Επειδή το standard JSON δεν υποστηρίζει `//` ή `#` comments, οι project-wide maintenance σημειώσεις βρίσκονται στο `_maintenance` metadata object της ενιαίας βάσης.
* Μην ξαναχωρίζεις την ενοποιημένη βάση σε εκατοντάδες φυσικά topic JSON· διατήρησε τα virtual source groups μέσα στο ένα αρχείο.
* Κράτα Αγγλικά και Ελληνικά συγχρονισμένα.
* Μην αυξάνεις το περιεχόμενο με duplicated ή ελαφρά ξαναγραμμένο filler.
* Μην προσθέτεις δεύτερο Python helper script· επέκτεινε το μοναδικό entry point.
* Κράτα το phone-browser behavior engine-neutral.
* Κράτα localhost ως default server binding.
* Τρέχε τους built-in checks μετά από σημαντικές αλλαγές.

Προτεινόμενοι έλεγχοι:

```bash
python "Offline Survival.py" --check
python "Offline Survival.py" --quality
python "Offline Survival.py" --translations
python "Offline Survival.py" --library-quality
python "Offline Survival.py" --self-test
python "Offline Survival.py" --api-test
python "Offline Survival.py" --audit
```

## Σημαντικές Σημειώσεις Ασφάλειας

* Το project είναι βοήθημα ετοιμότητας και αναφοράς.
* Δεν αντικαθιστά υπηρεσίες έκτακτης ανάγκης.
* Δεν αντικαθιστά επίσημες προειδοποιήσεις.
* Δεν αντικαθιστά επαγγελματίες υγείας.
* Δεν αντικαθιστά ειδικούς κατασκευών, ηλεκτρολόγους, πυροσβεστική, utilities, διασώστες, κτηνιάτρους, γεωπόνους, ναυτικές υπηρεσίες ή πολιτική προστασία.
* Οι ζωντανές επίσημες οδηγίες έχουν προτεραιότητα όταν είναι διαθέσιμες.
* Μην μπαίνεις σε επικίνδυνα κτίρια, πλημμυρικά νερά, μολυσμένες περιοχές, ζώνες φωτιάς, ασταθές έδαφος ή ηλεκτρικούς κινδύνους μόνο και μόνο για να ολοκληρώσεις checklist.
* Αν μία κατάσταση ξεπερνά την εκπαίδευση, τον εξοπλισμό ή τις ασφαλείς συνθήκες εργασίας σου, προτεραιότητα είναι η απομάκρυνση, η ασφαλής απομόνωση του κινδύνου όπου είναι δυνατό και η επαγγελματική βοήθεια.
