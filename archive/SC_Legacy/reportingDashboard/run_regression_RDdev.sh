#!/bin/bash
cd PycharmProjects\SupplyChain_Automated\SC_Legacy
virtualenv virtualenv_SC
virtualenv_SC\Scripts\activate
pytest -v -s --junit-xml=pytest_report.xml -m "regression" --env=dev --browser=chrome --headless=true ./testsuites/test_login.py

