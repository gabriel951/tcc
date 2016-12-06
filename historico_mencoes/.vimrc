"my vimrc. Vim is nice :)"

"--------------------------------- VUNDLE ---------------------------"
set nocompatible              " be iMproved, required
filetype off                  " required

" set the runtime path to include Vundle and initialize
set rtp+=~/.vim/bundle/Vundle.vim
call vundle#begin()
" alternatively, pass a path where Vundle should install plugins
"call vundle#begin('~/some/path/here')

" let Vundle manage Vundle, required
Plugin 'VundleVim/Vundle.vim'

" The following are examples of different formats supported.
" Keep Plugin commands between vundle#begin/end.

Plugin 'scrooloose/nerdtree'
"Plugin 'scrooloose/syntastic'
Plugin 'Valloric/YouCompleteMe'
Plugin 'tpope/vim-surround'
Plugin 'SirVer/ultisnips'

" All of your Plugins must be added before the following line
call vundle#end()            " required
filetype plugin indent on    " required
" To ignore plugin indent changes, instead use:
"filetype plugin on
"
" Brief help
" :PluginList       - lists configured plugins
" :PluginInstall    - installs plugins; append `!` to update or just :PluginUpdate
" :PluginSearch foo - searches for foo; append `!` to refresh local cache
" :PluginClean      - confirms removal of unused plugins; append `!` to auto-approve removal
"
" see :h vundle for more details or wiki for FAQ
" Put your non-Plugin stuff after this line

"-------------------------------- VUNDLE ----------------------------"

"------------------------------ MY PREFERENCES ----------------------"
set incsearch 
set hlsearch
set mouse=a 
set foldmethod=indent

"------------------------------ TAB WHITE-SPACE ---------------------"
"solving the tab white-space problem"
filetype plugin indent on
" show existing tab with 4 spaces width
set tabstop=4
" when indenting with '>', use 4 spaces width
set shiftwidth=4
" On pressing tab, insert 4 spaces
set expandtab
"------------------------------ TAB WHITE-SPACE ---------------------"

"----------------------------- MAPPING ENTER ------------------------"
nmap <CR> o<Esc>

"----------------------------- MAPPING tab-switch ------------------------"
nmap <C-l> gt
nmap <C-h> gT

"----------------------------- YCM FIX ------------------------------"
let g:ycm_global_ycm_extra_config =  '~/.vim/bundle/YouCompleteMe/third_party/ycmd/cpp/ycm'
" this is causing the autocompletion for ycm not to work let g:ycm_python_binary_path = 'python3'
" this is causing the autocompletion for ycm not to work 
" let g:ycm_path_to_python_interpreter = 'python3'
"--------------------------------------------------------------------"

"----------------------------- Ultisnips ------------------------------"
let g:letUltiSnipsEditSplit="vertical"
let g:UltiSnipsExpandTrigger="<c-j>"
"----------------------------- Ultisnips ------------------------------"
