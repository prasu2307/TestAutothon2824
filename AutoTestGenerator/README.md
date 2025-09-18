# AutoTestGenerator

**Standalone module for automatically generating test scripts from TestAutothon problem statements.**

## Quick Start

```bash
# Run demo
cd AutoTestGenerator/examples
python demo_generator.py

# Generate tests from problem statement
cd AutoTestGenerator
python auto_test_cli.py -p examples/testautothon2024_problem.txt -n MyTest
```

## Features

- **Problem Statement Parser** - Extracts structured info from natural language
- **Multi-Layer Test Generation** - UI, API, Mobile, Integration tests
- **Framework Integration** - Uses existing TestAutothon2824 classes
- **No External Dependencies** - Uses only built-in Python libraries

## Generated Test Types

- **UI Tests** - Selenium-based browser automation
- **API Tests** - HTTP requests and validation
- **Mobile Tests** - Appium mobile automation
- **Integration Tests** - End-to-end workflows

## PyCharm Setup

If PyCharm shows import errors:
1. Right-click on `AutoTestGenerator` folder
2. Select "Mark Directory as" → "Sources Root"
3. Or add to Python Path in Project Settings

## No External Packages Required

This module uses only Python built-in libraries. The generated tests integrate with your existing TestAutothon2824 framework dependencies.