# HER Mod — Research System Audit

Status: IN PROGRESS

Purpose: systematic audit of HER research mechanics across design, balance, integration, and code quality.

Audit dimensions:
- tree structure and progression;
- `start_year` timing and ahead-of-time behavior;
- `research_cost` and slot-day value;
- prerequisites / paths / dependencies;
- gameplay effects and cumulative scaling;
- equipment/module/building unlocks;
- technology categories and MIO/research-bonus integration;
- special-project integration;
- country starting technologies and focus/event/decision bonuses;
- AI weights and dead/impossible conditions;
- localisation/UI consistency;
- parser/runtime/code hygiene.

Severity convention:
- A — architectural/design problem;
- B — balance problem;
- C — polish/technical cleanup;
- BUG — confirmed code/logic error.

---

## 1. Technology categories / global integration

### Findings
- `common/technologies` is replaced wholesale by HER via `replace_path`; the research audit must therefore treat the HER technology tree as a closed system and check for missing vanilla definitions after game updates.
- `common/technology_tags/00_technology.txt` declares `air_equipment` twice. **C / cleanup**.
- The tree relies heavily on special categories (`cat_*`, `mio_cat_*`), so category correctness is functionally important for research bonuses and MIO/KB interaction.
- Social/civilian technologies currently use `construction_tech` in addition to `industry`, which may cause construction-research bonuses to affect education, healthcare, agriculture, etc. **B / integration review**.

---

## 2. Electronics / computing / radar

### Computing line
Current chain includes:
- `electronic_mechanical_engineering`: +5% research speed, cost 1, start 1936;
- `mechanical_computing`: +7% research speed, cost 2.5, no explicit `start_year` found;
- `computing_machine`: +9% research speed, cost 2.5, start 1938;
- `improved_computing_machine`: +11%, cost 2.5, start 1940;
- `advanced_computing_machine`: +13%, cost 2.5, start 1942.

Potential cumulative global research-speed gain from the line is about +45% by 1942 before national spirits, focuses, education techs, sharing, etc.

**A/B:** likely creates a mandatory early self-accelerating research meta. Retain the concept that computing improves research, but normalize total cumulative gain and review `mechanical_computing` timing.

### Radar
- `electronic_mechanical_engineering` has a direct path to `cavity_magnatron`.
- `radio_detection` also leads to `cavity_magnatron`.
- Both `radio_detection` and `cavity_magnatron` are gated around `sp_air_radar`.

**A:** likely leftover structural inconsistency from converting radar into a special-project-driven system. Decide whether `radio_detection` is a required bridge tech or obsolete/hidden compatibility content.

### Radio
- `radio` 1937 → `improved_radio` 1939 → `advanced_radio` 1941, all cost 2.
- Preliminary verdict: good cadence; later verify module value (`tank_radio_*`, navigation, Leigh light) before final cost judgment.

---

## 3. Industry — production organization

### Machine tools
- 1936 / 1938 / 1940 / 1942 cadence is coherent.
- `flexible_line` 1943 vs `streamlined_line` 1944 is a real strategic fork, but needs production-model testing to ensure one option does not dominate.

### Worker / process line
`tool_maintenance` → `worker_training` → `on_spot_training` → `worker_colleges` → `workplace_processes`.

Preliminary verdict: strong thematic progression. Review research costs and cumulative efficiency/output effects.

### `foriegn_labour`
- start 1943, cost 2;
- +25% factory output;
- +25% dockyard output;
- penalties to efficiency growth, line-change retention, and repair;
- available from both concentrated and dispersed branches.

**A/B:** effect is extremely strong and the concept is not a universal technological advance. Strong candidate for removal from the generic tech tree and relocation to law/decision/national mechanic. Do not rename the misspelled ID until all references are audited.

---

## 4. Concentrated vs dispersed industry

Cadence: 1936 → 1938 → 1940 → 1942 → 1944.

### Concentrated per level
- +20% building slots;
- -0.2% recruitable population;
- +10% industry air damage;
- +2% max production efficiency;
- -2% efficiency gain.

Approximate five-level cumulative state: +100% slots, -1% recruitable population, +50% industry air-damage vulnerability, +10% max efficiency, -10% efficiency gain.

### Dispersed per level
- +10% building slots;
- -0.2% recruitable population;
- -10% industry air damage;
- +5% repair;
- +3% line-change retention;
- +1% starting efficiency.

**B:** tree concept and cadence are good, but cumulative effects must be evaluated as a full 1944 package rather than per-tech values.

---

## 5. Construction / infrastructure branches

### Construction
Core construction levels use a regular 1936/38/40/42/44 cadence and branch into defenses, infrastructure, civilian works, and excavation.

### Rail infrastructure
Repeated per-level effects include:
- +4% factory output;
- +4% dockyard output;
- +1% max efficiency;
- +1% efficiency gain;
- -1% supply consumption;
- +5% railway and supply-hub construction.

Five levels imply roughly +20% factory and dockyard output from the rail branch alone.

### Road infrastructure
Repeated per-level effects include:
- +4% factory output;
- +4% dockyard output;
- -1% org loss while moving;
- +1% max efficiency;
- +1% line-change retention;
- +2% supply-node range;
- +5% infrastructure construction.

Five levels imply roughly another +20% factory and dockyard output.

**B/A:** rail/road branches overlap too heavily with direct production technology. Their primary role should be logistics, construction, movement, repair, supply, and infrastructure efficiency; consider sharply reducing direct factory/dockyard output.

### Air infrastructure
Repeated bonuses are thematically coherent (mission efficiency, weather penalty, accidents, airbase construction). Preliminary verdict: healthy; re-evaluate later alongside full air-combat audit.

### Port infrastructure
Thematic but powerful: repeated dockyard output, refit, repair, and naval-base construction bonuses. Keep linked to later naval-production audit.

### Defense works
Conceptually coherent. Repeated `army_core_defence_factor` becomes a direct army combat bonus and should be re-evaluated during land-combat audit.

### Confirmed AI bugs
**BUG:** `infra_works` contains a modifier requiring `tag = SOV`, `tag = GER`, and `tag = USA` simultaneously; impossible without `OR`.

**BUG:** `infra_works2` similarly contains `tag = SOV` and `tag = GER` in the same modifier without `OR`.

---

## 6. Civilian / social branches

### Civilian works
Each level gives energy/storage plus +2% stability on completion. Five levels imply +10% stability from technology clicks.

**B:** stability reward is mechanically artificial and overlaps political systems; review or replace.

### Agriculture / `housing_work`
Per level:
- -2% consumer goods;
- +0.2% recruitable population;
- +100 weekly manpower.

Five levels imply roughly -10% consumer goods, +1% recruitable population, +500 weekly manpower.

**A/B:** excessive and overlaps economic laws, conscription, population growth, and political systems. Rebuild around agricultural/demographic effects with much lower direct economic/manpower power.

### Healthcare
Repeated reductions to attrition/XP loss/climate attrition plus morale/acclimatization bonuses are conceptually strong. Numbers to be rechecked in land-combat audit.

### Education
Repeated per-level effects include +2% research speed and +1 army/navy leader start level. Five levels imply +10% research speed and potentially +5 starting leader levels.

**A/B:** contributes to research-speed inflation and may create absurd late-game leader starting levels depending on engine stacking. Verify engine behavior and normalize.

### Naming / semantic mismatch
`housing_work` is commented as Agricultural Advances while the ID implies housing and the effects are consumer goods / manpower / conscription. **C/A:** clarify system identity before final balancing.

---

## 7. Excavation / fuel / synthetic resources

### Excavation
Five levels, each +10% local resources and +5% storage size → roughly +50% extraction and +25% storage by 1944.

**B / integration:** must be re-evaluated against the newly rebalanced historical resource map so tech scaling does not erase strategic resource scarcity.

### Fuel refining
1938/40/42/44, cost 3, with +10% fuel gain and +10% fuel gain from states per level. Preliminary cadence/cost looks reasonable; validate against fuel economy later.

### Oil processing
1938/40/42/44, cost 1.5, each level gives `fuel_gain_factor_from_states = 0.5`; potential cumulative +200% from four levels.

**B:** very aggressive scaling; requires fuel-formula and wartime-consumption testing.

**BUG:** `advanced_oil_processing` AI modifiers check `rubber > 10/20/30` despite being an oil-processing technology; likely copy-paste from the rubber branch.

---

## 8. Cross-system preliminary conclusions

1. HER's industry tree contains many good specialized sub-branches, but too many branches independently improve the same global outputs (factory output, dockyard output, research speed). The main design task is to reduce role overlap, not flatten the tree.
2. Evaluate cumulative 1944 state, not isolated +1/+2/+4% tech effects.
3. Global research-speed inflation is already visible from computing + education before national modifiers.
4. Resource-tech scaling must be tested against the newly historicalized resource base.
5. Infrastructure technologies should primarily model logistics/infrastructure capability rather than act as secondary machine-tool branches.
6. Social systems (education, healthcare, agriculture) are interesting HER content, but their categories and effects currently bleed into construction/economic-law/general systems.

---

## TODO — next passes
- finish synthetic oil/rubber branch audit;
- audit infantry and support technologies;
- audit artillery;
- audit armor and NSB armor integration;
- audit air technologies and BBA modules;
- audit naval technologies and hidden naval-institute overrides;
- build category → technology → MIO/focus bonus map;
- audit country starting techs and research bonuses;
- convert confirmed findings into implementation changes only after each subsystem pass is complete.
