#!/bin/bash
#cd ~/workspace
virtualenv virtualenv_SC
cd ./SC_Legacy/reportingDashboard
pytest -v -s --junit-xml=pytest_report.xml -m "regression" --env=stage --browser=chrome --headless=true ./testsuites/

