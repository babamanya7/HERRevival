# HER Mod — Development Context & Technical Reference

> Persistent working reference for future HER Mod development sessions.
>
> Purpose: preserve stable project decisions, verified Hearts of Iron IV scripting/engine behavior, HER-specific conventions, known crash causes, file paths, IDs, and implementation lessons so future work does not rely on chat history alone.
>
> Maintenance rule: update this file proactively whenever a stable architectural decision, verified engine rule, important path/ID, recurring pitfall, or completed subsystem milestone appears during HER work.

---

## 1. How this reference must be used

Before making non-trivial HER code changes:

1. Read the relevant section of this reference.
2. Inspect existing HER code for the closest working pattern before inventing new syntax.
3. Prefer patterns already proven in HER or vanilla HOI4 over plausible-looking but unverified constructs.
4. Treat `Confirmed` rules as authoritative project knowledge.
5. Treat `Experimental / Unverified` notes as hypotheses only; do not silently promote them to facts.
6. After a successful in-game test, move useful findings from experimental notes into confirmed rules.
7. When a change causes a parser error, map error, bad scope behavior, silent failure, or crash, record the cause and fix here if it is likely to recur.

### Confidence labels

- **CONFIRMED-HER** — observed working in HER or directly verified in the repository/game.
- **CONFIRMED-HOI4** — reliably established HOI4 engine/syntax behavior.
- **EXPERIMENTAL** — design or syntax not yet verified in game.
- **OBSOLETE** — old HER behavior kept only for historical context; do not reuse without revalidation.

---

## 2. Project identity and current repository structure

**Repository:** `babamanya7/HERRevival`

**Default branch:** `main`

**Mod name:** `HER MOD: Revival`

**Descriptor supported version at time this file was created:** `1.19.2.0`

Main top-level mod areas currently present include:

- `common/`
- `events/`
- `gfx/`
- `history/`
- `interface/`
- `localisation/`
- `map/`
- `music/`
- `sound/`
- `tools/`

### Descriptor replacement paths — CONFIRMED-HER

The current `descriptor.mod` uses broad `replace_path` coverage. Important replaced trees include, among others:

- `common/characters`
- `common/decisions`
- `common/decisions/categories`
- `common/national_focus`
- `common/ideas`
- `common/technologies`
- `common/units`
- `common/units/equipment`
- `common/scripted_effects`
- `common/scripted_triggers`
- `events`
- `history/countries`
- `history/units`
- `history/states`
- `map/strategicregions`
- `map`

**Practical consequence:** when working in a replaced tree, do not assume missing vanilla content will still be inherited. Verify that every required vanilla definition/file is present where HER needs it.

**Important historical lesson:** HER has previously shown apparently contradictory behavior where vanilla files seemed to be read despite `replace_path`. Do not use that anecdotal behavior as a design assumption. When debugging replace-path issues, verify actual loaded files and error logs rather than trusting expected inheritance semantics alone.

---

## 3. General HER development rules

### 3.1 Stability over cleverness — CONFIRMED-HER

HER changes should prioritize reliable, readable HOI4 code over compact or overly abstract implementations.

When several implementations are possible:

1. Prefer a vanilla-like pattern already used by the engine.
2. Prefer an HER pattern already confirmed working.
3. Avoid unnecessary scope nesting, chained scripted effects, or indirect variables if a direct implementation is practical.
4. For systems that can destroy or duplicate equipment/resources, design failure-safe conditions first.

### 3.2 Multiplayer priorities — CONFIRMED-HER

HER is primarily designed as a historical multiplayer mod. AI behavior is secondary unless a mechanic explicitly needs AI compatibility.

Do not introduce AI-only complexity at the expense of MP stability unless requested.

### 3.3 Do not infer syntax from semantics — CONFIRMED-HER

A construct that sounds logically valid in English is not necessarily valid HOI4 script.

Before adding a new effect/trigger/scope pattern:

- search existing HER usage;
- if absent, compare against a known vanilla pattern or reliable documentation;
- keep uncertain syntax marked experimental until validated.

---

## 4. Scripting reference

### 4.1 Scopes and context

**Rule:** scope-sensitive effects and triggers must be validated in the exact context in which they will execute.

Do not assume that a trigger/effect valid in a country scope is valid in state, character, unit leader, or decision-target scope.

When debugging silent failures:

- identify the root scope;
- identify every scope transition;
- confirm which object each variable/flag/effect belongs to;
- inspect a nearby working HER or vanilla example.

### 4.2 Variables / flags

Use variables for quantities that change over time and flags for discrete state.

For economic/logistics systems, explicitly guard against:

- negative values where nonsensical;
- repeated payment on the same tick/event;
- integer/rounding drift;
- operations continuing after the underlying deficit/debt/route disappears.

### 4.3 On-actions

HER already uses on-actions for persistent mechanics, including the warehouse/storage system.

**CONFIRMED-HER design lesson from storage:** recurring systems must contain their own stop/cleanup logic. A process that activates to cover a deficit must stop once the deficit no longer exists; otherwise stock/resource state can drift or continue changing after the original condition ended.

### 4.4 Localisation

HER maintains localisation under both Russian and English directories, including replacement localisation trees.

Project convention:

- do not transliterate missing English text when a proper translation is needed;
- do not invent text when the task is specifically to preserve/translate existing Russian localisation;
- when adding gameplay content, remember both required localisation keys and correct YAML/file encoding/format expectations.

Exact localisation parser/encoding rules should be expanded here only after direct verification from current HER files.

---

## 5. Map and state safety reference

Map work is one of the highest-risk HER areas. Validate topology and references before assuming the game will recover from a malformed map entry.

### 5.1 Known crash / serious error patterns

#### Coastal province / port mismatch — CONFIRMED-HER

HER encountered the game error:

`Province 15439 is setup as coastal but has no port building in the nudger. This will likely crash the game.`

Practical rule:

- if a province is configured in a way that requires a valid coastal/port building setup, ensure the corresponding map building data is consistent;
- treat coastal/port mismatches as crash-risk errors, not cosmetic warnings.

#### Province with no strategic region — CONFIRMED-HER

HER has previously produced `MAP_ERROR` entries for provinces with no strategic region assigned.

Practical rule:

- every playable map province that requires strategic-region membership must be assigned exactly where expected after province-grid edits;
- after transferring/redrawing provinces, audit strategic-region membership before treating the map pass as complete.

#### State/province mismatch in buildings — CONFIRMED-HER

HER previously hit an error where an `air_base` entry in `map/buildings.txt` referenced a province expected in one state but actually belonging to another.

Practical rule:

- after moving province/state boundaries or airport locations, validate every touched `map/buildings.txt` province against its current state;
- do not assume old building placements remain legal after province reassignment.

#### BOM / malformed text files — CONFIRMED-HER

HER previously encountered BOM-related problems in state-history files.

Practical rule:

- preserve expected text encoding when programmatically editing HOI4 text files;
- avoid introducing BOMs unless the specific file format explicitly requires them.

### 5.2 HER map-editing conventions — CONFIRMED-HER

For the Soviet/European map rework, current project conventions include:

- preserve state borders unless a task explicitly changes them;
- preserve urban cells unless explicitly redesigning the city;
- avoid four-way province corners;
- avoid excessively elongated, rectangular, tiny, or otherwise pathological provinces;
- rivers should follow province borders where practical;
- river branches/intersections must follow the project's established color/topology conventions rather than visually plausible but invalid pixel patterns;
- airports should normally be placed on suitable terrain near settlements; major capitals may require urban placement by design;
- supply hubs should normally be tied to meaningful urban/VP locations rather than arbitrary non-VP provinces;
- railway topology should avoid gratuitous loops and dead ends and should connect important VPs/regions according to the HER railway design rules.

### 5.3 Terrain / forests — CONFIRMED-HER

For the Soviet terrain pass:

- terrain classification must correspond to the province grid rather than being painted independently of province boundaries;
- urban terrain must remain inside intended urban provinces;
- trees must correspond to provinces actually classified as forest;
- when forest terrain is removed, obsolete tree placement must also be removed.

Known HER terrain-map forest color reference used during prior work: `#59c755` on `terrain.bmp`.

---

## 6. Character and general-system conventions

### 6.1 General stat model — CONFIRMED-HER

HER interprets general skills as:

- `attack_skill` — mechanized, armored, and mobile offensive operations;
- `defense_skill` — infantry/artillery competence;
- `planning_skill` — operational and staff planning;
- `logistics_skill` — initiative, independence, and flexibility.

Project balance rule:

`attack + defense + planning + logistics = 4 × skill`

Apply the rule to the intended base stat model before unrelated perk modifiers where applicable.

### 6.2 Rank personality traits — CONFIRMED-HER

HER uses separate personality traits for ranks, including:

- `gen_lt`
- `gen_pk`
- `gen_arm`
- `gen_fm`
- `tank_gen_lt`
- `tank_gen_pk`
- `tank_gen_arm`
- `tank_gen_fm`

These rank traits affect experience gain behavior and should be considered when editing generals rather than recreated ad hoc.

---

## 7. Storage / resource-system lessons

### 7.1 Warehouses — CONFIRMED-HER

HER has a custom warehouse/storage system.

Verified design lessons from previous fixes:

- automatically covering a deficit must stop precisely once the deficit is gone;
- rounding behavior matters and must not accumulate systematic resource drift;
- country resource bonuses must not be accidentally counted twice when the storage system is intended to operate on the underlying resource flow;
- empty-storage states/events need explicit handling.

Before altering this subsystem, inspect the current implementation rather than rebuilding its logic from memory.

---

## 8. China aid / credit / logistics system

Status: **PROTOTYPE IMPLEMENTED — IN-GAME VALIDATION REQUIRED**

### 8.1 Current architectural decisions — CONFIRMED-HER DESIGN

The planned system links foreign military aid to physical logistics routes and Chinese repayment/resource obligations.

Current agreed principles:

- China can receive a credit denominated in a stockpile/resource obligation, e.g. a large tungsten debt.
- Repayment is delivered over time and constrained by available supply/logistics routes.
- Route capacity can therefore directly affect how quickly the debt is serviced and how quickly aid can flow.
- Japanese conquest/interdiction of relevant routes should reduce or cut aid throughput.
- China receives purchasing power/subsidies that can be used for equipment purchases and/or scripted direct purchases.
- The vanilla/HER warehouse-stockpile concept should be reused where practical instead of inventing a completely separate inventory abstraction.

### 8.2 US staging-country architecture — CONFIRMED-HER DESIGN

A service country, currently planned as `BRA`, is used only for the US-led equipment pipeline.

Current design:

- USA sends equipment to `BRA`.
- `BRA` forwards equipment onward according to available throughput/capacity.
- USSR sends aid directly rather than through the service country.
- UK aid is combined with the US pipeline for this system.
- `BRA` must be prevented from consuming or misusing staged equipment.

Required safeguards for the service country include:

- no useful airbase deployment path for staged aircraft;
- no normal division deployment consuming stored equipment;
- no market behavior that can list/export the staged stockpile in an unintended way;
- other safeguards should be added only using verified HOI4 mechanisms.

China is intended to be an exception to ordinary player-only gating where needed so that the system can function normally for China without broadly enabling unwanted AI behavior.

### 8.3 Experimental / not yet syntax-verified

The first isolated implementation lives on branch `china-foreign-aid`.

Prototype files:

- `common/decisions/HER_CHI_aid_decisions.txt`
- `common/decisions/categories/HER_CHI_aid_decision_categories.txt`
- `common/on_actions/HER_CHI_aid_on_actions.txt`
- `common/scripted_effects/HER_CHI_aid_scripted_effects.txt`
- `common/scripted_triggers/HER_CHI_aid_scripted_triggers.txt`
- `common/ai_strategy/BRA_service_country.txt`
- `events/HER_CHI_aid_events.txt`
- `localisation/replace/{russian,english}/HER_CHI_aid_l_*.yml`

Current prototype behavior:

- China can request a US commodity credit after `1940.1.1` while at war with Japan.
- US acceptance grants `500000` credit and creates `1000000` tungsten debt.
- A first test purchase transfers `5000` infantry equipment from USA to the `BRA` staging stockpile.
- `BRA` forwards a fixed packet of `1000` infantry equipment per daily tick when Western import capacity permits it.
- China exports a fixed packet of `1000` stored tungsten to USA per daily tick when Western export capacity, Chinese stock, debt, and free US tungsten-storage capacity all permit it.
- Current route capacity values are experimental: sea route `5000`, Hanoi route `2500`, Burma route `2500`.
- Cargo priority splits are military `80/20`, balanced `60/40`, and debt service `40/60` for imports/exports.

Route state IDs used by the prototype:

- Chinese sea ports: `592` Guangzhou, `593` Guangdong, `595` Fujian, `613` Shanghai.
- Hanoi route: `325` Yunnan and `671` Tonkin.
- Burma Road: `288` Western Burma, `325` Yunnan, `640` Shan State, `747` Dali.

Repository verification established that HER already uses the following fixed-amount pattern:

`send_equipment = { target = TAG type = infantry_equipment amount = 500 old_prioritised = yes }`

This syntax is therefore **CONFIRMED-HER** for fixed amounts and equipment archetypes. Variable `amount` remains unverified; the prototype deliberately uses fixed packets.

The exact runtime behavior of staged USA → `BRA` → China transfers, route triggers, cross-country variable display, and the interaction between imported tungsten and warehouse caps remains **EXPERIMENTAL** until checked in game and in `error.log`.

Do not generate final production code for these mechanisms solely from remembered syntax. Inspect current HER/vanilla examples first.

---

## 9. AI philosophy

### CONFIRMED-HER

HER's main target is historical multiplayer. AI is not the primary balancing target.

However, AI/player gating must be handled deliberately. Do not sprinkle `is_ai = no` into systems without checking whether specific countries (notably China in the planned aid system) need explicit exceptions.

---

## 10. Experimental / unverified technical notes

This section is intentionally allowed to contain ideas that may be wrong.

Rules:

- never cite this section as proof that syntax works;
- never copy an effect/trigger from here into production code without verification;
- once verified, move the finding to the relevant confirmed section.

Current items:

- Fixed-amount staged `send_equipment` syntax is repository-verified, but the complete two-stage pipeline still requires an in-game stockpile test.
- `BRA` already has market access disabled, division templates locked, zero research slots, zero convoys, no starting airbase in state `500`, and no military factories there. A dedicated AI strategy now assigns `-10000` air-base building target. Confirm in game that it never creates an airbase or consumes staged equipment.
- Route throughput currently uses fixed daily packets. Dynamic packet sizes and equipment-specific cargo weights remain future work after the first vertical test passes.

---

## 11. Known project workflow rules

### Branch discipline

HER frequently uses feature branches for large reworks. Before writing files, verify which branch the user wants changed when the task is branch-specific.

Do not assume the default branch is the active development branch merely because GitHub defaults to `main`.

### Large map / binary work

Map binaries and large visual assets require extra caution. Text-context notes should record what was changed, but do not assume a textual GitHub diff fully describes the state of binary map assets.

### Context maintenance

When future work establishes new knowledge, update this file proactively.

Good candidates for automatic updates:

- a new engine quirk is confirmed;
- a parser/map error is diagnosed and fixed;
- a reusable scripted-effect/trigger pattern is proven working;
- a system architecture is approved;
- an important country/state/province/strategic-region ID is assigned a stable role;
- a project-wide balance convention is approved;
- a subsystem reaches a known-good milestone;
- an old assumption is disproven.

Do **not** bloat this file with:

- transient brainstorming;
- every numeric balance tweak;
- abandoned options with no future diagnostic value;
- whole chat transcripts;
- speculative syntax presented as fact.

---

## 12. Future structure

As this reference grows, split detailed topics into dedicated files while keeping this document as the index and high-level source of truth.

Suggested future layout:

```text
docs/
├── HER_CONTEXT.md
├── engine/
│   ├── scripting.md
│   ├── map-safety.md
│   └── localisation.md
├── systems/
│   ├── warehouses.md
│   ├── china-aid.md
│   ├── generals.md
│   └── mio.md
└── map/
    ├── map-rules.md
    ├── railways.md
    └── weather.md
```

Split only when the main file becomes cumbersome; avoid fragmentation for its own sake.

---

## 13. Change log

### 2026-09-05

- Created persistent HER development context/reference.
- Added project workflow and confidence-label rules.
- Recorded current descriptor/replacement-path implications.
- Added initial map crash/safety lessons from prior HER debugging.
- Added general stat/rank conventions.
- Added warehouse-system lessons.
- Added initial China aid architecture and clearly marked unverified implementation details.
- Established proactive maintenance policy for future HER sessions.

### 2026-09-06

- Created the `china-foreign-aid` feature branch and implemented the first isolated China-aid prototype.
- Recorded verified fixed-amount `send_equipment` syntax already used by HER.
- Added the initial US tungsten credit, Western staging through `BRA`, route-capacity calculation, transport priorities, one rifle contract, and fixed-packet tungsten repayment.
- Added China and USA exceptions to the tungsten warehouse player-only gate so the credit pipeline can operate when either tag is AI-controlled.
- In-game testing confirmed that rifle staging/delivery and the displayed credit, debt, route-capacity, and pending-rifle values work. Added persistent last-daily-tick telemetry for actual tungsten exports and rifle deliveries, plus the import/export capacity allocation shown in the decision category.
- Replaced the legacy China-route factory abstraction with physical throughput: Burma, the Hump, and Ledo now increase route capacity instead of granting offsite military factories. Legacy close/reopen decisions and their state-control on-action were disabled because route triggers now react directly to map control.
- China no longer purchases equipment unilaterally from the US stockpile. The United States offers rifle, artillery, truck, and aircraft contracts through events; accepted equipment and unilateral US/UK grants are staged in BRA and delivered in equipment-specific daily packets.
- China may also initiate requests for the same four US equipment contracts. The request creates an event for the United States; approval requires the full equipment package to be present in the US stockpile, while refusal spends no Chinese credit. Thus neither side can unilaterally remove equipment from the other's stockpile.
- Expanded US contracts into eight physical cargo classes: a full infantry package (5,000 rifles, 2,400 machine guns, 800 mortars, 700 handheld anti-tank weapons), a mixed artillery package (240 field, 80 heavy, 120 anti-tank, 120 anti-air guns), 10,000 ammunition, 1,000 support equipment, 1,000 trucks, and separate 40-aircraft fighter, CAS, and light tactical-bomber wings. Grenades remain abstracted in `infantry_equipment` because HER has no separate grenade archetype.
- Added a two-stage delivery delay. A supplier immediately transfers accepted equipment to service tag `BRA`, but it becomes route-dispatchable only after a 14-day staging event. Each capacity-limited packet then spends another 7 days in an in-transit variable before `BRA` transfers the actual equipment to China. Parallel contracts therefore retain independent timers.
- The Chinese and American decision-category tooltips now expose staged cargo, cargo already in transit, and the amount or packet count dispatched during the last daily tick for every cargo class.
- In-game follow-up testing exposed three integration rules: route expansion decisions belong only to the US/UK side; state `601` (Xikang) has no controller and therefore cannot gate the Hump; and the US credit must establish a tungsten export depot in state `605` (Chongqing), otherwise loss of China's original warehouse reduces `tungsten_cap` to zero and destroys the stored balance.
- Aircraft route packets were reduced from 20 to 5 aircraft (250 cargo units). Dispatch now compares the pending counter with actual BRA stock minus equipment already marked in transit, so partial receipts such as 15 aircraft are delivered instead of becoming permanently stuck behind a 20-aircraft threshold.
- Replaced daily dispatch-only UI telemetry with mirrored China/USA logistics telemetry for all fourteen physical equipment components. Both decision categories display route queue, in-transit cargo, arrivals during the rolling last seven days, and cumulative arrivals. Each real arrival schedules its own seven-day expiry event, so the weekly figure is rolling rather than tied to a global weekly reset.
- Hidden staging and arrival events use the repository-proven multiline `hidden = yes` + `immediate` + empty `option` structure. Compact one-line hidden events were removed after `her_chi_aid.102` appeared in game as an invalid event.
- Added separate `BRA_CHI_queued_*` counters. They increase immediately when a contract transfers equipment to BRA, remain unchanged during the 14-day preparation period, and decrease only when capacity moves a packet into `BRA_CHI_in_transit_*`. Thus the UI no longer shows zero between contract acceptance and staging completion. A daily compatibility repair seeds these counters from older `pending` values in existing saves.
