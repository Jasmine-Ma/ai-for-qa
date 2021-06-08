import pytest
import logging
from pages import rd_login_page
import custom_logger as cl


@pytest.mark.regression
@pytest.mark.usefixtures("setup")
class TestLoginPage:

    log = cl.custom_logger(logging.DEBUG)

    def test_title(self):
        self.log.info("Running test_title...")
        assert "Sign On" in self.driver.title

    @pytest.mark.regression
    def test_valid_credentials(self):
        self.log.info("Running test_valid_credentials...")
        login_pg = rd_login_page.LoginPage(self.driver)
        home_pg = login_pg.login("", "")
        #assert "Reporting Dashboard" in self.driver.title
        home_pg.take_screenshot("Captured")
        home_pg.logout()

    @pytest.mark.regression
    def test_invalid_credentials(self):
        self.log.info("Running test_invalid_credentials...")
        login_pg = rd_login_page.LoginPage(self.driver)
        login_pg.login("something", @#")
        assert login_pg.is_displayed(login_pg.bad_credentials)

#    def test_user_not_found(self):
#       self.log.info("Running test_user_not_found...")
#       login_pg = login_page.LoginPage(self.driver)
#        login_pg.login("jasmine.ma@sonydadc.com", "something")
#        assert login_pg.is_displayed(login_pg.login_button)





