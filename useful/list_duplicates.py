import sys, json
from pathlib import Path
from collections import defaultdict

listingP = Path(sys.argv[1])
listing = json.loads(listingP.read_text("utf-8"))

v2p = defaultdict(list)
for p, v in listing.items():
    v2p[v].append(p)

for v, ps in v2p.items():
    if len(ps) == 1:
        continue
    print()
    print('\n'.join(ps))

print()
