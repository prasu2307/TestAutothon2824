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

    def select_edition(self, country_val, env):
        """
        Select Edition Country
        """
        try:
            self.click("edition_dropdown", env)
            # Read all the client labels listed for the user
            edition_labels = self.get_texts("dropdown_eles", env)
            with allure.step("Page Loaded Successfully."):
                if country_val in edition_labels:
                    self.click("dropdown_select", env, xpath_val=country_val, UnivWaitFor=10)
                    self.attach_snap("Edition Selected", UnivWaitFor=10)
        except Exception as e:
            self.logger.exception(f"Error occurred while selecting the Country. Please check the application.\n{e}")
            raise Exception("Error occurred while selecting the Country. Please check the application.")

    def launch_newslink(self, env):
        """
        Launch the News
        """
        try:
            # Get all window handles
            self.click("launch_business", env)
            time.sleep(3)
            window_handles = self.driver.window_handles

            # Switch to the new window
            self.driver.switch_to.window(window_handles[1])

            print(f"Business page title:\n{self.driver.title}")
        except Exception as e:
            self.logger.exception(f"Error occurred launching business\n{e}")
            raise Exception("Error occurred launching business")

    def access_new_info(self, env):
        """
        Data Search
        """
        try:
            news_items = {}
            date_list = []
            news_heading_list = []
            news_url_list = []
            for i in range(1, 4):
                self.scroll("carousel_ele", env, xpath_val=[i, i])
                # Get all window handles
                self.js_click("carousel_ele", env, xpath_val=[i, i])
                time.sleep(3)
                self.scroll(f"news_link_{i}", env)
                self.attach_snap(f"News Snapshot {i}", UnivWaitFor=10)
                self.click(f"news_link_{i}", env)

                date_txt = self.get_text('date_ele', env)
                news_heading = self.get_text('news_heading', env)
                news_url = self.driver.current_url

                self.scroll('news_heading', env)
                self.attach_snap(f"News Page Snapshot {i}", UnivWaitFor=10)

                news_url_list.append(news_url)
                news_heading_list.append(news_heading)
                date_list.append(date_txt)

                self.driver.back()
                time.sleep(2)

            news_items['link'] = news_url_list
            news_items['date_time'] = date_list
            news_items['headline'] = news_heading_list

            # Convert to list of dictionaries
            list_of_dicts = []
            for i in range(len(news_items['link'])):
                list_of_dicts.append({
                    'link': news_items['link'][i],
                    'date_time': news_items['date_time'][i],
                    'headline': news_items['headline'][i]
                })

            print(f"List of Dictionaries:\n{list_of_dicts}")

            # Open a file in write mode
            with open('Outputs/ActualOutputs/news_information_ui_result.txt', 'w', encoding='utf-8') as file:
                file.write(str(list_of_dicts))

            print("Data has been written to news_information_ui_result.txt")

        except Exception as e:
            self.logger.exception(f"Error occurred launching business\n{e}")
            raise Exception("Error occurred launching business")
