import logging
import os
import json
import base64
from pathlib import Path

import allure
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

output_user_logpath = os.getcwd() + '\\Outputs'


class LogGen:
    @staticmethod
    def loggen():
        """
            Author: Sachin R
            Description: Function to create testlog file and enable logger
            Return: Returns the logger object.
            Date: 19th feb 2024
        """
        # Create log file if not exists
        # dirpath = os.getcwd() + '\\Logs'
        dirpath = output_user_logpath + '\\Logs'
        isExist = os.path.exists(dirpath)
        if isExist:
            # filepath = Path(os.getcwd() + "\\Logs\\testlog.log")
            filepath = Path(output_user_logpath + "\\Logs\\testlog.log")
            filepath.touch(exist_ok=True)
        elif not isExist:
            os.makedirs(dirpath)
            # filepath = Path(os.getcwd() + "\\Logs\\testlog.log")
            filepath = Path(output_user_logpath + "\\Logs\\testlog.log")
            filepath.touch(exist_ok=True)

        # Create screenshots folder to save the snapshots
        # screenshot_dirpath = os.getcwd() + '\\Reports\\screenshots'
        screenshot_dirpath = output_user_logpath + '\\Reports\\screenshots'
        isExist = os.path.exists(screenshot_dirpath)
        if not isExist:
            os.makedirs(screenshot_dirpath)

        # Create Archive Reports folder to archive the Excel reports
        archive_folder = output_user_logpath + '\\Archive_Reports'
        isExist = os.path.exists(archive_folder)
        if not isExist:
            os.makedirs(archive_folder)

        # Create Allure Reports folder to record the files realted to Allure report
        allure_folder = output_user_logpath + '\\Allure_reports'
        isExist = os.path.exists(allure_folder)
        if not isExist:
            os.makedirs(allure_folder)

        logging.basicConfig(
            filename=output_user_logpath + "\\Logs\\testlog.log",
            format='%(asctime)s: %(levelname)s: %(message)s',
            datefmt='%m/%d/%Y %I:%M:%S %p',
            force=True
        )
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        # logger.setLevel(logging.DEBUG)
        return logger

    @staticmethod
    def attach_logger(message, msg_name):
        """
            Author: Sachin R
            Description: Function to write logger message into Allure html report
            Date: 10th Apr 2024
        """
        allure.attach(message, name=msg_name)

    def send_devtools(self, driver, cmd, params={}):
        """
            Author: Sachin R
            Description: Function to convert html file to pdf file using webdriver
            Return: Returns the api response.
            Date: 19th feb 2024
        """
        resource = "/session/%s/chromium/send_command_and_get_result" % driver.session_id
        url = driver.command_executor._url + resource
        body = json.dumps({"cmd": cmd, "params": params})
        response = driver.command_executor._request("POST", url, body)

        if not response:
            raise Exception(response.get("value"))

        return response.get("value")

    # Convert HTML to PDF file
    def get_pdf_from_html(
            self, path, print_options={}, install_driver=True, exec_path=None
    ):
        """
            Author: Sachin R
            Description: Function to convert html file to pdf file
            Date: 19th feb 2024
        """
        webdriver_options = Options()
        webdriver_prefs = {}
        driver = None

        webdriver_options.add_argument("--headless")
        webdriver_options.add_argument("--disable-gpu")
        webdriver_options.add_argument("--no-sandbox")
        webdriver_options.add_argument("--disable-dev-shm-usage")
        webdriver_options.experimental_options["prefs"] = webdriver_prefs

        webdriver_prefs["profile.default_content_settings"] = {"images": 2}

        if install_driver:
            driver = webdriver.Chrome(
                # service=Service(ChromeDriverManager().install()), options=webdriver_options
                service=Service(), options=webdriver_options
            )
        else:
            driver = webdriver.Chrome(executable_path=exec_path, options=webdriver_options)

        driver.get(path)

        calculated_print_options = {
            "landscape": False,
            "displayHeaderFooter": False,
            "printBackground": True,
            "preferCSSPageSize": True,
        }
        calculated_print_options.update(print_options)
        result = self.send_devtools(
            driver, "Page.printToPDF", calculated_print_options)
        driver.quit()
        return base64.b64decode(result["data"])
