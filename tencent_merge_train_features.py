import pandas as pd
    
def get_merge_features(mode):
    
    t2 = pd.read_csv('./datasets/train/user_installedapps.csv',dtype='int32')
    t2['has_installed_this_app']=1
    t1 = pd.read_csv('./datasets/train/f_train_user_position_app_categories.csv')
    t1 = pd.merge(t1, t2, how='left', on=['userID','appID'])
    t1.has_installed_this_app = t1.has_installed_this_app.fillna(0).astype('int32')
    t1.conversionTime = t1.conversionTime.fillna(value=-1).astype('int32')
    for c in t1.columns.tolist():
        t1[c] = t1[c].astype('int32')
    t3 = pd.read_csv('./datasets/train/user_app_actions.csv',dtype='int32')
    t1['click_day']=t1.clickTime.apply(lambda x: int(str(x)[:-4])).astype('int32')
    print t1[['click_day','clickTime']][:5]
    t3['install_day']=t3.installTime.apply(lambda x: int(str(x)[:-4])).astype('int32')
    print t3[['installTime','install_day']][:5]
    t2 = pd.merge(t1,t3,how='left',on=['userID','appID'])
    print t2[['appID','click_day','install_day','has_installed_this_app']][89:100]
    t2.installTime = t2.installTime.fillna(value=999999).astype('int32')
    t2.install_day = t2.install_day.fillna(value=99).astype('int32')
    print t2[['appID','click_day','install_day','has_installed_this_app']][89:100]
    t2.has_installed_this_app = t2.apply(lambda x: 1 if x.click_day > x.install_day else x.has_installed_this_app, axis=1)
    print t2[['appID','click_day','install_day','has_installed_this_app']][89:100]
    t2.to_csv('./datasets/train/f_train_ad_user_position_appCategories_appActions_appInstalled.csv', index=False)
