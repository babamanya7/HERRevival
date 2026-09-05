# HER Mod — Air Research Audit

Status: IN PROGRESS

This file is a focused companion to `docs/systems/research-audit.md` while the air research/designer pass is active. Consolidate durable conclusions into the main research audit and HER_CONTEXT once accepted.

## Scope
- BBA aircraft research tree (`common/technologies/bba_air_techs.txt`);
- legacy `air_techs.txt` only for compatibility comparison;
- airframe timing/cost;
- engine generations and engine tuning;
- radial/inline branch structure;
- designer weight/thrust/range constraints;
- weapons, survivability, electronics and role modules;
- MIO/category interactions;
- practical research-slot cost of representative 1939/1941/1943 aircraft.

## Findings so far

### Active architectural reference
The BBA aircraft system is the architectural reference for the planned Tank Designer 2.0. A single physical airframe generation can produce multiple operational identities through a required role slot and module restrictions. This is the preferred pattern for future tank chassis + role + modules design.

### Air Designer 2.0 — ACCEPTED DESIGN DIRECTION
The aircraft designer itself is now planned for a major structural rework rather than only balance tuning. Goal: turn the airframe into a real aircraft skeleton/physical layout, then mount engines, weapons, fuel, protection, avionics and mission equipment onto explicit structural locations.

Core principle:
`airframe skeleton -> physical layout -> propulsion layout -> role/equipment identity -> location-specific modules -> performance/resource tradeoffs`.

The current good weapon-layout pattern (separate cowling/capot, wing and fuselage/frame weapon locations) should be generalized to the whole aircraft.

Target structural sections should include, where engine limitations permit:
- nose/cowling section;
- left/right or abstracted wing sections;
- fuselage/frame section;
- engine / nacelle layout;
- fuel-system section;
- cockpit/crew section;
- defensive/turret positions for medium/large aircraft;
- avionics/navigation/radar section;
- structural/protection section;
- mission/special-equipment section.

The designer should model aircraft layout choices rather than only generic special slots. Candidate layout choices include:
- single-engine nose-mounted tractor layout;
- twin-engine wing nacelles;
- multi-engine nacelle layouts for medium/large aircraft;
- central/engine-mounted cannon compatibility;
- pusher / unusual propulsion layouts if engine/module syntax allows;
- jet/rocket/combined or other special propulsion arrangements where supported;
- internal vs external stores and bomb-bay/pylon tradeoffs;
- crew/turret arrangement for medium/large aircraft.

Layout choices should alter module compatibility, weight, drag/speed, agility, defence, reliability, fuel use, range, IC and strategic-resource demand. Avoid universal '+stats' modules where a physical engineering relationship can be modeled instead.

### Distinct fighter-bomber equipment identity — ACCEPTED TARGET
The current `role_small_fighter_bomber` is not sufficient because it remains an ordinary `fighter` equipment identity with an added CAS mission.

A genuine fighter-bomber should have its own duplicate equipment archetype / stockpile identity / air-wing subunit, while still being built from the same small-airframe generation and module family.

The engine air-type namespace appears fixed. Therefore the preferred implementation is to repurpose an unused recognized type channel on the relevant base airframe rather than invent a new type.

Current best candidate:
- SMALL airframe: repurpose the recognized `heavy_fighter` type channel, which is not currently used by the small-airframe family, for the fighter-bomber duplicate archetype.
- MEDIUM airframe: `fighter` and `interceptor` are currently unused recognized channels and may be available for future distinct medium fighter/strike identities.

Important distinction:
- engine-facing `type` is a technical duplicate-archetype routing channel;
- gameplay balancing should be separated through custom subunit categories, equipment/MIO categories, role modules and mission modifiers.

Thus a small fighter-bomber can technically route through `type = heavy_fighter` while using a distinct `category_fighter_bomber`, leaving the true medium heavy fighter on `category_heavy_fighter`.

This reuse must be audited for any hardcoded or script-level effects tied directly to `heavy_fighter`; visible HER doctrine bonuses mainly use subunit categories and mission modifiers, which is encouraging but not a full executable guarantee.

### Fighter-bomber as a KB / historical-series conflict resolver — ACCEPTED REQUIREMENT
The fighter-bomber identity is also required to solve current MIO/KB and historical-aircraft conflicts where multiple distinct aircraft families are forced onto the same airframe generation and the same equipment archetype.

Known recurring pattern:
- Germany: Bf 109 family and Fw 190A family can collide on the same small-airframe generation/archetype;
- USSR: fighter families such as Yak/LaGG/Lavochkin lines can collide in the same generic fighter slot; LaGG-3 is a strong candidate for migration into the fighter-bomber/strike identity where historical role and balance support it;
- similar conflicts exist in the USA and UK and must be audited country-by-country.

Air Designer 2.0 must therefore include a full historical-series/archetype mapping pass for at least GER/SOV/USA/ENG. The target is not arbitrary relabeling: each family should be assigned to the role/equipment identity that best represents its design intent and operational use, while also removing artificial competition between unrelated KB/MIO families.

Candidate examples to investigate, not blindly hard-code:
- Fw 190A -> fighter-bomber / strike-oriented small-aircraft identity, while Bf 109 remains the primary fighter family;
- LaGG-3 -> fighter-bomber / strike-oriented identity if its final module/role rules and historical usage justify that split;
- corresponding US and British fighter-vs-strike families should be identified during the MIO audit rather than left stacked on one archetype.

Implementation implication: once the fighter-bomber archetype is introduced, all MIO/KB applicability, historical variants, names, OOBs, starting production, research categories and focus bonuses must be reassigned by aircraft family rather than by broad old `fighter` membership alone.

Success criterion: distinct historical aircraft families should no longer be forced to compete for one archetype merely because the vanilla/HER role taxonomy is too coarse.

### Fighter-bomber integration checklist
Creating a distinct fighter-bomber archetype is a cross-system change, not a single equipment edit. The implementation pass must audit/update at least:
- `common/units/equipment/plane_airframes.txt` duplicate archetypes and `allowed_types`;
- aircraft role modules (`role_small_fighter_bomber` etc.);
- `common/units/air.txt` subunit definition and custom `category_fighter_bomber`;
- MIO/KB applicability and all relevant `mio_cat_*` categories;
- technology categories and research bonuses;
- national focuses / ideas / events / decisions that grant fighter, CAS or heavy-fighter bonuses;
- doctrines and air-mission modifiers;
- ace traits / air-chief traits if class-specific;
- AI designer templates / AI production weights / preferred roles;
- starting technology unlocks;
- historical OOB aircraft variants and deployed wings;
- country starting stockpiles and production lines;
- localization for role, duplicate airframe, subunit, category, designer UI and equipment names;
- icons, interface category/overview placement, sprites and map/wing icon behavior;
- conversion and `can_convert_from` relationships between fighter and fighter-bomber designs;
- lend-lease / market / stockpile filters;
- MIO auto-assign and equipment-policy filters;
- any scripted triggers/effects checking `fighter`, `heavy_fighter`, equipment archetypes, categories or air wing types;
- historical aircraft-family -> role/archetype -> KB/MIO mapping for GER/SOV/USA/ENG, with explicit conflict resolution for families that currently share one generic fighter identity.

Do not implement the new archetype before this dependency map is complete.

### Airframe cadence
Small/medium airframes follow a healthy broad cadence: interwar (1926) -> basic (1936) -> improved (1940 nominal) -> advanced (1943) -> modern/jet-era (1945). Large airframes are similar but the latest generation extends later.

Airframe research cost is generally 2, so the frame itself is not annually replaced. Most progression between generations comes from engines, weapons, survivability, range and electronics.

### Category breadth concern
Small airframe techs carry broad categories simultaneously (`light_air`, `light_fighter`, `cas_bomber`, `naval_air`, `naval_bomber`, `air_equipment` plus several MIO categories). A role-specific research bonus can therefore potentially accelerate the common airframe used by unrelated roles.

**B / integration review:** consider separating common airframe categories from role-specific fighter/CAS/naval categories so a naval-bomber bonus does not automatically become a generic fighter-frame rush bonus unless explicitly intended.

### Player availability vs nominal year
`improved_small_airframe` is nominally 1940 but its `allow` permits most countries after 1939-01-01, while SOV/USA are delayed to 1940. This makes earliest player access country-specific and earlier than `start_year` for many tags.

Audit rule: calculate earliest practical player unlock, not only nominal `start_year` or AI behavior.

### Engine generations
Inline/general engine generations currently progress approximately every two years:
- `engines_1` — 1932, cost 1;
- `engines_2` — 1934, cost 1;
- `engines_3` — 1936, cost 1.5;
- `engines_4` — 1938, cost 1.5;
- `engines_5` — 1940, cost 1.5;
- `engines_6` — 1942, cost 1.5;
- later generations continue to `engines_8` (1946).

Each generation opens 1x/2x/3x/4x engine modules with increasing thrust, maximum speed and production cost/fuel/weight.

Example 1x progression visible in the module file:
- engine I: thrust 11, speed 400, IC 10, fuel 0.12, weight 6.25;
- engine II: thrust 13, speed 420, IC 11, fuel 0.13, weight 6.5;
- engine III: thrust 15, speed 440, IC 12, fuel 0.14, weight 6.75;
- engine IV: thrust 17, speed 460, IC 13, fuel 0.15, weight 7;
- engine V: thrust 19, speed 480, IC 14, fuel 0.16, weight 7.25;
- engine VI: thrust 21, speed 500, IC 15, fuel 0.17, weight 7.5.

This is a strong physical-design pattern: later engines are not free stat buffs; they give more thrust/speed but cost more IC, fuel and weight.

### Engine tuning as a second parallel research ladder
In addition to engine generations, HER has `engine_tuning_1..7`, generally every ~2 years from 1933 through 1945, cost 1 each. Engine generation techs require both the previous engine generation and the corresponding tuning tech.

This creates a paired ladder: to stay current in piston engines, a country repeatedly researches both engine generation and tuning.

**B / research-density review:** this may be an intentional representation of engine development vs supercharging/tuning, but the combined slot-day burden must be evaluated. It can become a hidden mandatory tax for every air power, especially when combined with separate airframe, guns and survivability research.

### Designer engine tuning upgrade
`air_bba_engine_upgrade` has up to 20 designer levels, gated by `engine_tuning_*`. Per level it adds roughly:
- +0.5% maximum speed;
- +1% thrust;
- +2% fuel consumption;
- strategic tungsten cost rises progressively (roughly up to 10 tungsten at level 20).

This is a strong design principle: tuning expands the player's engineering envelope instead of automatically buffing every plane. Preserve this principle when adapting the tank designer.

### Radial vs inline engines
HER also has a separate radial engine branch. It shares the same tuning ladder but has its own `radial_engines_2..` generations. Several AI weights favor radial development for SOV/USA/JAP and later also GER depending on tier.

The branch structure is conceptually good because engine architecture can become a real national/aircraft-design choice. The actual stat differences between radial and inline modules still need full comparison.

### Range as an engineering axis
Small/medium/large aircraft have separate range upgrades, up to 20 levels, gated by `range_improvements_1..5`. These upgrades increase range but also add weight and reduce maximum speed, while progressively increasing aluminium demand.

This is another strong physical tradeoff and a useful reference for Tank Designer 2.0: capability expansion should carry mass/resource/performance costs, not only IC.

### Non-strategic materials tradeoff
Aircraft also have designer upgrades for reducing strategic-material use. At higher levels they reduce aluminium/rubber requirements, but trade this for lower air defence and increased weight while reducing build cost. This is an effective production-quality tradeoff rather than a pure bonus.

### Survivability research value
`survivability_studies` (1936, cost 1) unlocks self-sealing fuel tanks, armor plates and automatic extinguishers for small/medium/large aircraft simultaneously. This is very high value per slot-day and should be compared against narrower cost-1 weapon technologies.

### Fighter-bomber type limitation — corrected technical conclusion
Current `role_small_fighter_bomber` maps to the existing engine air type `fighter`. A separate duplicate airframe identity cannot be selected merely by inventing another duplicate archetype name if it shares the same `type`; BBA's `type_override`/duplicate-archetype selection is keyed through the recognized air `type` value.

HER's `small_plane_airframe` currently exposes `fighter`, `interceptor`, `cas`, `naval_bomber`, `suicide`, `scout_plane`, `tactical_bomber`, and `maritime_patrol_plane`. The recognized `heavy_fighter` type is not currently exposed/used by the SMALL family, while it is used normally by the MEDIUM family. This creates a plausible free routing channel for a separate small fighter-bomber duplicate.

The equipment documentation enumerates air `type` as a fixed engine-facing set rather than an open script-defined namespace. Treat a custom `type = fighter_bomber` as unsupported/hardcoded unless a minimal executable test proves otherwise.

**Current technical verdict:** a truly separate fighter-bomber equipment class on the same small-airframe designer is plausibly achievable by repurposing the unused `heavy_fighter` type channel on SMALL, provided that all direct `heavy_fighter` dependencies are audited and the engine does not impose hidden class behavior that breaks the intended role.

Do not claim that a custom air subunit alone solves identity: the key is a unique recognized type channel within the base airframe family plus a distinct duplicate archetype/subunit/category stack.

### Air weapons / mission payload pass
The weapon system is one of the stronger parts of the current designer because physical mounting location already matters. Cowling/capot and wing fighter weapons have different weight/IC values, while bombs/rockets/torpedoes are split into wing and frame/fuselage categories. Preserve this location-aware pattern and extend it to the rest of Air Designer 2.0.

Fighter guns follow a useful physical tradeoff: heavier guns increase `air_attack`, weight and IC while progressively reducing speed and range. Wing-mounted versions are generally somewhat heavier/more expensive than equivalent cowling weapons, reinforcing mounting-location identity.

**B / fighter-bomber vs CAS imbalance:** current fighter-bomber payload modules are not consistently paying the same aerodynamic penalty as equivalent CAS payloads. Examples:
- `fb_bomb_locks`: +4 ground attack, mission weight +3, IC 4; its speed/range penalties are commented out;
- `wing_bomb_locks`: +4 ground attack, mission weight +3, IC 2; active -4.5% speed / -3% range;
- `fb_heavy_bomb_locks`: +8 ground attack, mission weight +5, IC 6; its -7.5% speed / -5% range penalties are commented out;
- normal `heavy_bomb_locks`: same +8 ground attack / +5 mission weight / IC 6 but active -7.5% speed / -5% range;
- `fb_rocket_rails` / `_2`: same ground-attack and mission-weight values as CAS rocket rails, but the corresponding speed/range penalties are commented out while CAS rails retain them.

This is backwards for a compromise role: fighter-bombers should preserve more air-combat capability than dedicated CAS, but they should not get equivalent payload with effectively free aerodynamics. Air Designer 2.0 should make the distinction physical: smaller/restricted payload, pylons/external stores, less efficient ground attack per unit payload, or stronger drag/range penalties, while dedicated CAS receives heavier/denser ground-attack options and specialized attack equipment.

The current role module adds another -33% CAS `air_ground_attack` penalty to small fighter-bombers, so final balance depends on mission-stat stacking. Preserve the concept of reduced strike efficiency for fighter-bombers, but move more of the differentiation into physical payload/layout constraints rather than relying on a single blanket role penalty.

### Bombing / naval payload specialization
Normal CAS/bomber payloads have clearer mission specialization:
- AP bomb locks sacrifice ground attack for stronger naval strike/targeting;
- cluster bombs are particularly strong on logistics strike relative to ordinary CAS;
- torpedo generations increase naval strike and targeting while increasing weight/drag/cost;
- internal bomb bays scale strongly in IC, weight and drag from small -> medium -> large.

This is a good role-specialization pattern. Air Designer 2.0 should retain the idea that payload type and mounting location define mission efficiency rather than turning every weapon into generic attack.

### Electronics modules
Aircraft electronics already provide mission-specific rather than universal bonuses:
- radio navigation reduces night penalty and improves air superiority, bombing or naval targeting depending on mission;
- air-ground radar improves night performance plus bombing/detection or CAS ground attack by mission;
- air-air radar improves night performance, air attack and air-superiority contribution on interception/air-superiority missions.

This is a strong reference for the deeper designer: electronics should occupy explicit avionics/radar sections and enhance relevant missions rather than giving broad all-stat buffs.

## Active follow-ups
- Compare radial and inline engine module stats generation-by-generation.
- Audit full `engine_tuning_*` and range tech dates/costs against slot-day burden.
- Audit role modules for fighter/interceptor/fighter-bomber/CAS/tactical/naval/maritime/recon identities.
- Audit guns, bomb loads, survivability and electronics by module value and weight/thrust tradeoffs.
- Build representative 1939/1941/1943 fighter and CAS research packages and calculate total required research cost.
- Verify duplicate `allow` blocks on modern airframes and whether both gates apply or one overrides the other.
- Map every script-level dependency on `heavy_fighter` before repurposing it for SMALL fighter-bombers.
- Build a full Air Designer 2.0 slot/category dependency map before implementation.
- Audit GER/SOV/USA/ENG historical aircraft-series conflicts and produce a clean mapping of family -> role -> duplicate archetype -> subunit category -> KB/MIO applicability before rewriting designer data.
