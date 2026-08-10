# Security Notes

## Local Trust Boundary

- The default server binds to `127.0.0.1`.
- State-changing requests require same-origin checks.
- Localhost mode restricts accepted Host headers.
- Wildcard/LAN binding is an explicit advanced trust decision.

## Offline Library

- Library paths are normalized and traversal attempts are rejected.
- User-added symlinks are ignored.
- User-added HTML/SVG is delivered as an attachment with restrictive content security policy rather than trusted application content.
- Large binary Library items are not treated as ordinary text-search content.

## State And Backups

- State collections are bounded and sanitized before persistence.
- Full backups can contain sensitive household data.
- Local state/backups are plaintext unless protected by device or filesystem encryption.
- The project does not include built-in user authentication.

## Browser And Offline Shell

- The service worker caches only the application shell and excludes API/Library data.
- Phone-browser diagnostics remain local and do not upload reports.
- The standalone reader has no external JavaScript, CSS, font, fetch, XHR, or WebSocket dependency at runtime.

## Residual Limitations

- The application shell retains legacy inline handlers/styles permitted by its CSP.
- Anyone who can modify local project files can also alter the standalone reader or source code.
- Device and filesystem integrity remain part of the trust model.

---

# Σημειώσεις Ασφάλειας

## Τοπικό Όριο Εμπιστοσύνης

- Ο προεπιλεγμένος server συνδέεται στο `127.0.0.1`.
- Τα αιτήματα που αλλάζουν κατάσταση περνούν same-origin έλεγχο.
- Η λειτουργία localhost περιορίζει τα αποδεκτά Host headers.
- Η σύνδεση σε wildcard/LAN είναι ρητή προχωρημένη επιλογή εμπιστοσύνης.

## Offline Library

- Οι διαδρομές κανονικοποιούνται και απορρίπτεται path traversal.
- Symlinks που προσθέτει ο χρήστης αγνοούνται.
- HTML/SVG που προσθέτει ο χρήστης παραδίδονται ως συνημμένα με περιοριστική CSP και όχι σαν έμπιστο περιεχόμενο εφαρμογής.
- Μεγάλα δυαδικά αρχεία δεν αντιμετωπίζονται ως συνηθισμένο περιεχόμενο αναζήτησης κειμένου.

## Κατάσταση Και Backups

- Οι συλλογές κατάστασης έχουν όρια και καθαρίζονται πριν την αποθήκευση.
- Τα πλήρη backups μπορεί να περιέχουν ευαίσθητα δεδομένα νοικοκυριού.
- Η τοπική κατάσταση και τα backups είναι plaintext εκτός αν προστατεύονται από κρυπτογράφηση συσκευής ή filesystem.
- Δεν υπάρχει ενσωματωμένη αυθεντικοποίηση χρηστών.

## Browser Και Offline Shell

- Ο service worker αποθηκεύει μόνο το application shell και εξαιρεί API/Library δεδομένα.
- Τα διαγνωστικά browser παραμένουν τοπικά και δεν ανεβάζουν αναφορές.
- Ο αυτόνομος αναγνώστης δεν χρειάζεται εξωτερικό JavaScript, CSS, γραμματοσειρά, fetch, XHR ή WebSocket κατά την εκτέλεση.

## Υπολειπόμενοι Περιορισμοί

- Το application shell διατηρεί legacy inline handlers/styles που επιτρέπει η CSP.
- Όποιος μπορεί να τροποποιήσει τα τοπικά αρχεία μπορεί να αλλάξει και τον standalone reader ή τον source code.
- Η ακεραιότητα συσκευής και filesystem παραμένει μέρος του μοντέλου εμπιστοσύνης.
