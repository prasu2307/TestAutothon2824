import allure
import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
from tkinter import messagebox as msg

from HelperClasses.API.ValidateAPI import validate_api
from HelperClasses.UI.Base import Base
from utilities.readProperties import ReadConfig


# capabilities = {
#     "platformName": "Android",
#     "automationName": "uiautomator2",
#     "deviceName": "Android Emulator",
#     "app": "/path/to/your/app.apk",
#     "udid": "emulator-5554"
# }

# @pytest.fixture(scope="module")
# def driver():
#     options = UiAutomator2Options()
#     options.platform_name = 'Android'
#     options.udid = 'emulator-5554'
#     options.app_package = 'com.google.android.youtube'
#     options.app_activity = 'com.google.android.youtube.app.honeycomb.Shell$HomeActivity'
#     options.device_name = 'Pixel 8 Pro API 35'
#     options.automation_name = 'UiAutomator2'
#     options.platformVersion = '15'
#     options.auto_grant_permissions = True
#     driver = webdriver.Remote("http://127.0.0.1:4723", options=options)
#     yield driver
#     driver.quit()

# @pytest.mark.usefixtures("appium_driver")
class Test_appium_mobile:
    @pytest.fixture()
    def appium_driver(self):
        options = UiAutomator2Options()
        options.platform_name = 'Android'
        options.udid = 'emulator-5554'
        # options.device_name = 'Pixel 8 Pro API 35'
        options.device_name = 'Medium Phone API 35'
        options.automation_name = 'UiAutomator2'
        options.platformVersion = '15'
        options.auto_grant_permissions = True
        options.app = r"C:\Users\makprasa\Downloads\app-stepin.apk"
        driver = webdriver.Remote("http://127.0.0.1:4723", options=options)
        # request.cls.driver = driver
        yield driver
        driver.quit()

    @pytest.mark.mobile
    @pytest.mark.flaky(reruns=1, reruns_delay=2)
    def test_example(self,extra,appium_driver,env):

        driver=appium_driver
        base = Base(driver, extra)
        with allure.step(f'Validating APK data'):
            # Click on search icon
            base.check_presence_of_AndroidElement('get_products_btn',env)
            base.attach_snap("Application Home Page", UnivWaitFor=10)
            # search_icon.click()
            base.androidClick('get_products_btn',env)
            base.check_presence_of_AndroidElement('product_name', env)
            base.attach_snap("Product Page", UnivWaitFor=10)

            strProductName = base.get_Androidtext('product_name',env)
            strProductDesc = base.get_Androidtext('product_desc',env)
            strProductPrice = base.get_Androidtext('product_price',env)
            strProductPrice = str(strProductPrice).replace('₹', '')
            strTeamName = ReadConfig.getEpsilonTeamName()

            # Creating a list with Product details
            product_keylist = ['strProductName','strProductDesc','strProductPrice','strTeamName']
            product_valuelist = [strProductName,strProductDesc,strProductPrice,strTeamName]
            print('product_keylist\n',product_keylist)
            print('product_valuelist\n',product_valuelist)

            # Dictionary to hold key and value pair from APK
            dict_product_details= dict(zip(product_keylist,product_valuelist))

            print('dict_product_details\n',dict_product_details)

            # Create a list of dict
            list_of_dict_product_details = [dict_product_details]

            print('list_of_dict_product_details\n',list_of_dict_product_details)

        with allure.step(f'Validating API using APPIUM data'):
            # Validating the API requests using data retrieved from APPIUM
            validate_api(list_of_dict_product_details)
