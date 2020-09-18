#!/bin/bash

env=$1
test=$2
browser=$3
silent=$4
testname=$5
report=$6

DIR1="virtualenv_SC"
DIR2="virtualenv"

HERE=`pwd`

RED='\033[0;31m'
GRN='\033[0;32m'
BLCK='\033[0;30m'
PUR='\033[0;35m'

############################################################

function run_test () {
	pytest -v -s -m "$test" --env=$env --browser=$browser --headless=$silent ./tests/$testname
}

function run_test_report () {
        if [[ $report = "xml" ]]
        then
		pytest --junit-xml=pytest_report.xml -m "$test" --env=$env  --browser=$browser --headless=$silent ./tests/$testname
	else
		pytest -s -v --html=./reports/smoke_test_report.html -m "$test" --env=$env  --browser=$browser --headless=$silent ./tests/$testname
	fi
}

function set_virtual_env () {
	cd ~/workspace

	if [ -d "$DIR1" ]
	then
		source ./$DIR1/bin/activate
	else
		source ./$DIR2/bin/activate
	fi

	cd $HERE
}

########################### MAIN ###########################

        clear

        if [[ $env = "" || $test = "" || $browser = "" || $silent = "" || $testname = "" ]]
        then
                echo -ne "Enter parameter in exact order. Example: ./run.sh (${GRN}environment${BLCK}) (${GRN}test type${BLCK}) "
		echo -e "(${GRN}browser type${BLCK}) (${GRN}silent mode${BLCK}) (${GRN}test name${BLCK}) (${GRN}optional: report type${BLCK})"
                echo -ne "Here are the choices for parameter. Example: ./run.sh (${RED}qa|uat|prod${BLCK}) (${GRN}smoke|regression${BLCK}) "
		echo -e "(${RED}chrome${BLCK}) (${GRN}true|false${BLCK}) (${RED}all|abc.py${BLCK}) (optional: ${PUR}xml|html${BLCK})"
        else
		set_virtual_env

		if [[ $testname = "all" || $testname = "abc.py" ]]
  		then
			testname=""
		fi

                if [[ $report = "" ]]
                then
                	run_test $env $test $browser $silent $testname
                else
                        run_test_report $env $test $browser $silent $testname $report
                fi

		deactivate
        fi

        echo -e "\n"

