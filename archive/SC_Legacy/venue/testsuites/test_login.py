import pytest
import logging
import ven_login_page
import custom_logger as cl

@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.usefixtures("setup")
class TestLoginVenuePage:

    log = cl.custom_logger(logging.DEBUG)

    def test_title(self):
        self.log.info("Running test_title...")
        assert "Sign On" in self.driver.title

    def test_valid_credentials(self):
        self.log.info("Running test_valid_credentials...")
        login_pg = ven_login_page.VenLoginPage(self.driver)
        home_pg = login_pg.login("jasmine.ma@sonydadc.com", "HelloSony2020!@#")
        assert "Reporting Dashboard" in self.driver.title

    def test_invalid_credentials(self):
        self.log.info("Running test_invalid_credentials...")
        login_pg = ven_login_page.VenLoginPage(self.driver)
        login_pg.login("something", "HelloSony2020!@#")
        assert login_pg.is_displayed(login_pg.login_button)

    def test_user_not_found(self):
        self.log.info("Running test_user_not_found...")
        login_pg = ven_login_page.VenLoginPage(self.driver)
        login_pg.login("jasmine.ma@sonydadc.com", "something")
        assert login_pg.is_displayed(login_pg.login_button)



