#!/usr/bin/python
'''
    (C) 2014 Daniel Fairhead

    Very simple demo parser for simplified HTML syntax.

    Supports:

    indented
      levels
        of
          things

    which is then turned into a HTML tree.

    item #id .class.list

    item > subitem

    item = text contents of item

    item #title \
       .this.is.the.same.item.joined.with.backslash

    item :src:attributes :are:"encoded this way"

'''

from collections import namedtuple

# Simple Nestable DOM Element:
DomEl = namedtuple('DomEl', 'details children')


def tokenize(text):
    ''' given a block of "human" tml, return a list of tokens, ready for
        parsing.  joins escaped newlines, "quotes \"escaping\" works", etc. '''
    inside = None
    start = 0
    escaped = False
    text = '\n' + text

    for position, byte in enumerate(text):

        # escaping:
        if byte == '\\':
            escaped = not escaped
            continue

        # quoted text counts as continuous:
        if inside == '"':
            if not start:
                start = position
            if byte == '"' and not escaped:
                inside = None
                continue
            else:
                continue

        # newlines:
        if byte == '\n':
            if escaped:
                escaped = not escaped
                continue
            else:
                yield text[start:position]
                inside = byte
                start = position

        # spaces:
        elif byte == ' ':
            if start and inside != '\n':
                yield text[start:position]
                start = False
            elif inside == '\n':
                continue
            else:
                continue

        # regular characters:
        else:
            if not start:
                start = position

            if byte == '"':
                inside = '"'
                continue
            elif inside == '\n':
                yield text[start:position]
                inside = None
                start = position

def line_tokenize(text):
    """
        given a block of "human" tml text, chuck it through the tokenizer,
        and separate it into individual lines. Also joins together all tokens
        after a = into a single item.
    """
    current_line = []
    after_equals = False
    for block in tokenize(text):
        if block.startswith('\n'):
            if len(current_line) > 1:
                if after_equals != False:
                    current_line.append(' '.join(after_equals))
                    after_equals = False
                yield current_line
            current_line = [block[1:]]
        elif after_equals != False:
            after_equals.append(block)
        else:
            if block == '=':
                after_equals = []
                current_line.append(block)
            elif len(block):
                current_line.append(block)


def parse(text, ts=2):
    ''' given a block of 'human' TML text, lex and parse it, returning a
        DomEl Tree '''

    base = DomEl([], [])
    indent_stack = [0]
    item_stack = [base]

    lines = line_tokenize(text)

    for line in lines:
        if not line[0].strip():
            indent = len(line.pop(0).expandtabs(ts))
        else:
            indent = 0

        while indent < indent_stack[-1]:
            indent_stack.pop()
            item_stack.pop()

        new_indent = indent > indent_stack[-1]
        if new_indent:
            item_stack.append(item_stack[-1].children[-1])
            indent_stack.append(indent)

        if '=' in line[1:]:
            index = line.index('=')
            line = line[:index] + ['>'] + line[index:]

        if '>' in line:
            parent = item_stack[-1]

            while '>' in line:
                chevron = line.index('>')
                item = DomEl(line[0:chevron], [])
                # item = l[0:chevron] # list containing list (up to >)
                # remove from front of this line:
                line = line[chevron+1:]
                # add to stacks:
                parent.children.append(item)
                parent = item

            parent.children.append(DomEl(line, []))

        else:
            # full line w/o >:

            item = DomEl(line, [])
            item_stack[-1].children.append(item)

    return base

def parse_file(filename, ts=2):
    ''' take a filename, and parse the contents, returning a DomEl tree '''
    with open(filename, 'r') as f:
        return parse(f.read())

def render(parsed):
    ''' takes a DomEl parse tree, returns straight HTML (recursive) '''

    details = parsed.details
    children = parsed.children

    if details[0] == '=':
        return details[1]

    if children:
        rendered_children = [render(x) for x in children]
    else:
        rendered_children = []

    if details[0] == '!':
        return '<!-- ' + details[1:] + '-->'
    else:
        tag_info = details
        tag_contents = ''

    tag = details.pop(0)

    tag_vars = []

    for var in details:
        if var.startswith('#'):
            tag_vars.append(('id', var[1:]))
        if var.startswith('.'):
            tag_vars.append(('class', ' '.join(var[1:].split('.'))))
        if var.startswith(':'):
            tag_vars.append(var[1:].split(':', 1))
            if tag_vars[-1][-1][-1] == '"':
                tag_vars[-1][-1] = tag_vars[-1][-1][1:-1]

    parts_text = ' '.join([ (x[0] + '="' + x[1] + '"') for x in tag_vars])

    return '<' + tag + (' ' if parts_text else '') + parts_text + '>' \
            + (''.join(rendered_children)) + tag_contents.strip() \
            + '</' + tag + '>'


if __name__ == '__main__':
    import sys

    if sys.argv[1] != '-p':

        x = parse_file(sys.argv[1])

        print '<!doctype html>', render(x.children[0])

    else:
        from lxml import etree, html
        out = render(parse_file(sys.argv[2]).children[0])
        root = html.fromstring(out)
        print '<!doctype html>', etree.tostring(root, encoding='unicode',
            pretty_print=True)
