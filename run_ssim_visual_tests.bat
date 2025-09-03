@echo off
echo Starting SSIM Visual Tests for TestAutothon2824...

REM Create baseline tests first
echo Creating SSIM baselines...
pytest testCases/test_ssim_visual.py::Test_SSIM_Visual::test_create_ssim_baselines -m ssim_baseline_creation -v --alluredir=Outputs/Allure_reports

REM Run SSIM visual tests
echo Running SSIM visual tests...
pytest testCases/test_ssim_visual.py -m ssim_visual -v --alluredir=Outputs/Allure_reports

REM Run enhanced UI test with SSIM
echo Running enhanced UI tests with SSIM...
pytest testCases/test_ui.py::Test_UI::test_ui_site_with_ssim_validation -m ssim_visual -v --alluredir=Outputs/Allure_reports

echo SSIM Visual Tests completed!
echo Check Outputs/ssim_* directories for visual comparison results.

pause