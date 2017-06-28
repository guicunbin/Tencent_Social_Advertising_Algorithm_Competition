import tensorflow as tf
import numpy as np
import pandas as pd
import os
from model_single import *
logs_path     ='./log'
is_save_ckpt  =True
is_restore    =False
is_train      =True
ckpt_save_path='./ckpt'
train_csv_path='./datasets/dataset/dataset2_concat.csv'
valid_csv_path='./datasets/dataset/dataset4_concat.csv'
test_csv_path ='./datasets/dataset/dataset3_concat.csv'
need_feats    =[f.strip() for f in open(train_csv_path).readline().split(',') if f.strip()]
need_feats.remove('label')
print len(need_feats)
os.system('rm -r '+logs_path)
os.makedirs(logs_path+'/train')
os.makedirs(logs_path+'/valid')
n_epochs  = 20
split_time= 27



def logloss(act, pred):
    epsilon = 1e-15
    pred = tf.maximum(epsilon, pred)
    pred = tf.minimum(1-epsilon, pred)
    ll   = -1.0 * tf.reduce_mean(act*tf.log(pred) + tf.subtract(1.0,act)*tf.log(tf.subtract(1.0,pred)))
    return ll





class LR_Model:
    def __init__(self, num_classes=1, num_feats=101):
        self.num_classes = num_classes
        self.num_feats   = num_feats
        self._build_model()


    def _build_model(self):
        self.X                   =  tf.placeholder(tf.float32, [None, self.num_feats],       name = 'data')
        self.y                   =  tf.placeholder(tf.float32, [None, self.num_classes],     name = 'labels')
        self.lr                  =  tf.placeholder(tf.float32, [],                      name = 'lr')
        with tf.variable_scope('LR'):
            W           = tf.Variable(tf.random_normal([self.num_feats,self.num_classes], 0.0, 0.01),  name='w')
            b           = tf.Variable(tf.random_normal([self.num_classes],           0.0, 0.0),    name='b')
            self.pred   = tf.sigmoid(tf.nn.xw_plus_b(self.X,W,b))

        with tf.name_scope('loss'):
            self.pred_loss = logloss(self.y, self.pred)
            tf.summary.scalar('logloss',self.pred_loss)

        with tf.name_scope('accu'):
            self.accuracy  = tf.metrics.accuracy(self.y,self.pred)


model = LR_Model()
with tf.name_scope('train_op'):
    train_op = tf.train.MomentumOptimizer(model.lr, momentum=0.9, name='Momentum').minimize(model.pred_loss)
    
train_writer         =  tf.summary.FileWriter(logs_path+'/train', graph = tf.get_default_graph())
valid_writer         =  tf.summary.FileWriter(logs_path+'/valid')
merged_summary_op    =  tf.summary.merge_all()
if not os.path.exists(ckpt_save_path):
    os.makedirs(ckpt_save_path)

gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=0.2)
with tf.Session(graph = graph, config=tf.ConfigProto(gpu_options=gpu_options)) as sess:
    if is_restore:
        save = tf.train.Saver()
        save.restore(sess,ckpt_save_path)
    else:
        sess.run(tf.global_variables_initializer())

    if is_train:
        i=0
        for i_epoch in range(n_epochs):
            dfs  = pd.read_csv(train_csv_path,  dtype= 'float32', chunksize=5000)
            for df in dfs:
                print 'step ----- ',i
                i += 1
                X,y         = df[need_feats],df.label.reshape(-1,1)
                _,summary   = sess.run([train_op, merged_summary_op],feed_dict={model.X: X, model.y: y, model.lr: 0.001})
                train_writer.add_summary(summary,i)
            dfs = pd.read_csv(valid_csv_path,dtype='float32',chunksize=50000)
            eval_valid_li = [];     len_df = 0
            is_first = True
            for X in dfs:
                y=X.label.reshape(-1,1);   X=X[need_feats]
                if is_first:
                    is_first = False
                    summary    = sess.run(merged_summary_op, feed_dict={model.X: X, model.y: y})
                    valid_writer.add_summary(summary,i)
                eval_valid = sess.run(model.pred_loss, feed_dict={model.X: X, model.y: y})
                eval_valid_li.append(eval_valid * len(y))
                len_df += len(y)
                print eval_valid,len(y)
            eval_valid = sum(eval_valid_li) *1.0 / len_df
            print 'eval_valid -----',eval_valid
        
        if is_save_ckpt:
            saver = tf.train.Saver()
            saver.save(sess,ckpt_save_path)

    else:
        X           = pd.read_csv(test_csv_path,use_cols=need_feats+['instanceID'], dtype='float32')
        instanceID  = X.instanceID
        X           = X[need_feats]
        proba_test  = sess.run(model.pred,feed_dict={model.X: X})
        print "# submission"
        sub_dir_name  = './datasets/submit/lgb_train_split_'+str(split_time)+'_val_'+str(eval_valid)+'/'
        sub_file_name = sub_dir_name+'submission.csv'
        os.system('rm -r '+sub_dir_name)
        os.makedirs(sub_dir_name)
        ## sub to csv 
        df = pd.DataFrame({"instanceID": instanceID, "prob": proba_test})
        df.sort_values("instanceID", inplace=True)
        df.to_csv(sub_file_name, index=False, chunksize=10000)
        print 'save file to ',sub_file_name


        
