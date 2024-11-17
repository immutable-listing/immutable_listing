## Only regular files are supported
Because nothing more is needed.

Hard links are hard to deal with, both for the user and programmer.

Symbolic links are useless, because they don't allow to freely move files around.

Empty directories are not needed.

## Timestamps and permission are not preserved

To me, timestamps are relevant only for recently added files.

Permissions can be set ad hoc manually or with a script.

## With file segmentation in mind
That is, if you need segmentation,
the chunk hashes must be calculated at the time the full hash is being calculated,
to not waste time calculating them separately,
since IO is likely to be the bottleneck.

While also not forcing this.

