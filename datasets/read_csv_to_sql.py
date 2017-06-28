import sys
from sqlalchemy import create_engine
import pandas as pd
import MySQLdb
import time
c_size = 15000
start=time.time()
if len(sys.argv)!=3:
    print ('usage: python '+str(sys.argv[0])+' csv_file database_name ')
    sys.exit()
csv_file=sys.argv[1]
database_name=sys.argv[2]
table_name='tb_'+sys.argv[1].split('/')[-1].split('.')[0]
print database_name
print table_name

#####
engine=create_engine('mysql://root:0@localhost/'+database_name+'?charset=utf8')
conn = MySQLdb.connect(host = "localhost", user = "root", passwd = "0", db = database_name)
cur = conn.cursor()
cur.execute('drop table '+"if exists "+table_name)
#####
def dfs_to_sql(dfs):
    is_first  = True
    need_crop = False
    i = 0
    for df in dfs:
        df['idx_'+table_name] = df.index + i*c_size
        if is_first:
            need_cols = [c for c in df.columns if '.' not in c and '-' not in c]
            if len(need_cols)<len(df.columns):
                need_crop = True
        if need_crop:
            df = df[need_cols]
        df.to_sql(table_name,   engine, index=False, if_exists ='append')
        i +=1
        if is_first:
            print df[:10]
            is_first = False



####
with open(sys.argv[1],'r') as fr:
    line_0_0=fr.readline().split(',')[0]   ##read the first line first str
try:
    line_0_0_int=int(line_0_0)
    # if line_0_0 is str then raise Exception
    has_columns=False
except:
    has_columns=True
if not has_columns:
    print ("please input the "+str(df.shape[1])+' columns name')
    columns=raw_input("please split with ',': \n").split(',')
    print "columns: ",columns
    try:
        dfs = pd.read_csv(csv_file, names=columns, encoding="utf8", dtype='int32', chunksize=c_size)
        dfs_to_sql(dfs)
    except:
        dfs = pd.read_csv(csv_file, names=columns, encoding="utf8", chunksize=c_size)
        dfs_to_sql(dfs)
else:
    print ("this csv_file has columns")
    try:
        dfs = pd.read_csv(csv_file, encoding="utf8", dtype='int32',chunksize=c_size)
        dfs_to_sql(dfs)
    except:
        dfs = pd.read_csv(csv_file, encoding="utf8", chunksize=c_size)
        dfs_to_sql(dfs)
##### get the run time
print(table_name+"has write into sql ")
end=time.time()
print ("run_time: "+str(end-start)+' s')
print ('****************************************************')



