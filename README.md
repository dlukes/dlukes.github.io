# How this works

Content is edited and added on the `source` branch, which has to be pushed
manually to the appropriate remote. When you're ready to publish, just run `make
github`. Other useful command are e.g. `make serve` (serves the website on
`localhost:8000` by default). For additional tips, see
the [documentation](http://docs.getpelican.com/en/3.6.3/publish.html).

# Tips

If you ever need to include HTML files verbatim, you need to add the appropriate
directory to `STATIC_PATHS` and also `READERS = {"html": None}`. More at the
bottom of [this issue](https://github.com/getpelican/pelican/issues/1046).
