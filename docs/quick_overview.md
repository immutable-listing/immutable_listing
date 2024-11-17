
Everything revolves around the listing file.<br>
It's merely a json mapping of relative file paths to their size and hash.

Here's a demonstration of the glue scripts.

```shell
mkdir main backup
echo 1 > main/1
echo 12 > main/2
# This will ask for a hash function name and chunk size.
# Here we choose zero chunk size to opt out
# from computing hashes of chunks.
echo 'sha256\n0' | python glue/listing_update.py main
python glue/listing_backup.py main backup
cat backup/1 backup/2 # outputs '1', '12'
mv main/1 main/f1
mv main/2 main/f2
echo 123 > main/3
# Since there are changes, it will ask to approve the current listing
echo 'yes' | python glue/listing_update.py main
# demonstrate that source files are not accessed when syncing renames
rm main/f1 main/f2
python glue/listing_backup.py main backup
cat backup/f1 backup/f2 backup/3 # outputs '1', '12', '123'
```

The `glue` folder contains scripts for a specific workflow that fits my needs. (see `glue/README.md`)

Here's basically what `listing_update.py` would do, if you chose sha256 as your hash function and the chunk size to be 8MB.

```shell
python make.py main main/.listing_current
echo '{"": {"hash": "sha256", "bs": 8192}}' > main/.listing_chunker
python fill.py main main/.listing_current sha256 chunker main/.listing_chunker 128
# <compare current with approved and ask for confirmation>
# if confirmed, approve current listing by copying
cp main/.listing_current main/.listing_approved
```

And `listing_backup.py`

```shell
# <exit if main's current and approved listings aren't equal>
cp main/.listing_chunker backup/
python make.py backup backup/.listing_current
python fill.py main main/.listing_current sha256 chunker main/.listing_chunker 128
python sync.py main main/.listing_current backup backup/.listing_current
cp main/.listing_approved backup/
```

For information about each tool see the corresponding `.md` files.
(e.g., `fill.md`)

Only `make` and `fill` are the basis of the solution.<br>
`sync` is just one of the ways to maintain a backup.

The chunker, as it should be apparent, is separate as well,
a puzzle piece for another way of maintaining a backup.<br>
This segmentation part can very well be done separately from `fill`.

Even if you don't intend on using segmentation,
you still might want to make the chunk size non-zero,
because that will allow you to catch hash collisions (see `chunker_add.md`),
which allows to try a hash function like xxhash32 without much worry.

