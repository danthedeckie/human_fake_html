#!./.virtualenv/bin/python

from jinja2 import Template
from human_fake_html2 import convert

with open('jin_template.h','r') as f:
    temp = Template(f.read())

post_template =  temp.render(name='Daniel',
                    cats=[{"name": 'Cleo', "color": "black"},
                          {"name": 'Sophia', "color": "tortoise-shell"},
                          {"name": 'Jemima', "color": "dark-speckled"},
                          {"name": 'Tessa', "color": "white-and-orange"}])

print convert(post_template)
