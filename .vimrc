set nocindent
set nu
set nowrap
set noexpandtab
set autoindent
set shiftwidth=8
"set smartindent
filetype plugin indent on
set mouse=hvi
syntax enable

" Highlight trailing whitespace and tabs
highlight link RedundantSpaces Error
au BufEnter,BufRead * match RedundantSpaces "\t"
au BufEnter,BufRead * match RedundantSpaces "[[:space:]]\+$"

" Set default sh to bash
let g:is_sh	   = 1
