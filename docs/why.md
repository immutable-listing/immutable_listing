This was created to understand how I want to do backups,
because none of the existing popular solutions made sense to me.<br>
Though I didn't search much,
since there are too many repositories matching the word "backup".<br>
Maybe there's a reason why I couldn't find anything similar,<br>
and my approach is wrong, and I'm blind as to why.<br>
Or maybe it's just another case of NIH.

My use case: the main folder is on an SSD that I constantly use,
the backup folder (a mirror of the main) is on an HDD that's used only for backup,
and before updating the backup I want to make sure
I didn't accidentally delete or move any files, or added things I shouldn't have;
and want to be able to do distributed backups,
i.e. segment, encrypt, and treat multiple hosts as a single storage.

Before creating this I simply copied and renamed everything manually.<br>
That is, I would perform `rsync --ignore-existing -rli <main> <backup>`
and manually do the renames and deletions in backup that I did in main.<br>
By looking at the `rsync` output I checked that there were no unwanted additions.<br>
Also, with a script I periodically checked that the sizes of files in main
match those in backup, which includes seeing if there are any added or removed files.
(a couple of times I caught a change caused by an epub reader).<br>
And of course a couple of times I computed the hashes to confirm that there are no differences.
