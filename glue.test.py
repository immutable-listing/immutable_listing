import sys
from pathlib import Path
from tests import run, assert_eq, execute_tests

glue_dir = Path(Path(__file__).parent, 'glue')


def test_():
    Path('main').mkdir()
    Path('backup').mkdir()
    mf1 = Path('main/1')
    mf1.write_bytes(b'1')
    run(sys.executable, f'{glue_dir}/listing_update.py', 'main', input='sha256\n0', out=None)
    run(sys.executable, f'{glue_dir}/listing_backup.py', 'main', 'backup', out=None)
    assert_eq(Path('backup/1').read_bytes(), b'1')
    # # #
    mf1.unlink()
    mf1.write_bytes(b'2')
    run(sys.executable, f'{glue_dir}/listing_update.py', 'main', input='yes', out=None)
    run(sys.executable, f'{glue_dir}/listing_backup.py', 'main', 'backup', out=None)
    assert_eq(Path('backup/1').read_bytes(), b'2')



execute_tests(globals().values())
