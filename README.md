# Human Fake HTML

A very simple demo library which turns space-indented simple HTML into
proper HTML.

## Example Syntax:

    html
      head
        title = stuff
        link :rel:stylesheet :url:/css/main.css
      body .normal
        header #bodyheader
          h1 = Site Title
        article .main
          h2 = article title about cats
          div .cats_article
            = This is the first line of the actual article text.
            = And another line... \
              Wrapping around
            a :href:www.facebook.com = Cats Love Facebook
            = or so I am lead to believe...
        footer #bodyfooter
          nav
            ul
              li > a :href:index.html = Home
              li > a :href:about.html = About us
              li > a :href:details.html = Details

which then resolves into something like:

    <html>
        <head>
            <title>stuff</title>
            <link rel="stylesheet" url="/css/main.css"></link>
        </head>
        <body class="normal">
            <header id="bodyheader">
                <h1>Site Title</h1>
            </header>
            <article class="main">
                <h2>article title about cats</h2>
                <div class="cats_article">
                    This is the first line of the actual article text.
                    And another line... Wrapping around
                    <a href="www.facebook.com">Cats Love Facebook</a>
                    or so I am lead to believe...
                </div>
            </article>
            <footer id="bodyfooter">
                <nav>
                    <ul>
                        <li><a href="index.html">Home</a></li>
                        <li><a href="about.html">About us</a></li>
                        <li><a href="details.html">Details</a></li>
                    </ul>
                </nav>
            </footer>
        </body>
    </html>


Possibly something I may use as part of a larger project, one day.

GPL2.0 Licenced. (C) 2014 Daniel Fairhead
