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

## 5. Cross-doctrine findings so far

### Strong design features to keep
- national-school doctrine gating;
- XP-based progression;
- tactic unlocks;
- support-company synergies;
- doctrine-specific planning / reinforce / command / air-ground interaction;
- explicit late-war German emergency-mobilization alternative;
- trade-offs such as central planning: slower planning accumulation but higher planning ceiling.

### Recurring problems
1. **Organization inflation.** +5/+10 org appears very frequently, often on broad categories. Cumulative doctrine-end org must be computed by formation type.
2. **Raw speed inflation.** Several doctrines give +5/+10% equipment/unit speed, overlapping chassis/engine/road/general effects.
3. **Support-company universalization.** Interesting battalion multipliers sometimes target `category_army` or other huge categories, turning a support company into a universal stat multiplier.
4. **Late-tree universal stat packages.** Branches often begin specialized but end with infantry + tanks + artillery + air interaction all improving together.
5. **Structural effects need separate balance treatment.** `additional_brigade_column_size = 2` is not comparable to a normal 5–10% modifier and can reshape the entire template meta.
6. Doctrine balance should be assessed by historical formation archetype (foot infantry, artillery infantry, mechanized, armor, special forces), not only total tree modifier sums.

## Next land-doctrine pass
- finish Mass Assault/Soviet doctrine in detail;
- compute cumulative end-state packages for representative formation types;
- audit all support-company battalion multipliers and category scopes;
- identify duplicate tactic unlocks and dead/inaccessible branch gates;
- then move to Air Doctrine and Naval Doctrine.
