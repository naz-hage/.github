# Action Prompts

This directory contains specific, actionable prompts for executing individual development actions using the SDO CLI tool. These are the technical implementation details that complement the high-level workflow guides in the `workflows/` directory.

## Overview

While the `workflows/` directory contains comprehensive process guides (when, why, and prerequisites), the `actions/` directory provides the specific commands, file formats, and step-by-step instructions for executing individual actions.

## Action Prompts

### Work Item Management
- **[create-workitem.md](create-workitem.md)** - Create work items (Issues, PBIs, Tasks) in Azure DevOps or GitHub
  - File formats for different work item types
  - SDO CLI commands for work item creation
  - Platform-specific handling
  - Post-creation workflow integration

- **[start-workitem.md](start-workitem.md)** - Start work on tasks or PBIs
  - Branch creation and naming conventions
  - Linking to work items
  - Local environment setup
  - Integration with version control

- **[close-workitem.md](close-workitem.md)** - Complete and close work items
  - Work item validation and completion criteria
  - Cleanup procedures
  - Documentation and status updates
  - Closure workflows for Tasks and PBIs

### PR Management
- **[create-pr.md](create-pr.md)** - Create pull requests for code changes
  - Uses repository's standard PR template (`.github/PULL_REQUEST_TEMPLATE/pull_request_template.md`)
  - SDO CLI commands for PR creation
  - Work item linking and branch management
  - Files: `<issue-number>-pr-message.md` (e.g., `123-pr-message.md`)
  - Post-creation validation steps

- **[pr-squash-merge.md](pr-squash-merge.md)** - Squash merge pull requests
  - PR merge strategies
  - Branch cleanup after merge
  - Commit message conventions
  - Post-merge verification

## Relationship to Workflows

These action prompts are referenced by the workflow guides:

```
Workflow Level (High-level process)
├── PBI Creation Workflow
│   └── create-workitem.md (specific tool commands)
├── Task Creation Workflow
│   └── create-workitem.md (specific tool commands)
├── Task Start Workflow
│   └── start-workitem.md (branch and environment setup)
├── Code Review Workflow
│   ├── create-pr.md (create pull request)
│   └── pr-squash-merge.md (merge after review)
├── Task Completion Workflow
│   └── close-workitem.md (final closure)
└── PBI Closure Workflow
    └── close-workitem.md (PBI completion)
```

## File Format Standards

See [templates/](../templates/) for detailed formatting examples and standards:

- **Azure DevOps Work Items**: `issue-azdo-*.md` examples (PBI, Task, Bug, Epic)
- **GitHub Issues**: `issue-gh-example.md`
- **Pull Request Templates**: See `.github/PULL_REQUEST_TEMPLATE/`

## Tool Integration

All actions use the **SDO CLI tool** as the primary interface:

```bash
# Issue creation
sdo workitem create --file-path .temp/issue-message.md

# PR creation
sdo pr create --file .temp/pr-message.md --work-item <id>
```

## Best Practices

For detailed guidance on implementing actions, refer to the individual action files:
- Each action file contains step-by-step commands and workflows
- Use files in `.temp/` directory for temporary work item and PR files
- Always link work items and PRs to relevant tracking items
- Follow naming conventions documented in each action file

## Related Documentation

- [Workflow Guides](../workflows/README.md) - High-level process documentation
- [Quick Start Guide](../../../setup-guides/quick-start-guide.md) - Complete setup and configuration guide
- [Copilot Instructions](../../copilot-instructions.md) - AI-assisted development guidelines</content>
<parameter name="filePath">c:\source\.github\.temp\prompts\actions\README.md