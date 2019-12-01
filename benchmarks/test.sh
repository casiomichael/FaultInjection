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

		until [ $counter == 1000 ]; do
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

	echo "Ran $counter tests and all done"
	echo "Successes = $success"
	echo "Segfaults = $segfault"
	echo "Cache Access Spans Block = $cache_spans_block"
	echo "Invalid Syscalls = $inv_syscall"
	echo "Misc. Errors = $misc_error"
	echo "${list_faults[@]}"

	for ints in "${list_faults[@]}"
	do
		rm *"`printf %04d $ints`.txt"
	done
}

if [ $1 == "run_test" ]; then
	run_test $2 $3 $4
fi