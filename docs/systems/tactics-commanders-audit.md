# HER Mod — Commander-to-Tactics Audit

Status: IN PROGRESS

Purpose: verify how actual commander `skill`, `skill_advantage` and traits interact with the combat-tactic weights and triggers. This pass focuses on GER and SOV headline commanders and checks whether their tactical behavior matches their intended historical role.

## 1. Systemic observation: tactic selection mostly ignores subskills

Current combat-tactic code mainly checks:
- overall `skill`;
- `skill_advantage`;
- traits such as `trickster`, `brilliant_strategist`, `panzer_leader`, `defensive_doctrine`, `inflexible_strategist`, etc.;
- unit composition / hardness / reserves / frontage / terrain.

`attack_skill`, `defense_skill`, `planning_skill` and `logistics_skill` generally do not directly alter tactic eligibility or weight.

This means a commander can have a very low defensive subskill but still be excellent at defensive tactic selection if his overall `skill` and traits satisfy the tactic logic. Conversely, a high planning subskill does not itself increase `Planned Attack`, `Planned Defense`, `Breakthrough`, or other planning-heavy tactics.

Verdict: **A / architecture review.** The four subskills are currently meaningful for combat modifiers, but they are underused as descriptors of tactical behavior. A later pass should decide whether selected tactics should receive modest subskill-based weight modifiers instead of relying almost entirely on overall skill.

Do not simply replace overall `skill`: overall experience/command competence should remain important. The likely best model is `overall skill + relevant subskill + traits + battlefield conditions`.

## 2. German commanders

### Erich von Manstein
Current profile:
- skill 8;
- attack 5 / defense 9 / planning 10 / logistics 8;
- `trickster`, `brilliant_strategist`, engineer-related traits, `expert_improviser`, `good_logist`;
- notably **no `panzer_leader`, `panzer_expert`, or `combined_arms_expert`**.

Mechanical behavior:
- **Unexpected Thrust:** strong fit; `trickster` adds weight.
- **Encirclement:** can use it through `skill_advantage > 1`; `trickster` adds further weight, but he cannot open the maneuver through `panzer_leader`/combined-arms composition alone.
- **Breakthrough:** can access through skill advantage with armor/artillery conditions, but gets no specialist panzer/artillery weight.
- **Blitz:** important limitation — for hard formations the tactic requires `panzer_leader`, while soft formations require `combined_arms_expert`. Manstein has neither. Therefore he cannot use ordinary Blitz merely because he is skill 8 or has a skill advantage.
- **Planned Attack / Planned Defense:** `brilliant_strategist` gives +4 weight, making these an excellent fit when unlocked.
- **Ambush:** `trickster` gives +4 weight if its trigger is otherwise satisfied.
- **Backhand Blow:** excellent fit: `trickster` +5 and `brilliant_strategist` +3; skill 8 satisfies the base trigger.

Verdict: **mostly historically convincing, with one design question.** Current Manstein behaves as a planner/opportunist/mobile-defense commander rather than a generic tank commander. That is arguably better than simply giving him `panzer_leader`. However, the total inability to select `Blitz` is worth reviewing: if Blitz represents rapid exploitation rather than tactical tank handling, a high-skill `brilliant_strategist + trickster` route could plausibly qualify at lower weight.

### Heinz Guderian
Current profile:
- skill 9;
- attack 14 / defense 3 / planning 8 / logistics 11;
- `trickster`, `brilliant_strategist`, `panzer_leader`, `armor_officer`, `expert_improviser`.

Mechanical behavior:
- **Encirclement:** naturally available in hard formations through `panzer_leader`; `trickster` adds weight.
- **Blitz:** near-ideal user: `panzer_leader` satisfies the main composition gate and skill >7 adds +4 weight.
- **Unexpected Thrust:** `trickster` boosts it.
- **Planned Attack:** `brilliant_strategist` boosts it if doctrine unlock is present.
- **Ambush:** surprisingly strong defensive access in hard formations: `panzer_leader` can satisfy the trigger and `trickster` adds +4 weight.
- **Backhand Blow:** skill 9 satisfies the trigger; `trickster` and `brilliant_strategist` make him very strong at it as well.

Verdict: **B/A interaction risk.** His offensive mobile profile is excellent, but the tactic system makes him much better at sophisticated defensive reactions than his `defense_skill = 3` suggests. This is the clearest example of why defensive subskill should probably affect defensive tactic weights.

Recommended direction: do not hard-ban Guderian from defensive tactics; instead apply modest negative/positive weight scaling from `defense_skill` so he can still improvise but does not rival Model in defensive choice quality merely through overall skill and panzer traits.

### Walter Model
Current profile:
- skill 10;
- attack 5 / defense 14 / planning 12 / logistics 9;
- `defensive_doctrine`, `inflexible_strategist`, `unyielding_defender`, `trait_cautious`, artillery/career traits.

Mechanical behavior:
- **Delay:** `defensive_doctrine` gives +5 weight.
- **Ambush:** soft formations can satisfy the trigger via `defensive_doctrine`; it also adds +3 weight.
- **Elastic Defense:** high overall skill alone makes it very likely; skill >7 and >9 stack major weight bonuses.
- **Backhand Blow:** skill 10 satisfies the general trigger, although he lacks `trickster`/`brilliant_strategist` specialist weight.
- **Breakthrough:** `inflexible_strategist` applies -4 weight, appropriately suppressing aggressive breakthrough choices.
- **Shock:** high skill progressively reduces weight, so he is less likely to use crude frontal attacks.

Verdict: **STRONG KEEP.** Of the reviewed commanders, Model's current profile maps most cleanly onto the existing tactic logic. His high defense/planning subskills are not what drive the choice, but his traits happen to compensate and produce the intended behavior.

### Gerd von Rundstedt
Current profile:
- skill 6;
- attack 2 / defense 8 / planning 9 / logistics 5;
- `skilled_staffer`, `expert_delegator`, `organizer`, `old_guard`, `trait_cautious`.

Mechanical behavior:
- few reviewed tactics directly reference his traits;
- his main tactical qualification comes from overall skill and skill advantage;
- can use Elastic Defense via skill >5 and Backhand Blow via skill >5 once unlocked;
- receives no special weight toward prepared/planned methods despite planning 9 and his staff/delegation profile.

Verdict: **under-expressed.** Rundstedt's stats say competent senior operational commander, but the tactic system sees mostly a generic skill-6 commander. This is another argument for limited use of `planning_skill` and possibly `skilled_staffer`/`expert_delegator` in weights of Planned Attack/Defense, reserve-based reactions, or operationally deliberate tactics.

## 3. Soviet commanders

### Georgy Zhukov
Current profile:
- skill 8;
- attack 7 / defense 9 / planning 9 / logistics 7;
- `trickster`, `organizer`, `skilled_staffer`, `good_logist`, `inflexible_strategist`, etc.

Mechanical behavior:
- **Encirclement:** can qualify through `skill_advantage > 1`; `trickster` adds +3 weight.
- **Breakthrough:** can qualify through skill advantage + armor/artillery, but `inflexible_strategist` applies -4 weight.
- **Masterful Blitz:** requires hardness >0.3, skill >4, and either `panzer_leader` or positive skill advantage. Zhukov lacks `panzer_leader`, so he only gets it when he has command advantage.
- **Ambush:** positive skill advantage can open it and `trickster` adds +4 weight.
- **Backhand Blow:** skill 8 opens it; `trickster` gives +5.
- high overall skill also suppresses crude Shock/Human Wave choices relative to weaker commanders.

Verdict: **mixed.** The system correctly makes Zhukov a high-skill opportunistic commander rather than a universal panzer specialist. However, `inflexible_strategist` directly penalizing Breakthrough is questionable for a commander whose historical role in HER should include massive, prepared breakthrough operations. This does not necessarily mean removing the personality trait; the tactic-specific -4 may be too broad.

Possible solution: keep `inflexible_strategist` as a personality/stat profile, but make its tactical penalty target improvisational or rapidly changing attack methods rather than prepared Breakthrough itself.

### Konstantin Rokossovsky
Current profile:
- skill 6;
- attack 4 / defense 6 / planning 8 / logistics 6;
- `brilliant_strategist`, `trait_cautious`.

Mechanical behavior:
- **Breakthrough:** can qualify through positive skill advantage + armor/artillery; no inflexible penalty.
- **Masterful Blitz:** requires positive skill advantage because he lacks `panzer_leader`.
- **Encirclement:** requires skill advantage >1 because he lacks panzer/combined-arms gate traits.
- **Backhand Blow:** skill >5 qualifies; `brilliant_strategist` adds +3 weight.
- **Planned Attack/Defense:** where unlocked, `brilliant_strategist` adds +4 and planning 8 conceptually fits, although planning skill itself is ignored.

Verdict: **good conceptual profile, slightly underpowered by trait plumbing.** Rokossovsky naturally fits deliberate planning and sophisticated operational reactions, but his high planning is invisible to tactic weights. A planning-skill modifier would help him without needing to stuff more personality traits onto the character.

### Ivan Konev
Current profile:
- skill 5;
- attack 4 / defense 6 / planning 6 / logistics 4;
- `inflexible_strategist`, `harsh_leader`, politically connected.

Mechanical behavior:
- skill 5 is only just above several advanced-tactic thresholds;
- `inflexible_strategist` applies -4 to Breakthrough;
- no `trickster`, `brilliant_strategist`, `panzer_leader`, or artillery specialist weight;
- can access Masterful Blitz only with positive skill advantage and the doctrine, but receives no specialist weight;
- advanced defensive/offensive choices are largely generic.

Verdict: **likely under-expressed for the late-war Konev we want HER to represent.** The current character looks much closer to a 1940-41 Konev than a 1944-45 front commander. If HER intentionally models growth through XP/earned traits, this can be acceptable — but we need to verify whether his actual in-game progression reliably reaches the intended late-war profile. Do not simply buff the starting file without checking trait growth and focus/event upgrades.

### Aleksandr Vasilevsky
Current profile when available as field marshal:
- skill 11;
- attack 7 / defense 12 / planning 17 / logistics 12;
- `brilliant_strategist`, `organizer`, `logistics_wizard`, career/infantry traits;
- explicitly commented as staff-oriented (`#ШТАБНОЙ`);
- late availability.

Mechanical behavior:
- very high overall skill makes generic advanced tactical choices highly available;
- `brilliant_strategist` boosts Backhand Blow and Planned Attack/Defense;
- but the extraordinary **planning 17 / logistics 12** do not directly affect tactic weights;
- thus much of what makes Vasilevsky unique in the character definition is invisible to tactical selection.

Verdict: **A / identity leakage.** Vasilevsky is the strongest proof that planning/logistics subskills deserve some presence in tactic weighting. His current tactical behavior is mostly "skill-11 brilliant strategist," not "exceptional staff/operational planner."

## 4. Comparative findings

### Mobile offensive behavior
- Guderian is mechanically the cleanest pure Blitz/Encirclement commander because `panzer_leader + trickster + skill 9` directly matches the tactic code.
- Manstein is better at Unexpected Thrust, Encirclement through advantage, planned methods and Backhand Blow, but cannot select ordinary Blitz without a missing gate trait.
- Zhukov/Rokossovsky can use late Soviet Masterful Blitz primarily through `skill_advantage`, not because their character identities specifically support mechanized exploitation.

This is not automatically wrong: Soviet late-war operational art should be less dependent on individual "panzer genius" traits and more on institutional doctrine, reserves and force structure. The key is ensuring skill advantage is not the only meaningful commander discriminator.

### Defensive behavior
- Model works extremely well because his traits directly map to Delay/Ambush and his high skill maps to Elastic Defense.
- Guderian is unintentionally too capable of sophisticated defensive tactics because defensive subskill is ignored.
- Manstein is very strong in Backhand Blow, which is desirable.
- Rundstedt is under-expressed because his planning/staff traits have little tactical influence.

### Prepared-operation behavior
- `brilliant_strategist` is currently the main personal marker for Planned Attack/Defense and Backhand Blow.
- planning skill itself does nothing to their weight.
- this makes Vasilevsky/Rokossovsky less distinct than their stat lines imply and makes any brilliant strategist with mediocre planning disproportionately similar.

## 5. Recommended architecture for next pass

Do **not** rebuild the system around subskills alone. Add small, capped weight modifiers to selected tactics:

- offensive exploitation / breakthrough tactics: modest `attack_skill` influence;
- Delay / Ambush / Elastic Defense: modest `defense_skill` influence;
- Planned Attack / Planned Defense / Backhand Blow / perhaps Encirclement: modest `planning_skill` influence;
- Tactical Withdrawal / reserve-heavy or sustained-operation tactics: modest `logistics_skill` or planning influence where historically sensible.

Suggested philosophy:
- traits define **style**;
- overall skill defines **general competence**;
- subskills refine **which complex choices a commander is best at**;
- doctrine determines **what the army institution knows how to do**;
- force composition / reserves / frontage / terrain determine **whether the method is feasible now**.

This would make the tactic system finally use the full commander model rather than treating the four subskills mostly as combat-stat outputs.

## 6. Immediate review flags

1. **Manstein vs Blitz gate** — decide whether total exclusion from ordinary Blitz is intended.
2. **Guderian defensive overperformance** — test Ambush/Backhand/Elastic frequency despite defense skill 3.
3. **Zhukov `inflexible_strategist` vs Breakthrough -4** — likely too broad for prepared breakthrough operations.
4. **Rundstedt under-expression** — planning/staff profile barely affects tactics.
5. **Vasilevsky identity leakage** — planning 17/logistics 12 should matter to tactical/operational selection somehow.
6. **Konev progression** — verify that in-game trait/skill growth converts his 1940-style starting profile into a plausible 1944-45 front commander before editing start stats.

Next audit step: inspect the trait definitions and commander progression paths to determine whether these mismatches should be fixed in `combat_tactics.txt`, in character traits, or through wartime progression/focus/event upgrades rather than static starting buffs.
