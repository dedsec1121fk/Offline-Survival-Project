# Failure Mode 32: Offline backup data corrupted

## What has changed
A local backup expected to contain plans, records or reference material cannot be opened, validates incorrectly or is missing recent information.

## Evidence to confirm
- Check backup archive and checksum against the last known normal condition; write the time of the change.
- Look for a mismatch involving second copy, usb drive or export file before assuming the original plan still works.
- Confirm whether password note and restore test provide an independent fallback rather than another dependency on the same failure.

## Decisions for the next safe step
1. Mark the failed assumption explicitly and move the immediate task away from reliance on backup archive or second copy.
2. Use password note as the first alternate only after checking that file date does not change its safety or availability.
3. Record the decision with read-only copy and set a new review point around device storage so the temporary workaround is not forgotten.

## Safety boundary
For offline backup data corrupted, preserving the old plan is never more important than avoiding a second hazard. Treat problems involving backup archive, usb drive or file date as reasons to stop, use an established safe alternative, and follow relevant official or professional instructions.

## Recovery checkpoint
Close this failure mode only after backup archive and second copy are usable again, the workaround involving password note has been reviewed, and the record for read-only copy reflects what actually happened.

## Field cues
Use these concrete cues when searching notes, supplies, or related records: backup archive, checksum, second copy, usb drive, export file, password note, restore test, file date, read-only copy, device storage.
