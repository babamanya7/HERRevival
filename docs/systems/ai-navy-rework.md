# HER AI Navy Rework

Status: IN PROGRESS / FIRST IMPLEMENTATION PASS
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

## Important caveat: aggression and port behavior

`common/ai_navy` determines what naval objectives exist and what fleets/task forces are built to execute them. It does **not** contain every engine threshold controlling when the AI is willing to sortie, how much reserve it keeps, fuel thresholds, repair behavior or danger tolerance.

HER already has naval AI-related NAI defines such as reserve-ratio and peacetime fuel controls. Those are intentionally deferred until the later NAI pass. Do not compensate for missing goals by immediately making global sortie/danger thresholds extreme; first hands-off test the restored major goals and task-force structure.

If major fleets still sit in port while high-scoring objectives are unfulfilled, use `imgui show ai_navy` to distinguish:

1. no/low-scoring objective;
2. objective exists but no valid fleet/task force can be assembled;
3. fleet exists but NAI fuel/reserve/repair/danger logic refuses execution.

Only case 3 should be solved primarily through NAI defines.

## Required hands-off naval metrics

For integrated testing record at minimum:

- UK convoys and escorts lost per month to GER submarines;
- number of active ENG convoy-escort task forces and escorted Atlantic routes;
- GER submarine groups at sea vs in port and submarine losses;
- USA/JAP strike forces and patrol groups active in the Pacific;
- number and location of major US/Japanese naval battles;
- invasion-support objectives actually fulfilled;
- ITA capital ships active in the Mediterranean vs sitting in port;
- fuel state and repair state when a major fleet refuses to sortie.

Target is not zero convoy losses or constant suicidal sorties. The target is visible reaction: raiding creates escort/patrol pressure, fleets contest strategically important seas, and the Pacific produces repeated operational contact without immediately annihilating one side through obvious AI misuse.
