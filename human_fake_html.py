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

import shlex

def read_joined(filename):
    ''' reads a file, joining \ ended lines. '''

    multiline_buffer = []
    with open(filename,'r') as f:
        for line in [l.rstrip() for l in f]:

            if not line.strip():
                continue
            if line[-1] == '\\':
                multiline_buffer.append(line[:-1])
                continue

            if multiline_buffer:
                multiline_buffer.append(line)
                yield ' '.join(multiline_buffer)
                multiline_buffer = []
            else:
                yield line

def read(filename, ts=2):
    ''' reads a file (with read_joined), yielding:
        [(indent, text)...] '''

    for line in [l.expandtabs(ts) for l in read_joined(filename)]:
        stripped = line.lstrip()
        yield len(line) - len(stripped), stripped

def parse(filename):
    ''' reads a file, returns a [] based parse tree. '''

    base = []
    indent_stack = [0]
    item_stack = [base]

    for indent, line in read(filename):
        if indent > indent_stack[-1]:
            indent_stack.append(indent)
            item_stack.append(item_stack[-1][-1])

        elif indent < indent_stack[-1]:
            while ( indent < indent_stack[-1] ):
                indent_stack.pop()
                item_stack.pop()

        if '>' in line:
            splitline = line.split('>')
            line = splitline.pop().strip()
            for thing in reversed(splitline):
                line = [thing.strip(), [line]]
            item_stack[-1].append(line)
        else:
            item_stack[-1].append([line])

    return base

def render(parsed):
    ''' takes a [] parse tree, returns straight HTML '''

    base = parsed.pop(0)

    if base[0] == '=':
        return base[1:]
    if parsed:
        bits = [render(x) for x in parsed]
    else:
        bits = []
   
    print base
    if not base:
        return ''
    elif base[0] == '=':
        return base[1:]
    elif base[0] == '!':
        return '<!-- ' + base[1:] + '-->'
    if '=' in shlex.split(base):
        tag_info, tag_contents = base.split('=',1)
    else:
        tag_info = base
        tag_contents = ''

    parts = shlex.split(tag_info) #.split()
    tag = parts.pop(0)

    tag_vars = []

    for var in parts:
        if var.startswith('#'):
            tag_vars.append(('id', var[1:]))
        if var.startswith('.'):
            tag_vars.append(('class', ' '.join(var[1:].split('.'))))
        if var.startswith(':'):
            tag_vars.append(var[1:].split(':'))
            
    parts_text = ' '.join([ (x[0] + '="' + x[1] + '"') for x in tag_vars])

    return '<' + tag + (' ' if parts_text else '') + parts_text + '>' \
            + (''.join(bits)) + tag_contents.strip() \
            + '</' + tag + '>'


if __name__ == '__main__':
    import sys

    x = parse(sys.argv[1])
    print '<!doctype html>',render(x[0])
