csv1=$1
k11=$2
k12=$3
csv2=$4
k21=$5
k22=$6
csvout=$7
fields=$8
# --header header不加入比较   
# -a 1 第二个文件没有匹配的也打印出来，就是left outer join 
# 必须有sort, 否则打印的全是NAN
#cat $csv1 | awk -F',' '{print $'${k11}'"-"$'${k12}'","$0}' #| sort -t',' -k1n,1

join --header -j1 -t',' -a 1 -o $fields \
<(<$csv1 awk -F',' '{print $'${k11}'"-"$'${k12}'","$0}' | sort -t , -n -k 1,1) \
<(<$csv2 awk -F',' '{print $'${k21}'"-"$'${k22}'","$0}' | sort -t , -n -k 1,1) \
>$csvout

