# SSIM Visual Testing Guide for TestAutothon2824

## Overview

This framework now includes SSIM (Structural Similarity Index) based visual testing capabilities adapted from the DISNEY_AEM framework. SSIM provides more robust visual comparisons for dynamic content compared to traditional pixel-by-pixel comparison.

## Key Features

- **SSIM-based comparison**: More tolerant to minor visual changes
- **Configurable thresholds**: Different sensitivity levels for different UI elements
- **Visual diff generation**: Automatic creation of comparison visualizations
- **Allure integration**: Visual test results integrated with existing reporting
- **Element-specific testing**: Test specific UI elements rather than full pages
- **Baseline management**: Automatic baseline creation and management

## Quick Start

### 1. Basic SSIM Visual Checkpoint

```python
from HelperClasses.UI.Sample import Sample

def test_visual_checkpoint(self, extra, env, request, caseid):
    sample = Sample(self.driver, extra)
    sample.launch_application("Google", "https://www.google.com/", env)
    
    # Basic visual checkpoint
    sample.ssim_visual_checkpoint("homepage_test")
```

### 2. Element-Specific Visual Testing

```python
# Test specific element with strict threshold
sample.ssim_visual_checkpoint(
    "search_box_test", 
    element_selector="input[name='q']", 
    threshold=0.95
)
```

### 3. Multiple Checkpoints with Utility Class

```python
from HelperClasses.UI.SSIMVisualCheckpoint import SSIMVisualCheckpoint

def test_multiple_checkpoints(self, extra, env, request, caseid):
    ssim_checkpoint = SSIMVisualCheckpoint(self.driver, threshold=0.85)
    
    # Multiple checkpoints
    ssim_checkpoint.capture("step1_homepage")
    # ... perform actions ...
    ssim_checkpoint.capture("step2_after_login")
    # ... perform more actions ...
    ssim_checkpoint.capture("step3_final_state")
    
    # Assert all passed
    ssim_checkpoint.assert_all_passed()
```

## SSIM Thresholds

Choose appropriate thresholds based on content type:

- **0.95 (Strict)**: For critical UI elements that should never change
- **0.85 (Moderate)**: For content areas with some dynamic elements
- **0.75 (Relaxed)**: For areas with ads, timestamps, or frequently changing content

## Available Methods

### Sample Class Methods

#### `ssim_visual_checkpoint(checkpoint_name, element_selector=None, threshold=0.85, browser="chrome")`
Performs SSIM visual checkpoint and returns result dictionary.

#### `create_ssim_baseline(test_name, element_selector=None, browser="chrome")`
Creates baseline screenshot for future comparisons.

#### `ssim_visual_assert(test_name, element_selector=None, threshold=0.85, browser="chrome")`
Performs SSIM comparison and raises AssertionError if failed.

### SSIMVisualCheckpoint Class Methods

#### `capture(checkpoint_name, element_selector=None, threshold=None)`
Captures visual checkpoint with automatic baseline creation if needed.

#### `assert_all_passed()`
Asserts that all captured checkpoints passed.

## Directory Structure

```
TestAutothon2824/
├── Outputs/
│   ├── ssim_baselines/     # Baseline screenshots
│   ├── ssim_diffs/         # Diff visualizations (failures)
│   ├── ssim_pass/          # Pass visualizations (successes)
│   └── temp_screenshots/   # Temporary current screenshots
```

## Baseline Management

### Creating Baselines

Run tests with baseline creation first:

```python
@pytest.mark.ssim_baseline_creation
def test_create_baselines(self, extra, env, request, caseid):
    sample = Sample(self.driver, extra)
    sample.launch_application("App", "https://example.com/", env)
    sample.create_ssim_baseline("homepage_full")
```

### Updating Baselines

Delete existing baseline files and re-run baseline creation tests.

## Integration with Existing Framework

The SSIM visual testing is fully integrated with:

- **Allure Reporting**: Visual results appear in Allure reports
- **Logging**: SSIM results logged with existing logger
- **Exception Handling**: Follows existing error handling patterns
- **Configuration**: Uses existing configuration structure

## Example Test Cases

See `testCases/test_ssim_visual.py` for complete examples including:

- Basic homepage visual testing
- Element-specific visual testing
- Multiple checkpoint scenarios
- Baseline creation tests
- Assertion-based testing

## Configuration

SSIM settings can be configured in `Configurations/ssim_config.ini`:

```ini
[SSIM_VISUAL_TESTING]
strict_threshold = 0.95
moderate_threshold = 0.85
relaxed_threshold = 0.75
default_threshold = 0.85
```

## Best Practices

1. **Start with baselines**: Always create baselines before running visual tests
2. **Use appropriate thresholds**: Match threshold to content stability
3. **Element-specific testing**: Test specific elements rather than full pages when possible
4. **Regular baseline updates**: Update baselines when UI legitimately changes
5. **Combine with functional tests**: Use visual testing to complement functional testing

## Troubleshooting

### Common Issues

1. **Baseline not found**: Run baseline creation test first
2. **Low SSIM scores**: Check if UI has legitimately changed or adjust threshold
3. **Element not found**: Verify element selector is correct
4. **Directory errors**: Ensure Outputs directory exists and is writable

### Debug Information

SSIM results include detailed information:
- SSIM score
- Threshold used
- Baseline and current image paths
- Visualization paths
- Error messages (if any)

## Dependencies

The SSIM visual testing requires:
- opencv-python (already in requirements.txt)
- numpy (dependency of opencv-python)
- Existing Selenium and Allure dependencies

No additional installations required beyond existing framework dependencies.