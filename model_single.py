# -*- coding: utf-8 -*-
"""
baseline 2: ad.csv (creativeID/adID/camgaignID/advertiserID/appID/appPlatform) + lr
"""
#####TODO   lr use onehot features to get a output proba [n_samples,1] 
#####       use as a strongest feature to feed in lgb with other count features
#####TODO    use lr and lgb results merge
import pandas as pd
import numpy as np
import lightgbm as lgb
import os
import time
from sklearn.preprocessing import scale
from sklearn.linear_model import LogisticRegression
from utils import *
import fire
import itertools
import send_email
import copy
import re
from split_data import *
#### TODO use following feats to test_feats
#### TODO rank_feats 需要　转化成类别变量
#### TODO 有几个三特征组合据说效果不错,[('appID','connectionType','positionID'),('appID','haveBaby','gender')]
cate_feats      = []
### train
dataset2_csv_concat  = './datasets/dataset/dataset2_concat.csv'
### valid
dataset4_csv_concat  = './datasets/dataset/dataset4_concat.csv'
### train_total
dataset24_csv_concat = './datasets/dataset/dataset24_concat.csv'
### test
dataset3_csv_concat  = './datasets/dataset/dataset3_concat.csv'


# define params
split_time  = 27
num_boost_round_scale = 1.0
neg_pos     = None
is_email    = False
is_to_csv   = False
is_tiny     = False
#feat_csv    = './feats_csvs.txt'
#global_feats_csvs= [f.strip() for f in open(feat_csv).readlines() if f.strip()]
global_feats_csvs = [f.strip() for f in os.listdir('./feats/train/') if f.strip()]
### ***************** for lr the folowing feats get test 0.104140  on data_phase1 *****************
#lr_feats = ["creativeID", "adID", "camgaignID", "advertiserID", "appID", "appPlatform", "connectionType", "telecomsOperator",
#            "has_installed_this_app",  'age', 'gender','education', 'marriageStatus', 'haveBaby', 'appPlatform', 'sitesetID', 
#            'positionType','appCategory','positionID']

#rank_time = ['clickTime', 'click_day', 'click_day_hour', 'click_day_hour_minu']
#rank_feats= [key+'_rank'  for key in rank_time] + [key+'_rank_bool' for key in rank_time]
#rank_feats= [f for f in get_csv_header(dataset1_csv) if f in important_feats ]# and 'distance' not in f]
#rank_feats = [\
#'click_day_click_number',
#'click_day_lastone',
#'click_day_firstone',
#'click_day_rank',
#'click_day_rank_rate',
#'click_day_distance_to_lastone',
#'click_day_distance_to_firstone',
#'click_day_hour_click_number',
#'click_day_hour_lastone',
#'click_day_hour_firstone',
#'click_day_hour_rank',
#'click_day_hour_rank_rate',
#'click_day_hour_distance_to_lastone',
#'click_day_hour_distance_to_firstone',
#'click_day_hour_minu_click_number',
#'click_day_hour_minu_lastone',
#'click_day_hour_minu_firstone',
#'click_day_hour_minu_rank',
#'click_day_hour_minu_rank_rate',
#'click_day_hour_minu_distance_to_lastone',
#'click_day_hour_minu_distance_to_firstone',
#'click_day_hour_minu_s1_click_number',
#'click_day_hour_minu_s1_lastone',
#'click_day_hour_minu_s1_firstone',
#'click_day_hour_minu_s1_rank',
#'click_day_hour_minu_s1_rank_rate',
#'click_day_hour_minu_s1_distance_to_lastone',
#'click_day_hour_minu_s1_distance_to_firstone',
#]
#print rank_feats
base_feats= ['positionID', 'connectionType', 'camgaignID','creativeID', 'advertiserID', 'appID', 'userID',  'adID', 'gender',
             'is_installed_this_app_long']
            # ,'telecomsOperator','appPlatform', 'age','education', 'marriageStatus','haveBaby','hometown',
            # 'residence',  'sitesetID', 'positionType', 'appCategory',  'appCategory_1',  'appCategory_2',
            # ]

important_feats_csv     = './features_after_corr_select.txt'
global_important_feats  = [f.strip() for f in open(important_feats_csv).readlines() if f.strip()]
if len(set(global_important_feats)) != len(global_important_feats):
    raise Exception('please delete duplicate from '+important_feats_csv)
global_important_feats.reverse()

## define lgb params
params_0 = {
    'task': 'train',
    'boosting_type': 'gbdt',
#   'boosting_type': 'dart',
    'objective': 'binary',
#   'metric': {'l2', 'auc'},
#   'metric': 'binary_logloss',
#   'metric': 'fair'
########################
    'max_depth':7,          ## max_depth  : 1    2    3    4      5      6    ....           n
    'num_leaves':31,        ## num_leaves : 2   3-4  3-8  3-16   3-32   3-64  ....          3-2^n
    'learning_rate': 0.1 ,
#########################
    'min_data_in_leaf':100,
    'drop_rate':0.1,
    'feature_fraction': 0.9,
    'bagging_fraction': 0.9,
    'bagging_freq': 5,
    'verbose': 1
}



def get_concat_data(label_csv, label_col, other_csvs, is_rate, important_feats):
    print 'important_feats :  ',len(important_feats)
    rank_feats  = [f for f in get_csv_header(dataset1_csv) if 'click' in f]
    rank_feats  = [f for f in rank_feats if f in important_feats] if important_feats else rank_feats
    X           = pd.read_csv(label_csv, usecols = rank_feats+[label_col]).apply(small_dtype)
    X           = X[:1000000] if is_tiny else X
    print 'concat csvs ......'
    X           = pd.concat([X, get_need_feats(other_csvs, is_rate, is_tiny, important_feats)], axis=1)
    #if label_csv.split('/')[-1] == 'dataset2.csv':
    #    for c in X.columns:
    #        if c.endswith('_fset_total_cnt'):
    #            X = X.drop(X[X[c]==0].index, axis=0)
    feat_cols   = [f for f in X.columns if f != label_col]
    if is_to_csv:
        save_file = label_csv.split('.csv')[0]+'_concat.csv'
        if os.path.exists(save_file):
            print save_file + " has exists"
        else:
            print 'to csv ........'
            X            = X.replace(np.nan, -1)
            X            = X.replace(np.inf, -2)
            X[feat_cols] = scale(X[feat_cols]).astype('float16')
            X.to_csv(save_file, index=False, chunksize = 50000)
    print X.shape
    # TODO cate_feats = [f for f in X.columns if 'click' in f] 
    ## 据说这一步可以带来 3 个千分点的提升,因为rank_feats 实际上是类别变量
    X,      = change_to_category([X], cate_feats)
    y       = X[label_col].values
    X       = X[feat_cols]
    if label_col == 'label':
        print 'positive percent ',y.mean()
    return X, y

    



def get_data_by_type_by_feats(model='lgb', use_type='train_total',set_csvs=[], need_feats = global_important_feats):
    ''' if set_csvs: then concat more feats 
        else:        just use rank_feats
    '''
    print "load data ......"
    dataset1_add_csvs   = ['./feats/train/'+csv     for csv in set_csvs]
    dataset2_add_csvs   = ['./feats/valid/'+csv     for csv in set_csvs]
    dataset4_add_csvs   = ['./feats/extra_1/'+csv   for csv in set_csvs]
    dataset3_add_csvs   = ['./feats/test/' +csv     for csv in set_csvs]
    if 'train' in use_type:
        X_train,y_train  = get_concat_data(dataset2_csv, 'label',dataset2_add_csvs, is_rate=False, important_feats = need_feats)
        if use_type == 'train':
            if model == 'lr':
                X_train = X_train.replace(np.inf,-2)
                X_train = X_train.replace(np.nan,-1)
                return X_train, y_train
            if model == 'lgb':
                X_train = lgb.Dataset(X_train,  y_train)
                return X_train

        X_valid,y_valid = get_concat_data(dataset4_csv, 'label', dataset4_add_csvs, is_rate=False, important_feats = need_feats)
        if use_type == 'train_valid':
            if model == 'lr':
                X_valid = X_valid.replace(np.inf,-2)
                X_valid = X_valid.replace(np.nan,-1)
                return X_train, y_train, X_valid, y_valid
            if model == 'lgb':
                print ' lgb Dataset .....'
                X_train = lgb.Dataset(X_train,  y_train)
                print ' lgb Dataset .....'
                X_valid = lgb.Dataset(X_valid,  y_valid, reference=X_train)
                return X_train, X_valid

        if use_type == 'train_total':
            X_train        = pd.concat([X_train, X_valid],       axis=0)
            y_train        = np.concatenate([y_train, y_valid],  axis=0)
            print X_train.shape
            if model == 'lr':
                return X_train, y_train
            if model == 'lgb':
                print ' lgb Dataset .....'
                X_train = lgb.Dataset(X_train, y_train)
                return X_train

    if use_type == 'test':
        X_test, instanceID = get_concat_data(dataset3_csv, 'instanceID', dataset3_add_csvs, is_rate=False, important_feats = need_feats)
        if model == 'lr':
            X_test = X_test.replace(np.inf,-2)
            X_test = X_test.replace(np.nan,-1)
        if model =='lgb':
            return X_test, instanceID.astype('int32')

    print 'return None'
    return None


            
        



def lr_model_get_prob(feats):
    print "lr model training in split train_set "
    ##### lr model 
    X_train, y_train ,X_valid, y_valid = get_data_by_type_by_feats('lr', 'train_valid', feats)
    lr = LogisticRegression()
    lr.fit(X_train, y_train)
    prob_train = lr.predict_proba(X_train)[:,1].reshape(-1,1)
    prob_valid = lr.predict_proba(X_valid)[:,1].reshape(-1,1)
    eval_train = round(logloss(y_train, prob_train), 6)
    eval_valid = round(logloss(y_valid, prob_valid), 6)
    print 'lr eval_train eval_valid----- ', eval_train, eval_valid
    ### train_total
    print 'lr train again'
    X_train, y_train, X_valid, y_valid = 0, 0, 0, 0
    X_train_total, y_train_total = get_data_by_type_by_feats('lr', 'train_total', feats)
    lr.fit(X_train_total, y_train_total)
    prob_train_total= lr.predict_proba(X_train_total)[:,1].reshape(-1,1)
    ### test 
    print 'lr test '
    X_train_total = 0
    X_test, instanceID = get_data_by_type_by_feats('lr', 'test', feats) 
    proba_test      = lr.predict_proba(X_test)[:,1].reshape(-1,1)
    return prob_train_total, prob_train, prob_valid, proba_test





def train_test(mode, feat_csvs, need_feats=global_important_feats):
    #prob_train_total,       prob_train,       prob_valid,       proba_test                          = lr_model_get_prob(feat_csvs)
    ##### lgb model 
    Dataset_train,Dataset_valid = get_data_by_type_by_feats(model='lgb',use_type='train_valid',set_csvs=feat_csvs,need_feats=need_feats)
    ##### Dataset append lr_prob
    #Dataset_train_total.data= np.concatenate([Dataset_train_total.data, prob_train_total])
    #Dataset_train.data      = np.concatenate([Dataset_train.data,       prob_train])
    #Dataset_valid.data      = np.concatenate([Dataset_valid.data,       prob_valid])
    #Dataset_train_total.set_feature_name(feat_csvs+['lr_prob'])
    #Dataset_train.set_feature_name(feat_csvs+['lr_prob'])
    #Dataset_valid.set_feature_name(feat_csvs+['lr_prob'])
    #X_test['lr_prob']=prob_test
    gbm = lgb.train(params      = params_0,
                    train_set   = Dataset_train,
                    num_boost_round = 1000,
                    valid_sets      = Dataset_valid,
                    fobj = None,    feval=self_eval, 
                    early_stopping_rounds = 10)
    print gbm.eval_valid(self_eval)
    eval_train = round(gbm.eval_train(self_eval)[0][2], 6)
    eval_valid = round(gbm.eval_valid(self_eval)[0][2], 6)
    


    ##### eval valid
    print "# eval train and valid"
    print 'eval train log loss = ',eval_train
    print 'eval valid log loss = ',eval_valid
    with open('./feature_name_importance.txt', 'a') as fa:
        now_time=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        fa.writelines('\n\n\n\n\n************* new model ************')
        fa.writelines('\n'+str(now_time)+'\n')
        fa.writelines('\n    eval_train = '+str(eval_train))
        fa.writelines('\n    eval_valid = '+str(eval_valid)+'\n')
        feature_importance = gbm.feature_importance(importance_type="gain")
        feature_names      = gbm.feature_name()
        sorted_idx         = np.argsort(feature_importance)
        for i in sorted_idx:
            st=str(feature_names[i])+' : '+str(feature_importance[i])+'\n'
            fa.writelines(st)
    if mode == 'just_valid':
        return eval_train, eval_valid 



    print 'model training in total train_set'
    try:
        print ' gbm.best_iteration: ',gbm.best_iteration
        num_round  = int(gbm.best_iteration*num_boost_round_scale) if gbm.best_iteration!=-1 else gbm.current_iteration()
    except:
        eval_train  = '_'
        eval_valid  = '_'
        num_round   = 500
    #####  use total train_set train again
    Dataset_train_total = get_data_by_type_by_feats(model = 'lgb', use_type = 'train_total', set_csvs = feat_csvs, need_feats = need_feats)
    print 'train again .......'

    gbm = lgb.train(params = params_0,    
                    train_set   = Dataset_train_total,
                    valid_sets  = Dataset_train_total,
                    num_boost_round = num_round,
                    fobj = None,    feval=self_eval)
    X_test ,instanceID  = get_data_by_type_by_feats(model = 'lgb', use_type = 'test', set_csvs = feat_csvs, need_feats = need_feats)
    print 'test .......'
    proba_test = gbm.predict(X_test, gbm.best_iteration)
    

    ## submission prepare dirs
    print "# submission"
    sub_dir_name  = './datasets/submit/lgb_train_split_'+str(split_time)+'_tra_'+str(eval_train)+'_val_'+str(eval_valid)+'/'
    sub_file_name = sub_dir_name+'submission.csv'
    os.system('rm -r '+sub_dir_name)
    os.makedirs(sub_dir_name)
    ## sub to csv 
    df = pd.DataFrame({"instanceID": instanceID, "prob": proba_test})
    df.sort_values("instanceID", inplace=True)
    df.to_csv(sub_file_name, index=False, chunksize=50000)
    print 'save file to ',sub_file_name





def run_model_test_csvs(init_feats_num = '0:10', extra_feats_num = '10:46'):
    n1,n2 = [int(n) for n in init_feats_num.split(':')]
    n3,n4 = [int(n) for n in extra_feats_num.split(':')]
    init_feats  = global_feats_csvs[n1:n2]
    extra_feats = global_feats_csvs[n3:n4]
    f_batch_size = 2
    eval_train, eval_valid  = train_test(mode='just_valid',feat_csvs = init_feats)
    range_len = len(extra_feats) / f_batch_size
    range_len = range_len if int(range_len) == range_len else range_len + 1
    for i in  range(range_len):
        print_time(i)
        add_feats   = extra_feats[i*f_batch_size: (i+1)*f_batch_size]
        temp_feats  = init_feats + add_feats
        eval_train, eval_valid  = train_test(mode='just_valid',feat_csvs = temp_feats)
        context = '\n**** extra_feat =  '+str(add_feats)+'\n**** eval_train , eval_valid = '+str(eval_train)+', '+str(eval_valid)
        subject = 'TSA_contest'
        print context
        if i == 0:
            context_concat  = context
        else:
            context_concat += context
        if is_email and i==5:
            try:
                send_email.send_email(context,subject)
            except:
                pass
    with open('./feature_name_importance.txt', 'a') as fa:
        fa.writelines(context_concat)



def run_model_test_feats(init_feats_num = '0:10', extra_feats_num = '10:46'):
    ''' if is_test_feats:  extra_feats  is necessary
    '''
    print init_feats_num
    n1,n2 = [int(n) for n in init_feats_num.split(':')]
    n3,n4 = [int(n) for n in extra_feats_num.split(':')]
    init_feats  = global_important_feats[n1:n2]
    extra_feats = global_important_feats[n3:n4]
    f_batch_size = 1
    eval_train, eval_valid  = train_test(mode='just_valid',feat_csvs = global_feats_csvs, need_feats = init_feats)
    range_len  = len(extra_feats) / f_batch_size
    range_len  = range_len if int(range_len) == range_len else range_len + 1
    best_valid, best_train = 1.0, 1.0
    for i in  range(range_len):
        print_time(i)
        add_feats   = extra_feats[i*f_batch_size: (i+1)*f_batch_size]
        #temp_feats = init_feats + add_feats
        init_feats  = init_feats + add_feats
        eval_train, eval_valid  = train_test(mode='just_valid',feat_csvs = global_feats_csvs, need_feats = init_feats)#temp_feats)
        context = '\n**** extra_feat =  '+str(add_feats)+'\n**** eval_train , eval_valid = '+str(eval_train)+', '+str(eval_valid)
        subject = 'TSA_contest'
        print context
        if i == 0:
            context_concat  = context
        else:
            context_concat += context
        if is_email and i==5:
            try:
                send_email.send_email(context,subject)
            except:
                pass
        #*************************************************************************
        if best_valid - eval_valid < 8e-5:
            print 'delte this feats --- ',add_feats
            init_feats = [f for f in init_feats if f not in add_feats]
        else:
            best_train, best_valid = eval_train, eval_valid
        print '*** best_train, best_valid ***',best_train, best_valid
        print '********* cur_feats_num ******',len(init_feats)
        #*************************************************************************
    with open('./feature_name_importance.txt', 'a') as fa:
        fa.writelines(context_concat)



def train_main(test_type = 'test_csvs', mode='just_valid', init_num = '0:10', extra_num = '10:300'):
        
    if test_type == 'test_csvs':
        run_model_test_csvs(init_num, extra_num)
        return
    if test_type == 'test_feats':
        run_model_test_feats(init_num, extra_num)
        return
    train_test(mode, feat_csvs= global_feats_csvs, need_feats =global_important_feats)



if __name__ == '__main__':
    t1= time.time()
    fire.Fire(train_main)
    t2= time.time()
    print 'run: ',t2-t1

