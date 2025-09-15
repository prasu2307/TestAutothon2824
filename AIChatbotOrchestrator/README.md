# AI Chatbot Orchestrator

Natural Language Test Execution and Optimization for TestAutothon2824 Framework

## Features

- **Natural Language Processing**: Execute tests using plain English commands
- **Intelligent Test Selection**: Automatically maps commands to appropriate test files
- **Test Optimization**: AI-driven suggestions for improving test stability and performance
- **Multiple Interfaces**: CLI, Web, and programmatic access

## Quick Start

### 1. Command Line Interface
```bash
python run_chatbot.py
```

### 2. Web Interface
```bash
python AIChatbotOrchestrator/web_interface.py
```
Then open http://localhost:5000

### 3. Demo Mode
```bash
python run_chatbot.py demo
```

## Example Commands

### Test Execution
- "Run UI tests on Chrome"
- "Execute API tests for non-prod"
- "Test visual validation"
- "Start mobile testing"

### Test Optimization
- "Optimize visual tests"
- "Fix flaky tests"
- "Speed up test execution"
- "Improve test stability"

### Test Analysis
- "Analyze UI test results"
- "Check test performance"
- "Review test coverage"

## Architecture

```
AIChatbotOrchestrator/
├── chatbot_engine.py      # Main orchestration engine
├── nlp_processor.py       # Natural language processing
├── test_executor.py       # Test execution logic
├── chatbot_cli.py         # Command line interface
├── web_interface.py       # Web-based interface
└── README.md             # This file
```

## Integration

The chatbot integrates seamlessly with existing TestAutothon2824 framework:
- Uses existing test files without modification
- Leverages current pytest configuration
- Maintains all existing functionality
- Adds AI layer on top of existing infrastructure

## Dependencies

- No additional dependencies for basic functionality
- Flask (optional, for web interface)
- Existing TestAutothon2824 dependencies

## Usage Examples

```python
from AIChatbotOrchestrator import TestChatBot

chatbot = TestChatBot()
response = chatbot.process_command("Run visual tests with optimization")
print(response)
```