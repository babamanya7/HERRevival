# HER AI Hands-off Test 1 — Issue Log

Status: ACTIVE
Branch: `AI-rework`
Baseline: first integrated hands-off run

Purpose: collect observed AI/runtime/configuration problems during the first hands-off test without changing behavior mid-run. Fixes are intentionally batched after the run so the baseline remains interpretable.

## Logging rules

For each issue, record where possible:
- in-game date;
- country/tag;
- subsystem (`focus`, `construction`, `production`, `templates`, `front`, `air`, `navy`, `supply`, `FYP`, `runtime/parser`, etc.);
- observed behavior;
- expected behavior;
- suspected cause only if reasonably clear;
- severity: `BLOCKER`, `MAJOR`, `MEDIUM`, `MINOR`;
- evidence/screenshots/log text if provided.

Do not fix issues during the active baseline unless they prevent the run from continuing or corrupt the test itself.

## Observed issues

### HO1-001 — Missing `regimental_support` blocks in AI target templates
- Date: configuration defect identified during Test 1.
- Countries: all countries using the rewritten national AI target templates.
- Subsystem: `templates`.
- Severity: `MAJOR`.
- Observed: rewritten AI templates contain the line `regiments` and regular `support` setup but the separately discussed `regimental_support` layer was not carried into the target templates.
- Expected: relevant target templates must explicitly define `regimental_support` as its own block, distinct from line battalions and ordinary support companies, following the agreed HER template architecture.
- Cause: omission during the national AI-template rewrite; earlier caution about unverified parser support was incorrectly allowed to override the user's explicit design requirement.
- Batch action: audit every national and generic target template, restore the intended `regimental_support` composition, then parser-check and document the confirmed syntax/behavior.

### HO1-002 — `generic_decision` layer not updated as agreed
- Date: configuration defect identified during Test 1.
- Countries: global/generic AI layer.
- Subsystem: `decision` / generic AI configuration.
- Severity: `MAJOR`.
- Observed: the `generic_decision` configuration was not actually brought to the state discussed during the AI rework; old/unadjusted behavior remains.
- Expected: apply the previously agreed generic-decision cleanup/retuning instead of leaving the legacy layer untouched.
- Cause: the generic-decision pass was missed while the focus was on country strategy, templates and global strategy cleanup.
- Batch action: reopen the current `generic_decision` implementation against the prior agreed design, enumerate stale entries, and apply the complete intended cleanup in the post-run batch rather than piecemeal during Test 1.

### HO1-003 — German panzer target template has the wrong historical organization
- Date: observed during Test 1.
- Country: GER.
- Subsystem: `templates`.
- Severity: `MAJOR`.
- Observed: the current German AI tank target template has a strange/non-historical battalion mix and does not match the intended HER organization.
- Expected baseline organization: 3 tank battalions + 6 motorized infantry battalions + 3 artillery battalions, one of the artillery battalions being heavy artillery, + 3 motorized anti-tank battalions.
- Additional requirement: preserve the agreed historical organization while also checking the resulting combat width, ordinary support companies, the separate `regimental_support` block, equipment availability, and the upgrade/target conditions so the AI converges on the intended formation rather than lingering on malformed transitional templates.
- Scope expansion: this is not only a GER-panzer fix. The post-run pass must audit **all AI target templates for all countries** (national and generic) for historical organization, combat width, `regiments`, separate `regimental_support`, ordinary `support`, equipment realism, role assignment and upgrade/convergence conditions. GER panzer organization above is the explicit benchmark case already identified.
- Batch action: rebuild the German panzer target template around the exact 3 tank / 6 motorized / 3 artillery (1 heavy) / 3 motorized AT structure, then perform the full cross-country AI-template audit before considering the template layer complete.

### HO1-004 — `handle_economy_fatigue` can roll Germany back to Civilian Economy immediately before war
- Date: observed during Test 1, immediately before the coming war.
- Country: GER.
- Subsystem: `decision` / economy law management.
- Severity: `MAJOR`.
- Observed: the Reich took `handle_economy_fatigue` and switched onto Civilian Economy directly before war, undoing its pre-war mobilization state and damaging the entire German buildup.
- Expected: economy-fatigue handling must not demobilize Germany into Civilian Economy on the eve of a historical war. Any fatigue relief must respect imminent-war/historical mobilization context and preserve an appropriate wartime/pre-war economy law floor.
- Suspected cause: decision availability/effect logic is insufficiently gated against historical-war proximity and/or the AI is allowed to value the fatigue relief without accounting for the strategic cost of downgrading the economy law.
- Batch action: inspect the full `handle_economy_fatigue` decision chain and any related law-switch effects/AI weights. Add explicit historical-war and current-law guards so GER cannot use the decision to downgrade below the intended pre-war mobilization floor; check whether the same defect can affect other majors.

### HO1-005 — Generals are being reassigned between armies too frequently
- Date: observed during Test 1.
- Countries: observed globally; at minimum majors under active fronts.
- Subsystem: `front` / army leader assignment.
- Severity: `MAJOR`.
- Observed: AI repeatedly moves generals from one army to another instead of maintaining stable command assignments.
- Expected: generals should remain attached to an army/front for meaningful periods unless there is a strong reason to replace them, preserving specialization and avoiding constant command churn.
- Suspected cause: current leader-assignment scoring/reassignment thresholds are too permissive relative to the score advantage of a new assignment.
- Batch action: inspect NAI army-leader assignment/reassignment defines and any scripted assignment behavior; strengthen assignment persistence and reduce pointless leader churn without blocking genuinely better reassignment.

### HO1-006 — Britain commits roughly half of its army to France and still loses the campaign
- Date: observed during the Battle of France in Test 1.
- Country: ENG.
- Subsystem: `front` / expeditionary commitment / historical strategy.
- Severity: `MAJOR`.
- Observed: Britain sent roughly half of its army, about 600k men, into France, yet Germany still overran France.
- Expected: the BEF should be historically meaningful but bounded; Britain must retain sufficient home, imperial and strategic reserve while avoiding a huge commitment that does not materially improve the French defense.
- Batch action: audit ENG France/Benelux front weights, ally-front commitment, reserve/home-defense requirements and expeditionary behavior. Determine whether the issue is excessive commitment, poor placement, weak templates, bad front AI, or some combination rather than merely reducing the raw division count.

### HO1-007 — British India sends essentially its entire army to France
- Date: observed during the Battle of France in Test 1.
- Country: RAJ.
- Subsystem: `front` / expeditionaries / subject AI.
- Severity: `MAJOR`.
- Observed: British India transferred/committed all or nearly all of its divisions to France.
- Expected: RAJ should retain the overwhelming majority of its army for India, Burma, internal/imperial defense and the Asian theater; only a limited historical expeditionary contribution should be possible.
- Suspected cause: generic faction/ally front desire and expeditionary logic overwhelms local-defense priorities for subjects.
- Batch action: add/strengthen RAJ home-area and Asian-theater retention, cap European expeditionary participation, and review subject expeditionary NAI/strategy behavior so colonial armies are not emptied into Europe.

### HO1-008 — Japan bleeds equipment stockpiles in China and fails to take Wuhan
- Date: observed during the Sino-Japanese War in Test 1.
- Country: JAP.
- Subsystem: `front` / production / supply / China strategy.
- Severity: `MAJOR`.
- Observed: Japan is fighting in China at unsustainable intensity, driving equipment stockpiles deeply negative, while at the same time failing to capture Wuhan.
- Expected: Japan should maintain enough offensive pressure to progress historically through central China, including a credible Wuhan campaign, but should not destroy its entire equipment reserve through continuous low-value attacks.
- Batch action: diagnose attack aggressiveness, target/front priorities toward Wuhan, supply/terrain awareness, template cost, reinforcement needs and production balance together. Avoid solving this with blanket combat buffs; objective is better concentration and pacing, not free strength.

### HO1-009 — Soviet area-defense orders defend naval bases in inaccessible/non-applicable regions and strand divisions
- Date: observed during Test 1.
- Country: SOV.
- Subsystem: `front` / area defense / `ai_areas`.
- Severity: `MAJOR`.
- Evidence: screenshot shows a Soviet area-defense order with `Protect naval bases` enabled while divisions assigned to the order are in regions where no usable naval bases are accessible.
- Observed: divisions assigned to these territorial-defense orders remain idle/stuck because the order asks them to defend naval bases that do not exist or cannot be reached in the selected area.
- Expected: inland Soviet area-defense orders should not use naval-base defense as an active objective unless the selected area actually contains reachable naval bases; divisions must be assigned to valid VP/fort/border/rail/supply objectives instead of dead orders.
- Suspected cause: global default area-defense setting `AREA_DEFENSE_SETTING_PORTS = true` is being applied indiscriminately to scripted Soviet defense areas and/or the selected `ai_areas` contain no valid port targets for that order.
- Batch action: audit Soviet area-defense strategy generation and global NAI area-defense defaults. Ensure port-defense objectives are only used for coastal areas with reachable ports, and inspect all major-country defense orders for the same dead-order failure mode.

### HO1-010 — Germany misses the historical 22 June 1941 Barbarossa timing because the focus schedule drifts
- Date: 1941-06-22 checkpoint in Test 1.
- Country: GER.
- Subsystem: `focus` / historical strategy plan / war timing.
- Severity: `MAJOR`.
- Observed: Germany had not attacked the Soviet Union by 22 June 1941 because its focus progression had fallen behind schedule.
- Expected: with historical focuses enabled, the German AI should reliably reach the Barbarossa war trigger in time for an invasion on or very near 22 June 1941, assuming no major alternate-history blocker has occurred.
- Suspected cause: the German historical `ai_strategy_plan` still permits too much schedule drift in the chain leading into Barbarossa, whether from unnecessary intervening focuses, late prerequisites, or insufficiently hard prioritization of the eastern-war sequence.
- Batch action: reconstruct the full German focus timeline from the pre-war diplomatic/industrial chain through Barbarossa, identify exactly which focuses consumed the missing calendar time, and retime/reorder/prioritize the sequence so the eastern-war trigger lands around 22 June 1941. Do not patch only the final war focus if the upstream schedule is the actual cause.

### HO1-011 — Germany fields too few panzer divisions for Barbarossa
- Date: around the 1941 Barbarossa checkpoint in Test 1.
- Country: GER.
- Subsystem: `templates` / production / division targets.
- Severity: `MAJOR`.
- Observed: Germany has only about 15 tank divisions by the Soviet-war timing, which is too low for the intended HER historical/operational role of German armored forces.
- Expected: Germany should enter the war with the USSR with a materially larger armored arm while still preserving viable equipment strength and not hollowing out the rest of the army.
- Batch action: audit GER armor template target ratios, allowed/desired division counts, production-line weighting, equipment availability and upgrade timing. Raise the 1941 armored-force target deliberately rather than blindly increasing tank spam from 1936.

### HO1-012 — AI-vs-AI Sino-Japanese War does not settle into the intended historical stalemate by 1941
- Date: 1941 phase of Test 1.
- Countries: JAP and CHI, specifically when both are AI-controlled.
- Subsystem: `front` / historical strategy / theater pacing.
- Severity: `MAJOR`.
- Observed: China is strongly pushing Japan back in 1941. This means Japan can launch the Southern Operation against the Allies while simultaneously collapsing in China, producing an ahistorical strategic failure.
- Expected: when both JAP and CHI are AI-controlled, the China front should roughly stabilize after the main Japanese expansion phase, approximating the historical 1940–41 stalemate. Japan should not be driven out of China while it transitions toward war with the Western Allies, and China should not be crushed outright either.
- Design requirement: implement this specifically as an AI-vs-AI historical pacing rule so human JAP or human CHI are not artificially constrained by the same scripted stalemate.
- Batch action: add bounded AI-only front behavior/strategy for the post-Wuhan/post-main-expansion phase: reduce low-value Japanese offensive bleeding, prevent excessive Chinese counteroffensive pressure, preserve key Japanese-held areas and enough Japanese forces in China while allowing Southern Operation commitments. Prefer strategy/front weighting and pacing controls over blanket combat-stat buffs.

## Post-run batch

After the run, group fixes by layer rather than by observation order:
1. parser/runtime blockers;
2. historical focus/event sequencing;
3. economy/construction/production;
4. land strategy/front allocation/templates;
5. air AI;
6. naval AI;
7. supply/logistics;
8. global NAI defines;
9. documentation/test-protocol updates.
