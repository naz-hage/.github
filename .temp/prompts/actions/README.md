# Action Prompts

This directory contains specific, actionable prompts for executing individual development actions using the SDO CLI tool. These are the technical implementation details that complement the high-level workflow guides in the `workflows/` directory.

## Overview

While the `workflows/` directory contains comprehensive process guides (when, why, and prerequisites), the `actions/` directory provides the specific commands, file formats, and step-by-step instructions for executing individual actions.

## Action Prompts

### Issue Management
- **[create-issue.md](create-issue.md)** - Create issues in Azure DevOps, GitHub, or Jira
  - File format for issue creation
  - SDO CLI commands for issue creation
  - Branch naming conventions
  - Post-creation workflow integration

### PR Creation
- **[create-pr.md](create-pr.md)** - Create pull requests for code changes
  - Uses repository's standard PR template (`.github/PULL_REQUEST_TEMPLATE/pull_request_template.md`)
  - SDO CLI commands for PR creation
  - Work item linking and branch management
  - Files: `<issue-number>-pr-message.md` (e.g., `123-pr-message.md`)
  - Post-creation validation steps

## Relationship to Workflows

These action prompts are referenced by the workflow guides:

```
Workflow Level (High-level process)
├── PBI Creation Workflow
│   └── create-issue.md (specific tool commands)
├── Task Creation Workflow
│   └── create-issue.md (specific tool commands)
├── Code Review Workflow
│   └── create-pr.md (specific tool commands)
└── Task Implementation Workflow
    └── create-pr.md (when task is ready for review)
```

## File Format Standards

All action prompts follow consistent formatting:

### Issue Creation Format
```markdown
# [issue-number]: Issue Title

## Target: <github|azure>
## Repository: <owner/repo>
## Assignee: <username or leave blank>
## Labels: <comma-separated labels>

## Description
<Detailed description>

## Acceptance Criteria
- [ ] <Criteria 1>
- [ ] <Criteria 2>
```

### PR Creation Format
Uses the repository's standard PR template located at:
- **GitHub**: `.github/PULL_REQUEST_TEMPLATE/pull_request_template.md`
- **Azure DevOps**: Repository's configured PR template

**Process:**
1. Copy the standard template to `.temp/<issue-number>-pr-message.md`
2. Fill out the template sections with PR-specific details
3. Use SDO CLI to create the PR

**File Naming:** `<issue-number>-pr-message.md` (e.g., `123-pr-message.md` for issue #123)

## Tool Integration

All actions use the **SDO CLI tool** as the primary interface:

```bash
# Issue creation
sdo issue create --file .temp/issue-message.md

# PR creation
sdo pr create --file .temp/pr-message.md --work-item <id>
```

## Best Practices

1. **Use temp files**: Always create action files in `.temp/` directory from repo root
2. **Follow naming conventions**: Use descriptive, consistent file names
   - Issue files: `issue-message.md`
   - PR files: `<issue-number>-pr-message.md` (e.g., `123-pr-message.md`)
3. **Link work items**: Always link issues/PRs to relevant work items
4. **Clean up**: Remove temp files after successful creation (optional)
5. **Validate**: Check creation results and update references

## Related Documentation

- [Workflow Guides](../workflows/README.md) - High-level process documentation
- [Configuration](../CONFIG_USAGE.md) - Tool and platform configuration
- [Copilot Instructions](../../copilot-instructions.md) - AI-assisted development guidelines</content>
<parameter name="filePath">c:\source\.github\.temp\prompts\actions\README.md