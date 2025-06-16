#!/bin/bash
cd 1; python ../../ebd.py 1 1 0 2;
cd ..
cd 2; python ../../ebd.py 0 2 0 2;
cd ..
cd 3; python ../../ebd.py 1 2 0 3;
cd ..
cd 4; python ../../ebd.py 0 3 0 3;
cd ..
cd 5; python ../../ebd.py 1 1 0 4;
cd ..
cd 6; python ../../ebd.py 0 4 0 4;
cd ..