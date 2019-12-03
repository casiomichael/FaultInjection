#!/bin/bash
#This will be the script to automate running the hundreds of tests

#this is the function to run the program
run(){
	# ######### START OF RUU TESTS ##################
	# echo "OUTORDER 07100 RUU=32" >> log32-100.txt
	# ./test.sh run_test ruu100 32 FALSE 07100000000 &
	# echo "OUTORDER 07100 RUU=64" >> log64-100.txt
	# ./test.sh run_test ruu100 64 FALSE 07100000000 &

	# echo "OUTORDER 07333 RUU=16" >> log16-333.txt
	# ./test.sh run_test ruu333 16 FALSE 07033033033 &
	# echo "OUTORDER 07333 RUU=32" >> log32-333.txt
	# ./test.sh run_test ruu333 32 FALSE 07033033033 &
	# echo "OUTORDER 07333 RUU=64" >> log64-333.txt
	# ./test.sh run_test ruu333 64 FALSE 07033033033 &

	echo "OUTORDER 07525 RUU=16" >> log16-525.txt
	./test.sh run_test ruu525 16 FALSE 07050025025 &
	echo "OUTORDER 07525 RUU=32" >> log32-525.txt
	./test.sh run_test ruu525 32 FALSE 07050025025 &
	echo "OUTORDER 07525 RUU=64" >> log64-525.txt
	./test.sh run_test ruu525 64 FALSE 07050025025 &
}

if [ $1 == "run" ]; then
	run
fi