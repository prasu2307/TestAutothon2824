# Auto Test Generator

**Standalone module for automatically generating test scripts from TestAutothon problem statements.**

## 🎯 Purpose

This module analyzes TestAutothon problem statements and automatically generates:
- UI automation test scripts
- API automation test scripts  
- Mobile automation test scripts
- Integration test scripts

## 🏗️ Architecture

```
AutoTestGenerator/
├── parsers/           # Problem statement parsing
├── templates/         # Code generation templates
├── generators/        # Main generation logic
├── examples/          # Demo files and examples
└── README.md         # This file
```

## 🚀 Quick Start

### 1. Run the Demo
```bash
cd AutoTestGenerator/examples
python demo_generator.py
```

### 2. Generate from Problem Statement
```bash
cd AutoTestGenerator
python auto_test_cli.py -p examples/testautothon2024_problem.txt -n MyTest
```

### 3. Preview Generated Code
```bash
python auto_test_cli.py -p examples/testautothon2024_problem.txt --preview
```

## 📋 Features

### Problem Statement Parser
- Extracts structured information from natural language
- Identifies UI, API, Mobile, Setup, and Reporting steps
- Recognizes entities like URLs, data fields, API endpoints

### Code Templates
- **UI Templates**: Browser automation, element interaction, data extraction
- **API Templates**: HTTP requests, data validation, response handling
- **Mobile Templates**: App automation, element interaction, data extraction

### Smart Generation
- Maps problem requirements to code templates
- Integrates with existing TestAutothon2824 framework
- Generates complete test classes with proper imports

## 🔧 Usage Examples

### Basic Generation
```python
from generators.test_generator import TestGenerator

generator = TestGenerator("output_dir")
generated_files = generator.generate_from_problem_statement(problem_text, "MyTest")
saved_files = generator.save_generated_tests(generated_files)
```

### Custom Templates
```python
from templates.ui_templates import UITemplates

ui_code = UITemplates.launch_browser_template("IndianExpress", "https://indianexpress.com")
```

## 📊 Generated Test Structure

### UI Test Example
```python
@pytest.mark.usefixtures("init_driver")
class MyTest_UI:
    @pytest.mark.ui_test
    @pytest.mark.auto_generated
    def test_auto_generated_ui(self, extra, env, request, caseid):
        sample = Sample(self.driver, extra)
        sample.launch_application("IndianExpress", "https://indianexpress.com/", env)
        # ... generated code
```

### API Test Example
```python
class MyTest_API:
    @pytest.mark.api_test
    @pytest.mark.auto_generated
    def test_auto_generated_api(self):
        # ... generated API interaction code
```

## 🎛️ Configuration

### CLI Options
- `--problem-file, -p`: Path to problem statement file
- `--test-name, -n`: Name for generated test classes
- `--output-dir, -o`: Output directory for generated tests
- `--preview`: Preview code without saving

## 🔗 Integration

### With Existing Framework
Generated tests automatically integrate with:
- `HelperClasses.UI.Sample` for UI automation
- `HelperClasses.API.ValidateAPI` for API testing
- Existing pytest configuration
- SSIM visual testing capabilities
- Allure reporting

### Test Execution
```bash
# Run generated tests
pytest generated_tests/ -v

# Run with markers
pytest generated_tests/ -m auto_generated

# Run specific test type
pytest generated_tests/ui_test.py -v
```

## 🛠️ Extending the Generator

### Adding New Templates
1. Create template in appropriate `templates/` file
2. Add template method to template class
3. Update generator logic to use new template

### Custom Parsers
1. Extend `ProblemParser` class
2. Add new entity extraction methods
3. Update step classification logic

## 📈 Benefits

- **Time Saving**: Instantly generate test scaffolding
- **Consistency**: Standardized test structure
- **Framework Integration**: Works with existing TestAutothon2824 setup
- **Extensible**: Easy to add new templates and patterns
- **Standalone**: No impact on existing codebase

## 🎯 Future Enhancements

- AI-powered code generation
- Visual element recognition
- Dynamic selector generation
- Test data management
- Report generation templates

---

**Note**: This is a completely standalone module that doesn't modify any existing TestAutothon2824 code or functionality.