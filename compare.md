# Usage and Description

```
<listing_old> <listing_new>
```

Both arguments are paths to listings.

Compares two listings.
- keys not present in `<old>` will be shown as "Added"
- keys not present in `<new>` will be shown as "Removed"
- keys with differing values  will be shown as "Modified"

Keys in each group will be sorted.

If listings are identical, it will print "No changes" and the exit code will be `0`.<br>
If there were only renames, which is when the listings have the same values, it will print "Only renames" and the exit code will be `2`.<br>
Otherwise, the exit code will be `3`.


## Notes

The groups are ordered by the likelihood of happening, by outputting first "Added", then "Removed", then "Modified".<br>
This is because the user will kind of read the output upwards,
and without scrolling they will see only the end of the output.<br>
This allows infrequent types of changes to not get lost in the output.<br>
And the line with counts reverses the order, since it's a single line read from left to right.<br>
Though maybe I'm overthinking this... whatever.
