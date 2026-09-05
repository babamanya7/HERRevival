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

Status: **DESIGN IN PROGRESS**

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

The exact HOI4 implementation of staged `send_equipment`, throughput-limited forwarding, service-country restrictions, and market exclusion is **EXPERIMENTAL** until checked against actual working effects/triggers in the current game/mod version.

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

- Exact safest pattern for using `send_equipment` as a staged USA → service country → China pipeline still requires verification in the current HOI4 version.
- Exact means of making the service country unable to deploy divisions, aircraft, or participate in the market must be established from working game definitions rather than guessed.
- Exact route-throughput accounting for China aid remains a design task.

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
# Naval critical damage implementation

- Naval combat uses critical damage as the primary route to mission kills, major loss of combat capability and catastrophic losses; ordinary hits should later be balanced toward limited STR/ORG damage.
- Criticals are split between hull-wide casualties on naval sub-units and local system casualties attached to equipment modules.
- Each physical module family should have at least one relevant critical zone; role/classification modules are excluded because they are not physical compartments.
- Carrier criticals separately cover flight deck, aircraft elevators, hangar, aviation fuel, flight control and damage control. Wooden and armored decks retain different risk profiles.
- Naval criticals use the dedicated 41-frame `GFX_HER_critical_damage_icons` atlas. Each critical ID has a unique icon and frame.
- Carrier deck damage follows two opposite profiles: wooden flight decks suffer critical damage more often but impose a lighter direct flight-operations penalty, while armored flight decks are harder to damage but a successful penetration/deformation causes a severe mission kill and additional repair damage.
- Carrier mission kills are cumulative rather than binary. Deck holes, elevators, arresting gear, propulsion, flight control, hangar fire and aviation-fuel/ready-ordnance casualties stack into operational loss without requiring the hull to sink.
- Midway and the Solomon carrier actions are the historical baseline for critical balance: local damage should cause specific system failures, while catastrophic loss emerges from fire/flooding cascades, electrical or ventilation failures and disrupted damage-control organization.
- Balance order: critical map and effects, critical probability, severity/duration, ordinary hit damage, then repair/operational absence. Do not increase aircraft target weight merely because a ship is already damaged.
- Pre-defines critical scale: common local casualties weight `0.65-1.0`; ship-wide mission-kill casualties `0.25-0.65`; catastrophes `0.05-0.2`. Never use a critical-hit damage multiplier below `1.0`.
- First naval defines baseline: surface STR/ORG conversion `0.50/0.90`, naval-air STR/ORG conversion `1.25/1.75`, base critical chance `0.10`, global critical damage multiplier `2.0`, torpedo critical chance/multiplier `0.15/1.5`, and defined-part damage chance `0.65` from surface fire / `0.80` from air. Base hit chance remains unchanged for isolated testing.
- `toxic_gas_leakage` is submarine-only. Carriers instead use the separate aviation-fuel-fire casualty.
- Detailed implementation notes: `docs/systems/naval-critical-damage.md`.
