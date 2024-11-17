Almost forgot to write about the progress indication.

The files are grouped by their size, and are ordered
by alternating between files from each group.<br>
Additionally, files are sorted by size in ascending order
for the ETA to represent the worst-case scenario.<br>
The ETA is calculated by using average speed and remaining size of each group.
```
ETA = (group0_remaining / group0_speed) + (group1_remaining / group1_speed) + ...
```

Don't know if this kind of ETA calculation is used anywhere else,
or if there's a better method.<br>
This approach seemed like the obvious solution to the problem.<br>
And I see no way to improve it; anything more would probably be an overcomplication
that will have its own downsides.

Here's how the progress indication looks.<br>
`<total_size_done> % | <file_size> | <file_duration> | <file_speed> | ETA`

```
 0.00 % |    7.6 KB |  0.35 ms |    21 MB/s | ETA not ready
 0.20 % |    7.2 MB |    21 ms | 341.5 MB/s | ETA not ready
 0.82 % |   23.1 MB |    59 ms | 389.2 MB/s | ETA not ready
29.87 % |      1 GB |  2.3 sec | 461.2 MB/s | ETA 6 sec
29.87 % |     152 B |     1 ms |   103 KB/s | ETA 6 sec
29.97 % |    3.8 MB |    11 ms | 349.9 MB/s | ETA 6 sec
30.50 % |   19.3 MB |    50 ms | 387.5 MB/s | ETA 6 sec
97.24 % |    2.4 GB |  6.0 sec | 409.9 MB/s | ETA 265 ms
97.24 % |    1002 B |  0.28 ms |   3.5 MB/s | ETA 265 ms
97.48 % |    8.9 MB |    25 ms | 348.2 MB/s | ETA 239 ms
98.23 % |   27.6 MB |    67 ms | 410.4 MB/s | ETA 165 ms
98.23 % |      1 KB |     1 ms | 846.9 KB/s | ETA 165 ms
98.29 % |    2.2 MB |     7 ms | 308.2 MB/s | ETA 158 ms
98.73 % |   16.2 MB |    44 ms | 367.5 MB/s | ETA 119 ms
99.36 % |     23 MB |    57 ms | 405.9 MB/s | ETA 60 ms
100.00 % |   23.6 MB |    57 ms | 413.4 MB/s | ETA 0 ms

     range       | files |   size   |  time  |   speed   
---------------------------------------------------------
0 - 10 KB        |     4 |   9.8 KB |   3 ms |   2.9 MB/s
1 MB - 10 MB     |     4 |  22.1 MB |  65 ms | 341.8 MB/s
10 MB - 100 MB   |     6 | 132.8 MB | 334 ms | 397.3 MB/s
larger than 1 GB |     2 |   3.4 GB |  8 sec | 424.2 MB/s

total size: 3.6 GB
total duration: 9 sec
```

Progress for the file being currently processed is displayed like so.
```
current (2.4 GB) 68 %
``` 
There's noticeable overhead from printing current progress, because it's updated after reading each block.<br>
110 ms to update it 8192 times (128KB * 8192 = 1GB).<br>
But since the read speed of my drive is 500MB/s, the overhead is kind of negligible (~50 ms for every second (+5%), in theory).<br>
So I just don't care right now to make it update less frequently.


This exact progress indication is used both for processing files to calculate the hashes in `fill`, and to copy files in `sync`.

The size ranges can easily be changed in the code to any granularity; they're specified like so.
```
[10*1024, 1*MB, 10*MB, 100*MB, 1*MB*1024]
```

The code for this functionality is not tested and hasn't even been looked at carefully,
because nothing bad will happen if it contains a bug.<br>
The fact that each item gets processed is tested in `fill.test.py:test_several`,
that's the only thing I care about.

