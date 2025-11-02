# Quick Start Guide for New Projects

Get up and running with the generic template system in under 30 minutes.

## 🚀 5-Minute Setup

### Step 1: Copy Templates

```bash
# Clone the template repository
git clone https://github.com/naz-hage/.github.git temp-templates

# Copy templates to your new project
mkdir -p your-new-project/.github
cp -r temp-templates/.temp/* your-new-project/.github/

# Clean up
rm -rf temp-templates
```

### Step 2: Choose Your Language

```bash
cd your-new-project/.github

# For Python projects
cp project-config.python.yaml project-config.yaml

# For Node.js projects
cp project-config.nodejs.yaml project-config.yaml

# For .NET projects
cp project-config.dotnet.yaml project-config.yaml

# For Java projects
cp project-config.java.yaml project-config.yaml
```

### Step 3: Configure Project

Edit `project-config.yaml`:

```yaml
project:
  name: "MyAwesomeProject"
  organization: "my-company"
  description: "A brief description of what this project does"

platforms:
  azure_devops: true  # or github: true, jira: true

language: "python"    # python, javascript, java, dotnet
framework: "fastapi"  # your specific framework
```

### Step 4: Setup SAZ CLI

```bash
# Install SAZ CLI
pip install saz-cli

# Configure for your platform
saz config set platform azure-devops  # or github, jira
saz config set organization my-company
saz config set project MyAwesomeProject

# Authenticate
saz auth login
```

### Step 5: Test Setup

```bash
# Test SAZ connection
saz work-items list --top 3

# Validate configuration
python .github/validation/validate_configs.py
```

**Done!** Your project now has comprehensive development workflows and guidelines.

## 📋 Detailed Setup Guide

### Prerequisites

- **Git** - Version control system
- **Python 3.8+** - For SAZ CLI and validation scripts
- **Access to project management platform** - Azure DevOps, GitHub, or Jira

### Project Structure After Setup

```
your-project/
├── .github/
│   ├── project-config.yaml          # Your project configuration
│   ├── copilot-instructions.md      # AI-assisted development guide
│   ├── prompts/
│   │   ├── README.md               # Workflow overview
│   │   ├── CONFIG_USAGE.md         # Configuration guide
│   │   ├── workflows/              # Development workflow templates
│   │   │   ├── task-implementation.md
│   │   │   ├── testing.md
│   │   │   ├── code-review.md
│   │   │   └── pbi-implementation.md
│   │   └── examples/               # Code examples by language
│   │       ├── python/
│   │       ├── javascript/
│   │       ├── java/
│   │       └── dotnet/
│   └── PULL_REQUEST_TEMPLATE/
│       └── pull_request_template.md
├── src/                            # Your source code
├── tests/                          # Your tests
└── README.md                      # Project README
```

## ⚙️ Configuration Deep Dive

### Platform-Specific Settings

#### Azure DevOps Configuration

```yaml
platforms:
  azure_devops: true
  github: false
  jira: false

azure_devops:
  organization: "your-org"
  project: "your-project"
  area_path: "your-project\\Team"
  iteration_path: "your-project\\Sprint 1"
```

#### GitHub Configuration

```yaml
platforms:
  azure_devops: false
  github: true
  jira: false

github:
  organization: "your-org"
  repository: "your-repo"
  default_labels: ["enhancement", "bug"]
```

#### Jira Configuration

```yaml
platforms:
  azure_devops: false
  github: false
  jira: true

jira:
  server_url: "https://your-company.atlassian.net"
  project_key: "PROJ"
  default_issue_type: "Story"
```

### Language-Specific Settings

#### Python Project

```yaml
language: "python"
framework: "fastapi"

python:
  version: "3.9"
  package_manager: "poetry"  # or pip, pipenv
  test_framework: "pytest"
  linter: "flake8"
  formatter: "black"
```

#### Node.js Project

```yaml
language: "javascript"
framework: "express"

javascript:
  runtime: "node"
  version: "18"
  package_manager: "npm"  # or yarn, pnpm
  test_framework: "jest"
  linter: "eslint"
  typescript: true
```

#### .NET Project

```yaml
language: "dotnet"
framework: "aspnetcore"

dotnet:
  version: "7.0"
  project_type: "webapi"  # webapi, webapp, console
  test_framework: "xunit"
  orm: "efcore"
```

#### Java Project

```yaml
language: "java"
framework: "springboot"

java:
  version: "17"
  build_tool: "maven"  # or gradle
  spring_boot_version: "3.0"
  test_framework: "junit5"
```

## 🛠️ SAZ CLI Setup

### Installation

```bash
# Install from PyPI
pip install saz-cli

# Or install from source
git clone https://github.com/naz-hage/saz.git
cd saz
pip install -e .
```

### Authentication

#### Azure DevOps

```bash
# Set platform
saz config set platform azure-devops

# Set organization and project
saz config set organization your-org
saz config set project your-project

# Authenticate (opens browser)
saz auth login
```

#### GitHub

```bash
# Set platform
saz config set platform github

# Set organization and repository
saz config set organization your-org
saz config set repository your-repo

# Authenticate with personal access token
saz auth login --token your-github-token
```

#### Jira

```bash
# Set platform
saz config set platform jira

# Set server and project
saz config set server https://your-company.atlassian.net
saz config set project PROJ

# Authenticate
saz auth login
```

### Testing SAZ Setup

```bash
# Check configuration
saz config list

# Test work item access
saz work-items list --top 5

# Test project info
saz projects show
```

## 📋 Using the Templates

### Development Workflows

The templates provide guidance for common development activities:

1. **Task Implementation** - Breaking down user stories
2. **Code Review** - Structured review processes
3. **Testing** - Test-driven development
4. **PBI Implementation** - Product backlog item workflows

### Code Examples

Language-specific examples are available in `.github/prompts/examples/{language}/`:

- **API Client Patterns** - HTTP clients with retry logic
- **Testing Best Practices** - Comprehensive testing approaches
- **Error Handling** - Framework-neutral exception handling
- **Architecture Patterns** - Clean architecture, DDD, CQRS

### Copilot Integration

The `copilot-instructions.md` file provides AI-assisted development guidance specific to your project configuration.

## 🔧 Customization

### Modifying Workflows

```bash
# Edit workflow templates
edit .github/prompts/workflows/task-implementation.md

# Add project-specific sections
# Follow the existing format and placeholders
```

### Adding Code Examples

```bash
# Create new example
edit .github/prompts/examples/python/custom-pattern.md

# Follow the established format
# Use configuration placeholders where appropriate
```

### Updating Configuration

```bash
# Edit main configuration
edit .github/project-config.yaml

# Validate changes
python .github/validation/validate_configs.py
```

## 🧪 Validation and Testing

### Configuration Validation

```bash
# Validate configuration
python .github/validation/validate_configs.py

# Check for issues
python .github/validation/check_hardcoded_values.py
```

### Testing Workflows

```bash
# Test SAZ integration
saz work-items create --title "Test work item" --type "Task"

# Verify the work item was created
saz work-items list --filter "Title contains 'Test'"
```

### Example Testing

```bash
# Test Python examples
cd your-project
python -c "
# Test API client example
from .github.prompts.examples.python.api_client_patterns import APIClient
# Basic functionality test
"
```

## 📞 Getting Help

### Documentation Resources

- **[Configuration Guide](.github/prompts/CONFIG_USAGE.md)** - Detailed configuration options
- **[Workflow Guide](.github/prompts/workflows/README.md)** - Available workflow templates
- **[Migration Guide](setup-guides/migration-guide.md)** - For existing projects

### Common Issues

**SAZ Connection Issues**
```bash
# Check configuration
saz config list

# Re-authenticate
saz auth login

# Test basic connectivity
saz projects list
```

**Configuration Validation Errors**
```bash
# Run with verbose output
python .github/validation/validate_configs.py --verbose

# Check specific error messages
```

**Template Not Working**
```bash
# Verify file structure
find .github/ -name "*.md" -o -name "*.yaml" | sort

# Check configuration syntax
python -c "import yaml; yaml.safe_load(open('.github/project-config.yaml'))"
```

### Support Channels

- **Issues**: Open an issue in the template repository
- **Discussions**: Use GitHub Discussions for questions
- **Documentation**: Check the [full documentation](.github/prompts/README.md)

## 🎯 Next Steps

1. **Explore Workflows** - Try the different workflow templates
2. **Customize Examples** - Adapt code examples for your specific frameworks
3. **Team Training** - Share the new workflows with your team
4. **Iterate** - Gather feedback and improve the setup

## 📋 Quick Reference

### Essential Commands

```bash
# SAZ CLI
saz work-items list                    # List work items
saz work-items create --title "Title"  # Create work item
saz branches create feature/123       # Create feature branch

# Validation
python .github/validation/validate_configs.py    # Validate config
python .github/validation/check_hardcoded_values.py  # Check for hardcoded values
```

### Key Files

- `.github/project-config.yaml` - Main configuration
- `.github/copilot-instructions.md` - AI development guide
- `.github/prompts/workflows/` - Development workflow templates
- `.github/prompts/examples/` - Code examples by language

---

**Ready to build something amazing?** Your project is now equipped with professional development workflows and best practices!