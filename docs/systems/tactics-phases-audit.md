# HER combat tactics phase audit

Status: **IN PROGRESS**

This appendix audits phase-changing combat tactics in `common/combat_tactics.txt` and should be read together with `tactics-audit.md`.

## 1. Phase architecture

`CONFIRMED-HER`

Current explicit phases:
- `close_combat`
- `tactical_withdrawal`
- `seize_bridge`
- `hold_bridge`
- `street_fighting`

Commented / currently inactive concepts:
- `mountain_pass_combat`
- `artillery_preparation`

The phase layer is valuable because it lets a battle change character rather than merely rerolling another flat modifier every tactic swap.

Working design rule:

> A phase should represent a materially different tactical state of the battle, with a distinct set of available actions and a clear way to enter/exit it.

## 2. Close Combat

### Entry: `tactic_assault`

`CONFIRMED-HER`

`tactic_assault` is available in normal combat with very low base weight (1), but strongly gains weight from:
- assault engineers;
- armored engineers;
- `aggressive_assaulter`;
- fort attack conditions.

It changes the phase to `close_combat` and gives a strong attacker bonus while reducing organization-damage effectiveness for both sides.

Preliminary verdict: **STRONG KEEP**.

This is a good phase-entry mechanic. Close combat is not random: engineers, fort assaults and aggressive commanders make it much more likely.

### Internal phase tactics

Attacker:
- `cc_attack` — common baseline, weight 25;
- `cc_storm` — rare high-intensity action, weight 5;
- `cc_withdraw` — rare phase exit, weight 5, returns to normal phase.

Defender:
- `cc_defend` — common baseline, weight 25;
- `cc_local_strong_point` — rare strong-point defense, weight 5.

Preliminary concern: **phase asymmetry**.

The attacker has an explicit exit (`cc_withdraw`), while the defender has no corresponding phase-changing action. That can be fine if phase duration and tactic swaps naturally let the attacker control disengagement, but it should be tested in-game so `close_combat` does not persist too long or end too randomly.

`cc_storm` gives +75% attacker and +75% defender simultaneously. This does not necessarily mean it is wrong: it can represent extremely intense short-range combat where both sides' combat power is high and defender org loss remains suppressed. Still, the meaning should be tested against actual combat results rather than read from attack/defense modifiers alone.

## 3. Tactical Withdrawal

### Entry: `tactic_tactical_withdrawal`

`CONFIRMED-HER`

The defender can enter the phase only from normal combat and requires either:
- positive `skill_advantage`, or
- `trickster`.

It reduces combat width heavily and penalizes both sides, especially the attacker.

Preliminary verdict: **STRONG KEEP**.

This is a genuinely command-driven defensive phase rather than a generic retreat button. It is also the direct counter to `Encirclement`, which gives it a clear operational role: avoiding fixation/destruction when an envelopment develops.

### Attacker actions inside withdrawal

- `tw_attack` — baseline pursuit pressure;
- `tw_chase` — lighter pursuit;
- `tw_intercept` — skilled interception, with weight from motorbike recon, commander skill and skill advantage. It returns combat to normal phase and gives a large attacker/movement advantage.

### Defender actions inside withdrawal

- `tw_defend` — baseline controlled withdrawal;
- `tw_evade` — more effective evasion, with weight from `trickster` and skill advantage; countered by `tw_intercept`.

Preliminary verdict: **one of the strongest phase designs in the file**.

This is a clean mini-game:

`tactical withdrawal -> evade / controlled withdrawal -> attacker chase -> skilled intercept can terminate withdrawal`

The use of recon in `tw_intercept` is especially appropriate and should be preserved.

Potential improvement later: test whether additional reconnaissance types should contribute, not only `motorbike_recon`.

## 4. River / bridge phases

The file implements two related but distinct phase states:
- `seize_bridge`
- `hold_bridge`

Both are only entered from river-crossing combat.

### 4.1 `Seize Bridge`

`tactic_seize_bridge` is an attacker phase entry with base weight 20.

Notable modifier:
- `pontoneer_support` gives **-10** weight.

Preliminary interpretation: **likely intentional, but document clearly**.

Pontoneers reduce dependence on capturing an intact bridge because the force can establish its own crossing. Therefore lower probability of `Seize Bridge` can make sense. This should not be "fixed" merely because the modifier is negative.

Inside the phase, attacker choices are:
- hold the bridgehead;
- skillful defense of the bridgehead.

Defender choices are:
- assault;
- reckless assault;
- retake bridge.

`defender_sb_retake_bridge` can return combat to normal phase and is enabled by commander advantage, `trickster`, engineer or pontoneer support. This is a good phase exit and gives the bridge fight a coherent objective.

### 4.2 `Hold Bridge`

`tactic_hold_bridge` is a defender phase entry from river-crossing combat.

**HIGH-PRIORITY TECHNICAL REVIEW:** its current direct effects are:
- `attacker_movement_speed = +0.1`
- `combat_width = -0.25`
- `attacker = +0.25`
- `defender = -0.1`

For a defender-selected tactic named `Hold Bridge`, these signs are counter-intuitive because they improve the attacking side and penalize the defender.

This may be intentional only if the tactic is meant to represent the defender committing to a vulnerable forward bridge position rather than successfully holding a crossing. The naming and the rest of the phase do not make that interpretation obvious.

Do **not** change yet. First verify:
1. whether `attacker`/`defender` modifiers in a defender-selected tactic use the same absolute side semantics as elsewhere (expected: yes);
2. whether these values were copied from an old design with inverted meanings;
3. actual in-game effect on the river battle.

Other `hold_bridge` phase tactics also contain unusual sign patterns:
- `defender_hb_hold`: attacker +20%, defender -10%;
- `defender_hb_skillful_defence`: attacker +10%, defender +5%.

These deserve the same technical test.

### 4.3 Phase transition loop

Attacker actions in `hold_bridge` can switch back to `seize_bridge`:
- `attacker_hb_storm`;
- `attacker_hb_take_bridge`.

The second is enabled by skill advantage, `trickster`, engineer or pontoneer support.

This creates an interesting loop:

`river crossing -> defender holds bridge -> attacker contests / takes bridge -> seize_bridge -> defender retakes -> normal combat`

Conceptually this is excellent, provided the phase modifiers themselves are correct.

## 5. Street Fighting

### Entry: `tactic_urban_defense`

`CONFIRMED-HER`

Only the defender initiates `street_fighting`, and only in urban terrain.

Weight rises with:
- province VP thresholds (>4, >9, >14);
- `urban_assault_specialist`;
- `trait_engineer`.

It changes the battle to `street_fighting`, slows the attacker and gives the defender a strong advantage.

Preliminary verdict: **STRONG KEEP, with trait-ID review**.

The VP scaling is especially good: larger/more important cities are more likely to turn into prolonged street battles.

Technical check required: verify that `trait_engineer` is the intended actual trait id and not a stale/wrong identifier.

### Attacker actions

- `sf_storm` — baseline urban assault;
- `sf_barrage` — artillery-heavy slow assault, doctrine-gated (`active = no`);
- `sf_armor_supported_assault` — requires flame tanks;
- `sf_mouse_holing` — requires assault/armored engineers and counters fortification.

This is a very strong composition-driven phase.

Notable strengths:
- flame tanks have a concrete tactical role rather than merely flat stats;
- assault engineers unlock a historically sensible house-to-house method;
- artillery has a distinct urban assault style.

### Defender actions

- `sf_defense` — baseline defense;
- `sf_fortify` — stronger positional defense, countered by mouse-holing;
- `sf_ambush` — very strong ambush tactic, doctrine-gated (`active = no`), also countered by mouse-holing.

Preliminary verdict: **STRONG KEEP**.

`Street Fighting` is probably the most complete phase-specific ecosystem in HER. It ties city importance, engineers, specialized armor and artillery to genuinely different tactical options.

## 6. Immediate findings / priorities

### Keep with minimal structural changes
- `Close Combat` entry through assault engineers / fort fighting;
- entire `Tactical Withdrawal` mini-system;
- `Street Fighting` composition logic;
- bridge-phase objective loop itself.

### High-priority technical checks
1. `hold_bridge` sign semantics and real combat effect;
2. `defender_hb_hold` / `defender_hb_skillful_defence` sign semantics;
3. `trait_engineer` actual trait identifier;
4. whether `tw_intercept` should recognize additional recon types;
5. phase duration / exit behavior for `close_combat`.

### Design conclusion

Phase mechanics should be retained and expanded cautiously. They are one of HER's best ways to represent battlefield state changes without adding arbitrary country-wide stat modifiers.

The strongest existing examples are:
- tactical withdrawal as an anti-envelopment command decision;
- urban street fighting as a composition- and city-dependent sub-battle;
- close combat as a fort/engineer-driven escalation.

The bridge system is conceptually promising but should be treated as **technically unverified** until the sign issue is tested.
