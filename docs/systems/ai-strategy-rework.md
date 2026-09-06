# HER AI Strategy Rework

Status: IN PROGRESS
Branch: `AI-rework`
Started: 2026-09-06

## Scope

Block 6 covers `common/ai_strategy`: country production personalities, industry phases, front allocation, operational behavior, naval integration and scripted AI reactions. Block 7 covers `common/ai_strategy_plans`: historical focus sequencing and a deliberately small research/advisor overlay on top of `ai_focuses`.

## Architectural rules

1. `common/ai_strategy/naval_production.txt` owns HER/VNR ship-production roles.
2. Country files may add dynamic naval overrides, but current VNR roles (`vnr_naval_*`) must be used for actual ship-construction pressure.
3. GER/SOV/ENG/USA/JAP/ITA/FRA/CHI have dedicated AI personalities; generic production/frontline behavior should not stack on them unless explicitly intended.
4. Temporary behavior needs deliberate lifecycle handling (`abort_when_not_enabled` or explicit `abort`).
5. Prefer phase/condition logic over permanent huge weights.
6. AI defines belong in the main `common/defines/00_defines.lua`; do not create standalone AI define files.
7. Division-template design remains a later dedicated block; strategy files may set broad template priorities but should not become the final template implementation.
8. `ai_focuses` owns broad research personality. Historical strategy plans may add only a modest historical overlay; they must not use huge permanent research weights that overpower the country focus layer.
9. Historical strategy plans for the eight target majors should activate only with `is_historical_focus_on = yes` and cleanly abort when that condition no longer applies.

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

## Country strategies — FIRST PASS COMPLETE

All eight target majors now have dedicated first-pass country strategies.

- CHI: land-defense power focused on infantry/artillery/AA/AT, Japan front and defense in depth. Commits `99b3f1789b340a255bb2683942d9ef046413ec83`, `64882449bb3d0ce1720b64b84682a305eeae1ed7`.
- SOV: phased industrialization, 1941 defensive opening, winter counteroffensives, 1942 southern emphasis, 1943+ offensive transition and Far-East de-emphasis while Germany is the main threat. Commits `dd209ec98904365275281f29eb61b1903d9f4b94`, `42cc292067a72cb15e860d95f309471f63cc8e9f`.
- GER: staged rearmament, Poland/France campaigns, Barbarossa preparation, winter pause, 1942 southern offensive, later sustainable Eastern war and Allied-landing reaction. Commit `8498b28475d585a1657770c2c864f529047c1c90`.
- ENG: Home Defence/RAF, Battle of the Atlantic, limited expeditionary army, Mediterranean/Empire priorities and staged Torch/Normandy transition. Commit `fcebd166750dc12bed40a8478bf652c32be3a9ee`.
- USA: staged mobilization, two-ocean war, carrier/naval aviation, Europe First without abandoning the Pacific and explicit 1942+ counteroffensive. Commit `190e090d28a13b33057e41f2c26c26d4d87d144f`.
- JAP: China war -> Southern Operation -> 1942 Pacific offensive -> outer-perimeter/home defense. Commit `03475ca020fcea9a4d403a0e3620584b88386f4c`.
- ITA: Mediterranean-centered war, Libya/Egypt/Suez, bounded Eastern Front participation, homeland/Sicily reserves and stronger air/naval support. Commit `3d805e1da53fe5faabfb246544b68da3380863cf`.
- FRA: defensive metropolitan posture, careful Maginot defense, conditional Dyle/Benelux phase, withdrawal when the Low Countries collapse and mobile armored reserve. Commit `3137d7e08a6f2f90c81b4e92549c332211a65111`.

## Global microscripts — CLEANED

`common/ai_strategy/HER_Microscripts.txt` was audited because it still contained global orders capable of silently overriding the new country personalities.

Important fixes:

- generic civilian-only construction, naval invasion pressure, force concentration and military-factory ramping no longer apply to the eight dedicated majors;
- the global convoy-raiding strategy was removed;
- the global all-template `+100` block was removed so `ai_templates` can own division design;
- low-tension/minor-war garrison penalties were reduced from absolute `-9999` suppression to bounded values;
- aluminium refinery logic now checks aluminium rather than steel;
- useful special-project, scientist, nuclear, civil-war, train-stockpile and resource-refinery helpers were retained.

Commit: `7309fc859fc01a17cba646069e59f0d4ae09ee4a`.

## Generic frontline manager — ISOLATED FROM MAJORS

`common/ai_strategy/FAI_Frontline_Management.txt` was a second hidden global war-plan layer. Its rush/careful/emergency rules and tactical helpers could reach priorities from 50 to 10000 and override country phases.

The broad frontline posture and tactical rush helpers now explicitly exclude GER/SOV/ENG/USA/JAP/ITA/FRA/CHI. The supply/capital/invasion-positioning helper remains global because it adjusts local demand rather than selecting an overall offensive doctrine.

Commit: `039388fab5afa2a978d015580ad382c3bf7e0ffd`.

## Operation strategies — AUDITED / RETAINED

`GER_operation_strats.txt`, `SOV_operation_strats.txt`, `ENG_operation_strats.txt` and `generic_operation_strats.txt` were inspected. They are intelligence-agency/operative logic rather than land/naval operational war plans: collaboration governments, resistance work, Trotsky operations, Heavy Water/Anthropoid and generic operation execution. They do not conflict with the new front/naval strategy architecture and are retained for now.

## Strategy plans — NORMALIZATION PASS IN PROGRESS

The historical-plan layer was found to contain two recurring problems: some plans were enabled unconditionally, and several plans used research weights large enough to overpower the newer `ai_focuses` layer.

Implemented:

- USA historical plan: changed from `always = yes` to `is_historical_focus_on = yes`, added clean lifecycle and reduced the old large air-only overlay. Commits `4c30f4e25679cedc4f0ca16d08187df57a95f046`.
- CHI historical plan: same lifecycle correction and added a modest infantry/artillery/support/industry overlay rather than an empty research block. Commit `a1af66ce54bc32dba3f68f060b9ebcdc7b8fb9c0`.
- GER historical plan: changed from unconditional activation to historical-only lifecycle; removed the `template_prio = medium_armor 111` leakage into the future template block; reduced `infantry_weapons = 50` / `air_equipment = 70` into a balanced small historical overlay. Commit `5300cf215f7184a402df76531dff2c2a81394b57`.
- ENG historical plan: retained historical-only activation but replaced the ineffective dummy abort with `abort_when_not_enabled`; reduced `air_equipment = 100` to a modest RAF/naval/industry/support overlay. Commit `d983ddcfdca4d6d5804557e2e194e5c75e99e4cf`.
- JAP historical plan: retained historical-only activation, normalized lifecycle and replaced `air_equipment = 70` with a smaller air/naval/land-industry overlay. Commit `5e18e9b68fcc06175ac030a2a4283bdf3356bd8e`.
- ITA historical plan: normalized lifecycle and reduced `air_equipment = 40` into a balanced air/naval/artillery/industry overlay. Commit `c63dfd9d23213dbeda86daed0149bb1885fab64e`.
- FRA historical plan: normalized lifecycle and replaced `air_equipment = 60` with a smaller air/artillery/armor/industry overlay consistent with the metropolitan-defense profile. Commit `3148d7b20328c4aec463247001aacf12eebb987d`.

Remaining major-plan cleanup:

- SOV historical plan is still unconditionally enabled and still contains the old `air_equipment = 50`, `naval_equipment = -100`, `industry = 25` style research hammer. It is the final lifecycle/research cleanup item for the eight majors before focus-order validation.
- After SOV, validate the actual national-focus sequences against current HER focus IDs and the newly defined campaign/economic phases. Do not mechanically reorder long focus lists without checking prerequisite structure and historical timing.

## Defines policy / naval NAI status

The temporary standalone `common/defines/zz_HER_AI_navy.lua` was removed. Proposed naval NAI values are intentionally not active yet:

- `AI_TASKFORCE_REQUIRED_RESERVE_RATIO`: 0.20 -> proposed 0.10;
- `NAVAL_MISSION_AGGRESSIVE_ESCORT_DIVISOR`: 2.0 -> proposed 1.25.

They should be applied only by editing `common/defines/00_defines.lua` directly, after the scripted strategy layer is complete and hands-off behavior can be evaluated.

## Next audit order

1. Finish SOV strategy-plan lifecycle/research normalization.
2. Validate eight-major historical focus ordering and exact focus IDs/prerequisites.
3. Inventory remaining AI-only helper systems before adding new concessions.
4. `ai_templates` full division-template implementation.
5. NAI and direct edits to `common/defines/00_defines.lua` only after the scripted layers are stable.

## Hands-off requirement

Do not judge strategy weights only from code. After strategy-plan and template integration, record country behavior at fixed milestones and use AI debug interfaces to identify the layer that caused bad decisions before changing global NAI values.
