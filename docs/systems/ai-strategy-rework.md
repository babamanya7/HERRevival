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

- ENG: `EAI_ENG_focus_on_screens`, `ENG_naval_role_ratios_historical`, `ENG_naval_role_ratios_anti_submarines` use old roles. A new VNR bridge now supplies the intended ASW behavior; the old blocks should be removed or converted during cleanup.
- JAP: `JAP_naval_role_ratios_historical` and `_late` likewise use old naval production roles. Their non-role `unit_ratio` settings may still be useful and must not be deleted mechanically.

## Implemented bridge strategies

`common/ai_strategy/HER_naval_rework_strategies.txt` was added during the naval pass.

It provides:

- pre-war British VNR escort/screen buildup;
- dynamic British ASW emergency production using the existing `anti_submarine_strategy_required_trigger`;
- an always-on lighter ENG-vs-GER screen bias;
- USA/JAP Pacific-war carrier/screen/invasion-focus boosts.

This file is intentionally a bridge while the large legacy country files are audited. Once all country strategy cleanup is complete, duplicated dead blocks can be removed safely.

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

## Soviet strategy audit — IN PROGRESS

The current SOV file contains useful historical phase logic but also several legacy problems that need a deliberate rewrite rather than isolated number tweaks:

- `SOV_third_fyp` applies extremely large permanent military-industrial weights (`added_military_to_civilian_factory_ratio = 1000`, `arms_factory = 1500`) from February 1938 onward;
- pre-Barbarossa area priorities use `1000-2000` scale values across many regions simultaneously, which makes relative operational priority difficult to reason about;
- wartime front requests and area priorities likewise stack very large values across nearly the entire western front;
- a useful defensive phase already exists (`SOV_be_defensive`: careful, no manual attacks, no order execution before November 1941), which should be preserved conceptually;
- scripted winter counteroffensives exist for 1941/42 and 1942/43, and a late-war Bagration phase exists, providing a good basis for a cleaner phased Eastern Front model;
- numerous city-buffer strategies exist and should be checked against the current HER state map before being retained unchanged.

The SOV pass should therefore preserve the good phase architecture while normalizing industry/front weights and moving from broad legacy areas to the newer `soviet_north` / `soviet_center` / `soviet_south` / `caucasus` / `crimea` operational aliases where useful.

## Defines policy / naval NAI status

The temporary standalone file `common/defines/zz_HER_AI_navy.lua` was removed after the user requested that AI define changes stay in the main defines file.

The two proposed naval values therefore are **not active at this point**:

- `AI_TASKFORCE_REQUIRED_RESERVE_RATIO`: proposed 0.20 -> 0.10;
- `NAVAL_MISSION_AGGRESSIVE_ESCORT_DIVISOR`: proposed 2.0 -> 1.25.

They should be applied directly in `common/defines/00_defines.lua` when the main defines file is edited safely. No separate AI defines file should be reintroduced for this purpose.

## Next audit order

1. SOV country strategy phases and Eastern Front behavior.
2. GER country strategy phases.
3. ENG country strategy phases and removal of dead old naval-role helpers.
4. USA country strategy phases.
5. JAP country strategy phases and Pacific operation sequence.
6. ITA/FRA cleanup.
7. Operation strategy files and remaining microscripts.
8. Inventory existing AI-only helper systems before creating new concessions.

CHI already has a first-pass country strategy and should be revisited after division-template and aid-system integration.

## Hands-off requirement

Do not judge strategy weights only from code. After Block 6 and strategy-plan integration, record country behavior at fixed milestones and use AI debug interfaces to identify the layer that actually caused a bad decision before changing global NAI values.
