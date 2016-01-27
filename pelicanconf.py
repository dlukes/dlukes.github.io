AUTHOR = "dlukes"
SITENAME = "Little Umbrellas"
SITEURL = "http://dlukes.github.io"

TIMEZONE = "Europe/Prague"

DEFAULT_LANG = "en"

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

# But tags are
DISPLAY_TAGS_ON_SIDEBAR = True

# Tipue search
DIRECT_TEMPLATES = ["index", "tags", "categories", "archives", "search"]

# Blogroll
LINKS = (("Czech National Corpus", "http://www.korpus.cz"),
         ("My academic homepage", "http://trnka.korpus.cz/~lukes/"),
         ("A blonde in Poland", "http://wodymarcowe.blogspot.cz"),
         ("xkcd", "http://xkcd.com"),
         ("Perry Bible Fellowship", "http://pbfcomics.com"),
         ("PhD Comics", "http://phdcomics.com/comics.php"))


# Social widget
SOCIAL = (("github", "https://github.com/dlukes"),
          ("stack overflow", "http://stackoverflow.com/users/1826241/dlukes", "stack-overflow"),
          ("g+", "https://plus.google.com/+DavidLukešDvl", "google-plus"),
          ("facebook", "https://www.facebook.com/fyodor.konstantinovitch.cherdyntsev"))

# Eyebrows
AVATAR = "/images/avatar.jpeg"
ABOUT_ME = "Language tourist, Python enthusiast & Frank Zappa aficionado"
FAVICON = "images/favicon.ico"
PYGMENTS_STYLE = "zenburn"
THEME="pelican-bootstrap3"
DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

# Redirection for URLs with former output/ doc root
STATIC_PATHS = ["images", "output"]

# Pplugin
MARKUP = ("md", "ipynb")
PLUGIN_PATHS = ["pelican-plugins"]
PLUGINS = ["liquid_tags.notebook", "tag_cloud", "tipue_search"]

CC_LICENSE = "CC-BY-NC-SA"
