# HER AI Navy Rework

Status: IN PROGRESS / SECOND IMPLEMENTATION PASS
Branch: `AI-rework`
Started: 2026-09-06

## Goals

The naval AI must be an active operational opponent rather than a fleet-in-being that mostly sits in port.

Primary gameplay targets:

- ENG must protect Atlantic and imperial supply routes well enough that German submarines cannot erase British shipping unopposed.
- GER should remain a serious submarine-raiding threat and force the Allies to spend escorts, patrols, aircraft and research on ASW.
- USA and JAP should actively contest the Pacific with patrols, strike forces, invasion support, convoy protection and island defense.
- ITA should contest the Mediterranean rather than preserving the Regia Marina indefinitely in port.
- FRA should use its fleet defensively and for trade-route protection without sacrificing the continental war.
- SOV should defend coasts and limited sea lanes without over-investing in blue-water operations.

## How goal-based naval AI works

HER contains the newer goal-based naval AI system in `common/ai_navy`.

A **goal** is a high-level naval purpose, such as convoy protection or invasion support. The engine generates concrete **objectives** for specific routes, invasions, coasts or regions. Each objective receives a score between the goal's `min_priority` and `max_priority` according to objective importance. Objectives from all goals are then sorted together, and the AI attempts to execute the highest-scoring objectives first.

Current HER documentation explicitly lists goal/objective scripting and the `imgui show ai_navy` debug interface.

Working HER files additionally use objective types that are not listed in the short bundled documentation, including `naval_dominance`, `mines_planting`, `training` and `naval_blockade`. These are retained because they already exist in the working HER goal file; new major profiles only use existing HER objective tokens.

## Critical pre-rework bug

`common/ai_navy/goals/goals_generic.txt` blocked the following countries from every generic naval goal:

`ENG FRA GER ITA JAP SOV USA`

No country-specific goal files existed in HER.

Therefore the seven main naval powers were explicitly excluded from the only scripted naval-goal definitions in the mod. This is a major candidate explanation for passive naval behavior and fleets remaining in port: minors had goal-based naval objectives, while the majors had no replacement goal set in this folder.

CHI was not blocked and continues to use the generic goal set because it is not intended to operate as a major blue-water naval power in this AI pass.

## World Ablaze comparison

World Ablaze uses the same goal-based architecture but does **not** block the majors from its generic goals. Its priorities also show several useful patterns:

- invasion defense is much more important than in old HER (`15-25` in WA);
- convoy protection is higher (`3-10` instead of HER generic `1-5`);
- naval dominance starts higher (`4-13` instead of `1-13`);
- its task-force definitions have actual minimum compositions rather than leaving most minima empty;
- submarine raiding uses small operational groups (minimum 3, optimal 5), encouraging more simultaneous raiding task forces;
- escort fleets can scale to many task forces instead of stopping after only a few groups.

HER adopts these structural lessons but uses country-specific goal priorities rather than copying WA numbers globally.

## Implemented major naval-goal profiles

New file: `common/ai_navy/goals/goals_majors.txt`.

### ENG

Highest priority is convoy protection (`18-32`), followed by invasion defense (`15-28`). Naval dominance, coast defense and invasion support are meaningful but lower. This is intended to force the Royal Navy to respond to submarine pressure instead of allowing Atlantic routes to collapse while the battlefleet remains idle.

### USA

Naval dominance (`12-25`) and invasion support (`14-28`) are the central goals, with strong convoy protection (`10-22`). This should make the US Navy an offensive Pacific actor and support actual island-hopping rather than merely accumulating ships.

### JAP

Naval dominance and invasion support are both very high (`14-28`), with significant convoy raiding (`7-16`) and route protection (`9-18`). Japan is intended to seek initiative early rather than preserve the Combined Fleet indefinitely.

### GER

Convoy raiding is dominant (`15-30`). Coast/invasion defense and limited convoy protection remain meaningful, while blue-water dominance is deliberately secondary. Germany should force an Atlantic ASW response without behaving like a substitute Royal Navy.

### ITA

Mediterranean naval dominance (`10-22`), convoy protection (`10-20`) and invasion defense (`12-22`) are all high. Italy should actively contest sea control and protect North African logistics instead of keeping most capital ships parked.

### FRA

Convoy protection and invasion/coast defense dominate. Naval dominance remains useful but below the immediate defensive requirements of France and its empire.

### SOV

Coastal and invasion defense dominate. Convoy protection is moderate and blue-water dominance limited. This avoids wasting Soviet naval strength while still making Baltic/Black Sea/Northern Fleet assets operationally useful.

## Fleet-template changes

Old `generic_dominance_fleet_1` required:

- one strike force;
- two CA dominance patrols;
- one BC dominance patrol;
- two recon patrols.

That structure could make creation of a dominance fleet unnecessarily dependent on scarce cruiser/battlecruiser task forces.

New required core:

- one `StrikeForce_1`;
- two `PatrolReconForce_1`.

Heavier CA/BC patrols are now optional. This gives the AI a cheaper functional patrol/strike network and lets additional forces scale as ships become available.

Raiding fleets now allow up to six optional submarine groups plus a surface raider, instead of only two extra submarine groups. Escort fleets likewise allow up to six optional escort task forces. This is specifically intended to scale British/US route protection and German/Japanese raiding across multiple sea zones.

## Task-force changes

The old HER task-force templates had almost all `min_composition` blocks commented out. A one-ship or badly composed group could therefore satisfy a template and reserve/assignment behavior was poorly constrained.

The first rework pass adds real minimums and raises active mission preference:

- strike force: minimum 1 battleship + 6 destroyers; optimal 2 CV / 2 BB / 3 CA / 4 CL / 16 DD;
- recon patrol: minimum 1 CL + 2 DD, optimal 2 CL + 4 DD;
- CA patrol: minimum 1 CA + 4 DD;
- BC patrol: minimum 1 BC + 6 DD;
- submarine raiding: minimum 3 SS, optimal 6 SS;
- convoy escort: minimum 4 DD, optimal 12 DD + 2 CL;
- minelaying: minimum 2 role-4 DD.

`ai_will_do` was raised for patrol, escort and submarine-raiding templates so that the AI has more viable active task forces available to satisfy naval goals.

## Naval-production / ai_strategy audit

The next pass exposed a second major integration problem.

`common/ai_strategy/naval_production.txt` uses the HER/VNR naval production roles (`vnr_naval_screen`, `vnr_naval_submarine`, `vnr_naval_carrier`, etc.) and contains substantial country-specific production plans. For example, wartime ENG already asks for a large screen ratio, GER strongly pivots to submarines against ENG, while USA/JAP receive large wartime screen/carrier targets.

However several older naval strategies in `common/ai_strategy/ENG.txt` still used vanilla role IDs such as `naval_screen`, `naval_escort`, `naval_carrier`, `naval_submarine`, etc. At the same time `naval_production.txt` contains `no_old_navy_production`, which applies `-10000` to those old vanilla naval production roles when Man the Guns is active.

That means important older British helper strategies were effectively disconnected from the VNR production system. The clearest example was the existing `EAI_ENG_focus_on_screens`/historical/anti-submarine logic: it attempted to manipulate old `naval_*` role IDs while current HER ship designs are produced through `vnr_naval_*` roles.

The VNR destroyer screen design itself is suitable for ASW: current 1936+ screen designs contain sonar and depth charges. The main problem was therefore not the absence of an ASW-capable hull, but getting the AI to build and deploy enough of those ships when the submarine war becomes serious.

## Implemented naval strategy bridge

New file: `common/ai_strategy/HER_naval_rework_strategies.txt`.

### British pre-war escort buildup

From mid-1937 until the expected outbreak of the European war, ENG receives an extra VNR screen/light-cruiser bias and a higher convoy target. This is intentionally additive to the existing `naval_production.txt` plan rather than replacing it.

### Dynamic Battle of the Atlantic response

The existing working scripted trigger `anti_submarine_strategy_required_trigger` is reused rather than inventing a new submarine-threat detector.

When that trigger fires, ENG now shifts strongly toward:

- `vnr_naval_screen`;
- `vnr_naval_cruiser_light`;
- convoy replacement.

At the same time submarine, battleship and carrier pressure is reduced. The block also requests a minimum convoy production allocation so a badly damaged merchant fleet does not enter a permanent death spiral while every dockyard continues building prestige combatants.

A lighter always-on ENG-vs-GER screen bias sits underneath the emergency block, so the Royal Navy does not wait until catastrophic losses before caring about escorts.

### Pacific activity bridge

When USA and JAP are directly at war, both receive additional carrier/screen production pressure, `naval_invasion_focus`, and `pacific_front` area priority.

This is intended to bridge the gap between the high-scoring naval goals and the land/invasion planner: the goal system can support an invasion only if the broader AI is actually interested in planning Pacific operations.

It does not force specific historical island captures yet. Detailed island sequencing belongs in the main USA/JAP `ai_strategy` pass so it can be tested together with their existing invasion scripts.

## NAI activity overrides

New file: `common/defines/zz_HER_AI_navy.lua`.

Only two narrow overrides were added in this pass:

- `AI_TASKFORCE_REQUIRED_RESERVE_RATIO`: `0.20 -> 0.10`;
- `NAVAL_MISSION_AGGRESSIVE_ESCORT_DIVISOR`: `2.0 -> 1.25`.

The first reduces the share of each required task-force composition that the AI withholds as reinforcement reserve, releasing more actual ships for operational groups. This directly addresses the observed tendency to keep usable ships parked while objectives are unfulfilled.

The second reduces the scoring penalty applied to escort activity when the AI is not in a purely defensive posture. It is deliberately not set below `1.0`: convoy protection should become easier to justify without turning the entire navy into suicidal permanent escort patrols.

Other danger, repair, fuel and sortie thresholds remain unchanged for now. This preserves the ability to diagnose whether future passivity is caused by objective scoring, fleet assembly, fuel/repair state or danger evaluation rather than changing every naval threshold simultaneously.

## Known deferred bugs / next naval-linked work

- `common/ai_strategy/JAP.txt` contains an impossible first Southern Expansion window: `date > 1942.12.15` together with `date < 1942.1.1`. This must be corrected in the JAP strategy pass.
- The existing ENG file still contains obsolete vanilla `naval_*` role-ratio blocks. The new HER bridge makes the needed behavior functional immediately, but the dead old blocks should be removed/converted during the full `ai_strategy` cleanup rather than left as permanent technical debt.
- USA/JAP Pacific area/invasion priorities need a proper operational sequence after the generic strategy audit, not just a permanent high Pacific weight.

## Required hands-off naval metrics

For integrated testing record at minimum:

- UK convoys and escorts lost per month to GER submarines;
- number of active ENG convoy-escort task forces and escorted Atlantic routes;
- whether `anti_submarine_strategy_required_trigger` activates at a sensible loss/threat level;
- GER submarine groups at sea vs in port and submarine losses;
- USA/JAP strike forces and patrol groups active in the Pacific;
- number and location of major US/Japanese naval battles;
- invasion-support objectives actually fulfilled;
- ITA capital ships active in the Mediterranean vs sitting in port;
- fuel state and repair state when a major fleet refuses to sortie.

Target is not zero convoy losses or constant suicidal sorties. The target is visible reaction: raiding creates escort/patrol pressure, fleets contest strategically important seas, and the Pacific produces repeated operational contact without immediately annihilating one side through obvious AI misuse.

Debug procedure when a fleet still sits in port:

1. `imgui show ai_navy`: confirm there is a high-scoring objective.
2. Confirm the relevant fleet/task-force template can actually be assembled.
3. Check reserve, repair and fuel state.
4. Only then adjust further NAI danger/fuel/repair thresholds.
