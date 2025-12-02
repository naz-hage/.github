# Migration Guide for Existing Projects

This guide helps existing projects adopt the generic template system while preserving their current workflows and configurations.

## 📋 Migration Overview

The migration process involves:
1. **Assessment** - Evaluate current setup
2. **Backup** - Preserve existing configurations
3. **Copy Templates** - Add generic templates
4. **Configuration** - Set up project-specific values
5. **Customization** - Adapt templates as needed
6. **Testing** - Validate the new setup

## 🔍 Step 1: Assess Current Setup

### Check Existing Files

First, inventory your current `.github/` directory:

```bash
# List current .github contents
ls -la .github/

# Check for existing workflow files
find .github/ -name "*.md" -o -name "*.yaml" -o -name "*.yml" | head -20

# Look for existing configurations
find .github/ -name "*config*" -o -name "*settings*"
```

### Identify Key Elements

- **Project Management Tool**: Azure DevOps, GitHub Issues, Jira, or other
- **Primary Language**: Python, JavaScript, Java, C#, or other
- **Existing Workflows**: Custom scripts, GitHub Actions, or manual processes
- **Configuration Files**: Any existing config files to preserve

## 💾 Step 2: Backup Existing Setup

### Create Backup Directory

```bash
# Create backup directory
mkdir -p .github/backup/$(date +%Y%m%d)

# Backup existing files
cp -r .github/* .github/backup/$(date +%Y%m%d)/ 2>/dev/null || true

# List what was backed up
ls -la .github/backup/$(date +%Y%m%d)/
```

### Document Current Workflows

Create a document listing your current processes:

```markdown
# Current Project Workflows

## Work Item Management
- Tool: [Azure DevOps/GitHub/Jira]
- Process: [Describe current process]

## Code Review
- Process: [Describe current process]

## Testing
- Framework: [pytest/jest/junit/xunit]
- Process: [Describe current process]

## Deployment
- Process: [Describe current process]
```

## 📁 Step 3: Copy Generic Templates

### Copy Template Files

```bash
# Copy from the template repository
# Assuming you have access to the .github template repo
cp -r path/to/template/repo/.temp/* .github/

# Or if using git clone
git clone https://github.com/naz-hage/.github.git temp-templates
cp -r temp-templates/.temp/* .github/
rm -rf temp-templates
```

### Verify Copy

```bash
# Check that templates were copied
ls -la .github/

# Should see:
# project-config.yaml
# project-config.*.yaml (language templates)
# copilot-instructions.md
# prompts/
# PULL_REQUEST_TEMPLATE/
```

## ⚙️ Step 4: Configure Project Settings

### Choose Base Configuration

Select the appropriate language template:

```bash
# For Python projects
cp .github/project-config.python.yaml .github/project-config.yaml

# For Node.js projects
cp .github/project-config.nodejs.yaml .github/project-config.yaml

# For .NET projects
cp .github/project-config.dotnet.yaml .github/project-config.yaml
```

### Edit Configuration

Update `project-config.yaml` with your project details:

```yaml
# Basic project information
project:
  name: "YourProjectName"
  organization: "your-org"
  description: "Brief project description"

# Platform settings
platforms:
  azure_devops: true    # Set to true if using Azure DevOps
  github: false         # Set to true if using GitHub Issues
  jira: false          # Set to true if using Jira

# Language and framework
language: "python"      # python, javascript, java, dotnet
framework: "fastapi"    # Your specific framework

# Tool configuration
tools:
  cli: "sdo"           # Primary CLI tool (keep as 'sdo')
  test_runner: "pytest" # Your test runner
  linter: "flake8"     # Your linter
```

### Configure SDO CLI

Set up SDO for your platform:

```bash
# Install SDO if not already installed
pip install sdo-cli

# Configure for your platform
# For Azure DevOps:
sdo config set platform azure-devops
sdo config set organization your-org-name
sdo config set project your-project-name

# For GitHub:
sdo config set platform github
sdo config set organization your-org-name
sdo config set repository your-repo-name

# Authenticate
sdo auth login
```

## 🎨 Step 5: Customize Templates

### Update Workflow Templates

Modify workflow files to match your processes:

```bash
# Edit workflow templates
edit .github/prompts/workflows/task-implementation.md
edit .github/prompts/workflows/testing.md
edit .github/prompts/workflows/code-review.md
```

### Adapt Code Examples

Update examples for your specific frameworks:

```bash
# Choose relevant examples
cp .github/prompts/examples/python/api-client-patterns.md .
cp .github/prompts/examples/python/testing-best-practices.md .

# Edit for your specific needs
edit api-client-patterns.md
```

### Update Copilot Instructions

Customize the Copilot instructions:

```bash
edit .github/copilot-instructions.md
```

## 🧪 Step 6: Test and Validate

### Run Validation Scripts

Use the validation tools to check your setup:

```bash
# Run configuration validator
python .github/validation/validate_configs.py

# Check for hardcoded values
python .github/validation/check_hardcoded_values.py
```

### Test Workflows

Test key workflows with your new setup:

```bash
# Test SDO connection
sdo work-items list --top 5

# Test a workflow (if applicable)
# Follow the prompts in your customized workflow files
```

### Validate Examples

Test that code examples work in your environment:

```bash
# Test a simple example
cd your-project
python -c "
import sys
sys.path.append('.github/prompts/examples/python')
# Test import and basic functionality
"
```

## 🔄 Step 7: Gradual Rollout

### Phase Implementation

Consider rolling out changes gradually:

1. **Week 1**: Configuration and basic setup
2. **Week 2**: Test workflows with small team
3. **Week 3**: Roll out to full team
4. **Week 4**: Gather feedback and iterate

### Monitor and Adjust

- **Track Issues**: Monitor for any workflow disruptions
- **Gather Feedback**: Ask team for input on new processes
- **Iterate**: Make adjustments based on real usage

## 🆘 Troubleshooting

### Common Issues

**SDO Configuration Issues**
```bash
# Check SDO configuration
sdo config list

# Re-authenticate if needed
sdo auth login

# Test connection
sdo work-items list --top 1
```

**Template Conflicts**
```bash
# If you have conflicts with existing files
# Check what's different
diff .github/backup/$(date +%Y%m%d)/existing-file.md .github/prompts/workflows/existing-file.md

# Merge manually or choose which version to keep
```

**Configuration Validation Errors**
```bash
# Run validator with verbose output
python .github/validation/validate_configs.py --verbose

# Check the validation output for specific issues
```

### Getting Help

- **Documentation**: Check [CONFIG_USAGE.md](.github/prompts/CONFIG_USAGE.md)
- **Examples**: Look at [test-configs](.github/test-configs/) for working examples
- **Issues**: Open an issue in the template repository

## 📋 Migration Checklist

- [ ] Assessed current setup
- [ ] Created backup of existing files
- [ ] Copied generic templates
- [ ] Configured project settings
- [ ] Set up SDO CLI
- [ ] Customized templates for project needs
- [ ] Tested configuration and workflows
- [ ] Validated with team
- [ ] Documented any customizations

## 🎯 Success Criteria

- [ ] All team members can use the new workflows
- [ ] SDO CLI is properly configured and working
- [ ] Configuration validation passes
- [ ] No disruption to existing development processes
- [ ] Team is comfortable with new templates

## 📞 Support

If you encounter issues during migration:

1. Check the [troubleshooting section](#-troubleshooting) above
2. Review the [configuration guide](.github/prompts/CONFIG_USAGE.md)
3. Open an issue in the template repository
4. Contact the development team for assistance

---

**Migration complete?** Your project now uses the generic template system while maintaining your specific workflows and configurations!