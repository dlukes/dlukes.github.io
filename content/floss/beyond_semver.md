Title: Beyond semantic versioning? (cross-post)
Date: 2014-12-14
Tags: floss, semver, versioning, underscore.js, library, development, dependency
Slug: beyond-semver
Summary: Semantic versioning is a good idea, but it would be better to use an explicit keyword system to signal (non-)breaking changes in library versions.

# Background

Ever since I first read about [semantic versioning](http://semver.org/), I've
thought of it as a neat idea. But only recently did it occur to me that what
I liked about the idea was its goal, much less its execution (more on that
below). What made it obvious was [this lengthy
discussion](https://github.com/jashkenas/underscore/issues/1805) about breaking
changes introduced in v1.7 of [underscore.js](http://underscorejs.org/) without
an accompanying major version bump.

Even though I still think sticking to semver is the right thing to do if your
community of users expects you to (even if you don't personally like the
system), I am convinced there are fundamentally better ways of dealing with the
problem of safely and consistently updating dependencies.

It made me want to add [my two cents to the
discussion](https://github.com/jashkenas/underscore/issues/1805#issuecomment-66929684),
as someone who's more of a dabbler in programming and not really part of the
community, so feel free to ignore me :) I attach my commentary below for
reference (it's virtually the same text as in the link above).

# tl;dr

semver is trying to do the right thing, but doing it wrong -- instead of
**implicitly** encoding severity of change information in **version numbers**,
**explicit keywords** like :patch, :potentially-breaking or :major-api-change
would make much more sense.

# More verbosely

I've always found the goals of semver worthy, but this thread has made me
realize that while its aims are commendable, its methods are kind of broken:

1. semver tries to take an existing semiotic system (= version numbers), which
has developed informally and is therefore a loose convention rather than an
exact spec, and reinterpret it in terms of an exact spec (or impose that spec on
it). trouble is, the prior informal meaning won't go away so easily (why should
it?), especially for projects that have been around longer than semver. the
problem then is, since the two systems (the informal one and semver) look the
same in terms of their symbolic representation, it's hard to guess which one
you're dealing with by just eyeballing the version number of a library (or
project in general).

    it's like if someone decided that "f\*ck" should mean "orchid" from now on,
    because it's nicer -- on hearing the word, you'd never know if it's being
    used as the original profanity, or in its new meaning. homonymy is a pain to
    deal with when it's accidental (cf. NLP), so why introduce it on purpose?
    the job that semver set out to do should be fulfilled by a new formal means
    which is instantly recognizable, not by hijacking an existing one and
    overlaying additional interpretation on it and thus making it **ambiguous**.

2. even if version numbers hadn't existed before semver, they're terribly
**inadequate** for the purpose of conveying information about the severity of
changes introduced by an update (though I understand their appeal to
mathematically-minded people). they're inadequate because they're **implicit**
-- it's a bit like if someone decided they don't need hash maps because they can
make do with arrays by remembering the order in which they're adding in the
key-val pairs. if I remember the order, then I know which key the given index
implicitly refers to, and the result is as good as a hash map, isn't it?

    except it isn't. keys are useful because they have **explicit semantics**,
    making it instantly clear what kind of value you're retrieving. in the same
    way, encoding the information about the severity of changes into version
    numbers makes it implicit (in addition to being ambiguous, as stated
    previously). why not use explicit keyword tags along with the version number
    (which can be romantic, semantic -- whichever floats the dev team's boat and
    best reflects the progress of the project) to give a heads up as to the
    nature of the update? e.g. :patch, :potentially-breaking, :major-api-change
    etc.

    granted, even language is a code which needs to be learned, like semver
    (gross oversimplification here, but let's not get into the details of
    language acquisition), but since it's widely established and
    conventionalized for conveying the kinds of meanings semver is trying to
    convey, **why not just use it when it's available**? why use a system
    (version numbers) which is less well-suited to the purpose **and** ambiguous
    to boot?

    (on the other hand, numbers are eminently well-suited for keeping track of
    which version is newer than which and how much so -- the original purpose of
    version numbering -- because they are designed to have orderings defined on
    them. by contrast, words would do a terrible job at this. if you care to
    indicate the evolution of your codebase, you might introduce your own
    disciplined [romantic or sentimental](http://sentimentalversioning.org/)
    versioning scheme, which ironically is a more meaningful and ergo semantic
    way of doing versioning than semver, because it sticks to the conventional
    semantics of numbers (the closer the numbers, the more similar the
    versions). if you don't care about this, which is perfectly fine, you might
    as well use dates for version numbers.)

keyword tags have the advantage that they're instantly human-readable by anyone
who has a basic command of English. if there is sufficient will in the
community, a useful subset can be frozen in a binding spec, so that they are
machine-readable as well.

I'm not sure whether these keywords should be an appendix to the version number
(like v2.3.4-:potentially-breaking), or whether the information they provide
should be more extensive and included in a formalized preamble to the changelog
(finally forcing people to at least take a glance at it ;) ). using the latter
approach, the information provided could be (optionally) even more targeted,
e.g. detailing explicitly which parts of the API are affected in a non-backwards
compatible manner by the update.

anyways, just a few ideas :) I am not primarily a coder, so there may be obvious
drawbacks to this scheme that I can't see or which have already been discussed
by the community on multiple occasions which have escaped my attention. in which
case, please bear with me and excuse my lack of sophistication.
