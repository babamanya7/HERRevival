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

## Strong current fighter-bomber migration candidates
These are candidates for the implementation mapping pass, not blind final assignments:
- GER: Fw 190A/F family;
- SOV: LaGG-3 branch;
- USA: P-47 family;
- ENG: Typhoon/Tempest strike-oriented branch.

Primary-fighter counterparts that should remain distinct:
- GER: Bf 109 family;
- SOV: Yak / later La fighter lines as determined by full KB audit;
- USA: P-51 family;
- ENG: Spitfire family.

## Follow-ups
- Audit Yakovlev, Mikoyan-Gurevich and other Soviet fighter MIOs for cross-family collisions.
- Audit remaining US fighter MIOs (Curtiss, Bell, Lockheed where relevant) and decide whether interceptor / fighter-bomber / heavy-fighter identities resolve additional conflicts.
- Audit British Gloster/Bristol/de Havilland branches for interceptor/heavy-fighter/night-fighter conflicts.
- Audit Japan and France after GER/SOV/USA/ENG migration rules are stable.
- Build a final country-by-country migration table before touching production data.
