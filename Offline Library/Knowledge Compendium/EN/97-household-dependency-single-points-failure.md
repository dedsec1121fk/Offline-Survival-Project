# Household dependency map: find the single points of failure before an incident does

## Every critical need has a chain
A medication may depend on prescription, pharmacy, refrigeration and transport. Drinking water may depend on electricity for a pump. Communications may depend on one phone and one charger. Draw the chain for each critical need instead of writing only the final item.

## Mark components with no backup
If one caregiver, one key, one cable, one road or one power source is the only way a need is met, highlight it. Some single points can be duplicated cheaply; others require an early relocation trigger rather than equipment.

## Add time-to-failure
Estimate how long each dependency can be unavailable before the household must change strategy. A phone charger can fail immediately but be replaced easily; a refrigerated medicine may have clinically defined limits that require healthcare guidance. Use conservative, source-based timing.

## Connect chains that share the same resource
Water pumping, refrigeration and communications may all compete for one battery station. Treating them as independent plans overestimates resilience. The Power Operations ledger can expose this competition when loads are recorded honestly.

## Avoid “backup” systems with the same hidden dependency
A second internet messaging app is not communications redundancy if both require the same cellular data. A second electric heater is not heat redundancy if the same grid supplies it. Look one level deeper.

## Review after every change
A new medical device, electric vehicle, move to a high-rise or change in caregiver can create new dependencies. Update the map and drill the highest-impact failure first.

Evidence IDs: READY-PLAN-1, READY-DISABILITY-1, POWER-1.
