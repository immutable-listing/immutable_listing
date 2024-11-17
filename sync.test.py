import sys, os, stat
from xattr import getxattr, setxattr
from pathlib import Path
from tests import (
    run, execute_tests, json_save, json_load,
    assert_eq, assert_dict_eq, unicode_string,
)

tool_dir = Path(__file__).parent
cmd = [sys.executable, f'{tool_dir}/sync.py', 128]

def get_dir_contents(dir):
    return {
        str(p.relative_to(dir)): p.read_text('utf-8')
        for p in dir.rglob('*')
        if p.is_file() and not p.name.startswith('.listing')
    }

def create(dir, files, listingP):
    dir.mkdir()
    for p, v in files.items():
        src = Path(dir, p)
        src.parent.mkdir(parents=True, exist_ok=True)
        src.write_text(v, 'utf-8')
        setxattr(src, 'user.value', v.encode('ascii'))
    json_save(listingP, files)

def chmod(d, ps, m):
    for p in ps:
        Path(d, p).chmod(m)

def test(srcFiles, destFiles={}, expectedNewDestFiles={},
         onBeforeRun=lambda: None, onAfterRun=lambda: None
):
    srcDir = Path('src')
    destDir = Path('dest')
    srcListing = Path(srcDir, '.listing')
    destListing = Path(destDir, '.listing')
    # create files and fill the listings
    create(srcDir, srcFiles, srcListing)
    create(destDir, destFiles, destListing)

    onBeforeRun()
    run(*cmd, srcDir, srcListing, destDir, destListing, out=None) # ignore output
    onAfterRun()

    # # # Destination listing is unchanged (because we sync only files)
    assert_dict_eq(json_load(destListing), destFiles)

    for p, v in srcFiles.items():
        src = Path(srcDir, p)
        dest = Path(destDir, p)
        # # # Destination attributes must match the source
        da = getxattr(dest, 'user.value').decode('ascii')
        assert_eq(da, v)
        # # # Source attributes are still the same
        sa = getxattr(src, 'user.value').decode('ascii')
        assert_eq(sa, v)

    # # # Source files are unchanged and there are no new/removed files
    assert_eq(get_dir_contents(srcDir), srcFiles)

    destFilesNew = {**srcFiles, **expectedNewDestFiles}

    # # # No unexpected files in the destination and the contents are correct
    assert_eq(get_dir_contents(destDir), destFilesNew)

    # # # Rerunning with an up-to-date destination listing shouldn't do anything
    json_save(destListing, destFilesNew)
    # remove privileges
    chmod(srcDir, srcFiles.keys(), 0)
    chmod(destDir, destFilesNew.keys(), 0)
    #
    run(*cmd, srcDir, srcListing, destDir, destListing)
    # give back privileges
    chmod(srcDir, srcFiles.keys(), stat.S_IRUSR)
    chmod(destDir, destFilesNew.keys(), stat.S_IRUSR)



# # # Unicode in filenames
# # # Add a file to a new directory, multiple nesting
def test_add():
    test(
        srcFiles={f'not/indest/{unicode_string}': '1'},
    )

def test_remove():
    test(
        srcFiles={},
        destFiles={'sub/1': 'one'},
        expectedNewDestFiles={'_not_in_listing/one': 'one'},
    )
    # # # Last known path is saved for removed files
    assert_eq(getxattr('dest/_not_in_listing/one', 'user.last_path'), b'sub/1')

# # # Move file to a new directory, multiple nesting
def test_rename():
    test(
        srcFiles={'not/indest/1': '1'},
        destFiles={'1': '1'},
    )

def test_replace():
    test(
        srcFiles={'1': '1new'},
        destFiles={'1': '1'},
        expectedNewDestFiles={'_not_in_listing/1': '1'},
    )

def test_swap():
    # # # Files are be renamed and not copied from source.
    # Remove privileges to make sure the source files are not copied
    def beforerun():
        os.chmod('src/1', 0)
        os.chmod('src/2', 0)
    # give back privileges for further checks
    def afterrun():
        os.chmod('src/1', stat.S_IRUSR)
        os.chmod('src/2', stat.S_IRUSR)

    test(
        srcFiles={
            '1': '1',
            '2': '12',
        },
        destFiles={
            '1': '12',
            '2': '1',
        },
        onBeforeRun=beforerun,
        onAfterRun=afterrun,
    )

# Make sure files at destination get reused only once
def test_rename_and_duplicate():
    test(
        srcFiles={
            '1dup2': '1',
            '1dup': '1',
        },
        destFiles={
            '1': '1',
        },
    )

def test_collision_due_to_invalid_listing():
    srcDir = Path('src')
    srcDir.mkdir()
    destDir = Path('dest')
    destDir.mkdir()
    Path(srcDir, '1').write_bytes(b'one')
    Path(destDir, '1').write_bytes(b'one')
    srcListing = Path(srcDir, '.listing')
    destListing = Path(destDir, '.listing')
    json_save(srcListing, {'1': 'one'})
    json_save(destListing, {})
    run(*cmd, srcDir, srcListing, destDir, destListing, code=1, out=None) # ignore output


execute_tests(globals().values())
