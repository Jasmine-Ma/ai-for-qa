from selenium.webdriver.common.by import By
from pages.base_func import BaseFunc
from pages.rd_ingest_page import RDIngestPage


class RDRequestPage(BaseFunc):

    logout_button = (By.XPATH, "//a[@class='logout']")
    home_tab = (By.XPATH, "//a[contains(text(),'Home')]")
    request_tab = (By.XPATH, "//a[contains(text(),'Requests')]")
    ingest_tab = (By.XPATH, "//div[@id='navback']//a[contains(text(),'Ingests')]")
    setting_button = (By.XPATH, "// img[ @ id = 'imgSettings']")
    request_dashboard_link = (By.XPATH, "//a[contains(text(),'Request Dashboard')]")
    request_search_field = (By.XPATH, "//input[@id='txtRequestSearch']")
    request_search_button = (By.XPATH, "//input[@id='btnRequestSearch']")
    requestitem_search_field = (By.XPATH, "//input[@id='txtRequestItemSearch']")
    requestitem_search_button = (By.XPATH, "//input[@id='btnRequestItemSearch']")

    def goto_request_page(self):
        self.wait_for_seconds(3)
        self.click_and_wait(self.request_tab)

    def goto_ingest_page(self):
        self.wait_for_seconds(3)
        self.click_button(self.ingest_tab)

    def logout(self):
        self.wait_for_seconds(3)
        self.click_and_wait(self.logout_button)



