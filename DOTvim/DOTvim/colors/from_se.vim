""https://stackoverflow.com/questions/2019281/load-different-colorscheme-when-using-vimdiff
""cterm - sets the style
""ctermfg - set the text color
""ctermbg - set the highlighting
""DiffAdd - line was added
""DiffDelete - line was removed
""DiffChange - part of the line was changed (highlights the whole line)
""DiffText - the exact part of the line that changed
""highlight DiffAdd    cterm=bold ctermfg=190 ctermbg=17 gui=none guifg=bg guibg=Red
""highlight DiffDelete cterm=bold ctermfg=190 ctermbg=17 gui=none guifg=bg guibg=Red
""highlight DiffChange cterm=bold ctermfg=190 ctermbg=17 gui=none guifg=bg guibg=Red
""highlight DiffText   cterm=bold ctermfg=190 ctermbg=88 gui=none guifg=bg guibg=Red
hi DiffText   cterm=none ctermfg=Black ctermbg=Red gui=none guifg=Black guibg=Red
hi DiffChange cterm=none ctermfg=Black ctermbg=LightMagenta gui=none guifg=Black guibg=LightMagenta
