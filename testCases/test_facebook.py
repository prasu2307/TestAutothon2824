"""
Facebook.com Test with Streamlit Configuration
"""
import pytest
import os
import time
from HelperClasses.UI.Sample import Sample
from utilities.readProperties import ReadConfig

output_user_logpath = os.getcwd() + '\\Outputs'


@pytest.mark.usefixtures("init_driver")
class Test_Facebook:
    
    @pytest.mark.ui_test2
    @pytest.mark.flaky(reruns=1, reruns_delay=2)
    def test_facebook_operations(self, extra, env, request, caseid):
        """
        Test Facebook operations using Streamlit configuration
        """
        # Get config values from Streamlit or fallback
        baseURL = ReadConfig.getApplicationURL(env)
        browser = ReadConfig.getBrowserName()
        team_name = ReadConfig.getEpsilonTeamName()
        headless = ReadConfig.get_headless_mode()
        
        print(f"📋 Configuration:")
        print(f"   URL: {baseURL}")
        print(f"   Browser: {browser}")
        print(f"   Team: {team_name}")
        print(f"   Headless: {headless}")
        
        # Create Sample instance
        sample = Sample(self.driver, extra)
        
        # Launch Facebook
        sample.launch_application("Facebook", baseURL, env)
        
        # Wait for page load
        time.sleep(3)

        # SSIM Visual Testing Integration
        # Perform visual checkpoint after page load
        sample.ssim_visual_checkpoint("google_homepage_ui_test", threshold=0.95)
        
        # Verify Facebook loaded
        assert "facebook" in self.driver.current_url.lower()
        
        # Take screenshot
        sample.attach_snap("Facebook Homepage")
        
        print("✅ Facebook test completed successfully")
    
    @pytest.mark.ui_test2
    @pytest.mark.flaky(reruns=1, reruns_delay=2)
    def test_facebook_title_check(self, extra, env, request, caseid):
        """
        Test Facebook page title
        """
        baseURL = ReadConfig.getApplicationURL(env)
        sample = Sample(self.driver, extra)
        
        # Launch Facebook
        sample.launch_application("Facebook", baseURL, env)
        
        # Check title contains Facebook
        title = self.driver.title
        assert "Facebook" in title or "facebook" in title.lower()
        
        print(f"✅ Facebook title verified: {title}")
