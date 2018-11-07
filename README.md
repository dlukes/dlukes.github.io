# Cloning

Don't forget to initialize the plugin submodules after cloning!

```sh
git submodule init
git submodule update
```

# Python environment

Set it up using `pipenv install --ignore-pipfile --keep-outdated`
(trying to make sure Pipenv doesn't fetch a newer, possibly incompatible
version of some dependencies against our will, *sigh*), then prefix all
of the Makefile commands below with `pipenv run`. Or start a virtualenv
session with `pipenv shell`.

# Workflow

Content is edited and added on the `source` branch, which has to be
pushed manually to the appropriate remote.  When you're ready to
publish, just run `make github`. Other useful commands are e.g. `make
html` (recompiles source), `make serve` (serves the website on
`localhost:8000` by default) and `make devserver` (recompiles source and
restarts server on each edit). For additional tips, see the
[documentation](http://docs.getpelican.com/en/3.6.3/publish.html).

# Tips

If you ever need to include HTML files verbatim, you need to add the
appropriate directory to `STATIC_PATHS` and also `READERS = {"html":
None}`. More at the bottom of [this
issue](https://github.com/getpelican/pelican/issues/1046).
