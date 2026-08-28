import csv, math, re
from pathlib import Path

import cv2
import numpy as np
import osmium
from PIL import Image
from pyproj import Geod
from shapely.geometry import LineString, Polygon
from shapely.ops import unary_union
from shapely.strtree import STRtree

ROOT = Path('.')
STATE_DIR = ROOT / 'history' / 'states'
PROVINCES_BMP = ROOT / 'map' / 'provinces.bmp'
DEFINITION = ROOT / 'map' / 'definition.csv'
REPORT = ROOT / 'soviet-infra-report.csv'
OSM_DIR = ROOT / '.osm-cache'

WEIGHTS = {'A': 1.0, 'H': 0.7, 'G': 0.35, 'D': 0.1}
MIN_LON, MAX_LON = 18.0, 62.5
MIN_LAT, MAX_LAT = 38.0, 72.5
GEOD = Geod(ellps='WGS84')

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

ROAD_CLASS = {}
for x in ('motorway','motorway_link','trunk','trunk_link','primary','primary_link'):
    ROAD_CLASS[x] = 'A'
for x in ('secondary','secondary_link','tertiary','tertiary_link'):
    ROAD_CLASS[x] = 'H'
for x in ('unclassified','residential','living_street','service'):
    ROAD_CLASS[x] = 'G'
ROAD_CLASS['track'] = 'D'


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
    lon_rmse = float(np.sqrt(np.mean((np.polyval(lon_coef, xs) - np.asarray(lons)) ** 2)))
    lat_rmse = float(np.sqrt(np.mean((np.polyval(lat_coef, zs) - np.asarray(lats)) ** 2)))
    print(f'Projection controls={len(xs)} lon_rmse={lon_rmse:.3f} lat_rmse={lat_rmse:.3f}', flush=True)
    return lon_coef, lat_coef


def xy_to_lonlat(x, y, height, lon_coef, lat_coef):
    z = (height - 1) - y
    return float(np.polyval(lon_coef, x)), float(np.polyval(lat_coef, z))


def state_geometry(mask, lon_coef, lat_coef):
    contours, _ = cv2.findContours(mask.astype(np.uint8) * 255, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return None
    h = mask.shape[0]
    polys = []
    for c in contours:
        if cv2.contourArea(c) < 3:
            continue
        c = cv2.approxPolyDP(c, max(1.0, 0.0015 * cv2.arcLength(c, True)), True)
        coords = []
        for p in c[:, 0, :]:
            lon, lat = xy_to_lonlat(float(p[0]), float(p[1]), h, lon_coef, lat_coef)
            coords.append((lon, lat))
        if len(coords) < 3:
            continue
        poly = Polygon(coords)
        if not poly.is_valid:
            poly = poly.buffer(0)
        if not poly.is_empty:
            polys.append(poly)
    if not polys:
        return None
    geom = unary_union(polys)
    if not geom.is_valid:
        geom = geom.buffer(0)
    return geom


def geometry_km(geom):
    if geom.is_empty:
        return 0.0
    try:
        return abs(float(GEOD.geometry_length(geom))) / 1000.0
    except Exception:
        total = 0.0
        parts = [geom] if geom.geom_type == 'LineString' else list(getattr(geom, 'geoms', []))
        for part in parts:
            if part.geom_type != 'LineString':
                continue
            pts = list(part.coords)
            for a, b in zip(pts, pts[1:]):
                _, _, m = GEOD.inv(a[0], a[1], b[0], b[1])
                total += abs(m) / 1000.0
        return total


class RoadHandler(osmium.SimpleHandler):
    def __init__(self, state_ids, geoms, tree):
        super().__init__()
        self.state_ids = state_ids
        self.geoms = geoms
        self.tree = tree
        self.seen = set()
        self.lengths = {sid: {'A':0.0,'H':0.0,'G':0.0,'D':0.0} for sid in state_ids}
        self.relevant_ways = 0
        self.clipped_hits = 0

    def way(self, w):
        if w.id in self.seen:
            return
        cls = ROAD_CLASS.get(w.tags.get('highway'))
        if cls is None:
            return
        self.seen.add(w.id)
        coords = []
        for n in w.nodes:
            if not n.location.valid():
                return
            coords.append((n.lon, n.lat))
        if len(coords) < 2:
            return
        minx = min(x for x, _ in coords); maxx = max(x for x, _ in coords)
        miny = min(y for _, y in coords); maxy = max(y for _, y in coords)
        if maxx < MIN_LON - 1 or minx > MAX_LON + 1 or maxy < MIN_LAT - 1 or miny > MAX_LAT + 1:
            return
        line = LineString(coords)
        if line.is_empty:
            return
        self.relevant_ways += 1
        for idx in self.tree.query(line, predicate='intersects'):
            geom = self.geoms[int(idx)]
            inter = line.intersection(geom)
            km = geometry_km(inter)
            if km > 0:
                sid = self.state_ids[int(idx)]
                self.lengths[sid][cls] += km
                self.clipped_hits += 1


def main():
    pbf_files = sorted(OSM_DIR.glob('*.osm.pbf'))
    if not pbf_files:
        raise RuntimeError(f'No PBF files found in {OSM_DIR}')
    print(f'PBF extracts: {len(pbf_files)}', flush=True)
    for p in pbf_files:
        print(f'  {p.name}: {p.stat().st_size / (1024**2):.1f} MiB', flush=True)

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
        if not len(xs):
            continue
        lon, lat = xy_to_lonlat(float(xs.mean()), float(ys.mean()), prov.shape[0], lon_coef, lat_coef)
        if not (MIN_LON <= lon <= MAX_LON and MIN_LAT <= lat <= MAX_LAT):
            continue
        geom = state_geometry(state_raster == sid, lon_coef, lat_coef)
        if geom is None or geom.is_empty:
            raise RuntimeError(f'No geometry for state {sid}')
        targets.append({'state_id':sid, 'st':st, 'lon':lon, 'lat':lat, 'pixels':len(xs), 'geom':geom})
    targets.sort(key=lambda x: x['state_id'])
    print(f'Target Soviet states west of Urals: {len(targets)}', flush=True)
    if len(targets) < 25:
        raise RuntimeError('Unexpectedly small target set')

    state_ids = [x['state_id'] for x in targets]
    geoms = [x['geom'] for x in targets]
    tree = STRtree(geoms)
    handler = RoadHandler(state_ids, geoms, tree)

    for i, pbf in enumerate(pbf_files, 1):
        print(f'[{i}/{len(pbf_files)}] Reading {pbf.name}', flush=True)
        handler.apply_file(str(pbf), locations=True, idx='flex_mem')
        print(f'    relevant ways={handler.relevant_ways} clipped hits={handler.clipped_hits}', flush=True)

    results = []
    for item in targets:
        sid, st = item['state_id'], item['st']
        lengths = handler.lengths[sid]
        nprov = max(1, len(st['pids']))
        dens = {k: lengths[k] / nprov for k in WEIGHTS}
        score = sum(WEIGHTS[k] * dens[k] for k in WEIGHTS)
        results.append({
            'state_id':sid, 'name':st['name'], 'lon':item['lon'], 'lat':item['lat'],
            'provinces':nprov, 'pixels':item['pixels'],
            'A_km':lengths['A'], 'H_km':lengths['H'], 'G_km':lengths['G'], 'D_km':lengths['D'],
            'A_pp':dens['A'], 'H_pp':dens['H'], 'G_pp':dens['G'], 'D_pp':dens['D'],
            'S':score, 'old_infra':st['old_infra']
        })

    smax = max(r['S'] for r in results)
    if smax <= 0:
        raise RuntimeError('Smax is zero')
    for r in results:
        r['new_infra'] = max(0, min(10, int(math.floor(10.0 * r['S'] / smax + 1e-12))))

    fields = ['state_id','name','lon','lat','provinces','pixels','A_km','H_km','G_km','D_km',
              'A_pp','H_pp','G_pp','D_pp','S','old_infra','new_infra']
    with REPORT.open('w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in results:
            w.writerow({k:(f'{r[k]:.6f}' if isinstance(r[k],float) else r[k]) for k in fields})

    print(f'Smax={smax:.6f}', flush=True)
    print('Distribution:', {i:sum(r['new_infra']==i for r in results) for i in range(11)}, flush=True)
    print('Top:', [(r['state_id'], r['name'], round(r['S'],2), r['new_infra'])
                   for r in sorted(results,key=lambda x:x['S'],reverse=True)[:12]], flush=True)
    print('Bottom:', [(r['state_id'], r['name'], round(r['S'],2), r['new_infra'])
                      for r in sorted(results,key=lambda x:x['S'])[:12]], flush=True)

    changed = 0
    for r in results:
        st = states[r['state_id']]
        new, n = re.subn(r'(\binfrastructure\s*=\s*)\d+', lambda m:m.group(1)+str(r['new_infra']), st['text'], count=1)
        if n != 1:
            raise RuntimeError(f'Infrastructure replacement failed for {st["path"]}')
        if new != st['text']:
            st['path'].write_text(new, encoding='utf-8-sig' if st['bom'] else 'utf-8')
            changed += 1
    print(f'Changed state files: {changed}/{len(results)}', flush=True)


if __name__ == '__main__':
    main()
