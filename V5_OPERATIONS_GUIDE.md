# v5 Operations Guide

## Start

```bash
python "Offline Survival.py" --web
```

Use the terminal interface by running the same script without `--web`.

## Suggested preparedness workflow

1. Fill in Household Profile and risk flags.
2. Build Inventory and record expirations.
3. Add emergency contacts and communications methods.
4. Define meeting points and evacuation routes.
5. Record critical documents without storing secret credentials.
6. Add medical-continuity information that you already know and have been instructed to keep.
7. Map Shelter Zones and identify areas marked unknown/avoid.
8. Use Water Batch Traceability so uncertain water cannot be confused with accepted batches.
9. Build the Skill Matrix and identify single-person dependencies.
10. Record important decisions with an owner and review deadline.
11. Run a scenario drill and record the debrief.
12. Export a protected backup and test restore procedures periodically.

## During disruption

Prefer the smallest reliable operational loop:

- establish current hazards;
- confirm people/accountability;
- preserve safe water, shelter, communications and power;
- record decisions and unresolved items;
- set a next review time;
- escalate to official/professional help when required.

The Command Center is a coordination tool. It must not be used to overrule evacuation orders, emergency services or competent technical/medical advice.

## Shelter zones

Use statuses as **operational labels**, not engineering certifications. A zone marked useful means only that your team currently treats it as usable for the stated purpose. If there are structural, fire, gas, electrical, chemical, flood or other serious hazards, withdraw and obtain appropriate help.

## Water batches

Record each source/container separately. Use status labels to prevent accidental mixing. The tool does not calculate a universal treatment dose or certify potability.

## Recovery board

Record what is observed, who owns the next action and whether an area/item is isolated. Avoid turning the board into permission for hazardous repairs.

## Skill matrix

Record practised capability, not aspirational expertise. Use drills to improve coverage so essential functions do not depend on one person.

## Decision board

Write the issue and actual decision separately. Add a review time whenever changing conditions could invalidate the choice. Close or supersede decisions rather than silently editing history.

## Quality/system page

The System page links to the Universal Safety Baseline. Use it for principles intentionally removed from individual database entries to avoid repeated boilerplate.

Run periodic checks:

```bash
python "Offline Survival.py" --self-test
python "Offline Survival.py" --api-test
python "Offline Survival.py" --audit
```
