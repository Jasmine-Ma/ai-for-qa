import pytest
import logging
from pages import rd_login_page
import custom_logger as cl
import csv_util
from pages import const


@pytest.mark.regression
@pytest.mark.usefixtures("setup")
class TestRDHomepage:

    log = cl.custom_logger(logging.DEBUG)

    @pytest.mark.parametrize("rvalue", csv_util.get_csv_data(const.DATA_PATH))
    def test_rd_page(self, rvalue):
        login_pg = rd_login_page.RDLoginPage(self.driver)
        rd_pg = login_pg.login(rvalue[0], rvalue[1])
        rd_pg.wait_for_seconds(3)
        assert rd_pg.is_displayed(rd_pg.request_tab)
        rd_pg.goto_request_page()
        rd_pg.wait_for_seconds(3)
        assert rd_pg.is_displayed(rd_pg.ingest_tab)
        rd_pg.goto_ingest_page()
        rd_pg.wait_for_seconds(1)
        assert rd_pg.is_displayed(rd_pg.ingest_tab)
        print("test")