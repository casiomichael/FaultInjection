#!/bin/bash
#This will be the script to run thousands of tests and to keep track of exit statuses

#run: runs a specific test 5000 times and logs the results of each run
run_test(){
	if [ -z "$1" ]; then
		echo "NEED AN INPUT TO KNOW WHICH TEST TO RUN"
	else
		counter=0
		success=0
		segfault=0
		cache_spans_block=0
		inv_syscall=0
		misc_error=0
		list_faults=()
		percent_flip=$(echo $4 | cut -c1-2)
		decode_flip=$(echo $4 | cut -c3-5)
		reg_flip=$(echo $4 | cut -c6-8)
		alu_flip=$(echo $4 | cut -c9-11)
		code=$(echo $1 | cut -c4-6)

		prefix="$percent_flip-`printf %03d $decode_flip``printf %03d $reg_flip``printf %03d $alu_flip`with_injection_"

		until [ $counter == 100 ]; do
			./sim-outorder-$1 -ruu:size $2 -issue:inorder $3 cc1.alpha -O 1stmt.i
			status=$?
			if [ $status == 0 ]; then
				((success++))
			elif [ $status == 139 ]; then
				((segfault++))
				list_faults+=($counter)
			elif [ $status == 1 ]; then
				((cache_spans_block++))
				list_faults+=($counter)
			elif [ $status == 6 ]; then
				((inv_syscall++))
				list_faults+=($counter)
			else
				((misc_error++))
				list_faults+=($counter)
			fi
			((counter++))
		done
	fi

	echo "Ran $counter tests and all done" >> log$2-$code.txt
	echo "Successes = $success" >> log$2-$code.txt
	echo "Segfaults = $segfault" >> log$2-$code.txt
	echo "Cache Access Spans Block = $cache_spans_block" >> log$2-$code.txt
	echo "Invalid Syscalls = $inv_syscall" >> log$2-$code.txt
	echo "Misc. Errors = $misc_error" >> log$2-$code.txt
	echo "${list_faults[@]}" >> log$2-$code.txt
	echo "-------------------------" >> log$2-$code.txt

	for ints in "${list_faults[@]}"
	do
		rm "$prefix`printf %04d $ints`-ruu$2.txt"
	done

	mv *$prefix????-ruu$2.txt tests/ECE\ 552\ tests/outorder/ruu_size_tests
}

if [ $1 == "run_test" ]; then
	run_test $2 $3 $4 $5
fi