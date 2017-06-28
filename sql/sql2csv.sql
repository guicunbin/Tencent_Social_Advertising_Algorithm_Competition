use tecent_2017_06;

select * from tb_test_ad_user_position_appCates_act_Install  
into outfile "/var/lib/mysql-files/test_ad_user_position_appCates_act_Install.csv" 
FIELDS TERMINATED BY ','   
OPTIONALLY ENCLOSED BY '"'   
LINES TERMINATED BY '\n';


select * from tb_train_ad_user_position_appCates_act_Install  
into outfile "/var/lib/mysql-files/train_ad_user_position_appCates_act_Install.csv" 
FIELDS TERMINATED BY ','   
OPTIONALLY ENCLOSED BY '"'   
LINES TERMINATED BY '\n';

