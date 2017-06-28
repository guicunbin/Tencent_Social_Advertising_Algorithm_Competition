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
# define params
split_time  = 270000
neg_pos     = None
data_root   = "./datasets/train/"
### *****for lr the folowing feats get test 0.104140******
#feats = ["creativeID", "adID", "camgaignID", "advertiserID", "appID", "appPlatform", "connectionType", "telecomsOperator",
#         "has_installed_this_app",  'age', 'gender','education', 'marriageStatus', 'haveBaby', 'appPlatform', 'sitesetID', 
#         'positionType','appCategory','positionID']
#
feats =['creativeID', 'userID', 'positionID', 'connectionType', 'telecomsOperator', 'adID', 'camgaignID',
        'advertiserID','appID', 'appPlatform', 'age','gender','education', 'marriageStatus','haveBaby','hometown',
        'residence',  'sitesetID', 'positionType', 'appCategory',
        'has_installed_this_app_long_time_ago']
feats = [f+'_feat_set_click_total_count'                     for f in feats]+\
        [f+'_click_total_count_data_set_in_feat_set_rate'    for f in feats]+\
        [f+'_feat_set_click_label_1_count'                   for f in feats if f != 'click_day']+\
        [f+'_feat_set_click_label_1_count_in_total_rate'     for f in feats if f != 'click_day']+['age']+\
        [f+'_data_set_click_total_count'                     for f in feats]
        #[f+'_feat_set_click_label_0_count'                   for f in feats if f != 'click_day']+\
        #[f+'_feat_set_click_label_0_count_in_total_rate'     for f in feats if f != 'click_day']

cate_feats = []
cate_feats =   ['gender', 'education','haveBaby',
                'positionType','connectionType','telecomsOperator','has_installed_this_app_long_time_ago'
                ]
# 这些类别特征之前已经用　count　型的特征表示了，这时候再拿出来用，就是和上面的特征重复了，所以会出现过拟合，就是特征的相关性太大的原因
feats = feats + cate_feats

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
    'max_depth':5  ,     ## max_depth  : 1    2    3    4      5      6    ....           n
    'num_leaves':16  ,    ## num_leaves : 2   3-4  3-8  3-16   3-32   3-64  ....          3-2^n
    'learning_rate': 0.1,
#########################
    'min_data_in_leaf':100,
    'drop_rate':0.1,
    'feature_fraction': 0.9,
    'bagging_fraction': 0.9,
    'bagging_freq': 5,
    'verbose': 0
}




def get_data(model='lgb'):
    print "load data ......"
    dftrain         = pd.read_csv(data_root+'data_set1.csv', dtype='float32')
    dfvalid         = pd.read_csv(data_root+'data_set2.csv', dtype='float32')
    dftest          = pd.read_csv(data_root+'data_set3.csv', dtype='float32')
    #### change_to_category 
    dftrain, dfvalid, dftest = change_to_category([dftrain, dfvalid, dftest], cate_feats)

    dfTrain         = pd.concat([dftrain, dfvalid],axis=0)
    instanceID      = dftest["instanceID"].astype('int32').values
    #### 划分train valid test
    y_train_total   = dfTrain['label'].values
    y_train         = dftrain["label"].values
    y_valid         = dfvalid['label'].values
    print 'positive percent ',y_train[y_train==1].shape[0]*1.0/y_train.shape[0]


    
    print "# feature engineering/encoding"
    if model == 'lr':
        enc = OneHotEncoder()
        for i,feat in enumerate(feats):
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
    if model== 'lgb':
        X_train_total = dfTrain[feats]
        X_train       = dftrain[feats]
        X_valid       = dfvalid[feats]
        X_test        = dftest[feats]
        print (X_train).shape
        lgb_train_total = lgb.Dataset(X_train_total, y_train_total, )
        lgb_train       = lgb.Dataset(X_train,  y_train,            )
        lgb_valid       = lgb.Dataset(X_valid,  y_valid,            reference=lgb_train)
        return  lgb_train_total, lgb_train, lgb_valid,  X_test, instanceID



def train_test(model, mode):
    if model == 'lr':
        X_train_total, y_train_total,    X_train, y_train,   X_valid, y_valid,   X_test, instanceID    = get_data(model)
    if model == 'lgb':
        Dataset_train_total,    Dataset_train,    Dataset_valid,    X_test, instanceID                 = get_data(model)


    print "# model training in split train_set "
    ##### lr model 
    if model == 'lr':
        lr = LogisticRegression()
        lr.fit(X_train, y_train)
        eval_train = round(logloss(y_train,     lr.predict_proba(X_train)[:,1]),6)
        eval_valid = round(logloss(y_valid,     lr.predict_proba(X_valid)[:,1]),6)
    ##### lgb model 
    if model == 'lgb':
        gbm = lgb.train(params = params_0,    
                        train_set   = Dataset_train,
                        num_boost_round = 500,
                        valid_sets  = Dataset_valid,
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
        fa.writelines('\n\n\n************* new model ************')
        fa.writelines('\neval_train = '+str(eval_train))
        fa.writelines('\neval_valid = '+str(eval_valid)+'\n')
        if model=='lr':
            fa.writelines('\n\n####### feats #######\n'+str(feats))
        if model=='lgb':
            feature_importance = gbm.feature_importance(importance_type="gain")
            feature_names      = gbm.feature_name()
            sorted_idx         = np.argsort(feature_importance)
            for i in sorted_idx:
                st=str(feature_names[i])+' : '+str(feature_importance[i])+'\n'
                fa.writelines(st)
            
    if mode == 'just_valid':
        return 
     
    

    #####  use total train_set train again
    print 'model training in total train_set'
    #### lr model
    if model == 'lr':
        lr.fit(X_train_total, y_train_total)
        proba_test  = lr.predict_proba(X_test)[:,1]
    #### lgb model
    if model == 'lgb':
        print ' gbm.best_iteration: ',gbm.best_iteration
        gbm = lgb.train(params = params_0,    
                        train_set   = Dataset_train_total,
                        num_boost_round = gbm.best_iteration if gbm.best_iteration!=-1 else gbm.current_iteration(),
                        fobj = None,    feval=self_eval)
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





def main(test_feats = False):
    extra_feats = []
    if test_feats:
        for i in  range(len(extra_feats)):
            feats.append(extra_feats[i])
            fire.Fire(train_test)
    else:
        fire.Fire(train_test)



if __name__=='__main__':
    t1= time.time()
    main(test_feats = False)
    t2= time.time()
    print 'run: ',t2-t1

