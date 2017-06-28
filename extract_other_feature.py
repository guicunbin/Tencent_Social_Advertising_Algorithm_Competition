import pandas as pd
import time
from utils import *
from split_data import *
from tqdm import tqdm
from extract_feature import *



def cond_prob_feat(data_set_path, feat_set_path, mode = 'train', cond=['userID','connectionType']):
    time1 = time.time()
    
    suffix          = reduce(lambda f1,f2: f1+'_'+f2,  cond)
    feats           = [cond[0]]
    save_csv        = feat_dir+mode+'/' + suffix + '_prob.csv'
    fset_total_cnt  = cond[0] + '_fset_total_cnt'
    if os.path.exists(save_csv):
        return
    
    data_set_total  = pd.read_csv(data_set_path, usecols = cond).apply(small_dtype)
    feat_set        = pd.read_csv(feat_set_path, usecols = cond).apply(small_dtype)
    ###### for total cnt
    t                         = feat_set[feats].copy()
    t[fset_total_cnt]         = np.ones([len(t),],  dtype='int32')
    t                         = t.groupby(feats).agg('sum').reset_index()
    data_set                  = data_set_total[feats]
    data_set                  = pd.merge(data_set, t, how='left', on = feats)
    data_set[fset_total_cnt]  = pd.to_numeric(data_set[fset_total_cnt].fillna(0).astype('int32'), downcast = 'integer')
    
    for con_num in tqdm(set(feat_set[cond[1]].values)):
        fset_con_num_cnt            = suffix + '_num_' + str(con_num) + '_cnt'
        fset_rate                   = fset_con_num_cnt + '_rate'
        t                           = feat_set.copy()
        t                           = t[t[cond[1]]== con_num][feats]
        t[fset_con_num_cnt]         = np.ones([len(t), 1], dtype='int32')
        t                           = t.groupby(feats).agg('sum').reset_index()
        data_set                    = pd.merge(data_set, t, how='left', on = feats)
        data_set[fset_con_num_cnt]  = pd.to_numeric(data_set[fset_con_num_cnt].fillna(0).astype('int32'), downcast='integer')
        ### for transfer_rate
        data_set[fset_rate]=\
                ((data_set[fset_con_num_cnt]+alpha) * 1.0 / (data_set[fset_total_cnt]+beta)).astype('float16')
    
    need_cols = [f for f in data_set.columns.tolist() if f not in feats]
    print data_set[:5]
    print '*************************************** write data ............'
    data_set[need_cols].to_csv(save_csv, mode='w', index=False,chunksize=100000)
    print 'run time -----',time.time() - time1





def use_cond_prob_feat(mode):
    if mode == 'train':
        ##### train:  data_set1   27   feat_set1     17->26
        cond_prob_feat(dataset1_csv, featset1_csv,  'train',    cond=['userID','connectionType'])
        cond_prob_feat(dataset1_csv, featset1_csv,  'train',    cond=['userID','positionType'])
    if mode == 'valid':
        #### valid   data_set2   28   feat_set2     18->27      
        cond_prob_feat(dataset2_csv, featset2_csv,  'valid',    cond=['userID','connectionType'])
        cond_prob_feat(dataset2_csv, featset2_csv,  'valid',    cond=['userID','positionType'])
    if mode == 'test':
        #### test    data_set3   31   feat_set3     21->30 
        cond_prob_feat(dataset3_csv, featset3_csv,  'test',     cond=['userID','connectionType'])
        cond_prob_feat(dataset3_csv, featset3_csv,  'test',     cond=['userID','positionType'])
    if mode == 'extra_1':
        #### extra_1 data_set4   29   feat_set3     19->28
        cond_prob_feat(dataset4_csv, featset4_csv,  'extra_1',  cond=['userID','connectionType'])
        cond_prob_feat(dataset4_csv, featset4_csv,  'extra_1',  cond=['userID','positionType'])




def main():
    modes = ['train', 'valid','test', 'extra_1']
    map(use_cond_prob_feat,   modes)




if __name__ == '__main__':
    main()


