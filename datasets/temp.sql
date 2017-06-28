
--#现在就是可以提取多个rank 类型的特征，click_day_rank_by_UC,  
--# click_day_rank_by_U,  click_day_by_C(U userID, C creativeID,甚至还可以是positionID, appID......)
--# 或者这样起个名字，userID_click_day_rank,   userID_creativeID_click_day_rank,
drop   table temp_sql_tb; 
create table temp_sql_tb as 
SELECT idx_tb_test,label,
     CASE when click_day = @cur0 and creativeID = @cur1  and userID = @cur2 
        THEN @curRow := @curRow + 1 ELSE @curRow := 0 END AS click_day_rank,
     @cur0 :=  click_day     AS click_day,
     @cur1 :=  creativeID    AS creativeID,
     @cur2 :=  userID        AS userID
FROM tb_test_temp1_tiny t 
JOIN (SELECT @curRow := 0, @cur0 := '') r
ORDER BY idx_tb_test, click_day, creativeID, userID;

