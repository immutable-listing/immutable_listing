
import sys, xattr, os

dir = sys.argv[1]
names = sys.argv[2:]

if not names:
    print('Must specify which attribute to remove')
    raise SystemExit(1)

names = [ 'user.'+e for e in names ]

for dp, dps, fps in os.walk(dir):
    for fp in fps:
        p = dp + '/' + fp
        for a in xattr.listxattr(p):
            if a in names:
                xattr.removexattr(p, a)

