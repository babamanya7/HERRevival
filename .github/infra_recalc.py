import csv
import math
import re
from collections import defaultdict
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path('.')
STATE_DIR = ROOT / 'history' / 'states'
PROVINCES_BMP = ROOT / 'map' / 'provinces.bmp'
DEFINITION = ROOT / 'map' / 'definition.csv'
RAILWAYS = ROOT / 'map' / 'railways.txt'
SUPPLY_NODES = ROOT / 'map' / 'supply_nodes.txt'
REPORT = ROOT / 'soviet-infra-report.csv'

MIN_LON, MAX_LON = 18.0, 62.5
MIN_LAT, MAX_LAT = 38.0, 72.5
APPLY_CHANGES = False

COMPONENT_WEIGHTS = {'C': 0.40, 'P': 0.25, 'R': 0.15, 'T': 0.20}
MIN_EFFECTIVE_AREA = 300.0

TERRAIN_SUITABILITY = {
    'urban': 1.00,
    'plains': 0.95,
    'desert': 0.82,
    'hills': 0.72,
    'forest': 0.62,
    'jungle': 0.52,
    'marsh': 0.35,
    'mountain': 0.30,
    'ocean': 0.00,
    'unknown': 0.55,
}

CONTROL = {
    3151: (30.3351, 59.9343), 6380: (37.6173, 55.7558),
    3529: (44.5133, 48.7080), 525: (30.5234, 50.4501),
    11370: (27.5615, 53.9045), 7661: (49.8671, 40.4093),
    1599: (44.7930, 41.7151), 3134: (33.0827, 68.9707),
    3338: (40.5433, 64.5393), 6338: (49.1221, 55.7961),
    3578: (46.0343, 51.5336), 11375: (44.0060, 56.3269),
    9417: (39.7015, 47.2357), 3686: (33.5254, 44.6167),
    306: (32.0453, 54.7826), 9098: (28.3318, 57.8136),
    6474: (37.8028, 48.0159), 418: (36.2304, 49.9935),
}


def parse_definition(path):
    rgb_by_pid = {}
    terrain_by_pid = {}
    max_pid = 0
    with path.open('r', encoding='latin-1', errors='ignore', newline='') as f:
        for row in csv.reader(f, delimiter=';'):
            if len(row) < 7:
                continue
            try:
                pid, r, g, b = map(int, row[:4])
            except ValueError:
                continue
            rgb_by_pid[pid] = (r, g, b)
            terrain_by_pid[pid] = row[6].strip().lower()
            max_pid = max(max_pid, pid)
    return rgb_by_pid, terrain_by_pid, max_pid


def parse_states():
    states = {}
    vp_re = re.compile(r'\bvictory_points\s*=\s*\{\s*(\d+)\s+(\d+)', re.I)
    for path in STATE_DIR.glob('*.txt'):
        raw = path.read_bytes()
        text = raw.decode('utf-8-sig', errors='ignore')
        mid = re.search(r'(?m)^\s*id\s*=\s*(\d+)\s*$', text)
        mprov = re.search(r'\bprovinces\s*=\s*\{([^}]*)\}', text, re.S)
        mowner = re.search(r'\bowner\s*=\s*([A-Z0-9_]+)', text)
        minfra = re.search(r'\binfrastructure\s*=\s*(\d+)', text)
        manpower = re.search(r'(?m)^\s*manpower\s*=\s*(\d+)', text)
        if not (mid and mprov):
            continue
        sid = int(mid.group(1))
        states[sid] = {
            'id': sid,
            'path': path,
            'text': text,
            'bom': raw.startswith(b'\xef\xbb\xbf'),
            'pids': [int(x) for x in re.findall(r'\d+', mprov.group(1))],
            'owner': mowner.group(1) if mowner else '',
            'old_infra': int(minfra.group(1)) if minfra else None,
            'manpower': int(manpower.group(1)) if manpower else 0,
            'vps': [(int(pid), int(value)) for pid, value in vp_re.findall(text)],
            'name': path.stem,
        }
    return states


def build_province_raster(rgb_by_pid):
    img = np.asarray(Image.open(PROVINCES_BMP).convert('RGB'), dtype=np.uint8)
    code = ((img[:, :, 0].astype(np.uint32) << 16) |
            (img[:, :, 1].astype(np.uint32) << 8) |
            img[:, :, 2].astype(np.uint32))
    lut = np.zeros(1 << 24, dtype=np.int32)
    for pid, (r, g, b) in rgb_by_pid.items():
        lut[(r << 16) | (g << 8) | b] = pid
    return lut[code]


def projection_from_controls(prov):
    xs, zs, lons, lats = [], [], [], []
    h = prov.shape[0]
    for pid, (lon, lat) in CONTROL.items():
        ys, xx = np.where(prov == pid)
        if len(xx) < 3:
            continue
        xs.append(float(xx.mean()))
        zs.append(float((h - 1) - ys.mean()))
        lons.append(lon)
        lats.append(lat)
    if len(xs) < 10:
        raise RuntimeError(f'Only {len(xs)} projection controls found')
    lon_coef = np.polyfit(xs, lons, 1)
    lat_coef = np.polyfit(zs, lats, 3)
    lon_rmse = float(np.sqrt(np.mean((np.polyval(lon_coef, xs) - np.asarray(lons)) ** 2)))
    lat_rmse = float(np.sqrt(np.mean((np.polyval(lat_coef, zs) - np.asarray(lats)) ** 2)))
    print(f'Projection controls={len(xs)} lon_rmse={lon_rmse:.3f} lat_rmse={lat_rmse:.3f}', flush=True)
    return lon_coef, lat_coef


def xy_to_lonlat(x, y, height, lon_coef, lat_coef):
    z = (height - 1) - y
    return float(np.polyval(lon_coef, x)), float(np.polyval(lat_coef, z))


def parse_rail_connectivity():
    degree = defaultdict(int)
    presence = set()
    if not RAILWAYS.exists():
        return degree, presence
    for line in RAILWAYS.read_text(encoding='utf-8-sig', errors='ignore').splitlines():
        nums = [int(x) for x in re.findall(r'\d+', line)]
        if len(nums) < 4:
            continue
        count = nums[1]
        route = nums[2:2 + count]
        for pid in route:
            presence.add(pid)
        for a, b in zip(route, route[1:]):
            if a != b:
                degree[a] += 1
                degree[b] += 1
    return degree, presence


def parse_supply_nodes():
    nodes = set()
    if not SUPPLY_NODES.exists():
        return nodes
    for line in SUPPLY_NODES.read_text(encoding='utf-8-sig', errors='ignore').splitlines():
        nums = [int(x) for x in re.findall(r'\d+', line)]
        if len(nums) >= 2:
            nodes.add(nums[1])
    return nodes


def winsor_norm(values, lo=5.0, hi=95.0):
    arr = np.asarray(values, dtype=float)
    qlo = float(np.percentile(arr, lo))
    qhi = float(np.percentile(arr, hi))
    if qhi <= qlo + 1e-12:
        return [0.5 for _ in values], qlo, qhi
    out = [max(0.0, min(1.0, (float(v) - qlo) / (qhi - qlo))) for v in values]
    return out, qlo, qhi


def rank_percentiles(rows):
    order = sorted(range(len(rows)), key=lambda i: (rows[i]['score'], rows[i]['state_id']))
    n = len(order)
    pct = [0.0] * n
    for rank, idx in enumerate(order):
        pct[idx] = 100.0 * (rank + 0.5) / n
    return pct


def infra_from_percentile(p):
    if p <= 5: return 1
    if p <= 15: return 2
    if p <= 30: return 3
    if p <= 50: return 4
    if p <= 68: return 5
    if p <= 82: return 6
    if p <= 92: return 7
    if p <= 98: return 8
    return 9


def main():
    rgb_by_pid, terrain_by_pid, max_pid = parse_definition(DEFINITION)
    states = parse_states()
    prov = build_province_raster(rgb_by_pid)
    lon_coef, lat_coef = projection_from_controls(prov)
    rail_degree, rail_presence = parse_rail_connectivity()
    supply_nodes = parse_supply_nodes()

    sid_lookup = np.zeros(max(max_pid, int(prov.max())) + 1, dtype=np.int32)
    for sid, st in states.items():
        for pid in st['pids']:
            if 0 <= pid < len(sid_lookup):
                sid_lookup[pid] = sid
    state_raster = sid_lookup[prov]

    terrain_lut = np.full(len(sid_lookup), TERRAIN_SUITABILITY['unknown'], dtype=np.float32)
    for pid, terrain in terrain_by_pid.items():
        if 0 <= pid < len(terrain_lut):
            terrain_lut[pid] = TERRAIN_SUITABILITY.get(terrain, TERRAIN_SUITABILITY['unknown'])
    terrain_raster = terrain_lut[prov]

    targets = []
    for sid, st in states.items():
        if st['owner'] != 'SOV' or st['old_infra'] is None:
            continue
        ys, xs = np.where(state_raster == sid)
        if not len(xs):
            continue
        lon, lat = xy_to_lonlat(float(xs.mean()), float(ys.mean()), prov.shape[0], lon_coef, lat_coef)
        if not (MIN_LON <= lon <= MAX_LON and MIN_LAT <= lat <= MAX_LAT):
            continue

        pids = st['pids']
        nprov = max(1, len(pids))
        pixel_area = int(len(xs))
        area_proxy = max(1.0, pixel_area * max(0.20, math.cos(math.radians(lat))))
        effective_area = max(MIN_EFFECTIVE_AREA, area_proxy)
        area_100k = effective_area / 100000.0

        vp_values = [value for _, value in st['vps']]
        vp_weight = sum(math.sqrt(max(0, value)) for value in vp_values)
        max_vp = max(vp_values, default=0)
        urban_count = sum(terrain_by_pid.get(pid) == 'urban' for pid in pids)

        city_density_raw = (vp_weight + 1.25 * urban_count) / area_100k
        city_node_raw = math.log1p(max_vp) + 0.35 * math.log1p(len(vp_values)) + 0.45 * math.log1p(urban_count)

        pop_density_raw = math.log1p(max(0.0, st['manpower'] / effective_area))
        pop_mass_raw = math.log1p(max(0, st['manpower']))

        rail_degree_sum = sum(rail_degree.get(pid, 0) for pid in pids)
        rail_prov_count = sum(pid in rail_presence for pid in pids)
        hub_count = sum(pid in supply_nodes for pid in pids)
        rail_density_raw = (rail_degree_sum + 0.75 * rail_prov_count + 2.5 * hub_count) / area_100k
        rail_node_raw = math.log1p(rail_degree_sum + 2.0 * rail_prov_count + 6.0 * hub_count)

        t_raw = float(np.mean(terrain_raster[ys, xs])) if len(xs) else TERRAIN_SUITABILITY['unknown']

        targets.append({
            'state_id': sid, 'name': st['name'], 'lon': lon, 'lat': lat,
            'provinces': nprov, 'pixels': pixel_area, 'area_proxy': area_proxy,
            'effective_area': effective_area,
            'manpower': st['manpower'], 'vp_count': len(st['vps']), 'max_vp': max_vp,
            'vp_weight': vp_weight, 'urban_count': urban_count,
            'rail_degree': rail_degree_sum, 'rail_provinces': rail_prov_count, 'hubs': hub_count,
            'C_density_raw': city_density_raw, 'C_node_raw': city_node_raw,
            'P_density_raw': pop_density_raw, 'P_mass_raw': pop_mass_raw,
            'R_density_raw': rail_density_raw, 'R_node_raw': rail_node_raw,
            'T_raw': t_raw, 'old_infra': st['old_infra'],
        })

    targets.sort(key=lambda x: x['state_id'])
    print(f'Target Soviet states west of Urals: {len(targets)}', flush=True)
    if len(targets) < 25:
        raise RuntimeError('Unexpectedly small target set')

    norm_specs = [
        ('C_density', 'C_density_raw'), ('C_node', 'C_node_raw'),
        ('P_density', 'P_density_raw'), ('P_mass', 'P_mass_raw'),
        ('R_density', 'R_density_raw'), ('R_node', 'R_node_raw'),
        ('T', 'T_raw'),
    ]
    for out_name, raw_name in norm_specs:
        values = [x[raw_name] for x in targets]
        norm, qlo, qhi = winsor_norm(values)
        print(f'{out_name}: p05={qlo:.6f} p95={qhi:.6f}', flush=True)
        for row, value in zip(targets, norm):
            row[out_name] = value

    for row in targets:
        row['C'] = 0.72 * row['C_density'] + 0.28 * row['C_node']
        row['P'] = 0.78 * row['P_density'] + 0.22 * row['P_mass']
        row['R'] = 0.75 * row['R_density'] + 0.25 * row['R_node']
        row['score'] = sum(COMPONENT_WEIGHTS[c] * row[c] for c in COMPONENT_WEIGHTS)

    percentiles = rank_percentiles(targets)
    for row, pct in zip(targets, percentiles):
        row['percentile'] = pct
        row['new_infra'] = infra_from_percentile(pct)

    fields = [
        'state_id','name','lon','lat','provinces','pixels','area_proxy','effective_area',
        'manpower','vp_count','max_vp','vp_weight','urban_count','rail_degree','rail_provinces','hubs',
        'C_density_raw','C_node_raw','P_density_raw','P_mass_raw','R_density_raw','R_node_raw','T_raw',
        'C_density','C_node','P_density','P_mass','R_density','R_node','T','C','P','R',
        'score','percentile','old_infra','new_infra'
    ]
    with REPORT.open('w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for row in targets:
            writer.writerow({k: (f'{row[k]:.6f}' if isinstance(row[k], float) else row[k]) for k in fields})

    print('Distribution:', {i: sum(r['new_infra'] == i for r in targets) for i in range(1, 10)}, flush=True)
    print('Top:', [(r['state_id'], r['name'], round(r['score'],3), round(r['percentile'],1), r['new_infra']) for r in sorted(targets, key=lambda x:x['score'], reverse=True)[:15]], flush=True)
    print('Bottom:', [(r['state_id'], r['name'], round(r['score'],3), round(r['percentile'],1), r['new_infra']) for r in sorted(targets, key=lambda x:x['score'])[:15]], flush=True)

    if not APPLY_CHANGES:
        print('Report-only calibration pass: state files were not modified.', flush=True)
        return

    changed = 0
    for row in targets:
        st = states[row['state_id']]
        new, n = re.subn(r'(\binfrastructure\s*=\s*)\d+', lambda m: m.group(1) + str(row['new_infra']), st['text'], count=1)
        if n != 1:
            raise RuntimeError(f'Infrastructure replacement failed for {st["path"]}')
        if new != st['text']:
            st['path'].write_text(new, encoding='utf-8-sig' if st['bom'] else 'utf-8')
            changed += 1
    print(f'Changed state files: {changed}/{len(targets)}', flush=True)


if __name__ == '__main__':
    main()
