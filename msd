#!/bin/tcsh
#set echo
set steps = `cat OutputLog |awk '{print $3}'`
set skip_restarters = yes
if ( $1 == '-all' )  set skip_restarters = no
set last = `LastStep`   
#echo $last
#echo $steps
foreach i ($steps)
    if( "$skip_restarters" == "yes" && "$i" == "data0000" ) then
        continue
    endif
    if( "$skip_restarters" == "yes" && "$i" == "$last" ) then
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
    else
        echo "Unknown prefix for " $i "skipping"
        continue
    endif
    echo $dirname$number/$i `date`
    if( ! -e $dirname$number && -e $i ) mkdir $dirname$number
    #if( -e $i ) mv $i* $dirname$number
    if ( -e $i )  then
        echo Moving $i $dirname$number
        foreach file ( `lusg $i` )
            mv $file $dirname$number
        end
    endif

end
#end
