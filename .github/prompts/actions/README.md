# Action Prompts

This directory contains specific, actionable prompts for executing individual development actions using the SDO CLI tool. These are the technical implementation details that complement the high-level workflow guides in the `workflows/` directory.

## Overview

While the `workflows/` directory contains comprehensive process guides (when, why, and prerequisites), the `actions/` directory provides the specific commands, file formats, and step-by-step instructions for executing individual actions.

## Action Prompts

### Work Item Management
- **[create-wi.md](create-wi.md)** - Create work items for `sdo wi create` command
  - Single `.temp/wi.md` file format
  - Requires `.temp/sdo-config.yaml` for platform and type configuration
  - SDO CLI integration for work item creation

### PR Management
- **[update-pr.md](update-pr.md)** - Update PR message template with branch changes
  - Updates existing `.temp/<issue-number>-pr-message.md` template (created by `sdo wi start`)
  - Preserves template structure while filling sections
  - Updates: Title, Description, Changes, Why
  - Ready for `sdo pr create` submission

- **[pr-squash-merge.md](pr-squash-merge.md)** - Squash merge pull requests
  - PR merge strategies
  - Branch cleanup after merge
  - Commit message conventions
  - Post-merge verification

## Relationship to Workflows

These action prompts are referenced by the workflow guides:

```
Workflow Level (High-level process)
├── Work Item Creation
│   └── create-wi.md (sdo wi create)
└── PR Update and Creation
    ├── update-pr.md (update template)
    └── sdo pr create (submit PR)
```

## File Format Standards

See [templates/](../templates/) for detailed formatting examples and standards:

- **Azure DevOps Work Items**: `issue-azdo-*.md` examples (PBI, Task, Bug, Epic)
- **GitHub Issues**: `issue-gh-example.md`
- **Pull Request Templates**: See `.github/PULL_REQUEST_TEMPLATE/`

## Tool Integration

All actions use the **SDO CLI tool** as the primary interface:

```bash
# Work item creation
sdo wi create

# PR update and creation workflow
sdo wi start
sdo pr create
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