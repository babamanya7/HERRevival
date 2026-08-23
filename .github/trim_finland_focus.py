from pathlib import Path
import re
from collections import defaultdict

path = Path("common/national_focus/finland.txt")
raw = path.read_bytes()
had_bom = raw.startswith(b"\xef\xbb\xbf")
text = raw.decode("utf-8-sig")

FASCIST_BASE = {
    "FIN_a_fascist_regime",
    "FIN_academic_karelian_society",
    "FIN_advanced_jaeger_training_program",
    "FIN_bring_foreign_armor_experts",
    "FIN_discredit_the_democratic_system",
    "FIN_finnish_irredentism",
    "FIN_finnish_legion_of_honor",
    "FIN_finnish_supremacy_in_the_north",
    "FIN_indoctrinate_the_workers",
    "FIN_industrial_cooperation",
    "FIN_intellectual_elite",
    "FIN_join_axis",
    "FIN_keepers_of_the_north",
    "FIN_maan_turva",
    "FIN_military_promotions",
    "FIN_military_research",
    "FIN_mustapaidat",
    "FIN_national_fanatism",
    "FIN_patriotic_peoples_movement",
    "FIN_prepare_a_military_coup",
    "FIN_right_wing_policies",
    "FIN_seek_german_protection",
    "FIN_sotilaalliset_kappalaiset",
    "FIN_tactical_wargaming_department",
    "FIN_take_over_the_suojeluskunta",
}

COMMUNIST_BASE = {
    "FIN_cooperate_with_social_democrats",
    "FIN_the_peoples_democratic_league",
    "FIN_the_red_watch",
    "FIN_the_second_finnish_civil_war",
    "FIN_the_workers_state",
    "FIN_towards_a_red_government",
}


def mask_code(s):
    out = list(s)
    in_string = False
    escaped = False
    comment = False
    for i, ch in enumerate(s):
        if comment:
            if ch == "\n":
                comment = False
            else:
                out[i] = " "
            continue
        if in_string:
            out[i] = " "
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == '"':
                in_string = False
            continue
        if ch == "#":
            comment = True
            out[i] = " "
        elif ch == '"':
            in_string = True
            out[i] = " "
    return "".join(out)


def match_brace(src_mask, opening):
    depth = 0
    for i in range(opening, len(src_mask)):
        if src_mask[i] == "{":
            depth += 1
        elif src_mask[i] == "}":
            depth -= 1
            if depth == 0:
                return i
    raise RuntimeError(f"unmatched brace at {opening}")


def parse_focus_blocks(src):
    sm = mask_code(src)
    ft_match = re.search(r"(?m)^\s*focus_tree\s*=\s*\{", sm)
    if not ft_match:
        raise RuntimeError("focus_tree not found")
    ft_open = sm.find("{", ft_match.start())
    ft_end = match_brace(sm, ft_open)
    result = {}
    depth = 1
    pos = ft_open + 1
    while pos < ft_end:
        if sm[pos] == "{":
            depth += 1
            pos += 1
            continue
        if sm[pos] == "}":
            depth -= 1
            pos += 1
            continue
        if depth == 1:
            m = re.match(r"[ \t\r\n]*focus\s*=\s*\{", sm[pos:])
            if m:
                opening = pos + m.group(0).rfind("{")
                end = match_brace(sm, opening)
                block = src[pos:end + 1]
                mid = re.search(r"(?m)^\s*id\s*=\s*([A-Za-z0-9_.:-]+)", block)
                if mid:
                    result[mid.group(1)] = (pos, end + 1, block)
                pos = end + 1
                continue
        pos += 1
    return result


def named_block_bodies(src, keyword):
    sm = mask_code(src)
    result = []
    for m in re.finditer(r"(?m)^\s*" + re.escape(keyword) + r"\s*=\s*\{", sm):
        opening = sm.find("{", m.start())
        end = match_brace(sm, opening)
        result.append(src[opening + 1:end])
    return result


blocks = parse_focus_blocks(text)
all_ids = set(blocks)
missing = sorted((FASCIST_BASE | COMMUNIST_BASE) - all_ids)
if missing:
    raise RuntimeError("Expected focus IDs missing before trim: " + ", ".join(missing))

prerequisite_groups = defaultdict(list)
for fid, (_, _, block) in blocks.items():
    for body in named_block_bodies(block, "prerequisite"):
        group = set(re.findall(r"\bfocus\s*=\s*([A-Za-z0-9_.:-]+)", mask_code(body)))
        if group:
            prerequisite_groups[fid].append(group)

remove = set(FASCIST_BASE | COMMUNIST_BASE)
propagated = set()
changed = True
while changed:
    changed = False
    for fid in sorted(all_ids - remove):
        groups = prerequisite_groups.get(fid, [])
        if any(group <= remove for group in groups):
            remove.add(fid)
            propagated.add(fid)
            changed = True

for start, end, fid in sorted(
    [(blocks[fid][0], blocks[fid][1], fid) for fid in remove], reverse=True
):
    text = text[:start] + text[end:]

text, nordic_count = re.subn(
    r"(?m)^[ \t]*shared_focus\s*=\s*NORDIC_[A-Za-z0-9_.:-]+[ \t]*\r?\n",
    "",
    text,
)

removed_alt_pattern = "|".join(sorted(map(re.escape, remove), key=len, reverse=True))

text = re.sub(rf"\bfocus\s*=\s*(?:{removed_alt_pattern})\b", "", text)
text = re.sub(
    rf"NOT\s*=\s*\{{\s*has_completed_focus\s*=\s*(?:{removed_alt_pattern})\s*\}}",
    "always = yes",
    text,
)
text = re.sub(
    rf"has_completed_focus\s*=\s*(?:{removed_alt_pattern})\b",
    "always = no",
    text,
)
text = re.sub(
    r"(?m)^[ \t]*(?:prerequisite|mutually_exclusive)\s*=\s*\{[ \t\r\n]*\}[ \t]*\r?\n",
    "",
    text,
)

reanchors = []
surviving_blocks = parse_focus_blocks(text)
for fid, (start, end, block) in sorted(
    surviving_blocks.items(), key=lambda kv: kv[1][0], reverse=True
):
    mrel = re.search(r"(?m)^(\s*relative_position_id\s*=\s*)([A-Za-z0-9_.:-]+)(\s*)$", block)
    if not mrel or mrel.group(2) not in remove:
        continue
    retained_parents = []
    for body in named_block_bodies(block, "prerequisite"):
        retained_parents += [
            x
            for x in re.findall(r"\bfocus\s*=\s*([A-Za-z0-9_.:-]+)", mask_code(body))
            if x not in remove
        ]
    old = mrel.group(2)
    if retained_parents:
        new = retained_parents[0]
        new_block = block[:mrel.start()] + mrel.group(1) + new + mrel.group(3) + block[mrel.end():]
        reanchors.append(f"{fid}: {old} -> {new}")
    else:
        line_start = block.rfind("\n", 0, mrel.start()) + 1
        line_end = block.find("\n", mrel.end())
        line_end = mrel.end() if line_end == -1 else line_end + 1
        new_block = block[:line_start] + block[line_end:]
        reanchors.append(f"{fid}: removed relative_position_id {old}")
    text = text[:start] + new_block + text[end:]

final_mask = mask_code(text)
depth = 0
min_depth = 0
for ch in final_mask:
    if ch == "{":
        depth += 1
    elif ch == "}":
        depth -= 1
    min_depth = min(min_depth, depth)
if depth != 0 or min_depth < 0:
    raise RuntimeError(f"Brace validation failed: depth={depth}, min_depth={min_depth}")

leftovers = []
exact_removed = re.compile(rf"\b(?:{removed_alt_pattern})\b")
source_lines = text.splitlines()
for lineno, line in enumerate(final_mask.splitlines(), 1):
    if exact_removed.search(line):
        leftovers.append(f"{lineno}: {source_lines[lineno - 1].strip()}")
if leftovers:
    raise RuntimeError("Active references to removed focuses remain:\n" + "\n".join(leftovers[:50]))

final_blocks = parse_focus_blocks(text)
if remove & set(final_blocks):
    raise RuntimeError("Removed focus blocks still present")
if re.search(r"(?m)^\s*shared_focus\s*=\s*NORDIC_", final_mask):
    raise RuntimeError("NORDIC shared focus attachment still present")
for must_remain in ("FIN_suomalainen_sosialismi", "FIN_greater_finland"):
    if must_remain not in final_blocks:
        raise RuntimeError(f"Expected surviving focus was removed: {must_remain}")

path.write_bytes(text.encode("utf-8-sig" if had_bom else "utf-8"))

print(f"Fascist audited base removed: {len(FASCIST_BASE)}")
print(f"Communist audited base removed: {len(COMMUNIST_BASE)}")
print(f"Orphaned/dependent focuses additionally removed: {len(propagated)}")
print(f"Total focus blocks removed: {len(remove)}")
print(f"NORDIC shared_focus attachments removed: {nordic_count}")
if propagated:
    print("Additional removed:", ", ".join(sorted(propagated)))
if reanchors:
    print("Reanchors:", "; ".join(reanchors))
