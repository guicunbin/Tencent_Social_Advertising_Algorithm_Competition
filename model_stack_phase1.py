# -*- coding: utf-8 -*-
"""
baseline 2: ad.csv (creativeID/adID/camgaignID/advertiserID/appID/appPlatform) + lr
"""
#####TODO   lr use onehot features to get a output proba [n_samples,1] 
#####       use as a strongest feature to feed in lgb with other count features
#####TODO    use lr and lgb results merge
import zipfile
import pandas as pd
import lightgbm as lgb
import os
import time
from scipy import sparse
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LogisticRegression
from utils import *
from extract_feature import *
import fire
import itertools
import send_email
import copy
import re
# define params
split_time  = 270000
neg_pos     = None
data_root   = "./datasets/train/"
is_email    = False
feat_csv    = './bd_features.csv'
is_concat   = False
### *****for lr the folowing feats get test 0.104140******
#lr_feats = ["creativeID", "adID", "camgaignID", "advertiserID", "appID", "appPlatform", "connectionType", "telecomsOperator",
#            "has_installed_this_app",  'age', 'gender','education', 'marriageStatus', 'haveBaby', 'appPlatform', 'sitesetID', 
#            'positionType','appCategory','positionID']
#
#base_feats =['creativeID', 'userID', 'positionID', 'connectionType', 'telecomsOperator', 'adID', 'camgaignID',
#             'advertiserID','appID', 'appPlatform', 'age','gender','education', 'marriageStatus','haveBaby','hometown',
#             'residence',  'sitesetID', 'positionType', 'appCategory',
#             'has_installed_this_app_long_time_ago']
#before_day  = 9
#suffix_day  = '_beforeday_'+str(before_day)
#global_feats =  [f+'_feat_set_click_total_count'                     for f in base_feats]+\
#                [f+'_click_total_count_data_set_in_feat_set_rate'    for f in base_feats]+\
#                [f+'_feat_set_click_label_1_count'                   for f in base_feats if f != 'click_day']+\
#                [f+'_feat_set_click_label_1_count_in_total_rate'     for f in base_feats if f != 'click_day']+\
#                [f+'_data_set_click_total_count'                     for f in base_feats]
#
#cate_feats = []
##cate_feats =   ['gender', 'education','haveBaby',
##                'positionType','connectionType','telecomsOperator','has_installed_this_app_long_time_ago'
##                ]
## 这些类别特征之前已经用　count　型的特征表示了，这时候再拿出来用，就是和上面的特征重复了，所以会出现过拟合，就是特征的相关性太大的原因
#global_feats = global_feats + cate_feats
#
#
#base_2_feats = list(itertools.combinations(base_feats,2)) 
#suffix = lambda li: reduce(lambda x,y: x+'_'+y, li)
#
#two_feats =     [suffix(f) + '_feat_set_click_label_1_count_in_total_rate'     for f in base_2_feats if 'click_day' not in f]+\
#                [suffix(f) + '_feat_set_click_total_count'                     for f in base_2_feats]+\
#                [suffix(f) + '_feat_set_click_label_1_count'                   for f in base_2_feats if 'click_day' not in f]+\
#                [suffix(f) + '_click_total_count_data_set_in_feat_set_rate'    for f in base_2_feats]+\
#                [suffix(f) + '_data_set_click_total_count'                     for f in base_2_feats]
#
##global_feats= list(set([f.strip() for f in pd.read_csv(feat_csv, header=None).iloc[:,0].values.tolist()]))
##rank_time = ['clickTime', 'click_day', 'click_day_hour', 'click_day_hour_minu']
##rank_feats= [key+'_rank'  for key in rank_time] + [key+'_rank_bool' for key in rank_time]
##global_feats += rank_feats
global_feats    = [f.strip()  for f in pd.read_csv(feat_csv, header=None).iloc[:,0].values.tolist()]
re_sub0         = lambda f: re.sub(re.compile('beforeday_\d'),'beforeday_7',f)
re_sub1         = lambda f: re.sub(re.compile('beforeday_\d'),'beforeday_4',f)
global_feats_0  = [re_sub0(f) for f in global_feats if 'beforeday' in f]
global_feats_1  = [re_sub1(f) for f in global_feats if 'beforeday' in f]
##global_feats.reverse()
#### TODO use following feats to test_feats
two_feats   = []
cate_feats  = []
train_set_csv = './datasets/train/data_set1.csv'
train_extra0  = './datasets/train/data_set1_0.csv'
train_extra1  = './datasets/train/data_set1_1.csv'
train_concat  = './datasets/train/data_set1_concat.csv'

valid_set_csv = './datasets/train/data_set2.csv'
valid_extra0  = './datasets/train/data_set2_0.csv'
valid_extra1  = './datasets/train/data_set2_1.csv'
valid_concat  = './datasets/train/data_set2_concat.csv'

test_set_csv  = './datasets/train/data_set3.csv'
test_extra0   = './datasets/train/data_set3_0.csv'
test_extra1   = './datasets/train/data_set3_1.csv'
test_concat   = './datasets/train/data_set3_concat.csv'
#with open(train_set_csv,'r') as fa:
#    global_feats = [f.strip()  for f in fa.readline().split(',')[4:]]



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
    'max_depth':5,          ## max_depth  : 1    2    3    4      5      6    ....           n
    'num_leaves':20,        ## num_leaves : 2   3-4  3-8  3-16   3-32   3-64  ....          3-2^n
    'learning_rate': 0.1,
#########################
    'min_data_in_leaf':100,
    'drop_rate':0.1,
    'feature_fraction': 0.9,
    'bagging_fraction': 0.9,
    'bagging_freq': 5,
    'verbose': 0
}




def get_lr_data():
    dfTrain = pd.read_csv(data_root+'f_train_ad_user_position_appCategories_appActions_appInstalled.csv', dtype='float32') 
    dftest  = pd.read_csv(data_root+'f_test_ad_user_position_appCategories_appActions_appInstalled.csv',  dtype='float32') 
    dftrain = dfTrain[dfTrain.click_day.apply(lambda x: x<split_time)]
    ## TODO get_lr_data
    print "# feature engineering/encoding"
    enc = OneHotEncoder()
    for i,feat in enumerate(lr_feats):
        x_train_total = enc.fit_transform(dfTrain[feat].values.reshape(-1, 1))
        x_train       = enc.transform(dftrain[feat].values.reshape(-1, 1))
        x_valid       = enc.transform(dfvalid[feat].values.reshape(-1, 1))
        x_test        = enc.transform(dftest[feat].values.reshape(-1, 1))
        if i == 0:
            X_train_total, X_train, X_valid, X_test =   x_train_total, x_train, x_valid,  x_test
        else:
            X_train_total, X_train, X_valid, X_test =   sparse.hstack((X_train_total, x_train_total)),\
                                                        sparse.hstack((X_train, x_train)),\
                                                        sparse.hstack((X_valid, x_valid)),      sparse.hstack((X_test, x_test))
        print (X_train).shape
    return X_train_total, y_train_total,    X_train, y_train,   X_valid, y_valid,   X_test, instanceID





def lgb_data_by_type_and_feats(model='lgb', use_type='train_total', feats=['userID']):
    print "load data ......"
    if 'train' in use_type:
        X_train             = pd.read_csv(train_set_csv, dtype='float32',usecols = feats+['label'])
        X_valid             = pd.read_csv(valid_set_csv, dtype='float32',usecols = feats+['label'])
        if is_concat:
            t       = pd.read_csv(train_extra0,  dtype='float32',usecols = global_feats_0)
            X_train = pd.concat([X_train, t], axis=1) 
            t       = pd.read_csv(train_extra1,  dtype='float32',usecols = global_feats_1)
            X_train = pd.concat([X_train, t], axis=1)
            t       = pd.read_csv(valid_extra0,  dtype='float32',usecols = global_feats_0)
            X_valid = pd.concat([X_valid, t], axis=1) 
            t       = pd.read_csv(valid_extra1,  dtype='float32',usecols = global_feats_1)
            X_valid = pd.concat([X_valid, t], axis=1)
            X_train.to_csv(train_set_csv, index=False)
            X_valid.to_csv(valid_set_csv, index=False)

        print X_train.shape
        #### change_to_category 
        X_train, X_valid    = change_to_category([X_train, X_valid], cate_feats)

        if  use_type == 'train_valid':
            y_train         = X_train["label"].values
            y_valid         = X_valid["label"].values
            X_train         = X_train.drop('label', axis=1)
            X_valid         = X_valid.drop('label', axis=1)
            print 'positive percent ',y_train[y_train==1].shape[0]*1.0/y_train.shape[0]
            if   model == 'lgb':
                lgb_train   = lgb.Dataset(X_train,  y_train)
                lgb_valid   = lgb.Dataset(X_valid,  y_valid, reference=lgb_train)
                return lgb_train, lgb_valid
            elif model == 'lr':
                return X_train, y_train, X_valid, y_valid
        
        elif use_type == 'train_total':
            X_train_total   = pd.concat([X_train, X_valid],axis=0)
            y_train_total   = X_train_total['label'].values
            X_train_total   = X_train_total.drop('label',axis=1)
            print X_train_total.shape
            if   model == 'lgb': 
                lgb_train_total = lgb.Dataset(X_train_total, y_train_total)
                return lgb_train_total
            elif model == 'lr':
                return X_train_total, y_train_total

    elif use_type == 'test':
        X_test      = pd.read_csv(test_set_csv, dtype='float32',usecols = feats+['instanceID'])
        if is_concat:
            t       = pd.read_csv(test_extra0,  dtype='float32',usecols = global_feats_0)
            X_test  = pd.concat([X_test, t], axis=1) 
            t       = pd.read_csv(test_extra1,  dtype='float32',usecols = global_feats_1)
            X_test  = pd.concat([X_test, t], axis=1)
            X_test.to_csv(test_set_csv, index=False)
        #### change_to_category 
        X_test,         = change_to_category([X_test], cate_feats)
        instanceID      = X_test["instanceID"].astype('int32').values
        X_test          = X_test.drop('instanceID', axis=1)
        return X_test, instanceID
        



def lr_model_get_prob():
    X_train_total, y_train_total,    X_train, y_train,   X_valid, y_valid,   X_test, instanceID    = get_data('lr')
    print "# model training in split train_set "
    ##### lr model 
    lr = LogisticRegression()
    lr.fit(X_train, y_train)
    prob_train = lr.predict_proba(X_train)[:,1].reshape(-1,1)
    prob_valid = lr.predict_proba(X_valid)[:,1].reshape(-1,1)
    eval_train = round(logloss(y_train, prob_train), 6)
    eval_valid = round(logloss(y_valid, prob_valid), 6)
    print 'lr eval_train eval_valid----- ', eval_train, eval_valid
    lr.fit(X_train_total, y_train_total)
    prob_train_total= lr.predict_proba(X_train_total)[:,1].reshape(-1,1)
    proba_test      = lr.predict_proba(X_test)[:,1].reshape(-1,1)
    return prob_train_total, prob_train, prob_valid, proba_test





def train_test(mode, feats):
    #prob_train_total,       prob_train,       prob_valid,       proba_test                          = lr_model_get_prob()
    ##### lgb model 
    Dataset_train,    Dataset_valid = lgb_data_by_type_and_feats(model='lgb', use_type='train_valid', feats=feats)
    ###### Dataset append lr_prob
    #Dataset_train_total.data= np.concatenate([Dataset_train_total.data, prob_train_total])
    #Dataset_train.data      = np.concatenate([Dataset_train.data,       prob_train])
    #Dataset_valid.data      = np.concatenate([Dataset_valid.data,       prob_valid])
    #Dataset_train_total.set_feature_name(feats+['lr_prob'])
    #Dataset_train.set_feature_name(feats+['lr_prob'])
    #Dataset_valid.set_feature_name(feats+['lr_prob'])
    #X_test['lr_prob']=prob_test
    gbm = lgb.train(params      = params_0,
                    train_set   = Dataset_train,
                    num_boost_round = 500,
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
    

    #####  use total train_set train again
    print 'model training in total train_set'
    print ' gbm.best_iteration: ',gbm.best_iteration
    Dataset_train_total = lgb_data_by_type_and_feats(model='lgb', use_type='train_total', feats=feats)
    gbm = lgb.train(params = params_0,    
                    train_set   = Dataset_train_total,
                    num_boost_round = gbm.best_iteration if gbm.best_iteration!=-1 else gbm.current_iteration(),
                    fobj = None,    feval=self_eval)
    X_test ,instanceID  = lgb_data_by_type_and_feats(model='lgb', use_type='test', feats=feats)
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
    df.to_csv(sub_file_name, index=False)
    print 'save file to ',sub_file_name





def main(test_feats = False, init_feats=global_feats, extra_feats=two_feats):
    f_batch_size = 100
    if test_feats:
        eval_train, eval_valid  = train_test(mode='just_valid',feats=init_feats)
        range_len = len(extra_feats) / f_batch_size
        range_len = range_len if int(range_len) == range_len else range_len + 1
        for i in  range(range_len):
            print_time(i)
            add_feats   = extra_feats[i*f_batch_size: (i+1)*f_batch_size]
            temp_feats  = init_feats + add_feats
            eval_train, eval_valid  = train_test(mode='just_valid',feats=temp_feats)
            context = '\n**** extra_feat =  '+str(add_feats)+'\n**** eval_train , eval_valid = '+str(eval_train)+', '+str(eval_valid)
            subject = 'TSA_contest'
            print context
            if is_email:
                try:
                    send_email.send_email(context,subject)
                except:
                    pass
            with open('./feature_name_importance.txt', 'a') as fa:
                fa.writelines(context)
    else:
        train_test('test',feats=global_feats)


if __name__ == '__main__':
    t1= time.time()
    main(test_feats = False, init_feats = global_feats[:100], extra_feats = global_feats[100:])
    t2= time.time()
    print 'run: ',t2-t1

