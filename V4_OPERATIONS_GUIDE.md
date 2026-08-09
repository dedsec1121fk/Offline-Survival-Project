# Offline Survival Project — v4 Operations Guide

## Purpose

v4 is designed to help convert offline reference material into repeatable preparedness operations. It is not an automated emergency authority. Use it to keep plans, assumptions, resources, alternates, observations and practice results accessible when normal cloud services are unavailable.

## Recommended setup sequence

1. Run `python "Offline Survival.py" --check` once after copying the project to the device.
2. Run `python "Offline Survival.py" --self-test`.
3. Run `python "Offline Survival.py" --api-test` if Python can open localhost sockets on the device.
4. Launch `python "Offline Survival.py" --web`.
5. Set the household profile and planning horizon.
6. Select only the Risk Board hazards that are relevant to your plan.
7. Fill contacts, meeting points and communication alternatives.
8. Add only the inventory/resources you intend to maintain.
9. Build at least one primary and one alternate evacuation/route concept.
10. Record health-continuity metadata only when useful and only at the sensitivity level you are comfortable storing locally.
11. Assign household roles and backups.
12. Run a tabletop drill and record what failed.
13. Export a protected backup after meaningful changes.

## Resource use

The Resource Endurance board is intentionally generic. Enter a measured or chosen daily-use assumption and a minimum reserve. The displayed duration is simply the arithmetic time until that reserve is reached.

Do not interpret the value as a recommended water intake, medication allowance, generator schedule, food ration or other safety threshold unless that assumption came from an appropriate authoritative source for the situation.

## Go-bag / portable kits

Use different kits for different purposes instead of one enormous bag, for example:

- personal evacuation bag;
- vehicle kit;
- communications kit;
- document/administration pouch;
- shelter-in-place utility kit.

Mark only genuinely mission-critical items as critical so the warning state remains useful. Use actual measured item weights when weight matters.

## Accountability board

The board is a current-status view, not a permanent personnel-tracking system. Updating a person with the same name replaces the previous current row. Use the incident log if a historical timeline is needed.

## Field observation trends

Log a stable observation label and unit consistently, for example `Battery voltage` / `V`. The trend viewer groups by the exact label, uses the latest 100 numeric samples, and shows latest/min/max plus a simple line plot.

The plot does not know what value is safe. Set operational thresholds only from reliable equipment documentation, professional guidance or official instructions.

## Route-file workflow

GPX or GeoJSON can be imported directly in the browser. No upload occurs.

Before relying on a route:

- verify its source and date;
- compare it with current official closures/hazards when connectivity exists;
- keep at least one alternate;
- note constraints such as bridges, low crossings, tunnels, steep sections, fuel availability or accessibility requirements;
- avoid interpreting the schematic plot as a street/topographic map.

## Vehicle continuity

Use measured or manufacturer-appropriate consumption assumptions where possible. The range estimate is deliberately simple and can be optimistic if idling, traffic, terrain, weather, payload or mechanical condition changes.

## Library verification

Use the SHA-256 action when you want a repeatable fingerprint of an offline reference file before moving/copying it. A hash proves byte-for-byte identity to another known hash; it does not prove the content is accurate or trustworthy.

## Recovery and rollback

The Command Center keeps the immediately previous valid state before a new save. In System → Diagnostics, use **Restore previous state** when the latest edit/import was wrong.

For real resilience, also keep separate protected backups on media/devices appropriate to your threat model.

---

# Ελληνικός Οδηγός Λειτουργίας v4

## Σκοπός

Η v4 μετατρέπει τη γνώση εκτός σύνδεσης σε επαναλαμβανόμενες διαδικασίες ετοιμότητας. Δεν αποτελεί αυτόματη αρχή έκτακτης ανάγκης. Χρησιμοποίησέ την για σχέδια, παραδοχές, πόρους, εναλλακτικές, παρατηρήσεις και αποτελέσματα ασκήσεων όταν υπηρεσίες cloud δεν είναι διαθέσιμες.

## Προτεινόμενη σειρά αρχικής ρύθμισης

1. Εκτέλεσε `python "Offline Survival.py" --check` μετά την αντιγραφή του project στη συσκευή.
2. Εκτέλεσε `python "Offline Survival.py" --self-test`.
3. Εκτέλεσε `python "Offline Survival.py" --api-test` αν η συσκευή επιτρέπει localhost sockets.
4. Άνοιξε `python "Offline Survival.py" --web`.
5. Συμπλήρωσε προφίλ νοικοκυριού και ορίζοντα σχεδιασμού.
6. Επίλεξε μόνο τους σχετικούς κινδύνους στο Risk Board.
7. Συμπλήρωσε επαφές, σημεία συνάντησης και εναλλακτικές επικοινωνίας.
8. Κατέγραψε μόνο αποθέματα/πόρους που σκοπεύεις πραγματικά να συντηρείς.
9. Φτιάξε κύρια και εναλλακτική ιδέα διαδρομής/εκκένωσης.
10. Κατέγραψε ιατρικά metadata μόνο στο επίπεδο ευαισθησίας που θέλεις να αποθηκεύεται τοπικά.
11. Ανάθεσε κύριους και εφεδρικούς ρόλους.
12. Κάνε tabletop άσκηση και κατέγραψε τι απέτυχε.
13. Εξήγαγε προστατευμένο backup μετά από σημαντικές αλλαγές.

## Πόροι και κιτ

Ο υπολογισμός διάρκειας πόρου είναι απλή αριθμητική με βάση τη δική σου ημερήσια χρήση και ελάχιστη εφεδρεία. Δεν είναι ιατρική, διατροφική ή τεχνική σύσταση.

Στα κιτ χρησιμοποίησε πραγματικά βάρη όπου έχει σημασία και σημείωσε ως κρίσιμα μόνο τα αντικείμενα που πραγματικά μπλοκάρουν τη λειτουργία του κιτ.

## Check-ins και παρατηρήσεις

Το board check-in δείχνει την τρέχουσα κατάσταση. Για ιστορικό γεγονότων χρησιμοποίησε το incident log.

Το γράφημα παρατηρήσεων ομαδοποιεί με ακριβώς ίδια ονομασία, κρατά τα 100 τελευταία αριθμητικά δείγματα και δείχνει τελευταία/ελάχιστη/μέγιστη τιμή. Δεν γνωρίζει όρια ασφάλειας.

## Διαδρομές

Τα GPX/GeoJSON διαβάζονται τοπικά στον browser. Επιβεβαίωσε πηγή, ημερομηνία, επίσημους περιορισμούς, εναλλακτικές και πραγματικές συνθήκες πριν χρησιμοποιήσεις μια διαδρομή. Ο σχηματικός χάρτης δεν είναι οδικός ή τοπογραφικός χάρτης.

## Επαναφορά

Η v4 κρατά την αμέσως προηγούμενη έγκυρη κατάσταση. Η επιλογή **Restore previous state** μπορεί να αναιρέσει μια λάθος τελευταία αλλαγή/import. Για πραγματική ανθεκτικότητα, κράτησε και ξεχωριστά προστατευμένα backups.
