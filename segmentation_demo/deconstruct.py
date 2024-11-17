import json, sys
from pathlib import Path

listingDir = Path(sys.argv[1])
outDir = Path(sys.argv[2])

listingP = Path(listingDir, '.listing_approved')
chunkerP = Path(listingDir, '.listing_chunker')

listing = json.loads(listingP.read_text('utf-8'))
chunker = json.loads(chunkerP.read_text('utf-8'))

chunkSz = int(chunker['']['bs']) * 1024

for p, v in listing.items():
    sz, digest = v.split('~')
    file = Path(listingDir, p).open('rb')
    for chunk_i, chunkDigest in enumerate(chunker[digest] or [digest]):
        chunkP = Path(outDir, chunkDigest)
        if chunkP.exists():
            continue
        chunkP.write_bytes(file.read(chunkSz))




