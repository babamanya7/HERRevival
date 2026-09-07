# HER defensive tactics audit addendum

Status: **IN PROGRESS**

This file is a working addendum to `docs/systems/tactics-audit.md`. It exists to preserve defensive-tactic findings while the broader tactics/command audit is still being assembled. Merge back into the main audit once the full tactic inventory/counter matrix is complete.

## Defensive role taxonomy

`CONFIRMED-HER`: current HER defensive tactics are already differentiated enough that they should not be balanced as interchangeable +defense rolls.

Working role split:
- `tactic_basic_defend` = generic passive baseline;
- `tactic_counterattack` = immediate active reaction / local reserve commitment;
- `tactic_delay` = trading ground/time while reducing attacker tempo;
- `tactic_ambush` = prepared/localized disruption of a shock attack;
- `tactic_elastic_defense` = absorb penetration, preserve force, slow exploitation;
- `tactic_backhand_blow` = higher-skill mobile counterstroke against a penetration;
- `tactic_guerrilla_tactics` = dispersed low-density resistance by light formations;
- `tactic_planned_defense` = prepared engineered positional defense;
- `tactic_overwhelming_fire` = artillery-heavy firepower response, especially against massed assault.

The distinction between `elastic_defense` and `backhand_blow` is especially important. Elastic defense should represent controlled yielding/absorption; backhand blow should represent deliberately allowing or exploiting an enemy penetration and then striking it with mobile reserves. They should not collapse into two numeric versions of the same tactic.

## Counterattack

`CONFIRMED-HER`

Availability:
- normal phase;
- defender;
- commander skill > 2;
- globally active.

Weight:
- base 10;
- +3 for each step of skill advantage from >0 through >3;
- +4 with reserves.

Effect:
- defender +35%;
- defender org-damage modifier +10%;
- countered by `tactic_barrage`.

Verdict: **KEEP architecture**.

This is a good generic active-defense tactic. Requiring modest commander competence while strongly rewarding reserves makes it read as a local counterattack rather than passive holding. It should remain widely available because local counterattacks were universal rather than uniquely German or Soviet.

Possible later refinement: reserve weighting may deserve more than +4 relative to large skill-advantage stacking if HER wants the physical availability of a fresh reserve to matter at least as much as commander superiority.

## Delay

`CONFIRMED-HER`

Availability:
- defender;
- normal phase;
- only while `frontage_full = no`;
- doctrine-gated (`active = no`).

Weight:
- base 10;
- +15 with reserves;
- +5 `defensive_doctrine`;
- +8 `guerilla_fighter`.

Effect:
- attacker movement -33%;
- attacker -35%;
- defender -15%;
- attacker org-damage modifier -15%;
- countered by `tactic_shock`.

Verdict: **STRONG KEEP, but verify semantics of reserves + frontage**.

The effect is coherent: both sides fight less efficiently while the attacker is slowed, which looks like trading space/time rather than trying to win a static firefight. The huge reserve weight is conceptually plausible if reserves mean successive delaying detachments / ability to rotate the front.

Audit question: because the trigger requires frontage not full while reserves strongly increase selection weight, verify in actual battles that this combination occurs as intended and does not produce odd cases where large reserve pools make a sparse front excessively good at delay.

## Ambush

`CONFIRMED-HER`

Availability:
- defender;
- normal phase;
- skill > 4;
- plus one of: positive skill advantage, `ambusher`, armored force under `panzer_leader`, or soft force under `defensive_doctrine`;
- globally active.

Weight strongly rewards `ambusher` (+8), `trickster` (+4), defensive doctrine, some hardness and skill advantage.

Effect:
- attacker -30%;
- defender +10%;
- attacker movement -25%;
- defender org-damage modifier +5%;
- counters `shock` and is countered by `breakthrough`.

Verdict: **KEEP concept, review global availability**.

The commander/formation logic is good. The main question is whether `active = yes` makes a fairly sophisticated ambush too universally available once a commander exceeds skill 4. Because the trigger still requires an additional competence condition, this is not an immediate problem, but the final unlock matrix should confirm whether doctrine-gating would improve institutional differentiation or merely over-script national armies.

## Elastic Defense

`CONFIRMED-HER`

Availability:
- defender in normal phase;
- requires either skill advantage > 0 or skill > 5;
- doctrine-gated.

Weight:
- base 15;
- rewards combined skill >5 + advantage;
- further skill advantage;
- reserves (+3);
- full frontage (+2);
- high skill >7 and >9 (+5 each).

Effect:
- attacker movement -25%;
- attacker -15%;
- defender +25%;
- attacker org-damage modifier -5%.

Verdict: **STRONG KEEP**.

This is structurally one of HER's best defensive tactics. It requires competent command and becomes much more likely under genuinely high-skill commanders. It does not require armor, which is correct for elastic-defense concepts broader than a pure armored counterstroke.

Important distinction to preserve: `elastic_defense` should represent controlled depth, yielding, and preservation of combat power. It should generally be safer and less decisive than `backhand_blow`.

## Backhand Blow

`CONFIRMED-HER`

Availability:
- defender in normal phase;
- skill >4;
- plus at least one of: skill >5, hard force + `panzer_leader`, skill advantage, or `trickster`;
- doctrine-gated.

Weight:
- base 5;
- +4 skill advantage >0;
- +4 additional at >1;
- +2 reserves;
- +2 hardness >0.2;
- +2 hardness >0.4;
- +5 `trickster`;
- +3 `brilliant_strategist`;
- +3 `reckless`;
- +4 if opponent is flanked.

Effect:
- attacker movement -33%;
- attacker -35%;
- defender +20%;
- defender org-damage modifier +5%.

Verdict: **KEEP concept, HIGH-PRIORITY differentiation/historical review**.

The current weighting correctly makes this a rarer, commander-sensitive maneuver rather than generic defense. It rewards mobile/hard formations, tactical deception, skill advantage and opportunities created by enemy overextension/flanking.

Two concerns:
1. `reckless` increasing the weight is mechanically understandable as willingness to launch an aggressive counterstroke, but historically this trait may blur reckless aggression with operational insight. Check whether `reckless` should increase frequency while also carrying some risk/cost elsewhere.
2. reserves only add +2, less than several commander modifiers. If backhand blow is meant to model a true mobile reserve counterstroke, the presence and character of reserves should likely be a central prerequisite/weight factor, not a secondary bonus.

This is the key tactic for later Wehrmacht 1939-43 / 1944-45 historical comparison. German superiority should emerge from commander quality, staff work, mobile reserves and doctrine availability—not from a permanent country tag.

## Guerrilla Tactics

`CONFIRMED-HER`

Availability:
- defender in normal phase;
- requires militia, irregular infantry, or infantry;
- prohibited if heavy infantry is present;
- doctrine-gated.

Weight:
- base 20;
- +5 `trickster`;
- +5 `guerilla_fighter`;
- +5 at artillery ratio <0.15;
- +5 more at <0.30;
- +5 hardness <0.4;
- +5 more at <0.2.

Effect:
- combat width -33%;
- attacker -55%;
- defender -25%;
- attacker org-damage modifier -10%;
- attacker movement -33%.

Verdict: **REVIEW trigger precision; effect concept is good**.

The tactic models dispersed, low-density resistance rather than a conventional stand-up defense, which is coherent. The problem is the OR trigger: ordinary infantry alone is enough to qualify. Unless the doctrine unlock is very restrictive, conventional infantry armies can potentially use a tactic intended for militia/irregular/partisan-style defense.

Likely refinement direction: preserve access for infantry only under additional contextual conditions (terrain, low artillery/hardness, guerrilla trait, specific doctrine/idea, or similar), while militia/irregulars can qualify more naturally.

## Planned Defense

`CONFIRMED-HER`

Availability:
- defender in normal phase;
- requires `engineer` unit type;
- plus either full frontage + reserves, skill advantage, or skill >5;
- doctrine-gated.

Weight scales with:
- skill advantage;
- artillery ratio;
- hardness;
- `brilliant_strategist`.

Effect:
- defender +40%;
- attacker movement -5%;
- defender org-damage modifier +5%.

Verdict: **STRONG KEEP**.

This is a clean representation of a prepared positional defense because it requires engineers and then rewards staff quality, artillery, combined arms and reserves. It is conceptually distinct from elastic defense: planned defense means hold a deliberately prepared position; elastic defense means absorb and trade depth.

Possible audit item: check whether `has_unit_type = engineer` means the intended engineer support/company presence in HER combat scope or unintentionally requires a specific combat battalion type. Verify against actual templates before changing anything.

## Overwhelming Fire

`CONFIRMED-HER`

Availability/weight mirrors `Barrage` logic through real artillery/heavy-artillery equipment concentration and/or `bearer_of_artillery` + artillery ratio.

Effect:
- attacker movement -75%;
- attacker -50%;
- defender +35%;
- attacker org-damage modifier -15%.

It exists specifically as the counter to `Banzai Charge` in comments/current matchup logic.

Verdict: **KEEP architecture, REVIEW scope beyond anti-Banzai role**.

The real-equipment concentration gating is excellent. However, an artillery-dense defensive fire plan is useful against much more than a Japanese mass charge. The tactic should be understood as concentrated defensive fires / firepower dominance, with Banzai Charge merely one attack it counters, not its sole historical reason to exist.

Its relationship with `Barrage` is also elegant: the same artillery concentration can produce an offensive fire-preparation tactic or a defensive overwhelming-fire tactic depending on battle side.

## Defensive counter architecture — preliminary

Current obvious counter relationships:
- `basic_attack` -> countered by `counterattack`;
- `shock` -> countered by `ambush`;
- `breakthrough` -> countered by `backhand_blow`;
- `blitz` -> countered by `elastic_defense`;
- `human_wave_tactics` / `flank_attack` -> countered by `planned_defense`;
- `banzai_charge` -> countered by `overwhelming_fire`;
- `counterattack` -> countered by `barrage`;
- `delay` -> countered by `shock`;
- `ambush` -> countered by `breakthrough`.

This is already close to a meaningful tactical ecology rather than a flat rock-paper-scissors table. Final audit should check for loops, orphan tactics and doctrine-unlock timing so that counters actually coexist in plausible periods.

## Preliminary defensive verdict

The defensive half of `combat_tactics.txt` is stronger than expected. The main structure should be preserved.

Highest-value follow-ups:
1. strengthen the physical-reserve meaning of `backhand_blow` if historical/engine testing supports it;
2. verify `delay` behavior with `frontage_full = no` + heavy reserve weighting;
3. tighten `guerrilla_tactics` so ordinary infantry does not qualify too generically;
4. verify engineer scope in `planned_defense`;
5. preserve a strict conceptual distinction between planned defense, elastic defense, local counterattack and backhand blow;
6. later map doctrine unlocks and GER/SOV commander traits onto these roles by period rather than by permanent national stereotypes.
