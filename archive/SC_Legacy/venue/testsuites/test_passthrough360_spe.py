import pytest
import logging
import custom_logger as cl
import ven_login_page
import venue_home_page
import csv_util
from pages import const


#@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.usefixtures("setup")
class Test360PTspe:

    log = cl.custom_logger(logging.DEBUG)

    @pytest.mark.parametrize("rvalue", csv_util.get_csv_data(const.DATA_PATH))
    def test_spe_360_pt(self, rvalue):
        login_ven = ven_login_page.VenLoginPage(self.driver)
        venue_pg = login_ven.login(rvalue[0], rvalue[1])
        venue_pg.wait_for_seconds(1)
        assert venue_pg.is_displayed(venue_home_page.VenHomePage.avails2_app)
        venue_pg.open_request_app()
        venue_pg.wait_for_seconds(1)
        assert venue_pg.is_displayed(venue_pg.select_partner)
        # test on select partner
        # select partners
        venue_pg.execute_script("document.getElementById('request-partnersSelectForPopup').style.display = 'block'")
        select_element = venue_pg.select_partner.click
        select_element.select_by_visible_text("Sony Network Entertainment Inc")
        venue_pg.execute_script("document.getElementById('request-partnersSelectForPopup').style.display = 'none'")
        venue_pg.find_element_by_class_name("k-select").click()
        venue_pg.wait_for_seconds(1)
        venue_pg.find_element_by_css_selector("button.k-button.dbb-partnersButton").click()