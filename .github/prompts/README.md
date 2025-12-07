# Copilot Prompts and Instructions

This directory contains structured prompts and instructions to guide Copilot (GitHub Copilot) in providing high-quality assistance for development work in this repository.

## 🎯 Project-Agnostic Workflows

All workflows in this directory are **project-agnostic** and reference **`project-config.yaml`** for project-specific settings. This design enables easy transfer to other projects.

**Key Files:**
- **`../project-config.yaml`** - Project-specific configuration (organization, project, tools, paths)
- **`platform-mapping.md`** - Standardized term mappings between SDO, Azure DevOps, and GitHub
- **`../copilot-instructions.md`** - Project-specific development guidelines

## Directory Structure

```
.github/prompts/
├── README.md                    # This file - overview and usage guide
├── platform-mapping.md          # Standardized term mappings (SDO/AzDO/GitHub)
├── workflows/                   # Workflow-specific prompts (project-agnostic)
│   ├── workitem-creation.md # Creating PBIs and Tasks (portfolio and sprint level)
│   ├── workitem-closure.md      # Work item completion and validation (Tasks, PBIs, Issues)
│   ├── workitem-start.md        # Complete work item start workflow (Tasks and PBIs)
│   ├── pbi-breakdown.md        # Breaking PBIs into implementable tasks
│   ├── code-review.md          # Code review and PR processes
│   ├── pr-squash-merge.md      # PR squash merge process guidance
│   └── testing.md              # Testing workflow and validation
├── actions/                     # Action-specific prompts (tool commands)
│   ├── README.md               # Action prompts overview
│   ├── create-issue.md         # Create issues in Azure DevOps/GitHub/Jira
│   └── create-pr.md            # Create pull requests for code changes
└── templates/                   # Reusable prompt templates
    └── pull_request_template.md # GitHub PR template for SDO development
```

## Directory Purposes

### Workflows Directory
High-level guidance for development processes covering the complete issue lifecycle:
- **Work Item Creation**: Creating PBIs and Tasks with business value and acceptance criteria
- **PBI Breakdown**: Breaking committed PBIs into implementable Tasks for sprint planning
- **Task Implementation**: Step-by-step coding, testing, and validation workflow (one task at a time)
- **Task Closure**: Task completion validation and cleanup
- **PBI Closure**: PBI completion validation, testing, and stakeholder approval
- **Code Review**: Preparing pull requests and conducting thorough reviews
- **Testing**: Unit testing, integration testing, and CI/CD validation

### Actions Directory
Specific, actionable prompts for executing individual development actions using CLI tools:
- **Issue Creation**: Step-by-step instructions for creating issues in Azure DevOps, GitHub, or Jira
- **PR Creation**: Detailed commands and file formats for creating pull requests with proper linking

### Templates Directory
Reusable prompt templates with detailed step-by-step instructions for particular tools and workflows. These contain:
- **Tool-specific guides**: Instructions for `sdo` CLI commands, PowerShell scripts, etc.
- **Detailed workflows**: Step-by-step processes for specific scenarios
- **Project-specific context**: References to Proto Azure DevOps project and local tooling

## Complete Issue Lifecycle Coverage

This prompt system provides comprehensive guidance for the **entire software development lifecycle**:

```
Work Item Creation → PBI Breakdown → PBI Implementation → Task Implementation → Code Review → Testing → PBI Closure
     ↓                     ↓                ↓                 ↓            ↓         ↓            ↓
workflows/            workflows/       workflows/       workflows/        workflows/ workflows/  workflows/
workitem-creation     pbi-breakdown    pbi-implementation task-implementation code-review testing    pbi-closure
     ↓                     ↓                ↓                 ↓            ↓         ↓            ↓
 actions/              actions/        actions/         actions/       actions/   actions/     actions/
create-workitem       create-workitem create-workitem  create-pr      create-pr  create-pr    create-pr
```

Each phase includes:
- **Clear objectives** and success criteria
- **Step-by-step processes** with validation checkpoints
- **Error handling** and recovery procedures
- **Integration points** with other workflows
- **Quality gates** and acceptance criteria

## How to Use These Prompts

### For Developers
1. **Before starting work**: Review the relevant workflow prompt in the `workflows/` directory
2. **When stuck**: Use templates from the `templates/` directory as starting points

### For Copilot
These prompts are designed to be referenced in your Copilot chat or used as context. For example:
- "Follow the guidelines in `.github/prompts/workflows/implementation.md"`

## Workflow Integration

These prompts integrate with our Azure DevOps workflow:
- **PBIs** define high-level features and requirements
- **Tasks** break down PBIs into implementable units
- **Prompts** guide the implementation of each Task

## Contributing

When adding new prompts:
1. Place them in the appropriate subdirectory
2. Follow the naming convention: `kebab-case.md`
3. Include clear descriptions and examples
4. Update this README if adding new subdirectories

## Best Practices

- **Be specific**: Prompts work best when they provide clear, specific guidance
- **Include context**: Reference repository standards, technologies, and conventions
- **Show examples**: Include before/after examples whenever possible
- **Keep updated**: Review and update prompts as the repository evolves

## Related Files

- `.github/copilot-instructions.md` - General Copilot instructions for this repository
- `README.md` - Main repository documentation