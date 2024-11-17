
First off, this is my first time writing tests.<br>
So I have no idea how bad the situation is in this area.

I did whatever made sense.<br>
It's kind of good enough for me. (see `reliability.md`)

At some point I'll thoroughly research how other more serious projects
approach testing something similar.

---

The glue scripts are without tests.<br>
It could be argued that they're just scripts and thus don't need to be tested.<br>
But it still bugs me that they don't have tests.<br>
And at the same time, I can't seem to even dare to start writing them.

There's only one small test only to ensure that the tools work as intended when combined.<br>
It's a tiny bit about testing 'glue', but it was done to test that the tools play well together, so why not kill two birds with one stone.

---

I also almost started to write tests with a fuse file system to artificially fail
on specific operations.<br>
It's not complicated, but it's still quite a bit of code/complication for very simple tests,
and it's extremely easy to just look at the code to verify the desired properties.
Such desired properties are listed in each `.test.py` file at the end.
