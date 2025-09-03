"""
SSIM Visual Testing Example for TestAutothon2824 Framework
"""

import pytest
import os

from HelperClasses.UI.Sample import Sample
from HelperClasses.UI.SSIMVisualTesting import SSIMVisualCheckpoint
from utilities.readProperties import ReadConfig

output_user_logpath = os.getcwd() + '\\Outputs'


@pytest.mark.usefixtures("init_driver")
class Test_SSIM_Visual:
    
    @pytest.mark.ssim_visual
    @pytest.mark.flaky(reruns=1, reruns_delay=2)
    def test_google_homepage_ssim(self, extra, env, request, caseid):
        """
        Test Google homepage with SSIM visual validation
        """
        # Creating object of Sample class
        sample = Sample(self.driver, extra)

        # Launch application
        sample.launch_application("Google", "https://www.google.com/", env)
        
        # SSIM Visual Checkpoint 1: Full page screenshot with moderate threshold
        sample.ssim_visual_checkpoint("google_homepage_full", threshold=0.85)
        
        # SSIM Visual Checkpoint 2: Search box element with strict threshold
        sample.ssim_visual_checkpoint("google_search_box", element_selector="input[name='q']", threshold=0.95)
        
        # SSIM Visual Checkpoint 3: Google logo with relaxed threshold (may have dynamic elements)
        sample.ssim_visual_checkpoint("google_logo", element_selector="img[alt='Google']", threshold=0.75)

    @pytest.mark.ssim_visual
    @pytest.mark.flaky(reruns=1, reruns_delay=2)
    def test_google_search_ssim(self, extra, env, request, caseid):
        """
        Test Google search functionality with SSIM visual validation
        """
        sample = Sample(self.driver, extra)

        # Launch application
        sample.launch_application("Google", "https://www.google.com/", env)
        
        # Perform search
        search_box = self.driver.find_element("name", "q")
        search_box.send_keys("TestAutothon2824")
        search_box.submit()
        
        # Wait for results
        import time
        time.sleep(3)
        
        # SSIM Visual Checkpoint: Search results page
        sample.ssim_visual_checkpoint("google_search_results", threshold=0.80)

    @pytest.mark.ssim_visual
    @pytest.mark.flaky(reruns=1, reruns_delay=2)
    def test_multiple_ssim_checkpoints(self, extra, env, request, caseid):
        """
        Test with multiple SSIM checkpoints using SSIMVisualCheckpoint utility
        """
        sample = Sample(self.driver, extra)

        # Launch application
        sample.launch_application("Google", "https://www.google.com/", env)
        
        # Initialize SSIM checkpoint utility
        ssim_checkpoint = SSIMVisualCheckpoint(self.driver, threshold=0.85)
        
        # Multiple checkpoints
        ssim_checkpoint.capture("checkpoint_1_homepage")
        
        # Navigate to images
        images_link = self.driver.find_element("link text", "Images")
        images_link.click()
        
        import time
        time.sleep(2)
        
        ssim_checkpoint.capture("checkpoint_2_images_page", threshold=0.80)
        
        # Assert all checkpoints passed
        ssim_checkpoint.assert_all_passed()

    @pytest.mark.ssim_baseline_creation
    def test_create_ssim_baselines(self, extra, env, request, caseid):
        """
        Test to create SSIM baselines - run this first to establish baselines
        """
        sample = Sample(self.driver, extra)

        # Launch application
        sample.launch_application("Google", "https://www.google.com/", env)
        
        # Create baselines for different scenarios
        sample.create_ssim_baseline("google_homepage_full")
        sample.create_ssim_baseline("google_search_box", element_selector="input[name='q']")
        sample.create_ssim_baseline("google_logo", element_selector="img[alt='Google']")
        
        # Search scenario baseline
        search_box = self.driver.find_element("name", "q")
        search_box.send_keys("TestAutothon2824")
        search_box.submit()
        
        import time
        time.sleep(3)
        
        sample.create_ssim_baseline("google_search_results")

    @pytest.mark.ssim_visual
    @pytest.mark.flaky(reruns=1, reruns_delay=2)
    def test_ssim_with_assertion(self, extra, env, request, caseid):
        """
        Test SSIM visual assertion that will fail if visual differences exceed threshold
        """
        sample = Sample(self.driver, extra)

        # Launch application
        sample.launch_application("Google", "https://www.google.com/", env)
        
        # This will raise AssertionError if SSIM score is below threshold
        sample.ssim_visual_assert("google_homepage_assertion", threshold=0.85)