# HER Mod — Air Survivability / Construction Audit

Status: IN PROGRESS

Companion notes for `docs/systems/research-audit-air.md` while Air Designer 2.0 is being specified.

## Accepted design rule: no mandatory designer modules
If a module is almost always selected once its technology is available, it is not functioning as a meaningful designer choice. Treat such modules as a design smell.

Air Designer 2.0 rule:
- either integrate an effectively universal improvement into the baseline evolution of the relevant airframe/engine/fuel/cockpit subsystem;
- or redesign the module so that it creates a genuine physical tradeoff in weight, volume, drag, fuel, reliability, IC, strategic resources, maintenance or role compatibility.

Do not solve mandatory modules only by flat numerical nerfs if the underlying problem is structural.

Current priority candidates for this treatment:
- self-sealing fuel tanks;
- automatic extinguisher systems;
- pressurized cockpit;
- some engine-performance enhancement combinations;
- generic lightweight/reinforced construction sliders.

## Current findings

### Self-sealing fuel tanks
Current small self-sealing tanks preserve the same +400 range as the ordinary small fuel tank, while adding +20% air defence at +5% weight and 10 rubber. The NGS variant raises this to +30% defence at +7% weight, still preserving full range. Medium/large versions follow the same pattern with larger rubber costs.

**B / likely no-brainer risk:** for countries with adequate rubber, self-sealing tanks are very close to a strict upgrade over ordinary tanks because they retain the same range and add a large defence multiplier. The ordinary tank's main advantage is simply avoiding rubber cost. Test whether this produces near-universal selection among majors.

Air Designer 2.0 direction: fuel-system choices should be more physical and role-dependent: tank capacity/placement, self-sealing protection, drop tanks and internal armour should compete for weight/volume/drag/resources rather than one module mostly superseding another.

### Armour plates and extinguishers
Small armour plate: +4 air defence, +2 IC, +2 weight, -2% speed, -6% range, 4 steel.
Small automatic extinguisher: +2 air defence, +1 IC, +0.5 weight, +5% reliability, only -0.5% speed/-1.5% range.

The extinguisher has a very efficient defensive/reliability package and may be another high-value default once available. Armour plate is a clearer protection-vs-performance tradeoff.

### Lightweight / reinforced construction
Current construction modules are near-perfect mirrors:
- lightweight: -15% weight, -40% defence, -10% IC;
- reinforced: +15% weight, +40% defence, +10% IC.

**A/B design concern:** this behaves more like a generic quality slider than aircraft engineering. Air Designer 2.0 should decompose construction into physical choices (materials, structural reinforcement, armour/protection, stressed-skin/airframe construction, possibly wooden/metal/mixed construction where historically relevant) so effects emerge from actual layout/material decisions.

### Drop tanks
Small drop tanks add +75 range, +1 IC, +1 weight, +0.02 fuel consumption, -1 defence and -1% speed. Medium version doubles the scale.

This is a healthy explicit range-vs-drag/survivability/fuel tradeoff and should be retained, but moved into a dedicated external fuel / wing stores section rather than a generic special slot.

### Pressurized cockpit
Current pressurized cockpit gives +5% reliability, +15% range and +9 agility on air-superiority/interception missions for 3 IC (small) / 5 IC (medium), with no weight cost shown in the module itself.

**B / suspicious value:** this is a very broad high-altitude-performance abstraction and may become a strong default fighter module. In Air Designer 2.0, pressurization should interact with cockpit/crew, altitude role, engine supercharging/turbocharging and mass/complexity rather than being an isolated universal special-module buff.

### Fuel / engine enhancement modules
Examples:
- high-octane fuel: +3% speed, +6% thrust, +30% fuel consumption, +4% IC multiplier;
- fuel injection: +6% speed, -20% fuel consumption, +5% reliability for +6 IC;
- water injection: +3% speed, +10% fuel use, -10% reliability for +3 IC;
- turbo/superchargers improve speed/thrust while increasing fuel use and IC.

These are conceptually strong because they alter propulsion performance rather than directly buffing mission attack. However, some combinations may stack into mandatory performance packages. They should become part of an explicit propulsion/induction subsystem in Air Designer 2.0, with compatibility determined by engine family/layout.

### Gunsights and radar
Reflex/gyro sights and air-air radar already apply mission-specific bonuses rather than generic all-stat improvements. This is good architecture. Preserve but place them in dedicated sight/avionics slots. Air-ground radar similarly provides mission-specific CAS/naval/bombing and night benefits with weight/drag/IC costs.

### Emerging meta risk
The current designer has several modules that are individually sensible but may stack into a near-mandatory fighter package: self-sealing tanks, extinguisher, pressurized cockpit, engine-performance enhancement, gunsight/radar, and reinforced/lightweight construction depending meta. The next audit step should compare representative 1939/1941/1943 fighter and CAS builds to identify actual no-brainer combinations and total research burden.
