# HER tactics — commander recalculation after trait merge

Status: POST-MERGE AUDIT

Relevant tactic implementation commits:
- `0d1077797309a6db66415a8e43c2493dca5254b6` — HER subskill weighting rework
- `183f21882078ea8bc5abcf698442a8119ed43567` — commander-trait integration

## Method

The comparison below isolates the commander-driven part of tactic weight. Doctrine availability and identical battlefield conditions are held constant; situational bonuses such as reserves, frontage, flank, terrain and skill advantage are excluded unless they are part of access logic.

Effective HER subskills include direct skill changes from personality traits where applicable. This is important because the tactic engine now reads `attack_skill_level`, `defense_skill_level`, `planning_skill_level`, and `logistics_skill_level` directly.

## Effective profiles used

| Commander | Attack | Defense | Planning | Logistics | Important tactic traits |
|---|---:|---:|---:|---:|---|
| Guderian | 16 | 3 | 11 | 14 | trickster, improviser, independent_minded, brilliant_strategist, panzer_leader, mobile_warfare_officer |
| Manstein | 7 | 9 | 15 | 11 | trickster, improviser, independent_minded, brilliant_strategist, mobile_warfare_officer |
| Model | 5 | 16 | 14 | 8 | independent_minded, defensive_doctrine, inflexible_strategist |
| Rundstedt | 2 | 8 | 12 | 4 | staff_officer, methodical |
| Zhukov | 7 | 13 | 12 | 5 | trickster, inflexible_strategist |
| Rokossovsky | 6 | 6 | 14 | 6 | brilliant_strategist, independent_minded, methodical |
| Vasilevsky | 9 | 12 | 24 | 11 | brilliant_strategist, staff_officer, methodical |

## Commander-only indicative weights

These values are not final in-battle probabilities; they are the tactic base plus commander-derived modifiers under equal conditions.

| Commander | Encirclement | Blitz | Unexpected Thrust | Flank Attack | Elastic Defense | Backhand Blow |
|---|---:|---:|---:|---:|---:|---:|
| Guderian | 20 | 23 | 34 | 24 | 26 | 28 |
| Manstein | 20 | 17 | 30 | 22 | 29 | 26 |
| Model | 12 | 9 | 20 | 11 | 27 | 17 |
| Rundstedt | 10 | 6 | 17 | 8 | 20 | 15 |
| Zhukov | 13 | 9 | 21 | 14 | 25 | 20 |
| Rokossovsky | 12 | 8 | 19 | 9 | 22 | 18 |
| Vasilevsky | 15 | 11 | 22 | 14 | 28 | 26 |

## Prepared-operation weights

| Commander | Planned Attack (hard) | Planned Attack (soft) | Planned Defense |
|---|---:|---:|---:|
| Guderian | 17 | 14 | 14 |
| Manstein | 18 | 18 | 20 |
| Model | 13 | 16 | 18 |
| Rundstedt | 15 | 16 | 16 |
| Zhukov | 14 | 16 | 18 |
| Rokossovsky | 18 | 18 | 19 |
| Vasilevsky | 20 | 22 | 24 |

## Findings

### Guderian

The desired differentiation now works. Guderian is the strongest of the core sample in Blitz, Unexpected Thrust and Flank Attack. His very high Attack/Logistics plus `mobile_warfare_officer`, `panzer_leader`, `improviser` and `independent_minded` produce a clearly mobile/exploitation-heavy profile.

### Manstein

The previous hard gate problem is resolved: `mobile_warfare_officer` plus adequate Attack/Logistics provides a natural Blitz path without forcing `panzer_leader` onto him. His Blitz weight remains materially below Guderian's, while Encirclement, planned operations and Backhand Blow are very strong. This is the intended distinction.

### Model

His high Defense/Planning produces a strong defensive profile, but one issue remains: `defensive_doctrine` boosts Delay and Ambush directly but currently does not boost Elastic Defense or Planned Defense. As a result Manstein's commander-only Elastic Defense weight (29) slightly exceeds Model's (27). Recommended follow-up: add a moderate direct `defensive_doctrine` weight to Elastic Defense and Planned Defense, probably +3 each. This would preserve stats as the main mechanism while restoring the trait's doctrinal identity.

### Rundstedt

The staff profile is now visible. High effective Planning makes him respectable in Planned Attack/Defense despite low Attack and Logistics. He no longer behaves like a generic skill-6 commander. Low Logistics appropriately keeps him away from rapid mobile exploitation.

### Zhukov

The profile now strongly favors infantry/artillery command, prepared operations, counterattack and complex defense. `inflexible_strategist` no longer directly suppresses Breakthrough. His lower Logistics keeps him below the German mobile specialists in exploitation-oriented choices, which is desirable for the early/mid-war profile.

### Rokossovsky

The merged traits improve him substantially as an operational planner: effective Planning is very high, while `methodical` and `independent_minded` largely balance each other on Logistics. He is strong in Planned Attack/Defense and respectable in Backhand Blow, but deliberately not a Blitz specialist.

### Vasilevsky

The staff-specialist concept now works extremely clearly. Effective Planning becomes exceptional, producing the strongest Planned Attack/Defense values in the sample and a very strong Backhand Blow profile. This finally makes the large Planning value mechanically meaningful.

## Access-gate issue: Encirclement

The weight model is good, but access remains narrower than the commander model. At neutral `skill_advantage`, Encirclement is naturally accessible through combined-arms, panzer or mobile-warfare specialization. High-Planning staff/operational commanders without those traits still need `skill_advantage > 1`.

This means Rokossovsky/Vasilevsky/Zhukov may have good theoretical Encirclement weights but cannot select it in an even-skill fight unless another specialist access path applies. This should be reviewed separately. A possible future access path is exceptionally high Planning combined with adequate Logistics or `brilliant_strategist`, but it should not make every staff officer an encirclement specialist.

## Follow-up recommendations

1. Add `defensive_doctrine = +3` to Elastic Defense and Planned Defense weights.
2. Test whether Encirclement needs a high-Planning operational access path.
3. Run controlled combat-debug tests with Guderian vs Manstein and Model vs Manstein to validate actual selection frequencies.
4. Test early Zhukov against late Vasilevsky/Rokossovsky profiles after doctrine progression.
5. Do not change commander character stats solely to force tactic behavior unless combat-debug results show a genuine historical-profile problem; tactic weights are now the primary tuning layer.
