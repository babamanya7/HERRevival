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
7. Division-template design is owned by the dedicated `ai_templates` block; strategy files should not become a second template implementation.
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

## Strategy plans — BLOCK 7 CODE PASS COMPLETE

All eight target-major historical plans now use historical-only lifecycle behavior and a modest research overlay. `ai_focuses` remains the broad research personality. The source-level pass also checks exact IDs, prerequisites and availability against the current HER focus trees rather than trusting legacy comments.

### SOV

- unconditional activation removed;
- old air/naval/industry research hammer replaced by a bounded land/air/industry overlay;
- prewar naval/Far-East distractions and Iran were removed from the main 1941 queue;
- Winter-War-dependent and wartime emergency focuses remain governed by their actual availability gates.

Commit: `27efc0fe1bb544e681dc4358b56ae56b0aa9c9e6`.

### USA

The old plan started at `USA_cash_and_carry_act` even though HER requires `USA_start -> USA_renew_the_neutrality_act -> USA_spanish_civil_war_amendment -> USA_cash_and_carry_act`. Those prerequisites are now explicit. `USA_join_the_allies` also sits after its real prerequisite `USA_the_giant_wakes`.

Commit: `d8687ffdbe55b9b71da193ecdd527ad89679be36`.

### JAP

The Southern Operation path now follows its real HER dependency chain: `JAP_sign_tripartite_pact -> JAP_test_the_soviets / JAP_strike_south_doctrine -> JAP_non_aggression_pact_with_the_soviet_union -> JAP_preparations_to_secure_the_islands -> JAP_strike_on_the_southern_resource_area`. Optional army/naval improvements no longer delay the critical 1941 branch.

Commit: `fb3ffd73d063baae4d4f05b651b08742dc224e9b`.

### GER

The old plan placed `GER_prepare_barbarossa` ahead of the branch needed to unlock it. HER requires `GER_an_invincible_army` plus `GER_second_vienna_award`; the latter requires the Hungary/Romania alignment branch. The queue is now rearmament -> revisionism -> Poland/France -> conquest economy/Axis alignment -> Second Vienna -> Barbarossa. `GER_the_supreme_leader`, which actually checks German control of Moscow, was moved to the late-war section.

Commit: `0c21a46d4a9de06dfa516568c34d0ff7d15048e5`.

### ENG

The Home Defence chain is now dependency-safe: `ENG_home_defence -> ENG_womans_land_army -> ENG_emergency_powers -> ENG_kickstart_the_war_industry`, while `ENG_prepare_for_the_inevitable` also sits after Home Defence. The radar/intelligence queue now explicitly includes the Bawdsey/Shadow Scheme/Chain Home/Bletchley prerequisites before Tizard and crypto priorities.

Commit: `c7218d5fdf6f7354915aea431090aa13457fe62c`.

### FRA

A real dependency inversion was fixed in the industrial branch. HER `FRA_industrial_expansion` requires both `FRA_metropolitan_france` and `FRA_algerie_france`, while `FRA_algerie_france` itself requires the colonial-investment branch. The old plan tried `FRA_industrial_expansion` before `FRA_invest_in_the_colonies` / `FRA_algerie_france`; the queue now opens both halves before the combined expansion and research-slot follow-up.

Commit: `090e8b96397c9607b8c75f7136ebc6d30a4e567b`.

### CHI

The historical plan no longer begins as a stack of unavailable wartime focuses. It now builds the Three Principles/nationalism/foreign-threat/United Front and Military Affairs foundations first, then gives wartime priority to `CHI_war_of_resistance -> CHI_industrial_evacuations -> CHI_scorched_earth_tactics -> CHI_army_reform`. Aid-route development follows the immediate survival package. `CHI_war_of_national_liberation` remains surrender-progress gated by the actual HER focus and is deliberately placed after the first emergency measures.

Commit: `56a6111352dd320e38c08b7460aa54493e2ecd64`.

### ITA

First-pass source audit found the sampled historical chains already dependency-safe and therefore did not justify a mechanical rewrite. The plan has `ITA_italian_highways_bba` before `ITA_steel_industry_in_terni`, the Terni branch before `ITA_industria_della_gomma_sintetica`, and synthetic industry before `ITA_strengthen_northern_industry`. Likewise `ITA_naval_power_projection` precedes both `ITA_oto_naval_guns` and `ITA_expand_naval_facilities`; `ITA_culto_del_duce` precedes `ITA_the_man_of_providence`, and the propaganda chain keeps `ITA_ministero_della_cultura_popolare -> ITA_believe_obey_fight` in dependency order. No change was made merely for churn.

Block 7 is now code-complete pending integrated hands-off validation.

## Defines policy / naval NAI status

The temporary standalone `common/defines/zz_HER_AI_navy.lua` was removed. Proposed naval NAI values remain intentionally inactive:

- `AI_TASKFORCE_REQUIRED_RESERVE_RATIO`: 0.20 -> proposed 0.10;
- `NAVAL_MISSION_AGGRESSIVE_ESCORT_DIVISOR`: 2.0 -> proposed 1.25.

Apply them only by editing `common/defines/00_defines.lua` directly after the scripted strategy/template layers are stable.

## Next audit order

1. `ai_templates`: full division-template implementation for GER/SOV/ENG/USA/JAP/ITA/FRA/CHI, using current HER battalion/support IDs and country-specific roles.
2. Inventory remaining AI-only helper systems and add only targeted concessions that solve demonstrated engine limitations.
3. NAI and direct edits to `common/defines/00_defines.lua` only after the scripted/template layers are stable.

## Hands-off requirement

Do not judge strategy weights only from code. After strategy-plan and template integration, record country behavior at fixed milestones and use AI debug interfaces to identify the layer that caused bad decisions before changing global NAI values.
