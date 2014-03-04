" Vim syntax file
" Language: Human Simplified HTML
" Maintainer: Daniel Fairhead
" Latest Revision: 20 February 2014

"if exists("b:current_syntax")
"  finish
"endif

" Keywords
syn keyword syntaxElementKeyword html head body div ul ol li span article header footer table thead tr td th tbody tfoot h1 h2 h3 h4 h5 h6 title link script nav a

syn region syntaxString start='"' end='"'
syn region syntaxArg start=':' end=':' nextgroup=syntaxArgValue

syn region syntaxPreProc start='{{' end='}}'

" syn match syntaxArgValue '[^ ]*'
syn match syntaxClass ' \.[^ ]*'
syn match syntaxId '#[^ ]*'
syn region syntaxContent start='=' end='[^\\]$' contains=syntaxPreProc
syn match syntaxPreProc '^#.*$'

" Matches
"syn match syntaxElementMatch 'regexp' contains=syntaxElement1 nextgroup=syntaxElement2 skipwhite

" Regions
"syn region syntaxElementRegion start='x' end='y'

let b:current_syntax = "hshtml"

hi def link syntaxElementKeyword Type
hi def link syntaxArg Statement
hi def link syntaxId Function
hi def link syntaxString String
hi def link syntaxClass String
hi def link syntaxArgValue String
hi def link syntaxContent Comment
hi def link syntaxPreProc PreProc
hi def link syntaxContains PreProc
