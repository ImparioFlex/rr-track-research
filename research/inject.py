#!/usr/bin/env python3
"""Inject the merged 447-athlete list into index.html's DATA array.
Preserves the existing one-line-per-athlete JS-object-literal style.
"""
import json, re
from pathlib import Path

ROOT = Path(__file__).parent
REPO = ROOT.parent
HTML = REPO / 'index.html'

athletes = json.loads((ROOT / 'wa_merged_full.json').read_text())

def js_str(s: str) -> str:
    """Escape a string for JS double-quoted literal."""
    s = s.replace('\\', '\\\\').replace('"', '\\"')
    return f'"{s}"'

def js_age(a):
    if a is None or a == '':
        return 'null'
    return str(int(a))

def fmt(a: dict) -> str:
    parts = [f'name:{js_str(a["name"])}']
    if a.get('maiden'):
        parts.append(f'maiden:{js_str(a["maiden"])}')
    parts.append(f'age:{js_age(a.get("age"))}')
    if a.get('age_est'):
        parts.append('age_est:true')
    parts.append(f'college:{js_str(a.get("college", ""))}')
    parts.append(f'fk:{js_str(a.get("fk", ""))}')
    parts.append(f'sc:{js_str(a.get("sc", ""))}')
    parts.append(f'tenk:{js_str(a.get("tenk", ""))}')
    parts.append(f'events:{js_str(a.get("events", ""))}')
    parts.append(f'ig:{js_str(a.get("ig", ""))}')
    return '  {' + ','.join(parts) + '},'

new_block = 'const DATA = [\n' + '\n'.join(fmt(a) for a in athletes) + '\n];'

src = HTML.read_text()
new_src, n = re.subn(r'const DATA = \[.*?\n\];', new_block, src, count=1, flags=re.S)
if n != 1:
    raise SystemExit(f"Expected 1 replacement, got {n}")
HTML.write_text(new_src)

print(f'Injected {len(athletes)} athletes into index.html')
print(f'New DATA block: {len(new_block)} chars across {len(athletes)} rows')
