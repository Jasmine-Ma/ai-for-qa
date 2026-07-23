import logging
import pytest
import requests
import csv_util
import api_logger as al


class TestAPIStage:

    apilog = al.api_logger(logging.DEBUG)

    @pytest.mark.parametrize("rvalue", csv_util.get_csv_data("C:/Users/jma/PycharmProjects/SupplyChain_Automated/SC_Legacy/api2/data/stg_config_file.csv"))
    def test_get_status(self, rvalue):
        self.apilog.info("Running test_get_status...")
        api_list = []
        api_list.append(rvalue[1])
       # print(api_list)
        for rvalue in api_list:
            try:
                if requests.get(rvalue).status_code == 200:
                    print(rvalue + " " + "---->" + "200: Success!")
                elif requests.get(rvalue).status_code.status_code == 404:
                    print(rvalue + " " + "---->" + "404: NotFound!")
            except requests.exceptions.Timeout:
                errt = requests.exceptions.Timeout
                print(rvalue + " " + "---->Timeout Error:", errt)
        #   except requests.exceptions.ConnectionError:
        #       errc = requests.exceptions.ConnectionError
        #       print(rvalue + " " + "---->ConnectionError:", errc)
        #   except requests.exceptions.RequestException:
        #    err = requests.exceptions.RequestException
        #     print(rvalue + " " + "---->OOps: Something Else", err)