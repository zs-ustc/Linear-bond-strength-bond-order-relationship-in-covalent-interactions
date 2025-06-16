#!/bin/bash
[ -f Bond_length ] && rm Bond_length
for i in $(seq 1 6);do

if [ -f $i/finished ];then
	head $i/Bond_length 
	echo ""
	head $i/Bond_length >> Bond_length
	echo "" >> Bond_length
else
	echo "Error in job $i"
	exit
fi

done
