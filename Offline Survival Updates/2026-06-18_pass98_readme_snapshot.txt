# Offline Survival / Επιβίωση Χωρίς Σύνδεση

**Pass 98 — accessibility, continuity, recovery and usability polish**
**Έκδοση 98 — προσβασιμότητα, συνέχεια, αποκατάσταση και βελτίωση ευχρηστίας**

A dependency-free bilingual knowledge reader and preparedness toolkit for **Android and Termux**. It is designed to remain useful without internet access and combines a large English/Greek database, guided emergency access, search, personal planning tools, exports, and built-in quality checks.

Δίγλωσσο εργαλείο γνώσης και ετοιμότητας χωρίς εξωτερικές βιβλιοθήκες για **Android και Termux**. Είναι σχεδιασμένο ώστε να παραμένει χρήσιμο χωρίς σύνδεση στο διαδίκτυο και συνδυάζει μεγάλη αγγλική/ελληνική βάση, καθοδηγούμενη πρόσβαση σε καταστάσεις ανάγκης, αναζήτηση, εργαλεία προσωπικού σχεδιασμού, εξαγωγές και ενσωματωμένους ελέγχους ποιότητας.

> **Safety boundary / Όριο ασφάλειας:** This project supports preparation, organization, records, safer decisions, and recognition of danger signs. It does not replace 112, official instructions, trained first aid, clinicians, pharmacists, engineers, electricians, gas technicians, or other qualified professionals. / Το έργο βοηθά στην προετοιμασία, την οργάνωση, την καταγραφή, τις ασφαλέστερες αποφάσεις και την αναγνώριση επικίνδυνων σημείων. Δεν αντικαθιστά το 112, τις επίσημες οδηγίες, τις εκπαιδευμένες πρώτες βοήθειες, τους γιατρούς, τους φαρμακοποιούς, τους μηχανικούς, τους ηλεκτρολόγους, τους τεχνικούς αερίου ή άλλους ειδικευμένους επαγγελματίες.

## Current build / Τρέχουσα έκδοση

| Item / Στοιχείο | Count / Πλήθος |
|---|---:|
| Bilingual knowledge entries / Δίγλωσσες εγγραφές γνώσης | **1,682** |
| Required bilingual fields per entry / Απαραίτητα δίγλωσσα πεδία ανά εγγραφή | **42** |
| JSON database files / Αρχεία βάσης JSON | **73** |
| Categories / Κατηγορίες | **138** |
| Duplicate IDs / Διπλότυπα αναγνωριστικά | **0** |
| Duplicate English topics / Διπλότυποι αγγλικοί τίτλοι | **0** |
| Exact duplicate long blocks / Ακριβώς διπλότυπα μεγάλα κείμενα | **0** |
| Exact repeated core text between records / Ακριβώς επαναλαμβανόμενο κύριο κείμενο μεταξύ εγγραφών | **0** |
| Missing or unequal translation pairs / Ελλιπή ή άνισα μεταφραστικά ζεύγη | **0** |
| Reviewable English leakage in Greek fields / Αγγλικό κείμενο προς έλεγχο σε ελληνικά πεδία | **0** |
| Shallow records or known semantic mismatches / Ρηχές εγγραφές ή γνωστές σημασιολογικές αναντιστοιχίες | **0** |
| JSON load errors / Σφάλματα φόρτωσης JSON | **0** |

## What Pass 98 improves / Τι βελτιώνει η Έκδοση 98

### English

- Preserves all **1,642** records from Pass 97 and adds **40 original bilingual cards**.
- Expands practical coverage for the first 30 minutes of an emergency, accessibility, medicine continuity, vehicles, utilities, power outages, recovery, family coordination, Greek islands, villages, coastlines, heat, and prolonged water cuts.
- Rewrites the inherited fallback/support wording in **1,281 records** so it is tied to each card’s actual materials, actions, warnings, failure signs, and safety limits.
- Removes **2,850 exact repeated core-text occurrences** found by the strengthened cross-record audit.
- Adds a **“What is happening now?”** helper that leads directly to relevant records without requiring the user to know the right search term.
- Adds **recently viewed records**, clearer numbering, guided scenario packs, and visible Greek emergency numbers to the terminal menu.
- Adds a visible emergency strip and one-tap hazard searches to the local browser interface.
- Improves Greek category wording and keeps all required English and Greek fields aligned.
- Corrects **20 rural/coastal/mountain records** that a deeper semantic check found had inherited unrelated animal-care procedures.
- Strengthens the release audit so generic legacy wording, shallow records, translation gaps, duplicate text, and domain mistakes are visible rather than ignored.

### Ελληνικά

- Διατηρεί και τις **1.642** εγγραφές της Έκδοσης 97 και προσθέτει **40 πρωτότυπες δίγλωσσες κάρτες**.
- Επεκτείνει την πρακτική κάλυψη για τα πρώτα 30 λεπτά μιας ανάγκης, την προσβασιμότητα, τη συνέχεια φαρμάκων, τα οχήματα, τις παροχές, τις διακοπές ρεύματος, την αποκατάσταση, τον οικογενειακό συντονισμό, τα ελληνικά νησιά, τα χωριά, τις ακτές, τον καύσωνα και τις παρατεταμένες διακοπές νερού.
- Αναδιατυπώνει το παλαιότερο γενικό βοηθητικό κείμενο σε **1.281 εγγραφές**, ώστε να συνδέεται με τα πραγματικά υλικά, βήματα, προειδοποιήσεις, σημάδια αποτυχίας και όρια ασφάλειας κάθε κάρτας.
- Αφαιρεί **2.850 περιπτώσεις ακριβώς επαναλαμβανόμενου κύριου κειμένου** που εντόπισε ο αυστηρότερος έλεγχος μεταξύ εγγραφών.
- Προσθέτει βοηθό **«Τι συμβαίνει τώρα;»**, ο οποίος οδηγεί απευθείας σε σχετικά θέματα χωρίς να απαιτεί γνώση του σωστού όρου αναζήτησης.
- Προσθέτει **πρόσφατα θέματα**, καθαρότερη αρίθμηση, καθοδηγούμενα πακέτα και εμφανείς ελληνικούς αριθμούς ανάγκης στο τερματικό.
- Προσθέτει εμφανή λωρίδα ανάγκης και γρήγορες αναζητήσεις κινδύνων στο τοπικό περιβάλλον περιήγησης.
- Βελτιώνει τη διατύπωση ελληνικών κατηγοριών και διατηρεί ευθυγραμμισμένα όλα τα απαραίτητα αγγλικά και ελληνικά πεδία.
- Διορθώνει **20 εγγραφές για χωριό, ακτή και βουνό** στις οποίες βαθύτερος σημασιολογικός έλεγχος εντόπισε άσχετες διαδικασίες φροντίδας ζώων.
- Ενισχύει τον έλεγχο έκδοσης ώστε παλιά γενικά πρότυπα, ρηχές εγγραφές, μεταφραστικά κενά, διπλότυπο κείμενο και λάθη τομέα να εμφανίζονται αντί να αγνοούνται.

## Fastest way to use it / Γρηγορότερος τρόπος χρήσης

1. Start the program / Άνοιξε το πρόγραμμα.
2. Select English or Greek / Επίλεξε αγγλικά ή ελληνικά.
3. In an active problem, open **1. What is happening now? / Τι συμβαίνει τώρα;**.
4. For preparation, use guided packs, search, readiness check, or the one-page plan / Για προετοιμασία, χρησιμοποίησε τα καθοδηγούμενα πακέτα, την αναζήτηση, τον αυτοέλεγχο ή το μονοσέλιδο σχέδιο.
5. In immediate danger in Greece, call **112**. For poisoning advice, the official Greek Poison Centre number is **210 7793777** / Σε άμεσο κίνδυνο στην Ελλάδα, κάλεσε **112**. Για συμβουλή δηλητηρίασης, ο επίσημος αριθμός του Κέντρου Δηλητηριάσεων είναι **210 7793777**.

## Main menu / Κύριο μενού

1. What is happening now? / Τι συμβαίνει τώρα;
2. Search / Αναζήτηση
3. Guided emergency packs / Καθοδηγούμενα πακέτα έκτακτης ανάγκης
4. Quick emergency cards / Γρήγορες κάρτες έκτακτης ανάγκης
5. Recently viewed / Πρόσφατα θέματα
6. Favorites / Αγαπημένα
7. Browse topics / Περιήγηση θεμάτων
8. Browse categories / Περιήγηση κατηγοριών
9. Browse database files / Περιήγηση αρχείων βάσης
10. Preparedness self-check / Αυτοέλεγχος ετοιμότητας
11. One-page emergency plan / Μονοσέλιδο σχέδιο ανάγκης
12. Local browser interface / Τοπικό περιβάλλον περιήγησης
13. Exports / Εξαγωγές
14. Statistics / Στατιστικά
15. Integrity and translation audit / Έλεγχος ακεραιότητας και μετάφρασης
16. Update logs / Αρχεία ενημερώσεων
17. Switch language / Αλλαγή γλώσσας
18. Reload database / Επαναφόρτωση βάσης

## Guided packs / Καθοδηγούμενα πακέτα

Direct offline groups are available for:

Υπάρχουν άμεσα διαθέσιμες ομάδες χωρίς σύνδεση για:

- first 30 minutes / πρώτα 30 λεπτά,
- earthquakes and aftershocks / σεισμούς και μετασεισμούς,
- wildfires, smoke, and evacuation / δασικές πυρκαγιές, καπνό και εκκένωση,
- floods and severe weather / πλημμύρες και έντονα καιρικά φαινόμενα,
- power outages and utilities / διακοπές ρεύματος και παροχές,
- emergency water and food / νερό και τρόφιμα ανάγκης,
- medicine continuity / συνέχεια φαρμάκων,
- accessibility and support needs / προσβασιμότητα και ανάγκες υποστήριξης,
- travel and vehicles / μετακίνηση και οχήματα,
- cleanup and recovery / καθαρισμό και αποκατάσταση,
- family and information coordination / οικογενειακό συντονισμό και πληροφορίες,
- Greece, islands, villages, and coastal hazards / Ελλάδα, νησιά, χωριά και παράκτιους κινδύνους.

## Knowledge coverage / Κάλυψη γνώσης

The database covers immediate emergencies, household continuity, and long-term recovery, including water, food, sanitation, shelter, weather, navigation, communication, evacuation, cautious first-aid organization, public health, medicine records, accessibility, children, older adults, pets, livestock, tools, power, repair boundaries, agriculture, community operations, education, records, governance, and rebuilding essential systems.

Η βάση καλύπτει άμεσες καταστάσεις ανάγκης, συνέχεια νοικοκυριού και μακροπρόθεσμη αποκατάσταση, όπως νερό, τρόφιμα, υγιεινή, καταφύγιο, καιρός, προσανατολισμός, επικοινωνία, εκκένωση, προσεκτική οργάνωση πρώτων βοηθειών, δημόσια υγεία, αρχεία φαρμάκων, προσβασιμότητα, παιδιά, ηλικιωμένοι, κατοικίδια, κτηνοτροφία, εργαλεία, ενέργεια, όρια επισκευών, γεωργία, κοινοτική λειτουργία, εκπαίδευση, αρχεία, διακυβέρνηση και ανασυγκρότηση βασικών συστημάτων.

## Installation in Termux / Εγκατάσταση στο Termux

Place the ZIP in the Android **Download** folder, then run:

Τοποθέτησε το ZIP στον φάκελο **Download** του Android και εκτέλεσε:

```bash
pkg update -y && pkg install python unzip -y
termux-setup-storage
cd ~
unzip -o "/storage/emulated/0/Download/Offline-Survival-Project-Pass98-Accessibility-Continuity-Polished.zip" -d "$HOME"
cd "$HOME/Offline-Survival-Project-main"
python "Offline Survival.py"
```

No root access or Python package installation is required. / Δεν απαιτείται root ούτε εγκατάσταση εξωτερικών πακέτων Python.

## Safe update of an existing copy / Ασφαλής ενημέρωση υπάρχοντος αντιγράφου

```bash
pkg install python unzip -y
termux-setup-storage
cd "$HOME" || exit 1

if [ -d "Offline-Survival-Project-main" ]; then
    mv "Offline-Survival-Project-main" \
       "Offline-Survival-Project-backup-$(date +%Y%m%d-%H%M%S)"
fi

unzip -o \
"/storage/emulated/0/Download/Offline-Survival-Project-Pass98-Accessibility-Continuity-Polished.zip" \
-d "$HOME"

cd "$HOME/Offline-Survival-Project-main" || exit 1
python "Offline Survival.py"
```

This preserves the previous installation as a dated backup. / Η εντολή διατηρεί την προηγούμενη εγκατάσταση ως αντίγραφο ασφαλείας με ημερομηνία και ώρα.

## Useful commands / Χρήσιμες εντολές

```bash
# English / Αγγλικά
python "Offline Survival.py" --lang en

# Greek / Ελληνικά
python "Offline Survival.py" --lang el

# Machine-readable statistics / Στατιστικά
python "Offline Survival.py" --stats

# Full integrity and translation audit / Πλήρης έλεγχος
python "Offline Survival.py" --audit
```

Expected Pass 98 audit result / Αναμενόμενο αποτέλεσμα ελέγχου Έκδοσης 98:

```json
{
  "duplicate_ids": 0,
  "duplicate_topics": 0,
  "duplicate_blocks": 0,
  "repeated_core_text": 0,
  "missing_pairs": 0,
  "ascii_leaks": 0,
  "legacy_template_flags": 0,
  "semantic_mismatches": 0,
  "shallow_entries": 0,
  "load_errors": 0
}
```

## Project structure / Δομή έργου

```text
Offline-Survival-Project-main/
├── Offline Survival.py
├── README.md
├── LAST_UPDATE.txt
├── MEDICAL_SAFETY_WARNING.md
├── OFFICIAL_SAFETY_SOURCES.md
├── Offline Survival Database/      # 73 bilingual JSON files
├── Offline Survival Updates/       # dated development logs
├── Offline Survival Exports/       # audits, validation, manifest
└── .github/
```

## Local data and privacy / Τοπικά δεδομένα και ιδιωτικότητα

- The program does not require an account or internet connection. / Το πρόγραμμα δεν απαιτεί λογαριασμό ή σύνδεση.
- The browser interface binds to `127.0.0.1` for use on the same device. / Το περιβάλλον περιήγησης συνδέεται στο `127.0.0.1` για χρήση στην ίδια συσκευή.
- Favorites and recent history stay in `.offline_survival_user_state.json`. / Τα αγαπημένα και το πρόσφατο ιστορικό μένουν στο `.offline_survival_user_state.json`.
- Plans, exports, and audits are written to `Offline Survival Exports/`. / Τα σχέδια, οι εξαγωγές και οι έλεγχοι γράφονται στον φάκελο `Offline Survival Exports/`.

## Medical and technical safety / Ιατρική και τεχνική ασφάλεια

Read `MEDICAL_SAFETY_WARNING.md` before relying on health-related material. Do not use this database to calculate doses, diagnose, perform invasive care, override prescriptions, enter unsafe structures, repair energized electrical equipment, work on gas systems, mix hazardous chemicals, or ignore evacuation orders.

Διάβασε το `MEDICAL_SAFETY_WARNING.md` πριν βασιστείς σε υλικό υγείας. Μη χρησιμοποιείς τη βάση για υπολογισμό δόσεων, διάγνωση, επεμβατική φροντίδα, αλλαγή συνταγής, είσοδο σε επικίνδυνη κατασκευή, επισκευή ενεργού ηλεκτρικού εξοπλισμού, εργασία σε σύστημα αερίου, ανάμιξη επικίνδυνων χημικών ή αγνόηση εντολής εκκένωσης.

## Maintenance rules / Κανόνες συντήρησης

Every future pass must preserve useful material, update English and Greek together, avoid copied articles and unsafe procedural detail, cite official sources for high-risk guidance, keep IDs and topics unique, remove exact repeated core text, and run syntax, database, search, terminal, browser/API, translation, and archive tests before release.

Κάθε μελλοντική έκδοση πρέπει να διατηρεί το χρήσιμο υλικό, να ενημερώνει μαζί αγγλικά και ελληνικά, να αποφεύγει αντιγραμμένα άρθρα και επικίνδυνες διαδικαστικές λεπτομέρειες, να αναφέρει επίσημες πηγές για οδηγίες υψηλού κινδύνου, να κρατά μοναδικά αναγνωριστικά και θέματα, να αφαιρεί το ακριβώς επαναλαμβανόμενο κύριο κείμενο και να εκτελεί ελέγχους σύνταξης, βάσης, αναζήτησης, τερματικού, περιβάλλοντος/API, μετάφρασης και τελικού αρχείου πριν από τη δημοσίευση.

## Final reminder / Τελική υπενθύμιση

Offline information works best when prepared **before** an emergency. Save the project locally, print the one-page plan, keep emergency numbers on paper, practice evacuation and safe utility shutoff with qualified guidance, and refresh the project when official guidance changes.

Η γνώση χωρίς σύνδεση λειτουργεί καλύτερα όταν έχει προετοιμαστεί **πριν** από την ανάγκη. Αποθήκευσε το έργο τοπικά, τύπωσε το μονοσέλιδο σχέδιο, κράτησε αριθμούς ανάγκης σε χαρτί, εξασκήσου στην εκκένωση και στην ασφαλή διακοπή παροχών με ειδικευμένη καθοδήγηση και ενημέρωνε το έργο όταν αλλάζουν οι επίσημες οδηγίες.
