html
  head
    ! simple test showing jinja2 templating at work.
    ! [if lt IE 9]> \
        <script src="fix_ie.js"></script> \
        <![endif]
  body
    h1 = Hi {{ name }}
    article
      h2 = cats:
      ul
        li .divider = Not autogen.
      {% for cat in cats %}
        li .{{ cat.color }} > a :href:"{{ cat.name |lower }}.html" \
            = A cat named {{ cat.name }}
      {% endfor %}
    footer \
      = and done.
