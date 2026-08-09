# Validation — v7

A V7 release is acceptable only when all mandatory offline gates pass:

- curated database integrity;
- narrative anti-template/duplicate quality;
- English/Greek translation parity;
- Offline Library duplicate/template audit;
- structural self-test;
- real localhost API/security smoke suite;
- deterministic UI/state/export logic suite;
- installed-phone-browser route/static QA;
- standalone-reader QA;
- Python and JavaScript syntax checks;
- Deep Audit of active source/config/current documentation;
- ZIP integrity and clean-extraction re-test.

The phone-specific interactive check is intentionally **on-device**. `python "Offline Survival.py" --phone-browser-test` opens a local diagnostics page in the installed/default phone browser and tests that browser's actual capabilities. The build environment does not substitute another browser engine and does not claim an on-phone interactive PASS it could not execute on the user's device.

The quality rules reject detected narrative templates, exact substantive duplicates, repeated substantive sentence/paragraph groups, internal generation tags, exact duplicate Library payloads, inherited boilerplate and suspicious high-similarity document pairs. Translation checks cover database field parity, paired Library documents, Greek narrative, Greek headings, UI dictionaries and current release documentation.

The standalone reader has its own mandatory checks: exactly 220 paired subjects, bilingual nonempty bodies, no external assets, no runtime network calls, no remote resource tags, mobile viewport, local search, local favorites/review state, print support and valid embedded JavaScript.

---

# Επικύρωση — v7

Μια έκδοση V7 θεωρείται αποδεκτή μόνο όταν περνούν όλοι οι υποχρεωτικοί offline έλεγχοι:

- ακεραιότητα της επιμελημένης βάσης,
- ποιότητα αφήγησης χωρίς templates/διπλότυπα,
- ισότητα αγγλικών/ελληνικών μεταφράσεων,
- έλεγχος διπλοτύπων/templates της Offline Library,
- δομικό self-test,
- πραγματικό localhost API/security smoke suite,
- deterministic UI/state/export logic suite,
- στατικός έλεγχος της διαδρομής προς τον εγκατεστημένο browser τηλεφώνου,
- έλεγχος αυτόνομου αναγνώστη,
- έλεγχοι σύνταξης Python και JavaScript,
- Deep Audit ενεργού κώδικα/config/τρέχουσας τεκμηρίωσης,
- έλεγχος ακεραιότητας ZIP και επανάληψη δοκιμών από καθαρή εξαγωγή.

Ο διαδραστικός έλεγχος τηλεφώνου εκτελείται σκόπιμα **πάνω στη συσκευή**. Η εντολή `python "Offline Survival.py" --phone-browser-test` ανοίγει τοπική σελίδα διαγνωστικών στον εγκατεστημένο/προεπιλεγμένο browser και ελέγχει τις πραγματικές δυνατότητές του. Το περιβάλλον δημιουργίας δεν αντικαθιστά τον browser με διαφορετικό κινητήρα και δεν παρουσιάζει ψευδή διαδραστική επιτυχία τηλεφώνου που δεν εκτέλεσε στη συσκευή του χρήστη.

Οι κανόνες ποιότητας απορρίπτουν ανιχνευμένα narrative templates, ακριβή ουσιαστικά διπλότυπα, επαναλαμβανόμενες ουσιαστικές προτάσεις/παραγράφους, εσωτερικές ετικέτες δημιουργίας, ακριβή διπλότυπα αρχεία Library, παλιό boilerplate και ύποπτα πολύ παρόμοια έγγραφα. Οι μεταφραστικοί έλεγχοι καλύπτουν ισότητα πεδίων βάσης, ζευγαρωμένα έγγραφα Library, ελληνική αφήγηση, ελληνικούς τίτλους, λεξικά UI και την τρέχουσα τεκμηρίωση έκδοσης.

Ο αυτόνομος αναγνώστης έχει δικούς του υποχρεωτικούς ελέγχους: ακριβώς 220 ζευγαρωμένα θέματα, μη κενά δίγλωσσα σώματα, χωρίς εξωτερικά assets, χωρίς δικτυακά αιτήματα κατά την εκτέλεση, χωρίς απομακρυσμένα resources, mobile viewport, τοπική αναζήτηση, τοπικά αγαπημένα/κατάσταση μελέτης, εκτύπωση και έγκυρο ενσωματωμένο JavaScript.
