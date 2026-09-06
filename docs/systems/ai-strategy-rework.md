# HER AI Strategy Rework

Status: IN PROGRESS
Branch: `AI-rework`
Started: 2026-09-06

## Scope

Block 6 covers `common/ai_strategy`: country production personalities, industry phases, front allocation, operational behavior, naval integration and scripted AI reactions.

## Architectural rules

1. `common/ai_strategy/naval_production.txt` owns HER/VNR ship-production roles.
2. Country files may add dynamic naval overrides, but current VNR roles (`vnr_naval_*`) must be used for actual ship-construction pressure.
3. GER/SOV/ENG/USA/JAP/ITA/FRA/CHI have dedicated AI personalities; generic production should not stack on them unless explicitly intended.
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

`common/ai_strategy/SOV.txt` now uses explicit phases:

- 1936-37 civilian industrialization;
- 1938-39 gradual military ramp;
- 1940 prewar mobilization;
- full wartime economy;
- pre-Barbarossa westward concentration;
- defensive opening through mid-November 1941;
- winter 1941/42 counteroffensive;
- defensive spring-autumn 1942 with southern/Caucasus emphasis;
- winter 1942/43 counteroffensive;
- sustained 1943 offensive;
- Bagration rush phase;
- late-war drive into the Reich.

Large legacy `1000-2000` area priorities and permanent industrial weights were removed. City buffers were consolidated and Far-East demand is reduced while Germany is the main threat.

Main commit: `dd209ec98904365275281f29eb61b1903d9f4b94`; trigger fix: `42cc292067a72cb15e860d95f309471f63cc8e9f`.

## Germany — IMPLEMENTED FIRST PASS

`common/ai_strategy/GER.txt` now directly expresses the intended force structure rather than using negative armor/motorized values plus compensating helpers. It has:

- 1936-37 and 1938-39 rearmament phases;
- Poland rush and armor concentration;
- Benelux / France operational phases avoiding the Maginot;
- Barbarossa preparation with logistics stockpiling;
- aggressive 1941 opening;
- winter pause;
- 1942 southern/Caucasus offensive;
- more sustainable late Eastern war;
- emergency reaction to Allied landings;
- fighter/interceptor/CAS Schwerpunkt;
- U-boat-heavy Atlantic behavior without obsolete vanilla naval roles.

Commit: `8498b28475d585a1657770c2c864f529047c1c90`.

## United Kingdom — IMPLEMENTED FIRST PASS

`common/ai_strategy/ENG.txt` was rebuilt around Home Defence/RAF, Battle of the Atlantic and a limited expeditionary army.

Key changes:

- fighters/interceptors and maritime aviation are explicit priorities;
- home-island reserve and RAF Home Defence are maintained;
- Britain no longer overcommits the BEF into collapsing Benelux/France;
- Suez/Gibraltar/Malta and North Africa remain important without consuming an excessive share of the army;
- Burma/Malaya gain priority when Japan enters the war;
- early invasions remain restrained, then transition to Torch and later Normandy;
- obsolete `EAI_ENG_focus_on_screens`, `ENG_naval_role_ratios_historical` and old anti-submarine `naval_*` blocks were removed;
- VNR ASW response remains in the naval bridge.

Commit: `fcebd166750dc12bed40a8478bf652c32be3a9ee`.

## United States — IMPLEMENTED FIRST PASS

`common/ai_strategy/USA.txt` now uses staged mobilization and simultaneous Europe/Pacific pressure:

- 1936-38 civilian buildup;
- 1939-41 defense ramp;
- huge but bounded wartime expansion;
- large infantry army with meaningful armor/motorization and specialist marines;
- strong fighter/CAS/naval/carrier aviation;
- carrier/screen/convoy-heavy naval demand;
- dynamic VNR ASW response;
- Europe First without abandoning the Pacific;
- explicit Pacific counteroffensive from 1942 and Home Islands pressure from 1944;
- removal of old broad buffers that parked large fractions of the US Army across England, Spain and all of Africa.

Shared Torch/D-Day orchestration remains in the British strategy file to avoid duplicate invasion scripts.

Commit: `190e090d28a13b33057e41f2c26c26d4d87d144f`.

## Japan — IMPLEMENTED FIRST PASS

`common/ai_strategy/JAP.txt` was rebuilt around a China-war -> Southern Operation -> Pacific offensive -> outer-perimeter defense sequence.

### Force structure

- infantry/artillery remain the land-war core;
- marines are an important specialist arm but no longer an oversized `25` ratio on top of a 90-infantry baseline;
- armor/motorization remain limited;
- fighters, naval bombers and carrier aircraft receive strong pressure;
- strategic bombing is suppressed;
- general naval demand favors carriers/screens/convoys, while exact VNR ship construction remains in `naval_production.txt` and the naval bridge.

### China

Before the Pacific war, China receives the majority of Japanese land attention through north/central/coastal priorities and balanced offensive execution. Coastal invasion pressure is retained. Once the USA/ENG war begins, China demand is reduced rather than allowing the continental war to consume the whole army.

### Southern Operation

The old narrow scripted windows were replaced by a broader preparation and first-wave phase. From mid-1941 Japan prepares PHI/MAL/INS; once war begins, all three receive strong but ordered invasion demand with the Philippines highest, then Malaya, then the East Indies. Front pushes after landing use rush execution.

The earlier impossible Southern Expansion date gate was already fixed before this rewrite; the new phase structure no longer depends on a single tiny date window to make the whole Pacific opening work.

### Pacific war

During 1942 Japan strongly prioritizes `pacific_front`, `japan_routs`, Philippines and East Indies while keeping a high naval-invasion focus. The earlier naval bridge adds VNR carrier/screen production pressure while this country file provides the operational demand that should make those fleets leave port and support active objectives.

From 1943 the AI transitions toward an outer-perimeter posture: Japan still contests the Pacific but raises priority for home waters and the Home Islands. A separate late-war emergency buffer keeps a meaningful home reserve instead of spending every division in China/Burma.

Australia/New Zealand and deep India are deliberately downweighted before 1944 to prevent classic AI overextension after the initial conquests.

### Soviet policy

Japan is discouraged from opening a Soviet war while China or the Western Allies remain active threats. The intent is to avoid throwing the Kwantung Army into a second continental war during the decisive Pacific period.

### Cleanup

The old `JAP_naval_role_ratios_historical` and `_late` blocks using obsolete vanilla `naval_*` production roles were removed. The old broad always-on priorities for North/South America and other irrelevant theaters were also removed.

Commit: `03475ca020fcea9a4d403a0e3620584b88386f4c`.

## Defines policy / naval NAI status

The temporary standalone `common/defines/zz_HER_AI_navy.lua` was removed. Proposed naval NAI values are intentionally not active yet:

- `AI_TASKFORCE_REQUIRED_RESERVE_RATIO`: 0.20 -> proposed 0.10;
- `NAVAL_MISSION_AGGRESSIVE_ESCORT_DIVISOR`: 2.0 -> proposed 1.25.

They should be applied only by editing `common/defines/00_defines.lua` directly, after the scripted strategy layer is complete and hands-off behavior can be evaluated.

## Next audit order

1. ITA country strategy cleanup and Mediterranean/North Africa phases.
2. FRA country strategy cleanup and 1939-40 defense behavior.
3. Country operation-strategy files and remaining `HER_Microscripts`.
4. Inventory existing AI-only helper systems before adding new concessions.
5. `ai_strategy_plans` phase and historical-plan cleanup.

CHI/SOV/GER/ENG/USA/JAP now have first-pass country strategies. Revisit them after division-template/strategy-plan integration and hands-off observation.

## Hands-off requirement

Do not judge strategy weights only from code. After Block 6 and strategy-plan integration, record country behavior at fixed milestones and use AI debug interfaces to identify the layer that caused bad decisions before changing global NAI values.
