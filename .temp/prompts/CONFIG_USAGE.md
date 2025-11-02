# Using Project Configuration in Workflows

## Overview

All workflow prompts in this directory are **project-agnostic** and reference `project-config.yaml` for project-specific metadata. This makes workflows easily transferable between projects.

## Configuration File

**Location**: `.github/project-config.yaml`

This YAML file contains all project-specific metadata:
- Project management platforms (Azure DevOps, GitHub, Jira)
- Repository details (owner, name, remotes)
- Tool configurations (SAZ CLI, language-specific tools)
- Work item types, states, and story point scales
- Code style settings (formatters, linters)
- Authentication requirements
- Project type specific settings

## Quick Start

### For New Projects

1. **Copy a template**: Choose the appropriate template for your project type:
   - `project-config.python.yaml` - Python projects
   - `project-config.nodejs.yaml` - Node.js projects
   - `project-config.dotnet.yaml` - .NET projects

2. **Customize values**: Replace placeholder values with your project specifics

3. **Configure SAZ**: Set up SAZ tool for your platforms (Azure DevOps, GitHub, etc.)

### For Existing Projects

1. **Migrate from old config**: Use the migration guide below
2. **Update workflows**: Ensure workflows reference the new config structure
3. **Test configuration**: Validate that all tools work with new config

## Configuration Structure

### Core Sections

- **`project`** - Basic project information (name, language, version)
- **`project_management`** - Which platforms/tools to use
- **`repository`** - Git repository settings
- **`tools`** - Tool configurations (SAZ, CLI tools)
- **`development`** - Language-specific development settings
- **`authentication`** - Platform authentication settings
- **`workflows`** - Work item states and story points
- **`project_type`** - Project-specific settings

### Platform-Specific Sections

- **`azure_devops`** - Azure DevOps organization settings
  - `organization` - Organization name
  - `organization_url` - Full Azure DevOps URL
  - `project` - Project name
  - `project_id` - Project GUID
  - `area_path` - Default area path
  - `default_iteration` - Default iteration path
  - `process_template` - Process template (Agile, Scrum, etc.)
  - `default_team` - Default team name
  - `team_project` - Team project name (if different from project)

## Authentication Configuration

### Azure DevOps Personal Access Token (PAT)

**Required Permissions:**
- **Work Items: Read & Write** - Create, update, and query work items (PBIs, Tasks, Bugs)
- **Build: Read & Execute** - View build definitions and trigger builds
- **Code: Read** - Access to Git repositories and code
- **Project and Team: Read** - Access to project metadata and team information
- **Pull Request Threads: Read & Write** - Create and manage pull request discussions

**Setup Steps:**
1. Navigate to Azure DevOps → User Settings → Personal Access Tokens
2. Click "New Token"
3. Set name (e.g., "SAZ CLI Tool")
4. Set organization and expiration
5. Select the required permissions listed above
6. Copy token and set as environment variable: `AZURE_DEVOPS_PAT`

### GitHub Personal Access Token

**Required Scopes:**
- **repo** - Full access to repositories
- **workflow** - Update GitHub Action workflows

**Setup Steps:**
1. Go to GitHub → Settings → Developer settings → Personal access tokens
2. Click "Generate new token (classic)"
3. Select required scopes
4. Set expiration and description
5. Copy token and set as environment variable: `GITHUB_TOKEN`

### Environment Variables

Set these in your shell profile or CI/CD environment:

```bash
# Azure DevOps
export AZURE_DEVOPS_PAT="your-pat-token-here"

# GitHub
export GITHUB_TOKEN="your-github-token-here"

# Jira (if using)
export JIRA_TOKEN="your-jira-token-here"
```

## How Workflows Reference Config

### Pattern 1: Direct Reference
Workflows indicate where to find values:

```markdown
## Project: [FROM project-config.yaml: azure_devops.project]
## Area: [FROM project-config.yaml: azure_devops.area_path]
```

### Pattern 2: Variable Placeholders
Use bracketed placeholders that should be replaced with config values:

```bash
saz workitem create --file-path [TEMP_DIRECTORY]/pbi.md
```

### Pattern 3: Header Reference
Workflows include a reference at the top:

```markdown
> **Project Configuration**: See `.github/project-config.yaml` for project-specific settings
```

## Examples

### Example 1: PBI Template
**In workflow prompt (project-agnostic):**
```markdown
## Project: [FROM project-config.yaml: azure_devops.project]
## Area: [FROM project-config.yaml: azure_devops.area_path]
## Iteration: [FROM project-config.yaml: azure_devops.default_iteration]
```

**Resolved for a project:**
```markdown
## Project: MyProject
## Area: MyOrg\Development
## Iteration: MyOrg\Sprint 1
```

### Example 2: Tool Commands
**In workflow prompt (project-agnostic):**
```bash
saz workitem create --file-path [TEMP_DIRECTORY]/pbi.md
```

**Resolved for a project:**
```bash
saz workitem create --file-path .temp/pbi.md
```

### Example 3: Language-Specific Commands
**In workflow prompt (project-agnostic):**
```bash
[QUALITY_TOOLS[0]]  # Run first quality tool
[QUALITY_TOOLS[1]]  # Run second quality tool
```

**Resolved for Python project:**
```bash
make lint
make format
```

**Resolved for Node.js project:**
```bash
npm run lint
npm run format
```

## Project Type Templates

### Python Projects
Use `project-config.python.yaml` for:
- CLI tools
- APIs (FastAPI, Flask)
- Data science projects
- Libraries

**Key settings:**
- Python version requirements
- Testing framework (pytest)
- Code formatters (black, isort)
- Linters (flake8, pylint, mypy)

### Node.js Projects
Use `project-config.nodejs.yaml` for:
- Web applications (React, Vue, Angular)
- APIs (Express, Fastify)
- CLI tools
- Serverless functions

**Key settings:**
- Node.js version
- Package manager (npm, yarn, pnpm)
- Testing framework (Jest, Vitest)
- Code formatters (Prettier, ESLint)

### .NET Projects
Use `project-config.dotnet.yaml` for:
- Web APIs (ASP.NET Core)
- Web applications (Blazor, MVC)
- Libraries
- Console applications

**Key settings:**
- .NET version and target framework
- Testing framework (xUnit, NUnit)
- Code formatters (dotnet-format)
- Linters (StyleCop, Roslynator)

## Migration Guide

### From Old Config Structure

If you have an existing `project-config.yaml` from the old structure:

1. **Backup your current config**
2. **Choose the appropriate template** based on your project type
3. **Migrate values** from your old config to the new structure
4. **Update any custom sections** you may have added
5. **Test workflows** to ensure they work with the new config

### Value Mapping

| Old Path | New Path | Notes |
|----------|----------|-------|
| `project.name` | `project.name` | Same |
| `azure_devops.*` | `azure_devops.*` | Same |
| `tools.saz_cli.*` | `tools.saz_cli.*` | Same |
| `development.code_style.*` | `development.language_config.python.*` | Language-specific |
| `quality_tools` | `development.quality_tools` | Moved |

### Breaking Changes

- **Language-specific settings** moved to `development.language_config.[language]`
- **Quality tools** moved to `development.quality_tools`
- **New required sections**: `project_management`, `project_type`
- **Platform flags**: Must explicitly enable/disable platforms

## SAZ Tool Configuration

### Setting up SAZ for Multiple Platforms

1. **Install SAZ**:
```bash
pip install saz
# or
pip install -e .  # if developing SAZ
```

2. **Configure for Azure DevOps**:
```bash
saz config set azure_devops.organization "myorg"
saz config set azure_devops.project "MyProject"
saz config set azure_devops.pat "$AZURE_DEVOPS_PAT"
```

3. **Configure for GitHub**:
```bash
saz config set github.owner "myorg"
saz config set github.token "$GITHUB_TOKEN"
```

4. **Test configuration**:
```bash
saz repo list  # Test Azure DevOps
saz issue list  # Test GitHub
```

### SAZ Command Mapping

| Generic Action | SAZ Command | Alternative |
|----------------|-------------|-------------|
| Create work item | `saz workitem create` | `az boards work-item create` |
| List repositories | `saz repo list` | `gh repo list` |
| Create PR | `saz pr create` | `gh pr create` |
| Run pipeline | `saz pipeline run` | `az pipelines run` |

## Advanced Configuration

### Conditional Logic

The configuration supports conditional sections based on enabled platforms:

```yaml
# Only used if azure_devops: true
azure_devops:
  organization: "myorg"
  # ... other settings

# Only used if github: true
github:
  organization: "myorg"
  # ... other settings
```

### Custom Work Item Types

Add custom work item types beyond the defaults:

```yaml
work_items:
  types:
    - PBI
    - Bug
    - Task
    - Spike
    - Epic      # Custom type
    - Story     # Custom type
```

### Environment-Specific Overrides

Use environment variables for sensitive or environment-specific values:

```yaml
authentication:
  azure_devops:
    env_var: "${AZURE_DEVOPS_PAT:-DEFAULT_PAT}"
  github:
    env_var: "${GITHUB_TOKEN:-DEFAULT_TOKEN}"
```

## Troubleshooting

### Common Issues

**"Config section not found"**
- Check that required sections are present
- Verify YAML syntax
- Ensure platform flags are set correctly

**"SAZ command not found"**
- Verify SAZ is installed: `saz --version`
- Check PATH includes SAZ executable
- Try `python -m saz_package.cli` if using module

**"Authentication failed"**
- Verify environment variables are set
- Check token permissions
- Test with SAZ directly: `saz auth test`

**"Platform not configured"**
- Set platform flag to `true` in `project_management.platforms`
- Configure the platform-specific section
- Restart any running processes

### Validation

Run these commands to validate your configuration:

```bash
# Check YAML syntax
python -c "import yaml; yaml.safe_load(open('project-config.yaml'))"

# Test SAZ configuration
saz config list

# Validate required sections exist
python -c "
import yaml
config = yaml.safe_load(open('project-config.yaml'))
required = ['project', 'project_management', 'tools']
missing = [k for k in required if k not in config]
if missing:
    print(f'Missing required sections: {missing}')
else:
    print('Configuration is valid')
"
```

## Best Practices

### Configuration Management

1. **Version control**: Keep `project-config.yaml` in version control (but exclude secrets)
2. **Environment separation**: Use different configs for dev/staging/prod
3. **Documentation**: Comment complex configurations
4. **Validation**: Test configs before committing

### Security

1. **Never commit secrets**: Use environment variables for tokens/PATs
2. **Minimal permissions**: Grant only required permissions
3. **Token rotation**: Regularly rotate authentication tokens
4. **Access control**: Limit who can modify configuration

### Maintenance

1. **Regular updates**: Update tool versions and configurations
2. **Platform changes**: Update config when moving platforms
3. **Team alignment**: Ensure team agrees on configuration standards
4. **Documentation**: Keep configuration documentation current

## See Also

- **`project-config.yaml`** - Main configuration file
- **`project-config.*.yaml`** - Project type templates
- **`copilot-instructions.md`** - Development guidelines
- **Workflow files** - How configs are used in practice

**Resolved for SAZ project:**
```markdown
## Project: Proto
## Area: Proto\Warriors
## Iteration: Proto\Backlog
```

### Example 2: Tool Paths
**In workflow prompt (project-agnostic):**
```bash
saz workitem create --file-path [TEMP_DIRECTORY]/pbi.md
```

**Resolved for SAZ project:**
```bash
saz workitem create --file-path .temp/pbi.md
```

### Example 3: Story Points Scale
**In workflow prompt (project-agnostic):**
```markdown
Story points scale (see `project-config.yaml` for definitions):
- 1 point: <1 day
- 2 points: 1-2 days
- 3 points: 2-3 days
```

**Config defines the scale:**
```yaml
workflows:
  story_points:
    scale:
      1: "<1 day"
      2: "1-2 days"
      3: "2-3 days"
```

## Making Workflows Project-Agnostic

### ❌ Avoid Hardcoded Values:
```markdown
## Project: Proto
## Area: Proto\Warriors
python \source\ntools\atools\add-issue.py .temp/pbi.md
```

### ✅ Use Config References:
```markdown
## Project: [FROM project-config.yaml: azure_devops.project]
## Area: [FROM project-config.yaml: azure_devops.area_path]
saz workitem create --file-path [TEMP_DIRECTORY]/pbi.md
```

## Transferring Workflows to Other Projects

To use these workflows in a new project:

1. **Copy the workflow files** to the new project
2. **Create a new `project-config.yaml`** with that project's specific values
3. **Workflows automatically adapt** to the new project's configuration

## Config Sections Reference

### Key Sections in project-config.yaml:

- **`project`**: Project name, description, language
- **`azure_devops`**: Organization, project, area paths, iterations
- **`repository`**: Name, owner, branches, remotes
- **`work_items`**: Types, states, labels, assignees
- **`tools`**: Script paths, CLI commands, directories
- **`development`**: Code style, formatters, linters, testing
- **`authentication`**: Auth methods, environment variables, permissions
- **`workflows`**: Story points, states, PR settings

## Benefits

1. **Reusability** - Copy workflows to any project with minimal changes
2. **Consistency** - All projects follow the same process structure
3. **Maintainability** - Update processes in one place
4. **Clarity** - Project-specific values clearly separated from process
5. **Automation** - Easy to parse config programmatically

## Migration to Public Repo

When ready to move workflows to a public repository:

1. Workflows stay as-is (already project-agnostic)
2. Each project creates its own `project-config.yaml`
3. Projects reference public workflow repo + local config
4. No workflow changes needed - just config files

## See Also

- **`project-config.yaml`** - Project-specific configuration
- **`copilot-instructions.md`** - Project-specific development guidelines
- **`workflows/README.md`** - Workflow directory overview
