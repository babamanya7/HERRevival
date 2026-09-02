from pathlib import Path
import math
import re

STATE_DIR = Path('history/states')

TARGETS = {
    'ENG': 75,
    'USA': 40,
    'JAP': 30,
    'GER': 23,
    'FRA': 22,
    'ITA': 18,
    'SOV': 10,
    'CHI': 0,
    'HOL': 7,
    'NOR': 2,
    'DEN': 2,
    'CAN': 3,
    'AST': 3,
    'SPR': 4,
    'POL': 3,
}

def matching_brace(text, open_pos):
    depth = 0
    for i in range(open_pos, len(text)):
        if text[i] == '{': depth += 1
        elif text[i] == '}':
            depth -= 1
            if depth == 0: return i
    raise ValueError('unmatched brace')

def find_block(text, name, start=0, end=None, required_depth=None):
    if end is None: end = len(text)
    pat = re.compile(rf'\b{re.escape(name)}\s*=\s*\{{')
    for m in pat.finditer(text, start, end):
        op = text.find('{', m.start(), m.end())
        if required_depth is not None:
            d = 0
            for ch in text[start:m.start()]:
                if ch == '{': d += 1
                elif ch == '}': d -= 1
            if d != required_depth: continue
        return m.start(), op, matching_brace(text, op)
    return None

def top_level_value(body, key):
    depth = 0
    pat = re.compile(rf'^\s*{re.escape(key)}\s*=\s*([^#\s]+)')
    for line in body.splitlines():
        if depth == 0:
            m = pat.match(line)
            if m: return m.group(1)
        depth += line.count('{') - line.count('}')
    return None

def top_level_has(body, key, value):
    depth = 0
    pat = re.compile(rf'^\s*{re.escape(key)}\s*=\s*{re.escape(value)}(?:\s|$)')
    for line in body.splitlines():
        if depth == 0 and pat.match(line): return True
        depth += line.count('{') - line.count('}')
    return False

def direct_building_count(text, key):
    hist = find_block(text, 'history')
    if not hist: return 0
    _, ho, hc = hist
    b = find_block(text, 'buildings', ho+1, hc, required_depth=0)
    if not b: return 0
    _, bo, bc = b
    body = text[bo+1:bc]
    depth = 0
    pat = re.compile(rf'^\s*{re.escape(key)}\s*=\s*(\d+)\s*(?:#.*)?$')
    for line in body.splitlines():
        if depth == 0:
            m = pat.match(line)
            if m: return int(m.group(1))
        depth += line.count('{') - line.count('}')
    return 0

def replace_direct_building(text, key, value):
    hist = find_block(text, 'history')
    _, ho, hc = hist
    b = find_block(text, 'buildings', ho+1, hc, required_depth=0)
    if not b:
        if value == 0: return text
        ins = f'\n\t\tbuildings = {{\n\t\t\t{key} = {value}\n\t\t}}\n'
        return text[:hc] + ins + text[hc:]
    _, bo, bc = b
    body = text[bo+1:bc]
    lines = body.splitlines(keepends=True)
    depth = 0
    pat = re.compile(rf'^(\s*){re.escape(key)}\s*=\s*\d+(\s*(?:#.*)?)(\r?\n)?$')
    found = False
    for i, line in enumerate(lines):
        if depth == 0:
            m = pat.match(line)
            if m:
                found = True
                if value == 0: lines[i] = ''
                else:
                    nl = m.group(3) or ''
                    lines[i] = f'{m.group(1)}{key} = {value}{m.group(2)}{nl}'
                break
        depth += line.count('{') - line.count('}')
    if not found and value > 0:
        indent = '\t\t\t'
        suffix = '' if body.endswith(('\n','\r')) else '\n'
        lines.append(f'{suffix}{indent}{key} = {value}\n')
    return text[:bo+1] + ''.join(lines) + text[bc:]

def decode(path):
    data = path.read_bytes(); bom = data.startswith(b'\xef\xbb\xbf')
    return data.decode('utf-8-sig'), bom

def encode(path, text, bom):
    data = text.encode('utf-8')
    if bom: data = b'\xef\xbb\xbf' + data
    path.write_bytes(data)

def parse_state(path):
    text, bom = decode(path)
    hist = find_block(text, 'history')
    if not hist: return None
    _, ho, hc = hist
    hb = text[ho+1:hc]
    owner = top_level_value(hb, 'owner')
    if not owner: return None
    core = top_level_has(hb, 'add_core_of', owner)
    mm = re.search(r'\bmanpower\s*=\s*(\d+)', text)
    mp = int(mm.group(1)) if mm else 0
    return {'path':path,'text':text,'bom':bom,'owner':owner,'core':core,'manpower':mp,'dock':direct_building_count(text,'dockyard')}

def allocate(states, target):
    cur = [s['dock'] for s in states]
    if sum(cur) == target: return cur
    weights = cur[:]
    if sum(weights) == 0:
        weights = [max(1.0, math.sqrt(max(1,s['manpower']))) for s in states]
    tw = float(sum(weights))
    raw = [target*w/tw for w in weights]
    out = [int(math.floor(x)) for x in raw]
    rem = target - sum(out)
    order = sorted(range(len(states)), key=lambda i:(raw[i]-out[i],cur[i],states[i]['manpower']), reverse=True)
    for i in order[:rem]: out[i]+=1
    return out

states=[]
for p in sorted(STATE_DIR.glob('*.txt')):
    s=parse_state(p)
    if s: states.append(s)

before_total=after_total=0
changed=set(); report=[]
for tag,target in TARGETS.items():
    owned=[s for s in states if s['owner']==tag]
    before=sum(s['dock'] for s in owned)
    before_total+=before; after_total+=target
    adjustable=[s for s in owned if s['core']]
    fixed=[s for s in owned if not s['core']]
    fixed_d=sum(s['dock'] for s in fixed)
    adj_target=target-fixed_d
    if adj_target<0: raise RuntimeError(f'{tag}: target below fixed non-core docks ({fixed_d}>{target})')
    vals=allocate(adjustable, adj_target)
    for s,new in zip(adjustable,vals):
        if new!=s['dock']:
            nt=replace_direct_building(s['text'],'dockyard',new)
            encode(s['path'],nt,s['bom']); changed.add(str(s['path']))
            s['text']=nt; s['dock']=new
    after=fixed_d+sum(vals)
    if after!=target: raise RuntimeError(f'{tag}: verification failed {after}!={target}')
    report.append(f'{tag}: {before} -> {after} (delta {after-before:+d})')
print('\n'.join(report))
print(f'\nChanged state files: {len(changed)}')
print(f'Selected-country docks: {before_total} -> {after_total} ({after_total-before_total:+d}, {(after_total/before_total-1)*100:+.2f}%)')
