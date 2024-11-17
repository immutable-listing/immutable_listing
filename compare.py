import json, sys
from pathlib import Path

listingOldP = Path(sys.argv[1]).absolute()
listingNewP = Path(sys.argv[2]).absolute()

listingOld = json.loads(listingOldP.read_text('utf-8'))
listingNew = json.loads(listingNewP.read_text('utf-8'))

if listingOld == listingNew:
    print('No changes')
    raise SystemExit(0)

listingOldKeys = set(listingOld.keys())
listingNewKeys = set(listingNew.keys())
added = sorted(listingNewKeys - listingOldKeys)
removed = sorted(listingOldKeys - listingNewKeys)
modified = []
for p in sorted(listingNewKeys & listingOldKeys):
    newV = listingNew[p]
    oldV = listingOld[p]
    if newV != oldV:
        modified.append((p, oldV, newV))

tab = '    '
print('Added:')
for p in added:
    print(f'{tab}{p}')
print('Removed:')
for p in removed:
    print(f'{tab}{p}')
print('Modified:')
for p, oldV, newV in modified:
    print(f'{tab}{p}')
    print(f'{tab*2}-{oldV}')
    print(f'{tab*2}+{newV}')

print(f'Modified {len(modified)}, Removed {len(removed)}, Added {len(added)}')

if sorted(listingOld.values()) == sorted(listingNew.values()):
    print('Only renames')
    raise SystemExit(2)

raise SystemExit(3)
