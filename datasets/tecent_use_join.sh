##### 测试
#python use_join.py \
#        ./tb_1.csv \
#        ./tb_2.csv \
#        ./tb_12.csv \
#        a
##############################################
#
#
#
#sleep 30
#
#python use_join.py \
#        ./train/test.csv \
#        ./train/ad.csv \
#        ./train/test_ad.csv \
#        creativeID
#
#sleep 30
#
#python use_join.py \
#        ./train/test_ad.csv \
#        ./train/user.csv \
#        ./train/test_ad_user.csv \
#        userID
#
#
#sleep 30
#
#
#python use_join.py \
#        ./train/test_ad_user.csv \
#        ./train/position.csv \
#        ./train/test_ad_user_position.csv \
#        positionID
#
#sleep 30
#
## 这段程序执行的结果多出了400行左右，经过排查是排序的时候出错了，因此将sort和join分开进行，将sort的结果文件删掉400多行之后就可以了
#python use_join.py \
#        ./train/test_ad_user_position.csv \
#        ./train/app_categories.csv \
#        ./train/test_ad_user_position_appCates.csv \
#        appID
#
#sleep 30
#
#python use_join.py \
#        ./train/test_ad_user_position_appCates.csv \
#        ./train/tb_user_app_actions_add_one_column.csv \
#        ./train/test_ad_user_position_appCates_act.csv \
#        appID userID


sleep 30

python use_join.py \
        ./train/test_ad_user_position_appCates_act.csv \
        ./train/tb_user_installedapps_add_one_column.csv \
        ./train/test_ad_user_position_appCates_act_Install.csv \
        appID userID







#########################  for train   ##############################




#sleep 30
#
#python use_join.py \
#        ./train/train.csv \
#        ./train/ad.csv \
#        ./train/train_ad.csv \
#        creativeID
#
#sleep 30
#
#python use_join.py \
#        ./train/train_ad.csv \
#        ./train/user.csv \
#        ./train/train_ad_user.csv \
#        userID
#
#
#sleep 30
#
#
#python use_join.py \
#        ./train/train_ad_user.csv \
#        ./train/position.csv \
#        ./train/train_ad_user_position.csv \
#        positionID
#
#sleep 30
#
## 这段程序执行的结果多出了400行左右，经过排查是排序的时候出错了，因此将sort和join分开进行，将sort的结果文件删掉400多行之后就可以了
#python use_join.py \
#        ./train/train_ad_user_position.csv \
#        ./train/app_categories.csv \
#        ./train/train_ad_user_position_appCates.csv \
#        appID
#
#sleep 30
#
#python use_join.py \
#        ./train/train_ad_user_position_appCates.csv \
#        ./train/tb_user_app_actions_add_one_column.csv \
#        ./train/train_ad_user_position_appCates_act.csv \
#        appID userID
#

sleep 30

python use_join.py \
        ./train/train_ad_user_position_appCates_act.csv \
        ./train/tb_user_installedapps_add_one_column.csv \
        ./train/train_ad_user_position_appCates_act_Install.csv \
        appID userID



