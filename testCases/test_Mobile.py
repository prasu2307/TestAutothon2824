import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# capabilities = {
#     "platformName": "Android",
#     "automationName": "uiautomator2",
#     "deviceName": "Android Emulator",
#     "app": "/path/to/your/app.apk",
#     "udid": "emulator-5554"
# }

@pytest.fixture(scope="module")
def driver():
    options = UiAutomator2Options()
    options.platform_name = 'Android'
    options.udid = 'emulator-5554'
    options.app_package = 'com.google.android.youtube'
    options.app_activity = 'com.google.android.youtube.app.honeycomb.Shell$HomeActivity'
    options.device_name = 'Pixel 4 API 33'
    options.automation_name = 'UiAutomator2'
    options.platformVersion = '13'
    options.auto_grant_permissions = True
    driver = webdriver.Remote("http://127.0.0.1:4723", options=options)
    yield driver
    driver.quit()

@pytest.mark.mobile
def test_example(driver):
    # Click on search icon
    search_icon = WebDriverWait(driver, 10).until(EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "Search")))
    search_icon.click()

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

