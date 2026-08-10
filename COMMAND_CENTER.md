# Command Center

The Command Center is the local operational interface for Offline Survival Project.

## Main Areas

- emergency lookup and verified essentials;
- household planning and readiness;
- inventory, food, water, sanitation, and power operations;
- medical continuity and dependent/accessibility records;
- navigation, routes, vehicles, kits, and evacuation planning;
- communications, accountability, decisions, and shift handovers;
- shelter zoning, damage/recovery, costs, and maintenance;
- drills, incident logs, field observations, and trend viewing;
- Knowledge Atlas and Offline Library search;
- local diagnostics, backup, restore, and redacted template export.

## Knowledge Atlas

- indexes 220 bilingual survival subjects;
- searches the local Knowledge Compendium without an external search service;
- supports domain shortcuts and full-text search;
- tracks reviewed and review-later chapters locally;
- can derive a reading queue from the hazards selected in the Risk Board.

## Phone Browser Workflow

Run:

```bash
python "Offline Survival.py" --web
```

On Android/Termux, the launcher delegates the local URL to the installed/default phone browser. It does not choose Chromium or another browser engine.

For on-device browser checks:

```bash
python "Offline Survival.py" --phone-browser-test
```

The diagnostic page checks the browser actually in use. Results stay local.

## Standalone Reader

```bash
python "Offline Survival.py" --reader
```

`Offline Survival Reader.html` embeds all 220 English and 220 Greek Knowledge Compendium chapters in one file and has no runtime network dependency.

## Operational Privacy

- operational state is stored locally;
- full backups can contain sensitive household information;
- redacted/template export starts from a blank schema instead of partially copying personal state;
- localhost remains the default trust boundary.

---

# Command Center — Ελληνικά

Το Command Center είναι η τοπική επιχειρησιακή διεπαφή του Offline Survival Project.

## Βασικές Περιοχές

- αναζήτηση έκτακτης ανάγκης και επαληθευμένα βασικά θέματα,
- σχεδιασμός νοικοκυριού και ετοιμότητα,
- inventory, τρόφιμα, νερό, υγιεινή και ενέργεια,
- ιατρική συνέχεια και εξαρτώμενα άτομα/προσβασιμότητα,
- πλοήγηση, διαδρομές, οχήματα, κιτ και εκκένωση,
- επικοινωνίες, λογοδοσία, αποφάσεις και παράδοση βάρδιας,
- ζώνες καταφυγίου, ζημιές/αποκατάσταση, κόστη και συντήρηση,
- ασκήσεις, incident logs, παρατηρήσεις πεδίου και τάσεις,
- Άτλας Γνώσης και αναζήτηση Offline Library,
- τοπικά diagnostics, backup, restore και κενό redacted template.

## Άτλας Γνώσης

- ευρετηριάζει 220 δίγλωσσα θέματα επιβίωσης,
- αναζητεί τοπικά τη Συλλογή Γνώσης χωρίς εξωτερική υπηρεσία,
- υποστηρίζει θεματικές συντομεύσεις και πλήρη αναζήτηση κειμένου,
- αποθηκεύει τοπικά κατάσταση μελέτης/μελέτης αργότερα,
- μπορεί να δημιουργήσει σειρά μελέτης από τους κινδύνους του Risk Board.

## Ροή Browser Τηλεφώνου

```bash
python "Offline Survival.py" --web
```

Σε Android/Termux, ο launcher παραδίδει το τοπικό URL στον εγκατεστημένο/default browser. Δεν επιλέγει Chromium ή άλλον browser engine.

Για διαγνωστικά πάνω στη συσκευή:

```bash
python "Offline Survival.py" --phone-browser-test
```

Η σελίδα ελέγχει τον browser που χρησιμοποιείται πραγματικά. Τα αποτελέσματα παραμένουν τοπικά.

## Αυτόνομος Αναγνώστης

```bash
python "Offline Survival.py" --reader
```

Το `Offline Survival Reader.html` ενσωματώνει 220 αγγλικά και 220 ελληνικά κεφάλαια της Συλλογής Γνώσης σε ένα αρχείο και δεν χρειάζεται δίκτυο κατά την εκτέλεση.

## Επιχειρησιακή Ιδιωτικότητα

- η επιχειρησιακή κατάσταση αποθηκεύεται τοπικά,
- τα πλήρη backups μπορεί να περιέχουν ευαίσθητες πληροφορίες,
- το redacted/template export ξεκινά από κενό schema και όχι από μερικώς καθαρισμένα προσωπικά δεδομένα,
- το localhost παραμένει το προεπιλεγμένο όριο εμπιστοσύνης.
