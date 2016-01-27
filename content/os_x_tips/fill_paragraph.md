Title: Filling (hardwrapping) paragraphs in Airmail with `par`
Date: 2014-06-27
Category: os x tips
Tags: osx, par, airmail, automator, services, fill, wrap, lines
Slug: fill-par-in-airmail
Summary: How to use `par` for conveniently filling (hardwrapping) paragraphs in plain text e-mail in Airmail [Beta] on OS X.

# tl;dr

Jump directly to [the proposed solution](#solution). Tested on OS X 10.9
(Mavericks).

# Back story

Airmail is a great application -- being very happy with Gmail's in-browser UI,
it's honestly the first e-mail desktop client that I ever felt even remotely
tempted to use. It has:

- a sleek, functional design
- almost flawless integration with Gmail (except for categories -- but there's
a
[not-too-hackish way](http://airmail.tenderapp.com/help/discussions/suggestion-new-features/396-workaround-for-gmail-categories)
to deal with those)
- a Markdown compose mode (yay!) -- and tons of other good stuff.

Especially that last feature almost got me sold -- you see, I like my e-mail
hardwrapped (what Emacs calls "filling paragraphs"), because most of the time,
I view it on monitors that are too wide for soft line wrapping to achieve a
comfortable text width.

(By the way, Airmail's layout deals with this issue very elegantly, but I know
I won't be using only Airmail. Plus there are the obvious
[netiquette issues](https://wiki.openstack.org/wiki/MailingListEtiquette#Line_Wrapping)
-- lines "should be" wrapped at 72 characters etc.)

In Gmail, I therefore use plain-text compose, which is fine for the purposes
described above, but frustrating whenever you want to apply formatting
(obviously, you can't -- it's plain text). I tried using the usual replacements
for formatting like stars & co., and I don't know about your grandma, but
*mine* certainly doesn't take \*...\* to mean emphasis.

I thought the Markdown compose mode in Airmail would solve my problems -- I
could apply formatting if and when I wanted (using the frankly more streamlined
process of *typing it in* rather than fumbling around for the right button in
the GUI) *and* fill my paragraphs, because I somehow automatically assumed
there'd by a hard-wrap feature like in any decent editor (read: emacs or
vi). Markdown is plain text after all, isn't it?

Long story short, as of yet, **there isn't**. There isn't even one for the
plain-text compose mode, as far as I'm aware. So I added my two cents to
[this feature request thread](http://feedback.airmailapp.com/forums/209001-airmail-mac-1-2/suggestions/4078595-add-line-wrap-for-plain-text-mails)
and went back to the Gmail in-browser UI.

# Solution <a name="solution"></a>

But then I realized (it took me a while, I'm still very much an OS X newbie):

1. in OS X, you can define custom actions with shortcuts[^1] for any
   application using Automator Services
2. these actions can be easily set to receive text selected in the application
   as input
3. these actions can also involve shell scripts
4. there already *is* a great (command line) program for filling paragraphs --
   it's called `par`, and as much as I admire what Airmail's developers have
   achieved, it's unlikely that they'd come up with a more sophisticated
   hard-wrapping algorithm than `par`'s simply as a side project for Airmail
   (see the EXAMPLES section in `man par`)

With that in mind, you can have hard-wrapping in Markdown or plain-text Airmail
compose at your fingertips in no time flat. If you don't have `homebrew`, start
by installing that (or any other ports manager that will allow you to install
`par`; I'll assume `homebrew` below) by pasting

        ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

at a Terminal prompt. Then:

1. install `par` with `brew install par` at a Terminal prompt
2. open Automator (e.g. by typing "Automator" into Spotlight) and create a new
   Service
3. select the applications for which you want the service to be active (for me,
   that's just Airmail) and tick the "Output replaces selected text" box
4. drag the "Run Shell Script" action onto the workflow canvas, and as the
   shell script, paste in

        :::sh
        PARINIT="rTbgqR B=.,?_A_a Q=_s>|" /usr/local/bin/par 79

    - the $PARINIT environment variable contains the default recommended
      settings for `par` (if you want to customize its behavior, you can -- good
      luck wrapping your head around `par`'s manpage, though)
    - you should set the full path to the `par` executable, the shell spawned by
      the Service might not inherit your $PATH -- for `par` installed via
      `homebrew`, it's `/usr/local/bin/par`
    - the parameter at the end is the max number of characters per
      line -- mailing list etiquette stipulates 72, I personally prefer the
      pythonesque 79, but it's your choice

At this point, your service should look something like in the screenshot
below:

![Fill Paragraph Service in Automator](/output/images/fill-par.png)

Save it, open Keyboard preferences (type "Keyboard" into Spotlight), navigate
to Shortcuts → Services → Text and set a keyboard shortcut for your newly
created Service, e.g. Cmd+Opt+P. Next time you compose an e-mail in Airmail,
just select the entire text when you're done (Cmd+A), press Cmd+Opt+P, and
voilà! Your lines have been hardwrapped, your paragraphs filled :) (Same thing,
I know.)

If the shortcut doesn't appear to work[^1], try fiddling around with it,
resetting it (maybe the one you've chosen conflicts with a pre-existing one?),
restarting Airmail, logging out and back in, rebooting... The custom shortcut
part is unfortunately the least reliable aspect of this whole setup. Automator
is a great idea, I was pleasantly surprised by it when I started using OS X a
few days back, but it could seriously use some bug-squashing.

If you fail miserably at getting the shortcut to work, you can **still access
your fill paragraph service via the menu** (select the text you want to
hard-wrap, then navigate to Airmail → Services → <name of your fill paragraph
service\>). Clicking around in a GUI is tedious (though hey -- it's the Apple
way after all, isn't it?), but it shouldn't be too much of a bother since you
need to do it only once per e-mail.

**Bottom line**: I am now officially completely sold on Airmail (even bought
the released version instead of using the free beta) and look forward to the
joy of using it!

EDIT: In order to have the **least trouble possible getting the shell script up
and running as a Service**, two rules of thumb:

1. Leave it completely up to OS X where it stores the Service (.workflow)
   file. This will probably be in `~/Library/Services`, and I learnt the hard
   way not to tinker with it -- if `Services` is a symlink instead of a real
   directory, the OS won't discover new Service files (though old ones will
   still be accessible).
2. If the Service doesn't show up in the keyboard shortcuts menu after
   creation, try refreshing the service list with
   `/System/Library/CoreServices/pbs -update`.

[^1]: Those shortcuts are in fact quite buggy, especially those that you want
to be global (not specific to a concrete app) -- at least on Mavericks (OS
X 10.9). They tend to get disabled on a whim, especially if you tinker with
them, and are a pain to get working again (login, logout, reboot -- anything
goes). If anyone knows why, please let me know!
