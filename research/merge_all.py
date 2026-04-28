#!/usr/bin/env python3
"""Master merge: existing 102 + WA-new 342 + USAs 134 → unified DATA array.

Outputs `wa_merged_full.json` (the new combined DATA list ready for index.html)
plus a sanity report.
"""
import json, re
from pathlib import Path

ROOT  = Path(__file__).parent
REPO  = ROOT.parent
HTML  = REPO / 'index.html'

# ---------- 1. Extract existing 102 from index.html ----------
src = HTML.read_text()
m = re.search(r'const DATA = \[(.*?)\n\];', src, re.S)
if not m:
    raise SystemExit("Couldn't find DATA array in index.html")
js_body = m.group(1)

# Convert JS object syntax → JSON.
# Each row looks like: {name:"Foo",age:27,college:"X",fk:"14:50",...}
# Quote unquoted keys, replace null OK as-is.
def js_to_json(js: str) -> str:
    s = js
    # Quote bare keys (\w+:) → "\w+":
    s = re.sub(r'([{,])\s*(\w+)\s*:', r'\1"\2":', s)
    # Strip trailing commas before ] or }
    s = re.sub(r',(\s*[\]\}])', r'\1', s)
    return s

rows_json = '[' + js_to_json(js_body) + ']'
# Strip trailing commas now that brackets are in place.
rows_json = re.sub(r',(\s*[\]\}])', r'\1', rows_json)
existing = json.loads(rows_json)
print(f'Loaded existing: {len(existing)} athletes')

# ---------- 2. Load WA-new merged (342) and USAs (134) ----------
wa_new = json.loads((ROOT / 'wa_merged_new.json').read_text())
usas   = json.loads((ROOT / 'usas_starters.json').read_text())
print(f'Loaded WA-new: {len(wa_new)} athletes')
print(f'Loaded USAs starters: {len(usas)} athletes')

# ---------- 3. Canonical alias map ----------
# Maps lowercase variant → canonical lowercase. Canonical is what the existing
# list uses, or our chosen primary name for new athletes.
ALIASES = {
    # USAs agent's names → existing canonical names
    'andrea rodenfels':       'annie rodenfels',
    'gabbi jennings':         'gabrielle jennings',
    'kayley delay':           'kayley delay',          # cap variant only
    'krissy gear':            'kristlin gear',
    'lexy halladay-lowry':    'lexy halladay',
    'lucy nodler jenks':      'lucy jenks',
    'cailie hughes':          'cailie logue hughes',
    'margaret liebich':       'maggie liebich',
    'sam nadel':              'samantha nadel',
    'kasandra parker':        'kassie parker',
    'jackie gaughan':         'jacqueline gaughan',
    'amaya noe':              'amaya aramini',         # same person? verify
    # WA-new internal aliases (already merged by WA id, just safety)
    'sydney vaught':          'sydney thorvaldson',
    'danielle polerecky':     'danielle shanahan',
    'raygan peterson':        'raygan dimond',
    'lauren goss':            'lauren hurley',
    # Maiden → married for existing list
    'josette norris':         'josette andrews',
    'whittni orton':          'whittni morgan',
    'rachel schneider':       'rachel smith',
    'lucy nodler':            'lucy jenks',
    'jessica tonn':           'jessica mcclain',
    "abbey d'agostino":       'abbey cooper',
    'kellyn johnson':         'kellyn taylor',
    'logan morris':           'logan jolly',
    'stephanie rothstein':    'stephanie bruce',
    'amy davis':              'amy davis-green',
    'jessica gockley':        'jessica gockley-day',
    'cailie logue':           'cailie logue hughes',
    'lauren goss':            'lauren hurley',
    'anna camp':              'anna camp bennett',
    # Spelling/alias variants
    'jessica mclain':         'jessica mcclain',       # typo
    'elena henes':            'elly henes',
    'valerie constien':       'val constien',
    'weini kelati frezghi':   'weini kelati',
    'katie thronson':         'katherine thronson',
    'faith demars':           'faith demars',          # cap
    'emma grace hurley':      'emma grace hurley',
}

def canon_key(name: str) -> str:
    k = name.lower().strip()
    # Apply alias chain (max 3 hops).
    for _ in range(3):
        if k in ALIASES and ALIASES[k] != k:
            k = ALIASES[k]
        else:
            break
    return k

# ---------- 4. Build canonical store ----------
master: dict[str, dict] = {}

def ensure(name: str, defaults: dict | None = None) -> dict:
    key = canon_key(name)
    if key not in master:
        master[key] = {
            'name': name,
            'age':     None,
            'college': '',
            'fk': '', 'sc': '', 'tenk': '',
            'events': '',
            'ig': '',
        }
        if defaults:
            master[key].update(defaults)
    return master[key]

# 4a. Seed from existing 102 (full source of truth for these athletes).
for a in existing:
    key = canon_key(a['name'])
    obj = {
        'name':    a['name'],
        'age':     a.get('age'),
        'college': a.get('college', ''),
        'fk':      a.get('fk', ''),
        'sc':      a.get('sc', ''),
        'tenk':    a.get('tenk', ''),
        'events':  a.get('events', ''),
        'ig':      a.get('ig', ''),
    }
    if 'maiden' in a:
        obj['maiden'] = a['maiden']
    master[key] = obj

# 4b. Layer WA-new athletes (PBs + flags). If key already exists from existing,
#     skip — existing has authoritative PBs. Otherwise create new entry.
wa_added, wa_merged = 0, 0
for a in wa_new:
    key = canon_key(a['name'])
    if key in master:
        # Already on existing list (probably under a different name).
        # Don't overwrite existing PBs, but record the WA URL on a side channel
        # if we want it later. For now, just skip silently.
        wa_merged += 1
        continue
    obj = {
        'name': a['name'],
        'age':  None,
        'college': '',
        'fk':    a.get('fk', ''),
        'sc':    a.get('sc', ''),
        'tenk':  a.get('tenk', ''),
        'events': '',
        'ig':    '',
    }
    if 'maiden' in a:
        obj['maiden'] = a['maiden']
    master[key] = obj
    wa_added += 1

print(f'WA-new: {wa_added} added as new athletes, {wa_merged} matched into existing 102')

# 4c. Layer USAs events. If athlete unknown, add new entry with events only.
def merge_events(existing: str, incoming: str) -> str:
    """Union years per event code."""
    if not existing:
        return incoming
    if not incoming:
        return existing
    def parse(s):
        out = {}
        for chunk in [c.strip() for c in s.split(',') if c.strip()]:
            parts = chunk.split()
            ev = parts[0]
            yrs = set(parts[1:])
            out.setdefault(ev, set()).update(yrs)
        return out
    a, b = parse(existing), parse(incoming)
    keys = list(dict.fromkeys(list(a) + list(b)))   # preserve order
    out = []
    for k in keys:
        yrs = sorted(a.get(k, set()) | b.get(k, set()))
        out.append(f"{k} " + ' '.join(yrs))
    return ', '.join(out)

usas_added, usas_merged = 0, 0
for a in usas:
    key = canon_key(a['name'])
    if key in master:
        master[key]['events'] = merge_events(master[key].get('events',''), a['events'])
        usas_merged += 1
    else:
        master[key] = {
            'name': a['name'],
            'age':  None,
            'college': '',
            'fk': '', 'sc': '', 'tenk': '',
            'events': a['events'],
            'ig': '',
        }
        usas_added += 1

print(f'USAs: {usas_added} added as new (criterion-B only), {usas_merged} merged events into known athletes')

# ---------- 5. Sort + emit ----------
def time_to_sec(t):
    if not t: return 9999
    try:
        m, s = t.split(':')
        return float(m) * 60 + float(s)
    except Exception:
        return 9999

def sort_key(a):
    fk_s   = time_to_sec(a['fk'])
    sc_s   = time_to_sec(a['sc'])
    tenk_s = time_to_sec(a['tenk'])
    primary = min(fk_s, sc_s + 0.0001, tenk_s)
    return (primary, fk_s, sc_s, tenk_s, a['name'].lower())

result = list(master.values())
result.sort(key=sort_key)

# Output JSON.
out = ROOT / 'wa_merged_full.json'
out.write_text(json.dumps(result, indent=2))
print(f'\nFinal: {len(result)} unique athletes')
print(f'  with 5K mark:  {sum(1 for a in result if a["fk"])}')
print(f'  with SC mark:  {sum(1 for a in result if a["sc"])}')
print(f'  with 10K mark: {sum(1 for a in result if a["tenk"])}')
print(f'  with USAs events: {sum(1 for a in result if a["events"])}')
print(f'  with no PBs (USAs-only): {sum(1 for a in result if not (a["fk"] or a["sc"] or a["tenk"]))}')
print(f'  with college (existing 102): {sum(1 for a in result if a["college"])}')
