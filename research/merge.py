#!/usr/bin/env python3
"""Merge the three WA event lists (5K / SC / 10K) into one deduped athlete list.
Dedupe key: WA athlete ID extracted from `wa_url`; falls back to lowercased name.
"""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).parent

FILES = [
    ('wa_5k_new.json',  'fk'),
    ('wa_sc_new.json',  'sc'),
    ('wa_10k_new.json', 'tenk'),
]

def extract_id(url: str) -> str | None:
    if not url:
        return None
    m = re.search(r'(?:athlete=|-)(\d+)$', url)
    return m.group(1) if m else None

master: dict[str, dict] = {}
name_to_key: dict[str, str] = {}

for fname, field in FILES:
    path = ROOT / fname
    rows = json.loads(path.read_text())
    for r in rows:
        wid = extract_id(r.get('wa_url', ''))
        nlow = r['name'].lower().strip()
        # If we already saw this name with a different id, treat as alias.
        if nlow in name_to_key:
            key = name_to_key[nlow]
        elif wid:
            key = wid
            name_to_key[nlow] = key
        else:
            key = nlow
            name_to_key[nlow] = key

        if key not in master:
            master[key] = {
                'name': r['name'],
                'wa_url': r.get('wa_url', ''),
                'fk': '', 'sc': '', 'tenk': '',
            }
            if 'maiden' in r:
                master[key]['maiden'] = r['maiden']
            if '_review' in r:
                master[key]['_review'] = r['_review']
        master[key][field] = r[field]
        # Carry forward review/maiden if seen on later list.
        if 'maiden' in r and 'maiden' not in master[key]:
            master[key]['maiden'] = r['maiden']
        if '_review' in r and '_review' not in master[key]:
            master[key]['_review'] = r['_review']

result = list(master.values())

# Sort: best 5K first (those who appear there), then SC, then 10K-only.
def time_to_sec(t):
    if not t:
        return 9999
    try:
        m, s = t.split(':')
        return float(m) * 60 + float(s)
    except Exception:
        return 9999

def sort_key(a):
    fk_s   = time_to_sec(a['fk'])
    sc_s   = time_to_sec(a['sc'])
    tenk_s = time_to_sec(a['tenk'])
    primary = min(fk_s, sc_s + 0.0001, tenk_s)  # tiny tiebreak
    return (primary, fk_s, sc_s, tenk_s, a['name'].lower())

result.sort(key=sort_key)

out = ROOT / 'wa_merged_new.json'
out.write_text(json.dumps(result, indent=2))

# Stats
def has(field):
    return sum(1 for a in result if a[field])
print(f'Total unique new athletes: {len(result)}')
print(f'  with 5K mark:   {has("fk")}')
print(f'  with SC mark:   {has("sc")}')
print(f'  with 10K mark:  {has("tenk")}')
print(f'  flagged for review: {sum(1 for a in result if "_review" in a)}')
print()
print('Cross-event athletes (appear on 2+ lists):')
multi = [a for a in result if sum([bool(a["fk"]), bool(a["sc"]), bool(a["tenk"])]) >= 2]
print(f'  count: {len(multi)}')
for a in multi[:20]:
    marks = []
    if a['fk']:   marks.append(f'5K {a["fk"]}')
    if a['sc']:   marks.append(f'SC {a["sc"]}')
    if a['tenk']: marks.append(f'10K {a["tenk"]}')
    print(f'  {a["name"]}: {" / ".join(marks)}')
if len(multi) > 20:
    print(f'  ... and {len(multi)-20} more')
