# HER combat tactics — commander-skill weight rework

Status: IMPLEMENTED, REQUIRES HANDS-OFF / COMBAT DEBUG VALIDATION

Implementation commit: `0d1077797309a6db66415a8e43c2493dca5254b6`

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

The tactic system now follows the established HER interpretation of commander stats:

- `attack_skill_level` = mechanized / armored tactical competence;
- `defense_skill_level` = infantry / artillery tactical competence;
- `planning_skill_level` = operational planning and prepared execution;
- `logistics_skill_level` = initiative, flexibility and self-reliance.

This HER meaning is intentionally more specific than the vanilla localisation of the four subskills.

## 4. Architecture rule

Tactic selection is now intended to be layered:

1. **Doctrine unlock** — whether the military institution knows the tactic at all.
2. **Combat situation** — composition, hardness, artillery concentration, frontage, reserves, terrain, flanking and phases determine whether the tactic makes sense.
3. **Traits** — commander style and specialist experience.
4. **Overall `skill` / `skill_advantage`** — general command quality and relative superiority.
5. **HER subskills** — steer which sophisticated tactic a commander prefers within the available pool.

Subskills deliberately use moderate, stepped additive weights. They are not meant to override doctrine, composition or reserves.

## 5. Main weighting changes

### Attack / maneuver group

`Encirclement`
- Planning and Logistics are now primary commander-quality weights.
- Attack contributes for hard/mobile formations; Defense contributes lightly for soft formations.
- `skill_advantage` remains useful but no longer dominates through a long stack of equal bonuses.

`Breakthrough`
- Planning is central.
- Hard formations read Attack; soft/artillery-heavy formations read Defense.
- Reserves gained more importance.
- The old flat `inflexible_strategist = -4` weight penalty was removed: inflexibility should not mean inability to conduct a deliberately prepared breakthrough.

`Blitz`
- Strongly reads Attack + Logistics, with a smaller Planning contribution.
- This is intended to make mobile specialists such as Guderian mechanically distinct from equally skilled infantry/defensive commanders.

`Masterful Blitz`
- Reads Attack + Logistics + Planning and still rewards reserves/full frontage.
- Its lack of a direct `countered_by` remains a separate architectural review item; this rework did not silently change the counter network.

`Unexpected Thrust` / `Flank Attack`
- Logistics and Planning now matter strongly because these represent rapid exploitation of local opportunities.
- Attack matters more when a hard/mobile formation is involved.

### Prepared / firepower group

`Planned Attack`
- Planning is now the dominant commander stat.
- Attack is used for hard formations; Defense for soft formations.

`Barrage`
- Artillery/equipment concentration remains the physical prerequisite and major weight source.
- Defense now represents artillery competence; Planning represents organization of the fire plan.

`Relentless Assault`
- Reserves remain the defining condition.
- Planning and Logistics now represent the command capacity to keep successive echelons moving and sustain pressure.

### Crude assault group

`Shock`
- High Planning reduces its relative appeal.
- Relevant branch competence can still raise it somewhat, but it is no longer primarily controlled by overall skill thresholds.

`Human Wave`
- Low Planning and low Logistics increase its weight.
- High Planning/Logistics and very high Defense reduce its weight.
- This strengthens the intended institutional transition: crude mass assault fades as Soviet command quality develops.

`Banzai Charge`
- Base weight reduced from 30 to 12.
- Low Planning/Logistics raise the chance; high Planning/high overall skill reduce it.
- This is the first step away from the old behaviour where Japan treated Banzai as an ordinary default attack throughout the war.

### Defensive group

`Counterattack`
- Defense + Planning now matter, with Attack contributing for hard/mobile formations.
- Reserves remain important.

`Delay`
- Defense + especially Logistics now steer the tactic.
- Reserves remain the largest situational weight.

`Ambush`
- Defense, Logistics and Planning all contribute.
- `ambusher`, `trickster` and `defensive_doctrine` remain stronger stylistic signals.

`Elastic Defense`
- The old large raw bonuses from high overall `skill` were replaced by Defense + Logistics + Planning steps.
- This prevents a generic high-skill attacker from automatically becoming an elite elastic defender.

`Backhand Blow`
- Reserves increased from a minor factor to a central one.
- Planning and Logistics are the main commander skills; Defense matters, while Attack matters additionally for hard/mobile formations.
- `trickster` and `brilliant_strategist` remain important.

`Planned Defense`
- Planning is dominant; Defense is secondary.

`Overwhelming Fire`
- Artillery concentration remains decisive.
- Defense + Planning now represent defensive fire-control competence.

## 6. Phase tactics

The same mapping was extended into battle phases instead of leaving them on raw base weights:

- Close Combat: infantry/armor branch competence and Planning influence assault/storm/withdraw/strong-point choices.
- Tactical Withdrawal: Logistics is the main stat for withdrawal, evasion, chase and interception; Planning and Attack/Defense provide secondary differentiation.
- Bridge fighting: Planning/Logistics influence bridge seizure/retaking; Defense influences holding and skillful bridge defense.
- Street Fighting: Defense/Planning drive fortification and urban defense; Attack drives armored assault; Defense/Planning drive mouse-holing and artillery urban assault; Logistics contributes to urban ambushes.

## 7. Expected commander differentiation

The target behaviour after this rework:

- **Guderian-type profile:** disproportionately strong Blitz / mobile exploitation / interception; no longer equally strong merely because overall skill is high in unrelated defensive tactics.
- **Manstein-type profile:** strong prepared maneuver, encirclement, planned operations and Backhand Blow through Planning/Logistics plus traits.
- **Model-type profile:** strong Delay / Ambush / Elastic Defense / prepared defensive choices through very high Defense and Planning.
- **Rundstedt / staff-heavy profile:** high Planning should now visibly affect prepared operational choices rather than being nearly invisible.
- **Zhukov / Rokossovsky / Vasilevsky-type profiles:** high Planning and improving Logistics should progressively shift the Soviet tactic pool away from crude mass assault and toward prepared breakthrough, echeloned pressure and sophisticated operational responses.

## 8. Things intentionally NOT changed in this commit

- Doctrine unlock order.
- Tactic combat-effect magnitudes.
- The counter network, including the open question around `Masterful Blitz`.
- The suspicious bridge-phase effect signs identified in the phase audit.
- The broad Guerrilla Tactics infantry trigger.
- The exact trigger gating of normal Blitz (including the Manstein-without-`panzer_leader` question).

Those remain separate audit items so the effect of the commander-weight rework can be isolated.

## 9. Validation checklist

Before calling the system final:

1. Run parser/error-log validation for all `*_skill_level` tactic checks.
2. Debug several controlled combats with commanders that have similar overall skill but sharply different subskill profiles.
3. Compare actual tactic frequency for Guderian vs Model, and Manstein vs a similarly skilled pure armor commander.
4. Compare early-war Soviet commanders against late high-Planning/Logistics commanders.
5. Verify that high skill no longer makes every commander converge on the same advanced tactics.
6. Check that base fallback tactics remain common enough when situational prerequisites are absent.
7. Revisit numerical steps only after observed frequency data; do not rebalance from isolated tooltip impressions.

## 10. Commander-traits rework integration plan

Target source branch: `commander-traits-rework`.

The branch introduces personality-style traits and new professional specialization chains that must be treated differently by the tactic system.

### 10.1 Core rule: avoid double counting personality traits

The following new personality traits already alter HER subskills and therefore should affect most tactics **indirectly** through the `*_skill_level` checks rather than receiving large direct tactic weights:

- `independent_minded` — raises Logistics/initiative profile;
- `staff_officer` — raises Planning/staff profile;
- `methodical` — raises Planning while reducing Logistics/initiative;
- `improviser` — raises Logistics/initiative while reducing Planning.

Direct tactic bonuses for these traits, where used at all, should be small (`+1` or occasionally `+2`) and reserved for tactics whose behavioral meaning is especially specific to the personality. The trait's subskill changes remain the primary mechanism.

Recommended personality interaction:

- `independent_minded`: light preference for `Flank Attack`, `Unexpected Thrust`, `Tactical Withdrawal` / `TW Evade` and opportunity exploitation;
- `staff_officer`: normally no direct bonus; Planning already feeds `Planned Attack`, `Planned Defense`, `Breakthrough`, `Backhand Blow`, artillery preparation and reserve-heavy operations;
- `methodical`: small positive preference for `Planned Attack`, `Planned Defense`, `Barrage`; small negative preference for `Unexpected Thrust`, `Flank Attack`, rapid pursuit/interception;
- `improviser`: small positive preference for `Unexpected Thrust`, `Flank Attack`, `TW Intercept`, bridge seizure/retaking; small negative preference for the most prepared fire-plan/position-defense choices.

### 10.2 Professional traits should directly mark tactical school

Professional/formation-specialist traits may receive direct tactic weights because they mean the commander has actual specialist experience, not merely a personality inclination.

The most important new chain is:

`mobile_warfare_officer -> mobile_warfare_leader -> assignable mobile-warfare expertise`

`mobile_warfare_officer` is gained from motorized/mechanized command and feeds `mobile_warfare_leader`. This fills the previous gap where mobile/mechanized commanders were often represented by tank-only `panzer_leader` semantics.

Planned direct integration after merge:

- `mobile_warfare_officer`: `Unexpected Thrust` +2, `Flank Attack` +1, `Blitz` +1;
- `mobile_warfare_leader`: `Unexpected Thrust` +2, `Flank Attack` +2, `Blitz` +2, `Encirclement` +1, `TW Intercept` +1;
- higher mobile-warfare expert trait: additional +1 to `Blitz`, `Encirclement`, `Flank Attack` and pursuit/interception-type choices, without replacing `panzer_expert` as the stronger pure armored marker.

The intended distinction is:

- `panzer_leader` / `panzer_expert` = armored shock, armored breakthrough and tank-led exploitation;
- `mobile_warfare_officer` / `mobile_warfare_leader` = motorized/mechanized maneuver, rapid exploitation and pursuit;
- `combined_arms_expert` = combined-arms execution across softer formations;
- `bearer_of_artillery` = artillery-centric fire preparation and fire control.

### 10.3 Planned trigger changes after merge

The current normal `Blitz` trigger is too binary because it effectively requires either `panzer_leader` for hard formations or `combined_arms_expert` for soft formations.

After the trait branch is merged, review the trigger toward this structure:

- hard formations: `panzer_leader` OR `mobile_warfare_leader` OR exceptionally high Attack+Logistics with suitable overall skill/advantage;
- medium/mobile formations: `mobile_warfare_officer` / `mobile_warfare_leader` should become a natural access path;
- soft formations: `combined_arms_expert` remains the main specialist path.

This should allow an operationally gifted mobile commander to use Blitz without forcing every such commander to carry a tank-specialist trait, while a true panzer specialist still receives the strongest weight.

### 10.4 Tactic-by-tactic trait overlay after merge

**Encirclement**
- keep `trickster`, `panzer_expert`, `combined_arms_expert`;
- add light `mobile_warfare_leader` weight;
- personality traits mainly act through Planning/Logistics.

**Blitz / Masterful Blitz**
- direct `mobile_warfare_officer`/`mobile_warfare_leader` weights;
- preserve stronger `panzer_leader`/`panzer_expert` armored identity;
- do not use `staff_officer` as a direct Blitz booster.

**Unexpected Thrust / Flank Attack**
- strongest beneficiaries of mobile-warfare traits;
- `improviser` and `independent_minded` may receive small direct bonuses because the behavior matches opportunity exploitation.

**Breakthrough**
- remain primarily Planning + formation competence + reserves;
- direct mobile-warfare bonuses should be small or absent;
- `panzer_expert`, `combined_arms_expert`, `bearer_of_artillery` remain the important professional markers.

**Planned Attack / Planned Defense / Barrage / Overwhelming Fire**
- mostly driven by Planning/Defense and specialist professional traits;
- `methodical` may receive a small direct preference;
- `staff_officer` should normally work only through its Planning increase.

**Delay / Tactical Withdrawal / TW Evade / TW Intercept**
- Logistics remains primary;
- `independent_minded` / `improviser` may receive small direct opportunity-response bonuses;
- `mobile_warfare_leader` can directly help interception/pursuit where mobile formations are present.

**Backhand Blow**
- Planning + Logistics + reserves remain central;
- light `mobile_warfare_leader` contribution is acceptable for hard/mobile formations;
- do not turn it into a generic panzer tactic: `trickster` / `brilliant_strategist` and operational-quality stats remain more important.

### 10.5 Post-merge implementation order

1. Confirm exact final trait IDs after merge.
2. Add direct weights for the professional mobile-warfare chain.
3. Add only small personality-specific direct modifiers where justified.
4. Expand Blitz and selected maneuver-tactic triggers so mobile-warfare specialists are valid access paths.
5. Re-run commander comparison matrix with the merged GER/SOV character rosters.
6. Only then tune numerical weights from combat-debug frequencies.

This integration plan is intentionally documented before merge so the tactic system does not have to be redesigned a second time after the trait branch lands.
