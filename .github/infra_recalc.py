import csv, math, re, time
from pathlib import Path

import cv2
import numpy as np
import requests
from PIL import Image

ROOT = Path('.')
STATE_DIR = ROOT / 'history' / 'states'
PROVINCES_BMP = ROOT / 'map' / 'provinces.bmp'
DEFINITION = ROOT / 'map' / 'definition.csv'
REPORT = ROOT / 'soviet-infra-report.csv'

# User-approved model:
# S = 1.0*A + 0.7*H + 0.35*G + 0.1*D
# Infra = floor(10*S/Smax)
WEIGHTS = {'A': 1.0, 'H': 0.7, 'G': 0.35, 'D': 0.1}
MAX_LON = 62.5
MIN_LON = 18.0
MIN_LAT = 38.0
MAX_LAT = 72.5

OVERPASS = [
    'https://overpass-api.de/api/interpreter',
    'https://overpass.kumi.systems/api/interpreter',
]

# Province id -> (lon, lat). Used only to calibrate this branch's modified Miller projection.
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
    max_pid = 0
    with path.open('r', encoding='latin-1', errors='ignore', newline='') as f:
        for row in csv.reader(f, delimiter=';'):
            if len(row) < 4:
                continue
            try:
                pid = int(row[0]); r = int(row[1]); g = int(row[2]); b = int(row[3])
            except ValueError:
                continue
            rgb_by_pid[pid] = (r, g, b)
            max_pid = max(max_pid, pid)
    return rgb_by_pid, max_pid


def parse_states():
    states = {}
    for path in STATE_DIR.glob('*.txt'):
        text = path.read_text(encoding='utf-8-sig', errors='ignore')
        mid = re.search(r'(?m)^\s*id\s*=\s*(\d+)\s*$', text)
        mprov = re.search(r'\bprovinces\s*=\s*\{([^}]*)\}', text, re.S)
        mowner = re.search(r'\bowner\s*=\s*([A-Z0-9_]+)', text)
        minfra = re.search(r'\binfrastructure\s*=\s*(\d+)', text)
        if not (mid and mprov):
            continue
        sid = int(mid.group(1))
        states[sid] = {
            'id': sid,
            'path': path,
            'text': text,
            'pids': [int(x) for x in re.findall(r'\d+', mprov.group(1))],
            'owner': mowner.group(1) if mowner else '',
            'old_infra': int(minfra.group(1)) if minfra else None,
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
        raise RuntimeError(f'Only {len(xs)} projection controls found; need >=10')
    lon_coef = np.polyfit(np.asarray(xs), np.asarray(lons), 1)
    lat_coef = np.polyfit(np.asarray(zs), np.asarray(lats), 3)
    lon_rmse = float(np.sqrt(np.mean((np.polyval(lon_coef, xs) - np.asarray(lons)) ** 2)))
    lat_rmse = float(np.sqrt(np.mean((np.polyval(lat_coef, zs) - np.asarray(lats)) ** 2)))
    print(f'Projection controls={len(xs)} lon_rmse={lon_rmse:.3f} lat_rmse={lat_rmse:.3f}')
    return lon_coef, lat_coef


def xy_to_lonlat(x, y, height, lon_coef, lat_coef):
    z = (height - 1) - y
    return float(np.polyval(lon_coef, x)), float(np.polyval(lat_coef, z))


def state_polygon(mask, lon_coef, lat_coef):
    u8 = mask.astype(np.uint8) * 255
    contours, _ = cv2.findContours(u8, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return None
    contours.sort(key=cv2.contourArea, reverse=True)
    c = contours[0]
    peri = cv2.arcLength(c, True)
    c = cv2.approxPolyDP(c, max(1.5, 0.0025 * peri), True)
    h = mask.shape[0]
    pts = []
    for p in c[:, 0, :]:
        lon, lat = xy_to_lonlat(float(p[0]), float(p[1]), h, lon_coef, lat_coef)
        pts.append((lat, lon))
    if len(pts) < 3:
        return None
    if len(pts) > 120:
        step = math.ceil(len(pts) / 120)
        pts = pts[::step]
    return pts


def overpass_lengths(poly, sid):
    poly_s = ' '.join(f'{lat:.5f} {lon:.5f}' for lat, lon in poly)
    query = f'''[out:csv(class,length;false;";")][timeout:180];
way["highway"~"^(motorway|motorway_link|trunk|trunk_link|primary|primary_link)$"](poly:"{poly_s}")->.a;
make stat class="A",length=.a.sum(length()); out;
way["highway"~"^(secondary|secondary_link|tertiary|tertiary_link)$"](poly:"{poly_s}")->.h;
make stat class="H",length=.h.sum(length()); out;
way["highway"~"^(unclassified|residential|living_street|service)$"](poly:"{poly_s}")->.g;
make stat class="G",length=.g.sum(length()); out;
way["highway"="track"](poly:"{poly_s}")->.d;
make stat class="D",length=.d.sum(length()); out;'''
    last = None
    for attempt in range(5):
        url = OVERPASS[attempt % len(OVERPASS)]
        try:
            r = requests.post(url, data={'data': query}, timeout=220,
                              headers={'User-Agent': 'HER-Mod-infrastructure-audit/1.0'})
            if r.status_code == 200 and r.text.strip():
                vals = {'A': 0.0, 'H': 0.0, 'G': 0.0, 'D': 0.0}
                for row in csv.reader(r.text.splitlines(), delimiter=';'):
                    if len(row) >= 2 and row[0] in vals:
                        try:
                            vals[row[0]] = max(0.0, float(row[1])) / 1000.0
                        except ValueError:
                            pass
                return vals
            last = RuntimeError(f'HTTP {r.status_code}: {r.text[:160]}')
        except Exception as e:
            last = e
        time.sleep(4 + 3 * attempt)
    raise RuntimeError(f'Overpass failed for state {sid}: {last}')


def main():
    rgb_by_pid, max_pid = parse_definition(DEFINITION)
    states = parse_states()
    prov = build_province_raster(rgb_by_pid)
    lon_coef, lat_coef = projection_from_controls(prov)

    sid_lookup = np.zeros(max(max_pid, int(prov.max())) + 1, dtype=np.int32)
    for sid, st in states.items():
        for pid in st['pids']:
            if 0 <= pid < len(sid_lookup):
                sid_lookup[pid] = sid
    state_raster = sid_lookup[prov]

    targets = []
    for sid, st in states.items():
        if st['owner'] != 'SOV' or st['old_infra'] is None:
            continue
        ys, xs = np.where(state_raster == sid)
        if len(xs) == 0:
            continue
        lon, lat = xy_to_lonlat(float(xs.mean()), float(ys.mean()), prov.shape[0], lon_coef, lat_coef)
        if MIN_LON <= lon <= MAX_LON and MIN_LAT <= lat <= MAX_LAT:
            targets.append((sid, st, lon, lat, len(xs)))
    targets.sort()
    print(f'Target Soviet states west of Urals: {len(targets)}')
    if len(targets) < 25:
        raise RuntimeError(f'Unexpectedly small target set: {len(targets)}')

    results = []
    failures = []
    for idx, (sid, st, lon, lat, pixels) in enumerate(targets, 1):
        mask = state_raster == sid
        poly = state_polygon(mask, lon_coef, lat_coef)
        if not poly:
            failures.append((sid, 'no polygon'))
            continue
        try:
            lengths = overpass_lengths(poly, sid)
        except Exception as e:
            print(e)
            failures.append((sid, str(e)))
            continue
        nprov = max(1, len(st['pids']))
        dens = {k: v / nprov for k, v in lengths.items()}
        score = sum(WEIGHTS[k] * dens[k] for k in WEIGHTS)
        results.append({
            'state_id': sid, 'name': st['name'], 'path': str(st['path']),
            'lon': lon, 'lat': lat, 'provinces': nprov, 'pixels': pixels,
            'A_km': lengths['A'], 'H_km': lengths['H'],
            'G_km': lengths['G'], 'D_km': lengths['D'],
            'A_pp': dens['A'], 'H_pp': dens['H'],
            'G_pp': dens['G'], 'D_pp': dens['D'],
            'S': score, 'old_infra': st['old_infra'],
        })
        print(f'[{idx}/{len(targets)}] {sid:>3} {st["name"][:28]:28} S={score:.2f}')
        time.sleep(1.0)

    if failures:
        print('FAILURES:')
        for f in failures:
            print(f)
        raise RuntimeError(f'{len(failures)} target states failed; refusing partial rewrite')
    if not results:
        raise RuntimeError('No infrastructure scores calculated')

    smax = max(r['S'] for r in results)
    if smax <= 0:
        raise RuntimeError('Smax is zero')
    for r in results:
        r['new_infra'] = max(0, min(10, int(math.floor(10.0 * r['S'] / smax + 1e-12))))

    fields = ['state_id', 'name', 'lon', 'lat', 'provinces', 'pixels',
              'A_km', 'H_km', 'G_km', 'D_km', 'A_pp', 'H_pp', 'G_pp', 'D_pp',
              'S', 'old_infra', 'new_infra']
    with REPORT.open('w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in results:
            w.writerow({k: (f'{r[k]:.6f}' if isinstance(r[k], float) else r[k]) for k in fields})

    print(f'Smax={smax:.6f}')
    print('Distribution:', {i: sum(r['new_infra'] == i for r in results) for i in range(11)})

    changed = 0
    for r in results:
        st = states[r['state_id']]
        old = st['text']
        new, n = re.subn(r'(\binfrastructure\s*=\s*)\d+',
                         lambda m: m.group(1) + str(r['new_infra']), old, count=1)
        if n != 1:
            raise RuntimeError(f'Infrastructure replacement failed for {st["path"]}')
        if new != old:
            st['path'].write_text(new, encoding='utf-8')
            changed += 1
    print(f'Changed state files: {changed}/{len(results)}')


if __name__ == '__main__':
    main()
