# SDO CLI Tool - Copilot Development Guidelines

## Overview

Welcome to the SDO (Simple DevOps) CLI tool development! This document provides comprehensive guidelines for AI-assisted development using GitHub Copilot. SDO is an open-source CLI tool that provides a unified interface for managing development operations across multiple platforms. It is part of the ntools suite available at https://github.com/naz-hage/ntools/tree/main/atools.

## Project Context

**Technology Stack:**
- **Language**: Python 3.8+ (tested with 3.8, 3.9, 3.10, 3.11, 3.12)
- **Architecture**: Modular CLI with separate command modules
- **APIs**: DevOps platform REST APIs (Azure DevOps, GitHub, etc.)
- **Authentication**: Personal Access Tokens (PAT)
- **Packaging**: Standard Python packaging with setup.py/pyproject.toml

**Key Components:**
- `sdo_package/cli.py`: Command-line interface and argument parsing
- `sdo_package/client.py`: DevOps platform REST API client
- `sdo_package/repositories.py`: Repository operations
- `sdo_package/pipelines.py`: Pipeline operations
- `sdo_package/pull_requests.py`: Pull request operations
- `sdo_package/users.py`: User management operations

## Development Guidelines

### Code Quality Standards

**Black Code Formatting:**
- Line length: 100 characters
- Use Black formatter for consistent styling
- Import sorting with `isort` using black profile

**Type Hints:**
- Use type hints for all function parameters and return values
- Compatible with Python 3.8+ type annotation syntax
- Use `typing` module for complex types

**Error Handling:**
- Handle Azure DevOps API errors gracefully
- Provide meaningful error messages with actionable guidance
- Log errors with appropriate log levels (DEBUG, INFO, WARNING, ERROR)
- Don't expose sensitive information in error messages

**Logging:**
- Use Python's `logging` module
- Include timestamps, log levels, and contextual information
- Log API requests/responses at DEBUG level for troubleshooting

### API Interaction Patterns

**REST API Client Design:**
```python
# Preferred pattern for API calls
def get_repository_info(self, repo_name: str) -> Dict[str, Any]:
    """Get detailed repository information."""
    url = f"{self.base_url}/git/repositories/{repo_name}"
    response = self.session.get(url, headers=self.headers)

    if response.status_code != 200:
        logger.error(f"Failed to get repository info: {response.status_code}")
        response.raise_for_status()

    return response.json()
```

**Authentication:**
- Use Personal Access Tokens (PAT) from environment variables
- Store PAT securely, never in code or version control
- Validate PAT permissions before operations

**Rate Limiting & Retry Logic:**
```python
# Implement exponential backoff for API calls
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

retry_strategy = Retry(
    total=3,
    status_forcelist=[429, 500, 502, 503, 504],
    backoff_factor=1
)
adapter = HTTPAdapter(max_retries=retry_strategy)
```

### CLI Design Patterns

**Command Structure:**
```python
# Standard command handler pattern
def cmd_repo_show(args: argparse.Namespace) -> None:
    """Show detailed repository information."""
    client = AzureDevOpsClient(verbose=getattr(args, 'verbose', False))

    try:
        repo_info = client.get_repository(args.repo_name)
        display_repository_info(repo_info)

        # Show full API response in verbose mode
        if getattr(args, 'verbose', False):
            print("Full API Response:")
            print(json.dumps(repo_info, indent=2, default=str))

    except requests.exceptions.RequestException as e:
        logger.error(f"API request failed: {e}")
        print(f"[ERROR] Failed to get repository information: {e}")
        sys.exit(1)
```

**Argument Parsing:**
- Use `argparse` for command-line arguments
- Support global `--verbose` flag for detailed API output
- Validate required parameters before API calls
- Provide helpful error messages for invalid arguments

### Testing Standards

**Unit Testing:**
- Use `pytest` for test framework
- Mock external API calls with `unittest.mock`
- Test error conditions and edge cases
- Aim for high test coverage

**Integration Testing:**
- Test with real Azure DevOps instances when possible
- Use test PATs with limited permissions
- Validate end-to-end workflows

**Test Structure:**
```python
# Example test pattern
def test_repo_show_success(client_mock):
    """Test successful repository show command."""
    # Arrange
    mock_repo_data = {"name": "test-repo", "id": "123"}
    client_mock.get_repository.return_value = mock_repo_data

    # Act
    with patch('sys.argv', ['sdo', 'repo', 'show', 'test-repo']):
        main()

    # Assert
    client_mock.get_repository.assert_called_once_with('test-repo')
    # Verify output contains expected information
```

### Documentation Expectations

**Code Documentation:**
- Write docstrings for all public functions and classes
- Include parameter types and return value descriptions
- Document exceptions that may be raised
- Use Google/NumPy docstring format

**README Updates:**
- Update README.md for new features and commands
- Include usage examples with `--verbose` flag
- Document prerequisites and setup instructions
- Keep installation and configuration instructions current

**Architecture Documentation:**
- Update ARCHITECTURE.md for significant changes
- Document new components and their responsibilities
- Include data flow diagrams when adding new features

## When to Use Copilot Effectively

### Ideal Scenarios for Copilot

**Repetitive Code Patterns:**
- API client methods following similar patterns
- CLI command handlers with standard structure
- Error handling and logging boilerplate
- Unit test skeletons

**Standard Library Usage:**
- Common Python patterns and idioms
- File I/O operations
- JSON parsing and manipulation
- HTTP request handling

**Azure DevOps API Integration:**
- REST API endpoint construction
- Response parsing and validation
- Authentication header setup
- Error response handling

### When to Be Cautious

**Complex Business Logic:**
- Custom algorithms or complex workflows
- Security-sensitive operations
- Performance-critical code paths

**Azure DevOps Specific Knowledge:**
- Organization/project/repository extraction logic
- PAT permission requirements
- API versioning and deprecation handling

**Cross-Platform Compatibility:**
- Windows-specific path handling
- Unicode encoding considerations
- Console output formatting

## Preferred Code Patterns

### Repository Operations
```python
def cmd_repo_list(args: argparse.Namespace) -> None:
    """List all repositories in the project."""
    client = AzureDevOpsClient(verbose=getattr(args, 'verbose', False))

    try:
        repos = client.list_repositories()

        if not repos:
            print("[INFO] No repositories found in project.")
            return

        print(f"Repositories in project '{client.project}' ({len(repos)} total):")
        print("-" * 70)

        for repo in repos:
            print(f"-- {repo['name']}")
            print(f"   ID: {repo['id']}")
            print(f"   URL: {repo['webUrl']}")
            print(f"   Default Branch: {repo.get('defaultBranch', 'main')}")
            print()

        if getattr(args, 'verbose', False):
            print("Full API Response:")
            print(json.dumps(repos, indent=2, default=str))

    except Exception as e:
        logger.error(f"Failed to list repositories: {e}")
        print(f"[ERROR] Failed to list repositories: {e}")
        sys.exit(1)
```

### Pipeline Operations
```python
def cmd_pipeline_run(args: argparse.Namespace) -> None:
    """Run/queue a pipeline."""
    client = AzureDevOpsClient(verbose=getattr(args, 'verbose', False))

    try:
        # Validate pipeline exists first
        pipeline_info = client.get_pipeline(args.pipeline_name)
        if not pipeline_info:
            print(f"[ERROR] Pipeline '{args.pipeline_name}' not found.")
            sys.exit(1)

        # Queue the pipeline run
        run_result = client.run_pipeline(args.pipeline_name)

        print(f"[OK] Pipeline '{args.pipeline_name}' queued successfully.")
        print(f"Build ID: {run_result['id']}")
        print(f"Build Number: {run_result.get('buildNumber', 'N/A')}")
        print(f"Status: {run_result.get('status', 'Unknown')}")

        if getattr(args, 'verbose', False):
            print("\nFull API Response:")
            print(json.dumps(run_result, indent=2, default=str))

    except Exception as e:
        logger.error(f"Failed to run pipeline: {e}")
        print(f"[ERROR] Failed to run pipeline '{args.pipeline_name}': {e}")
        sys.exit(1)
```

### Error Handling Pattern
```python
def safe_api_call(func: Callable, *args, **kwargs) -> Any:
    """Execute API call with proper error handling."""
    try:
        return func(*args, **kwargs)
    except requests.exceptions.ConnectionError:
        logger.error("Network connection failed")
        raise click.ClickException("Unable to connect to Azure DevOps. Check your internet connection.")
    except requests.exceptions.Timeout:
        logger.error("API request timed out")
        raise click.ClickException("Request timed out. Azure DevOps may be experiencing issues.")
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            raise click.ClickException("Authentication failed. Check your AZURE_DEVOPS_PAT token.")
        elif e.response.status_code == 403:
            raise click.ClickException("Access denied. Your PAT may not have sufficient permissions.")
        elif e.response.status_code == 404:
            raise click.ClickException("Resource not found. Check the repository/pipeline name.")
        else:
            logger.error(f"HTTP error {e.response.status_code}: {e.response.text}")
            raise click.ClickException(f"Azure DevOps API error: {e.response.status_code}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise click.ClickException(f"An unexpected error occurred: {e}")
```

## Best Practices for Copilot Usage

### Code Review Checklist
- [ ] **Security**: No hardcoded credentials or sensitive data
- [ ] **Error Handling**: Proper exception handling and user-friendly messages
- [ ] **Logging**: Appropriate log levels and contextual information
- [ ] **Type Hints**: All parameters and return values typed
- [ ] **Documentation**: Docstrings for public functions
- [ ] **Testing**: Unit tests for new functionality
- [ ] **Cross-Platform**: Windows compatibility verified

### Commit Message Standards
```
feat: add verbose flag to all CLI commands

- Add --verbose/-v flag to display full API JSON responses
- Update all command handlers in repositories.py, pipelines.py, pull_requests.py, users.py
- Fix Unicode encoding issues for Windows console compatibility
- Update README.md and ARCHITECTURE.md documentation

Closes #160
```

### Pull Request Guidelines
- **Title**: `Task #160: Add Copilot Instructions with Development Guidelines`
- **Description**: Include acceptance criteria and implementation details
- **Labels**: `development`, `documentation`, `enhancement`
- **Reviewers**: Request review from team members familiar with CLI tools
- **Testing**: Include test results and validation steps

## Common Pitfalls to Avoid

### Azure DevOps API Issues
- **PAT Permissions**: Ensure PAT has required permissions before testing
- **API Versions**: Use current API versions and handle deprecations
- **Rate Limits**: Implement backoff strategies for rate-limited endpoints
- **Organization URLs**: Handle different Azure DevOps organization URL formats

### Python Environment Issues
- **Version Compatibility**: Test with Python 3.8+ versions
- **Dependencies**: Keep requirements.txt/pyproject.toml updated
- **Virtual Environments**: Use virtual environments for development
- **Path Handling**: Use pathlib for cross-platform path operations

### CLI Design Issues
- **Argument Validation**: Validate all required arguments before API calls
- **Help Messages**: Provide clear, actionable help text
- **Exit Codes**: Use appropriate exit codes (0 for success, 1 for errors)
- **Output Formatting**: Ensure readable output on different terminal widths

Remember: Copilot is a powerful assistant, but understanding the SDO project's architecture, DevOps APIs, and Python best practices is essential for producing high-quality code. Always review and test Copilot-generated code thoroughly before committing.

---

# SDO - DevOps CLI Tool

SDO (Simple DevOps) is a comprehensive command-line interface tool for managing DevOps resources across multiple platforms including repositories, pipelines, pull requests, and user operations. Built with Python and designed for unified platform support.

Always reference these instructions first and fallback to search or bash commands only when you encounter unexpected information that does not match the info here.

## Working Effectively

### Prerequisites and Environment Setup
- **CRITICAL**: Requires Python 3.8+ (tested with Python 3.8, 3.9, 3.10, 3.11, 3.12)
- **Azure DevOps PAT Required**: Personal Access Token with appropriate permissions for operations
- **Git Repository**: Must be in a Git repository with Azure DevOps remote configured

```bash
# Install Python dependencies - takes 30-60 seconds
pip install -r requirements.txt

# For development work, install additional tools
pip install -e .
pip install flake8 black isort pylint mypy pytest build

# Set up Azure DevOps PAT (required for all operations)
export AZURE_DEVOPS_PAT="your-personal-access-token-here"

# Verify Git remote is configured for Azure DevOps
git remote -v
```

### Project Structure Overview
SDO uses a modular Python package architecture:
- `sdo_package/`: Main package directory
- `sdo_package/cli.py`: Command-line interface entry point
- `sdo_package/client.py`: DevOps platform REST API client
- `sdo_package/repositories.py`: Repository operations
- `sdo_package/pipelines.py`: Pipeline operations
- `sdo_package/pull_requests.py`: Pull request operations
- `sdo_package/users.py`: User management operations

### Core Commands

**TIMING WARNING**: API operations may take 5-30 seconds depending on Azure DevOps response times. Set reasonable timeouts.

```bash
# Basic repository operations - takes 5-15 seconds each
python -m saz_package.cli repo list                    # List all repositories
python -m saz_package.cli repo show                    # Show current repository info
python -m saz_package.cli repo create my-new-repo      # Create a new repository

# Pipeline operations - takes 10-30 seconds
python -m saz_package.cli pipeline list                # List all pipelines
python -m saz_package.cli pipeline run "My Pipeline"   # Run a pipeline
python -m saz_package.cli pipeline status 12345        # Check pipeline status

# Pull request operations - takes 5-20 seconds
python -m saz_package.cli pr list                      # List active pull requests
python -m saz_package.cli pr create --title "My PR" --source-branch feature/branch
python -m saz_package.cli pr show 123                  # Show PR details
python -m saz_package.cli pr approve 123               # Approve a PR
python -m saz_package.cli pr merge 123                 # Merge a PR

# User operations - takes 3-10 seconds
python -m saz_package.cli user show                    # Show current user info
python -m saz_package.cli user list                    # List organization users
python -m saz_package.cli user search "john"           # Search for users

# Azure DevOps CLI operations - useful for project management

## List all Product Backlog Items and Tasks - takes 5-15 seconds
az boards query --wiql "SELECT [System.Id], [System.Title], [System.State] FROM WorkItems WHERE [System.WorkItemType] = 'Product Backlog Item'" --output table

## List all Tasks - takes 5-15 seconds
az boards query --wiql "SELECT [System.Id], [System.Title], [System.State] FROM WorkItems WHERE [System.WorkItemType] = 'Task'" --output table

## Show details of a specific work item - takes 3-10 seconds
az boards work-item show --id 170 --output table

## Delete a work item (permanent - use with caution) - takes 3-10 seconds
az boards work-item delete --id 123 --yes

## Update a work item field - takes 3-10 seconds
az boards work-item update --id 170 --fields System.State=Done

**Valid State Values (Scrum Process Template):**
- **Product Backlog Item**: New, Approved, Committed, Done
- **Bug**: New, Approved, Committed, Done
- **Task**: To Do, In Progress, Done
- **Epic**: New, In Progress, Done

## PowerShell: Check Work Item Type Programmatically
```powershell
# Check if work item is a PBI
az boards work-item show --id 170 --output table | Select-String "Product Backlog Item"

# Check if work item is a Task  
az boards work-item show --id 159 --output table | Select-String "Task"

# Conditional logic based on work item type
$output = az boards work-item show --id 170 --output table
if ($output | Select-String "Product Backlog Item") { 
    "This is a PBI - valid states: New, Approved, Committed, Done"
} elseif ($output | Select-String "Task") { 
    "This is a Task - valid states: To Do, In Progress, Done"
} else { 
    "Unknown work item type" 
}
```

##
```

### Development Workflow

**Remote Naming Convention:**
- **azure**: Primary remote for Azure DevOps development and PR creation
- **origin**: GitHub backup remote for repository mirroring
- Always create pull requests on Azure DevOps (azdo), not GitHub
- Use `azure` remote for all development operations (fetch, pull, push)

**Pull Request Creation:**
- Always create PRs on Azure DevOps, never on GitHub
- Use the `saz pr create` command for PR preparation
- Create PR markdown file with title and description, then run: `saz pr create --file pr-description.md --work-item <id>`
- Link PRs to relevant work items using task IDs
- Follow the code-review.md workflow for PR processes

**Code Quality Tools**:
- **Black**: Code formatting (line length: 100)
- **isort**: Import sorting with black profile
- **flake8**: Style guide enforcement
- **pylint**: Static analysis
- **mypy**: Type checking (Python 3.8+ compatible)

```bash
# Run all quality checks - takes 30-60 seconds
make lint

# Format code - takes 10-30 seconds
make format

# Run individual checks
make lint-flake8    # Style checking
make lint-black     # Format checking
make lint-isort     # Import sorting check
make lint-pylint    # Static analysis
make lint-mypy      # Type checking
```

### Testing Infrastructure

**NOTE**: Test coverage may be limited. Focus on integration testing with real Azure DevOps instances.

```bash
# Run tests (if available) - takes 10-30 seconds
make test
# or
python -m pytest

# Build distribution packages - takes 5-15 seconds
python -m build
```

## Complete Validation Workflow

### COMPREHENSIVE VALIDATION SCENARIO
Run this complete validation to ensure all major functionality works:

```bash
# Complete validation workflow - takes 30-60 seconds total
echo "=== COMPREHENSIVE VALIDATION OF SAZ ==="

# 1. Verify Python version compatibility
python --version
python -c "import sys; print(f'Python {sys.version_info.major}.{sys.version_info.minor}')"
echo "✅ Python version: PASSED"

# 2. Install dependencies
pip install -r requirements.txt
echo "✅ Dependencies: PASSED"

# 3. Verify package structure
python -c "import saz_package; print('Package import: OK')"
echo "✅ Package structure: PASSED"

# 4. Check Azure DevOps PAT is configured
if [ -z "$AZURE_DEVOPS_PAT" ]; then
    echo "❌ AZURE_DEVOPS_PAT not set"
    exit 1
else
    echo "✅ Azure DevOps PAT: CONFIGURED"
fi

# 5. Verify Git remote configuration
if git remote -v | grep -q "dev.azure.com"; then
    echo "✅ Git remote: AZURE DEVOPS CONFIGURED"
else
    echo "⚠️  Git remote: NOT AZURE DEVOPS (some features may not work)"
fi

# 6. Test basic CLI help
python -m saz_package.cli --help > /dev/null 2>&1
echo "✅ CLI interface: RESPONDS"

# 7. Run code quality checks
make lint 2>/dev/null || echo "⚠️  Code quality: ISSUES FOUND (check manually)"
echo "✅ Code quality: CHECKED"

echo "=== ALL VALIDATIONS COMPLETE ==="
```

**Expected Results**:
- Python version check: Instant
- Dependencies: 10-30 seconds
- Package structure: Instant
- CLI interface: 1-2 seconds
- Code quality: 20-40 seconds
- Total validation time: 30-60 seconds

### MANUAL VALIDATION REQUIREMENT
After making any changes, you MUST run these validation scenarios:

1. **Package Validation**:
```bash
# Verify package imports and basic functionality - takes 5 seconds
python -c "import saz_package.cli; print('CLI import: OK')"
python -c "import saz_package.client; print('Client import: OK')"
```

2. **Code Quality Validation**:
```bash
# Run all linting tools - takes 30 seconds
make lint
# Check for any critical issues
```

3. **CLI Interface Validation**:
```bash
# Test CLI responds to help - takes 2 seconds
python -m saz_package.cli --help
# Test basic commands don't crash
python -m saz_package.cli repo --help 2>/dev/null || echo "Help system works"
```

4. **Configuration Validation**:
```bash
# Verify PAT is available (don't print it)
if [ -n "$AZURE_DEVOPS_PAT" ]; then echo "PAT configured"; else echo "PAT missing"; fi
# Check Git remote
git remote -v
```

## Common Issues and Solutions

### Azure DevOps Authentication Issues
```bash
# PAT not configured
export AZURE_DEVOPS_PAT="your-token-here"

# PAT has insufficient permissions
# Solution: Create new PAT with these permissions:
# - Work Items: Read & Write
# - Build: Read & Execute
# - Code: Read
# - Project and Team: Read
# - Pull Request Threads: Read & Write
```

### Git Remote Configuration Issues
```bash
# Not in Azure DevOps repository
git remote -v  # Check current remotes

# Multiple remotes, SAZ uses 'azure' by default for development
# Configure specific remote if needed
export AZURE_DEVOPS_REMOTE="azure"
```

### Python Version Compatibility
```bash
# Check Python version
python --version

# SAZ requires Python 3.8+
# Upgrade Python if needed
pyenv install 3.11
pyenv global 3.11
```

### Network/Proxy Issues
```bash
# Azure DevOps API timeouts
export AZURE_DEVOPS_TIMEOUT="60"  # Increase timeout

# Corporate proxy blocking requests
export HTTP_PROXY="http://proxy.company.com:8080"
export HTTPS_PROXY="http://proxy.company.com:8080"
```

## Development Best Practices

### Code Style
- Follow PEP 8 with Black formatting (100 character line length)
- Use type hints for all function parameters and return values
- Write docstrings for all public functions and classes
- Use descriptive variable names

### Error Handling
- Always handle Azure DevOps API errors gracefully
- Provide meaningful error messages to users
- Log errors with appropriate log levels
- Don't expose sensitive information in error messages

### Testing
- Write integration tests for Azure DevOps API calls
- Mock external API calls in unit tests
- Test error conditions and edge cases
- Validate CLI argument parsing

### Documentation
- Keep this instructions file updated
- Document new CLI commands in instructions.md
- Update requirements.txt for new dependencies
- Maintain changelog for releases

## Architecture Guidelines

### Modular Design
- Keep CLI, client, and operation modules separate
- Use dependency injection for testability
- Avoid tight coupling between components
- Make components easily replaceable

### API Client Design
- Use requests library for HTTP calls
- Implement proper retry logic with exponential backoff
- Handle rate limiting gracefully
- Cache responses when appropriate

### CLI Design
- Use consistent command structure
- Provide helpful error messages
- Support both interactive and scripted usage
- Allow configuration through environment variables

## Performance Considerations

### API Call Optimization
- Batch operations when possible
- Use appropriate page sizes for list operations
- Cache frequently accessed data
- Implement connection pooling

### Memory Management
- Process large result sets in chunks
- Clean up temporary files
- Avoid loading entire API responses into memory
- Use generators for large data processing

### Error Recovery
- Implement retry logic for transient failures
- Handle network timeouts gracefully
- Provide clear feedback on long-running operations
- Allow operations to be resumed after interruptions