# Balkans 1940–41 event chain

## Design rule

The Balkan sequence is integrated into existing HER country systems. Do not create a parallel decision/controller system for Bessarabia, the Second Vienna Award, Southern Dobruja, Antonescu's rise, or the post-war partition of Yugoslavia/Greece where existing focuses/events already handle them.

Historical timing is enforced mainly by country events and broad date windows. Exact historical dates are not required except for the German response to the Belgrade coup: Germany declares war on Yugoslavia exactly 10 days after the coup event fires.

## Axis accessions

### Hungary
- `events/Hungary.txt`, `hungary.7`.
- Historical window opens after `1940.11.10`.
- Requires `HUN_joint_aluminum_mining_company`, French capitulation, Germany alive and faction leader.
- Event directly adds Hungary to Germany's faction.
- `HUN_join_axis` remains available as a manual/non-historical focus path, but it is removed from `HUN_historical_strategy_plan.txt`.
- The old historical `alliance = GER` AI strategy is also removed so ordinary diplomacy cannot pre-empt the event and pull Hungary into the Axis early.

### Romania
- Reuses existing `events/Romania.txt` event `romania.6`; no parallel accession event.
- Historical window opens after `1940.11.10`.
- Keeps the territorial-crisis prerequisites: Bessarabia ceded, Second Vienna Award accepted, Treaty of Craiova accepted.
- Also requires `ROM_force_abdication`, integrating Axis entry with the existing Antonescu political chain.
- Replaces the old generic faction invitation with direct accession to Germany's faction.

### Bulgaria
- `events/Bulgaria.txt`, `bulgaria.6`.
- Historical window opens after `1941.2.15` with short MTTH.
- Requires Bulgarian ownership of Southern Dobruja, French capitulation, and Germany alive as faction leader.
- Event adds Bulgaria to the Axis but does not script Bulgaria into the wars against Yugoslavia or Greece.

## Yugoslavia and Greece

Implemented in `events/Yugoslavia.txt` under namespace `her_balkans`.

1. `her_balkans.1` — Yugoslavia signs the Tripartite Pact in the second half of March 1941 once Hungary, Romania and Bulgaria are already in Germany's faction. This is represented by `HER_YUG_signed_tripartite_pact`; Yugoslavia is deliberately **not** added to the Axis faction to avoid accidental war propagation during the brief pre-coup period.
2. `her_balkans.2` — Belgrade coup, scheduled 2 days after signing. Clears the pact flag, sets `HER_YUG_belgrade_coup`, applies a stability hit, and schedules the German response.
3. `her_balkans.3` — Directive No. 25. Fires exactly 10 days after the coup and declares the German-Yugoslav war in `immediate`, so the timing cannot be delayed by a player leaving an event window open. Italy joins the Yugoslav war if still aligned with Germany. If the Italian-Greek war is still active, Germany also declares war on Greece at this moment.
4. `her_balkans.4` — Hungary enters the Yugoslav campaign 4 days after Germany, provided Yugoslavia still exists and Hungary is not already at war with it.

Bulgaria is intentionally not called into either war by this chain.

## Existing systems left authoritative

- Soviet Bessarabian demand/cession chain.
- German Second Vienna Award focus and associated events.
- Treaty of Craiova / Southern Dobruja events.
- Romanian Antonescu focus chain.
- German scripted post-campaign partition/fate focuses for Yugoslavia and Greece.

Do not add duplicate partition logic to `her_balkans`.

## Localisation

New keys are in:
- `localisation/russian/HER_balkans_events_l_russian.yml`
- `localisation/english/HER_balkans_events_l_english.yml`
