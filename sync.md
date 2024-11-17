# Usage and Description

```
<srcDir> <srcListing> <destDir> <destListing>
```

Updates files in `<destDir>` according to the differences in the listings,
such that upon completion `<srcListing>` could be used to work with `<destDir>`.

New files will be copied with their extended attributes, no guarantees regarding any other metadata.<br>
Those removed will be be renamed to `_not_in_listing/<value_in_listing>`, and their relative path will be stored in the extended attribute `user.last_path`.<br>
Only one file with the same hash is guaranteed to be reused (when files are being renamed).

If there exists an unlisted file in `<destDir>`
and one with the same path is listed in `<srcListing>`,
the program will exit with an error.
