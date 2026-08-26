# Failure Mode 06: Battery-reserve exhaustion

## What has changed
Stored electrical energy is being consumed faster than planned and cannot support every communication and monitoring device.

## Evidence to confirm
- Check power bank and replaceable cell against the last known normal condition; write the time of the change.
- Look for a mismatch involving charging port, cable match or low-power mode before assuming the original plan still works.
- Confirm whether radio window and device priority provide an independent fallback rather than another dependency on the same failure.

## Decisions for the next safe step
1. Mark the failed assumption explicitly and move the immediate task away from reliance on power bank or charging port.
2. Use radio window as the first alternate only after checking that battery swelling does not change its safety or availability.
3. Record the decision with runtime note and set a new review point around spare adapter so the temporary workaround is not forgotten.

## Safety boundary
For battery-reserve exhaustion, preserving the old plan is never more important than avoiding a second hazard. Treat problems involving power bank, cable match or battery swelling as reasons to stop, use an established safe alternative, and follow relevant official or professional instructions.

## Recovery checkpoint
Close this failure mode only after power bank and charging port are usable again, the workaround involving radio window has been reviewed, and the record for runtime note reflects what actually happened.

## Field cues
Use these concrete cues when searching notes, supplies, or related records: power bank, replaceable cell, charging port, cable match, low-power mode, radio window, device priority, battery swelling, runtime note, spare adapter.
