from selenium.webdriver.common.by import By
from pages.base_func import BaseFunc
import connect_dbb


class RDIngestPage(BaseFunc):

    logout_button = (By.XPATH, "//a[@class='logout']")
    home_tab = (By.XPATH, "//a[contains(text(),'Home')]")
    request_tab = (By.XPATH, "//a[contains(text(),'Requests')]")
    ingest_tab = (By.XPATH, "//div[@id='navback']//a[contains(text(),'Ingests')]")
    setting_button = (By.XPATH, "// img[ @ id = 'imgSettings']")
    new_ingest_for_list = (By.XPATH, "//select[@id='ddlPartners']")
    SNEI = (By.XPATH, "//option[contains(text(),'Sony Network Entertainment Inc')]")
    file_loc_input = (By.XPATH, "//input[@id='txtLoc']")
    vendor_org_list = (By.XPATH, "//select[@id='ddlVendorOrganization']")
    bulk_ingest_button = (By.XPATH, "//input[@id='btnAdd']")
    script_ingest_button = (By.XPATH, "//input[@id='btnFinish']")
    scanned_ingest_button = (By.XPATH, "//input[@id='btnScan']")
    shir_task_link = (By.XPATH, "//a[@id='hlScanned']")
    detail_search_tab = (By.XPATH, "//span[contains(text(),'Details')]")
    summary_search_tab = (By.XPATH, "//span[contains(text(),'Summary')]")
    partner_select = (By.XPATH, "//select[@id='ddlSearchPartner']")
    status_select = (By.XPATH, "//select[@id='ddlStatus']")
    ingest_type_select = (By.XPATH, "//select[@id='ddlIngestType']")
    date_ingest_select = (By.XPATH, "//select[@id='ddlDateRange']")
    request_code_select = (By.XPATH, "//input[@id='txtRequestDisplayCode']")
    workflowid_select = (By.XPATH, "//input[@id='tbWorkflow']")
    external_alpha_key_select = (By.XPATH, "//input[@id='txtExternalAlphaKey']")
    filename_select = (By.XPATH, "//input[@id='txtFileName']")
    filter_button = (By.XPATH, "//input[@id='lbGoDetail']")
    clearfilter_button = (By.XPATH, "//input[@id='btnClear']")
    get_result_excel_link = (By.XPATH, "//a[@id='btnExcel']")
    expand_all_button = (By.XPATH, "//span[@id='expandall']")
    expand_records_button = (By.XPATH, "//img[@id='gvDetail_ctl02_btnExecutionSteps0']")

    def goto_request_page(self):
        self.wait_for_seconds(1)
        self.click_and_wait(self.request_tab)

    def goto_ingest_page(self):
        self.wait_for_seconds(1)
        self.click_button(self.ingest_tab)
        return RDIngestPage(self.driver)

    def logout(self):
        self.wait_for_seconds(1)
        self.click_and_wait(self.logout_button)

    def select_ingest_partner(self):
        self.wait_for_seconds(1)
        self.click_and_wait(self.new_ingest_for_list)
        self.driver.execute_script("document.getElementById('ddlPartners').style.display = 'block'")
        self. click_and_wait(self.SNEI)

    def ingest_file_loc(self):
        self.wait_for_seconds(1)
        self.send_keys(self.file_loc_input, "s3://supplychain-stgcontent/ingestprocess/Jasmine/Atest/1")

    def select_scanned(self):
        self.wait_for_seconds(1)
        self.click_button(self.scanned_ingest_button)

    def select_bulk(self):
        self.wait_for_seconds(1)
        self.click_button(self.bulk_ingest_button)

    def select_script(self):
        self.wait_for_seconds(1)
        self.click_button(self.script_ingest_button)

    def select_request(self):
        self.wait_for_seconds(1)
        self.click_button(self.expand_records_button)

    def db_request_check(self):
        new_con = connect_dbb.connect_stage_dbb()
        new_con.execute('SELECT top 10 * FROM SonyDBB.dbo.requestitem')
        for row in new_con:
            print(row)

        # select partners
        # driver.execute_script("document.getElementById('request-partnersSelectForPopup').style.display = 'block'")
        # select_element = Select(driver.find_element_by_id("request-partnersSelectForPopup"))
        # select_element.select_by_visible_text("Sony Network Entertainment Inc")
        # driver.execute_script("document.getElementById('request-partnersSelectForPopup').style.display = 'none'")
        # driver.find_element_by_class_name("k-select").click()
        # time.sleep(3)
        # driver.find_element_by_css_selector("button.k-button.dbb-partnersButton").click()

