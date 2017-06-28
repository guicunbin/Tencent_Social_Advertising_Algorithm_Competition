#bash ./sort.sh ./train/train_ad_user_position.csv 27 ./train/train_ad_user_position_sorted_by_appID.csv
# 不知道为什么上面的命令在header 的前面多出了好多行，再将前面的删掉后就可以了
bash ./join.sh ./train/train_ad_user_position_sorted_by_appID.csv 27 \
./train/app_categories.csv 1 \
./train/train_ad_user_position_appCates.csv
