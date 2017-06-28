import os
dir_1='./train/'
li_1=os.listdir(dir_1)
print li_1
for file1 in li_1:
    os.system("python read_csv_to_sql.py "+dir_1+file1+" tecent_2017_06")
