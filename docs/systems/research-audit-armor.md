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

**A/B / symmetry review:** this is a powerful way to represent national development paths, but the full set must be checked country-by-country so one major is not structurally delayed or accelerated unintentionally. `start_year` alone no longer describes actual availability.

### Armor technology side branch
- `armor_tech_1`: 1936, cost 1; unlocks riveted/cast armor and armor upgrade levels 21–40.
- `armor_tech_2`: 1939, cost 1; welded/sloped armor and armor upgrade levels 41–80.
- `armor_tech_3`: 1941, cost 1; armor skirts and armor upgrade levels 81–120.
- `armor_tech_4`: 1943, cost 1; armor upgrade levels 121–200.

The techs are not empty: the designer upgrade definitions use them as level gates. The unlock ranges are strongly uneven (20 / 40 / 40 / 80 new levels), so `armor_tech_4` potentially opens a disproportionately large late-war design envelope. Confirm engine interpretation of `level_requirements` before changing these thresholds.

Armor thickness itself carries real tradeoffs: more armor reduces speed and reliability, increases IC cost, and steadily increases steel demand. Heavy/default, medium and light armor gain different armor value per level (1.0 / 0.8 / 0.5 respectively), while the resource ladder adds roughly one steel per five armor-upgrade levels. After the resource rebalance this must be re-evaluated against actual national steel availability.

### Armor-construction modules
Armor thickness and armor construction are separate axes, which is a strong design pattern. Current modules include:
- riveted armor: cheap baseline with small defense/breakthrough;
- welded armor: higher defense/breakthrough, strength and armor multiplier at higher IC cost;
- cast armor: still larger defensive/armor multiplier at substantially higher IC cost;
- `tank_welded_armor_2`: special hidden module enabled by `weld_armor_2`, which is not normally researchable (`allow = { always = no }`). It gives a very favorable combination of +30% armor and -8% build cost at only a reliability penalty, so its actual national/event/focus grant must be found and audited. Do not rebalance it until the intended recipient and historical rationale are identified.

### Engine technology side branch
- `engine_tech_1`: 1936, cost 1; unlocks diesel/gasoline engines and engine upgrade levels 1–5.
- `engine_tech_2`: 1939, cost 1; unlocks engine upgrade levels 6–10.
- `engine_tech_3`: 1941, cost 1; unlocks petrol-electric engine and engine upgrade levels 11–15.
- `engine_tech_4`: 1943, cost 1; unlocks engine upgrade levels 16–20.

Each designer engine-upgrade level increases speed and breakthrough but raises IC/fuel use and lowers reliability. This is a good pattern: research expands the engineering envelope rather than automatically buffing every tank.

Engine-type modules also create meaningful tradeoffs between gasoline, diesel, petrol-electric and gas-turbine engines through IC, fuel, reliability, speed and strategic-resource requirements. The gas-turbine unlock still needs to be traced.

### Alloying branch
`alloying_tech_1..4` are special-project-gated, cost 1, dated 1937/39/41/43. The prerequisite project is `sp_land_alloying_armor`, available after `armor_tech_1`; it has large complexity, medium prototype time, breakthrough cost 2 and project resource cost of 100 steel + 100 tungsten + 100 chromium.

The project does not itself grant the whole chain; it unlocks access to `alloying_tech_1`, after which normal research proceeds through the dated chain.

Each alloying tech unlocks five more levels in two designer axes:
- tungsten alloying upgrade: levels 1–20;
- chromium alloying upgrade: levels 1–20.

Each alloying level consumes a corresponding strategic resource on the production line (level N requires N tungsten/chromium). This makes alloying a potentially very strong resource/industrial limiter after the resource rebalance.

Per-level effects:
- tungsten alloying: +2% armor, +2% max strength, +0.4% hardness, but -0.2% reliability, +0.3 flat IC and +1% multiplicative IC;
- chromium alloying: +3% armor, +1% max strength, +0.8% hardness, but -0.3% reliability, +0.2 flat IC and +1% multiplicative IC.

These are not simple duplicates of armor thickness: alloying trades scarce resources and cost/reliability for better effective protection/hardness.

### Special-project integration
Tank-related special projects are tightly integrated with ordinary research and can alter effective tech timing:
- `sp_land_amphibious_drive`: requires improved medium or advanced light chassis; short prototype, large complexity, breakthrough cost 1; unlocks the `amphibious_drive` technology and broad amphibious chassis access.
- `sp_land_alloying_armor`: requires `armor_tech_1`; medium prototype, large complexity, breakthrough cost 2, heavy strategic-resource project cost; unlocks the alloying research chain.
- `sp_land_stabilizator`: requires `improved_computing_machine`; medium prototype, medium complexity, breakthrough cost 2; unlocks stabilizer module.
- `sp_land_improved_stabilizator`: requires `advanced_computing_machine` and the first stabilizer project; medium prototype, large complexity, breakthrough cost 2; unlocks stabilizer II.

This creates a real dependency from electronics/computing into late-war tank fire-control quality and should be included when judging computing-tech value.

### Prototype reward interaction
Many tank/land special projects include generic prototype rewards that can give a one-use research bonus to category `armor`:
- low: +10%;
- medium: +20%;
- high: +35%.

Because `armor` is a broad category used by chassis and by armor/engine/alloying techs, these random rewards can accelerate a new chassis generation or a side-branch technology. Effective historical availability therefore cannot be inferred from `start_year` alone.

The same reward pool can also give permanent equipment bonuses to the broad `armor` archetype (e.g. +2% armor/hardness or +3% speed/reliability). These are small individually but are part of the cumulative late-war tank power budget.

### Early module availability
`gwtank_chassis` already unlocks many advanced design concepts, including torsion-bar, Christie, bogie and interleaved suspensions, multi-man turrets, fixed superstructures, wet ammunition storage and smoke launchers. This weakens historical differentiation because a 1930s design can use several mature-war construction concepts before later chassis/technology gates are researched.

**A/B design review:** consider moving selected advanced modules behind existing armor/engine/chassis/electronics techs or national MIO/focus progression rather than creating extra standalone research nodes. Multi-man turret availability is particularly important for representing historically different crew-layout quality between countries such as France and Germany.

### Amphibious drive
`amphibious_drive` is a 1941 special-project tech, cost 1, requiring `sp_land_amphibious_drive`, and unlocks amphibious variants across light/medium/heavy chassis generations. This is a strong cross-generation unlock; evaluate project cost against how broadly it expands the designer.

### Integration rule
Because tank guns are unlocked in artillery/AT/AA/heavy-artillery trees, the armor audit must not conclude on chassis cost before the weapon tree is included. A nominal cost-2.5 medium chassis may require several additional slot investments before it can field the historically expected gun.

## Active follow-ups
- Locate every grant/reference to `weld_armor_2` / `tank_welded_armor_2` and identify intended country/path.
- Locate the gas-turbine engine unlock.
- Audit stabilizer/autoloader/other tank special-project modules against historical dates and gun dependencies.
- Build representative 1939/1941/1943 medium-tank research packages and calculate total research cost/slot-days including gun techs.
- Recheck steel/tungsten/chromium line costs against the post-resource-rebalance economy.
