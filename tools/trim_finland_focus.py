from pathlib import Path
import re
import sys
import traceback
from collections import defaultdict

PATH = Path('common/national_focus/finland.txt')
REPORT = Path('.github/finland_focus_apply_report.txt')

FASCIST_BASE = {
    'FIN_a_fascist_regime', 'FIN_academic_karelian_society',
    'FIN_advanced_jaeger_training_program', 'FIN_bring_foreign_armor_experts',
    'FIN_discredit_the_democratic_system', 'FIN_finnish_irredentism',
    'FIN_finnish_legion_of_honor', 'FIN_finnish_supremacy_in_the_north',
    'FIN_indoctrinate_the_workers', 'FIN_industrial_cooperation',
    'FIN_intellectual_elite', 'FIN_join_axis', 'FIN_keepers_of_the_north',
    'FIN_maan_turva', 'FIN_military_promotions', 'FIN_military_research',
    'FIN_mustapaidat', 'FIN_national_fanatism',
    'FIN_patriotic_peoples_movement', 'FIN_prepare_a_military_coup',
    'FIN_right_wing_policies', 'FIN_seek_german_protection',
    'FIN_sotilaalliset_kappalaiset', 'FIN_tactical_wargaming_department',
    'FIN_take_over_the_suojeluskunta',
}

COMMUNIST_BASE = {
    'FIN_cooperate_with_social_democrats', 'FIN_the_peoples_democratic_league',
    'FIN_the_red_watch', 'FIN_the_second_finnish_civil_war',
    'FIN_the_workers_state', 'FIN_towards_a_red_government',
}


def mask_code(s):
    out = list(s)
    in_string = False
    escaped = False
    comment = False
    for i, ch in enumerate(s):
        if comment:
            if ch == '\n':
                comment = False
            else:
                out[i] = ' '
            continue
        if in_string:
            out[i] = ' '
            if escaped:
                escaped = False
            elif ch == '\\':
                escaped = True
            elif ch == '"':
                in_string = False
            continue
        if ch == '#':
            comment = True
            out[i] = ' '
        elif ch == '"':
            in_string = True
            out[i] = ' '
    return ''.join(out)


def match_brace(src_mask, opening):
    depth = 0
    for i in range(opening, len(src_mask)):
        if src_mask[i] == '{':
            depth += 1
        elif src_mask[i] == '}':
            depth -= 1
            if depth == 0:
                return i
    raise RuntimeError(f'unmatched brace at {opening}')


def parse_focus_blocks(src):
    sm = mask_code(src)
    ft_match = re.search(r'(?m)^\s*focus_tree\s*=\s*\{', sm)
    if not ft_match:
        raise RuntimeError('focus_tree not found')
    ft_open = sm.find('{', ft_match.start())
    ft_end = match_brace(sm, ft_open)
    result = {}
    depth = 1
    pos = ft_open + 1
    while pos < ft_end:
        if sm[pos] == '{':
            depth += 1
            pos += 1
            continue
        if sm[pos] == '}':
            depth -= 1
            pos += 1
            continue
        if depth == 1:
            m = re.match(r'[ \t\r\n]*focus\s*=\s*\{', sm[pos:])
            if m:
                opening = pos + m.group(0).rfind('{')
                end = match_brace(sm, opening)
                block = src[pos:end + 1]
                mid = re.search(r'(?m)^\s*id\s*=\s*([A-Za-z0-9_.:-]+)', block)
                if mid:
                    result[mid.group(1)] = (pos, end + 1, block)
                pos = end + 1
                continue
        pos += 1
    return result


def named_block_bodies(src, keyword):
    sm = mask_code(src)
    result = []
    for m in re.finditer(r'(?m)^\s*' + re.escape(keyword) + r'\s*=\s*\{', sm):
        opening = sm.find('{', m.start())
        end = match_brace(sm, opening)
        result.append(src[opening + 1:end])
    return result


def main():
    raw = PATH.read_bytes()
    had_bom = raw.startswith(b'\xef\xbb\xbf')
    text = raw.decode('utf-8-sig')

    blocks = parse_focus_blocks(text)
    all_ids = set(blocks)
    missing = sorted((FASCIST_BASE | COMMUNIST_BASE) - all_ids)
    if missing:
        raise RuntimeError('Expected focus IDs missing before trim: ' + ', '.join(missing))

    groups = defaultdict(list)
    for fid, (_, _, block) in blocks.items():
        for body in named_block_bodies(block, 'prerequisite'):
            group = set(re.findall(r'\bfocus\s*=\s*([A-Za-z0-9_.:-]+)', mask_code(body)))
            if group:
                groups[fid].append(group)

    remove = set(FASCIST_BASE | COMMUNIST_BASE)
    propagated = set()
    changed = True
    while changed:
        changed = False
        for fid in sorted(all_ids - remove):
            # Multiple prerequisite blocks are AND. Entries inside one block are alternatives.
            if any(group <= remove for group in groups.get(fid, [])):
                remove.add(fid)
                propagated.add(fid)
                changed = True

    for start, end, fid in sorted(
        [(blocks[fid][0], blocks[fid][1], fid) for fid in remove],
        reverse=True,
    ):
        text = text[:start] + text[end:]

    text, nordic_count = re.subn(
        r'(?m)^[ \t]*shared_focus\s*=\s*NORDIC_[A-Za-z0-9_.:-]+[ \t]*\r?\n',
        '', text,
    )

    removed_pattern = '|'.join(sorted(map(re.escape, remove), key=len, reverse=True))

    # Delete removed alternatives from prerequisite and mutex declarations.
    text = re.sub(rf'\bfocus\s*=\s*(?:{removed_pattern})\b', '', text)

    # Deleted focus checks used only for branch/layout logic become constants.
    text = re.sub(
        rf'NOT\s*=\s*\{{\s*has_completed_focus\s*=\s*(?:{removed_pattern})\s*\}}',
        'always = yes', text,
    )
    text = re.sub(
        rf'has_completed_focus\s*=\s*(?:{removed_pattern})\b',
        'always = no', text,
    )

    # Empty groups are unnecessary and can confuse later maintenance.
    text = re.sub(
        r'(?m)^[ \t]*(?:prerequisite|mutually_exclusive)\s*=\s*\{[ \t\r\n]*\}[ \t]*\r?\n',
        '', text,
    )

    # Re-anchor layout entries that pointed to deleted focuses.
    reanchors = []
    surviving = parse_focus_blocks(text)
    for fid, (start, end, block) in sorted(surviving.items(), key=lambda kv: kv[1][0], reverse=True):
        mrel = re.search(r'(?m)^(\s*relative_position_id\s*=\s*)([A-Za-z0-9_.:-]+)(\s*)$', block)
        if not mrel or mrel.group(2) not in remove:
            continue
        retained = []
        for body in named_block_bodies(block, 'prerequisite'):
            retained.extend(
                x for x in re.findall(r'\bfocus\s*=\s*([A-Za-z0-9_.:-]+)', mask_code(body))
                if x not in remove
            )
        old = mrel.group(2)
        if retained:
            new = retained[0]
            new_block = block[:mrel.start()] + mrel.group(1) + new + mrel.group(3) + block[mrel.end():]
            reanchors.append(f'{fid}: {old} -> {new}')
        else:
            line_start = block.rfind('\n', 0, mrel.start()) + 1
            line_end = block.find('\n', mrel.end())
            line_end = mrel.end() if line_end == -1 else line_end + 1
            new_block = block[:line_start] + block[line_end:]
            reanchors.append(f'{fid}: removed relative_position_id {old}')
        text = text[:start] + new_block + text[end:]

    # Syntax sanity: comments/strings ignored, all structural braces must balance.
    fm = mask_code(text)
    depth = 0
    minimum = 0
    for ch in fm:
        if ch == '{':
            depth += 1
        elif ch == '}':
            depth -= 1
        minimum = min(minimum, depth)
    if depth != 0 or minimum < 0:
        raise RuntimeError(f'Brace validation failed: depth={depth}, min_depth={minimum}')

    # No exact active reference to a deleted focus ID may survive.
    exact = re.compile(rf'\b(?:{removed_pattern})\b')
    original_lines = text.splitlines()
    leftovers = []
    for lineno, line in enumerate(fm.splitlines(), 1):
        if exact.search(line):
            leftovers.append(f'{lineno}: {original_lines[lineno - 1].strip()}')
    if leftovers:
        raise RuntimeError('Active references remain:\n' + '\n'.join(leftovers[:80]))

    final_ids = set(parse_focus_blocks(text))
    present = sorted(remove & final_ids)
    if present:
        raise RuntimeError('Focus blocks still present: ' + ', '.join(present))
    if re.search(r'(?m)^\s*shared_focus\s*=\s*NORDIC_', fm):
        raise RuntimeError('NORDIC shared focus attachment still present')

    PATH.write_bytes(text.encode('utf-8-sig' if had_bom else 'utf-8'))

    report = [
        'SUCCESS',
        f'Fascist audited base removed: {len(FASCIST_BASE)}',
        f'Communist audited base removed: {len(COMMUNIST_BASE)}',
        f'Orphaned/dependent focuses additionally removed: {len(propagated)}',
        f'Total focus blocks removed: {len(remove)}',
        f'NORDIC shared_focus attachments removed: {nordic_count}',
        '',
        'ADDITIONAL ORPHANED/DEPENDENT FOCUSES:',
    ]
    report += [f'  {x}' for x in sorted(propagated)] or ['  (none)']
    report += ['', 'LAYOUT REANCHORS:']
    report += [f'  {x}' for x in reanchors] or ['  (none)']
    REPORT.write_text('\n'.join(report) + '\n', encoding='utf-8')


if __name__ == '__main__':
    try:
        main()
    except Exception:
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text('FAILED\n\n' + traceback.format_exc(), encoding='utf-8')
        sys.exit(1)
