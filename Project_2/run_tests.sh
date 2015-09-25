#!/bin/bash

echo
echo "Running Tests for Puzzle 1"
python ga.py 1 file_input_1.txt 10
python ga.py 1 file_input_1.txt 10
python ga.py 1 file_input_1.txt 10
python ga.py 1 file_input_1.txt 10
python ga.py 1 file_input_1.txt 10
if [ ! -d P_1 ]; then
    mkdir P_1
fi
mv P_1_* P_1

echo
echo "Running Tests for Puzzle 2"
python ga.py 2 file_input_2.txt 10
python ga.py 2 file_input_2.txt 10
python ga.py 2 file_input_2.txt 10
python ga.py 2 file_input_2.txt 10
python ga.py 2 file_input_2.txt 10
if [ ! -d P_2 ]; then
    mkdir P_2
fi
mv P_2_* P_2

echo
echo "Running Tests for Puzzle 3"
python ga.py 3 file_input_3.txt 10
python ga.py 3 file_input_3.txt 10
python ga.py 3 file_input_3.txt 10
python ga.py 3 file_input_3.txt 10
python ga.py 3 file_input_3.txt 10
if [ ! -d P_3 ]; then
    mkdir P_3
fi
mv P_3_* P_3
