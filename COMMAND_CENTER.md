# Command Center v7

The local Command Center is the operational interface for Offline Survival Project. It contains 32 integrated sections spanning immediate emergency lookup, planning, household state, health continuity, navigation, training, resources, accountability, transport, shelter, water, food, sanitation, power, communications, dependents/accessibility, recovery, costs, decisions, Knowledge Atlas, Offline Library and diagnostics.

## Knowledge Atlas

The V7 Knowledge Atlas indexes **220 bilingual survival subjects** and searches their local text without requiring an external search service. It supports domain shortcuts, collection-scoped full-text search, review/review-later state and a risk-derived reading queue. Search requests remain on localhost.

## Phone browser workflow

`python "Offline Survival.py" --web` starts the localhost Command Center and delegates URL opening to the operating system. On Android/Termux, the launcher uses the phone's installed/default browser rather than selecting a browser engine.

`python "Offline Survival.py" --phone-browser-test` opens an on-device diagnostics page in the same way. The page tests the browser actually in use for API access, local storage, service worker, downloads, shell assets, touch and viewport behavior. Diagnostic data stays local.

## Standalone reader

`python "Offline Survival.py" --reader` opens `Offline Survival Reader.html`. The reader embeds all 220 English and 220 Greek Knowledge Compendium chapters in one file and has no runtime network dependency. It is intended as a fallback when the full Command Center is unnecessary or undesirable.

## Operational privacy

The Command Center stores operational state locally. Full backups can contain sensitive household information and should be protected like other private files. The redacted/template export contains a blank schema rather than a partially scrubbed copy of personal state.

---

# Command Center v7 — Ελληνικά

Το τοπικό Command Center είναι η επιχειρησιακή διεπαφή του Offline Survival Project. Περιλαμβάνει 32 ενσωματωμένες ενότητες για άμεση αναζήτηση έκτακτης ανάγκης, σχεδιασμό, κατάσταση νοικοκυριού, συνέχεια υγείας, πλοήγηση, εκπαίδευση, πόρους, λογοδοσία ομάδας, μεταφορές, καταφύγιο, νερό, τρόφιμα, υγιεινή, ενέργεια, επικοινωνίες, εξαρτώμενα άτομα/προσβασιμότητα, αποκατάσταση, κόστη, αποφάσεις, Άτλαντα Γνώσης, Offline Library και διαγνωστικά.

## Άτλας Γνώσης

Ο Άτλας Γνώσης V7 ευρετηριάζει **220 δίγλωσσα θέματα επιβίωσης** και αναζητεί το τοπικό τους κείμενο χωρίς εξωτερική υπηρεσία αναζήτησης. Υποστηρίζει θεματικές συντομεύσεις, αναζήτηση πλήρους κειμένου περιορισμένη ανά συλλογή, κατάσταση μελέτης/μελέτης αργότερα και προτεινόμενη σειρά μελέτης που προκύπτει από τους δηλωμένους κινδύνους. Τα αιτήματα αναζήτησης μένουν στο localhost.

## Ροή browser τηλεφώνου

Η εντολή `python "Offline Survival.py" --web` ξεκινά το τοπικό Command Center και αναθέτει στο λειτουργικό σύστημα το άνοιγμα του URL. Σε Android/Termux, ο launcher χρησιμοποιεί τον εγκατεστημένο/προεπιλεγμένο browser του τηλεφώνου χωρίς να επιλέγει κινητήρα browser.

Η εντολή `python "Offline Survival.py" --phone-browser-test` ανοίγει με τον ίδιο τρόπο μια σελίδα διαγνωστικών πάνω στη συσκευή. Η σελίδα ελέγχει τον browser που χρησιμοποιείται πραγματικά για πρόσβαση API, τοπική αποθήκευση, service worker, λήψεις, βασικά αρχεία εφαρμογής, αφή και viewport. Τα διαγνωστικά δεδομένα παραμένουν τοπικά.

## Αυτόνομος αναγνώστης

Η εντολή `python "Offline Survival.py" --reader` ανοίγει το `Offline Survival Reader.html`. Ο αναγνώστης ενσωματώνει και τα 220 αγγλικά και τα 220 ελληνικά κεφάλαια της συλλογής γνώσης σε ένα αρχείο και δεν έχει εξάρτηση από δίκτυο κατά την εκτέλεση. Προορίζεται ως εφεδρική λύση όταν δεν χρειάζεται ή δεν είναι επιθυμητό το πλήρες Command Center.

## Επιχειρησιακή ιδιωτικότητα

Το Command Center αποθηκεύει την επιχειρησιακή κατάσταση τοπικά. Τα πλήρη αντίγραφα ασφαλείας μπορεί να περιέχουν ευαίσθητες πληροφορίες νοικοκυριού και πρέπει να προστατεύονται σαν άλλα ιδιωτικά αρχεία. Η redacted/template εξαγωγή περιέχει κενό schema και όχι μερικώς καθαρισμένο αντίγραφο προσωπικών δεδομένων.
