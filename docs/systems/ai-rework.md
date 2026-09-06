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

`common/ai_areas/*.txt` defines named geographic groups used by AI strategies such as `area_priority`, `front_unit_request`, force-concentration strategies, `front_control`, and `put_unit_buffers`.

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

Membership is additive/OR when multiple selectors are used. A province may belong to multiple AI areas or to none.

AI area names are internal identifiers and do not require localisation for AI use.

Important implication for HER: AI areas should correspond to actual operational questions. Broad aliases remain useful for generic behavior, while front allocation, force concentration, invasions and unit buffers benefit from smaller operational areas.

### Area-targeting tokens — CONFIRMED-HOI4 / WORKING-HER

Current documentation and existing HER code confirm area targeting for the following useful strategy families:

- `area_priority`
- `front_unit_request`
- `force_concentration_front_factor`
- `force_concentration_factor`
- `force_concentration_target_weight`
- `front_control`
- `put_unit_buffers`

`front_unit_request` may target an area, strategic region, state or country/front depending on syntax. Its value modifies troop demand for the matching front rather than directly moving a fixed number of divisions.

HER already uses AI areas actively:

- SOV uses `finland`, `baltics`, `belorussia`, `ukraine`, `kuban`, `leningrad_region`, `moscow_region`, `reich`, `balkans` and `north_china` in front/area priorities.
- GER uses broad areas such as `europe`, `norway`, `north_america`, `south_america`, `north_china`, `middle_east`, `suez`, `africa`, `pacific_front` and `australia_new_zealand`.
- JAP uses `burma`, `thailand`, `malaysia`, `philippines`, `japan_routs`, `australia_new_zealand`, `molucass`, `core_japan`, `pacific_front`, `china_coast` and `south_china`.
- USA uses broad `europe`/`africa` areas for buffers, ally-front support and African priorities.

Therefore stale strategic-region membership in `ai_areas` is a gameplay bug, not merely organizational debt.

### AI strategy lifecycle — CONFIRMED-HOI4

For `common/ai_strategy/*.txt`:

- `allowed` is evaluated before game start and should be used for cheap, effectively static gating such as country/DLC restrictions.
- `enable` is evaluated continuously and activates the strategy when true.
- an enabled strategy does not automatically disappear merely because `enable` later becomes false unless `abort_when_not_enabled = yes` is used.
- `abort` removes/prevents the strategy when its trigger is true.

HER rule: every dynamic strategy must deliberately define its lifecycle. Do not leave temporary front/production/operation strategies permanently active by accident.

### AI focuses and research weighting — CONFIRMED-HOI4

`common/ai_focuses/*.txt` is not a set of manually activated country strategies. The engine maintains several dynamic AI focus values (defensive, aggressive, war production, military equipment, military advancements, peaceful, naval, naval air and aviation) from the country's current situation. These values are then multiplied into the research-category weights listed in the matching `ai_focus_*` block.

Country-specific blocks use the country tag suffix, for example `ai_focus_aviation_GER`, to provide the country-specific mapping for that AI focus.

The dynamic focus values themselves depend on game state. Important examples from current documentation:

- defensive rises in defensive wars and makes battle-plan execution more cautious;
- aggressive rises for aggressive wars and makes battle-plan execution less cautious;
- war production rises strongly in war;
- military equipment is high both in peace and war;
- military advancements scales with available research slots and war status;
- peaceful is primarily a peacetime focus;
- naval depends heavily on dockyards, convoy/resource usage and whether the country has a navy;
- naval air depends on carrier availability;
- aviation depends on air-base capacity.

Country modifiers such as `ai_focus_naval_air_factor` modify these calculated focus values. Therefore numbers inside `common/ai_focuses` should be treated as category multipliers, not as direct percentages of research slots.

Research selection has several layers that can stack:

1. technology `ai_will_do` score;
2. the technology's category membership;
3. current engine AI-focus category weighting from `common/ai_focuses`;
4. active `ai_strategy_plan` `research = { ... }` category weights;
5. specific AI strategies such as `research_tech` / `research_weight_factor` where used.

HER rule: use `ai_focuses` for broad national research character, `ai_strategy_plans` for historical/phase priorities, and exact-tech strategies only for genuinely mandatory technologies. Do not attempt to encode the entire research order in one layer.

The old `ai_historical_focus_list_TAG` mechanism in `common/ai_focuses` is legacy functionality. Strategy plans provide a more capable historical focus-order mechanism and should be the single authoritative source for the eight majors. Do not maintain duplicate historical focus lists in both systems.

## 5. Block 1 — `common/ai_areas`

Status: IMPLEMENTED — awaiting in-game hands-off validation

### 5.1 HER / map audit findings

The current HER strategic-region tree was checked rather than importing vanilla or World Ablaze IDs. Several area entries had become stale after HER map reworks.

Confirmed bad or obsolete memberships found and corrected:

- `italy` contained region `115`, which is now Central Northeastern Pacific, and region `169`, Tyrrhenian Sea. It now contains the Italian land regions 21/23/238/236.
- `ukraine` contained region `30` (Black Sea) and omitted region `130` (Kiev). The land-area definition was corrected.
- `leningrad_region` omitted the new/relocated Volkhov region `149`.
- `moscow_region` omitted Smolensk `205` and Yaroslavl `286` after the map subdivision.
- old `urals` mixed Vologda/Arctic/Ryazan/Western Steppe with the actual industrial rear. For compatibility the old key was retained, but its membership now represents Penza/Volga/Ural industrial regions: 275, 40, 138, 212, 216, 289, 291.
- `balkans` contained Aegean Sea `202`; the sea region was removed from the land operational area.
- `south_italy_landing_zone` contained Tyrrhenian Sea `169`; the landing destination is now Southern Italy `238`, while Sicily stays separate.
- `north_africa` contained broad Middle East region `28`; it was removed from the North African land area while `suez` and `iraq_iran_zone` retain it where intentional.
- `china_coast` included Korea `186`; Korea is now its own area to keep Japanese China-coast buffers from spreading onto the peninsula.
- duplicate region `90` was removed from the existing `japan_routs` key. The misspelled key itself is retained because active JAP strategies reference it.

### 5.2 New operational areas

Following the useful World Ablaze pattern, HER now has smaller aliases ready for later country strategies while retaining old broad keys for compatibility:

- Soviet: `soviet_north`, `soviet_center`, `soviet_south`, `caucasus`, `crimea`, `soviet_far_east`.
- Central/Western Europe: `germany_core`, `benelux`, `poland`, `north_france`, `south_france`.
- Italy: `north_italy`, `south_italy`, `sicily`.
- USA: `usa_east`, `usa_central`, `usa_west`.
- Japan/Korea: `japan_home_islands`, `japan_home_waters`, `korea`.

These new aliases are intentionally mostly inert until their consumers are added during `ai_strategy`, `ai_faction_theaters` and related passes. This avoids changing several subsystems at once while giving later strategies stable geographic targets.

### 5.3 World Ablaze comparison

World Ablaze uses the same general architecture but with more operational granularity: Britain/coast, multiple French and Italian sectors, Benelux, USSR north/west/south/Caucasus/Crimea, Mediterranean/Atlantic/Pacific bands, continental USA sectors, and detailed China/Japan areas.

HER adopted the structural lesson, not WA strategic-region IDs or numeric priorities. HER map IDs remain authoritative.

### 5.4 Deferred issues discovered while tracing consumers

Do not fix these in `ai_areas`; revisit in their proper folder:

- `common/ai_strategy/USA.txt`: a North Africa `put_unit_buffers` block uses `area = europe`; likely copy/paste logic error.
- `common/ai_strategy/JAP.txt`: `Japan_southern_expansion_1_fire` currently has mutually impossible date requirements (`date > 1942.12.15` and `date < 1942.1.1`).
- broad GER `area_priority` values and SOV pre-Barbarossa area priorities need reassessment after all geographic aliases are available.
- `core_japan` still mixes home-island and surrounding strategic regions because existing JAP behavior consumes it; new `japan_home_islands`/`japan_home_waters` aliases allow a safe migration later.

## 6. Block 2 — `common/ai_equipment`

Status: DEFERRED BY DESIGN

The folder controls AI creation/upgrading of equipment variants for roles: tank designs, aircraft designs and ship designs. This is exactly the equipment-template work intentionally postponed for the current AI pass.

HER currently contains a functioning aircraft design file and multiple VNR naval design groups, while `generic_tank.txt` and `generic_naval.txt` are empty. No changes should be made here until equipment-design templates are explicitly brought back into scope.

## 7. Block 3 — `common/ai_faction_theaters`

Status: EMPTY / DEFERRED

HER's only file, `common/ai_faction_theaters/ai_faction_theaters.txt`, is currently empty.

Do not populate it merely to fill the folder. First complete the operational-area and `ai_strategy` passes and only add faction-theater definitions when they solve a demonstrated multi-country theater-allocation problem that area priorities and normal theater strategies cannot solve cleanly.

## 8. Block 4 — `common/ai_focuses`

Status: AUDIT IN PROGRESS

### 8.1 Current HER structure

Separate research-focus mappings exist for GER, SOV, ENG, USA, JAP, ITA and FRA, plus `generic.txt`. They are structurally near-copies of the generic file with country-specific numeric changes.

CHI is the exception: `common/ai_focuses/CHI.txt` contains only the legacy `ai_historical_focus_list_CHI` and therefore has no country-specific research-focus mappings. China consequently relies on generic research-focus mappings plus its strategy-plan/technology-level logic.

### 8.2 Important current weights

Several existing weights are strong enough to dominate research decisions when their corresponding dynamic AI focus is high:

- GER `military_advancements`: `armor = 100`, `land_doctrine = 100`, `nuclear = 100`.
- USA `military_advancements`: `land_doctrine = 100`, `nuclear = 100`; USA also has `air_doctrine = 75` in aviation.
- JAP naval: `naval_doctrine = 100`, `cv_tech = 10`, `shbb_tech = 10`; naval air uses `naval_air = 14`.
- ENG naval: `naval_doctrine = 100`, strong DD/BB/CV weighting and explicit ASW weighting.
- SOV naval is much lower than the maritime majors, while its land doctrine remains heavily weighted.

These are multipliers on dynamic focus values, so values of 100 are not equivalent to "100% of research" but they are still extremely strong compared with neighboring category weights of roughly 1–20.

### 8.3 Overlap with historical strategy plans

Current historical strategy plans add another research-category layer:

- ENG: `air_equipment = 100`.
- USA: `air_equipment = 80`.
- JAP: `air_equipment = 70`.
- FRA: `air_equipment = 60`.
- ITA: `air_equipment = 40`.
- GER and SOV also define their own broader research weights in their historical plans.
- CHI's historical strategy plan currently has an empty `research` block.

Therefore the maritime/western majors currently receive substantial air-equipment pressure from strategy plans on top of the aviation AI-focus system. This should be tuned intentionally instead of assuming `common/ai_focuses` acts alone.

### 8.4 Historical focus-order duplication / lifecycle findings

- CHI has two historical focus-order sources: legacy `ai_historical_focus_list_CHI` in `common/ai_focuses/CHI.txt` and `CHI_nationalist_historical_plan` in `common/ai_strategy_plans/CHI_historical_strategy_plan.txt`. They contain different orders. This is architectural debt and should be reduced to the strategy plan only.
- USA's old `ai_historical_focus_list_USA` in `common/ai_focuses/USA.txt` is already commented out, confirming that the strategy-plan path is effectively intended as authoritative.
- USA's historical strategy plan currently uses `enable = { always = yes }`, not `is_historical_focus_on = yes`.
- CHI's historical strategy plan also uses `enable = { always = yes }`.
- ENG/FRA/ITA/JAP use `is_historical_focus_on = yes`.

The USA/CHI lifecycle difference must be reviewed in the strategy-plan block because it can force historical planning even when historical AI is disabled.

### 8.5 HER technology-category audit findings so far

The categories used by the current broad AI-focus files are still live in the HER technology tree. For example:

- the HER infantry chain uses `infantry_weapons`;
- artillery/heavy artillery uses `artillery`;
- paratrooper technology uses `para_tech`;
- technology files retain their own `ai_will_do` date/country/industry modifiers.

This confirms that the broad-category system itself is still valid, but also shows why extreme category weights can interact nonlinearly with the strong `ai_will_do` modifiers already embedded in HER technologies.

### 8.6 Planned implementation rule

For the eight majors:

- keep `ai_focuses` broad and characteristic rather than scripting exact research sequences;
- eliminate obsolete duplicate historical-focus lists from `ai_focuses`;
- give CHI a real country-specific research-focus mapping;
- normalize obviously runaway category weights unless there is a deliberate historical reason;
- move phase-specific priorities (for example a pre-Barbarossa armor/air push or a late US nuclear push) into `ai_strategy_plans` / exact research strategies rather than leaving them permanently amplified whenever a generic focus becomes high;
- validate all category names against the current HER technology files before implementation.

## 9. Sources used during this audit

Reference classes:

- current HER repository (`AI-rework` branch)
- current HER `map/strategicregions` tree as the authoritative source for HER IDs
- Paradox/HOI4 AI modding documentation mirrors and reliable working-mod documentation
- current vanilla file inventory / game-data references where accessible
- official World Ablaze public repository

Do not treat old forum posts or old mod files as authoritative when contradicted by current working syntax or current game data.

## 10. Progress log

### 2026-09-06

- Created branch `AI-rework` from `main`.
- Established AI rework scope and folder order.
- Established policy allowing targeted AI-only helper decisions/events/advantages.
- Confirmed `ai_areas` syntax and strategy lifecycle notes from documentation.
- Inspected current HER and World Ablaze `common/ai_areas/default.txt`.
- Traced active HER AI-area consumers in GER/SOV/JAP/USA strategies.
- Audited HER area IDs against the current strategic-region map.
- Corrected stale/wrong `ai_areas` memberships created by prior map changes.
- Added operational area aliases for USSR, Europe, Italy, USA and Japan/Korea.
- Preserved legacy keys where existing strategies depend on them.
- Logged USA/JAP strategy bugs discovered during consumer tracing for the later `ai_strategy` block.
- Block 1 implementation complete; hands-off validation remains for the integrated AI pass.
- Confirmed `ai_equipment` is equipment-variant design logic and deferred it per scope.
- Confirmed `ai_faction_theaters` is empty and deferred population until a concrete theater-allocation need is demonstrated.
- Documented the actual `ai_focuses` research-weighting model and its interaction with technology `ai_will_do` and strategy-plan research weights.
- Audited all eight major-country `ai_focuses` / historical strategy-plan relationships.
- Identified CHI duplicate historical focus ordering and missing country-specific research-focus mappings.
- Identified USA/CHI historical strategy plans that are always enabled even when historical AI is disabled; deferred correction to the strategy-plan block.
- Began validation of AI-focus research categories against the current HER technology tree.
