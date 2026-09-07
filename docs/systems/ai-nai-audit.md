# HER AI — NAI Defines Audit

Status: PRE-HANDS-OFF AUDIT
Branch: `AI-rework`
Date: 2026-09-07

## Goal

Audit the global `NAI` block in `common/defines/00_defines.lua` after the scripted AI, strategy plans, naval goals and division-template passes. The goal is not to make the AI globally stronger by brute force, but to remove engine-level behavior that can undermine the new country-specific scripting.

## Confirmed pre-run changes

These values are suitable to change before hands-off test #1 because they address generic AI pathologies rather than country balance.

1. `AI_TASKFORCE_REQUIRED_RESERVE_RATIO = 0.20 -> 0.10`
   - Current task-force templates already require real minimum compositions.
   - Keeping 20% of required optimal composition in reserve can strand too many usable ships in reserve and reduce the number of active task forces.
   - 10% still retains replacement reserve while allowing the new naval-goal system to field more operational groups.

2. `NAVAL_MISSION_AGGRESSIVE_ESCORT_DIVISOR = 2.0 -> 1.25`
   - The current value halves convoy-escort scoring outside a defensive posture.
   - This directly conflicts with the HER objective that ENG/USA actively protect long oceanic routes while conducting wider offensive operations.
   - 1.25 retains a posture penalty without making escort an afterthought.

3. `CONSTRUCTION_PRIO_FACTOR_REPAIRING = 0.0 -> 0.30`
   - A zero multiplier effectively sends damaged construction/repair items to the bottom of the AI construction queue.
   - This is especially harmful under strategic bombing and on the Eastern Front where railways, infrastructure, ports and factories take repeated damage.
   - 0.30 is a conservative value also seen in vanilla-derived/strong-AI implementations: repair remains below fresh core construction, but is no longer ignored.

4. `RELATIVE_STRENGTH_TO_INVADE = 0.0 -> 0.08`
5. `RELATIVE_STRENGTH_TO_INVADE_DEFENSIVE = 0.0 -> 0.40`
   - Zero disables the generic relative-strength safety filter for invasions.
   - HER now has explicit USA/JAP/ENG/ITA invasion strategies and naval-goal support, so the global engine no longer needs to be told to ignore force balance entirely.
   - Restoring a weak general threshold should reduce suicidal opportunistic invasions while scripted high-priority operations remain possible.

## Values reviewed and intentionally NOT changed before test #1

### `PLAN_VALUE_TO_EXECUTE = -0.61`

This looked extreme at first glance, but public vanilla-derived files commonly place the baseline around `-0.5`, and other AI mods use `-0.61`. The difference is modest rather than a fundamental "attack regardless of odds" switch. Leave it unchanged for the first baseline and judge actual battle-plan behavior together with the country-specific careful/aggressive strategy phases.

### `PLAN_ACTIVATION_SUPERIORITY_AGGRO = 1.75`

Do not increase globally before the test. World Ablaze uses much more aggressive values in its full AI stack, but HER already has explicit national offensive phases and AIFC. Raising this globally would make it difficult to distinguish scripted operational behavior from define-driven aggression.

### Lend-lease fractions

`LENDLEASE_FRACTION_OF_PRODUCTION = 0.5` is not a HER-specific outlier; it appears in multiple vanilla-derived implementations and World Ablaze. Do not reduce solely because 50% sounds large: this is a ceiling/base fraction inside AI lend-lease evaluation, not an unconditional transfer of half of national production.

### Construction base priorities

`CONSTRUCTION_PRIO_INFRASTRUCTURE = 30`, `CONSTRUCTION_PRIO_RAILWAY = 20`, `CONSTRUCTION_PRIO_CIV_FACTORY = 1`, `CONSTRUCTION_PRIO_MIL_FACTORY = 0.70` look numerically extreme but belong to construction-queue ordering, not direct building-choice desire. Do not normalize these ratios without an in-game queue trace. The clear bug in this group is the repairing multiplier being zero.

### Fuel assignment thresholds

`MIN_FUEL_RATIO_TO_NOT_IGNORE_STRIKE_FORCE_COST = 0.0` and `MIN_FUEL_RATIO_TO_NOT_IGNORE_INVASION_SUPPORT_COST = 0.0` are common vanilla-derived values. Do not change before the first naval run. If fleets sortie and immediately become fuel-starved, tune these after observing fuel/mission behavior rather than pre-emptively making fleets passive.

### Research selection

Current research truncation/randomness should remain unchanged for baseline #1. The newly rebuilt `ai_focuses` and historical strategy-plan research overlays need to be observed first; global NAI research tuning now would obscure which layer causes any bad tech choices.

### Wanted-unit calculation and manpower buffers

Do not alter `WANTED_UNITS_*`, deployment manpower buffers, or upgrade-deficit thresholds before test #1. The new national 30-width templates materially changed equipment/manpower demand, so these values need empirical validation against actual fielded division counts and stockpile deficits.

## Hands-off observations tied directly to NAI

During test #1 specifically record:

- damaged factories/railways/infrastructure and whether repair queue items now receive civilian factories;
- active vs reserve ships for ENG/USA/JAP/ITA/GER;
- number of active escort task forces and convoy routes covered;
- failed/suicidal naval invasions, especially tiny unsupported invasions;
- battle-plan activation when local strength is bad, equal or favorable;
- front reassignment churn and tank assignment to unsuitable fronts;
- manpower held in deployment/reinforcement buffers;
- fuel state when strike forces refuse to sail or stay at sea too long.

## Current recommendation

Apply the five confirmed pre-run define changes above before the first integrated hands-off test. Leave broader land-aggression, research, wanted-unit, manpower and fuel thresholds unchanged until the first run provides evidence.
