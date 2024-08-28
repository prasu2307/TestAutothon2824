"""
Conftest -> ConfigurationTest File
Configuration we can add here like fixtures we will add here and can be used these
fixtures in our other test cases
"""
import configparser
import os
import shutil
import subprocess

from appium.options.android import UiAutomator2Options
from py.xml import html
import pytest
import platform
import socket
import psutil
import datetime
import glob
from pathlib import Path
from tkinter import messagebox as msg
from utilities.customLogger import LogGen
from utilities.readProperties import ReadConfig
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import ChromeOptions
from selenium.webdriver import FirefoxOptions
from selenium.webdriver import EdgeOptions
from selenium import webdriver

output_user_logpath = os.getcwd() + '\\Outputs'
logger = LogGen.loggen()


def pytest_addoption(parser):
    config = configparser.ConfigParser()
    config.read(os.getcwd() + "\\Configurations\\config.ini")
    parser.addoption("--env", action="store")


# This fixture will read the environment value which we pass in command line
@pytest.fixture(scope="class")
def env(request):
    return request.config.getoption("--env")


# This fixture will read the marker name which we pass in command line
@pytest.fixture()
def caseid(request):
    return request.config.getoption("-m")


# This fixture is to initialize the driver and teardown the initialization
@pytest.fixture(params=["chrome"], scope='class') #, "firefox", "edge"
def init_driver(request):
    if request.param == "chrome":
        options = ChromeOptions()
        prefs = {'profile.default_content_setting_values.automatic_downloads': 1}
        prefs["profile.default_content_settings.popups"] = 0
        # getcwd should always return the root directory of the framework
        prefs["download.default_directory"] = f"{output_user_logpath}\\ActualOutputs"
        # options.add_argument("--headless")
        # # ***Enable below line when script is integrated with CICD pipeline or script is being executed in headless mode
        # options.add_argument("--window-size=1920,1080")
        options.add_argument("--start-maximized")
        options.add_argument('--disable-gpu')
        options.add_argument("--log-level=3")  # fatal
        options.add_experimental_option("prefs", prefs)
        options.add_experimental_option("detach", True)
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        # web_driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        web_driver = webdriver.Chrome(service=Service(), options=options)
        params = {'behavior': 'allow', 'downloadPath': f"{output_user_logpath}\\ActualOutputs"}
        web_driver.execute_cdp_cmd('Page.setDownloadBehavior', params)
    if request.param == "firefox":
        options = FirefoxOptions()
        profile = webdriver.FirefoxProfile()

        # Set preferences similar to Chrome
        profile.set_preference('browser.download.folderList', 2)
        profile.set_preference('browser.download.manager.showWhenStarting', False)
        profile.set_preference('browser.download.dir', f"{output_user_logpath}\\ActualOutputs")
        profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'application/pdf')  # Add MIME types as needed
        profile.set_preference('pdfjs.disabled', True)  # Disable built-in PDF viewer

        # Add options similar to Chrome
        # options.headless = True  # Set to True if running in headless mode
        # options.add_argument("--width=1920")
        # options.add_argument("--height=1080")
        options.add_argument("--start-maximized")
        options.add_argument('--disable-gpu')
        options.log.level = "fatal"  # Set log level

        # Attach the profile to options
        options.profile = profile

        # Initialize the Firefox driver with options and profile
        web_driver = webdriver.Firefox(service=Service(), options=options)
    if request.param == "edge":
        options = EdgeOptions()

        # Set preferences similar to Chrome
        prefs = {
            'profile.default_content_setting_values.automatic_downloads': 1,
            'profile.default_content_settings.popups': 0,
            'download.default_directory': f"{output_user_logpath}\\ActualOutputs"
        }
        options.add_experimental_option("prefs", prefs)

        # Add options similar to Chrome
        # options.add_argument("--headless")  # Enable headless mode if needed
        # options.add_argument("--window-size=1920,1080")
        options.add_argument("--start-maximized")
        options.add_argument('--disable-gpu')
        options.add_argument("--log-level=3")  # fatal
        options.add_experimental_option("detach", True)
        options.add_experimental_option('excludeSwitches', ['enable-logging'])

        web_driver = webdriver.Edge(service=Service(), options=options)

    request.cls.driver = web_driver
    # web_driver.maximize_window()
    web_driver.implicitly_wait(10)

    # Yield will act as Teardown method which automatically quit driver once the test is completed
    yield
    web_driver.quit()


# ############ pytest HTML Report ##############
@pytest.hookimpl(tryfirst=True)
def pytest_sessionstart(session):
    try:
        # if os.path.exists(output_user_logpath + '\\Logs\\'):
        #     # Clearing the logs before test runs
        #     open(output_user_logpath + "\\Logs\\testlog.log", "w").close()
        #
        # # Removing the screenshots and results reports before the test runs
        # if os.path.exists(output_user_logpath + '\\Reports\\'):
        #     for root, dirs, files in os.walk(output_user_logpath + '\\Reports\\'):
        #         for file in files:
        #             os.remove(os.path.join(root, file))
        #     for root, dirs, files in os.walk(output_user_logpath + '\\Reports\\screenshots\\'):
        #         for file in files:
        #             os.remove(os.path.join(root, file))

        # # Removing the downloaded report files before the test runs
        # if os.path.exists(output_user_logpath + '\\ActualOutputs\\'):
        #     for root, dirs, files in os.walk(output_user_logpath + '\\ActualOutputs\\'):
        #         for file in files:
        #             os.remove(os.path.join(root, file))

        # # Removing the allure-report json files before the test runs
        # if os.path.exists(output_user_logpath + '\\Allure_reports\\'):
        #     for root, dirs, files in os.walk(output_user_logpath + '\\Allure_reports\\'):
        #         list_of_files = os.listdir(output_user_logpath + '\\Allure_reports\\')
        #         for file in list_of_files:
        #             if file.endswith(".json") or file.endswith(".png") or file.endswith(".attach") or file.endswith(".txt"):
        #                 os.remove(os.path.join(root, file))
        #         break

        # Copy properties file to Allure_reports dir which can be added in html report
        # shutil.copyfile('environment.properties', output_user_logpath + f'\\Allure_reports')
        src_path = 'environment.properties'
        dest_path = output_user_logpath + f'\\Allure_reports'
        os.system(f'copy {src_path} {dest_path}')
    except FileNotFoundError as e:
        msg.showerror('Error!', str(e))
    except ValueError as v:
        msg.showerror('Error!', str(v))
    except PermissionError as p:
        msg.showerror('File is already opened. Try closing the file and try again', str(p))
