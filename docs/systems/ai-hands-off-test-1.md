# HER AI — Hands-off Test 1

Status: READY TO RUN
Branch: `AI-rework`
Baseline prepared: 2026-09-07

## Purpose

The first hands-off run is a diagnostic baseline for the integrated HER AI rework. It is not a final balance test. The goal is to identify runtime failures and systemic AI mistakes after the first complete scripted pass, before tuning global NAI defines or adding further AI-only compensation.

## Baseline configuration

- Historical AI focuses: ON.
- Player/hands-off tag: BRA (`NGame.HANDS_OFF_START_TAG = "BRA"`).
- No manual intervention after game start except pausing to inspect/debug.
- Run target: at least 1943-01-01; continue farther only if the world state remains useful.
- Primary countries: GER, SOV, ENG, USA, JAP, ITA, FRA, CHI.
- Equipment-designer AI templates (tank/air/ship designs) remain deliberately outside this baseline pass.
- Global NAI naval values remain at the current baseline for Test 1. In particular, do not yet change `AI_TASKFORCE_REQUIRED_RESERVE_RATIO = 0.20` or `NAVAL_MISSION_AGGRESSIVE_ESCORT_DIVISOR = 2.0`; scripted naval behavior should be observed first so later define changes have an attributable effect.

## Integrated systems included in Test 1

1. Reworked `ai_areas` and operational aliases.
2. Country research personalities in `common/ai_focuses`.
3. Dedicated country AI strategies for GER/SOV/ENG/USA/JAP/ITA/FRA/CHI.
4. Historical strategy plans with historical-only lifecycle and dependency-safe focus queues.
5. National 30-width AI division-template families for all eight primary countries.
6. Major-country naval goals, task-force/fleet templates and VNR naval-production integration.
7. Soviet Second and Third Five-Year Plan AI mission fallbacks.
8. Existing AI compensation policy: free equipment-design cost where retained, plus the confirmed production-line/command-power compensation already used by HER. Do not add blanket combat or attrition cheats for this baseline.

## Soviet Five-Year Plan validation

### Second Five-Year Plan

At completion verify:

- Azovstal project completed.
- Zaporozhstal project completed.
- Ural heavy-industry project completed.
- Donbass heavy-industry project completed.
- Chelyabinsk/ChTZ project completed.
- DneproGES project completed.
- `SOV_finish_the_second_five_year_plan` completed.
- Final macro mission does not fail solely because AI narrowly misses the civilian-factory threshold after completing the real industrial projects.

### Third Five-Year Plan

The current HER decision file contains two Third Five-Year Plan construction missions and both are covered by AI fallbacks:

- Ural Aluminium Plant — original deadline 640 days; AI fallback matures at 520 days.
- Kazan Aircraft Plant No. 124 — original deadline 720 days; AI fallback matures at 600 days.

Verify both mission flags/rewards fire normally rather than merely seeing the fallback buildings appear.

## Mandatory checkpoints

Record the world at:

- 1937-01-01
- 1938-01-01
- 1939-09-01
- 1941-06-22
- 1942-01-01
- 1943-01-01

If historical wars occur on different dates, also record immediately before and roughly 30 days after the relevant war begins.

## Country metrics at every checkpoint

For each primary major record:

- civilian factories;
- military factories;
- dockyards;
- current construction queue and obvious overbuilding/slot waste;
- manpower and conscription law;
- deployed divisions by major role where practical;
- division-template convergence (especially obsolete/understrength templates);
- stockpile deficits/surpluses for infantry equipment, artillery, heavy artillery, AT, AA, motorized, armor and aircraft;
- aircraft totals by main role;
- active production lines and factory allocations;
- researched technologies / obvious research-family distortion;
- current and recently completed national focuses;
- political/economic laws and obvious PP deadlocks;
- fuel state;
- surrender progress and casualties once at war.

## Land-war checks

### GER

- Poland is attacked and defeated without a major timing deadlock.
- Western campaign proceeds through the intended 1940 logic rather than stalling on an unavailable focus.
- Barbarossa preparation chain completes.
- Germany concentrates meaningful force against SOV instead of bleeding divisions into irrelevant theaters.
- Winter pause / 1942 southern phase / later sustainable eastern-war phases actually switch when their triggers are met.

### SOV

- Industrial plans complete without mission failure.
- Pre-Barbarossa buildup does not strand the bulk of the army in the Far East or irrelevant borders.
- 1941 opening is defensive rather than constant suicidal counterattacking.
- Moscow/Leningrad/Ukraine and later southern priorities receive sensible force allocation.
- Wartime emergency focus chain unlocks and executes.
- Tank/motorized templates appear without bankrupting basic infantry equipment.

### FRA / ENG

- France does not empty the Maginot line or commit its whole army to a bad Dyle posture.
- UK does not feed the bulk of its army into doomed Benelux fronts.
- UK preserves Home Defence and Suez while still sending a limited useful expeditionary force.

### CHI / JAP

- China maintains a coherent defensive front and does not destroy its army through impossible offensive behavior.
- Japan prosecutes the China war and later reaches the Southern Operation chain.
- Southern/Pacific priorities activate around the intended historical phase rather than from an impossible date condition.

### ITA / USA

- Italy prioritizes Mediterranean/North Africa and does not dump an excessive share of its army onto the Eastern Front.
- USA mobilizes before becoming a major combat participant and transitions into both Europe and Pacific operations after entry.

## Naval checks

Use `imgui show ai_navy` whenever a major fleet appears passive.

Record at minimum:

- ENG convoy losses and whether escort/patrol response grows when submarine pressure rises;
- number of active ENG convoy-escort task forces;
- GER submarine groups at sea versus sitting in port;
- GER submarine losses;
- USA/JAP strike forces and patrol groups active in the Pacific;
- major US/Japanese naval battles and invasion-support activity;
- ITA capital ships active in the Mediterranean versus sitting in port;
- fuel and repair state whenever a fleet refuses to sortie.

Do not tune NAI values merely because a fleet is in port. Diagnose in this order: objective -> task-force composition -> reserve -> repair -> fuel -> only then global NAI.

## Parser / runtime failure rules

Any parser error referencing the following files is a Test-1 blocker and should be fixed before interpreting balance results:

- `common/ai_areas/*`
- `common/ai_focuses/*`
- `common/ai_strategy/*`
- `common/ai_strategy_plans/*`
- `common/ai_templates/*`
- `common/ai_navy/*`
- `common/decisions/HER_SOV_fyp_ai*.txt`
- `events/HER_AI.txt`

Likewise treat these as blockers rather than balance outcomes:

- historical focus plan stuck indefinitely on an impossible prerequisite;
- AI repeatedly selecting an invalid/nonexistent template role;
- mass equipment starvation caused by a template parser/role problem;
- navy unable to assemble any valid task force despite having ships;
- Soviet FYP mission failure caused by the helper decision itself not activating.

## What NOT to change before Test 1

- Do not add blanket attack/defense bonuses.
- Do not restore old free-division/free-tech AI events.
- Do not add huge attrition reductions.
- Do not globally increase production efficiency growth to hide bad production switching.
- Do not activate the proposed naval NAI changes before observing the scripted baseline.
- Do not rebalance dozens of weights from screenshots taken at one date; identify the responsible layer first.

## Test-1 exit criteria

Test 1 is successful as a diagnostic run if:

1. the game reaches 1943 without an AI-script parser/runtime blocker;
2. all eight majors follow broadly recognizable historical strategic phases;
3. SOV completes both Five-Year Plan systems without AI-only mission deadlock;
4. major armies converge toward valid national templates without catastrophic universal equipment starvation;
5. the Atlantic and Pacific naval AIs generate visible operational activity;
6. the collected checkpoint data is sufficient to distinguish production, research, template, front-allocation and naval problems.

The next code pass should be based on failures observed in this run, not on additional speculative weighting.
