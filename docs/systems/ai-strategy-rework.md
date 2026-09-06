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
9. Historical strategy plans for the eight target majors activate only with `is_historical_focus_on = yes` and cleanly abort when that condition no longer applies.
10. A historical focus plan is a priority queue, not a substitute for the focus tree. Availability/prerequisite gates remain authoritative; plan ordering must therefore be checked against the actual HER national-focus files.

## Generic strategy layer — CLEANED

`common/ai_strategy/default.txt` was rebuilt so generic production/template logic is fallback behavior rather than a second personality for the eight majors. Obsolete generic vanilla naval-role ratios and accidental major overlaps were removed.

Commit: `cde47aa9f87bb20c3ae7d5e9d0e9ee19a11d9ce4`.

## Naval strategy integration

`naval_production.txt` owns country-specific VNR ship-production plans. `HER_naval_rework_strategies.txt` provides dynamic ENG escort/ASW behavior and USA/JAP Pacific carrier-screen-invasion pressure. Old vanilla `naval_*` helpers are removed during country rewrites.

## Country strategies — FIRST PASS COMPLETE

All eight target majors have dedicated first-pass country strategies:

- CHI: land-defense power focused on infantry/artillery/AA/AT, Japan front and defense in depth. Commits `99b3f1789b340a255bb2683942d9ef046413ec83`, `64882449bb3d0ce1720b64b84682a305eeae1ed7`.
- SOV: phased industrialization, 1941 defensive opening, winter counteroffensives, 1942 southern emphasis, 1943+ offensive transition and Far-East de-emphasis while Germany is the main threat. Commits `dd209ec98904365275281f29eb61b1903d9f4b94`, `42cc292067a72cb15e860d95f309471f63cc8e9f`.
- GER: staged rearmament, Poland/France campaigns, Barbarossa preparation, winter pause, 1942 southern offensive, later sustainable Eastern war and Allied-landing reaction. Commit `8498b28475d585a1657770c2c864f529047c1c90`.
- ENG: Home Defence/RAF, Battle of the Atlantic, limited expeditionary army, Mediterranean/Empire priorities and staged Torch/Normandy transition. Commit `fcebd166750dc12bed40a8478bf652c32be3a9ee`.
- USA: staged mobilization, two-ocean war, carrier/naval aviation, Europe First without abandoning the Pacific and explicit 1942+ counteroffensive. Commit `190e090d28a13b33057e41f2c26c26d4d87d144f`.
- JAP: China war -> Southern Operation -> 1942 Pacific offensive -> outer-perimeter/home defense. Commit `03475ca020fcea9a4d403a0e3620584b88386f4c`.
- ITA: Mediterranean-centered war, Libya/Egypt/Suez, bounded Eastern Front participation, homeland/Sicily reserves and stronger air/naval support. Commit `3d805e1da53fe5faabfb246544b68da3380863cf`.
- FRA: defensive metropolitan posture, careful Maginot defense, conditional Dyle/Benelux phase, withdrawal when the Low Countries collapse and mobile armored reserve. Commit `3137d7e08a6f2f90c81b4e92549c332211a65111`.

## Global strategy cleanup — COMPLETE FIRST PASS

`HER_Microscripts.txt` was cleaned so generic civilian construction, naval-invasion pressure, force concentration and military-factory ramping no longer overwrite the eight dedicated majors. The global convoy-raiding helper and global all-template `+100` block were removed, extreme garrison suppression was bounded, and the aluminium-refinery condition was fixed. Commit `7309fc859fc01a17cba646069e59f0d4ae09ee4a`.

`FAI_Frontline_Management.txt` was isolated from the eight majors so generic rush/careful/emergency and priority-10000 tactical orders cannot override deliberate national phases. Local supply/capital/invasion positioning remains global. Commit `039388fab5afa2a978d015580ad382c3bf7e0ffd`.

`GER_operation_strats.txt`, `SOV_operation_strats.txt`, `ENG_operation_strats.txt` and `generic_operation_strats.txt` were audited and retained because they are intelligence/operative logic rather than land/naval operational war plans.

## Strategy plans — MAJOR LIFECYCLE / RESEARCH NORMALIZATION COMPLETE

All eight target-major historical plans now use historical-only lifecycle behavior and a modest research overlay. `ai_focuses` remains the broad research personality.

- USA: historical gating and bounded air/naval/industry overlay. Commit `4c30f4e25679cedc4f0ca16d08187df57a95f046`.
- CHI: historical gating and modest infantry/artillery/support/industry overlay. Commit `a1af66ce54bc32dba3f68f060b9ebcdc7b8fb9c0`.
- GER: historical gating; removed `template_prio = medium_armor 111`; reduced the old infantry/air research hammer. Commit `5300cf215f7184a402df76531dff2c2a81394b57`.
- ENG: normalized lifecycle and reduced `air_equipment = 100` into a mixed RAF/naval/industry/support overlay. Commit `d983ddcfdca4d6d5804557e2e194e5c75e99e4cf`.
- JAP: normalized lifecycle and replaced `air_equipment = 70` with a smaller air/naval/land-industry overlay. Commit `5e18e9b68fcc06175ac030a2a4283bdf3356bd8e`.
- ITA: normalized lifecycle and replaced the old air-heavy overlay with air/naval/artillery/industry weighting. Commit `c63dfd9d23213dbeda86daed0149bb1885fab64e`.
- FRA: normalized lifecycle and replaced `air_equipment = 60` with air/artillery/armor/industry weighting. Commit `3148d7b20328c4aec463247001aacf12eebb987d`.
- SOV: changed unconditional activation to historical-only lifecycle; reduced the old `air_equipment = 50`, `naval_equipment = -100`, `industry = 25` hammer to a balanced industry/land/air overlay; removed prewar naval/Far-East distractions and the Iran operation from the main historical queue while retaining the late anti-Japanese objective. Commit `27efc0fe1bb544e681dc4358b56ae56b0aa9c9e6`.

## Focus-queue validation — IN PROGRESS

The next pass validates exact IDs, prerequisites and availability against the current HER focus trees instead of trusting legacy comments or old plan order.

SOV audit notes already confirmed directly from `common/national_focus/soviet.txt`:

- the industrial/political focus IDs used by the cleaned plan are current HER IDs;
- `SOV_superior_war_machines` is date-gated after 1940-06-01 and follows the artillery branch;
- `SOV_evolution_of_the_air_strategy` and `SOV_lessons_of_war` depend on the Winter War/FIN resolution path, so their historical placement must be treated as availability-gated rather than a guaranteed calendar slot;
- wartime focuses such as `SOV_emergency_powers`, `SOV_form_the_stavka`, `SOV_move_industry_to_the_urals`, `SOV_tankograd` and `SOV_great_patriotic_war` have their own war/major-enemy gates and therefore belong after the prewar queue rather than being forced by generic research/strategy weights;
- the Soviet naval branch exists and remains available, but it is intentionally no longer part of the main 1941 historical priority queue because the land-air emergency against Germany is strategically dominant.

The same source-level validation is required for GER/ENG/USA/JAP/ITA/FRA/CHI before Block 7 is considered complete.

## Defines policy / naval NAI status

The temporary standalone `common/defines/zz_HER_AI_navy.lua` was removed. Proposed naval NAI values remain intentionally inactive:

- `AI_TASKFORCE_REQUIRED_RESERVE_RATIO`: 0.20 -> proposed 0.10;
- `NAVAL_MISSION_AGGRESSIVE_ESCORT_DIVISOR`: 2.0 -> proposed 1.25.

Apply them only by editing `common/defines/00_defines.lua` directly after the scripted strategy/template layers are stable.

## Next audit order

1. Validate GER/JAP/USA/ENG focus queues against current HER focus trees.
2. Validate ITA/FRA/CHI focus queues.
3. Inventory remaining AI-only helper systems before adding new concessions.
4. `ai_templates` full division-template implementation.
5. NAI and direct edits to `common/defines/00_defines.lua` only after the scripted layers are stable.

## Hands-off requirement

Do not judge strategy weights only from code. After strategy-plan and template integration, record country behavior at fixed milestones and use AI debug interfaces to identify the layer that caused bad decisions before changing global NAI values.
