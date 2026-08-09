# Offline Survival Project — Ultimate Operations Edition v7

Offline Survival Project is a bilingual, offline-first survival knowledge and household-operations environment for English and Greek users. V7 combines a curated survival database, a 32-section local Command Center, operational ledgers and calculators, a searchable Offline Library, a 220-subject Knowledge Compendium, and a completely standalone single-file reader.

The core uses only the Python standard library, binds to `127.0.0.1` by default, needs no account or cloud service, and is designed to remain useful when ordinary internet access is unavailable.

## Survival knowledge depth

The V7 Knowledge Compendium contains **220 distinct subjects plus one index in each language**. The subject chapters contain approximately **65,638 English words and 65,302 Greek words**, excluding the indexes. Coverage includes immediate emergency priorities, water, sanitation, food, first-aid boundaries and medical continuity, fire and smoke, heat and cold, earthquake/tsunami/flood/wildfire, severe and coastal weather, evacuation, navigation, shelter, electrical and battery safety, solar and generator operations, transport, communications, children and accessibility, animals, recovery, contamination, boating, avalanche/rip-current hazards, search-and-rescue signaling, and long-duration household continuity.

Safety-sensitive chapters use dated authoritative source anchors. The manuals paraphrase and organize that material for offline use rather than copying source text.

The curated database remains deliberately smaller than older releases: **871 substantive records per language**. Records that failed the stricter anti-template/narrative-quality rules were removed instead of being retained to inflate the count.

## Offline Library

The Library currently contains **732 files**, including **365 paired English documents and 365 paired Greek documents** across 10 bilingual collections. Its release gate rejects exact duplicate payloads, repeated substantive paragraphs, inherited boilerplate and suspicious template-similarity pairs.

The Command Center can search readable Library material locally. Large binary/Kiwix material is discoverable without being scanned as ordinary text.

## Standalone Survival Reader

`Offline Survival Reader.html` is a self-contained fallback containing all **220 English + 220 Greek Knowledge Compendium chapters**. It has:

- full local text search;
- subject/domain filters;
- English/Greek switching;
- favorites and reviewed-state tracking using browser-local storage;
- mobile navigation;
- print support;
- no CDN, remote font, external JavaScript or external stylesheet;
- no runtime `fetch`, XHR or WebSocket network dependency.

Open it through the launcher with:

```bash
python "Offline Survival.py" --reader
```

It can also be opened directly as an HTML file when the phone browser permits local-file access.

## Installed/default phone browser

The web launcher does **not** select a particular browser engine. On Android/Termux it asks Android to open the local URL in the phone's installed/default browser. The launcher prefers `termux-open-url` and falls back to the Android VIEW intent when available.

Run the full Command Center:

```bash
python "Offline Survival.py" --web
```

Run diagnostics inside the phone browser you actually use:

```bash
python "Offline Survival.py" --phone-browser-test
```

The diagnostics page checks localhost API access, local storage, service-worker support, shell assets, download APIs, touch/viewport behavior and relevant browser capabilities. The report stays local and can be exported as JSON; it is not uploaded.

Convenience scripts are also included:

- `start-phone-browser.sh`
- `phone-browser-diagnostics.sh`
- `open-standalone-reader.sh`
- `Phone Browser Diagnostics.bat`
- `Open Standalone Reader.bat`

## Command Center

V7 retains the 32-section operational interface: emergency search, essentials, food and supplies, inventory, communications, planning, health, navigation, training, resources, accountability, transport, shelter, water operations, recovery, skills, decisions, shift handover, sanitation, power, dependents/accessibility, recovery costs, Knowledge Atlas, Offline Library and diagnostics among the integrated workflows.

The Knowledge Atlas adds collection-scoped local search, risk-derived reading suggestions and local review progress. Operational state remains on the local device unless the user explicitly exports it.

## Quality and audit commands

```bash
python "Offline Survival.py" --check
python "Offline Survival.py" --quality
python "Offline Survival.py" --translations
python "Offline Survival.py" --library-quality
python "Offline Survival.py" --self-test
python "Offline Survival.py" --api-test
python "Offline Survival.py" --ui-test
python "Offline Survival.py" --audit
```

V7 additionally ships permanent static QA for the installed-phone-browser route and the standalone reader. Interactive browser diagnostics are intentionally executed on the target phone rather than simulated by selecting a desktop browser engine in the release environment.

## Safety boundary

This project is an offline preparedness and reference system, not a replacement for emergency services, official warnings, professional rescue, medical diagnosis or individualized treatment. Where live official instructions are available, they take precedence over cached reference material. The guide deliberately gives escalation boundaries for hazards that should not be handled at household level.

## Why V7 differs from Project NOMAD

The supplied Project NOMAD codebase is a broad offline-server platform with a larger service stack. Offline Survival Project intentionally takes a different path: it stays lightweight and survival-specific, uses a standard-library local server rather than requiring a containerized server stack, includes a deep bilingual survival compendium and operational state tools, and can fall back to one standalone HTML reader. The goal is not to duplicate every general-purpose NOMAD service; it is to be the more useful package when the primary problem is **surviving and operating without internet**.

---

# Offline Survival Project — Ultimate Operations Edition v7 (Ελληνικά)

Το Offline Survival Project είναι ένα δίγλωσσο, offline-first περιβάλλον γνώσης επιβίωσης και επιχειρησιακής οργάνωσης νοικοκυριού για αγγλικά και ελληνικά. Η V7 συνδυάζει επιμελημένη βάση επιβίωσης, τοπικό Command Center 32 ενοτήτων, επιχειρησιακά μητρώα και υπολογιστές, αναζητήσιμη Offline Library, συλλογή γνώσης 220 θεμάτων και έναν πλήρως αυτόνομο αναγνώστη ενός αρχείου.

Ο βασικός πυρήνας χρησιμοποιεί μόνο την τυπική βιβλιοθήκη της Python, συνδέεται από προεπιλογή στο `127.0.0.1`, δεν χρειάζεται λογαριασμό ή υπηρεσία cloud και έχει σχεδιαστεί ώστε να παραμένει χρήσιμος όταν δεν υπάρχει κανονική πρόσβαση στο διαδίκτυο.

## Βάθος γνώσης επιβίωσης

Η συλλογή γνώσης V7 περιέχει **220 διαφορετικά θέματα και ένα ευρετήριο σε κάθε γλώσσα**. Τα θεματικά κεφάλαια περιέχουν περίπου **65.638 αγγλικές λέξεις και 65.302 ελληνικές λέξεις**, χωρίς τα ευρετήρια. Η κάλυψη περιλαμβάνει άμεσες προτεραιότητες έκτακτης ανάγκης, νερό, υγιεινή, τρόφιμα, όρια πρώτων βοηθειών και ιατρική συνέχεια, φωτιά και καπνό, ζέστη και κρύο, σεισμό, τσουνάμι, πλημμύρα, δασική πυρκαγιά, ακραία και παράκτια καιρικά φαινόμενα, εκκένωση, πλοήγηση, καταφύγιο, ηλεκτρική ασφάλεια και μπαταρίες, ηλιακή ενέργεια και γεννήτριες, μεταφορές, επικοινωνίες, παιδιά και προσβασιμότητα, ζώα, αποκατάσταση, μόλυνση, ασφάλεια σε σκάφη, χιονοστιβάδες, ρεύματα θάλασσας, σήματα διάσωσης και μακροχρόνια συνέχεια νοικοκυριού.

Τα κεφάλαια υψηλής κρισιμότητας χρησιμοποιούν χρονολογημένες αναφορές σε έγκυρες επίσημες πηγές. Τα εγχειρίδια οργανώνουν και παραφράζουν το υλικό για χρήση χωρίς σύνδεση αντί να αντιγράφουν το αρχικό κείμενο.

Η επιμελημένη βάση παραμένει σκόπιμα μικρότερη από παλαιότερες εκδόσεις: **871 ουσιαστικές εγγραφές ανά γλώσσα**. Εγγραφές που δεν πέρασαν τους αυστηρότερους ελέγχους κατά των templates και της επαναλαμβανόμενης αφήγησης αφαιρέθηκαν αντί να διατηρηθούν μόνο για μεγαλύτερο αριθμό.

## Offline Library

Η Library περιέχει σήμερα **732 αρχεία**, μεταξύ των οποίων **365 ζευγαρωμένα αγγλικά και 365 ζευγαρωμένα ελληνικά έγγραφα** σε 10 δίγλωσσες συλλογές. Ο έλεγχος έκδοσης απορρίπτει ακριβή διπλότυπα payloads, επαναλαμβανόμενες ουσιαστικές παραγράφους, παλιό boilerplate και ύποπτα πολύ παρόμοια templates.

Το Command Center μπορεί να αναζητεί τοπικά το αναγνώσιμο περιεχόμενο της Library. Μεγάλα δυαδικά/Kiwix αρχεία εντοπίζονται χωρίς να σαρώνονται σαν απλό κείμενο.

## Αυτόνομος αναγνώστης επιβίωσης

Το `Offline Survival Reader.html` είναι ένα αυτοτελές εφεδρικό αρχείο που περιλαμβάνει και τα **220 αγγλικά + 220 ελληνικά κεφάλαια** της συλλογής γνώσης. Προσφέρει:

- πλήρη τοπική αναζήτηση κειμένου,
- φίλτρα θεμάτων και περιοχών γνώσης,
- εναλλαγή αγγλικών/ελληνικών,
- αγαπημένα και κατάσταση μελέτης σε τοπική αποθήκευση του browser,
- πλοήγηση για κινητό,
- εκτύπωση,
- χωρίς CDN, απομακρυσμένες γραμματοσειρές, εξωτερικό JavaScript ή εξωτερικό stylesheet,
- χωρίς εξάρτηση από `fetch`, XHR ή WebSocket κατά την εκτέλεση.

Άνοιξέ τον με:

```bash
python "Offline Survival.py" --reader
```

Μπορεί επίσης να ανοιχτεί απευθείας σαν αρχείο HTML όταν ο browser του τηλεφώνου επιτρέπει τοπικά αρχεία.

## Εγκατεστημένος/προεπιλεγμένος browser τηλεφώνου

Ο web launcher **δεν επιλέγει συγκεκριμένο κινητήρα browser**. Σε Android/Termux ζητά από το Android να ανοίξει το τοπικό URL στον εγκατεστημένο/προεπιλεγμένο browser του τηλεφώνου. Προτιμά το `termux-open-url` και, όταν είναι διαθέσιμο, χρησιμοποιεί ως εναλλακτική το Android VIEW intent.

Εκτέλεση πλήρους Command Center:

```bash
python "Offline Survival.py" --web
```

Διαγνωστικά μέσα στον browser που χρησιμοποιείς πραγματικά στο τηλέφωνο:

```bash
python "Offline Survival.py" --phone-browser-test
```

Η σελίδα διαγνωστικών ελέγχει πρόσβαση στο localhost API, τοπική αποθήκευση, service worker, βασικά αρχεία εφαρμογής, δυνατότητες λήψης, αφή/viewport και σχετικές δυνατότητες του browser. Η αναφορά παραμένει τοπική και μπορεί να εξαχθεί ως JSON· δεν αποστέλλεται πουθενά.

Περιλαμβάνονται επίσης scripts ευκολίας:

- `start-phone-browser.sh`
- `phone-browser-diagnostics.sh`
- `open-standalone-reader.sh`
- `Phone Browser Diagnostics.bat`
- `Open Standalone Reader.bat`

## Command Center

Η V7 διατηρεί την επιχειρησιακή διεπαφή 32 ενοτήτων: αναζήτηση έκτακτης ανάγκης, βασικές ανάγκες, τρόφιμα και αποθέματα, inventory, επικοινωνίες, σχεδιασμό, υγεία, πλοήγηση, εκπαίδευση, πόρους, λογοδοσία ομάδας, μεταφορές, καταφύγιο, λειτουργίες νερού, αποκατάσταση, δεξιότητες, αποφάσεις, παράδοση βάρδιας, υγιεινή, ενέργεια, εξαρτώμενα άτομα/προσβασιμότητα, κόστη αποκατάστασης, Άτλαντα Γνώσης, Offline Library και διαγνωστικά, μαζί με τις υπόλοιπες ενσωματωμένες ροές.

Ο Άτλας Γνώσης προσθέτει τοπική αναζήτηση περιορισμένη ανά συλλογή, προτάσεις μελέτης που προκύπτουν από τους δηλωμένους κινδύνους και τοπική κατάσταση μελέτης. Η επιχειρησιακή κατάσταση παραμένει στη συσκευή εκτός αν ο χρήστης επιλέξει ρητά εξαγωγή.

## Εντολές ποιότητας και ελέγχου

```bash
python "Offline Survival.py" --check
python "Offline Survival.py" --quality
python "Offline Survival.py" --translations
python "Offline Survival.py" --library-quality
python "Offline Survival.py" --self-test
python "Offline Survival.py" --api-test
python "Offline Survival.py" --ui-test
python "Offline Survival.py" --audit
```

Η V7 περιλαμβάνει επιπλέον μόνιμο στατικό έλεγχο για τη διαδρομή προς τον εγκατεστημένο browser τηλεφώνου και για τον αυτόνομο αναγνώστη. Τα διαδραστικά διαγνωστικά browser εκτελούνται σκόπιμα στο πραγματικό τηλέφωνο και δεν προσομοιώνονται με επιλογή κινητήρα desktop browser στο περιβάλλον δημιουργίας.

## Όριο ασφάλειας

Το έργο είναι σύστημα ετοιμότητας και αναφοράς χωρίς σύνδεση και δεν αντικαθιστά υπηρεσίες έκτακτης ανάγκης, επίσημες προειδοποιήσεις, επαγγελματική διάσωση, ιατρική διάγνωση ή εξατομικευμένη θεραπεία. Όταν υπάρχουν ζωντανές επίσημες οδηγίες, έχουν προτεραιότητα έναντι αποθηκευμένου υλικού. Ο οδηγός δίνει σκόπιμα όρια κλιμάκωσης για κινδύνους που δεν πρέπει να αντιμετωπίζονται σε επίπεδο νοικοκυριού.

## Γιατί η V7 διαφέρει από το Project NOMAD

Το παρεχόμενο Project NOMAD είναι μια ευρύτερη πλατφόρμα τοπικού server με μεγαλύτερο σύνολο υπηρεσιών. Το Offline Survival Project ακολουθεί σκόπιμα διαφορετική κατεύθυνση: παραμένει ελαφρύ και ειδικά σχεδιασμένο για επιβίωση, χρησιμοποιεί τοπικό server βασισμένο στην τυπική βιβλιοθήκη αντί να απαιτεί containerized server stack, περιλαμβάνει βαθιά δίγλωσση συλλογή επιβίωσης και επιχειρησιακά εργαλεία και μπορεί να υποχωρήσει σε έναν μόνο αυτόνομο HTML αναγνώστη. Στόχος δεν είναι να αντιγράψει κάθε γενικής χρήσης υπηρεσία του NOMAD· στόχος είναι να είναι πιο χρήσιμο όταν το βασικό πρόβλημα είναι **η επιβίωση και η οργάνωση χωρίς διαδίκτυο**.
