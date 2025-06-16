#!/bin/bash

rm energy.dat strain.dat
for i in $(seq -60 60);do
	((filename=$i+100))&&((filename=$filename*100))
	#filename=$(printf "%02d" $i)
	filename=$(printf "%05d" $filename)

#filename=$(printf "%02d" $i)
if [ -f ${filename}/finished ];then
  cd ${filename}
  [[ -f energy.dat ]] && rm energy.dat
  grep "SCF Done" *.log | tail -n 1
  
  
  echo $i >> ../strain.dat
  grep "SCF Done" *.log | tail -n 1|awk '{print $5}' >> ../energy.dat
  
  echo ${filename}
  cd ..
fi
done
