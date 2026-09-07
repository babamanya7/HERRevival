# HER AI Hands-off Test 1 — Issue Log, continued

Status: ACTIVE
Branch: `AI-rework`
Parent log: `docs/systems/ai-hands-off-test-1-issues.md`

This file continues the live Test 1 issue log. It will be consolidated into the main issue log during the post-run batch.

## Observed issues

### HO1-019 — Remove artificial Chinese division spawning from `CHI_div_spam`
- Date: observed/identified during Test 1.
- Country: CHI.
- Subsystem: `events` / scripted AI helpers / force generation.
- Severity: `MAJOR`.
- Observed: China still benefits from the legacy `CHI_div_spam` scripted division spawn layer.
- Expected: Chinese force generation should come from normal recruitment, templates, production and bounded historical AI behavior rather than free spawned divisions.
- Batch action: locate every active consumer/trigger of `CHI_div_spam` and remove the division-spawn behavior completely. Re-evaluate China/Japan balance only after this artificial force source is gone, because it may materially contribute to HO1-012 and the Japanese collapse.

### HO1-020 — Bulgaria sends troops to the Eastern Front instead of remaining a Balkan/local-defense participant
- Date: observed after the Axis-Soviet war begins in Test 1.
- Country: BUL.
- Subsystem: `front` / faction theater allocation / expeditionary behavior.
- Severity: `MAJOR`.
- Observed: Bulgarian divisions travel to fight on the German-Soviet front.
- Expected: AI Bulgaria should remain primarily committed to Balkan occupation, coastal/local defense and historically plausible regional duties rather than contributing a substantial field force to Barbarossa.
- Batch action: add strong Balkan/home-theater retention and negative/ignore weighting for the Soviet front for AI BUL, while preserving emergency behavior if Bulgaria itself is directly threatened.

### HO1-021 — Italy wastes a large formation on the Vichy French border
- Date: observed during Test 1 after Vichy France exists.
- Country: ITA.
- Subsystem: `front` / diplomatic-border evaluation / theater allocation.
- Severity: `MAJOR`.
- Observed: a large Italian grouping remains deployed against the Vichy French border despite Vichy not being an active enemy/front that should consume major forces.
- Expected: Vichy France should be ignored as a military front by Axis AI while the diplomatic situation does not require combat there; Italian divisions should instead support North Africa, the Mediterranean, Balkans or other active fronts.
- Design requirement: add an explicit ignore/no-front priority for Vichy France where needed so the AI does not freeze armies on that border.
- Batch action: inspect ITA front weights and generic border-threat logic toward VIC. Add country-specific ignore/negative weighting for VIC while allied/neutral/non-hostile, and check GER/other Axis countries for the same wasted-border behavior.

### HO1-022 — Britain is far too passive in Africa despite having the strength to destroy the Italian position
- Date: observed during the North African phase of Test 1.
- Country: ENG.
- Subsystem: `front` / Africa theater / offensive posture.
- Severity: `MAJOR`.
- Observed: British forces remain overly passive in Africa even where the local balance would allow them to defeat Italian forces decisively.
- Expected: once Britain has a clear local advantage, AI ENG should actively prosecute the North African campaign: defend Egypt/Suez first, then attack into Libya and eliminate vulnerable Italian positions rather than sitting behind the line indefinitely.
- Batch action: audit ENG Egypt/Libya/East Africa front importance, plan activation/aggressiveness, local reserve requirements and whether home/France commitments are starving Africa of command priority. Add a clear offensive phase when local strength/supply conditions are favorable.

### HO1-023 — Japanese AI strategic performance is globally unacceptable in the China/Pacific war
- Date: 1941-42 Pacific phase of Test 1.
- Country: JAP.
- Subsystem: `front` / historical strategy / naval invasions / theater allocation / production.
- Severity: `MAJOR` (systemic).
- Observed: Japan is failing simultaneously across its core historical objectives: it is losing to China and has already surrendered parts of the Chinese coast; it has not conquered Malaya; Bangkok is being lost; the Philippines have barely been attacked, with only a minor island captured. This occurs after Japan has already opened the wider war against the Allies.
- Expected: AI Japan should first reach and then hold a stable position in China, while executing the Southern Operation as a concentrated staged campaign that rapidly threatens/captures the Philippines, Malaya and the Dutch East Indies before expanding farther south/east.
- Diagnostic interpretation: treat this as a systemic failure of the current JAP AI pass, not as five unrelated target-weight bugs. HO1-008, HO1-012, HO1-013, HO1-014 and HO1-016 are all likely interacting: equipment bleeding in China, no historical stalemate, fragmented invasions, insufficient patrol/dominance preparation and large idle fleet reserves.
- Batch action: rebuild the JAP 1937-42 operational lifecycle as a coherent sequence: (1) China advance with bounded losses and Wuhan objective; (2) AI-vs-AI China stabilization; (3) preserve a defined China holding force; (4) activate Southern Operation; (5) concentrate army and patrol-generated naval dominance by phase; (6) Philippines -> Malaya -> DEI -> Papua/New Guinea; (7) ensure fleet utilization and production support each phase. Re-test Japan as one integrated theater system rather than tuning isolated weights.

## Consolidation note
During the post-run batch, merge HO1-019 through HO1-023 into `ai-hands-off-test-1-issues.md` and delete this continuation file.