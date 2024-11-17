
import os, sys
from pathlib import Path
from tests import run, assert_dict_eq, json_load, json_save, execute_tests, unicode_string

tool_dir = Path(__file__).parent
cmd = [sys.executable, f'{tool_dir}/fill.py']
dummy_cmd = ['dummy']

def test_catch_hash_command_failures():
    Path('f').touch()
    listing = Path('listing')
    json_save(listing, ['f'])
    # # # Catch hash command invalid output
    run(*cmd, '.', listing, 'dummyfail', *dummy_cmd, 'invalid char', code=1,
        out_contains='Hash string contains a non-alnum char'
    )
    # # # Catch hash command failure
    run(*cmd, '.', listing, 'dummyfail', *dummy_cmd, 'fail', code=1)
    # # # Catch hash command empty output
    run(*cmd, '.', listing, 'dummyfail', *dummy_cmd, '', code=1, out='Hash command returned no hash')

def test_basic():
    # # # Files in subdirectories
    # # # Unicode in filenames
    os.mkdir('sub')
    file = Path('sub', unicode_string)
    file.write_bytes(b'123')
    listing = Path('listing')
    mBase = [ f'sub/{file.name}' ]
    mResult = {str(file): '3~hashof123'}
    # # #
    json_save(listing, mBase)
    run(*cmd, '.', listing, 'dummy', *dummy_cmd, out=None) # ignore output
    assert_dict_eq(json_load(listing), mResult)
    # # # Rerun shouldn't do anything
    run(*cmd, '.', listing, 'dummy', *dummy_cmd)
    assert_dict_eq(json_load(listing), mResult)
    # # # Rerun without hashes in the listing should use cached(xattr) values
    json_save(listing, mBase)
    # with a failing command, to ensure no invocation
    run(*cmd, '.', listing, 'dummy', *dummy_cmd, 'fail')
    assert_dict_eq(json_load(listing), mResult)

def test_zero():
    Path('f').touch()
    listing = Path('listing')
    # # # Zero size in total doesn't fail
    json_save(listing, ['f'])
    run(*cmd, '', listing, 'dummy', *dummy_cmd, out=None)

# # #
# Make sure "every" number of items gets processed.
# This is needed in case there's special ordering
# that might accidentally leave out some items.
# # #
def test_several():
    listing = Path('listing')
    Path('1').write_text('1', 'utf-8')
    # Might be a good idea to temporarily test with a bigger number
    # when changing something related to ordering.
    max_files = 7 # why 7? Not too few, not too many to slow down testing
    for N in range(1, max_files):
        m = []
        mResult = {}
        for n in range(1, N+1):
            ns = str(n)
            content = '1' * n
            Path(ns).write_text(content, 'utf-8')
            m.append(ns)
            mResult[ns] = ns + '~hashof' + content
        json_save(listing, m)
        run(*cmd, '.', listing, 'dummy', *dummy_cmd, out=None)
        assert_dict_eq(json_load(listing), mResult)
        # need to remove to get rid of attributes
        for n in range(1, N+1):
            Path(str(n)).unlink()


execute_tests(globals().values())

