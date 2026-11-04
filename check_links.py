"""Checks every link in the built pages: local files, #anchors, and external URLs (HTTP status)."""
import re, urllib.request
from pathlib import Path
root = Path(__file__).parent; bad = 0; ext = set()
pages = {p.name: p.read_text(encoding='utf8') for p in root.glob('*.html')}
for name, s in pages.items():
    for u in re.findall(r'(?:href|src)="([^"]+)"', s):
        u = u.replace('&amp;', '&')
        if u.startswith('http'): ext.add(u); continue
        if u.startswith(('mailto:', 'tel:')): continue
        f, _, a = u.partition('#'); t = f or name
        if not (root / t).exists(): print('MISSING', name, u); bad += 1
        elif a and f'id="{a}"' not in pages.get(t, ''): print('NO ANCHOR', name, u); bad += 1
    if re.search(r'href="#"', s): print('DEAD #', name); bad += 1
for u in sorted(ext):
    try: c = urllib.request.urlopen(urllib.request.Request(u), timeout=25).status
    except Exception as e: c = getattr(e, 'code', str(e))
    print(c, u[:90])
    if c != 200 and 'fonts.g' not in u: bad += 1
print('problems:', bad); assert bad == 0
