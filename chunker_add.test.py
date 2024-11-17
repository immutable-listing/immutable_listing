
import sys, hashlib
from pathlib import Path
from tests import run, assert_dict_eq, json_load, json_save, execute_tests, unicode_string

tool_dir = Path(__file__).parent
cmd = [sys.executable, f'{tool_dir}/chunker_add.py']
readBsKb = 128
chunkSzKb = 512
chunkSzB = chunkSzKb * 1024

def singlefile_test(data, hashName, digest, chunkDigests, name=None):
    p = Path('f' if name is None else name)
    p.write_bytes(data)
    m = { '': {'hash': hashName, 'bs': chunkSzKb} }
    json_save('chunker', m)
    run(*cmd, 'chunker', readBsKb, p, out_lastline=digest)
    m[digest] = chunkDigests
    assert_dict_eq(m, json_load('chunker'))

# # # Unicode in filename
# # # Zero-size file
def test_basic():
    singlefile_test(b'', 'sha256',
        'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', [],
        name = unicode_string
    )

# # # Data that fits in one chunk, less than chunkSzB, non-zero size
def test_unsplittable():
    singlefile_test(b'123', 'sha256',
        'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3', []
    )

# # # Data that fits in several chunks, the last chunk is equal to chunkSzB
def test_splittable_divisible():
    data = b'1' * chunkSzB + b'2' * chunkSzB
    singlefile_test(data, 'sha256',
        hashlib.sha256(data).hexdigest(),
        [hashlib.sha256(data[:chunkSzB]).hexdigest(), hashlib.sha256(data[chunkSzB:]).hexdigest()]
    )

# # # Data that fits in several chunks, the last chunk is less than chunkSzB
def test_splittable_indivisible():
    data = b'1' * chunkSzB + b'2' * (chunkSzB - 1)
    singlefile_test(data, 'sha256',
        hashlib.sha256(data).hexdigest(),
        [hashlib.sha256(data[:chunkSzB]).hexdigest(), hashlib.sha256(data[chunkSzB:]).hexdigest()]
    )

# # # Error when chunkSz is not a multiple of readBs
def test_chunksz_error():
    Path('f').touch()
    json_save('chunker', {'': {'hash': 'sha256', 'bs': 2048}})
    run(*cmd, 'chunker', 4096, 'f', code=1,
        out='Chunk size(2048) must be a multiple of read block size(4096)'
    )

# # # Chunk size equal to zero
def test_chunksz_zero():
    Path('f').touch()
    m = { '': {'hash': 'sha256', 'bs': 0} }
    json_save('chunker', m)
    digest = 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'
    run(*cmd, 'chunker', readBsKb, 'f', out_lastline=digest)
    # # # The mapping didn't change
    assert_dict_eq(m, json_load('chunker'))

def test_collision():
    b1 = ('d131dd02c5e6eec4693d9a0698aff95c2fcab58712467eab4004583eb8fb7f89'
          '55ad340609f4b30283e488832571415a085125e8f7cdc99fd91dbdf280373c5b'
          'd8823e3156348f5bae6dacd436c919c6dd53e2b487da03fd02396306d248cda0'
          'e99f33420f577ee8ce54b67080a80d1ec69821bcb6a8839396f9652b6ff72a70')
    b2 = ('d131dd02c5e6eec4693d9a0698aff95c2fcab50712467eab4004583eb8fb7f89'
          '55ad340609f4b30283e4888325f1415a085125e8f7cdc99fd91dbd7280373c5b'
          'd8823e3156348f5bae6dacd436c919c6dd53e23487da03fd02396306d248cda0'
          'e99f33420f577ee8ce54b67080280d1ec69821bcb6a8839396f965ab6ff72a70')
    Path('1').write_bytes(bytes.fromhex(b1))
    Path('2').write_bytes(bytes.fromhex(b2))
    digest = '79054025255fb1a26e4bc422aef54eb4'
    m = { '': {'hash': 'md5', 'bs': '64b'} }
    json_save('chunker', m)
    out = (
        f"{digest}\n"
        "Computed chunk digests don't match existing\n"
        "File path: 2"
    )
    run(*cmd, 'chunker', '64b', '1', '2', code=1, out=out)

# # # Unsupported hash
def test_unsupported_hash():
    json_save('chunker', { '': {'hash': 'nohash', 'bs': 1024} })
    run(*cmd, 'chunker', 1024, 'f', code=1, out='Unsupported hash name: "nohash"')
    # # # Errors don't erase the listing
    assert(Path('chunker').stat().st_size != 0)


#--------------------- OPTIONAL --------------------------

# # # BLAKE3
def test_blake3():
    singlefile_test(b'123', 'blake3',
        'b3d4f8803f7e24b8f389b072e75477cdbcfbe074080fb5e500e53e26e054158e', [],
    )

# # # XXHASH32
def test_xxhash32():
    singlefile_test(b'123', 'xxhash32',
        'b6855437', [],
    )

# # # XXHASH64
def test_xxhash64():
    singlefile_test(b'123', 'xxhash64',
        '3c697d223fa7e885', [],
    )

# # # XXHASH128
def test_xxhash128():
    singlefile_test(b'123', 'xxhash128',
        '0e45f72b026d434f404a763b3f4c8c9a', [],
    )


execute_tests(globals().values())

# # # The mapping file must not become invalid upon abrupt termination (use a temporary file)

