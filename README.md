# TestAutothon2824
This repo created to handle Test Autothon 2024 scripts

## New Feature: SSIM Visual Testing

This framework now includes SSIM (Structural Similarity Index) based visual testing capabilities for robust UI validation.

### Quick Start with SSIM Visual Testing

1. **Run baseline creation first:**
   ```bash
   pytest testCases/test_ssim_visual.py::Test_SSIM_Visual::test_create_ssim_baselines -m ssim_baseline_creation
   ```

2. **Run SSIM visual tests:**
   ```bash
   pytest testCases/test_ssim_visual.py -m ssim_visual
   ```

3. **Or use the batch file:**
   ```bash
   run_ssim_visual_tests.bat
   ```

### Key Features
- SSIM-based visual comparison (more robust than pixel comparison)
- Configurable thresholds for different UI stability levels
- Automatic visual diff generation
- Integration with existing Allure reporting
- Element-specific visual testing

### Documentation
See `SSIM_VISUAL_TESTING_GUIDE.md` for complete documentation and examples.
