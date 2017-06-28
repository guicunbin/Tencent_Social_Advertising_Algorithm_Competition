#import pandas as pd
#import dask.dataframe as pd
import pandas as pd
import fire
from utils import *
data_dir = './datasets/dataset/'

def get_rank_feats_to_csv(mode='dataset1', groupby_feats = ['userID','creativeID']):
    print 'process .... '+mode
    t = pd.read_csv('./datasets/dataset/' + mode +'.csv').apply(small_dtype)
    idx = 'index'
    t = t.sort_values([idx], ascending=[True])
    t['click_day']              = t.clickTime.apply(lambda x: int(str(int(x))[:-6])).astype('int16')
    t['click_day_hour']         = t.clickTime.apply(lambda x: int(str(int(x))[:-4])).astype('int16')
    t['click_day_hour_minu']    = t.clickTime.apply(lambda x: int(str(int(x))[:-2])).astype('int32')
    t['click_day_hour_minu_s1'] = t.clickTime.apply(lambda x: int(str(int(x))[:-1])).astype('int32')
    for key in ['clickTime', 'click_day', 'click_day_hour', 'click_day_hour_minu', 'click_day_hour_minu_s1']:
        t[key+'_rank']      = t.groupby(groupby_feats + [key]).cumcount().astype('int32')
        t[key+'_rank_mul_timeDistance'] = t.apply(lambda x: (x['clickTime']-x['click_day']*10**6)*x[key+'_rank'],axis=1).astype('int32')
        t[key+'_rank_bool'] = t[key+'_rank'].apply(lambda x: 1 if x==0 else 0).astype('int32')
    print t[:10]
    t.to_csv('./datasets/dataset/' + mode + '.csv', index=False, chunksize=50000)
    
    







def merge_some(mode):
    #t1 = pd.read_csv('./datasets/train/'+mode+'.csv',dtype= 'float32')
    #print 'merge 1 .....'
    #t1 = pd.merge(t1, pd.read_csv('./datasets/train/ad.csv', dtype='int32'),                 on='creativeID')
    #print 'merge 2 .....'
    #t1 = pd.merge(t1, pd.read_csv('./datasets/train/user.csv', dtype='int32'),               on='userID')
    print 'merge 3 .....'
    t1 = pd.merge(t1, pd.read_csv('./datasets/train/position.csv', dtype='int32'),           on='positionID')
    print 'merge 4 .....'
    t1 = pd.merge(t1, pd.read_csv('./datasets/train/app_categories.csv', dtype='int32'),     on='appID')
    print t1.shape
    t1.to_csv('./datasets/train/f_'+mode+'_ad_user_position_appCategories.csv', index=False)
    return t1



def merge_csv_and_simple_feat(mode):
    t1 = merge_some(mode)
    t2 = pd.read_csv('./datasets/train/user_installedapps.csv',dtype='int32')
    t2['has_installed_this_app_long_time_ago']=1
    t2 = t2.astype('int32')
    print 'merge 1 ....'
    t1 = pd.merge(t1, t2, how='left', on=['userID','appID'])
    t1.has_installed_this_app_long_time_ago   = t1.has_installed_this_app_long_time_ago.fillna(0).astype('int32')
    try:
        t1.conversionTime       = t1.conversionTime.fillna(value=-1).astype('int32')
    except:
        pass
    t1 = t1.astype('int32')
    print t1[['clickTime','click_day']][:20]
    t1.to_csv('./datasets/train/f_'+mode+'_ad_user_position_appCategories_appInstalled.csv', index=False)
    
    
    t2 = pd.read_csv('./datasets/train/user_app_actions.csv',dtype='int32')
    t2['install_day'] = t2.installTime.apply(lambda x: int(str(x)[:-6])).astype('int32')
    print t2[['installTime','install_day']][:20]
    print 'merge 2 ....'
    t1 = pd.merge(t1,t2,how='left',on=['userID','appID'])
    print t1[['appID','click_day','installTime','install_day','has_installed_this_app_long_time_ago']][89:100]
    t1.installTime = t1.installTime.fillna(value=99999999).astype('int32')
    t1.install_day = t1.install_day.fillna(value=99).astype('int32')
    print t1[['appID','click_day','installTime','install_day','has_installed_this_app_long_time_ago']][89:100]
    t1['has_installed_this_app'] = t1.apply(lambda x: 1 if x.click_day > x.install_day else x.has_installed_this_app_long_time_ago, axis=1)
    print t1[['appID','click_day','installTime','install_day','has_installed_this_app_long_time_ago']][89:100]
    t1.to_csv('./datasets/train/f_'+mode+'_ad_user_position_appCategories_appActions_appInstalled.csv', index=False)
    


#if __name__=='__main__':
#    #get_rank_feats_to_csv('dataset1')
#    #get_rank_feats_to_csv('dataset2')
#    #get_rank_feats_to_csv('dataset3')
#    ##merge_csv_and_simple_feat('train')
#    ##merge_csv_and_simple_feat('test')

