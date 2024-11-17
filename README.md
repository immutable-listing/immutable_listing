No idea whether this will be useful to anyone, maybe to a "control freak" who can program and will fully examine the sources.<br>
I'm using this every day, and don't see myself switching to anything else ever.

This whole thing, including most of the documentation, was written strictly for personal use.<br>
But I figured, why not make it public, maybe it'll be useful to someone.

Forgive my English, if there are any mistakes or oddities, as I haven't had much practice.<br>
Patches with corrections are welcome.

## Description

This a set of tools for backing up and keeping track of **IMMUTABLE** files in a simple
[to implement, test, use and understand] way.

The main, and currently the only, way of backing up files is to simply maintain
a mirror of your directory.<br>
The tracking aspect is checking what's changed in your directory (without even involving a backup).

What makes all of this possible is using extended file attributes to store the hashes.

Cloud backup with encryption and segmentation is possible,<br>
though it's not yet implemented due to the lack of immediate need.

Abrupt termination of execution must not create problems.

## How I use this

I have a script that looks like this (with paths simplified)
```shell
main='/mnt/main/immutable'
backup='/mnt/backup/immutable'
python glue/listing_update.py $main
python glue/listing_backup.py $main $backup
```
When running for the first time on `$main`, initialization will be performed.<br>
Subsequent runs will show the changes, ask to approve them, and apply them to `$backup`.

## [A quick overview](docs/quick_overview.md)

## [Why](docs/why.md)

## [Decisions](docs/decisions.md)

## [Regarding testing](docs/testing.md)

## [Reliability](docs/reliability.md)

## [Somewhat accurate ETA](docs/eta.md)

## Requirements

python3<br>
xattr (pip package)<br>
optional pip packages for non-standard hash functions (see `chunker_add.md`)

## Supported platforms

Whatever `xattr` supports should work (Linux, MacOS, FreeBSD[?]).<br>
Obviously, the filesystem in question must have extended attribute support.

Windows support can be added easily, since extended attributes on NTFS are accessed like files (Alternate Data Streams).
```
echo value > file:myattr
more < file:myattr
```
And no need to list the attributes to check if a particular one exists, just check whether that path exists.

## If you're interested

You can open an issue, or contact me at immutable_listing@tuta.io









