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
