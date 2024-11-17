
import os, sys
from pathlib import Path
from tests import run, assert_sorted_eq, json_load, execute_tests, unicode_string

tool_dir = Path(__file__).parent
cmd = [sys.executable, f'{tool_dir}/make.py']


def test_full():
    listing = Path('.listing')
    # # # Files in subdirectories
    # # # Unicode in filenames
    # # # Several files
    os.mkdir('sub')
    file = Path('sub', unicode_string)
    file.write_bytes(b'123')
    Path('f').write_bytes(b'111')
    expected = [f'sub/{file.name}', 'f']
    # # # Files starting with `.listing` are not listed
    Path('.listing_123').write_bytes(b'123')
    # # #
    run(*cmd, '.', listing)
    assert_sorted_eq(json_load(listing), expected)
    # # # No symlinks
    sln = Path('1s')
    sln.symlink_to(file)
    run(*cmd, '.', listing, out=f'Symbolic links are not supported: {sln.name}', code=1)
    os.remove(sln)
    # # # No hardlinks
    hln = Path('1h')
    hln.hardlink_to(file)
    run(*cmd, '.', listing, code=1, out_contains='Hard links are not supported')


execute_tests(globals().values())
