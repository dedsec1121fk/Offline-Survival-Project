# Information and Database Validation

**Validation date:** July 26, 2026  
**Ημερομηνία ελέγχου:** 26 Ιουλίου 2026

## Scope

The packaged databases contain 2,378 English records and 2,378 Greek records. Every record was processed by the built-in validator. The validator confirms database structure, bilingual parity, source provenance, update-date validity, and field consistency.

This is stronger than the previous validator, which checked mainly JSON structure and mirroring.

## Results

The final packaged project reports:

```text
English: 2,378 records, 703 JSON files, 260 category folders
Ελληνικά: 2,378 records, 703 JSON files, 260 category folders
```

All of the following report `0` errors in both languages:

- Invalid JSON files
- Missing required fields
- Empty required values
- Field-type errors
- Duplicate record IDs
- Duplicate titles
- Invalid or future update dates
- Record-language mismatches
- Records without sources
- Invalid source URLs
- Sources outside the approved official-domain list

The following bilingual checks also pass:

- Matching relative JSON paths
- Matching record-ID sets
- Matching IDs inside every corresponding English and Greek file

Run the same checks locally with:

```bash
python "Offline Survival.py" --check
```

## Source validation

All source values are plain HTTPS URLs. The English database currently uses 141 unique source URLs and the Greek database uses 143 across the same 23 approved official domains, including:

- `civilprotection.gov.gr`
- `moh.gov.gr`
- `cdc.gov`
- `who.int`
- `ready.gov`
- `redcross.org`
- `fao.org`
- `cisa.gov`
- `epa.gov`
- `osha.gov`
- `usgs.gov`
- `nal.usda.gov`
- `nrcs.usda.gov`
- `ars.usda.gov`
- `minagric.gr`
- `nchfp.uga.edu`

The validator rejects malformed URLs, non-HTTPS sources, missing domains, and domains not present in the explicit official-source allowlist.

## Manually cross-checked critical facts

Ten new mirrored emergency-essential records were manually reviewed against current official pages. The following critical facts were confirmed:

### Greece 112

- 112 is the single European emergency number.
- It can be called free of charge in Greece and the EU when immediate assistance is required.
- Greek Civil Protection warns against unnecessary calls.

Sources:

- https://civilprotection.gov.gr/en/112
- https://civilprotection.gov.gr/en/112/pote-pos-kalo
- https://civilprotection.gov.gr/112

### Greek Poison Centre

- The Ministry of Health lists the Poison Centre at **210 7793777**.
- It operates 24 hours a day, 7 days a week.
- Information is provided free of charge.

Source:

- https://www.moh.gov.gr/articles/citizen/xrhsima-thlefwna-amp-dieythynseis/203-210-7793777-kentro-dhlhthriasewn

### Emergency water

- For microbial contamination, clear water should be brought to a full rolling boil for 1 minute.
- Above approximately 2,000 metres, CDC guidance uses 3 minutes.
- Boiling does not remove chemical contamination.

Sources:

- https://www.cdc.gov/water-emergency/about/index.html
- https://www.cdc.gov/water-emergency/about/drinking-water-advisories-an-overview.html

### Food during a power outage

When appliance doors remain closed:

- Refrigerator: up to 4 hours
- Full freezer: up to 48 hours
- Half-full freezer: up to 24 hours

Sources:

- https://www.cdc.gov/food-safety/foods/keep-food-safe-after-emergency.html
- https://www.cdc.gov/natural-disasters/response/what-to-do-protect-yourself-during-a-power-outage.html

### Generator and carbon monoxide

- Generators must never be operated inside a home or garage, even with doors or windows open.
- CDC guidance places generators outdoors more than 20 feet, approximately 6 metres, from windows, doors, and vents.

Source:

- https://www.cdc.gov/carbon-monoxide/about/index.html

### Heat stroke

- Confusion, altered mental status or speech, loss of consciousness, seizures, and very high body temperature are emergency warning signs.
- Emergency services should be called and rapid cooling started while help is coming.

Sources:

- https://www.cdc.gov/niosh/heat-stress/about/illnesses.html
- https://civilprotection.gov.gr/en/odigies-prostasias/kaysonas

### Floods

Greek Civil Protection advises:

- Move away from underground areas to a secure higher point.
- Do not cross torrents on foot or by car.
- Stop and change direction at a flooded street.
- Avoid water that may conduct electricity.

Source:

- https://civilprotection.gov.gr/en/odigies-prostasias/plimmyres

### Wildfires

Greek Civil Protection advises:

- Report a fire immediately and provide clear location information.
- Keep emergency access available.
- Strictly follow organised-relocation instructions and official routes.

Source:

- https://civilprotection.gov.gr/en/odigies-prostasias/dasikes-pyrkagies

## Food-growing and preservation expansion

This release adds **60 English and 60 Greek guides** under the mirrored `Verified - Food Growing and Preservation` folder. Every new guide was reviewed for complete bilingual content, five actionable steps, explicit warnings, official HTTPS sources, and conservative failure handling.

The collection covers seven validation groups:

```text
Planning and season management:                    7
Soil, compost, mulch, salinity and raised beds:    7
Containers, water, heat, rain and drought:         9
Seeds, propagation, seed saving and storage:       7
Crop-specific growing and pollination:             11
Integrated pest and disease management:            6
Harvesting and safe food preservation:             13
Total per language:                                60
```

Representative source-backed checks performed on July 26, 2026 include:

- USDA/NAL describes planning, site selection, soil preparation, planting, maintenance, harvesting, containers, and raised beds as core home-gardening areas.
- USDA/ARS and NRCS support soil organic matter, compost, cover, reduced disturbance, soil testing, root-zone irrigation, and dry foliage as practical soil and plant-health controls.
- EPA guidance supports watering according to plant and soil needs, preventing pooling and runoff, and using microirrigation to apply water near roots.
- FAO material supports home-garden planning, crop rotation, quality seed systems, seed storage, integrated pest management, and proactive drought preparation.
- WHO guidance treats wastewater, greywater, and excreta reuse as a risk-management system requiring health targets, monitoring, and local controls—not an improvised household shortcut.
- CDC states that collected rainwater may contain germs and chemicals and recommends public-system tap or bottled water, when possible, for watering plants intended for eating.
- CDC identifies raw or undercooked sprouts as a riskier choice and thoroughly cooked sprouts as the safer option.
- NCHFP guidance requires tested proportions and methods for freezing, blanching, drying, pickling, fermenting, boiling-water canning, and pressure canning.
- CDC states that pressure canning is the only recommended home-canning method for low-acid foods and warns never to taste suspect home-canned food to determine safety.

The new guides intentionally avoid universal planting dates, homemade pesticide recipes, casual wastewater reuse, untested fermentation proportions, and improvised canning times or pressures.

## Safety correction applied across the database

A repeated cleaning-chemical sentence was strengthened in 180 records across both languages. The updated wording now says not to mix different cleaning products or add bleach to another cleaner, and to use one product at a time according to its label. The CDC chemical-emergency source was added to every modified record, and their `last_updated` value was changed to `2026-07-26`.

## Validation limits

The automated validator can prove structural correctness, parity, provenance rules, and internally testable constraints. It cannot prove that every sentence in 4,756 language-specific records will remain correct forever or apply safely to every real-world situation.

Official instructions, emergency alerts, product labels, local law, and qualified professional guidance always take priority. Source pages can change after this validation date; the database should therefore be reviewed periodically and before major releases.

---

# Ελληνική σύνοψη

Η τελική έκδοση ελέγχει αυτόματα και τις **4.756 εγγραφές** για δομή JSON, υποχρεωτικά πεδία, τύπους δεδομένων, μοναδικά IDs, σωστή γλώσσα, ημερομηνίες, πηγές HTTPS από επίσημους τομείς και πλήρη αντιστοιχία Αγγλικών–Ελληνικών.

Επιπλέον, 10 βασικές κάρτες έκτακτης ανάγκης διασταυρώθηκαν χειροκίνητα με επίσημες πηγές στις 26 Ιουλίου 2026. Προστέθηκαν επίσης 60 πλήρεις οδηγοί καλλιέργειας και ασφαλούς διατήρησης ανά γλώσσα και διορθώθηκε η καθοδήγηση για ανάμειξη καθαριστικών σε 180 εγγραφές.

Ο έλεγχος δεν αντικαθιστά ζωντανές επίσημες οδηγίες ή επαγγελματική αξιολόγηση. Σε πραγματική έκτακτη ανάγκη ακολούθησε τις αρχές και κάλεσε 112.
