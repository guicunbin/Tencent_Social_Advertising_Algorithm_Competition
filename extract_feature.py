# coding:utf-8
## TODO connectiontype 可以分出多个
##   positionID_connectiontype_0_rate
##   positionID_connectiontype_1_rate
import pandas as pd
import numpy as np
from datetime import date
import time
import itertools
import os
from utils import * 
from tqdm import tqdm
from split_data import *
from multiprocessing.dummy import Pool as ThreadPool
import os

## 平滑参数
alpha = 0.0
beta  = 0.0

tqdm        = lambda x: x
feat_dir    = './feats/'
data_dir    ='./datasets/train/'
split_time  =270000
print "split_time: ",split_time

rm_and_re_extract_feats = True
base_feats= ['positionID', 'connectionType', 'camgaignID','creativeID', 'advertiserID', 'appID', 'userID',  'adID', 'gender',
             'is_installed_this_app_long','telecomsOperator','appPlatform', 'age','education', 'marriageStatus','haveBaby','hometown',
             'residence',  'sitesetID', 'positionType', 'appCategory',  'appCategory_1',  'appCategory_2', 'clickTime']


def get_rank_feats_to_csv(mode='dataset1', groupby_feats = ['userID','creativeID']):
    print 'get_rank_feats_to_csv    process .... '+mode
    t = pd.read_csv('./datasets/dataset/' + mode +'.csv').apply(small_dtype)
    t['click_day']              = t.clickTime.apply(lambda x: int(str(int(x))[:-6])).astype('int16')
    t['click_day_hour']         = t.clickTime.apply(lambda x: int(str(int(x))[:-4])).astype('int16')
    t['click_day_hour_minu']    = t.clickTime.apply(lambda x: int(str(int(x))[:-2])).astype('int32')
    t['click_day_hour_minu_s1'] = t.clickTime.apply(lambda x: int(str(int(x))[:-1])).astype('int32')
    #### ****************************************************************************************
    ### 这一步非常关键，直接导致后面的feature_cnt_v2提出来的特征能不能concat
    t = t.sort_values(['idx'], ascending=[True])
    #### ****************************************************************************************
    for key in tqdm(['click_day', 'click_day_hour', 'click_day_hour_minu', 'click_day_hour_minu_s1']):
        ####******************  for idx  *********************
        t3                      = t[groupby_feats + [key,'idx']]
        t3['temp_idx']          = t3.idx.astype('str')
        t3                      = t3.groupby(groupby_feats + [key])['temp_idx'].agg(lambda x:':'.join(x)).reset_index()

        t2                      = t[groupby_feats + [key,'idx']]
        t2                      = pd.merge(t2, t3, 'inner',on = groupby_feats + [key])

        t2[key+'_click_number'] = t2['temp_idx'].apply(lambda s:len(s.split(':')))
        t2                      = t2[t2[key+'_click_number']>1]
        t2[key+'_max_idx']      = t2.temp_idx.apply(lambda s:max([int(d) for d in s.split(':')]))
        t2[key+'_min_idx']      = t2.temp_idx.apply(lambda s:min([int(d) for d in s.split(':')]))
        t2                      = (t2[['idx',  key+'_click_number', key+'_max_idx', key+'_min_idx']]).apply(small_dtype)
    
        t                       = pd.merge(t,t2,on='idx',how='left')
        print t.info()
        t[key+'_click_number']  = t[key+'_click_number'].fillna(1).astype('int32')
        t[key + '_lastone']     = (t[key+'_max_idx'] - t['idx']).apply(is_firstlastone)
        t[key + '_firstone']    = (t['idx'] - t[key+'_min_idx']).apply(is_firstlastone)
        t                       = t.drop([key+'_max_idx', key+'_min_idx'],axis=1).apply(small_dtype)
        t[key+'_rank']          = t.groupby(groupby_feats + [key]).cumcount().astype('int32')
        t[key+'_rank_rate']     = ((t[key+'_rank']+1) * 1.0 / t[key+'_click_number']).astype('float16')

        ####******************  for clickTime  *********************
        t3                      = t[groupby_feats + [key,'clickTime']]
        t3['temp_clickTime']    = t3.clickTime.astype('str')
        t3                      = t3.groupby(groupby_feats + [key])['temp_clickTime'].agg(lambda x:':'.join(x)).reset_index()
        print t3.info()

        t2                      = t[groupby_feats + [key,'clickTime', 'idx']]
        t2                      = pd.merge(t2, t3, 'inner',on = groupby_feats + [key])
        print t2.info()

        t2[key+'_click_number'] = t2['temp_clickTime'].apply(lambda s:len(s.split(':')))
        t2                      = t2[t2[key+'_click_number']>1]
        t2[key+'_max_clickTime']= t2.temp_clickTime.apply(lambda s:max([int(d) for d in s.split(':')]))
        t2[key+'_min_clickTime']= t2.temp_clickTime.apply(lambda s:min([int(d) for d in s.split(':')]))
        t2                      = (t2[['idx',  key+'_max_clickTime', key+'_min_clickTime']]).apply(small_dtype)

        t                       = pd.merge(t,t2,on='idx',how='left')
        t[key + '_distance_to_lastone']     = (t[key+'_max_clickTime'] - t['clickTime']).apply(compute_distance)
        t[key + '_distance_to_firstone']    = (t['clickTime'] - t[key+'_min_clickTime']).apply(compute_distance)
        t                       = t.drop([key+'_max_clickTime', key+'_min_clickTime'],axis=1).apply(small_dtype)
    ### *****************************************************************************
    print t[:10]
    t.to_csv('./datasets/dataset/' + mode + '.csv', index=False, chunksize=500000)
    






def feature_cnt(data_set, feat_set, n_feats=1, before_day=10):
    for feats in itertools.combinations(base_feats, n_feats):
        feats=list(feats)
        suffix      = reduce(lambda f1,f2: f1+'_'+f2,  feats)
        suffix_day  = '_beforeday_'+str(before_day)
        ###### make feat_names
        fset_total_cnt                = suffix + suffix_day + '_fset_total_cnt'
        ###### this feature just compute 1 time　##########################
        dset_total_cnt                = suffix + '_dset_total_cnt'
        ###################################################################
        total_cnt_dset_in_fset_rate   = suffix + suffix_day + '_total_cnt_d_in_f_rate'
        fset_label_1_cnt              = suffix + suffix_day + '_fset_label_1_cnt'
        fset_label_1_cnt_in_total_rate= suffix + suffix_day + '_fset_label_1_cnt_in_total_rate'
        print ' processing ..... '+suffix
        ###### for total cnt
        # for feat_set
        t  = feat_set[feats]
        t[fset_total_cnt]=1
        t  = t.groupby(feats).agg('sum').reset_index().astype('float32')
        data_set = pd.merge(data_set, t, how='left', on = feats)
        # for data_set
        if dset_total_cnt not in data_set.columns:
            t  = data_set[feats]
            t[dset_total_cnt]=1
            t  = t.groupby(feats).agg('sum').reset_index().astype('float32')
            data_set = pd.merge(data_set, t, how='left', on = feats)
        data_set[total_cnt_dset_in_fset_rate] = \
                (data_set[dset_total_cnt] / data_set[fset_total_cnt]).astype('float16')
        if 'click_day' in feats:
        ### 点击日当天的　label 我们是不知道的, 只知道当天点击了多少次
        ### TODO 可以改用点击日之前所有的天的　label 
            continue
        ######　下面的这些涉及到 label 那么就只能在feat_set上面提取
        ### for label 1
        t = feat_set[feat_set.label==1][feats]
        t[fset_label_1_cnt] = 1
        t = t.groupby(feats).agg('sum').reset_index().astype('float32')
        data_set = pd.merge(data_set, t, how='left', on = feats)
        data_set[fset_label_1_cnt].fillna(value=0,inplace=True)
        ### for transfer_rate
        data_set[fset_label_1_cnt_in_total_rate]=\
                (data_set[fset_label_1_cnt] / data_set[fset_total_cnt]).astype('float16')
        ###TODO tranfer_rate 是否需要 fillna -1
    return data_set




def feature_cnt_v2(data_set_path, feat_set_path, mode = 'train', n_feats=2, before_day=10):
    '''this func will use less Memory, but will use more time
        and this func add some extra feature
    '''
    if rm_and_re_extract_feats:
        os.system('rm -r '+feat_dir+mode)
        os.makedirs(feat_dir+mode)
    ##for feats in tqdm(itertools.combinations(base_feats, n_feats)):
    featset_feats = base_feats + ['label']
    featset_feats = [featset_feats[i * 5 : (i+1) * 5] for i in range(len(featset_feats) / 5 + 1)]
    print 'read  dataset and featset ......' 
    is_first = True
    for cols in featset_feats:
        df       = pd.read_csv(feat_set_path, usecols = cols).apply(small_dtype)
        featset  = df if is_first else pd.concat([featset, df], axis=1) 
        is_first = False
    data_set_total  = pd.read_csv(data_set_path, usecols = base_feats).apply(small_dtype)
    def func_feats(feats):
        time1 = time.time()
        feats=list(feats)
        suffix      = reduce(lambda f1,f2: f1+'_'+f2,  feats)
        suffix_day  = '_bday_'+str(before_day)
        save_csv  = feat_dir+mode+'/'+suffix+suffix_day+'.csv'
        if os.path.exists(save_csv):
            return
        ###### make feat_names
        fset_total_cnt                  = suffix + suffix_day + '_fset_total_cnt'
        ###### this feature just compute 1 time　##########################
        dset_total_cnt                  = suffix + '_dset_total_cnt'
        ###################################################################
        total_cnt_dset_in_fset_rate     = suffix + suffix_day + '_total_cnt_d_in_f_rate'
        fset_label_1_cnt                = suffix + suffix_day + '_fset_label_1_cnt'
        fset_label_1_cnt_in_total_rate  = suffix + suffix_day + '_fset_label_1_cnt_in_total_rate'
        print ' processing ..... '+suffix
        ###### for total cnt
        # for feat_set
        #featset                  = pd.read_csv(feat_set_path,usecols=feats+['label']).apply(small_dtype)
        t                         = featset[feats].copy()
        t[fset_total_cnt]         = np.ones([len(t),],  dtype='int32')
        t                         = t.groupby(feats).agg('sum').reset_index()
        #data_set                 = pd.read_csv(data_set_path,  usecols=feats).apply(small_dtype)
        data_set                  = data_set_total[feats]
        data_set                  = pd.merge(data_set, t, how='left', on = feats)
        data_set[fset_total_cnt]  = pd.to_numeric(data_set[fset_total_cnt].fillna(0).astype('int32'), downcast = 'integer')
        ### some  rate
        for f in feats:
            single_f_cnt          = f + suffix_day + '_fset_cnt' 
            f_rate                = fset_total_cnt + '_rate_in_'+f
            ##t                   = pd.read_csv(feat_set_path, usecols=[f]).apply(small_dtype)
            t                     = featset[[f]].copy()
            t[single_f_cnt]       = np.ones([len(t),],  dtype='int32')
            t                     = t.groupby(f).agg('sum').reset_index()
            #print t[:10]
            #print '***************************************'
            data_set              = pd.merge(data_set, t, how='left', on=f)
            data_set[single_f_cnt]= pd.to_numeric(data_set[single_f_cnt].fillna(0).astype('int32'), downcast = 'integer')
            #print data_set[:10]
            #print '***************************************'
            data_set[f_rate]      = ((data_set[fset_total_cnt]+alpha) * 1.0 / (data_set[single_f_cnt]+beta)).astype('float16')
        #print data_set.info()
        data_set                  = data_set.apply(small_dtype)
        #print data_set.info()
        #print data_set[:10]
        #print '***************************************'
        # for data_set
        t                         = data_set[feats]
        t[dset_total_cnt]         = np.ones([len(t),], dtype='int32')
        t                         = t.groupby(feats).agg('sum').reset_index()
        data_set = pd.merge(data_set, t, how='left', on = feats)
        data_set[total_cnt_dset_in_fset_rate] = \
                ((data_set[dset_total_cnt]+alpha) * 1.0 / (data_set[fset_total_cnt]+beta)).astype('float16')
        if 'click' in suffix:
        ### 点击日当天的　label 我们是不知道的, 只知道当天点击了多少次
        ### TODO 可以改用点击日之前所有的天的　label 
            need_cols = [f for f in data_set.columns.tolist() if f not in feats]
            print '*************************************** write data ............'
            data_set[need_cols].to_csv(save_csv, mode='w', index=False)
            print 'run time -----',time.time()-time1
            return
        ######　下面的这些涉及到 label 那么就只能在feat_set上面提取
        ### for label 1
        #t                          = pd.read_csv(feat_set_path,usecols=feats+['label']).apply(small_dtype)
        t                           = featset.copy()
        t                           = t[t.label==1][feats]
        t[fset_label_1_cnt]         = np.ones([len(t), 1], dtype='int32')
        t                           = t.groupby(feats).agg('sum').reset_index()
        data_set                    = pd.merge(data_set, t, how='left', on = feats)
        data_set[fset_label_1_cnt]  = pd.to_numeric(data_set[fset_label_1_cnt].fillna(0).astype('int32'), downcast='integer')
        ### some rate
        for f in feats:
            single_f_cnt_1          = f + suffix_day    + '_fset_label_1_cnt' 
            f_rate_1                = fset_label_1_cnt  + '_rate_of_'+f
            #t                      = pd.read_csv(feat_set_path, usecols=[f,'label']).apply(small_dtype)
            t                       = featset[[f,'label']].copy()
            t                       = t[t.label==1][[f]]
            t[single_f_cnt_1]       = np.ones([len(t), 1], dtype='int32')
            t                       = t.groupby(f).agg('sum').reset_index()
            data_set                = pd.merge(data_set, t, how='left', on=f)
            data_set[single_f_cnt_1]= pd.to_numeric(data_set[single_f_cnt_1].fillna(0).astype('int32'), downcast = 'integer')
            data_set[f_rate_1]      = ((data_set[fset_label_1_cnt]+alpha) * 1.0 / (data_set[single_f_cnt_1]+beta)).astype('float16')
        #t = None;   featset =None;
        ### for transfer_rate
        data_set[fset_label_1_cnt_in_total_rate]=\
                ((data_set[fset_label_1_cnt]+alpha) * 1.0 / (data_set[fset_total_cnt]+beta)).astype('float16')
        ###TODO tranfer_rate 是否需要 fillna -1
        need_cols = [f for f in data_set.columns.tolist() if f not in feats]
        #print data_set[:5]
        print '*************************************** write data ............'
        data_set[need_cols].to_csv(save_csv, mode='w', index=False,chunksize=100000)
        print 'run time -----',time.time()-time1
    
    ##### map the func_feats
    map(func_feats, list(itertools.combinations(base_feats, n_feats)))
    
    #pool = ThreadPool(3)
    #pool.map(func_feats, list(itertools.combinations(base_feats, n_feats)))
    #pool.close()




def get_data_set123(data_set,   feat_set,  before_day):
    '''this func just use for data_set_phase1
    '''
    t1 = time.time()
    data_set = feature_cnt(data_set, feat_set, n_feats=1, before_day = before_day)
    print data_set.shape
    data_set = feature_cnt(data_set, feat_set, n_feats=2, before_day = before_day)
    print data_set.shape
    print '************ this step run time ',time.time() - t1
    return data_set



def main():
    #### train:  data_set1   27   feat_set1     17->26
    #### valid   data_set2   28   feat_set2     18->27  
    #### test    data_set3   31   feat_set3     21->30 
    #### 最后在test的时候可以将df_train = pd.concat([df_train,df_valid],axis=0)

    #### train:  data_set1   27   feat_set1     17->26
    #data_set = pd.read_csv(data_dir+'f_train_ad_user_position_appCategories_appActions_appInstalled.csv', dtype='float32')
    #data_set = data_set[data_set.click_day==27]
    #feat_set = pd.read_csv(data_dir+'f_train_ad_user_position_appCategories_appActions_appInstalled.csv', dtype='float32')
    #feat_set = feat_set[(feat_set.click_day>=17)&(feat_set.click_day<=26)]
    #data_set = get_data_set123(data_set,feat_set, before_day=9)
    #data_set.to_csv(data_dir+'data_set1.csv',index=False)

    #### valid   data_set2   28   feat_set2     18->27  
    #data_set = pd.read_csv(data_dir+'f_train_ad_user_position_appCategories_appActions_appInstalled.csv', dtype='float32')
    #data_set = data_set[data_set.click_day==28]
    #feat_set = pd.read_csv(data_dir+'f_train_ad_user_position_appCategories_appActions_appInstalled.csv', dtype='float32')
    #feat_set = feat_set[(feat_set.click_day>=18)&(feat_set.click_day<=27)]
    #data_set = get_data_set123(data_set,feat_set,before_day=9)
    #data_set.to_csv(data_dir+'data_set2.csv',index=False)

    ##### test    data_set3   31   feat_set3     21->30 
    data_set = pd.read_csv(data_dir+'f_test_ad_user_position_appCategories_appActions_appInstalled.csv', dtype='float32')
    data_set = data_set[data_set.click_day==31]
    feat_set = pd.read_csv(data_dir+'f_train_ad_user_position_appCategories_appActions_appInstalled.csv', dtype='float32')
    feat_set = feat_set[(feat_set.click_day>=21)&(feat_set.click_day<=30)]
    data_set = get_data_set123(data_set,feat_set,before_day=9)
    data_set.to_csv(data_dir+'data_set3.csv',index=False)




def use_feature_cnt_v2(mode):
    if mode == 'train':
        ##### train:  data_set1   27   feat_set1     17->26
        feature_cnt_v2(dataset1_csv, featset1_csv,  'train')
    if mode == 'valid':
        #### valid   data_set2   28   feat_set2     18->27  
        feature_cnt_v2(dataset2_csv, featset2_csv,  'valid')
    if mode == 'test':
        #### test    data_set3   31   feat_set3     21->30 
        feature_cnt_v2(dataset3_csv, featset3_csv,  'test')
    if mode == 'extra_1':
        #### extra_1 data_set4   29   feat_set3     19->28
        feature_cnt_v2(dataset4_csv, featset4_csv,  'extra_1')




def main_v2():
    '''less Memory but more time
    '''

    # ***** 必须得先排序，否则就是乱的，根本匹配不上的concat
    get_rank_feats_to_csv('dataset1', groupby_feats = ['userID','creativeID'])
    get_rank_feats_to_csv('dataset2', groupby_feats = ['userID','creativeID'])
    get_rank_feats_to_csv('dataset3', groupby_feats = ['userID','creativeID'])
    get_rank_feats_to_csv('dataset4', groupby_feats = ['userID','creativeID'])
    modes = ['train', 'valid','test', 'extra_1']

    map(use_feature_cnt_v2,   modes[:])





if __name__ =='__main__':
    main_v2()
