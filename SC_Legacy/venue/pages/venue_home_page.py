from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from pages.base_func import BaseFunc
from configs import config


class VenHomePage(BaseFunc):

    user_name = (By.XPATH, "//span[@class='user-display-name']")
    logout_button = (By.XPATH, "//a[contains(text(),'LOGOUT')]")
    user_setting = (By.XPATH, "// a[contains(text(), 'USER SETTINGS')]")
    avails2_app = (By.XPATH, "//a[@id='option-405']//span[@class='icon']")
    catalog2_app = (By.XPATH, "//a[@id='option-54']//span[@class='icon']")
    metadata_app = (By.XPATH, "//a[@id='option-306']//span[@class='icon']")
    component_app = (By.XPATH, "//a[@id='option-53']//span[@class='icon']")
    transfers_app = (By.XPATH, "//a[@id='option-26']//span[@class='icon']")
    cloud_playout_app = (By.XPATH, "//a[@id='option-105']//span[@class='icon']")
    venue_commerce_app = (By.XPATH, "//a[@id='option-6001']//span[@class='icon']")
    storefront_app = (By.XPATH, "//a[@id='option-251']//span[@class='icon']")
    orders_app = (By.XPATH, "//a[@id='option-24']//span[@class='icon']")
    request_app = (By.XPATH, "//a[@id='option-403']//span[@class='icon']")
    core_media_app = (By.XPATH, "//a[@id='option-402']//span[@class='icon']")
    supporting_material_app = (By.XPATH, "//a[@id='option-308']//span[@class='icon']")
    external_tasks_app = (By.XPATH, "//a[@id='option-305']//span[@class='icon']")
    client_profile_app = (By.XPATH, "//a[@id='option-307']//span[@class='icon']")
    operation_app = (By.XPATH, "//a[@id='option-404']//span[@class='icon']")
    build_tool_app = (By.XPATH, "//a[@id='option-309']//span[@class='icon']")
    dash_board_menu = (By.XPATH, "//li[@class='app-menu-group dashboard open active app-open']//span[@class='icon']")
    admin_menu = (By.XPATH, "//li[@class='app-menu-group admin']//span[@class='icon']")
    avails2_menu = (By.XPATH, "//li[@class='app-menu-group avails2']")
    request_menu = (By.XPATH, "//li[@class='app-menu-group request show-next-line-menu app-open']")
    core_media_menu = (By.XPATH, "//li[@class='app-menu-group inventory show-next-line-menu app-open']")
    supporting_material_menu = (By.XPATH, "//li[@class='app-menu-group supporting-material show-next-line-menu']")
    external_tasks_menu = (By.XPATH, "//li[@class='app-menu-group external-tasks show-next-line-menu']")
    client_profile_menu = (By.XPATH, "//li[@class='app-menu-group client-profile show-next-line-menu']")
    operation_menu = (By.XPATH, "//li[@class='app-menu-group operations show-next-line-menu']")
    build_tool_menu = (By.XPATH, "//li[@class='app-menu-group build-tool show-next-line-menu']")
    report_bug_menu = (By.XPATH, "//li[@class='app-menu-group report-bug active']")
    select_partner = (By.XPATH, "//span[@id='request-partnerPopup_wnd_title']")

    def open_request_app(self):
        self.wait_for_seconds(3)
        self.click_and_wait(self.request_app)

    def open_user_setting(self):
        self.wait_for_seconds(3)
        self.click_and_wait(self.user_setting)

    def open_avail2_app(self):
        self.wait_for_seconds(3)
        self.click_button(self.avails2_app)

    def open_transfer_app(self):
        self.wait_for_seconds(3)
        self.click_button(self.transfers_app)

    def open_core_media_app(self):
        self.wait_for_seconds(3)
        self.click_and_wait(self. core_media_app)

    def open_supporting_material_app(self):
        self.wait_for_seconds(3)
        self.click_and_wait(self. supporting_material_app)

    def open_client_profile_app(self):
        self.wait_for_seconds(3)
        self.click_and_wait(self. client_profile_app)

    def open_operation_app(self):
        self.wait_for_seconds(3)
        self.click_and_wait(self.operation_app)