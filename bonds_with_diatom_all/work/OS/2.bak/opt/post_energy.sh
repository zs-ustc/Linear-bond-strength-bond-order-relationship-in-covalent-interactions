#!/bin/bash

[[ -f energy.dat ]] && rm energy.dat
[[ -f strain.dat ]] && rm strain.dat

folder="input"
if [ ! -d "$folder" ]; then
  echo "文件夹 $folder 不存在！"
  exit 1
fi

if [ ! -d "00000" ]; then
	cp 10000.gjf input/00000.gjf
	mkdir 00000
	cd 00000 && ln -s ../input/00000.gjf && cp ../../opt.log . && touch finished && cd ..
fi
cd 00000 && head -n 10 *.gjf | tail -n 1 | awk '{print $2}' >> ../strain.dat && cd ..

# 遍历文件夹中的文件
for file in "$folder"/*.gjf; do
  [ -e "$file" ] || continue # 跳过不存在的情况（避免没有匹配的文件时报错）
  filename=$(basename "$file")           # 获取文件名（去掉路径）
  #value=${filename#POSCAR_}      # 删除前缀部分
  value=${filename%.gjf}                   # 删除后缀部分
  # 输出结果
  echo "$value"
  filename="$value"
  echo $filename

  if [ -f ${filename}/finished ];then
  cd ${filename}
  [[ -f energy.dat ]] && rm energy.dat
  grep "SCF Done" *.log | tail -n 1
  
  grep " -1 " *.gjf | head -n 1 | tail -n 1 | awk '{print $3}' >> ../strain.dat
  grep "SCF Done" *.log | tail -n 1|awk '{print $5}' >> ../energy.dat
  
  cd ..
  fi

done
