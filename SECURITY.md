# Security notes — v7

The default server binds to `127.0.0.1`. State-changing requests require same-origin checks and localhost mode restricts Host headers. Library paths are normalized and traversal is rejected. User-added Library HTML/SVG is delivered as an attachment with restrictive content security policy rather than trusted application content. User-added Library symlinks are ignored. State collections are bounded and sanitized before persistence. The service worker caches the application shell but excludes API and Library data.

The phone-browser diagnostics page is local-only. It reads browser capability information and performs local API/storage/service-worker/download/viewport checks; it does not upload the diagnostic report. The standalone reader contains no external JavaScript/CSS/font dependency and its generated code contains no runtime `fetch`, XHR or WebSocket network path.

Residual limits: local operational state and full backups are plaintext unless the device/filesystem encrypts them; there is no built-in user authentication; the application shell retains legacy inline handlers/styles allowed by its CSP. Wildcard/LAN binding is therefore an explicit advanced trust decision rather than the default. A standalone HTML file can still be copied, modified or replaced by anyone who can alter the file on disk, so device/file integrity remains part of the trust model.

---

# Σημειώσεις ασφάλειας — v7

Ο προεπιλεγμένος server συνδέεται στο `127.0.0.1`. Τα αιτήματα που αλλάζουν κατάσταση περνούν same-origin έλεγχο και η λειτουργία localhost περιορίζει τα αποδεκτά Host headers. Οι διαδρομές της Library κανονικοποιούνται και απορρίπτεται path traversal. Αρχεία HTML/SVG που προσθέτει ο χρήστης παραδίδονται ως συνημμένα με περιοριστική πολιτική ασφάλειας περιεχομένου αντί να θεωρούνται έμπιστο μέρος της εφαρμογής. Symlinks που προσθέτει ο χρήστης αγνοούνται. Οι συλλογές κατάστασης έχουν όρια και καθαρίζονται πριν την αποθήκευση. Ο service worker αποθηκεύει το application shell αλλά εξαιρεί API και δεδομένα Library.

Η σελίδα διαγνωστικών browser τηλεφώνου είναι μόνο τοπική. Διαβάζει πληροφορίες δυνατοτήτων του browser και εκτελεί τοπικούς ελέγχους API, αποθήκευσης, service worker, λήψεων και viewport· δεν ανεβάζει την αναφορά. Ο αυτόνομος αναγνώστης δεν έχει εξωτερική εξάρτηση JavaScript/CSS/γραμματοσειρών και ο παραγόμενος κώδικάς του δεν περιέχει διαδρομή δικτύου `fetch`, XHR ή WebSocket κατά την εκτέλεση.

Υπολειπόμενα όρια: η τοπική επιχειρησιακή κατάσταση και τα πλήρη backups είναι απλό κείμενο εκτός αν κρυπτογραφούνται από τη συσκευή ή το σύστημα αρχείων, δεν υπάρχει ενσωματωμένη αυθεντικοποίηση χρηστών και το application shell διατηρεί παλιότερους inline handlers/styles που επιτρέπει η CSP. Επομένως η σύνδεση σε wildcard/LAN είναι ρητή προχωρημένη επιλογή εμπιστοσύνης και όχι προεπιλογή. Ένα αυτόνομο HTML αρχείο μπορεί να αντιγραφεί, τροποποιηθεί ή αντικατασταθεί από όποιον μπορεί να αλλάξει το αρχείο στον δίσκο, επομένως η ακεραιότητα της συσκευής/αρχείου παραμένει μέρος του μοντέλου εμπιστοσύνης.
