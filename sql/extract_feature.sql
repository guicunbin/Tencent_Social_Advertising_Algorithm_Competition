-- App开发者设定的App类目标签，类目标签有两层，使用3位数字编码，百位数表示一级类目，十位个位数表示二级类目，
-- “210”表示一级类目编号为2，二级类目编号为10，类目未知或者无法获取时，标记为0。
--#TODO 现在就是可以提取多个rank 类型的特征，click_day_rank_by_UC,  
--# click_day_rank_by_U,  click_day_by_C(U userID, C creativeID,甚至还可以是positionID, appID......)
--# 或者这样起个名字，userID_click_day_hour_minu_s1_rank,   userID_creativeID_click_day_hour_minu_s1_rank,
--# 观察一个特征强不强的标志就是，在该feature的各个取值上面，label=1和label=0的占比是否不均匀,
--# 比如click_day_rank,那就group by click_day_rank,label 看看分布情况,最好是先取出一个tb_train_tiny 来做特征测试 
--# python Df.plot() 或者 mysql  select feat,label count(*) from tb group by feat,label
--#+----------------+-------+----------+ 就比如左图这个分布，很明显 click_day_rank是一个强特征,因为click_day_rank=0几乎是 label=1的必要条件
--#| click_day_rank | label | count(*) |
--#+----------------+-------+----------+
--#|              0 |     0 |    97038 |
--#|              0 |     1 |     2944 |
--#|              1 |     0 |       18 |
--#+----------------+-------+----------+
--           dateset3: 31 ,features3 from 21~30
--           dateset2: 28 ,features2 from 18~27  
--           dateset1: 27 ,features1 from 17~26        



use tecent_2017_06;
--# --## tb_user_installedapps_add_one_column
--# create table if not exists tb_user_installedapps_add_one_column as
--# select userID,  appID,  1 as is_installed_this_app_long
--# from tb_user_installedapps;
--# create index index0 on tb_user_installedapps_add_one_column (userID,appID);
--# 
--# 
--# --## tb_user_app_actions_add_one_column
--# create table if not exists tb_user_app_actions_add_one_column as
--# select userID,  appID,  installTime,
--# cast(installTime / 1000000 as unsigned) as install_day
--# from tb_user_app_actions;
--# create index index0 on tb_user_app_actions_add_one_column (userID,appID);
--# 
--#create index index0 on tb_ad                (creativeID);
--#create index index0 on tb_user              (userID);
--#create index index0 on tb_position          (positionID);
--#create index index0 on tb_app_categories    (appID);
--# 
--# 
--# --######## for tb_test ###########
--# create table if not exists tb_test_temp1 as 
--# select instanceID, label, clickTime, creativeID, userID, positionID, connectionType, telecomsOperator, idx_tb_test,
--# cast(substr(clickTime,1,2) as unsigned) as click_day,
--# cast(substr(clickTime,1,4) as unsigned) as click_day_hour,
--# cast(substr(clickTime,1,6) as unsigned) as click_day_hour_minu,
--# cast(substr(clickTime,1,7) as unsigned) as click_day_hour_minu_s1
--# from tb_test;
--# create index index0 
--# on tb_test_temp1 (clickTime,creativeID,userID,click_day,click_day_hour,click_day_hour_minu,click_day_hour_minu_s1,idx_tb_test);
--# create index index1 on tb_test_temp1 (label);
--# 
--# 
--# --#--# for click_day_rank
--# create table tb_test_temp11 as  
--# SELECT idx_tb_test,   label,
--#      CASE when click_day = @cur0 and creativeID = @cur1  and userID = @cur2 
--#         THEN @curRow := @curRow + 1 ELSE @curRow := 0 END AS click_day_rank,
--#      @cur0 :=  click_day     AS click_day,
--#      @cur1 :=  creativeID    AS creativeID,
--#      @cur2 :=  userID        AS userID
--# FROM tb_test_temp1 t
--# JOIN (SELECT @curRow := 0, @cur0 := '') r
--# ORDER BY idx_tb_test,  click_day,  creativeID,  userID;
--# 
--# 
--# --#--# for click_day_hour_rank
--# create table tb_test_temp12 as  
--# SELECT idx_tb_test,   label,
--#      CASE when click_day_hour = @cur0 and creativeID = @cur1  and userID = @cur2 
--#         THEN @curRow := @curRow + 1 ELSE @curRow := 0 END AS click_day_hour_rank,
--#      @cur0 :=  click_day_hour     AS click_day_hour,
--#      @cur1 :=  creativeID    AS creativeID,
--#      @cur2 :=  userID        AS userID
--# FROM tb_test_temp1 t
--# JOIN (SELECT @curRow := 0, @cur0 := '') r
--# ORDER BY idx_tb_test,  click_day_hour,  creativeID,  userID;
--# 
--# 
--# --#--# for click_day_hour_minu_rank
--# create table tb_test_temp13 as  
--# SELECT idx_tb_test,   label,
--#      CASE when click_day_hour_minu = @cur0 and creativeID = @cur1  and userID = @cur2 
--#         THEN @curRow := @curRow + 1 ELSE @curRow := 0 END AS click_day_hour_minu_rank,
--#      @cur0 :=  click_day_hour_minu     AS click_day_hour_minu,
--#      @cur1 :=  creativeID    AS creativeID,
--#      @cur2 :=  userID        AS userID
--# FROM tb_test_temp1 t
--# JOIN (SELECT @curRow := 0, @cur0 := '') r
--# ORDER BY idx_tb_test,  click_day_hour_minu,  creativeID,  userID;
--# 
--# 
--# --#--# for click_day_hour_minu_s1_rank
--# create table tb_test_temp14 as  
--# SELECT idx_tb_test,   label,
--#      CASE when click_day_hour_minu_s1 = @cur0 and creativeID = @cur1  and userID = @cur2 
--#         THEN @curRow := @curRow + 1 ELSE @curRow := 0 END AS click_day_hour_minu_s1_rank,
--#      @cur0 :=  click_day_hour_minu_s1     AS click_day_hour_minu_s1,
--#      @cur1 :=  creativeID    AS creativeID,
--#      @cur2 :=  userID        AS userID
--# FROM tb_test_temp1 t
--# JOIN (SELECT @curRow := 0, @cur0 := '') r
--# ORDER BY idx_tb_test,  click_day_hour_minu_s1,  creativeID,  userID;
--# 
--# 
--# 
--# --#--# for clickTime_rank
--# create table tb_test_temp15 as  
--# SELECT idx_tb_test,   label,
--#      CASE when clickTime = @cur0 and creativeID = @cur1  and userID = @cur2 
--#         THEN @curRow := @curRow + 1 ELSE @curRow := 0 END AS clickTime_rank,
--#      @cur0 :=  clickTime     AS clickTime,
--#      @cur1 :=  creativeID    AS creativeID,
--#      @cur2 :=  userID        AS userID
--# FROM tb_test_temp1 t
--# JOIN (SELECT @curRow := 0, @cur0 := '') r
--# ORDER BY idx_tb_test,  clickTime,  creativeID,  userID;
--# 
--# 
--# create index index0 on tb_test_temp11 (idx_tb_test);
--# create index index0 on tb_test_temp12 (idx_tb_test);
--# create index index0 on tb_test_temp13 (idx_tb_test);
--# create index index0 on tb_test_temp14 (idx_tb_test);
--# create index index0 on tb_test_temp15 (idx_tb_test);
--# --# merge rank_feats to one table
--# create table if not exists tb_test_merge_temp1 as 
--# select t1.*,
--# click_day_rank,
--# click_day_hour_rank,
--# click_day_hour_minu_rank
--# from tb_test_temp1  t1 
--# join tb_test_temp11 t11 on t1.idx_tb_test = t11.idx_tb_test
--# join tb_test_temp12 t12 on t1.idx_tb_test = t12.idx_tb_test
--# join tb_test_temp13 t13 on t1.idx_tb_test = t13.idx_tb_test;
--# create index index0 on tb_test_merge_temp1 (idx_tb_test);
--# 
--# 
--# create table if not exists tb_test_merge as 
--# select t.*,
--# case when click_day                 = 0 then 0 else 1 end as click_day_rank_bool,
--# case when click_day_hour            = 0 then 0 else 1 end as click_day_hour_rank_bool,
--# case when click_day_hour_minu       = 0 then 0 else 1 end as click_day_hour_minu_rank_bool,
--# case when click_day_hour_minu_s1    = 0 then 0 else 1 end as click_day_hour_minu_s1_rank_bool,
--# case when clickTime                 = 0 then 0 else 1 end as clickTime_rank_bool
--# from 
--# (
--# select t1.*,
--# click_day_hour_minu_s1_rank,
--# clickTime_rank
--# from tb_test_merge_temp1 t1
--# join tb_test_temp14 t14 on t1.idx_tb_test = t14.idx_tb_test
--# join tb_test_temp15 t15 on t1.idx_tb_test = t15.idx_tb_test
--# )t;
--# create index index0 on tb_test_merge (idx_tb_test, creativeID,    userID);
--#
--#
--#--## merge tb_test_ad_user
--#create table if not exists tb_test_ad_user as
--#select t1.*,
--#adID,  camgaignID,  advertiserID,  appID,  appPlatform,
--#age,  gender,  education,  marriageStatus,  haveBaby,  hometown, residence
--#from tb_test_merge t1
--#join tb_ad          t2 on t1.creativeID = t2.creativeID
--#join tb_user        t3 on t1.userID     = t3.userID;
--#create index index0 on tb_test_ad_user (positionID, appID);
--#
--#
--#--## merge tb_test_ad_user_position_appCates
--#create table if not exists tb_test_ad_user_position_appCates as 
--#select t1.*,
--#sitesetID,  positionType, appCategory,
--#cast(appCategory / 100 as unsigned) as appCategory_1,
--#appCategory % 100 as appCategory_2
--#from tb_test_ad_user   t1
--#join tb_position        t2 on t1.positionID = t2.positionID
--#join tb_app_categories  t3 on t1.appID      = t3.appID;
--#create index index0 on tb_test_ad_user_position_appCates (userID, appID);
--#
--#
--#--# for tb_test_ad_user_position_appCates_act_Install
--#create table if not exists tb_test_ad_user_position_appCates_act_Install as 
--#select 
--#instanceID, label, clickTime, creativeID, userID, positionID, connectionType, telecomsOperator, idx_tb_test,
--#click_day,                  click_day_rank,                             click_day_rank_bool,  
--#click_day_hour,             click_day_hour_rank,                        click_day_hour_rank_bool,
--#click_day_hour_minu,        click_day_hour_minu_rank,                   click_day_hour_minu_rank_bool,
--#click_day_hour_minu_s1,     click_day_hour_minu_s1_rank,                click_day_hour_minu_s1_rank_bool,
--#sitesetID,  positionType, appCategory, appCategory_1, appCategory_2, 
--#adID,  camgaignID,  advertiserID,  appID,  appPlatform,
--#age,  gender,  education,  marriageStatus,  haveBaby,  hometown, residence,
--#case when is_installed_this_app_long  is null then 0        else is_installed_this_app_long end as is_installed_this_app_long,
--#case when installTime                 is null then 99999999 else installTime                end as installTime,
--#case when install_day                 is null then 99       else install_day                end as install_day
--#from
--#(
--#select t1.*,
--#is_installed_this_app_long,  installTime,    install_day
--#from        tb_test_ad_user_position_appCates      t1 
--#left join   tb_user_installedapps_add_one_column    t2  on t1.userID = t2.userID and t1.appID = t2.appID
--#left join   tb_user_app_actions_add_one_column      t3  on t1.userID = t3.userID and t1.appID = t3.appID
--#)t;
--#
--#
--#
--#
--#
--#
--#
--#
--# --######## for tb_train ###########
--# create table if not exists tb_train_temp1 as 
--# select label, clickTime, conversionTime, creativeID, userID, positionID, connectionType, telecomsOperator, idx_tb_train,
--# cast(substr(clickTime,1,2) as unsigned) as click_day,
--# cast(substr(clickTime,1,4) as unsigned) as click_day_hour,
--# cast(substr(clickTime,1,6) as unsigned) as click_day_hour_minu,
--# cast(substr(clickTime,1,7) as unsigned) as click_day_hour_minu_s1
--# from tb_train;
--# create index index0 
--# on tb_train_temp1 (clickTime,creativeID,userID,click_day,click_day_hour,click_day_hour_minu,click_day_hour_minu_s1,idx_tb_train);
--# create index index1 on tb_train_temp1 (label);
--# 
--# 
--# --#--# for click_day_rank
--# create table tb_train_temp11 as  
--# SELECT idx_tb_train,   label,
--#      CASE when click_day = @cur0 and creativeID = @cur1  and userID = @cur2 
--#         THEN @curRow := @curRow + 1 ELSE @curRow := 0 END AS click_day_rank,
--#      @cur0 :=  click_day     AS click_day,
--#      @cur1 :=  creativeID    AS creativeID,
--#      @cur2 :=  userID        AS userID
--# FROM tb_train_temp1 t
--# JOIN (SELECT @curRow := 0, @cur0 := '') r
--# ORDER BY idx_tb_train,  click_day,  creativeID,  userID;
--# 
--# 
--# --#--# for click_day_hour_rank
--# create table tb_train_temp12 as  
--# SELECT idx_tb_train,   label,
--#      CASE when click_day_hour = @cur0 and creativeID = @cur1  and userID = @cur2 
--#         THEN @curRow := @curRow + 1 ELSE @curRow := 0 END AS click_day_hour_rank,
--#      @cur0 :=  click_day_hour     AS click_day_hour,
--#      @cur1 :=  creativeID    AS creativeID,
--#      @cur2 :=  userID        AS userID
--# FROM tb_train_temp1 t
--# JOIN (SELECT @curRow := 0, @cur0 := '') r
--# ORDER BY idx_tb_train,  click_day_hour,  creativeID,  userID;
--# 
--# 
--# --#--# for click_day_hour_minu_rank
--# create table tb_train_temp13 as  
--# SELECT idx_tb_train,   label,
--#      CASE when click_day_hour_minu = @cur0 and creativeID = @cur1  and userID = @cur2 
--#         THEN @curRow := @curRow + 1 ELSE @curRow := 0 END AS click_day_hour_minu_rank,
--#      @cur0 :=  click_day_hour_minu     AS click_day_hour_minu,
--#      @cur1 :=  creativeID    AS creativeID,
--#      @cur2 :=  userID        AS userID
--# FROM tb_train_temp1 t
--# JOIN (SELECT @curRow := 0, @cur0 := '') r
--# ORDER BY idx_tb_train,  click_day_hour_minu,  creativeID,  userID;
--# 
--# 
--# --#--# for click_day_hour_minu_s1_rank
--# create table tb_train_temp14 as  
--# SELECT idx_tb_train,   label,
--#      CASE when click_day_hour_minu_s1 = @cur0 and creativeID = @cur1  and userID = @cur2 
--#         THEN @curRow := @curRow + 1 ELSE @curRow := 0 END AS click_day_hour_minu_s1_rank,
--#      @cur0 :=  click_day_hour_minu_s1     AS click_day_hour_minu_s1,
--#      @cur1 :=  creativeID    AS creativeID,
--#      @cur2 :=  userID        AS userID
--# FROM tb_train_temp1 t
--# JOIN (SELECT @curRow := 0, @cur0 := '') r
--# ORDER BY idx_tb_train,  click_day_hour_minu_s1,  creativeID,  userID;
--# 
--# 
--# 
--# --#--# for clickTime_rank
--# create table tb_train_temp15 as  
--# SELECT idx_tb_train,   label,
--#      CASE when clickTime = @cur0 and creativeID = @cur1  and userID = @cur2 
--#         THEN @curRow := @curRow + 1 ELSE @curRow := 0 END AS clickTime_rank,
--#      @cur0 :=  clickTime     AS clickTime,
--#      @cur1 :=  creativeID    AS creativeID,
--#      @cur2 :=  userID        AS userID
--# FROM tb_train_temp1 t
--# JOIN (SELECT @curRow := 0, @cur0 := '') r
--# ORDER BY idx_tb_train,  clickTime,  creativeID,  userID;
--# 
--# 
--# create index index0 on tb_train_temp11 (idx_tb_train);
--# create index index0 on tb_train_temp12 (idx_tb_train);
--# create index index0 on tb_train_temp13 (idx_tb_train);
--# create index index0 on tb_train_temp14 (idx_tb_train);
--# create index index0 on tb_train_temp15 (idx_tb_train);
--# --# merge rank_feats to one table
--# create table if not exists tb_train_merge_temp1 as 
--# select t1.*,
--# click_day_rank,
--# click_day_hour_rank,
--# click_day_hour_minu_rank
--# from tb_train_temp1  t1 
--# join tb_train_temp11 t11 on t1.idx_tb_train = t11.idx_tb_train
--# join tb_train_temp12 t12 on t1.idx_tb_train = t12.idx_tb_train
--# join tb_train_temp13 t13 on t1.idx_tb_train = t13.idx_tb_train;
--# create index index0 on tb_train_merge_temp1 (idx_tb_train);
--# 
--# 
--# 
--# create table if not exists tb_train_merge as 
--# select t.*,
--# case when click_day                 = 0 then 0 else 1 end as click_day_rank_bool,
--# case when click_day_hour            = 0 then 0 else 1 end as click_day_hour_rank_bool,
--# case when click_day_hour_minu       = 0 then 0 else 1 end as click_day_hour_minu_rank_bool,
--# case when click_day_hour_minu_s1    = 0 then 0 else 1 end as click_day_hour_minu_s1_rank_bool,
--# case when clickTime                 = 0 then 0 else 1 end as clickTime_rank_bool
--# from 
--# (
--# select t1.*,
--# click_day_hour_minu_s1_rank,
--# clickTime_rank
--# from tb_train_merge_temp1 t1
--# join tb_train_temp14 t14 on t1.idx_tb_train = t14.idx_tb_train
--# join tb_train_temp15 t15 on t1.idx_tb_train = t15.idx_tb_train
--# )t;
--# create index index0 on tb_train_merge (idx_tb_train, creativeID,    userID);
--#
--#
--#--## merge tb_train_ad_user
--#create table if not exists tb_train_ad_user as
--#select t1.*,
--#adID,  camgaignID,  advertiserID,  appID,  appPlatform,
--#age,  gender,  education,  marriageStatus,  haveBaby,  hometown, residence
--#from tb_train_merge t1
--#join tb_ad          t2 on t1.creativeID = t2.creativeID
--#join tb_user        t3 on t1.userID     = t3.userID;
--#create index index0 on tb_train_ad_user (positionID, appID);
--#
--#
--#
--#
--#--## merge tb_train_ad_user_position_appCates
--#create table if not exists tb_train_ad_user_position_appCates as 
--#select t1.*,
--#sitesetID,  positionType, appCategory,
--#cast(appCategory / 100 as unsigned) as appCategory_1,
--#appCategory % 100 as appCategory_2
--#from tb_train_ad_user   t1
--#join tb_position        t2 on t1.positionID = t2.positionID
--#join tb_app_categories  t3 on t1.appID      = t3.appID;
--#create index index0 on tb_train_ad_user_position_appCates (userID, appID);
--#
--#
--#--# for tb_train_ad_user_position_appCates_act_Install
--#create table if not exists tb_train_ad_user_position_appCates_act_Install as 
--#select 
--#conversionTime, label, clickTime, creativeID, userID, positionID, connectionType, telecomsOperator, idx_tb_train,
--#click_day,                  click_day_rank,                             click_day_rank_bool,  
--#click_day_hour,             click_day_hour_rank,                        click_day_hour_rank_bool,
--#click_day_hour_minu,        click_day_hour_minu_rank,                   click_day_hour_minu_rank_bool,
--#click_day_hour_minu_s1,     click_day_hour_minu_s1_rank,                click_day_hour_minu_s1_rank_bool,
--#sitesetID,  positionType, appCategory,
--#--#appCategory_1, appCategory_2, 
--#cast(appCategory / 100 as unsigned) as appCategory_1,
--#appCategory % 100 as appCategory_2,
--#adID,  camgaignID,  advertiserID,  appID,  appPlatform,
--#age,  gender,  education,  marriageStatus,  haveBaby,  hometown, residence,
--#case when is_installed_this_app_long  is null then 0        else is_installed_this_app_long end as is_installed_this_app_long,
--#case when installTime                 is null then 99999999 else installTime                end as installTime,
--#case when install_day                 is null then 99       else install_day                end as install_day
--#from
--#(
--#select t1.*,
--#is_installed_this_app_long,  installTime,    install_day
--#from        tb_train_ad_user_position_appCates      t1 
--#left join   tb_user_installedapps_add_one_column    t2  on t1.userID = t2.userID and t1.appID = t2.appID
--#left join   tb_user_app_actions_add_one_column      t3  on t1.userID = t3.userID and t1.appID = t3.appID
--#)t;










--## 37912916 rows
create index index0 on tb_train_ad_user_position_appCates_act_Install (click_day);

--           dateset3: 31 ,features3 from 21~30
--           dateset2: 28 ,features2 from 18~27  
--           dateset1: 27 ,features1 from 17~26        
create table if not exists gui_dataset3 as select * from tb_test_ad_user_position_appCates_act_Install;
create table if not exists gui_dataset2 as select * from tb_train_ad_user_position_appCates_act_Install  
where click_day = 28;
create table if not exists gui_dataset1 as select * from tb_train_ad_user_position_appCates_act_Install  
where click_day = 27;

create table if not exists gui_featset3 as select * from tb_train_ad_user_position_appCates_act_Install  
where click_day > 20;
create table if not exists gui_featset3 as select * from tb_train_ad_user_position_appCates_act_Install  
where click_day < 28 and click_day >=18;
create table if not exists gui_featset3 as select * from tb_train_ad_user_position_appCates_act_Install  
where click_day < 27 and click_day >=17;
create index index0 on gui_dataset1 
(positionID, connectionType, creativeID, userID, appID, appPlatform, gender, is_installed_this_app_long, camgaignID, advertiserID, adID,
telecomsOperator, age, education, sitesetID, appCategory_1, appCategory_2, positionType, marriageStatus, hometown, residence, haveBaby);
create index index0 on gui_dataset2
(positionID, connectionType, creativeID, userID, appID, appPlatform, gender, is_installed_this_app_long, camgaignID, advertiserID, adID,
telecomsOperator, age, education, sitesetID, appCategory_1, appCategory_2, positionType, marriageStatus, hometown, residence, haveBaby);
create index index0 on gui_dataset3
(positionID, connectionType, creativeID, userID, appID, appPlatform, gender, is_installed_this_app_long, camgaignID, advertiserID, adID,
telecomsOperator, age, education, sitesetID, appCategory_1, appCategory_2, positionType, marriageStatus, hometown, residence, haveBaby);

create index index0 on gui_featset1 
(positionID, connectionType, creativeID, userID, appID, appPlatform, gender, is_installed_this_app_long, camgaignID, advertiserID, adID,
telecomsOperator, age, education, sitesetID, appCategory_1, appCategory_2, positionType, marriageStatus, hometown, residence, haveBaby);
create index index0 on gui_featset2
(positionID, connectionType, creativeID, userID, appID, appPlatform, gender, is_installed_this_app_long, camgaignID, advertiserID, adID,
telecomsOperator, age, education, sitesetID, appCategory_1, appCategory_2, positionType, marriageStatus, hometown, residence, haveBaby);
create index index0 on gui_featset3
(positionID, connectionType, creativeID, userID, appID, appPlatform, gender, is_installed_this_app_long, camgaignID, advertiserID, adID,
telecomsOperator, age, education, sitesetID, appCategory_1, appCategory_2, positionType, marriageStatus, hometown, residence, haveBaby);

-- ##############  for dataset3 and featset3 ################### 
--# positionID_connectionType_conver_rate 
--### positionID_connectionType_fset_total_cnt
--### positionID_connectionType_fset_label_1_cnt
create table if not exists gui_dataset3_f001_t1 as 
select positionID, connectionType,
count(*) as positionID_connectionType_fset_total_cnt 
from 
(
    select positionID, connectionType from gui_featset3
)t 
group by positionID, connectionType;
create index index0 on gui_dataset3_f001_t1 (positionID, connectionType);



create table if not exists gui_dataset3_f001_t2 as 
select positionID, connectionType,
count(*) as positionID_connectionType_fset_label_1_cnt
from 
(
    select positionID, connectionType from gui_featset3 where label = 1
)t 
group by positionID, connectionType;
create index index0 on gui_dataset3_f001_t2 (positionID, connectionType);



create table if not exists gui_dataset3_f001 as 
select t.*,
case when positionID_connectionType_fset_total_cnt = 0 then -1 else 
positionID_connectionType_fset_label_1_cnt *1.0 / positionID_connectionType_fset_total_cnt 
end as positionID_connectionType_conver_rate 
from
(
select t0.*,
positionID_connectionType_fset_total_cnt,
case when positionID_connectionType_fset_label_1_cnt is null then 0 else 
    positionID_connectionType_fset_label_1_cnt 
end as positionID_connectionType_fset_label_1_cnt
from            gui_dataset3           t0
left join       gui_dataset3_f001_t1   t1
on t0.positionID = t1.positionID and t0.connectionType = t1.connectionType
left join       gui_dataset3_f001_t2   t2 
on t0.positionID = t2.positionID and t0.connectionType = t2.connectionType
)t;
create index index0 on gui_dataset3_f001 (positionID, connectionType);


--# positionID_camgaignID_conver_rate 
--### positionID_camgaignID_fset_total_cnt
--### positionID_camgaignID_fset_label_1_cnt


--# positionID_creativeID_conver_rate 
--### positionID_creativeID_fset_total_cnt
--### positionID_creativeID_fset_label_1_cnt


--# positionID_advertiserID_conver_rate 
--### positionID_advertiserID_fset_total_cnt
--### positionID_advertiserID_fset_label_1_cnt





--# positionID_appID_conver_rate 
--### positionID_appID_fset_total_cnt
--### positionID_appID_fset_label_1_cnt



--# userID_adID_dset_total_cnt
create table if not exists gui_dataset3_f006 as 
select userID, adID,
count(*) as userID_adID_fset_total_cnt
from 
(
    select userID, adID from gui_dataset3
)t 
group by userID, adID;
create index index0 on gui_dataset3_f006_t1 (userID, adID);




--# connectionType_camgaignID_conver_rate 
--### connectionType_camgaignID_fset_total_cnt
--### connectionType_camgaignID_fset_label_1_cnt



--# gender_creativeID_conver_rate 
--### gender_creativeID_fset_total_cnt
--### gender_creativeID_fset_label_1_cnt



--# connectionType_creativeID_conver_rate 
--### connectionType_creativeID_fset_total_cnt
--### connectionType_creativeID_fset_label_1_cnt




--# positionID_userID_conver_rate 
--### positionID_userID_fset_total_cnt
--### positionID_userID_fset_label_1_cnt



--# positionID_is_installed_this_app_long_conver_rate 
--### positionID_is_installed_this_app_long_fset_total_cnt
--### positionID_is_installed_this_app_long_fset_label_1_cnt




--# positionID_gender_conver_rate 
--### positionID_gender_fset_total_cnt
--### positionID_gender_fset_label_1_cnt





--# u_c_cnt_in_c_rate, 这种条件概率分布特征,先在小数据集上面试试
--# userID, creativeID, 
--##            userID_fset_total_cnt,                                       userID_dset_total_cnt,             
--##        creativeID_fset_total_cnt,                                   creativeID_dset_total_cnt,         
--## userID_creativeID_fset_total_cnt,                            userID_creativeID_dset_total_cnt, 
--## userID_creativeID_fset_total_cnt_userID_rate,                userID_creativeID_dset_total_cnt_userID_rate,                    
--## userID_creativeID_fset_total_cnt_creativeID_rate,            userID_creativeID_dset_total_cnt_creativeID_rate,
--## 这里面的userID, creativeID 作为on 键，左边是gui_dataset3, 右边不断地left join 新的特征表, rate 特征是在join 之后再去求的。
--## select userID,count(*) as userID_dset_total_cnt from gui_dataset3 group by userID
--#########################################################################
--##            userID_fset_label_1_cnt,                           
--##        creativeID_fset_label_1_cnt,                           
--## userID_creativeID_fset_label_1_cnt,                           
--## userID_creativeID_fset_label_1_cnt_userID_rate,               
--## userID_creativeID_fset_label_1_cnt_creativeID_rate,           
--## 这里面的userID, creativeID 作为on 键，左边是gui_dataset3, 右边不断地left join 新的特征表, rate 特征是在join 之后再去求的。
--## select userID,count(*) as userID_dset_total_cnt from gui_dataset3 group by userID
create table if not exists gui_dataset3_f013_t10 as
select userID,count(*) as userID_fset_total_cnt from gui_featset3 group by userID;
create index index0 on gui_dataset3_f013_t10 (userID);



create table if not exists gui_dataset3_f013_t11  as
select userID,count(*) as userID_fset_label_1_cnt from gui_featset3 where label=1 group by userID ;
create index index0 on gui_dataset3_f013_t11 (userID);



create table if not exists gui_dataset3_f013_t2 as 
select userID,count(*) as userID_dset_total_cnt from gui_dataset3 group by userID;
create index index0 on gui_dataset3_f013_t2 (userID);



create table if not exists gui_dataset3_f013_t30 as
select creativeID,count(*) as creativeID_fset_total_cnt from gui_featset3 group by creativeID;
create index index0 on gui_dataset3_f013_t30 (creativeID);



create table if not exists gui_dataset3_f013_t31 as
select creativeID,count(*) as  creativeID_fset_label_1_cnt from gui_featset3 where label=1 group by creativeID ;
create index index0 on gui_dataset3_f013_t31 (creativeID);



create table if not exists gui_dataset3_f013_t4 as 
select creativeID,count(*) as creativeID_dset_total_cnt from gui_dataset3 group by creativeID;
create index index0 on gui_dataset3_f013_t4 (creativeID);



create table if not exists gui_dataset3_f013_t50 as 
select userID,creativeID,count(*) as userID_creativeID_fset_total_cnt 
from gui_featset3 group by userID, creativeID;
create index index0 on gui_dataset3_f013_t50 (userID,creativeID);



create table if not exists gui_dataset3_f013_t51 as 
select userID,creativeID,count(*) as userID_creativeID_fset_label_1_cnt
from gui_featset3 where label=1 group by userID, creativeID ;
create index index0 on gui_dataset3_f013_t51 (userID,creativeID);



create table if not exists gui_dataset3_f013_t6 as 
select userID,creativeID,count(*) as userID_creativeID_dset_total_cnt 
from gui_dataset3 group by userID, creativeID;
create index index0 on gui_dataset3_f013_t6 (userID,creativeID);



create table if not exists gui_dataset3_f013_merge_temp1 as 
select t.*,
case when  userID_creativeID_fset_total_cnt is null then 0 else userID_creativeID_fset_total_cnt 
    end as userID_creativeID_fset_total_cnt,
case when  userID_creativeID_fset_label_1_cnt is null then 0 else userID_creativeID_fset_label_1_cnt 
    end as userID_creativeID_fset_label_1_cnt
from
(
select t1.*, 
userID_creativeID_fset_total_cnt,
userID_creativeID_fset_label_1_cnt
from              gui_dataset3_f013_t6   t1
left join   gui_dataset3_f013_t51  t2 on  t1.userID = t2.userID  and  t1.creativeID = t2.creativeID
left join   gui_dataset3_f013_t50  t3 on  t1.userID = t3.userID  and  t1.creativeID = t3.creativeID
)t;
create index index0 on gui_dataset3_f013_merge_temp1(creativeID);



create table if not exists gui_dataset3_f013_merge_temp2 as
select t.*,
case when creativeID_fset_label_1_cnt is null then 0 else creativeID_fset_label_1_cnt end as creativeID_fset_label_1_cnt, 
case when creativeID_fset_total_cnt   is null then 0 else creativeID_fset_total_cnt   end as creativeID_fset_total_cnt
from 
(
select t1.*,
creativeID_dset_total_cnt,
creativeID_fset_label_1_cnt,
creativeID_fset_total_cnt
from      gui_dataset3_f013_merge_temp1  t1
left join gui_dataset3_f013_t4           t2 on t1.creativeID = t2.creativeID
left join gui_dataset3_f013_t31          t3 on t1.creativeID = t3.creativeID
left join gui_dataset3_f013_t30          t4 on t1.creativeID = t4.creativeID
)t;
create index index0 on gui_dataset3_f013_merge_temp2 (userID);



create table if not exists gui_dataset3_f013_merge_temp3 as
select t.*,
case when userID_fset_label_1_cnt is null then 0 else userID_fset_label_1_cnt end as userID_fset_label_1_cnt, 
case when userID_fset_total_cnt   is null then 0 else userID_fset_total_cnt   end as userID_fset_total_cnt
from 
(
select t1.*,
userID_dset_total_cnt,
userID_fset_label_1_cnt,
userID_fset_total_cnt
from      gui_dataset3_f013_merge_temp2  t1
left join gui_dataset3_f013_t2           t2 on t1.userID = t2.userID
left join gui_dataset3_f013_t11          t3 on t1.userID = t3.userID
left join gui_dataset3_f013_t10          t4 on t1.userID = t4.userID
)t;



create table if not exists gui_dataset3_f013 as
select 
case when userID_fset_label_1_cnt = 0 then -1 else userID_creativeID_fset_label_1_cnt*1.0 / userID_fset_label_1_cnt 
    end as userID_creativeID_fset_label_1_cnt_userID_rate,
case when creativeID_fset_label_1_cnt = 0 then -1 else userID_creativeID_fset_label_1_cnt*1.0 / creativeID_fset_label_1_cnt 
    end as userID_creativeID_fset_label_1_cnt_creativeID_rate,

case when userID_dset_total_cnt = 0 then -1 else userID_creativeID_dset_total_cnt*1.0 / userID_dset_total_cnt 
    end as userID_creativeID_dset_total_cnt_userID_rate,
case when creativeID_dset_total_cnt = 0 then -1 else userID_creativeID_dset_total_cnt*1.0 / creativeID_dset_total_cnt 
    end as userID_creativeID_dset_total_cnt_creativeID_rate,

case when userID_fset_total_cnt = 0 then -1 else userID_creativeID_fset_total_cnt*1.0 / userID_fset_total_cnt 
    end as userID_creativeID_fset_total_cnt_userID_rate,
case when creativeID_fset_total_cnt = 0 then -1 else userID_creativeID_fset_total_cnt*1.0 / creativeID_fset_total_cnt 
    end as userID_creativeID_fset_total_cnt_creativeID_rate
from 
gui_dataset3_f013_merge_temp3;







--# u_c_cnt_in_c_rate, 这种条件概率分布特征,先在小数据集上面试试
--# TODO 这是强特
--# userID, connectionType, 
--##            userID_fset_total_cnt,                                       userID_dset_total_cnt,             
--##        connectionType_fset_total_cnt,                                   connectionType_dset_total_cnt,         
--## userID_connectionType_fset_total_cnt,                            userID_connectionType_dset_total_cnt, 
--## userID_connectionType_fset_total_cnt_userID_rate,                userID_connectionType_dset_total_cnt_userID_rate,              
--## userID_connectionType_fset_total_cnt_connectionType_rate,        userID_connectionType_dset_total_cnt_connectionType_rate,
--## 这里面的userID, connectionType 作为on 键，左边是gui_dataset3, 右边不断地left join 新的特征表, rate 特征是在join 之后再去求的。
--## select userID,count(*) as userID_dset_total_cnt from gui_dataset3 group by userID
--#########################################################################
--##            userID_fset_label_1_cnt,                           
--##        connectionType_fset_label_1_cnt,                           
--## userID_connectionType_fset_label_1_cnt,                           
--## userID_connectionType_fset_label_1_cnt_userID_rate,               
--## userID_connectionType_fset_label_1_cnt_connectionType_rate,           
--## 这里面的userID, connectionType 作为on 键，左边是gui_dataset3, 右边不断地left join 新的特征表, rate 特征是在join 之后再去求的。
--## select userID,count(*) as userID_dset_total_cnt from gui_dataset3 group by userID






--# u_c_cnt_in_c_rate, 这种条件概率分布特征,先在小数据集上面试试
--# TODO 这或许是强特
--# positionID, connectionType, 
--##            positionID_fset_total_cnt,                                       positionID_dset_total_cnt,             
--##        connectionType_fset_total_cnt,                                   connectionType_dset_total_cnt,         
--## positionID_connectionType_fset_total_cnt,                            positionID_connectionType_dset_total_cnt, 
--## positionID_connectionType_fset_total_cnt_positionID_rate,            positionID_connectionType_dset_total_cnt_positionID_rate, 
--## positionID_connectionType_fset_total_cnt_connectionType_rate,        positionID_connectionType_dset_total_cnt_connectionType_rate,
--## 这里面的positionID, connectionType 作为on 键，左边是gui_dataset3, 右边不断地left join 新的特征表, rate 特征是在join 之后再去求的。
--## select positionID,count(*) as positionID_dset_total_cnt from gui_dataset3 group by positionID
--#########################################################################
--##            positionID_fset_label_1_cnt,                           
--##        connectionType_fset_label_1_cnt,                           
--## positionID_connectionType_fset_label_1_cnt,                           
--## positionID_connectionType_fset_label_1_cnt_positionID_rate,               
--## positionID_connectionType_fset_label_1_cnt_connectionType_rate,           
--## 这里面的positionID, connectionType 作为on 键，左边是gui_dataset3, 右边不断地left join 新的特征表, rate 特征是在join 之后再去求的。
--## select positionID,count(*) as positionID_dset_total_cnt from gui_dataset3 group by positionID

