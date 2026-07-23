import pytest
import logging
from pages import rd_login_page
import custom_logger as cl
import csv_util
from pages import const
from pages import rd_ingest_page


@pytest.mark.regression
@pytest.mark.usefixtures("setup")
class TestManualIngest:

    log = cl.custom_logger(logging.DEBUG)

    @pytest.mark.parametrize("rvalue", csv_util.get_csv_data(const.DATA_PATH))
    def test_manual_scan_ingest(self, rvalue):
        login_pg = rd_login_page.RDLoginPage(self.driver)
        rd_pg = login_pg.login(rvalue[0], rvalue[1])
        rd_pg.wait_for_seconds(1)
        assert rd_pg.is_displayed(rd_pg.ingest_tab)
        rd_pg.goto_ingest_page()
        rd_pg.wait_for_seconds(1)
        assert rd_pg.is_displayed(rd_pg.ingest_tab)
        # test on Scanned ingest
        ingest_pg = rd_ingest_page.RDIngestPage(self.driver)
        ingest_pg.select_ingest_partner()  # select partner (currently hard code to pick SNEI- it can be written to looks through csv file and select partners accordingly for doing ingest for multiple partners)
        ingest_pg.ingest_file_loc()  # (this can be written to look for csv file for multiple file)
        ingest_pg.select_scanned()
        assert ingest_pg.is_displayed(ingest_pg.scanned_ingest_button)
        ingest_pg.page_refresh()
        ingest_pg.wait_for_seconds(10)

