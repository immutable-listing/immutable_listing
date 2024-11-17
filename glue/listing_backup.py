from common import *

srcDir = Path(sys.argv[1]).absolute()
destDir = Path(sys.argv[2]).absolute()

if not destDir.exists():
    print(f"Directory doesn't exist: {destDir}")
    raise SystemExit(1)
    
srcCurrentL = Path(srcDir, currentName)
srcApprovedL = Path(srcDir, approvedName)
srcChunker = Path(srcDir, chunkerMappingName)

destCurrentL = Path(destDir, currentName)
destApprovedL = Path(destDir, approvedName)
destChunker = Path(destDir, chunkerMappingName)

if not srcApprovedL.exists() or srcCurrentL.read_bytes() != srcApprovedL.read_bytes():
    print("Current source listing doesn't match approved")
    raise SystemExit(1)


copy_through_temporary(srcChunker, destChunker)

print('Updating backup listing')
update_listing(destDir)

print('Syncing')
run(sys.executable, sync_path, read_bs, srcDir, srcApprovedL, destDir, destCurrentL)

copy_through_temporary(srcApprovedL, destApprovedL)
