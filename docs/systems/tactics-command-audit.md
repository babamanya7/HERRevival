# HER Tactics & Command Audit

Status: **IN PROGRESS**

This audit is deliberately separate from `doctrine-audit.md`. Land doctrines cannot be evaluated only through their passive modifiers because HER combat tactics are already coupled to commander quality, force composition, frontage, reserves and battlefield situation.

## Audit principle

The working HER combat model is:

`doctrine -> unlocked tactics -> commander capability -> force composition -> frontage/reserves -> logistics -> tactical result -> operational continuation`

A strong division is not an automatic breakthrough. In HER a breakthrough against echeloned defence requires local concentration, reserves and the logistics to sustain them. A failed or mistimed commitment can leave even elite formations at near-zero organisation and vulnerable to counterattack.

Therefore tactics must be judged by their effect on the **operation**, not only by their displayed combat modifier.

## Historical comparison framework

Do **not** model the German–Soviet difference as a simple "German generals good / Soviet generals bad" axis.

Evaluate separately:

1. **Tactical initiative / subordinate autonomy**
2. **Speed of local decision and adaptation**
3. **Staff planning and operational preparation**
4. **Command-and-control / communications**
5. **Concentration of forces and fires**
6. **Reserve management / echelon commitment**
7. **Artillery coordination**
8. **Exploitation after breakthrough**
9. **Ability to sustain tempo under logistical strain**
10. **Historical evolution over time**

### Wehrmacht target profile

`CONFIRMED-HISTORICAL (framework)`

The German command tradition, especially in the early/mid war army, should receive a meaningful advantage in tactical initiative, rapid local adaptation and decentralized execution. Auftragstaktik was tied to competent subordinate leadership and was particularly valuable in Bewegungskrieg.

This must **not** become a generic German bonus to every level of war. Decentralized initiative could also create coordination problems at higher operational levels, and German command quality degraded as the war consumed experienced officers/NCOs and political interference increased.

Gameplay implication: German commanders should be unusually good at exploiting a changing local situation — unexpected thrusts, flank attacks, mobile counterstrokes, blitz/exploitation — especially when the commander and formation are appropriate.

### RKKA target profile

`CONFIRMED-HISTORICAL (framework)`

The Red Army must be modeled dynamically rather than from a frozen 1941 stereotype. The 1941 force suffered severe problems in command, communications, staff work and initiative. By 1943–45 the RKKA had developed formidable operational capabilities: concentration, massed fires, deception, echeloning, reserve commitment, breakthrough organization and exploitation in depth.

Gameplay implication: Soviet command quality should evolve from early-war fragility toward strong prepared/operational tactics. The mature RKKA should be particularly effective when it has prepared the battlefield, concentrated artillery and forces, retained reserves and can sustain successive echelons.

The Soviet advantage should therefore not simply copy German low-level tactical initiative.

## Current HER system — first pass

Source: `common/combat_tactics.txt`.

### Structural finding: reserves already matter

`CONFIRMED-HER`

`has_reserves = yes` affects the weight or availability of many important tactics, including:

- `tactic_encirclement`
- `tactic_breakthrough`
- `tactic_blitz`
- `tactic_human_wave_tactics`
- `tactic_planned_attack`
- `tactic_relentless_assault`
- `tactic_flank_attack`
- `tactic_unexpected_thrust`
- `tactic_counterattack`
- `tactic_delay`
- `tactic_elastic_defense`
- `tactic_backhand_blow`
- `tactic_planned_defense`

This is a major strength of the HER system. It connects tactical outcomes to the same reserve/echelon problem that dominates actual HER operations.

**Verdict: KEEP as a core design principle.**

### Structural finding: commander quality already changes tactic selection

`CONFIRMED-HER`

The system heavily uses:

- `skill`
- `skill_advantage`
- personality/earned traits
- formation hardness
- artillery ratio
- frontage state
- flanking state
- terrain

This means commander quality is not merely a passive stat multiplier: it changes the probability of tactical choices.

**Verdict: KEEP and expand deliberately rather than replacing.**

## Offensive tactics — first findings

### Basic Attack

`tactic_basic_attack`
- base weight 50
- attacker +15%
- countered by Counterattack

This is the neutral fallback. Its high base weight is useful because specialist tactics need to earn their probability through commander/formation/situation conditions.

### Encirclement

`tactic_encirclement`
- requires full frontage
- requires combined-arms/panzer suitability or skill advantage
- weight rises with Panzer/Combined Arms expertise, flanking, reserves, Trickster, plains and skill advantage
- combat width +100%
- attacker +75%
- defender -10%
- attacker org damage -15%
- countered by Tactical Withdrawal

**Preliminary verdict: GOOD CONCEPT.**

It represents a high-payoff maneuver rather than a generic attack button. The explicit links to flank state, reserves and commander superiority are exactly the direction wanted for HER.

Audit later: verify whether `combat_width = 1` is multiplicative/appropriate and whether the payoff is too binary when it fires.

### Shock

`tactic_shock`
- base 30
- Aggressive Assaulter increases weight
- increasing commander skill progressively **reduces** its weight
- attacker +35%, defender -20%
- attacker org damage +5%
- countered by Ambush

**Preliminary verdict: STRONG DESIGN IDEA.**

A blunt shock attack becoming less attractive to sophisticated commanders is a clever way of representing quality through tactic selection rather than raw stat superiority.

Audit later: determine whether the skill penalties decay the weight too far for historically competent commanders who deliberately used shock action when appropriate.

### Breakthrough

`tactic_breakthrough`
- doctrine-locked (`active = no`)
- requires full frontage and skill >4
- access depends on armor/combined-arms/artillery capability and commander advantage/traits
- weight rises strongly with artillery concentration, reserves, skill advantage and high skill
- Inflexible Strategist reduces weight
- +50% movement, +65% attacker, -15% defender
- attacker org damage -5%
- countered by Backhand Blow

**Preliminary verdict: EXCELLENT SYSTEMIC FIT.**

This is already close to the desired HER breakthrough model: adequate commander + concentrated force + artillery/armor + reserves.

### Blitz

`tactic_blitz`
- doctrine-locked
- requires suitable mobile/combined-arms commander and a situational advantage (skill/frontage/reserves/etc.)
- weight rises with commander expertise, reserves plus full frontage, plains and skill advantage
- +50% movement, +50% attacker, -20% defender
- attacker org damage +10%
- countered by Elastic Defense
- removed once the Soviet `masterful_blitz` technology exists

**Preliminary verdict: GOOD.**

It rewards tactical/mobile command quality. It should become a key point in the Wehrmacht vs RKKA historical overlay.

### Human Wave

`tactic_human_wave_tactics`
- infantry/soft formation and full frontage
- strongly prefers reserves, very low hardness and low artillery ratio
- high commander skill reduces its weight substantially
- Soviet owner gets a small extra weight
- +50% combat width, +30% attack, +15% defense, +5% attacker org damage
- countered by Planned Defense

**Preliminary verdict: NEEDS HISTORICAL REVIEW, NOT AUTOMATIC REMOVAL.**

The existing logic is more nuanced than the name: it models an unsophisticated mass attack that good commanders increasingly avoid. This is mechanically coherent, but care is needed not to make "Human Wave" a defining Soviet combat behavior once the RKKA has matured.

### Planned Attack

`tactic_planned_attack`
- doctrine-locked
- relies on frontage + reserves, skill advantage or high skill
- gains weight from artillery, hardness and Brilliant Strategist
- attacker +40%
- slight movement bonus

**Preliminary verdict: GOOD candidate for staff/operational quality.**

This may be a better home than generic attack bonuses for commanders known for deliberate preparation.

### Relentless Assault

`tactic_relentless_assault`
- Deep Battle attack tactic
- base 10
- +5 full frontage
- **+10 reserves**
- +4 Soviet owner
- attacker +35%, defender +15%
- movement +20%
- attacker org damage +5%, defender org damage -10%

**Preliminary verdict: VERY IMPORTANT.**

This is one of the clearest existing links between Soviet doctrine and the HER reserve/echelon model. It should be evaluated as a sustained-pressure tactic, not as a simple attack buff.

### Flank Attack

`tactic_flank_attack`
- requires an actual flanked opponent
- benefits from mobile hardness, Panzer/Combined Arms traits, Trickster, reserves and skill advantage
- +25% combat width, +35% attack, -15% defender

**Preliminary verdict: KEEP.**

This is exactly the kind of local situational tactic where German early-war command culture can appear through commander distribution rather than a country-wide hardcoded bonus.

### Unexpected Thrust

`tactic_unexpected_thrust`
- Mobile Warfare doctrine tactic
- weight rises with Panzer/Combined Arms expertise, flanking, reserves, Trickster, plains and skill advantage
- +15% movement, +30% attack
- attacker org damage +10%

**Preliminary verdict: KEEP.**

Strong candidate for the distinctive early/mid-war German tactical-command profile.

### Barrage

`tactic_barrage`
- doctrine-locked
- availability and weight are tied directly to actual artillery/heavy-artillery equipment density and `bearer_of_artillery`
- movement -75%
- attacker +35%, defender -50%
- defender org damage -15%

**Preliminary verdict: EXCELLENT CONCEPT / NUMBERS TO TEST.**

This is exactly the desired connection between material concentration and tactical behavior. The tactic does not appear merely because a doctrine says "artillery good"; the force must actually possess enough artillery.

The commented `tactic_back_hop` ("German 1944 antisoviet artillery tactic") is a useful future audit lead; do not implement it until historical evidence and gameplay role are clear.

### Masterful Blitz

`tactic_masterful_blitz`
- Soviet-only display
- requires >30% hardness, skill >4, and Panzer Leader or skill advantage
- improves with reserves/full frontage and commander advantage
- +50% movement, +55% attacker, -15% defender
- attacker org damage +5%, defender org damage -10%

**Preliminary verdict: HISTORICALLY PROMISING.**

It can represent the mature Soviet capability to exploit breakthroughs with mechanized forces. It should not imply that Soviet low-level mission command simply became German Auftragstaktik; its availability should remain tied to mature doctrine, commander quality and prepared operational conditions.

## Defensive tactics — first findings

### Counterattack

- requires skill >2
- weight rises sharply with skill advantage and reserves
- defender +35%
- defender org damage +10%

**KEEP.** Reserves are correctly central to counterattack capability.

### Delay

- requires incomplete frontage
- reserves provide a very large +15 weight
- Defensive Doctrine +5, Guerrilla Fighter +8
- attacker movement -33%, attacker -35%

**KEEP / important operational-defense tactic.**

### Ambush

- requires skill >4 plus advantage/appropriate traits
- strongly favors Ambusher, Trickster and defensive competence
- attacker -30%, movement -25%

**KEEP.** Good example of commander differentiation.

### Elastic Defense

- doctrine-locked
- requires commander skill/advantage
- reserves, full frontage and higher skill raise weight
- attacker movement -25%, attacker -15%, defender +25%

**KEEP.** Natural counterpart to Blitz and a good place to model high-quality mobile defense.

### Backhand Blow

- doctrine-locked
- requires a capable commander
- weight rises with skill advantage, reserves, hardness, Trickster, Brilliant Strategist, Reckless and actual flanking
- attacker movement -33%, attacker -35%, defender +20%

**High-priority historical audit item.**

The tactic is powerful and appears in both German and Soviet doctrine progression. We need to distinguish the German concept/history from later Soviet operational counterstroke capability rather than treating the label as nationally neutral without thought.

### Planned Defense

- requires engineers
- requires frontage/reserves or commander superiority/high skill
- artillery, hardness and Brilliant Strategist raise weight
- defender +40%

**KEEP concept.** Strong candidate for prepared, staff-heavy defense.

### Overwhelming Fire

- artillery-dependent defensive tactic using actual artillery/heavy-artillery equipment thresholds
- weight scales with artillery ratio and Bearer of Artillery
- attacker movement -75%, attacker -50%, defender +35%

**KEEP concept / test numbers.** Like Barrage, this makes artillery organization materially visible in tactic selection.

## Combat phases

HER uses additional phases beyond the default exchange:

- `close_combat`
- `tactical_withdrawal`
- `seize_bridge`
- `hold_bridge`
- `street_fighting`

This is important: the tactics audit must include **phase transitions**, because a tactic that moves combat into a special phase can be much stronger or weaker than its immediate modifiers suggest.

`assault`, for example, opens `close_combat` and is weighted by assault/armored engineers, Aggressive Assaulter and fort-attack context. Close-combat follow-up tactics then alter both sides' combat and org-damage profile.

## Commander-system integration

Source family: `common/unit_leader/*`.

HER already has a rich custom commander model. The tactics file directly checks traits including:

- `panzer_leader`
- `panzer_expert`
- `combined_arms_expert`
- `bearer_of_artillery`
- `trickster`
- `aggressive_assaulter`
- `brilliant_strategist`
- `inflexible_strategist`
- `defensive_doctrine`
- `guerilla_fighter`
- `ambusher`
- `reckless`

This confirms that doctrine and general audits cannot remain independent.

### Important existing examples

`brilliant_strategist` in HER heavily raises planning/attack competence and receives direct tactic weight synergy in Planned Attack, Planned Defense and Backhand Blow.

`inflexible_strategist` reduces Breakthrough tactic weight by 4 while its stat profile favors defense/planning and penalizes logistics/initiative. This is a good example of a personality trait affecting **decision quality**, not merely passive combat stats.

**Design rule:** when historically justified, prefer commander traits changing the probability/availability of fitting tactics over merely stacking more generic attack/defense.

## Historical evidence baseline

Sources to retain for the next pass:

- U.S. Army Combat Studies Institute / Army University Press, Martin Sonnenberger, *Initiative Within the Philosophy of Auftragstaktik* (2015): Auftragstaktik emphasizes subordinate initiative within commander intent and adaptation to fundamental changes in the situation.
- Army University Press, *The U.S. Army and Mission Command: Philosophy versus Practice* (2018): Truppenführung and German leader development explicitly connected independent decisive action to Bewegungskrieg.
- Army University Press, *History, Mission Command, and the Auftragstaktik Infatuation* (2022): useful corrective against treating German decentralized command as universally superior, especially above the tactical level.
- Army University Press / Combat Studies Institute, *Deep Operations: Theoretical Approaches to Fighting Deep* (2021): Red Army performance from Kursk onward showed rapid maturation in shock, massed fires, deception, simultaneous actions, depth and exploitation; Bagration is a key case.

## Preliminary historical model for HER

### Germany 1939–42

Advantages should emerge mostly through:
- higher distribution of capable commanders
- traits that favor mobile/local adaptive tactics
- skill advantage
- tactical flanking and exploitation
- faster tactical response
- better use of Blitz / Unexpected Thrust / Encirclement / mobile Counterattack

Not through a universal "German tactic bonus".

### USSR 1941

Weakness should emerge through:
- poorer average commander distribution after purges/expansion
- weaker communications/initiative representation
- less frequent access to sophisticated tactics through skill/trait requirements
- organizational/focus/idea debuffs where already appropriate

Avoid hardcoding ahistorical permanent incompetence into Soviet tactics themselves.

### USSR 1943–45

Strength should increasingly emerge through:
- doctrine unlocks
- improved surviving/promoted commander pool
- artillery concentration
- reserves/echelons
- full frontage/preparation
- Relentless Assault / Barrage / Breakthrough / Masterful Blitz / counterstroke capabilities
- logistical and org-retention systems that let successive echelons continue the operation

This creates historical convergence in overall combat effectiveness **without making the command cultures identical**.

## High-priority audit questions

1. Build the complete tactic inventory and counter graph.
2. Identify tactics with no counters, dead counters or dead unlocks.
3. Audit every `active = no` tactic against doctrine/focus/event unlocks.
4. Audit `skill` and `skill_advantage` thresholds against HER's unusually high commander skill scale.
5. Quantify how much `has_reserves` changes selection probabilities in representative combats.
6. Audit actual German and Soviet general trait distributions by year/rank.
7. Check whether German tactical superiority is already emergent from the general roster or is being double-counted by doctrine/tactic rules.
8. Check whether Soviet 1943–45 maturation emerges naturally from doctrine + commander progression or needs explicit historical progression.
9. Audit special combat phases (`close_combat`, `tactical_withdrawal`, bridges, street fighting) separately.
10. Test the whole system against HER's real combat environment: deep defense, high lethality, reserve rotations, concentration and logistics.

## Current verdict

The tactics system should **not** be simplified. Its existing architecture is one of HER's strongest foundations: commander quality, reserves, force composition and doctrine already interact meaningfully.

The task is to calibrate historical identities and probability weights, eliminate dead/broken interactions, and make the 1939–45 evolution of German and Soviet command cultures emerge from the system rather than from stereotypes.
