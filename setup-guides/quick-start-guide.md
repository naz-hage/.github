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

### Step 2: Configure Project

Edit `.temp/sdo-config.yaml` with your project details:

```yaml
project:
  name: "MyAwesomeProject"
  organization: "my-company"

project_management:
  platforms:
    azure_devops: true  # or github: true

azure_devops:
  organization: "my-company"
  project: "MyAwesomeProject"
  area_path: "my-company\\MyAwesomeProject\\Development"
  default_iteration: "my-company\\MyAwesomeProject\\Backlog"

tools:
  sdo_cli:
    temp_directory: ".temp"
```

### Step 3: Setup SDO CLI

```bash
# Build C# SDO (from ntools repository)
git clone https://github.com/naz-hage/ntools.git
cd ntools

# Build SDO CLI
.\dev-setup\install.ps1

# The executable is now available at:
# Windows: bin\Release\net10.0\sdo.exe
# Add to PATH or use the full path in commands

# Set environment variables for authentication
# Azure DevOps
$env:AZURE_DEVOPS_PAT = "your-personal-access-token"

# GitHub (uses GitHub CLI authentication)
gh auth login

# Test SDO connection
./bin/Release/net10.0/sdo wi list --type "Product Backlog Item"
```

### Step 4: Test Setup

```bash
# Test SDO connection
./bin/Release/net10.0/sdo wi list --assigned-to-me --top 3
```

**Done!** Your project now has comprehensive development workflows and guidelines.

## 📋 Detailed Setup Guide

### Prerequisites

- **Git** - Version control system
- **.NET 10.0 SDK** - For building SDO CLI
- **Access to project management platform** - Azure DevOps or GitHub

### Project Structure After Setup

```
your-project/
├── .github/
│   ├── sdo-config.yaml              # SDO configuration file
│   ├── copilot-instructions.md      # AI-assisted development guide
│   ├── prompts/
│   │   ├── README.md               # Workflow overview
│   │   ├── workflows/              # Development workflow templates
│   │   │   ├── workitem-start.md   # Complete work item start workflow
│   │   │   ├── testing.md
│   │   │   └── code-review.md
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
project_management:
  platforms:
    azure_devops: true
    github: false

azure_devops:
  organization: "your-org"
  project: "your-project"
  area_path: "your-project\\Team"
  default_iteration: "your-project\\Sprint 1"
```

#### GitHub Configuration

```yaml
project_management:
  platforms:
    azure_devops: false
    github: true

github:
  owner: "your-org"
  repository: "your-repo"
```

### Authentication Setup

#### Azure DevOps Personal Access Token (PAT)

**Required Permissions:**
- **Work Items: Read & Write** - Create, update, and query work items (PBIs, Tasks, Bugs)
- **Build: Read & Execute** - View build definitions and trigger builds
- **Code: Read** - Access to Git repositories and code
- **Project and Team: Read** - Access to project metadata and team information
- **Pull Request Threads: Read & Write** - Create and manage pull request discussions

**Setup Steps:**
1. Navigate to Azure DevOps → User Settings → Personal Access Tokens
2. Click "New Token"
3. Set name (e.g., "SDO CLI Tool")
4. Set organization and expiration
5. Select the required permissions listed above
6. Copy token and set as environment variable: `AZURE_DEVOPS_PAT`

#### GitHub Personal Access Token

**Required Scopes:**
- **repo** - Full access to repositories
- **workflow** - Update GitHub Action workflows

**Setup Steps:**
1. Go to GitHub → Settings → Developer settings → Personal access tokens
2. Click "Generate new token (classic)"
3. Select required scopes
4. Set expiration and description
5. Copy token and set as environment variable: `GITHUB_TOKEN`

#### Environment Variables

Set these in your shell profile or CI/CD environment:

```bash
# Azure DevOps
export AZURE_DEVOPS_PAT="your-pat-token-here"

# GitHub
export GITHUB_TOKEN="your-github-token-here"
```

### How Workflows Reference Config

All workflow prompts reference `sdo-config.yaml` for project-specific metadata. This makes workflows easily transferable between projects.

#### Pattern 1: Direct Reference
Workflows indicate where to find values:

```markdown
## Project: [FROM project-config.yaml: azure_devops.project]
## Area: [FROM project-config.yaml: azure_devops.area_path]
```

#### Pattern 2: Variable Placeholders
Use bracketed placeholders that should be replaced with config values:

```bash
sdo wi create --file-path [TEMP_DIRECTORY]/pbi.md
```

#### Pattern 3: Header Reference
Workflows include a reference at the top:

```markdown
> **Project Configuration**: See `.temp/sdo-config.yaml` for project-specific settings
```

### Configuration Examples

**PBI Template (project-agnostic):**
```markdown
## Project: [FROM sdo-config.yaml: azure_devops.project]
## Area: [FROM sdo-config.yaml: azure_devops.area_path]
## Iteration: [FROM sdo-config.yaml: azure_devops.default_iteration]
```

**Resolved for a specific project:**
```markdown
## Project: MyProject
## Area: MyOrg\Development
## Iteration: MyOrg\Sprint 1
```

**Tool Commands (project-agnostic):**
```bash
sdo wi create --file-path [TEMP_DIRECTORY]/pbi.md
```

**Resolved for a specific project:**
```bash
sdo wi create --file-path .temp/pbi.md
```

### Migration Guide

#### From Old Config Structure

If you have an existing `sdo-config.yaml` from the old structure:

1. **Backup your current config**
2. **Use the simplified SDO template** - the new `sdo-config.yaml` contains only essential SDO and platform settings
3. **Migrate only the required values** - most language-specific and quality tool settings have been removed as they're not referenced by prompts
4. **Test workflows** to ensure they work with the simplified config

#### Installation

```bash
# Build SDO CLI from ntools
git clone https://github.com/naz-hage/ntools.git
cd ntools/Sdo

# Build the C# version
dotnet build -c Release

# The executable is located at:
# bin\Release\net10.0\sdo.exe (Windows)
# bin/Release/net10.0/sdo (Linux/macOS)

# Add to PATH or use the full path for commands
```

### Authentication

#### Azure DevOps

```bash
# Set environment variable for PAT
$env:AZURE_DEVOPS_PAT = "your-personal-access-token"

# Test connection
sdo wi list --type "Product Backlog Item"
```

#### GitHub

```bash
# Authenticate with GitHub CLI
gh auth login

# Test connection
sdo wi list --type "Issue"
```

### Testing SDO Setup

```bash
# Test work item access
sdo wi list --top 5

# Test repository access
sdo repo ls
```

## 📋 Using the Templates

### Development Workflows

The templates provide guidance for common development activities:

1. **Task Implementation** - Breaking down user stories
2. **Code Review** - Structured review processes
3. **Testing** - Test-driven development
4. **PBI Implementation** - Product backlog item workflows

### Copilot Integration

The `copilot-instructions.md` file provides AI-assisted development guidance specific to your project configuration.

## 🔧 Customization

### Modifying Workflows

```bash
# Edit workflow templates
edit .github/prompts/workflows/workitem-start.md

# Add project-specific sections
# Follow the existing format and placeholders
```

### Updating Configuration

```bash
# Edit main configuration
edit .temp/sdo-config.yaml

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
# Test SDO integration
sdo wi create --file-path .temp/test-pbi.md

# Verify the work item was created
sdo wi list --filter "Title contains 'Test'"
```

## 📞 Getting Help

### Documentation Resources

- **[Workflow Guide](.github/prompts/workflows/README.md)** - Available workflow templates
- **[Configuration Deep Dive](#-configuration-deep-dive)** - Detailed configuration options in this guide

### Common Issues

**SDO Connection Issues**
```bash
# Check environment variables are set
echo $AZURE_DEVOPS_PAT  # Should show your PAT
echo $GITHUB_TOKEN      # Should show your token

# Test basic connectivity
sdo wi list --type "Product Backlog Item"
```

**"Config section not found"**
- Check that required sections are present in `sdo-config.yaml`
- Verify YAML syntax with: `python -c "import yaml; yaml.safe_load(open('sdo-config.yaml'))"`
- Ensure platform flags are set correctly in `project_management.platforms`

**"SDO command not found"**
- Verify SDO is installed: `sdo --version`
- Check PATH includes SDO executable
- Try `python -m sdo_package.cli` if using module installation

**"Authentication failed"**
- Verify environment variables are set correctly
- Check token permissions match the requirements listed above
- Test with SDO directly: `sdo wi list --type "Task"`

**"Platform not configured"**
- Set platform flag to `true` in `project_management.platforms`
- Configure the platform-specific section (azure_devops or github)
- Restart any running processes

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
python -c "import yaml; yaml.safe_load(open('.temp/sdo-config.yaml'))"
```

### Support Channels

- **Issues**: Open an issue in the template repository
- **Discussions**: Use GitHub Discussions for questions
- **Documentation**: Check the [full documentation](.github/prompts/README.md)

## 🛡️ Best Practices

### Configuration Management

1. **Version control**: Keep `sdo-config.yaml` in version control (but exclude secrets)
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

## 🎯 Next Steps

1. **Explore Workflows** - Try the different workflow templates
2. **Team Training** - Share the new workflows with your team
3. **Iterate** - Gather feedback and improve the setup

## 📋 Quick Reference

### Essential Commands

```bash
# SDO CLI
sdo wi list                    # List work items
sdo wi create --file-path pbi.md  # Create work item from markdown file
sdo repo ls                         # List repositories

# Validation
python .github/validation/validate_configs.py    # Validate config
python .github/validation/check_hardcoded_values.py  # Check for hardcoded values
```

### Key Files

- `.temp/sdo-config.yaml` - Main SDO configuration
- `.github/copilot-instructions.md` - AI development guide
- `.github/prompts/workflows/` - Development workflow templates

---

**Ready to build something amazing?** Your project is now equipped with professional development workflows and best practices!