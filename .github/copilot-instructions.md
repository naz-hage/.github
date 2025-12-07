# Generic Project Templates - Copilot Development Guidelines

## Overview

Welcome to the generic project template system! This document provides comprehensive guidelines for AI-assisted development when using these templates in your projects. These templates provide standardized workflows, coding standards, and project management processes that work across multiple programming languages and DevOps platforms.

## Project Context

**Template System:**
- **Purpose**: Reusable templates for consistent development workflows
- **Platforms**: Azure DevOps, GitHub Issues
- **Languages**: Python, JavaScript/TypeScript, Java, C#, and others
- **Tools**: SDO CLI for unified work item and project management

**Key Components:**
- `project-config.yaml`: Generic project configuration
- `prompts/workflows/`: Standardized development workflow templates
- `prompts/actions/`: Action-specific workflow templates
- `validation/`: Configuration validation tools

## Development Guidelines

### Configuration Management

**Project Configuration:**
- Use `project-config.yaml` for all project-specific settings
- Keep sensitive information (PATs, tokens) in environment variables
- Validate configuration with `python validation/validate_configs.py`
- Reference config values in workflow prompts using bracket notation: `[FROM project-config.yaml: azure_devops.project]`

**Platform-Specific Settings:**
```yaml
# Azure DevOps configuration
project_management:
  platforms:
    azure_devops: true
    github: false

azure_devops:
  organization: "your-org"
  project: "YourProject"
  area_path: "your-org\\YourProject\\Development"
  default_iteration: "your-org\\YourProject\\Backlog"

# GitHub configuration
github:
  owner: "your-org"
  repository: "your-repo"
```

### Workflow Template Usage

**Generic Workflow Patterns:**
- Workflows are project-agnostic and use config references
- Replace bracketed placeholders with actual values when using
- Customize workflows for your team's specific processes
- Maintain consistency across similar projects

**Common Workflow Structure:**
```markdown
## Project: [FROM project-config.yaml: azure_devops.project]
## Area: [FROM project-config.yaml: azure_devops.area_path]
## Iteration: [FROM project-config.yaml: azure_devops.default_iteration]

### Description
[Brief description of the work]

### Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2

### Implementation Notes
[Technical details and approach]
```

### SDO CLI Integration

**Work Item Management:**
```bash
# Create work items
sdo workitem create --file-path .temp/pbi.md
sdo workitem create --file-path .temp/task.md

# List work items
sdo workitem list --type "Product Backlog Item"
sdo workitem list --type "Task"
```

**Platform Commands:**
```bash
# Set environment variables for authentication
# Azure DevOps
$env:AZURE_DEVOPS_PAT = "your-personal-access-token"

# GitHub (uses GitHub CLI authentication)
gh auth login

# Work item operations
sdo workitem create --type "Product Backlog Item" --title "Feature Title"
sdo workitem list --type "Task"
```

**Configuration Setup:**
- Copy `project-config.yaml` to your project
- Update organization, project, and repository values
- Set required environment variables
- Use GitHub CLI for GitHub authentication

### Code Quality Standards

**Language-Agnostic Practices:**
- Follow language-specific best practices
- Use consistent formatting tools (Black for Python, Prettier for JS, etc.)
- Include comprehensive error handling
- Write clear, maintainable code

**Documentation:**
- Use workflow templates for consistent documentation
- Document configuration changes
- Keep README files updated

### Template Customization

**Adapting for Your Project:**
- Copy templates to your `.github/` directory
- Modify workflow templates for your processes
- Update configuration with project-specific values

**Maintaining Consistency:**
- Use the same workflow structure across projects
- Reference configuration values instead of hardcoding
- Keep templates in sync across similar projects
- Document customizations for team knowledge

## When to Use Copilot Effectively

### Ideal Scenarios

**Template Customization:**
- Adapting workflow templates for specific projects
- Creating project-specific configuration examples
- Customizing validation scripts

**Workflow Creation:**
- Creating new workflow templates following established patterns
- Writing clear, actionable workflow steps
- Including appropriate acceptance criteria
- Adding implementation guidance

**Configuration Management:**
- Setting up project-config.yaml for different platforms
- Writing validation scripts for configuration
- Creating setup guides for different project types

### When to Be Cautious

**Platform-Specific Logic:**
- Azure DevOps vs GitHub API differences
- Authentication method variations
- Work item type differences between platforms

**Security Considerations:**
- Never commit sensitive information
- Use environment variables for tokens/PATs
- Validate permission requirements

**Complex Business Logic:**
- Custom workflow requirements
- Organization-specific processes
- Integration with proprietary tools

## Preferred Code Patterns

### Configuration Validation
```python
# Example validation script pattern
import yaml
import os
from typing import Dict, Any

def validate_config(config_path: str) -> bool:
    """Validate project configuration."""
    if not os.path.exists(config_path):
        print(f"Configuration file not found: {config_path}")
        return False

    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)

        # Validate required sections
        required_sections = ['project', 'project_management']
        for section in required_sections:
            if section not in config:
                print(f"Missing required section: {section}")
                return False

        # Validate platform configuration
        platforms = config.get('project_management', {}).get('platforms', {})
        if not any(platforms.values()):
            print("At least one platform must be enabled")
            return False

        return True

    except yaml.YAMLError as e:
        print(f"Invalid YAML syntax: {e}")
        return False
```

### Workflow Template Structure
```markdown
# [WORKFLOW TYPE] - [BRIEF DESCRIPTION]

## Overview
[Explain the purpose and scope of this workflow]

## Prerequisites
- [ ] Required tools installed
- [ ] Configuration validated
- [ ] Access permissions confirmed

## Process Steps

### Step 1: Preparation
[Detail preparation activities]

### Step 2: Implementation
[Detail implementation steps]

### Step 3: Validation
[Detail validation and testing]

### Step 4: Documentation
[Detail documentation requirements]

## Acceptance Criteria
- [ ] All process steps completed
- [ ] Validation passed
- [ ] Documentation updated
- [ ] Team review completed

## Common Issues
- **Issue**: [Common problem]
  **Solution**: [How to resolve]

## Related Templates
- [Link to related workflow templates]
- [Reference to code examples]
```

## Best Practices for Copilot Usage

### Template Development
- Follow established patterns from existing templates
- Include comprehensive error handling
- Provide clear, actionable guidance
- Test templates with real projects

### Configuration Management
- Use environment variables for sensitive data
- Validate configurations before use
- Document configuration requirements
- Provide migration guides for changes

### Documentation Standards
- Keep instructions current and accurate
- Include practical examples
- Document common pitfalls
- Provide troubleshooting guidance

## Common Patterns

### Work Item Creation
```markdown
## Product Backlog Item: [FEATURE TITLE]

## Description
[Clear, concise description of the feature]

## Business Value
[Why this feature matters to stakeholders]

## Acceptance Criteria
- [ ] Given [context], when [action], then [result]
- [ ] [Additional criteria]

## Technical Notes
[Implementation approach, dependencies, etc.]

## Story Points: [ESTIMATE]
## Priority: [HIGH/MEDIUM/LOW]
## Risk: [HIGH/MEDIUM/LOW]
```

### Task Breakdown
```markdown
## Task: [TASK TITLE]

## Parent Work Item: [PBI/TASK ID]

## Description
[Specific task description]

## Implementation Steps
1. [Step 1]
2. [Step 2]
3. [Step 3]

## Testing Requirements
- [ ] Unit tests written
- [ ] Integration tests passed
- [ ] Code review completed

## Time Estimate: [HOURS/DAYS]
```

### Code Review Checklist
```markdown
## Code Review Checklist

### Functionality
- [ ] Requirements implemented correctly
- [ ] Edge cases handled
- [ ] Error conditions tested

### Code Quality
- [ ] Code follows language standards
- [ ] Appropriate error handling
- [ ] Security considerations addressed

### Testing
- [ ] Unit tests included
- [ ] Tests pass
- [ ] Test coverage adequate

### Documentation
- [ ] Code documented
- [ ] README updated if needed
- [ ] Breaking changes documented
```

## Template Maintenance

### Updating Templates
- Review templates periodically for improvements
- Add new language/framework support
- Remove outdated patterns

### Version Control
- Keep templates in version control
- Document changes in commit messages
- Tag releases for template versions
- Maintain changelog for major updates

### Community Contributions
- Accept contributions following established patterns
- Review changes for consistency
- Test contributions across platforms
- Document new features clearly

Remember: These templates are designed to be generic and reusable. When using Copilot, focus on maintaining consistency with existing patterns while adapting to specific project needs. Always test templates in real project scenarios before relying on them for critical workflows.
