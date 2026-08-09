# V7 Audit Report

V7 was audited as both a software expansion and a survival-content expansion. It deliberately keeps the curated database at **871 substantive records per language** while expanding the dedicated Knowledge Compendium to **220 distinct subject chapters plus an index per language**. The subject chapters contain approximately **65,638 English words and 65,302 Greek words**.

## Knowledge and Library quality

The full Offline Library contains **732 files**, with **365 paired English and 365 paired Greek documents** across 10 bilingual collections. Release acceptance requires zero exact duplicate payload groups, zero repeated substantive paragraph groups, zero inherited boilerplate hits and zero suspicious template-similarity pairs. Database narrative gates separately require zero detected template/repeated units, zero exact substantive duplicate groups, zero repeated substantive sentence groups, zero internal generation tags and zero records below the minimum narrative threshold.

The V7 additions extend safety-specific coverage through chapter 220 rather than duplicating generic preparedness advice. The final expansion includes emergency medical-recognition boundaries, fire/fuel safety, batteries and electrical systems, solar and generators, well/rain/grey water, sanitation, food preservation and rationing, shelter boundaries, navigation/load planning, tornadoes, hurricanes, storm surge, flash floods, rip currents, avalanche terrain, dust/severe storms, stranded vehicles, boating/capsize response, rescue signaling, evacuation centers and knowledge-maintenance procedures.

## Translation

Release translation gates require exact database ID/path pairing, paired field presence and list lengths, Greek narrative coverage, paired Library coverage, Greek Library headings/text, matching UI translation dictionaries and substantial Greek coverage in all current operator documentation. The final source tree reports zero failures in those categories.

## Phone browser policy

V7 does not select or automate a browser engine for phone validation. The Android/Termux launcher delegates the localhost URL to the installed/default browser using `termux-open-url` with Android VIEW intent fallback. Static route/launcher QA is mandatory. Interactive compatibility is checked by `--phone-browser-test` **on the actual target phone**; the build environment does not invent a PASS for a device it cannot operate.

The on-device diagnostics page tests local API access, storage, service worker, download APIs, shell assets, viewport/touch behavior and relevant browser capabilities. Its report remains local unless the user explicitly exports the JSON file.

## Standalone fallback

`Offline Survival Reader.html` embeds all 220 English and 220 Greek subject chapters in one self-contained HTML file. Release QA requires no external resources, no runtime network calls, local search, local favorites/review state, print support, mobile viewport support and valid embedded JavaScript.

## Engineering gate

Final source-tree gate before packaging:

- database validator: PASS;
- strict content quality: PASS;
- translation audit: PASS;
- Library quality: PASS;
- structural self-test: **62/62 PASS**;
- live localhost API/security: **33/33 PASS**;
- deterministic UI/state/export logic: **46/46 PASS**;
- installed-phone-browser route/static QA: **11/11 PASS**;
- standalone-reader QA: **13/13 PASS**;
- Deep Audit: PASS across **31 active source/config/current-documentation files** and **6,692 lines**, with **953 parsed JSON files** and **732 Library files**;
- interactive phone browser: intentionally run on the target phone via `--phone-browser-test`, not substituted in the build environment.

Final certification must be repeated from a fresh extraction of the release ZIP. Historical audit documents remain historical records and are not rewritten to pretend their older measurements belonged to v7.

---

# Αναφορά ελέγχου V7

Η V7 ελέγχθηκε τόσο ως επέκταση λογισμικού όσο και ως επέκταση γνώσης επιβίωσης. Διατηρεί σκόπιμα την επιμελημένη βάση στις **871 ουσιαστικές εγγραφές ανά γλώσσα**, ενώ επεκτείνει τη συλλογή γνώσης σε **220 διαφορετικά θεματικά κεφάλαια και ένα ευρετήριο ανά γλώσσα**. Τα θεματικά κεφάλαια περιέχουν περίπου **65.638 αγγλικές λέξεις και 65.302 ελληνικές λέξεις**.

## Ποιότητα γνώσης και Library

Η πλήρης Offline Library περιέχει **732 αρχεία**, με **365 ζευγαρωμένα αγγλικά και 365 ζευγαρωμένα ελληνικά έγγραφα** σε 10 δίγλωσσες συλλογές. Η αποδοχή έκδοσης απαιτεί μηδενικά ακριβή διπλότυπα payloads, μηδενικές επαναλαμβανόμενες ουσιαστικές παραγράφους, μηδενικό παλιό boilerplate και μηδενικά ύποπτα template-similarity ζεύγη. Οι ξεχωριστοί έλεγχοι αφήγησης της βάσης απαιτούν μηδενικά ανιχνευμένα template/repeated units, μηδενικά ακριβή ουσιαστικά διπλότυπα, μηδενικές επαναλαμβανόμενες ουσιαστικές προτάσεις, μηδενικές εσωτερικές ετικέτες δημιουργίας και καμία εγγραφή κάτω από το ελάχιστο όριο αφήγησης.

Οι προσθήκες V7 επεκτείνουν την ειδική γνώση ασφάλειας μέχρι το κεφάλαιο 220 αντί να επαναλαμβάνουν γενικές συμβουλές ετοιμότητας. Η τελική επέκταση περιλαμβάνει όρια αναγνώρισης ιατρικών επειγόντων, ασφάλεια φωτιάς/καυσίμων, μπαταρίες και ηλεκτρικά συστήματα, ηλιακά/γεννήτριες, πηγάδια/βρόχινο/γκρίζο νερό, υγιεινή, συντήρηση και κατανομή τροφίμων, όρια καταφυγίου, πλοήγηση/φορτίο, ανεμοστρόβιλους, τυφώνες, παράκτια πλημμύρα, αιφνίδιες πλημμύρες, θαλάσσια ρεύματα, χιονοστιβάδες, αμμοθύελλες/ακραίες καταιγίδες, ακινητοποιημένα οχήματα, σκάφη/ανατροπή, σήματα διάσωσης, κέντρα εκκένωσης και διαδικασίες συντήρησης της γνώσης.

## Μετάφραση

Οι έλεγχοι μετάφρασης απαιτούν ακριβή ζευγοποίηση IDs/paths της βάσης, ίδια παρουσία πεδίων και μήκη λιστών, ελληνική αφήγηση, πλήρη ζευγοποίηση Library, ελληνικούς τίτλους/κείμενο Library, αντίστοιχα λεξικά UI και ουσιαστική ελληνική κάλυψη σε όλη την τρέχουσα επιχειρησιακή τεκμηρίωση. Το τελικό source tree αναφέρει μηδενικές αποτυχίες σε αυτές τις κατηγορίες.

## Πολιτική browser τηλεφώνου

Η V7 δεν επιλέγει ούτε αυτοματοποιεί κινητήρα browser για τον έλεγχο τηλεφώνου. Ο Android/Termux launcher αναθέτει το localhost URL στον εγκατεστημένο/προεπιλεγμένο browser μέσω `termux-open-url`, με Android VIEW intent ως εναλλακτική. Ο στατικός έλεγχος route/launcher είναι υποχρεωτικός. Η διαδραστική συμβατότητα ελέγχεται από `--phone-browser-test` **πάνω στο πραγματικό τηλέφωνο-στόχο**· το περιβάλλον δημιουργίας δεν επινοεί PASS για συσκευή που δεν μπορεί να χειριστεί.

Η σελίδα διαγνωστικών πάνω στη συσκευή ελέγχει τοπική πρόσβαση API, storage, service worker, download APIs, βασικά assets, viewport/αφή και σχετικές δυνατότητες browser. Η αναφορά παραμένει τοπική εκτός αν ο χρήστης επιλέξει ρητά εξαγωγή JSON.

## Αυτόνομη εφεδρική λειτουργία

Το `Offline Survival Reader.html` ενσωματώνει και τα 220 αγγλικά και τα 220 ελληνικά θεματικά κεφάλαια σε ένα αυτοτελές HTML αρχείο. Ο έλεγχος έκδοσης απαιτεί χωρίς εξωτερικά resources, χωρίς δικτυακά αιτήματα κατά την εκτέλεση, τοπική αναζήτηση, τοπικά αγαπημένα/κατάσταση μελέτης, εκτύπωση, mobile viewport και έγκυρο ενσωματωμένο JavaScript.

## Τεχνική πύλη

Τελικός έλεγχος source tree πριν το πακετάρισμα:

- database validator: PASS,
- strict content quality: PASS,
- translation audit: PASS,
- Library quality: PASS,
- structural self-test: **62/62 PASS**,
- πραγματικό localhost API/security: **33/33 PASS**,
- deterministic UI/state/export logic: **46/46 PASS**,
- installed-phone-browser route/static QA: **11/11 PASS**,
- standalone-reader QA: **13/13 PASS**,
- Deep Audit: PASS σε **31 ενεργά αρχεία source/config/τρέχουσας τεκμηρίωσης** και **6.692 γραμμές**, με **953 JSON αρχεία** και **732 αρχεία Library**,
- διαδραστικός browser τηλεφώνου: εκτελείται σκόπιμα στη συσκευή-στόχο μέσω `--phone-browser-test` και δεν αντικαθίσταται στο περιβάλλον δημιουργίας.

Η τελική πιστοποίηση πρέπει να επαναληφθεί από καθαρή εξαγωγή του release ZIP. Τα παλιότερα audit documents παραμένουν ιστορικά αρχεία και δεν ξαναγράφονται ώστε να φαίνεται ότι οι παλιές τους μετρήσεις ανήκαν στη v7.
