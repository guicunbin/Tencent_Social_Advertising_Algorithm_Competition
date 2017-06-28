import os
import fire
import pandas 


def get_csv_header(csv1):
    with open(csv1,'r') as fr:
        cols1 = [c.strip() for c in fr.readline().split(',')]
        print cols1
    return cols1


def sort(csv1,csvout,on1,on2=None):
    print 'please check csv1 and csv2 all have header'
    cols1 = get_csv_header(csv1)
    k1 = cols1.index(on1) + 1
    if on2:
        k2          = cols1.index(on2) + 1
        command     ='sort -t , -n -k '+str(k1)+','+str(k1)+' '+str(k2)+','+str(k2)+' '+csv1 +' -o '+csvout
    else:
        command     ='sort -t , -n -k '+str(k1)+','+str(k1)+' '+csv1 +' -o '+csvout
    print command
    os.system(command)

fire.Fire(sort)
    
