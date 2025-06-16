#!/bin/bash

cd 2; python ../../ebd.py 0 1 0 1;
cd ..

cd 4; python ../../ebd.py 0 2 0 2;
cd ..

cd 5; python ../../ebd.py 0 1 1 2;
cd ..

cd 6; python ../../ebd.py 0 1 0 3;
cd ..

cd 8; python ../../ebd.py 0 2 0 4;
cd ..
