#!/bin/bash
cd ~/workspace
source ./virtualenv_SC/Script/activate
cd ./Supplychain_Legacy/reportingDashboard
pytest -v -s --junit-xml=pytest_report.xml -m "regression" --env=prod --browser=chrome --headless=true ./testsuites/

