All of the tests were written before I started using this for my data.<br>
Every assertion is confirmed to check what it's supposed to.

Along with using this solution I'm still maintaining the manual backup(as described in `why.md`) on a separate disk.<br>
Every time I perform a backup (the manual and with this solution), which is at least once a day, I do the following:
- check with a script that both trees match, and the size of each file matches
- update the listing of the manual backup and compare it against the other

And at some point I'll do something like `find <dir> -type f -exec xxh128sum {} \; > sums`
for both directories and compare the `sums` files.<br>

That way it's unlikely that a bug will go unnoticed.<br>
Sure, it probably won't invoke the corner cases, but at least it's real usage.<br>
There are new files being added every day, and I quite frequently delete and move files/directories.<br>

I've been using this since 4-Nov-2024.<br>
(But realistically, one should only be concerned with how long it has been
since the last change in the source files)

I have yet to catch a bug.

When I'll encounter a serious problem, I'll document it right here.

Not sure when I'm going to stop maintaining the manual backup
and doing this constant checking.<br>
But after I stop, I'll definitely start doing this again when I change something in the sources.
