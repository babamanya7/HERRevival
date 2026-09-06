# HER Mod — Doctrine Audit

Status: IN PROGRESS

Purpose: systematic audit of land, air, and naval doctrines across historical role, balance, integration, and code quality.

Severity:
- A — architectural/design problem
- B — balance/numerical problem
- C — polish/cleanup
- BUG — confirmed logic/code error

## 1. Land doctrine architecture

HER retains the old XP-unlocked doctrine-tree model. Doctrine entries use `xp_research_type = army` and mostly `xp_unlock_cost = 100`.

### National-school gating
Current doctrine roots are not fully universal:
- `mobile_warfare` is gated to GER;
- `mass_assault` is gated to SOV;
- `superior_firepower` and `trench_warfare` explicitly exclude GER and SOV.

Preliminary verdict: KEEP. This is a strong HER-specific historical design choice. It prevents doctrine shopping and makes doctrine represent national military institutions rather than a pre-war meta toggle.

Audit implication: branches should be judged against the historical school they represent, not by strict one-to-one symmetry.

## 2. Mobile Warfare — first pass

### Root
`mobile_warfare`:
- +15% breakthrough to all armor;
- +20% planning speed;
- +5% army speed;
- -10% org loss while moving;
- unlocks unexpected thrust tactic.

This is already a very dense opening doctrine. **B:** review whether the root should simultaneously improve armor breakthrough, movement speed, planning speed and moving-org retention. Strong identity is good, but the opening click may front-load too much of the whole doctrine concept.

### Early progression
`delay` gives +5 org to all infantry.

`elastic_defence` gives:
- +2% reinforce rate;
- +10% army defense through `category_army`;
- +10% maximum speed to all armor;
- elastic-defense tactic.

**B / role overlap:** +10% armor speed on an elastic-defense doctrine is large and competes with designer/engine/chassis performance. Preserve operational mobility, but consider shifting part of the effect from raw equipment speed toward reinforce/withdrawal/initiative/organization recovery.

### Mobile-infantry branch
`mobile_infantry` gives +10% speed and +10% morale to vehicle infantry, armored cars and mobile combat support.

`mass_motorization` gives +10 org to all infantry.

`mechanised_offensive` gives +5 org and +10% breakthrough to vehicle infantry and tanks.

Preliminary verdict: coherent role, but **B:** repeated large organization grants quickly make the branch universally valuable even outside genuinely mobile formations. `mass_motorization` affecting `category_all_infantry` is especially broad; inspect whether ordinary foot infantry unintentionally receives a major org boost from a motorization doctrine.

### Armored-spearhead branch
`armored_spearhead`:
- tanks +5 org, +5% hard/soft attack;
- logistics company reduces tank supply and fuel by 3%;
- unlocks Blitz tactic.

`schwerpunk`:
- tanks +5 org;
- motorcycle recon buffs all artillery +6% breakthrough and soft attack;
- assault engineers buff all army +5% breakthrough and soft attack;
- barrage tactic.

**A/B:** support-company battalion multipliers are interesting and should be retained, but `assault_engineer -> category_army +5% soft attack +5% breakthrough` is extremely broad. A support company becomes a doctrine-wide universal combat multiplier rather than a situational engineering capability.

### Late German branches
`firebrigades` is focus-gated by `GER_refinement_of_bewegungskrieg` and improves mobile infantry/tanks/TDs.

`backhand_blow` gives +10% morale and +5% HA/SA to all armor plus +10 org to all infantry.

`modern_blitzkrieg` adds further signal/recon synergies and +30% planning speed.

Alternative late-war branch:
- `volkssturm` +0.5% recruitable population but -5 org to infantry/heavy infantry;
- `nd_conscription` repeats another +0.5% recruitable and -5 org;
- `werwolf_guerillas` adds resistance damage and defensive/garrison effects.

Preliminary verdict: the existence of a late-war emergency mobilization branch is excellent and historically expressive. KEEP concept. Review cumulative manpower and org effects together with conscription laws.

## 3. Superior Firepower — first pass

Root `superior_firepower` gives +10% soft attack to `category_front_line`.

`sup_delay` gives +10 org to light infantry.

`mobile_defence` gives all infantry +10% defense and +5% maximum speed.

**B:** raw infantry speed again appears as a doctrine effect. Across doctrines, speed bonuses should be rationed because they compound with road techs, equipment, generals and designer effects.

### Fire-control / artillery branch
`concentrated_fire_plans` is a major structural doctrine:
- `additional_brigade_column_size = 2`;
- all artillery +5 morale, +5 org, +10% soft/hard attack, +2% initiative.

**A:** changing division-designer column capacity is far more powerful than an ordinary +stat doctrine and can create template/meta exploits. This should be tested as a structural mechanic, not balanced as if it were another 10% attack bonus. If kept, the branch should probably pay for the increased template flexibility elsewhere.

`centralized_fire_control` gives:
- artillery +10% soft attack and +5 org;
- AT +10% hard attack and +5 org;
- AA +10% air attack and +5 org.

`forward_observers` makes recon support directly buff front-line soft/hard attack by 5%, plus recon/initiative.

`advanced_firebases` gives all infantry +10 org/+10% morale and allows engineer/armored-engineer companies to add strength/org to line artillery.

`shock_and_awe` adds:
- +10% air-superiority combat bonus;
- +10% CAS efficiency;
- +5% soft/hard attack to infantry, line artillery and tanks;
- breakthrough tactic.

**A/B:** late Superior Firepower becomes increasingly universal: artillery specialization ends in infantry+tank+air bonuses. Preserve combined-arms identity, but reduce the tendency for the final nodes to become a universal best-stat package.

### Combined-arms branch
`combined_arms` gives tanks, vehicle infantry and mobile combat supports +5% HA/SA/breakthrough.

`tactical_control` gives +5% initiative factor and +15% planning speed.

`air_land_battle` gives +5 org to front line and +20% army benefit from air superiority.

Preliminary verdict: conceptually strong. Air-land integration is a good doctrine identity and should remain mission/system oriented rather than becoming additional direct equipment attack where possible.

## 4. Grand Battleplan — first pass

Observed late branch examples:
- `assault_breakthrough`: assault engineers give +20% breakthrough to all army category;
- `central_planning`: -15% planning speed but +5% max planning and +50 max command power, with signal-company combat bonuses;
- `c3i_theory`: +15% army air-superiority factor plus recon/signal buffs;
- `infantry_offensive`: light infantry +5 org, +10% breakthrough, +10% soft attack;
- `armored_operations`: armor gains org, morale, initiative and +10% HA/SA;
- `infiltration_assault`: -5% supply use, +10% command-power gain, special forces +15% HA/SA;
- `night_assault_tactics`: +10% land night attack;
- `attritional_containment`: infantry +5 org and +10% defense.

### Important finding
`central_planning` reducing `planning_speed` while increasing `max_planning` is a genuinely good trade-off and one of the better doctrine effects found so far. It represents deliberate preparation rather than generic strength. KEEP principle.

### Potential overbreadth
`assault_breakthrough` gives a support-company-driven +20% breakthrough multiplier to `category_army`. **A/B:** likely too broad; assault engineers should favor fortified/urban/river/assault contexts rather than globally making every battalion 20% better at breakthrough whenever the company exists.

`armored_operations` gives all armor a large combined package (org + morale + initiative +10% HA/SA). **B:** may overinflate armored stats in a doctrine that is not primarily the specialized armored school.

`infiltration_assault` giving special forces +15% hard and soft attack is a large direct multiplier. Consider replacing part with night, terrain, supply, initiative or planning advantages so infiltration remains operational rather than raw DPS scaling.

## 5. Mass Assault / Soviet doctrine — detailed pass

### Root: `mass_assault`
The Soviet doctrine root is already structural rather than just numerical:
- SOV-only;
- `additional_brigade_column_size = 2`;
- -5% supply consumption;
- -10% minimum training level;
- `experience_loss_factor = 0.05`;
- costs the standard 100 Army XP.

**A / structural:** the +2 division-designer columns appears immediately at the root. As with `concentrated_fire_plans`, this must be balance-tested as a template-system change, not as a normal doctrine modifier. It materially changes how many battalions can be packed into one division and may alter optimal combat-width and support density.

The lower minimum training level is a very good Soviet mass-expansion lever in principle: it increases mobilization speed rather than directly improving combat quality. KEEP concept.

`experience_loss_factor = 0.05` should be engine-verified before balance changes. If positive values increase experience loss, it is a useful quality/quantity trade-off that offsets rapid expansion; if the sign behaves differently, reassess.

### Early defensive foundation
`pocket_defence`:
- +48 hours no-supply grace;
- -10% out-of-supply penalty;
- -5% pocket penalty.

`defence_in_depth`:
- +5 max entrenchment;
- +5 org to light infantry.

These are among the strongest thematic nodes in the land doctrines. They model operational resilience, encirclement tolerance and defensive depth without merely adding generic attack. KEEP direction.

### Deep-operations branch
`large_front_operations`:
- +5 org to front-line units;
- -5% supply consumption.

`deep_operations`:
- tanks +5 org and +5% soft/hard attack;
- -5% org loss while moving;
- unlocks Blitz.

`operational_concentration`:
- all artillery +5 org/+5% morale;
- all infantry +5 org;
- unlocks Barrage.

`vast_offensives`:
- another -5% supply consumption;
- +5 org to front line;
- +5% air-superiority combat bonus;
- unlocks Overwhelming Fire.

Preliminary verdict: the operational identity is strong, especially supply efficiency + movement-org retention + concentration. **B:** organization is nevertheless accumulating on very broad categories almost every other node. The branch should become better at sustaining operations primarily through supply, reinforcement, planning, movement-org retention and reserves rather than repeated +5 org to nearly everyone.

### Breakthrough / mechanized phase
`breakthrough_priority`:
- line artillery +5 org and +15% breakthrough;
- SP artillery +5 org and +20% breakthrough;
- tank destroyers +5 org and +20% breakthrough;
- unlocks Breakthrough tactic.

`mechanized_wave`:
- tanks +10% morale, +5 org, +1% initiative;
- SP artillery and TDs +5% morale, +5 org, +5% SA/HA.

This branch is conceptually useful because Soviet deep operations should eventually integrate armor, mobile artillery and exploitation forces. **B:** direct breakthrough on artillery/TD categories is very high and risks turning support/fire units into pseudo-tanks. Prefer some of this value as planning, coordination, reinforce, breakthrough for combined formations, or movement/recovery benefits rather than raw battalion breakthrough.

### `continuous_offensive`
- -15% org loss while moving;
- +5% reinforce rate;
- +5% max planning;
- front line +5% SA/HA;
- unlocks Backhand Blow.

This is one of the better late Soviet nodes. The combination of lower movement-org loss, reinforcement and planning expresses continuous operations much better than a generic stat package. The extra +5% universal front-line attack is the least interesting part and is a candidate for removal/reduction if cumulative attack inflation is excessive.

### People's Army branch
`peoples_army` is highly structural:
- military police can add +5 org to front-line categories;
- penal battalion +10 org;
- **militia combat width -0.45**;
- -10% attrition;
- +20% resistance damage to enemy garrisons on occupied Soviet states;
- Human Wave tactic.

**A / template-meta risk:** `militia combat_width = -0.45` is enormous. If this is a 45% width reduction, militia can potentially pack nearly twice as many battalions into the same combat frontage. This needs dedicated combat-width testing with actual militia stats/equipment/manpower before any doctrine balance conclusion. It can be either a brilliant mass-army identity mechanic or a severe template exploit depending on resulting damage/HP/org per width.

The attrition/resistance effects are thematic and preferable to generic attack bonuses.

`human_infantry_offensive`:
- light infantry +5% morale and +10% soft attack.

`large_front_offensive`:
- +5 org to all infantry;
- Relentless Assault tactic.

`human_wave_offensive`:
- +0.5% recruitable population;
- MP support gives +10% morale to all infantry.

`guerilla_warfare`:
- -10% out-of-supply penalty;
- +5% morale to the army;
- +20% resistance growth in occupied home states;
- Elastic Defense tactic.

This branch has a much clearer quantity/resilience identity than the generic late stat stacking seen in other doctrines. However, **B:** the +10% infantry soft attack and repeated morale/org gains still need cumulative comparison against the militia-width advantage. A 45% width reduction already supplies a potentially huge effective per-frontage combat multiplier; direct attack bonuses on top may be unnecessary.

### Final mechanized convergence: `masterful_blitz`
- all armor +5 org, +5% SA/HA/breakthrough;
- vehicle infantry +5 org, +10% morale, +1% initiative;
- Masterful Blitz tactic.

This makes sense as a mature Soviet operational-art endpoint, but its raw stat package overlaps heavily with German Mobile Warfare. Final differentiation should be:
- GER Mobile Warfare: faster local concentration, initiative, tactical penetration, command/signal, high-quality armored spearhead;
- SOV Deep Operations: larger operational depth, reserves, reinforce rate, supply tolerance, movement-org retention, follow-on echelons and continuous exploitation.

If both endpoints simply give armor org + attack + breakthrough, their historical identities converge mechanically.

### Mass Assault overall verdict
The Soviet tree is arguably the most structurally distinctive land doctrine currently in HER. Its strongest mechanics are not the raw combat buffs but:
- rapid deployment via lower training threshold;
- extra template columns;
- pocket/out-of-supply resilience;
- supply-consumption reductions;
- entrenchment/defense in depth;
- reduced org loss while moving;
- reinforce rate;
- militia-width manipulation;
- resistance/partisan effects;
- eventual mechanized exploitation.

KEEP these as the core identity.

Primary balance risks:
1. **A:** +2 template columns at doctrine root;
2. **A:** militia -45% combat width;
3. **B:** repeated +5 org across front line / infantry / artillery / armor;
4. **B:** very high breakthrough buffs for SPG/TD/artillery in `breakthrough_priority`;
5. **B:** late mechanized stats becoming too similar to German Mobile Warfare;
6. cumulative manpower/recruitable effects must be checked with Soviet laws/focuses rather than in isolation.

## 6. Cross-doctrine role comparison — preliminary

The desired mechanical identities now look clearer:

### German Mobile Warfare
Primary value should come from:
- local concentration and penetration;
- armored/mobile initiative;
- speed/operational tempo, but avoid excessive raw equipment-speed stacking;
- signal/recon integration;
- reduced movement-org loss;
- high-quality combined-arms spearheads;
- tactical flexibility / Blitz-family tactics.

### Soviet Mass Assault / Deep Operations
Primary value should come from:
- operational depth and multiple echelons;
- reserve/reinforce mechanics;
- supply tolerance and lower supply use;
- encirclement resilience;
- movement-org retention;
- large-front/template structure;
- quantity/resilience options;
- continuous mechanized exploitation late.

### Superior Firepower
Primary value should come from:
- artillery/fire-control efficiency;
- forward observers/recon;
- support integration;
- combined-arms fire coordination;
- air-land/fire-support synergy.

Avoid ending as a generic infantry+tank+artillery attack tree.

### Grand Battleplan
Primary value should come from:
- planning ceiling and deliberate preparation;
- command/control;
- entrenchment/defensive preparation;
- infiltration/night/terrain/special-force advantages;
- operational deception and controlled assaults.

Avoid excessive universal raw attack/breakthrough.

## 7. Cross-doctrine findings so far

### Strong design features to keep
- national-school doctrine gating;
- XP-based progression;
- tactic unlocks;
- support-company synergies;
- doctrine-specific planning / reinforce / command / air-ground interaction;
- explicit late-war German emergency-mobilization alternative;
- trade-offs such as central planning: slower planning accumulation but higher planning ceiling;
- Soviet pocket/supply/continuous-operation mechanics.

### Recurring problems
1. **Organization inflation.** +5/+10 org appears very frequently, often on broad categories. Cumulative doctrine-end org must be computed by formation type.
2. **Raw speed inflation.** Several doctrines give +5/+10% equipment/unit speed, overlapping chassis/engine/road/general effects.
3. **Support-company universalization.** Interesting battalion multipliers sometimes target `category_army` or other huge categories, turning a support company into a universal stat multiplier.
4. **Late-tree universal stat packages.** Branches often begin specialized but end with infantry + tanks + artillery + air interaction all improving together.
5. **Structural effects need separate balance treatment.** `additional_brigade_column_size = 2` and militia combat-width reduction can reshape the entire template meta and cannot be compared directly with normal percentage modifiers.
6. Doctrine balance should be assessed by historical formation archetype (foot infantry, artillery infantry, mechanized, armor, special forces, militia), not only total tree modifier sums.
7. German and Soviet late mechanized branches need deliberate differentiation so both do not converge on the same armor org/attack/breakthrough package.

## Next land-doctrine pass
- compute cumulative end-state packages for representative formation types;
- audit all support-company battalion multipliers and category scopes;
- test structural doctrine effects: extra columns and militia width;
- identify duplicate tactic unlocks and dead/inaccessible branch gates;
- then move to Air Doctrine and Naval Doctrine.
