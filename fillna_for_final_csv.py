import pandas as pd
from tqdm import tqdm
import os

def main(mode='train'):
    data_file       = './datasets/train/'+ mode +'_ad_user_position_appCates_act_Install.csv'
    final_data_file = './datasets/train/final_'+ mode +'_ad_user_position_appCates_act_Install.csv'
    os.system('rm '+final_data_file)
    dfs = pd.read_csv(data_file, chunksize=500000)
    is_first = True
    for df in tqdm(dfs):
        if 'conversionTime' in df.columns:
            df['conversionTime']            = df['conversionTime'].fillna(0).astype('int32')
        df['is_installed_this_app_long']= df['is_installed_this_app_long'].fillna(0).astype('int32')
        df = df.astype('int32')
        df.to_csv(final_data_file, mode = 'a', index=False, header = is_first)
        if is_first:
            print df.info()
            print df[:10]
            is_first = False

main('train')
main('test')
