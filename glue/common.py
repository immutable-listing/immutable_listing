import os, subprocess, sys, json
from pathlib import Path

read_bs = int(os.environ.get('read_bs', 128)) # in KB
print('read_bs =', read_bs, 'KB')
listing_suffix = os.environ.get('listing_suffix', '')
if listing_suffix:
    print('listing_suffix =', repr(listing_suffix))
    listing_suffix = '_' + listing_suffix
attr_suffix = os.environ.get('attr_suffix', '')
if attr_suffix:
    print('attr_suffix =', repr(attr_suffix))
    attr_suffix = '_' + attr_suffix

currentName = '.listing_current' + listing_suffix
approvedName = '.listing_approved' + listing_suffix
chunkerMappingName = '.listing_chunker' + listing_suffix

tool_dir = os.path.abspath(os.path.dirname(__file__) + '/..')
make_path = tool_dir + '/make.py'
sync_path = tool_dir + '/sync.py'
fill_path = tool_dir + '/fill.py'
sync_path = tool_dir + '/sync.py'
compare_path = tool_dir + '/compare.py'
compare_renames_path = tool_dir + '/compare_only_renames.py'

def copy_through_temporary(src, dest):
    tmp = Path(str(dest) + '~tmp')
    tmp.write_bytes(src.read_bytes())
    tmp.rename(dest)

def json_load(p: Path):
    return json.loads(p.read_text('utf-8'))

def run(*cmd, success_codes=[0]):
    cmd = list(map(str, cmd))
    r = subprocess.run(cmd)
    if r.returncode not in success_codes:
        print('Command failed:', cmd)
        raise SystemExit(1)
    return r.returncode

def create_chunker_interactively_ifneeded(dir):
    chunker = Path(dir, chunkerMappingName)
    if chunker.exists():
        return
    print("No chunker mapping exists. Let's create one.")
    print("You'll need to choose what hash function to use and the chunk size.")
    print()
    hashName = input("Hash (sha256,blake3,xxhash32,xxhash64,xxhash128): ")
    chunkSz = input("Chunk size (in KB): ")
    chunker.write_bytes(
        json.dumps({"": {"hash": hashName, "bs": chunkSz}}).encode('utf-8')
    )

def fill(dir):
    attrName = get_chunker_hash(Path(dir, chunkerMappingName)) + attr_suffix
    assert(attrName)
    run(sys.executable, fill_path,
        dir, f'{dir}/{currentName}',
        attrName,
        'chunker', f'{dir}/{chunkerMappingName}', read_bs,
    )

def make(dir):
    run(sys.executable, make_path, dir, f'{dir}/{currentName}')

def update_listing(dir):
    make(dir)
    fill(dir)

def get_chunker_hash(chunker):
    return json_load(chunker)[""]["hash"]

