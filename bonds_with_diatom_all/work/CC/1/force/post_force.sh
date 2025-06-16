#!/bin/bash
[[ -f force.dat ]] && rm force.dat
#for i in $(seq 0 15);do
#filename=$(printf "%02d" $i)

for i in $(seq -15 40);do
	((filename=$i+100))&&((filename=$filename*100))
	#filename=$(printf "%02d" $i)
	filename=$(printf "%05d" $filename)

cd ${filename}

file="force.log"

# 找到 "Forces (Hartrees/Bohr)" 所在的行号
line=$(grep -n "Forces (Hartrees/Bohr)" "$file" | cut -d: -f1)

# 读取 Forces 行后的第3行和第4行的第三列 (即 X 值)
F1=$(sed -n "$((line+3))p" "$file" | awk '{print $3}')
F2=$(sed -n "$((line+4))p" "$file" | awk '{print $3}')

# 输出 F1 和 F2
echo "${filename} F1: $F1 ;F2: $F2 "
echo "$F1 $F2">> ../force.dat


#echo $i >> ../strain.dat
#grep "SCF Done" *.log >> ../energy.dat


cd ..

done
