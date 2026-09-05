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
- `tank_welded_armor_2`: special Soviet module enabled through the Paton automatic-welding project chain. It is intentionally national rather than a general research option. Do not rebalance it in isolation from the project cost and the Soviet mass-production model.

### Engine technology side branch
- `engine_tech_1`: 1936, cost 1; unlocks diesel/gasoline engines and engine upgrade levels 1–5.
- `engine_tech_2`: 1939, cost 1; unlocks engine upgrade levels 6–10.
- `engine_tech_3`: 1941, cost 1; unlocks petrol-electric engine and engine upgrade levels 11–15.
- `engine_tech_4`: 1943, cost 1; unlocks engine upgrade levels 16–20.

Each designer engine-upgrade level increases speed and breakthrough but raises IC/fuel use and lowers reliability. This is a good pattern: research expands the engineering envelope rather than automatically buffing every tank.

Engine-type modules also create meaningful tradeoffs between gasoline, diesel, petrol-electric and gas-turbine engines through IC, fuel, reliability, speed and strategic-resource requirements. The gas-turbine unlock still needs to be traced; if no grant exists it is an orphan module.

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
- Soviet `sp_fluid_autowelding`: national follow-up project gated by armor/alloying progression; completion grants `weld_armor_2` through `sov_armor.800`.

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

### Fire-control / command modules
Current late-war tank modules are substantial combat multipliers rather than decorative add-ons:
- radio I/II/III progressively gives very large defense/breakthrough and smaller SA/HA bonuses;
- stabilizer I/II gives broad combat-stat multipliers at IC/resource/reliability cost;
- autoloader gives large SA/HA and moderate defense/breakthrough at IC/tungsten/reliability cost.

This means late-war tank quality in HER is driven more by systems integration than by chassis generation alone. Preserve that principle, but re-audit the exact stacking and separate vehicle-level effects from crew/doctrine/formation-level command effects where possible.

### Amphibious drive
`amphibious_drive` is a 1941 special-project tech, cost 1, requiring `sp_land_amphibious_drive`, and unlocks amphibious variants across light/medium/heavy chassis generations. This is a strong cross-generation unlock; evaluate project cost against how broadly it expands the designer.

### Integration rule
Because tank guns are unlocked in artillery/AT/AA/heavy-artillery trees, the armor audit must not conclude on chassis cost before the weapon tree is included. A nominal cost-2.5 medium chassis may require several additional slot investments before it can field the historically expected gun.

## Tank Designer 2.0 — accepted design direction
The current tank designer should be treated as a candidate for a major rebuild, at least to the architectural quality of HER's aircraft designer rather than as a minor numerical rebalance.

Target principles:
- chassis is a weight/volume/engineering envelope, not merely a generation stat package;
- turret is a real subsystem: crew count, ring size, gun capacity, cost, situational awareness and combat efficiency;
- main gun is a physical constraint with recoil/size/resource/weight implications;
- armor separates thickness, construction method, slope and alloy quality;
- engine/transmission/suspension create distinct mobility/reliability/maintenance tradeoffs;
- crew layout and ergonomics should be separated from electronics;
- radio should model command/control rather than act as a universal substitute for doctrine/crew quality;
- optics, stabilizers and loading systems should have narrower, legible functions;
- stacking the best module in every slot must create an expensive/heavy/unreliable design rather than a universally optimal tank;
- national tank-building schools should emerge from design choices + MIO/special projects, not only from flat national stat bonuses.

Avoid adding research nodes merely to gate every module. Prefer existing armor/engine/electronics/chassis techs, MIO progression and special projects as unlock gates.

## Tank role layer — ACCEPTED
Specialized armored vehicles must be designable **on the basis of each ordinary light/medium/heavy chassis**, not implemented primarily as separate bespoke chassis/archetypes.

Target architecture:
`chassis -> required vehicle role -> role-specific module restrictions/effects -> battalion/formation usage`.

The desired role layer should be analogous in concept to the aircraft designer's required `role_type_slot`, while respecting whatever land-equipment syntax the engine actually supports. If a direct tank `type_override`/role-slot mechanism is not supported, emulate the user-facing result through duplicated chassis archetypes or another safe mechanism, but keep the design experience centered on one physical chassis family rather than separate researchable hulls.

Candidate roles on every suitable chassis generation:
- line tank;
- tank destroyer;
- self-propelled artillery;
- self-propelled AA;
- flame tank;
- command tank;
- assault gun / assault tank / infantry-support vehicle;
- armored engineer vehicle;
- recovery/maintenance vehicle;
- reconnaissance/scout role where useful;
- amphibious role where compatible.

Role is not merely a label. It must shape the allowed design:
- command role: requires radio/command equipment, may reduce ammunition/weapon capacity, raises IC/electronics use, and should primarily improve formation command/control rather than raw vehicle firepower;
- engineer role: requires dozer/demolition/recovery/bridging-style equipment and should trade weapon capacity for engineering value;
- assault/infantry-support role: favors howitzers/close-support weapons, protection and urban/fortification assault at the cost of anti-tank versatility/mobility;
- SPG role: represents indirect mobile artillery and should remain distinct from an assault gun used for direct infantry support;
- TD/AA/flame roles continue to be specialized derivatives of the same base chassis.

This role layer is a core part of Tank Designer 2.0 and should be designed together with battalion equipment requirements, not as a cosmetic extension.

## New armored-vehicle roles — feasibility direction
HER should investigate additional role-specific armored equipment beyond the standard tank/TD/SPG/SPAA/flame set. The engine already supports custom equipment archetypes: HER itself defines `armored_support_vehicle` as an `is_archetype = yes` custom armor equipment. This makes new land equipment identities technically plausible even if the engine's `type =` enum remains limited.

A particularly promising model for command tanks is to make them a small secondary equipment requirement inside tank battalions/companies (if unit equipment syntax supports the desired ratio) rather than a full battalion. This would model Panzerbefehlswagen / command Shermans / Soviet command vehicles as a formation-level capability and avoid template clutter.

## Aircraft role expansion — feasibility direction
HER's aircraft designer already has a dedicated required `role_type_slot`, and `00_plane_role_modules.txt` defines role modules through `add_equipment_type`, mission permissions and mission-specific stat modifiers. Current `role_small_fighter_bomber` is still classified as engine type `fighter` while gaining air-superiority + CAS mission access. Therefore the user's criticism is correct: it is operationally a fighter with a ground-attack mission rather than a truly separate stockpile/class identity.

The equipment documentation enumerates a fixed set of air `type` values (`fighter`, `cas`, `interceptor`, `tactical_bomber`, `strategic_bomber`, `naval_bomber`, etc.). Treat arbitrary new engine-level air types such as `fighter_bomber` as unconfirmed/likely unsupported until tested. However, separate aircraft archetypes and designer roles can still be created while mapping them to an existing supported engine type and restricting missions/modules accordingly.

Design target for the air audit:
- fighter;
- interceptor;
- fighter-bomber as a genuinely distinct design/production identity if technically possible;
- dedicated CAS / assault aircraft;
- tactical bomber;
- strategic bomber;
- torpedo bomber;
- maritime patrol aircraft;
- reconnaissance aircraft;
- potentially night fighter / heavy fighter roles if their operational behavior can be represented cleanly.

If a truly new engine air type cannot be created, test whether a separate archetype with an existing underlying type is sufficient to keep production, stockpile, MIO/category and wing identity distinct. Do not settle for the current 'fighter + CAS button' model without testing this route.

## Active follow-ups
- Locate the gas-turbine engine unlock.
- Audit stabilizer/autoloader/other tank special-project modules against historical dates and gun dependencies.
- During the unit/equipment audit, verify whether one battalion can require a controlled mix of normal tanks + command/support vehicles and whether designer variants can satisfy separate archetypes cleanly.
- During the air audit, prototype the distinction between engine-level air type, equipment archetype, required role module, allowed mission set and wing/stockpile identity.
- Determine whether custom air `type` tokens are accepted by the current engine; treat as experimental until a minimal test mod is proven.
- Recheck steel/tungsten/chromium line costs against the post-resource-rebalance economy.
