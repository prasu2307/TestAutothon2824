"""
This class is to perform sample operation
"""
import time

import allure
from allure_commons.types import AttachmentType

from HelperClasses.UI.Base import Base
from selenium.webdriver.common.by import By
from utilities.customLogger import LogGen
from utilities.readProperties import ReadConfig


class Sample(Base):
    """Constructor of the Sample class"""
    def __init__(self, driver, extra):
        # initializing the driver from base class
        super().__init__(driver, extra)
        self.driver = driver
        self.extra = extra
        # Instantiate the Base class
        self.base = Base(self.driver, self.extra)
        # instantiate the logger class
        self.logger = LogGen.loggen()

    """Page Actions for Sample"""

    def launch_application(self, title, url, env):
        """
        Application launch
        """
        try:
            self.driver.get(url)
            time.sleep(5)
            with allure.step(f"Application URL is : {url}"):
                pass
        except Exception:
            pass
        # check whether the page is opened or not
        try:
            self.assertPageTitle(title, UnivWaitFor=10)
            with allure.step("Page Loaded Successfully."):
                self.attach_snap("Application Home Page", UnivWaitFor=10)
        except Exception as e:
            self.logger.exception(f"Page is not loaded. Please check the application availability and try again.\n{e}")
            raise Exception("Page is not loaded")

    def sample_operation(self, value_to_search, env):
        """
        Data Search
        """
        # Search data
        try:
            # enter username
            with allure.step("Enter Value to Search in Search Box"):
                self.input_text("search_box", value_to_search, env, UnivWaitFor=10)

                self.attach_snap("Search Box", UnivWaitFor=10)

            # submit password
            self.click("submit_search", env, UnivWaitFor=3)
            time.sleep(5)
            with allure.step("Data searched"):
                self.attach_snap("Results of data search", UnivWaitFor=10)
        except Exception as e:
            self.logger.exception(
                f"Error in Data search. Please check the application availability and try again.\n{e}")
            raise Exception("Search Page is not loaded")
