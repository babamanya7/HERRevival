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

_No issues logged yet._

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
