import os
import pytest
from selenium import webdriver
from configs import config
from pages import const


def pytest_addoption(parser):
    parser.addoption("--baseurl",
                     action="store",
                     default=const.STAGE_URL,
                     help="base url for nhra")

    parser.addoption("--browser",
                     action="store",
                     default="chrome",
                     help="name of the browser to test with")

    parser.addoption("--region",
                     action="store",
                     default="US",
                     help="country where the tests are run")

    parser.addoption("--env",
                     action="store",
                     default="stage",
                     help="environment to run tests in, qa or stage or prod")

    parser.addoption("--headless",
                     action="store",
                     default="false",
                     help="Is headless browser?")


@pytest.fixture(scope="class")
def setup(request):
    config.browser = request.config.getoption("--browser").lower()
    config.region = request.config.getoption("--region")
    config.env = request.config.getoption("--env")
    config.headless = request.config.getoption("--headless")

    # if config.region != "US":
    #     run Foxy proxy to setup region

    if config.env == "qa":
        config.baseurl = const.QA_URL
    elif config.env == "stage":
        config.baseurl = const.STAGE_URL
    elif config.env == "prod":
        config.baseurl = const.PROD_URL
    else:
        config.baseurl = request.config.getoption("--baseurl")

    print("\nbrowser = {}".format(config.browser))
    print("region = {}".format(config.region))
    print("env = {}".format(config.env))
    print("url = {}".format(config.baseurl))
    print("headless = {}".format(config.headless))

    if config.browser == 'firefox':
        geckodriver = os.path.join(os.getcwd(), 'drivers', 'geckodriver')
        driver = webdriver.Firefox(executable_path=geckodriver)
    elif config.browser == 'chrome':
        if config.headless == "true":
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--window-size=1420,1080')
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--disable-gpu')
            driver = webdriver.Chrome(options=chrome_options)
        else:
            driver = webdriver.Chrome(executable_path="C:/Users/jma/Documents/drivers/chromedriver.exe")
#    elif config.browser == 'safari':
#       driver = webdriver.Safari(executable_path=const.SAFARI_EXEC_PATH)

    driver.get(config.baseurl)
    request.cls.driver = driver
    driver.maximize_window()
    driver.implicitly_wait(30)

    yield driver

    def tear_down():
        print("Calling tear_down...")
        driver.quit()

    request.addfinalizer(tear_down)




