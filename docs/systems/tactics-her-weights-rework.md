# HER combat tactics — commander-skill weight rework

Status: IMPLEMENTED, REQUIRES HANDS-OFF / COMBAT DEBUG VALIDATION

Implementation commits:
- `0d1077797309a6db66415a8e43c2493dca5254b6` — initial HER subskill weighting rework;
- `183f21882078ea8bc5abcf698442a8119ed43567` — merged commander-trait integration.

## 1. Reason for the rework

The previous tactic-selection model used doctrine unlocks, combat situation, overall commander `skill`, `skill_advantage`, reserves, frontage, composition and traits, but it barely read the four HER commander subskills.

That caused an important mismatch: HER deliberately gives commanders strongly differentiated profiles, but tactic selection largely flattened them back into one overall skill value plus traits. A high-skill armored attacker could therefore become too competent at advanced defensive choices even with a very low defensive subskill, while a staff/operational specialist's high Planning/Logistics values were almost invisible to tactic selection.

## 2. Confirmed engine syntax

HOI4 exposes the following valid unit-leader/combat trigger variables:

- `attack_skill_level`
- `defense_skill_level`
- `planning_skill_level`
- `logistics_skill_level`

These are used directly in tactic `base` weight modifiers.

## 3. HER semantic mapping

The tactic system follows the established HER interpretation of commander stats:

- `attack_skill_level` = mechanized / armored tactical competence;
- `defense_skill_level` = infantry / artillery tactical competence;
- `planning_skill_level` = operational planning and prepared execution;
- `logistics_skill_level` = initiative, flexibility and self-reliance.

This HER meaning is intentionally more specific than the vanilla localisation of the four subskills.

## 4. Architecture rule

Tactic selection is layered:

1. **Doctrine unlock** — whether the military institution knows the tactic at all.
2. **Combat situation** — composition, hardness, artillery concentration, frontage, reserves, terrain, flanking and phases determine whether the tactic makes sense.
3. **Professional traits** — actual branch/specialist experience may directly open or strongly weight relevant tactics.
4. **Personality traits** — primarily modify style through HER subskills; direct tactic weights stay small.
5. **Overall `skill` / `skill_advantage`** — general command quality and relative superiority.
6. **HER subskills** — steer which sophisticated tactic a commander prefers within the available pool.

Subskills deliberately use moderate, stepped additive weights. They are not meant to override doctrine, composition or reserves.

## 5. Main weighting changes

### Attack / maneuver group

`Encirclement`
- Planning and Logistics are primary commander-quality weights.
- Attack contributes for hard/mobile formations; Defense contributes lightly for soft formations.
- `mobile_warfare_leader` now directly opens the tactic; `mobile_warfare_officer` can open it with strong Logistics.
- Mobile-warfare traits add direct weight, but `trickster` remains a major stylistic signal.
- `skill_advantage` remains useful but no longer dominates through a long stack of equal bonuses.

`Breakthrough`
- Planning is central.
- Hard formations read Attack; soft/artillery-heavy formations read Defense.
- Reserves gained more importance.
- `mobile_warfare_leader` provides an additional mobile-formation access path but remains weaker than dedicated armored/artillery specialist signals.
- The old flat `inflexible_strategist = -4` weight penalty remains removed: inflexibility should not mean inability to conduct a deliberately prepared breakthrough.

`Blitz`
- Strongly reads Attack + Logistics, with a smaller Planning contribution.
- `mobile_warfare_officer` and `mobile_warfare_leader` are now valid access paths in addition to `panzer_leader` / `combined_arms_expert`.
- `mobile_warfare_leader` receives a stronger direct weight than the officer trait.
- `independent_minded` and `improviser` add small direct preference; `methodical` slightly reduces preference.
- This separates panzer specialists from motorized/mechanized mobile-warfare specialists without forcing both into the same trait.

`Masterful Blitz`
- Uses the same mobile-warfare professional chain as an access/weight source.
- Reads Attack + Logistics + Planning and still rewards reserves/full frontage.
- Its lack of a direct `countered_by` remains a separate architectural review item.

`Unexpected Thrust` / `Flank Attack`
- Logistics and Planning matter strongly because these represent rapid exploitation of local opportunities.
- `mobile_warfare_officer` / `mobile_warfare_leader` receive strong direct weights.
- `improviser` and `independent_minded` receive only small direct bonuses; most of their effect remains indirect through Logistics.
- `methodical` slightly reduces `Unexpected Thrust` preference.

### Prepared / firepower group

`Planned Attack`
- Planning is the dominant commander stat.
- Attack is used for hard formations; Defense for soft formations.
- `staff_officer` and `methodical` receive only +1 direct preference each to avoid double counting their Planning bonuses.

`Barrage`
- Artillery/equipment concentration remains the physical prerequisite and major weight source.
- Defense represents artillery competence; Planning represents organization of the fire plan.

`Relentless Assault`
- Reserves remain the defining condition.
- Planning and Logistics represent the command capacity to keep successive echelons moving and sustain pressure.
- `staff_officer` receives only a small direct preference.

### Crude assault group

`Shock`
- High Planning reduces its relative appeal.
- `improviser` gives a small preference while `methodical` gives a small penalty.
- Relevant branch competence can still raise it somewhat, but it is no longer primarily controlled by overall skill thresholds.

`Human Wave`
- Low Planning and low Logistics increase its weight.
- High Planning/Logistics and very high Defense reduce its weight.
- This strengthens the intended institutional transition: crude mass assault fades as Soviet command quality develops.

`Banzai Charge`
- Base weight remains reduced from 30 to 12.
- Low Planning/Logistics raise the chance; high Planning/high overall skill reduce it.

### Defensive group

`Counterattack`
- Defense + Planning matter, with Attack contributing for hard/mobile formations.
- Reserves remain important.

`Delay`
- Defense + especially Logistics steer the tactic.
- Reserves remain the largest situational weight.
- `independent_minded` / `improviser` receive only light direct preference.

`Ambush`
- Defense, Logistics and Planning all contribute.
- `ambusher`, `trickster` and `defensive_doctrine` remain stronger stylistic signals.
- `independent_minded` / `improviser` only add small direct opportunity-response weights.

`Elastic Defense`
- Raw overall-skill dominance was replaced by Defense + Logistics + Planning steps.
- Mobile-warfare professional traits now contribute lightly because mobile reserves and maneuver competence are relevant, but they do not dominate the tactic.

`Backhand Blow`
- Reserves remain central.
- Planning and Logistics are the main commander skills; Defense matters, while Attack matters additionally for hard/mobile formations.
- `mobile_warfare_leader` is now a direct access/weight source.
- `staff_officer` / `methodical` only add +1 each; `trickster` / `brilliant_strategist` remain stronger direct signals.

`Planned Defense`
- Planning is dominant; Defense is secondary.
- `staff_officer` and `methodical` only receive +1 direct preference each.

`Overwhelming Fire`
- Artillery concentration remains decisive.
- Defense + Planning represent defensive fire-control competence.

## 6. Phase tactics

The same mapping extends into battle phases:

- Close Combat: infantry/armor branch competence and Planning influence assault/storm/withdraw/strong-point choices.
- Tactical Withdrawal: Logistics is the main stat for withdrawal, evasion, chase and interception.
- `mobile_warfare_officer` / `mobile_warfare_leader` now directly improve chase/interception.
- `independent_minded` / `improviser` can directly enable or weight tactical withdrawal/evasion, reflecting initiative and local freedom of action.
- The stale `has_trait = cautious` check in Close Combat withdrawal was corrected to the actual `trait_cautious` ID.
- Bridge fighting remains primarily Planning/Logistics/Defense driven.
- Street Fighting remains mostly Defense/Planning driven; opportunity-oriented traits only receive light direct weight for urban ambushes.

## 7. Trait integration rule after commander-traits merge

The merged commander trait system introduces two categories that must stay distinct.

### Personality / command-style traits

- `independent_minded`
- `staff_officer`
- `methodical`
- `improviser`

These already modify HER subskills. Therefore they normally receive only `+1` or occasionally `+2` direct tactic weights when the *behavior itself* matches the personality. They must not become large flat tactic multipliers.

### Professional / branch traits

- `panzer_leader` / `panzer_expert`
- `mobile_warfare_officer` / `mobile_warfare_leader`
- `combined_arms_expert`
- `bearer_of_artillery`
- engineer-related specialization traits

These may directly unlock or strongly weight tactics because they represent actual specialist experience.

Intended professional distinction:

- **Panzer chain** = armored shock, tank-led breakthrough and armored exploitation.
- **Mobile-warfare chain** = motorized/mechanized maneuver, exploitation, pursuit and interception.
- **Combined arms** = mixed-formation execution, including softer formations.
- **Artillery specialization** = fire preparation and defensive fire control.

## 8. Expected commander differentiation

Target behaviour:

- **Guderian-type profile:** disproportionately strong Blitz / mobile exploitation / interception via high Attack/Logistics plus panzer/mobile traits.
- **Manstein-type profile:** strong prepared maneuver, encirclement, planned operations and Backhand Blow without requiring every such commander to be a pure tank specialist.
- **Model-type profile:** strong Delay / Ambush / Elastic Defense / prepared defensive choices through very high Defense and Planning.
- **Rundstedt / staff-heavy profile:** high Planning and staff traits should visibly affect prepared operational choices rather than being nearly invisible.
- **Late Soviet mobile commanders:** mobile-warfare traits can now support Blitz/Masterful Blitz without forcing all mech/motor specialists into `panzer_leader` semantics.
- **Zhukov / Rokossovsky / Vasilevsky-type profiles:** high Planning and improving Logistics progressively shift the pool away from crude mass assault and toward prepared breakthrough, echeloned pressure and sophisticated operational responses.

## 9. Things intentionally NOT changed yet

- Doctrine unlock order.
- Tactic combat-effect magnitudes.
- The counter network, including the open question around `Masterful Blitz`.
- The suspicious bridge-phase effect signs identified in the phase audit.
- The broad Guerrilla Tactics infantry trigger.
- Numerical weight tuning based on observed combat frequency.

## 10. Validation checklist

Before calling the system final:

1. Run parser/error-log validation for all `*_skill_level` and merged `has_trait` tactic checks.
2. Debug several controlled combats with commanders that have similar overall skill but sharply different subskill/trait profiles.
3. Compare actual tactic frequency for Guderian vs Model, and Manstein vs a similarly skilled pure armor commander.
4. Compare panzer specialists against `mobile_warfare_*` specialists commanding motorized/mechanized formations.
5. Compare early-war Soviet commanders against late high-Planning/Logistics commanders.
6. Verify that high skill no longer makes every commander converge on the same advanced tactics.
7. Check that base fallback tactics remain common enough when situational prerequisites are absent.
8. Revisit numerical steps only after observed frequency data; do not rebalance from isolated tooltip impressions.
