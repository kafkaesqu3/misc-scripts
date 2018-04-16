#!/bin/bash

#vim config
rm /root/.vimrc
echo set wildmenu >> /root/.vimrc
echo "set whichwrap+=<,>,h,l,[,]" >> /root/.vimrc
echo syntax on >> /root/.vimrc
echo set cursorline >> /root/.vimrc
echo set showmatch >> /root/.vimrc
echo set tabstop=4 >> /root/.vimrc
echo set shiftwidth=4 >> /root/.vimrc
echo set number >> /root/.vimrc
echo set wrap >> /root/.vimrc
echo set autoindent >> /root/.vimrc
echo set smartindent >> /root/.vimrc
echo set incsearch >> /root/.vimrc
echo set hlsearch >> /root/.vimrc
echo set ignorecase >> /root/.vimrc
echo set smartcase >> /root/.vimrc
echo set lazyredraw >> /root/.vimrc
echo set mouse=a >> /root/.vimrc

cat << EOF > /root/.screenrc
termcapinfo xterm* ti@:te@
startup_message off
vbell off
bell_msg 'Bell in window %n^G'
defscrollback 500
hardstatus off
altscreen on
EOF

cat << EOF >> /root/.bashrc
export EDITOR=vim

alias la='ls -a --color=auto'
alias ll='ls -l --color=auto'
alias ..='cd ..'
alias ...='cd ../../../'
alias ....='cd ../../../../'
alias .....='cd ../../../../'
alias .4='cd ../../../../'
alias .5='cd ../../../../..'
alias h='history'
alias j='jobs -l'
alias ports='netstat -tulnp'
alias listen='nc -nvlp'
alias processes='ps auwwx'
PS1='\[\033[01;31m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]$ '
EOF
