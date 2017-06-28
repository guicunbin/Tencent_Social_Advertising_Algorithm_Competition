import os
import fire
import pandas 


def get_csv_header(csv1):
    with open(csv1,'r') as fr:
        cols1 = [c.strip() for c in fr.readline().split(',')]
        print cols1
    return cols1


def join(csv1,csv2,csvout,on1,on2=None):
    print 'please ensure csv1 and csv2 all have header'
    cols1 = get_csv_header(csv1)
    cols2 = get_csv_header(csv2)
    k11 = cols1.index(on1) + 1
    k21 = cols2.index(on1) + 1
    if on2:
        k12     = cols1.index(on2) + 1
        k22     = cols2.index(on2) + 1
        idx1    = [str(1)+'.'+str(i) for i in range(2, len(cols1)+2)]
        idx2    = [str(2)+'.'+str(i) for i in range(2, len(cols2)+2) if i != k21+1 and i !=k22+1]
        fields  = reduce(lambda x,y: x+','+y,  idx1+idx2)
        print fields
        command = 'bash join_two_key.sh '+csv1+' '+str(k11)+' '+str(k12)+' '+csv2+' '+str(k21)+' '+str(k22)+' '+csvout+' '+fields
    else:
        command = 'bash join_one_key.sh '+csv1+' '+str(k11)+' '+csv2+' '+str(k21)+' '+csvout
    print command
    os.system(command)

fire.Fire(join)
    
