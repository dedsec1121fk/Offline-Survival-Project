# V7 source-verification register and maintenance method

## Why this register exists
An offline survival library can remain readable for years while the official guidance behind it changes. V7 therefore treats sources as maintenance anchors rather than decorative citations. A chapter should state which authority controls the safety-critical claim, avoid copying long passages, and be rechecked before a future release changes numeric thresholds, medical instructions, evacuation behavior, or water-treatment procedures.

## Primary public-health anchors
**CDC** — disaster health, floodwater, wildfire smoke, chronic-disease continuity, infant feeding, radiation emergencies, food safety, vector exposure, and selected first-aid/public-health boundaries. Start at https://www.cdc.gov and prefer current topic pages over archived documents when both exist.

**WHO** — emergency water/sanitation, risk communication, psychological first aid, community-health and broader international public-health principles. Start at https://www.who.int. WHO material is useful where country-neutral principles are needed, but local emergency orders still override a generic manual.

## Drinking-water and environmental anchors
**US EPA** — emergency drinking-water disinfection, private wells after flooding, water-system advisories, environmental contamination, and indoor/environmental recovery boundaries. Start at https://www.epa.gov. A water manual must distinguish biological contamination from chemical or radiological contamination; ordinary boiling/disinfection does not solve every hazard.

## General preparedness and hazard anchors
**Ready.gov / FEMA** — household planning, kits, sheltering, accessibility, communications, evacuation, power outage, winter/severe-weather and hazard-specific preparedness. Start at https://www.ready.gov.

**National Weather Service / NOAA and USGS** — weather, lightning, flood, tsunami and geologic-hazard principles where relevant. Their role is hazard recognition and official alerting, not individualized medical treatment.

## Greece-specific anchors
**Greek Ministry for Climate Crisis and Civil Protection / General Secretariat for Civil Protection** — local protective actions for wildfire, earthquake, flood, severe weather, technological hazards and 112 alerting. Start at https://civilprotection.gov.gr. Greek official instructions, evacuation orders, closure notices and emergency messages take priority over stored generic guidance for an incident in Greece.

**112 Greece / responsible local authorities** — emergency alerts and incident-specific instructions. Store the meaning of a message and the location/action it specifies; do not assume a previous event’s wording applies to a new one.

## Clinical and equipment anchors
For prescription medicines, oxygen, CPAP/BiPAP, dialysis, diabetes technology, pregnancy, infant feeding problems, epilepsy rescue medicine, mobility devices or other individualized care, the controlling source is the person’s clinician plus current pharmacy/manufacturer/equipment instructions. A public preparedness page can identify the dependency; it cannot safely create a dose, device setting, or individualized treatment plan.

## Verification workflow for future releases
1. Identify every chapter that contains a numeric threshold, treatment/disinfection step, health escalation rule, or evacuation/shelter instruction.
2. Open the current official source, not a search-result snippet or third-party summary.
3. Record the source page title and review date in the maintenance notes.
4. Compare the claim with the offline chapter; update only the affected passage.
5. Mirror the conceptual change in English and Greek rather than translating words mechanically.
6. Run translation, duplicate, sentence-repetition, Library-quality, structural, API, UI, and Deep Audit gates.
7. If an official recommendation is ambiguous or equipment-specific, narrow the offline chapter instead of guessing.

## Current-build verification date
The new safety-critical additions in this compendium were checked against current official pages available on 2026-08-09. A future release should re-verify them rather than treating that date as permanent approval.
