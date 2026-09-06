# HER AI Division Template Rework

Status: FIRST FULL MAJOR PASS COMPLETE
Branch: `AI-rework`

## Scope

This block owns `common/ai_templates` only. It defines which division templates the AI builds and upgrades toward. Equipment-designer templates for tanks, aircraft and ships remain a separate deferred task.

## Hard design rules

1. Normal combat divisions target exactly **30 combat width**.
2. HER line battalions used here are 2 combat width each, therefore a normal combat template contains exactly **15 line battalions**.
3. The universal infantry baseline is three infantry regiments plus divisional fire support:
   - 9 infantry/heavy infantry;
   - 3 artillery;
   - 1 heavy artillery;
   - 1 anti-tank + 1 anti-air, or 2 anti-tank for a deliberately anti-armor variant.
4. Historical OOB structure is the starting point, but oversized or undersized peacetime formations are normalized to the 30-width combat standard rather than preserved literally.
5. `regiments`, `regimental_support`, and `support` are distinct layers. Only line `regiments` count toward the 30-width target. Historical regimental assets must never be mistaken for divisional support or counted as line width.
6. Current HER `ai_templates` provide proven `target_template` syntax for `regiments` and `support`. No unverified `regimental_support` block is added to AI target templates until parser support is confirmed from a proven example or test.
7. Rich majors receive dense support packages when their industry can sustain them. China economises through support density/equipment quality, not by using weak under-width frontline divisions.
8. Garrisons/suppression are utility formations and are exempt from the 30-width combat rule.

## National template files

- GER: infantry, armor, motorized, Panzergrenadier, anti-armor, mountain, airborne, garrison. Standard infantry normalized to 9 HI + 3 ART + 1 HART + AT + AA. Anti-armor variant uses 2 AT. Latest normalization commit: `b0768e8c99de31d6bad382cdad3377f18b6bf0a8`.
- SOV: rifle, light/medium/heavy armor, motor rifle, mechanized assault, mountain, airborne, garrison. 30-width normalization commit: `a9b60f4645794528b6799230b61fb0e9cb959f75`.
- CHI: early 15 INF, wartime 12 HI + 3 ART, late 9 HI + 3 ART + HART + AT + AA; national garrison added so generic garrison can be blocked. Latest commit: `0cbba58bd3af413512b964614c775a1960068ae1`.
- ENG: infantry, cruiser/medium armor, motorized, mechanized assault, Royal Marines, mountain, airborne, garrison. 30-width normalization commit: `b0bdb50eaf1db3eca8d598250c53ebb0355d1caf`.
- USA: infantry, armor, motorized, mechanized assault, Marines, airborne, garrison. Oversized 1936 12 HI + 6 ART OOB was normalized to the 30-width combat standard. Commit: `f3f27762e8fa380d176e835299f8c0789627bf1f`.
- JAP: infantry, Marines/SNLF, armor, motorized, mountain, garrison. Historical square-division and regimental-support structure informed the design, but AI combat formations are normalized to 30 width. Commit: `18eaf1d999ac54d18229988e1fd14c0c1e32dcd6`.
- ITA: infantry, light/medium armor, motorized, Alpini, Marines, garrison. Built from the current HER 1936 three-regiment Italian OOB and normalized to 30 width. Commit: `34ecfc58311da0b5a0e9826756963fca21b1ec7c`.
- FRA: infantry, motorized, light/medium armor, mechanized assault, Alpine, Marines, garrison. Built from the current HER three-regiment French OOB and normalized to 30 width. Commit: `c58b399dd96a7945f3cd6f4d1f7104bf242ca7f9`.

## Generic template isolation

`common/ai_templates/generic.txt` was rebuilt as a fallback for countries without dedicated national profiles.

- GER/SOV/ENG/USA/JAP/ITA/FRA/CHI are blocked from generic combat and garrison roles.
- Generic infantry/armor/mechanized/mountain/marine/airborne formations are normalized to 30 width.
- `mountaineers_generic` now correctly uses `role = mountaineers` instead of the old `role = infantry`.
- Generic suppression remains global as a non-combat utility fallback.

Commit: `9923f623c46a3954f6e0897525ea70bd953a926f`.

## Validation backlog

1. Confirm whether `regimental_support` is accepted inside AI `target_template`; do not guess.
2. Hands-off test all eight majors for template upgrade convergence, equipment starvation, and role selection.
3. Check that special-force templates do not consume excessive cap or equipment relative to country strategy weights.
4. Verify no invalid support/sub-unit IDs survive parser logs.
5. Only after template behavior is stable should remaining AI-only helper systems and NAI defines be tuned.
