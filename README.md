# Generate site based on Markdown source

    $ cd ~/.virtualenvs/pelican
    $ . ./bin/activate
    (pelican)$ cd ~/Documents/dropbox/www/dlukes.github.io
    (pelican)$ pelican content/ -s publishconf.py
    (pelican)$ git add output
    (pelican)$ git commit
    (pelican)$ git push -u origin master
