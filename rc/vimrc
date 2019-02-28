"install pathogen:
"mkdir -p ~/.vim/autoload ~/.vim/bundle && \
"curl -LSso ~/.vim/autoload/pathogen.vim https://tpo.pe/pathogen.vim

" install vundle
" git clone https://github.com/VundleVim/Vundle.vim.git ~/.vim/bundle/Vundle.vim

" infect file for easy plugin installation into ~/.vim/bundle
" execute pathogen#infect()

" required for Vundle
"set nocompatible              " be iMproved, required
"filetype off                  " required
"set rtp+=~/.vim/bundle/Vundle.vim
"call vundle#begin()
"Plugin 'VundleVim/Vundle.vim'
" OTHER PLUGINS HERE
"call vundle#end()            " required
"let g:ycm_global_ycm_extra_conf = "~/.vim/.ycm_extra_conf.py"
"filetype plugin indent on    " required

" automatically close quotes, brackets, parens, etc
" git clone https://github.com/vim-scripts/delimitMate.vim.git ~/.vim/bundle/delimitMate.vim

" VIM OPTIONS
set wildmenu                    " Better command-line completion
" may require install the packages vim-gtk or vim-gnome in debian or vim-X11/vimx in CentOS
set clipboard=unnamedplus " use system clipboard

" NAVIGATION
set whichwrap+=<,>,h,l,[,]      " enables line wrapping via left/right keys at end of a line

" COLORS/HIGHLIGHTIHNG
syntax on                       " enable syntax processing
set cursorline                  " highlight current line
set showmatch                   " highlight matching [{()}]

" FORMATTING
set tabstop=4                   " number of visual spaces per TAB
set shiftwidth=4                " sets tabs for tab/auto indentation
set number                      " show line numbers
set wrap                        " long lines wrap to next line
"filetype indent on             " load filetype-specific indent files
set autoindent                  " indentation inherited from previous line
set smartindent

" SEARCH
set incsearch                   " search as characters are entered
set hlsearch                    " highlight matches
set ignorecase
set smartcase                   " searches all in lowercase become case insensitive

" PERFORMANCE
set lazyredraw

" OTHER
set mouse=a                             " this lets me scroll from putty while in GNU screen

" KEY MAPPINGS
nnoremap <buffer> <F5> :w <bar> exec '!python' shellescape(@%, 1)<cr> "execute python script when pressing f5

" Powerline
" pip install powerline-status
" wget https://github.com/powerline/powerline/raw/develop/font/PowerlineSymbols.otf
" wget https://github.com/powerline/powerline/raw/develop/font/10-powerline-symbols.conf
" mv PowerlineSymbols.otf ~/.fonts/
" fc-cache -vf ~/.fonts/
" mv 10-powerline-symbols.conf ~/.config/fontconfig/conf.d/
" set rtp+=/usr/local/lib/python2.7/dist-packages/powerline/bindings/vim/
" Always show statusline
" set laststatus=2
