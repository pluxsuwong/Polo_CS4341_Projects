#!/bin/bash
function puz_1 {
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

}
function puz_2 {
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
}
function puz_3 {
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
}
if [ "$#" -ne 1 ]; then
    puz_1
    puz_2
    puz_3
fi
for var in "$@"
do
    if [ "$var" == 1 ]; then
        puz_1
    fi
    if [ "$var" == 2 ]; then
        puz_2
    fi
    if [ "$var" == 3 ]; then
        puz_3
    fi
done
