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

<details>
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

<details>
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
  - project continuation logs, coverage tracking, duplicate-avoidance notes, and development history

---

## Termux Download, Install, Run, and Update

<details>
<summary><strong>🇬🇧 English</strong></summary>

### Option 1: Download ZIP from GitHub

Open this repository on GitHub, tap **Code**, and choose **Download ZIP**. The ZIP usually downloads into your phone's internal storage **Downloads** folder as:

```bash
Offline-Survival-Project-main.zip
```

Extract it into your Termux home with:

```bash
rm -rf ~/Offline-Survival-Project-main && unzip -o "/storage/emulated/0/Download/Offline-Survival-Project-main.zip" -d ~
```

Then run the script with:

```bash
cd ~/Offline-Survival-Project-main
python "Offline Survival.py"
```

If your device uses `python3`, run:

```bash
cd ~/Offline-Survival-Project-main
python3 "Offline Survival.py"
```

### Option 2: Clone directly with Git

If you want the repository as a real Git directory inside your Termux home, use:

```bash
pkg install git -y
cd ~
git clone https://github.com/dedsec1121fk/Offline-Survival-Project.git
cd ~/Offline-Survival-Project
python "Offline Survival.py"
```

If your device uses `python3`, use:

```bash
pkg install git -y
cd ~
git clone https://github.com/dedsec1121fk/Offline-Survival-Project.git
cd ~/Offline-Survival-Project
python3 "Offline Survival.py"
```

### Update after you already cloned it

If you already cloned the repository with Git and want the newest files later, use:

```bash
cd ~/Offline-Survival-Project
git pull
```

If you made local changes and want to pull first, a safer basic sequence is:

```bash
cd ~/Offline-Survival-Project
git stash
git pull
git stash pop
```

If Termux does not yet have storage permission, run:

```bash
termux-setup-storage
```

</details>

<details>
<summary><strong>🇬🇷 Ελληνικά</strong></summary>

### Επιλογή 1: Download ZIP από GitHub

Άνοιξε αυτό το repository στο GitHub, πάτησε **Code** και μετά **Download ZIP**. Το ZIP συνήθως κατεβαίνει στον φάκελο **Downloads** της εσωτερικής αποθήκευσης με όνομα:

```bash
Offline-Survival-Project-main.zip
```

Κάνε extract στο home του Termux με:

```bash
rm -rf ~/Offline-Survival-Project-main && unzip -o "/storage/emulated/0/Download/Offline-Survival-Project-main.zip" -d ~
```

Μετά τρέξε το script με:

```bash
cd ~/Offline-Survival-Project-main
python "Offline Survival.py"
```

Αν η συσκευή σου χρησιμοποιεί `python3`, τρέξε:

```bash
cd ~/Offline-Survival-Project-main
python3 "Offline Survival.py"
```

### Επιλογή 2: Άμεσο clone με Git

Αν θέλεις το repository ως κανονικό Git directory μέσα στο home του Termux, χρησιμοποίησε:

```bash
pkg install git -y
cd ~
git clone https://github.com/dedsec1121fk/Offline-Survival-Project.git
cd ~/Offline-Survival-Project
python "Offline Survival.py"
```

Αν η συσκευή σου χρησιμοποιεί `python3`, χρησιμοποίησε:

```bash
pkg install git -y
cd ~
git clone https://github.com/dedsec1121fk/Offline-Survival-Project.git
cd ~/Offline-Survival-Project
python3 "Offline Survival.py"
```

### Ενημέρωση αφού έχεις ήδη κάνει clone

Αν έχεις ήδη κάνει clone το repository με Git και θέλεις αργότερα τα νεότερα αρχεία, χρησιμοποίησε:

```bash
cd ~/Offline-Survival-Project
git pull
```

Αν έχεις τοπικές αλλαγές και θέλεις πρώτα να τραβήξεις τα νέα αρχεία, μια πιο ασφαλής βασική σειρά είναι:

```bash
cd ~/Offline-Survival-Project
git stash
git pull
git stash pop
```

Αν το Termux δεν έχει ακόμη άδεια αποθηκευτικού χώρου, τρέξε:

```bash
termux-setup-storage
```

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
