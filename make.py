import json, sys, os

def make(dir):
    r = []
    for dpath, _dnames, fnames in os.walk(dir):
        for fname in fnames:
            p = dpath + '/' + fname
            rel = p[len(dir) + 1:] # +1 for the slash
            if rel.startswith('.listing'):
                continue
            if os.path.islink(p):
                print(f'Symbolic links are not supported: {rel}')
                raise SystemExit(1)
            if os.path.isfile(p):
                stat = os.stat(p)
                if stat.st_nlink > 1:
                    print(f'Hard links are not supported: {rel}')
                    raise SystemExit(1)
                r.append(rel)
    return r


def main():
    dir = os.path.abspath(sys.argv[1])
    outP = os.path.abspath(sys.argv[2])
    listing = make(dir)
    with open(outP, 'w', encoding='utf-8') as f:
        json.dump(listing, f, indent=4, ensure_ascii=False)

if __name__ == '__main__':
    main()

