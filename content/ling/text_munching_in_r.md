Title: Text munching in R?
Date: 2017-10-28
Tags: python, r, rust, perl, text processing
Slug: text-munching-in-r
Summary: Is R suited for processing large quantities of text data?

R has been [gaining traction][r-growth] as a language for data analysis. My
feelings about the whole ecosystem are mixed -- it has some [incredibly
well-designed libraries][tidyverse] and a [top-of-the-game IDE][rstudio], but
the core language makes me cringe (it feels like "Perl and Lisp: The Worse
Parts"). Be that as it may, it has undeniably become the go-to programming
language for many people for whom programming is not their main breadwinner,
many linguists among them. If you're one of these people and wondering whether
it's worth undergoing the cognitive burden of learning another language and
having to context-switch between them, read on!

The main problem with R and large data is of course that R is fast as long as
you can load everything into memory at once and use vectorized operations. The
whole point of this post is that with the current size of a typical corpus, you
often can't do that. You'll have to process the corpus line by line, which
means using a for-loop, and these are notoriously slow in R. I'm not pretending
this is some new discovery (it's not), I'm just trying to quantify how
problematic this slowness is for processing large quantities of text
(prohibitive, in my opinion), so that you don't have to figure it out for
yourself and can get started [learning Python 3][nltk-book] right away instead
;)

(Another big problem is that R doesn't have an efficient and versatile hash
table data structure.)

tl;dr
=====

If you're planning to process corpora of hundreds of millions of tokens or more
-- spoiler alert, you probably shouldn't do it in R.

R: 1 day (!) / 15 hours (see EDIT below, but still !)
=====================================================

After quite some exploration of various alternatives for the individual
subtasks, this is the program that I came up with:

```r
library(stringi)
library(hash)

# read input from STDIN
con <- file("stdin", open="rt")

pos_sets <- hash()
start <- Sys.time()
while (TRUE) {
  line <- readLines(con, n=1)
  if (length(line) == 0) {
    break
  }
  # lines with tokens (as opposed to metadata) contain tabs
  if (stri_detect_fixed(line, "\t")) {
    # individual token attributes are tab-separated
    attrs <- stri_split_fixed(line, "\t")
    # for each token, we're interested in the lemma (headword)...
    lemma <- attrs[[1]][2]
    # ... and the part-of-speech, which is the first character of the tag
    tag <- attrs[[1]][3]
    pos <- stri_split_boundaries(tag, n=2, type="character")[[1]][1]
    # build a per-part-of-speech frequency distribution as a nested hash:
    # {
    #   "noun": {
    #     "cat": 5,
    #     "dog": 3,
    #     ...
    #   },
    #   "verb": {
    #     "look": 2,
    #     ...
    #   },
    #   ...
    # }
    if (is.null(pos_sets[[pos]])) {
      pos_sets[[pos]] <- hash()
    }
    if (is.null(pos_sets[[pos]][[lemma]])) {
      pos_sets[[pos]][[lemma]] <- 1
    } else {
      pos_sets[[pos]][[lemma]] <- pos_sets[[pos]][[lemma]] + 1
    }
  }
}

# report running time
diff <- Sys.time() - start
cat(sprintf("Done in %g %s.\n", diff, units(diff)), file=stderr())
```

Given the input corpus mentioned above, this code takes **1.33** days to run.
Compared to other languages one might conceivably use (see below), this is just
ridiculous.

Now, I'm certainly not an expert in R, so there may be better ways of doing
some of this. But I doubt such improvements, if any, would be of any practical
relevance, because even reducing the running time to *a tenth* of the original
duration wouldn't be enough. And if there *is* a way to go even further, say to
a hundredth, which would begin to make R competitive, then I would argue that a
language which lets you shoot yourself so spectacularly in the foot
performance-wise if you're not hip to some clever tricks should just be avoided
for tasks where said performance matters.

---

**EDIT:** Replacing `stri_split_boundaries(tag, n=2, type="character")[[1]][1]`
above with `stri_sub(tag, from=1, to=1)`, you can cut the running time down to
15 hours. That's still way too much in comparison with the competitors, and
just reinforces one of the points made below: there's often no default and
efficient way of doing some basic operations (like string manipulation) in R.

This is in great part due to R's emphasis on vectorization, which leads to a
proliferation of subtly different functions designed for doing subtly different
kinds of vectorized passes over data. Good luck trying to remember them all.
And if you pick the wrong one (cf. `stri_split_boundaries()` vs. `stri_sub()`)
-- because there are just too many similar ways of achieving the same result
and too much documentation to read before you even begin to see what you should
use -- you get penalized heavily. This is very programmer-unfriendly design.

Contrast this with the [Zen of Python][py-zen]: "There should be one -- and
preferably only one -- obvious way to do it."

---

With these general considerations out of the way, let's look at some details of
how to implement this task in R. In many cases, it's unclear how you should
even approach the problem in R, due to **missing or confusing built-in
functionality**. As a result, in addition to having a lousy running time on
this task, R also puts a strain on the programmer's time.

Reading the data
----------------

This sounds so basic it should be obvious, right? Not so fast.

First of all, the `file("path/to/file")` function creates a file connection,
which is however not open unless you also specify a mode in the `open=`
argument, or alternatively, unless you call the `open()` function on the
connection. Why you would want to create a connection that's not open is beyond
me, but R adds insult to injury by allowing `readLines()` to work on a closed
connection: it just opens the connection before doing the reading and closes it
afterwards. This means that repeated calls to `readLines(unopened_connection,
n=1)` will **repeatedly read the first line of the file**, which is most likely
not what you want. This is API design level PHP.

Second, the corpus is gzip compressed, so you'll need to uncompress it. There
are basically two options:

1. have an external program (`zcat`) do the decompression and pipe the data
   into R via `STDIN`
2. handle the decompression within R itself

As a general rule (for any language), it will always be faster to handle the
decompression in a different process on a multi-core system, because the tasks
can proceed in parallel.[^1] On the other hand, it's more portable not to
depend on external programs, and R does have a built-in function to open a
connection to a gzipped file, namely `gzfile()`. Based on tests on shorter
inputs, it's about 50% slower than external decompression, which is a somewhat
worse performance deterioration than e.g. Python 3 (40% based on the full
input). In light of the already dire running time, it's something we can't
really afford.

Third, having to do the line-by-line reading in a `while (TRUE)` loop, using a
function called `readLines()` (note the plural) with an argument of `1`,
checking the length of the resulting character vector in order to determine the
end of the input -- that's just gross.

String manipulation
-------------------

R has built-in functions for string matching (`grepl()` et al.), not so much
for string splitting. This is the point where I got suspicious of the
performance of everything and started testing alternatives. I finally ended up
using the [stringi][stringi] package, which is fast and has a fairly consistent
API. [stringr][stringr] is a set of higher-level wrappers around it, which have
however proven somewhat slower than the built-ins in my highly informal
testing.

O hash map, where art thou?
---------------------------

Building a per-part-of-speech frequency distribution of headwords requires an
appropriate data structure. As indicated in the comments in the R source, we
want to build a nested collection that looks something like this:

```
{
  "noun": {
    "cat": 5,
    "dog": 3,
    ...
  },
  "verb": {
    "look": 2,
    ...
  },
  ...
}
```

The requirements on the data structure we need are the following:

1. it's a collection
2. strings can be used as keys
3. it can be arbitrarily nested
4. key lookup is fast, i.e. constant time

In other words, we need a hash (or a dict, in Python terminology). R doesn't
*have* a hash (I'll qualify this statement in a bit).

The workhorse data structure in R that satisfies points 1--3 is a list.
Unfortunately, it has [linear access time][r-bigoh]. That's not going to work.

R also has environments, which it uses to store and access variables. Under the
hood, environments are implemented as hashes, but using them as such is a
massive pain, because their API isn't meant for it. Fortunately, there's [a
wrapper package][hash] which makes it more convenient. Unfortunately,
environments weren't optimized with this use case in mind. They were designed
to hold key--value (variable name--variable value) pairs explicitly defined by
people as part of their programs, not millions of items extracted from data. As
a result, they [slow down dramatically][r-lookup] once the number of items
grows large.

(The article in the previous link provides a survey of the state of the art of
fast key lookup in R. The state of the art is... dismal. Your only option is
basically indexing a data table, which is fine for a finalized data set, but
useless when *building the data set* -- you can't afford to reindex after each
new data point.)

There's also the [hashmap library][hashmap], which is a wrapper around C++
Boost hashes. However, it doesn't do nesting, so it's of no use to us, and of
very limited usefulness in general.

Conclusion: technically, we have to concede that R has hashes, but **for all
practical intents and purposes, it doesn't**.

There's one last twist, though. Funnily enough, in our use case, it turns out
it doesn't really matter anyway. Indeed, it seems the performance of for-loops
in R is *so egregiously bad* that it dwarfs even the inefficiencies accrued by
the linear lookup time of lists: if you reimplement the script with lists, it
takes just a little longer than the version with hashes, about 1.36 days.

(Or maybe it's just that the performance of environment-based hashes becomes so
bad when they grow large as to be comparable with that of lists? Who knows, and
frankly, I don't care enough to want to find out. If it's the for-loops though,
then adding efficient hashes to R won't really solve anything.)

---

**EDIT:** With `stri_sub()` substituted for `stri_split_boundaries()` as
detailed above, the code using lists runs in about 1.28 days, which is a much
smaller improvement than in the case of the code using lists (1.33 days → 15
hours).

---

Summary
-------

If you like R and your reaction to this is, "That's not fair! R was never meant
to do any of this, that's why everything feels so backhanded." -- then good,
that's basically the gist of this post: **don't use R for something it wasn't
meant to do**.

What are the alternatives, then?

Task
====

The following details an informal test comparing the speed of R, Python 3, Rust
and Perl at processing a large corpus file (~120M tokens, 1.5GB gzipped) and
creating a frequency distribution of headwords per part-of-speech. The idea is
to see whether R is a viable alternative in this domain, or whether the slowing
down caused by the inability to use vectorized computations (because we can't
load the entire thing into memory at once) will just be too much.

Python 3: 5 minutes
=================

Yes, that's right. It takes Python 3 **5 minutes** to do the same task that
took R **over a day**. The code feels a lot simpler too:

```python
import sys
import time


def main():
    pos_sets = {}
    start = time.time()
    for line in sys.stdin:
        if "\t" in line:
            _, lemma, tag, _ = line.split("\t", maxsplit=3)
            pos = tag[0]
            # this is an intentionally naive implementation which mimicks
            # the R code and something an inexperienced coder might do;
            # a more concise and probably better performing solution could
            # be achieved using dict.setdefault() or collections.defaultdict
            # / collections.Counter
            if pos not in pos_sets:
                pos_sets[pos] = {}
            if lemma not in pos_sets[pos]:
                pos_sets[pos][lemma] = 1
            else:
                pos_sets[pos][lemma] += 1

    diff = time.time() - start
    print(f"Done in {diff:.0f} seconds.", file=sys.stderr)


if __name__ == "__main__":
    main()
```

FYI, this was run using Python 3.6. As a rule, use always the most recent
version of Python 3 you can (at least 3.5, 3.4 in a pinch; with earlier
releases, you may encounter performance issues). In any case, **do not use
Python 2** for new projects and let it end-of-life in peace.

Perl: 13 minutes
================

Perl used to be a popular alternative for text processing. Like R, it has its
fair share of nauseating language design and weird quirks, but since it was
actually meant for use in this domain, it won't spectacularly let you down.

(Unless your data is silently corrupted because you handled text encoding
wrong. Perl's behavior in this respect is a relict of a pre-UTF-8-everywhere
past, and it's the single biggest reason for why the language should be put out
of its misery already.)

Here's the code:

```perl
use strict;
use utf8;
use open qw(:std :encoding(utf8));

my $start = time();
my %pos_sets = ();
while (<>) {
  if (/\t/) {
    my @attrs = split /\t/;
    my $lemma = @attrs[1];
    my $tag = @attrs[2];
    my $pos = substr $tag, 0, 1;
    # auto-vivification: ergonomic, but also made possible by the whole
    # "implicit defaults that have a potential of screwing stuff up
    # without you even knowing about it" culture of Perl
    $pos_sets{$pos}{$lemma} += 1;
  }
}
my $diff = time() - $start;
print STDERR "Done in $diff seconds.\n";
```

Bottom line though, being more than twice as slow as Python 3 (which came as a
surprise to me, I must admit) and definitely the worse language, it has little
to recommend itself if you're considering to learn a new language for this type
of task.

Except maybe if you want to continuously log what the program is doing to a
terminal -- like output the number of lines processed after each line. Perl is
clearly very efficient at writing to a terminal, the running time is basically
the same with continuous logging incorporated. By contrast, Python 3 takes
about three times longer (~ 15 minutes).

(I guess maybe Python flushes output after each `print()` call, whereas Perl
does some smart buffering which results in it not being slowed down by the
latency of the terminal...? Who knows, at any rate, it's hardly a "killer"
feature.)

Rust: 1.25 minutes
==================

As a compiled, systems-level language, Rust is in a different league compared
to the previous contestants: of course it's going to be faster. I included it
because it provides a frame of reference. The important takeaway is that we're
in the same ballpark with Python 3 (roughly units of minutes), so there's no
pressing need to turn to a compiled language for this task.

Here's the code, for completeness sake:

```rust
use std::io;
use std::io::prelude::*;
use std::collections::HashMap;
use std::time;

type LemmaCount = HashMap<String, i32>;
type PosSet = HashMap<char, LemmaCount>;

fn main() {
    let start = time::SystemTime::now();
    let mut pos_sets = PosSet::new();
    let stdin = io::stdin();
    for line in stdin.lock().lines() {
        let line = line.unwrap();
        if line.contains("\t") {
            let mut attrs = line.split("\t").skip(1).take(2);
            let lemma = attrs.next().unwrap();
            let tag = attrs.next().unwrap();
            let pos = tag.chars().take(1).next().unwrap();
            let pos_set = pos_sets.entry(pos).or_insert(LemmaCount::new());
            let count_for_lemma = pos_set.entry(String::from(lemma)).or_insert(0);
            *count_for_lemma += 1;
        }
    }
    let diff = start.elapsed().unwrap().as_secs();
    println!("Done in {:.0} seconds.", diff);
}
```

Note in passing how nicely the Rust code reads for a compiled language. Of
course, since it's a much stricter (and safer) language than Python, it's more
ceremonious to write and the APIs are more complicated, because they have to
adhere to the various memory management guarantees Rust gives you (among other
things). But once the code is written, it's very readable and clear. And all
necessary functions and data structures are (a) available in the standard
library, and (b) plenty efficient.

Conclusion
==========

Just to be clear: the ultimate purpose of this post is **not** bashing R (not
for being slow at text munching, at any rate); it's to give a convincing
account of why it's just not the right tool for the job. And not in a small
way, either -- in a way that requires to learn a different tool, there's no way
around it. Let me reiterate that my recommendation would hands down be [Python
3][nltk-book].

Once the data is extracted, go back to R by all means. Although
Python does have a fairly nice high-level [data analysis library][pandas], it's
not my intention to discourage anyone from using R for what it *is* good at,
especially if this is a skill they are already proficient in.

The internet is full of people asking advice on which programming language to
learn, and the answers are invariably evasive -- it depends on your tastes,
what fits your brain better, what your use case is. In the hopes that some
people might find opinionated guidance useful for a change (I know I personally
often do, when flirting with a new language): if you're looking to process
large quantities of text data, the answer is a big, resounding **NOT R**!

A vectorized postscript
=======================

Since I ran these on a server with 64 GB of RAM, I figured I might as well try
loading everything into memory in R and doing it the proper, vectorized way,
while I'm at it. Here's the code, using `dplyr`:

```r
library(dplyr)
library(stringi)

start <- Sys.time()

con <- file("stdin", open="rt")
corpus <- readLines(con)

diff <-  Sys.time() - start
cat(sprintf("Corpus read in after %g %s.\n", diff, units(diff)))

corpus <- stri_subset_fixed(corpus, "\t")
corpus <- stri_split_fixed(corpus, "\t", simplify=TRUE)
freq_dist <- tibble(
  POS=stri_sub(corpus[, 3], from=1, to=1),
  LEMMA=corpus[, 2]
) %>%
  group_by(POS, LEMMA) %>%
  summarize(FREQ=n())

diff <- Sys.time() - start
cat(sprintf("Finished processing corpus after %g %s.\n", diff, units(diff)))
```

Let me say at the outset that this code looks much nicer -- it's clean, modern
R, made possible in great part by Hadley Wickham's efforts to redesign the data
manipulation vocabulary from the ground up. Note also that we've made a
concession on our requirements: the resulting data structure is a tibble, not a
hash, i.e. key lookup time is not constant but depends on the size of the data.

Well, just loading the corpus into memory took ~18 minutes. The script then ran
for **several days**, in the course of which I checked every now and then to
see how much memory it was using: ~35 GB. I don't suppose anyone has that much
RAM on their laptop. Then someone rebooted the server before the program could
complete. I think you'll agree the experiment is conclusive even so.

<!----------------------------- LINKS AND NOTES ----------------------------->

[r-growth]: https://stackoverflow.blog/2017/10/10/impressive-growth-r/
[tidyverse]: https://www.tidyverse.org/
[rstudio]: https://www.rstudio.com/
[nltk-book]: http://www.nltk.org/book/
[stringi]: http://www.gagolewski.com/software/stringi/
[stringr]: https://cran.r-project.org/web/packages/stringr/vignettes/stringr.html
[pandas]: http://pandas.pydata.org/
[r-lookup]: http://appsilondatascience.com/blog/rstats/2017/03/02/r-fast-lookup.html
[r-bigoh]: https://stackoverflow.com/questions/41353298/what-is-the-time-complexity-of-name-look-up-in-an-r-list
[hash]: https://cran.r-project.org/web/packages/hash/index.html
[hashmap]: https://cran.r-project.org/web/packages/hashmap/index.html
[py-zen]: https://www.python.org/dev/peps/pep-0020/#the-zen-of-python

[^1]: You could also offload the decompression to a different thread in the
same process, but that complicates the implementation. Piping gives you
parallelization basically for free.
