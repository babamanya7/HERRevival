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

## 8. Infantry weapons

### Main equipment / upgrade cadence
Current structure:
- `infantry_weapons` — 1918, cost 1.5, unlocks infantry equipment 0 and `antitank_1`;
- `infantry_weapons1` — 1937, cost 1.5, unlocks infantry equipment 1 and `antitank_2`;
- `infantry_weapons2` — 1939, cost 1.5, gives +3% soft attack and +3% breakthrough to all infantry and applies `inf_up_1` / cost increase;
- `improved_infantry_weapons` — 1940, cost 2, unlocks infantry equipment 2;
- `improved_infantry_weapons_2` — 1941, cost 2, another +3% soft attack / breakthrough and `inf_up_2`;
- `advanced_infantry_weapons` — 1943, cost 2, unlocks infantry equipment 3;
- `advanced_infantry_weapons2` — 1944, cost 1.5, another +3% soft attack / breakthrough and `inf_up_3`.

### Findings
- The separation between new equipment models and generic infantry-combat upgrades is conceptually interesting, but it means the practical research burden of keeping infantry current is higher than the visible weapon-model cadence alone. Evaluate each model + following stat-upgrade pair as one research cycle.
- 1937 → 1939 → 1940 → 1941 → 1943 → 1944 is fairly dense. Check whether the repeated annual 1939–41 sequence crowds out support/artillery research, especially for countries with fewer slots.
- `infantry_weapons2`, `improved_infantry_weapons_2`, and `advanced_infantry_weapons2` each also add an idea (`inf_up_1/2/3`) and custom tooltip `inf_increase_cost`; exact equipment-cost escalation must be audited together with the weapon equipment definitions before judging value.
- Early infantry weapon techs also unlock `antitank_1/2`, so infantry-weapon research currently controls part of the infantry AT equipment progression. Verify whether this is intentional and whether relevant AT/MIO categories are present.

### Infantry AT
- `infantry_at` — 1942, cost 1.5, unlocks `antitank_3` and the `sp_antitank_rockets` project.
- `infantry_at2` — 1944, cost 1.5, unlocks `antitank_4`.
- `infantry_at2` has its folder definition commented out. **A/C / visibility check:** verify whether it is intentionally hidden/indirect or accidentally absent from the visible research tree. If players cannot normally select it, this is a functional bug.

---

## 9. Special forces in infantry tree

### Paratroopers
- 1936 / 1939 / 1943 progression, costs 2 / 1.5 / 2.
- `paratroopers2` (1939) unlocks `mech_paratrooper` and para equipment 1.

**B / historical-role review:** 1939 mechanized paratrooper availability may be too early or too broad depending on what `mech_paratrooper` represents in HER. Re-evaluate against unit/equipment implementation, not name alone.

### Marines
- 1936 / 1939 / 1943 progression, costs 2 / 1.5 / 2.
- Later levels give meaningful river/amphibious/marsh attack bonuses rather than generic stat inflation.

Preliminary verdict: healthy thematic progression; revisit with amphibious-combat balance.

### General special-forces note
Special-force techs use dedicated categories (`para_tech`, `marine_tech`, etc.), which is good for targeted bonuses. Audit later against any generic `cat_special_forces_generic` and doctrine categories to prevent missing/double bonuses.

---

## 10. Support equipment and companies

### Support equipment chassis
Current equipment progression is roughly:
- base `tech_support` — 1918, cost 1;
- `tech_support_2` — 1939, cost 2;
- `tech_support_3` — 1941, cost 2;
- `tech_support_4` — 1943, cost 2;
- `tech_support_5` — 1945, cost 2.

Cadence 1939/41/43/45 is coherent. However, each support-equipment level also serves as a hub that paths toward the matching level of engineers, recon, field hospitals, logistics, MP, signals, and maintenance. This means the support-equipment chain is a structural gate for a very large share of army-support research.

**A/B / gating review:** verify whether every company really should require the next generic support-equipment technology. If all support branches are effectively synchronized behind one chassis tech, player specialization may be more constrained than intended.

### Engineers
- `tech_engineers` 1936 unlocks engineer, assault engineer, HQ engineer.
- `tech_engineers2` 1939 adds entrenchment, fort bonuses and dozer blade.
- `tech_engineers3` 1941 adds urban/forest bonuses, unlocks `heavy_infantry_support_armor`, and buffs flame tanks.

**A / role-overlap review:** `tech_engineers3` is no longer purely an engineer-company improvement; it also gates heavy-infantry support armor and flame-tank terrain performance. Verify whether these unlocks belong here or in armor/heavy-infantry techs. This matters for category bonuses and research discounts as well as tree clarity.

### General support-tech observation
The support tree appears very broad and regular, which is good for readability, but that regularity can hide cross-system unlocks. Every support-company level should be audited for side effects outside its nominal company (modules, unit types, armor unlocks, terrain buffs, etc.).

---

## 11. Cross-system preliminary conclusions

1. HER's industry tree contains many good specialized sub-branches, but too many branches independently improve the same global outputs (factory output, dockyard output, research speed). The main design task is to reduce role overlap, not flatten the tree.
2. Evaluate cumulative 1944 state, not isolated +1/+2/+4% tech effects.
3. Global research-speed inflation is already visible from computing + education before national modifiers.
4. Resource-tech scaling must be tested against the newly historicalized resource base.
5. Infrastructure technologies should primarily model logistics/infrastructure capability rather than act as secondary machine-tool branches.
6. Social systems (education, healthcare, agriculture) are interesting HER content, but their categories and effects currently bleed into construction/economic-law/general systems.
7. Infantry/support research shows another recurring pattern: nominally narrow technologies often unlock or modify content from adjacent systems. Integration/category auditing is therefore as important as raw stat balancing.
8. Research burden must be measured by complete capability packages (equipment model + generic upgrade + support gate), not by individual technology cost alone.

---

## 12. Special projects / secret-technology integration

### General structure
HER has a large special-project layer split across air, land, rockets, nuclear, naval projects and a separate set of naval-institute projects. This is not a minor side system: it acts as a second research economy using facilities, scientists, breakthrough points, prototype time and strategic-resource costs.

**Audit rule:** a special project should represent a capability that is qualitatively different from ordinary incremental research. Where possible it should unlock a module, equipment type, building, design option or new role rather than apply a blanket stat multiplier to an entire equipment archetype.

### Radar project
`sp_air_radar` requires `electronic_mechanical_engineering`, consumes air-specialization breakthrough and resources, then directly grants `radio_detection`, creates a level-1 radar station in the facility state, and enables `ship_radar_1`. It also advertises `cavity_magnatron` as the next unlocked technology.

This confirms that the earlier radar-tree inconsistency is real at the architecture level: ordinary tech paths and the special-project path currently overlap. **A:** radar progression should be normalized into a single explicit chain: prerequisite electronics -> radar project -> post-project radar/magnetron technologies/modules. Avoid direct tech-tree bypasses around the project.

### Air special projects — global archetype bonuses
`sp_air_bouncing_bomb` currently applies an equipment bonus to all `large_plane_airframe`: +10% `air_bombing` and +5% `build_cost_ic`.

**A:** a highly specific special-purpose weapon project should not globally improve every large aircraft. Replace the blanket archetype bonus with an explicit bomb/release module or another design-level unlock. The current cost increase on every large airframe is especially artificial.

`sp_air_intercontinental_bomber` applies +50% `air_range` and +20% `build_cost_ic` to all `large_plane_airframe`.

**A:** this effectively turns every large aircraft into an intercontinental design after one project. In Air Designer 2.0 this should become a physical design capability: enlarged fuel/wing/structure/engine configuration, distinct large-airframe variant, or other explicit module set with substantial trade-offs.

By contrast, `sp_air_earthshaker_bomb` enables `earthshaker_bomb_release`. **KEEP / good pattern:** this is the preferred project architecture because the project unlocks a concrete capability that the player must actually design into an aircraft.

### Land special projects
Land projects are generally closer to the desired pattern:
- `sp_land_flamethrower_tank` enables the flamethrower module and flame-tank subunits;
- `sp_land_military_engineering_vehicles` enables armored-support equipment and several specialist support subunits;
- `sp_land_stabilizator` and `sp_land_improved_stabilizator` enable actual stabilizer modules;
- `sp_land_amphibious_drive` is tied to tank-chassis prerequisites and design-template bonuses.

**KEEP / integration review:** these projects represent concrete equipment/design capabilities rather than generic global modifiers. Their exact timing and resource costs should be revisited after Tank Designer 2.0 because several outputs will need to map onto the new role/chassis architecture.

`sp_land_stabilizator` requires `improved_computing_machine`, while the improved stabilizer requires `advanced_computing_machine`. This is a good cross-system dependency in principle, but computing is already extremely high-value, so it further increases the indirect military payoff of the computing line. **B / integration:** account for these unlocks when reducing computing research-speed inflation.

### Rocket projects
The flying-bomb project is structurally healthy: it requires `experimental_rockets`, unlocks `guided_missile_equipment_1`, and its prototype choices modify the guided-missile equipment itself (range, payload, speed, production cost) rather than unrelated aircraft.

**KEEP / preferred pattern:** project decisions produce trade-offs on the capability that was actually developed.

### Nuclear projects
The reactor project is also structurally strong: it requires `atomic_research`, unlocks the appropriate reactor technology/building, supports graphite vs heavy-water choices, and includes a first-successful-reactor information/publicity interaction that can accelerate other countries' nuclear progress.

**KEEP / good system design:** this is an example of a special project acting as a genuine technological program with branching engineering choices and international knowledge spillover rather than a flat national-stat bonus.

### Hidden naval overrides
`common/special_projects/projects/_overwrite.txt` explicitly keeps vanilla `sp_naval_fleet_submarine`, `sp_naval_cruiser_submarine`, and `sp_naval_super_heavy_battleship` definitions hidden (`visible = { always = no }`) with empty outputs. This appears intentional because HER replaces them with its own naval-institute/project architecture.

**C / maintenance:** document these as intentional disabled compatibility stubs so a future vanilla update does not cause them to be mistaken for unfinished content or accidentally re-enabled.

### Special-project systemic verdict
Current quality is uneven:
- nuclear, rocket and many land projects already follow a strong "project -> concrete capability -> design/use choice" model;
- several air projects still follow a weak "project -> blanket archetype modifier" model and should be reworked alongside Air Designer 2.0;
- radar currently has duplicated responsibility between ordinary technologies and the special-project chain;
- naval special projects are a separate HER architecture and remain assigned to the dedicated naval audit branch.

---

## TODO — next passes
- finish synthetic oil/rubber branch audit;
- finish infantry special-forces branches and full support-company audit;
- audit artillery;
- armor implementation is deferred to Tank Designer 2.0 after the accepted architecture pass;
- air implementation is deferred to Air Designer 2.0 after the accepted architecture/MIO pass;
- naval implementation/final combat block is deferred to the dedicated naval branch;
- audit remaining special-project timing/resource costs and prototype-reward value;
- build category → technology → MIO/focus bonus map;
- audit country starting techs and research bonuses;
- then move the general audit into national focuses / doctrines and cross-system bonus inflation;
- convert confirmed findings into implementation changes only after each subsystem pass is complete.
