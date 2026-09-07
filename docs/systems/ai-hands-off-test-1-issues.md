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
