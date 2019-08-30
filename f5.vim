if !exists('g:ljl')
    let g:ljl = 0
endif
function! s:run_ljl() abort
    let l:self = expand('%:p')
    let l:self = substitute(l:self, '\\', '/', 'g')
    let l:cmd = printf('ljl %d "%s"', g:ljl, l:self)
    " echo l:cmd
    let l:out = system(l:cmd)
    echo l:out
endfunction
nnoremap <F5> :call <SID>run_ljl()<CR>

