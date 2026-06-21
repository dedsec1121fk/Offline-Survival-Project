# Offline Survival

**Pass 103 — daily operations expansion, urgent-helper polish, and GitHub-safe release**

Offline Survival is a dependency-free English/Greek preparedness reader for Android and Termux. The complete database, search, guided packs, planning tools, favorites, exports, validation tools, and local browser work offline on the phone.

[Μετάβαση στην ελληνική ενότητα](#επιβίωση-χωρίς-σύνδεση)

> **Safety boundary:** This project helps with preparation, organization, records, safer decisions, and recognition of danger signs. It does not replace 112, official instructions, certified first-aid training, clinicians, pharmacists, engineers, electricians, gas technicians, veterinarians, or other qualified professionals.

## Current build

| Item | Pass 103 status |
|---|---:|
| Bilingual knowledge entries | **1,752** |
| Authoritative JSON files | **75** |
| Categories | **184** |
| Fields per record | **48** |
| New Pass 103 practical cards | **40** |
| Duplicate IDs/topics | **0** |
| Accidental repeated core instructions | **0** |
| Missing or unequal English/Greek pairs | **0** |
| Reviewable English leakage in Greek fields | **0** |
| Entries without sources | **0** |
| JSON loading errors | **0** |
| Files at or above 40 MB | **0** |
| Largest repository file | **2,799,797 bytes** |

All Pass 102 knowledge, translations, identifiers, and sources were preserved. Pass 103 adds practical daily-operation cards for moments that often happen after the first emergency shock: night movement, smoke in stairwells, phone-battery triage, generator sharing, sewer backup, water queues, welfare checks, rumours, shelter conflict, tool sharing, medicine refill tracking, child separation, fuel separation, and bilingual shelter notices.

## Pass 103 improvements

- Added **40** fully bilingual practical field cards.
- Added new urgent-helper choices for night evacuation, apartment-stair smoke, sewer backup, rumour/welfare/shelter conflict, and other daily emergency operations.
- Updated browser quick buttons so phone users can jump directly to first five minutes, night routes, smoke stairs, phone battery, generator safety, water queue, sewer backup, rumours, welfare checks, documents, pets, maps, recovery, digital continuity, and food.
- Added scenario-pack labels for shelter operations and animal/pet support.
- Rebuilt the compact offline search index for all **1,752** entries.
- Updated release documentation, validation reports, audit summaries, and the SHA-256 manifest.
- Kept every repository file safely below the 40 MB GitHub limit.

## Fastest way to use it

1. Run `python "Offline Survival.py"`.
2. Choose English or Greek.
3. During an active problem, open **1. What is happening now?**
4. For preparation, use guided packs, search, the self-check, or the one-page emergency-plan builder.
5. In immediate danger in Greece, call **112**. For poisoning advice, use the official Greek Poison Centre number **210 7793777**.

Official instructions and emergency services always override an offline card.

## Termux installation or update

Place the ZIP in the phone's **Download** folder and run:

```bash
pkg install python unzip -y && termux-setup-storage && cd "$HOME" && if [ -d "Offline-Survival-Project-main" ]; then mv "Offline-Survival-Project-main" "Offline-Survival-Project-backup-$(date +%Y%m%d-%H%M%S)"; fi && unzip -o "/storage/emulated/0/Download/Offline-Survival-Project-Pass103-Daily-Operations-Expanded-Polished.zip" -d "$HOME" && cd "$HOME/Offline-Survival-Project-main" && python "Offline Survival.py"
```

The previous installation is retained as a dated backup.

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
12. Launch local browser interface
13. Export knowledge
14. Database statistics
15. Integrity and translation audit
16. Update logs
17. Official safety-source guide
18. Switch language
19. Reload database
0. Exit

In long category, file, and update lists, use `N` and `P` for pages, `/text` to filter, `C` to clear the filter, and Enter to return.

## Search and command-line use

Search accepts English, Greek, and Greek without accents. The compact SQLite index is verified against the authoritative JSON database before use. If it is missing or stale, the application safely searches the JSON records instead.

```bash
python "Offline Survival.py" --search "sewer backup" --lang en
python "Offline Survival.py" --search "λυματα αποχετευση" --lang el
python "Offline Survival.py" --entry pass103-0006-sewer-backup-stop-rules-for-a-home --lang en
python "Offline Survival.py" --stats
python "Offline Survival.py" --audit
python "Offline Survival.py" --version
```

## Local browser interface

The browser server listens only on `127.0.0.1`, for the same phone. It includes English/Greek switching, accent-insensitive search, related-result fallback, category and priority filters, shared favorites/recent entries, persistent text size, quick hazard buttons, complete entry cards, copy/print actions, and phone-friendly layout.

## Maintenance

```bash
python "Maintenance/Rebuild Search Index.py"
python "Maintenance/Check GitHub File Sizes.py"
python "Maintenance/Run Full Validation.py"
```

## Project structure

```text
Offline-Survival-Project-main/
├── Offline Survival.py
├── Offline Survival Search Index.sqlite3
├── Offline Survival Database/        # 75 authoritative JSON files
├── Maintenance/                       # index, size, and full validation tools
├── Offline Survival Exports/          # current and historical audit material
├── Offline Survival Updates/          # release history
├── OFFICIAL_SAFETY_SOURCES.md
├── MEDICAL_SAFETY_WARNING.md
├── RELEASE_VALIDATION_PASS103.txt
├── LAST_UPDATE.txt
└── README.md
```

## Reference policy

The project favors government, public-health, emergency-service, recognized humanitarian, and primary technical sources. Source lists are reference starting points, not a claim that every sentence is copied from or separately endorsed by a listed organization. The bilingual text is original and does not reproduce complete articles or manuals.

See `OFFICIAL_SAFETY_SOURCES.md` for source families and safety boundaries.

---

# Επιβίωση Χωρίς Σύνδεση

**Έκδοση 103 — επέκταση καθημερινών λειτουργιών, βελτίωση βοηθού ανάγκης και έκδοση ασφαλής για GitHub**

Το Offline Survival είναι δίγλωσσο εργαλείο ετοιμότητας χωρίς εξωτερικές βιβλιοθήκες για Android και Termux. Ολόκληρη η βάση, η αναζήτηση, τα καθοδηγούμενα πακέτα, τα εργαλεία σχεδιασμού, τα αγαπημένα, οι εξαγωγές, οι έλεγχοι και το τοπικό περιβάλλον λειτουργούν χωρίς διαδίκτυο στο κινητό.

> **Όριο ασφάλειας:** Το έργο βοηθά στην προετοιμασία, την οργάνωση, τις καταγραφές, τις ασφαλέστερες αποφάσεις και την αναγνώριση σημείων κινδύνου. Δεν αντικαθιστά το 112, τις επίσημες οδηγίες, την πιστοποιημένη εκπαίδευση πρώτων βοηθειών, γιατρούς, φαρμακοποιούς, μηχανικούς, ηλεκτρολόγους, τεχνικούς αερίου, κτηνιάτρους ή άλλους ειδικούς.

## Τρέχουσα έκδοση

| Στοιχείο | Κατάσταση Έκδοσης 103 |
|---|---:|
| Δίγλωσσες εγγραφές γνώσης | **1,752** |
| Επίσημα αρχεία JSON | **75** |
| Κατηγορίες | **184** |
| Πεδία ανά εγγραφή | **48** |
| Νέες πρακτικές κάρτες Έκδοσης 103 | **40** |
| Διπλά αναγνωριστικά ή θέματα | **0** |
| Τυχαίες επαναλήψεις βασικών οδηγιών | **0** |
| Ελλιπή ή άνισα ζεύγη Αγγλικών/Ελληνικών | **0** |
| Αγγλικά που χρειάζονται έλεγχο σε ελληνικά πεδία | **0** |
| Εγγραφές χωρίς πηγές | **0** |
| Σφάλματα φόρτωσης JSON | **0** |
| Αρχεία ίσα ή πάνω από 40 MB | **0** |
| Μεγαλύτερο αρχείο αποθετηρίου | **2,799,797 bytes** |

Διατηρήθηκαν όλες οι γνώσεις, μεταφράσεις, αναγνωριστικά και πηγές της Έκδοσης 102. Η Έκδοση 103 προσθέτει πρακτικές κάρτες καθημερινής λειτουργίας για καταστάσεις μετά το πρώτο σοκ: νυχτερινή μετακίνηση, καπνό σε σκάλες, μπαταρία κινητού, κοινή γεννήτρια, επιστροφή λυμάτων, ουρά νερού, έλεγχο ηλικιωμένων, φήμες, σύγκρουση σε καταφύγιο, κοινά εργαλεία, ανανέωση φαρμάκων, χωρισμό παιδιών, καύσιμα και δίγλωσσες ανακοινώσεις.

## Βελτιώσεις Έκδοσης 103

- Προστέθηκαν **40** πλήρως δίγλωσσες πρακτικές κάρτες πεδίου.
- Προστέθηκαν νέες επιλογές στον βοηθό ανάγκης για νυχτερινή εκκένωση, καπνό σε κλιμακοστάσιο, επιστροφή λυμάτων, φήμες, ελέγχους ευημερίας, σύγκρουση σε καταφύγιο και πρακτικές καθημερινές λειτουργίες.
- Ενημερώθηκαν τα γρήγορα κουμπιά του τοπικού περιβάλλοντος για χρήση από κινητό.
- Προστέθηκαν ετικέτες πακέτων για λειτουργίες καταφυγίου και ζώα/κατοικίδια.
- Ξαναχτίστηκε το συμπαγές ευρετήριο αναζήτησης για όλες τις **1,752** εγγραφές.
- Ενημερώθηκαν τεκμηρίωση, αναφορές ελέγχου, σύνοψη ακεραιότητας και αρχείο SHA-256.
- Κάθε αρχείο του αποθετηρίου παραμένει με ασφάλεια κάτω από το όριο των 40 MB.

## Γρήγορη χρήση

1. Τρέξε `python "Offline Survival.py"`.
2. Διάλεξε Αγγλικά ή Ελληνικά.
3. Σε ενεργό πρόβλημα, άνοιξε **1. Τι συμβαίνει τώρα;**
4. Για προετοιμασία, χρησιμοποίησε τα πακέτα, την αναζήτηση, τον αυτοέλεγχο ή το μονοσέλιδο σχέδιο ανάγκης.
5. Σε άμεσο κίνδυνο στην Ελλάδα, κάλεσε **112**. Για δηλητηρίαση, χρησιμοποίησε τον επίσημο αριθμό του Κέντρου Δηλητηριάσεων **210 7793777**.

Οι επίσημες οδηγίες και οι υπηρεσίες ανάγκης υπερισχύουν πάντα κάθε κάρτας εκτός σύνδεσης.

## Εγκατάσταση ή ενημέρωση σε Termux

Βάλε το ZIP στον φάκελο **Download** του κινητού και τρέξε:

```bash
pkg install python unzip -y && termux-setup-storage && cd "$HOME" && if [ -d "Offline-Survival-Project-main" ]; then mv "Offline-Survival-Project-main" "Offline-Survival-Project-backup-$(date +%Y%m%d-%H%M%S)"; fi && unzip -o "/storage/emulated/0/Download/Offline-Survival-Project-Pass103-Daily-Operations-Expanded-Polished.zip" -d "$HOME" && cd "$HOME/Offline-Survival-Project-main" && python "Offline Survival.py"
```

Η προηγούμενη εγκατάσταση κρατιέται ως αντίγραφο με ημερομηνία.
