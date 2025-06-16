#!/bin/bash

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
  echo "value: $value"
  filename="$value"
  echo "${filename}"

done

