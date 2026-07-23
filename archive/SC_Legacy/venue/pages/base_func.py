import time
import logging
import custom_logger as cl
from traceback import print_stack
from configs import config
import selenium.webdriver.support.ui as ui
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
import selenium.webdriver.support.expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains


class BaseFunc(object):

    log = cl.custom_logger(logging.DEBUG)

    def __init__(self, driver):
        self.driver = driver

    def visit(self, url):
        self.log.info("Visit url: {}".format(url))
        self.driver.get(url)
        if url.startswith("http"):
            self.driver.get(url)
        else:
            self.driver.get(config.baseurl + url)

    def set_field_by_id(self, loc, value):
        self.log.info("Set field by id: loc = {}, value = {}".format(loc, value))
        elem = self.driver.find_element_by_id(*loc)
        elem.send_keys(value)

    def set_field_by_name(self, loc, value):
        self.log.info("Set field by name: loc = {}, value = {}".format(loc, value))
        elem = self.driver.find_element_by_name(*loc)
        elem.send_keys(value)

    def set_field_by_css(self, loc, value):
        self.log.info("Set field by css: loc = {}, value = {}".format(loc, value))
        elem = self.driver.find_element_by_css_selector(*loc)
        elem.send_keys(value)

    def set_field_by_xpath(self, loc, value):
        self.log.info("Set field by xpath: loc = {}, value = {}".format(loc, value))
        elem = self.driver.find_element_by_xpath(*loc)
        elem.send_keys(value)

    def click_link_text(self, loc):
        self.log.info("Click link by text: loc = {}".format(loc))
        elem = self.driver.find_element_by_link_text(*loc)
        elem.click()

    def click_partial_link_text(self, loc):
        self.log.info("Click link by partial text: loc = {}".format(loc))
        elem = self.driver.find_element_by_partial_link_text(*loc)
        elem.click()

    def click_button(self, loc):
        self.log.info("Click button: loc = {}".format(loc))
        btn = self.driver.find_element(*loc)
        btn.click()

    def click_elem_by_css(self, loc):
        self.log.info("Click element by css: loc = {}".format(loc))
        elem = self.driver.find_element_by_css_selector(*loc)
        elem.click()

    def select_menu_item_by_value(self, loc, value):
        self.log.info("Select menu item by value: loc = {}, value = {}".format(loc, value))
        elem = self.driver.find_element(*loc)
        elem.select_by_visible_text(value)

    def select_menu_item_by_index(self, loc, index):
        self.log.info("Select menu item by index: loc = {}, index = {}".format(loc, index))
        elem = self.driver.find_element(*loc)
        elem.select_by_index(index)

    def select_drop_down_by_text(self, loc, text):
        self.log.info("Select dropdown by text: loc = {}, text = {}".format(loc, text))
        elem = self.driver.find_element(*loc)
        try:
            Select(elem).select_by_visible_text(text)
        except NoSuchElementException:
            self.log.error("Error selecting dropdown {} by text {}".format(loc, text))
            print_stack()

    def select_drop_down_by_index(self, loc, index):
        self.log.info("Select dropdown by text: loc = {}, index = {}".format(loc, index))
        elem = self.driver.find_element(*loc)
        try:
            Select(elem).select_by_index(index)
        except NoSuchElementException:
            self.log.error("Error selecting dropdown {} by index {}".format(loc, index))
            print_stack()

    def click_and_wait(self, loc, timeout=20):
        self.log.info("click and wait: loc = {}".format(loc))
        elem = self.driver.find_element(*loc)
        try:
            elem.click()
            self.driver.implicitly_wait(timeout)
        except Exception as e:
            self.log.error("Exception caught: {}".format(str(e)))
            self.log.error("Unable to click the element {}".format(*loc))

    def hover_on_element(self, loc):
        self.log.info("Hovering on element: loc = {}".format(loc))
        elem_to_hover = self.driver.find_element(*loc)
        try:
            hover = ActionChains(self.driver).move_to_element(elem_to_hover)
            hover.perform()
            self.wait_for_seconds(6)
        except Exception as e:
            self.log.error("Exception caught: {}".format(str(e)))
            self.log.error("Unable to hover on the element {}".format(loc))

    def hover_and_click(self, loc):
        self.log.info("Hove and click the element: loc = {}".format(loc))
        try:
            clicker = ActionChains(self.driver).click(loc)
            clicker.perform()
        except Exception as e:
            self.log.error("Exception caught: {}".format(str(e)))
            self.log.error("Unable to hover and click on the element {}".format(loc))

    def send_keys(self, loc, value, clear_first=True, click_first=True, timeout=8):
        self.log.info("send keys: loc = {} with value = {}".format(loc, value))
        try:
            if click_first:
                self.driver.find_element(*loc).click()
            if clear_first:
                self.driver.find_element(*loc).clear()
            self.driver.find_element(*loc).send_keys(value)
            self.driver.implicitly_wait(timeout)
        except Exception as e:
            self.log.error("Exception caught: {}".format(str(e)))
            self.log.error("Unable to send keys on the element: {}".format(loc))

    def is_visible(self, loc, timeout=5):
        self.log.info("Checking if element is visible, element = {}".format(loc))
        try:
            ui.WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(loc))
        except TimeoutException:
            return False
        return True

    def is_not_visible(self, loc, timeout=5):
        self.log.info("Checking if element is not visible, element = {}".format(loc))
        try:
            ui.WebDriverWait(self.driver, timeout).until_not(EC.visibility_of_element_located(loc))
        except TimeoutException:
            return False
        return True

    def is_displayed(self, loc):
        self.log.info("Checking if element is displayed, loc = {}".format(loc))
        try:
            self.driver.find_element(*loc).is_displayed()
        except NoSuchElementException:
            return False
        return True

    def wait_for_seconds(self, seconds):
        time.sleep(seconds)

    def wait_for_element_displayed(self, loc, timeout=12):
        self.log.info("Wait for element to be displayed, element = {}".format(loc))
        try:
            ui.WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(loc))
        except TimeoutException:
            self.log.error("Time out exception.")
            self.log.error("Unable to locate element: {}".format(*loc))

    def wait_for_page_load(self):
        try:
            self.log.info("Waiting for page to load...")
            wait = WebDriverWait(self.driver, 10)
            wait.until(lambda driver: self.driver.execute_script("return jQuery.active == 0"))
        except NoSuchElementException:
            self.wait_for_seconds(8)
        except TimeoutException:
            pass
        except WebDriverException:
            seconds_to_wait = 5
            self.log.warning("Failed to execute wait on page. Waiting for seconds = {}".format(seconds_to_wait))
            self.wait_for_seconds(seconds_to_wait)

    def delete_text(self, loc):
        # when the text input field can't be cleared using clear()
        input_elm = self.driver.find_element(*loc)
        text_2_clear = input_elm.get_attribute('value')
        for i in range(len(text_2_clear)):
            input_elm.send_keys(Keys.BACKSPACE)

    def get_element_text(self, loc):
        elm = self.driver.find_element(*loc)
        return elm.text

    def get_element_text_by_tag_name(self, tag_name):
        elm = self.driver.find_element_by_tag_name(tag_name)
        return elm.text

    def enter_input_text(self, input_key, num_times=1):
        self.log.info("enter input text, input_key = {}".format(input_key))
        try:
            actions = ActionChains(self.driver)
            actions.send_keys(input_key * num_times)
            actions.perform()
        except Exception as e:
            self.log.error("Exception caught : {}".format(str(e)))
            self.log.error("Failed to enter input text.")

    def switch_to_frame(self, loc):
        self.log.info("Switch to frame, loc = {}".format(loc))
        try:
            element = self.driver.find_element(*loc)
            self.driver.switch_to.frame(element)
        except Exception as e:
            self.log.error("Exception caught : {}".format(str(e)))
            print_stack()

    def switch_to_default_content(self):
        self.log.info("Switch back to default content.")
        self.wait_for_seconds(1)
        try:
            self.driver.switch_to.default_content()
        except Exception as e:
            self.log.error("Exception caught : {}".format(str(e)))
            print_stack()

    def take_screenshot(self, result_message):
        """
        Takes screenshot of the current open web page
        """
        self.log.info("Take screenshot...")
        file_name = resultMessage + "." + str(round(time.time() * 1000)) + ".png"
        screenshot_directory = "../screenshots/"
        relative_file_name = screenshot_directory + file_name
        current_directory = os.path.dirname(__file__)
        destination_file = os.path.join(current_directory, relative_file_name)
        destination_directory = os.path.join(current_directory, screenshot_directory)

        try:
            if not os.path.exists(destination_directory):
                os.makedirs(destination_directory)
            self.driver.save_screenshot(destination_file)
            self.log.info("Screenshot save to directory: " + destination_file)
        except Exception as e:
            self.log.error("Exception caught when taking screenshot : {}".format(str(e)))
            print_stack()

    def page_scroll(self, direction="down"):
        self.log.info("Scroll down the page...")
        if direction == "up":
            # Scroll Up
            self.driver.execute_script("window.scrollBy(0, -1000);")

        if direction == "down":
            # Scroll Down
            self.driver.execute_script("window.scrollBy(0, 1000);")

    def page_refresh(self):
        self.log.info("Refresh page...")
        self.driver.refresh()
