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

- infantry/artillery are the land-war core with specialist marines and limited armor;
- fighter/naval/carrier aviation has high priority;
- China receives the main land focus before the Pacific war, then demand is reduced;
- Southern Operation is a broad phase rather than a fragile tiny date window;
- 1942 is an active Pacific offensive phase;
- from 1943 Japan increasingly protects the outer perimeter, home waters and Home Islands;
- Australia/New Zealand and deep India are downweighted before 1944;
- obsolete Japanese vanilla `naval_*` role blocks were removed.

Commit: `03475ca020fcea9a4d403a0e3620584b88386f4c`.

## Italy — IMPLEMENTED FIRST PASS

`common/ai_strategy/ITA.txt` was rebuilt around the Mediterranean rather than generic Axis participation.

Key changes:

- army remains infantry/artillery-heavy, with limited armor and mobile formations;
- Regia Aeronautica now has meaningful fighter/interceptor/CAS/naval-bomber demand;
- exact naval construction is left to VNR `naval_production.txt`, while general demand favors screens, submarines, convoys and a modest surface fleet;
- 1936-37 industrial buildup and 1938-40 rearmament replace the old mixed static logic;
- Ethiopia is attacked hard early but the Horn is deliberately deprioritized once the major European war begins;
- major-war entry is delayed only until roughly the historical June 1940 window instead of using an extreme effectively permanent `dont_join_wars_with = 1000000` style block;
- France is treated cautiously rather than as the main offensive axis;
- once at war with Britain, Libya/Egypt/Suez and the Italian homeland become the dominant theaters;
- Mediterranean transport avoidance is reduced to caution rather than paralysis so Libya can still be supplied;
- Greece receives a dedicated balanced campaign;
- Italian divisions are discouraged from wandering to Finland, Poland, Denmark and other irrelevant Axis fronts;
- a limited Soviet contribution is allowed without letting the Eastern Front consume the army needed for North Africa and homeland defense;
- homeland reserves now explicitly include north/south Italy and Sicily, with an emergency recall when Allied landings occur;
- obsolete Italian vanilla `naval_*` role-ratio block was removed.

Commit: `3d805e1da53fe5faabfb246544b68da3380863cf`.

## France — IMPLEMENTED FIRST PASS

`common/ai_strategy/FRA.txt` was rebuilt as a defensive metropolitan power with an artillery-heavy army, serious fighter force and mobile armored reserve.

Key changes:

- the old oversized `mountaineers = 30` ratio was removed;
- infantry remains the majority while armor, AT/AA, artillery and modest motorization receive explicit demand;
- the prewar economy now transitions from civilian construction into rearmament, then full wartime expansion against Germany;
- metropolitan reserves were reduced from overlapping 30% static buffers to a single smaller reserve behind northern France/Paris;
- the Maginot line is held carefully without concentrating armor or launching wasteful attacks through it;
- a Dyle/Benelux phase exists while Belgium remains viable, but once the Low Countries begin collapsing the AI pulls demand back into northern France;
- late defensive behavior increases homeland concentration rather than sending troops to colonies;
- fighter/interceptor production and strategic air importance are raised for northern/eastern France;
- Norway, Pacific and distant colonial theaters are downweighted;
- obsolete French vanilla `naval_*` role-ratio production block was removed, leaving VNR naval production as the authoritative ship layer;
- Vichy relation helpers were retained in simplified form.

Commit: `3137d7e08a6f2f90c81b4e92549c332211a65111`.

## Defines policy / naval NAI status

The temporary standalone `common/defines/zz_HER_AI_navy.lua` was removed. Proposed naval NAI values are intentionally not active yet:

- `AI_TASKFORCE_REQUIRED_RESERVE_RATIO`: 0.20 -> proposed 0.10;
- `NAVAL_MISSION_AGGRESSIVE_ESCORT_DIVISOR`: 2.0 -> proposed 1.25.

They should be applied only by editing `common/defines/00_defines.lua` directly, after the scripted strategy layer is complete and hands-off behavior can be evaluated.

## Next audit order

1. Country operation-strategy files and remaining `HER_Microscripts`.
2. Inventory existing AI-only helper systems before adding new concessions.
3. `ai_strategy_plans` phase and historical-plan cleanup.
4. `ai_templates` full division-template implementation.
5. NAI and direct edits to `common/defines/00_defines.lua` only after the scripted layers are stable.

All eight target majors now have first-pass country strategy rewrites. Revisit them after division-template/strategy-plan integration and hands-off observation.

## Hands-off requirement

Do not judge strategy weights only from code. After Block 6 and strategy-plan integration, record country behavior at fixed milestones and use AI debug interfaces to identify the layer that caused bad decisions before changing global NAI values.
