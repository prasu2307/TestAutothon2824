# Auto Test Generator - Usage Guide

## 🚀 Quick Start

### 1. Run Demo
```bash
cd AutoTestGenerator/examples
python demo_generator.py
```

### 2. Generate Tests from Problem Statement
```bash
cd AutoTestGenerator
python auto_test_cli.py -p examples/testautothon2024_problem.txt -n MyTestSuite
```

### 3. Preview Generated Code
```bash
python auto_test_cli.py -p examples/testautothon2024_problem.txt --preview
```

## 📋 What Gets Generated

From a TestAutothon problem statement, the generator creates:

### UI Test (`ui_test.py`)
- Browser automation with Selenium
- Element interaction and data extraction
- Integration with existing Sample class
- SSIM visual checkpoints
- Proper pytest structure

### API Test (`api_test.py`) 
- HTTP requests for data submission
- Response validation
- Date formatting (DDMMYYYY)
- Item ID extraction and validation

### Mobile Test (`mobile_test.py`)
- Appium-based mobile automation
- Product data extraction
- Mobile element interactions
- Driver setup and cleanup

### Integration Test (`integration_test.py`)
- Complete end-to-end flow
- UI → API → Mobile workflow
- Data validation across all layers

## 🎯 Key Features

### Smart Parsing
- Recognizes UI, API, Mobile, Setup, and Reporting steps
- Extracts entities like URLs, data fields, API endpoints
- Maps natural language to code templates

### Framework Integration
- Uses existing `HelperClasses.UI.Sample`
- Integrates with `HelperClasses.API.ValidateAPI`
- Maintains pytest structure and markers
- Supports SSIM visual testing

### Customizable Output
- Template-based generation
- Easy to extend with new patterns
- Configurable test names and output directories

## 📝 Example Generated Code

### UI Test Structure
```python
@pytest.mark.usefixtures("init_driver")
class MyTest_UI:
    @pytest.mark.ui_test
    @pytest.mark.auto_generated
    def test_auto_generated_ui(self, extra, env, request, caseid):
        sample = Sample(self.driver, extra)
        
        # Auto-generated browser launch
        sample.launch_application("IndianExpress", "https://indianexpress.com/", env)
        
        # Auto-generated element interactions
        section_links = ["India", "Sports", "Business", "Politics"]
        # ... generated interaction code
        
        # Auto-generated data extraction
        extracted_data = []
        # ... generated extraction code
```

## 🔧 Customization

### Adding New Templates
1. Edit files in `templates/` directory
2. Add new template methods
3. Update generator logic in `generators/test_generator.py`

### Extending Parser
1. Modify `parsers/problem_parser.py`
2. Add new keywords and entity extraction
3. Update step classification logic

## 🎪 Integration with Existing Framework

Generated tests automatically work with your existing:
- `conftest.py` configuration
- `utilities/readProperties.py`
- `HelperClasses/` modules
- Allure reporting setup
- SSIM visual testing

## 🏃‍♂️ Running Generated Tests

```bash
# Run all generated tests
pytest generated_tests/ -v

# Run specific test type
pytest generated_tests/ui_test.py -v

# Run with auto-generated marker
pytest -m auto_generated -v

# Run with Allure reporting
pytest generated_tests/ --alluredir=allure-results
```

## 💡 Tips

1. **Review Generated Code**: Always review and customize generated tests
2. **Update Selectors**: Modify CSS selectors based on actual website structure
3. **Add Assertions**: Enhance generated tests with specific validations
4. **Integrate Gradually**: Start with one test type and expand

## 🔄 Workflow

1. **Input**: TestAutothon problem statement (text file)
2. **Parse**: Extract structured information
3. **Generate**: Create test code from templates
4. **Review**: Customize generated code as needed
5. **Execute**: Run tests with existing framework
6. **Report**: Use Allure for comprehensive reporting

---

**Note**: This generator creates scaffolding code that may need customization based on actual website structures and API specifications.