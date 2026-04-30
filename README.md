# Offline Survival / Επιβίωση Χωρίς Σύνδεση

Serious bilingual offline survival guide for Android + Termux, built to stay useful when the internet is unavailable, unstable, censored, or no longer practical.

---

<details>
<summary><strong>🇬🇧 English</strong></summary>

**Offline Survival** is a bilingual offline-first knowledge project for **Android + Termux**. It combines a large JSON survival database, a terminal app, a local browser interface, TXT export tools, and long-form update logs in one package.

The aim of the project is not just short emergency advice. It is designed to help with **immediate survival, organized daily operations, recovery, and long-term rebuilding**, while keeping both **English** and **Greek** content available side by side.

This README follows the same bilingual structure style as the example you provided: the project description, installation, usage, structure, update notes, and safety reminders are all written in both languages.

</details>

<details>
<summary><strong>🇬🇷 Ελληνικά</strong></summary>

Το **Offline Survival** είναι ένα δίγλωσσο offline-first project γνώσης για **Android + Termux**. Συνδυάζει μια μεγάλη JSON βάση survival γνώσης, εφαρμογή terminal, local browser interface, εργαλεία εξαγωγής TXT και αναλυτικά update logs σε ένα ενιαίο πακέτο.

Ο στόχος του project δεν είναι μόνο σύντομες συμβουλές έκτακτης ανάγκης. Έχει σχεδιαστεί για να βοηθά σε **άμεση επιβίωση, οργανωμένη καθημερινή λειτουργία, αποκατάσταση και μακροπρόθεσμη ανασυγκρότηση**, κρατώντας ταυτόχρονα διαθέσιμο περιεχόμενο και στα **English** και στα **Greek**.

Αυτό το README ακολουθεί το ίδιο δίγλωσσο στυλ δομής με το παράδειγμα που έδωσες: η περιγραφή του project, η εγκατάσταση, η χρήση, η δομή, οι σημειώσεις ενημερώσεων και οι υπενθυμίσεις ασφαλείας είναι όλα γραμμένα και στις δύο γλώσσες.

</details>

## 📋 Table of Contents

- [What This Project Includes](#-what-this-project-includes)
- [How To Install And Run Offline Survival](#-how-to-install-and-run-offline-survival)
- [How To Update An Existing Copy](#-how-to-update-an-existing-copy)
- [Project Structure](#-project-structure)
- [Database Coverage](#-database-coverage)
- [Important Use Notes](#-important-use-notes)
- [Safety Reminder](#️-safety-reminder)

---

## 📦 What This Project Includes

<details>
<summary><strong>🇬🇧 English</strong></summary>

This project includes:

- **Offline Survival.py** as the main application
- **Offline Survival Database/** with the bilingual knowledge base in JSON files
- **Offline Survival Updates/** with dated TXT change logs
- **Offline Survival Exports/** with audit and validation summaries
- **OFFICIAL_SAFETY_SOURCES.md** for reference material and safe context

The current build focuses on practical offline knowledge for:

- water, sanitation, hygiene, and public health
- shelter, weather, clothing, and household survival
- food storage, cooking, preservation, and agriculture
- medicine, body awareness, and cautious care guidance
- communication, navigation, logging, and records
- repair, tools, materials, low-tech power, and maintenance
- community organization, morale, education, and long-term rebuilding
- Greece-specific and Mediterranean-oriented scenarios alongside broader survival topics

</details>

<details>
<summary><strong>🇬🇷 Ελληνικά</strong></summary>

Αυτό το project περιλαμβάνει:

- το **Offline Survival.py** ως κύρια εφαρμογή
- τον φάκελο **Offline Survival Database/** με τη δίγλωσση βάση γνώσης σε JSON αρχεία
- τον φάκελο **Offline Survival Updates/** με χρονολογημένα TXT change logs
- τον φάκελο **Offline Survival Exports/** με audit και validation summaries
- το **OFFICIAL_SAFETY_SOURCES.md** για υλικό αναφοράς και ασφαλές πλαίσιο

Η τρέχουσα έκδοση εστιάζει σε πρακτική offline γνώση για:

- νερό, αποχέτευση, υγιεινή και δημόσια υγεία
- καταφύγιο, καιρό, ρουχισμό και επιβίωση στο σπίτι
- αποθήκευση τροφίμων, μαγείρεμα, συντήρηση και γεωργία
- ιατρική, γνώση σώματος και προσεκτική φροντίδα
- επικοινωνία, πλοήγηση, καταγραφή και αρχεία
- επισκευές, εργαλεία, υλικά, low-tech ενέργεια και συντήρηση
- οργάνωση κοινότητας, ηθικό, εκπαίδευση και μακροπρόθεσμη ανασυγκρότηση
- σενάρια ειδικά για Ελλάδα και Μεσόγειο μαζί με ευρύτερα survival θέματα

</details>

---

## 🚀 How To Install And Run Offline Survival

<details>
<summary><strong>🇬🇧 English</strong></summary>

### Requirements

| Component | Minimum Recommendation |
| :-------- | :--------------------- |
| **Device** | Android phone or tablet |
| **App** | Termux installed |
| **Storage** | At least **2GB** free recommended |
| **RAM** | **2GB+** recommended |
| **Internet** | Needed for initial download or project updates |

### First-Time Setup

1. Install **Termux** on your Android device.
2. Open Termux.
3. If you want storage access for exports and files in Downloads, run:

```bash
termux-setup-storage
```

4. Move into the project folder.
5. Run the main script.

If your folder is already named `Offline-Survival-Project-main`, use:

```bash
cd ~/Offline-Survival-Project-main
python "Offline Survival.py"
```

If your device uses `python3`, use:

```bash
cd ~/Offline-Survival-Project-main
python3 "Offline Survival.py"
```

### Browser UI

From the terminal menu, choose the browser option. The local interface runs at:

```text
http://127.0.0.1:8765/
```

### What The App Can Do

- browse the bilingual database offline
- search by keyword, file, category, and subcategory
- inspect entries in English and Greek
- export content to TXT files
- view update logs from inside the project
- run integrity-style checks against the loaded database

</details>

<details>
<summary><strong>🇬🇷 Ελληνικά</strong></summary>

### Απαιτήσεις

| Στοιχείο | Ελάχιστη Πρόταση |
| :-------- | :---------------- |
| **Συσκευή** | Κινητό ή tablet Android |
| **Εφαρμογή** | Εγκατεστημένο Termux |
| **Αποθηκευτικός χώρος** | Προτείνονται τουλάχιστον **2GB** ελεύθερα |
| **RAM** | Προτείνονται **2GB+** |
| **Internet** | Απαιτείται για το αρχικό κατέβασμα ή για ενημερώσεις του project |

### Πρώτη Εκτέλεση

1. Εγκατέστησε το **Termux** στη συσκευή Android.
2. Άνοιξε το Termux.
3. Αν θέλεις πρόσβαση αποθήκευσης για exports και αρχεία στα Downloads, τρέξε:

```bash
termux-setup-storage
```

4. Μπες στον φάκελο του project.
5. Τρέξε το κύριο script.

Αν ο φάκελος ονομάζεται ήδη `Offline-Survival-Project-main`, χρησιμοποίησε:

```bash
cd ~/Offline-Survival-Project-main
python "Offline Survival.py"
```

Αν η συσκευή σου χρησιμοποιεί `python3`, χρησιμοποίησε:

```bash
cd ~/Offline-Survival-Project-main
python3 "Offline Survival.py"
```

### Browser UI

Από το terminal menu, επίλεξε την browser επιλογή. Το local interface τρέχει στο:

```text
http://127.0.0.1:8765/
```

### Τι Μπορεί Να Κάνει Η Εφαρμογή

- να περιηγείται offline στη δίγλωσση βάση
- να κάνει αναζήτηση με keyword, file, category και subcategory
- να εμφανίζει εγγραφές σε English και Greek
- να εξάγει περιεχόμενο σε TXT αρχεία
- να προβάλλει update logs μέσα από το project
- να εκτελεί integrity-style ελέγχους πάνω στη φορτωμένη βάση

</details>

---

## 🔄 How To Update An Existing Copy

<details>
<summary><strong>🇬🇧 English</strong></summary>

If you already have the project and only want the newest files, replace the old folder contents with the updated files, then run the script again.

Typical launch after updating:

```bash
cd ~/Offline-Survival-Project-main
python "Offline Survival.py"
```

or:

```bash
cd ~/Offline-Survival-Project-main
python3 "Offline Survival.py"
```

</details>

<details>
<summary><strong>🇬🇷 Ελληνικά</strong></summary>

Αν έχεις ήδη το project και θέλεις μόνο τα πιο νέα αρχεία, αντικατέστησε τα περιεχόμενα του παλιού φακέλου με τα ενημερωμένα αρχεία και μετά τρέξε ξανά το script.

Τυπική εκτέλεση μετά από update:

```bash
cd ~/Offline-Survival-Project-main
python "Offline Survival.py"
```

ή:

```bash
cd ~/Offline-Survival-Project-main
python3 "Offline Survival.py"
```

</details>

---

## 🗂️ Project Structure

```text
Offline-Survival-Project-main/
├── Offline Survival.py
├── Offline Survival Database/
├── Offline Survival Updates/
├── Offline Survival Exports/
├── OFFICIAL_SAFETY_SOURCES.md
└── README.md
```

<details>
<summary><strong>🇬🇧 English</strong></summary>

The database is intentionally split across many JSON files so it stays easier to expand, audit, and repair. New entries should keep full English and Greek parity instead of adding one language later.

</details>

<details>
<summary><strong>🇬🇷 Ελληνικά</strong></summary>

Η βάση είναι σκόπιμα χωρισμένη σε πολλά JSON αρχεία ώστε να είναι πιο εύκολο να επεκταθεί, να ελεγχθεί και να διορθωθεί. Οι νέες εγγραφές πρέπει να διατηρούν πλήρη ισοτιμία English και Greek αντί να προστίθεται η μία γλώσσα αργότερα.

</details>

---

## 🧠 Database Coverage

<details>
<summary><strong>🇬🇧 English</strong></summary>

This update keeps the project centered on realistic offline use:

- emergency and non-emergency survival routines
- practical household and field organization
- cautious medical and sanitation guidance
- resilience planning for apartments, villages, rural areas, coast, and mountain settings
- tools, materials, maintenance, logging, and decision discipline
- long-term rebuilding knowledge, including low-tech production basics and training routines

</details>

<details>
<summary><strong>🇬🇷 Ελληνικά</strong></summary>

Αυτό το update κρατά το project προσανατολισμένο σε ρεαλιστική offline χρήση:

- emergency και non-emergency survival ρουτίνες
- πρακτική οργάνωση σπιτιού και πεδίου
- προσεκτική ιατρική και υγειονομική καθοδήγηση
- σχεδιασμό ανθεκτικότητας για διαμερίσματα, χωριά, αγροτικές περιοχές, ακτές και ορεινά μέρη
- εργαλεία, υλικά, συντήρηση, καταγραφή και πειθαρχία λήψης αποφάσεων
- γνώση μακροπρόθεσμης ανασυγκρότησης, μαζί με βασικά low-tech παραγωγής και ρουτίνες εκπαίδευσης

</details>

---

## 📝 Important Use Notes

<details>
<summary><strong>🇬🇧 English</strong></summary>

- Keep the project offline-capable and lightweight enough for practical Android use.
- Keep English and Greek fields together for every new entry.
- Avoid duplicate entries, duplicate IDs, and repeated filler phrasing.
- Prefer practical instructions, clear limits, fallback options, and written review steps.
- TXT exports and validation files are part of the working project, not just extras.

</details>

<details>
<summary><strong>🇬🇷 Ελληνικά</strong></summary>

- Κράτα το project ικανό για offline χρήση και αρκετά ελαφρύ για πρακτική χρήση σε Android.
- Κράτα μαζί τα English και Greek πεδία σε κάθε νέα εγγραφή.
- Απόφυγε duplicate εγγραφές, duplicate IDs και επαναλαμβανόμενο filler κείμενο.
- Προτίμησε πρακτικές οδηγίες, καθαρά όρια, fallback επιλογές και γραπτά βήματα επανελέγχου.
- Τα TXT exports και τα validation files είναι μέρος του λειτουργικού project και όχι απλώς έξτρα αρχεία.

</details>

---

## ⚠️ Safety Reminder

<details>
<summary><strong>🇬🇧 English</strong></summary>

This project is a survival knowledge base, not a replacement for emergency services or licensed professionals. In urgent situations, prioritize evacuation, emergency care, fire safety, structural safety, poison guidance, and official local instructions.

</details>

<details>
<summary><strong>🇬🇷 Ελληνικά</strong></summary>

Αυτό το project είναι βάση survival γνώσης και όχι υποκατάστατο για υπηρεσίες έκτακτης ανάγκης ή αδειοδοτημένους επαγγελματίες. Σε επείγουσες καταστάσεις, δώσε προτεραιότητα σε εκκένωση, επείγουσα φροντίδα, πυρασφάλεια, στατική ασφάλεια, οδηγίες για δηλητηριάσεις και επίσημες τοπικές οδηγίες.

</details>
