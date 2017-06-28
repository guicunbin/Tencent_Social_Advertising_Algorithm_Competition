### tencent_2017_contest_final    http://algo.tpai.qq.com (2017腾讯社交广告算法大赛) 
### (决赛)86th      
###  ID  gui式弧线  
---------------------------------------------------------------------------------------------



## dependency
> sudo pip install lightgbm  pandas  numpy  sklearn   fire

---------------------------------------------------------------------------------------------


## useage

> ./run_phase_1.sh
##### need:      8G RAM;       50G disk;     2 hour time;
##### 初赛的脚本只需 8G 运行内存，　　  50G 硬盘空间，　 整个流程只需不到 2 个小时


or 


> ./run.sh
##### need:      8G RAM;       500G disk;    10 hour time;
##### 决赛的脚本同样只需 8G 运行内存,       500G 硬盘空间，　整个流程需要大约 10 个小时



---------------------------------------------------------------------------------------------

## notice 
> "sort: 写入失败: 标准输出: 断开的管道"         这个没有关系，可以继续执行
> the run.sh or run_phase_1.sh will auto download the data,  auto preprocess, auto extract feature, auto run model 
##### run.sh 或 run_phase_1.sh 会自动下载数据，自动预处理，自动提取特征，自动跑模型生成submiss.csv, 一气呵成。


---------------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------------

## other solutions    
###### final 14th  https://github.com/z564808896/Tencent_Social_Ads
> 贝叶斯平滑　　
> rank_feature 处理成类别特征
> 三组合交叉特征
###### final 23th  https://github.com/BladeCoda/Tencent2017_Final_Coda_Allegro
