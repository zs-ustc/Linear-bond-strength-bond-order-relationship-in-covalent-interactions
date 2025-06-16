#!/bin/bash

for i in $(seq 5 5);do

if [ -f $i/finished ];then
	cd $i/ && python ../../1_NBO.py && python ../../2_NBO.py && cd ..
else
	echo "Error in job $i"
	exit
fi

done
