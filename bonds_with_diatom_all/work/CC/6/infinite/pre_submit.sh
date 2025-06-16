#!/bin/bash
#PBS -l nodes=1:ppn=8  		# Requests 1 node and 8 processors per node
#PBS -l walltime=72:00:00 	# Sets max walltime for the job to 48 hours
#PBS -j oe			# Merge output and error files as standard output.
cd $PBS_O_WORKDIR		# to the directory that you are submitting the job

ulimit -s unlimited

# 指定文件夹路径
folder="input"

# 检查文件夹是否存在
if [ ! -d "$folder" ]; then
  echo "文件夹 $folder 不存在！"
  exit 1
fi

# 遍历文件夹中的文件
for file in "$folder"/*.gjf; do
  # 跳过不存在的情况（避免没有匹配的文件时报错）
  [ -e "$file" ] || continue
  
  # 获取文件名
  filename=$(basename "$file")           # 获取文件名（去掉路径）
  
  # 提取 output_poscars_ 和 .vasp 之间的部分
  #value=${filename#POSCAR_}      # 删除前缀部分
  #value=${value%.vasp}                   # 删除后缀部分
  value=${filename%.gjf}                   # 删除后缀部分
  
  # 输出结果
  echo "$value"
  filename="$value"
  echo $filename
	if [ ! -f $filename/finished ];then
		mkdir $filename
		cd $filename
		ln -s ../input/${filename}.gjf
		cp ../g16.sub ${filename}_opt.sub
		
		# 使用 if 语句判断是否为五的倍数
		#if (( i % 5 == 0 )); then
			g16<$filename.gjf >opt.log
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

