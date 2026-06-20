# Offline Survival

**Pass 100 — structural continuity, unsafe-water, accessibility, digital-resilience, and recovery expansion**

Offline Survival is a dependency-free English/Greek preparedness reader for
Android and Termux. It keeps the complete knowledge database, search,
emergency navigation, planning tools, exports, favorites, and the local web
interface available without an internet connection.

> **Safety boundary:** This project supports preparation, organization,
> records, safer decisions, and recognition of danger signs. It does not
> replace 112, official instructions, certified first-aid training, clinicians,
> pharmacists, engineers, electricians, gas technicians, veterinarians, or
> other qualified professionals.

## Current build

| Item | Pass 100 status |
|---|---:|
| Bilingual knowledge entries | **1,712** |
| JSON database files | **74** |
| Categories | **144** |
| Fields per record | **48** |
| Duplicate IDs | **0** |
| Duplicate English topics | **0** |
| Duplicate Greek topics | **0** |
| Accidental exact repeated core text | **0** |
| Missing or unequal English/Greek pairs | **0** |
| Reviewable English leakage in Greek fields | **0** |
| Entries without reference sources | **0** |
| Shallow records detected by the release audit | **0** |
| JSON loading errors | **0** |

“Zero repeated core text” means the audit found no accidentally copied complete
instruction, warning, paragraph, or list item between different records.
Necessary terms, emergency boundaries, official numbers, and source links may
recur where accuracy requires them.

## What Pass 100 adds and improves

- Preserves all **1,682** Pass 99 entries and adds **30 new, fully bilingual field cards** without reusing an existing identifier or topic.
- Adds dedicated structural-collapse, entrapment, damaged-building, missing-person, and family-reunification procedures.
- Adds landslide, post-wildfire debris-flow, hail, destructive-wind, and whiteout travel-stop cards.
- Distinguishes **boil-water**, **do-not-drink**, and **do-not-use** advisories and adds infant-formula, infant-equipment cleaning, and flooded-well continuity guidance.
- Adds person-led wheelchair evacuation, sensory communication, hearing-device power, oxygen-concentrator outage, and dialysis-disruption plans.
- Adds cash-only outage, protected document, damage-evidence, ransomware-isolation, and lost-phone account-recovery cards.
- Adds service-animal and livestock evacuation, snakebite, suspected poisonous-mushroom exposure, and staged return-home procedures.
- Integrates the new cards into **What is happening now?**, Guided emergency packs, Quick emergency cards, English search, and accent-insensitive Greek search.
- Makes `--lang en` and `--lang el` work correctly on a completely fresh first launch and exits cleanly on end-of-input.
- Rebuilds and signs the bundled SQLite full-text index for all **1,712** records.
- Retains the Pass 99 strict audit rules for duplicate IDs/topics, exact repeated core text, bilingual parity, Greek-language leakage, shallow records, semantic mismatches, source lists, placeholders, and JSON load failures.

## Fastest way to use it

1. Run the program.
2. Choose English or Greek.
3. During an active problem, open **1. What is happening now?**
4. For preparation, use **Guided emergency packs**, search, the preparedness
   self-check, or the one-page emergency-plan builder.
5. In immediate danger in Greece, call **112**. For poisoning advice, use the
   official Greek Poison Centre number **210 7793777**.

Official instructions and emergency services always override an offline card.

## Termux installation

Put the ZIP in the phone’s **Download** folder, then run:

```bash
pkg install python unzip -y
termux-setup-storage

cd "$HOME" || exit 1

if [ -d "Offline-Survival-Project-main" ]; then
    mv "Offline-Survival-Project-main" \
       "Offline-Survival-Project-backup-$(date +%Y%m%d-%H%M%S)"
fi

unzip -o \
"/storage/emulated/0/Download/Offline-Survival-Project-Pass100-Structural-Continuity-Recovery-Expansion.zip" \
-d "$HOME"

cd "$HOME/Offline-Survival-Project-main" || exit 1
python "Offline Survival.py"
```

The previous installation is preserved as a dated backup.

## Main menu

1. What is happening now?
2. Search
3. Guided emergency packs
4. Quick emergency cards
5. Recently viewed
6. Favorites
7. Browse topics
8. Browse categories
9. Browse database files
10. Preparedness self-check
11. Build a one-page emergency plan
12. Launch the local browser interface
13. Export knowledge
14. Database statistics
15. Integrity and translation audit
16. Update logs
17. Official safety-source guide
18. Switch language
19. Reload database
0. Exit

## Search

Search accepts English, Greek, and Greek text without accents. The bundled file
`Offline Survival Search Index.sqlite3` contains only a normalized search index;
the 74 JSON files remain the authoritative knowledge database. The application
checks the index against a SHA-256 signature of the database before using it.
If the index is absent or stale, search falls back to the JSON data rather than
returning unverified results.

Examples:

```bash
python "Offline Survival.py" --stats
python "Offline Survival.py" --audit
python "Offline Survival.py" --lang el
```

## Local browser interface

The browser interface runs only on `127.0.0.1` and is intended for the same
phone. It provides:

- English/Greek language switching
- localized category filters
- accent-insensitive search
- quick hazard buttons
- favorites stored in the browser
- readable cards for steps, warnings, alternatives, failure signs, and sources
- copy and print actions
- larger/smaller text controls

Stop the local server by returning to Termux and pressing Enter.

## Project structure

```text
Offline-Survival-Project-main/
├── Offline Survival.py
├── Offline Survival Search Index.sqlite3
├── Offline Survival Database/        # 74 authoritative JSON files
├── Offline Survival Exports/         # current and historical audit material
├── Offline Survival Updates/         # release history
├── OFFICIAL_SAFETY_SOURCES.md
├── MEDICAL_SAFETY_WARNING.md
├── RELEASE_VALIDATION_PASS100.txt
├── LAST_UPDATE.txt
└── README.md
```

## Reference policy

The project favors current pages from governments, public-health agencies,
emergency services, recognized humanitarian organizations, and primary
technical guidance. Source lists are reference starting points, not a claim
that every sentence is copied from or individually endorsed by a listed body.
The bilingual text is original and intentionally avoids reproducing complete
articles or manuals.

See `OFFICIAL_SAFETY_SOURCES.md` for the reviewed source families and safety
boundaries.

---

# Επιβίωση Χωρίς Σύνδεση

**Έκδοση 100 — επέκταση δομικής συνέχειας, μη ασφαλούς νερού, προσβασιμότητας, ψηφιακής ανθεκτικότητας και αποκατάστασης**

Το Offline Survival είναι δίγλωσσο εργαλείο ετοιμότητας χωρίς εξωτερικές
βιβλιοθήκες για Android και Termux. Διατηρεί διαθέσιμα χωρίς διαδίκτυο ολόκληρη
τη βάση γνώσης, την αναζήτηση, την πλοήγηση σε καταστάσεις ανάγκης, τα εργαλεία
σχεδιασμού, τις εξαγωγές, τα αγαπημένα και το τοπικό περιβάλλον περιήγησης.

> **Όριο ασφάλειας:** Το έργο βοηθά στην προετοιμασία, την οργάνωση, την
> καταγραφή, τις ασφαλέστερες αποφάσεις και την αναγνώριση επικίνδυνων σημείων.
> Δεν αντικαθιστά το 112, τις επίσημες οδηγίες, την πιστοποιημένη εκπαίδευση
> πρώτων βοηθειών, τους γιατρούς, τους φαρμακοποιούς, τους μηχανικούς, τους
> ηλεκτρολόγους, τους τεχνικούς αερίου, τους κτηνιάτρους ή άλλους ειδικευμένους
> επαγγελματίες.

## Τρέχουσα έκδοση

| Στοιχείο | Κατάσταση Έκδοσης 100 |
|---|---:|
| Δίγλωσσες εγγραφές γνώσης | **1.712** |
| Αρχεία βάσης JSON | **74** |
| Κατηγορίες | **144** |
| Πεδία ανά εγγραφή | **48** |
| Διπλότυπα αναγνωριστικά | **0** |
| Διπλότυποι αγγλικοί τίτλοι | **0** |
| Διπλότυποι ελληνικοί τίτλοι | **0** |
| Ακούσια ακριβώς επαναλαμβανόμενο κύριο κείμενο | **0** |
| Ελλιπή ή άνισα αγγλικά/ελληνικά ζεύγη | **0** |
| Αγγλικό κείμενο προς έλεγχο σε ελληνικά πεδία | **0** |
| Εγγραφές χωρίς πηγές αναφοράς | **0** |
| Ρηχές εγγραφές που εντόπισε ο έλεγχος έκδοσης | **0** |
| Σφάλματα φόρτωσης JSON | **0** |

Το «μηδενικό επαναλαμβανόμενο κύριο κείμενο» σημαίνει ότι ο έλεγχος δεν βρήκε
τυχαία αντιγραμμένη πλήρη οδηγία, προειδοποίηση, παράγραφο ή στοιχείο λίστας
ανάμεσα σε διαφορετικές εγγραφές. Αναγκαίοι όροι, όρια έκτακτης ανάγκης,
επίσημοι αριθμοί και σύνδεσμοι πηγών μπορούν να επαναλαμβάνονται όταν το απαιτεί
η ακρίβεια.

## Τι προσθέτει και βελτιώνει η Έκδοση 100

- Διατηρεί και τις **1.682** εγγραφές της Έκδοσης 99 και προσθέτει **30 νέες, πλήρως δίγλωσσες κάρτες πεδίου** χωρίς επανάληψη αναγνωριστικού ή θέματος.
- Προσθέτει ειδικές διαδικασίες για δομική κατάρρευση, παγίδευση, κατεστραμμένο κτίριο, αγνοούμενο άτομο και οικογενειακή επανένωση.
- Προσθέτει κάρτες για κατολίσθηση, ροή φερτών υλικών μετά από πυρκαγιά, χαλάζι, καταστροφικό άνεμο και διακοπή μετακίνησης σε μηδενική ορατότητα.
- Ξεχωρίζει τις οδηγίες **βρασμού**, **μη πόσης** και **πλήρους απαγόρευσης χρήσης** νερού και προσθέτει συνέχεια βρεφικού γάλακτος, καθαρισμό ειδών σίτισης και αποκατάσταση πλημμυρισμένου πηγαδιού.
- Προσθέτει σχέδια για εκκένωση αμαξιδίου με επιλογές του ατόμου, αισθητηριακή επικοινωνία, ενέργεια συσκευών ακοής, διακοπή συμπυκνωτή οξυγόνου και διαταραχή αιμοκάθαρσης.
- Προσθέτει κάρτες για πληρωμές μόνο με μετρητά, προστατευμένα έγγραφα, αποδεικτικά ζημιών, απομόνωση επίθεσης με λύτρα και ανάκτηση λογαριασμών μετά από απώλεια τηλεφώνου.
- Προσθέτει εκκένωση ζώου βοήθειας και παραγωγικών ζώων, αντιμετώπιση δαγκώματος φιδιού, ύποπτη δηλητηρίαση από μανιτάρι και σταδιακή ασφαλή επιστροφή στο σπίτι.
- Ενσωματώνει τις νέες κάρτες στο **Τι συμβαίνει τώρα;**, στα καθοδηγούμενα πακέτα, στις γρήγορες κάρτες και στην αγγλική ή ελληνική αναζήτηση χωρίς τόνους.
- Διορθώνει τα `--lang en` και `--lang el` ώστε να λειτουργούν και στην πρώτη εκκίνηση και προσθέτει καθαρή έξοδο όταν τελειώσει η είσοδος.
- Ανακατασκευάζει και υπογράφει το πλήρες ευρετήριο SQLite για όλες τις **1.712** εγγραφές.
- Διατηρεί τους αυστηρούς ελέγχους της Έκδοσης 99 για διπλότυπα, επαναλαμβανόμενο βασικό κείμενο, δίγλωσση ισοτιμία, αγγλική διαρροή στα ελληνικά, ρηχές εγγραφές, σημασιολογικές αστοχίες, πηγές, προσωρινούς τίτλους και σφάλματα φόρτωσης.

## Γρηγορότερη χρήση

1. Άνοιξε το πρόγραμμα.
2. Επίλεξε αγγλικά ή ελληνικά.
3. Σε ενεργό πρόβλημα, άνοιξε **1. Τι συμβαίνει τώρα;**
4. Για προετοιμασία, χρησιμοποίησε τα **Καθοδηγούμενα πακέτα έκτακτης ανάγκης**,
   την αναζήτηση, τον αυτοέλεγχο ετοιμότητας ή το μονοσέλιδο σχέδιο ανάγκης.
5. Σε άμεσο κίνδυνο στην Ελλάδα, κάλεσε **112**. Για συμβουλή δηλητηρίασης,
   χρησιμοποίησε τον επίσημο αριθμό του Κέντρου Δηλητηριάσεων **210 7793777**.

Οι επίσημες οδηγίες και οι υπηρεσίες έκτακτης ανάγκης υπερισχύουν πάντα μιας
κάρτας χωρίς σύνδεση.

## Εγκατάσταση στο Termux

Τοποθέτησε το ZIP στον φάκελο **Download** του κινητού και εκτέλεσε την εντολή
της αγγλικής ενότητας παραπάνω. Η προηγούμενη εγκατάσταση διατηρείται αυτόματα
ως αντίγραφο ασφαλείας με ημερομηνία και ώρα.

## Κύριο μενού

1. Τι συμβαίνει τώρα;
2. Αναζήτηση
3. Καθοδηγούμενα πακέτα έκτακτης ανάγκης
4. Γρήγορες κάρτες έκτακτης ανάγκης
5. Πρόσφατα θέματα
6. Αγαπημένα
7. Περιήγηση θεμάτων
8. Περιήγηση κατηγοριών
9. Περιήγηση αρχείων βάσης
10. Αυτοέλεγχος ετοιμότητας
11. Δημιουργία μονοσέλιδου σχεδίου ανάγκης
12. Άνοιγμα τοπικού περιβάλλοντος περιήγησης
13. Εξαγωγή γνώσης
14. Στατιστικά βάσης
15. Έλεγχος ακεραιότητας και μετάφρασης
16. Αρχεία ενημερώσεων
17. Οδηγός επίσημων πηγών ασφάλειας
18. Αλλαγή γλώσσας
19. Επαναφόρτωση βάσης
0. Έξοδος

## Αναζήτηση

Η αναζήτηση δέχεται αγγλικά, ελληνικά και ελληνικό κείμενο χωρίς τόνους. Το
αρχείο `Offline Survival Search Index.sqlite3` περιέχει μόνο κανονικοποιημένο
ευρετήριο αναζήτησης· τα 74 αρχεία JSON παραμένουν η έγκυρη βάση γνώσης. Η
εφαρμογή ελέγχει το ευρετήριο με υπογραφή SHA-256 της βάσης πριν το χρησιμοποιήσει.
Αν λείπει ή είναι παλιό, η εφαρμογή επιστρέφει στα δεδομένα JSON αντί να
εμφανίσει μη επαληθευμένα αποτελέσματα.

## Τοπικό περιβάλλον περιήγησης

Το περιβάλλον λειτουργεί μόνο στη διεύθυνση `127.0.0.1` και προορίζεται για το
ίδιο κινητό. Παρέχει αλλαγή γλώσσας, τοπικοποιημένα φίλτρα, αναζήτηση χωρίς
τόνους, γρήγορα κουμπιά κινδύνων, αγαπημένα, πλήρεις κάρτες οδηγιών, αντιγραφή,
εκτύπωση και ρύθμιση μεγέθους κειμένου.

## Πολιτική πηγών

Το έργο προτιμά ενημερωμένες σελίδες κυβερνήσεων, φορέων δημόσιας υγείας,
υπηρεσιών έκτακτης ανάγκης, αναγνωρισμένων ανθρωπιστικών οργανισμών και
πρωτογενών τεχνικών οδηγιών. Οι λίστες πηγών είναι σημεία αφετηρίας αναφοράς και
όχι ισχυρισμός ότι κάθε πρόταση αντιγράφηκε ή εγκρίθηκε ξεχωριστά από τον
αντίστοιχο φορέα. Το δίγλωσσο κείμενο είναι πρωτότυπο και δεν αναπαράγει πλήρη
άρθρα ή εγχειρίδια.

Δες το `OFFICIAL_SAFETY_SOURCES.md` για τις ελεγμένες οικογένειες πηγών και τα
όρια ασφάλειας.
