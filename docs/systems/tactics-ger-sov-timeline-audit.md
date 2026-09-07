# HER tactics audit — GER/SOV historical pool timeline

Status: **IN PROGRESS / TARGET TIMELINE**

This document complements `tactics-audit.md`, `tactics-unlocks-counters-audit.md` and `doctrine-audit.md`.

## Critical timing rule

HER land doctrines are XP-unlocked, not calendar-year technologies. Most nodes cost 100 Army XP. Therefore a label such as "1941 pool" is **not automatically guaranteed by the calendar**. It is a historical target / expected multiplayer state that must later be validated against actual Army XP income, focus-granted XP/cost modifiers and hands-off/player progression.

Do not hard-code conclusions from year labels until timing is tested.

## 1. Confirmed 1936 starting asymmetry

### Germany
`history/countries/GER - Germany.txt` starts with `mobile_warfare = 1`.

The Mobile Warfare root enables/unlocks `tactic_unexpected_thrust`.

Therefore Germany begins the game with a doctrine-specific maneuver tactic on top of the globally active/basic tactical pool.

Interpretation: this is appropriate. The German army should begin HER with a comparatively mature operational/tactical maneuver school rather than having to invent it from scratch after 1936.

### Soviet Union
`history/countries/SOV - Soviet union.txt` starts with `mass_assault = 1`.

The Mass Assault root itself does not unlock a special combat tactic. Its early effects instead emphasize supply economy, training threshold, formation structure and experience behavior.

Interpretation: also appropriate. The Soviet Union starts with a doctrinal/institutional framework but should not automatically possess the mature tactical execution of the 1943–45 Red Army.

This starting asymmetry is a strong HER design feature and should be preserved unless later timing tests show extreme gameplay distortion.

## 2. Globally available baseline pool

Before doctrine-specific unlocks, commanders can still draw from globally active tactics when their triggers are satisfied. Important examples include:
- Basic Attack;
- Shock;
- Encirclement (conditional);
- Flank Attack (requires actual flank);
- Basic Defend;
- Counterattack;
- Ambush (conditional/high-skill);
- Assault -> Close Combat phase;
- situational river/urban phase starters.

Therefore "no doctrine tactic" does not mean "no tactical competence". Doctrine expands and reshapes the pool rather than creating tactics from nothing.

## 3. Historical target snapshots

The snapshots below are **audit targets**, not yet confirmed save-state outputs.

### 1939 target

#### GER
Expected doctrine-specific core:
- Unexpected Thrust;
- Delay;
- Elastic Defense;
- likely Blitz if Armored Spearhead has been reached;
- Barrage is plausible by the Polish/French campaign transition, but its exact prewar timing requires XP testing.

Desired battlefield identity:
- strong local initiative;
- maneuver and exploitation;
- competent elastic/local defense;
- better ability than opponents to turn commander advantage into sophisticated tactics;
- not yet the full late-war Backhand Blow / fire-brigade defensive system.

#### SOV
Expected doctrine-specific pool should still be shallow.

Depending on branch choice/progression:
- early Deep Operations path may be approaching Blitz but should not automatically have the full Barrage -> Overwhelming Fire -> Breakthrough chain;
- People's Army path may unlock Human Wave relatively early, but this must not imply that all Soviet attacks are mass frontal assaults.

Desired battlefield identity:
- strong theoretical mass/depth concepts but uneven tactical execution;
- fewer sophisticated doctrine-specific tactical options than GER;
- larger dependence on commander quality, raw reserves and basic tactics.

### 1941 target

#### GER
Expected mature Barbarossa-era pool:
- Unexpected Thrust;
- Delay;
- Elastic Defense;
- Blitz;
- Barrage;
- Breakthrough;
- plus global Encirclement / Flank Attack / Ambush / Counterattack where triggers permit.

Backhand Blow should **not necessarily** be universal/fully mature yet; its exact timing should reflect the later development of mobile defensive practice and the tree's late placement.

Desired identity:
- widest and most reliable maneuver/penetration pool of the two armies;
- high-skill commanders frequently access sophisticated options;
- superior tactical responsiveness should come from skill/initiative/traits and pool composition rather than country-tagged free bonuses.

#### SOV
Expected June 1941 pool should be materially less mature in execution than GER even if doctrine theory is present.

Plausible Deep Operations progression:
- Blitz may be available;
- Barrage may be available or emerging depending on XP/focus timing;
- Overwhelming Fire / Breakthrough should be checked carefully and probably should not all be trivially online before Barbarossa.

People's Army progression may include:
- Human Wave;
- potentially Relentless Assault if heavily invested.

Desired identity:
- access to concepts does not equal German-level execution;
- low/medium commander quality should keep crude fallback tactics competitive in weight;
- high-quality Soviet commanders can outperform the institutional average, but the whole army must not play like 1944.

### 1943 target

#### GER
Expected pool:
- full early/mid Mobile Warfare package;
- Overwhelming Fire if Fire Brigades branch/focus gate has been reached;
- Backhand Blow increasingly available;
- strong Elastic Defense / Counterattack / Ambush interaction.

Desired identity:
- still tactically dangerous and often superior at local response;
- increasingly forced to use mobile defense/counterattack rather than only offensive penetration;
- reserve availability and fuel/logistics must constrain the practical use of high-end mobile-defense tactics.

#### SOV
Expected Deep Operations maturation:
- Blitz;
- Barrage;
- Overwhelming Fire;
- Breakthrough;
- increasingly strong reserve-dependent Relentless Assault / sustained offensive behavior depending on branch path;
- Backhand Blow possible only late in the deep branch and should represent growing operational sophistication, not simple imitation of Germany.

Desired identity:
- clear convergence in tactical competence versus 1941;
- strong artillery concentration and echelon/reserve interaction;
- Soviet superiority should increasingly come from sequencing and sustained operations rather than a single unbeatable tactic.

### 1945 target

#### GER
Expected surviving high-end pool can include:
- Blitz / Breakthrough / Barrage;
- Elastic Defense;
- Overwhelming Fire;
- Backhand Blow;
- possibly emergency Guerrilla tactics if the Volkssturm/Werwolf branch is taken.

But institutional degradation should be reflected outside the mere unlock list:
- lower average commander/formation quality after losses;
- weaker fuel/logistics/reserve availability;
- command centralization constraints;
- reduced ability to satisfy high-end tactic triggers consistently.

Important principle: **do not remove German learned tactics merely to simulate decline**. Make the late army less able to execute them reliably.

#### SOV
Expected mature pool:
- Barrage;
- Overwhelming Fire;
- Breakthrough;
- Backhand Blow through Continuous Offensive;
- Masterful Blitz replacing ordinary Blitz;
- Relentless Assault / other branch tools depending on doctrine path.

Desired identity:
- mature operational command;
- strong artillery + armor + reserve sequencing;
- excellent ability to sustain offensive tempo;
- less dependence on crude Human Wave behavior as commander quality and advanced options rise.

## 4. Critical asymmetry: Blitz -> Masterful Blitz replacement

`tactic_blitz` is disabled for an owner after `masterful_blitz` is researched.

This means the Soviet late-war pool does not simply add another option: it **replaces** ordinary Blitz with Masterful Blitz.

Current problem:
- ordinary Blitz is countered by Elastic Defense;
- Masterful Blitz has no explicit `countered_by` entry.

Therefore late Soviet progression changes not only magnitude but counter-network topology.

Severity: **A/B — architectural balance question**.

Do not add a counter until exact tactic initiative/counter behavior is verified and the desired 1944–45 Soviet advantage is defined.

## 5. Key GER-vs-SOV interpretation

The desired progression is not:

`GER strong -> SOV becomes same as GER`

It should be:

`1939–41 GER: superior local tactical execution and maneuver response`

`1942–43: Soviet rapid institutional catch-up; German local quality still dangerous`

`1944–45 SOV: mature deep-operational system with strong artillery, reserves, reinforcement and exploitation; GER retains learned tactical methods but increasingly lacks the material/institutional conditions to execute them consistently`

This distinction must be represented through:
- tactic pool;
- tactic weights;
- commander skill/traits;
- tactical initiative/recon;
- reserves;
- formation composition;
- fuel/supply;
- doctrine/focus modifiers;
- manpower-quality degradation.

## 6. Timing validation task

Before these year snapshots become `CONFIRMED-HER`, measure representative doctrine progression under actual HER conditions:

1. GER player/AI Army XP available by Sep 1939, May 1940, Jun 1941, Jul 1943, Jun 1944.
2. SOV player/AI Army XP available by Dec 1939, Jun 1941, Nov 1942, Jul 1943, Jun 1944.
3. Focuses/ideas that change land-doctrine XP cost or grant Army XP.
4. Typical chosen branch and node order.
5. Whether 100-XP node pricing causes too-early full trees or historically late options arriving too late.

Only after this test should year labels be converted from target snapshots into hard balance requirements.

## 7. Immediate next comparison

Overlay representative commanders on these pools:
- GER: Manstein, Guderian, Model (and optionally Rundstedt);
- SOV: Zhukov, Rokossovsky, Konev, Vasilevsky.

For each, map skill/personality/earned traits to actual tactic trigger and weight changes. This will show whether commander differentiation reinforces or contradicts the intended 1939–45 institutional progression.
