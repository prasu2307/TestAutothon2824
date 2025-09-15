# TestAutothon2824 Web Platform

A web-based interface for executing and managing TestAutothon2824 automation tests, similar to the AUTO_WEB_HOST platform.

## Quick Start

1. **Start the web platform:**
   ```bash
   run_web_platform.bat
   ```
   Or manually:
   ```bash
   python app_fastapi.py
   ```

2. **Access the platform:**
   Open your browser and go to: `http://127.0.0.1:8000`

## Features

### Test Components Available
- **🔍 SSIM Visual Tests** - Run SSIM-based visual comparison tests
- **📸 SSIM Baseline Creation** - Create baseline images for visual testing
- **🖥️ UI Tests** - Execute UI automation tests
- **🔗 API Tests** - Run API validation tests
- **📱 Mobile Tests** - Execute mobile automation tests
- **🎯 All Tests** - Run complete test suite

### Platform Capabilities
- **Real-time Execution Monitoring** - Live logs and status updates
- **Report Management** - Automatic report detection and download
- **Multiple Report Types** - Allure reports, HTML reports, SSIM diffs, baselines
- **Clean Interface** - Modern, responsive web UI

### Report Types Supported
- 📊 Allure Reports (HTML)
- 📄 HTML Test Reports
- 📁 Archive Reports
- 🔍 SSIM Visual Diffs
- 📸 SSIM Baseline Images

## Usage

1. Select your desired test component from the dropdown
2. Click "🚀 Execute Test" to start execution
3. Monitor real-time logs in the output console
4. Download generated reports from the Reports section
5. Use "🔄 Reset" to clear the interface

## File Structure

```
TestAutothon2824/
├── app_fastapi.py                    # Main Flask application
├── run_web_platform.bat     # Quick start batch file
├── WEB_PLATFORM_GUIDE.md    # This guide
└── [existing test files]
```

## Technical Details

- **Framework**: Flask web application
- **Port**: 8000 (configurable in app.py)
- **Host**: 127.0.0.1 (localhost only)
- **Real-time Updates**: 2-second polling interval
- **Report Detection**: Automatic scanning of output directories

## Customization

To add new test components, modify the `TEST_COMPONENTS` dictionary in `app_fastapi.py`:

```python
TEST_COMPONENTS = {
    'Your Test Name': 'pytest your_test_command',
    # ... existing components
}
```

## Troubleshooting

- Ensure Flask is installed: `pip install flask`
- Check that port 8000 is available
- Verify test commands work from command line first
- Check console logs for detailed error information