from selenium.webdriver.common.by import By
from configs import config
from pages.base_func import BaseFunc
from pages.rd_home_page import RDHomePage


class RDLoginPage(BaseFunc):

    login_button = (By.XPATH, "//a[@class='ping-button normal allow']")
    username = (By.ID, "username")
    password = (By.ID, "password")
    forgot_password_link = (By.XPATH, "//a[contains(text(),'Forgot Password?')]")
    bad_credentials = (By.XPATH, "//div[@class='ping-error']")

    def __init__(self, driver):
        self.driver = driver
        self.visit(config.baseurl)
        driver.maximize_window()

    def goto_rd(self):
        self.visit(config.baseurl)

    def login(self, user, password):
        self.send_keys(self.username, user)
        self.send_keys(self.password, password)
        self.click_and_wait(self.login_button)
        return RDHomePage(self.driver)

    def select_forgot_password(self):
        self.click_and_wait(self.forgot_password_link)



