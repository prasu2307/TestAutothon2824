"""
Website Navigation and Data Extraction Test case
"""

import pytest
import os

from HelperClasses.UI.Sample import Sample
from utilities.readProperties import ReadConfig

output_user_logpath = os.getcwd() + '\\Outputs'


@pytest.mark.usefixtures("init_driver")
class Test_UI:
    @pytest.mark.ui_test
    @pytest.mark.flaky(reruns=1, reruns_delay=2)
    def test_ui_site(self, extra, env, request, caseid):

        baseURL = ReadConfig.getApplicationURL(env)
        # Creating object of Sample class
        sample = Sample(self.driver, extra)

        sample.launch_application("The Indian Express", baseURL, env)
        sample.select_edition("India", env)
        sample.launch_newslink(env)
        sample.access_new_info(env)
