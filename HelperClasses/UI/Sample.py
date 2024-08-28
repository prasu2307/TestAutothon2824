"""
This class is to perform UI operations
"""
import time
import os
import allure

from selenium.common import NoSuchElementException

from HelperClasses.API.ValidateAPI import validate_api
from HelperClasses.UI.Base import Base
from utilities.customLogger import LogGen
from utilities.readProperties import ReadConfig

output_user_logpath = os.getcwd() + '\\Outputs'


class Sample(Base):
    newsname = ReadConfig.get_news_name()
    no_of_sliders = ReadConfig.get_no_of_carousel()
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

    def remove_allure_reports(self):
        """
        Removes the old reports before the start of test execution
        """
        try:
            # Removing the allure-report json files before the test runs
            if os.path.exists(output_user_logpath + '\\Allure_reports\\'):
                for root, dirs, files in os.walk(output_user_logpath + '\\Allure_reports\\'):
                    list_of_files = os.listdir(output_user_logpath + '\\Allure_reports\\')
                    for file in list_of_files:
                        if file.endswith(".json") or file.endswith(".png") or file.endswith(".attach") or file.endswith(
                                ".txt"):
                            os.remove(os.path.join(root, file))
                    break
        except Exception as e:
            self.logger.exception(f"Error while removing the files in Allure_reports folder.\n{e}")
            allure.attach(f"Error while removing the files in Allure_reports folder.\n{e}", "Exception")

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
            with allure.step("Application Homepage Loaded Successfully."):
                self.attach_snap("Application Home Page", UnivWaitFor=10)
        except Exception as e:
            self.logger.exception(f"Page is not loaded. Please check the application availability and try again.\n{e}")
            allure.attach(f"Page is not loaded. Please check the application availability and try again.\n{e}",
                          "Exception")
            raise Exception("Page is not loaded")

    def select_edition(self, country_val, env):
        """
        Select Edition Country
        """
        try:
            self.check_presence_of_element("edition_dropdown", env)
            self.click("edition_dropdown", env)
            # Read all the client labels listed for the user
            edition_labels = self.get_texts("dropdown_eles", env)
            with allure.step("Page Loaded Successfully."):
                if str(country_val).upper() in edition_labels:
                    self.click("dropdown_select", env, xpath_val=country_val, UnivWaitFor=10)
                    self.attach_snap("Edition Selected", UnivWaitFor=10)
        except NoSuchElementException:
            self.refreshpage()
            self.check_presence_of_element("edition_dropdown", env)
            self.click("edition_dropdown", env)
            # Read all the client labels listed for the user
            edition_labels = self.get_texts("dropdown_eles", env)
            with allure.step("Page Loaded Successfully."):
                if str(country_val).upper() in edition_labels:
                    self.click("dropdown_select", env, xpath_val=country_val, UnivWaitFor=10)
                    self.attach_snap("Edition Selected", UnivWaitFor=10)
        except Exception as e:
            self.logger.exception(f"Error occurred while selecting the Country. Please check the application.\n{e}")
            allure.attach(f"Error occurred while selecting the Country. Please check the application.\n{e}", "Exception")
            raise Exception("Error occurred while selecting the Country. Please check the application.")

    def launch_newslink(self, env):
        """
        Launch the News
        """
        # newsname = ReadConfig.get_news_name()
        try:
            print(f"News name is inside launch {self.newsname}")
            if str(self.newsname).lower() == 'business':
                print(f"Inside if")
                self.check_presence_of_element("launch_business", env)
                # Get all window handles
                self.click("launch_business", env)
            elif str(self.newsname).lower() == 'politics':
                self.check_presence_of_element("launch_politics", env)
                # Get all window handles
                self.click("launch_politics", env)
            # Get all window handles
            window_handles = self.driver.window_handles

            # Switch to the new window
            self.driver.switch_to.window(window_handles[-1])

            print(f"News page title:\n{self.driver.title}")
        except NoSuchElementException:
            self.refreshpage()
            if str(self.newsname).lower() == 'business':
                print(f"Inside if")
                self.check_presence_of_element("launch_business", env)
                self.click("launch_business", env)
            elif str(self.newsname).lower() == 'politics':
                self.check_presence_of_element("launch_politics", env)
                self.click("launch_politics", env)
            # Get all window handles
            window_handles = self.driver.window_handles

            # Switch to the new window
            self.driver.switch_to.window(window_handles[-1])

            print(f"News page title:\n{self.driver.title}")
        except Exception as e:
            self.logger.exception(f"Error occurred launching business\n{e}")
            allure.attach(f"Error occurred launching {self.newsname}\n{e}", "Exception")
            raise Exception(f"Error occurred launching {self.newsname}")

    def access_new_info(self, env):
        """
        Data Search
        """
        # no_of_sliders = ReadConfig.get_no_of_carousel()
        print(f"no_of_sliders:{self.no_of_sliders}")
        try:
            news_items = {}
            date_list = []
            news_heading_list = []
            news_url_list = []
            with allure.step(f'Validating news information in UI'):
                for i in range(int(self.no_of_sliders)):
                    i += 1
                    self.scroll("carousel_ele", env, xpath_val=[i, i])
                    # Get all window handles
                    self.js_click("carousel_ele", env, xpath_val=[i, i])
                    time.sleep(3)
                    if str(self.newsname).lower() == 'business':
                        self.scroll(f"b_news_link_{i}", env)
                        self.attach_snap(f"News Snapshot {i}", UnivWaitFor=10)
                        self.click(f"b_news_link_{i}", env)
                    elif str(self.newsname).lower() == 'politics':
                        self.scroll(f"p_news_link_{i}", env)
                        self.attach_snap(f"News Snapshot {i}", UnivWaitFor=10)
                        self.click(f"p_news_link_{i}", env)

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

            with allure.step(f'Validating API using UI data'):
                # Validating the API requests using data retrieved from UI
                validate_api(list_of_dicts)

        except NoSuchElementException as nse:
            allure.attach(f"Element not found. Please check the locator.\n{nse}", f"Element not found error")
        except Exception as e:
            self.logger.exception(f"Error occurred launching business\n{e}")
            allure.attach(f"Error occurred launching {self.newsname}\n{e}", "Exception")
            raise Exception(f"Error occurred launching {self.newsname}")
