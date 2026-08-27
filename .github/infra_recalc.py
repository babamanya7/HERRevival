import csv, math, re, time
from concurrent.futures import ThreadPoolExecutor, as_completed
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

WEIGHTS = {'A': 1.0, 'H': 0.7, 'G': 0.35, 'D': 0.1}
MIN_LON, MAX_LON = 18.0, 62.5
MIN_LAT, MAX_LAT = 38.0, 72.5
BATCH_SIZE = 12
WORKERS = 3
OVERPASS = [
    'https://overpass-api.de/api/interpreter',
    'https://overpass.kumi.systems/api/interpreter',
]
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
ROAD_RE = {
    'A': '^(motorway|motorway_link|trunk|trunk_link|primary|primary_link)$',
    'H': '^(secondary|secondary_link|tertiary|tertiary_link)$',
    'G': '^(unclassified|residential|living_street|service)$',
    'D': '^track$',
}


def parse_definition(path):
    rgb_by_pid, max_pid = {}, 0
    with path.open('r', encoding='latin-1', errors='ignore', newline='') as f:
        for row in csv.reader(f, delimiter=';'):
            if len(row) < 4:
                continue
            try:
                pid, r, g, b = map(int, row[:4])
            except ValueError:
                continue
            rgb_by_pid[pid] = (r, g, b)
            max_pid = max(max_pid, pid)
    return rgb_by_pid, max_pid


def parse_states():
    states = {}
    for path in STATE_DIR.glob('*.txt'):
        raw = path.read_bytes()
        text = raw.decode('utf-8-sig', errors='ignore')
        mid = re.search(r'(?m)^\s*id\s*=\s*(\d+)\s*$', text)
        mprov = re.search(r'\bprovinces\s*=\s*\{([^}]*)\}', text, re.S)
        mowner = re.search(r'\bowner\s*=\s*([A-Z0-9_]+)', text)
        minfra = re.search(r'\binfrastructure\s*=\s*(\d+)', text)
        if not (mid and mprov):
            continue
        sid = int(mid.group(1))
        states[sid] = {
            'id': sid, 'path': path, 'text': text,
            'bom': raw.startswith(b'\xef\xbb\xbf'),
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
        xs.append(float(xx.mean())); zs.append(float((h - 1) - ys.mean()))
        lons.append(lon); lats.append(lat)
    if len(xs) < 10:
        raise RuntimeError(f'Only {len(xs)} projection controls found')
    lon_coef = np.polyfit(xs, lons, 1)
    lat_coef = np.polyfit(zs, lats, 3)
    print('Projection controls=', len(xs),
          'lon_rmse=', round(float(np.sqrt(np.mean((np.polyval(lon_coef, xs)-lons)**2))), 3),
          'lat_rmse=', round(float(np.sqrt(np.mean((np.polyval(lat_coef, zs)-lats)**2))), 3), flush=True)
    return lon_coef, lat_coef


def xy_to_lonlat(x, y, height, lon_coef, lat_coef):
    z = (height - 1) - y
    return float(np.polyval(lon_coef, x)), float(np.polyval(lat_coef, z))


def state_polygon(mask, lon_coef, lat_coef):
    contours, _ = cv2.findContours(mask.astype(np.uint8) * 255, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return None
    c = sorted(contours, key=cv2.contourArea, reverse=True)[0]
    c = cv2.approxPolyDP(c, max(1.5, 0.0025 * cv2.arcLength(c, True)), True)
    h = mask.shape[0]
    pts = []
    for p in c[:, 0, :]:
        lon, lat = xy_to_lonlat(float(p[0]), float(p[1]), h, lon_coef, lat_coef)
        pts.append((lat, lon))
    if len(pts) < 3:
        return None
    if len(pts) > 100:
        pts = pts[::math.ceil(len(pts) / 100)]
    return pts


def make_batch_query(batch):
    lines = ['[out:csv(sid,class,length;false;";")][timeout:300];']
    for item in batch:
        sid = item['state_id']
        poly = ' '.join(f'{lat:.5f} {lon:.5f}' for lat, lon in item['poly'])
        for cls, regex in ROAD_RE.items():
            setname = f's{sid}{cls.lower()}'
            lines.append(f'way["highway"~"{regex}"](poly:"{poly}")->.{setname};')
            lines.append(f'make stat sid="{sid}",class="{cls}",length=.{setname}.sum(length()); out;')
    return '\n'.join(lines)


def fetch_batch(batch, batch_no):
    query = make_batch_query(batch)
    last = None
    for attempt in range(4):
        url = OVERPASS[(batch_no + attempt) % len(OVERPASS)]
        try:
            r = requests.post(url, data={'data': query}, timeout=360,
                              headers={'User-Agent': 'HER-Mod-infrastructure-audit/2.0'})
            if r.status_code == 200 and r.text.strip():
                out = {x['state_id']: {'A':0.0,'H':0.0,'G':0.0,'D':0.0} for x in batch}
                for row in csv.reader(r.text.splitlines(), delimiter=';'):
                    if len(row) < 3:
                        continue
                    try:
                        sid = int(row[0]); cls = row[1]; km = max(0.0, float(row[2])) / 1000.0
                    except ValueError:
                        continue
                    if sid in out and cls in out[sid]:
                        out[sid][cls] = km
                return out
            last = RuntimeError(f'HTTP {r.status_code}: {r.text[:160]}')
        except Exception as e:
            last = e
        time.sleep(3 + 4 * attempt)
    raise RuntimeError(f'Batch {batch_no} failed: {last}')


def main():
    rgb_by_pid, max_pid = parse_definition(DEFINITION)
    states = parse_states()
    prov = build_province_raster(rgb_by_pid)
    lon_coef, lat_coef = projection_from_controls(prov)

    sid_lookup = np.zeros(max(max_pid, int(prov.max())) + 1, dtype=np.int32)
    for sid, st in states.items():
        for pid in st['pids']:
            if 0 <= pid < len(sid_lookup): sid_lookup[pid] = sid
    state_raster = sid_lookup[prov]

    targets = []
    for sid, st in states.items():
        if st['owner'] != 'SOV' or st['old_infra'] is None: continue
        ys, xs = np.where(state_raster == sid)
        if not len(xs): continue
        lon, lat = xy_to_lonlat(float(xs.mean()), float(ys.mean()), prov.shape[0], lon_coef, lat_coef)
        if not (MIN_LON <= lon <= MAX_LON and MIN_LAT <= lat <= MAX_LAT): continue
        poly = state_polygon(state_raster == sid, lon_coef, lat_coef)
        if not poly: raise RuntimeError(f'No polygon for state {sid}')
        targets.append({'state_id':sid, 'st':st, 'lon':lon, 'lat':lat, 'pixels':len(xs), 'poly':poly})
    targets.sort(key=lambda x: x['state_id'])
    print(f'Target Soviet states west of Urals: {len(targets)}', flush=True)
    if len(targets) < 25: raise RuntimeError('Unexpectedly small target set')

    batches = [targets[i:i+BATCH_SIZE] for i in range(0, len(targets), BATCH_SIZE)]
    all_lengths = {}
    print(f'Overpass batches: {len(batches)} x <= {BATCH_SIZE}, workers={WORKERS}', flush=True)
    with ThreadPoolExecutor(max_workers=WORKERS) as ex:
        futs = {ex.submit(fetch_batch, b, i): i for i, b in enumerate(batches, 1)}
        for fut in as_completed(futs):
            i = futs[fut]
            data = fut.result()
            all_lengths.update(data)
            print(f'Batch {i}/{len(batches)} done ({len(data)} states)', flush=True)

    results = []
    for item in targets:
        sid, st = item['state_id'], item['st']
        lengths = all_lengths.get(sid)
        if lengths is None: raise RuntimeError(f'Missing result for state {sid}')
        nprov = max(1, len(st['pids']))
        dens = {k: lengths[k] / nprov for k in WEIGHTS}
        score = sum(WEIGHTS[k] * dens[k] for k in WEIGHTS)
        results.append({'state_id':sid,'name':st['name'],'lon':item['lon'],'lat':item['lat'],
                        'provinces':nprov,'pixels':item['pixels'],
                        'A_km':lengths['A'],'H_km':lengths['H'],'G_km':lengths['G'],'D_km':lengths['D'],
                        'A_pp':dens['A'],'H_pp':dens['H'],'G_pp':dens['G'],'D_pp':dens['D'],
                        'S':score,'old_infra':st['old_infra']})

    smax = max(r['S'] for r in results)
    if smax <= 0: raise RuntimeError('Smax is zero')
    for r in results:
        r['new_infra'] = max(0, min(10, int(math.floor(10.0*r['S']/smax + 1e-12))))

    fields = ['state_id','name','lon','lat','provinces','pixels','A_km','H_km','G_km','D_km',
              'A_pp','H_pp','G_pp','D_pp','S','old_infra','new_infra']
    with REPORT.open('w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields); w.writeheader()
        for r in results:
            w.writerow({k:(f'{r[k]:.6f}' if isinstance(r[k],float) else r[k]) for k in fields})

    print(f'Smax={smax:.6f}', flush=True)
    print('Distribution:', {i:sum(r['new_infra']==i for r in results) for i in range(11)}, flush=True)
    print('Top:', [(r['state_id'], r['name'], round(r['S'],2), r['new_infra']) for r in sorted(results,key=lambda x:x['S'],reverse=True)[:12]], flush=True)

    changed = 0
    for r in results:
        st = states[r['state_id']]
        new, n = re.subn(r'(\binfrastructure\s*=\s*)\d+', lambda m:m.group(1)+str(r['new_infra']), st['text'], count=1)
        if n != 1: raise RuntimeError(f'Infrastructure replacement failed for {st["path"]}')
        if new != st['text']:
            st['path'].write_text(new, encoding='utf-8-sig' if st['bom'] else 'utf-8')
            changed += 1
    print(f'Changed state files: {changed}/{len(results)}', flush=True)


if __name__ == '__main__':
    main()
