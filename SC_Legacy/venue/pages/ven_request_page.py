from pages.base_func import BaseFunc
from selenium.webdriver.common.by import By


class VenRequestPage(BaseFunc):

    login_button = (By.XPATH, "//a[@class='ping-button normal allow']")
    username = (By.ID, "username")
    password = (By.ID, "password")
    forgot_password_link = (By.XPATH, "//a[contains(text(),'Forgot Password?')]")
    bad_credentials = (By.XPATH, "//div[@class='ping-error']")

