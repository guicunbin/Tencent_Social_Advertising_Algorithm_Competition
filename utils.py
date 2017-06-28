#coding: utf-8
import scipy as sp
import numpy as np
import pandas as pd
import time
from tqdm import tqdm
import matplotlib.pyplot as plt
#important_feats_csv = './features.csv'
#important_feats_csv = './features_after_corr_select.txt'
#important_feats     = list(set([f.strip() for f in open(important_feats_csv).readlines() if f.strip()]))
#important_feats = None
#print 'important_feats :  ',len(important_feats)


def is_firstlastone(x):
    if x==0:
        return int(1)
    elif x>0:
        return int(0)
    else:
        #those only once
        return int(-1)
        
    


def compute_distance(x):
    if x>=0 or x<0:
        return  int(x)
    else:
        #np.nan
        #those only  once
        return int(-1)








def plot_feat_label(dataset, feat_col, label_col):
    dataset = dataset[[feat_col,label_col]]
    df = dataset.groupby(feat_col)[label_col].mean()
    if len(df)<20:
        df.plot(kind='bar')
    else:
        df.plot(kind='line')
    plt.show()
    return df






def get_csv_header(csv):
    feats = [f.strip() for f in open(csv,'r').readline().split(',')]
    return feats



def get_need_feats(csvs, is_rate = True, is_tiny=False, important_feats=[]):
    '''
    concat csvs to df_concat 
    '''
    #print csvs
    if not csvs:
        return pd.DataFrame()
    is_first    = True
    feats_all   = []
    for csv in tqdm(csvs):
        need_feats = [f for f in get_csv_header(csv) if f not in feats_all]
        if important_feats:
            need_feats = [f for f in need_feats if f in important_feats]
        if is_rate:
            need_feats = [f for f in need_feats if 'rate' in f]
        if len(need_feats) == 0:
            continue
        df         = pd.read_csv(csv, usecols = need_feats).apply(small_dtype)
        df         = df[:1000000] if is_tiny  else df
        df_concat  = df if is_first else  pd.concat([df_concat, df], axis=1)
        feats_all+= need_feats
        is_first   = False
    #feats_all = list(set(feats_all))
    #print len(feats_all)
    ## delete duplicate feats
    #df_concat = df_concat[feats_all]
    try:
        print df_concat.shape
        print df_concat.info()
        return df_concat
    except:
        return pd.DataFrame()






def small_dtype(x):
    '''
    this is very very useful to reduce Memory_using  ! ! ! !
    but please ensure your dataframe's float number is small than 2^15 ! ! ! !
    or change you large float number to int32,  then use this function
    **********************************
    useage: df = df.apply(small_dtype)
    **********************************
    
    '''
    #return x.astype(np.float16) if 'float' in str(x.dtype) else pd.to_numeric(x downcast='integer')
    return pd.to_numeric(x, downcast='integer') if 'int' in str(x.dtype) else x.astype(np.float16)





def logloss(act, pred):
    epsilon = 1e-15
    pred = sp.maximum(epsilon, pred)
    pred = sp.minimum(1-epsilon, pred)
    ll = sum(act*sp.log(pred) + sp.subtract(1,act)*sp.log(sp.subtract(1,pred)))
    ll = ll * -1.0/len(act)
    return ll


def print_time(i):
    global t1, t2
    t2 = time.time()
    try:
        t3 = t2-t1; print " this step "+str(i)+" run_time:  ",t3,'\n'
    except:
        pass
    t1 = time.time()







def self_eval(pred,train_data):
    '''
    :pred 
    :train_data 或者 labels
    '''
    try:
        labels=train_data.get_label()
    except:
        labels=train_data
    epsilon = 1e-15
    pred = np.maximum(epsilon,  pred)
    pred = np.minimum(1-epsilon,pred)
    ll = sum(labels*np.log(pred) + (1 - labels)*np.log(1 - pred))
    ll = ll * (-1.0)/len(labels)
    return 'log loss', ll, False
    


def create_weights(df_train,use_column='label'):
    '''
    for binary classfier 
    labels= 0 and 1
    '''
    row_num=df_train.shape[0]
    weights=np.ones(shape=(row_num,),dtype=np.float)
    labels=np.array(df_train[use_column]) ##labels.shape=(row_num,)
    count_1=labels[labels==1].shape[0]
    count_0=labels[labels==0].shape[0]
    rate_0=1.0
    rate_1=count_1*1.0/count_0

    for i in range(row_num):
        if labels[i]==1:
            weights[i]=rate_1
    return weights


def change_to_category(df_li, columns_li):
    ''' 
    df_li:      all dfs in df_li will change same as each other
    columns_li: columns to be change
    '''
    for col in columns_li:
        for df in df_li:
            df[col]=df[col].astype("category")
    return df_li


def merge_reduce(df_li,key):
    return reduce(lambda x,y: pd.merge(x,y,on=key), df_li)





def compute_distinct_nums(df,feat):
    i=0
    for i,j in df[[feat]].groupby(feat):
        i+=1
    return i

if __name__ =='__main__':
    df=pd.read_csv('./datasets/train/f_train_ad_user_position_appCategories_appActions_appInstalled.csv')
    with open('./Readme.md', 'a') as fa:
        fa.writelines('\n\n## feat distinct nums')
        for feat in df.columns.tolist():
            fa.writelines('\n> '+feat+'  '+str(compute_distinct_nums(df, feat)))

