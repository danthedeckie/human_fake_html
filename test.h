html .nojs.article
  head
    title = stuff
    link :rel:stylesheet :url:/css/main.css
    script :src:/js/jquery.js
    script :src:/js/main.js
  body .normal.single
    div #content
      header #mainheader
        h1 :data-el:"Data element for h1 title" = Site title.
        nav .main_nav
          ul :class:"This is a class list"
            li > a :href:index.html = Home
            li > a :href:about_us.html = About Us
            li \
                > a :href:links.html \
                = Links
      article #stuff
        header #things
          h1 = Article Header
        div .article_text
          = This is the article actual text.
          a :href:link.html a link.
          = and more text. \
            and more. \
            and more!

      footer #mainfooter
    
