from utils import *
import pandas as pd
import fire
import os


def preprocess():
    temp_csv  = './datasets/train/train_fillna.csv' 
    os.system('rm -rf '+temp_csv)
    train_csv = './datasets/train/train.csv'
    dfs = pd.read_csv(train_csv,chunksize=500000)
    is_first =True
    for df in dfs:
        df['conversionTime'] = df['conversionTime'].fillna(0).astype('int32')
        df.to_csv(temp_csv, index = False, mode = 'a', header = is_first)
        if is_first:
            is_first = False
    return temp_csv
       


def main(mode,phase=2):
    ''' mode = 'train' or 'test'
    '''
    print 'merge process ...... '+mode
    mode_csv = './datasets/train/' + mode + '.csv'
    #********************************
    if mode =='train':
        mode_csv = preprocess()
    #********************************
    df = pd.read_csv(mode_csv).apply(small_dtype)
    print 'process conversiontime'
    if 'conversionTime' in df.columns:
        df['conversionTime'] = df['conversionTime'].fillna(0).astype('int32')
    if int(phase) == 1:
        df['clickTime'] = df['clickTime']*100
    if int(phase) == 1 and 'conversionTime' in df.columns:
        df['conversionTime'] = df['conversionTime']*100

    df = pd.merge(df, pd.read_csv('./datasets/train/ad.csv').apply(small_dtype),'left',on='creativeID')
    df = pd.merge(df, pd.read_csv('./datasets/train/user.csv').apply(small_dtype),'left',on='userID')
    df = pd.merge(df, pd.read_csv('./datasets/train/position.csv').apply(small_dtype),'left',on='positionID')
    df = pd.merge(df, pd.read_csv('./datasets/train/app_categories.csv').apply(small_dtype),'left',on='appID')
    print df.info()
    df = pd.merge(df, pd.read_csv('./datasets/train/tb_user_app_actions_add_one_column.csv',dtype='int32').apply(small_dtype),'left',on=['userID','appID'])
    df.installTime = df.installTime.fillna(99999999).astype('int32')
    df.install_day = df.install_day.fillna(99).astype('int8')
    print df.info()
    df['idx'] = df.index.astype('int32')
    df.to_csv('./datasets/train/' + mode + '_ad_user_position_appCates_act.csv',index=False, chunksize=100000)

if __name__ == "__main__":
    fire.Fire(main)
