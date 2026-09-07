# HER combat tactics & command audit

Status: **IN PROGRESS**

Confidence labels:
- `CONFIRMED-HER` — verified directly in HER code/current gameplay model.
- `CONFIRMED-HOI4` — verified engine behavior / reliable documentation.
- `EXPERIMENTAL` — hypothesis or proposed interpretation requiring test.
- `OBSOLETE` — superseded finding.

## 1. Audit scope

This audit is deliberately separate from `doctrine-audit.md`.

Target chain:

`doctrine -> unlocked tactics -> tactic availability/weight/counters -> commander quality/traits -> formation composition -> reserves -> logistics -> operational outcome`

The purpose is not to make every army use equally strong tactics. HER should model genuine differences in military institutions and commander quality while avoiding caricatures such as "Germany always tactically superior" or "RKKA = human wave".

Historical comparison must be periodized:
- **1939-41**
- **1942-43**
- **1944-45**

Separate:
- military theory;
- institutional ability to execute it;
- tactical command;
- operational command;
- staff work / communications;
- reserves and echeloning;
- logistics;
- individual commander quality.

## 2. HER operational model — audit baseline

`CONFIRMED-HER` from current multiplayer behavior/design:

- A successful operation depends heavily on **reserves**.
- Breaking a deep echeloned defense is difficult; the attacker must progressively wear through successive defensive belts.
- Concentration of force is required for a serious breakthrough.
- Concentration is primarily constrained by **logistics**: supply throughput, ammunition, fuel, rail/hub capacity, trucks and ability to sustain several echelons in one sector.
- A powerful elite formation is not self-sufficient. A badly timed commitment or enemy counterattack can zero its organization; without fresh reserves it can then be defeated despite excellent nominal stats.
- Doctrine/tactic balance must therefore be evaluated as an operational sequence rather than by isolated division stats.

Useful conceptual sequence:

`concentration -> preparation -> first echelon -> defender reserve reaction -> second echelon -> counter-counterattack -> exploitation -> sustain corridor / continue operation`

This is a central criterion for all tactic judgments below.

## 3. Current HER tactics architecture

Primary file: `common/combat_tactics.txt`.

`CONFIRMED-HER`: HER substantially rewrites combat tactics rather than relying only on vanilla doctrine stat modifiers.

The tactic layer already uses:
- commander `skill`;
- `skill_advantage`;
- `has_reserves`;
- `frontage_full`;
- hardness;
- artillery ratio / artillery equipment concentration;
- terrain;
- flanking;
- commander traits;
- doctrine unlocks;
- tactic counters;
- battle-phase changes.

This means the intended doctrine/general/reserve interaction is already structurally present and should be refined rather than replaced.

### Engine-side selection model

`CONFIRMED-HOI4` (Paradox preferred-tactics design; exact current numeric implementation still to be verified against game defines/code behavior):
- available tactics have selection weights;
- national / field-marshal / general preferred tactics increase selection weight;
- tactical initiative determines which side selects second and therefore has an increased opportunity to select a counter;
- doctrine unlocks restrict the tactic pool.

Need to verify current HER/1.19 exact initiative/recon numbers before encoding them as hard audit rules.

## 4. Initial tactic findings

### 4.1 Breakthrough

`CONFIRMED-HER`

`tactic_breakthrough` is not a generic attack roll. Availability already requires a meaningful command/formation condition: full frontage, commander skill > 4 and either armored/combined-arms/artillery competence or a skill advantage.

Its weight increases with:
- `panzer_expert` / `combined_arms_expert`;
- `bearer_of_artillery`;
- artillery ratio;
- **reserves**;
- plains;
- successive levels of `skill_advantage`;
- high commander skill.

`inflexible_strategist` reduces its weight.

Effect:
- major attacker combat bonus;
- defender penalty;
- movement acceleration;
- reduced attacker org-damage pressure;
- countered by `tactic_backhand_blow`.

Preliminary verdict: **KEEP architecture**. This is a good HER example of a tactic representing an operationally prepared breakthrough rather than a free combat buff.

### 4.2 Blitz / Masterful Blitz

`CONFIRMED-HER`

Regular `tactic_blitz` is strongly associated with armored/combined-arms command and benefits from reserves + a filled frontage, commander skill and skill advantage. It is disabled once `masterful_blitz` is researched.

`masterful_blitz` is explicitly presented as an improved Soviet Blitz. It requires:
- SOV visibility;
- hardness > 0.3;
- skill > 4;
- panzer leadership or skill advantage.

Its weight again rises with reserves/full frontage, high skill and skill advantage.

Preliminary concern **A/B — historical role, not raw power**:
- the mature Soviet operational school should absolutely gain a powerful mobile exploitation tactic;
- however, we must verify whether an essentially stronger one-shot `Blitz` is the best historical representation, or whether part of Soviet superiority in 1943-45 should emerge from sequencing artillery preparation, echelon commitment, reserve introduction and operational exploitation.

Do **not** nerf it merely because the numeric combat bonus is large.

### 4.3 Human Wave

`CONFIRMED-HER`

`tactic_human_wave_tactics` is much subtler than its name suggests in current code:
- requires full frontage and low hardness;
- weight rises with reserves and very soft / artillery-light forces;
- weight is reduced at high commander skill (`skill > 7`, further at `> 9`);
- SOV gets a small extra weight;
- before `masterful_blitz`, it receives a larger additional weight.

This effectively creates an institutional transition: crude mass assault is more likely with low-quality/early command conditions and loses relative prominence as command quality and mature mobile doctrine improve.

Preliminary verdict: **KEEP concept, HISTORICAL REVIEW REQUIRED**.

Main question is terminology and periodization. "Human wave" risks encoding a popular-history caricature if the actual modeled behavior is better described as poorly coordinated massed infantry assault / frontal assault under weak command.

### 4.4 Relentless Assault

`CONFIRMED-HER`

Deep Battle attacker tactic. Its selection weight rises heavily with **reserves** (+10) and full frontage (+5), plus Soviet/doctrinal weighting.

Preliminary verdict: **STRONG KEEP candidate**.

This directly expresses HER's operational model: the ability to continue pressure after the first echelon has engaged is conditional on actual reserves, not merely a flat national attack bonus.

### 4.5 Barrage

`CONFIRMED-HER`

Barrage availability/weight depends on actual artillery/heavy-artillery concentration and/or `bearer_of_artillery`, with progressive weight increases at higher artillery concentration.

It strongly suppresses the defender and defender organization but slows attacker movement while the barrage is underway.

Preliminary verdict: **KEEP architecture; audit magnitude + sequencing**.

The use of actual equipment concentration is excellent. Historical audit should determine whether the tactic should be a stand-alone combat state or feed into a preparation/breakthrough sequence.

### 4.6 Defensive tactics and reserves

`CONFIRMED-HER`

Current defense is also reserve-sensitive:
- `counterattack` gets substantial weight from reserves;
- `delay` gets a very large reserve weight bonus;
- `elastic_defense` gets reserve and full-frontage bonuses;
- `backhand_blow` gets reserve weighting and strongly rewards skill advantage / trickster / brilliant-strategist characteristics.

This is important: reserves in HER are not merely extra divisions waiting to reinforce. They already alter the commander's tactical option distribution.

Preliminary verdict: **core system worth preserving**.

## 5. Historical questions to answer

### Wehrmacht
For each period, establish evidence for:
- mission command / Auftragstaktik in actual field practice;
- subordinate initiative and quality of NCO/officer cadre;
- Schwerpunkt and local concentration;
- combined-arms execution;
- local counterattack / mobile defense;
- reconnaissance and communications;
- staff-work quality;
- reserve employment;
- effects of casualties, cadre dilution, fuel/logistics and command centralization by 1944-45.

### RKKA
For each period, separate doctrine from execution:
- prewar Deep Battle theory;
- 1941 command/communications/reorganization failures;
- rebuilding of staffs and command cadres;
- artillery planning and concentration;
- echeloning and operational reserves;
- maskirovka;
- front/army-level operational planning;
- mobile groups / exploitation;
- degree of lower-level initiative vs centralized control;
- 1943-45 improvement and remaining weaknesses.

## 6. General-system overlay

The commander audit must not reduce a general to one stat or one trait.

For each important GER/SOV general, inspect:
- skill and four HER attributes;
- personality traits;
- earned traits;
- preferred tactic, if any / if assigned through the current system;
- which tactic triggers and weight modifiers those traits satisfy;
- whether the general's historical strengths match the tactical opportunities the game gives him.

HER stat interpretation currently used in the project:
- Attack = mechanized/tank competence;
- Defense = infantry/artillery competence;
- Planning = operational thinking;
- Logistics = initiative/flexibility/self-reliance.

These mappings must be tested against tactic mechanics rather than assumed to be sufficient by themselves.

## 7. Immediate audit tasks

1. Inventory every tactic and phase in `common/combat_tactics.txt`.
2. Build full counter matrix.
3. Build unlock-source matrix from `land_doctrine.txt` and any focuses/events/traits.
4. Map every tactic trigger/weight modifier to commander traits and formation properties.
5. Verify exact HOI4 1.19 tactic selection / initiative / preferred-tactic behavior.
6. Historical research by 1939-41 / 1942-43 / 1944-45.
7. Overlay representative Wehrmacht and RKKA generals.
8. Only then propose balance/code changes.

## 8. Current high-level verdict

The existing HER tactic system is **not a throwaway vanilla layer**. It already encodes reserves, command skill, artillery concentration, formation hardness, flanking and specialized traits in ways consistent with HER's operational combat philosophy.

The main audit problem is therefore not "make tactics more complex". It is:

> preserve the strong existing operational structure while moving every tactic and commander interaction onto the thinnest defensible line between historical differentiation and historical caricature.
