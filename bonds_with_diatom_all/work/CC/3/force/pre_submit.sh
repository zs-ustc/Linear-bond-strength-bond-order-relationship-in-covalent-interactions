#!/bin/bash
#PBS -l nodes=1:ppn=8  		# Requests 1 node and 8 processors per node
#PBS -l walltime=72:00:00 	# Sets max walltime for the job to 48 hours
#PBS -j oe			# Merge output and error files as standard output.
cd $PBS_O_WORKDIR		# to the directory that you are submitting the job

ulimit -s unlimited

for i in $(seq -40 60)
do

	((filename=$i+100))&&((filename=$filename*100))
	#filename=$(printf "%02d" $i)
	filename=$(printf "%05d" $filename)
    echo $filename
	if [ ! -f $filename/finished ];then
		mkdir $filename
		cd $filename
		ln -s ../input/${filename}.gjf
		cp ../g16.sub ${filename}_force.sub
		
		# 使用 if 语句判断是否为五的倍数
		#if (( i % 5 == 0 )); then
			g16<$filename.gjf | tee force.log
			formchk *.chk
			
			#--------------CHECK-----------------
			TailOut=$(tail -n 1 *.log | awk '{print $1}')
			[[ "$TailOut" = "Normal" ]] && touch finished || touch terminated
			#------------------------------------

			#continue  # 跳过五的倍数
		#fi
		cd ..
	fi
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
