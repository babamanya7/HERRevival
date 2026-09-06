# HER AI Rework — Technical Log & Design Reference

Status: IN PROGRESS
Branch: `AI-rework`
Started: 2026-09-06

## 1. Scope

Full AI audit/rework for HER Mod, processed in repository order:

1. `common/ai_areas`
2. `common/ai_equipment`
3. `common/ai_faction_theaters`
4. `common/ai_focuses`
5. `common/ai_navy`
6. `common/ai_strategy`
7. `common/ai_strategy_plans`
8. `common/ai_templates`
9. `NAI` section in `common/defines/00_defines.lua`

Equipment-design templates for tanks, aircraft and ships are postponed for now. Division templates are in scope.

Primary country set for country-specific AI work:

- GER
- SOV
- ENG
- USA
- JAP
- ITA
- FRA
- CHI

## 2. Design philosophy

### CONFIRMED-HER DESIGN

The target is not a perfectly symmetrical or perfectly "fair" AI. The target is an AI that produces a strong, historically plausible opponent and compensates for generic engine limitations where scripting alone cannot do so.

Priority order for solving AI weaknesses:

1. Use normal AI systems (`ai_areas`, `ai_strategy`, `ai_strategy_plans`, `ai_focuses`, templates, theater logic, etc.).
2. Add HER-specific AI helper systems where engine limitations remain: hidden AI-only decisions, events, ideas, scripted effects, variables or controlled stockpile/production/logistics assistance.
3. Use direct statistical/combat bonuses only where a weakness cannot reasonably be compensated by behavior or helper systems.
4. Tune `NAI` only after the scripted AI folders have been audited, so engine-wide values do not mask bad country strategies.

AI-only advantages are explicitly allowed when they compensate for obvious limitations common to AI control. They should preferably be targeted and explainable rather than blanket bonuses.

World Ablaze is used as a reference implementation for strong scripted AI and AI compensation patterns, not as a source of numbers to copy blindly.

## 3. Audit method for every AI folder

For each folder/block:

1. Inspect current HER implementation on `AI-rework`.
2. Compare with current/recent vanilla behavior and file structure where available.
3. Compare with World Ablaze implementation.
4. Verify syntax and semantics against Paradox Wiki / reliable technical documentation / working code.
5. Identify obsolete, conflicting, duplicate or missing logic.
6. Define what should be generic and what should be country-specific for the 8 majors.
7. Implement changes only after the behavior and syntax are understood.
8. Record stable findings and decisions in this file.

## 4. Verified AI scripting notes

### AI areas — CONFIRMED-HOI4

`common/ai_areas/*.txt` defines named geographic groups used by AI strategies such as `area_priority`, `front_unit_request`, force-concentration strategies and other area-targeted logic.

Syntax:

```txt
areas = {
    example_area = {
        continents = {
            europe
        }
        strategic_regions = {
            1
            2
        }
    }
}
```

Within an AI area, valid selectors are:

- `continents = { ... }`
- `strategic_regions = { ... }`

If both are present, membership is additive/OR: a province can belong because it is in any listed continent or strategic region. A province may belong to multiple AI areas or to none.

AI area names are internal identifiers and can be inspected in debug mode. They do not require localisation for AI use.

Important implication for HER: AI areas are only useful if later `ai_strategy` / theater logic actually references them. Therefore every area should have a clear operational purpose; dead aliases add maintenance cost and can hide obsolete strategic-region IDs after map changes.

### AI strategy lifecycle — CONFIRMED-HOI4

For `common/ai_strategy/*.txt`:

- `allowed` is evaluated before game start and should be used for cheap, effectively static gating such as country/DLC restrictions.
- `enable` is evaluated continuously and activates the strategy when true.
- an enabled strategy does not automatically disappear merely because `enable` later becomes false unless `abort_when_not_enabled = yes` is used.
- `abort` removes/prevents the strategy when its trigger is true.

HER rule: every dynamic strategy must deliberately define its lifecycle. Do not leave temporary front/production/operation strategies permanently active by accident.

## 5. Block 1 — `common/ai_areas`

Status: AUDIT STARTED

### 5.1 Current HER state

HER currently contains a single file: `common/ai_areas/default.txt`.

Current groups include broad continental aliases (`europe`, `africa`, `north_america`, `south_america`, `middle_east`) plus many operational areas:

- Finland / Baltics / Belarus / Ukraine / Kuban / Leningrad / Moscow / Urals
- Italy / Reich / Britain / France / Balkans / Norway
- Normandy, Sicily, South Italy and Torch landing zones
- Suez / North Africa / Central Africa / Horn of Africa / Iraq-Iran
- Philippines / East Indies / Moluccas / Papua / Burma / Japan / China subregions
- Pacific island and front zones
- Japanese route-related regions

HER's Soviet/European map rework means many IDs intentionally differ from vanilla and must not be replaced from vanilla/World Ablaze mechanically.

### 5.2 World Ablaze comparison — initial findings

World Ablaze also uses one `common/ai_areas/default.txt`, but its area design is notably more operationally granular in several theaters.

Examples of useful patterns:

- separates Britain from `britain_coast`;
- splits France into north/west/south operational areas;
- splits Italy into main Italy and south Italy;
- defines Benelux separately;
- splits Scandinavia/Karelia;
- divides USSR into north/west/south/Caucasus/Crimea/east areas;
- separates Mediterranean, Atlantic and multiple Pacific bands;
- divides continental USA into east/central/west and separates eastern seaboard;
- divides China into operational subregions and Shanghai/coastal areas;
- defines Norwegian coast separately from Norway itself.

Design lesson: areas should represent actual operational questions the AI needs to answer (front allocation, invasion buffer, defense, offensive concentration, naval route/coast control), rather than only geographic labels.

### 5.3 Initial HER concerns to verify before editing

- Some HER areas are very broad (`reich`, `europe`, `africa`) and may be too coarse for operational allocation.
- `japan_routs` appears to be a route-focused area and contains repeated region `90`; duplicates should be checked for harmlessness and cleaned if unnecessary.
- `iraq_iran_zone` includes region `28`, which also belongs to `suez`; confirm this overlap is intentional for the strategies that consume these areas.
- `china_coast` contains land-oriented Chinese strategic regions rather than only literal sea/coast zones; verify how it is referenced before renaming or changing it.
- landing-zone areas are potentially valuable and should be preserved/expanded if referenced by invasion strategies.
- map-rework strategic region IDs must be validated against current HER `map/strategicregions` before any restructuring.

No gameplay change has yet been made to `ai_areas`; current work is research/audit first.

## 6. Sources used during this audit

Reference classes:

- current HER repository (`AI-rework` branch)
- Paradox/HOI4 AI modding documentation mirrors and CWTools schema
- current vanilla file inventory / game data references where accessible
- official World Ablaze public repository

Do not treat old forum posts or old mod files as authoritative when contradicted by current working syntax or current game data.

## 7. Progress log

### 2026-09-06

- Created branch `AI-rework` from `main`.
- Established AI rework scope and folder order.
- Established policy allowing targeted AI-only helper decisions/events/advantages.
- Confirmed `ai_areas` syntax and strategy lifecycle notes from documentation.
- Inspected current HER `common/ai_areas/default.txt`.
- Inspected World Ablaze `common/ai_areas/default.txt` and recorded initial structural differences.
- Began Block 1 (`ai_areas`) audit; no gameplay file changes yet.
