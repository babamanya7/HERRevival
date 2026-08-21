#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HERRevival: migrate 1936 piston-engine starting setup from Engine IV to Engine III
and grant the common engine tuning technologies.

Run from the repository root:
    python tools_rework_starting_air_engines.py

Optional dry-run:
    python tools_rework_starting_air_engines.py --dry-run
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent

COUNTRIES_DIR = REPO_ROOT / "history" / "countries"
UNITS_DIR = REPO_ROOT / "history" / "units"
AIR_UPGRADES = REPO_ROOT / "common" / "units" / "equipment" / "upgrades" / "air_upgrades.txt"


AIR_ENGINE_MODULE_REPLACEMENTS = {
    "engine_4_1x": "engine_3_1x",
    "engine_4_2x": "engine_3_2x",
    "engine_4_3x": "engine_3_3x",
    "engine_4_4x": "engine_3_4x",
    "radial_engine_4_1x": "radial_engine_3_1x",
    "radial_engine_4_2x": "radial_engine_3_2x",
    "radial_engine_4_3x": "radial_engine_3_3x",
    "radial_engine_4_4x": "radial_engine_3_4x",
}


def read_text(path: Path) -> tuple[str, bool]:
    raw = path.read_bytes()
    has_bom = raw.startswith(b"\xef\xbb\xbf")
    if has_bom:
        raw = raw[3:]
    return raw.decode("utf-8"), has_bom


def write_text(path: Path, text: str, has_bom: bool) -> None:
    raw = text.encode("utf-8")
    if has_bom:
        raw = b"\xef\xbb\xbf" + raw
    path.write_bytes(raw)


def find_block(text: str, start_match: re.Match[str]) -> tuple[int, int]:
    """Return [start, end) for a Paradox-script {...} block."""
    brace_pos = text.find("{", start_match.start(), start_match.end() + 2)
    if brace_pos < 0:
        raise ValueError("Opening brace not found")

    depth = 0
    in_string = False
    escaped = False

    for i in range(brace_pos, len(text)):
        ch = text[i]

        if in_string:
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == '"':
                in_string = False
            continue

        if ch == '"':
            in_string = True
        elif ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return start_match.start(), i + 1

    raise ValueError("Unclosed block")


def first_set_technology_block(text: str) -> tuple[int, int] | None:
    m = re.search(r"(?m)^[ \t]*set_technology[ \t]*=[ \t]*\{", text)
    if not m:
        return None
    return find_block(text, m)


def replace_or_add_tech(block: str, tech: str, value: str = "1") -> str:
    if re.search(rf"(?m)^[ \t]*{re.escape(tech)}[ \t]*=", block):
        return block

    # Insert before early_bombs / aircraft_construction when possible,
    # otherwise before the closing brace.
    anchor = re.search(r"(?m)^([ \t]*)(early_bombs|aircraft_construction)[ \t]*=", block)
    if anchor:
        indent = anchor.group(1)
        return block[:anchor.start()] + f"{indent}{tech} = {value}\n" + block[anchor.start():]

    close = block.rfind("}")
    if close < 0:
        return block
    return block[:close] + f"\t{tech} = {value}\n" + block[close:]


def remove_tech_line(block: str, tech: str) -> str:
    return re.sub(
        rf"(?m)^[ \t]*{re.escape(tech)}[ \t]*=[ \t]*1[ \t]*(?:#.*)?\r?\n?",
        "",
        block,
    )


def normalize_starting_engine_techs(text: str) -> tuple[str, list[str]]:
    span = first_set_technology_block(text)
    if not span:
        return text, []

    a, b = span
    block = text[a:b]
    changes: list[str] = []

    has_inline_3 = bool(re.search(r"(?m)^[ \t]*engines_3[ \t]*=[ \t]*1", block))
    has_inline_4 = bool(re.search(r"(?m)^[ \t]*engines_4[ \t]*=[ \t]*1", block))
    has_radial_3 = bool(re.search(r"(?m)^[ \t]*radial_engines_3[ \t]*=[ \t]*1", block))
    has_radial_4 = bool(re.search(r"(?m)^[ \t]*radial_engines_4[ \t]*=[ \t]*1", block))

    # If a country somehow had IV without III, retain its technological level
    # by downgrading IV to III rather than leaving a gap.
    if has_inline_4 and not has_inline_3:
        block = replace_or_add_tech(block, "engines_3")
        has_inline_3 = True
        changes.append("added engines_3 (country had engines_4 without III)")

    if has_radial_4 and not has_radial_3:
        block = replace_or_add_tech(block, "radial_engines_3")
        has_radial_3 = True
        changes.append("added radial_engines_3 (country had radial_engines_4 without III)")

    if has_inline_4:
        block = remove_tech_line(block, "engines_4")
        changes.append("removed engines_4")

    if has_radial_4:
        block = remove_tech_line(block, "radial_engines_4")
        changes.append("removed radial_engines_4")

    # Common tuning progression: countries that start with any III-generation
    # piston engine receive the two pre-1936 tuning technologies.
    if has_inline_3 or has_radial_3:
        before = block
        block = replace_or_add_tech(block, "engine_tuning_1")
        if block != before:
            changes.append("added engine_tuning_1")

        before = block
        block = replace_or_add_tech(block, "engine_tuning_2")
        if block != before:
            changes.append("added engine_tuning_2")

    return text[:a] + block + text[b:], changes


def downgrade_air_engine_modules(text: str) -> tuple[str, dict[str, int]]:
    counts: dict[str, int] = {}
    for old, new in AIR_ENGINE_MODULE_REPLACEMENTS.items():
        n = text.count(old)
        if n:
            text = text.replace(old, new)
            counts[f"{old} -> {new}"] = n
    return text, counts


def replace_named_block(text: str, block_name: str, new_inner: str) -> tuple[str, bool]:
    m = re.search(rf"(?m)^[ \t]*{re.escape(block_name)}[ \t]*=[ \t]*\{{", text)
    if not m:
        return text, False
    a, b = find_block(text, m)

    opening = text.find("{", m.start(), m.end() + 2)
    closing = b - 1
    indent_match = re.match(r"(?m)^([ \t]*)", text[m.start():])
    base_indent = indent_match.group(1) if indent_match else ""

    replacement = text[a:opening + 1] + "\n" + new_inner + base_indent + "}"
    return text[:a] + replacement + text[b:], True


ENGINE_UPGRADE_REQUIREMENTS = """\
\t\t2 = {
\t\t\thas_tech = engine_tuning_1
\t\t}
\t\t4 = {
\t\t\thas_tech = engine_tuning_2
\t\t}
\t\t6 = {
\t\t\thas_tech = engine_tuning_3
\t\t}
\t\t9 = {
\t\t\thas_tech = engine_tuning_4
\t\t}
\t\t12 = {
\t\t\thas_tech = engine_tuning_5
\t\t}
\t\t15 = {
\t\t\thas_tech = engine_tuning_6
\t\t}
\t\t18 = {
\t\t\thas_tech = engine_tuning_7
\t\t}
"""


def patch_air_bba_engine_upgrade(text: str) -> tuple[str, bool]:
    # Locate air_bba_engine_upgrade first, then its own level_requirements.
    m = re.search(r"(?m)^[ \t]*air_bba_engine_upgrade[ \t]*=[ \t]*\{", text)
    if not m:
        return text, False
    a, b = find_block(text, m)
    block = text[a:b]

    req = re.search(r"(?m)^[ \t]*level_requirements[ \t]*=[ \t]*\{", block)
    if not req:
        return text, False

    ra, rb = find_block(block, req)
    opening = block.find("{", req.start(), req.end() + 2)
    replacement = block[ra:opening + 1] + "\n" + ENGINE_UPGRADE_REQUIREMENTS + "\t}"
    new_block = block[:ra] + replacement + block[rb:]

    if new_block == block:
        return text, False
    return text[:a] + new_block + text[b:], True


def process_country(path: Path, dry_run: bool) -> tuple[bool, list[str]]:
    text, bom = read_text(path)
    original = text
    notes: list[str] = []

    text, tech_changes = normalize_starting_engine_techs(text)
    notes.extend(tech_changes)

    text, module_changes = downgrade_air_engine_modules(text)
    for desc, count in module_changes.items():
        notes.append(f"{desc}: {count}")

    changed = text != original
    if changed and not dry_run:
        write_text(path, text, bom)
    return changed, notes


def process_starting_air_oob(path: Path, dry_run: bool) -> tuple[bool, list[str]]:
    text, bom = read_text(path)
    original = text
    notes: list[str] = []

    text, module_changes = downgrade_air_engine_modules(text)
    for desc, count in module_changes.items():
        notes.append(f"{desc}: {count}")

    changed = text != original
    if changed and not dry_run:
        write_text(path, text, bom)
    return changed, notes


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if not COUNTRIES_DIR.is_dir():
        raise SystemExit(f"Not a HERRevival repo root: {COUNTRIES_DIR} not found")

    changed_files: list[tuple[Path, list[str]]] = []
    skipped_oob_hits: list[tuple[Path, dict[str, int]]] = []

    # 1) Starting technology and starting equipment variants.
    for path in sorted(COUNTRIES_DIR.glob("*.txt")):
        changed, notes = process_country(path, args.dry_run)
        if changed:
            changed_files.append((path, notes))

    # 2) Starting air OOBs. Most only reference version_name, but scan them
    # explicitly so no embedded variant with Engine IV survives.
    if UNITS_DIR.is_dir():
        for path in sorted(UNITS_DIR.glob("*.txt")):
            name = path.name.lower()
            is_starting_air_oob = (
                "_1936_air_bba" in name
                or "_1939_air_bba" in name
            )

            text, _ = read_text(path)
            hits = {
                old: text.count(old)
                for old in AIR_ENGINE_MODULE_REPLACEMENTS
                if text.count(old)
            }

            if not hits:
                continue

            if is_starting_air_oob:
                changed, notes = process_starting_air_oob(path, args.dry_run)
                if changed:
                    changed_files.append((path, notes))
            else:
                skipped_oob_hits.append((path, hits))

    # 3) Engine "+" unlocks: tuning techs, not engine generations.
    if AIR_UPGRADES.is_file():
        text, bom = read_text(AIR_UPGRADES)
        new_text, changed = patch_air_bba_engine_upgrade(text)
        if changed:
            if not args.dry_run:
                write_text(AIR_UPGRADES, new_text, bom)
            changed_files.append((
                AIR_UPGRADES,
                ["air_bba_engine_upgrade level_requirements -> engine_tuning_1..7"],
            ))

    print("\n=== HER starting piston-engine migration ===")
    print("MODE:", "DRY RUN" if args.dry_run else "WRITE")
    print("Changed files:", len(changed_files))

    for path, notes in changed_files:
        print(f"\n{path.relative_to(REPO_ROOT)}")
        for note in notes:
            print(f"  - {note}")

    if skipped_oob_hits:
        print("\nWARNING: Engine-IV module references found in non-starting history/units files.")
        print("They were intentionally NOT changed:")
        for path, hits in skipped_oob_hits:
            print(f"  {path.relative_to(REPO_ROOT)}: {hits}")

    # Post-checks in starting data.
    leftovers = []
    for path in sorted(COUNTRIES_DIR.glob("*.txt")):
        text, _ = read_text(path)
        span = first_set_technology_block(text)
        if span:
            block = text[span[0]:span[1]]
            if re.search(r"(?m)^[ \t]*(?:radial_)?engines_4[ \t]*=[ \t]*1", block):
                leftovers.append(f"{path.relative_to(REPO_ROOT)}: starting Engine IV tech remains")
        for token in AIR_ENGINE_MODULE_REPLACEMENTS:
            if token in text:
                leftovers.append(f"{path.relative_to(REPO_ROOT)}: {token} remains")

    if leftovers:
        print("\nPOST-CHECK WARNINGS:")
        for item in leftovers:
            print("  -", item)
        return 2

    print("\nPost-check: no starting Engine IV technology or Engine-IV aircraft modules remain in history/countries.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
