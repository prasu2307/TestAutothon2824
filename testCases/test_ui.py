"""
Website Navigation and Data Extraction Test case
"""

import time
import pytest

from HelperClasses.UI.Base import Base
from HelperClasses.UI.Sample import Sample
from utilities.readProperties import ReadConfig


@pytest.mark.usefixtures("init_driver")
class Test_Sample:
    @pytest.mark.ui_test
    @pytest.mark.flaky(reruns=2, reruns_delay=2)
    def test_ui_site(self, extra, env, request, caseid):
        baseURL = ReadConfig.getApplicationURL(env)
        # Creating object of Sample class
        sample = Sample(self.driver, extra)

        # Invoking the methods from Sample
        sample.driver.get(baseURL)
        time.sleep(5)
        sample.launch_application("The Indian Express", baseURL, env)
        sample.select_edition("India", env)
        sample.launch_newslink(env)
        sample.access_new_info(env)
