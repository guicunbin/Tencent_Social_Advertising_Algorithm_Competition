csv1=$1
k1=$2
csv2=$3
k2=$4
csvout=$5
join --header -t',' -1 $k1 -2 $k2 -a 1  $csv1  $csv2 >$csvout
