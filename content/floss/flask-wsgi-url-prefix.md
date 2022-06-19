Title: How to mount a Flask app under a URL prefix (or really, any WSGI app)
Date: 2020-11-15
Tags: python, flask, wsgi
Slug: flask-wsgi-url-prefix
Summary: Arguably the best kept secret in the Flask ecosystem ;)

# Intro

In a hurry? Skip to the [minimal working example](#mwe) below!

So this is probably something that seasoned Flask webapp devs will find
trivial, especially if they're also well-acquainted with [WSGI
itself][wsgi] (the Python web server standard that Flask and the other
popular synchronous Python web frameworks comply with).

[wsgi]: https://wsgi.readthedocs.io/

But my background is not like that. I've only occasionally used Flask
for a project here and there over the years (and I've been really happy
with it, since it delivers on its promise of being "micro" and keeps out
of the way most of the time). I learned it mostly through its own docs.
I've been aware that WSGI is a thing, but it never occurred to me I
should learn more about it, it always felt like the Flask docs (should)
cover everything I need.

Which they did, except for the issue mentioned in the title of the
article: transparently mounting the app under a URL prefix. Up until
yesterday (when I found out basically by sheer luck that this is
addressed by the WSGI standard that Flask conforms to), I had no idea
what the proper way to do it in Flask was. I never could find any
guidance in the Flask docs; as far as I know, I don't think the
idiomatic solution I'll be discussing below is covered in there (and
I've tried searching them again now that I know what I'm looking for).
So I always resorted to clunky workarounds in order to achieve this.

I'm fairly sure I'm not the only person like this -- a happy occasional
user of Flask whose one major frustration has been having to manually
smuggle URL prefixes into his routes. If you have a similar background,
then may Google be more clement than it was to me and rank this article
on the first page of its results when you hit this particular roadblock
;)

If you're a Flask / WSGI whiz, then your reaction will probably be "But
of course [this](#solution) is how it's done!" So in order to get
something out of this article, you can instead muse upon the relative
merits and drawbacks of splitting up technical documentation in a way
that's well-organized / clearly delineated / methodical / logical (=
Flask info in Flask docs, WSGI info in WSGI docs) vs. in a way that's
useful and accessible even to occasional users, beginners etc. (= Flask
docs might want to cover the parts of WSGI that a budding Flask dev
might want to care about, even though that means duplicating
information).

# The problem

As you're prototyping and developing a Flask app, routing is pretty easy
and straightforward:

```python
@app.route("/login", methods=["GET", "POST"])
def login_func():
    ...
```

But when the time comes to deploy it, you often realize you need to
**mount it under a URL prefix**, e.g. `/my-app`. For the route above,
that means that you want to trigger it when users navigate to
`example.com/my-app/login`, not `example.com/login`. And similarly, you
want this prefix added when generating internal redirects or links in
your templates.

So you think to yourself, this is surely such a common use case that
there's definitely an example how to do this directly in [Flask's
*Quickstart*][quickstart]. Or failing that, definitely *somewhere* in
the docs.

[quickstart]: https://flask.palletsprojects.com/en/1.1.x/quickstart/

So you search the docs for a reasonable query like "url prefix", which
sounds like what you're interested in, and you learn about [blueprints],
which is where stuff starts to become confusing. Blueprints are for
making reusable application components and they support registering at a
URL prefix and/or a subdomain.

[blueprints]: https://flask.palletsprojects.com/en/1.1.x/blueprints/

They're also a fairly advanced feature useful in more complicated apps,
so they sort of go against the grain of your expectations with Flask.
You likely picked up Flask because you liked that a simple app can
consist of just a single Python module and a few lines of code, but now
it looks like if you want to run it in production in a flexible way,
you'll need to learn about blueprints and rewrite it as one? Because it
sure doesn't look like vanilla Flask apps support URL prefixes, the docs
don't mention any promising leads...

So you end up deciding to roll your own homegrown solution, which might
be configurable but still boilerplate-y if you still have some mental
energy left to invest into the problem:

```python
PREFIX = "/my-app"

@app.route(f"{PREFIX}/login", methods=["GET", "POST"])
def login_func():
    ...
```

Or it might just be hardcoded to show you really don't care anymore, if
you've just lost an hour searching for a Flask feature that would handle
this in a civilized manner, and/or reading up on blueprints (before
giving up):

```python
@app.route("/my-app/login", methods=["GET", "POST"])
def login_func():
    ...
```

If that sounds like you (and it certainly sounds like me), then boy do I
have good news for you :) Turns out there actually *is* a right way to
do it!

# The idiomatic solution <a name=solution></a>

The title of the article hints at the reason why the right way to do it
is so hard to figure out: it turns out that deploying a Flask app under
a URL prefix isn't actually a feature of Flask per se, it's a feature of
the Python [WSGI] standard that Flask conforms to. So that's probably
why the way to achieve this isn't described in the Flask docs
themselves, because I suppose you're expected to read up on the
available WSGI knobs and handles separately...? Frankly, I don't think
that's a realistic expectation :) I think this information would make a
great addition to the Flask docs, maybe even directly in the
*Quickstart* section.

So what's the trick? The trick is to set the rather quirkily/quaintly
named [`SCRIPT_NAME` environment variable][wsgi-env] prior to starting
the web server running the app. If you set `SCRIPT_NAME=/my-app`, WSGI
guarantees that the web server running your app will strip this prefix
from incoming URLs, and add it to outgoing URLs (redirects, in-app links
in templates). That's it, no need to modify your app at all, whether to
add a configurable or hardcoded prefix to all the routes, or to rewrite
it as a blueprint. Nice.

[wsgi-env]: https://wsgi.readthedocs.io/en/latest/definitions.html

---

**EDIT:** As [u/james\_pic][jpic] points out over on [Reddit], reading
`SCRIPT_NAME` from an env var is actually not required by the WSGI spec,
it's a convenience feature provided by some WSGI servers, e.g.
[Gunicorn].

[jpic]: https://www.reddit.com/user/james_pic/
[reddit]: https://www.reddit.com/r/Python/comments/juwj3x/how_to_mount_a_flask_app_under_a_url_prefix_or/gchdsld
[gunicorn]: https://gunicorn.org/

---

# Caveats

Because of course, there are a few issues you might run into.

## Flask's builtin web server ignores `SCRIPT_NAME`

---

**EDIT:** As should be clear from the previous edit, Flask's builtin web
server only ignores the `SCRIPT_NAME` env var. It works perfectly well
with the `SCRIPT_NAME` WSGI variable, which however requires quite a bit
more work to set up. You need to add WSGI routing middleware to your
application, e.g. like this:

```python
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.wrappers import Response

app.wsgi_app = DispatcherMiddleware(
    Response('Not Found', status=404),
    {'/my-app': app.wsgi_app}
)
```

Presumably, you'd make the actual value of the prefix part of the app's
config.

(Code sample courtesy of [u/james\_pic][jpic] over on [Reddit], thank
you!)

---

When you find out about `SCRIPT_NAME`, your first intuition is to test
if it indeed does what you need with Flask's builtin dev server,
because, well, that's what you use for development. Unfortunately, it
turns out that Flask's server couldn't care less about this env var,
which might lead you to (wrongly) conclude that you're on the wrong
path. I actually think this happened to me a few years back because I
feel like I've tinkered with `SCRIPT_NAME` before, only to conclude it
doesn't seem to do anything.

The fix: just use a <del>fully-featured production</del> WSGI server
<ins>that supports reading this configuration from an environment
variable</ins>, e.g. [Gunicorn]. I promise `SCRIPT_NAME` works there.

<ins>Alternatively, add some routing middleware of the kind sketched
above to your app.</ins>

<del>
Is this one of the reasons why Flask's builtin server warns "This is a
development server. Do not use it in a production deployment"? I'd
always thought it was for performance / stability / security reasons,
but it looks like it also just isn't (fully) WSGI-compliant.
</del>

## Use `url_for` to generate internal links

I.e. instead of writing `href="/login"` in your templates or
`redirect("/login")` in your view functions, write `href="{{
url_for('login_func') }}"` and `redirect(url_for("login_func"))`. This
will make sure the URLs are correctly prefixed with `SCRIPT_NAME`, if
applicable.

This is [recommended as best practice][url-building] by the Flask docs
anyway, so it's not like it's additional hoops to jump through.
Interestingly, this section in the Flask docs is the closest they brush
with discussing mounting the app under a URL prefix. They tell you:

[url-building]: https://flask.palletsprojects.com/en/1.1.x/quickstart/#url-building

> If your application is placed outside the URL root, for example, in
> `/myapplication` instead of `/`, [`url_for()`][url-for] properly
> handles that for you.

[url-for]: https://flask.palletsprojects.com/en/1.1.x/api/#flask.url_for

But they don't tell you *how* to place your application outside the URL
root in the first place, which is kind of maddening. If you open the
[link to the `url_for()` docs][url-for], you are further teased with
mentions of `APPLICATION_ROOT` and `SERVER_NAME` configuration values,
which sound a lot like the kind of setting you were looking for, except
the docs immediately dash your hopes and remain silent about what you
really want, i.e. the `SCRIPT_NAME` env var:

> Configuration values `APPLICATION_ROOT` and `SERVER_NAME` are only used
> when generating URLs outside of a request context.

I remember tearing my hair out in despair at this point of digging
through the Flask docs and trying in vain (of course) to tinker with
those configuration values a few years back.

---

**EDIT:** Again, after reading [u/james\_pic][jpic]'s very helpful and
insightful comment on [Reddit], I've realized the Flask docs technically
*do* contain information which can help you figure this out, in the
[*Application Dispatching*] section, specifically under [*Dispatch by
Path*].

The trouble is that the section is introduced by the following sentence:

> Application dispatching is the process of combining multiple Flask
> applications on the WSGI level.

Which sounds like it's once again a more advanced topic (kind of like
blueprints) meant for people who are trying to run multiple apps under
the same WSGI server at the same time (which you're not). The code
examples are fairly complex to match, so at first sight, it doesn't look
like this is what you should be spending your time reading if you just
need to figure out something as basic as running your app under a URL
prefix in production.

[*Application Dispatching*]: https://flask.palletsprojects.com/en/1.1.x/patterns/appdispatch/
[*Dispatch by Path*]: https://flask.palletsprojects.com/en/1.1.x/patterns/appdispatch/#dispatch-by-path

---

## Don't strip the prefix in your reverse proxy config

If you're configuring your Flask app under a URL prefix, it's probably
running behind a reverse proxy of some sort (Nginx, Apache, etc.).
Reverse proxies can be configured to strip these prefixes when relaying
requests to individual apps, but **don't do this**!

You want to leave the handling of the prefix to the WSGI server running
your app, because the WSGI server has intimate knowledge about the app
(it knows it can expect the app to talk WSGI), so it can be smart about
how exactly prefix handling should be done. By contrast, the reverse
proxy has very little information about your app -- it can rewrite
incoming URLs in request headers fairly easily, but that's about it, it
can hardly rewrite outgoing URLs in response bodies, that would be
non-trivial. That's what sprinkling `url_for()`s where appropriate
throughout your app is for (see previous section).

So make sure your reverse proxy leaves the prefix alone. As an example,
for Nginx, you don't want this, which would get rid of the `/my-app/`
prefix:

```nginx
location /my-app/ {
    proxy_pass http://127.0.0.1:8000/;
    # ...
}
```

<del>
Instead, you want this:
</del>

```nginx
location /my-app/ {
    proxy_pass http://127.0.0.1:8000/my-app/;
    # ...                            ^^^^^^^
}
```

Actually, as Ivan Shatsky helpfully pointed out in the comments, you
want **this**:

```nginx
location /my-app/ {
    proxy_pass http://127.0.0.1:8000;
    # ...
}
```

Notice the lack of a trailing slash after the port number. The effect
will be the same, but you'll save some CPU cycles -- instead of first
stripping the prefix and then adding the same one, Nginx just
completely leaves it alone.

# Minimal working example <a name=mwe></a>

Let's wrap up with a runnable demo. Put this in `app.py`:

```python
from flask import Flask, url_for

app = Flask(__name__)

@app.route("/")
def index():
    return url_for("index")
```

Run the app with a WSGI-compliant web server, e.g. [Gunicorn] (again,
*not* Flask's builtin dev server, see above), while setting the
`SCRIPT_NAME` env var:

```sh
$ SCRIPT_NAME=/my-app gunicorn app:app
```

Now try accessing `/` with `curl`:

```sh
$ curl localhost:8000/
```

You should get an internal server error. If you inspect the traceback in
the window where the app is running, you'll see this was due to the fact
that the expected `/my-app` prefix wasn't found, so try adding it:

```sh
$ curl localhost:8000/my-app/
/my-app/
```

Now everything works, even though your app's source code is clean and
blissfully unaware of any prefix. Gunicorn strips away the prefix from
the request before passing it on to your app's router, and `url_for`
takes care of adding the prefix back into any internal link generated by
your app, as you can see in the output (`/my-app/` instead of `/`).

Just to confirm Flask's builtin development server doesn't <del>properly
handle</del> <ins>read</ins> `SCRIPT_NAME` <ins>from the
environment</ins> -- run the app with it:

```sh
$ FLASK_APP=app SCRIPT_NAME=/my-app flask run
```

The prefix is ignored, which means that accessing `/` works (which we
don't want):

```sh
$ curl localhost:5000/
/
```

And `/my-app/` unfortunately doesn't:

```sh
$ curl localhost:5000/my-app/
# outputs Flask's default 404 message
```
