import pandas as pd
import os
old_csv     = './datasets/train/user_installedapps.csv'
new_csv     = './datasets/train/tb_user_installedapps_add_one_column.csv'
os.system('rm -rf '+new_csv)
dfs         = pd.read_csv(old_csv, chunksize=500000)
need_header = True
for df in dfs:
    df['is_installed_this_app_long'] = 1
    df.to_csv(new_csv, index = False, mode = 'a', header = need_header)
    if need_header:
        need_header = False





old_csv     = './datasets/train/user_app_actions.csv'
new_csv     = './datasets/train/tb_user_app_actions_add_one_column.csv'
os.system('rm -rf '+new_csv)
dfs         = pd.read_csv(old_csv, chunksize=500000)
need_header = True
for df in dfs:
    df['install_day'] = (df['installTime'] / 1000000).astype('int8')
    df.to_csv(new_csv, index = False, mode = 'a', header = need_header)
    if need_header:
        need_header = False
