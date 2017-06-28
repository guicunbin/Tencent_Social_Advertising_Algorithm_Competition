#coding:utf-8
import pandas as pd
import os
from tqdm import tqdm
import time
## TODO 一天的样本根本不够，trick的分布可以说是一天一个样，所以需要多天，才能学好trick特征的，2-4天最好了
## 27 28 训练， 29验证

train_csv   = './datasets/train/final_train_ad_user_position_appCates_act_Install.csv'
test_csv    = './datasets/train/final_test_ad_user_position_appCates_act_Install.csv'
dataset_path= './datasets/dataset/'
dataset1_csv= './datasets/dataset/dataset1.csv'  
dataset2_csv= './datasets/dataset/dataset2.csv' 
dataset3_csv= './datasets/dataset/dataset3.csv'  
# dataset3_csv 是test 
dataset4_csv= './datasets/dataset/dataset4.csv'

featset1_csv= './datasets/dataset/featset1.csv' 
featset2_csv= './datasets/dataset/featset2.csv' 
featset3_csv= './datasets/dataset/featset3.csv'  
# featset3_csv 是test 
featset4_csv= './datasets/dataset/featset4.csv'
featset_total_csv = './datasets/dataset/featset_total.csv'


def fix_label(df, click_day):
    mask = df['conversionTime'] >= click_day*10**6
    df.ix[mask,['label','conversionTime']] = 0
    return df




def main():
    print './datasets/dataset/ will be remove' 
    os.system('rm -r '+dataset_path)
    os.makedirs(dataset_path)
    os.system(' cp {0} {1} '.format(test_csv, dataset3_csv))

    ## ****** for dataset3_csv  *******
    df = pd.read_csv(dataset3_csv)
    df['click_day']     = (df.clickTime / 1000000).astype('int8')
    df['appCategory_1'] = df['appCategory'].apply(lambda x: int(x / 100) if x >= 100 else x).astype('int8')
    df['appCategory_2'] = df['appCategory'].apply(lambda x: int(x % 100) if x >= 100 else -1).astype('int8')
    df.to_csv(dataset3_csv, index=False)
    ## ****** for dataset3_csv  *******

    dftrains     = pd.read_csv(train_csv,chunksize=500000)
    need_header = True
    
    print 'split data .....'
    for df in tqdm(dftrains):
        #print df[:10]
        df['click_day']     = (df.clickTime / 1000000).astype('int8')
        df['appCategory_1'] = df['appCategory'].apply(lambda x: int(x / 100) if x >= 100 else x).astype('int8')
        df['appCategory_2'] = df['appCategory'].apply(lambda x: int(x % 100) if x >= 100 else -1).astype('int8')
        t = df[(df.click_day >= 17)&\
                (df.click_day < 27)]
        t =         fix_label(t,27)
        t.to_csv(featset1_csv, index=False, mode='a', header = need_header)
        t = df[df.click_day  == 27]
        t.to_csv(dataset1_csv, index=False, mode='a', header = need_header)
    

        t = df[(df.click_day >= 18)&\
                (df.click_day < 28)]
        t =         fix_label(t,28)
        t.to_csv(featset2_csv, index=False, mode='a', header = need_header)
        t = df[df.click_day  == 28]
        t.to_csv(dataset2_csv, index=False, mode='a', header = need_header)
        
        t = df[(df.click_day >= 21)&\
                (df.click_day < 31)]
        t.to_csv(featset3_csv, index=False, mode='a', header = need_header)
    
        # TODO extra dataset   and  featset 
        
        t = df[(df.click_day >= 19)&\
                (df.click_day < 29)]
        t =         fix_label(t,29)
        t.to_csv(featset4_csv, index=False, mode='a', header = need_header)
        t = df[df.click_day  == 29]
        t.to_csv(dataset4_csv, index=False, mode='a', header = need_header)


        #df[df.click_day >= 17].to_csv(featset_total_csv, index = False, mode='a', header = need_header)
        need_header  = False
    
if __name__ == '__main__':
    main()

