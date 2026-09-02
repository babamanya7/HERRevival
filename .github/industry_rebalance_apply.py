from pathlib import Path
import math
import re

STATE_DIR = Path("history/states")

# Final agreed starting targets. Docks are intentionally left for a separate pass.
TARGETS = {
    "USA": (953, 48),
    "GER": (223, 133),
    "SOV": (198, 148),
    "ENG": (208, 68),
    "FRA": (102, 43),
    "JAP": (88, 63),
    "ITA": (68, 33),
    "CHI": (78, 24),
    "CZE": (33, 22),
    "POL": (28, 14),
    "ROM": (19, 9),
    "HUN": (18, 8),
    "YUG": (17, 6),
    "HOL": (24, 8),
    "SPR": (22, 8),
    "AUS": (23, 4),
    "FIN": (11, 7),
    "NOR": (17, 3),
    "BUL": (11, 7),
    "BEL": (27, 8),
    "AST": (22, 9),
    "CAN": (39, 9),
    "RAJ": (48, 12),
    "SWE": (22, 2),
    "DEN": (14, 3),
    "MEX": (13, 4),
    "SAF": (13, 4),
}


def matching_brace(text: str, open_pos: int) -> int:
    depth = 0
    for i in range(open_pos, len(text)):
        ch = text[i]
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return i
    raise ValueError("Unmatched brace")


def find_named_block(text: str, name: str, start: int = 0, end: int | None = None, required_depth: int | None = None):
    if end is None:
        end = len(text)
    pat = re.compile(rf"\b{re.escape(name)}\s*=\s*\{{")
    for m in pat.finditer(text, start, end):
        open_pos = text.find("{", m.start(), m.end())
        if required_depth is not None:
            # Depth relative to start of searched area.
            depth = 0
            for ch in text[start:m.start()]:
                if ch == "{":
                    depth += 1
                elif ch == "}":
                    depth -= 1
            if depth != required_depth:
                continue
        return m.start(), open_pos, matching_brace(text, open_pos)
    return None


def top_level_value(body: str, key: str):
    depth = 0
    pat = re.compile(rf"^\s*{re.escape(key)}\s*=\s*([^#\s]+)")
    for line in body.splitlines():
        if depth == 0:
            m = pat.match(line)
            if m:
                return m.group(1)
        depth += line.count("{") - line.count("}")
    return None


def top_level_has(body: str, key: str, value: str) -> bool:
    depth = 0
    pat = re.compile(rf"^\s*{re.escape(key)}\s*=\s*{re.escape(value)}(?:\s|$)")
    for line in body.splitlines():
        if depth == 0 and pat.match(line):
            return True
        depth += line.count("{") - line.count("}")
    return False


def direct_building_count(text: str, key: str) -> int:
    hist = find_named_block(text, "history")
    if not hist:
        return 0
    _, h_open, h_close = hist
    b = find_named_block(text, "buildings", h_open + 1, h_close, required_depth=0)
    if not b:
        return 0
    _, b_open, b_close = b
    body = text[b_open + 1:b_close]
    depth = 0
    pat = re.compile(rf"^\s*{re.escape(key)}\s*=\s*(\d+)\s*(?:#.*)?$")
    for line in body.splitlines():
        if depth == 0:
            m = pat.match(line)
            if m:
                return int(m.group(1))
        depth += line.count("{") - line.count("}")
    return 0


def replace_direct_building(text: str, key: str, value: int) -> str:
    hist = find_named_block(text, "history")
    if not hist:
        raise ValueError("State has no history block")
    _, h_open, h_close = hist
    b = find_named_block(text, "buildings", h_open + 1, h_close, required_depth=0)

    if not b:
        if value == 0:
            return text
        insert = f"\n\t\tbuildings = {{\n\t\t\t{key} = {value}\n\t\t}}\n"
        return text[:h_close] + insert + text[h_close:]

    _, b_open, b_close = b
    body = text[b_open + 1:b_close]
    lines = body.splitlines(keepends=True)
    depth = 0
    pat = re.compile(rf"^(\s*){re.escape(key)}\s*=\s*\d+(\s*(?:#.*)?)(\r?\n)?$")
    found = False

    for i, line in enumerate(lines):
        if depth == 0:
            m = pat.match(line)
            if m:
                found = True
                if value == 0:
                    lines[i] = ""
                else:
                    newline = m.group(3) or ""
                    lines[i] = f"{m.group(1)}{key} = {value}{m.group(2)}{newline}"
                break
        depth += line.count("{") - line.count("}")

    if not found and value > 0:
        # Match the prevailing indentation of direct building entries.
        indent = "\t\t\t"
        for line in lines:
            if re.match(r"^\s*(?:infrastructure|air_base|anti_air_building|dockyard|industrial_complex|arms_factory)\s*=", line):
                indent = re.match(r"^(\s*)", line).group(1)
                break
        suffix = "" if body.endswith(("\n", "\r")) else "\n"
        lines.append(f"{suffix}{indent}{key} = {value}\n")

    new_body = "".join(lines)
    return text[:b_open + 1] + new_body + text[b_close:]


def decode_file(path: Path):
    data = path.read_bytes()
    bom = data.startswith(b"\xef\xbb\xbf")
    return data.decode("utf-8-sig"), bom


def encode_file(path: Path, text: str, bom: bool):
    data = text.encode("utf-8")
    if bom:
        data = b"\xef\xbb\xbf" + data
    path.write_bytes(data)


def parse_state(path: Path):
    text, bom = decode_file(path)
    hist = find_named_block(text, "history")
    if not hist:
        return None
    _, h_open, h_close = hist
    h_body = text[h_open + 1:h_close]
    owner = top_level_value(h_body, "owner")
    if not owner:
        return None
    core = top_level_has(h_body, "add_core_of", owner)
    manpower_m = re.search(r"\bmanpower\s*=\s*(\d+)", text)
    manpower = int(manpower_m.group(1)) if manpower_m else 0
    return {
        "path": path,
        "text": text,
        "bom": bom,
        "owner": owner,
        "core": core,
        "manpower": manpower,
        "civ": direct_building_count(text, "industrial_complex"),
        "mil": direct_building_count(text, "arms_factory"),
    }


def allocate(states, field: str, target: int):
    current = [s[field] for s in states]
    if sum(current) == target:
        return current

    weights = current[:]
    if sum(weights) == 0:
        other = "mil" if field == "civ" else "civ"
        weights = [s[other] for s in states]
    if sum(weights) == 0:
        weights = [max(1.0, math.sqrt(max(1, s["manpower"]))) for s in states]

    total_w = float(sum(weights))
    raw = [target * w / total_w for w in weights]
    out = [int(math.floor(x)) for x in raw]
    remainder = target - sum(out)

    # Largest remainder; ties prefer already more industrial / populous states.
    order = sorted(
        range(len(states)),
        key=lambda i: (raw[i] - out[i], current[i], states[i]["manpower"]),
        reverse=True,
    )
    for i in order[:remainder]:
        out[i] += 1
    return out


states = []
for path in sorted(STATE_DIR.glob("*.txt")):
    try:
        s = parse_state(path)
    except Exception as exc:
        raise RuntimeError(f"Failed parsing {path}: {exc}") from exc
    if s:
        states.append(s)

world_before = 0
world_after = 0
changed_files = set()
report = []

for tag, (target_civ, target_mil) in TARGETS.items():
    owned = [s for s in states if s["owner"] == tag]
    if not owned:
        raise RuntimeError(f"No starting states found for {tag}")

    before_civ = sum(s["civ"] for s in owned)
    before_mil = sum(s["mil"] for s in owned)
    world_before += before_civ + before_mil
    world_after += target_civ + target_mil

    adjustable = [s for s in owned if s["core"]]
    fixed = [s for s in owned if not s["core"]]
    fixed_civ = sum(s["civ"] for s in fixed)
    fixed_mil = sum(s["mil"] for s in fixed)

    adj_target_civ = target_civ - fixed_civ
    adj_target_mil = target_mil - fixed_mil
    if adj_target_civ < 0 or adj_target_mil < 0:
        raise RuntimeError(
            f"{tag}: target below fixed non-core industry: fixed={fixed_civ}/{fixed_mil}, target={target_civ}/{target_mil}"
        )
    if not adjustable:
        raise RuntimeError(f"{tag}: no owned core states available for adjustment")

    new_civs = allocate(adjustable, "civ", adj_target_civ)
    new_mils = allocate(adjustable, "mil", adj_target_mil)

    for s, new_civ, new_mil in zip(adjustable, new_civs, new_mils):
        new_text = s["text"]
        if new_civ != s["civ"]:
            new_text = replace_direct_building(new_text, "industrial_complex", new_civ)
        if new_mil != s["mil"]:
            new_text = replace_direct_building(new_text, "arms_factory", new_mil)
        if new_text != s["text"]:
            encode_file(s["path"], new_text, s["bom"])
            changed_files.add(str(s["path"]))
            s["text"] = new_text
            s["civ"] = new_civ
            s["mil"] = new_mil

    # Verify exact owned-country total after edits, including untouched non-core states.
    after_civ = fixed_civ + sum(new_civs)
    after_mil = fixed_mil + sum(new_mils)
    if (after_civ, after_mil) != (target_civ, target_mil):
        raise RuntimeError(f"{tag}: verification failed: got {after_civ}/{after_mil}")

    report.append(
        f"{tag}: {before_civ}/{before_mil} -> {after_civ}/{after_mil} "
        f"(delta {after_civ-before_civ:+d}/{after_mil-before_mil:+d})"
    )

print("\n".join(report))
print(f"\nChanged state files: {len(changed_files)}")
print(f"Selected-country civ+mil total: {world_before} -> {world_after} ({world_after-world_before:+d}, {(world_after/world_before-1)*100:+.2f}%)")
