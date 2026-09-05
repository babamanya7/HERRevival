# HER Mod — Air Designer Meta Build Audit

Status: IN PROGRESS

Purpose: test the current aircraft designer as an actual player-facing optimization problem rather than auditing modules in isolation. These builds are generic baseline constructions without national MIO/KB, focus or idea bonuses; country-specific meta can differ.

## Structural finding: too many non-competing special slots
The current SMALL airframe exposes six broad generic special slots (`special_type_slot_1..6`) plus a dedicated construction slot, gunsight slot and electronics slot. Many high-value survivability and engine-performance modules therefore do not compete with one another for scarce physical space.

This is an architectural source of no-brainer stacking. Even a module with a reasonable individual downside can become mandatory if it occupies a slot that has no equally valuable competing subsystem.

**Air Designer 2.0 requirement:** reduce generic universal slots and replace them with explicit physical subsystem/location slots. Protection, fuel, cockpit, induction, cooling, avionics, stores and structural choices should compete where they would compete physically.

## Generic 1939 fighter package
Practical baseline for an air major:
- improved small airframe is player-accessible from 1939 for most tags (SOV/USA delayed to 1940 by `allow`);
- engine IV is a 1938 technology and requires engine III + engine tuning III;
- heavy MG is a 1938 technology;
- survivability studies is a 1936 cost-1 technology and simultaneously unlocks self-sealing tanks, armour plate and automatic extinguisher for all frame sizes;
- engine tuning IV is 1939.

A highly optimized fighter therefore naturally wants:
- fighter role;
- strongest practical engine generation;
- heavy MG / cannon mix constrained by thrust and desired speed;
- self-sealing fuel tank if rubber is affordable;
- automatic extinguisher;
- one engine-performance module where available;
- gunsight where available;
- construction choice according to the current agility/defence meta;
- electronics/radio/radar as soon as the tech path makes it worthwhile.

The key result is not one exact weapon count but that survivability and performance subsystems can be stacked simultaneously with little slot competition.

## Generic 1941 fighter package
By 1941 the optimized fighter has access to a broader mandatory stack:
- improved small airframe;
- later engine generation/tuning;
- improved HMG/cannon progression;
- self-sealing tanks;
- extinguisher;
- engine enhancement (supercharger/turbocharger/fuel system depending unlocks and engine family);
- fighter gunsight;
- potentially pressurized cockpit;
- construction module;
- electronics/radar where available.

**Meta concern:** the player is not primarily choosing an aircraft philosophy; the player is increasingly filling every subsystem with the best unlocked upgrade. The designer becomes a checklist.

## Generic 1943 fighter package
Advanced small airframe itself has 64 agility, 14 defence and weight 3.5. It continues to expose the same broad special-slot architecture. By this stage, late guns, engine tuning, advanced induction/performance modules, pressurized cockpit, self-sealing tanks, extinguisher, construction module, improved sight and radar can all coexist.

This strongly rewards technology breadth and module stacking. The late-war design problem is therefore less "which architecture do I choose?" and more "how many best-in-slot technologies have I researched?"

## Generic CAS package
CAS has a more meaningful weapon tradeoff than fighters because bombs, rockets, tank-buster guns and bomb bays consume weapon locations and impose weight/drag. However its survivability/propulsion layer suffers from the same generic-slot stacking problem as fighters.

A typical optimized CAS wants:
- CAS role;
- strongest engine compatible with payload;
- best mission-appropriate payload (bombs/rockets/tank-buster depending target);
- self-sealing tanks where resources allow;
- extinguisher;
- armour plate where survivability is worth speed/range;
- dive brakes for dedicated dive/CAS use;
- CAS gunsight / air-ground radar as available;
- engine-performance module(s);
- reinforced/lightweight construction according to meta.

CAS therefore has a healthy payload-design core but an unhealthy universal-upgrade shell around it.

## Fighter-bomber comparison
Current fighter-bomber payloads often duplicate CAS ground-attack/weight values while carrying weaker or commented-out aerodynamic penalties, with the role applying a blanket CAS ground-attack penalty. This creates a role distinction through arithmetic rather than construction.

Air Designer 2.0 should instead force fighter-bombers to trade fighter performance for external stores/payload capacity physically, while dedicated CAS receives superior payload density, attack equipment and survivability/low-altitude options.

## No-brainer candidates
High-priority modules/systems for redesign rather than simple numerical nerf:
1. self-sealing fuel tanks — ordinary tank is largely superseded when rubber is affordable;
2. automatic extinguisher — very efficient defence + reliability package;
3. pressurized cockpit — broad range/reliability plus large mission agility benefit, insufficient physical cost;
4. generic engine-performance modules — individually sensible but can stack because they occupy broad slots;
5. lightweight/reinforced construction — abstract mirrored quality slider rather than physical construction;
6. gunsight/radar progression — healthy mission-specific effects, but should occupy explicit avionics/sight capacity rather than being free additions to an already full optimal stack.

## Design conclusion
The core problem is not merely overtuned values. It is insufficient exclusivity.

Current pattern:
`airframe + many generic special slots -> install every good subsystem`

Target Air Designer 2.0 pattern:
`airframe skeleton -> choose layout/capacity -> subsystems compete for physical locations, mass, drag, volume, power, crew workload, IC and resources`

A good late-war fighter should not automatically carry every available protection, range, high-altitude, engine-performance and electronics upgrade. Different historical aircraft families should emerge from incompatible or costly engineering choices, not from stacking all unlocked modules.

## Research burden observation
The generic air-major path also contains substantial hidden research tax. By 1939 a competitive fighter program already spans airframe, multiple engine generations, multiple tuning technologies, guns and survivability. By 1941-43 it adds further engine/tuning, weapons, sights/electronics and specialized modules. This reinforces the earlier conclusion that engine-generation + tuning density must be reviewed together with the designer redesign; reducing module stacking without reducing research tax could simply turn mandatory modules into mandatory research with fewer slots.
