import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC

from HelperClasses.UI.Base import Base


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
        options.app_package = 'com.google.android.youtube'
        options.app_activity = 'com.google.android.youtube.app.honeycomb.Shell$HomeActivity'
        options.device_name = 'Pixel 8 Pro API 35'
        options.automation_name = 'UiAutomator2'
        options.platformVersion = '15'
        options.auto_grant_permissions = True
        driver = webdriver.Remote("http://127.0.0.1:4723", options=options)
        # request.cls.driver = driver
        yield driver
        driver.quit()
    @pytest.mark.mobile
    def test_example(self,extra,appium_driver,env):
        driver=appium_driver
        base = Base(driver, extra)
        # Click on search icon
        base.check_presence_of_AndroidElement('search_icon',env)
        base.attach_snap("Application Home Page", UnivWaitFor=10)
        # search_icon.click()
        base.androidClick('search_icon',env)

        # Send keys to search bar
        search_bar = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((AppiumBy.ID, "com.google.android.youtube:id/search_edit_text")))
        search_bar.send_keys("Rick Rolled (Short Version)")

        # Click on search suggestion
        new_xpath = '//android.widget.TextView[@text="rick rolled (short version)"]'
        search_suggestion = WebDriverWait(driver, 5).until(EC.presence_of_element_located((AppiumBy.XPATH, new_xpath)))
        search_suggestion.click()

        # Click on search result
        title_xpath = '//android.view.ViewGroup[contains(@content-desc, "Rick Rolled (Short Version)")]'
        search_result = WebDriverWait(driver, 10).until(EC.presence_of_element_located((AppiumBy.XPATH, title_xpath)))
        search_result.click()

