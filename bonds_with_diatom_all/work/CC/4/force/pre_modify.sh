#!/bin/bash

for i in $(seq -40 60)
do
	filename=$(printf "%02d" $i)_trans.gjf
    echo $filename
	sed -i "s/%nprocshared=32/%nprocshared=28/g" input/$filename
	sed -i "s/force/force int=superfine/g" input/$filename

done


#for i in {0..1}
#do
#	filename=$(printf "%02d" $i)
#    
#    # 使用 if 语句判断是否为五的倍数
#    if (( i % 5 == 0 )); then
#        continue  # 跳过五的倍数
#    fi
#	echo $filename
#	cd $filename
#	qsub *.sub
#	cd ..
#done


#for i in $(seq 0 40);do
#filename=$(printf "%02d" $i)
#mkdir -p ${filename}
#cd ${filename}
#ln -s ../stretched/${filename}.gjf
#cp ../g16.sub ${filename}.sub
#
#
#echo ${filename}
#cd ..
#
#done
