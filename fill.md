# Usage and Description

```
<dir> <listing> <xattr> <hash_cmd...>
```

`<dir>` is the directory to which files in `<listing>` are relative.

`<listing>` is in the format as produced by the `make` command.

`<xattr>` denotes a name of an extended attribute [`"user.<xattr>"`] that will be used for retrieving and storing the hash of a file.

`<hash_cmd...>` is several strings that denote which class to use for getting the hashes
and the arguments to pass to it when initializing.<br>
For the `chunker` class see `chunker_add.md`.

---

The result will be stored in `<listing>` in the following form
```
{
    "<rel_path>": "<size>~<hash>",
    ...
}
```

For a given path, if `"user.<xattr>"` attribute exists, its value will be used as the hash.<br>
Otherwise the hash will be determined with `<hash_cmd>`.

If the program doesn't exit with successfully, `<listing>` is NOT guaranteed to have valid contents.

# Notes

Initially, <hash_cmd...> specified an actual command to be invoked by starting a process.<br>
And after realizing that the chunker command took too much time saving its mapping file
I even made it to create the process only one time by communicating each file name through _stdin_
and this still allowed the command to communicate the progress for each file through _stdout_,
and it was fairly simple.<br>
But the overhead was still too big when processing many small files. For some reason, most of the time was being spent waiting on _stdin_ by the command for the next file path.<br>
Though it's still possible to add a class for executing a command.