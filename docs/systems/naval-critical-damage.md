# Naval critical damage system

Status: first integrated critical-probability and raw-damage defines baseline implemented; combat testing is still required.

The system uses a dedicated 41-frame horizontal icon atlas at
`gfx/interface/navalcombat/HER_critical_damage_icons.dds`. Every critical part
has its own frame; no two critical IDs intentionally share an icon.

## Design rule

Normal hits should primarily cause limited STR/ORG damage. Mission kills, loss of combat capability and catastrophic losses should primarily come from critical damage to specific systems.

Critical parts are split into two layers:

- sub-unit criticals represent ship-wide casualties which do not depend on a fitted module;
- module criticals represent local casualties to installed equipment and scale their available damage instances with the fitted modules.

`base_damage_instance`, `damage_instance_per_added_module` and `max_damage_instance` are explicit on all newly introduced criticals. Hull-wide casualties are capped at one instance. Repeated local weapon casualties can scale with the number of installed mounts.

## Hull-wide criticals

Surface ships receive bridge damage, electrical failure, severe flooding, magazine explosion, fire, propeller damage and rudder damage. Submarines use electrical failure, pressure-hull rupture, magazine explosion, fire, propeller/rudder damage, ballast failure and toxic gas leakage. Toxic gas leakage is submarine-only; carrier fuel vapors and volatile aviation fuel are represented by the separate aviation-fuel fire critical.

## Pre-defines severity scale

- Common local equipment casualties normally carry relative weights of `0.65-1.0` and remove roughly `30-60%` of the affected system.
- Ship-wide mission-kill casualties normally carry weights of `0.25-0.65` and combine moderate ORG/speed penalties with limited extra damage.
- Catastrophic casualties carry weights of `0.05-0.2`. Magazine explosion is capped at `x4` damage; aviation-fuel fire at `x2.25`; pressure-hull rupture at `x2` STR damage.
- Critical-hit damage multipliers below `1.0` are prohibited. A critical casualty must not reduce the damage of the hit which caused it.
- Carrier capacity penalties are deliberately cumulative: one local casualty degrades operations, while several simultaneous deck/elevator/hangar/control casualties can create a full mission kill.
- Wooden and armored flight decks use opposite risk profiles. A wooden deck has a high critical weight but a relatively light direct operational penalty because local holes can be patched at sea. An armored deck has a much lower critical weight, but a successful penetration or structural deformation causes a severe mission kill and additional repair damage.

## Defines baseline

The first integrated balance pass deliberately leaves base gun accuracy unchanged so hit frequency and hit consequence can be tested separately.

| Define | Previous | Baseline | Purpose |
|---|---:|---:|---|
| `COMBAT_DAMAGE_TO_STR_FACTOR` | 0.80 | 0.50 | Ordinary surface hits remove less hull strength |
| `COMBAT_DAMAGE_TO_ORG_FACTOR` | 1.20 | 0.90 | Ordinary hits still disrupt without deciding the battle alone |
| `COMBAT_BASE_CRITICAL_CHANCE` | 0.07 | 0.10 | System casualties become the main route to mission kills |
| `COMBAT_CRITICAL_DAMAGE_MULT` | 4.00 | 2.00 | Avoid a universal damage explosion before the selected critical part applies its own severity |
| `COMBAT_TORPEDO_CRITICAL_CHANCE` | 0.10 | 0.15 | Torpedoes more often cause flooding and machinery casualties |
| `COMBAT_TORPEDO_CRITICAL_DAMAGE_MULT` | 2.00 | 1.50 | Torpedo lethality shifts toward critical effects rather than universal raw damage |
| `CHANCE_TO_DAMAGE_PART_ON_CRITICAL_HIT` | 0.10 | 0.65 | Most surface criticals now damage a defined ship system |
| `CHANCE_TO_DAMAGE_PART_ON_CRITICAL_HIT_FROM_AIR` | 0.10 | 0.80 | Air hits strongly favor deck, hangar and internal-system casualties |
| `NAVAL_STRIKE_DAMAGE_TO_STR` | 2.00 | 1.25 | Limits direct aircraft STR deletion |
| `NAVAL_STRIKE_DAMAGE_TO_ORG` | 2.00 | 1.75 | Aircraft remain strong at operational disruption |

With these values, a critical is no longer synonymous with an automatic universal `x4` damage spike. The global multiplier is moderate, while magazine explosions, aviation-fuel fires, pressure-hull ruptures and other selected critical parts provide their own differentiated multipliers and fixed damage.

## Module zones

| Module family | Critical zones |
|---|---|
| Main/light/secondary batteries | Local battery damage; magazine explosion remains hull-wide |
| Anti-aircraft weapons | Disabled AA mounts |
| Torpedo tubes and computers | Damaged tubes; damaged torpedo fire control; rare torpedo-warhead detonation |
| Depth charges | Damaged depth-charge racks |
| Mine warfare equipment | Damaged laying/sweeping gear |
| Engines | Damaged engine room; carriers additionally risk loss of wind-over-deck capability through carrier propulsion failure |
| Armor and armor scheme | Breached armor belt |
| Torpedo protection | Severe flooding |
| Radar and mast | Damaged radar |
| Sonar | Damaged sonar |
| Submarine pressure hull | Pressure-hull rupture |
| Periscope and snorkel | Damaged periscope; damaged snorkel |
| Missile weapons | Damaged missile launchers |
| Shipborne aviation facilities | Damaged aviation facilities |
| Carrier deck space | Aircraft elevator and arresting-gear damage; hangar fire; aviation-fuel fire; armed-aircraft detonation |
| Flight deck | Separate wooden and armored flight-deck profiles; arresting-gear damage |
| Carrier air-control unit | Flight operations disrupted |
| Carrier damage-control unit | Damage-control center hit |
| Carrier fuel storage | Fuel-tank rupture; aviation-fuel fire |

Role modules are deliberately excluded: they classify a design and do not represent a physical compartment which can be hit.

## Carrier profile

Carrier damage is intended to produce a mission kill before sinking the hull. Flight-deck, elevator, arresting-gear, propulsion and air-control casualties reduce effective carrier capacity; hangar, aviation-fuel and armed-aircraft fires combine capacity loss with substantial ORG/STR damage. Wooden deck damage is common but comparatively repairable. Armored deck damage is rare but severe and represents structural work that cannot be improvised at sea.

The Midway and Solomon carrier cases establish the cumulative model: a local wooden-deck hole is not automatically a mission kill, two disabled elevators do not automatically disable every remaining flight operation, and a carrier may retain speed while its air group is disabled. Conversely, propulsion damage can stop fully fueled and armed launches even when the deck itself is intact. Fires become catastrophic through fuel, ready ordnance, ventilation, electrical distribution and failed damage-control organization rather than through an automatic sinking result.

Ship-wide ventilation failure and disrupted damage-control parties are available to all surface combatants. These casualties primarily reduce ORG, morale and reliability, allowing later flooding, fire and machinery damage to become harder to contain without turning the initial hit into excessive direct STR damage.

## Next balance pass

1. Test the effective critical pool by class and representative 1936/1940/1944 designs.
2. Measure criticals per 100 gun, torpedo and air hits across representative reliability values.
3. Tune artillery, torpedo and carrier-air critical chances with armor/piercing interactions.
4. Tune critical severity and repair duration.
5. Balance damage-control technologies and total critical-risk reduction only after the baseline frequency is measured.
6. Balance repair time and operational absence from the campaign.

Do not grant aircraft extra target weight against ships merely because they are already damaged.
