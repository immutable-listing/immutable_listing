
These are scripts that put the pieces together in a way that fits my needs.

There are the following files:
- `.listing_current`, this listing is used when updating
- `.listing_approved` contains the last "good" listing
- `.listing_chunker` is a chunker mapping (see `chunker_add.md`)

Every command that updates the current listing will interactively create the chunker mapping,
if it doesn't already exist.

For every command you can set an option through an environment variable.
- `read_bs` is the read block size in kilobytes to pass to every command that accepts it.<br>
  The default is `128`.
- `listing_suffix` is a suffix to use for every `.listing` file.<br>
  When specified, an underscore will be added. E.g., `.listing_current_<suffix>`
- `attr_suffix` is a suffix to use for the attribute name for the fill command.<br>
  When specified, an underscore will be added. E.g., `sha256_<suffix>`

### Examples:<br>
Use a 64KB block size for reading files in backup to calculate the hashes, and for copying files from main
```shell
read_bs=64 python listing_backup.py main backup
```
Recalculate all the hashes and compare against approved.
That is, make sure none of the files have changed.
```shell
attr_suffix=2 python listing_update.py main
# after making sure everything is ok, remove the now unneeded attribute
python remove_xattrs.py main sha256_2
```
Try a different hash function separately from the default listing
```shell
listing_suffix=xxhash32 python listing_update.py main
```

## listing_update
```
<dir>
```
Updates the current listing.<br>
If the approved listing doesn't exist, it becomes a copy of the current.<br>
Otherwise, the current and approved are compared(see `compare.md`)
and, if there are changes, the user is prompted to approve the current listing.

## listing_backup
```
<source_dir> <dest_dir>
```
Copies the chunker mapping from `<source>` to `<dest>`.<br>
Updates the current listing in `<dest>`.<br>
Executes `sync.py`.<br>
Copies approved listing from `<source>` to `<dest>`.

It's important to note that after performing this
the current listing in `<dest>` will become invalid.<br>
And even if it were kept up-to-date, it's likely to not be equal to the approved listing,
since the current listing would include "removed" files located in `_not_in_listing`.
