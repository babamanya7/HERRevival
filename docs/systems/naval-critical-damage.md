# Naval critical damage system

Status: implementation baseline. Probability and raw-damage defines are not balanced yet.

The system uses a dedicated 35-frame horizontal icon atlas at
`gfx/interface/navalcombat/HER_critical_damage_icons.dds`. Every critical part
has its own frame; no two critical IDs intentionally share an icon.

## Design rule

Normal hits should primarily cause limited STR/ORG damage. Mission kills, loss of combat capability and catastrophic losses should primarily come from critical damage to specific systems.

Critical parts are split into two layers:

- sub-unit criticals represent ship-wide casualties which do not depend on a fitted module;
- module criticals represent local casualties to installed equipment and scale their available damage instances with the fitted modules.

`base_damage_instance`, `damage_instance_per_added_module` and `max_damage_instance` are explicit on all newly introduced criticals. Hull-wide casualties are capped at one instance. Repeated local weapon casualties can scale with the number of installed mounts.

## Hull-wide criticals

Surface ships receive bridge damage, electrical failure, severe flooding, magazine explosion, fire, propeller damage and rudder damage. Aircraft carriers additionally retain the volatile-gas casualty. Submarines use electrical failure, pressure-hull rupture, magazine explosion, fire, propeller/rudder damage, ballast failure and gas leakage.

## Module zones

| Module family | Critical zones |
|---|---|
| Main/light/secondary batteries | Local battery damage; magazine explosion remains hull-wide |
| Anti-aircraft weapons | Disabled AA mounts |
| Torpedo tubes and computers | Damaged tubes; damaged torpedo fire control |
| Depth charges | Damaged depth-charge racks |
| Mine warfare equipment | Damaged laying/sweeping gear |
| Engines | Damaged engine room |
| Armor and armor scheme | Breached armor belt |
| Torpedo protection | Severe flooding |
| Radar and mast | Damaged radar |
| Sonar | Damaged sonar |
| Submarine pressure hull | Pressure-hull rupture |
| Periscope and snorkel | Damaged periscope; damaged snorkel |
| Missile weapons | Damaged missile launchers |
| Shipborne aviation facilities | Damaged aviation facilities |
| Carrier deck space | Aircraft elevator damage; hangar fire; aviation-fuel fire |
| Flight deck | Separate wooden and armored flight-deck profiles |
| Carrier air-control unit | Flight operations disrupted |
| Carrier damage-control unit | Damage-control center hit |
| Carrier fuel storage | Fuel-tank rupture; aviation-fuel fire |

Role modules are deliberately excluded: they classify a design and do not represent a physical compartment which can be hit.

## Carrier profile

Carrier damage is intended to produce a mission kill before sinking the hull. Flight-deck damage, elevator damage and disrupted flight control reduce effective carrier capacity; hangar and aviation-fuel fires combine capacity loss with substantial ORG/STR damage. Wooden and armored flight decks remain separate critical parts so their chance and severity can be balanced independently.

## Next balance pass

1. Test the effective critical pool by class and representative 1936/1940/1944 designs.
2. Tune artillery, torpedo and carrier-air critical chances with reliability and armor/piercing interactions.
3. Tune critical severity and repair duration.
4. Reduce ordinary non-critical STR damage only after the critical model is producing plausible mission kills.
5. Balance repair time and operational absence from the campaign.

Do not grant aircraft extra target weight against ships merely because they are already damaged.
