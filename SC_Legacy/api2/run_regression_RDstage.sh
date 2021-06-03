#!/bin/bash
#cd ~/workspace
source ./virtualenv_SC/Script/activate
cd ./SC_Legacy/api2
pytest -v -s --junit-xml=pytest_report.xml -m "parametrize" --env=stage --browser=chrome --headless=true ./testsuites/

