# HER Mod — Doctrine Audit

Status: IN PROGRESS

Purpose: systematic audit of land, air, and naval doctrines across historical role, balance, integration, and code quality.

Severity:
- A — architectural/design problem
- B — balance/numerical problem
- C — polish/cleanup
- BUG — confirmed logic/code error

## 0. Revised doctrine-audit principle

Direct bonuses to organization, morale/recovery, attack, breakthrough, defense, planning, reinforce rate and initiative are NOT treated as design problems by default.

In HER these stats are one of the main ways to represent differences in the quality of military institutions: staff work, communications, junior leadership, combined-arms coordination, reserve handling, operational tempo, cohesion under movement, fire control, and the ability to continue an operation after the first contact.

Therefore the audit question is not "does this doctrine give +5 org?" but:
- is the source historically intelligible for this military school;
- is the scope correct (foot infantry / armor / artillery / mobile units / support etc.);
- is the magnitude plausible relative to competing military schools;
- does the cumulative result create the intended quality hierarchy between armies;
- does the bonus produce a distinctive doctrinal profile rather than accidentally making every formation equally better;
- is the effect a normal quality modifier or a structural/meta-changing effect that requires separate testing.

Raw stat bonuses are legitimate. Structural effects such as division-template columns and combat-width changes remain special-risk mechanics because they can reshape the entire template meta.

## 1. Land doctrine architecture

HER retains the old XP-unlocked doctrine-tree model. Doctrine entries use `xp_research_type = army` and mostly `xp_unlock_cost = 100`.

### National-school gating
Current doctrine roots are not fully universal:
- `mobile_warfare` is gated to GER;
- `mass_assault` is gated to SOV;
- `superior_firepower` and `trench_warfare` explicitly exclude GER and SOV.

Verdict: KEEP. This makes doctrine represent national military institutions rather than doctrine shopping.

Doctrine trees do not need strict symmetry. A highly developed German mobile school should legitimately produce better organization/initiative/breakthrough for mobile formations than a weaker contemporary army. Likewise late-war Soviet doctrine should legitimately improve cohesion, reserve handling and sustained offensive quality compared with the 1941 Red Army.

## 2. Mobile Warfare — German school

### Root
`mobile_warfare`:
- +15% breakthrough to all armor;
- +20% planning speed;
- +5% army speed;
- -10% org loss while moving;
- unlocks Unexpected Thrust.

Revised verdict: the density of the root is not automatically a problem. It coherently expresses an already-developed German operational school: faster preparation, movement, preservation of cohesion and stronger armored penetration.

Balance question: whether all of this belongs at the first doctrine node or should be distributed across early nodes for pacing.

### Early progression
`delay` gives +5 org to all infantry.

`elastic_defence` gives:
- +2% reinforce rate;
- +10% army defense through `category_army`;
- +10% maximum speed to all armor;
- Elastic Defense tactic.

Direct defense/org bonuses are acceptable as institutional-quality differences. The main scope question is the +10% raw armor speed: verify that it does not make equipment-engine/chassis choices irrelevant.

### Mobile-infantry branch
`mobile_infantry` gives +10% speed and +10% morale to vehicle infantry, armored cars and mobile combat support.

`mass_motorization` gives +10 org to all infantry.

`mechanised_offensive` gives +5 org and +10% breakthrough to vehicle infantry and tanks.

Revised verdict: the branch may legitimately produce a large organization gap between German formations and weaker armies. The main question is whether `mass_motorization -> category_all_infantry` intentionally improves ordinary foot infantry or should be restricted to motorized/mechanized formations.

### Armored-spearhead branch
`armored_spearhead`:
- tanks +5 org, +5% hard/soft attack;
- logistics company reduces tank supply and fuel by 3%;
- unlocks Blitz.

`schwerpunk`:
- tanks +5 org;
- motorcycle recon buffs artillery +6% breakthrough and soft attack;
- assault engineers buff `category_army` +5% breakthrough and soft attack;
- Barrage tactic.

The tank org/attack/breakthrough package is appropriate for a mature German armored school. The questionable element remains support-company scope: `assault_engineer -> category_army` makes one support company a universal formation-wide combat multiplier. Test scope rather than rejecting the direct stats themselves.

### Late German branches
`firebrigades` is focus-gated by `GER_refinement_of_bewegungskrieg` and improves mobile infantry/tanks/TDs.

`backhand_blow` gives +10% morale and +5% HA/SA to all armor plus +10 org to all infantry.

`modern_blitzkrieg` adds further signal/recon synergies and +30% planning speed.

These are legitimate late-war improvements in organizational quality if cumulative values stay within the intended GER-vs-other-armies hierarchy.

Alternative emergency branch:
- `volkssturm` +0.5% recruitable population but -5 org to infantry/heavy infantry;
- `nd_conscription` repeats another +0.5% recruitable and -5 org;
- `werwolf_guerillas` adds resistance/garrison effects.

Verdict: excellent quality-vs-quantity branch. KEEP concept.

## 3. Superior Firepower — firepower / support integration school

Root `superior_firepower` gives +10% soft attack to `category_front_line`.

`sup_delay` gives +10 org to light infantry.

`mobile_defence` gives all infantry +10% defense and +5% maximum speed.

These bonuses are not intrinsically excessive. They should be judged against the doctrine's intended users and historical baseline armies.

### Fire-control / artillery branch
`concentrated_fire_plans`:
- `additional_brigade_column_size = 2`;
- all artillery +5 morale, +5 org, +10% soft/hard attack, +2% initiative.

The artillery quality package is doctrinally coherent. **A / structural:** +2 division-designer columns requires separate template-meta testing because it changes design capacity rather than merely combat quality.

`centralized_fire_control`:
- artillery +10% soft attack and +5 org;
- AT +10% hard attack and +5 org;
- AA +10% air attack and +5 org.

`forward_observers` makes recon support buff front-line soft/hard attack by 5%, plus recon/initiative.

`advanced_firebases` gives infantry +10 org/+10% morale and engineer synergies with line artillery.

`shock_and_awe` adds:
- +10% air-superiority combat bonus;
- +10% CAS efficiency;
- +5% soft/hard attack to infantry, line artillery and tanks;
- Breakthrough tactic.

Revised verdict: combined-arms expansion at the end is not inherently wrong. The question is whether the final tree still produces a recognizably firepower/support-centric army rather than simply matching specialized German armor or Soviet deep-operations strengths in their own domains.

### Combined-arms branch
`combined_arms` gives tanks, vehicle infantry and mobile combat supports +5% HA/SA/breakthrough.

`tactical_control` gives +5% initiative factor and +15% planning speed.

`air_land_battle` gives +5 org to front line and +20% army benefit from air superiority.

Verdict: strong doctrinal identity. KEEP unless cumulative comparison shows it dominates unrelated schools.

## 4. Grand Battleplan — preparation / control / infiltration school

Observed late branch examples:
- `assault_breakthrough`: assault engineers give +20% breakthrough to `category_army`;
- `central_planning`: -15% planning speed but +5% max planning and +50 max command power;
- `c3i_theory`: +15% army air-superiority factor plus recon/signal buffs;
- `infantry_offensive`: light infantry +5 org, +10% breakthrough, +10% soft attack;
- `armored_operations`: armor gains org, morale, initiative and +10% HA/SA;
- `infiltration_assault`: -5% supply use, +10% command-power gain, special forces +15% HA/SA;
- `night_assault_tactics`: +10% land night attack;
- `attritional_containment`: infantry +5 org and +10% defense.

### Strong design
`central_planning` reducing planning speed while increasing planning ceiling is a particularly good doctrinal trade-off. KEEP.

### Scope checks
`assault_breakthrough -> assault_engineer -> category_army +20% breakthrough` remains a red flag because of scope and magnitude, not because breakthrough is a direct stat.

`armored_operations` giving substantial armor quality is acceptable if Grand Battleplan is intended to include a serious prepared armored-offensive school; compare cumulative armor quality against Mobile Warfare rather than assuming the bonus is wrong.

`infiltration_assault` special-forces +15% HA/SA is also acceptable in principle if this is the branch's elite assault identity; verify cumulative effect with night/terrain bonuses.

## 5. Mass Assault / Soviet doctrine — detailed pass

### Root: `mass_assault`
- SOV-only;
- `additional_brigade_column_size = 2`;
- -5% supply consumption;
- -10% minimum training level;
- `experience_loss_factor = 0.05`.

The lower training threshold is a strong Soviet mass-expansion mechanic. `experience_loss_factor` should be engine-verified for sign/behavior.

**A / structural:** +2 template columns requires separate testing because it changes formation-design possibilities.

### Early defensive foundation
`pocket_defence`:
- +48 hours no-supply grace;
- -10% out-of-supply penalty;
- -5% pocket penalty.

`defence_in_depth`:
- +5 max entrenchment;
- +5 org to light infantry.

Verdict: excellent Soviet resilience identity. KEEP.

### Deep-operations branch
`large_front_operations`:
- +5 org front line;
- -5% supply consumption.

`deep_operations`:
- tanks +5 org and +5% SA/HA;
- -5% org loss while moving;
- Blitz tactic.

`operational_concentration`:
- artillery +5 org/+5% morale;
- infantry +5 org;
- Barrage tactic.

`vast_offensives`:
- another -5% supply consumption;
- +5 org front line;
- +5% air-superiority combat bonus;
- Overwhelming Fire tactic.

Revised verdict: repeated +5 org is not a problem by itself. It is a plausible representation of the Red Army's improving operational cohesion and command system. The real audit task is to compute the cumulative 1941/42/43/44 quality progression and ensure the late Red Army becomes substantially better organized than the early-war one without simply cloning German strengths.

### Breakthrough / mechanized phase
`breakthrough_priority`:
- line artillery +5 org and +15% breakthrough;
- SP artillery +5 org and +20% breakthrough;
- TD +5 org and +20% breakthrough;
- Breakthrough tactic.

These direct bonuses may be valid if they represent better integration of artillery/assault guns/TDs into shock formations. The remaining question is scope: whether ordinary line artillery and TDs should receive the full breakthrough package in every formation, or whether part of the effect should depend on assault-support composition.

`mechanized_wave`:
- tanks +10% morale, +5 org, +1% initiative;
- SP artillery/TD +5% morale, +5 org, +5% SA/HA.

Legitimate late-war quality growth.

### `continuous_offensive`
- -15% org loss while moving;
- +5% reinforce rate;
- +5% max planning;
- front line +5% SA/HA;
- Backhand Blow tactic.

Verdict: one of the strongest representations of Soviet operational depth. KEEP core package.

### People's Army branch
`peoples_army`:
- MP can add +5 org to front-line categories;
- penal battalion +10 org;
- militia combat width -0.45;
- -10% attrition;
- resistance effects;
- Human Wave tactic.

**A / structural:** militia -45% combat width requires dedicated damage/HP/org/manpower/equipment-per-width testing. It can be a valid mass-army identity mechanic, but its effect is multiplicative and cannot be judged like +10% attack.

`human_infantry_offensive`:
- light infantry +5% morale and +10% soft attack.

`large_front_offensive`:
- +5 org all infantry;
- Relentless Assault tactic.

`human_wave_offensive`:
- +0.5% recruitable population;
- MP gives +10% infantry morale.

`guerilla_warfare`:
- -10% out-of-supply penalty;
- +5% army morale;
- resistance effects;
- Elastic Defense tactic.

Verdict: quality/resilience improvements are valid. Their cumulative value must be assessed together with the militia-width mechanic.

### Final mechanized convergence: `masterful_blitz`
- armor +5 org, +5% SA/HA/breakthrough;
- vehicle infantry +5 org, +10% morale, +1% initiative;
- Masterful Blitz tactic.

Direct armor bonuses are acceptable. The important differentiation is qualitative profile:
- GER should remain superior at rapid local concentration, initiative, C2 and tactical penetration;
- SOV should excel at sustaining deep operations, reinforcement, supply tolerance, movement cohesion and follow-on echelons.

The two armies may share some org/attack/breakthrough bonuses without becoming mechanically identical if their broader profiles remain distinct.

## 6. Desired end-state military quality profiles

Doctrine balance should be evaluated through representative formation quality, not by counting modifier lines.

### German Mobile Warfare
Expected strongest areas:
- tank/mechanized organization;
- breakthrough;
- initiative and tactical responsiveness;
- planning speed;
- movement tempo;
- reduced cohesion loss while moving;
- signal/recon/support integration;
- high-quality local combined-arms spearheads.

It is acceptable for a German armored/mechanized division to be materially better organized and more effective than the equivalent formation of a weaker contemporary military institution.

### Soviet Mass Assault / Deep Operations
Expected strongest areas:
- operational depth;
- reserve/reinforce handling;
- supply tolerance / lower supply use;
- pocket resilience;
- reduced movement-org loss;
- large-front operations;
- artillery/mechanized integration;
- rapid wartime expansion;
- strong late-war mechanized quality.

The key historical progression should be visible: 1941 Soviet formations should not automatically possess the mature qualities of the 1944-45 Red Army merely because the same national doctrine family exists.

### Superior Firepower
Expected strongest areas:
- artillery/fire-control efficiency;
- front-line firepower;
- support-company effectiveness;
- recon/forward-observer integration;
- combined-arms fire coordination;
- air-ground cooperation.

### Grand Battleplan
Expected strongest areas:
- max planning / prepared attack;
- entrenchment and defensive preparation;
- command/control;
- deliberate assaults;
- infiltration/night/special-forces advantages;
- operational deception and controlled commitment of reserves.

## 7. What now counts as a real doctrine balance risk

1. **Wrong scope.** Example: a motorization doctrine buffing all foot infantry if that was not intended.
2. **Wrong magnitude relative to institutional quality.** A weaker military school matching the specialist school in its core domain without historical justification.
3. **Role leakage.** Support-company effects targeting `category_army` and unintentionally boosting every battalion in a division.
4. **Structural/meta multipliers.** Extra division columns, major combat-width reductions, etc.
5. **Timing mismatch.** Late-war institutional quality becoming available too early through cheap doctrine progression/focuses/starting doctrines.
6. **Identity convergence.** Different schools ending with similar final profiles even if the individual stat bonuses are individually reasonable.
7. **Hidden interaction stacking.** Doctrine + focus + general trait + equipment designer + road/industry bonuses producing extreme totals.

Direct +org/+attack/+breakthrough is not itself a listed risk.

## 8. Next land-doctrine pass

- calculate representative cumulative end-state profiles for foot infantry, artillery infantry, tank, mechanized, militia and special-forces formations;
- compare GER/SOV/Superior-Firepower/Grand-Battleplan quality profiles by role;
- audit support-company battalion multipliers and category scopes;
- test structural effects: extra columns and militia width;
- audit doctrine timing / national starting doctrine state / focus-granted doctrine progress;
- identify duplicate tactic unlocks and dead/inaccessible gates;
- then move to Air Doctrine and Naval Doctrine.
