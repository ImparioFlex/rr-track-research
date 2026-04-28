#!/usr/bin/env python3
"""Apply enrichment chunks to wa_merged_full.json.
Updates `age` / `college` / `ig` fields where the chunk has non-empty values.
"""
import json
from pathlib import Path

ROOT = Path(__file__).parent

master = json.loads((ROOT / 'wa_merged_full.json').read_text())
by_name = {a['name'].lower().strip(): a for a in master}

age_n, college_n, ig_n, missed = 0, 0, 0, 0
missed_names = []

for i in range(1, 6):
    p = ROOT / f'enrich_chunk_{i}_out.json'
    if not p.exists():
        print(f'!! missing {p.name}')
        continue
    rows = json.loads(p.read_text())
    for r in rows:
        key = r['name'].lower().strip()
        target = by_name.get(key)
        if not target:
            missed += 1
            missed_names.append(r['name'])
            continue
        if r.get('age') not in (None, '') and target.get('age') in (None, ''):
            target['age'] = r['age']
            age_n += 1
        if r.get('college') and not target.get('college'):
            target['college'] = r['college']
            college_n += 1
        if r.get('ig') and not target.get('ig'):
            target['ig'] = r['ig']
            ig_n += 1

(ROOT / 'wa_merged_full.json').write_text(json.dumps(master, indent=2))

print(f'Applied: age +{age_n}, college +{college_n}, ig +{ig_n}')
if missed:
    print(f'Missed (name not in master): {missed}')
    for n in missed_names[:10]:
        print(f'  - {n}')
print(f'\nMaster now: {len(master)} athletes')
print(f'  with age:     {sum(1 for a in master if a.get("age") not in (None,""))}')
print(f'  with college: {sum(1 for a in master if a.get("college"))}')
print(f'  with IG:      {sum(1 for a in master if a.get("ig"))}')
