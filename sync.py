import sys, json
from xattr import getxattr, listxattr, setxattr
from pathlib import Path
from progress import progress, print_item_progress


def sync(srcDir, srcListing, destDir, destListing, readBs):
    # Don't care about reusing several files with the same hash, thus use a 1 to 1 mapping.
    old = {}
    new = []
    notinlistingDir = Path(destDir, '_not_in_listing')

    notinlistingDir.mkdir(exist_ok=True)

    # Collect files that can be reused.
    # It's those that either don't exist in the source
    # or their value doesn't match that of the source.
    # (it means they've either been renamed or removed in the source).
    def addToReuse(p, v):
        dest = Path(destDir, p)
        # Files that will be left unused we want to leave for the possibility of archival,
        # for the user to deal with them manually.
        newP = Path(notinlistingDir, v)
        # This one is already unlisted.
        if dest == newP:
            old[v] = dest
            return
        # Set before renaming, in case we get terminated
        setxattr(dest, 'user.last_path', p.encode('utf-8'))
        # Need to remove existing, since `rename` could fail otherwise.
        # It's fine if we get terminated after removing it,
        # since `dest` has the same value.
        if newP.exists():
            newP.unlink()
        dest.rename(newP)
        old[v] = newP

    for p, v in destListing.items():
        if p not in srcListing:
            addToReuse(p, v)

    for p, srcV in srcListing.items():
        destV = destListing.get(p)
        if destV == srcV:
            continue
        new.append((p, srcV))
        if destV:
            addToReuse(p, destV)

    toCopy = []

    for p, srcV in new:
        dest = Path(destDir, p)
        if dest.exists():
            print(f"There's an existing file that's not listed: {dest}")
            raise SystemExit(1)
        dest.parent.mkdir(parents=True, exist_ok=True)
        oldP = old.pop(srcV, None)
        if oldP:
            oldP.rename(dest)
        else:
            src = Path(srcDir, p)
            toCopy.append((src,dest,src.stat().st_size))

    def f(item):
        src, dest, sz = item
        with src.open('rb') as srcF:
            with dest.open('wb') as destF:
                pos = 0
                while True:
                    data = srcF.read(readBs)
                    if not data:
                        break
                    destF.write(data)
                    pos += len(data)
                    print_item_progress(pos, sz)
        for attr in listxattr(src):
            setxattr(dest, attr, getxattr(src, attr))

    progress(toCopy, lambda v: v[2], f)


def main():
    readBs = int(sys.argv[1]) * 1024
    srcDir = Path(sys.argv[2])
    srcListingP = Path(sys.argv[3])
    destDir = Path(sys.argv[4])
    destListingP = Path(sys.argv[5])
    srcListing = json.loads(srcListingP.read_text('utf-8'))
    destListing = json.loads(destListingP.read_text('utf-8'))
    sync(srcDir, srcListing, destDir, destListing, readBs)


if __name__ == '__main__':
    main()

