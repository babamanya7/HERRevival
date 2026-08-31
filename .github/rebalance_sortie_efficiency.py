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
japan = Path('common/ideas/japan.txt')
text = japan.read_text(encoding='utf-8-sig')
pat = re.compile(r'(?m)^(\s*)sortie_efficiency\s*=\s*0\.2\b')
matches = list(pat.finditer(text))
if len(matches) != 2:
    raise RuntimeError(f'Expected exactly 2 Japanese sortie_efficiency = 0.2 entries, found {len(matches)}')
text = pat.sub(lambda m: m.group(1) + 'sortie_efficiency = 0.05', text)
japan.write_text(text, encoding='utf-8')
for _ in matches:
    CHANGED.append('common/ideas/japan.txt: sortie_efficiency 0.2 -> 0.05')

# Audit: no unhandled non-define sortie-efficiency modifiers should remain outside the files above.
# This deliberately ignores common/defines because the base value is maintained separately.
unhandled = []
for p in Path('common').rglob('*'):
    if not p.is_file() or 'defines' in p.parts:
        continue
    if p.suffix.lower() not in {'.txt', '.lua'}:
        continue
    try:
        s = p.read_text(encoding='utf-8-sig')
    except UnicodeDecodeError:
        continue
    for n, line in enumerate(s.splitlines(), 1):
        if re.search(r'\b(?:sortie_efficiency|fighter_sortie_efficiency)\s*=', line):
            # Everything remaining is allowed only in the explicitly rebalanced files.
            if str(p).replace('\\', '/') not in {
                doctrine,
                traits,
                country_traits,
                'common/ideas/japan.txt',
            }:
                unhandled.append(f'{p}:{n}: {line.strip()}')

if unhandled:
    raise RuntimeError('Unhandled sortie-efficiency modifiers remain:\n' + '\n'.join(unhandled))

print('Sortie efficiency rebalance:')
for x in CHANGED:
    print(' -', x)
