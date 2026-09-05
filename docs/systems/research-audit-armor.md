# HER Mod — Armor Research Audit

Status: IN PROGRESS

This file is a focused companion to `docs/systems/research-audit.md` while the armor pass is active. Consolidate durable conclusions into the main research audit after the subsystem is finished.

## Scope
- legacy `common/technologies/armor.txt`;
- NSB `common/technologies/NSB_armor.txt`;
- chassis timing/cost;
- armor/engine side branches;
- artillery/AT/AA weapon dependencies;
- MIO/focus/special-project gates;
- total slot-day cost of fielding a competitive tank.

## Findings so far

### Dual implementation
HER has separate legacy `armor.txt` and NSB `NSB_armor.txt` implementations. Armor balance must be audited against the active DLC branch; do not infer NSB behavior from the legacy file.

### NSB chassis cadence
- `gwtank_chassis`: 1918, cost 2.5.
- `basic_light_tank_chassis`: 1934, cost 2.5.
- `improved_light_tank_chassis`: 1936, cost 2.
- `advanced_light_tank_chassis`: 1941, cost 2.5.
- `basic_medium_tank_chassis`: 1936, cost 2.5.
- `improved_medium_tank_chassis`: 1940, cost 2.5.
- `advanced_medium_tank_chassis`: 1943, cost 2.5.
- `main_battle_tank_chassis`: 1945, cost 3.
- `basic_heavy_tank_chassis`: 1934, cost 2.5.
- `improved_heavy_tank_chassis`: 1941, cost 3.
- `advanced_heavy_tank_chassis`: 1944, cost 3.

### Preliminary design conclusions
- Medium armor as a chassis class is available very early (1936). This is not inherently wrong, but it means historical differentiation between early and mature medium tanks must come primarily from guns, armor, engines, modules, MIOs and country gates rather than chassis timing alone.
- Tank research cost must be evaluated as a package: chassis + armor tech + engine tech + gun branch (artillery/AT/AA/heavy artillery) + optional special projects + MIO/focus prerequisites.
- Chassis technologies unlock tank/TD/SPG/SPAA chassis together under NSB, so variant access itself is cheap compared with the legacy sub-technology model. Variant balance therefore depends heavily on module/equipment cost and weapon-tech requirements.

### Country-specific gates
- `advanced_light_tank_chassis` has a USA-only MIO gate requiring specific Army Ordnance Department traits.
- `improved_medium_tank_chassis` has special access logic: USSR can access through `SOV_superior_war_machines`; Germany can access from 1938 despite a nominal 1940 start year; USA requires specific MIO traits.
- `advanced_medium_tank_chassis` and later heavy chassis likewise use USA MIO progression gates.

**A/B / symmetry review:** this is a powerful way to represent national development paths, but the full set must be checked country-by-country so one major is structurally delayed or accelerated unintentionally. `start_year` alone no longer describes actual availability.

### Armor technology side branch
- `armor_tech_1`: 1936, cost 1; unlocks riveted/cast armor.
- `armor_tech_2`: 1939, cost 1; welded/sloped armor.
- `armor_tech_3`: 1941, cost 1; armor skirts.
- `armor_tech_4`: 1943, cost 1; effects are delivered through custom tooltip/scripted implementation and need follow-up inspection.

Cadence and cost are low compared with chassis techs; likely intended as incremental construction/material improvements.

### Alloying branch
`alloying_tech_1..4` are special-project-gated, cost 1, dated 1937/39/41/43. Their actual effects are hidden behind custom tooltip/scripted implementation and must be inspected before balance judgment.

### Engine technology side branch
- `engine_tech_1`: 1936, cost 1; unlocks diesel/gasoline engines.
- `engine_tech_2`: 1939, cost 1.
- `engine_tech_3`: 1941, cost 1; unlocks petrol-electric engine.
- `engine_tech_4`: 1943, cost 1.

Like armor techs, important effects are exposed through custom tooltips rather than obvious inline modifiers. Need to inspect localization/scripted effects/modules to know actual scaling.

### Amphibious drive
`amphibious_drive` is now a 1941 special-project tech, cost 1, requiring `sp_land_amphibious_drive`, and unlocks amphibious variants across light/medium/heavy chassis generations. This is a strong cross-generation unlock; evaluate project cost against how broadly it expands the designer.

### Integration rule
Because tank guns are unlocked in artillery/AT/AA/heavy-artillery trees, the armor audit must not conclude on chassis cost before the weapon tree is included. A nominal cost-2.5 medium chassis may require several additional slot investments before it can field the historically expected gun.
