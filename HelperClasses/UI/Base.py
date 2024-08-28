"""
This class is the parent of all pages
It contains all the generic methods and utilites for all the pages

Fluent wait:    will wait for a max of n sec until a specific element is located (type of explicit wait)
                Intelligent wait used with expected_conditions confined to one web element
                Can specify poll frequency and list of ignored exceptions
                Don't mix implicit and explicit/fluent waits, it can cause unpredictable wait times
"""
import functools
import time
from logging import exception

import allure
import pandas as pd
from allure_commons.types import AttachmentType
from selenium.common import NoSuchElementException, ElementNotVisibleException, ElementNotSelectableException, \
    ElementClickInterceptedException

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from appium.webdriver.common.appiumby import AppiumBy
from utilities.customLogger import LogGen
from utilities.readProperties import ReadConfig, config


# decorator to wait for action to be executed
def fWaitFor(input_func):
    @functools.wraps(input_func)
    def wrapper(*args, **kwargs):
        try:
            UnivWaitFor = kwargs['UnivWaitFor']
        except KeyError:
            UnivWaitFor = 0
        # simply return the decorated function if waitFor argument isn't explicitly provided
        if UnivWaitFor == 0:
            return input_func(*args, **kwargs)
        # else ignore any error till {UnivWaitFor} seconds. If the functions execute, return the function's output
        else:
            errorPresent = True
            timePassed = 0
            while errorPresent is True and timePassed < UnivWaitFor:
                try:
                    result = input_func(*args, **kwargs)
                    errorPresent = False
                    return result
                except Exception:
                    timePassed += 1
                    time.sleep(1)
            # if function fails even after {UnivWaitFor} seconds, return the error as is
            if errorPresent:
                return input_func(*args, **kwargs)

    return wrapper


class Base:

    def __init__(self, driver, extra):
        self.driver = driver
        self.extra = extra
        self.wait = WebDriverWait(driver, timeout=120, poll_frequency=2,
                                  ignored_exceptions=[ElementNotVisibleException, ElementNotSelectableException])
        # instantiate the logger class
        self.logger = LogGen.loggen()

    # Read object repository csv to get a list of lists
    @fWaitFor
    def read_data_from_csv(self, filename, UnivWaitFor=0):
        df = pd.read_csv(filename)
        return df

    # Identify locatorpath from locationname-object in csv
    @fWaitFor
    def locatorpath(self, locatorname, env, value=None, UnivWaitFor=0):
        df = self.read_data_from_csv(ReadConfig.getORFilePath(env))
        if value is None:
            locpath = df.loc[df['Object'] == locatorname]['Path'].to_list()[0]
        elif type(value) is list and len(value) == 2:
            locpath = df.loc[df['Object'] == locatorname]['Path'].to_list()[0] % (value[0], value[1])
        else:
            locpath = df.loc[df['Object'] == locatorname]['Path'].to_list()[0] % value
        return locpath

    # Identify locatortype from locationname-object in csv
    @fWaitFor
    def locatortype(self, locatorname, env, UnivWaitFor=0):
        df = self.read_data_from_csv(ReadConfig.getORFilePath(env))
        return df.loc[df['Object'] == locatorname]['Type'].to_list()[0]

    # Click a web element using locatorname
    @fWaitFor
    def click(self, locator, env, xpath_val=None, UnivWaitFor=0):
        """
        Given locator, identify the locator type and path from the OR file and click on the element
        """
        self.driver.find_element(getattr(By, self.locatortype(locator, env)), self.locatorpath(locator, env, xpath_val)).click()

    # Click a web element using Javascript executor
    @fWaitFor
    def js_click(self, locator, env, xpath_val=None, UnivWaitFor=0):
        """
        Given locator, identify the locator type and path from the OR file and click on the element using Javascript
        executor
        """
        self.driver.execute_script("arguments[0].scrollIntoView(true);",
                                   self.driver.find_element(getattr(By, self.locatortype(locator, env)),
                                                            self.locatorpath(locator, env, xpath_val)))
        self.driver.execute_script("arguments[0].click();",
                                   self.driver.find_element(getattr(By, self.locatortype(locator, env)),
                                                            self.locatorpath(locator, env, xpath_val)))

    # Navigate to particular page using locator
    @fWaitFor
    def go_to_page(self, locator, env, xpath_val=None, UnivWaitFor=0):
        """
        Navigate to the page with the given locator
        """
        with allure.step("Landing Page"):
            self.click(locator, env, xpath_val, UnivWaitFor=10)
            time.sleep(5)
            allure.attach(self.driver.get_screenshot_as_png(), name='PageInfo',
                          attachment_type=AttachmentType.PNG)

    # Input text to web element using locatorname and value
    @fWaitFor
    def input_text(self, locator, value, env, xpath_val=None, UnivWaitFor=0):
        """
        Given locator, identify the locator type and path from the OR file and input text to the element
        """
        self.driver.find_element(getattr(By, self.locatortype(locator, env)), self.locatorpath(locator, env, xpath_val)).clear()
        self.driver.find_element(getattr(By, self.locatortype(locator, env)), self.locatorpath(locator, env, xpath_val)). \
            send_keys(value)

    # Clear text from web element using locatorname and value
    @fWaitFor
    def clear(self, locator, env, xpath_val=None, UnivWaitFor=0):
        """
        Given locator, identify the locator type and path from the OR file and clear the text
        """
        self.driver.find_element(getattr(By, self.locatortype(locator, env)), self.locatorpath(locator, env, xpath_val)).clear()

    # Refresh the webpage
    @fWaitFor
    def refreshpage(self):
        """
        Given locator, identify the locator type and path from the OR file and clear the text
        """
        self.driver.refresh()

    # Assertion validation using pagetitle
    @fWaitFor
    def assertPageTitle(self, pageTitle, UnivWaitFor=0):
        """
        Assert the title of the page
        """
        self.logger.info(f"Expected Page Title is : '{pageTitle}' and Actual Page Title is : '{self.driver.title}'")
        assert str(self.driver.title).__contains__(pageTitle)

    # Function to select an element
    @fWaitFor
    def select_element(self, locator, env, xpath_val=None, UnivWaitFor=0):
        """
        Given locator, identify the locator type and path from the OR file and select the element
        """
        element = self.driver.find_element(getattr(By, self.locatortype(locator, env)), self.locatorpath(locator, env, xpath_val))
        return element

    # Function to select multiple elements
    @fWaitFor
    def select_elements(self, locator, env, xpath_val=None, UnivWaitFor=0):
        """
        Given locator, identify the locator type and path from the OR file and select the elements
        """
        elements = self.driver.find_elements(getattr(By, self.locatortype(locator, env)), self.locatorpath(locator,
                                                                                                           env, xpath_val))
        return elements

    # Read the element text using locatorname
    @fWaitFor
    def check_presence_of_element(self, locator, env, xpath_val=None, UnivWaitFor=0):
        """
        Given locator, identify the locator type and path from the OR file and check the presence of element
        """
        return self.wait.until(ec.presence_of_element_located((getattr(By, self.locatortype(locator, env)), self.locatorpath(locator, env, xpath_val))))

    # Read the element text using locatorname
    @fWaitFor
    def get_text(self, locator, env, xpath_val=None, UnivWaitFor=0):
        """
        Given locator, identify the locator type and path from the OR file and return the text
        """
        return self.driver.find_element(getattr(By, self.locatortype(locator, env)), self.locatorpath(locator, env, xpath_val)).text

    # Read the elements text using locatorname
    @fWaitFor
    def get_texts(self, locator, env, xpath_val=None, UnivWaitFor=0):
        """
        Given locator, identify the locator type and path from the OR file and return the texts
        """
        eles = self.select_elements(locator, env, xpath_val)
        res = [i.text for i in eles]
        return res

    # Read the element text using locatorname
    @fWaitFor
    def scroll(self, locator, env, xpath_val=None, UnivWaitFor=0):
        """
        Given locator, identify the locator type and path from the OR file and scroll to the element
        """
        self.driver.execute_script("arguments[0].scrollIntoView(true);",
                                   self.driver.find_element(getattr(By, self.locatortype(locator, env)),
                                                            self.locatorpath(locator, env, xpath_val)))

    # Check whether Checkbox/Radiobutton is selected or not
    @fWaitFor
    def isselected(self, locator, env, xpath_val=None, UnivWaitFor=0):
        """
        Given locator, identify the locator type and path from the OR file and check the selection of checkbox/radiobutton
        """
        return self.driver.find_element(getattr(By, self.locatortype(locator, env)), self.locatorpath(locator, env, xpath_val)).is_selected()

    # Check whether Particular button is enabled or not
    @fWaitFor
    def isenabled(self, locator, env, xpath_val=None, UnivWaitFor=0):
        """
        Given locator, identify the locator type and path from the OR file and check the butotn is enabled or not
        """
        return self.driver.find_element(getattr(By, self.locatortype(locator, env)), self.locatorpath(locator, env, xpath_val)).is_enabled()

    # Check whether Particular button is enabled or not
    @fWaitFor
    def wait_till_button_is_enabled(self, locator, env, xpath_val=None, UnivWaitFor=0):
        """
        Given locator, identify the locator type and path from the OR file and check the butotn is enabled or not
        """
        return self.wait.until(ec.element_to_be_clickable((getattr(By, self.locatortype(locator, env)), self.locatorpath(locator, env, xpath_val))))

    # Attach the snapshot into allure report
    @fWaitFor
    def attach_snap(self, snap_name, UnivWaitFor=0):
        allure.attach(self.driver.get_screenshot_as_png(), name=snap_name,
                      attachment_type=AttachmentType.PNG)

    # Attach the logger messages into allure report
    @fWaitFor
    def attach_logger(self, message, msg_name, UnivWaitFor=0):
        allure.attach(message, name=msg_name)

# Read the element text using locatorname
    @fWaitFor
    def check_presence_of_AndroidElement(self, locator, env, xpath_val=None, UnivWaitFor=0):
        """
        Given locator, identify the locator type and path from the OR file and check the presence of element
        """
        return self.wait.until(ec.presence_of_element_located((getattr(AppiumBy, self.locatortype(locator, env)), self.locatorpath(locator, env, xpath_val))))

    @fWaitFor
    def androidClick(self, locator, env, xpath_val=None, UnivWaitFor=0):
        """
        Given locator, identify the locator type and path from the OR file and click on the element
        """
        try:
            self.driver.find_element(getattr(AppiumBy, self.locatortype(locator, env)),
                                     self.locatorpath(locator, env, xpath_val)).click()
        except Exception:
            self.driver.execute_script("arguments[0].scrollIntoView(true);",
                                       self.driver.find_element(getattr(AppiumBy, self.locatortype(locator, env)),
                                                                self.locatorpath(locator, env, xpath_val)))
            self.driver.find_element(getattr(AppiumBy, self.locatortype(locator, env)),
                                     self.locatorpath(locator, env, xpath_val)).click()

    # Read the element text using locatorname
    @fWaitFor
    def get_Androidtext(self, locator, env, xpath_val=None, UnivWaitFor=0):
        """
        Given locator, identify the locator type and path from the OR file and return the text
        """
        return self.driver.find_element(getattr(AppiumBy, self.locatortype(locator, env)),
                                        self.locatorpath(locator, env, xpath_val)).text
