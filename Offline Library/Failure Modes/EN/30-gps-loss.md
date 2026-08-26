# Failure Mode 30: GPS or device-position loss

## What has changed
The device cannot produce a trustworthy position, so routing must stop depending on a moving map dot or automated directions.

## Evidence to confirm
- Check gps fix and coordinate note against the last known normal condition; write the time of the change.
- Look for a mismatch involving landmark, road sign or compass before assuming the original plan still works.
- Confirm whether printed map and last known position provide an independent fallback rather than another dependency on the same failure.

## Decisions for the next safe step
1. Mark the failed assumption explicitly and move the immediate task away from reliance on gps fix or landmark.
2. Use printed map as the first alternate only after checking that route bearing does not change its safety or availability.
3. Record the decision with odometer and set a new review point around meeting point so the temporary workaround is not forgotten.

## Safety boundary
For gps or device-position loss, preserving the old plan is never more important than avoiding a second hazard. Treat problems involving gps fix, road sign or route bearing as reasons to stop, use an established safe alternative, and follow relevant official or professional instructions.

## Recovery checkpoint
Close this failure mode only after gps fix and landmark are usable again, the workaround involving printed map has been reviewed, and the record for odometer reflects what actually happened.

## Field cues
Use these concrete cues when searching notes, supplies, or related records: gps fix, coordinate note, landmark, road sign, compass, printed map, last known position, route bearing, odometer, meeting point.
