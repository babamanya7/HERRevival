# HER tactics unlock & counter matrix audit

Status: **IN PROGRESS**

This appendix records tactic unlock sources and direct counter relationships from the current HER code. It is intentionally separated from numerical balance changes.

## 1. Doctrine unlock model

`CONFIRMED-HER`: doctrine technologies use both `enable_tactic = tactic_*` and an `on_research_complete` hidden `unlock_tactic = tactic_*`. This duplicated pattern is widespread and appears intentional/legacy-safe. Do not remove one side casually until engine behavior is verified.

## 2. Mobile Warfare / GER tactical progression

Current GER-gated doctrine starts with `mobile_warfare` and builds a recognizable progression:

- `mobile_warfare` -> `tactic_unexpected_thrust`
- `delay` -> `tactic_delay`
- `elastic_defence` -> `tactic_elastic_defense`
- `armored_spearhead` -> `tactic_blitz`
- `schwerpunk` -> `tactic_barrage`
- `blitzkrieg` -> `tactic_breakthrough`
- `firebrigades` -> `tactic_overwhelming_fire`
- `backhand_blow` -> `tactic_backhand_blow`
- late Volksturm/Werwolf branch -> `tactic_guerrilla_tactics`

Interpretation: this is not simply an offensive tree. It gives GER early access to maneuver attack, delay, elastic defense, blitz/breakthrough, artillery concentration and later mobile defensive responses.

Important design note: `firebrigades` is additionally gated by `GER_refinement_of_bewegungskrieg`, so some late tactical access depends on focus progression as well as XP doctrine spending.

## 3. Superior Firepower tactical progression

Current Superior Firepower is barred to SOV and GER and acts as the generic artillery/combined-arms school for other countries.

Verified unlocks include:

- `sup_delay` -> `tactic_delay`
- `mobile_defence` -> `tactic_elastic_defense`
- `overwhelming_firepower` -> `tactic_overwhelming_fire`
- `sup_mechanized_offensive` -> `tactic_blitz`
- `shock_and_awe` -> `tactic_breakthrough`

This means the tree is not tactically static. It can eventually gain the same broad mobile/rupture vocabulary as Mobile Warfare, but later and through different doctrinal investments.

Preliminary concern: tactic identity must come from unlock timing + composition/weight conditions, not merely exclusive ownership, because several high-end tactics are intentionally shared across trees.

## 4. Grand Battleplan tactical progression

Verified unlocks include:

- `prepared_defense` -> `tactic_planned_defense`
- `grand_assault` -> `tactic_planned_attack`
- `grand_mechanized_offensive` -> `tactic_blitz`
- `attritional_containment` -> `tactic_delay`

This gives GBP a strong set-piece identity: prepared defense -> planned attack -> mechanized exploitation, with delay available in the later positional/infiltration side.

The current architecture supports the intended distinction that GBP should be best at preparation/coherence rather than being permanently barred from mobile exploitation.

## 5. Mass Assault / SOV tactical progression

Current Mass Assault is SOV-gated and contains two doctrinal concepts inside one tree.

Deep-operations side verified unlocks:

- `deep_operations` -> `tactic_blitz`
- `operational_concentration` -> `tactic_barrage`
- `vast_offensives` -> `tactic_overwhelming_fire`
- `breakthrough_priority` -> `tactic_breakthrough`
- `continuous_offensive` -> `tactic_backhand_blow`
- `masterful_blitz` -> `tactic_masterful_blitz`

People's-army side verified unlocks:

- `peoples_army` -> `tactic_human_wave_tactics`
- `large_front_offensive` -> `tactic_relentless_assault`
- `guerilla_warfare` -> `tactic_elastic_defense`

Important interpretation: mature SOV doctrine is already coded as a progression away from simple mass infantry attack toward artillery concentration, breakthrough, exploitation, operational continuity and sophisticated defensive reaction. This strongly argues against evaluating the SOV tree as "Human Wave doctrine" based on one tactic name.

## 6. Direct counter matrix — verified current relationships

### Normal-phase attacker tactics

- `tactic_basic_attack` <- countered by `tactic_counterattack`
- `tactic_encirclement` <- `tactic_tactical_withdrawal`
- `tactic_shock` <- `tactic_ambush`
- `tactic_breakthrough` <- `tactic_backhand_blow`
- `tactic_blitz` <- `tactic_elastic_defense`
- `tactic_human_wave_tactics` <- `tactic_planned_defense`
- `tactic_banzai_charge` <- `tactic_overwhelming_fire`
- `tactic_flank_attack` <- `tactic_planned_defense`

No direct `countered_by` was observed in the audited definitions for:
- `tactic_infantry_charge`
- `tactic_planned_attack`
- `tactic_relentless_assault`
- `tactic_unexpected_thrust`
- `tactic_barrage` (a commented placeholder for a future German anti-Soviet artillery response exists)
- `tactic_masterful_blitz`

This asymmetry is a major audit point. A tactic without a direct counter is not automatically overpowered because selection weights, phase constraints and raw effects still matter, but it is structurally less vulnerable to the initiative/counter system.

### Normal-phase defender tactics

- `tactic_basic_defend` <- `tactic_breakthrough`
- `tactic_counterattack` <- `tactic_barrage`
- `tactic_delay` <- `tactic_shock`
- `tactic_ambush` <- `tactic_breakthrough`

Other defensive tactics are primarily themselves counters to attacker actions rather than being recursively countered.

### Tactical Withdrawal phase

- `tactic_tw_evade` <- `tactic_tw_intercept`

This creates a clean chase/escape mini-game rather than a generic stat exchange.

### Street Fighting phase

- `tactic_sf_fortify` <- `tactic_sf_mouse_holing`
- `tactic_sf_ambush` <- `tactic_sf_mouse_holing`

This is a good equipment/formation-driven counter model: assault engineers can open a tactic that directly defeats specific urban defensive methods.

### Bridge phases

Verified examples:
- `tactic_defender_sb_retake_bridge` <- `tactic_attacker_sb_skillful_defence`
- `tactic_attacker_hb_storm` <- `tactic_defender_hb_skillful_defence`
- `tactic_attacker_hb_take_bridge` <- `tactic_defender_hb_skillful_defence`

Bridge-phase signs/effects still require technical validation before balance conclusions.

## 7. High-priority structural findings

### A. Masterful Blitz currently lacks the ordinary Blitz counter

`CONFIRMED-HER`: `tactic_blitz` is directly countered by `tactic_elastic_defense`; the audited `tactic_masterful_blitz` definition has no `countered_by` line.

This may be intentional, but it is a high-priority review item because `masterful_blitz` replaces regular Blitz for SOV after the doctrine tech. If intentional, the reason should be explicit: e.g. mature Soviet exploitation is meant to be harder to tactically neutralize. If not intentional, it is a legacy omission.

Do not add a counter until the full initiative/selection math and late-war GER/SOV matchup are tested.

### B. Barrage has a commented future counter concept

The code contains a commented placeholder:

`#countered_by = tactic_back_hop #german 1944 antisoviet artillery tactic`

This is useful design archaeology. It indicates an earlier intention to model a late-war German response to Soviet artillery preparation, but the tactic is not currently implemented in the active counter network.

Do not revive it automatically; first determine whether the intended behavior is better represented through prepared defense, withdrawal from forward positions, counter-battery fire, elastic defense or another existing mechanism.

### C. Shared tactics are a feature, not necessarily a loss of doctrine identity

`Blitz`, `Breakthrough`, `Delay`, `Elastic Defense`, `Barrage`, and `Overwhelming Fire` can occur in multiple doctrinal trees.

Doctrine differentiation therefore comes from:
- **when** the tactic unlocks;
- which other tactics compete in the same pool;
- formation requirements and weight modifiers;
- commander skill/traits;
- country/focus gating;
- supporting division stats and logistics.

The audit should not force artificial exclusivity merely to make each tree visually distinct.

## 8. Next checks

1. Verify every remaining `enable_tactic` in `land_doctrine.txt` and produce an exhaustive tree-by-tree table.
2. Search focuses/events/ideas/traits for non-doctrine `unlock_tactic` effects.
3. Verify preferred-tactic assignments on generals/field marshals and any national preferred tactic effects.
4. Confirm exact current tactic initiative/counter selection behavior in HOI4 1.19/HER.
5. Build representative 1939 / 1941 / 1943 / 1945 tactic pools for GER and SOV.
6. Only after that decide whether missing counters (especially `masterful_blitz`) are design choices or omissions.
