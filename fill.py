import sys, json, xattr
from pathlib import Path
from progress import progress, print_item_progress
from chunker_add import Chunker
from fill_dummy import Dummy

def getHash(hashObj, p, sz):
    def current_progress(processed):
        print_item_progress(processed, sz)

    r = hashObj.hash(p, current_progress)
    # ---
    if not r:
        print('Hash command returned no hash')
        raise SystemExit(1)
    # ---
    for c in r:
        if not c.isalnum():
            print('Hash string contains a non-alnum char: ', repr(c))
            print('Full string:', repr(r))
            raise SystemExit(1)
    return r

def fill(dir, listing, attrName, hashObj):
    r = {}
    toSet = []

    for rel in listing:
        p = Path(dir, rel)
        sz = p.stat().st_size
        v = f'{sz}~'
        if attrName in xattr.listxattr(p):
            v += xattr.getxattr(p, attrName).decode('ascii')
        else:
            toSet.append((rel, p, sz))
        r[rel] = v

    def f(item):
        rel, p, sz = item
        val = getHash(hashObj, p, sz)
        xattr.setxattr(p, attrName, val.encode('ascii'))
        r[rel] += val

    progress(toSet, lambda v: v[2], f)

    return r

def main():
    dir = Path(sys.argv[1]).absolute()
    listingP = Path(sys.argv[2]).absolute()
    attrName = 'user.' + sys.argv[3]
    hashClassName = sys.argv[4]
    hashArgs = sys.argv[5:]

    listing = json.loads(listingP.read_text('utf-8'))
    hashClass = {'chunker': Chunker, 'dummy': Dummy}[hashClassName]
    hashObj = hashClass(*hashArgs)
    listing = fill(dir, listing, attrName, hashObj)

    listingP.write_bytes(
        json.dumps(listing, indent=4, ensure_ascii=False).encode('utf-8')
    )

if __name__ == '__main__':
    main()

