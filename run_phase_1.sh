echo 'if download is very slow ,  please go to  https://pan.baidu.com/s/1mi2vwXq'
echo '***********************************************************************'
wget -c -O pre.zip 'https://nbcache00.baidupcs.com/file/4cbd34ed6353bfdc7278b0d3b8a9aa15?bkt=p3-0000c333135708b6ca9f2cdc23effe4591ba&xcode=8026802456e5018b514f142bcc10e09261291142801df6b2ded0b7c77404c736&fid=2200549635-250528-373781708148591&time=1498643121&sign=FDTAXGERLBHS-DCb740ccc5511e5e8fedcff06b081203-nZ5xqg%2Bbj5g%2FEz3EDqXYpubXM3M%3D&to=h5&size=226487872&sta_dx=226487872&sta_cs=57&sta_ft=zip&sta_ct=0&sta_mt=0&fm2=MH,Yangquan,Netizen-anywhere,,beijing,ct&newver=1&newfm=1&secfm=1&flow_ver=3&pkey=0000c333135708b6ca9f2cdc23effe4591ba&sl=74186830&expires=8h&rt=sh&r=316892035&mlogid=4145481365429095928&vuk=2200549635&vbdid=2356142494&fin=pre.zip&fn=pre.zip&rtype=1&iv=0&dp-logid=4145481365429095928&dp-callid=0.1.1&hps=1&csl=179&csign=VbQRDDfl6OrtBnNUdGXIP9v0THs%3D&so=0&ut=6&uter=4&serv=0&by=themis'



unzip pre.zip 
mv ./pre/* ./datasets/train/




echo 'add_one_column ........'
python ./add_one_column.py


echo 'merge csv use very small memory ........'
python ./merge_use_small_dtype.py train   1
python ./merge_use_small_dtype.py test    1


sleep 10
echo "use Linux cmd join the last csv tb_user_installedapps_add_one_column ........."
cd ./datasets/ && \
./tecent_use_join.sh


sleep 10
echo "fillna for the final_csv ......"
cd ../ &&  \
python ./fillna_for_final_csv.py



sleep 10 
echo "split dataset and featset ........"
python ./split_data.py


echo "extract_feature for dataset and featset ......."
python ./extract_feature.py
python ./extract_other_feature.py



#sleep 10 
# single model train 
## 后期准备用　不同的模型，不同的特征，不同的训练数据,　不同的迭代次数，不同的树深度。。。。。然后做一个融合


echo "training model ......."
python model_single.py \
   --test_type '' \
   --mode test \
   --init_num 0:2 \
   --extra_num 1:300


