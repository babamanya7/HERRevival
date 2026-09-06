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

## Defines policy / naval NAI status

The temporary standalone file `common/defines/zz_HER_AI_navy.lua` was removed after the user requested that AI define changes stay in the main defines file.

The two proposed naval values therefore are **not active at this point**:

- `AI_TASKFORCE_REQUIRED_RESERVE_RATIO`: proposed 0.20 -> 0.10;
- `NAVAL_MISSION_AGGRESSIVE_ESCORT_DIVISOR`: proposed 2.0 -> 1.25.

They should be applied directly in `common/defines/00_defines.lua` when the main defines file is edited safely. No separate AI defines file should be reintroduced for this purpose.

## Next audit order

1. GER country strategy phases.
2. ENG country strategy phases and removal of dead old naval-role helpers.
3. USA country strategy phases.
4. JAP country strategy phases and Pacific operation sequence.
5. ITA/FRA cleanup.
6. Operation strategy files and remaining microscripts.
7. Inventory existing AI-only helper systems before creating new concessions.

CHI and SOV have first-pass country strategies and should be revisited after division-template/strategy-plan integration and hands-off observation.

## Hands-off requirement

Do not judge strategy weights only from code. After Block 6 and strategy-plan integration, record country behavior at fixed milestones and use AI debug interfaces to identify the layer that actually caused a bad decision before changing global NAI values.
