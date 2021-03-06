set nocindent
set nu
set nowrap
set autoindent
set shiftwidth=4 ts=4 et
set incsearch hlsearch
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

function! s:DiffWithSaved()
    let filetype=&ft
    diffthis
    vnew | r # | normal! 1Gdd
    diffthis
    exe "setlocal bt=nofile bh=wipe nobl noswf ro ft=" . filetype
endfunction
com! DiffSaved call s:DiffWithSaved()

"Will allow you to use :w!! to write to a file using sudo if you forgot to
""sudo vim file" (it will prompt for sudo password when writing)
cmap w!! %!sudo tee > /dev/null %

autocmd FileType python set omnifunc=pythoncomplete#Complete
