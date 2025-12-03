# .github
Repository Template
# .github - Generic Project Templates

A comprehensive template system for project management workflows, development guidelines, and best practices that can be used across multiple programming languages and frameworks.

## 🎯 Overview

This repository contains **generic, reusable templates** that projects can copy to their `.github/` directory to establish consistent development workflows, coding standards, and project management processes. The templates are designed to work with multiple platforms (Azure DevOps, GitHub) and programming languages (Python, JavaScript/TypeScript, Java, C#).

### Key Features

- **🔧 SDO CLI Integration**: Uses [SDO](https://github.com/naz-hage/sdo) as the primary CLI tool for unified project management across platforms
- **🌍 Multi-Language Support**: Examples and patterns for Python, JavaScript/TypeScript, Java, and C#
- **⚙️ Configurable**: All project-specific values are managed through configuration files
- **📋 Generic Workflows**: Tool-agnostic workflows that work with any project management platform
- **🚀 Easy Adoption**: Simple copy-and-configure setup for new projects

## 📁 Repository Structure

```
.github/                           # GitHub templates and workflows
├── ISSUE_TEMPLATE/                # Issue templates
├── PULL_REQUEST_TEMPLATE/         # Pull request template
├── workflows/                     # GitHub Actions workflows
└── .temp/                         # Generic templates (copy to project .github/)
    ├── project-config.yaml         # Generic configuration template
    ├── copilot-instructions.md     # GitHub Copilot instructions template
    ├── prompts/                    # Workflow and development guides
    │   ├── README.md              # Generic workflow overview
    │   ├── workflows/             # Tool-agnostic workflow templates
    │   ├── actions/               # Action-specific workflow templates
    │   └── examples/              # Multi-language code examples
    │       ├── {language}/        # Language-specific implementations
    └── PULL_REQUEST_TEMPLATE/     # Generic PR template
setup-guides/                      # Project setup and migration guides
validation/                        # Configuration validation tools
README.md                          # This file
```

## 🚀 Quick Start

### For New Projects

1. **Copy Templates**
   ```bash
   # Copy the .temp directory contents to your project's .github directory
   cp -r .github/.temp/* your-project/.github/
   ```

2. **Configure Project**
   ```bash
   # Edit project-config.yaml with your project details
   cd your-project/.github
   # The config is generic and works for all languages
   # Edit project-config.yaml with your specific values
   ```

3. **Setup SDO CLI**
   ```bash
   # Install SDO CLI (if not already installed)
   pip install sdo-cli

   # Configure SDO for your platform
   sdo config set platform azure-devops  # or github, jira
   sdo config set organization your-org
   sdo config set project your-project
   ```

4. **Customize as Needed**
   - Modify workflow templates in `prompts/workflows/`
   - Update examples in `prompts/examples/`
   - Adjust Copilot instructions in `copilot-instructions.md`

### For Existing Projects

Follow the [Quick Start Guide](setup-guides/quick-start-guide.md) to adopt these templates in existing projects.

## ⚙️ Configuration

### Project Configuration

The `project-config.yaml` file contains all project-specific settings:

```yaml
# Project Information
project:
  name: "MyProject"
  organization: "my-org"

# Platform Configuration
project_management:
  platforms:
    azure_devops: true
    github: false

# Azure DevOps settings (if enabled)
azure_devops:
  organization: "my-org"
  project: "MyProject"
  area_path: "my-org\\MyProject\\Development"
  default_iteration: "my-org\\MyProject\\Backlog"

# Tool Configuration
tools:
  sdo_cli:
    temp_directory: ".temp"
```

### Configuration Template

The configuration is now **generic** and works for all project types:

- `project-config.yaml` - Generic project configuration (works for all languages)

## 🛠️ Supported Platforms & Languages

### Project Management Platforms
- **Azure DevOps** (primary, via SDO CLI)
- **GitHub Issues**

### Programming Languages
- **Python** - Web APIs, data processing, CLI tools
- **JavaScript/TypeScript** - React, Node.js, Express
- **Java** - Spring Boot, enterprise applications
- **C#** - ASP.NET Core, domain-driven design

### Frameworks & Patterns
- **API Development**: REST, GraphQL, microservices
- **Testing**: Unit tests, integration tests, end-to-end tests
- **Error Handling**: Retry patterns, circuit breakers, structured logging
- **Architecture**: Clean architecture, domain-driven design, CQRS

## 📋 Available Templates

### Workflow Templates
- **Task Implementation** - Breaking down user stories into tasks
- **Code Review** - Structured code review processes
- **Testing** - Test-driven development guidelines
- **PBI Implementation** - Product backlog item workflows

### Code Examples
- **API Client Patterns** - HTTP clients with retry logic
- **Error Handling** - Framework-neutral exception handling
- **Testing Best Practices** - Comprehensive testing patterns
- **Component Architecture** - Reusable component patterns

### Development Guides
- **Daily Standup Reference** - Effective standup meeting formats
- **Copilot Best Practices** - AI-assisted development guidelines
- **Branching Strategy** - Git workflow recommendations

## 🔧 SDO CLI Integration

[SDO](https://github.com/naz-hage/sdo) is the recommended CLI tool for project management operations. It provides a unified interface for:

- **Work Item Management**: Create, update, query work items
- **Sprint Planning**: Manage sprints and capacity
- **Branch Management**: Create feature branches
- **Pull Request Management**: Create and manage PRs

### SDO Configuration

```bash
# Configure for Azure DevOps
sdo config set platform azure-devops
sdo config set organization your-org
sdo config set project your-project
sdo auth login

# Configure for GitHub
sdo config set platform github
sdo config set organization your-org
sdo config set repository your-repo
```

## 📖 Documentation

- **[Quick Start Guide](setup-guides/quick-start-guide.md)** - Complete setup and configuration guide
- **[Workflow Guide](.temp/prompts/workflows/README.md)** - Available workflow templates
- **[Setup Guides](setup-guides/)** - Project setup and migration guides
- **[Validation Tools](validation/)** - Configuration validation scripts

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run validation scripts: `python validation/validate_configs.py`
5. Test with different project types
6. Submit a pull request

### Adding New Language Support

1. Create language directory: `.temp/prompts/examples/{language}/`
2. Add 3 core files: patterns, testing, error-handling
3. Create config template: `project-config.{language}.yaml`
4. Update Quick Start Guide with new language examples
5. Test with sample project

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [SDO CLI](https://github.com/naz-hage/sdo) - Unified project management CLI
- Community contributors for language-specific examples
- Open source projects that inspired these patterns

---

**Ready to get started?** Copy the templates to your project and configure for your specific needs!
