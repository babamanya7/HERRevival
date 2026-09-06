# HER AI Strategy Rework

Status: IN PROGRESS
Branch: `AI-rework`
Started: 2026-09-06

## Scope

Block 6 covers `common/ai_strategy`: country production personalities, industry phases, front allocation, operational behavior, naval integration and scripted AI reactions.

## Architectural rules

1. `common/ai_strategy/naval_production.txt` owns HER/VNR ship-production roles.
2. Country files may add dynamic naval overrides, but current VNR roles (`vnr_naval_*`) must be used for actual ship-construction pressure.
3. GER/SOV/ENG/USA/JAP/ITA/FRA/CHI have dedicated AI personalities; generic production/frontline behavior should not stack on them unless explicitly intended.
4. Temporary behavior needs deliberate lifecycle handling (`abort_when_not_enabled` or explicit `abort`).
5. Prefer phase/condition logic over permanent huge weights.
6. AI defines belong in the main `common/defines/00_defines.lua`; do not create standalone AI define files.
7. Division-template design remains a later dedicated block; strategy files may set broad template priorities but should not become the final template implementation.

## Generic strategy layer — CLEANED

`common/ai_strategy/default.txt` was rebuilt so generic production/template logic is fallback behavior rather than a second personality for the eight majors.

Fixed overlaps included USA inheriting default production, FRA/CHI inheriting old generic naval roles, most majors inheriting generic BBA air production, ITA inheriting generic garrison behavior, and CHI inheriting generic template priorities. Obsolete generic `naval_*` role-ratio logic was removed because HER uses VNR production roles.

Commit: `cde47aa9f87bb20c3ae7d5e9d0e9ee19a11d9ce4`.

## Naval strategy integration

`naval_production.txt` already contains country-specific VNR ship-production plans. The naval rework added `HER_naval_rework_strategies.txt` as a bridge for dynamic behavior:

- ENG prewar escort buildup;
- ENG Battle of the Atlantic / ASW emergency response through `anti_submarine_strategy_required_trigger`;
- USA Pacific carrier/screen/invasion pressure;
- JAP Pacific carrier/screen/invasion pressure.

Old vanilla `naval_*` role helpers are being removed country-by-country during rewrites.

## China — IMPLEMENTED FIRST PASS

`common/ai_strategy/CHI.txt` now treats Nationalist China as a land-defense power: infantry/artillery/AA/AT, minimal armor and offensive aviation, no blue-water fleet program, Japan-focused front priorities and defense in depth.

Commits: `99b3f1789b340a255bb2683942d9ef046413ec83`, trigger fix `64882449bb3d0ce1720b64b84682a305eeae1ed7`.

## Soviet Union — IMPLEMENTED FIRST PASS

`common/ai_strategy/SOV.txt` now uses explicit economic and Eastern Front phases, including a defensive opening in 1941, winter counteroffensive, 1942 southern-defense/offensive cycle, sustained 1943 pressure and a Bagration phase. Large legacy 1000-2000 area priorities and permanent industrial weights were removed. Far-East demand is reduced while Germany is the main threat.

Main commit: `dd209ec98904365275281f29eb61b1903d9f4b94`; trigger fix: `42cc292067a72cb15e860d95f309471f63cc8e9f`.

## Germany — IMPLEMENTED FIRST PASS

`common/ai_strategy/GER.txt` now has staged rearmament, Poland/France campaigns, Barbarossa preparation, aggressive 1941 opening, winter pause, 1942 southern/Caucasus emphasis, later sustainable Eastern war, Allied-landing reaction, fighter/interceptor/CAS focus and U-boat-heavy Atlantic behavior without obsolete vanilla naval roles.

Commit: `8498b28475d585a1657770c2c864f529047c1c90`.

## United Kingdom — IMPLEMENTED FIRST PASS

`common/ai_strategy/ENG.txt` was rebuilt around Home Defence/RAF, Battle of the Atlantic and a limited expeditionary army. Britain no longer overcommits to collapsing France/Benelux; Suez/Gibraltar/Malta remain important; Burma/Malaya rise when Japan enters; invasion logic transitions from restraint to Torch/Normandy. Obsolete British vanilla naval-role blocks were removed.

Commit: `fcebd166750dc12bed40a8478bf652c32be3a9ee`.

## United States — IMPLEMENTED FIRST PASS

`common/ai_strategy/USA.txt` now uses staged mobilization, a large combined-arms army, strong carrier/naval aviation, dynamic VNR ASW response, Europe First without abandoning the Pacific, and an explicit Pacific counteroffensive from 1942. Old broad buffers that parked large army fractions across multiple continents were removed.

Commit: `190e090d28a13b33057e41f2c26c26d4d87d144f`.

## Japan — IMPLEMENTED FIRST PASS

`common/ai_strategy/JAP.txt` now follows China war -> Southern Operation -> 1942 Pacific offensive -> outer-perimeter/home defense. Southern Operation is a broad phase instead of fragile narrow date windows. Australia/deep India are downweighted before 1944, and obsolete Japanese vanilla naval-role blocks were removed.

Commit: `03475ca020fcea9a4d403a0e3620584b88386f4c`.

## Italy — IMPLEMENTED FIRST PASS

`common/ai_strategy/ITA.txt` was rebuilt around Mediterranean war: infantry/artillery-heavy army, limited armor, meaningful Regia Aeronautica, phased rearmament, fast Ethiopia cleanup, Libya/Egypt/Suez focus, bounded Eastern Front participation, homeland/Sicily reserves and reduced naval paralysis. Obsolete Italian vanilla naval-role blocks were removed.

Commit: `3d805e1da53fe5faabfb246544b68da3380863cf`.

## France — IMPLEMENTED FIRST PASS

`common/ai_strategy/FRA.txt` now acts as a defensive metropolitan power: artillery-heavy army, serious fighter force, mobile armored reserve, careful Maginot defense, conditional Dyle/Benelux phase, withdrawal when the Low Countries collapse, and reduced colonial distractions. Obsolete French vanilla naval-role production was removed.

Commit: `3137d7e08a6f2f90c81b4e92549c332211a65111`.

## Global microscripts — CLEANED

`common/ai_strategy/HER_Microscripts.txt` was audited because it still contained global orders capable of silently overriding the new country personalities.

Important fixes:

- the old `only_civ_construction` no longer applies a `building_target = 1000` to the eight dedicated majors; it is now a bounded fallback for other peaceful isolation/civilian-economy countries;
- the global `convoy_raiding_enthusiast` was removed. Previously every country at war received the same convoy-raiding threshold, which worked directly against differentiated naval behavior such as British escort/ASW and US/Japanese fleet warfare;
- generic naval-invasion pressure and force-concentration helpers now exclude the eight dedicated majors;
- the global `division_template_is_really_cool` block was removed. It gave +100 priority to almost every template family and therefore erased country differentiation; final template design belongs to `ai_templates`;
- low-tension/minor-war garrison penalties were reduced from `-9999` to bounded values. The old logic could effectively disable home/coastal defense for long periods;
- generic military-factory ramping now excludes the eight majors so it no longer stacks on country economic phases;
- the aluminium refinery helper was corrected to check low `aluminium` output rather than low `steel` output;
- special-project facility/scientist helpers, nuclear late-game helpers, civil-war behavior, train stockpiling and resource-refinery logic were retained.

Commit: `7309fc859fc01a17cba646069e59f0d4ae09ee4a`.

## Generic frontline manager — ISOLATED FROM MAJORS

`common/ai_strategy/FAI_Frontline_Management.txt` was a second hidden global war-plan layer. Its normal/rush/careful rules, emergency modes, pocket closure and empty-state rushes used priorities from 50 up to 10000 and could override deliberate country phases.

The broad frontline posture and tactical rush helpers now explicitly exclude GER/SOV/ENG/USA/JAP/ITA/FRA/CHI. This is critical for planned pauses such as Soviet opening defense or German winter pauses: a global `this_state_is_empty` priority 10000 must not silently order attacks during those phases.

The generic manager remains available to countries without dedicated operational personalities. The supply/capital/invasion-positioning helper remains global because it adjusts local demand rather than selecting an overall offensive doctrine.

Commit: `039388fab5afa2a978d015580ad382c3bf7e0ffd`.

## Operation strategies — AUDITED / RETAINED

`GER_operation_strats.txt`, `SOV_operation_strats.txt`, `ENG_operation_strats.txt` and `generic_operation_strats.txt` were inspected. They are intelligence-agency/operative logic rather than land/naval operational war plans: collaboration governments, resistance work, Trotsky operations, Heavy Water/Anthropoid and generic operation execution. They do not conflict with the new front/naval strategy architecture and are retained for now.

## Defines policy / naval NAI status

The temporary standalone `common/defines/zz_HER_AI_navy.lua` was removed. Proposed naval NAI values are intentionally not active yet:

- `AI_TASKFORCE_REQUIRED_RESERVE_RATIO`: 0.20 -> proposed 0.10;
- `NAVAL_MISSION_AGGRESSIVE_ESCORT_DIVISOR`: 2.0 -> proposed 1.25.

They should be applied only by editing `common/defines/00_defines.lua` directly, after the scripted strategy layer is complete and hands-off behavior can be evaluated.

## Next audit order

1. Inventory remaining AI-only helper systems before adding new concessions.
2. `ai_strategy_plans` phase and historical-plan cleanup.
3. `ai_templates` full division-template implementation.
4. NAI and direct edits to `common/defines/00_defines.lua` only after the scripted layers are stable.

All eight target majors now have first-pass country strategy rewrites. Revisit them after division-template/strategy-plan integration and hands-off observation.

## Hands-off requirement

Do not judge strategy weights only from code. After Block 6 and strategy-plan integration, record country behavior at fixed milestones and use AI debug interfaces to identify the layer that caused bad decisions before changing global NAI values.
