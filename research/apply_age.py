#!/usr/bin/env python3
"""Apply age_chunk_{1..4}_out.json results to wa_merged_full.json.

Updates `age` and `age_est` fields where the chunk has a value AND the master
doesn't already have one. Verified ages (`age_est: false` or omitted) are
preferred over estimates if both are available for the same athlete.
"""
import json
from pathlib import Path

ROOT = Path(__file__).parent

master = json.loads((ROOT / 'wa_merged_full.json').read_text())
by_name = {a['name'].lower().strip(): a for a in master}

verified, estimated, missed = 0, 0, 0
missed_names = []

for i in range(1, 5):
    p = ROOT / f'age_chunk_{i}_out.json'
    if not p.exists():
        print(f'!! missing {p.name}')
        continue
    rows = json.loads(p.read_text())
    for r in rows:
        if r.get('age') in (None, ''):
            continue
        target = by_name.get(r['name'].lower().strip())
        if not target:
            missed += 1
            missed_names.append(r['name'])
            continue
        if target.get('age') not in (None, ''):
            continue   # already filled (probably from earlier enrichment)
        target['age'] = r['age']
        if r.get('age_est'):
            target['age_est'] = True
            estimated += 1
        else:
            verified += 1

(ROOT / 'wa_merged_full.json').write_text(json.dumps(master, indent=2))

print(f'Applied: verified +{verified}, estimated +{estimated}')
if missed:
    print(f'Missed (name not in master): {missed}')
    for n in missed_names[:10]:
        print(f'  - {n}')
print(f'\nMaster now: {len(master)} athletes')
total_age = sum(1 for a in master if a.get('age') not in (None, ''))
total_est = sum(1 for a in master if a.get('age_est'))
print(f'  with age:        {total_age}')
print(f'    verified:      {total_age - total_est}')
print(f'    estimated (~): {total_est}')
