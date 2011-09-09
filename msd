#!/bin/tcsh
set steps = `cat OutputLog |awk '{print $3}'`
set skip_restarters = yes
if ( $1 == '-all' )  set skip_restarters = no
set last = `LastStep`   
echo $last
foreach i ($steps)
    if( "$skip_restarters" == "yes" && "$i" == "data0000" ) then
        continue
    endif
    if( $skip_restarters == yes && $i == $last ) then
        continue
    endif

    set number = `echo $i | sed -e 's,.*\([[:digit:]]\{4\}\).*,\1,'`
    set prefix = `echo $i | sed -e 's,\(.*\)[[:digit:]]\{4\}.*,\1,'`
    if( $prefix == 'data' ) then
        set dirname = 'DD'
    else if ( $prefix == 'time' ) then
        set dirname = 'TD'
    else if ( $prefix == 'cycle' ) then
        set dirname = 'CD'
    endif
    echo $dirname$number/$i
    if( ! -e $dirname$number ) mkdir $dirname$number
    if( -e $i ) mv $i* $dirname$number

end
#end
