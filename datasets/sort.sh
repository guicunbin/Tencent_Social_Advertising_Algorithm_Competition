csv1=$1
k1=$2
csvout=$3
sort -t , -n -k ${k1},$k1 $csv1 -o $csvout

