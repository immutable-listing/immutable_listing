import subprocess, json, os, shutil
from pathlib import Path

def run(*args, code = 0, input=b'', out = '', out_exact='', out_contains='', out_lastline=''):
    args = list(map(str, args))
    r = subprocess.run(args, capture_output=True, input=str(input).encode('utf-8'))
    rout = r.stdout.decode('utf-8')
    stderr = r.stderr.decode('utf-8')
    #
    if r.returncode != code:
        print(f'Expected code: {code}')
        print(f'Got:           {r.returncode}')
        line = '='*20
        print(line, 'STDOUT', line)
        print(rout)
        print(line, 'STDERR', line)
        print(stderr)
        print('=' * 48)
        raise Exception('Unexpected exit code')
    # this indicates that the caller wants to deal with the output themselves
    if out is None:
        return rout
    if out_contains:
        if out_contains in rout:
            return None
        print('Expected to be in output: ' + repr(out_contains))
        print('Stdout                  : ' + repr(rout))
        if stderr:
            print('Stderr:\n--------\n' + stderr + '----------\n')
        raise Exception("Output doesn't start with expected string")
    if out_lastline:
        got = rout.splitlines(True)[-1]
        out_lastline += '\n'
        if got == out_lastline:
            return None
        print('Expected last line o be: ' + repr(out_lastline))
        print('Output:                : ' + repr(got))
        if stderr:
            print('Stderr:\n--------\n' + stderr + '----------\n')
        raise Exception("Output's last line not equal to expected")
    if out:
        out_exact = out + '\n'
    #
    if rout == out_exact:
        return None
    print('Expected output: ' + repr(out_exact))
    print('Got:             ' + repr(rout))
    if stderr:
        print('Stderr:\n--------\n' + stderr + '----------\n')
    raise Exception("Output not equal expected")

def json_load(fname):
    with open(fname, 'r', encoding='utf-8') as f:
        return json.load(f)

def json_save(fname, obj):
    with open(fname, 'w', encoding='utf-8') as f:
        json.dump(obj, f)

def assert_dict_eq(a, b):
    if sorted(a.items()) != sorted(b.items()):
        print('a:', json.dumps(a, ensure_ascii=False, indent=4))
        print('b:', json.dumps(b, ensure_ascii=False, indent=4))
        raise Exception('Dicts are not equal')

def assert_sorted_eq(a, b):
    assert_eq(sorted(a), sorted(b))

def assert_eq(a, b):
    if a != b:
        print('a:', repr(a))
        print('b:', repr(b))
        raise Exception('Values are not equal')

def assert_startswith(s, sub):
    if not s.startswith(sub):
        print('str:', repr(s))
        print('sub:', repr(sub))
        raise Exception('String does not start with')


def execute_tests(objs):
    test_dir = Path('test_dir').absolute()
    base_prefix = 'test_'
    test_fs = []
    for obj in objs:
        if callable(obj) and getattr(obj, '__name__', '').startswith(base_prefix):
            test_fs.append(obj)
    for f in test_fs:
        print(f.__name__)
        #
        os.chdir(test_dir.parent)
        if test_dir.exists():
            shutil.rmtree(test_dir)
        test_dir.mkdir()
        os.chdir(test_dir)
        #
        f()

    assert(test_fs)
    print('Number of tests:', len(test_fs))
    shutil.rmtree(test_dir)


unicode_string = (
    '\u043e\u0434\u0438\u043d,'
    '\u4e8c,'
    '\u03c4\u03c1\u03af\u03b1,'
    '\u0e2a\u0e32\u0e21'
)
