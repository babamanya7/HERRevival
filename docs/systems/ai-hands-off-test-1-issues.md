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

### HO1-013 — Japanese Southern Operation invasions are fragmented instead of sequential and concentrated
- Date: observed during the Pacific-war phase of Test 1.
- Country: JAP.
- Subsystem: `navy` / naval invasions / historical strategy.
- Severity: `MAJOR`.
- Observed: Japan launches amphibious operations in a disorganized, fragmented manner instead of concentrating forces and resolving objectives in sequence.
- Expected operational sequence: prioritize and complete major invasion phases in roughly this order: Philippines -> Malaya -> Indonesia/Dutch East Indies -> Papua/New Guinea. Parallel side operations are acceptable only when they do not dilute the main phase.
- Design requirement: Southern Operation should be represented as staged AI behavior, with each phase receiving concentrated invasion-force, escort, patrol and fleet-support priority before the next phase becomes dominant.
- Batch action: audit JAP invasion target weights, `invasion`/`naval_invasion` strategy entries, target-area activation conditions, army commitment and task-force support. Convert the current broad Pacific desire into sequential phase logic tied to conquest/control of the preceding objectives.

### HO1-014 — Japan lacks sufficiently explicit patrol/dominance preparation for scripted invasions
- Date: observed during the Pacific-war phase of Test 1.
- Country: JAP.
- Subsystem: `navy` / patrol / naval dominance / invasion support.
- Severity: `MAJOR`.
- Observed: Japanese invasion plans are not consistently preceded by concentrated naval missions in the relevant sea zones, reducing `naval_dominance` and causing invasion preparation/execution to stall or scatter.
- Confirmed HER mechanic: `naval_dominance` is generated by **patrol** missions; `strike force` does not generate it by itself but amplifies/supports the effect of patrol presence. Therefore patrol is the primary gating mission and must receive the explicit phase priority.
- Expected: before each Southern Operation phase, the AI should deliberately assign enough patrol task forces to the sea regions required by that phase to generate the needed `naval_dominance`, then reinforce that patrol coverage with strike forces and invasion-support groups.
- Batch action: add phase-specific patrol priorities for the Philippines, Malaya, Indonesia and Papua/New Guinea routes; ensure patrol groups are physically active in the exact required sea zones before army invasion priorities peak, then layer strike force and invasion support on top. Validate interaction with the new major-navy goals/taskforce templates rather than relying only on generic mission scoring.

### HO1-015 — Investigate AI-only scripted naval invasions without the normal naval-superiority gate
- Date: design request raised during Test 1.
- Country: primarily JAP; potentially reusable for other scripted historical AI invasions.
- Subsystem: `navy` / naval invasion engine constraints / NAI defines.
- Severity: `MEDIUM` pending feasibility; becomes `MAJOR` if dominance gating remains a recurrent blocker after HO1-014.
- Requested behavior: if technically possible, historical AI-controlled scripted invasions should be able to launch without satisfying the normal player-facing naval-superiority/naval-dominance requirement, while human invasions and ordinary unscripted AI invasions retain the normal rule.
- Constraint: do not globally remove naval-superiority requirements for players or all AI. Any bypass should be narrowly scoped to AI-only historical operations and should not create free unrestricted teleport-style invasions.
- Batch action: inspect available invasion-related defines, scripted effects/triggers and operation mechanisms for a supported way to bypass or satisfy the supremacy gate only for targeted AI operations. If no safe AI-only bypass exists, retain the normal gate and solve reliability through HO1-014 mission/dominance preparation instead.

### HO1-016 — Roughly one third of the Japanese fleet idles in Hiroshima despite full fuel reserves
- Date: observed during the Pacific-war phase of Test 1.
- Country: JAP.
- Subsystem: `navy` / task-force assignment / reserve behavior / mission utilization.
- Severity: `MAJOR`.
- Observed: approximately one third of the Japanese fleet remains sitting in Hiroshima and shows no intention of joining active operations, while Japan has a full fuel stockpile. The inactivity therefore cannot be explained by fuel shortage.
- Expected: with ample fuel and active Southern Operation objectives, the majority of combat-capable Japanese fleet strength should be assigned to useful patrol, strike-force, convoy-protection, invasion-support or reserve-reinforcement roles instead of remaining indefinitely idle in port.
- Suspected causes to inspect: task-force reserve thresholds, incomplete/invalid fleet-template composition, mission-assignment score thresholds, region-priority coverage, repair/readiness state, fleet assignment to inactive naval goals, or excessive hold/reserve behavior. Do not assume fuel gating.
- Batch action: audit which exact task forces are idle in Hiroshima, their composition/template role, readiness/repair status and assigned naval goal. Trace objective -> fleet template -> task force -> mission -> region assignment and identify the first layer where activation stops. Cross-check `AI_TASKFORCE_REQUIRED_RESERVE_RATIO`, mission minimum-priority thresholds and Japanese country naval goals before further global NAI tuning.

### HO1-017 — United States has the same large idle-fleet problem while Britain does not
- Date: observed during the Pacific-war phase of Test 1.
- Countries: USA; ENG as control/comparison case.
- Subsystem: `navy` / task-force assignment / reserve behavior / mission utilization.
- Severity: `MAJOR`.
- Observed: roughly 150 US ships sit idle in San Diego instead of joining operations. Britain shows the opposite behavior: almost the entire Royal Navy is actively assigned, with only about 19 mostly light ships left in reserve.
- Expected: the US Navy should actively employ the overwhelming majority of its combat-capable fleet in Pacific/Atlantic missions once at war, while keeping only a sensible repair/reinforcement reserve.
- Diagnostic value: because ENG uses the same global NAI but successfully keeps nearly its whole fleet operational, this strongly suggests the primary fault is country-specific naval goals/fleet templates/mission-region assignment for USA and JAP rather than a purely global reserve/fuel define.
- Batch action: compare USA and JAP directly against ENG through the whole naval chain: active goals, generated fleet templates, task-force completion status, reserve pools, mission scoring, region coverage and repair/readiness. Reuse the working ENG pattern where appropriate instead of blindly lowering global reserve thresholds further.

### HO1-018 — Barbarossa stalls near the old Soviet border and Germany burns itself against a ~7M-man Soviet army
- Date: observed after the start of the German-Soviet war in Test 1.
- Countries: GER and SOV.
- Subsystem: `front` / force generation / offensive concentration / production / templates.
- Severity: `MAJOR`.
- Observed: the Eastern Front stabilizes approximately around the old Soviet border. Germany repeatedly attacks and bleeds against a Soviet army of roughly 7 million men without achieving the intended deep 1941 penetration.
- Expected: the first Barbarossa phase should produce substantial German operational penetration before the front hardens later, while the Soviet AI should survive through depth and mobilization rather than already presenting an effectively immovable wall at the pre-1939 frontier.
- Diagnostic requirement: do not solve this with a blanket German combat buff. Audit both sides together: Soviet division count/manpower target and deployment timing, German infantry/armor force totals, panzer concentration (linked to HO1-011), attack pacing, equipment strength, templates, front allocation/AIFC, supply, and whether Germany is launching broad continuous attacks instead of concentrated breakthroughs.
- Batch action: reconstruct the June–winter 1941 force balance and loss curve. Determine whether the main cause is excessive Soviet force generation (~7M too early), inadequate German armored mass, malformed templates, poor concentration/front AI, unsustainable attack aggressiveness, or a combination. Tune the historical 1941 campaign so Germany can advance deeply without scripting a guaranteed Soviet collapse.

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
