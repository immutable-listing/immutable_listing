# Usage and Description

```
<mapping> <read_bs_kb> <file>
```

`<mapping>` is a path to a file containing
```json
{
    "": {"hash": <hash_name>, "bs": <bs_kb>}
}
```
where `<hash_name>` is one of {sha256,blake3,xxhash32,xxhash64,xxhash128},<br>
and `<bs_kb>` is the chunk size in kilobytes.

`<read_bs_kb>` is the block size for reads in kilobytes.<br>
Must be a multiple of the chuck size.<br>
If zero, no chunk hashes will be calculated, and no new entry will be added to the mapping.

`<file>` is a file for which to calculate the hashes.

---

Calculates the hash of a file and of each chunk.<br>
The result is added to the mapping in the following form
```
{
    <file_digest>: [<chunk0_digest>, <chunk1_digest>, ...]
}
```
If there's only one chunk, the chunk array will be empty,
since that one chunk digest would be equal to the full digest.

If the file's digest is already present in the mapping,
the computed chunk array is compared against the existing one,
and if they differ, which would mean a hash collision, the process exits with an error.

# Dependencies

The module for a given hash function is loaded only when that function is used.<br>
- for sha256, the standard hashlib
- for blake3, package blake3
- for xxhash, package xxhash 

