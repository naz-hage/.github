# Testing Workflow

This workflow guides the testing and validation of code changes, ensuring quality and reliability before deployment.

## Overview

The testing workflow covers unit testing, integration testing, manual validation, and cross-platform compatibility testing to ensure code changes meet quality standards.

## Prerequisites
- Code changes implemented and committed
- Development environment set up
- Access to testing tools and frameworks
- Azure DevOps work item context

## Testing Types

### 1. Unit Testing
Test individual functions, methods, and classes in isolation.

**Commands:**
```bash
# Run all unit tests
python -m pytest

# Run specific test file
python -m pytest tests/test_filename.py

# Run with coverage
python -m pytest --cov=src --cov-report=html

# Run specific test function
python -m pytest tests/test_filename.py::test_function_name
```

**Best Practices:**
- [ ] Test both positive and negative scenarios
- [ ] Mock external dependencies
- [ ] Test edge cases and error conditions
- [ ] Maintain high test coverage (>80%)
- [ ] Write descriptive test names

### 2. Integration Testing
Test component interactions and end-to-end workflows.

**Commands:**
```bash
# Run integration tests
python -m pytest tests/integration/

# Test Azure DevOps integration
python -m pytest tests/integration/test_azdo_integration.py

# Test CLI commands
python -c "import subprocess; subprocess.run(['python', '-m', 'saz_package.cli', 'repo', 'list'])"
```

**Validation Steps:**
- [ ] API calls work correctly
- [ ] Authentication is handled properly
- [ ] Error responses are processed
- [ ] Data transformations are accurate

### 3. Manual Testing
Interactive testing of user-facing functionality.

**CLI Testing Checklist:**
```bash
# Test basic commands
python -m saz_package.cli --help
python -m saz_package.cli repo --help
python -m saz_package.cli pipeline --help

# Test with real Azure DevOps data
python -m saz_package.cli repo list
python -m saz_package.cli pipeline list

# Test error scenarios
python -m saz_package.cli repo show invalid-repo-name
python -m saz_package.cli pipeline run invalid-pipeline
```

**Manual Validation:**
- [ ] Commands execute without errors
- [ ] Output is readable and informative
- [ ] Error messages are helpful
- [ ] Authentication prompts work
- [ ] Large data sets display correctly

### 4. Cross-Platform Testing
Ensure compatibility across Windows, macOS, and Linux.

**Platform Testing:**
- [ ] Windows (PowerShell/cmd)
- [ ] macOS (Terminal/zsh)
- [ ] Linux (bash)
- [ ] Different Python versions (3.8+)

**Path Handling:**
- [ ] Absolute and relative paths work
- [ ] File separators are handled correctly
- [ ] Unicode characters in paths
- [ ] Long path names (>260 characters on Windows)

## PBI Status Checking

Use the PBI status checker to validate work item completion:

### Input Parameters
```
Repository: [PROJECT_ROOT]
Current Branch: [CURRENT_BRANCH]
PBI Number: [PBI_ID]
Work Item Type: PBI
```

### Status Validation
- [ ] All acceptance criteria marked complete [x]
- [ ] Related tasks are in "Done" state
- [ ] Code changes implement all requirements
- [ ] Documentation is updated
- [ ] Tests are passing

## Automated Testing Setup

### pytest Configuration
```ini
# pytest.ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --tb=short --cov=src --cov-report=term-missing
```

### Test Structure
```
tests/
├── unit/
│   ├── test_client.py
│   ├── test_cli.py
│   └── test_repositories.py
├── integration/
│   ├── test_azdo_integration.py
│   └── test_end_to_end.py
└── fixtures/
    ├── azdo_responses.json
    └── test_data.py
```

## Performance Testing

### Benchmarking
```python
import time
import pytest

def test_api_response_time():
    start_time = time.time()
    # Execute API call
    result = client.get_repository("test-repo")
    end_time = time.time()

    assert end_time - start_time < 5.0  # Should respond within 5 seconds
    assert result is not None
```

### Load Testing Considerations
- [ ] Handle large result sets
- [ ] Memory usage stays within limits
- [ ] Network timeouts are handled
- [ ] Rate limiting is respected

## Security Testing

### Authentication Testing
- [ ] Valid PAT tokens work
- [ ] Invalid tokens show appropriate errors
- [ ] Token permissions are validated
- [ ] Secure token storage (not in code/logs)

### Input Validation
- [ ] SQL injection prevention
- [ ] XSS protection in outputs
- [ ] Path traversal attacks blocked
- [ ] Malformed input handling

## Accessibility Testing

### CLI Usability
- [ ] Commands have helpful --help output
- [ ] Error messages are clear and actionable
- [ ] Progress indicators for long operations
- [ ] Consistent command structure

## Continuous Integration

### GitHub Actions Validation
```yaml
# .github/workflows/test.yml
name: Test
on: [push, pull_request]
jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        python-version: [3.8, 3.9, '3.10', '3.11']
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    - name: Install dependencies
      run: pip install -r requirements.txt
    - name: Run tests
      run: python -m pytest --cov=src --cov-report=xml
```

## Test Reporting

### Coverage Reports
```bash
# Generate HTML coverage report
python -m pytest --cov=src --cov-report=html
# Open htmlcov/index.html in browser

# Generate XML for CI
python -m pytest --cov=src --cov-report=xml
```

### Quality Gates
- [ ] Test coverage > 80%
- [ ] All tests pass
- [ ] No critical security issues
- [ ] Performance benchmarks met
- [ ] Cross-platform compatibility verified

## Error Handling Validation

### Expected Error Scenarios
- [ ] Network connectivity issues
- [ ] Invalid authentication
- [ ] Permission denied
- [ ] Resource not found
- [ ] Rate limiting
- [ ] Malformed responses

### Error Message Quality
- [ ] Messages are user-friendly
- [ ] Include actionable guidance
- [ ] Don't expose sensitive information
- [ ] Consistent error format across commands