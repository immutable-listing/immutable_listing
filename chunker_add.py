import sys, json
from importlib import import_module
from pathlib import Path


def hashM(n):
    if n == 'sha256':
        return import_module('hashlib').sha256
    if n == 'md5':
        return import_module('hashlib').md5
    if n == 'blake3':
        return import_module('blake3').blake3
    if n == 'xxhash32':
        return import_module('xxhash').xxh32
    if n == 'xxhash64':
        return import_module('xxhash').xxh64
    if n == 'xxhash128':
        return import_module('xxhash').xxh128
    print(f'Unsupported hash name: "{n}"')
    raise SystemExit(1)

class Chunker:
    def __init__(self, mP, readBsKb):
        self.mP = Path(mP)
        self.m = json.loads(self.mP.read_text('ascii'))
        settings = self.m['']
        self.Hash = hashM(settings['hash'])
        chunkSzKb = str(settings['bs'])
        # 'b' suffix processing is only for testing
        self.readBs = int(readBsKb[:-1]) if readBsKb[-1] == 'b' else int(readBsKb) * 1024
        self.chunkSz = int(chunkSzKb[:-1]) if chunkSzKb[-1] == 'b' else int(chunkSzKb) * 1024
        if self.chunkSz % self.readBs:
            print(f'Chunk size({chunkSzKb}) must be a multiple of read block size({readBsKb})')
            raise SystemExit(1)

    def hash(self, inputP, progress_f):
        fullHash = self.Hash()
        chunkHash = self.Hash()
        chunkDigests = []
        pos = 0 # don't want to use f.tell()
        with open(inputP, 'rb') as inputF:
            for dataBlock in iter(lambda: inputF.read(self.readBs), b""):
                pos += len(dataBlock)
                progress_f(pos)
                fullHash.update(dataBlock)
                if self.chunkSz:
                    chunkHash.update(dataBlock)
                    if pos % self.chunkSz == 0:
                        chunkDigests.append(chunkHash.hexdigest())
                        chunkHash = self.Hash()

        fullDigest = fullHash.hexdigest()
        if not self.chunkSz:
            return fullDigest
        # trailing hash, the last dataBlock length is less than chunkSz
        if pos % self.chunkSz:
            chunkDigests.append(chunkHash.hexdigest())
        # One chunk digest which is equal to the full digest
        if len(chunkDigests) == 1:
            chunkDigests = []
        #
        if fullDigest in self.m:
            if self.m[fullDigest] != chunkDigests:
                print("Computed chunk digests don't match existing")
                print(f"File path: {inputP}")
                raise SystemError(1)
        else:
            self.m[fullDigest] = chunkDigests

        return fullDigest

    def save(self):
        tmp = Path(str(self.mP) + '.~tmp')
        tmp.write_bytes(json.dumps(self.m, indent=4).encode('utf-8'))
        tmp.rename(self.mP)

    def __del__(self):
        self.save()

if __name__ == '__main__':
    c = Chunker(sys.argv[1], sys.argv[2])
    for p in sys.argv[3:]:
        print(c.hash(p, lambda v: None))

