<div align="center">
  <h1>Offline Survival</h1>
  <p><strong>Bilingual offline-first survival knowledge system for Termux on Android</strong></p>
  <p>
    <img src="https://img.shields.io/badge/Platform-Android%20(Termux)-brightgreen.svg" alt="Platform: Android (Termux)">
    <img src="https://img.shields.io/badge/Language-Python-yellow.svg" alt="Language: Python">
    <img src="https://img.shields.io/badge/Mode-Offline--First-blue.svg" alt="Mode: Offline-First">
    <img src="https://img.shields.io/badge/Content-English%20%2B%20Greek-purple.svg" alt="Content: English + Greek">
  </p>
</div>

---

<details open>
<summary><strong>🇬🇧 English</strong></summary>

Offline Survival is a serious offline knowledge and workflow system designed for use when internet access is absent, weak, censored, unreliable, or too dangerous to depend on.

It is built for Termux on Android and is meant to remain useful during:

- emergency response
- long blackouts
- water and sanitation disruption
- food scarcity
- medical isolation
- civil instability
- wartime civilian hardship
- communications failure
- digital-dependency collapse
- long-term household and small-group continuity
- rebuilding after system failure

</details>

<details open>
<summary><strong>🇬🇷 Ελληνικά</strong></summary>

Το Offline Survival είναι ένα σοβαρό offline σύστημα γνώσης και ροών εργασίας σχεδιασμένο για χρήση όταν η πρόσβαση στο internet απουσιάζει, είναι αδύναμη, λογοκριμένη, αναξιόπιστη ή πολύ επικίνδυνη για να βασιστείς σε αυτήν.

Είναι χτισμένο για Termux σε Android και στοχεύει να παραμένει χρήσιμο σε:

- άμεση ανταπόκριση έκτακτης ανάγκης
- μεγάλης διάρκειας blackouts
- διακοπή νερού και υγιεινής
- έλλειψη τροφής
- ιατρική απομόνωση
- κοινωνική αστάθεια
- δυσκολία αμάχων σε πόλεμο
- αποτυχία επικοινωνιών
- κατάρρευση εξάρτησης από ψηφιακά συστήματα
- μακροχρόνια συνέχεια νοικοκυριού και μικρής ομάδας
- ξαναχτίσιμο μετά από αποτυχία συστημάτων

</details>

---

## Repository Structure

```text
Offline Survival.py
Offline Survival Database/
Offline Survival Updates/
```

### What each part does

- `Offline Survival.py`
  - main offline menu-driven Termux interface
  - search, browse, read, export, bookmarks, integrity checks, update-log reading
- `Offline Survival Database/`
  - topic-based JSON knowledge files
  - combined bilingual English/Greek content
- `Offline Survival Updates/`
  - encrypted project continuation logs in `.txt` format
  - planning, coverage tracking, duplicate-avoidance notes, and development history

---

## How to Get the Repository from GitHub and Open It in Termux

<details>
<summary><strong>🇬🇧 English</strong></summary>

Open this repository on GitHub, tap **Code**, and choose **Download ZIP**. The ZIP usually downloads into your phone's internal storage **Downloads** folder as:

```bash
Offline-Survival-Project-main.zip
```

After the ZIP finishes downloading, open **Termux** and run:

```bash
rm -rf ~/Offline-Survival-Project-main && unzip -o "/storage/emulated/0/Download/Offline-Survival-Project-main.zip" -d ~
```

That command removes the previous extracted repository from your Termux home directory if it already exists, then extracts the new ZIP there so it is replaced cleanly.

### Step by step

1. Open the repository on GitHub.
2. Tap **Code**.
3. Tap **Download ZIP**.
4. Wait for the download to finish.
5. Open **Termux**.
6. Paste and run:

```bash
rm -rf ~/Offline-Survival-Project-main && unzip -o "/storage/emulated/0/Download/Offline-Survival-Project-main.zip" -d ~
```

### After extracting

The repository will be in:

```bash
~/Offline-Survival-Project-main
```

To enter it:

```bash
cd ~/Offline-Survival-Project-main
```

To list the files:

```bash
ls
```

### Storage permission

If Termux does not yet have storage permission, run:

```bash
termux-setup-storage
```

That usually only needs to be done once.

</details>

<details>
<summary><strong>🇬🇷 Ελληνικά</strong></summary>

Άνοιξε αυτό το repository στο GitHub, πάτησε **Code** και μετά **Download ZIP**. Το ZIP συνήθως κατεβαίνει στον φάκελο **Downloads** της εσωτερικής αποθήκευσης με όνομα:

```bash
Offline-Survival-Project-main.zip
```

Αφού ολοκληρωθεί το κατέβασμα, άνοιξε το **Termux** και τρέξε:

```bash
rm -rf ~/Offline-Survival-Project-main && unzip -o "/storage/emulated/0/Download/Offline-Survival-Project-main.zip" -d ~
```

Αυτή η εντολή διαγράφει πρώτα τον παλιό extracted φάκελο από το home directory του Termux αν υπάρχει ήδη και μετά κάνει extract το νέο ZIP εκεί ώστε να αντικατασταθεί καθαρά.

### Βήμα προς βήμα

1. Άνοιξε το repository στο GitHub.
2. Πάτησε **Code**.
3. Πάτησε **Download ZIP**.
4. Περίμενε να ολοκληρωθεί το κατέβασμα.
5. Άνοιξε το **Termux**.
6. Κάνε επικόλληση και τρέξε:

```bash
rm -rf ~/Offline-Survival-Project-main && unzip -o "/storage/emulated/0/Download/Offline-Survival-Project-main.zip" -d ~
```

### Μετά το extract

Το repository θα βρίσκεται στο:

```bash
~/Offline-Survival-Project-main
```

Για να μπεις μέσα:

```bash
cd ~/Offline-Survival-Project-main
```

Για να δεις τα αρχεία:

```bash
ls
```

### Άδεια αποθηκευτικού χώρου

Αν το Termux δεν έχει ακόμη άδεια αποθηκευτικού χώρου, τρέξε:

```bash
termux-setup-storage
```

Αυτό συνήθως χρειάζεται μόνο μία φορά.

</details>

---

## Main Script Features

<details>
<summary><strong>🇬🇧 English</strong></summary>

`Offline Survival.py` is the main interface of the project.

Current major functions include:

- language selection at startup
- smart keyword search with survival-oriented synonym expansion
- search by tag
- search by category
- search by topic
- browse all categories
- browse all topics
- easy-read terminal mode for long entries
- full-detail mode
- common-mistakes view
- related-topic suggestions
- bookmarks
- recent search history
- exports to text files
- whole-library TXT extraction
- database statistics
- integrity checks for duplicate IDs and missing fields
- update-log reading

The script is intentionally dependency-light and uses the Python standard library so it stays practical for Termux and budget devices.

</details>

<details>
<summary><strong>🇬🇷 Ελληνικά</strong></summary>

Το `Offline Survival.py` είναι το κύριο interface του project.

Οι βασικές λειτουργίες του περιλαμβάνουν:

- επιλογή γλώσσας στην εκκίνηση
- έξυπνη αναζήτηση λέξεων με επέκταση συνωνύμων γύρω από την επιβίωση
- αναζήτηση με ετικέτα
- αναζήτηση με κατηγορία
- αναζήτηση με θέμα
- περιήγηση όλων των κατηγοριών
- περιήγηση όλων των θεμάτων
- λειτουργία εύκολης ανάγνωσης για μεγάλες καταχωρήσεις
- λειτουργία πλήρους ανάλυσης
- προβολή συχνών λαθών
- προτάσεις σχετικών θεμάτων
- σελιδοδείκτες
- ιστορικό πρόσφατων αναζητήσεων
- εξαγωγές σε αρχεία κειμένου
- εξαγωγή όλης της βιβλιοθήκης σε TXT
- στατιστικά βάσης δεδομένων
- έλεγχοι ακεραιότητας για διπλά IDs και ελλιπή πεδία
- ανάγνωση αρχείων ενημερώσεων

Το script είναι σκόπιμα ελαφρύ σε dependencies και χρησιμοποιεί τη standard library της Python ώστε να παραμένει πρακτικό για Termux και για οικονομικές συσκευές.

</details>

---

## Runtime Folders and Saved Data

<details>
<summary><strong>🇬🇧 English</strong></summary>

At runtime, the script creates and uses:

```text
~/Offline Survival/
```

Inside it, the project stores data such as:

- bookmarks
- recent searches
- exported text bundles

The whole-library TXT extraction goes to:

```text
/storage/emulated/0/Download/Offline Survival TXT's
```

This keeps the library easier to access from Android file managers and easier to move to other devices.

</details>

<details>
<summary><strong>🇬🇷 Ελληνικά</strong></summary>

Κατά την εκτέλεση, το script δημιουργεί και χρησιμοποιεί:

```text
~/Offline Survival/
```

Μέσα σε αυτόν τον φάκελο το project αποθηκεύει δεδομένα όπως:

- σελιδοδείκτες
- πρόσφατες αναζητήσεις
- εξαγόμενα bundles κειμένου

Η εξαγωγή ολόκληρης της βιβλιοθήκης σε TXT πηγαίνει στο:

```text
/storage/emulated/0/Download/Offline Survival TXT's
```

Αυτό κάνει τη βιβλιοθήκη πιο εύκολη στην πρόσβαση από Android file managers και πιο εύκολη στη μεταφορά σε άλλες συσκευές.

</details>

---

## Database Design

<details>
<summary><strong>🇬🇧 English</strong></summary>

The knowledge base is split into topic-based JSON files so it can grow without turning into one oversized file.

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

This structure is designed to support bilingual parity, safer searching, easier expansion in batches, duplicate control, better reader formatting, and more useful exports.

</details>

<details>
<summary><strong>🇬🇷 Ελληνικά</strong></summary>

Η βάση γνώσης είναι χωρισμένη σε JSON αρχεία ανά θέμα ώστε να μπορεί να επεκτείνεται χωρίς να γίνεται ένα υπερβολικά μεγάλο ενιαίο αρχείο.

Τα συνηθισμένα πεδία περιλαμβάνουν:

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

Αυτή η δομή σχεδιάστηκε για να υποστηρίζει ισοτιμία δύο γλωσσών, ασφαλέστερη αναζήτηση, ευκολότερη επέκταση σε παρτίδες, έλεγχο διπλοτύπων, καλύτερη μορφοποίηση ανάγνωσης και πιο χρήσιμες εξαγωγές.

</details>

---

## Update Logs

<details>
<summary><strong>🇬🇧 English</strong></summary>

The `Offline Survival Updates/` folder exists so future work can continue cleanly.

It is intended to track:

- what was added
- what was expanded
- what was cleaned
- what still needs work
- duplicate-prevention logic
- database coverage status
- next priorities

</details>

<details>
<summary><strong>🇬🇷 Ελληνικά</strong></summary>

Ο φάκελος `Offline Survival Updates/` υπάρχει ώστε η μελλοντική εργασία να συνεχίζεται καθαρά.

Σκοπός του είναι να παρακολουθεί:

- τι προστέθηκε
- τι επεκτάθηκε
- τι καθαρίστηκε
- τι ακόμη χρειάζεται δουλειά
- λογική αποφυγής διπλοτύπων
- κατάσταση κάλυψης της βάσης
- επόμενες προτεραιότητες

</details>

---

## Knowledge Scope

<details>
<summary><strong>🇬🇧 English</strong></summary>

The repository is being expanded across practical survival areas such as:

- water collection, treatment, storage, staging, and ration discipline
- fire building, fuel preparation, coal management, and fire-site control
- shelter setup, tarp work, storm resets, and shelter-site selection
- food preservation, portioning, sick-person feeding, and emergency kitchen workflow
- first aid, bleeding control, burns, fever care, wound follow-up, infection control, and recovery-space logic
- hygiene, sanitation, handwashing stations, spread control, and waste separation
- movement, route marking, backtracking, mountain judgment, and day-plan discipline
- psychology, morale, group conflict reset, sleep/watch discipline, and decision-making under pressure
- tools, salvage, handle repair, workholding, layout, fastening, drilling, lashing, pivots, and tool preservation
- household continuity, inventory discipline, logs, planning, and long-term function

The project is not meant to become a dramatic collection of generic tips.
It is meant to become a readable, field-usable system of practical knowledge.

</details>

<details>
<summary><strong>🇬🇷 Ελληνικά</strong></summary>

Το repository επεκτείνεται σε πρακτικούς τομείς επιβίωσης όπως:

- συλλογή, επεξεργασία, αποθήκευση, στάδιο και πειθαρχία χρήσης νερού
- άναμμα φωτιάς, προετοιμασία καυσίμου, διαχείριση κάρβουνων και έλεγχο σημείου φωτιάς
- στήσιμο καταλύματος, tarp, επαναστησίματα καταιγίδας και επιλογή σημείου καταλύματος
- συντήρηση τροφής, μεριδοποίηση, τάισμα ασθενών και ροή έκτακτης κουζίνας
- πρώτες βοήθειες, έλεγχο αιμορραγίας, εγκαύματα, φροντίδα πυρετού, παρακολούθηση τραυμάτων, έλεγχο μολύνσεων και λογική χώρου ανάρρωσης
- υγιεινή, αποχέτευση, σταθμούς πλυσίματος, έλεγχο εξάπλωσης και διαχωρισμό αποβλήτων
- κίνηση, σήμανση διαδρομής, επιστροφή, ορεινή κρίση και πειθαρχία σχεδίου ημέρας
- ψυχολογία, ηθικό, επαναφορά μετά από σύγκρουση, πειθαρχία ύπνου/επιτήρησης και λήψη αποφάσεων υπό πίεση
- εργαλεία, διάσωση υλικών, επισκευή λαβών, συγκράτηση εργασίας, χάραξη, στερέωση, διάτρηση, δεσίματα, pivots και διατήρηση εργαλείων
- συνέχεια νοικοκυριού, πειθαρχία αποθέματος, καταγραφές, σχεδιασμό και μακροχρόνια λειτουργία

Ο στόχος δεν είναι να γίνει μια δραματική συλλογή γενικών συμβουλών.
Ο στόχος είναι να γίνει ένα αναγνώσιμο και χρήσιμο σύστημα πρακτικής γνώσης πεδίου.

</details>

---

## Design Rules

<details>
<summary><strong>🇬🇧 English</strong></summary>

The project is being built with these rules:

- practical over dramatic
- clear over bloated
- field-useful over decorative
- bilingual parity over mixed leftovers
- depth over duplication
- offline reliability over dependency-heavy design
- workflow knowledge over random fragments

</details>

<details>
<summary><strong>🇬🇷 Ελληνικά</strong></summary>

Το project χτίζεται με αυτούς τους κανόνες:

- πρακτικό πάνω από δραματικό
- καθαρό πάνω από φουσκωμένο
- χρήσιμο στο πεδίο πάνω από διακοσμητικό
- ισοτιμία δύο γλωσσών πάνω από μισομεταφρασμένα υπολείμματα
- βάθος πάνω από διπλοτυπία
- offline αξιοπιστία πάνω από βαριά dependencies
- γνώση ροής εργασίας πάνω από τυχαία αποσπάσματα

</details>

---

## Basic Usage

<details>
<summary><strong>🇬🇧 English</strong></summary>

From the project directory in Termux, run:

```bash
python "Offline Survival.py"
```

If your system uses `python3`, run:

```bash
python3 "Offline Survival.py"
```

Then use the menu to:

- search
- browse
- read
- bookmark
- export
- inspect update logs
- run integrity checks

</details>

<details>
<summary><strong>🇬🇷 Ελληνικά</strong></summary>

Από τον φάκελο του project στο Termux, τρέξε:

```bash
python "Offline Survival.py"
```

Αν το σύστημά σου χρησιμοποιεί `python3`, τρέξε:

```bash
python3 "Offline Survival.py"
```

Μετά χρησιμοποίησε το menu για να:

- κάνεις αναζήτηση
- περιηγηθείς
- διαβάσεις
- βάλεις σελιδοδείκτες
- κάνεις εξαγωγή
- δεις αρχεία ενημερώσεων
- τρέξεις ελέγχους ακεραιότητας

</details>

---

## Final Note

<details>
<summary><strong>🇬🇧 English</strong></summary>

Offline Survival is being built to become a durable bilingual offline reference system for crisis, collapse, survival continuity, and long-term rebuilding.

It is not finished.
It is being improved in direct repo pushes with the goal of becoming deeper, cleaner, more practical, and more usable under stress.

</details>

<details>
<summary><strong>🇬🇷 Ελληνικά</strong></summary>

Το Offline Survival χτίζεται ώστε να γίνει ένα ανθεκτικό δίγλωσσο offline σύστημα αναφοράς για κρίση, κατάρρευση, συνέχεια επιβίωσης και μακροχρόνιο ξαναχτίσιμο.

Δεν έχει ολοκληρωθεί ακόμη.
Βελτιώνεται με άμεσα pushes στο repo με στόχο να γίνεται βαθύτερο, καθαρότερο, πιο πρακτικό και πιο χρήσιμο κάτω από πραγματικό στρες.

</details>
