#!/usr/bin/env python3
"""Apply ig_chunk_{1..4}_out.json results to wa_merged_full.json.

Updates `ig` field where the chunk has a value AND the master doesn't already
have one. Also opportunistically backfills `college` if it was blank in master
but the agent surfaced one (rare case — happened with Joy Gill).
"""
import json
from pathlib import Path

ROOT = Path(__file__).parent

master = json.loads((ROOT / 'wa_merged_full.json').read_text())
by_name = {a['name'].lower().strip(): a for a in master}

ig_n, college_n, missed = 0, 0, 0
missed_names = []

for i in range(1, 5):
    p = ROOT / f'ig_chunk_{i}_out.json'
    if not p.exists():
        print(f'!! missing {p.name}')
        continue
    rows = json.loads(p.read_text())
    for r in rows:
        target = by_name.get(r['name'].lower().strip())
        if not target:
            missed += 1
            missed_names.append(r['name'])
            continue
        if r.get('ig') and not target.get('ig'):
            target['ig'] = r['ig']
            ig_n += 1
        if r.get('college') and not target.get('college'):
            target['college'] = r['college']
            college_n += 1

(ROOT / 'wa_merged_full.json').write_text(json.dumps(master, indent=2))

print(f'Applied: ig +{ig_n}, college +{college_n} (backfill)')
if missed:
    print(f'Missed (name not in master): {missed}')
print(f'\nMaster now: {len(master)} athletes')
print(f'  with IG:      {sum(1 for a in master if a.get("ig"))}')
print(f'  with college: {sum(1 for a in master if a.get("college"))}')
