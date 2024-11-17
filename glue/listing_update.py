from common import *

dir = Path(sys.argv[1]).absolute()

cur = Path(dir, currentName)
apr = Path(dir, approvedName)

create_chunker_interactively_ifneeded(dir)

update_listing(dir)

if not apr.exists():
    copy_through_temporary(cur, apr)
    raise SystemExit(0)

# 2 - only renames, 3 - changes
code = run(sys.executable, compare_path, apr, cur, success_codes=[0,2,3])
if code != 0:
    print('-' * 50)
    while True:
        ans = input('Approve? (yes/no): ')
        if ans == 'no':
            break
        elif ans == 'yes':
            copy_through_temporary(cur, apr)
            break
