# HER AI Strategy Rework

Status: IN PROGRESS
Branch: `AI-rework`
Started: 2026-09-06

## Scope

This document tracks Block 6 of the AI rework: `common/ai_strategy`.

The folder is the main behavioral glue layer between country plans, production, front allocation, operations, naval goals and engine AI. It must be audited for overlapping generic strategies, obsolete role IDs, lifecycle bugs and country-specific phase logic before broad NAI tuning.

## Architectural rules

1. `common/ai_strategy/naval_production.txt` is the authoritative ship-production role layer for HER/VNR naval roles.
2. Country files may add dynamic wartime/operational overrides, but must use current `vnr_naval_*` production roles rather than obsolete vanilla `naval_*` role IDs when they intend to affect HER ship construction.
3. Generic strategies must explicitly exclude the eight major-country AI profiles where those countries have dedicated logic: GER/SOV/ENG/USA/JAP/ITA/FRA/CHI.
4. Temporary strategies must have deliberate lifecycle behavior (`abort_when_not_enabled` or an explicit `abort`).
5. Country operation logic should prefer phase/condition triggers over permanent huge weights.
6. AI defines should stay in the main `common/defines/00_defines.lua`; do not create standalone HER AI define override files unless a future technical requirement makes it unavoidable.

## Generic strategy layer — CLEANED

`common/ai_strategy/default.txt` was rebuilt so generic production/template personalities are a fallback rather than an accidental second personality for the eight majors.

Old problems included:

- USA inheriting `default_unit_production` on top of USA-specific logic;
- FRA/CHI inheriting the old generic naval `default_role_ratios`;
- USA/JAP/ITA/FRA/SOV/CHI inheriting generic BBA air production;
- ITA inheriting generic garrison production;
- CHI inheriting generic early/mid-late division-template priorities;
- generic mountaineer/mobile/armor helpers stacking on country role ratios;
- broad major naval nudges stacking with the already country-specific `naval_production.txt`.

Implemented cleanup:

- `default_unit_production`, generic BBA air production, paratrooper/patrol-bomber/garrison/mountaineer/mobile/armor helpers now exclude GER/SOV/ENG/USA/JAP/ITA/FRA/CHI;
- CZE exceptions that existed for specialized armored behavior are retained where relevant;
- obsolete `default_role_ratios` was removed because it used vanilla `naval_*` production roles while HER uses VNR roles;
- the old `slightly_naval_focused_nation` and `more_naval_focused_nation` major nudges were removed; major ship production is already defined country-by-country in `naval_production.txt`;
- treaty logic retains the generic capital-ship `unit_ratio` reduction but drops dead vanilla BB/BC role-ratio modifiers;
- generic early/mid-late division-template priorities now explicitly exclude CHI along with the other seven majors;
- unrelated global utility behavior (PP spending, agencies, foreign garrison manpower, economy-fatigue civ stop, etc.) was retained.

Commit: `cde47aa9f87bb20c3ae7d5e9d0e9ee19a11d9ce4`.

## Findings: naval strategy integration

`naval_production.txt` already has substantial country-specific VNR production plans:

- GER strongly pivots into submarines against ENG;
- ENG has large wartime screen/light-cruiser targets;
- USA has very large wartime screen/carrier targets;
- JAP has carrier/screen-heavy wartime production;
- ITA/FRA/SOV have their own phase profiles.

However older country files still contain vanilla `naval_*` role-ratio blocks. Because `naval_production.txt` activates `no_old_navy_production` and applies `-10000` to those old roles with Man the Guns, such blocks are obsolete/dead as HER ship-production controls.

Confirmed technical debt:

- ENG: old `EAI_ENG_focus_on_screens`, `ENG_naval_role_ratios_historical` and `ENG_naval_role_ratios_anti_submarines` were removed in the British rewrite. The working VNR bridge remains responsible for the dynamic ASW production response.
- JAP: `JAP_naval_role_ratios_historical` and `_late` still use old naval production roles and will be handled in the Japanese pass.

## Implemented bridge strategies

`common/ai_strategy/HER_naval_rework_strategies.txt` was added during the naval pass.

It provides:

- pre-war British VNR escort/screen buildup;
- dynamic British ASW emergency production using the existing `anti_submarine_strategy_required_trigger`;
- an always-on lighter ENG-vs-GER screen bias;
- USA/JAP Pacific-war carrier/screen/invasion-focus boosts.

This file is intentionally a bridge while the large legacy country files are audited. Once all country strategy cleanup is complete, duplicated behavior can be moved into final country files or left here only where cross-country separation is useful.

## JAP Southern Expansion bug — FIXED

`Japan_southern_expansion_1_fire` previously required both `date > 1942.12.15` and `date < 1942.1.1`, making the first scripted Southern Expansion invasion impossible.

It now uses:

```txt
date > 1941.12.15
date < 1942.1.1
```

This creates a late-December 1941 Philippines operation window and matches the following staged windows for Malaya in February 1942 and the East Indies in March 1942.

Commit: `2f90529d1eaca3b7641a56360dbe242fc77b30d0`.

## China strategy — IMPLEMENTED FIRST PASS

`common/ai_strategy/CHI.txt` was rebuilt around the actual HER target for Nationalist China instead of retaining the inherited generic/WA-style production mix.

Main changes:

- infantry remains the dominant division role;
- armor is strongly suppressed;
- mountaineers are allowed at a small level because Chinese terrain can justify them;
- air investment is reduced to a small fighter arm, with CAS/tactical/strategic/naval bomber ratios at zero;
- the old capital-ship/submarine/screen aspirations were removed from the Chinese production personality; only a modest convoy requirement remains;
- equipment production now explicitly favors infantry, artillery, AA and some AT while suppressing armor/motorized investment;
- the existing `ignore_army_incompetence` helper is retained;
- Japan preparation now raises `north_china`, `central_china` and `south_china` priorities and forces army growth;
- during war with Japan, China requests more forces on that front and increases military-industry pressure;
- pre-war military construction remains meaningful but no longer uses the old extreme `1000/1500` industrial weights;
- coastal buffer was reduced from 12% to 8%, while the central reserve was increased from 10% to 12% to improve defense in depth.

Commits: `99b3f1789b340a255bb2683942d9ef046413ec83`, follow-up trigger correction `64882449bb3d0ce1720b64b84682a305eeae1ed7`.

## Soviet strategy — IMPLEMENTED FIRST PASS

`common/ai_strategy/SOV.txt` was rebuilt around explicit economic and Eastern Front phases instead of a large set of overlapping 1000-2000 scale area priorities and permanent military-industry weights.

### Economic phases

- 1936-37: strong civilian construction bias and suppressed military/air expansion;
- 1938-39: gradual military ramp while the USSR still remains an industrializing peacetime power;
- from 1940 while at peace: accelerated military construction and air buildup;
- major war: full wartime industrial pressure and faster army expansion.

The old `SOV_third_fyp` permanent `added_military_to_civilian_factory_ratio = 1000` / `arms_factory = 1500` behavior was removed.

The first rewrite accidentally made the 1940 mobilization block require both war with GER and peace; this impossible trigger was caught immediately and corrected in follow-up commit `42cc292067a72cb15e860d95f309471f63cc8e9f`.

### Production personality

The Soviet baseline now strongly favors infantry, artillery, armor, AA/AT, fighters/interceptors and CAS, while strategic/naval bombers and blue-water naval construction are suppressed. Medium armor and mechanized/motorized templates gain more importance after 1940.

### Eastern Front phases

- pre-Barbarossa: move forces west and deliberately pull demand away from the Far East;
- opening Barbarossa through mid-November 1941: careful front execution, no manual attacks and no plan execution, with the center receiving the highest weight;
- winter 1941/42: balanced counteroffensive;
- spring-autumn 1942: defensive posture again, with increased priority for the southern front/Caucasus;
- winter 1942/43: second balanced counteroffensive centered on the south/center;
- 1943 to June 1944: sustained balanced general offensive;
- Bagration window: temporary rush behavior and maximum central-front concentration;
- late 1944 onward: final offensive into the Reich and secondary Balkan pressure.

The rework uses the new operational aliases `soviet_north`, `soviet_center`, `soviet_south`, `caucasus`, `crimea` and `soviet_far_east` rather than stacking huge weights on every old regional alias.

### Reserves / Far East

The many separate city-buffer strategies were consolidated into smaller north/center and south reserve groups. Moscow/Leningrad and southern operational centers retain reserve forces without consuming a huge fraction of the entire Red Army. Far-East demand is intentionally reduced when Germany becomes the main threat, then rises again for the late-war anti-Japanese phase.

Main rewrite commit: `dd209ec98904365275281f29eb61b1903d9f4b94`.
Trigger correction: `42cc292067a72cb15e860d95f309471f63cc8e9f`.

## German strategy — IMPLEMENTED FIRST PASS

`common/ai_strategy/GER.txt` was rebuilt from the inherited compensation-heavy stack into a phase-driven German war plan.

### Production personality

The old baseline used negative armor/motorized/mechanized role ratios and then tried to add armor back through several separate helper blocks. The new baseline directly expresses the intended force structure:

- infantry remains the majority of the army;
- armor is a substantial but limited elite component;
- motorized/mechanized support is positive rather than being suppressed and then re-added elsewhere;
- artillery, AA/AT, tanks, fighters/interceptors and CAS receive meaningful production pressure;
- strategic bombing is suppressed;
- naval unit ratios strongly favor submarines, while carriers are suppressed.

Dynamic enemy-armor detection is retained and now adds AT pressure rather than being the only meaningful anti-armor signal.

### Rearmament phases

- 1936-37: moderate rearmament rather than an immediate all-military economy;
- 1938 to the Polish campaign: strong arms-factory and air buildup with increased mobile/armored force demand;
- major war: full military expansion.

The old permanent `GER_no_wants_civ = -10000` behavior was removed from the German country file so the AI is not absolutely forbidden from civilian construction in all fascist phases.

### Poland / France

The Polish campaign now has an explicit preparation block followed by a concentrated rush phase. Armor is pulled away from France while Poland remains active. The Low Countries and French phases are separate:

- avoid armor concentration through the Maginot;
- prepare HOL/BEL/LUX after Poland;
- rush Benelux with dedicated front requests;
- then concentrate armor and breakthrough targets into northern France/Paris while continuing to avoid the Maginot rear.

### Barbarossa / Eastern Front

The old German file had useful individual pieces but also overlapping permanent `front_armor_score`, SOV preparation and rush strategies. These were consolidated into explicit phases:

- from late 1940 after France: Barbarossa preparation, logistics buildup and suppression of African distractions;
- opening campaign through mid-November 1941: maximum concentration and `rush` execution;
- winter 1941/42: operational pause with careful/no-execute behavior;
- spring-autumn 1942: renewed balanced offensive with strong southern/Caucasus emphasis;
- late 1942 onward: sustained but less reckless Eastern war;
- Allied landing / meaningful surrender progress: pull force demand and armor back toward France and switch the Soviet front to careful defense.

This is intended to stop the AI from endlessly running the 1941 blitz posture after the operational situation has changed.

### Air and Atlantic war

The Luftwaffe now has explicit prewar and wartime fighter/CAS production profiles, including the HER interceptor role. A Battle of Britain phase prioritizes Southern England while continuing to downweight the English Channel air region.

The working North Sea / Atlantic U-boat region priorities are retained and simplified. Atlantic raiding can begin with a somewhat smaller submarine force once western French bases are available.

### Technical cleanup

The old `GER_naval_role_ratios_historical` block using dead vanilla `naval_*` production roles was removed. VNR ship production remains owned by `naval_production.txt`.

Several duplicated/dead strategies were removed, including permanently disabled war/claim helpers and duplicate Italy alliance logic. Useful shared Axis/minor de-crowding helpers from the old GER file were retained.

Main rewrite commit: `8498b28475d585a1657770c2c864f529047c1c90`.

## British strategy — IMPLEMENTED FIRST PASS

`common/ai_strategy/ENG.txt` was rebuilt around three simultaneous British constraints: Home Defence/RAF, Battle of the Atlantic, and a limited expeditionary army that must protect imperial nodes without being annihilated in continental traps.

### Production personality

The old file had several overlapping air-production stacks plus a very large `marines = 30` land ratio and multiple dead vanilla naval-role helpers. The new baseline:

- keeps infantry as the majority of the army;
- keeps armor meaningful but smaller than the old 15/70 split implied;
- reduces marines to a specialist role rather than treating them as a third of the desired army mix;
- adds modest motorized/mechanized demand;
- strongly favors fighters/interceptors, with meaningful naval bombers and maritime patrol aircraft;
- retains strategic bombers as a secondary capability rather than a dominant early-war program;
- gives convoy/screens high unit-ratio pressure while specific VNR ship construction remains owned by `naval_production.txt` and the naval bridge.

### Industry / RAF phases

- 1936-37: civilian buildup and only limited air expansion;
- 1938 to war: accelerated rearmament with a strong fighter/interceptor program;
- major war: full wartime industry and army expansion;
- Home Defence: Southern England and the British home air region gain explicit strategic air importance;
- fighter emergency: if the deployed fighter force falls below the desired wartime threshold, fighter/interceptor production receives an additional temporary boost;
- maritime patrol/naval bomber production has its own naval-air block instead of being mixed into every aircraft strategy.

### Atlantic / naval integration

The obsolete `EAI_ENG_focus_on_screens`, `ENG_naval_role_ratios_historical` and `ENG_naval_role_ratios_anti_submarines` blocks using old `naval_*` role IDs were removed.

The British file now only contains high-level naval behavior and dockyard balance. Actual VNR screen/escort construction remains in `naval_production.txt` plus the existing ASW bridge, which reacts to `anti_submarine_strategy_required_trigger`.

The Channel avoidance value was reduced from an overly strong blanket avoidance to a moderate penalty; the Baltic remains heavily discouraged. Britain can therefore defend nearby routes without treating the entire Channel as effectively unusable.

### France / home reserve

The old file contained several overlapping "don't die in France" strategies. They were consolidated into:

- a permanent modest home-island reserve;
- Benelux reluctance while Germany is breaking through;
- a stronger withdrawal trigger when French surrender progress rises;
- a post-capitulation France demand penalty through mid-1942.

This is intended to preserve the BEF enough for later Mediterranean and invasion operations without making Britain completely refuse continental support.

### Mediterranean / Empire

Suez, Alexandria, Gibraltar and Malta remain high-priority imperial nodes. The North Africa/Suez buffer is retained at a smaller proportion so the AI does not park an excessive fraction of the army there.

When Japan enters the war, ENG/RAJ receive Burma priority and Britain adds Malaysia/Burma pressure while keeping Australia/New Zealand secondary. Commonwealth helpers were retained but normalized from several 500-2000 scale values.

### Allied offensive transition

Early invasions remain discouraged before 1942, but the old permanent/stacking invasion blocks were consolidated. From 1942 onward the Allies can build toward Torch; from 1943 naval-invasion focus rises; from spring 1944 Normandy receives explicit invasion demand and execution.

British rewrite commit: `fcebd166750dc12bed40a8478bf652c32be3a9ee`.

## Defines policy / naval NAI status

The temporary standalone file `common/defines/zz_HER_AI_navy.lua` was removed after the user requested that AI define changes stay in the main defines file.

The two proposed naval values therefore are **not active at this point**:

- `AI_TASKFORCE_REQUIRED_RESERVE_RATIO`: proposed 0.20 -> 0.10;
- `NAVAL_MISSION_AGGRESSIVE_ESCORT_DIVISOR`: proposed 2.0 -> 1.25.

They should be applied directly in `common/defines/00_defines.lua` when the main defines file is edited safely. No separate AI defines file should be reintroduced for this purpose.

## Next audit order

1. USA country strategy phases.
2. JAP country strategy phases and Pacific operation sequence.
3. ITA/FRA cleanup.
4. Operation strategy files and remaining microscripts.
5. Inventory existing AI-only helper systems before creating new concessions.

CHI, SOV, GER and ENG have first-pass country strategies and should be revisited after division-template/strategy-plan integration and hands-off observation.

## Hands-off requirement

Do not judge strategy weights only from code. After Block 6 and strategy-plan integration, record country behavior at fixed milestones and use AI debug interfaces to identify the layer that actually caused a bad decision before changing global NAI values.
