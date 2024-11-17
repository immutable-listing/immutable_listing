# Usage and Description
```
<dir> <out_file>
```

Makes a json list of relative file paths in `<dir>`.

Paths starting with `.listing` are ignored.

If symbolic or hard links are encountered, the program will exit with an error.

If the program doesn't exit successfully, `<out_file>` is NOT guaranteed to have valid contents.

