echo 'if download is very slow,  please go to  https://pan.baidu.com/s/1pLTZA7T '
echo '***********************************************************************'
wget -c -O final.zip 'https://nj02all01.baidupcs.com/file/8d39ff258bfb2c103197985e982cc1b3?bkt=p3-0000934f3b0a8506fb5e1f0b2440cb45e248&fid=2200549635-250528-750364636984313&time=1498640661&sign=FDTAXGERLBHS-DCb740ccc5511e5e8fedcff06b081203-HeqSOyKPqqSoii8t%2FqFsOzQwjG0%3D&to=69&size=2371948861&sta_dx=2371948861&sta_cs=9&sta_ft=zip&sta_ct=0&sta_mt=0&fm2=MH,Guangzhou,Netizen-anywhere,,beijing,ct&newver=1&newfm=1&secfm=1&flow_ver=3&pkey=0000934f3b0a8506fb5e1f0b2440cb45e248&sl=72286286&expires=8h&rt=sh&r=449974553&mlogid=4144820961110861813&vuk=2200549635&vbdid=2356142494&fin=final.zip&fn=final.zip&rtype=1&iv=0&dp-logid=4144820961110861813&dp-callid=0.1.1&hps=1&csl=144&csign=%2FuHJZyFePtrdpzldRd%2F%2FGHQOXmo%3D&so=0&ut=6&uter=4&serv=0&by=themis'

unzip final.zip 
mv ./final/* ./datasets/train/


echo 'add_one_column ........'
python ./add_one_column.py


echo 'merge csv use very small memory ........'
python ./merge_use_small_dtype.py train
python ./merge_use_small_dtype.py test


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
## 不同的模型，不同的特征，不同的迭代次数，不同的树深度。。。。。
# 然后做一个融合


echo "training model ......."
python model_single.py \
   --test_type '' \
   --mode test \
   --init_num 0:2 \
   --extra_num 1:300




