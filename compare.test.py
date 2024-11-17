
from tests import json_save, execute_tests, run, unicode_string
from pathlib import Path
import sys

tool_dir = Path(__file__).parent
cmd = [sys.executable, f'{tool_dir}/compare.py']


def test_basic():
    expected_out = '''
Added:
    4
    5
Removed:
    0
    3
Modified:
    1
        -one
        +ONE
    2
        -two
        +TWO
Modified 2, Removed 2, Added 2
'''[1:-1]
    # # # Unicode in filenames
    oldP = unicode_string + '_old'
    newP = unicode_string + '_new'
    # # # Output must be sorted, so make input unsorted
    json_save(oldP, {'2': 'two', '3': 'three', '1':'one', '0': 'zero'})
    json_save(newP, {'5': 'five', '2': 'TWO', '1':'ONE', '4': 'four'})
    run(*cmd, oldP, newP, code=3, out=expected_out)

def test_no_changes():
    json_save('old', {'1':'one', '3': 'three'})
    json_save('new', {'3': 'three', '1':'one'})
    run(*cmd, 'old', 'new', code=0, out='No changes')

def test_renames():
    expected_out = '''
Added:
    2
Removed:
    3
Modified:
    1
        -one
        +three
Modified 1, Removed 1, Added 1
Only renames
'''[1:-1]
    json_save('old', {'1':'one', '3': 'three'})
    json_save('new', {'2':'one', '1': 'three'})
    run(*cmd, 'old', 'new', code=2, out=expected_out)


execute_tests(globals().values())

