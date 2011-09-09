#! /bin/csh
if( $1 == "" ) then
    emacs &
else   
emacs $1 -name $1 -fn 10x20 &
endif
echo Yo

