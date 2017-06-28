#coding: utf-8
## index 越靠前的特征越有用(但是可能由于相关度太高而导致过拟合)
## corr  越小的特征越不相关，但是可能会欠拟合
import pandas as pd
from model_single import  *
import numpy as np
import time
import os


#data_file      = './datasets/train/data_set1_concat.csv'
old_feats_file  = './features.csv'
new_feats_file  = './features_after_corr_select.txt'
corr_df_csv     = './corr_df.csv'


def main():
    all_feats = [f.strip() for f in open(old_feats_file).readlines() if f.strip()]
    all_feats.reverse()
    if os.path.exists(corr_df_csv):
        corr_df = pd.read_csv(corr_df_csv,index_col=0)
    else:
        corr_df = abs(get_data_by_type_by_feats('lr','train', global_feats_csvs)[0].corr())
        corr_df.to_csv(corr_df_csv,index=True)
    print corr_df.shape
    need_feats  = all_feats[:1]
    select_feats= all_feats[1:]
    num_select  = len(select_feats)
    merge       = lambda corr,idx_rate:  0.1 * corr + 0.9 * idx_rate
    print need_feats
    for i in range(num_select):
        f = select_feats[i]
        merge_li = [round(merge(corr_df.loc[f, feat], i*1.0 / num_select),2)  for feat in need_feats]
        if len(merge_li)<5:
            print '----------------------------------------------------------------------------------------------------------------'
            print  f,'\n',merge_li
        max_cor = np.max(merge_li)
        if max_cor < 0.4:
            merge_li.remove(np.max(merge_li))
            if len(merge_li) ==0 :
                print '*** add *** '+str(i)+'---'+f 
                need_feats.append(f)
            else:
                if np.mean(merge_li) < 0.27:
                    print '*** add *** '+str(i)+'---'+f 
                    need_feats.append(f)
                
    print '\ntotal need_feats num ******** ',len(need_feats)
    
    with open(new_feats_file,'w') as fw:
        for f in need_feats:
            fw.writelines(f+'\n')
    print 'save to new_feats_file: ',new_feats_file

if __name__ == '__main__':
    t1 = time.time()
    main()
    print 'run ----',time.time() -t1
