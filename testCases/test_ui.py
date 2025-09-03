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

        sample.launch_application("Facebook", "https://www.facebook.com/", env)
        
        # SSIM Visual Testing Integration
        # Perform visual checkpoint after page load
        sample.ssim_visual_checkpoint("google_homepage_ui_test", threshold=0.95)
        
        # sample.launch_application("The Indian Express", baseURL, env)
        # sample.select_edition("India", env)
        # sample.launch_newslink(env)
        # sample.access_new_info(env)
    
    @pytest.mark.ui_test
    @pytest.mark.ssim_visual
    @pytest.mark.flaky(reruns=1, reruns_delay=2)
    def test_ui_site_with_ssim_validation(self, extra, env, request, caseid):
        """
        Enhanced UI test with SSIM visual validation
        """
        baseURL = ReadConfig.getApplicationURL(env)
        sample = Sample(self.driver, extra)

        # Launch application with visual validation
        sample.launch_application("Google", "https://www.google.com/", env)
        
        # SSIM Visual Checkpoints
        sample.ssim_visual_checkpoint("google_homepage_enhanced", threshold=0.85)
        
        # Test search functionality with visual validation
        search_box = self.driver.find_element("name", "q")
        search_box.send_keys("TestAutothon2824 Framework")
        
        # Visual checkpoint before search
        sample.ssim_visual_checkpoint("google_search_entered", threshold=0.80)
        
        search_box.submit()
        
        # Wait for results and validate visually
        import time
        time.sleep(3)
        
        # Visual checkpoint after search results
        sample.ssim_visual_checkpoint("google_search_results", threshold=0.75)
