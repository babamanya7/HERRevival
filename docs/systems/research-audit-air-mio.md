# HER Mod — Air MIO / KB Audit

Status: IN PROGRESS

Companion audit for Air Designer 2.0 and the distinct fighter-bomber archetype.

## Core systemic finding
Current aircraft MIO trees frequently encode distinct historical aircraft families while still applying them to the same generic equipment archetype via `limit_to_equipment_type`. This creates real conflicts between KB families and historical series that are not merely cosmetic.

The planned fighter-bomber duplicate archetype should be used as a structural conflict resolver, not just as an extra mission role.

## Germany
### Messerschmitt
`GER_messerschmitt_organization` researches broad light-fighter and medium/heavy-air categories. Bf 109E/F/G/K branches are built around small generic fighter airframes; Bf 109F-specific traits are limited to `small_plane_airframe_2`.

### Focke-Wulf
`GER_focke_wulf_organization` covers light fighter + CAS + medium aircraft. Fw 190A and the separate Fw 190F/Jabo branch are both still limited to `small_plane_airframe_2`.

This is the archetypal conflict: Bf 109F and Fw 190A/F represent different historical families and operational emphases but compete for the same generic equipment identity.

Air Designer 2.0 target:
- keep the Bf 109 family on the primary fighter identity;
- move Fw 190A/F strike-oriented branches to the new small fighter-bomber identity where historically and mechanically appropriate;
- audit Fw 190D/Ta 152 separately, because the current Fw 190D line already uses `small_plane_interceptor_airframe_2`, showing that HER already uses role/archetype reassignment to separate late variants.

## USSR
### Lavochkin / LaGG
`SOV_lavochkin_organization` is currently in `mio_cat_all_light_fighter_and_modules`.

LaGG-3 is limited to `small_plane_airframe_2`, and there is already an explicit trait named `mio_lavochkin_lagg3_fighter_bomber`, but the equipment identity remains the generic fighter airframe.

La-5 then transitions to `small_plane_airframe_3`.

This is strong internal evidence that HER already conceptually treats LaGG-3 as strike-capable/fighter-bomber material but lacks a separate equipment channel to represent it.

Air Designer 2.0 target:
- evaluate LaGG-3 as a fighter-bomber identity candidate;
- keep La-5/La-7 on the primary fighter identity unless the full historical-series review suggests otherwise;
- update Lavochkin MIO equipment categories so the LaGG branch and later La branch can address different equipment identities cleanly.

### Yakovlev
`SOV_yakovlev_organization` is a pure light-fighter MIO and currently maps Yak-1, Yak-7 and early Yak-9 progression onto generic small fighter airframes.

Observed mapping:
- Yak-1 -> `small_plane_airframe_2`;
- Yak-7 -> `small_plane_airframe_2`;
- Yak-9 branch transitions to `small_plane_airframe_3` once `advanced_small_airframe` is available.

This family is internally coherent as the Soviet primary-fighter line. Unlike LaGG-3, no explicit strike/fighter-bomber identity is visible in the audited Yak traits.

Air Designer 2.0 target:
- Yak-1/7/9/3 family should remain in the primary fighter identity by default;
- preserve its lightweight / agility / production-efficiency design language rather than forcing role reassignment merely to reduce overlap;
- use it as the clean Soviet fighter counterpart against LaGG-derived fighter-bomber identity and MiG interceptor identity.

### Mikoyan-Gurevich
`SOV_mikoyan_gurevich_organization` already demonstrates the desired role separation much better than most current MIOs.

Observed mapping:
- MiG-1 -> `small_plane_interceptor_airframe_1`;
- MiG-3 -> `small_plane_interceptor_airframe_2`;
- MiG-9 later moves to `small_plane_airframe_4` in the jet era.

The MiG-1/3 traits explicitly emphasize high-altitude layout/engine performance. This is a strong precedent for keeping interceptor as a true separate equipment identity rather than folding all Soviet fighters together.

Air Designer 2.0 target:
- keep MiG-1/3 in the interceptor identity;
- preserve high-altitude/interception-focused module and MIO restrictions;
- review MiG-9 separately when jet-role architecture is redesigned.

### Polikarpov
`SOV_polikarpov_organization` currently maps:
- I-15/I-153 -> `small_plane_airframe_0`;
- I-16 -> `small_plane_airframe_1`;
- I-185 -> `small_plane_airframe_2`.

The I-15/I-16 line is a coherent early primary-fighter family. I-185 collides chronologically/archetypically with Yak-1/7, LaGG-3 and other improved-small-airframe families, but this is not automatically a reason to create another role identity: it is primarily an alternate fighter design school rather than a distinct operational class.

Air Designer 2.0 target:
- keep I-15/I-16 as early primary fighters;
- treat I-185 as an alternate/experimental primary-fighter branch unless later historical-role review provides a stronger justification for interceptor or fighter-bomber reassignment;
- solve same-role KB competition through MIO/family availability and historical production logic, not by inventing fake operational roles.

### Soviet role map — current preferred direction
- Primary fighter: Polikarpov early line -> Yak family / later La family;
- Interceptor/high-altitude: MiG-1/3;
- Fighter-bomber/strike: LaGG-3 branch candidate;
- Dedicated CAS: retain dedicated CAS bureaus/airframes separately.

This is significantly cleaner than the current generic-fighter pile-up because the new fighter-bomber identity creates a third real small-aircraft production channel alongside fighter and interceptor.

## USA
### Republic P-47
The Republic tree contains a dedicated P-47 fighter-bomber branch (`mio_republic_p47_fighter_bomber`, external ordnance, ground attack), but every relevant P-47 trait remains limited to `small_plane_airframe_3`.

### North American P-51
The P-51 line also uses `small_plane_airframe_3`.

Thus P-47 and P-51 currently collide on the same generic fighter equipment identity despite the P-47 tree already containing explicit strike/fighter-bomber specialization.

Air Designer 2.0 target:
- strong candidate: P-47 -> fighter-bomber / strike-oriented identity;
- P-51 -> primary fighter identity;
- revise Republic / North American MIO applicability, starting variants and OOBs accordingly.

### Curtiss / P-39 / P-40 branch
The current `USA_curtiss_organization` contains a shared Allison V-1710 branch that splits into P-39 and P-40 paths.

Observed mapping:
- P-39 cannon and late P-39 traits -> `small_plane_airframe_2`;
- P-40E / P-40N -> `small_plane_airframe_2`.

This creates another same-archetype collision, but the correct solution is not obvious enough to assign blindly.

Preliminary role interpretation for redesign:
- P-40 remains a conventional primary fighter / fighter-bomber-capable family depending variant and theatre;
- P-39 is a stronger candidate for a specialized low-altitude / cannon-armed fighter identity, but HER currently has no dedicated low-altitude type channel;
- neither should be force-mapped to interceptor merely to free archetype space unless the resulting mission/bonus semantics fit.

Air Designer 2.0 implication:
- the new fighter-bomber identity can potentially absorb later strike-oriented P-40 variants if this helps MIO and production separation;
- P-39 may remain primary fighter or become a family-specific variant inside the primary-fighter channel rather than receiving an artificial role;
- the Curtiss tree should be reviewed together with Bell naming/ownership representation, because the current tree groups P-39/P-40 under one organization even though the historical manufacturers differ.

### Lockheed / P-38
`USA_lockheed_organization` already uses the medium heavy-fighter identity cleanly. Its initial applicability includes `medium_plane_fighter_airframe_2/3`; P-38 progression is limited to those medium fighter archetypes.

Air Designer 2.0 target:
- retain P-38 as a medium heavy-fighter family rather than forcing it into the new small fighter-bomber channel;
- represent long range, twin-engine layout, concentrated nose armament and high-altitude performance through the new physical layout/module system;
- allow strike capability through compatible payload modules without changing its core stockpile identity unless a later historical variant specifically warrants a separate role.

### US role map — current preferred direction
- Primary fighter: P-51 and conventional P-40/P-39 branches unless later reassigned by variant;
- Fighter-bomber/strike: P-47 is the strongest clear candidate;
- Heavy fighter: P-38 / Lockheed medium-airframe family;
- Dedicated CAS/naval: Douglas and other specialized MIOs remain separate.

The US case therefore does not require every conflicting family to receive a new role. The fighter-bomber archetype should be used where the operational identity is real (P-47), while remaining same-role manufacturer competition should be handled through KB/MIO availability and historical variant mapping.

## United Kingdom
### Supermarine
Spitfire I/II/V/IX and related traits use `small_plane_airframe_2`; Supermarine is a pure light-fighter MIO.

### Hawker
Hawker covers both light-fighter and CAS research categories. Hurricane is on `small_plane_airframe_1`; Typhoon progression is on `small_plane_airframe_2`.

The Spitfire vs Typhoon conflict mirrors the German case: both can occupy the same generic small fighter archetype even though Typhoon naturally fits a strike/fighter-bomber identity much better than the Spitfire.

Air Designer 2.0 target:
- Spitfire -> primary fighter identity;
- Typhoon/Tempest strike-oriented branch -> strong fighter-bomber identity candidate, subject to detailed historical mapping by variant;
- Hurricane should be reviewed separately because early-war fighter/ground-attack variants may justify either staying fighter or branching into fighter-bomber later.

### de Havilland / Mosquito
`ENG_de_havilland_organization` is an especially useful architectural precedent because the same physical Mosquito platform is already represented through multiple duplicate equipment identities.

Observed mapping:
- Mosquito F/NF branch -> `medium_plane_fighter_airframe_2`;
- Mosquito bomber branch -> `medium_plane_airframe_2`;
- Mosquito fighter-bomber branch -> `medium_plane_cas_airframe_2`.

The night-fighter specialization remains inside the medium fighter identity rather than receiving a separate stockpile/archetype. This is desirable: night fighting is primarily a mission/equipment/configuration specialization (radar, crew, guns, interception doctrine), not necessarily a separate physical aircraft class.

Air Designer 2.0 target:
- preserve Mosquito F/NF as medium heavy fighter;
- preserve bomber and fighter-bomber derivatives as distinct equipment identities where their operational/production use differs;
- use the Mosquito pattern as a direct precedent for the new small fighter-bomber architecture: one physical platform generation can support several role-specific duplicate archetypes without inventing new hardcoded engine types;
- deepen the night-fighter distinction through radar/avionics, crew, armament, range and night-performance modules rather than a new `night_fighter` stockpile type.

### Bristol / Blenheim-Beaufort-Beaufighter
`ENG_bristol_organization` also already separates medium-airframe roles well:
- Blenheim -> `medium_plane_airframe_1`;
- Beaufort -> `medium_plane_naval_bomber_airframe_1`;
- Beaufighter -> `medium_plane_fighter_airframe_1`.

This again supports keeping heavy fighter as the main two-engine fighter identity and using mission/layout modules for night fighter or strike variants.

Air Designer 2.0 target:
- retain Beaufighter as medium heavy fighter by default;
- permit night-fighter specialization through radar/crew/weapon layout;
- review strike/torpedo Beaufighter derivatives at variant level rather than creating a new broad class unless production/wing identity genuinely benefits.

### Gloster
`ENG_gloster_organization` maps Gladiator to the early generic small fighter and Meteor to `small_plane_airframe_4`. It does not currently create a separate interceptor or night-fighter role problem.

Air Designer 2.0 target:
- keep Gladiator/Meteor in primary-fighter lineage unless jet architecture later creates a stronger reason to split roles;
- review the broad `research_categories = { fighter }` syntax during category cleanup for consistency with HER's custom MIO categories.

### UK role map — current preferred direction
- Primary fighter: Spitfire; Hurricane early; Meteor later;
- Fighter-bomber/strike: Typhoon/Tempest strong candidate, plus selected Hurricane variants if desired;
- Heavy fighter: Beaufighter and Mosquito F;
- Night fighter: specialization inside heavy-fighter identity through radar/crew/modules, not a new stockpile class;
- Medium fighter-bomber: Mosquito FB already has a useful distinct duplicate identity via `medium_plane_cas_airframe_2`.

## Night-fighter design rule — accepted direction
Do not create a separate night-fighter equipment identity by default.

Preferred model:
`heavy fighter / interceptor base identity -> radar + avionics + crew/layout + armament + mission bonuses -> night-fighter configuration`.

Create a separate stockpile identity only if gameplay requires different reinforcement/wing handling strongly enough to justify the extra archetype. Current Mosquito and Beaufighter architecture indicates that this is unnecessary for the normal WWII night-fighter case.

## Systemic MIO migration requirements
Introducing a new fighter-bomber duplicate archetype requires more than adding a new MIO category. At minimum:
- create/assign a fighter-bomber equipment category usable by MIO `equipment_type` blocks;
- create `mio_cat_all_fighter_bomber_and_modules` or an equivalent narrow category if the MIO/category system supports it cleanly;
- decide whether common small-airframe technologies remain under broad generic airframe categories while fighter-bomber-specific modules use the new role category;
- revise `research_categories` for every affected aircraft MIO to avoid unrelated research bonuses spilling across fighter / fighter-bomber / CAS;
- revise every `limit_to_equipment_type` in affected MIO trees;
- revise `available` gates tied to airframe generations where a historical family moves to another duplicate archetype;
- revise starting MIO assignment / auto-assign filters;
- revise historical variants, OOB equipment, production lines and stockpiles;
- revise localization/tree headers only where the equipment identity changes affect display or progression clarity;
- audit production bonuses so MIO experience/funds are not split or duplicated unintentionally when a family changes archetype;
- audit focus/event research bonuses that currently target broad fighter/CAS MIO categories.

## Design rule for future MIO trees
A historical KB should not be forced to share one generic equipment identity with another unrelated aircraft family merely because both fit the same physical airframe generation.

Preferred mapping:
`historical family -> operational identity -> duplicate archetype -> subunit category -> MIO equipment category -> family-specific trait limits`.

The physical airframe generation remains common technology; the equipment identity expresses the actual role/family that production and air wings use.

A second rule is equally important: do not invent fake operational identities merely to separate manufacturers. If two families are genuinely both primary fighters, their competition should be represented through MIO availability, production choices and variant design rather than abusing interceptor/fighter-bomber categories.

## Strong current fighter-bomber migration candidates
These are candidates for the implementation mapping pass, not blind final assignments:
- GER: Fw 190A/F family;
- SOV: LaGG-3 branch;
- USA: P-47 family;
- ENG: Typhoon/Tempest strike-oriented branch.

Primary-fighter counterparts that should remain distinct:
- GER: Bf 109 family;
- SOV: Yak / later La fighter lines, with Polikarpov as early/alternate fighter school;
- USA: P-51 family, with P-39/P-40 reviewed by variant rather than automatically reassigned;
- ENG: Spitfire family.

Interceptor identities already supported by current HER architecture:
- SOV: MiG-1/MiG-3;
- GER: late Fw 190D path currently uses interceptor airframe and must be reassessed alongside Ta 152.

Heavy-fighter identities already cleanly represented on medium airframes:
- USA: P-38 / Lockheed;
- ENG: Beaufighter / Bristol and Mosquito F/NF / de Havilland.

## Follow-ups
- Audit Japan and France after GER/SOV/USA/ENG migration rules are stable.
- Build a final country-by-country migration table before touching production data.
- Audit MIO category definitions themselves to confirm how a new fighter-bomber category must be wired into `equipment_type` / research categories / module categories.
- Audit starting OOB/variants for Mosquito, Beaufighter, P-38, P-47, Fw 190, LaGG-3 and Typhoon to estimate migration cost.
