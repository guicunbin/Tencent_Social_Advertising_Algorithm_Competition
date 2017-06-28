csv1=$1
k1=$2
csv2=$3
k2=$4
csvout=$5
# --header 保留header   
# -a 1 第二个文件没有匹配的也打印出来，就是left outer join 
# 必须有sort, 否则打印的全是NAN
#sort -t',' -k${k1}n,$k1 $csv1
#sort -t',' -k${k2}n,${k2} $csv2
join --header -t',' -1 $k1 -2 $k2 -a 1  <(sort -t , -n -k ${k1},$k1 $csv1) <(sort -t , -n -k ${k2},$k2 $csv2) >$csvout
#sort -t , -k 1,1 -n

