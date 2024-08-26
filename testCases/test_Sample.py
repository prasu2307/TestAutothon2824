"""
Sample Test case
"""

import time
import pytest

from HelperClasses.UI.Base import Base
from HelperClasses.UI.Sample import Sample
from utilities.readProperties import ReadConfig


@pytest.mark.usefixtures("init_driver")
class Test_Sample:
    @pytest.mark.sample_run
    # @pytest.mark.regression
    def test_sample_run(self, extra, env, request, caseid):
        baseURL = ReadConfig.getApplicationURL(env)
        # Creating object of Sample class
        sample = Sample(self.driver, extra)

        # Invoking the methods from Sample
        sample.driver.get(baseURL)
        time.sleep(5)
        sample.launch_application("Welcome to Python.org", baseURL, env)
        sample.sample_operation("getting started with python", env)
