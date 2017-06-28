import pandas as pd
!vim model_stack.py
global_feats= list(set([f.strip() for f in pd.read_csv('./old_features.csv', header=None).iloc[:,0].values.tolist()]))
len(global_feats)
global_feats
new_feats= list(set([f.strip() for f in pd.read_csv('./features.csv', header=None).iloc[:,0].values.tolist()]))
new_feats[:10]
!vim model_stack.py
re_sub0         = lambda f: re.sub(re.compile('beforeday_\d'),'beforeday_7',f)
re_sub0         = lambda f: re.sub(re.compile('_feat_set_'),'_beforeday_9_feat_set_',f)
global_feats = [re_sub0(f) for f in global_feats ]
import re
global_feats = [re_sub0(f) for f in global_feats ]
global_feats
data_set_feats = [f  for f in global_feats if 'data_set' in f]
data_set_feats
re_sub0         = lambda f: re.sub(re.compile('_feat_set_'),'_beforeday_9_feat_set_',f)
resub1          = lambda f: re.sub(re.compile('_beforeday_9_'),'',f)
global_feats = [resub1(f) if 'data_set' in f else f for f in global_feats]
global_feats
data_set_feats = [f  for f in global_feats if 'data_set' in f]
data_set_feats
global_feats= list(set([f.strip() for f in pd.read_csv('./old_features.csv', header=None).iloc[:,0].values.tolist()]))
resub1          = lambda f: re.sub(re.compile('_beforeday_9_'),'',f)
re_sub0         = lambda f: re.sub(re.compile('_feat_set_'),'_beforeday_9_feat_set_',f)
data_set_feats = [f  for f in global_feats if 'data_set' in f]
data_set_feats[:2]
resub2          = lambda f: re.sub(re.compile('_click_total_'),'_beforeday_9_click_total_',f)
!vim extract_feature.py
base_feats= ['creativeID', 'userID', 'positionID', 'connectionType', 'telecomsOperator', 'adID', 'camgaignID',
             'advertiserID','appID', 'appPlatform', 'age','gender','education', 'marriageStatus','haveBaby','hometown',
             'residence',  'sitesetID', 'positionType', 'appCategory', 'click_day',
             'has_installed_this_app_long_time_ago']
!vim extract_feature.py
for feats in itertools.combinations(base_feats, 1):
    suffix      = reduce(lambda f1,f2: f1+'_'+f2,  feats)
    suffix_day  = '_beforeday_9'
    fset_total_count                = suffix + suffix_day + '_feat_set_click_total_count'
    ###### this feature just compute 1 time　##########################
    dset_total_count                = suffix + '_data_set_click_total_count'
    ###################################################################
    total_count_dset_in_fset_rate   = suffix + suffix_day + '_click_total_count_data_set_in_feat_set_rate'
    fset_label_1_count              = suffix + suffix_day + '_feat_set_click_label_1_count'
    fset_label_1_count_in_total_rate= suffix + suffix_day + '_feat_set_click_label_1_count_in_total_rate'
global_feats= list(set([f.strip() for f in pd.read_csv('./old_features.csv', header=None).iloc[:,0].values.tolist()]))
suffix_day  = '_beforeday_9'
re_sub_1  = lambda f: re.sub(re.compile('_feat_set_click_total_count'), suffix_day + '_feat_set_click_total_count',f)
re_sub_1  = lambda f: re.sub(re.compile('_click_total_count_data_set_in_feat_set_rate'), suffix_day + '_click_total_count_data_set_in_feat_set_rate',f)
re_sub_1  = lambda f: re.sub(re.compile('_feat_set_click_total_count'), suffix_day + '_feat_set_click_total_count',f)
re_sub_2  = lambda f: re.sub(re.compile('_click_total_count_data_set_in_feat_set_rate'), suffix_day + '_click_total_count_data_set_in_feat_set_rate',f)
re_sub_3  = lambda f: re.sub(re.compile('_feat_set_click_label_1_count'), suffix_day + '_feat_set_click_label_1_count',f)
re_sub_4  = lambda f: re.sub(re.compile('_feat_set_click_label_1_count_in_total_rate'), suffix_day + '_feat_set_click_label_1_count_in_total_rate',f)
re_sub_all = lambda f: re_sub_4(re_sub_3(re_sub_2(re_sub_1(f))))
global_feats = [re_sub_all(f) for f in global_feats]
global_feats
global_feats= list(set([f.strip() for f in pd.read_csv('./old_features.csv', header=None).iloc[:,0].values.tolist()]))
re_sub_1  = lambda f: re.sub(re.compile('_feat_set_click_total_count'), suffix_day + '_feat_set_click_total_count',f)
re_sub_2  = lambda f: re.sub(re.compile('_click_total_count_data_set_in_feat_set_rate'), suffix_day + '_click_total_count_data_set_in_feat_set_rate',f)
re_sub_3  = lambda f: re.sub(re.compile('_feat_set_click_label_1_count'), suffix_day + '_feat_set_click_label_1_count',f)
re_sub_4  = lambda f: re.sub(re.compile('_feat_set_click_label_1_count_in_total_rate'), suffix_day + '_feat_set_click_label_1_count_in_total_rate',f)
s1 = '_feat_set_click_total_count'
s2 = '_click_total_count_data_set_in_feat_set_rate'
s3 = '_feat_set_click_label_1_count'
s4 = '_feat_set_click_label_1_count_in_total_rate'
re_sub_all = lambda f: re_sub_3(re_sub_2(re_sub_1(f)))
global_feats = [re_sub_all(f) for f in global_feats]
global_feats
with open('bd_features.csv','w') as fw:
    for f in global_feats:
        fw.writelines(f+'\n')
%hist -f TSA_history.py
