import json, sys
from pathlib import Path

listingDir = Path(sys.argv[1])
chunkDir = Path(sys.argv[2])
outDir = Path(sys.argv[3])

listingP = Path(listingDir, '.listing_approved')
chunkerP = Path(listingDir, '.listing_chunker')

listing = json.loads(listingP.read_text('utf-8'))
chunker = json.loads(chunkerP.read_text('utf-8'))

for p, v in listing.items():
    sz, digest = v.split('~')
    fileP = Path(outDir, p)
    fileP.parent.mkdir(parents=True, exist_ok=True)
    file = fileP.open('wb')
    for chunk_i, chunkDigest in enumerate(chunker[digest] or [digest]):
        chunk = Path(chunkDir, chunkDigest).read_bytes()
        file.write(chunk)




