# Test Configurations

This directory contains example configurations for testing the validation scripts and demonstrating different project setups.

## Available Test Configurations

### Python Projects
- **`python-fastapi-test.yaml`** - FastAPI REST API project with Poetry
- Example: Inventory management API with Azure DevOps integration

### JavaScript/Node.js Projects
- **`nodejs-react-test.yaml`** - React application with TypeScript
- Example: Customer portal with GitHub integration

### .NET Projects
- **`dotnet-aspnet-test.yaml`** - ASP.NET Core Web API
- Example: Order service with Azure DevOps and Jira integration

## Using Test Configurations

### Validate a Test Configuration

```bash
# Validate a specific test configuration
python ../validation/validate_configs.py test-configs/python-fastapi-test.yaml

# Run all validations
python ../validation/validate_configs.py test-configs/*.yaml
```

### Test Hardcoded Values Checker

```bash
# Check for hardcoded values in templates
python ../validation/check_hardcoded_values.py
```

## Configuration Patterns

### Platform Integration
- **Single Platform**: Most projects use one primary platform (Azure DevOps, GitHub, or Jira)
- **Multi-Platform**: Some projects may integrate with multiple platforms
- **SDO CLI**: All configurations use SDO as the primary CLI tool

### Language-Specific Settings
- **Python**: Poetry/pip, pytest/unittest, flake8/black
- **JavaScript**: npm/yarn/pnpm, jest/mocha, eslint
- **Java**: Maven/Gradle, JUnit/TestNG, Checkstyle
- **.NET**: NuGet, xUnit/NUnit, StyleCop

### Tool Configuration
- **CLI**: Always set to 'sdo' for consistency
- **Test Runners**: Language-appropriate testing frameworks
- **Linters**: Popular linting tools for each language

## Adding New Test Configurations

When adding new test configurations:

1. **Follow Naming Convention**: `{language}-{framework}-test.yaml`
2. **Include All Required Fields**: project, platforms, language, tools
3. **Use Realistic Values**: Based on actual project setups
4. **Test Validation**: Ensure it passes validation scripts
5. **Document Purpose**: Add comments explaining the scenario

### Template for New Configurations

```yaml
# Test Configuration: {Language} {Framework} Project
# Description of the scenario this configuration represents

project:
  name: "ExampleProject"
  organization: "example-org"
  description: "Brief description of the project"

platforms:
  azure_devops: true  # or github: true, jira: true
  github: false
  jira: false

language: "python"  # python, javascript, java, dotnet
framework: "fastapi"  # specific framework

# Language-specific settings (optional)
python:
  version: "3.9"
  package_manager: "poetry"

tools:
  cli: "sdo"  # Always use 'sdo'
  test_runner: "pytest"
  linter: "flake8"

# Platform-specific settings (optional)
azure_devops:
  organization: "example-org"
  project: "ExampleProject"
```

## Validation Testing

Use these configurations to test the validation system:

```bash
# Test all configurations
for config in test-configs/*.yaml; do
    echo "Testing $config..."
    python ../validation/validate_configs.py "$config"
    echo "---"
done

# Test edge cases by modifying configurations temporarily
# (e.g., remove required fields, use invalid values)
```

## Integration Testing

These configurations can be used for integration testing:

1. **Copy to Test Project**: Copy a config to a test project
2. **Run Validation**: Ensure it passes all checks
3. **Test Workflows**: Use the config with actual workflows
4. **Verify SDO Integration**: Test SDO commands with the configuration

## Contributing

When contributing new test configurations:

- Ensure they represent real-world scenarios
- Include comprehensive comments
- Test with validation scripts
- Follow the established naming and structure conventions
- Update this README with the new configuration