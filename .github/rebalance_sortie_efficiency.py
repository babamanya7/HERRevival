from pathlib import Path
import re

CHANGED = []


def replace_in_named_block(path, key, field, value):
    p = Path(path)
    text = p.read_text(encoding='utf-8-sig')
    marker = re.compile(r'(?m)^([ \t]*)' + re.escape(key) + r'\s*=\s*\{')
    pos = 0
    found = 0
    while True:
        m = marker.search(text, pos)
        if not m:
            break
        opening = text.find('{', m.start())
        depth = 0
        end = None
        for i in range(opening, len(text)):
            if text[i] == '{':
                depth += 1
            elif text[i] == '}':
                depth -= 1
                if depth == 0:
                    end = i + 1
                    break
        if end is None:
            raise RuntimeError(f'Unmatched block {key} in {path}')
        block = text[m.start():end]
        pat = re.compile(r'(?m)^(\s*)' + re.escape(field) + r'\s*=\s*([-+]?[0-9]*\.?[0-9]+)')
        mm = pat.search(block)
        if not mm:
            raise RuntimeError(f'{field} not found in {key} ({path})')
        old = mm.group(2)
        new_block = block[:mm.start()] + mm.group(1) + f'{field} = {value}' + block[mm.end():]
        text = text[:m.start()] + new_block + text[end:]
        pos = m.start() + len(new_block)
        CHANGED.append(f'{path}: {key}: {field} {old} -> {value}')
        found += 1
    if not found:
        raise RuntimeError(f'Block {key} not found in {path}')
    p.write_text(text, encoding='utf-8')


def replace_exact(path, old, new, expected=None):
    p = Path(path)
    text = p.read_text(encoding='utf-8-sig')
    count = text.count(old)
    if expected is not None and count != expected:
        raise RuntimeError(f'{path}: expected {expected} occurrences of {old!r}, found {count}')
    if count == 0:
        raise RuntimeError(f'{path}: {old!r} not found')
    p.write_text(text.replace(old, new), encoding='utf-8')
    for _ in range(count):
        CHANGED.append(f'{path}: {old.strip()} -> {new.strip()}')


# Naval doctrines. Base Strike totals +30%; the two non-carrier doctrines retain a smaller +15% total.
doctrine = 'common/technologies/naval_doctrine.txt'
for key, value in {
    'subsidiary_carrier_role': '0.05',
    'floating_airfield': '0.10',
    'subsidiary_carrier_role_ti': '0.05',
    'floating_airfield_ti': '0.10',
    'carrier_primacy': '0.08',
    'floating_airfield_bs': '0.10',
    'massed_strikes': '0.12',
}.items():
    replace_in_named_block(doctrine, key, 'sortie_efficiency', value)

# Admiral traits.
traits = 'common/unit_leader/00_traits.txt'
replace_in_named_block(traits, 'air_controller', 'sortie_efficiency', '0.05')
replace_in_named_block(traits, 'flight_deck_manager', 'sortie_efficiency', '0.05')
replace_in_named_block(traits, 'fighter_director', 'fighter_sortie_efficiency', '0.10')

# Carrier high command / advisor grades.
country_traits = 'common/country_leader/00_traits.txt'
replace_in_named_block(country_traits, 'navy_carrier_1', 'sortie_efficiency', '0.03')
replace_in_named_block(country_traits, 'navy_carrier_2', 'sortie_efficiency', '0.05')
replace_in_named_block(country_traits, 'navy_carrier_3', 'sortie_efficiency', '0.07')

# Japan has two separate +20% sortie-efficiency national bonuses. Both become +5%.
replace_exact('common/ideas/japan.txt', 'sortie_efficiency = 0.2', 'sortie_efficiency = 0.05', expected=2)

# Italy progression: halve fighter-only sortie bonuses.
replace_exact('common/ideas/italy.txt', 'fighter_sortie_efficiency = 0.05', 'fighter_sortie_efficiency = 0.025', expected=1)
replace_exact('common/ideas/italy.txt', 'fighter_sortie_efficiency = 0.1', 'fighter_sortie_efficiency = 0.05', expected=1)

# Carrier experience and full-screening bonuses are also external sortie-efficiency sources.
static_mods = 'common/modifiers/00_static_modifiers.txt'
replace_in_named_block(static_mods, 'carrier_experience_bonus_max', 'fighter_sortie_efficiency', '0.10')
replace_in_named_block(static_mods, 'carrier_experience_malus_min', 'fighter_sortie_efficiency', '-0.10')
replace_in_named_block(static_mods, 'capital_screening_bonus', 'sortie_efficiency', '0.05')

# Early carrier operations technology; keep it useful, but smaller on the new scale.
replace_in_named_block('common/technologies/MTG_naval.txt', 'arresting_gear', 'sortie_efficiency', '0.03')

# Locate every place that changes Norway's dynamic sortie-efficiency variable before committing anything.
needle = 'NOR_royal_navy_dmod_sortie_efficiency'
nor_hits = []
for p in Path('.').rglob('*'):
    if not p.is_file() or '.git' in p.parts:
        continue
    try:
        s = p.read_text(encoding='utf-8-sig')
    except (UnicodeDecodeError, OSError):
        continue
    for n, line in enumerate(s.splitlines(), 1):
        if needle in line:
            nor_hits.append(f'{p}:{n}: {line.strip()}')
print('NORWAY VARIABLE HITS:')
print('\n'.join(nor_hits))
raise RuntimeError('Audit stop: inspect Norway sortie-efficiency variable sources above')
