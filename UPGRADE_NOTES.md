# Upgrade notes — v7

V7 keeps backward state compatibility while using active state schema 7. The Knowledge Atlas stores only local reading progress in `knowledge_progress`; it does not modify the manuals themselves.

## Knowledge expansion

The V7 Knowledge Compendium has grown to **220 distinct subjects plus an index in each language**, approximately **65,638 English words and 65,302 Greek words** across the subject chapters. The final 60 additions concentrate on emergency medical-recognition boundaries, fire and fuel safety, battery/solar/electrical operations, water and sanitation decisions, food preservation and rationing, shelter and navigation, tornado/hurricane/coastal and flash-flood hazards, rip currents, avalanche terrain, dust/severe storms, stranded vehicles, boating, signaling, evacuation centers and knowledge-maintenance practice.

The complete Offline Library now contains **732 files**, including **365 paired documents per language**. Expansion is accepted only if the duplicate/template/translation gates still pass.

## Curated database

The database remains at **871 substantive records per language**. V7 retains the stricter sentence-level narrative detector introduced during curation rather than restoring removed boilerplate to increase the headline count.

## Installed/default phone browser

Browser opening has been redesigned around the phone's installed/default browser. The Python launcher does not import the generic Python browser-opening module and does not choose a browser engine. On Android/Termux it uses `termux-open-url`, then the Android VIEW intent as a fallback when available.

A new `--phone-browser-test` mode serves a local bilingual diagnostic page that runs in the browser on the target phone. It tests the environment actually being used rather than treating a separate desktop rendering engine as proof of phone compatibility.

## Standalone reader

V7 adds `Offline Survival Reader.html`, generated from the 220-subject bilingual compendium. The single file embeds both languages, local search, filters, favorites/review state and print support with no external assets or runtime network request. Use `--reader` to open it through the installed/default browser.

---

# Σημειώσεις αναβάθμισης — v7

Η V7 διατηρεί συμβατότητα με παλιότερα δεδομένα κατάστασης και χρησιμοποιεί ενεργό schema 7. Ο Άτλας Γνώσης αποθηκεύει μόνο τοπική πρόοδο μελέτης στο `knowledge_progress` και δεν τροποποιεί τα ίδια τα εγχειρίδια.

## Επέκταση γνώσης

Η συλλογή γνώσης V7 έχει αυξηθεί σε **220 διαφορετικά θέματα και ένα ευρετήριο ανά γλώσσα**, με περίπου **65.638 αγγλικές λέξεις και 65.302 ελληνικές λέξεις** στα θεματικά κεφάλαια. Οι τελευταίες 60 προσθήκες εστιάζουν σε όρια αναγνώρισης ιατρικών επειγόντων, ασφάλεια φωτιάς και καυσίμων, μπαταρίες/ηλιακή ενέργεια/ηλεκτρικά συστήματα, αποφάσεις νερού και υγιεινής, συντήρηση και κατανομή τροφίμων, καταφύγιο και πλοήγηση, ανεμοστρόβιλους, τυφώνες, παράκτιους και αιφνίδιους πλημμυρικούς κινδύνους, θαλάσσια ρεύματα, χιονοστιβάδες, αμμοθύελλες και ακραίες καταιγίδες, ακινητοποιημένα οχήματα, σκάφη, σήματα διάσωσης, κέντρα εκκένωσης και συντήρηση της ίδιας της offline γνώσης.

Η πλήρης Offline Library περιέχει πλέον **732 αρχεία**, μεταξύ των οποίων **365 ζευγαρωμένα έγγραφα ανά γλώσσα**. Η επέκταση γίνεται αποδεκτή μόνο όταν εξακολουθούν να περνούν οι έλεγχοι διπλοτύπων, templates και μεταφράσεων.

## Επιμελημένη βάση

Η βάση παραμένει στις **871 ουσιαστικές εγγραφές ανά γλώσσα**. Η V7 διατηρεί τον αυστηρότερο ανιχνευτή επαναλαμβανόμενης αφήγησης αντί να επαναφέρει αφαιρεμένο boilerplate μόνο για μεγαλύτερο αριθμό εγγραφών.

## Εγκατεστημένος/προεπιλεγμένος browser τηλεφώνου

Το άνοιγμα browser έχει επανασχεδιαστεί γύρω από τον εγκατεστημένο/προεπιλεγμένο browser του τηλεφώνου. Ο Python launcher δεν χρησιμοποιεί το γενικό module ανοίγματος browser και δεν επιλέγει κινητήρα. Σε Android/Termux χρησιμοποιεί `termux-open-url` και στη συνέχεια, όταν είναι διαθέσιμο, το Android VIEW intent ως εναλλακτική.

Η νέα λειτουργία `--phone-browser-test` σερβίρει τοπική δίγλωσση σελίδα διαγνωστικών που εκτελείται στον browser της συσκευής-στόχου. Έτσι ελέγχεται το πραγματικό περιβάλλον χρήσης αντί να θεωρείται ένας ξεχωριστός desktop renderer απόδειξη συμβατότητας τηλεφώνου.

## Αυτόνομος αναγνώστης

Η V7 προσθέτει το `Offline Survival Reader.html`, το οποίο παράγεται από τη δίγλωσση συλλογή 220 θεμάτων. Το μοναδικό αρχείο ενσωματώνει και τις δύο γλώσσες, τοπική αναζήτηση, φίλτρα, αγαπημένα/κατάσταση μελέτης και εκτύπωση χωρίς εξωτερικά assets ή δικτυακά αιτήματα κατά την εκτέλεση. Χρησιμοποίησε `--reader` για άνοιγμα μέσω του εγκατεστημένου/προεπιλεγμένου browser.
